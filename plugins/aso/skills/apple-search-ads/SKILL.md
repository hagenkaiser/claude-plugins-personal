---
name: apple-search-ads
description: Apple Search Ads strategy and optimization using real keyword popularity scores and ranking data to prioritize bids and campaign structure
type: user-invocable
---

## Data Collection (run before analysis)

Call these MCP tools to get live data:
- `get_keyword_popularity` — popularity scores (0–5) to calibrate bid priorities
- `get_rankings` — organic rankings to identify where ASA can amplify or cover gaps

If data seems stale, call `collect_data` first.

## Methodology

**Apple Search Ads** — Native App Store ad platform, keyword-based only (no audience targeting), highest purchase intent of any ad channel.

### Campaign Types

| Type | Use Case | Intent Level |
|------|----------|--------------|
| Search Results | Primary performance channel | Highest |
| Search Tab | Brand awareness | Medium |
| Today Tab | High-visibility brand moments | Lower |
| Product Pages | Competitive conquesting | High |

### Recommended Account Structure

```
Account → App
  ├── Brand Campaign (exact match, app name + misspellings)
  ├── Competitor Campaign (exact match, competitor names)
  ├── Category Campaign (exact + broad, generic keywords)
  ├── Discovery Campaign (Search Match only, find new terms)
  └── Search Tab Campaign (optional, brand awareness)
```

### Keyword Strategy Using MCP Data

From `get_keyword_popularity`:
- **Popularity 4–5**: High-volume keywords — prioritize in Category campaign, bid competitively
- **Popularity 2–3**: Mid-tier — core of Category campaign, solid ROI
- **Popularity 0–1**: Long-tail — high CVR, low competition, low bids needed

From `get_rankings`:
- Keywords where you already rank organically top 3 → bid Brand or lower bid (you'll get the click anyway)
- Keywords where you rank #4–20 → prime ASA opportunity (cover the gap)
- Keywords where you don't rank at all → Discovery campaign to test

### Starting Bid Ranges

| Campaign | Starting Bid |
|----------|-------------|
| Brand | $2–5 |
| Competitor | $1–2 |
| Category (high volume) | $0.80–1.50 |
| Discovery / Search Match | $0.50–0.80 |

### Bid Optimization Signals

| Signal | Action |
|--------|--------|
| Low impression share (<50%) | Increase bid |
| Low TTR (<3%) | Improve creative via Custom Product Pages |
| High TTR, low CVR (<30%) | Fix product page (screenshots, ratings) |
| High CPI vs. LTV | Reduce bid or pause keyword |
| Organic rank improving | Reduce ASA bid (let organic carry it) |

### Match Types

- **Exact** — use for proven keywords with good CVR history
- **Broad** — use for discovery within known keyword groups
- **Search Match** — Discovery campaign only; mine new keywords weekly

### Creative Product Sets + Custom Product Pages

Route ad groups to keyword-specific Custom Product Pages (CPP):
- Example: "meditation" keyword → CPP showing meditation screenshots
- Typically +15–30% TTR and CVR vs. default product page
- Create one CPP per major keyword theme (not per keyword)

### Key Metrics & Benchmarks

| Metric | Target | Investigate If |
|--------|--------|----------------|
| TTR (Taps/Impressions) | >5% | <3% |
| CVR (Installs/Taps) | >50% | <30% |
| ROAS | >150% | <100% |

### Weekly Optimization Checklist

1. Review spend pacing vs. budget
2. Pause keywords with >50 taps, CPI >3× target
3. Promote high-CVR Search Match discoveries to exact
4. Add new negative keywords from Search Match terms
5. Review CPP performance vs. default page

### Negative Keywords

Add at account level to prevent waste:
- Competitor brand names (unless in Competitor campaign)
- Irrelevant category terms
- Terms with consistently <20% CVR after 30+ taps
