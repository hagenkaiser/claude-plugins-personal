---
name: market-pulse
description: Comprehensive App Store market overview combining ranking changes, trending keywords, and category dynamics to brief on what's happening in the market
type: user-invocable
---

## Data Collection (run before analysis)

Call these MCP tools to get live data:
- `get_rankings` — current keyword positions across the market
- `compare_snapshots` — ranking changes over time (use daysAgo: 7 for weekly pulse)
- `get_keyword_popularity` — trending keyword volume signals

If data seems stale, call `collect_data` first.

## Methodology

**Market Pulse** — Comprehensive market overview from available data signals.

### Initial Assessment

Ask for:
- Scope: full market or specific category focus
- Country (default: US)
- Format: quick briefing, detailed weekly report, or competitive focus

### Market Briefing Framework

**1. Headlines**
Top 3–5 most significant events from `compare_snapshots`:
- Big ranking shifts (±10 positions)
- New apps entering tracked keywords
- Your own position changes

**2. Ranking Dynamics**
From `compare_snapshots`:
- Top gainers (apps showing consistent improvement across keywords)
- Notable drops (potential weaknesses to exploit)
- New entrants on previously stable keywords

**3. Keyword Volume Signals**
From `get_keyword_popularity`:
- Highest popularity keywords (4–5 score) — most competitive
- Mid-tier keywords (2–3 score) — opportunity zone
- Low volume (0–1 score) — long-tail opportunities
- Note any seasonal patterns based on current date

**4. Competitive Landscape**
From `get_rankings` + `get_app_metadata`:
- Who's winning the most tracked keywords
- Concentration: is one app dominating or is it fragmented?
- Your relative position across all tracked keywords

**5. Category Health**
Infer from available data:
- Is the market volatile (many ranking changes) or stable?
- Download threshold inference from `get_app_metadata` rating counts
- How recently are top apps updating (version dates)

### Output Formats

**Quick Briefing (default):** 5–7 bullet summary, top 3 action items, 2-minute read

**Detailed Weekly Report:**
- Each section above with supporting data tables
- Your position vs. prior period
- Recommended focus areas for the coming week

**Competitive Focus:**
- Which competitor is most active (most changes in compare_snapshots)
- Opportunities opened by competitor drops
- Threats from competitor gains
