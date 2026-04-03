---
name: onboarding-optimization
description: Drive user activation and Day 1 retention by optimizing the onboarding flow — from install to first value delivery
type: user-invocable
---

## Methodology

**Onboarding Optimization** — Drive activation, not just sign-up. Activation (the first meaningful action) is the single best predictor of long-term retention.

### Initial Assessment Questions

1. What is your **activation event**? (The one action that reliably predicts a user staying)
2. What % of new installs reach activation within **24 hours**?
3. At which screen do most users **drop off**?
4. How many screens does your current onboarding have?

### Recommended Onboarding Structure

```
1. Open — immediate value hook (don't show a logo splash)
2. Core demo — show the app doing something useful (no sign-up yet)
3. Activation — let them do the core action (even without an account)
4. Sign-up — NOW ask for an account (after they've experienced value)
5. Permissions — ask contextually, with explanation screens first
6. Personalization — only questions that visibly change the experience
7. Paywall — after activation, never before
```

### Critical Friction Points

**1. Permission Prompts**

- Never request permissions cold on first launch
- Show a **native explanation screen** before the system prompt:
  - "We'll need camera access to [specific reason]. This is used only for [X]."
  - Pre-permission screens improve grant rates by 2–3×
- Request permissions only when contextually triggered (e.g., notification permission after user sets a reminder, not during sign-up)

**2. Sign-Up Gate**

| Approach | Conversion Rate | Notes |
|----------|----------------|-------|
| Hard gate (sign-up first) | 15–30% | Blocks all value delivery |
| Guest mode with conversion prompt | 40–60% | Industry best practice |
| Social sign-in only | 25–40% | Faster but limits reach |

Allow users to experience core value before requiring an account. "Guest" users who activate convert at 40–60%.

**3. Personalization**

- Limit to **3–5 questions max**
- Every question must **visibly affect the experience** (if it doesn't change anything, remove it)
- Use visual selection (icons, images) over text-only choices
- Show a progress indicator (users are more likely to complete with a visual progress bar)

### Activation Focus

Time-to-activation in under 60 seconds is the goal for simple apps; under 5 minutes for complex apps.

Common activation killers:
- Sign-up before value delivery
- Tutorial that explains every feature upfront (explain on first use instead)
- Asking for permissions on a cold open
- Too many personalization questions before the user has any context

### Benchmarks

| Metric | Target |
|--------|--------|
| First interaction (tap) | > 85% |
| Sign-up completion | > 60% |
| Day 0 activation | > 40% |
| Day 1 retention | > 30% |

### Onboarding Analysis Framework

For each drop-off point:
1. Identify the screen where users leave
2. Ask: "Is this screen delivering value, or asking for something?"
3. If asking without delivering — reorder or remove
4. Run an A/B test with that screen removed or moved later

### Push Notification Timing

Do **not** ask for push notification permission during onboarding. Wait until:
- User has completed activation
- User has set a preference that would naturally trigger a notification
- Or at least Day 2 after install
