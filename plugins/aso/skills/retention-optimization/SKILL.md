---
name: retention-optimization
description: Diagnose and improve mobile app retention across four pillars — activation, habit formation, engagement deepening, and long-term retention
type: user-invocable
---

## Methodology

**Retention Optimization** — Retention is revenue. A 5% improvement in D30 retention compounds into dramatically higher LTV.

### Four Strategy Pillars

**1. Activation** — Deliver immediate value before asking for anything
**2. Habit Formation** — Encourage repeat visits through triggers and rewards
**3. Engagement Deepening** — Gradually introduce advanced features
**4. Long-term Retention** — Sustain usage beyond the 30-day honeymoon period

### Industry Retention Benchmarks

| Category | Day 1 | Day 7 | Day 30 |
|----------|-------|-------|--------|
| Social / Messaging | 30–40% | 15–20% | 8–12% |
| Games | 25–35% | 10–15% | 4–8% |
| Health & Fitness | 20–30% | 10–15% | 5–10% |
| Productivity | 25–35% | 12–18% | 6–12% |
| Finance | 20–30% | 10–15% | 5–10% |
| E-commerce | 15–25% | 7–12% | 3–7% |

### Pillar 1: Activation (Days 0–1)

Goal: Get users to the core value moment in < 60 seconds (simple apps) or < 5 minutes (complex apps).

**Activation Optimization:**
- Define your single activation event (the action that predicts long-term retention)
- Remove all friction before activation: no sign-up gates, minimal permissions
- Show the app's best output immediately (demo content if needed)
- Measure % of users reaching activation within 24 hours

See `onboarding-optimization` skill for detailed onboarding framework.

### Pillar 2: Habit Formation (Days 1–7)

Goal: Create a return visit habit before the novelty wears off.

**Notification Strategy:**
| Day | Notification Goal | Message Type |
|-----|-----------------|-------------|
| 1 | Return visit | "Continue where you left off" |
| 3 | Streak initiation | "You've used [App] 3 days in a row!" |
| 7 | Streak reinforcement | "1-week streak — keep it going!" |

**Notification limits:** Maximum 3–5 push notifications per week per user. More than this decreases open rates and increases opt-outs.

**In-app triggers:** Daily or weekly goals, streak counters, progress bars, and completion rewards.

### Pillar 3: Engagement Deepening (Days 7–30)

Goal: Ensure users discover features beyond the core loop.

**Feature Introduction Sequence:**
- Don't show everything in onboarding — introduce features contextually after the user has mastered the core
- Trigger feature discovery at logical moments ("You've done X 10 times — try Y to go further")
- In-app tooltips on second or third session, never first

**Content Strategy (for content apps):**
- New content notifications are the highest-CTR push type
- Personalization increases engagement — surface content based on past behavior

### Pillar 4: Long-term Retention (Day 30+)

Goal: Prevent subscription cancellation and extend LTV.

**Churn Prevention Signals (act before they cancel):**
- Sessions < 1/week → send value-reminder push
- Core feature unused 14+ days → in-app coach mark
- Push notification permission disabled → use email or in-app banners
- Last session > 7 days → win-back sequence

**Re-engagement Campaign Templates:**

*Inactive 7 days:*
> "You haven't [core action] this week — your [streak/progress/goal] is waiting."

*Inactive 14 days:*
> "[Feature they used most] has been updated since your last visit — see what's new."

*Inactive 30 days:*
> "We've added [specific new feature] since you last checked in. Come see."

**Cancellation Flow (for subscription apps):**
See `subscription-lifecycle` skill for full cancellation flow and dunning strategy.

### Retention Diagnostic Framework

When retention is below benchmark, diagnose in this order:

1. **D1 Retention low** → Activation problem (see `onboarding-optimization`)
2. **D7 Retention low but D1 is OK** → Habit formation problem (notifications, return triggers)
3. **D30 Retention low but D7 is OK** → Engagement depth problem (feature discovery, content freshness)
4. **D90+ Churn** → Value plateau (need new content, features, or subscription churn flow)
