---
name: ua-campaign
description: Paid mobile user acquisition strategy across Apple Search Ads, Meta, TikTok, and Google — channel selection, campaign structure, and optimization cadence by budget
type: user-invocable
---

## Methodology

**UA Campaign** — Paid mobile user acquisition across major ad platforms.

### Initial Assessment

Before planning campaigns, confirm:
- Monthly budget
- Target CPI (Cost Per Install)
- Current LTV (or proxy: ARPU × average subscription months)
- Target audience (demographics, interests)
- Geographic markets
- App category

**Golden Rule:** CPI must be < LTV/3 to have a viable acquisition business. If LTV is $30, target CPI ≤ $10.

### Channel Strategy by Budget

| Monthly Budget | Recommended Channels |
|---------------|---------------------|
| ≤ $1,000 | Apple Search Ads only |
| $1,000–$5,000 | ASA + one social channel (Meta or TikTok) |
| $5,000–$20,000 | ASA + Meta + one more (Google or TikTok) |
| $20,000+ | Diversify: ASA, Meta, Google UAC, TikTok, influencer |

### Apple Search Ads (Highest Priority)

**Why prioritize ASA:** Active search intent = highest purchase intent. 30–50% tap-to-install CVR. No creative production required initially.

**Campaign Structure:**
```
Brand Campaign (exact match)
  → App name, common misspellings
  → Bid: $2–5
Category Campaign (exact + broad)
  → Generic category keywords
  → Bid: $0.80–1.50
Competitor Campaign (exact match)
  → Top 5–10 competitor names
  → Bid: $1–2
Discovery Campaign (Search Match only)
  → Finds new keywords automatically
  → Bid: $0.50–0.80
```

See `apple-search-ads` skill for detailed ASA optimization.

### Meta (Facebook/Instagram) Campaign Framework

**Three Audience Layers:**

| Layer | Audience | Notes |
|-------|----------|-------|
| Lookalike | 1–3% LAL from paying users | Highest intent, start here |
| Interest | Category + lifestyle interests | Scale layer |
| Broad | No targeting (algorithm-driven) | Scale at higher budget |

**Creative Strategy:**
- Video with strong 3-second hook performs best on Meta
- Hook options: "If you [problem]..." / "This changed how I [activity]..." / Social proof numbers
- Always test 2–3 creative variants simultaneously
- Refresh creative every 2–3 weeks or when CTR drops > 20%

**Bidding:** Start with Cost Cap at 2× target CPI. Move to Value Optimization once you have 50+ conversion events.

### Google UAC (Universal App Campaigns)

- Fully automated — provide assets (text headlines, images, videos) and Google optimizes
- Works well for apps with strong organic keyword intent
- Give at least 15 text assets, 5 image assets, 5 video assets for algorithm to optimize
- Minimum $50/day to exit learning phase

### TikTok

- Best for: entertainment, lifestyle, fitness, games
- Creative-driven: authentic-feeling UGC (user-generated content style) outperforms polished ads
- Test native-style videos with voiceover, no heavy branding
- Use Spark Ads to amplify organic content that's already performing

### Key Performance Indicators

Track the full funnel from impression to revenue:

| Metric | Formula | Target |
|--------|---------|--------|
| CTR (Click-Through Rate) | Clicks / Impressions | > 1.5% (Meta), > 5% (ASA) |
| CVR (Conversion Rate) | Installs / Clicks | > 40% (ASA), > 25% (Meta) |
| CPI | Spend / Installs | < LTV/3 |
| ROAS | Revenue / Spend | > 1.0 (break even), > 2.0 (good) |
| D7 ROAS | 7-day revenue / Spend | > 0.5 (signals future profitability) |

### Optimization Cadence

| Frequency | Action |
|-----------|--------|
| Daily | Check spend pacing vs. budget |
| Weekly | Pause underperforming keywords/ad sets; scale winners; refresh creative |
| Bi-weekly | Keyword bid adjustments; negative keyword additions |
| Monthly | Channel budget reallocation; new audience tests; creative strategy review |

### Attribution Setup

Before running paid UA, set up attribution:
- **Apple Search Ads:** Built-in reporting in ASA console
- **Other channels:** Adjust or AppsFlyer (paid) — required for multi-channel attribution
- **SKAdNetwork:** Required for iOS 14.5+ privacy compliance — configure in all SDKs

Without attribution, you cannot know which channel or creative is driving installs.
