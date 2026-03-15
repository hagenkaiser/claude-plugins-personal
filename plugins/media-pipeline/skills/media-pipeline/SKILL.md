---
name: media-pipeline
description: Use when generating images, voice audio, or video clips via Replicate (Flux 2 Pro, Chatterbox TTS, Wan 2.5) and assembling them with ffmpeg. Generic pipeline — not tied to any specific project.
---

# Media Generation Pipeline

Generate images, voice audio, and video clips via Replicate, then assemble them into finished videos with ffmpeg + Pillow text overlays.

## Prerequisites

- `REPLICATE_API_TOKEN` env var (typically stored in `~/.zshenv`)
- Python scripts located in the project's `marketing/` directory (paths may vary by project)
- Shared Replicate client: `replicate_client.py` (token resolution, retry logic, polling)

## Image Generation (Flux 2 Pro via Replicate)

Generate images using `generate_image.py`:

```bash
./marketing/generate_image.py "PROMPT" output.png --character REFERENCE_NAME --aspect-ratio 1:1
```

- `--character`: Name of a character reference image (project-specific, maps to a URL used as `image_prompt` for style consistency)
- `--aspect-ratio`: 1:1 (square), 4:5 (portrait), 9:16 (stories/reels/vertical), 16:9 (landscape)
- Do NOT include text in image prompts — text overlays are added separately in assembly

For images without a character reference, use `generate_image_noref.py`:

```bash
./marketing/generate_image_noref.py "PROMPT" output.png --aspect-ratio 9:16
```

Both scripts output the Replicate delivery URL alongside the local file — capture this URL for video generation.

## Voice Generation (Chatterbox TTS via Replicate)

Generate voice lines using `generate_voice.py`:

```bash
./marketing/generate_voice.py "Text to speak" output.wav --exaggeration 0.7 --cfg-weight 0.5 --temperature 0.8
```

- Uses a WAV reference file for voice cloning (auto-detected from script directory, project-specific)
- `--exaggeration`: 0.0–1.0 (default: 0.7) — higher = more intense delivery
- `--cfg-weight`: 0.0–1.0 (default: 0.5) — adherence to reference voice
- `--temperature`: 0.0–1.0 (default: 0.8) — randomness/variation
- Output: WAV file + prints `VOICE_URL=...` for scripting

### Audio Format Notes

- Chatterbox output is **24kHz mono**
- For clean concatenation with other audio, resample to **48kHz stereo**: `-ar 48000 -ac 2`
- Energy matching: Chatterbox delivers calm/confident speech — match motion prompts accordingly (arms crossed, head nods — NOT screaming/yelling)

## Video Generation

Three Replicate-based video generators are available. Each takes an image URL and a motion prompt to produce an animated clip.

### Model Comparison

| Script | Model | Audio | Best For |
|--------|-------|-------|----------|
| `generate_video_wan.py` | Wan 2.5 I2V | Generates audio from prompt text; supports `--audio` for lip sync | **Default** — best audio generation, lip sync support |
| `generate_video_hailuo.py` | Hailuo 02 | No audio generation | Fallback — reliable motion quality, no safety filter issues |
| `generate_video.py` | Veo 3.1 | N/A | Legacy — aggressive safety filter (E005), use only if others fail |

### Wan 2.5 I2V (Default)

```bash
./marketing/generate_video_wan.py "IMAGE_URL" "motion prompt" output.mp4 --duration 5 --resolution 1080p
```

- `IMAGE_URL`: Replicate delivery URL from `generate_image.py` (not a local file)
- `--duration`: 5 (default) or 10 seconds
- `--resolution`: 480p, 720p (default), 1080p
- `--audio`: Pass a WAV/MP3 file for voice/music synchronization (enables lip sync)
- `--negative-prompt`: Avoid certain elements
- `--no-prompt-expansion`: Follow prompt more strictly

Wan generates audio from the motion prompt text. To bake music into a clip, describe the music in the prompt (e.g., "heavy rock guitar riff playing, aggressive drumbeat soundtrack"). To add voice for lip sync, pass a voice file via `--audio`.

### Hailuo 02 (Fallback)

```bash
./marketing/generate_video_hailuo.py "IMAGE_URL" "motion prompt" output.mp4
```

- Good motion quality, reliable generation
- No audio generation — audio must be added in post-production
- No safety filter issues

### Veo 3.1 (Legacy)

```bash
./marketing/generate_video.py "IMAGE_URL" "motion prompt" output.mp4
```

