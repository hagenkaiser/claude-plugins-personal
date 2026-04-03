# ASO Intelligence

An MCP (Model Context Protocol) server that brings real App Store data directly into Claude — plus 28 ASO methodology skills for a complete App Store Optimization workflow.

Ask Claude to run an ASO audit, research keywords, track competitors, or optimize metadata, and it pulls live data from the App Store and Apple Search Ads automatically.

---

## What It Does

**Tracks** keyword rankings across your app and competitors, updated on demand.

**Measures** Apple Search Ads keyword popularity scores (0–5) directly from Apple's API.

**Compares** snapshots over time to surface ranking movements, metadata changes, and rating shifts.

**Guides** every ASO decision with 28 built-in skills — from keyword research to UA campaigns to subscription lifecycle optimization.

---

## MCP Tools

Five tools are available to Claude through the MCP server:

| Tool | Description |
|------|-------------|
| `collect_data` | Fetch fresh App Store data for all tracked apps and keywords. Saves a timestamped snapshot. |
| `get_rankings` | Show the latest keyword ranking table — positions for each tracked app per keyword. |
| `get_keyword_popularity` | Show Apple Search Ads popularity scores (0–5) for all tracked keywords. |
| `get_app_metadata` | Side-by-side metadata comparison — name, rating, price, version, update date, category. |
| `compare_snapshots` | Diff two snapshots to see ranking changes, rating shifts, and metadata updates. |

---

## Skills

28 ASO skills live in `skills/`. When installed as a plugin, Claude picks them up automatically.

**Data-enhanced** — these skills call MCP tools to pull live data before analyzing:

| Skill | MCP Tools Used |
|-------|---------------|
| `/aso-audit` | `get_rankings` · `get_keyword_popularity` · `get_app_metadata` |
| `/keyword-research` | `get_keyword_popularity` · `get_rankings` |
| `/competitor-analysis` | `get_rankings` · `get_app_metadata` · `compare_snapshots` |
| `/competitor-tracking` | `compare_snapshots` |
| `/metadata-optimization` | `get_app_metadata` · `get_rankings` |
| `/market-pulse` | `get_rankings` · `compare_snapshots` · `get_keyword_popularity` |
| `/market-movers` | `compare_snapshots` |
| `/seasonal-aso` | `get_keyword_popularity` |
| `/apple-search-ads` | `get_keyword_popularity` · `get_rankings` |

**Framework skills** — methodology and frameworks, no live data required:

`/screenshot-optimization` · `/rating-prompt-strategy` · `/review-management` · `/monetization-strategy` · `/subscription-lifecycle` · `/onboarding-optimization` · `/app-store-featured` · `/in-app-events` · `/ab-test-store-listing` · `/app-launch` · `/localization` · `/retention-optimization` · `/ua-campaign` · `/press-and-pr` · `/app-clips` · `/crash-analytics` · `/app-analytics` · `/app-icon-optimization` · `/app-marketing-context`

---

## Setup

### 1. Install dependencies

```bash
npm run setup
```

### 2. Install as a Claude Code plugin

```
/plugin install /path/to/aso
```

This registers the MCP server and all 28 skills automatically.

### 3. Configure your apps and keywords

On your first session after installing, run:

```
/aso-config
```

Claude will ask for your app ID, competitors, keywords, and country code. The config is saved to the plugin's persistent data directory and survives plugin updates.

App IDs are the numeric IDs from App Store URLs: `apps.apple.com/app/id123456789`

### 4. (Optional) Apple Search Ads API for keyword popularity

Without this, popularity scores show as `?`. To enable:

1. In your Apple Search Ads account: **Settings → API → Create API Certificate**
2. Download the `.p8` private key, note your Client ID and Team ID
3. Set environment variables:

```bash
export SEARCH_ADS_KEY_PATH=/path/to/key.p8
export SEARCH_ADS_CLIENT_ID=SEARCHADS.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
export SEARCH_ADS_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

<details>
<summary>Legacy: manual MCP registration</summary>

If you prefer not to use the plugin system, add to your `.claude/settings.json` or `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aso": {
      "command": "npx",
      "args": ["tsx", "/absolute/path/to/aso/src/server.ts"],
      "env": {
        "ASO_CONFIG_PATH": "/path/to/your/config.json",
        "ASO_DATA_PATH": "/path/to/your/data/dir"
      }
    }
  }
}
```
</details>

### 5. Collect your first snapshot

Either ask Claude to `collect_data`, or run directly:

```bash
npm run collect
```

Snapshots are saved to `data/` as timestamped JSON files. Run this daily or weekly to build up a history for trend analysis.

### Updating

After changing skills or server code, run `/reload-plugins` in Claude Code to pick up changes without restarting your session.

---

## Usage

Once the MCP server is connected, just talk to Claude:

```
/aso-audit
```
> Claude calls get_rankings, get_keyword_popularity, and get_app_metadata, then produces a scored audit across 10 factors with prioritized action items.

```
/competitor-tracking
```
> Claude calls compare_snapshots and produces a weekly change report — ranking shifts, metadata updates, and competitive opportunities.

```
/keyword-research
```
> Claude pulls popularity scores and ranking data, then outputs a keyword opportunity table with placement recommendations.

```
/screenshot-optimization
```
> No data needed — Claude walks through the screenshot strategy framework for your app.

---

## Data & Privacy

- All data is fetched from public App Store APIs (iTunes Search API) and the Apple Search Ads API using your own credentials
- Snapshots are stored locally in `data/` — excluded from git by default
- No data is sent to any third-party service

---

## Project Structure

```
aso/
├── src/
│   ├── server.ts        # MCP server — registers all 5 tools
│   ├── collect.ts       # Data collection + snapshot storage
│   ├── analyze.ts       # Ranking table formatting + snapshot diffing
│   ├── itunes.ts        # iTunes Search API client
│   └── searchads.ts     # Apple Search Ads API client
├── .claude-plugin/
│   └── plugin.json      # Claude Code plugin manifest
├── skills/              # 28 ASO skills (plugin format)
│   ├── aso-audit/SKILL.md
│   ├── keyword-research/SKILL.md
│   └── ...
├── data/                # Snapshots (gitignored)
├── certs/               # Search Ads keys (gitignored)
├── .mcp.json            # MCP server config (auto-loaded by plugin)
└── config.example.json  # Reference for config JSON shape
```
