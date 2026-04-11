---
name: wiki-init
description: Bootstrap the personal wiki vault at ~/Documents/wiki/ and migrate all existing Claude memory files into it. Run once.
---

# wiki-init — Bootstrap the Wiki

One-time setup. Creates the vault structure, writes the schema, and migrates all existing per-project memory files.

## Step 1: Scaffold vault directories

```bash
mkdir -p ~/Documents/wiki/{ideas,lessons,projects,markets,sources,assets}
```

Confirm creation:
```bash
ls ~/Documents/wiki/
```
Expected: `assets  ideas  lessons  markets  projects  sources` (CLAUDE.md, index.md, log.md are written in the following steps)

## Step 2: Write vault schema (~/Documents/wiki/CLAUDE.md)

Write the following exactly to `~/Documents/wiki/CLAUDE.md`:

```markdown
# Wiki Schema

This file defines how Claude maintains the wiki. Follow these conventions exactly on every write.

## Directory Guide

| Directory | What goes here |
|-----------|----------------|
| `ideas/` | Raw ideas captured during sessions — half-formed is fine |
| `lessons/` | Lessons learned: technical decisions, strategic insights, process improvements, Claude behavior feedback |
| `projects/` | One page per project/repo — cross-session context, goals, current state |
| `markets/` | Market observations, competitive intel, trends, product opportunities |
| `sources/` | Summaries of external articles, papers, docs, podcasts |
| `assets/` | Downloaded images only — not markdown |

Root pages (`~/Documents/wiki/*.md`) are reserved for: CLAUDE.md (this file), index.md, log.md, and a user profile page.

## Page Template

Every wiki page uses this structure:

```
---
tags: [<type>]
updated: YYYY-MM-DD
---

# Title

> One-line summary (also used verbatim in index.md)

Body content. Use [[wikilinks]] when referencing other pages in the vault.

## Related
- [[path/to/related-page]]
```

Valid tags: `idea`, `lesson`, `project`, `market`, `source`, `user`

## Wikilink Rules

- Use `[[filename-without-extension]]` or `[[folder/filename]]` to link pages
- Obsidian resolves by filename — use the exact filename without path when unambiguous
- Link when a reference is substantive (the relationship matters). Do NOT link for passing mentions.
- When creating a page, check index.md for related pages and add links in both directions

## index.md Format

Organized by directory. One line per page:

```
## Ideas
- [[ideas/idea-name]] — one-line summary

## Lessons
- [[lessons/lesson-name]] — one-line summary

## Projects
- [[projects/project-name]] — one-line summary

## Markets
- [[markets/market-name]] — one-line summary

## Sources
- [[sources/source-name]] — one-line summary
```

Update index.md on every write — add new entries, update changed summaries.

## log.md Format

Append-only. Never edit past entries. Each entry:

```
## [YYYY-MM-DD] <type> | <title>

Brief note on what was added/changed and why.
```

Types: `init`, `ingest`, `idea`, `lesson`, `project`, `market`, `query`, `lint`

## Proactive Logging

Log something when it passes the "worth reading in 6 months?" test:
- A non-obvious technical or architectural decision ("chose X over Y because Z")
- A market or product insight discovered during research
- A lesson from a failure, workaround, or unexpected discovery
- An idea worth preserving before it disappears into chat history
- New information about a project that changes its context page

Do NOT log: routine commands, typo fixes, mundane status updates, things derivable from git history.

Threshold is **high**. Signal-dense over comprehensive.

When logging proactively, announce to the user: `Logging to wiki: [title]` — then do it without asking permission.

## Session Start Behavior

When starting a session in a repo, check `~/Documents/wiki/projects/<repo-name>.md`. If it exists, read it for context before beginning work. This replaces per-project Claude memory.
```

## Step 3: Write index.md

Write to `~/Documents/wiki/index.md`:

```markdown
# Wiki Index

Catalog of all pages. Updated on every write.

## Ideas

## Lessons

## Projects

## Markets

## Sources
```

## Step 4: Write log.md

Write to `~/Documents/wiki/log.md`:

```markdown
# Wiki Log

Append-only chronological record. Format: `## [YYYY-MM-DD] type | title`

## [<TODAY>] init | Wiki bootstrapped

Initial vault scaffold created. Memory migration follows.
```

Replace `<TODAY>` with today's date in YYYY-MM-DD format.

## Step 5: Migrate existing Claude memory files

Scan all project memory directories:
```bash
find ~/.claude/projects -name "*.md" ! -name "MEMORY.md" | sort
```

For each file found:

1. Read the file and extract its frontmatter `type` field and body content
2. Map type to vault directory:
   - `feedback` → `lessons/`
   - `project` → `projects/`
   - `reference` → `sources/`
   - `user` → write as root-level `user-profile.md`
3. Derive the source project name from the directory path:
   - Take the last hyphen-separated segment (e.g., `Good-Morning` from `-Users-hagenkaiser-Code-GoodMorning-Good-Morning`, or `Throwdown` from `-Users-hagenkaiser-Code-Throwdown`)
   - Convert hyphens to spaces → human-readable name (`Good Morning`, `Throwdown`)
   - For the wiki page filename: lowercase with hyphens (e.g., `good-morning`)
4. The new wiki page filename follows the pattern: `<project-slug>-<original-name-without-type-prefix>.md`
   - Strip the type prefix from the original filename (`feedback_`, `project_`, `reference_`)
   - Replace underscores with hyphens
   - Prepend the project slug
   - Example: `feedback_backward_compat.md` in GoodMorning project → `good-morning-backward-compat.md`
5. Write a new vault page using the page template (preserve the original content in the body, add `tags`, `updated` from today, and add `## Related` section linking to the project page: `- [[projects/<project-slug>]]`)
6. Add wikilinks to the project page if the memory file belongs to a known project (create the project page stub if needed)

After all migrations:
- Update `index.md` with all migrated pages
- Append a log entry for the migration

Example migration — source file:
```
~/.claude/projects/-Users-hagenkaiser-Code-GoodMorning-Good-Morning/memory/feedback_backward_compat.md
```

Becomes:
```
~/Documents/wiki/lessons/good-morning-backward-compat.md
```

With content:
```markdown
---
tags: [lesson]
updated: 2026-04-11
---

# Backward Compatibility for Released Clients

> All API and schema changes must be additive — never break existing released iOS clients.

All changes to the worker API and database schema must be backward-compatible with currently released iOS clients.

**Why:** Good Morning is live on the App Store with active users. Breaking changes to the API would cause existing clients to fail, and users can't be forced to update instantly.

**How to apply:**
- New API endpoints only — never modify existing request/response schemas
- New DB columns must have defaults or be nullable
- New StoreKit products are additive — don't modify existing product behavior
- New SwiftData fields must be optional (`Type?`) to avoid crash on existing databases
- Deploy worker changes first, verify, then release the iOS update

## Related
- [[projects/good-morning]]
```

## Step 6: Announce completion

After all steps complete, tell the user:

> "Wiki initialized at `~/Documents/wiki/`. Migrated N memory files from M projects. Open Obsidian and point it at `~/Documents/wiki/` to browse. Run `/wiki-lint` anytime to health-check the vault."
