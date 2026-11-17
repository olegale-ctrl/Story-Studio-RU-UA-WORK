"""Image generation client for Story Studio RU/UA.

Sends image prompts to a locally running ComfyUI instance and saves the results.
Works 100% offline — no cloud, no paid services.

Supports:
- ComfyUI API (http://localhost:8188) — primary backend
- Automatic1111 / Forge WebUI API (http://localhost:7860) — secondary backend
- Fallback: Pillow procedural art (always available, used when no generator is running)

Usage:
    from core.image_gen import generate_images_for_plan, BackendType

    images = generate_images_for_plan(
        story_plan,
        output_dir=Path("output/my_story/images"),
        backend="comfyui",          # or "a1111" or "pillow"
        comfyui_url="http://localhost:8188",
        checkpoint="Realistic_Vision_V5.1.safetensors",
        width=1280,
        height=720,
        steps=20,
        cfg=7.0,
    )
    # Returns list of Paths, one per scene
"""
from __future__ import annotations

import base64
import io
import json
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import List, Literal, Optional

BackendType = Literal["comfyui", "a1111", "pillow"]

# ---------------------------------------------------------------------------
# Probe: check which backends are available
# ---------------------------------------------------------------------------

def probe_backend(
    comfyui_url: str = "http://localhost:8188",
    a1111_url: str = "http://localhost:7860",
    timeout: int = 3,
) -> BackendType:
    """Return the first available backend in priority order."""
    for url, name in [(comfyui_url, "comfyui"), (a1111_url, "a1111")]:
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout):
                return name  # type: ignore[return-value]
        except Exception:
            pass
    return "pillow"


# ---------------------------------------------------------------------------
# ComfyUI backend
# ---------------------------------------------------------------------------

def _comfyui_txt2img(
    prompt: str,
    negative_prompt: str,
    *,
    url: str = "http://localhost:8188",
    checkpoint: str = "Realistic_Vision_V5.1.safetensors",
    width: int = 1280,
    height: int = 720,
    steps: int = 20,
    cfg: float = 7.0,
    sampler: str = "euler",
    scheduler: str = "karras",
    seed: int = -1,
    timeout: int = 300,
) -> bytes:
    """Generate one image via ComfyUI /prompt API and return raw PNG bytes."""
    import random
    if seed < 0:
        seed = random.randint(0, 2**32 - 1)

    # Minimal SD 1.5 / SDXL workflow via basic KSampler nodes
    client_id = str(uuid.uuid4())
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": checkpoint},
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["1", 1],
                "text": prompt,
            },
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["1", 1],
                "text": negative_prompt,
            },
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": height,
                "width": width,
            },
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": cfg,
                "denoise": 1.0,
                "latent_image": ["4", 0],
                "model": ["1", 0],
                "negative": ["3", 0],
                "positive": ["2", 0],
                "sampler_name": sampler,
                "scheduler": scheduler,
                "seed": seed,
                "steps": steps,
            },
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2],
            },
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "story_studio",
                "images": ["6", 0],
            },
        },
    }

    payload = json.dumps({"prompt": workflow, "client_id": client_id}).encode()
    req = urllib.request.Request(
        f"{url}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    prompt_id = result["prompt_id"]

    # Poll /history until job is complete
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        time.sleep(2)
        try:
            req2 = urllib.request.Request(f"{url}/history/{prompt_id}")
            with urllib.request.urlopen(req2, timeout=10) as r:
                hist = json.loads(r.read())
        except Exception:
            continue
        if prompt_id not in hist:
            continue
        job = hist[prompt_id]
        if "outputs" not in job:
            continue
        # Find first SaveImage output
        for node_id, node_out in job["outputs"].items():
            if "images" in node_out:
                img_info = node_out["images"][0]
                img_req = urllib.request.Request(
                    f"{url}/view?filename={img_info['filename']}"
                    f"&subfolder={img_info.get('subfolder', '')}"
                    f"&type={img_info.get('type', 'output')}"
                )
                with urllib.request.urlopen(img_req, timeout=30) as ir:
                    return ir.read()
        break

    raise TimeoutError(f"ComfyUI job {prompt_id} did not complete within {timeout}s")


# ---------------------------------------------------------------------------
# AUTOMATIC1111 / Forge WebUI backend
# ---------------------------------------------------------------------------

def _a1111_txt2img(
    prompt: str,
    negative_prompt: str,
    *,
    url: str = "http://localhost:7860",
    checkpoint: str | None = None,
    width: int = 1280,
    height: int = 720,
    steps: int = 20,
    cfg: float = 7.0,
    sampler: str = "Euler a",
    seed: int = -1,
    timeout: int = 300,
) -> bytes:
    """Generate one image via A1111 txt2img API and return raw PNG bytes."""
    payload: dict = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler_name": sampler,
        "seed": seed,
        "batch_size": 1,
        "n_iter": 1,
        "send_images": True,
        "save_images": False,
    }
    if checkpoint:
        payload["override_settings"] = {"sd_model_checkpoint": checkpoint}
        payload["override_settings_restore_afterwards"] = False

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{url}/sdapi/v1/txt2img",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read())

    img_b64 = result["images"][0]
    return base64.b64decode(img_b64)


