#!/usr/bin/env python3
"""
Generate SFW images using Nano Banana Pro on Replicate.

Uses the Replicate HTTP API (not the SDK, which is broken on Python 3.14).

Usage:
    python3 scripts/generate_image.py \
        --prompt "She is sitting by a campfire, carving a wooden spoon" \
        --face-ref path/to/face_reference.jpg \
        --output output/shot1.jpg \
        --aspect 4:5
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

PROMPT_PREFIX = "Generate a new photo of this exact same woman."

ASPECT_CHOICES = ["4:5", "16:9", "9:16", "1:1"]


def create_prediction(token: str, prompt: str, face_ref: Path, aspect_ratio: str) -> str:
    """Submit a prediction to Replicate and return the prediction ID."""
    image_bytes = face_ref.read_bytes()
    image_b64 = base64.b64encode(image_bytes).decode()
    data_uri = f"data:image/jpeg;base64,{image_b64}"

    payload = json.dumps({
        "version": "google/nano-banana-pro",
        "input": {
            "prompt": f"{PROMPT_PREFIX} {prompt}",
            "image_input": [data_uri],
            "aspect_ratio": aspect_ratio,
            "output_format": "jpg",
            "safety_filter_level": "block_only_high",
        },
    }).encode()

    req = Request(
        "https://api.replicate.com/v1/models/google/nano-banana-pro/predictions",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "wait",
        },
    )
    with urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())

    if result.get("status") == "succeeded" and result.get("output"):
        return result

    # If not done yet, poll
    pred_id = result["id"]
    return poll_prediction(token, pred_id)


def poll_prediction(token: str, pred_id: str) -> dict:
    """Poll a prediction until it completes."""
    url = f"https://api.replicate.com/v1/predictions/{pred_id}"
    for _ in range(60):
        req = Request(url, headers={"Authorization": f"Bearer {token}"})
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        status = result.get("status")
        if status == "succeeded":
            return result
        if status in ("failed", "canceled"):
            print(f"Error: prediction {status}: {result.get('error')}", file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
    print("Error: prediction timed out after 120s", file=sys.stderr)
    sys.exit(1)


def download_output(result: dict, output: Path) -> None:
    """Download the output image from a completed prediction."""
    out = result["output"]
    url = out[0] if isinstance(out, list) else str(out)
    req = Request(url)
    with urlopen(req, timeout=60) as resp:
        data = resp.read()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    print(f"  Saved: {output} ({len(data) // 1024} KB)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SFW images via Nano Banana Pro on Replicate."
    )
    parser.add_argument("--prompt", required=True, help="Scene description (prefix is added automatically).")
    parser.add_argument("--output", type=Path, required=True, help="Output image path.")
    parser.add_argument(
        "--face-ref", type=Path, required=True,
        help="Face reference image (required).",
    )
    parser.add_argument(
        "--aspect", choices=ASPECT_CHOICES, default="4:5",
        help="Aspect ratio (default: 4:5).",
    )
    args = parser.parse_args()

    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("Error: REPLICATE_API_TOKEN is not set.", file=sys.stderr)
        sys.exit(1)

    if not args.face_ref.exists():
        print(f"Error: face reference not found: {args.face_ref}", file=sys.stderr)
        sys.exit(1)

    full_prompt = f"{PROMPT_PREFIX} {args.prompt}"
    print(f"Generating image...")
    print(f"  Prompt: {full_prompt[:100]}{'...' if len(full_prompt) > 100 else ''}")
    print(f"  Face ref: {args.face_ref}")
    print(f"  Aspect: {args.aspect}")

    result = create_prediction(token, args.prompt, args.face_ref, args.aspect)
    download_output(result, args.output)


if __name__ == "__main__":
    main()
