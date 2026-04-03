---
name: market-movers
description: Identifies top ranking gainers, losers, and breakout apps from snapshot comparison data with actionable competitive insights
type: user-invocable
---

## Data Collection (run before analysis)

Call this MCP tool:
- `compare_snapshots` — ranking changes (default daysAgo: 7; use 30 for monthly view)

If data seems stale, call `collect_data` first.

## Methodology

**Market Movers** — Analyzes ranking changes to identify top gainers, losers, and breakout apps.

### Initial Assessment

Confirm:
- Time period (weekly default, or monthly)
- Focus: all tracked keywords or specific keyword group

### Analysis Framework

**1. Chart Movement Summary**
Key metrics from `compare_snapshots`:
- Total ranking changes detected
- Number of apps gaining vs. losing
- Average magnitude of changes
- Most volatile keyword (most position changes)

**2. Top Gainers**
For each app showing ranking improvement:
- Keywords gained and positions moved
- Pattern: is it one keyword or broad gains? (broad = algorithm signal; single = probably metadata change)
- Sustainability assessment: new app getting initial boost vs. established app optimizing

**3. Notable Losers**
For each app showing ranking decline:
- Keywords lost and positions dropped
- Likely cause: update disruption, rating drop, metadata change, or new competitor
- Opportunity assessment: can you capture their lost position?

**4. New Entrants**
Apps appearing on tracked keywords for the first time:
- Threat level: well-funded launch vs. organic newcomer
- Keywords they're targeting
- Whether they overlap with your primary keywords

**5. Category Volatility Patterns**
- Is movement concentrated in one keyword area?
- Are the changes correlated with a known external event?
- How does current volatility compare to typical periods?

### Actionable Output

**Immediate Opportunities:**
- Apps that dropped from top 3 on your target keywords
- Vacated keyword positions you could move into

**Threat Assessment:**
- New top-10 entrants on your primary keywords
- Competitors showing consistent multi-keyword improvement

**Timing Insights:**
- If a category is seeing unusual movement, it may indicate a featured app boost or seasonal effect

### Delivery Formats

- **Quick summary** (default): 3–5 bullets, emoji indicators (📈 gainers, 📉 losers, 🆕 new)
- **Detailed report**: full tables for each section above
- **Alert format**: only show changes exceeding ±5 positions
