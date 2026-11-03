# ADR-0008 — Standard-library CLI and schema conformance

Status: IMPLEMENTED (CLI); JSON Schema cross-validation remains pending.

- `python -m core.cli` exposes `check`, `preview`, `bundle`, `verify`.
- No external dependencies, paid API, editor or Windows-specific package is required.
- `check` uses authoritative Python validation; the draft JSON Schema is **not** yet a fully equivalent semantic contract.
- A JSON Schema validator and negative conformance suite are required before claiming formal schema parity.
- Bundle integrity is checksum verification, not cryptographic authenticity or protection against a maliciously replaced integrity manifest.
