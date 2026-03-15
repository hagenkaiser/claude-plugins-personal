#!/usr/bin/env python3
"""
Generate diary-style voiceover narration using qwen/qwen3-tts on Replicate.

Uses voice_clone mode with a reference audio file to match the target voice.
Uses the Replicate HTTP API (not the SDK, which is broken on Python 3.14).

For large reference audio files (>2MB), the file is uploaded via the Replicate
Files API before submitting the prediction.

Usage:
    python3 scripts/generate_voice.py \
        --text "The frost never left the fjord today." \
        --voice-ref path/to/voice_reference.wav \
        --output output/narration.wav

    # With optional reference text (transcript of the voice reference):
    python3 scripts/generate_voice.py \
        --text "The frost never left the fjord today." \
        --voice-ref path/to/voice_reference.wav \
        --reference-text "This is what the voice reference says." \
        --output output/narration.wav
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def upload_file(token: str, file_path: Path) -> str:
    """Upload a file to Replicate Files API. Returns the file URL."""
    data = file_path.read_bytes()
    content_type = "audio/wav"

    req = Request(
        "https://api.replicate.com/v1/files",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
            "Content-Length": str(len(data)),
        },
    )
    with urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())

    return result["urls"]["get"]


def create_prediction(
    token: str,
    text: str,
    voice_ref_url: str,
    reference_text: str,
    style_instruction: str,
) -> dict:
    """Submit a TTS prediction to Replicate. Returns the result or prediction dict."""
    inputs = {
        "mode": "voice_clone",
        "text": text,
        "reference_audio": voice_ref_url,
        "language": "auto",
    }
    if reference_text:
        inputs["reference_text"] = reference_text
    if style_instruction:
        inputs["style_instruction"] = style_instruction

    payload = json.dumps({
        "version": "qwen/qwen3-tts",
        "input": inputs,
    }).encode()

    req = Request(
        "https://api.replicate.com/v1/models/qwen/qwen3-tts/predictions",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "wait",
        },
    )
    with urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())

    if result.get("status") == "succeeded" and result.get("output"):
        return result

    # If not done yet, poll
    pred_id = result["id"]
    return poll_prediction(token, pred_id)


def poll_prediction(token: str, pred_id: str) -> dict:
    """Poll a prediction until it completes."""
    url = f"https://api.replicate.com/v1/predictions/{pred_id}"
    for _ in range(120):
        req = Request(url, headers={"Authorization": f"Bearer {token}"})
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        status = result.get("status")
        if status == "succeeded":
            return result
        if status in ("failed", "canceled"):
            print(f"Error: prediction {status}: {result.get('error')}", file=sys.stderr)
            sys.exit(1)
        time.sleep(3)
    print("Error: prediction timed out after 360s", file=sys.stderr)
    sys.exit(1)


def download_output(result: dict, output: Path) -> None:
    """Download the audio output from a completed prediction."""
    out = result["output"]
    url = out[0] if isinstance(out, list) else str(out)
    req = Request(url)
    with urlopen(req, timeout=120) as resp:
        data = resp.read()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    size_kb = len(data) // 1024
    print(f"Saved: {output} ({size_kb} KB)")


def generate_voice(
    text: str,
    voice_ref: Path,
    output: Path,
    reference_text: str = "",
    style_instruction: str = "",
) -> None:
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("Error: REPLICATE_API_TOKEN is not set.", file=sys.stderr)
        sys.exit(1)

    if not voice_ref.exists():
        print(f"Error: voice reference not found: {voice_ref}", file=sys.stderr)
        sys.exit(1)

    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating voice narration...")
    print(f"  Text: {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"  Voice ref: {voice_ref}")
    if style_instruction:
        print(f"  Style: {style_instruction}")

    # Upload voice reference via Files API (avoids 2MB data URI limit)
    print(f"  Uploading voice reference...")
    voice_ref_url = upload_file(token, voice_ref)

    result = create_prediction(
        token=token,
        text=text,
        voice_ref_url=voice_ref_url,
        reference_text=reference_text,
        style_instruction=style_instruction,
    )

    download_output(result, output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate TTS narration using qwen/qwen3-tts on Replicate."
    )
    parser.add_argument("--text", required=True, help="Narration text to synthesize.")
    parser.add_argument(
        "--voice-ref",
        type=Path,
        required=True,
        help="Path to voice reference WAV (required).",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output WAV path.")
    parser.add_argument(
        "--reference-text",
        type=str,
        default="",
        help="Transcript of the reference audio (optional, improves cloning quality).",
    )
    parser.add_argument(
        "--style",
        type=str,
        default="",
        help="Style/emotion instruction (e.g., 'speak slowly and calmly', 'soft whisper').",
    )

    args = parser.parse_args()

    generate_voice(
        text=args.text,
        voice_ref=args.voice_ref,
        output=args.output,
        reference_text=args.reference_text,
        style_instruction=args.style,
    )


if __name__ == "__main__":
    main()
