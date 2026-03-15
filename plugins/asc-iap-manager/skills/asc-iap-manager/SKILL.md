---
name: asc-iap-manager
description: Use when managing App Store Connect in-app purchases or auto-renewable subscriptions - creating, listing, pricing, localizing, or deleting IAPs and subscriptions. Also use for downloading/uploading App Store screenshots (via ASC API or fastlane). Complements the appstore-connect MCP server which lacks IAP/subscription management and screenshot access.
tools: Bash, Read
---

# App Store Connect IAP & Subscription Manager

Manage in-app purchases and auto-renewable subscriptions via the App Store Connect REST API. This skill fills the gap left by the `appstore-connect` MCP server, which supports apps, versions, beta groups, devices, and analytics — but NOT IAP or subscription CRUD.

## When to Use

- Creating, listing, updating, or deleting in-app purchases
- Creating and managing auto-renewable subscription groups and subscriptions
- Adding localizations to IAPs or subscriptions
- Setting or changing IAP/subscription prices
- Checking IAP/subscription status (MISSING_METADATA, READY_TO_SUBMIT, APPROVED, etc.)
- Downloading or uploading App Store screenshots/preview images via fastlane

## When NOT to Use

- For general App Store Connect operations (apps, versions, beta groups, devices, users, analytics) — use the `mcp__appstore-connect__*` MCP tools instead
- The MCP `appstore-connect` server does NOT have screenshot endpoints — use fastlane (see below)

## Prerequisites

The CLI tool requires a Python venv with `PyJWT` and `cryptography`. On first use, run setup:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/setup_venv.sh
```

Auth credentials are read from environment variables or auto-discovered from `~/.appstoreconnect/`:
- `APP_STORE_CONNECT_KEY_ID` (or extracted from `AuthKey_XXXXXX.p8` filename)
- `APP_STORE_CONNECT_ISSUER_ID` (or from `~/.appstoreconnect/config.json`)
- `APP_STORE_CONNECT_P8_PATH` (or first `.p8` file found in `~/.appstoreconnect/`)

## CLI Tool

The tool lives at `${CLAUDE_PLUGIN_ROOT}/asc_iap.py` and is run via the skill's venv:

```bash
VENV=${CLAUDE_PLUGIN_ROOT}/.venv/bin/python
```

### IAP Commands

#### List IAPs for an app
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py list <APP_ID>
```

#### Get IAP details
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py get <IAP_ID>
```

#### Create a new IAP
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py create <APP_ID> <PRODUCT_ID> <REFERENCE_NAME> [--type NON_CONSUMABLE|CONSUMABLE|NON_RENEWING_SUBSCRIPTION]
```

#### Add localization to IAP
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py add-localization <IAP_ID> <LOCALE> <DISPLAY_NAME> <DESCRIPTION>
```
Note: Description max is 55 characters for non-consumable IAPs.

#### Set IAP price
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py set-price <IAP_ID> <PRICE_USD> [--territory USA]
```

#### Delete an IAP
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py delete <IAP_ID>
```

### Subscription Commands

#### List subscription groups for an app
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py list-groups <APP_ID>
```

#### Create a subscription group
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py create-group <APP_ID> <REFERENCE_NAME>
```

#### List subscriptions in a group
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py list-subs <GROUP_ID>
```

#### Create an auto-renewable subscription
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py create-sub <GROUP_ID> <PRODUCT_ID> <REFERENCE_NAME> --period <PERIOD>
```
Period values: `ONE_WEEK`, `ONE_MONTH`, `TWO_MONTHS`, `THREE_MONTHS`, `SIX_MONTHS`, `ONE_YEAR`

Optional: `--review-note "Note for reviewers"`

#### Get subscription details
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py get-sub <SUB_ID>
```

