"""Sprint 26: make a real RU/UA narrated MP4 from a scene plan and local audio.

No remote API calls. Existing WAV files or an explicitly trusted local Silero
model are supported. Uses the existing v3 timeline and FFmpeg renderer.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.project_schema import Project
from core.mp4_render import render_mp4

FRAME_MS = 40  # 25 fps


def read_plan(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or data.get("locale") not in ("ru", "uk"):
        raise ValueError("Plan requires locale: ru or uk")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 20:
        raise ValueError("Plan requires 1..20 scenes")
    for scene in scenes:
        if not isinstance(scene, dict) or not isinstance(scene.get("text"), str) or not scene["text"].strip():
            raise ValueError("Every scene requires nonempty text")
        if len(scene["text"]) > 2000:
            raise ValueError("Scene text exceeds 2000 characters")
        if "image" in scene and (not isinstance(scene["image"], str) or not scene["image"]):
            raise ValueError("image must be a filename")
    return data


def wav_ms(path: Path) -> int:
    with wave.open(str(path), "rb") as f:
        if f.getnframes() == 0 or f.getframerate() <= 0:
            raise ValueError("Empty WAV: " + str(path))
        return (f.getnframes() * 1000 + f.getframerate() - 1) // f.getframerate()


def make_background(path: Path, index: int, width: int = 640, height: int = 360) -> None:
    palette = [(32, 69, 96), (43, 90, 79), (88, 55, 91), (95, 75, 45)]
    rgb = palette[index % len(palette)]
    with path.open("wb") as f:
        f.write(f"P6\n{width} {height}\n255\n".encode("ascii"))
        for y in range(height):
            shade = y * 45 // height
            f.write(bytes(max(0, c - shade) for c in rgb) * width)


def safe_image(source_dir: Path, filename: str) -> Path:
    name = Path(filename)
    if name.is_absolute() or name.name != filename or filename in (".", ".."):
        raise ValueError("Image must be a simple filename, not a path")
    if name.suffix.lower() not in (".png", ".jpg", ".jpeg", ".ppm"):
        raise ValueError("Image must be PNG, JPG or PPM")
    root = source_dir.resolve(strict=True)
    path = (root / filename).resolve(strict=True)
    if path.parent != root or not path.is_file():
        raise ValueError("Image must be a regular file inside --images-dir")
    return path


def build(plan_path: Path, output_dir: Path, *, audio_dir: Path | None = None,
          images_dir: Path | None = None, silero_model: Path | None = None,
          voice: str | None = None, render: bool = True,
          width: int = 1280, height: int = 720) -> tuple[Path, Path | None]:
    if (audio_dir is None) == (silero_model is None):
        raise ValueError("Choose exactly one: --audio-dir OR --silero-model")
    if width % 2 or height % 2 or not 2 <= width <= 8192 or not 2 <= height <= 8192:
        raise ValueError("Width and height must be even, between 2 and 8192")
    plan = read_plan(plan_path)
    locale = plan["locale"]
    if silero_model is not None and not voice:
        raise ValueError("--voice required with --silero-model")
    if output_dir.exists():
        raise FileExistsError("Output directory already exists: " + str(output_dir))
    if audio_dir is not None and not audio_dir.is_dir():
        raise FileNotFoundError("Audio directory missing: " + str(audio_dir))
    if images_dir is not None and not images_dir.is_dir():
        raise FileNotFoundError("Images directory missing: " + str(images_dir))

    # Validate user-provided images before writing anything.
    images = []
    for scene in plan["scenes"]:
        filename = scene.get("image")
        if filename and images_dir is None:
            raise ValueError("--images-dir required when scene specifies image")
        images.append(safe_image(images_dir, filename) if filename else None)

    provider = None
    if silero_model is not None:
        from integrations.silero_local import SileroLocalProvider
        provider = SileroLocalProvider(silero_model, trusted=True)

    output_dir.mkdir(parents=True)
    media_dir = output_dir / "media"
    media_dir.mkdir()
    project = dict(title=plan.get("title") or "Story Studio RU/UA — first video",
                   content_locale=locale, scenes=[], fps=25, width=width, height=height,
                   schema_version=3, tracks=[
                       dict(id="v", kind="video", label="Images"),
                       dict(id="a", kind="audio", label="Voice"),
                       dict(id="s", kind="subtitle", label="Subtitles")],
                   subtitles=[], media=[], clips=[])
    cursor = 0
    for index, (scene, image_source) in enumerate(zip(plan["scenes"], images), 1):
        wav = media_dir / f"voice{index}.wav"
        if audio_dir is not None:
            source = audio_dir / f"voice{index}.wav"
            if not source.is_file():
                raise FileNotFoundError("Missing audio: " + str(source))
            shutil.copyfile(source, wav)
        else:
            provider.synthesize(text=scene["text"], locale=locale, voice=voice, output=wav)
        audio_ms = wav_ms(wav)
        scene_ms = ((audio_ms + 400 + FRAME_MS - 1) // FRAME_MS) * FRAME_MS
        image_name = f"frame{index}" + (image_source.suffix.lower() if image_source else ".ppm")
        image_target = media_dir / image_name
        if image_source:
            shutil.copyfile(image_source, image_target)
        else:
            make_background(image_target, index - 1)
        project["media"].extend([
            dict(id=f"i{index}", kind="image", path=image_name),
            dict(id=f"a{index}", kind="audio", path=wav.name)])
        project["clips"].extend([
            dict(id=f"v{index}", track_id="v", media_id=f"i{index}",
                 start_ms=cursor, duration_ms=scene_ms, source_in_ms=0),
            dict(id=f"c{index}", track_id="a", media_id=f"a{index}",
                 start_ms=cursor, duration_ms=audio_ms, source_in_ms=0)])
        project["subtitles"].append(
            dict(id=f"s{index}", track_id="s", start_ms=cursor,
                 duration_ms=audio_ms, text=scene["text"], locale=locale))
        cursor += scene_ms

    validated = Project.from_dict(project)
    project_file = output_dir / "project.json"
    project_file.write_text(validated.to_json() + "\n", encoding="utf-8")
    video = None
    if render:
        video = output_dir / "first-video.mp4"
        result = render_mp4(validated, media_dir, video, burn_subtitles=True,
                            width=width, height=height, crf=22)
        print("RENDER:", json.dumps(result, ensure_ascii=False))
    print("PROJECT:", project_file)
    if video:
        print("VIDEO:", video)
    return project_file, video


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RU/UA narrated video from local WAV or Silero")
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--audio-dir", type=Path)
    source.add_argument("--silero-model", type=Path)
    p.add_argument("--voice", help="Silero speaker, e.g. ukr_igor")
    p.add_argument("--images-dir", type=Path)
    p.add_argument("--no-render", action="store_true")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    args = p.parse_args(argv)
    try:
        build(args.plan, args.output_dir, audio_dir=args.audio_dir,
              images_dir=args.images_dir, silero_model=args.silero_model,
              voice=args.voice, render=not args.no_render,
              width=args.width, height=args.height)
    except (ValueError, OSError, RuntimeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
