---
name: rating-prompt-strategy
description: Framework for optimizing when, how, and to whom to show review prompts to maximize ratings and review volume
type: user-invocable
---

## Methodology

**Rating Prompt Strategy** — Show prompts to users who have experienced value.

**Core Rule:** Only prompt users at a success moment. Timing at a positive moment produces 4–5 star ratings. Timing at a frustration moment produces 1–2 star reviews.

### iOS Mechanics (SKStoreReviewRequest)

- Apple shows the system prompt at most **3 times per 365-day period**
- Apple controls whether the prompt actually displays (may not show every time)
- Never prompt after: error messages, crashes, onboarding, failed actions
- Cannot be customized — use a pre-prompt survey to filter first

### Success Moment Triggers by Category

| App Type | Good Trigger | Bad Trigger |
|----------|-------------|-------------|
| Fitness | After completing a workout | After skipping a day |
| Meditation | After finishing a session | During a session |
| Productivity | After completing a task | After a sync error |
| Games | After winning or leveling up | After losing |
| Finance | After reaching a savings goal | After a declined payment |
| Education | After passing a quiz | After a wrong answer |
| Social | After receiving positive engagement | After a rejection |

### Session-Based Eligibility Criteria

Before showing the prompt, verify ALL of these:
- [ ] Sessions ≥ 3
- [ ] Days since install ≥ 3
- [ ] Activation event completed (user experienced core value)
- [ ] No crash in the last session
- [ ] No negative signal in the current session (error, failed action)
- [ ] Not already rated this version

### Pre-Prompt Survey (Recommended)

Show a custom in-app screen before triggering `SKStoreReviewRequest`:

> "Are you enjoying [App Name]?"
> [Yes, love it!] [Not really]

- "Yes" → trigger native App Store prompt
- "Not really" → show in-app feedback form (collect insights, do NOT trigger App Store prompt)

**Expected improvement:** +0.3–0.8 stars over direct prompting.

### Version-Gating (iOS)

After a major improvement update:
1. Reset — use a new `appVersion` key so users who rated old version can be prompted again
2. Run aggressive filtered prompt campaign in first 7 days post-update
3. Target only most engaged users (≥10 sessions, no recent crashes)

### Recovery from Rating Drop

When average rating drops below 4.2:

1. **Diagnose** — which version caused it? What's the root cause? (Check 1-star reviews)
2. **Fix** — ship the fix as fast as possible
3. **Respond** — reply to every 1–3 star review within 24 hours
4. **Prompt campaign** — immediately after shipping the fix, trigger prompts for your loyal user segment
5. **Monitor** — watch rating trend daily for 2 weeks

### Prompt Frequency Limits

| Platform | Limit |
|----------|-------|
| iOS | Max 3 per 365 days (Apple-enforced) |
| Android | Max 1 per 30 days per user (Google guidance) |
