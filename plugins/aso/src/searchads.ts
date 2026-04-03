import { readFileSync } from "fs";
import { createSign } from "crypto";

/**
 * Apple Search Ads API — keyword popularity scores.
 *
 * Setup:
 *   1. In your Search Ads account: Settings → API → Create API Certificate
 *   2. Download the .p8 private key and note the Client ID + Team ID
 *   3. Set env vars:
 *        SEARCH_ADS_KEY_PATH=/path/to/key.p8
 *        SEARCH_ADS_CLIENT_ID=SEARCHADS.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
 *        SEARCH_ADS_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
 *
 * Docs: https://developer.apple.com/documentation/apple_ads/implementing_oauth_for_the_apple_search_ads_api
 */

const API_BASE = "https://api.searchads.apple.com/api/v4";
const AUTH_URL = "https://appleid.apple.com/auth/oauth2/token";

let cachedToken: { token: string; expiresAt: number } | null = null;

function buildClientAssertion(): string {
  const keyPath = process.env.SEARCH_ADS_KEY_PATH;
  const clientId = process.env.SEARCH_ADS_CLIENT_ID;
  const teamId = process.env.SEARCH_ADS_TEAM_ID;

  if (!keyPath || !clientId || !teamId) {
    throw new Error(
      "Missing Search Ads env vars: SEARCH_ADS_KEY_PATH, SEARCH_ADS_CLIENT_ID, SEARCH_ADS_TEAM_ID"
    );
  }

  const privateKey = readFileSync(keyPath, "utf8");
  const now = Math.floor(Date.now() / 1000);

  const header = Buffer.from(JSON.stringify({ alg: "ES256", typ: "JWT" })).toString("base64url");
  const payload = Buffer.from(
    JSON.stringify({
      sub: clientId,
      aud: "https://appleid.apple.com",
      iat: now,
      exp: now + 180,
      iss: teamId,
    })
  ).toString("base64url");

  const data = `${header}.${payload}`;
  const sign = createSign("SHA256");
  sign.update(data);
  const signature = sign.sign(privateKey, "base64url");

  return `${data}.${signature}`;
}

async function getAccessToken(): Promise<string> {
  if (cachedToken && cachedToken.expiresAt > Date.now() + 5000) {
    return cachedToken.token;
  }

  const assertion = buildClientAssertion();
  const clientId = process.env.SEARCH_ADS_CLIENT_ID!;

  const res = await fetch(AUTH_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      client_id: clientId,
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: assertion,
      scope: "searchadsorg",
    }),
  });

  const json = (await res.json()) as { access_token: string; expires_in: number };
  cachedToken = {
    token: json.access_token,
    expiresAt: Date.now() + json.expires_in * 1000,
  };
  return cachedToken.token;
}

export interface KeywordPopularity {
  keyword: string;
  popularity: number | null; // 0–5 scale from Apple, null if unavailable
}

export async function getKeywordPopularity(
  keywords: string[],
  country = "us"
): Promise<KeywordPopularity[]> {
  const token = await getAccessToken();

  // Apple Search Ads API accepts up to 25 keywords per request
  const chunks: string[][] = [];
  for (let i = 0; i < keywords.length; i += 25) {
    chunks.push(keywords.slice(i, i + 25));
  }

  const results: KeywordPopularity[] = [];

  for (const chunk of chunks) {
    const res = await fetch(`${API_BASE}/keywords/search?storefront=${country.toUpperCase()}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ keywords: chunk }),
    });

    if (!res.ok) {
      // If auth not set up, return nulls gracefully
      for (const kw of chunk) results.push({ keyword: kw, popularity: null });
      continue;
    }

    const json = (await res.json()) as {
      data: { keyword: string; searchPopularity: number }[];
    };

    for (const item of json.data) {
      results.push({ keyword: item.keyword, popularity: item.searchPopularity ?? null });
    }
  }

  return results;
}
