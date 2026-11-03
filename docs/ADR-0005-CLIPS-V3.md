# ADR-0005 — Typed clips and media, schema v3
Status: PROTOTYPE ACCEPTED, 2026-10-30

`MediaAsset(id,kind,path)` stores a portable media reference. `Clip(id,track_id,media_id,start_ms,duration_ms,source_in_ms)` places it on a video or audio track. Subtitle tracks use existing `Subtitle` records. IDs are unique within their own collections. A video track accepts image/video; an audio track accepts audio. Paths are relative and validated independently of host OS.

Project schema v3 adds `media` and `clips` arrays. v1 and v2 are migrated in memory without writing input files. `schemas/project-v3.schema.json` is structural only: Python validates cross references, duplicates and portability.

Not implemented: source duration checks, overlap policy, video editor project export, file copying.
