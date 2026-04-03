---
name: ab-test-store-listing
description: Design, run, and interpret App Store A/B tests (Product Page Optimization) improving conversion rate with statistical rigor
type: user-invocable
---

## Methodology

**A/B Test Store Listing** — Systematically improve App Store conversion rate through rigorous testing.

### What Can Be Tested

**Via Product Page Optimization (PPO) — Apple's native A/B test tool:**
- App icon (up to 3 variants)
- Screenshots (up to 3 variants)
- App preview video (up to 3 variants)

**Cannot be tested via PPO:**
- App title
- Subtitle
- Description
- Keyword field

**Custom Product Pages (CPP):** 35 pages per app, each with unique screenshots, videos, and promotional text. These are not A/B tests — they're used to route specific paid traffic (e.g., ad campaigns) to tailored pages.

### PPO Mechanics

- Only applies to **organic traffic** (not paid)
- Minimum **90% confidence** threshold required (Apple shows the winner)
- Tests run **7–90 days**
- One test at a time per app
- Apple handles traffic splitting automatically
- Minimum viable test: 1,000+ impressions per variant

### Test Prioritization

Run in this order (Impact × Effort):

| Test | Impact | Effort | Priority |
|------|--------|--------|----------|
| First screenshot (hero) | Very High | Medium | 1st |
| App icon | High | Medium | 2nd |
| Screenshot order | Medium | Low | 3rd |
| Screenshot style | Medium | High | 4th |
| App preview video | Medium | High | 5th |

### Test Design Framework

**1. Write a Hypothesis**
> "If we [specific change], then [metric — CVR/TTR/page views] will [increase/decrease] because [reason based on user psychology]."

Example: "If we change the first screenshot from a feature showcase to a social proof image (4.8 stars, 50K reviews), then CVR will increase because new users are uncertain about quality."

**2. Design Variants**

Rules:
- Change **one variable** per test (otherwise you can't isolate cause)
- Design 2 variants max in most cases (control + challenger)
- Document what exactly is different in each variant

**3. Calculate Required Sample Size and Duration**

Rules of thumb:
| Daily Impressions | Minimum Duration |
|-------------------|-----------------|
| < 1,000 | 30–90 days |
| 1,000–5,000 | 14–30 days |
| 5,000+ | 7–14 days |

**4. Run Without Stopping Early**

The most common mistake: stopping when one variant looks like it's winning after only a few days. This produces false positives. Let the test reach 90%+ confidence before concluding.

### Test Ideas

**Icon Tests:**
- Color scheme (e.g., blue vs. orange background)
- Style (flat vs. illustrated vs. 3D)
- Main element (character vs. abstract mark)
- Dark vs. light background

**Screenshot Tests:**
- First screenshot: benefit statement vs. social proof vs. problem/solution
- Text size: large headline vs. small caption
- Dark mode vs. light mode screenshots
- With vs. without device mockup frame
- Screenshot order (feature priority)

**Video Tests:**
- With preview video vs. without
- Different hook in first 3 seconds

### Interpreting Results

**Is it significant?** Did it reach 90%+ confidence?

**What's the actual lift?** Not just "winner" — what's the % improvement and confidence interval?
- Example: "Variant B improved CVR by +12% (±3%, 94% confidence)"

**Segment differences?** Check if the winner varies by country or source (sometimes a test wins in US but loses in other markets).

**Annual impact estimate:** (Current downloads × % CVR improvement × 365) = estimated incremental downloads per year.

**What's the next test?** Never stop testing. Once a winner is found, immediately design the next test.
