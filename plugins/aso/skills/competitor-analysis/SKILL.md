---
name: competitor-analysis
description: Deep competitive intelligence comparing 3–5 competitors across metadata, keywords, creative strategy, ratings, growth signals, and monetization
type: user-invocable
---

## Data Collection (run before analysis)

Call these MCP tools to get live data:
- `get_rankings` — keyword positions for all tracked apps
- `get_app_metadata` — side-by-side metadata comparison (ratings, price, version, update date)
- `compare_snapshots` — changes over time (use daysAgo: 30 for monthly context)

If data seems stale, call `collect_data` first.

## Methodology

**Competitor Analysis** — Competitive intelligence across six dimensions.

### Initial Assessment

Confirm:
- My app ID (from `app-marketing-context.md` if available)
- Which competitors to analyze (use tracked competitors from MCP data, or ask for additional ones)
- Focus area (metadata, keywords, creative, monetization, or all)

### Six Analysis Dimensions

**1. Metadata Analysis**
Using `get_app_metadata`:
- Compare titles — do competitors lead with brand or keyword?
- Compare ratings and review counts — who has the strongest social proof?
- Compare pricing — free vs. paid vs. freemium
- Compare update frequency — who ships faster?

**2. Keyword Gap Analysis**
Using `get_rankings`:
- Keywords where competitors rank in top 10 but you don't → high-priority gaps
- Keywords where you rank but competitors don't → strengths to defend
- Keywords where no one ranks well → untapped opportunities

**3. Creative Strategy**
Based on metadata and reasoning:
- Screenshot philosophy (features vs. benefits vs. social proof)
- Icon design approach

**4. Ratings & Reviews**
Using `get_app_metadata`:
- Rating comparison
- Review count comparison (proxy for download volume)
- Identify who's winning user satisfaction

**5. Growth Signals**
Using `compare_snapshots`:
- Ranking improvements/declines over past period
- Recent metadata changes (sign of active ASO)
- Update frequency (version + date from metadata)

**6. Monetization**
Using `get_app_metadata`:
- Pricing model from price field
- Free vs. paid positioning

### Output Format

1. **Executive Summary** — 3–5 bullet competitive overview
2. **Competitive Positioning Map** — table comparing all 6 dimensions
3. **Top Opportunities**
   - Quick wins (keyword gaps, metadata improvements)
   - Creative advantages to exploit
4. **Threats to Monitor** — competitors showing strong growth signals
5. **Recommended Actions** — prioritized, actionable list
