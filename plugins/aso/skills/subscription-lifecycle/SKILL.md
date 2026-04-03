---
name: subscription-lifecycle
description: Optimize every stage of the subscription funnel — trial conversion, voluntary churn, involuntary churn (failed payments), and win-back campaigns
type: user-invocable
---

## Methodology

**Subscription Lifecycle** — Maximize LTV by optimizing every stage from trial to win-back.

### Lifecycle Stages

```
Install → Trial Start → [Trial Period] → Conversion → Renewal → ... → Cancel/Lapse → Win-back
```

### Key Metrics & Benchmarks

| Stage | Metric | Target | Strong |
|-------|--------|--------|--------|
| Trial-to-Paid | Conversion rate | >25% | >40% |
| Month 1 Renewal | M1 retention | >60% | >70% |
| Month 6 Renewal | M6 retention | >40% | >55% |
| Monthly Churn | Churn rate | <5% | <2% |
| Annual Churn | Annual churn | <30% | <20% |

### Stage 1: Trial Optimization

**Trial Length by Category:**
- Simple utility (to-do, timer): 3–7 days
- Health, productivity, education: 7–14 days
- Complex or enterprise: 14–30 days

**Trial Nurture Sequence:**

| Day | Message | Goal |
|-----|---------|------|
| 0 | Welcome + single best action | First value delivery |
| 1 | Core feature walkthrough | Feature discovery |
| 3 | Social proof or case study | Reinforce decision |
| 5 | "X days left" urgency | Activation nudge |
| 6 | Value recap | Justify purchase |
| Last day | "Don't lose access" | Convert |

### Stage 2: Reducing Voluntary Churn

**Why Users Cancel:**

| Reason | Signal | Fix |
|--------|--------|-----|
| Forgot about subscription | Low session count | Push notification re-engagement |
| Not enough value | Core feature unused | In-app tooltip or coach mark |
| Too expensive | Price complaint in reviews | Introduce lower tier or pause |
| Switching to competitor | Competitor mention in reviews | Identify and address gap |
| Life change | No signal | Win-back is only option |

**Cancellation Flow (present in this order):**
1. Offer **pause** (1–3 month pause without cancelling)
2. Show **value recap** ("In the past X days you've done Y")
3. Offer **discount** (last resort — 30–50% off 3 months)
4. Exit survey if they still cancel

**Engagement Risk Signals (proactively trigger re-engagement):**
- Sessions < 1/week
- Core feature not used in 14+ days
- Push notifications disabled
- Last session > 7 days ago

### Stage 3: Involuntary Churn (Failed Payments)

Involuntary churn accounts for 20–40% of all cancellations. Never ignore this.

**Dunning Timeline:**

| Day | Action |
|-----|--------|
| 0 | Payment fails → begin Apple/Google grace period |
| 1 | In-app banner: "Update your payment method" |
| 3 | Push notification: "Action needed to keep access" |
| 7 | Email (if available): "Your subscription is at risk" |
| 10 | Final in-app alert with benefit reminder |
| 15 | Grace period ends → access revoked |

**Grace Periods:**
- iOS: 6 days default (configurable up to 16 days in App Store Connect)
- Android: 3 days

**Recommended tool:** RevenueCat handles dunning automation.

### Stage 4: Win-Back Campaigns

**Offer Ladder (don't lead with maximum discount):**

| Timing | Message | Offer |
|--------|---------|-------|
| Week 1 post-cancel | "We miss you" | None — just re-engagement |
| Week 3 | "Come back" | 30% off first renewal |
| Week 6 | "Special offer" | 50% off 3 months |
| Week 12+ | Archive | If no re-engagement, stop |

**Channels:**
- Push notification (if still enabled)
- Email (if captured)
- Apple Win-Back Offer via StoreKit 2 (iOS 18+) — native, no friction
- Paid retargeting (last resort for high-LTV users)

**StoreKit 2 Win-Back Offers (iOS 18+):**
- Apple can automatically surface win-back offers to lapsed subscribers
- No additional developer code required after initial setup
- Configure in App Store Connect under Subscriptions → Win-Back Offers
