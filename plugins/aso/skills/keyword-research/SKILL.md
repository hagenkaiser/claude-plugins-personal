---
name: keyword-research
description: Systematic four-phase keyword research using real popularity scores and ranking data to find the best keywords for App Store metadata
type: user-invocable
---

## Data Collection (run before analysis)

Call these MCP tools to get live data:
- `get_keyword_popularity` — Apple Search Ads popularity scores (0–5) for all tracked keywords
- `get_rankings` — current ranking positions for all tracked apps and keywords

If data seems stale, call `collect_data` first.

## Methodology

**Keyword Research** — Systematic, four-phase approach to find the best keywords.

### Phase 1: Initial Assessment

Ask for:
- Seed keywords (3–5 that describe the app)
- Target country (default: US)
- Primary optimization intent (rankings vs. conversion)
- Competitor app IDs (if not in `app-marketing-context.md`)

### Phase 2: Research

Using MCP data plus reasoning:
- Expand seed keywords via autocomplete logic
- Identify competitor ranking gaps (keywords where competitors rank but the tracked app doesn't)
- Generate synonyms and related terms
- Identify long-tail variations

### Phase 3: Evaluation

Assess each candidate keyword across:

| Factor | Weight | Notes |
|--------|--------|-------|
| Search volume (popularity score) | 40% | Use MCP popularity data (0–5) |
| Competition difficulty | 30% | Infer from rankings: many strong apps = hard |
| Relevance | 30% | How well it matches the app's core value |

### Phase 4: Opportunity Scoring

**Opportunity Score** = Volume (40%) + (5 − Difficulty) (30%) + Relevance (30%)

Organize into four tiers:
- **Primary** — title and subtitle placement
- **Secondary** — keyword field
- **Long-tail** — fill remaining keyword field space
- **Aspirational** — future growth once authority builds

### Output Format

1. **Keyword Opportunity Table** — keyword, popularity score (from MCP), estimated difficulty, relevance, opportunity score, recommended placement
2. **Metadata Placement Strategy** — which keywords go where
3. **Competitor Gap Analysis** — keywords competitors rank for that you don't (from MCP rankings data)
4. **Recommendations** — top 5 actions, update cadence (quarterly)

### Key Rules
- No keyword repetition across title/subtitle/keyword field
- Singular forms only in the keyword field
- No brand names of competitors
- No generic terms like "app" or "free"
