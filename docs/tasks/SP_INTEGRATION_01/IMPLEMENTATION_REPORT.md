# Implementation report

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

Final status: **PARTIAL_IMPLEMENTATION**. Pure offline components and read-only diagnostics implemented; Dispatcher/JobStore, authority/attestation, qualified final gates, storage publication and release remain BLOCKED_CONTRACT. No end-to-end film generation is claimed.

Base `f0bce140451bf00a86f3939330e77ed63b2c98be`, tree `0b5238611cc84ef0a665f75b552757666935516e`; branch `feat/sp-integration-01-topic-to-film`. Exact final commit/tree, full-index diff, source and changed-file SHA manifests, remote verification and packet digest are supplied externally to avoid self-referential hashes.

Changed files: three new modules, one synthetic test module, seven proposal schemas and eleven documents. Existing G1/G2/G3.1/experimental implementation, owner records and CI unchanged. No queue/JobStore/retry/recovery/lock implementation, new provider/network service, heavy generation, artifact cleanup, production grant, merge or release.

## Actual verification

Linux x86_64, Python **3.12.14**, Tk **9.0.4**, pytest **9.2.0**, FFmpeg/FFprobe **7.1.5-0+deb13u1**, jsonschema **4.26.0** (schema-check tooling only). No packages/models installed for this task. GUI regressions used existing Xvfb on DISPLAY=:91, not Windows or independent visual/audio acceptance.

|Check / command|Actual result|Exit code|
|---|---|---|
|`python -m unittest tests.test_topic_to_film -v`|37 tests, all PASS;0 skipped|0|
|Initial `python -m pytest -q tests experimental_mvp` with unavailable DISPLAY=:91|863 passed,11 failed,2 skipped,3689 subtests passed; failures were Tk unable to connect to display|1|
|After starting existing Xvfb: selected asset/media/timeline/stabilization GUI suites|27 passed,0 skipped,23 subtests passed|0|
|Final `DISPLAY=:91 python -m pytest -q tests experimental_mvp`|874 passed,2 skipped,3689 subtests passed|0|
|Seven proposal schemas: metaschemas, A/B/C/D fixtures and negative boolean/grant fixtures|59 checks PASS; not production qualification|0|
|`python scripts/check_hardware.py`|Linux CPU inventory; RAM unknown, diagnostics_complete=false; no workload qualification|0|
|CLI topic plus requested attestations and `--wait 1`|Explicit BLOCKED_DISPATCHER_CONTRACT/BLOCKED_JOBSTORE_CONTRACT; empty IDs, all axes unknown|3 (expected BLOCKED)|
|CLI `--skip-gates`|Rejected unsupported option; no bypass|2 (expected invalid input)|
|Windows10/11, NTFS/reparse, Python3.10/3.13|NOT_RUN; no Windows or alternate-interpreter PASS claimed|N/A|

Final full-suite skips: `tests/test_editor_preview.py::PreviewOutputPaths::test_native_directory_junction` (Windows junction requires NTFS) and `experimental_mvp/test_asset_library.py::LibraryTests::test_windows_junction` (WINDOWS_NOT_RUN: requires Windows/NTFS). These are not silently treated as successes. Pytest emitted one existing anyio/pytest deprecation warning; no test failure remained. Initial unavailable-display failures are retained in `regression.log`, and successful rerun is `regression-final.log`; per-command exit codes/timings are in external JSON.

No existing code was changed to obtain passing results. Final Git diff/mode/allowlist/source-hash/tree reconstruction and remote checks are recorded in the external packet.

Limits: Windows NOT_RUN; actual Dispatcher submission/idempotency/recovery/publication crash injection NOT_RUN (missing APIs); final image/clip/MP4 worker validation NOT_RUN; rights/facts/creative suitability and authenticity not proven; filesystem TOCTOU/reparse/hardlink/storage qualification incomplete; no production permissions; S3/Library mutations not performed. Model presence and sufficient hardware do not authorize execution. Historical baseline test counts are not reused as current results.

Evidence packet permits independent reconstruction from exact base with the supplied full-index diff, verification of Git blobs/raw SHA-256/modes/tree, and rerunning tests without provider credentials. Final tree cannot include its own commit hash, so final identity is in external ACCEPTANCE_PACKET.json and final handoff. STOP for independent ChatGPT review and owner decision; no automatic continuation.

## Exact changed-file allowlist

- `core/topic_to_film.py`
- `core/topic_to_film_gates.py`
- `scripts/topic_to_film.py`
- `tests/test_topic_to_film.py`
- `schemas/topic-to-film-v1/artifact_manifest.schema.json`
- `schemas/topic-to-film-v1/job_intent.schema.json`
- `schemas/topic-to-film-v1/jobs.schema.json`
- `schemas/topic-to-film-v1/production_readiness_report.schema.json`
- `schemas/topic-to-film-v1/readiness.schema.json`
- `schemas/topic-to-film-v1/route.schema.json`
- `schemas/topic-to-film-v1/technical_gate_report.schema.json`
- `docs/tasks/SP_INTEGRATION_01/ARTIFACT_SCHEMAS.md`
- `docs/tasks/SP_INTEGRATION_01/FALLBACK_POLICY.md`
- `docs/tasks/SP_INTEGRATION_01/HARDWARE_PREFLIGHT_INTEGRATION.md`
- `docs/tasks/SP_INTEGRATION_01/IMPLEMENTATION_REPORT.md`
- `docs/tasks/SP_INTEGRATION_01/INTEGRATION_INVENTORY.md`
- `docs/tasks/SP_INTEGRATION_01/OPEN_CONTRACT_GAPS.md`
- `docs/tasks/SP_INTEGRATION_01/READINESS_AND_RELEASE_POLICY.md`
- `docs/tasks/SP_INTEGRATION_01/ROUTING_AND_JOB_MATRIX.md`
- `docs/tasks/SP_INTEGRATION_01/TECHNICAL_GATES_CONTRACT.md`
- `docs/tasks/SP_INTEGRATION_01/TEST_ORACLES.md`
- `docs/tasks/SP_INTEGRATION_01/TOPIC_TO_FILM_CONTRACT.md`
