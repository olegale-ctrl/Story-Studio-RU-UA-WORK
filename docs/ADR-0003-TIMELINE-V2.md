# ADR-0003 — Timeline schema v2 and SRT baseline
Date: 2026-10-30 | Status: ACCEPTED (implementation partial)

## Decision
- Keep editor-neutral data model in Python standard library; preserve original Jianying scripts unchanged.
- `schema_version=2` adds typed `tracks` (`video`, `audio`, `subtitle`) and `subtitles` (id, track_id, start_ms, duration_ms, text, locale).
- Version 1 JSON payloads are accepted and migrated **in memory** to v2 with empty tracks/subtitles. Saving always writes v2.
- Reject unknown JSON fields, duplicate ids, invalid timing, non-subtitle track references and unsupported locales.
- SRT exporter targets one explicitly selected subtitle track, uses millisecond timestamps, Unicode text and deterministic ordering.

## Scope limitations
- Video/audio tracks currently have metadata only; no clips, transitions, effects, media mapping or rendering.
- Subtitles are not yet constrained to project duration; overlapping subtitles are allowed.
- `fps` is display metadata; no frame-accurate rounding or editor-specific export.
- No native Kdenlive/DaVinci/CapCut project format; CapCut remains feasibility-only.
- v1 input migration requires the original strict v1 field set; it is not a universal migration engine.

## Compatibility
- Sprint 03 Python callers that instantiate `Project(title, content_locale, scenes)` continue to work.
- Sprint 03 JSON with `schema_version=1` is readable; after serialization it becomes v2.
- Older Sprint 03 code cannot read v2; retain backups before replacing files.

## Follow-up
1. Introduce clip references and project media validation; choose stable asset ID strategy.
2. Add JSON Schema and explicit migration fixtures.
3. Prototype Kdenlive-compatible interchange and test in actual editor on Windows.
4. Document SRT limitations and verify Unicode roundtrip in Windows.
