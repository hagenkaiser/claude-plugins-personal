---
name: metadata-optimization
description: ASO copywriting framework for title, subtitle, keyword field, and description — balancing search visibility and conversion with real ranking data
type: user-invocable
---

## Data Collection (run before analysis)

Call these MCP tools to get live data:
- `get_app_metadata` — current title, version, rating (baseline to improve)
- `get_rankings` — which keywords are already ranking to preserve

If data seems stale, call `collect_data` first.

## Methodology

**Metadata Optimization** — Copywriting framework balancing search visibility and conversion.

### Platform Field Limits

| Field | iOS | Google Play |
|-------|-----|-------------|
| Title | 30 chars | 30 chars |
| Subtitle | 30 chars | — |
| Short Description | — | 80 chars |
| Keyword Field | 100 chars | — |
| Description | 4,000 chars | 4,000 chars |

### Title Strategy

**Formula options:**
- `[Brand] - [Primary Keyword]` — use when brand is well-known
- `[Primary Keyword]: [Brand]` — use when brand is new, keyword is high-value

**Checklist:**
- Contains the single highest-volume relevant keyword
- Under 30 characters
- Readable as natural language (not keyword-stuffed)
- Communicates the core value proposition

### Subtitle Strategy (iOS)

- Secondary keyword not already in title
- Benefit-oriented phrasing preferred
- Exactly 30 characters — use every character
- Works as a standalone tagline

### Keyword Field Rules (iOS)

- Comma-separated, **no spaces** after commas
- **Singular forms only** (App Store also indexes plurals)
- No words repeated from title or subtitle
- No brand names (competitors or yours — already indexed)
- No generic filler: "app", "free", "best", "top"
- 100 characters — use all of them

### Description Structure

First 170 characters are visible without tapping "more" — this is your most valuable real estate:

```
[Hook — what problem you solve in one line]
[Social proof — X users, rating, awards]
[Core features — 3 bullet points]
[How it works — 2–3 sentences]
[Testimonial or user story]
[CTA — "Download free today"]
```

### Output Format

For each field, provide **3 options** with:
- Character count
- Keywords included (cross-referenced with MCP ranking data)
- Brief rationale

Then recommend the best option and explain why, noting any keywords from `get_rankings` that should be preserved to protect existing ranking positions.

### Common Pitfalls to Avoid
- Repeating keywords across fields (wastes limited space)
- Weak description opener ("Welcome to..." or "Introducing...")
- Cramming keywords that don't match user intent
- Ignoring currently ranking keywords (risk of ranking drop)
