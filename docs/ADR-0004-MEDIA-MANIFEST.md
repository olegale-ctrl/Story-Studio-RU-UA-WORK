# ADR-0004 — Portable media manifest (Sprint 05)

Status: PROTOTYPE. Existing project schema v2 remains unchanged.

`core/media_manifest.py` derives an inventory of image/audio references from scene fields. It does not copy, access or license media. Paths are normalized to portable forward-slash relative paths; absolute, drive, UNC, traversal and URL-like paths are rejected. These restrictions apply to manifest export only; legacy scene JSON may still contain absolute paths and must be migrated explicitly before export.

A manifest is **not** an editor project, a rights clearance, an SBOM or a guarantee that files exist. Future work: v3 typed clips with source offsets, track placement, media IDs and schema migration; exporters; Windows validation.
