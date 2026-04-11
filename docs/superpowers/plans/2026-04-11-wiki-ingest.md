# wiki-ingest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add source ingestion to the llm-wiki plugin — a `wiki-ingest` skill that processes files from `~/Documents/wiki/raw/` into summary pages, entity pages, wikilinks, and log entries.

**Architecture:** One new skill file in the existing plugin. Two new vault directories (`raw/`, `entities/`). Two existing vault files updated (CLAUDE.md schema, index.md). No other plugin files change.

**Tech Stack:** Markdown, Obsidian wikilinks, YAML frontmatter, bash for directory scaffolding.

---

## File Map

| File | Action |
|------|--------|
| `~/Documents/wiki/raw/` | Create directory |
| `~/Documents/wiki/entities/` | Create directory |
| `~/Documents/wiki/CLAUDE.md` | Append `raw/` and `entities/` sections |
| `~/Documents/wiki/index.md` | Add `## Entities` section |
| `plugins/llm-wiki/skills/wiki-ingest/SKILL.md` | Create |

---

## Task 1: Scaffold Vault + Update Schema

**Files:**
- Create: `~/Documents/wiki/raw/`
- Create: `~/Documents/wiki/entities/`
- Modify: `~/Documents/wiki/CLAUDE.md` (append two sections)
- Modify: `~/Documents/wiki/index.md` (add `## Entities` section)

Note: these are vault files outside the git repo — no commit for this task.

- [ ] **Step 1: Create directories**

```bash
mkdir -p ~/Documents/wiki/raw
mkdir -p ~/Documents/wiki/entities
```

Verify:
```bash
ls ~/Documents/wiki/
```
Expected output includes `entities` and `raw` alongside existing dirs.

- [ ] **Step 2: Append to ~/Documents/wiki/CLAUDE.md**

The current file ends at line 99 (`...This replaces per-project Claude memory.`). Append the following after the last line:

```markdown

## raw/ Directory

`raw/` contains immutable source files — articles, PDFs, markdown clips, personal notes. Claude reads from here, never writes. Drop files here to queue them for ingestion via wiki-ingest.

Subdirectories are allowed (e.g. `raw/articles/`, `raw/pdfs/`).

## entities/ Directory

Entity pages track recurring people, companies, technologies, and concepts across all sources. Each entity page is enriched by every source that mentions it.

Valid entity tags: `[entity, person]`, `[entity, company]`, `[entity, technology]`, `[entity, concept]`

Entity page template:

```
---
tags: [entity, <person|company|technology|concept>]
updated: YYYY-MM-DD
---

# Entity Name

> One-line description

Body: what we know — description, key facts, current understanding. Grows with each ingest.

## Sources
- [[sources/<slug>]] — what this source said about this entity

## Related
- [[entities/<related>]]
```

When ingesting a source, identify entities heuristically: flag anything that recurs in the source or is substantive enough to be referenced again in future sources. Create a stub for new entities; update existing ones.
```

- [ ] **Step 3: Verify CLAUDE.md has both new sections**

```bash
grep -n "raw/ Directory\|entities/ Directory" ~/Documents/wiki/CLAUDE.md
```
Expected: two matching lines with their line numbers.

- [ ] **Step 4: Add ## Entities section to index.md**

The current `index.md` ends with the `## Sources` section (around line 59). Add a new section after `## Sources`:

```markdown

## Entities

```

The `## Entities` section starts empty — entries are added by wiki-ingest as entities are created.

- [ ] **Step 5: Verify index.md has Entities section**

```bash
grep -n "## Entities" ~/Documents/wiki/index.md
```
Expected: one matching line.

---

## Task 2: wiki-ingest SKILL.md

**Files:**
- Create: `plugins/llm-wiki/skills/wiki-ingest/SKILL.md`

- [ ] **Step 1: Create wiki-ingest/SKILL.md**

Create file at `plugins/llm-wiki/skills/wiki-ingest/SKILL.md` with this exact content:

```markdown
---
name: wiki-ingest
description: Ingest a source file from ~/Documents/wiki/raw/ into the wiki. Writes a summary page, identifies and updates entity pages, maintains bidirectional wikilinks, updates index and log.
---

# wiki-ingest — Ingest a Source

Process an external source (article, PDF, web clip, personal note) into the wiki. Creates a summary page in `sources/`, identifies entities and updates their pages in `entities/`, and keeps index and log current.

## Step 1: Identify the source

Ask: "Which file do you want to ingest?"

List available files if the user isn't sure:
```bash
find ~/Documents/wiki/raw -type f | sort
```

## Step 2: Choose mode

Ask: "Discuss-first (I summarize, we talk, then file) or auto-process (file immediately)?"

## Step 3: Read the source

Read the full source file. Determine:
- **Title**: from the document's heading, or derive from filename if no heading
- **Type**: `article` / `pdf` / `note` / `clip`
- **Slug**: kebab-case of title (e.g. "Apple Search Ads Overview" → `apple-search-ads-overview`)
- **Target path**: `~/Documents/wiki/sources/<slug>.md`

## Step 4a: Discuss mode

Present 3–5 key takeaways:

> "Key takeaways from [Title]:
> 1. ...
> 2. ...
> 3. ...
>
> Anything to add, correct, or emphasize before I file this?"

Incorporate user feedback into the summary, then continue to Step 5.

## Step 4b: Auto mode

Skip to Step 5 immediately.

## Step 5: Identify entities

From the source, identify entities worth tracking — people, companies, technologies, concepts.

Heuristic — flag an entity when it:
- Appears multiple times in the source, OR
- Is specific enough to be referenced in future sources (named tools, companies, frameworks, concepts with their own body of knowledge)

Do NOT flag: generic terms ("API", "user", "database"), passing one-off mentions.

For each entity:
- Determine type: `person` / `company` / `technology` / `concept`
- Derive slug: kebab-case of name (e.g. "Apple Search Ads" → `apple-search-ads`)

Check which entities already have pages:
```bash
ls ~/Documents/wiki/entities/ 2>/dev/null || echo "empty"
```

## Step 6: Write summary page

Write to `~/Documents/wiki/sources/<slug>.md`:

```
---
tags: [source, <article|pdf|note|clip>]
updated: <YYYY-MM-DD>
source-path: raw/<filename>
source-type: <article|pdf|note|clip>
---

# <Title>

> <One-line summary of what this source covers>

## Key Points
- <key point>
- <key point>
- <key point>

## Entities
- [[entities/<entity-slug>]] — <what this source says about this entity>

## Related
- [[<lessons/projects/markets/ideas page if directly relevant>]]
```

Include only truly relevant pages in Related — don't link everything, just where the relationship is substantive.

## Step 7: Create or update entity pages

For each entity from Step 5:

**If `~/Documents/wiki/entities/<entity-slug>.md` exists:**
1. Read the existing page
2. Integrate new findings from this source into the body — add information, don't replace existing content
3. Add to Sources section: `- [[sources/<slug>]] — <one sentence on what this source said>`
4. Update `updated:` date in frontmatter to today

**If entity is new:**
Write `~/Documents/wiki/entities/<entity-slug>.md`:

```
---
tags: [entity, <person|company|technology|concept>]
updated: <YYYY-MM-DD>
---

# <Entity Name>

> <One-line description>

<Body: what this source says about the entity. Future ingests will add more.>

## Sources
- [[sources/<slug>]] — <one sentence on what this source said>

## Related
```

## Step 8: Update wikilinks bidirectionally

Summary → entities is already done via the Entities section in Step 6.

Ensure each entity page links back — Sources section in Step 7 handles this.

Optionally: check if any existing wiki pages (lessons, projects, markets, ideas) mention this topic and should now link to the new summary. Add `[[sources/<slug>]]` to their Related section only if the connection is direct and meaningful.

## Step 9: Update index.md

Add to `## Sources` section of `~/Documents/wiki/index.md`:
```
- [[sources/<slug>]] — <one-line summary>
```

For each new entity page, add to `## Entities` section:
```
- [[entities/<entity-slug>]] — <one-line description>
```

For updated entity pages: update their one-liner in `## Entities` if it changed.

## Step 10: Append to log.md

Append to `~/Documents/wiki/log.md`:

```
## [<YYYY-MM-DD>] ingest | <Source Title>

<type> from raw/<filename>. <N> entities (N new, N updated): <entity names>. <One sentence on the key insight worth keeping.>
```