- Aggressive safety filter (E005 error) blocks many prompts, especially with props/objects
- Use only if Wan and Hailuo both fail

### Motion Prompt Tips

- Keep prompts simple — 1-2 actions max
- Do NOT include text descriptions in motion prompts — text overlays are added separately
- 5 seconds is ideal for short-form video hooks (TikTok, Reels, Shorts)
- For audio baking with Wan: append music/sound description at the end of the motion prompt

## Video Assembly (ffmpeg + Pillow)

Combine two shots + voice audio into a single video with text overlays and an end card:

```bash
./marketing/assemble_video.py -a shot_a.mp4 -c shot_b.mp4 -v voice.wav -o output.mp4 \
  --hook-text "Text overlay on shot A" \
  --roast-text "Text overlay on shot B" \
  [--order athlete-first|character-first]
```

### What It Does

- Normalizes both clips to **1080x1920 @ 30fps**
- **Preserves** shot A audio (e.g., AI-generated music)
- **Strips** shot B audio and replaces with the voice file
- **`--hook-text`**: White text overlay on shot A (upper area, dark background box)
- **`--roast-text`**: White text overlay on shot B (vertically centered, dark background box)
- **End card** (always appended, 3s): Customizable end screen (project-specific)
- Concatenates in specified order (default: `athlete-first`) + end card
- Output: MP4 with H.264 + AAC, optimized for web

### Technical Notes

- Homebrew ffmpeg may lack freetype/drawtext — Pillow is used for text rendering, ffmpeg `overlay` filter composites the text frames
- Text overlays are rendered as PNG frames via Pillow, then composited with ffmpeg

## Gated Workflow (3-Phase Approval Pattern)

Always use a gated workflow when generating media. This prevents wasting compute on clips derived from rejected images.

### Phase 1: Generate Static Assets + Voice
1. Generate images (Flux 2 Pro) — one per shot
2. Generate voice audio (Chatterbox TTS) if needed
3. **GATE: Show all generated images + play voice audio for user approval**
   - User reviews each asset, approves or requests regeneration
   - Regenerate any rejected assets before proceeding

### Phase 2: Generate Video Clips
1. Animate approved images into video clips (Wan 2.5 or fallback)
2. **GATE: Show/list generated video clips for user approval**
   - User reviews each clip, approves or requests regeneration

### Phase 3: Final Assembly
1. Assemble approved clips + voice audio via `assemble_video.py`
2. Show/play final video for user confirmation

**Never skip gates** — each phase depends on the previous phase's approved output.

## App Store Marketing Screenshots (Nano Banana 2)

Create polished App Store screenshots using Nano Banana 2 (Google Gemini Flash Image) on Replicate. The model takes raw app screenshots + a style reference and generates complete marketing images with device frames, illustrated backgrounds, and headline text — no manual compositing needed.

### Why Nano Banana 2 (not Flux or Pillow compositing)

- **Preserves actual app UI** inside a realistic device frame (Flux hallucinated the UI)
- **Single-step generation** — no need for separate background generation, device frame download, or Pillow compositing
- **Style transfer** via reference images — pass an existing App Store screenshot as style reference
- **Pillow compositing looks amateur** — gradient backgrounds with rounded rectangles can't compete with AI-generated marketing images

### Script: `generate_appstore_screenshot.py`

Located in the project's `marketing/` directory.

```bash
./marketing/generate_appstore_screenshot.py screenshot.png "HEADLINE TEXT." output.png \
  --style-ref path/to/existing_marketing_screenshot.png \
  --size 6.5
```

- `screenshot.png`: Raw app screenshot (any size — will be used as content reference)
- `"HEADLINE TEXT."`: Bold headline for the top of the image
- `--style-ref`: An existing App Store marketing screenshot to match style (cartoon backgrounds, device frame style, layout)
- `--size`: Target App Store size — `6.5` (1242x2688, default), `6.7` (1290x2796)

### How It Works

1. **Upload images** to Replicate file hosting (multipart form upload to `/v1/files`)
2. **Generate** via `google/nano-banana-2` with both images as `image_input` at 1K resolution
3. **Upscale** to exact App Store dimensions with Pillow LANCZOS
4. **Upload** to App Store Connect via ASC API (3-step: reserve → upload chunks → commit)

### Resolution Gotchas

- **Use 1K resolution** with Nano Banana 2 when passing 2 images — 2K with 2 images causes `httpx.ReadTimeout`
- Upscale from 1K (768x1376) to target size (1242x2688) via Pillow LANCZOS — quality is acceptable
- Single-image mode at 2K works fine, but style matching requires the second reference image

