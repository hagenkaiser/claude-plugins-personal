# wiki-ingest — Design Spec

**Date:** 2026-04-11
**Status:** Approved design, ready for implementation planning

---

## Context

The llm-wiki plugin (built earlier this session) handles logging during work sessions but lacks a source ingestion layer. The original LLM Wiki concept describes three layers: raw sources, wiki, and schema. Only the wiki and schema layers were built. This spec adds the missing raw sources layer and a `wiki-ingest` skill to process external documents (articles, PDFs, web clips, notes) into the wiki with entity tracking.

---

## Vault Structure Changes

Two new directories added to `~/Documents/wiki/`:

```
~/Documents/wiki/
  raw/              ← immutable source files (articles, PDFs, clipped pages, notes)
  entities/         ← entity pages (people, companies, technologies, concepts)
  ideas/            (existing)
  lessons/          (existing)
  projects/         (existing)
  markets/          (existing)
  sources/          (existing — summaries of ingested raw sources)
  assets/           (existing)
  CLAUDE.md         ← schema updated with raw/ and entities/ sections
  index.md          ← updated with entities/ section
  log.md            (existing)
```

`raw/` is read-only from the wiki's perspective — Claude never writes there, only reads. You drop files in (or save Obsidian Web Clipper output there), Claude processes them. Subdirectories in `raw/` are fine (e.g. `raw/articles/`, `raw/pdfs/`).

The vault `CLAUDE.md` schema gets two new sections added:
- `raw/` explanation (immutable, source of truth)
- `entities/` explanation + entity page template

`index.md` gets a new `## Entities` section.

---

## Plugin Changes

One new skill added to `plugins/llm-wiki/`:

```
plugins/llm-wiki/skills/wiki-ingest/SKILL.md    ← new
```

No other plugin files change.

---

## wiki-ingest Skill Workflow

### Invocation

User invokes `/wiki-ingest` (or says "ingest this"). Claude asks:
1. Which source? (path or filename from `~/Documents/wiki/raw/`)
2. Discuss-first or auto-process?

### Discuss Mode

1. Read the source file
2. Present 3–5 key takeaways
3. Ask: "Anything to add, correct, or emphasize before I file this?"
4. Incorporate feedback
5. Write to wiki (see below)

### Auto Mode

1. Read the source file
2. Write to wiki immediately
3. Report: "Filed: [[sources/slug]], updated N entity pages"

### Writing to Wiki (both modes)

**Step 1: Write summary page** to `sources/<slugified-title>.md`

Template:
```markdown
---
tags: [source, <type>]
updated: YYYY-MM-DD
source-path: raw/<filename>
source-type: article | pdf | note | clip
---

# <Title>

> <One-line summary>

## Key Points
- <point>
- <point>

## Entities
- [[entities/<entity>]] — <what this source says about it>

## Related
- [[lessons/...]]
- [[projects/...]]
- [[markets/...]]
```

Valid source types: `article`, `pdf`, `note`, `clip`

**Step 2: Identify entities** — people, companies, technologies, concepts worth tracking independently. Heuristic: flag anything that recurs in the source or is substantive enough to be referenced again in future sources.

**Step 3: For each entity:**
- If `entities/<name>.md` exists: read it, append new findings to body, add source to its Sources section
- If new: create entity page stub (see template below)
- Add wikilink back to this summary in the entity's Sources section

**Step 4: Bidirectional wikilinks** — summary page links to all entities; each entity page links back to summary

**Step 5: Update index.md** — add summary to `## Sources` section; add any new entities to `## Entities` section

**Step 6: Append to log.md**
```
## [YYYY-MM-DD] ingest | <Source Title>

<One sentence: what type of source, what it covers, how many entities updated.>
```

---

## Entity Page Template

```markdown
---
tags: [entity, <person|company|technology|concept>]
updated: YYYY-MM-DD
---

# <Entity Name>

> <One-line description>

<Body: what we know — description, key facts, current understanding. Grows with each source.>

## Sources
- [[sources/<slug>]] — <what this source said about this entity>

## Related
- [[entities/<related>]]
- [[markets/...]]
```

Entity pages start as stubs and compound with every ingest that mentions them. That's the core mechanic.

---

## Vault CLAUDE.md Additions

Append two sections to `~/Documents/wiki/CLAUDE.md`:

```markdown
## raw/ Directory

`raw/` contains immutable source files — articles, PDFs, markdown clips, personal notes. Claude reads from here, never writes. Drop files here to queue them for ingestion.

## entities/ Directory

Entity pages track recurring people, companies, technologies, and concepts across all sources. Each entity page is enriched by every source that mentions it. Use tags `[entity, person]`, `[entity, company]`, `[entity, technology]`, or `[entity, concept]`.

When ingesting a source, identify entities heuristically: flag anything that recurs in the source or is substantive enough to be referenced again in future sources. Create a stub page for new entities; update existing ones.

Entity page template: see wiki-ingest skill.
```

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `plugins/llm-wiki/skills/wiki-ingest/SKILL.md` | Create |
| `~/Documents/wiki/raw/` | Create directory |
| `~/Documents/wiki/entities/` | Create directory |
| `~/Documents/wiki/CLAUDE.md` | Append raw/ and entities/ sections |
| `~/Documents/wiki/index.md` | Add `## Entities` section |

---

## Verification

1. Drop a markdown article into `~/Documents/wiki/raw/`
2. Invoke `wiki-ingest`, choose discuss mode
3. Confirm: key takeaways presented, user can give feedback
4. Confirm: `sources/<slug>.md` created with correct frontmatter and entity links
5. Confirm: entity pages created in `entities/` with source backlinks
6. Confirm: `index.md` updated with new source and entity entries
7. Confirm: `log.md` has ingest entry
8. Ingest a second source mentioning the same entity — confirm entity page is updated (not duplicated), source count grows
9. Open Obsidian graph view — confirm source pages link to entity pages and back
