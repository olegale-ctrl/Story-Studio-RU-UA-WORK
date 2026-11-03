"""Windows-friendly Story Studio project/bundle command line (stdlib only)."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from core.project_schema import Project
from core.export_bundle import write_bundle, build_bundle_manifest
from core.bundle_integrity import verify_bundle
from core.timeline_audit import audit_timeline
from core.mp4_render import render_mp4


def run(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m core.cli", description="Story Studio RU/UA project utilities")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Validate project JSON (v1-v3) and show timeline warnings")
    check.add_argument("project", type=Path)
    preview = commands.add_parser("preview", help="Print bundle manifest without writing files")
    preview.add_argument("project", type=Path)
    build = commands.add_parser("bundle", help="Copy project media into a new portable bundle")
    build.add_argument("project", type=Path)
    build.add_argument("--media-root", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify", help="Verify SHA-256 integrity of a bundle")
    verify.add_argument("bundle", type=Path)
    render = commands.add_parser("render-mp4", help="Experimental still-image MP4 via local FFmpeg")
    render.add_argument("project", type=Path)
    render.add_argument("--media-root", type=Path, required=True)
    render.add_argument("--output", type=Path, required=True)
    render.add_argument('--burn-subtitles', action='store_true', help='Burn one SRT track into the video (requires FFmpeg libass)')
    render.add_argument('--width', type=int, help='Output width (even pixels, e.g. 1920)')
    render.add_argument('--height', type=int, help='Output height (even pixels, e.g. 1080)')
    render.add_argument('--export-srt', action='store_true', help='Also save SRT next to burned MP4')
    render.add_argument('--crf', type=int, default=23, help='H.264 quality: 0 best, 51 worst; default 23')
    args = parser.parse_args(argv)
    try:
        if args.command == "verify":
            errors = verify_bundle(args.bundle)
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            if errors:
                return 2
            print("OK: bundle integrity verified")
            return 0
        project = Project.from_json(args.project.read_text(encoding="utf-8-sig"))
        if args.command == "render-mp4":
            result = render_mp4(project, args.media_root, args.output, burn_subtitles=args.burn_subtitles, crf=args.crf, width=args.width, height=args.height, export_srt_files=(True if args.export_srt else None))
            print("OK: " + json.dumps(result, ensure_ascii=False))
            return 0
        if args.command == "check":
            warnings = audit_timeline(project)
            print(f"OK: schema v{project.schema_version}, locale={project.content_locale}, clips={len(project.clips)}")
            for warning in warnings:
                print("WARNING: " + json.dumps(warning, ensure_ascii=False))
            return 0
        if args.command == "preview":
            print(json.dumps(build_bundle_manifest(project), ensure_ascii=False, indent=2))
            return 0
        if args.command == "bundle":
            write_bundle(project, args.media_root, args.output, dry_run=False)
            print(f"OK: bundle created at {args.output}")
            return 0
        parser.error("unsupported command")
    except (ValueError, OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(run())
