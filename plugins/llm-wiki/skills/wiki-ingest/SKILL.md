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

## Step 2.5: Convert PDF (if applicable)

If the source file has a `.pdf` extension, convert it to markdown before reading:

```bash
${CLAUDE_PLUGIN_ROOT}/.venv/bin/python ${CLAUDE_PLUGIN_ROOT}/scripts/pdf_to_md.py <source-path>
```

Capture the path printed to stdout — this is the `.md` file to use in all subsequent steps.

If the venv is not set up yet, tell the user:
> "Run `bash <path-to-llm-wiki-plugin>/setup_venv.sh` first to install PDF dependencies, then retry."

If the source is not a `.pdf`, skip this step entirely.

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
