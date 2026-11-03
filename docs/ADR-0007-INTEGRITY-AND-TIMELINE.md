# ADR-0007 — Timeline diagnostics and bundle integrity

Status: implemented in Sprint 08 (2026-10-30).

- Overlapping clips on a track are permitted by the v3 contract; `audit_timeline` reports warnings, not validation failures.
- `source_in_ms` cannot be checked against media duration without trusted probing; an informational diagnostic is issued.
- Opt-in bundle writing now includes `integrity.json` with SHA-256 and byte length for each output file, excluding itself.
- `verify_bundle` detects missing, modified, and unlisted files. This is integrity, **not** authenticity or license verification.
- Native editor import, Windows behavior, codec support, and original Chinese media licensing remain unverified.
