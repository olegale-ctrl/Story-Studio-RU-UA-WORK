
## 2026-10-30 — Sprint 03: master prompt v1.1 and initial core
- Replaced master prompt with v1.1 (fork/rework, REPLACE/BLOCKED Chinese content, local-first providers, separate locales, CapCut feasibility, transitive dependencies).
- Added ADR-0002, initial `core/project_schema.py`, 7 unit tests, original RU/UA prompt templates and UI strings.
- No original modules or scripts changed.
- No paid APIs, Windows tests, editor imports, license approvals or releases performed.
- Run: `python -m unittest discover -s tests -v` from project root.
- Remaining: dependency license verification, SBOM, real export adapters, robust schema expansion.
