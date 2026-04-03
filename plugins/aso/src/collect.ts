import { readFileSync, writeFileSync, readdirSync } from "fs";
import { resolve, join } from "path";
import { lookupApp, collectKeywordRankings } from "./itunes.js";
import { getKeywordPopularity } from "./searchads.js";
import type { AppMeta } from "./itunes.js";

const ROOT = resolve(import.meta.dirname, "..");
const DATA_DIR = process.env.ASO_DATA_PATH ?? join(ROOT, "data");

export interface Config {
  myAppId: string;
  competitors: { name: string; id: string }[];
  keywords: string[];
  country: string;
}

export interface Snapshot {
  timestamp: string;
  keywords: Record<
    string,
    {
      popularity: number | null;
      rankings: Record<string, number | null>;
    }
  >;
  apps: Record<string, AppMeta>;
}

export function loadConfig(): Config {
  const configPath = process.env.ASO_CONFIG_PATH;
  if (!configPath) {
    throw new Error(
      "ASO_CONFIG_PATH is not set. Run /aso-config to configure the plugin."
    );
  }
  return JSON.parse(readFileSync(configPath, "utf8")) as Config;
}

export function loadLatestSnapshot(): Snapshot | null {
  const files = readdirSync(DATA_DIR)
    .filter((f) => f.endsWith(".json"))
    .sort();
  if (files.length === 0) return null;
  return JSON.parse(readFileSync(join(DATA_DIR, files[files.length - 1]), "utf8")) as Snapshot;
}

export function loadSnapshotBefore(daysAgo: number): Snapshot | null {
  const files = readdirSync(DATA_DIR)
    .filter((f) => f.endsWith(".json"))
    .sort();
  if (files.length < daysAgo + 1) return files.length > 1 ? JSON.parse(readFileSync(join(DATA_DIR, files[0]), "utf8")) as Snapshot : null;
  return JSON.parse(readFileSync(join(DATA_DIR, files[files.length - 1 - daysAgo]), "utf8")) as Snapshot;
}

export async function collect(): Promise<Snapshot> {
  const config = loadConfig();
  const allIds = [config.myAppId, ...config.competitors.map((c) => c.id)];

  console.log(`Fetching metadata for ${allIds.length} apps...`);
  const appMetas: Record<string, AppMeta> = {};
  for (const id of allIds) {
    const meta = await lookupApp(id, config.country);
    if (meta) appMetas[id] = meta;
    else console.warn(`  App ${id} not found`);
  }

  console.log(`Fetching rankings for ${config.keywords.length} keywords...`);
  const keywordResults = await collectKeywordRankings(config.keywords, allIds, config.country);

  console.log(`Fetching keyword popularity from Search Ads...`);
  let popularityMap: Record<string, number | null> = {};
  try {
    const pop = await getKeywordPopularity(config.keywords, config.country);
    for (const p of pop) popularityMap[p.keyword] = p.popularity;
  } catch (e) {
    console.warn("  Search Ads auth not configured, skipping popularity scores.");
  }

  const snapshot: Snapshot = {
    timestamp: new Date().toISOString(),
    keywords: {},
    apps: appMetas,
  };

  for (const result of keywordResults) {
    snapshot.keywords[result.keyword] = {
      popularity: popularityMap[result.keyword] ?? null,
      rankings: result.rankings,
    };
  }

  const filename = snapshot.timestamp.replace(/[:.]/g, "-").slice(0, 16) + ".json";
  const outPath = join(DATA_DIR, filename);
  writeFileSync(outPath, JSON.stringify(snapshot, null, 2));
  console.log(`Saved snapshot: ${filename}`);

  return snapshot;
}

// Allow running directly: npx tsx src/collect.ts
if (process.argv[1]?.endsWith("collect.ts") || process.argv[1]?.endsWith("collect.js")) {
  collect().catch(console.error);
}
