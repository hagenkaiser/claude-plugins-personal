---
name: app-icon-optimization
description: Audit, redesign, and A/B test app icons to maximize tap-through rate — five design principles, an audit scoring rubric, and a designer brief template
type: user-invocable
---

## Methodology

**App Icon Optimization** — Icons can lift tap-through rate (TTR) by 20–40% with no other changes.

**Why icons matter:** In search results, your icon is the first visual element users see. A distinctive, legible icon at 60×60pt drives curiosity and trust before users even read the app name.

### Five Design Principles

**1. Simplicity at Small Size**
- Icons render at ~60×60pt in search results — test yours at exactly this size
- Maximum 2 visual elements
- No text (illegible at small sizes, and redundant with the app name below)
- Strong, recognizable silhouette (can you recognize it as a shape in monochrome?)

**2. Color Contrast**
- Test on both light and dark mode backgrounds
- Avoid white-dominant icons (disappear on light mode)
- Avoid very dark icons (disappear on dark mode or night displays)
- Ensure foreground element has ≥ 4.5:1 contrast ratio against background

**3. Category Visual Language**

| Category | Common Approach | Stand Out By |
|----------|----------------|--------------|
| Productivity | Blue, minimal, geometric | Warmer colors, bolder geometric mark |
| Health & Fitness | Green/teal, activity imagery | High energy, contrasting colors |
| Finance | Blue/green, charts | Trustworthy but distinctive mark |
| Games | Character or game element | Strong character personality |
| Social | Gradient, speech bubble | Unique shape or color palette |
| Education | Books, graduation cap | Playful color, modern illustration |

**4. Recognizable Mark**
- Test: describe your icon in 3 words. If you can't, it's too complex.
- ✅ "Red speech bubble" — recognizable
- ✅ "Orange flame" — recognizable
- ❌ "Abstract colorful shapes" — not recognizable

**5. Brand Consistency**
- Match the app's primary color palette
- Consistent with your splash screen, push notification icon, and marketing materials
- Users who see your icon in ads should recognize it in the App Store

### Required Sizes

Submit a single 1024×1024px PNG (no transparency, no rounded corners — Apple applies the rounded rect mask automatically).

| Usage | Size |
|-------|------|
| App Store master | 1024×1024px |
| iPhone home screen | 60×60pt @2x, @3x |
| iPad home screen | 76×76pt @2x |
| Apple Watch | 40–44pt |

### Icon Audit Scoring

Score each dimension /10, calculate total /50:

| Dimension | Score | Notes |
|-----------|-------|-------|
| Clarity at 60×60px | /10 | Is it legible and recognizable at small size? |
| Color contrast | /10 | Works on light and dark backgrounds? |
| Category differentiation | /10 | Does it stand out from competitors? |
| Simplicity | /10 | Maximum 2 elements, no text |
| Brand alignment | /10 | Matches app's visual identity |

**Total /50:**
- 45–50: Excellent, test minor variants only
- 35–44: Good, one redesign iteration recommended
- 25–34: Needs improvement, run an A/B test
- < 25: Priority redesign

### A/B Testing Icons

**iOS (Product Page Optimization):**
App Store Connect → Product Page Optimization → New Test → Icon variant
- Up to 3 variants
- Automatic traffic split
- Minimum 90% confidence before declaring winner
- One test at a time

**What to test (one variable at a time):**
1. Color scheme (e.g., blue background vs. orange)
2. Mark style (flat vs. illustrated vs. 3D)
3. Dark vs. light background
4. Character vs. abstract mark
5. Simple vs. complex composition

### Designer Brief Template

Use this when commissioning a new icon design:

```
App Name: [Name]
App Purpose: [One sentence]
Target Audience: [Demographics]
Primary Brand Colors: [Hex codes]
Mood/Tone: [Modern + minimal | Playful + energetic | Professional + trustworthy]
Core Element to Convey: [The one thing the icon should communicate]
What to Avoid: [Colors, styles, elements used by direct competitors]
Competitor Reference Icons: [App Store links]

Deliverables Requested:
- 3 distinct concepts (not variations)
- Each at 1024×1024px PNG and 60×60px mockup
- Final icon as 1024×1024px PNG (no transparency, no rounded corners)
```
