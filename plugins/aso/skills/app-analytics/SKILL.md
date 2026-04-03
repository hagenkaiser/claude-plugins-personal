---
name: app-analytics
description: Set up meaningful app analytics tracking, interpret key metrics, and build dashboards to make data-driven decisions across acquisition, engagement, and revenue
type: user-invocable
---

## Methodology

**App Analytics** — Set up tracking, interpret data, and make data-driven decisions.

### Recommended Analytics Stack

| Tool | Purpose | Cost |
|------|---------|------|
| App Store Connect | Store metrics, conversion funnel, retention | Free (required) |
| Firebase Analytics | In-app events, funnels, audiences | Free |
| Firebase Crashlytics | Crash reporting | Free |
| Mixpanel or Amplitude | Product analytics, cohort analysis | Free tier available |
| RevenueCat | Subscription analytics | Free tier (< $10K MRR) |
| Adjust or AppsFlyer | Multi-channel attribution | Paid (if running paid UA) |

**Minimum viable setup:** App Store Connect + Firebase Analytics + Crashlytics. Add RevenueCat if you have subscriptions.

### App Store Connect Key Metrics

| Metric | What It Tells You |
|--------|-----------------|
| Impressions | How many times your app appeared in search/browse |
| Product Page Views | How many users visited your product page |
| App Units | Downloads (first-time installs) |
| Conversion Rate | Page Views → Downloads (benchmark: 30–60%) |
| Proceeds | Revenue after Apple's cut |
| Sessions | App opens |
| Active Devices | Unique devices with the app open in last 30 days |
| Day 1 Retention | % of users who return the day after first install |
| Day 7 Retention | % who return 7 days later |
| Day 28 Retention | % who return 28 days later |
| Crash Rate | % of sessions with a crash |

**Source types:** Search, Browse, Web Referral, App Referral — use these to understand which channels are driving downloads.

### Key Metrics Framework

**Acquisition:**
- Impressions → TTR (Taps / Impressions) — how well your icon/listing grabs attention
- TTR → CVR (Downloads / Page Views) — how well your product page converts
- CPI (paid only) — cost per install from paid campaigns
- Organic % — what share of downloads come without paid spend

**Engagement:**
- DAU (Daily Active Users), MAU (Monthly Active Users)
- DAU/MAU Stickiness ratio — target > 20% (> 25% is excellent)
- Average Sessions per User per Day
- Average Session Length

**Retention:**
- D1: 25–40% target, D7: 10–20%, D30: 5–10%
- Monthly Churn: < 5% for subscriptions

**Revenue:**
- ARPU (Average Revenue Per User)
- ARPPU (Average Revenue Per Paying User)
- LTV (Lifetime Value)
- Trial-to-Paid Conversion Rate: 25–40% target
- MRR (Monthly Recurring Revenue)

### Core Events to Track

```
# Onboarding
onboarding_started
onboarding_step_completed {step: "name"}
onboarding_completed
onboarding_skipped

# Core Action (customize to your app)
[primary_action]_started
[primary_action]_completed
[primary_action]_failed {reason: "..."}

# Monetization
paywall_viewed {source: "onboarding|feature_gate|organic"}
trial_started
purchase_completed {product_id: "..."}
purchase_failed {reason: "..."}
subscription_renewed
subscription_cancelled {reason: "..."}

# Session
session_started
feature_used {feature_name: "..."}
notification_received {type: "..."}
notification_tapped {type: "..."}

# Settings
notification_permission_granted
notification_permission_denied
```

**Event Naming Convention:** snake_case, `[object]_[action]` format, consistent across iOS and Android.

### Dashboard Setup

**Executive Dashboard (review weekly):**
- Downloads, Revenue, DAU, CVR (App Store), D1 Retention, Average Rating

**Funnel Dashboard (review daily during growth phase):**
- Impressions → Page Views → Downloads → Activation → Purchase
- Identify and investigate any step with > 30% drop-off

**Cohort Dashboard (review monthly):**
- Retention curves by install date (are newer cohorts improving?)
- Retention by acquisition source (which channel brings best users?)
- Retention by country (which market retains best?)
- Subscription cohort revenue (when does LTV plateau?)

### Interpreting Conversion Rate

| CVR | Assessment |
|-----|-----------|
| > 60% | Excellent — strong brand or unique positioning |
| 40–60% | Good — competitive |
| 20–40% | Average — room to improve screenshots/metadata |
| < 20% | Poor — prioritize product page optimization |

**CVR drop alert:** If CVR drops > 10% week-over-week without a known cause (metadata change, category shift), investigate immediately — could be a competitor entering top results or a negative review surge.
