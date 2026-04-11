# LLM Wiki Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 4-skill Claude Code plugin (`llm-wiki`) that creates and maintains a persistent, Obsidian-backed personal knowledge base at `~/Documents/wiki/`, replacing the existing per-project flat-file memory system.

**Architecture:** Four skills — `wiki-init` (bootstrap + migrate), `wiki-log` (ingest/log), `wiki-query` (search/synthesize), `wiki-lint` (health check) — define how Claude operates the vault. The vault itself is a plain Obsidian markdown directory. No scripts; skill files are the entire interface.

**Tech Stack:** Markdown, Obsidian wikilinks (`[[page]]`), YAML frontmatter, bash for vault scaffolding during init.

---

## File Map

| File | Action |
|------|--------|
| `plugins/llm-wiki/.claude-plugin/plugin.json` | Create |
| `plugins/llm-wiki/skills/wiki-init/SKILL.md` | Create |
| `plugins/llm-wiki/skills/wiki-log/SKILL.md` | Create |
| `plugins/llm-wiki/skills/wiki-query/SKILL.md` | Create |
| `plugins/llm-wiki/skills/wiki-lint/SKILL.md` | Create |
| `.claude-plugin/marketplace.json` | Modify (add llm-wiki entry) |
| `~/.claude/CLAUDE.md` | Modify (add wiki awareness) |

The vault at `~/Documents/wiki/` is created by *running* the `wiki-init` skill — it is not scaffolded by this plan directly.

---

## Task 1: Plugin Manifest + Marketplace Registration

**Files:**
- Create: `plugins/llm-wiki/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create plugin.json**

Create file at `plugins/llm-wiki/.claude-plugin/plugin.json`:

```json
{
  "name": "llm-wiki",
  "version": "1.0.0",
  "description": "Maintain a persistent, Obsidian-backed personal knowledge base — capturing ideas, lessons, and cross-project context across all work sessions.",
  "author": {
    "name": "Hagen Kaiser"
  }
}
```

- [ ] **Step 2: Register in marketplace.json**

In `.claude-plugin/marketplace.json`, add to the `"plugins"` array (after the `"aso"` entry):

```json
    {
      "name": "llm-wiki",
      "description": "Maintain a persistent, Obsidian-backed personal knowledge base — capturing ideas, lessons, and cross-project context across all work sessions.",
      "version": "1.0.0",
      "author": {
        "name": "Hagen Kaiser"
      },
      "source": "./plugins/llm-wiki",
      "category": "productivity"
    }
```

- [ ] **Step 3: Verify JSON is valid**

Run:
```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('valid')"
```
Expected: `valid`

- [ ] **Step 4: Commit**

```bash
git add plugins/llm-wiki/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "feat: add llm-wiki plugin manifest and marketplace registration"
```

---

## Task 2: wiki-init Skill

**Files:**
- Create: `plugins/llm-wiki/skills/wiki-init/SKILL.md`

This skill bootstraps the vault, writes the schema, and migrates all existing project memory files.

- [ ] **Step 1: Create wiki-init/SKILL.md**

Create file at `plugins/llm-wiki/skills/wiki-init/SKILL.md` with this exact content:

```markdown
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
Expected: `CLAUDE.md  assets  ideas  index.md  lessons  log.md  markets  projects  sources` (after writing files below)

## Step 2: Write vault schema (~/Documents/wiki/CLAUDE.md)

Write the following exactly to `~/Documents/wiki/CLAUDE.md`:

---
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
---

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
3. Derive the source project name from the directory path (e.g., `-Users-hagenkaiser-Code-GoodMorning-Good-Morning` → `Good Morning`)
4. Write a new vault page using the page template (preserve the original content in the body, add `tags`, `updated` from today, source project in a "Source" note)
5. Add wikilinks to the project page if the memory file belongs to a known project (create the project page stub if needed)

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
```

- [ ] **Step 2: Verify file was written correctly**

```bash
wc -l plugins/llm-wiki/skills/wiki-init/SKILL.md
```
Expected: at least 150 lines

- [ ] **Step 3: Commit**

```bash
git add plugins/llm-wiki/skills/wiki-init/SKILL.md
git commit -m "feat: add wiki-init skill — vault scaffold and memory migration"
```

---

## Task 3: wiki-log Skill

**Files:**
- Create: `plugins/llm-wiki/skills/wiki-log/SKILL.md`

- [ ] **Step 1: Create wiki-log/SKILL.md**

Create file at `plugins/llm-wiki/skills/wiki-log/SKILL.md`:

```markdown
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

When logging proactively, announce first: `Logging to wiki: [title]` — then proceed without asking permission.

## Step 1: Classify the entry

