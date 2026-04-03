---
name: app-launch
description: Multi-phase app launch strategy with 8-week countdown, channel prioritization, press strategy, and post-launch optimization plan
type: user-invocable
---

## Methodology

**App Launch** — Structured multi-phase strategy for maximum first-week momentum.

**Why Launch Momentum Matters:** The App Store algorithm heavily weights first-week velocity. Strong download and rating momentum in week 1 can push an app into top charts, triggering editorial consideration and organic discovery loops.

### 8-Week Pre-Launch Plan

**8 Weeks Out**
- [ ] ASO complete: title, subtitle, keywords, description, screenshots, icon optimized
- [ ] Pre-launch landing page live with App Store link / waitlist
- [ ] Press kit assembled (icon, screenshots, preview video, founder photos, one-liner)
- [ ] Identify target journalists and publications (Tier 1, 2, 3 — see `press-and-pr`)
- [ ] Identify relevant communities (subreddits, newsletters, Discord/Slack groups)
- [ ] Beta test recruitment open (TestFlight)

**4 Weeks Out**
- [ ] Beta testing in progress; actively collecting crash and UX feedback
- [ ] Blog post or launch article drafted
- [ ] Social media content calendar built
- [ ] Product Hunt listing created (Coming Soon page)
- [ ] Apple Search Ads account set up and campaigns ready to activate
- [ ] Ratings/review flow implemented and tested

**1 Week Out**
- [ ] Final app binary submitted to App Store (leave buffer for review)
- [ ] Press embargo scheduled with interested journalists
- [ ] Paid campaigns ready to activate at launch
- [ ] Community posts drafted and scheduled
- [ ] Product Hunt hunter identified and briefed

**Launch Day**
- [ ] App Store release activated
- [ ] Press embargo lifted — articles live
- [ ] Product Hunt post live (Tuesday–Thursday preferred, 12:01am PST)
- [ ] Apple Search Ads Brand + Category campaigns activated
- [ ] Social media posts published
- [ ] Community posts published (r/iphone, relevant subreddits, Hacker News "Show HN")
- [ ] All-day engagement: reply to every Product Hunt comment, tweet, message

### Amplification Channels

**Organic (free):**
| Channel | Effort | Expected Impact |
|---------|--------|----------------|
| Product Hunt | Medium | High for dev/tech audience |
| Hacker News "Show HN" | Low | High for technical apps |
| Twitter/X launch thread | Medium | Moderate |
| Reddit (relevant subreddits) | Medium | Moderate-High |
| YouTube (app demo video) | High | Long-term SEO value |

**Paid:**
| Channel | Best For | Starting Budget |
|---------|----------|----------------|
| Apple Search Ads | Any iOS app | $500–$1,000/week |
| Meta (Facebook/Instagram) | Consumer apps | $500+/week |
| TikTok | Entertainment, lifestyle, games | $300+/week |
| Google Ads UAC | Cross-platform | $500+/week |
| Influencer partnerships | Visual/lifestyle apps | Varies |

### Post-Launch Monitoring

**Week 1 Priorities:**
- Monitor ratings daily — respond to every review
- Watch crash rate (Firebase Crashlytics + App Store Connect)
- Track keyword rankings vs. pre-launch baseline
- Monitor Apple Search Ads CVR and CPI

**Month 1 Priorities:**
- Full ASO audit (use `aso-audit` skill)
- Keyword rankings: which keywords moved up/down from launch burst?
- Review themes: what are early users praising and complaining about?
- Update metadata based on organic search terms driving downloads (App Store Connect Sources)
- Plan first major feature update (aim for Day 30)

### Success Metrics

| Metric | Week 1 Target | Month 1 Target |
|--------|-------------|---------------|
| Downloads | Top 200 in category | Organic traffic > paid |
| Rating | 4.3+ (first reviews) | 4.5+ |
| D1 Retention | > 30% | > 35% |
| ASA CVR | > 40% | > 45% |
