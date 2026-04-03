# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Installation

### As a Claude Code Plugin (recommended)
1. `npm run setup` — installs dependencies
2. In Claude Code: `/plugin install /path/to/aso`
3. On first session, run `/aso-config` to set your app IDs, competitors, keywords, and country

### Legacy (manual registration)
1. `npm install`
2. Set `ASO_CONFIG_PATH` and `ASO_DATA_PATH` env vars (or config is read from env)
3. Add MCP server entry to your `.claude/settings.json` manually

### Updating
After changing skills or server code, run `/reload-plugins` in Claude Code to pick up changes.

## Commands

- `npm run setup` — First-time setup (install deps)
- `npm start` — Run the MCP server (stdio transport)
- `npm run collect` — Collect a fresh data snapshot (saved to `data/`)

No build step required — the project runs directly via `tsx`.

## Architecture

This is a Claude Code plugin providing an MCP server for App Store Optimization (ASO) intelligence. It serves live App Store data to Claude through 5 tools and powers 28 interactive skills in `skills/`.

### Data Flow

1. Claude skill (e.g. `/aso-audit`) triggers MCP tool calls
2. `server.ts` dispatches to collection/analysis functions
3. `itunes.ts` and `searchads.ts` fetch from Apple APIs
4. `analyze.ts` formats results as text tables and diffs
5. `collect.ts` persists timestamped JSON snapshots to `data/`

### Source Files (`src/`)

| File | Role |
|------|------|
| `server.ts` | MCP server entry point — registers all 5 tools, stdio transport |
| `collect.ts` | Data collection pipeline, snapshot persistence, Config/Snapshot interfaces |
| `analyze.ts` | Ranking table formatting, snapshot comparison/diffing |
| `itunes.ts` | iTunes Search API client (app metadata, keyword rankings, 3s rate limit) |
| `searchads.ts` | Apple Search Ads API client (OAuth2 JWT/ES256, keyword popularity 0-5) |

### MCP Tools

- `collect_data` — Fetch fresh data and save snapshot
- `get_rankings` — Current keyword positions
- `get_keyword_popularity` — Search Ads popularity scores
- `get_app_metadata` — Side-by-side metadata comparison
- `compare_snapshots` — Diff two snapshots (accepts optional `daysAgo`)

### Skills

Skills live in `skills/` (plugin format: `skills/<name>/SKILL.md`) and fall into two categories:
- **Data-enhanced** (call MCP tools): `/aso-audit`, `/keyword-research`, `/competitor-analysis`, `/metadata-optimization`, etc.
- **Framework** (methodology only): `/screenshot-optimization`, `/localization`, `/app-launch`, etc.

The `/app-marketing-context` skill is foundational — it creates a reference document used by other skills.

## Configuration

- **Plugin config** is stored in `${CLAUDE_PLUGIN_DATA}/config.json` (persists across plugin updates)
  - Run `/aso-config` to set or update your app IDs, competitors, keywords, and country
  - The MCP server reads config from the `ASO_CONFIG_PATH` env var (set automatically by the plugin)
- **Data snapshots** are stored in `${CLAUDE_PLUGIN_DATA}/data/` (via `ASO_DATA_PATH` env var)
- **Search Ads env vars** (optional, gracefully degrades without them):
  - `SEARCH_ADS_KEY_PATH` — Path to `.p8` private key
  - `SEARCH_ADS_CLIENT_ID` — OAuth client ID
  - `SEARCH_ADS_TEAM_ID` — Apple Team ID

## Conventions

- ES modules (`"type": "module"`) with strict TypeScript
- No test framework currently configured
- Secrets (`.env`, `certs/`, `*.p8`) are gitignored
- iTunes API has a 3-second delay between requests to respect rate limits
