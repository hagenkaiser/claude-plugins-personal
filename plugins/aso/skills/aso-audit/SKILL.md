---
name: aso-audit
description: Comprehensive ASO health audit scoring 10 factors (title, subtitle, keywords, screenshots, ratings, etc.) with real App Store data
type: user-invocable
---

## Data Collection (run before analysis)

Call these MCP tools to get live data:
- `get_rankings` — keyword positions for all tracked apps
- `get_keyword_popularity` — Apple Search Ads popularity scores (0–5)
- `get_app_metadata` — side-by-side metadata comparison

If data seems stale, call `collect_data` first.

## Methodology

**ASO Audit** — Expert ASO health audit with a prioritized action plan.

**Initial Assessment:** Check `app-marketing-context.md` if it exists, ask for App ID, target country, and platform (iOS/Android/Both).

### Audit Framework

Score each factor 0–10, weighted average for overall ASO Score:

| Factor | Weight |
|--------|--------|
| Title | 20% |
| Subtitle (iOS) | 15% |
| Keyword Field (iOS) | 15% |
| Description | 5% |
| Screenshots | 15% |
| App Preview Video | 5% |
| Ratings & Reviews | 15% |
| Icon | 5% |
| Keyword Rankings | 10% |
| Conversion Signals | 5% |

### Scoring Rubric

**Title (20%):** Does it contain the primary keyword? Is it under 30 chars? Is it readable? Does it communicate value?

**Subtitle (15%):** Does it complement the title? Contains secondary keywords? Communicates a clear benefit?

**Keyword Field (15%):** No repeated words from title/subtitle? Uses commas without spaces? Singular forms? No filler words?

**Screenshots (15%):** Does the first screenshot immediately communicate value? Are there benefit-driven captions? Is it visually compelling?

**Ratings & Reviews (15%):** Is average rating ≥ 4.5? Is review volume competitive? Are there recent reviews?

**Keyword Rankings (10%):** How many tracked keywords rank in top 10? Top 3?

**Conversion Signals (5%):** App preview video present? Social proof visible? Strong CTA in description?

### Output Format

1. **Visual Score Card** — table with each factor, score, and brief note
2. **Overall ASO Score** (weighted average) with grade (A/B/C/D/F)
3. **Quick Wins** (do today) — ranked by impact
4. **High-Impact Changes** (this week) — requiring more work
5. **Strategic Recommendations** (this month) — longer-term
6. **Competitor Comparison** — your scores vs. top competitor based on MCP data
