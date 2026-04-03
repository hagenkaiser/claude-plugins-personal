import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { collect, loadLatestSnapshot, loadSnapshotBefore, loadConfig } from "./collect.js";
import { formatRankingTable, diffSnapshots, formatDiff } from "./analyze.js";

const server = new McpServer({
  name: "aso-competitor-analysis",
  version: "1.0.0",
});

// Tool: collect fresh data
server.registerTool(
  "collect_data",
  {
    description:
      "Fetch fresh App Store data for all tracked apps and keywords. Saves a timestamped snapshot. This takes a few minutes due to API rate limits.",
    inputSchema: {},
  },
  async () => {
    const snapshot = await collect();
    const config = loadConfig();
    const allIds = [config.myAppId, ...config.competitors.map((c) => c.id)];
    const appCount = Object.keys(snapshot.apps).length;
    const kwCount = Object.keys(snapshot.keywords).length;
    return {
      content: [
        {
          type: "text",
          text: `Snapshot collected at ${snapshot.timestamp}\n- ${appCount}/${allIds.length} apps fetched\n- ${kwCount} keywords tracked\n\n${formatRankingTable(snapshot)}`,
        },
      ],
    };
  }
);

// Tool: get latest rankings
server.registerTool(
  "get_rankings",
  {
    description:
      "Show the latest keyword ranking table — which position each tracked app appears for each keyword, plus Apple Search Ads popularity score.",
    inputSchema: {},
  },
  async () => {
    const snapshot = loadLatestSnapshot();
    if (!snapshot) {
      return {
        content: [{ type: "text", text: "No snapshots found. Run collect_data first." }],
      };
    }
    return {
      content: [
        {
          type: "text",
          text: `Rankings as of ${snapshot.timestamp}\n\n${formatRankingTable(snapshot)}`,
        },
      ],
    };
  }
);

// Tool: compare snapshots
server.registerTool(
  "compare_snapshots",
  {
    description:
      "Compare the latest snapshot against a previous one to see ranking changes, metadata changes, price changes, and rating changes.",
    inputSchema: {
      daysAgo: z
        .number()
        .int()
        .min(1)
        .default(7)
        .describe("How many snapshots back to compare against (default: 7)"),
    },
  },
  async ({ daysAgo }) => {
    const latest = loadLatestSnapshot();
    if (!latest) {
      return { content: [{ type: "text", text: "No snapshots found. Run collect_data first." }] };
    }
    const before = loadSnapshotBefore(daysAgo ?? 7);
    if (!before) {
      return {
        content: [{ type: "text", text: "Not enough snapshots for comparison yet. Run collect_data more times." }],
      };
    }
    const diff = diffSnapshots(before, latest);
    return { content: [{ type: "text", text: formatDiff(diff) }] };
  }
);

// Tool: app metadata comparison
server.registerTool(
  "get_app_metadata",
  {
    description:
      "Show a side-by-side metadata comparison table for all tracked apps (my app + competitors) from the latest snapshot.",
    inputSchema: {},
  },
  async () => {
    const snapshot = loadLatestSnapshot();
    if (!snapshot) {
      return { content: [{ type: "text", text: "No snapshots found. Run collect_data first." }] };
    }
    const config = loadConfig();

    const appIds = [config.myAppId, ...config.competitors.map((c) => c.id)];
    const appLabels: Record<string, string> = { [config.myAppId]: "My App" };
    for (const c of config.competitors) appLabels[c.id] = c.name;

    const apps = appIds.map((id) => ({ id, label: appLabels[id] ?? id, meta: snapshot.apps[id] }));
    const available = apps.filter((a) => a.meta);

    if (available.length === 0) {
      return { content: [{ type: "text", text: "No app metadata in latest snapshot." }] };
    }

    const col = 18;
    const header = ["Field".padEnd(20), ...available.map((a) => a.label.substring(0, col).padEnd(col))].join(" | ");
    const sep = "-".repeat(header.length);

    const row = (label: string, vals: string[]) =>
      [label.padEnd(20), ...vals.map((v) => v.substring(0, col).padEnd(col))].join(" | ");

    const lines = [
      `App Metadata — ${snapshot.timestamp}`,
      "",
      header,
      sep,
      row("Name", available.map((a) => a.meta.trackName)),
      row("Seller", available.map((a) => a.meta.sellerName)),
      row("Rating", available.map((a) => `${a.meta.averageUserRating.toFixed(1)} (${a.meta.userRatingCount.toLocaleString()})`)),
      row("Price", available.map((a) => a.meta.formattedPrice)),
      row("Version", available.map((a) => a.meta.version)),
      row("Last Updated", available.map((a) => a.meta.currentVersionReleaseDate.slice(0, 10))),
      row("Category", available.map((a) => a.meta.primaryGenreName)),
    ];

    return { content: [{ type: "text", text: lines.join("\n") }] };
  }
);

// Tool: keyword popularity
server.registerTool(
  "get_keyword_popularity",
  {
    description:
      "Show Apple Search Ads popularity scores (0–5) for all tracked keywords from the latest snapshot.",
    inputSchema: {},
  },
  async () => {
    const snapshot = loadLatestSnapshot();
    if (!snapshot) {
      return { content: [{ type: "text", text: "No snapshots found. Run collect_data first." }] };
    }
    const lines = Object.entries(snapshot.keywords)
      .map(([kw, data]) => {
        const bar = data.popularity != null ? "█".repeat(data.popularity) + "░".repeat(5 - data.popularity) : "     ";
        return `${bar} ${data.popularity ?? "?"}/5  ${kw}`;
      })
      .sort((a, b) => b.localeCompare(a));

    return {
      content: [
        {
          type: "text",
          text: `Keyword Popularity (Apple Search Ads scores) — ${snapshot.timestamp}\n\n${lines.join("\n")}`,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
