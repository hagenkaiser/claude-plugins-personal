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
  ! -path "*/assets/*" \
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

Read pages in the same directory that cover similar topics (identified by title similarity or shared keywords in their Related sections). Flag pairs that may contradict:

```
🟠 Potential contradictions (review):
- lessons/good-morning-backward-compat.md vs lessons/api-versioning-strategy.md
  Both discuss API versioning — check for conflicting guidance
```

This is heuristic — flag pairs that share keywords in their titles or Related sections.

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

Append to `~/Documents/wiki/log.md`:

```
## [<YYYY-MM-DD>] lint | Health check

N pages audited. N issues found. <Brief summary of most important finding.>
```
