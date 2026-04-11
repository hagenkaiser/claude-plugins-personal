# PDF-to-Markdown Conversion — Design Spec

**Date:** 2026-04-11
**Status:** Approved design, ready for implementation planning

---

## Context

The wiki-ingest skill lists PDFs as a supported source type but has no mechanism to handle them. Claude's Read tool can read small PDFs natively but fails on PDFs over ~10 pages without explicit pagination. A conversion script pre-processes any PDF into clean LLM-friendly markdown before ingestion, removing the size limitation entirely and producing better-structured input than raw PDF text extraction.

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `plugins/llm-wiki/scripts/pdf_to_md.py` | Create |
| `plugins/llm-wiki/setup_venv.sh` | Create |
| `plugins/llm-wiki/skills/wiki-ingest/SKILL.md` | Modify (add PDF step) |

---

## pdf_to_md.py

**Location:** `plugins/llm-wiki/scripts/pdf_to_md.py`

**Library:** `pymupdf4llm` — PyMuPDF extension that produces LLM-ready markdown preserving headings, tables, and lists.

**Interface:**
```bash
# Run via plugin venv:
${CLAUDE_PLUGIN_ROOT}/.venv/bin/python ${CLAUDE_PLUGIN_ROOT}/scripts/pdf_to_md.py <input.pdf>

# Output: writes <input>.md alongside the PDF, prints output path to stdout
# Exit 0 on success, non-zero on failure
```

**Behavior:**
- Takes one positional argument: path to PDF file
- Converts using `pymupdf4llm.to_markdown(pdf_path)`
- Writes output to `<same-directory>/<same-stem>.md`
- Prints the output path to stdout on success (so the caller can capture it)
- Prints error to stderr and exits non-zero on failure

**Example:**
```
Input:  ~/Documents/wiki/raw/apple-search-ads-guide.pdf
Output: ~/Documents/wiki/raw/apple-search-ads-guide.md  (printed to stdout)
```

The original PDF is never modified.

---

## setup_venv.sh

**Location:** `plugins/llm-wiki/setup_venv.sh`

One-time setup script following the same pattern as `plugins/asc-iap-manager/setup_venv.sh`:

```bash
#!/bin/bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SKILL_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -q pymupdf4llm
    echo "Done."
else
    echo "Venv already exists at $VENV_DIR"
fi
```

User runs this once: `bash plugins/llm-wiki/setup_venv.sh`

---

## wiki-ingest SKILL.md Update

Add a new **Step 2.5** between the existing "Step 2: Choose mode" and "Step 3: Read the source".

**New step content:**

```
## Step 2.5: Convert PDF (if applicable)

If the source file has a `.pdf` extension, convert it to markdown before reading:

```bash
${CLAUDE_PLUGIN_ROOT}/.venv/bin/python ${CLAUDE_PLUGIN_ROOT}/scripts/pdf_to_md.py <source-path>
```

Capture the output path printed to stdout — this is the `.md` file to use in Step 3.

If the venv doesn't exist yet, tell the user:
> "Run `bash plugins/llm-wiki/setup_venv.sh` first to install PDF dependencies, then retry."

If conversion succeeds, use the `.md` output path as the source for all subsequent steps. The original `.pdf` remains untouched in `raw/`.

If the source is not a PDF, skip this step.
```

**Renumber:** existing steps 3–11 stay as-is (Step 2.5 slots in without renumbering).

---

## Verification

1. Run `bash plugins/llm-wiki/setup_venv.sh` — confirm `.venv/` created, `pymupdf4llm` installed
2. Drop a multi-page PDF (>10 pages) into `~/Documents/wiki/raw/`
3. Run: `plugins/llm-wiki/.venv/bin/python plugins/llm-wiki/scripts/pdf_to_md.py ~/Documents/wiki/raw/<file>.pdf`
4. Confirm `.md` written alongside PDF, stdout shows the output path
5. Invoke wiki-ingest on the PDF — confirm Step 2.5 fires, conversion runs, ingest proceeds from the `.md`
6. Confirm source page and entity pages created correctly in wiki
