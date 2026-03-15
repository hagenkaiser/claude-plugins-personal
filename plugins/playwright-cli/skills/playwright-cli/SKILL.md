---
name: playwright-cli
description: Use when automating browser interactions, filling forms, taking screenshots, scraping web pages, testing web UIs, or any task requiring programmatic browser control via the command line
---

# Playwright CLI

Browser automation via CLI. Each command returns a snapshot with element references for the next action.

## Core Workflow

```
open [url] → (snapshot with refs) → interact using refs → screenshot → close
```

1. `playwright-cli open <url>` — launch browser, get first snapshot
2. Read snapshot — find element refs (e.g. `e21`, `e35`)
3. Interact — `click e21`, `fill e35 "text"`, etc.
4. Each command returns an updated snapshot with new refs
5. `screenshot` to capture visual proof, `close` when done

## Element References

Every command returns a snapshot listing interactive elements with short refs like `e21`. Use these refs to target elements:

```bash
playwright-cli click e21          # click element
playwright-cli fill e35 "hello"   # fill input
playwright-cli screenshot e21     # screenshot specific element
```

Refs are regenerated with each snapshot — always use refs from the most recent output.

## Command Reference

### Browser & Navigation

| Command | Description |
|---------|-------------|
| `open [url]` | Launch browser, optionally navigate |
| `open [url] --headed` | Launch with visible browser window |
| `open [url] --browser=firefox` | Use firefox or webkit instead of chromium |
| `goto <url>` | Navigate to URL |
| `go-back` | Navigate back |
| `go-forward` | Navigate forward |
| `reload` | Reload page |
| `close` | Close page |

### Interaction

| Command | Description |
|---------|-------------|
| `click <ref> [button]` | Click element (button: left/right/middle) |
| `dblclick <ref> [button]` | Double-click element |
| `fill <ref> <text>` | Fill form field (clears first) |
| `type <text>` | Type into focused element (keystroke by keystroke) |
| `hover <ref>` | Hover over element |
| `select <ref> <val>` | Select dropdown option |
| `check <ref>` | Check checkbox/radio |
| `uncheck <ref>` | Uncheck checkbox |
| `drag <startRef> <endRef>` | Drag and drop |
| `upload <file>` | Upload file |

### Keyboard & Mouse

| Command | Description |
|---------|-------------|
| `press <key>` | Press key (e.g. `Enter`, `Tab`, `ArrowDown`, `a`) |
| `keydown <key>` | Key down event |
| `keyup <key>` | Key up event |
| `mousemove <x> <y>` | Move cursor to coordinates |
| `mousedown [button]` | Mouse button down |
| `mouseup [button]` | Mouse button up |
| `mousewheel <dx> <dy>` | Scroll |

### Screenshots & Output

| Command | Description |
|---------|-------------|
| `screenshot [ref]` | Capture page or specific element |
| `screenshot --filename=f` | Save with custom filename |
| `snapshot [--filename=f]` | Capture page state (accessibility snapshot) |
| `pdf [--filename=f]` | Save page as PDF |

### Tabs

| Command | Description |
|---------|-------------|
| `tab-list` | Show all tabs |
| `tab-new [url]` | Open new tab |
| `tab-select <index>` | Switch to tab |
| `tab-close [index]` | Close tab |

### Storage

**Cookies:** `cookie-list [--domain]`, `cookie-get <name>`, `cookie-set <name> <val>`, `cookie-delete <name>`, `cookie-clear`

**localStorage:** `localstorage-list`, `localstorage-get <key>`, `localstorage-set <k> <v>`, `localstorage-delete <k>`, `localstorage-clear`

**sessionStorage:** `sessionstorage-list`, `sessionstorage-get <k>`, `sessionstorage-set <k> <v>`, `sessionstorage-delete <k>`, `sessionstorage-clear`

**State persistence:** `state-save [filename]`, `state-load <filename>`

### Network & Dialogs

| Command | Description |
|---------|-------------|
| `route <pattern> [opts]` | Mock/intercept network requests |
| `route-list` | List active routes |
| `unroute [pattern]` | Remove route |
| `dialog-accept [prompt]` | Accept dialog (alert/confirm/prompt) |
| `dialog-dismiss` | Dismiss dialog |

### Dev Tools

| Command | Description |
|---------|-------------|
| `console [min-level]` | Show console messages |
| `network` | Show network requests |
| `run-code <code>` | Execute JavaScript in page |
| `eval <func> [ref]` | Evaluate JS function, optionally on element |
| `tracing-start` | Start trace recording |
| `tracing-stop` | Stop trace recording |
| `video-start` | Start video recording |
| `video-stop [filename]` | Stop video recording |

