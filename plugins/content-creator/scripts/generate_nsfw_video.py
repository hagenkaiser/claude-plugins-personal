#!/usr/bin/env python3
"""
Generate NSFW video clips using Wan 2.2 AIO NSFW on Modal ComfyUI.

Usage:
    python3 scripts/generate_nsfw_video.py \
        --image path/to/starting_frame.jpg \
        --prompt "she moves slowly, eyes closed, candlelight" \
        --output output/nsfw_clip.mp4 \
        --workflow path/to/wan22_i2v_nsfw.json \
        --frames 81 \
        --resolution 480p
"""

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comfyui_client import ComfyUIError, run_workflow, upload_image

RESOLUTIONS = {
    "480p": (512, 512),   # Wan 2.2 AIO uses square at 512px
    "720p": (720, 720),   # Higher res, needs more VRAM
}


def build_workflow(
    workflow_template: Path,
    prompt: str,
    image_filename: str,
    num_frames: int,
    width: int,
    height: int,
    steps: int,
    fps: int,
    seed: int,
) -> dict:
    """Load workflow template and fill in dynamic values."""
    wf = json.loads(workflow_template.read_text())
    # Set values directly to preserve correct types (int, float, str)
    wf["3"]["inputs"]["image"] = image_filename
    wf["5"]["inputs"]["text"] = prompt
    wf["7"]["inputs"]["width"] = width
    wf["7"]["inputs"]["height"] = height
    wf["7"]["inputs"]["length"] = num_frames
    wf["8"]["inputs"]["seed"] = seed
    wf["8"]["inputs"]["steps"] = steps
    wf["10"]["inputs"]["frame_rate"] = float(fps)
    return wf


def main():
    parser = argparse.ArgumentParser(
        description="Generate NSFW video clips via Wan 2.2 on Modal ComfyUI."
    )
    parser.add_argument("--image", type=Path, required=True, help="Starting frame image.")
    parser.add_argument("--prompt", required=True, help="Motion/action description.")
    parser.add_argument("--output", type=Path, required=True, help="Output MP4 path.")
    parser.add_argument(
        "--workflow", type=Path, required=True,
        help="Path to ComfyUI workflow JSON template (required, project-specific).",
    )
    parser.add_argument(
        "--frames", type=int, default=81,
        help="Number of frames (default: 81, ~5s at 16fps).",
    )
    parser.add_argument(
        "--resolution", choices=list(RESOLUTIONS.keys()), default="480p",
        help="Video resolution (default: 480p).",
    )
    parser.add_argument("--fps", type=int, default=12, help="Frames per second (default: 12).")
    parser.add_argument("--steps", type=int, default=14, help="Sampling steps (default: 14).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"Error: starting image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    if not args.workflow.exists():
        print(f"Error: workflow template not found: {args.workflow}", file=sys.stderr)
        sys.exit(1)

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    width, height = RESOLUTIONS[args.resolution]

    print(f"Generating NSFW video clip...")
    print(f"  Image: {args.image}")
    print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
    print(f"  Workflow: {args.workflow}")
    print(f"  Frames: {args.frames} @ {args.fps}fps ({args.frames / args.fps:.1f}s)")
    print(f"  Resolution: {args.resolution} ({width}x{height})")
    print(f"  Steps: {args.steps}")
    print(f"  Seed: {seed}")

    # Upload starting frame
    print(f"  Uploading starting frame...")
    image_filename = upload_image(args.image)

    # Build and submit workflow
    workflow = build_workflow(
        workflow_template=args.workflow,
        prompt=args.prompt,
        image_filename=image_filename,
        num_frames=args.frames,
        width=width,
        height=height,
        steps=args.steps,
        fps=args.fps,
        seed=seed,
    )

    try:
        result = run_workflow(workflow, args.output, timeout=300)
        size_kb = result.stat().st_size // 1024
        print(f"  Saved: {result} ({size_kb} KB)")
    except (ComfyUIError, TimeoutError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
