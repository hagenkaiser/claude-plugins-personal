---
name: review-management
description: Framework for responding to App Store reviews, managing reputation, and extracting product insights using the HEAR model
type: user-invocable
---

## Methodology

**Review Management** — Turn reviews into retention, product intelligence, and conversion signals.

### Critical Metrics

| Metric | Target |
|--------|--------|
| Average rating | ≥ 4.5 stars |
| Response time (negative reviews) | < 24 hours |
| Response rate (negative reviews) | 100% |
| Response rate (positive reviews) | 10–20% (prioritize top reviewers) |

### The HEAR Response Model

**H — Hear:** Acknowledge what the user said specifically. Don't use a generic opener.

**E — Empathize:** Show you understand their frustration or appreciate their input. One sentence.

**A — Act:** Explain what you're doing about it (if a bug: "we're fixing this in the next update"). If a feature request: "I've noted this for our roadmap."

**R — Resolve:** Give them a path forward. Email support link, suggest a workaround, or tell them when a fix ships.

### Response Templates by Review Type

**1-star (bug/crash):**
> "Hi [Name], sorry to hear about this crash — that's not the experience we want. We've noted the issue and are working on a fix. Please email [support@] with your device model so we can expedite this. We'll update this response when it's resolved."

**1-star (pricing complaint):**
> "Hi [Name], I understand the subscription pricing feels steep. We offer a [X-day free trial] — if you'd like to continue at a lower price, please reach out at [support@] and we'll see what we can do."

**1-star (feature request disguised as complaint):**
> "Thanks for the feedback. [Feature] is on our roadmap — we'll be sure to update when it's live. In the meantime, [workaround if any]."

**5-star:**
> "Thank you so much! [Specific acknowledgment of what they said]. More good things coming soon."

### Review Analysis Categories

Systematically categorize reviews into:
1. **Technical bugs** — crashes, errors, sync issues
2. **Feature requests** — "I wish it could..."
3. **UX friction** — confusing flows, hard to find things
4. **Pricing concerns** — too expensive, unexpected charges
5. **Positive sentiment** — specific praised features
6. **Competitive comparisons** — mentioned switching from/to which competitors

### Strategic Value of Negative Reviews

Negative reviews, when properly analyzed, reveal:
- **Unmet needs** → feature roadmap input
- **Switching triggers** → what drives users to competitors
- **Onboarding failures** → where new users get confused
- **Price sensitivity signals** → which tier/price point to test

Run a review analysis whenever preparing for a metadata update or product roadmap planning.

### Developer Response Visibility

- Responses are **public** and appear directly under the review
- Responses are visible in search results for your app
- Updating a response after a fix encourages users to revise their rating
- Always invite resolved users to update: "Feel free to update your review if this is now working for you!"

### Escalation: When to Go Beyond the Response

If a review describes a pattern affecting multiple users:
1. Check if it's a known issue in crash analytics
2. If not, prioritize investigation
3. Proactively reach out to all 1-star reviewers via developer response when a fix ships
