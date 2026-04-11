---
name: wiki-log
description: Add an entry to the personal wiki. Used both proactively (Claude decides) and explicitly (user asks). Creates or updates pages, maintains wikilinks, updates index and log.
---

# wiki-log — Log to the Wiki

Used two ways:
- **Proactively**: Claude notices something worth filing during normal work and logs it without being asked
- **Explicitly**: User says "log this", "add this to the wiki", "remember this", etc.

Proactive trigger — log when it passes the "worth reading in 6 months?" test:
- Non-obvious technical or architectural decision ("chose X over Y because Z")
- Market or product insight discovered during research
- Lesson from a failure, workaround, or unexpected discovery
- Idea worth preserving before it disappears
- New information about a project that changes its context page

When logging proactively, announce first: `Logging to wiki: [title]` — then proceed without asking permission.

## Step 1: Classify the entry

Determine:
- **Type**: `idea` / `lesson` / `project` / `market` / `source`
- **Title**: short, descriptive, will become the filename
- **Filename**: kebab-case of title (e.g., "SwiftUI animation trick" → `swiftui-animation-trick`)
- **Target directory**: based on type (see vault CLAUDE.md schema at `~/Documents/wiki/CLAUDE.md`)
- **Full path**: `~/Documents/wiki/<directory>/<filename>.md`

## Step 2: Read index.md

```bash
cat ~/Documents/wiki/index.md
```

Identify any existing pages related to this entry. Note their paths for linking.

## Step 3: Check if page exists

```bash
ls ~/Documents/wiki/<directory>/<filename>.md 2>/dev/null || echo "new"
```

**If exists**: read the page, then integrate new information into the body, update the `updated:` date in frontmatter. Preserve existing content — add, don't replace.

**If new**: create the page using the template from vault CLAUDE.md.

## Step 4: Write the page

New page template:
```
---
tags: [<type>]
updated: <YYYY-MM-DD>
---

# <Title>

> <One-line summary>

<Body content>

## Related
<wikilinks to related pages>
```

For lessons, structure the body as:
- What happened / what was learned
- **Why it matters:**
- **How to apply:**

For project pages, structure as:
- What the project is (one paragraph)
- Current state / goals
- Key decisions made
- Open questions

## Step 5: Update wikilinks bidirectionally

For each related page identified in Step 2:
1. Read that page
2. If it doesn't already link to the new/updated page, add `[[new-page]]` to its Related section
3. Write the updated page back

## Step 6: Append to log.md

Append to `~/Documents/wiki/log.md`:

```
## [<YYYY-MM-DD>] <type> | <Title>

<One sentence describing what was added and why it's worth keeping.>
```

## Step 7: Update index.md

Add or update the entry for this page in the correct section of `~/Documents/wiki/index.md`:

```
- [[<directory>/<filename>]] — <one-line summary>
```

If the entry already exists (updating a page), update its summary line if the summary changed.
