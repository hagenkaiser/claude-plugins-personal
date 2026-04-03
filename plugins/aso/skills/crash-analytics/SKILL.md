---
name: crash-analytics
description: Monitor, triage, and reduce app crashes using a priority framework — crash-free rate targets, tooling setup, and phased rollout monitoring
type: user-invocable
---

## Methodology

**Crash Analytics** — Protect ratings, rankings, and editorial eligibility by maintaining high crash-free rates.

### Why Crash Rates Matter for ASO

- App Store crash rate is a **direct input to search ranking algorithms**
- Apps with high crash rates are penalized in search rankings
- High crash rates disqualify apps from editorial featuring consideration
- 1-star reviews citing crashes damage conversion rate
- Apple surfaces crash data to editors reviewing featuring pitches

### Targets

| Metric | Target | Excellent |
|--------|--------|-----------|
| Crash-free sessions | > 99.5% | > 99.9% |
| Crash-free users | > 99% | > 99.8% |

### Primary Tools

| Tool | Purpose | Cost |
|------|---------|------|
| Firebase Crashlytics | Real-time crashes with symbolicated stack traces | Free |
| App Store Connect | Built-in crash rate trending by version/device | Free |
| Xcode Organizer | Aggregated crashes from TestFlight and production | Free |
| MetricKit | On-device diagnostics, hang rates, disk I/O (iOS 13+) | Free |

**Minimum required:** Firebase Crashlytics + App Store Connect. Both are free and complementary.

### Triage Priority Framework

**Priority Score** = Crash Frequency × Affected Users × User Segment Weight

| Priority | Threshold | Action |
|----------|-----------|--------|
| P0 Critical | > 1% of sessions | Same-day hotfix, consider pulling version |
| P1 High | > 0.1% of sessions | Fix in current release cycle (< 1 week) |
| P2 Medium | < 0.1% of sessions | Schedule for next release |
| P3 Low | < 0.01% of sessions | Add to backlog |

**User Segment Weight Adjustment:**
- Crashes on launch (affects all users) → ×2 priority multiplier
- Crashes for new users (affects conversion) → ×1.5 multiplier
- Crashes for paid users (affects revenue) → ×1.5 multiplier
- Crashes only on deprecated OS → ×0.5 multiplier

### Crash Investigation Workflow

1. **Get the stack trace** — Crashlytics provides symbolicated stack traces; Xcode Organizer aggregates top crashes
2. **Identify the OS/device pattern** — Is it device-specific (memory), OS-specific (API behavior), or universal?
3. **Reproduce locally** — Try to reproduce using the crash context (app state, user action)
4. **Write a failing test** — If possible, write a test that reproduces the crash before fixing
5. **Fix and verify** — Ensure the stack trace location is resolved
6. **Monitor post-release** — Watch the crash rate for 24–48 hours after the fix ships

### Phased Rollout Monitoring

When releasing updates:
1. Release to 5% of users first
2. Monitor Crashlytics for 24 hours
3. If crash rate increases by > 0.2% → pause rollout and investigate
4. If stable → proceed to 20%, then 50%, then 100%

App Store Connect supports phased release (7-day automatic rollout). Enable this for every update.

### Preventing Crashes

**Common crash categories and prevention:**

| Category | Prevention |
|----------|-----------|
| Force unwrap / nil crash | Use optional chaining and guard statements |
| Array out of bounds | Validate indices before access |
| Background thread UI updates | Dispatch to main queue for all UIKit/SwiftUI |
| Memory pressure | Profile with Instruments Allocations; release caches |
| API changes (iOS version) | Use `if #available(iOS X, *)` checks |
| Third-party SDK updates | Test each SDK update in staging before shipping |

### Reporting to the Team

Weekly crash report should include:
- Current crash-free rate (vs. prior week)
- New crashes introduced in latest version
- P0/P1 open issues with owners assigned
- Crashes resolved this week
- Trend line (improving or worsening)
