---
name: seasonal-aso
description: Optimize App Store metadata around calendar events and trending seasonal moments using real keyword popularity data
type: user-invocable
---

## Data Collection (run before analysis)

Call this MCP tool:
- `get_keyword_popularity` — current popularity scores to identify seasonal trends

If data seems stale, call `collect_data` first.

## Methodology

**Seasonal ASO** — Capitalize on time-sensitive keyword spikes while protecting evergreen rankings.

**Core Principle:** "Seasonal rankings are competitive and time-sensitive." Metadata takes 1–3 days to index. Plan 2 weeks before events. Revert 3–5 days after peak passes.

### Seasonal Calendar

| Event | Peak Window | Example Keywords |
|-------|-------------|-----------------|
| New Year (Jan 1) | Dec 26 – Jan 7 | new year goals, habit tracker, resolution |
| Valentine's Day (Feb 14) | Feb 7–14 | romantic, couples, love |
| Spring/Easter | 2 weeks before | spring challenge, refresh |
| Mother's/Father's Day | 1 week before | gift, family, parents |
| Summer | Jun–Aug | travel, vacation, outdoor |
| Back to School | Aug–Sep | study, student, organize |
| Halloween | Oct 15–31 | spooky, costume, scary |
| Thanksgiving | Nov 20–28 | family, gratitude |
| Christmas/Holiday | Dec 1–25 | gift, holiday, Christmas |
| End of Year | Dec 26–31 | year review, goals, planning |

### Workflow

**Step 1: Identify Relevant Events**
- Which upcoming seasonal events are relevant to your app's category?
- Rate compatibility: High (core use case), Medium (adjacent), Low (stretch)
- Skip Low compatibility — seasonal speculation hurts more than it helps

**Step 2: Research Seasonal Keywords**
Using `get_keyword_popularity`:
- Compare current popularity of seasonal terms vs. evergreen terms
- Identify which seasonal keywords have genuine volume (score ≥ 3)
- Flag keywords currently ranking well that should NOT be touched

**Step 3: Plan Metadata Changes**
Fields to update:
- **Promotional text** (iOS only, no review required) — update instantly, revert instantly
- **Subtitle** — swap one underperforming keyword for seasonal term
- **Keyword field** — replace low-volume evergreen terms with seasonal ones

Fields NOT to touch:
- Title (too risky to change frequently)
- Any field containing a currently top-10 ranking keyword

**Step 4: Execute 14-Day Timeline**

```
T-14: Identify event and keywords, draft copy
T-10: Submit metadata update for review
T-7:  Confirm metadata live, update promotional text
T-3:  Final promotional text push (no review needed)
Peak: Monitor rankings daily
T+3: Submit revert for review
T+7: Confirm evergreen metadata restored
```

### Key Trade-Off

Never sacrifice a top-10 ranking keyword for seasonal speculation. The rule: only replace keywords that are currently ranking below position 20 or not ranking at all.
