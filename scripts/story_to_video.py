"""End-to-end Topic-to-Video pipeline for Story Studio RU/UA.

From a single topic sentence to a fully produced narrated video:
1. Generates structured dramatic story plan & image prompts (LLM or offline engine).
2. Synthesizes voice narration via Silero TTS.
3. Generates dynamic rhythmic subtitles with syllable timing.
4. Adds background music (BGM) with automatic sidechain audio ducking.
5. Applies smooth Ken Burns camera motion.
6. Encodes horizontal (16:9) or vertical (9:16) MP4 video via FFmpeg.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.story_generator import generate_story
from scripts.first_video import build


def run_story_to_video(
    topic: str,
    output_dir: Path,
    *,
    locale: str = "uk",
    style: str = "cinematic",
    silero_model: Path | None = None,
    voice: str | None = None,
    audio_dir: Path | None = None,
    images_dir: Path | None = None,
    vertical: bool = False,
    motion: bool = True,
    bgm_path: Path | None = None,
    bgm_volume: float = 0.22,
    ducking: bool = True,
    sub_words: int = 3,
    llm_url: str | None = None,
    llm_model: str = "llama3",
    llm_api_key: str | None = None,
    width: int | None = None,
    height: int | None = None,
) -> tuple[Path, Path | None]:
    """Execute the end-to-end topic-to-video workflow."""
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")

    output_dir.mkdir(parents=True)

    print(f"[*] Generating screenplay for topic: '{topic}' ({locale.upper()})...")
    story_plan = generate_story(
        topic=topic,
        locale=locale,
        style=style,
        api_url=llm_url,
        model=llm_model,
        api_key=llm_api_key,
    )

    # Save comprehensive story plan with visual prompts
    story_plan_file = output_dir / "story_plan.json"
    story_plan_file.write_text(
        json.dumps(story_plan.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[+] Screenplay created: {len(story_plan.scenes)} scenes")
    print(f"    Saved story plan with visual prompts: {story_plan_file}")

    # Generate standard first_video.py plan
    first_video_plan = output_dir / "plan.json"
    first_video_plan.write_text(
        json.dumps(story_plan.to_first_video_plan(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Determine resolution
    if vertical:
        w = width if width is not None else 720
        h = height if height is not None else 1280
    else:
        w = width if width is not None else 1280
        h = height if height is not None else 720

    print(f"[*] Rendering video ({w}x{h}, motion={motion}, ducking={ducking})...")
    render_dir = output_dir / "render"
    proj_file, video_file = build(
        first_video_plan,
        render_dir,
        audio_dir=audio_dir,
        images_dir=images_dir,
        silero_model=silero_model,
        voice=voice,
        render=True,
        width=w,
        height=h,
        motion=motion,
        bgm_path=bgm_path,
        bgm_volume=bgm_volume,
        ducking=ducking,
        sub_chunk_words=sub_words,
    )

    # Move final video to root of output_dir for clean access
    final_video = None
    if video_file and video_file.is_file():
        final_video = output_dir / "final_story_video.mp4"
        video_file.rename(final_video)
        print(f"[SUCCESS] Video ready: {final_video}")

    return story_plan_file, final_video


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="End-to-end Topic to Video for Story Studio RU/UA")
    p.add_argument("--topic", type=str, required=True, help="Topic or title for the video story")
    p.add_argument("--output-dir", type=Path, required=True, help="Destination directory for outputs")
    p.add_argument("--locale", choices=["ru", "uk"], default="uk", help="Language: uk (default) or ru")
    p.add_argument("--style", choices=["cinematic", "historical", "dark_mystery", "anime_epic"], default="cinematic")

    # Audio & Voice
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--silero-model", type=Path, help="Path to local Silero .pt model")
    source.add_argument("--audio-dir", type=Path, help="Directory containing pre-recorded voice1.wav, voice2.wav...")
    p.add_argument("--voice", help="Silero speaker (e.g. ukr_igor, ru_dmitriy)")

    # Visuals & Format
    p.add_argument("--images-dir", type=Path, help="Optional folder with custom frame images")
    p.add_argument("--vertical", action="store_true", help="Render in 9:16 vertical format for Shorts/Reels/TikTok")
    p.add_argument("--no-motion", action="store_true", help="Disable Ken Burns camera motion")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)

    # Music & Subtitles
    p.add_argument("--bgm", type=Path, default=None, help="Background music audio file")
    p.add_argument("--bgm-volume", type=float, default=0.20, help="BGM volume factor (default 0.20)")
    p.add_argument("--no-ducking", action="store_true", help="Disable automatic audio ducking")
    p.add_argument("--sub-words", type=int, default=3, help="Max words per subtitle chunk")

    # Optional LLM endpoint
    p.add_argument("--llm-url", type=str, default=None, help="OpenAI-compatible LLM endpoint (e.g. http://localhost:11434/v1/chat/completions)")
    p.add_argument("--llm-model", type=str, default="llama3", help="LLM model name")
    p.add_argument("--llm-key", type=str, default=None, help="API key for cloud LLM")

    args = p.parse_args(argv)

    try:
        run_story_to_video(
            topic=args.topic,
            output_dir=args.output_dir,
            locale=args.locale,
            style=args.style,
            silero_model=args.silero_model,
            voice=args.voice,
            audio_dir=args.audio_dir,
            images_dir=args.images_dir,
            vertical=args.vertical,
            motion=not args.no_motion,
            bgm_path=args.bgm,
            bgm_volume=args.bgm_volume,
            ducking=not args.no_ducking,
            sub_words=args.sub_words,
            llm_url=args.llm_url,
            llm_model=args.llm_model,
            llm_api_key=args.llm_key,
            width=args.width,
            height=args.height,
        )
    except (ValueError, OSError, RuntimeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
