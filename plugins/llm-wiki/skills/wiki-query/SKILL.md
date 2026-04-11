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