### Prompt Template

```
Transform the first image into an App Store marketing screenshot matching the exact style
of the second image. Place the first image (app screenshot) inside a realistic iPhone
device mockup. Use a cartoon illustrated gym equipment background with warm terracotta
orange tones and dark gradient, matching the illustrated cartoon art style of the second
reference image. Bold white headline '{HEADLINE}' at the top. Keep the app screenshot
content exactly as-is inside the phone.
```

Adapt the background description to match the app's brand. The key phrases are:
- "matching the exact style of the second image" — forces style transfer
- "Keep the app screenshot content exactly as-is" — prevents UI hallucination

### Uploading to App Store Connect

**Preferred: Direct ASC API upload** (fastlane has Ruby version/auth issues):

```python
# 1. Reserve screenshot slot
POST /v1/appScreenshots
body: { data: { type: "appScreenshots", attributes: { fileName, fileSize },
        relationships: { appScreenshotSet: { data: { type: "appScreenshotSets", id: SET_ID }}}}}

# 2. Upload file chunks (using uploadOperations from step 1)
PUT {upload_url} with chunk data + request headers from response

# 3. Commit upload
PATCH /v1/appScreenshots/{id}
body: { data: { type: "appScreenshots", id, attributes: { sourceFileChecksum: md5, uploaded: true }}}
```

The `generate_appstore_screenshot.py` script handles all three steps with `--upload`.

**To find screenshot set IDs:**
```python
# Get version → localizations → screenshot sets
GET /v1/apps/{APP_ID}/appStoreVersions
GET /v1/appStoreVersions/{VERSION_ID}/appStoreVersionLocalizations
GET /v1/appStoreVersionLocalizations/{LOC_ID}/appScreenshotSets
```

**Fallback: fastlane deliver** (if the API approach has issues):
```bash
fastlane deliver download_screenshots --api_key_path fastlane/api_key.json --app_identifier com.example.app
```
Note: fastlane requires a properly configured `Appfile` with `app_identifier` and may fail with Ruby version issues.

### Uploading Files to Replicate

Nano Banana 2 needs URLs for `image_input`, not local files or data URIs (data URIs cause timeouts). Upload via multipart form:

```python
boundary = "----ReplicateUploadBoundary"
body = BytesIO()
body.write(f"--{boundary}\r\n".encode())
body.write(f'Content-Disposition: form-data; name="content"; filename="{filename}"\r\n'.encode())
body.write(f"Content-Type: image/png\r\n\r\n".encode())
body.write(file_data)
body.write(f"\r\n--{boundary}--\r\n".encode())

req = Request("https://api.replicate.com/v1/files", data=body.getvalue(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
result = json.loads(urlopen(req).read())
file_url = result["urls"]["get"]  # Use this URL in image_input
```

### Workflow: Complete App Store Marketing Screenshots

1. **Download existing screenshots** as style reference (via ASC API or keep a local copy)
2. **Take raw app screenshots** (simulator or device)
3. **Generate marketing images** — one per screenshot, show each for approval
4. **Upscale** to target dimensions
5. **Upload** to ASC via API or fastlane

## Quick Reference

```bash
# Image (with character reference)
./marketing/generate_image.py "PROMPT" out.png --character NAME --aspect-ratio 9:16

# Image (no reference)
./marketing/generate_image_noref.py "PROMPT" out.png --aspect-ratio 9:16

# Voice
./marketing/generate_voice.py "Text" out.wav --exaggeration 0.7

# Video (Wan 2.5 — default)
./marketing/generate_video_wan.py "$IMAGE_URL" "motion prompt" out.mp4 --duration 5 --resolution 1080p

# Video with lip sync
./marketing/generate_video_wan.py "$IMAGE_URL" "motion prompt" out.mp4 --audio voice.wav --duration 5

# Video (Hailuo — fallback)
./marketing/generate_video_hailuo.py "$IMAGE_URL" "motion prompt" out.mp4

# Assembly
./marketing/assemble_video.py -a shot_a.mp4 -c shot_b.mp4 -v voice.wav -o final.mp4 \
  --hook-text "Hook" --roast-text "Punchline"

# App Store marketing screenshots (Nano Banana 2)
./marketing/generate_appstore_screenshot.py screenshot.png "HEADLINE." output.png --style-ref existing_marketing.png --size 6.5
```
