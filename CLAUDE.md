# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Claude Code plugin marketplace (`hagen-personal-plugins`) containing four self-contained plugins under `plugins/`. Each plugin has its own `plugin.json` manifest and `skills/` directory with SKILL.md workflow definitions. The central registry is `.claude-plugin/marketplace.json`.

## Plugins

| Plugin | Purpose | Tech |
|---|---|---|
| **content-creator** | Media generation (images, voice, slideshows) + Instagram scheduling | Python scripts, Replicate, Modal ComfyUI, Late API |
| **swiftui-designer** | Iterative SwiftUI design with visual preview capture and validation | Swift CLI (`swift-cli/`), requires macOS 14+/Xcode 15+ |
| **asc-iap-manager** | App Store Connect IAP/subscription management and screenshot handling | Python CLI (`asc_iap.py`), ASC REST API |
| **playwright-cli** | Browser automation for testing, scraping, screenshots | Skill-only (wraps playwright CLI) |

Plugins have **no interdependencies** — each is fully self-contained.

## Build Commands

### swiftui-designer Swift CLI
```bash
cd plugins/swiftui-designer/swift-cli
swift build -c release
# Binary output: .build/release/swiftui-preview
```

### asc-iap-manager Python venv
```bash
cd plugins/asc-iap-manager
bash setup_venv.sh
# Creates .venv/ and installs PyJWT + cryptography
# Run with: .venv/bin/python asc_iap.py <command>
```

## Architecture

```
.claude-plugin/marketplace.json    ← plugin registry
plugins/
  <plugin>/
    .claude-plugin/plugin.json     ← plugin metadata (name, version, description)
    skills/<skill-name>/SKILL.md   ← workflow/command documentation loaded by Claude
    scripts/                       ← executable tools (Python, not all plugins have these)
```

Skill files (SKILL.md) are the primary interface — they define how Claude invokes each plugin's capabilities. Scripts in `content-creator/scripts/` are called directly from the shell.

## Required Environment Variables

- **content-creator:** `REPLICATE_API_TOKEN`, `MODAL_COMFYUI_URL`, `LATE_API_KEY`, `LATE_INSTAGRAM_ACCOUNT_ID`
- **asc-iap-manager:** ASC credentials via env vars or auto-discovered from `~/.appstoreconnect/` (`.p8` key + `config.json`)

## Known Issues

- ASC `set-sub-price` returns HTTP 500 (Apple API bug as of Feb 2026)
- Review screenshots must be uploaded manually in ASC web UI
- IAP deletion only works for non-submitted items
