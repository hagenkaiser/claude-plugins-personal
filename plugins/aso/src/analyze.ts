import type { Snapshot } from "./collect.js";

export function formatRankingTable(snapshot: Snapshot): string {
  const appIds = Object.keys(snapshot.apps);
  const appNames = Object.fromEntries(appIds.map((id) => [id, snapshot.apps[id].trackName]));

  const header = ["Keyword", "Pop", ...appIds.map((id) => appNames[id])].join("\t");
  const divider = "─".repeat(header.length);

  const rows = Object.entries(snapshot.keywords).map(([kw, data]) => {
    const pop = data.popularity != null ? String(data.popularity) : "?";
    const positions = appIds.map((id) => {
      const pos = data.rankings[id];
      return pos != null ? `#${pos}` : "—";
    });
    return [kw, pop, ...positions].join("\t");
  });

  return [header, divider, ...rows].join("\n");
}

export interface SnapshotDiff {
  timestamp: { from: string; to: string };
  rankingChanges: {
    keyword: string;
    appId: string;
    appName: string;
    before: number | null;
    after: number | null;
    delta: number | null;
  }[];
  metadataChanges: {
    appId: string;
    appName: string;
    field: string;
    before: unknown;
    after: unknown;
  }[];
}

export function diffSnapshots(before: Snapshot, after: Snapshot): SnapshotDiff {
  const rankingChanges: SnapshotDiff["rankingChanges"] = [];
  const metadataChanges: SnapshotDiff["metadataChanges"] = [];

  // Keyword ranking diffs
  for (const [kw, afterData] of Object.entries(after.keywords)) {
    const beforeData = before.keywords[kw];
    for (const [appId, afterPos] of Object.entries(afterData.rankings)) {
      const beforePos = beforeData?.rankings[appId] ?? null;
      if (beforePos !== afterPos) {
        const delta =
          beforePos != null && afterPos != null ? beforePos - afterPos : null; // positive = improved
        rankingChanges.push({
          keyword: kw,
          appId,
          appName: after.apps[appId]?.trackName ?? appId,
          before: beforePos,
          after: afterPos,
          delta,
        });
      }
    }
  }

  // App metadata diffs
  const fields = ["trackName", "price", "averageUserRating", "userRatingCount", "version"] as const;
  for (const [appId, afterApp] of Object.entries(after.apps)) {
    const beforeApp = before.apps[appId];
    if (!beforeApp) continue;
    for (const field of fields) {
      if (beforeApp[field] !== afterApp[field]) {
        metadataChanges.push({
          appId,
          appName: afterApp.trackName,
          field,
          before: beforeApp[field],
          after: afterApp[field],
        });
      }
    }
  }

  return {
    timestamp: { from: before.timestamp, to: after.timestamp },
    rankingChanges,
    metadataChanges,
  };
}

export function formatDiff(diff: SnapshotDiff): string {
  const lines: string[] = [`Comparison: ${diff.timestamp.from} → ${diff.timestamp.to}`, ""];

  if (diff.rankingChanges.length === 0 && diff.metadataChanges.length === 0) {
    lines.push("No changes detected.");
    return lines.join("\n");
  }

  if (diff.rankingChanges.length > 0) {
    lines.push("## Ranking Changes");
    for (const c of diff.rankingChanges) {
      const before = c.before != null ? `#${c.before}` : "unranked";
      const after = c.after != null ? `#${c.after}` : "unranked";
      const arrow = c.delta != null ? (c.delta > 0 ? `▲${c.delta}` : `▼${Math.abs(c.delta)}`) : "";
      lines.push(`  ${c.keyword} | ${c.appName}: ${before} → ${after} ${arrow}`);
    }
    lines.push("");
  }

  if (diff.metadataChanges.length > 0) {
    lines.push("## Metadata Changes");
    for (const c of diff.metadataChanges) {
      lines.push(`  ${c.appName} | ${c.field}: ${c.before} → ${c.after}`);
    }
  }

  return lines.join("\n");
}