## Step 11: Report to user

> "Ingested: [[sources/<slug>]]
> Entities: [[entities/X]] (new), [[entities/Y]] (updated)
> Related pages linked: <list or 'none'>"
```

- [ ] **Step 2: Verify file was written**

```bash
wc -l plugins/llm-wiki/skills/wiki-ingest/SKILL.md
```
Expected: at least 120 lines.

```bash
grep -c "^## Step" plugins/llm-wiki/skills/wiki-ingest/SKILL.md
```
Expected: `11`

- [ ] **Step 3: Commit**

```bash
git add plugins/llm-wiki/skills/wiki-ingest/SKILL.md
git commit -m "feat: add wiki-ingest skill — source ingestion with entity tracking"
```

---

## Task 3: Verify End-to-End

- [ ] **Step 1: Create a test source file**

```bash
cat > ~/Documents/wiki/raw/test-article.md << 'EOF'
# Apple Search Ads: A Practical Guide

Apple Search Ads (ASA) is Apple's paid user acquisition platform for the App Store.

## Key Points

Apple Search Ads offers two tiers: Basic (automated, limited control) and Advanced (full keyword and bid control). Advanced is recommended for serious UA campaigns.

Keywords in ASA fall into three match types: exact, broad, and search match. Exact match gives the most control; search match is fully automated.

Cost-per-tap (CPT) and cost-per-acquisition (CPA) are the primary metrics. Industry average CPA for productivity apps is $3–8.

Apple's attribution API (SKAdNetwork) limits conversion data but ASA provides first-party attribution that bypasses iOS privacy restrictions.

## Tools

- MMP (Mobile Measurement Partner): tracks installs beyond ASA dashboard
- Apple Ads API: programmatic campaign management

EOF
```

- [ ] **Step 2: Invoke wiki-ingest in discuss mode**

Tell Claude: "ingest `~/Documents/wiki/raw/test-article.md`" and choose discuss mode.

Verify Claude:
- Lists 3–5 key takeaways from the article
- Asks for feedback before filing

- [ ] **Step 3: Confirm output after filing**

```bash
ls ~/Documents/wiki/sources/ | grep apple
```
Expected: `apple-search-ads-a-practical-guide.md` (or similar slug)

```bash
ls ~/Documents/wiki/entities/
```
Expected: at least `apple-search-ads.md`, likely also `skadnetwork.md` or similar

```bash
grep "apple-search-ads" ~/Documents/wiki/index.md
```
Expected: entry in `## Sources` and at least one in `## Entities`

```bash
tail -10 ~/Documents/wiki/log.md
```
Expected: ingest entry for the test article

- [ ] **Step 4: Ingest the same source again (idempotency check)**

Tell Claude: "ingest `~/Documents/wiki/raw/test-article.md`" again in auto mode.

Verify Claude updates existing entity pages rather than creating duplicates — entity source list should have one entry per source, not two.

- [ ] **Step 5: Clean up test file (optional)**

```bash
rm ~/Documents/wiki/raw/test-article.md
# Also remove test pages if you want a clean slate:
# rm ~/Documents/wiki/sources/apple-search-ads-*.md
# rm ~/Documents/wiki/entities/apple-search-ads.md
```

---

## Verification Summary

| Check | Command | Pass Condition |
|-------|---------|----------------|
| Directories exist | `ls ~/Documents/wiki/` | `entities` and `raw` visible |
| Schema updated | `grep -c "raw/ Directory\|entities/ Directory" ~/Documents/wiki/CLAUDE.md` | `2` |
| Index updated | `grep "## Entities" ~/Documents/wiki/index.md` | Match found |
| Skill created | `wc -l plugins/llm-wiki/skills/wiki-ingest/SKILL.md` | 120+ lines |
| All 11 steps | `grep -c "^## Step" plugins/llm-wiki/skills/wiki-ingest/SKILL.md` | `11` |
| Source page created | `ls ~/Documents/wiki/sources/` | Test article slug present |
| Entity pages created | `ls ~/Documents/wiki/entities/` | ≥1 entity from test article |
| Wikilinks bidirectional | Read source page + entity page | Each links to the other |
| Log updated | `tail -5 ~/Documents/wiki/log.md` | Ingest entry present |
