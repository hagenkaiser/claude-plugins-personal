#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Installing ASO plugin dependencies..."
npm install

mkdir -p data

echo ""
echo "Setup complete! Next steps:"
echo "  1. In Claude Code, run: /plugin install $(pwd)"
echo "  2. Run /aso-config to set your app IDs, competitors, and keywords"
echo "  3. (Optional) Set Search Ads env vars: SEARCH_ADS_KEY_PATH, SEARCH_ADS_CLIENT_ID, SEARCH_ADS_TEAM_ID"
