# ADR-0006 — Portable export bundle (Sprint 07)

Status: IMPLEMENTED PROTOTYPE, not editor integration.

`core/export_bundle.py` generates a deterministic JSON manifest with clip placements, media inventory, subtitle track mapping, and timeline duration. `write_bundle(..., dry_run=True)` is the default and does no I/O. With `dry_run=False`, it preflights relative media paths under the source root, rejects existing destinations, copies media, exports SRT and writes project JSON.

**Not supported:** native Kdenlive/DaVinci/CapCut project files, video rendering, file-hash attestations, or full Windows integration. Clips on the same track may overlap; editorial policy remains pending.

**Security:** path traversal and symlinks resolving outside media root are rejected. Treat media root as trusted and do not concurrently modify it during export. No original Chinese corpus assets are included.
