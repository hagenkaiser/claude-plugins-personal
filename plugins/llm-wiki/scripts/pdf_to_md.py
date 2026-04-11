#!/usr/bin/env python3
"""Convert a PDF file to LLM-friendly markdown using pymupdf4llm.

Usage:
    python3 pdf_to_md.py <input.pdf>

Output:
    Writes <input>.md alongside the PDF.
    Prints the output path to stdout on success.
    Exits non-zero on failure.
"""

import sys
from pathlib import Path

def convert(pdf_path: str) -> str:
    """Convert PDF to markdown, return output path."""
    import pymupdf4llm

    src = Path(pdf_path).expanduser().resolve()
    if not src.exists():
        print(f"Error: file not found: {src}", file=sys.stderr)
        sys.exit(1)
    if src.suffix.lower() != ".pdf":
        print(f"Error: expected a .pdf file, got: {src.suffix}", file=sys.stderr)
        sys.exit(1)

    md_text = pymupdf4llm.to_markdown(str(src))

    out = src.with_suffix(".md")
    out.write_text(md_text, encoding="utf-8")
    return str(out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input.pdf>", file=sys.stderr)
        sys.exit(1)

    output_path = convert(sys.argv[1])
    print(output_path)
