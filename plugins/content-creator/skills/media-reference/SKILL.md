---
name: media-reference
description: Use when generating images, voice audio, video clips, or slideshows via Replicate/Modal, or scheduling Instagram posts via Late API
---

# Media Generation Scripts Reference

Quick reference for all content-creator plugin scripts.

## Scripts

### 1. generate_image.py — SFW image generation via Nano Banana Pro on Replicate

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py \
  --prompt "scene description" \
  --output path/to/output.jpg \
  [--face-ref path/to/reference_image.jpg] \
  --aspect 4:5
```

Arguments:
- `--prompt` (required) — Scene description (passed directly to the model, no prefix added)
- `--output` (required) — Output image path
- `--face-ref` (optional) — Reference image for character/style consistency
- `--aspect` (default: `4:5`) — Choices: `4:5`, `16:9`, `9:16`, `1:1`

Example (with face reference):
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py \
  --prompt "Generate a new image of this same character sitting by a campfire, golden hour light" \
  --output data/generated/shot1.jpg \
  --face-ref data/reference_images/canonical/face.jpg \
  --aspect 4:5
```

Example (without face reference):
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py \
  --prompt "A dramatic mountain landscape at sunset, wide angle" \
  --output data/generated/landscape.jpg \
  --aspect 16:9
```

---

### 2. generate_voice.py — TTS narration via Qwen3 TTS on Replicate

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_voice.py \
  --text "narration text here" \
  --voice-ref path/to/voice_reference.wav \
  --output path/to/output.wav \
  [--reference-text "transcript of reference audio"] \
  [--style "speak slowly and softly, introspective diary reading"]
```

Arguments:
- `--text` (required) — Narration text to speak
- `--voice-ref` (required) — Voice reference WAV for cloning
- `--output` (required) — Output WAV path
- `--reference-text` (optional) — Transcript of reference audio (improves cloning quality)
- `--style` (optional) — Style instruction

Example:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_voice.py \
  --text "The snow fell quietly last night. I woke to silence." \
  --voice-ref data/reference_audio/voice_reference.wav \
  --output data/generated/narration.wav \
  --reference-text "transcript here" \
  --style "speak slowly and softly, introspective diary reading"
```

---

### 3. generate_slideshow.py — Ken Burns + crossfade reel composition via ffmpeg

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_slideshow.py \
  --images shot1.jpg shot2.jpg shot3.jpg \
  --music path/to/track.mp3 \
  --output path/to/reel.mp4 \
  [--narration path/to/narration.wav] \
  [--duration 4] \
  [--fade 1.0] \
  [--width 1080] \
  [--height 1920] \
  [--fps 30]
```

Arguments:
- `--images` (required) — Input images in order (space-separated)
- `--music` (required) — Background music track
- `--output` (required) — Output MP4 path
- `--narration` (optional) — Voiceover WAV. When provided: voice at full volume, music ducked to 20%, image duration auto-scaled to narration length.
- `--duration` (optional, default: `4`) — Seconds per image (ignored when `--narration` is set)
- `--fade` (optional, default: `1.0`) — Crossfade duration in seconds
- `--width` (optional, default: `1080`)
- `--height` (optional, default: `1920`)
- `--fps` (optional, default: `30`)

Example (music-only):
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_slideshow.py \
  --images shot1.jpg shot2.jpg shot3.jpg \
  --music data/music/contemplative_kantele_norse_307s.mp3 \
  --output data/generated/reels/my_reel/reel.mp4
```

Example (narrated):
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_slideshow.py \
  --images shot1.jpg shot2.jpg shot3.jpg \
  --music data/music/peaceful_nyckelharpa_norse_142s.mp3 \
  --narration data/generated/reels/my_reel/narration.wav \
  --output data/generated/reels/my_reel/reel.mp4
```

---

### 4. generate_nsfw_image.py — NSFW image generation via Flux + PuLID on Modal ComfyUI

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_nsfw_image.py \
  --prompt "scene description" \
  --output path/to/output.jpg \
  --face-ref path/to/face_reference.jpg \
  --workflow path/to/workflow_template.json \
  [--aspect 4:5] \
  [--lora-strength 0.9] \
  [--seed 12345]
```

Arguments:
- `--prompt` (required) — Scene description
- `--output` (required) — Output image path
- `--face-ref` (required) — Face reference image for PuLID consistency
- `--workflow` (required) — ComfyUI workflow JSON template
- `--aspect` (default: `4:5`) — Choices: `4:5`, `16:9`, `9:16`, `1:1`
- `--lora-strength` (optional, default: `0.9`)
- `--seed` (optional) — Reproducible generation

Example:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_nsfw_image.py \
  --prompt "intimate portrait, soft candlelight" \
  --output data/generated/reels/shield_maiden/shot1.jpg \
  --face-ref data/reference_images/canonical/face.jpg \
  --workflow modal/workflows/nsfw_image.json \
  --aspect 4:5
```

---