#### Add localization to a subscription
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py add-sub-localization <SUB_ID> <LOCALE> <DISPLAY_NAME> <DESCRIPTION>
```

#### Set subscription price
```bash
$VENV ${CLAUDE_PLUGIN_ROOT}/asc_iap.py set-sub-price <SUB_ID> <PRICE_USD> [--territory USA]
```

## Typical Workflow: Create a Complete IAP

1. **Create the IAP**:
   ```bash
   $VENV asc_iap.py create 6749178301 com.example.premium "Premium Upgrade"
   ```

2. **Add localizations** (EN + DE):
   ```bash
   $VENV asc_iap.py add-localization <IAP_ID> en-US "Premium" "Unlock all features."
   $VENV asc_iap.py add-localization <IAP_ID> de-DE "Premium" "Alle Funktionen freischalten."
   ```

3. **Set the price**:
   ```bash
   $VENV asc_iap.py set-price <IAP_ID> 9.99
   ```

4. **Upload review screenshot**: Must be done manually in App Store Connect UI.

5. **Verify state**:
   ```bash
   $VENV asc_iap.py get <IAP_ID>
   ```

## Typical Workflow: Create Auto-Renewable Subscriptions

1. **Create subscription group**:
   ```bash
   $VENV asc_iap.py create-group 6747745091 "Good Morning Premium"
   ```
   Returns the group ID.

2. **Create subscriptions**:
   ```bash
   $VENV asc_iap.py create-sub <GROUP_ID> org.hagenkaiser.Good_Morning.monthly "Monthly Subscription" --period ONE_MONTH
   $VENV asc_iap.py create-sub <GROUP_ID> org.hagenkaiser.Good_Morning.annual "Annual Subscription" --period ONE_YEAR
   ```

3. **Add localizations**:
   ```bash
   $VENV asc_iap.py add-sub-localization <SUB_ID> en-US "Good Morning Monthly" "Personalized morning show every day"
   $VENV asc_iap.py add-sub-localization <SUB_ID> de-DE "Good Morning Monatlich" "Personalisierte Morgenshow jeden Tag"
   ```

4. **Set prices**:
   ```bash
   $VENV asc_iap.py set-sub-price <MONTHLY_ID> 4.99
   $VENV asc_iap.py set-sub-price <ANNUAL_ID> 39.99
   ```

5. **Upload review screenshot**: Must be done manually in App Store Connect UI.

6. **Verify**:
   ```bash
   $VENV asc_iap.py list-groups 6747745091
   $VENV asc_iap.py get-sub <SUB_ID>
   ```

## API Reference

| Operation | Endpoint | API Version |
|---|---|---|
| **IAP** | | |
| Create IAP | `POST /v2/inAppPurchases` | v2 |
| Get IAP | `GET /v2/inAppPurchases/{id}` | v2 |
| List IAPs | `GET /v1/apps/{id}/inAppPurchasesV2` | v1 |
| Delete IAP | `DELETE /v2/inAppPurchases/{id}` | v2 |
| Add IAP localization | `POST /v1/inAppPurchaseLocalizations` | v1 |
| List IAP price points | `GET /v2/inAppPurchases/{id}/pricePoints` | v2 |
| Set IAP price | `POST /v1/inAppPurchasePriceSchedules` | v1 |
| **Subscriptions** | | |
| List groups | `GET /v1/apps/{id}/subscriptionGroups` | v1 |
| Create group | `POST /v1/subscriptionGroups` | v1 |
| List subscriptions | `GET /v1/subscriptionGroups/{id}/subscriptions` | v1 |
| Create subscription | `POST /v1/subscriptions` | v1 |
| Get subscription | `GET /v1/subscriptions/{id}` | v1 |
| Add sub localization | `POST /v1/subscriptionLocalizations` | v1 |
| List sub price points | `GET /v1/subscriptions/{id}/pricePoints` | v1 |
| Set sub price | `POST /v1/subscriptionPrices` | v1 |

## App Store Screenshots

The `appstore-connect` MCP server has no screenshot endpoints. Two methods are available:

### Method 1: Direct ASC API Upload (Preferred)

Upload screenshots directly via the App Store Connect REST API. No fastlane dependency, no Ruby issues.

**3-step process:**

```python
# Uses the same auth as asc_iap.py (get_auth_config + generate_token)

