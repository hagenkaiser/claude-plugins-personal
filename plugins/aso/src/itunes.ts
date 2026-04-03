const BASE = "https://itunes.apple.com";
const DELAY_MS = 3000; // ~20 req/min safe rate

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export interface AppMeta {
  trackId: string;
  trackName: string;
  sellerName: string;
  price: number;
  formattedPrice: string;
  averageUserRating: number;
  userRatingCount: number;
  primaryGenreName: string;
  version: string;
  currentVersionReleaseDate: string;
  description: string;
}

export async function lookupApp(id: string, country = "us"): Promise<AppMeta | null> {
  const url = `${BASE}/lookup?id=${id}&country=${country}&entity=software`;
  const res = await fetch(url);
  const json = (await res.json()) as { resultCount: number; results: Record<string, unknown>[] };
  if (json.resultCount === 0) return null;
  const r = json.results[0];
  return {
    trackId: String(r.trackId),
    trackName: String(r.trackName ?? ""),
    sellerName: String(r.sellerName ?? ""),
    price: Number(r.price ?? 0),
    formattedPrice: String(r.formattedPrice ?? "Free"),
    averageUserRating: Number(r.averageUserRating ?? 0),
    userRatingCount: Number(r.userRatingCount ?? 0),
    primaryGenreName: String(r.primaryGenreName ?? ""),
    version: String(r.version ?? ""),
    currentVersionReleaseDate: String(r.currentVersionReleaseDate ?? ""),
    description: String(r.description ?? ""),
  };
}

export interface SearchResult {
  keyword: string;
  // appId -> 1-based position, or null if not in top results
  rankings: Record<string, number | null>;
}

export async function searchKeyword(
  keyword: string,
  trackedIds: string[],
  country = "us",
  limit = 50
): Promise<SearchResult> {
  const url = `${BASE}/search?term=${encodeURIComponent(keyword)}&entity=software&country=${country}&limit=${limit}`;
  const res = await fetch(url);
  const json = (await res.json()) as { results: { trackId: number }[] };

  const rankings: Record<string, number | null> = {};
  for (const id of trackedIds) rankings[id] = null;

  json.results.forEach((app, idx) => {
    const id = String(app.trackId);
    if (trackedIds.includes(id)) rankings[id] = idx + 1;
  });

  return { keyword, rankings };
}

export async function collectKeywordRankings(
  keywords: string[],
  trackedIds: string[],
  country = "us"
): Promise<SearchResult[]> {
  const results: SearchResult[] = [];
  for (const kw of keywords) {
    results.push(await searchKeyword(kw, trackedIds, country));
    await sleep(DELAY_MS);
  }
  return results;
}
