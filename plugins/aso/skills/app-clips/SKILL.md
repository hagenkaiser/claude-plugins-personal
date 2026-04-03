---
name: app-clips
description: Plan and implement App Clips — lightweight iOS experiences that convert to full app installs at 3–5× the rate of cold organic traffic
type: user-invocable
---

## Methodology

**App Clips** — Lightweight iOS experiences (max 15MB) that launch without installing the full app. Convert at 3–5× the rate of cold organic traffic.

### Where App Clips Appear

- App Store search results (as a separate card below the full app result)
- Smart App Banners on websites
- QR codes and NFC codes (physical world)
- Safari (website visits)
- Messages (shared links)
- Maps (for location-based businesses)
- Nearby suggestions (NFC/visual codes)
- Siri suggestions (contextual)

### Best Use Cases

| Category | App Clip Experience |
|----------|-------------------|
| Food & Beverage | Menu browsing, ordering, payment |
| Retail | Product preview, purchase, try-before-install |
| Transit / Parking | Ticketing, payment |
| Fitness | Demo workout, free class preview |
| Games | Demo level (first level free) |
| Finance | Calculator, rate checker |
| Events | Ticketing, event info |

**Poor use cases:** Complex apps with no single "try this" entry point, apps requiring full sign-up for any value.

### App Store Discovery

The App Clip card appears as a **separate result** below the full app in search results:
- Labeled "App Clip" with an "Open" button (vs. "Get" for full app)
- After the user completes the App Clip experience, a banner appears: "Get the full app"
- Conversion from App Clip user → full install: typically **3–5× higher** than cold organic

**ASO Implication:** The App Clip card inherits the main app's title and description metadata. Optimizing your main App Store listing also improves App Clip discoverability.

### Technical Requirements

- Maximum binary size: **15MB** (thinned — the smallest slice, not total download)
- Sign in with Apple or Apple Pay required (no custom sign-up forms)
- No App Clip-only content (content must also exist in the full app)
- Only request essential permissions (camera/location only if core to the experience)
- **No push notifications** from an App Clip

### Multiple App Clip Experiences

Configure one experience per URL pattern in App Store Connect:

| Experience Type | Use Case | URL Pattern |
|----------------|----------|------------|
| Default | General App Store discovery | app.com/clip |
| Location | NFC/visual code at specific venue | app.com/location/venue-id |
| Campaign | Specific marketing link | app.com/promo/campaign-name |
| Feature | Deep link to specific feature | app.com/feature/name |

### App Clip Card Field Limits

| Field | Limit | Tip |
|-------|-------|-----|
| Title | 18 chars | Use action/benefit ("Order Coffee"), not app name |
| Subtitle | 13 chars | "Skip the line", "Free demo" |
| Header image | 3000×2000px | Show outcome, not app UI; must work as thumbnail |
| Action button | Custom text | "Open", "Order", "Play" — action-oriented |

### Implementation Checklist

- [ ] App Clip target added in Xcode
- [ ] Binary size verified < 15MB
- [ ] Associated Domains configured (for App Clip URL handling)
- [ ] All experiences registered in App Store Connect
- [ ] Apple Pay or Sign in with Apple implemented
- [ ] SKOverlay configured to appear after value delivery (not immediately on launch)
- [ ] Data handoff to full app on install (preserve user's progress)
- [ ] App Clip card assets uploaded for each experience

### SKOverlay (Post-Experience Install Prompt)

Show the full app install prompt **after** the user has experienced value, not at launch:
- For a demo workout: show after they complete it
- For a restaurant order: show after successful payment
- For a game demo level: show after they win (not lose)

Showing too early lowers conversion. Show at the moment of highest satisfaction.

### Metrics to Track

- App Clip sessions vs. full app installs from App Clip (conversion rate)
- Which experience URL drives most conversions
- Completion rate within the App Clip (did they get to the value moment?)
- D7 retention of users who came through App Clip vs. other sources