# Step 1: Reserve screenshot slot
POST /v1/appScreenshots
{
  "data": {
    "type": "appScreenshots",
    "attributes": { "fileName": "screenshot.png", "fileSize": 2373006 },
    "relationships": {
      "appScreenshotSet": { "data": { "type": "appScreenshotSets", "id": "SET_ID" } }
    }
  }
}
# Returns: screenshot ID + uploadOperations (URL, offset, length, headers)

# Step 2: Upload file chunks
PUT {uploadOperations[n].url}
# Headers from uploadOperations[n].requestHeaders
# Body: file bytes[offset:offset+length]

# Step 3: Commit
PATCH /v1/appScreenshots/{screenshot_id}
{
  "data": {
    "type": "appScreenshots",
    "id": "screenshot_id",
    "attributes": { "sourceFileChecksum": "md5_hex", "uploaded": true }
  }
}
```

**Finding screenshot set IDs:**
```
GET /v1/apps/{APP_ID}/appStoreVersions
GET /v1/appStoreVersions/{VERSION_ID}/appStoreVersionLocalizations
GET /v1/appStoreVersionLocalizations/{LOC_ID}/appScreenshotSets
# Each set has a screenshotDisplayType: APP_IPHONE_65, APP_IPHONE_67, APP_WATCH_ULTRA, etc.
```

**Downloading existing screenshots:**
```
GET /v1/appScreenshotSets/{SET_ID}/appScreenshots
# Each screenshot has imageAsset.templateUrl — replace {w}, {h}, {f} with actual values
```

### Method 2: Fastlane Deliver (Fallback)

Use **fastlane deliver** as a fallback. Note: may have Ruby version issues.

### Prerequisites

Fastlane must be installed (`gem install fastlane`) and an API key JSON file must exist:

```json
// fastlane/api_key.json
{
  "key_id": "YOUR_KEY_ID",
  "issuer_id": "YOUR_ISSUER_ID",
  "key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
  "in_house": false
}
```

**Important:** The `key` field must contain the .p8 key content inline with `\n` newlines — NOT a file path. Fastlane does not accept `key_filepath`.

Credentials can be sourced from `~/.appstoreconnect/config.json` (key_id, issuer_id) and `~/.appstoreconnect/AuthKey_XXXXXX.p8`.

Also create a minimal `fastlane/Appfile`:
```ruby
app_identifier "your.bundle.id"
```

### Download Screenshots

```bash
fastlane deliver download_screenshots --api_key_path fastlane/api_key.json
```

Downloads to `fastlane/screenshots/<locale>/` (e.g., `fastlane/screenshots/en-US/`).

File naming convention: `<order>_APP_IPHONE_<size>_<index>.png`
- `0_APP_IPHONE_65_0.png` — iPhone 6.5" first screenshot
- `1_APP_IPHONE_65_1.png` — iPhone 6.5" second screenshot
- `0_APP_IPHONE_61_0.png` — iPhone 6.1" first screenshot
- `0_APP_IPAD_PRO_3GEN_129_0.png` — iPad Pro 12.9" first screenshot

### Upload Screenshots

```bash
fastlane deliver \
  --api_key_path fastlane/api_key.json \
  --skip_metadata true \
  --skip_binary_upload true \
  --overwrite_screenshots true \
  --precheck_include_in_app_purchases false \
  --force