Determine:
- **Type**: `idea` / `lesson` / `project` / `market` / `source`
- **Title**: short, descriptive, will become the filename
- **Filename**: kebab-case of title (e.g., "SwiftUI animation trick" → `swiftui-animation-trick`)
- **Target directory**: based on type (see vault CLAUDE.md schema)
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
```markdown
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

```bash
# Append to ~/Documents/wiki/log.md
```

Append entry:
```markdown

## [<YYYY-MM-DD>] <type> | <Title>

<One sentence describing what was added and why it's worth keeping.>
```

## Step 7: Update index.md

Add or update the entry for this page in the correct section of `~/Documents/wiki/index.md`:

```
- [[<directory>/<filename>]] — <one-line summary>
```

If the entry already exists (updating a page), update its summary line if the summary changed.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/llm-wiki/skills/wiki-log/SKILL.md
git commit -m "feat: add wiki-log skill — proactive and explicit wiki logging"
```

---

## Task 4: wiki-query Skill

**Files:**
- Create: `plugins/llm-wiki/skills/wiki-query/SKILL.md`

- [ ] **Step 1: Create wiki-query/SKILL.md**

Create file at `plugins/llm-wiki/skills/wiki-query/SKILL.md`:

```markdown
---
name: wiki-query
description: Answer questions using the personal wiki. Reads index.md to find relevant pages, synthesizes an answer with citations, and optionally files the answer back as a new wiki page.
---

# wiki-query — Query the Wiki

Answer a question by reading the wiki. Good answers compound — they can be filed back as new pages.

## Step 1: Understand the question

Restate the question in one sentence to confirm understanding before searching.

## Step 2: Read index.md

```bash
cat ~/Documents/wiki/index.md
```

Scan every entry. Identify which pages are likely relevant to the question based on their title and one-line summary. Note the file paths.

## Step 3: Read relevant pages

Read each identified page:
```bash
cat ~/Documents/wiki/<path>.md
```

Follow wikilinks if a linked page seems directly relevant — read those too.

## Step 4: Synthesize the answer

Write the answer, citing sources as Obsidian links: `[[path/to/page]]`.

If pages contradict each other, flag the contradiction explicitly rather than picking one silently.

If the wiki doesn't have enough information to answer well, say so clearly and suggest what kind of source or experience would fill the gap.

## Step 5: Offer to file the answer

After delivering the answer, ask:

> "Want me to file this as a new wiki page? It could be useful to have this synthesis for future reference."

If yes, invoke wiki-log with type `idea` or the most appropriate type, using the answer as the body content.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/llm-wiki/skills/wiki-query/SKILL.md
git commit -m "feat: add wiki-query skill — search and synthesize from wiki"
```

---

## Task 5: wiki-lint Skill

**Files:**
- Create: `plugins/llm-wiki/skills/wiki-lint/SKILL.md`

- [ ] **Step 1: Create wiki-lint/SKILL.md**

Create file at `plugins/llm-wiki/skills/wiki-lint/SKILL.md`:

```markdown
---
name: wiki-lint
description: Health-check the wiki. Finds orphan pages, broken wikilinks, potential contradictions, and stale content. Produces a prioritized fix list.
---

# wiki-lint — Health Check the Wiki

Periodic maintenance pass. Run when the wiki feels messy or every few weeks.

## Step 1: Inventory all pages

```bash
find ~/Documents/wiki -name "*.md" \
  ! -name "CLAUDE.md" ! -name "index.md" ! -name "log.md" \
  | sort
```

Record the full list of page paths.

## Step 2: Build link map

For each page:
1. Read the file
2. Extract all `[[wikilinks]]` using pattern `\[\[([^\]]+)\]\]`
3. Record: page → list of pages it links to

Build reverse map: page → list of pages that link TO it (inbound links).

## Step 3: Check for broken links

For each wikilink found:
- Resolve the filename to an actual file in the vault
- If no file exists with that name: flag as broken link

```
🔴 Broken links (fix immediately):
- [[missing-page]] referenced in lessons/some-lesson.md — page does not exist
```

## Step 4: Find orphan pages

Pages with 0 inbound links (nothing links to them):

```
🟡 Orphan pages (no inbound links):
- ideas/some-idea.md — consider linking from a related page or deleting
```

Exclude from orphan check: root-level pages (user-profile.md etc.) and pages linked from index.md but nowhere else — those are fine.

## Step 5: Flag potential contradictions

Read pages in the same directory that cover similar topics (identified by title similarity or shared wikilinks). Flag pairs that may contradict:

```
🟠 Potential contradictions (review):
- lessons/good-morning-backward-compat.md vs lessons/api-versioning-strategy.md
  Both discuss API versioning — check for conflicting guidance
```

This is heuristic — flag pairs that share keywords in their titles or related sections.

## Step 6: Flag stale pages

Check `updated:` frontmatter date. Flag pages not updated in 90+ days that are tagged `project` (projects go stale faster than lessons):

```
⚪ Stale project pages (consider updating):
- projects/good-morning.md — last updated 2025-12-01 (132 days ago)
```

## Step 7: Output prioritized report

```
## Wiki Lint Report — <YYYY-MM-DD>