# ---------------------------------------------------------------------------
# Pillow fallback procedural art
# ---------------------------------------------------------------------------

def _pillow_placeholder(
    scene_index: int,
    prompt: str,
    width: int,
    height: int,
) -> bytes:
    """Generate a simple gradient placeholder using Pillow. Zero dependencies beyond PIL."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise RuntimeError("Pillow is required for fallback image generation: pip install Pillow")

    # Colour palettes per scene index (cycling)
    palettes = [
        ((10, 15, 60), (80, 120, 200)),   # deep blue night
        ((60, 20, 10), (200, 90, 30)),    # warm amber / fire
        ((10, 40, 10), (40, 120, 60)),    # forest green
        ((40, 10, 50), (100, 40, 140)),   # purple dusk
        ((10, 50, 60), (30, 130, 160)),   # teal ocean
    ]
    top_col, bot_col = palettes[scene_index % len(palettes)]

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / height
        r = int(top_col[0] + (bot_col[0] - top_col[0]) * t)
        g = int(top_col[1] + (bot_col[1] - top_col[1]) * t)
        b = int(top_col[2] + (bot_col[2] - top_col[2]) * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Print prompt excerpt as text overlay
    excerpt = prompt[:80] + ("…" if len(prompt) > 80 else "")
    try:
        font = ImageFont.truetype("arial.ttf", max(14, width // 60))
    except Exception:
        font = ImageFont.load_default()

    # Text shadow
    tx, ty = width // 20, height // 2
    draw.text((tx + 2, ty + 2), excerpt, font=font, fill=(0, 0, 0, 180))
    draw.text((tx, ty), excerpt, font=font, fill=(240, 240, 240))
    draw.text((tx, ty + 40), f"[Scene {scene_index + 1} — Pillow placeholder]", font=font, fill=(180, 180, 100))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_image(
    prompt: str,
    negative_prompt: str = "",
    *,
    scene_index: int = 0,
    backend: BackendType = "comfyui",
    comfyui_url: str = "http://localhost:8188",
    a1111_url: str = "http://localhost:7860",
    checkpoint: str = "Realistic_Vision_V5.1.safetensors",
    width: int = 1280,
    height: int = 720,
    steps: int = 20,
    cfg: float = 7.0,
    seed: int = -1,
    timeout: int = 300,
) -> bytes:
    """Generate one image and return raw PNG bytes.

    Parameters
    ----------
    prompt:         Positive prompt (English, descriptive).
    negative_prompt: Negative prompt. If empty, a sensible default is used.
    scene_index:    Zero-based scene number (used by Pillow fallback for colour cycling).
    backend:        'comfyui' | 'a1111' | 'pillow'
    comfyui_url:    Base URL of running ComfyUI instance.
    a1111_url:      Base URL of running A1111 instance.
    checkpoint:     Model filename (must already be in ComfyUI/A1111 models/checkpoints/).
    width/height:   Image resolution.
    steps:          Sampling steps (20 is a good CPU balance; use 15 for speed).
    cfg:            Classifier-free guidance scale.
    seed:           Fixed seed for reproducibility; -1 = random.
    timeout:        Max seconds to wait for ComfyUI/A1111 to finish.
    """
    if not negative_prompt.strip():
        negative_prompt = (
            "cartoon, illustration, 3d render, deformed, blurry, low quality, "
            "oversaturated, text, watermark, signature, logo"
        )

    if backend == "comfyui":
        return _comfyui_txt2img(
            prompt, negative_prompt,
            url=comfyui_url, checkpoint=checkpoint,
            width=width, height=height, steps=steps, cfg=cfg, seed=seed, timeout=timeout,
        )
    elif backend == "a1111":
        return _a1111_txt2img(
            prompt, negative_prompt,
            url=a1111_url, checkpoint=checkpoint,
            width=width, height=height, steps=steps, cfg=cfg, seed=seed, timeout=timeout,
        )
    else:  # pillow
        return _pillow_placeholder(scene_index, prompt, width, height)


def generate_images_for_plan(
    story_plan,
    output_dir: Path,
    *,
    backend: BackendType | None = None,
    comfyui_url: str = "http://localhost:8188",
    a1111_url: str = "http://localhost:7860",
    checkpoint: str = "Realistic_Vision_V5.1.safetensors",
    width: int = 1280,
    height: int = 720,
    steps: int = 20,
    cfg: float = 7.0,
    seed: int = -1,
    timeout: int = 300,
) -> List[Path]:
    """Generate images for every scene in a StoryPlan and save as PNG files.

    Parameters
    ----------
    story_plan:  StoryPlan object (from core.story_generator).
    output_dir:  Directory to save scene images (created automatically).
    backend:     Force a specific backend; None = auto-detect.

    Returns
    -------
    List of Path objects (one per scene, in order).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Auto-detect backend if not forced
    if backend is None:
        backend = probe_backend(comfyui_url=comfyui_url, a1111_url=a1111_url)
        print(f"[image_gen] Auto-detected backend: {backend}")
    else:
        print(f"[image_gen] Using backend: {backend}")

    if backend == "comfyui":
        print(f"[image_gen] ComfyUI endpoint: {comfyui_url}")
        print(f"[image_gen] Checkpoint: {checkpoint}")
    elif backend == "a1111":
        print(f"[image_gen] A1111 endpoint: {a1111_url}")

    paths: List[Path] = []
    total = len(story_plan.scenes)

    for i, scene in enumerate(story_plan.scenes):
        out_path = output_dir / f"scene_{i + 1:02d}.png"

        # Use image_prompt if available; fall back to visual_description
        raw_prompt = getattr(scene, "image_prompt", None) or getattr(scene, "visual_description", scene.text)
        negative = getattr(scene, "negative_prompt", "")

        print(f"[image_gen] [{i+1}/{total}] Generating image for scene {i+1}...")
        print(f"            Prompt: {raw_prompt[:100]}{'…' if len(raw_prompt) > 100 else ''}")

        t0 = time.monotonic()
        try:
            png_bytes = generate_image(
                raw_prompt,
                negative,
                scene_index=i,
                backend=backend,
                comfyui_url=comfyui_url,
                a1111_url=a1111_url,
                checkpoint=checkpoint,
                width=width,
                height=height,
                steps=steps,
                cfg=cfg,
                seed=seed if seed >= 0 else -1,
                timeout=timeout,
            )
            out_path.write_bytes(png_bytes)
            elapsed = time.monotonic() - t0
            print(f"            Saved: {out_path}  ({elapsed:.1f}s)")
        except Exception as exc:
            print(f"[image_gen] WARNING: Failed to generate scene {i+1}: {exc}")
            print(f"[image_gen]          Falling back to Pillow placeholder.")
            png_bytes = _pillow_placeholder(i, raw_prompt, width, height)
            out_path.write_bytes(png_bytes)

        paths.append(out_path)

    print(f"[image_gen] Done. {len(paths)} images saved to: {output_dir}")
    return paths
