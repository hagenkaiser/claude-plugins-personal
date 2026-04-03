---
name: app-marketing-context
description: Create or update the foundational app-marketing-context.md reference document used by all other ASO skills
type: user-invocable
---

## Methodology

**App Marketing Context** — The starting point for all ASO work. Creates `app-marketing-context.md` as the foundational reference for every other skill.

**Run this skill first**, before using `aso-audit`, `keyword-research`, `competitor-analysis`, or any other ASO skill.

### Initial Check

1. Look for `app-marketing-context.md` in the project root
2. If it **exists**: read it and offer to update any section
3. If it **doesn't exist**: walk through each section interactively

### Document Structure

Walk through each section with the user:

---

**Section 1: App Overview**

```markdown
## App Overview
- App Name:
- Apple App Store ID:
- Google Play ID: (if applicable)
- Primary Category:
- Secondary Category: (if applicable)
- Platform: iOS / Android / Both
- Price Model: Free / Paid ($X) / Freemium / Subscription
- Launch Date:
- Current Version:
```

**Section 2: Value Proposition**

```markdown
## Value Proposition
- Problem Solved: [One sentence — what pain does this app eliminate?]
- Target Audience: [Who specifically — not "everyone", be specific]
- Unique Differentiator: [What does this app do that no competitor does as well?]
- Elevator Pitch: [One sentence combining audience + problem + solution]
```

**Section 3: Competitive Landscape**

```markdown
## Competitive Landscape
| Competitor | App Store ID | Strengths | Weaknesses |
|-----------|-------------|-----------|-----------|
| [Name]    | [ID]        | [...]     | [...]     |
```

Aim for 3–5 direct competitors. Use tracked competitors from MCP config if available.

**Section 4: Current ASO State**

```markdown
## Current ASO State
- Title: [current title]
- Subtitle: [current subtitle]
- Keyword Field: [current keywords, comma-separated]
- Average Rating: X.X (N reviews)
- Primary Keywords We're Targeting: [list]
- Keywords We Rank For (Top 20): [list from MCP data if available]
```

**Section 5: Goals & KPIs**

```markdown
## Goals & KPIs
1. [Goal]: Target [metric] by [date]
2. [Goal]: Target [metric] by [date]
3. [Goal]: Target [metric] by [date]
```

Example goals: Reach top 10 for "meditation app"; achieve 4.8 average rating; 5,000 monthly organic downloads.

**Section 6: Resources & Constraints**

```markdown
## Resources & Constraints
- Monthly ASO/Marketing Budget: $
- Team Size: [Solo / 2-3 / Small team / Agency]
- Tools in Use: [App Store Connect, Firebase, RevenueCat, etc.]
- Key Constraints: [Update frequency, team bandwidth, content limitations]
```

**Section 7: Markets**

```markdown
## Markets
- Primary Market: [Country, language]
- Secondary Markets: [Countries]
- Supported Languages: [list]
```

---

### Output

1. Save as `app-marketing-context.md` in the project root
2. Provide a summary:
   - **Key Strengths to Leverage** (2–3 bullet points)
   - **Obvious Gaps to Address** (2–3 bullet points)
   - **Recommended Next Skills** (ordered list based on what would have most impact)

### Note

This document is referenced by all other skills. Keep it updated whenever:
- The app ships a major update
- A new competitor emerges
- Goals or KPIs change
- ASO metadata is significantly revised