### 5. generate_nsfw_video.py — NSFW video generation via Wan 2.2 on Modal ComfyUI

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_nsfw_video.py \
  --image path/to/starting_frame.jpg \
  --prompt "motion description" \
  --output path/to/output.mp4 \
  --workflow path/to/workflow_template.json \
  [--frames 81] \
  [--resolution 480p] \
  [--fps 12] \
  [--steps 14] \
  [--seed 12345]
```

Arguments:
- `--image` (required) — Starting frame image (can be SFW image from generate_image.py)
- `--prompt` (required) — Motion/action description
- `--output` (required) — Output MP4 path
- `--workflow` (required) — ComfyUI workflow JSON template
- `--frames` (optional, default: `81`)
- `--resolution` (optional, default: `480p`) — Choices: `480p`, `720p`
- `--fps` (optional, default: `12`)
- `--steps` (optional, default: `14`)
- `--seed` (optional)

Example:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_nsfw_video.py \
  --image data/generated/shot1.jpg \
  --prompt "slowly removes cloak, intimate, soft motion" \
  --output data/generated/reels/ppv/clip1.mp4 \
  --workflow modal/workflows/nsfw_video.json \
  --frames 81 \
  --resolution 480p
```

---

### 6. comfyui_client.py — Modal ComfyUI HTTP client (library, not CLI)

Not a CLI script — imported by generate_nsfw_image.py and generate_nsfw_video.py. Handles workflow submission and polling against the Modal ComfyUI endpoint.

Requires `MODAL_COMFYUI_URL` environment variable.

---

### 7. schedule_instagram.py — Instagram scheduling via Zernio API (formerly Late)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/schedule_instagram.py \
  --media path/to/media_file \
  --caption "caption text" \
  [--schedule "2026-03-16T18:00:00"] \
  [--timezone "Europe/Berlin"] \
  [--publish-now] \
  [--account-id ACCOUNT_ID]
```

Arguments:
- `--media` (required) — Media file path (image or video)
- `--caption` (required) — Caption text
- `--schedule` (optional) — ISO 8601 datetime for scheduled posting
- `--timezone` (optional, default: `Europe/Berlin`)
- `--publish-now` (optional flag) — Publish immediately instead of scheduling
- `--account-id` (optional) — Override `ZERNIO_INSTAGRAM_ACCOUNT_ID` env var

Upload flow (handled automatically by the script):
1. `POST /v1/media/upload-token` → get upload token
2. `POST /v1/media/upload?token=TOKEN` with `files=` multipart field → get media URL
3. `POST /v1/posts` with `mediaItems: [{url}]` → schedule/publish

Example (scheduled):
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/schedule_instagram.py \
  --media data/generated/ready/2026-03-16/free/shot1.jpg \
  --caption "The forest was quiet this morning." \
  --schedule "2026-03-16T18:00:00" \
  --timezone "Europe/Berlin"
```

Example (publish now):
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/schedule_instagram.py \
  --media data/generated/ready/2026-03-16/free/reel.mp4 \
  --caption "First light over the settlement." \
  --publish-now
```

---

## Environment Variables

| Variable | Required for |
|---|---|
| `REPLICATE_API_TOKEN` | `generate_image.py`, `generate_voice.py` |
| `MODAL_COMFYUI_URL` | `generate_nsfw_image.py`, `generate_nsfw_video.py` |
| `ZERNIO_API_KEY` (or `LATE_API_KEY`) | `schedule_instagram.py` |
| `ZERNIO_INSTAGRAM_ACCOUNT_ID` (or `LATE_INSTAGRAM_ACCOUNT_ID`) | `schedule_instagram.py` (or pass `--account-id`) |

## Script Paths

All scripts are at: `${CLAUDE_PLUGIN_ROOT}/scripts/`

## Zernio API — Managing Instagram Posts

Late rebranded to Zernio (`zernio.com`). The API is identical, just a new domain. Old `LATE_API_KEY` env vars still work.

The `schedule_instagram.py` script handles uploading and scheduling. For post management, use curl directly:

```bash
# List scheduled posts
curl -s -H "Authorization: Bearer $ZERNIO_API_KEY" \
  "https://zernio.com/api/v1/posts?status=scheduled"

# List published posts
curl -s -H "Authorization: Bearer $ZERNIO_API_KEY" \
  "https://zernio.com/api/v1/posts?status=published"

# Update a scheduled/draft post
curl -s -X PATCH -H "Authorization: Bearer $ZERNIO_API_KEY" \
  -H "Content-Type: application/json" \
  "https://zernio.com/api/v1/posts/POST_ID" \
  -d '{"content": "Updated caption"}'

# Delete a scheduled/draft post
curl -s -X DELETE -H "Authorization: Bearer $ZERNIO_API_KEY" \
  "https://zernio.com/api/v1/posts/POST_ID"

# Retry a failed post
curl -s -X POST -H "Authorization: Bearer $ZERNIO_API_KEY" \
  "https://zernio.com/api/v1/posts/POST_ID/retry"

# Check account health
curl -s -H "Authorization: Bearer $ZERNIO_API_KEY" \
  "https://zernio.com/api/v1/accounts/ACCOUNT_ID/health"
```

Post statuses: `draft` → `scheduled` → `publishing` → `published` | `failed`