```

- `--overwrite_screenshots` deletes ALL existing screenshots (all sizes) before uploading
- `--force` skips the HTML preview confirmation
- `--precheck_include_in_app_purchases false` suppresses IAP precheck warnings when using API key auth
- Place screenshots in `fastlane/screenshots/<locale>/` with the naming convention above
- **Back up originals** before overwriting — fastlane deletes all screenshots across all device sizes

### Required Dimensions

| Device | Size Label | Dimensions |
|--------|-----------|------------|
| iPhone 6.7" | `67` | 1290x2796 |
| iPhone 6.5" | `65` | 1242x2688 |
| iPhone 6.1" | `61` | 1179x2556 |
| iPad Pro 12.9" 3rd gen | `IPAD_PRO_3GEN_129` | 2048x2732 |

### Gotchas

- Fastlane's precheck may warn about copyright year or support URL — these are non-blocking
- `--overwrite_screenshots` removes ALL device sizes, not just the ones you're uploading — back up first
- Ruby 2.7 triggers deprecation warnings but still works
- The `list_app_store_versions` MCP endpoint returns an error — use fastlane for version-related screenshot work

## AI-Generated Marketing Screenshots (Nano Banana 2)

Create polished App Store marketing screenshots using Nano Banana 2 (`google/nano-banana-2` on Replicate). The model takes a raw app screenshot + a style reference and generates a complete marketing image with device frame, illustrated background, and headline text — no manual compositing needed.

**Why Nano Banana 2:** Flux hallucinated the UI. Pillow compositing looks amateur. Nano Banana 2 preserves the actual app UI inside a realistic device frame with AI-generated backgrounds via style transfer.

### Generate a marketing screenshot

```bash
./marketing/generate_appstore_screenshot.py screenshot.png "HEADLINE TEXT." output.png \
  --style-ref path/to/existing_marketing_screenshot.png \
  --size 6.5
```

- `screenshot.png` — Raw app screenshot (any size)
- `"HEADLINE TEXT."` — Bold headline for the top
- `--style-ref` — Existing marketing screenshot to match style (backgrounds, device frame, layout)
- `--size` — `6.5` (1242x2688, default) or `6.7` (1290x2796)

### How it works

1. Upload both images to Replicate (`/v1/files`, multipart form — data URIs cause timeouts)
2. Generate via `google/nano-banana-2` at 1K resolution (2K with 2 images causes `httpx.ReadTimeout`)
3. Upscale to exact App Store dimensions with Pillow LANCZOS
4. Upload to ASC via the 3-step API process (reserve → upload chunks → commit)

### Prompt template

```
Transform the first image into an App Store marketing screenshot matching the exact style
of the second image. Place the first image (app screenshot) inside a realistic iPhone
device mockup. Use a [BRAND-APPROPRIATE BACKGROUND DESCRIPTION] matching the illustrated
art style of the second reference image. Bold white headline '{HEADLINE}' at the top.
Keep the app screenshot content exactly as-is inside the phone.
```

Key phrases: "matching the exact style of the second image" (forces style transfer), "Keep the app screenshot content exactly as-is" (prevents UI hallucination).

### Workflow

1. Download existing screenshots as style reference (via ASC API or keep local)
2. Take raw app screenshots (simulator or device)
3. Generate marketing images — one per screenshot, show each for approval
4. Upscale to target dimensions
5. Upload to ASC via API

## Gotchas

- **v1 vs v2**: IAP creation/deletion use v2, but subscriptions use v1 exclusively. The CLI handles this automatically.
- **Description length**: Non-consumable IAP descriptions are limited to 55 characters. Subscription descriptions have no such limit.
- **Price points**: Prices must match an Apple-defined price point exactly. The `set-price`/`set-sub-price` commands find the closest match.
- **Review screenshot**: Cannot be uploaded via API. IAPs/subscriptions will stay in `MISSING_METADATA` until a screenshot is added via the ASC web UI.
- **Deletion**: Only works for IAPs that haven't been submitted for review yet.
- **Subscription pricing**: Uses `POST /v1/subscriptionPrices` per-territory (different from IAP price schedules). **Known Apple API bug (Feb 2026):** `set-sub-price` returns HTTP 500 despite correct request body matching the OpenAPI spec. Workaround: set prices manually in the ASC web UI.
- **Subscription periods**: Must be one of: `ONE_WEEK`, `ONE_MONTH`, `TWO_MONTHS`, `THREE_MONTHS`, `SIX_MONTHS`, `ONE_YEAR`.
- **Introductory offers**: Use `add-intro-offer` with `--mode FREE_TRIAL|PAY_AS_YOU_GO|PAY_UP_FRONT`. Only one intro offer per subscription per territory. Duration options: `THREE_DAYS`, `ONE_WEEK`, `TWO_WEEKS`, `ONE_MONTH`, `TWO_MONTHS`, `THREE_MONTHS`, `SIX_MONTHS`, `ONE_YEAR`.
