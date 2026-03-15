---
name: late-instagram
description: Use when scheduling or publishing Instagram posts, reels, carousels, or stories via the Late API - also covers media upload, analytics, and multi-platform posting
---

# Late API — Instagram Scheduling

Schedule and publish Instagram posts via the Late unified social media API.

## Setup

**API Key:** Stored in `LATE_API_KEY` env var (prefix `sk_`).
**Base URL:** `https://getlate.dev/api/v1`
**Auth header:** `Authorization: Bearer $LATE_API_KEY`

## Core Workflow

```
1. List accounts → get accountId
2. Upload media (if needed) → get publicUrl
3. Create post with scheduledFor or publishNow
```

## Quick Reference

### List connected accounts

```bash
curl -s -H "Authorization: Bearer $LATE_API_KEY" \
  "https://getlate.dev/api/v1/accounts"
```

Response includes `_id` (accountId), `platform`, `username`, `profileId._id`.

### Upload media

```bash
# 1. Get presigned upload URL
curl -s -H "Authorization: Bearer $LATE_API_KEY" \
  "https://getlate.dev/api/v1/media/presigned-url?fileName=photo.jpg&contentType=image/jpeg"

# Response: { "uploadUrl": "...", "publicUrl": "..." }

# 2. Upload file via PUT
curl -X PUT -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg "$UPLOAD_URL"

# 3. Use publicUrl in post creation
```

Supports files up to 5GB. Instagram requires media on every post (no text-only).

### Schedule a post

```bash
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/posts" \
  -d '{
    "content": "Caption here #hashtags",
    "platforms": [{"platform": "instagram", "accountId": "ACCOUNT_ID"}],
    "media": [{"url": "PUBLIC_URL_FROM_UPLOAD"}],
    "scheduledFor": "2026-03-20T14:00:00Z",
    "timezone": "Europe/Berlin"
  }'
```

### Publish immediately

```bash
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/posts" \
  -d '{
    "content": "Caption here",
    "platforms": [{"platform": "instagram", "accountId": "ACCOUNT_ID"}],
    "media": [{"url": "PUBLIC_URL"}],
    "publishNow": true
  }'
```

Response includes `platformPostUrl` with the live Instagram URL.

### Create a carousel (multi-image)

```bash
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/posts" \
  -d '{
    "content": "Swipe through!",
    "platforms": [{"platform": "instagram", "accountId": "ACCOUNT_ID"}],
    "media": [
      {"url": "PUBLIC_URL_1"},
      {"url": "PUBLIC_URL_2"},
      {"url": "PUBLIC_URL_3"}
    ],
    "scheduledFor": "2026-03-20T14:00:00Z",
    "timezone": "Europe/Berlin"
  }'
```

### Save as draft (no schedule, no publishNow)

```bash
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/posts" \
  -d '{
    "content": "Draft caption",
    "platforms": [{"platform": "instagram", "accountId": "ACCOUNT_ID"}],
    "media": [{"url": "PUBLIC_URL"}]
  }'
```

## Managing Posts

```bash
# List posts
curl -s -H "Authorization: Bearer $LATE_API_KEY" \
  "https://getlate.dev/api/v1/posts?status=scheduled"

# Update a scheduled/draft post
curl -s -X PATCH -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/posts/POST_ID" \
  -d '{"content": "Updated caption"}'

# Delete a scheduled/draft post
curl -s -X DELETE -H "Authorization: Bearer $LATE_API_KEY" \
  "https://getlate.dev/api/v1/posts/POST_ID"

# Retry a failed post
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  "https://getlate.dev/api/v1/posts/POST_ID/retry"

# Unpublish a published post
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  "https://getlate.dev/api/v1/posts/POST_ID/unpublish"
```

## Multi-Platform Posting

Post to Instagram + other platforms simultaneously:

```bash
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/posts" \
  -d '{
    "content": "Cross-platform post",
    "platforms": [
      {"platform": "instagram", "accountId": "IG_ACCOUNT_ID"},
      {"platform": "facebook", "accountId": "FB_ACCOUNT_ID"},
      {"platform": "threads", "accountId": "THREADS_ACCOUNT_ID"}
    ],
    "media": [{"url": "PUBLIC_URL"}],
    "publishNow": true
  }'
```

## Validation

```bash
# Check media is valid for Instagram
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/validate/media" \
  -d '{"url": "PUBLIC_URL", "platform": "instagram"}'

# Check caption length
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/validate/post-length" \
  -d '{"content": "Caption text", "platform": "instagram"}'

# Check hashtag safety
curl -s -X POST -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://getlate.dev/api/v1/tools/check-hashtags" \
  -d '{"hashtags": ["fitness", "gym"]}'
```

## Useful Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /v1/accounts` | List connected accounts |
| `GET /v1/accounts/{id}/health` | Check account connection health |
| `GET /v1/profiles` | List profiles |
| `GET /v1/posts?status=scheduled` | List scheduled posts |
| `GET /v1/posts?status=published` | List published posts |
| `GET /v1/analytics/best-time-to-post` | Optimal posting times |
| `GET /v1/usage` | Check plan limits and usage |
| `GET /v1/comments` | List posts with comments |
| `POST /v1/comments/{id}/reply` | Reply to a comment |

## Post Statuses

`draft` → `scheduled` → `publishing` → `published` | `failed` | `partial` | `cancelled`

## Connected Account

- **vikinggirldk** (Instagram, MEDIA_CREATOR)
- Account ID: `69b68ea6f7920cff86c70e92`
- Profile ID: `69b68e53526a3d3d0fceedc4` (Default Profile)
- Token expires: 2026-05-14 (refresh before then)

## Common Mistakes

- **Forgetting media on Instagram posts** — Instagram requires at least one image or video, text-only posts will fail
- **Using local file paths instead of uploaded URLs** — must upload via presigned URL first
- **Scheduling in the past** — `scheduledFor` must be in the future
- **Not refreshing expired tokens** — check `GET /v1/accounts/{id}/health` if posts start failing