## Sessions

Manage multiple isolated browser instances with named sessions:

```bash
playwright-cli open https://app.example.com                    # default session
playwright-cli -s=admin open https://admin.example.com         # named session
playwright-cli -s=admin fill e12 "admin@example.com"           # interact in named session
playwright-cli list                                            # show all active sessions
playwright-cli -s=admin close                                  # close specific session
playwright-cli close-all                                       # close all browsers
playwright-cli kill-all                                        # force kill all
```

**Persistence:**
- Default: in-memory profile, lost on close
- `--persistent`: save profile to disk (cookies, storage survive restart)
- `--profile=<path>`: custom profile directory

**Environment variable:** `PLAYWRIGHT_CLI_SESSION=my-app` sets default session name.

**Dashboard:** `playwright-cli show` opens a visual dashboard with live screencasts of all sessions.

## Configuration

Optional config file at `.playwright/cli.config.json`:

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": { "headless": true },
    "contextOptions": { "viewport": { "width": 1280, "height": 720 } }
  },
  "timeouts": { "action": 5000, "navigation": 60000 },
  "outputDir": "./artifacts",
  "testIdAttribute": "data-testid"
}
```

Override config path: `playwright-cli --config path/to/config.json open`.

## Using Real Chrome Profile (with saved passwords/sessions)

Playwright can't access the macOS Keychain, so it can't decrypt Chrome's saved passwords directly. The workaround is to copy the Chrome profile to a separate location and use `--profile`.

### First-time setup (requires Chrome to be quit)

```bash
# 1. Quit Chrome (profile is locked while Chrome runs)
osascript -e 'tell application "Google Chrome" to quit'
sleep 3

# 2. Copy Chrome profile to a working location
mkdir -p /tmp/chrome-profile
cp -R "$HOME/Library/Application Support/Google/Chrome/Default" /tmp/chrome-profile/Default
cp "$HOME/Library/Application Support/Google/Chrome/Local State" /tmp/chrome-profile/

# 3. Launch with the copied profile
playwright-cli open https://example.com --browser=chrome --headed --profile=/tmp/chrome-profile

# 4. Log in manually on first use (passwords won't auto-fill due to Keychain restriction)

# 5. Save session state for future reuse
playwright-cli state-save /tmp/chrome-profile/session-state.json
playwright-cli close
```

### Subsequent sessions (no login needed)

```bash
# Launch with saved profile (cookies persist in the profile dir)
playwright-cli open https://example.com --browser=chrome --headed --profile=/tmp/chrome-profile

# Or restore state into a fresh session
playwright-cli open https://example.com --browser=chrome --headed
playwright-cli state-load /tmp/chrome-profile/session-state.json
```

**Key points:**
- `--profile` must NOT point to Chrome's default data dir — Chrome blocks remote debugging for its default path
- The copied profile preserves cookies/localStorage but not Keychain-encrypted passwords
- After first manual login, `state-save` captures cookies so you won't need to log in again (until cookies expire)
- Re-copy the profile periodically if you need fresh cookie/storage data from Chrome

## Common Patterns

### Fill and submit a form

```bash
playwright-cli open https://example.com/login --headed
playwright-cli fill e12 "user@example.com"
playwright-cli fill e15 "password123"
playwright-cli click e18                      # submit button
playwright-cli screenshot --filename=logged-in.png
```

### Multi-step interaction with verification

```bash
playwright-cli open https://demo.playwright.dev/todomvc/
playwright-cli type "Buy groceries"
playwright-cli press Enter
playwright-cli type "Water flowers"
playwright-cli press Enter
playwright-cli check e21                      # complete first todo
playwright-cli screenshot
```

### Work across multiple tabs

```bash
playwright-cli open https://example.com
playwright-cli tab-new https://other-site.com
playwright-cli tab-list                       # see all tabs
playwright-cli tab-select 0                   # switch back to first tab
```

### Persist and restore state

```bash
playwright-cli open https://app.example.com --persistent
# ... login, set preferences ...
playwright-cli state-save session.json
playwright-cli close
# Later:
playwright-cli open https://app.example.com
playwright-cli state-load session.json        # restore cookies/storage
```

### Resize viewport

```bash
playwright-cli resize 375 812                 # iPhone X dimensions
playwright-cli screenshot --filename=mobile.png
```
