# comfyui_client.py
"""HTTP client for submitting ComfyUI workflows to Modal endpoint."""

import json
import os
import time
import uuid
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class ComfyUIError(Exception):
    """Raised when ComfyUI returns an error for a workflow."""
    pass


def get_base_url() -> str:
    url = os.environ.get("MODAL_COMFYUI_URL", "")
    if not url:
        raise RuntimeError("MODAL_COMFYUI_URL not set. Deploy the Modal app first.")
    return url.rstrip("/")


def upload_image(image_path: Path, subfolder: str = "") -> str:
    """Upload an image to ComfyUI's input directory. Returns the filename."""
    base = get_base_url()
    name = f"{uuid.uuid4().hex[:8]}_{image_path.name}"

    image_data = image_path.read_bytes()

    # Build multipart/form-data body manually
    boundary = uuid.uuid4().hex
    body_parts = []

    # File field
    body_parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    )
    body = "".join(body_parts).encode() + image_data + b"\r\n"

    # overwrite field
    body += (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="overwrite"\r\n\r\n'
        f"true\r\n"
    ).encode()

    if subfolder:
        body += (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="subfolder"\r\n\r\n'
            f"{subfolder}\r\n"
        ).encode()

    body += f"--{boundary}--\r\n".encode()

    req = Request(
        f"{base}/upload/image",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
    )
    with urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    return result["name"]


def submit_workflow(workflow: dict) -> str:
    """Submit a workflow JSON to ComfyUI. Returns the prompt ID."""
    base = get_base_url()
    client_id = uuid.uuid4().hex
    payload = json.dumps({"prompt": workflow, "client_id": client_id}).encode()

    req = Request(
        f"{base}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    if "error" in data:
        raise ComfyUIError(f"Workflow rejected: {data['error']}")
    return data["prompt_id"]


def poll_result(prompt_id: str, timeout: int = 300, interval: int = 3) -> dict:
    """Poll /history until the workflow completes. Returns output info."""
    base = get_base_url()
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = Request(f"{base}/history/{prompt_id}")
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if prompt_id in data:
            result = data[prompt_id]
            if result.get("status", {}).get("status_str") == "error":
                msgs = result.get("status", {}).get("messages", [])
                raise ComfyUIError(f"Workflow failed: {msgs}")
            if result.get("outputs"):
                return result["outputs"]
        time.sleep(interval)
    raise TimeoutError(f"Workflow {prompt_id} timed out after {timeout}s")


def download_output(prompt_id: str, outputs: dict, output_path: Path) -> Path:
    """Download the first output file from a completed workflow."""
    base = get_base_url()
    # Find the first image or video output
    for node_id, node_output in outputs.items():
        for key in ("images", "gifs"):
            if key in node_output:
                item = node_output[key][0]
                filename = item["filename"]
                subfolder = item.get("subfolder", "")
                file_type = item.get("type", "output")
                url = f"{base}/view?filename={filename}&subfolder={subfolder}&type={file_type}"
                req = Request(url)
                with urlopen(req, timeout=120) as resp:
                    data = resp.read()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(data)
                return output_path
    raise ComfyUIError(f"No output files found in workflow {prompt_id}")


def run_workflow(workflow: dict, output_path: Path, timeout: int = 300) -> Path:
    """Submit workflow, poll for completion, download result. Returns output path."""
    prompt_id = submit_workflow(workflow)
    print(f"  Submitted workflow (prompt_id: {prompt_id[:12]}...)")
    outputs = poll_result(prompt_id, timeout=timeout)
    return download_output(prompt_id, outputs, output_path)
