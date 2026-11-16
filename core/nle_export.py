"""NLE (Non-Linear Editor) project exporters for Story Studio RU/UA.

Exports timeline projects to free and open exchange formats:
1. FCPXML 1.8 (Final Cut Pro XML) — for DaVinci Resolve (Free), Kdenlive, and Premiere.
2. CapCut Desktop Draft (draft_content.json) — for CapCut / Jianying Desktop.
3. CMX 3600 EDL — universal edit decision list standard.
"""
from __future__ import annotations

import json
import time
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from .project_schema import Project


def _ms_to_timecode_edl(ms: int, fps: float = 25.0) -> str:
    """Format milliseconds into SMPTE timecode HH:MM:SS:FF for EDL."""
    total_frames = int(round(ms * fps / 1000.0))
    fps_int = int(round(fps))
    frames = total_frames % fps_int
    total_seconds = total_frames // fps_int
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    hours = total_minutes // 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def _file_uri(path: Path) -> str:
    """Convert a local path into a file:// URI compatible with FCPXML."""
    resolved = path.resolve()
    as_posix = resolved.as_posix()
    if not as_posix.startswith("/"):
        as_posix = "/" + as_posix
    return f"file://{quote(as_posix, safe='/:')}"


# =========================================================================
# 1. FCPXML Exporter (DaVinci Resolve / Kdenlive / Premiere)
# =========================================================================