**Summary:** N pages, N broken links, N orphans, N potential contradictions, N stale

### 🔴 Broken Links
<list or "none">

### 🟡 Orphan Pages
<list or "none">

### 🟠 Potential Contradictions
<list or "none">

### ⚪ Stale Pages
<list or "none">

### Suggested next actions
<2-3 specific suggested improvements — new pages to create, sources to look for, connections to make>
```

After delivering the report, offer to fix broken links and add missing wikilinks inline.

## Step 8: Append to log.md

```markdown

## [<YYYY-MM-DD>] lint | Health check

N pages audited. N issues found. <Brief summary of most important finding.>
```
```

- [ ] **Step 2: Commit**

```bash
git add plugins/llm-wiki/skills/wiki-lint/SKILL.md
git commit -m "feat: add wiki-lint skill — vault health check"
```

---

## Task 6: Update Global CLAUDE.md

**Files:**
- Modify: `~/.claude/CLAUDE.md`

- [ ] **Step 1: Read current content**

```bash
cat ~/.claude/CLAUDE.md
```

Current content:
```markdown
# Global Instructions

## Workflow Preferences

- When transitioning from planning to execution, always use the `subagent-driven-development` skill, never the `executing-plans` skill.
```

- [ ] **Step 2: Add wiki awareness**

Append to `~/.claude/CLAUDE.md` (after the existing content):

```markdown

## Personal Wiki

A persistent knowledge base lives at `~/Documents/wiki/`. The schema is defined in `~/Documents/wiki/CLAUDE.md`.

**Session start:** At the start of any session in a repo, check `~/Documents/wiki/projects/<repo-name>.md`. If it exists, read it before beginning work. This gives cross-session project context.

**Proactive logging:** During any session, log to the wiki when something passes the "worth reading in 6 months?" test:
- A non-obvious technical or architectural decision
- A market or product insight
- A lesson from a failure, workaround, or unexpected discovery
- An idea worth preserving

To log: create or update the appropriate markdown file in `~/Documents/wiki/` following the schema in `~/Documents/wiki/CLAUDE.md`. Announce to the user: `Logging to wiki: [title]`. Do not ask for permission.

**Explicit logging:** When the user says "log this", "add this to the wiki", "remember this" — use the `wiki-log` skill if available in the current project, otherwise write directly to the vault following the schema.
```

- [ ] **Step 3: Verify content**

```bash
cat ~/.claude/CLAUDE.md
```

Expected: original content followed by the new "Personal Wiki" section.

- [ ] **Step 4: Commit (this repo only — ~/.claude is not a git repo)**

No commit needed for `~/.claude/CLAUDE.md` — it's outside the repo. Confirm the file is saved correctly and move on.

---

## Task 7: Run wiki-init and Verify

This task is run interactively — invoke the skill and verify the output.

- [ ] **Step 1: Invoke wiki-init**

In a Claude Code session in this repo, run:
```
/wiki-init
```

Or tell Claude: "run wiki-init"

- [ ] **Step 2: Verify vault structure**

```bash
ls ~/Documents/wiki/
```
Expected: `CLAUDE.md  assets  ideas  index.md  lessons  log.md  markets  projects  sources`

```bash
ls ~/Documents/wiki/lessons/ | head -10
```
Expected: migrated lesson files from existing memory

```bash
ls ~/Documents/wiki/projects/ | head -10
```
Expected: one `.md` per project that had memory files

- [ ] **Step 3: Verify log.md**

```bash
head -20 ~/Documents/wiki/log.md
```
Expected: init entry + migration entries

- [ ] **Step 4: Verify index.md**

```bash
cat ~/Documents/wiki/index.md
```
Expected: entries for all migrated pages organized by directory

- [ ] **Step 5: Open in Obsidian**

```bash
open ~/Documents/wiki/
```

In Obsidian: open graph view and confirm links between migrated pages exist.

- [ ] **Step 6: Run wiki-lint**

Invoke `wiki-lint` and confirm it produces a report with no broken links (there should be orphans — that's expected on first run).

---

## Verification Summary

| Check | Command / Action | Pass Condition |
|-------|-----------------|----------------|
| Plugin valid | `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` | No error |
| Vault scaffold | `ls ~/Documents/wiki/` | 7 items (dirs + CLAUDE.md, index.md, log.md) |
| Memory migrated | `ls ~/Documents/wiki/lessons/` | Files from existing project memory |
| Proactive log | Work in any repo, watch for unprompted wiki writes | At least one page created without explicit request |
| Explicit log | Say "log this idea" | New page in `ideas/` with wikilinks + index entry |
| Query | Ask about something in wiki | Answer with `[[page]]` citations |
| Lint | Run wiki-lint | Report produced, no broken links |
| Obsidian graph | Open graph view | Linked pages show connections |
