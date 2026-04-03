---
name: screenshot-optimization
description: Framework for designing App Store screenshots that convert browsers to downloaders — content strategy, design standards, and A/B test ideas
type: user-invocable
---

## Methodology

**Screenshot Optimization** — Convert browsers to downloaders.

**Key Insight:** Users spend 3–6 seconds on a product page. The first 3 screenshots determine 80% of the conversion decision.

### First Screenshot Strategy

The first screenshot must answer: "Does this app solve my problem?"

Options ranked by conversion effectiveness:
1. **Problem/Solution** — Show the pain on left, solution on right
2. **Transformation** — Before/after or "from X to Y"
3. **Social proof** — "4.8 stars · 50,000 reviews" with hero UI
4. **Benefit statement** — Bold headline + supporting UI (most common, often highest performer)

**What not to do:** Generic feature showcase, app UI with no context, logo-only hero image.

### Content Structure (10 Screenshot Slots)

| Slot | Goal | Content |
|------|------|---------|
| 1 | Hook | Answer "what does this do?" — bold benefit + key UI |
| 2 | Core Feature 1 | Primary use case with benefit headline |
| 3 | Core Feature 2 | Second most important feature |
| 4–7 | Feature Depth | Individual features: Benefit + UI + detail |
| 8–9 | Trust Signals | Reviews, awards, media coverage, user count |
| 10 | CTA Recap | Recap value prop + download encouragement |

### Copywriting for Screenshots

- Headlines: 4–6 words max, benefit-first ("Sleep faster" not "Sleep tracking feature")
- Font size: minimum 60px at export resolution
- Avoid: full sentences, more than 2 lines of text per screenshot

### Design Standards

- **Contrast**: Text must pass WCAG AA contrast ratio
- **Consistency**: Same color palette, font, and device mockup style throughout
- **Real content**: Show actual app content, not placeholder data
- **Dark mode**: Consider providing dark mode variants (boosts conversion for some categories)
- **Device mockup**: Use the current iPhone Pro model frame
- **Background**: Consistent background color or gradient throughout the set

### Screenshot Dimensions (iOS)

| Device | Size |
|--------|------|
| iPhone 6.9" (default) | 1320×2868px |
| iPhone 6.5" | 1242×2688px |
| iPad Pro 12.9" | 2048×2732px |

Upload 6.9" — it auto-scales to all sizes.

### App Preview Video

Best for: complex apps, games, apps where motion demonstrates value.

**Specs:** 15–30 seconds, landscape or portrait (match screenshots), MP4/MOV.

**Structure:**
- 0–3s: Hook — show the best feature or outcome immediately
- 3–20s: Core features in action
- 20–30s: Call to action + branding

**Must have:** Caption overlays for no-sound viewing (most users watch without sound).

### A/B Test Priorities

Run in this order (via App Store Connect Product Page Optimization):
1. First screenshot (highest impact — hero of the set)
2. Screenshot order (low effort, meaningful lift)
3. Screenshot style (lifestyle vs. UI-only vs. illustrated)
4. App preview video (does it help or hurt?)

See `ab-test-store-listing` skill for full A/B testing methodology.
