#!/usr/bin/env python3
"""
Compose a Ken Burns + crossfade slideshow reel from images with music.

Supports two modes:
  - Music only: images + background music
  - Narrated: images + voiceover at full volume + ducked music

Usage:
    # Music only
    python3 scripts/generate_slideshow.py \
        --images shot1.jpg shot2.jpg shot3.jpg \
        --music music/track.mp3 \
        --output output/reel.mp4

    # With narration
    python3 scripts/generate_slideshow.py \
        --images shot1.jpg shot2.jpg shot3.jpg \
        --narration output/narration.wav \
        --music music/track.mp3 \
        --output output/reel.mp4

    # Custom duration per image (default: 4s, or auto-scaled to narration length)
    python3 scripts/generate_slideshow.py \
        --images shot1.jpg shot2.jpg shot3.jpg \
        --music music/track.mp3 \
        --duration 5 \
        --output reel.mp4
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def get_duration(audio_path: Path) -> float:
    """Get audio duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(audio_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error: ffprobe failed on {audio_path}", file=sys.stderr)
        sys.exit(1)
    return float(json.loads(result.stdout)["format"]["duration"])


def build_command(
    images: list[Path],
    music: Path,
    output: Path,
    narration: Path | None = None,
    duration: float | None = None,
    fade_dur: float = 1.0,
    width: int = 1080,
    height: int = 1920,
    fps: int = 30,
) -> list[str]:
    """Build the ffmpeg command for Ken Burns + crossfade composition."""
    n = len(images)

    # Determine per-image duration
    if duration is not None:
        dur = duration
    elif narration is not None:
        narration_dur = get_duration(narration)
        dur = max(3.0, narration_dur / n)
    else:
        dur = 4.0

    total_frames = int(dur * fps)
    total_video_dur = n * dur - (n - 1) * fade_dur

    # Input streams
    inputs = []
    for img in images:
        inputs.extend(["-loop", "1", "-t", str(dur), "-framerate", str(fps), "-i", str(img)])

    if narration is not None:
        inputs.extend(["-i", str(narration)])
        inputs.extend(["-i", str(music)])
        narr_idx = n
        music_idx = n + 1
    else:
        inputs.extend(["-i", str(music)])
        music_idx = n

    # Video filters: scale, crop, Ken Burns zoom
    filter_parts = []
    for i in range(n):
        zoom_expr = f"1.0+(0.08)*on/{total_frames}"
        x_expr = "(iw-iw*zoom)/2"
        y_expr = "(ih-ih*zoom)/2"
        filter_parts.append(
            f"[{i}:v]scale={width * 2}:{height * 2}:force_original_aspect_ratio=increase,"
            f"crop={width * 2}:{height * 2},"
            f"zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}'"
            f":d={total_frames}:s={width}x{height}:fps={fps},"
            f"format=yuv420p,setpts=PTS-STARTPTS[v{i}]"
        )

    # Chain xfade transitions
    prev = "v0"
    for i in range(1, n):
        offset = i * dur - i * fade_dur
        out_label = f"xf{i - 1}" if i < n - 1 else "vout"
        filter_parts.append(
            f"[{prev}][v{i}]xfade=transition=fade:duration={fade_dur}"
            f":offset={offset},setpts=PTS-STARTPTS[{out_label}]"
        )
        prev = out_label

    # Audio filters
    if narration is not None:
        # Narrated: voice at full volume, music ducked to 20%
        filter_parts.append(
            f"[{narr_idx}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=1.0[voice]"
        )
        filter_parts.append(
            f"[{music_idx}:a]atrim=0:{total_video_dur},afade=t=in:d=1,"
            f"afade=t=out:st={total_video_dur - 2}:d=2,volume=0.2[bgmusic]"
        )
        filter_parts.append(
            "[voice][bgmusic]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        )
    else:
        # Music only: trim and fade
        filter_parts.append(
            f"[{music_idx}:a]atrim=0:{total_video_dur},afade=t=in:d=1,"
            f"afade=t=out:st={total_video_dur - 2}:d=2,volume=0.85[aout]"
        )

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";\n".join(filter_parts),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(output),
    ]
    return cmd


def main():
    parser = argparse.ArgumentParser(
        description="Compose a Ken Burns + crossfade slideshow reel with music (and optional narration)."
    )
    parser.add_argument("--images", type=Path, nargs="+", required=True, help="Input images in order.")
    parser.add_argument("--music", type=Path, required=True, help="Background music track.")
    parser.add_argument("--output", type=Path, required=True, help="Output MP4 path.")
    parser.add_argument("--narration", type=Path, default=None, help="Voiceover WAV (enables narrated mode).")
    parser.add_argument("--duration", type=float, default=None, help="Seconds per image (default: 4, or auto from narration).")
    parser.add_argument("--fade", type=float, default=1.0, help="Crossfade duration in seconds (default: 1).")
    parser.add_argument("--width", type=int, default=1080, help="Output width (default: 1080).")
    parser.add_argument("--height", type=int, default=1920, help="Output height (default: 1920).")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30).")
    args = parser.parse_args()

    # Validate inputs
    for img in args.images:
        if not img.exists():
            print(f"Error: image not found: {img}", file=sys.stderr)
            sys.exit(1)
    if not args.music.exists():
        print(f"Error: music not found: {args.music}", file=sys.stderr)
        sys.exit(1)
    if args.narration and not args.narration.exists():
        print(f"Error: narration not found: {args.narration}", file=sys.stderr)
        sys.exit(1)

    n = len(args.images)
    mode = "narrated" if args.narration else "music-only"
    print(f"Composing {mode} slideshow...")
    print(f"  Images: {n}")
    print(f"  Music: {args.music.name}")
    if args.narration:
        print(f"  Narration: {args.narration}")
    print(f"  Output: {args.output}")
    print(f"  Resolution: {args.width}x{args.height} @ {args.fps}fps")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    cmd = build_command(
        images=args.images,
        music=args.music,
        output=args.output,
        narration=args.narration,
        duration=args.duration,
        fade_dur=args.fade,
        width=args.width,
        height=args.height,
        fps=args.fps,
    )

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"Error: ffmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    size_kb = args.output.stat().st_size // 1024
    print(f"  Saved: {args.output} ({size_kb} KB)")


if __name__ == "__main__":
    main()
