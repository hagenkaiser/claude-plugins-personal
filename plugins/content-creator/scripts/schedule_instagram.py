#!/usr/bin/env python3
"""
Schedule or publish an Instagram post via the Zernio API (formerly Late).

Upload flow:
  1. POST /v1/media/upload-token → get upload token
  2. POST /v1/media/upload?token=TOKEN with files= multipart field
  3. POST /v1/posts with mediaItems=[{url}]

Usage:
    # Schedule for a specific time
    python3 scripts/schedule_instagram.py \\
        --media reel.mp4 \\
        --caption "Caption text #hashtags" \\
        --schedule "2026-03-20T18:00:00" \\
        --timezone "Europe/Berlin"

    # Publish immediately
    python3 scripts/schedule_instagram.py \\
        --media reel.mp4 \\
        --caption "Caption text" \\
        --publish-now

    # Save as draft
    python3 scripts/schedule_instagram.py \\
        --media reel.mp4 \\
        --caption "Draft caption"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ZERNIO_API_BASE = "https://zernio.com/api/v1"

CONTENT_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/mp4",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}


def detect_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    ct = CONTENT_TYPES.get(ext)
    if not ct:
        print(f"Error: unsupported file extension '{ext}'. Supported: {', '.join(CONTENT_TYPES)}", file=sys.stderr)
        sys.exit(1)
    return ct


def get_upload_token(api_key: str, filename: str, content_type: str) -> str:
    """Step 1: Get an upload token from Zernio."""
    payload = json.dumps({"fileName": filename, "contentType": content_type}).encode()
    req = Request(
        f"{ZERNIO_API_BASE}/media/upload-token",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["token"]
    except HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"Error: Zernio API returned {e.code} for upload token: {body}", file=sys.stderr)
        sys.exit(1)


def upload_media(upload_token: str, media_path: Path, content_type: str) -> str:
    """Step 2: Upload media via multipart POST with token. Returns the media URL."""
    import subprocess
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "-F", f"files=@{media_path};type={content_type}",
            f"{ZERNIO_API_BASE}/media/upload?token={upload_token}",
        ],
        capture_output=True, text=True,
    )
    try:
        data = json.loads(result.stdout)
        if "error" in data:
            print(f"Error: media upload failed: {data['error']}", file=sys.stderr)
            sys.exit(1)
        return data["files"][0]["url"]
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        print(f"Error: unexpected upload response: {result.stdout[:200]}", file=sys.stderr)
        sys.exit(1)


def create_post(api_key: str, caption: str, account_id: str, media_url: str,
                schedule: str | None, timezone: str, publish_now: bool) -> dict:
    """Step 3: Create the post on Zernio."""
    body: dict = {
        "content": caption,
        "platforms": [{"platform": "instagram", "accountId": account_id}],
        "mediaItems": [{"url": media_url}],
    }
    if publish_now:
        body["publishNow"] = True
    elif schedule:
        body["scheduledFor"] = schedule
        body["timezone"] = timezone

    payload = json.dumps(body).encode()
    req = Request(
        f"{ZERNIO_API_BASE}/posts",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        body_text = e.read().decode(errors="replace")
        print(f"Error: Zernio API returned {e.code} for post creation: {body_text}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Schedule or publish an Instagram post via the Late API."
    )
    parser.add_argument("--media", type=Path, required=True, help="Path to media file (image or video).")
    parser.add_argument("--caption", required=True, help="Caption text.")
    parser.add_argument(
        "--schedule", default=None,
        help="ISO 8601 datetime to schedule the post (e.g. 2026-03-20T18:00:00Z).",
    )
    parser.add_argument(
        "--timezone", default="Europe/Berlin",
        help="Timezone for scheduled post (default: Europe/Berlin).",
    )
    parser.add_argument(
        "--publish-now", action="store_true",
        help="Publish immediately instead of scheduling.",
    )
    parser.add_argument(
        "--account-id", default=None,
        help="Override LATE_INSTAGRAM_ACCOUNT_ID env var.",
    )
    args = parser.parse_args()

    # Validate env / args (accept both old LATE_ and new ZERNIO_ env vars)
    api_key = os.environ.get("ZERNIO_API_KEY") or os.environ.get("LATE_API_KEY")
    if not api_key:
        print("Error: ZERNIO_API_KEY (or LATE_API_KEY) is not set.", file=sys.stderr)
        sys.exit(1)

    account_id = args.account_id or os.environ.get("ZERNIO_INSTAGRAM_ACCOUNT_ID") or os.environ.get("LATE_INSTAGRAM_ACCOUNT_ID")
    if not account_id:
        print("Error: ZERNIO_INSTAGRAM_ACCOUNT_ID is not set and --account-id was not provided.", file=sys.stderr)
        sys.exit(1)

    if not args.media.exists():
        print(f"Error: media file not found: {args.media}", file=sys.stderr)
        sys.exit(1)

    if args.publish_now and args.schedule:
        print("Error: --publish-now and --schedule are mutually exclusive.", file=sys.stderr)
        sys.exit(1)

    content_type = detect_content_type(args.media)
    file_size_kb = args.media.stat().st_size // 1024
    caption_preview = args.caption[:60] + ("..." if len(args.caption) > 60 else "")

    # Print summary
    mode = "now" if args.publish_now else (f"{args.schedule} ({args.timezone})" if args.schedule else "draft")
    if args.publish_now:
        print("Publishing Instagram post immediately...")
    elif args.schedule:
        print("Scheduling Instagram post...")
    else:
        print("Saving Instagram post as draft...")

    print(f"  Media: {args.media.name} ({file_size_kb} KB, {content_type})")
    print(f"  Caption: {caption_preview} ({len(args.caption)} chars)")
    if args.schedule:
        print(f"  Schedule: {args.schedule} ({args.timezone})")

    # Step 1: Get upload token
    print("  Getting upload token...")
    upload_token = get_upload_token(api_key, args.media.name, content_type)

    # Step 2: Upload media
    print("  Uploading media...")
    media_url = upload_media(upload_token, args.media, content_type)
    print(f"  Uploaded: {media_url}")

    # Step 3: Create post
    print("  Creating post...")
    result = create_post(
        api_key=api_key,
        caption=args.caption,
        account_id=account_id,
        media_url=media_url,
        schedule=args.schedule,
        timezone=args.timezone,
        publish_now=args.publish_now,
    )

    post_data = result.get("post", result)
    post_id = post_data.get("_id") or post_data.get("id") or post_data.get("postId", "unknown")
    status = post_data.get("status", result.get("message", "unknown"))
    print(f"  Post created: {post_id}")
    print(f"  Status: {status}")

    if args.schedule and result.get("scheduledFor"):
        print(f"  Scheduled for: {result['scheduledFor']}")

    platform_url = result.get("platformPostUrl")
    if platform_url:
        print(f"  Platform URL: {platform_url}")


if __name__ == "__main__":
    main()
