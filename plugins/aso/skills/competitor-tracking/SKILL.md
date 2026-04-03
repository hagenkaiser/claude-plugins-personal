---
name: competitor-tracking
description: Weekly competitor surveillance report detecting metadata changes, keyword shifts, rating drops, and growth signals using snapshot comparison
type: user-invocable
---

## Data Collection (run before analysis)

Call this MCP tool:
- `compare_snapshots` — compare latest vs. previous snapshot (default daysAgo: 7 for weekly report; use 30 for monthly deep-dive)

If data seems stale, call `collect_data` first to get a fresh snapshot, then run `compare_snapshots`.

## Methodology

**Competitor Tracking** — Ongoing surveillance catching changes before they impact your rankings.

**Distinction from competitor-analysis:** This skill produces a recurring change log + alerts. Use `competitor-analysis` for one-time deep dives; use this skill for weekly/monthly monitoring.

### Weekly Monitoring Focus

Using `compare_snapshots` output, look for:

**1. Keyword Ranking Changes**
- Competitors entering top 10 for your primary keywords (threat)
- Competitors dropping from top 10 on shared keywords (opportunity)
- Your own ranking improvements/declines

**2. Metadata Changes**
- Title or subtitle updates (aggressive ASO pivot)
- App version bumps (active development signal)
- Price changes (monetization experiments)

**3. Ratings & Review Changes**
- Rating drops (weakness to exploit, or product issue to learn from)
- Rapid rating increases (their review prompt is working)

**4. Growth Velocity**
- Ranking jumps of 10+ positions on any keyword (algorithm boost or campaign)
- Consistent multi-keyword improvement (sustained investment)

### Weekly Report Template

```
## Competitor Tracking Report — [Date]

### Summary
[1–2 sentence overview of the week's most important changes]

### Changes Detected
| App | Change Type | Detail | Impact |
|-----|-------------|--------|--------|
| ... | Ranking +   | "meditation" #12 → #4 | High |

### Opportunities Identified
- [Competitor X dropped on keyword Y — opportunity to push bid/metadata]

### Threats
- [Competitor Z entered top 10 for your #1 keyword]

### Action Items
1. [Specific, actionable response]
2. ...
```

### Monthly Deep-Dive Triggers

Escalate to full `competitor-analysis` when:
- A competitor jumps 10+ positions across multiple keywords
- A competitor changes their title (signals major ASO pivot)
- A new app enters the top 10 in your category
- Your own ranking drops 5+ positions on a primary keyword

### Competitive Response Playbook

| Scenario | Response |
|----------|----------|
| Competitor targets your #1 keyword | Reinforce metadata + increase Apple Search Ads bids |
| Competitor drops in ratings | Opportunity window — push review prompt to your engaged users |
| New entrant takes top 10 | Run full competitor-analysis immediately |
| Competitor updates title | Check if they dropped/gained rankings 2 weeks later |
| Your ranking drops | Check compare_snapshots for metadata changes you may have missed |
