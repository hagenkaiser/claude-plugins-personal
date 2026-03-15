#!/usr/bin/env python3
"""
Generate NSFW images using Flux Dev + PuLID + NSFW LoRA on Modal ComfyUI.

Usage:
    python3 scripts/generate_nsfw_image.py \
        --prompt "woman lying nude on wool blanket, candlelit shelter" \
        --output output/nsfw_frame.jpg \
        --face-ref path/to/face_reference.jpg \
        --workflow path/to/flux_pulid_nsfw.json \
        --aspect 4:5
"""

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comfyui_client import ComfyUIError, run_workflow, upload_image

TRIGGER_WORD = "aidmaNSFWunlock"

ASPECT_RATIOS = {
    "4:5": (768, 960),
    "16:9": (1216, 688),
    "9:16": (688, 1216),
    "1:1": (832, 832),
}


def build_workflow(
    workflow_template: Path,
    prompt: str,
    face_ref_filename: str,
    width: int,
    height: int,
    lora_strength: float,
    seed: int,
) -> dict:
    """Load workflow template and fill in dynamic values."""
    wf = json.loads(workflow_template.read_text())
    # Set values directly to preserve correct types (int, float, str)
    wf["7"]["inputs"]["image"] = face_ref_filename
    wf["9"]["inputs"]["strength_model"] = lora_strength
    wf["10"]["inputs"]["text"] = f"{TRIGGER_WORD} {prompt}"
    wf["12"]["inputs"]["width"] = width
    wf["12"]["inputs"]["height"] = height
    wf["13"]["inputs"]["seed"] = seed
    return wf


def main():
    parser = argparse.ArgumentParser(
        description="Generate NSFW images via Flux + PuLID on Modal ComfyUI."
    )
    parser.add_argument("--prompt", required=True, help="Scene description.")
    parser.add_argument("--output", type=Path, required=True, help="Output image path.")
    parser.add_argument(
        "--face-ref", type=Path, required=True,
        help="Face reference image (required).",
    )
    parser.add_argument(
        "--workflow", type=Path, required=True,
        help="Path to ComfyUI workflow JSON template (required, project-specific).",
    )
    parser.add_argument(
        "--aspect", choices=list(ASPECT_RATIOS.keys()), default="4:5",
        help="Aspect ratio (default: 4:5).",
    )
    parser.add_argument(
        "--lora-strength", type=float, default=0.9,
        help="NSFW LoRA strength 0.0-1.0 (default: 0.9).",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    args = parser.parse_args()

    if not args.face_ref.exists():
        print(f"Error: face reference not found: {args.face_ref}", file=sys.stderr)
        sys.exit(1)

    if not args.workflow.exists():
        print(f"Error: workflow template not found: {args.workflow}", file=sys.stderr)
        sys.exit(1)

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    width, height = ASPECT_RATIOS[args.aspect]

    print(f"Generating NSFW image...")
    print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
    print(f"  Face ref: {args.face_ref}")
    print(f"  Workflow: {args.workflow}")
    print(f"  Aspect: {args.aspect} ({width}x{height})")
    print(f"  LoRA strength: {args.lora_strength}")
    print(f"  Seed: {seed}")

    # Upload face reference
    print(f"  Uploading face reference...")
    face_filename = upload_image(args.face_ref)

    # Build and submit workflow
    workflow = build_workflow(
        workflow_template=args.workflow,
        prompt=args.prompt,
        face_ref_filename=face_filename,
        width=width,
        height=height,
        lora_strength=args.lora_strength,
        seed=seed,
    )

    try:
        result = run_workflow(workflow, args.output, timeout=120)
        size_kb = result.stat().st_size // 1024
        print(f"  Saved: {result} ({size_kb} KB)")
    except (ComfyUIError, TimeoutError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
