---
name: localization
description: Framework for expanding globally through App Store localization — market prioritization, keyword research by locale, and cultural adaptation strategy
type: user-invocable
---

## Methodology

**Localization** — Expand globally by localizing App Store presence for each target market.

**Critical Principle:** Don't translate English keywords directly. Run separate keyword research for each target market. Search behavior differs significantly by language and culture.

> Example: German users search "Haushaltsbuch" (household book), not "budget tracker." Japanese users search by brand once brands establish trust. Brazilian users are mobile-first and price-sensitive.

### Market Prioritization Framework

Score each target market and prioritize:

| Factor | Weight | Notes |
|--------|--------|-------|
| Market size | 30% | App Store revenue by country |
| Competition level | 25% | Lower competition = easier opportunity |
| Localization effort | 20% | Language complexity, cultural gap |
| Revenue potential | 15% | Category monetization in that market |
| Strategic fit | 10% | Alignment with product roadmap |

**Tier 1 Markets (highest priority):**
- United States (en-US) — default, largest market
- Germany (de-DE) — highest revenue per user in Europe
- Japan (ja-JP) — high ARPU, unique ASO behavior
- Brazil (pt-BR) — largest market by download volume in LatAm

**Tier 2 Markets:**
- United Kingdom, France, Australia, Canada, South Korea, Mexico, Italy, Spain

### Localization Scope

| Element | Required | Notes |
|---------|----------|-------|
| App Store title | Yes | 30 chars, must use local keywords |
| Subtitle | Yes | Local secondary keywords |
| Keyword field | Yes | Run fresh research per market |
| Description | Yes | Adapt tone and cultural references |
| Screenshots | Yes | Localized text overlays on screenshots |
| Preview video | Optional | High impact, high effort |
| In-app UI | Yes (eventually) | Required for full conversion |

### Keyword Research by Locale

For each target market:

1. **Identify seed keywords** in the local language (use native speaker input or translation as starting point only)
2. **Validate with search behavior** — check that locals actually use those terms (Google Trends, App Store suggest)
3. **Analyze competitor metadata** in that locale — what are top-ranked local apps using?
4. **Check keyword volume** — use Apple Search Ads in that country to see relative popularity

Common pitfalls:
- Machine translation of keywords produces unnatural phrases locals don't search
- Brand names that work in English may have different connotations in other languages
- Length constraints differ when translated (German words are often much longer)

### Cultural Adaptation

| Market | Tone | Key Considerations |
|--------|------|-------------------|
| Germany | Formal, precise | Data privacy is paramount; highlight security |
| Japan | Polite, detail-oriented | Credential/authority signals matter; manga/anime aesthetic can work |
| Brazil | Warm, informal | Price sensitivity high; social proof from Brazilian users preferred |
| France | Sophisticated | Francophones use French-language apps strongly; partial localization underperforms |
| South Korea | Technology-forward | High expectations for polish and features |

### Implementation Phases

**Phase 1: Research (Week 1–2)**
- Market scoring exercise
- Top 2–3 target market selection
- Competitor metadata audit in each locale
- Native speaker keyword research

**Phase 2: Create Localized Assets (Week 2–4)**
- Translate and adapt metadata with ASO-aware native speakers (not just translators)
- Create localized screenshot text overlays
- Cultural review of imagery (no culturally inappropriate photos)

**Phase 3: Launch and Monitor**
- Submit to App Store (separate metadata per locale in App Store Connect)
- Monitor keyword rankings in each country (add to tracking config)
- Monitor conversion rates by country (App Store Connect → Sources → by territory)
- Iterate based on ranking performance

### Success Signals

| Metric | 4-Week Target |
|--------|--------------|
| Keyword ranking improvement (new market) | Top 20 on primary keywords |
| CVR (localized market) | ≥ CVR in English-language markets |
| Downloads from new market | 15%+ of total downloads |
