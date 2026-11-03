"""Validated portable editing handoff bundle (stdlib only).

Dry-run creates a manifest in memory. Materialization is opt-in and copies only
referenced files under the chosen media root; it does not produce native editor files.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
from core.project_schema import Project
from core.media_paths import validate_media_path
from core.subtitles import export_srt


def build_bundle_manifest(project: Project) -> dict:
    project.validate()
    paths = {}
    for asset in project.media:
        paths[asset.path] = asset.kind
    for scene in project.scenes:
        for kind, value in (("image", scene.image_path), ("audio", scene.audio_path)):
            if value is not None:
                path = validate_media_path(value)
                if path in paths and paths[path] != kind:
                    raise ValueError("conflicting media kind for path")
                paths[path] = kind
    return {
        "bundle_version": 1, "project_schema_version": project.schema_version,
        "title": project.title, "locale": project.content_locale,
        "timeline_duration_ms": max([0] + [s.start_ms+s.duration_ms for s in project.scenes]
              + [c.start_ms+c.duration_ms for c in project.clips]
              + [s.start_ms+s.duration_ms for s in project.subtitles]),
        "media": [{"path": p, "kind": paths[p]} for p in sorted(paths)],
        "subtitle_tracks": [{"track_id": t.id, "path": f"subtitles/{i:03d}.srt"}
             for i,t in enumerate((t for t in project.tracks if t.kind == "subtitle"), 1)],
        "clips": [dict(id=c.id, track_id=c.track_id, media_id=c.media_id,
                       start_ms=c.start_ms, duration_ms=c.duration_ms,
                       source_in_ms=c.source_in_ms) for c in project.clips],
    }


def write_bundle(project: Project, media_root: str | Path, destination: str | Path, *, dry_run: bool = True) -> dict:
    manifest = build_bundle_manifest(project)
    if dry_run:
        return manifest
    source = Path(media_root).resolve(strict=True)
    if not source.is_dir():
        raise ValueError("media_root must be a directory")
    dest = Path(destination).resolve()
    if dest.exists():
        raise FileExistsError("destination must not exist")
    if dest == source or source in dest.parents or dest in source.parents:
        raise ValueError("media_root and destination must be disjoint")
    # Preflight ALL inputs before writing any output.
    sources = []
    for item in manifest["media"]:
        rel = validate_media_path(item["path"])
        path = (source / rel).resolve(strict=True)
        if source not in path.parents or not path.is_file():
            raise ValueError("media path escapes root or is not a file")
        sources.append((rel, path))
    try:
        dest.mkdir(parents=True, exist_ok=False)
        for rel, path in sources:
            target = dest / "media" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        for item in manifest["subtitle_tracks"]:
            target = dest / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(export_srt(project, track_id=item["track_id"]), encoding="utf-8")
        (dest / "project.json").write_text(project.to_json()+"\n", encoding="utf-8")
        (dest / "bundle-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        from core.bundle_integrity import make_integrity_manifest
        integrity = make_integrity_manifest(dest)
        (dest / "integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(dest)
        raise
    return manifest
