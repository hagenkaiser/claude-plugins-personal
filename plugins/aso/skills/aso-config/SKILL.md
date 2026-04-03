---
name: aso-config
description: Configure the ASO plugin — set your app ID, competitors, keywords, and country
type: user-invocable
---

## Purpose

Set up or update the ASO plugin configuration. The config is saved to `$ASO_CONFIG_PATH` so it persists across sessions and plugin updates.

## Workflow

1. **Check for existing config:** Read the file at the `ASO_CONFIG_PATH` environment variable path. If it exists, show the current values to the user.

2. **Collect values from the user.** Ask for each field:
   - **App ID** — The user's App Store app ID (numeric, e.g. `1234567890`)
   - **Competitors** — A list of competitor apps, each with a name and App Store ID
   - **Keywords** — A list of keywords to track rankings for
   - **Country** — Two-letter country code (default: `us`)

   If updating an existing config, only ask about fields the user wants to change.

3. **Write the config file** to the path in `ASO_CONFIG_PATH`. The JSON format is:

```json
{
  "myAppId": "1234567890",
  "competitors": [
    { "name": "Competitor A", "id": "1111111111" },
    { "name": "Competitor B", "id": "2222222222" }
  ],
  "keywords": ["keyword one", "keyword two", "keyword three"],
  "country": "us"
}
```

4. **Search Ads API keys (optional).** Ask the user if they want to set up Apple Search Ads for keyword popularity data. If yes, walk them through it:

   - Go to [Search Ads UI](https://searchads.apple.com) → Settings → API → Create API Certificate
   - Download the `.p8` private key file and save it somewhere safe (e.g. `~/.config/aso/key.p8`)
   - Note the **Client ID** (format: `SEARCHADS.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) and **Team ID** (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
   - These need to be set as environment variables so the MCP server can use them. Guide the user to add them to their shell profile (`~/.zshrc` or `~/.bashrc`):
     ```
     export SEARCH_ADS_KEY_PATH=/path/to/key.p8
     export SEARCH_ADS_CLIENT_ID=SEARCHADS.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     export SEARCH_ADS_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     ```
   - Remind them to restart Claude Code (or `source ~/.zshrc`) for the vars to take effect
   - Reference: [Apple docs — Implementing OAuth for the Search Ads API](https://developer.apple.com/documentation/apple_ads/implementing_oauth_for_the_apple_search_ads_api)

   If the user declines, let them know keyword popularity data won't be available but everything else works fine.

5. **Confirm** that the config was saved and suggest running `/aso-audit` or `/keyword-research` to get started.