def export_fcpxml(
    project: Project,
    media_root: Path,
    output_file: Path,
    *,
    bgm_path: Optional[Path] = None,
    bgm_volume: float = 0.22,
) -> Path:
    """Export project timeline as FCPXML 1.8 document."""
    media_root = media_root.resolve()
    tracks = {t.id: t.kind for t in project.tracks}
    media = {m.id: m for m in project.media}
    video_clips = sorted(
        [c for c in project.clips if tracks.get(c.track_id) == "video"],
        key=lambda c: (c.start_ms, c.id),
    )
    audio_clips = sorted(
        [c for c in project.clips if tracks.get(c.track_id) == "audio"],
        key=lambda c: (c.start_ms, c.id),
    )

    fps = float(project.fps if project.fps > 0 else 25.0)
    total_ms = sum(c.duration_ms for c in video_clips)
    total_sec = total_ms / 1000.0

    fcpxml = ET.Element("fcpxml", version="1.8")
    resources = ET.SubElement(fcpxml, "resources")

    # Format resource
    ET.SubElement(
        resources, "format",
        id="r1",
        name=f"FFVideoFormat{project.width}x{project.height}",
        frameDuration=f"1/{int(fps)}s",
        width=str(project.width),
        height=str(project.height),
    )

    # Register media assets
    res_map: Dict[str, str] = {}
    res_counter = 2

    for asset in project.media:
        asset_file = (media_root / asset.path).resolve()
        res_id = f"r{res_counter}"
        res_counter += 1
        res_map[asset.id] = res_id

        if asset.kind == "image":
            ET.SubElement(
                resources, "asset",
                id=res_id,
                name=asset_file.name,
                src=_file_uri(asset_file),
                format="r1",
                hasVideo="1",
            )
        elif asset.kind == "audio":
            ET.SubElement(
                resources, "asset",
                id=res_id,
                name=asset_file.name,
                src=_file_uri(asset_file),
                hasAudio="1",
            )

    bgm_res_id = None
    if bgm_path and Path(bgm_path).is_file():
        bgm_file = Path(bgm_path).resolve()
        bgm_res_id = f"r{res_counter}"
        res_counter += 1
        ET.SubElement(
            resources, "asset",
            id=bgm_res_id,
            name=bgm_file.name,
            src=_file_uri(bgm_file),
            hasAudio="1",
        )

    # Library / Event / Project / Sequence
    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name="Story Studio")
    proj_elem = ET.SubElement(event, "project", name=project.title or "Story")
    sequence = ET.SubElement(
        proj_elem, "sequence",
        format="r1",
        duration=f"{total_sec:.3f}s",
        tcStart="0s",
    )
    spine = ET.SubElement(sequence, "spine")

    # Sequence video clips
    for idx, vclip in enumerate(video_clips):
        res_id = res_map.get(vclip.media_id, "r1")
        v_dur_s = vclip.duration_ms / 1000.0
        v_offset_s = vclip.start_ms / 1000.0

        clip_elem = ET.SubElement(
            spine, "asset-clip",
            name=f"Scene_{idx+1}",
            ref=res_id,
            offset=f"{v_offset_s:.3f}s",
            duration=f"{v_dur_s:.3f}s",
            start="0s",
        )

        # Attach voice audio for this scene if present
        matching_audio = [
            a for a in audio_clips
            if a.start_ms >= vclip.start_ms and a.start_ms < vclip.start_ms + vclip.duration_ms
        ]
        for aclip in matching_audio:
            a_res = res_map.get(aclip.media_id)
            if a_res:
                a_dur_s = aclip.duration_ms / 1000.0
                a_offset_s = (aclip.start_ms - vclip.start_ms) / 1000.0
                ET.SubElement(
                    clip_elem, "asset-clip",
                    name=f"Voice_{idx+1}",
                    ref=a_res,
                    lane="-1",
                    offset=f"{a_offset_s:.3f}s",
                    duration=f"{a_dur_s:.3f}s",
                    start="0s",
                )

    # Background music clip on secondary audio lane
    if bgm_res_id:
        ET.SubElement(
            spine, "asset-clip",
            name="Background Music",
            ref=bgm_res_id,
            lane="-2",
            offset="0s",
            duration=f"{total_sec:.3f}s",
            start="0s",
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(fcpxml)
    ET.indent(tree, space="    ")
    tree.write(str(output_file), encoding="utf-8", xml_declaration=True)
    return output_file


# =========================================================================
# 2. CapCut Desktop Exporter (draft_content.json)
# =========================================================================

def export_capcut_draft(
    project: Project,
    media_root: Path,
    output_dir: Path,
    *,
    draft_name: Optional[str] = None,
    bgm_path: Optional[Path] = None,
    bgm_volume: float = 0.22,
) -> Path:
    """Export project timeline as a native CapCut Desktop draft folder."""
    output_dir.mkdir(parents=True, exist_ok=True)
    media_root = media_root.resolve()
    name = draft_name or project.title or "Story Studio Project"

    tracks = {t.id: t.kind for t in project.tracks}
    media = {m.id: m for m in project.media}
    video_clips = sorted(
        [c for c in project.clips if tracks.get(c.track_id) == "video"],
        key=lambda c: (c.start_ms, c.id),
    )
    audio_clips = sorted(
        [c for c in project.clips if tracks.get(c.track_id) == "audio"],
        key=lambda c: (c.start_ms, c.id),
    )

    total_us = sum(c.duration_ms for c in video_clips) * 1000

    videos_materials: List[Dict[str, Any]] = []
    audios_materials: List[Dict[str, Any]] = []
    texts_materials: List[Dict[str, Any]] = []

    video_segments: List[Dict[str, Any]] = []
    voice_segments: List[Dict[str, Any]] = []
    text_segments: List[Dict[str, Any]] = []

    # 1. Video track
    for idx, clip in enumerate(video_clips):
        mat_id = str(uuid.uuid4())
        seg_id = str(uuid.uuid4())
        file_path = (media_root / media[clip.media_id].path).resolve()
        dur_us = clip.duration_ms * 1000
        start_us = clip.start_ms * 1000

        videos_materials.append({
            "id": mat_id,
            "path": str(file_path),
            "type": "photo" if file_path.suffix.lower() in (".ppm", ".png", ".jpg", ".jpeg") else "video",
            "duration": dur_us,
            "width": project.width,
            "height": project.height,
        })

        video_segments.append({
            "id": seg_id,
            "material_id": mat_id,
            "target_timerange": {"start": start_us, "duration": dur_us},
            "source_timerange": {"start": 0, "duration": dur_us},
        })

    # 2. Voice audio track
    for clip in audio_clips:
        mat_id = str(uuid.uuid4())
        seg_id = str(uuid.uuid4())
        file_path = (media_root / media[clip.media_id].path).resolve()
        dur_us = clip.duration_ms * 1000
        start_us = clip.start_ms * 1000

        audios_materials.append({
            "id": mat_id,
            "path": str(file_path),
            "type": "extract_music",
            "duration": dur_us,
        })

        voice_segments.append({
            "id": seg_id,
            "material_id": mat_id,
            "target_timerange": {"start": start_us, "duration": dur_us},
            "source_timerange": {"start": 0, "duration": dur_us},
            "volume": 1.0,
        })

    # 3. Subtitles track
    for sub in project.subtitles:
        mat_id = str(uuid.uuid4())
        seg_id = str(uuid.uuid4())
        dur_us = sub.duration_ms * 1000
        start_us = sub.start_ms * 1000

        texts_materials.append({
            "id": mat_id,
            "content": json.dumps({"text": sub.text, "styles": [{"size": 10.0, "fill": {"alpha": 1.0, "content": {"render_type": "solid", "color": [1.0, 1.0, 1.0]}}}]}),
        })

        text_segments.append({
            "id": seg_id,
            "material_id": mat_id,
            "target_timerange": {"start": start_us, "duration": dur_us},
        })

    # Assemble draft tracks
    capcut_tracks = [
        {"id": str(uuid.uuid4()), "type": "video", "attribute": 0, "flag": 0, "segments": video_segments},
    ]
    if voice_segments:
        capcut_tracks.append({"id": str(uuid.uuid4()), "type": "audio", "attribute": 0, "flag": 0, "segments": voice_segments})

    # 4. Background music track if provided
    if bgm_path and Path(bgm_path).is_file():
        bgm_file = Path(bgm_path).resolve()
        bgm_mat_id = str(uuid.uuid4())
        bgm_seg_id = str(uuid.uuid4())
        audios_materials.append({
            "id": bgm_mat_id,
            "path": str(bgm_file),
            "type": "extract_music",
            "duration": total_us,
        })
        bgm_segment = {
            "id": bgm_seg_id,
            "material_id": bgm_mat_id,
            "target_timerange": {"start": 0, "duration": total_us},
            "source_timerange": {"start": 0, "duration": total_us},
            "volume": bgm_volume,
        }
        capcut_tracks.append({"id": str(uuid.uuid4()), "type": "audio", "attribute": 0, "flag": 0, "segments": [bgm_segment]})

    if text_segments:
        capcut_tracks.append({"id": str(uuid.uuid4()), "type": "text", "attribute": 0, "flag": 0, "segments": text_segments})

    draft_content = {
        "id": str(uuid.uuid4()),
        "fps": int(round(project.fps if project.fps > 0 else 25)),
        "duration": total_us,
        "canvas_config": {
            "width": project.width,
            "height": project.height,
            "ratio": "original",
        },
        "materials": {
            "videos": videos_materials,
            "audios": audios_materials,
            "texts": texts_materials,
        },
        "tracks": capcut_tracks,
    }

    now_us = int(time.time() * 1_000_000)
    draft_meta = {
        "draft_id": str(uuid.uuid4()),
        "draft_name": name,
        "draft_root_path": str(output_dir),
        "tm_draft_create": now_us,
        "tm_draft_modified": now_us,
        "draft_timeline_materials_size": 0,
    }

    (output_dir / "draft_content.json").write_text(
        json.dumps(draft_content, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "draft_meta_info.json").write_text(
        json.dumps(draft_meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return output_dir


# =========================================================================
# 3. CMX 3600 EDL Exporter (Universal Edit Decision List)
# =========================================================================

def export_edl(
    project: Project,
    media_root: Path,
    output_file: Path,
) -> Path:
    """Export project timeline as standard CMX 3600 EDL file."""
    media_root = media_root.resolve()
    tracks = {t.id: t.kind for t in project.tracks}
    media = {m.id: m for m in project.media}
    video_clips = sorted(
        [c for c in project.clips if tracks.get(c.track_id) == "video"],
        key=lambda c: (c.start_ms, c.id),
    )

    fps = float(project.fps if project.fps > 0 else 25.0)

    lines = [
        f"TITLE: {project.title or 'STORY STUDIO'}",
        "FCM: NON-DROP FRAME",
        "",
    ]

    for idx, clip in enumerate(video_clips, 1):
        asset = media[clip.media_id]
        asset_file = (media_root / asset.path).resolve()

        src_in = _ms_to_timecode_edl(clip.source_in_ms, fps)
        src_out = _ms_to_timecode_edl(clip.source_in_ms + clip.duration_ms, fps)
        rec_in = _ms_to_timecode_edl(clip.start_ms, fps)
        rec_out = _ms_to_timecode_edl(clip.start_ms + clip.duration_ms, fps)

        # Event line: Event# | Reel (AX=aux) | Track (V/A) | Cut (C) | SrcIn SrcOut RecIn RecOut
        lines.append(f"{idx:03d}  AX       V     C        {src_in} {src_out} {rec_in} {rec_out}")
        lines.append(f"* FROM CLIP NAME: {asset_file.name}")
        lines.append("")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_file
