## 2026-10-30 — Sprint 04: editor-neutral timeline v2 + SRT
- Read `MASTER_PROMPT.md` v1.1 and `NEXT_SESSION.md` from Sprint 03; no Git checkout was available in the isolated update workspace (Git state on user's machine unknown).
- Changed: `core/project_schema.py` (v2 tracks/subtitles + strict validation + v1 in-memory migration); `tests/test_project_schema.py` (14 new cases).
- Added: `core/subtitles.py`, `tests/test_subtitles.py` (3 cases), `docs/ADR-0003-TIMELINE-V2.md`, `audits/SPRINT04_TEST_RESULTS.txt`, installer.
- Tests: 24/24 passed, Python 3.13 Linux. Command `PYTHONPATH=<Sprint04Root> python -m unittest discover -s <Sprint04Root>/tests -q`. No Windows, editor, full-repository or integration tests.
- License: new Python code uses only stdlib; no license approvals issued. Upstream binaries, Python/npm transitive deps, Chinese corpora and third-party media remain release-blocked pending evidence.
- No original scripts/modules changed. No network, API calls, publication or payments.
- Next: clip references, JSON Schema/fixtures, static dependency inventory with provenance; Windows smoke test by user when ready.
