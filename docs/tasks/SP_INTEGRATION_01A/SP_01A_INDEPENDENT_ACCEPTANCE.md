# Independent acceptance

**SP-INTEGRATION-01a · 2026-11-19 · DOCS_ONLY · FREEZE_FOR_REVIEW, NOT OWNER_APPROVED.**

Review target: commit `8f0b4dec17b3ba56adec74b73c86ef3cf7e11649`, tree `0abb32b2d453fa4d9db50f6b6aef9597cf4e43a2`, parent `f0bce140451bf00a86f3939330e77ed63b2c98be` (tree `0b5238611cc84ef0a665f75b552757666935516e`). Remote candidate branch matches the target. New documentation branch `docs/sp-integration-01a-acceptance-contract-freeze` starts at that exact target. Observed main remains `a28277b4cb68a3db5da52edc598c37ce66314604` (tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`).

Authority: the current owner task reports a **preliminary independent ChatGPT verdict ACCEPTED_WITH_LIMITATIONS for limited offline implementation**. This document records that assertion and a fresh source/hash/test replay. It does not pretend a separate human/model reviewer was newly engaged, convert the preliminary audit into owner approval of SP/1, or grant merge/execution/release authority. Original implementation status PARTIAL_IMPLEMENTATION remains accurate.

|Claim|Result|Evidence and scope|
|---|---|---|
|Exact candidate commit/tree/parent|VERIFIED|Fresh Git object inspection, raw source bytes and private-index tree reconstruction|
|Exactly22 added files, no existing files changed|VERIFIED|Full parent→candidate name/status inventory; all A, all mode100644; manifest below|
|No second Dispatcher/JobStore/retry/locks/recovery in SP addition|VERIFIED|Full three-module source and call review; no such state owner or runtime mechanism; repository definition search exit1/no matches|
|No direct first_video.build bypass|VERIFIED|New gates import read_plan/safe_image/wav_ms only; CLI has no build call; existing test mocks build/subprocess to fail if invoked|
|Flags cannot create permissions|VERIFIED|requested_attestations only; initial_readiness all unknown; CLI returns3, no accepted IDs|
|SI eligibility independent of factual review|VERIFIED|Separate field; assess_release separately requires facts_reviewed true; test and FV18|
|Diagnostic return cannot release|VERIFIED|Every release_allowed literal in SP production modules is false; both relevant schemas const false; FV24 tests all asserted axes true|
|Draft cannot bypass release/gates|VERIFIED|FV25 denies production prerequisite; no --skip-gates option; final gates always blocked|
|Windows/storage/technical claims limited correctly|VERIFIED_WITH_LIMITATIONS|Source explicitly retains TOCTOU/reparse/storage and missing decoder/authority limitations; no native platform qualification performed|
|Schema validity equals semantic validity|REJECTED|G01–G03 differential probes; shape success cannot certify routing, digest, path, exact hash syntax or rights|
|necessary_conditions_satisfied proves complete valid readiness/authority|REJECTED|G04 accepts supplied minimal assertions; release_allowed remains false|
|Dispatcher/JobStore acceptance, idempotency, status, recovery and publication|BLOCKED_CONTRACT|Absent runtime API in inspected tree; MVP08B.1 explicitly proposal-only|
|MVP08B.2 implementation/compatibility|NOT_TESTED|No advertised/local artifact located; availability search is VERIFIED, runtime cannot be verified|
|Windows/native TOCTOU, final MP4/image/clip decoding, live provider, production|NOT_TESTED|No such test or operation executed; not inferred from unit results|

Actual fresh execution on Linux/Python3.12.14: `python -m unittest tests.test_topic_to_film -v` →37 tests,0 skipped,exit0. Independent schema/vector replay with jsonschema4.26.0 →117 assertions,46 vectors,4 recorded differential gaps,exit0. These counts are different metrics, not additive test totals. Full video/GUI regression was NOT_RUN in this documentation stage; prior874/2-skip result is historical only. No video generation, decoder subprocess, ComfyUI/Wan or provider request was initiated.

Acceptance conclusion: **VERIFIED_WITH_LIMITATIONS**, consistent with the task-supplied preliminary ACCEPTED_WITH_LIMITATIONS for offline preparation. Strict normative SP/1 interchange, Dispatcher integration, authority and final execution/release acceptance remain blocked. Four contract gaps must accompany any owner decision; no code/schema is silently corrected here.

## Exact candidate file inventory

|Path|Git blob SHA1|
|---|---|
|`core/topic_to_film.py`|`08ae2c9b39616d8d450c02fbdb2deefcc2378808`|
|`core/topic_to_film_gates.py`|`1d94063013dcf88bf15e1db86d9743f109b44046`|
|`docs/tasks/SP_INTEGRATION_01/ARTIFACT_SCHEMAS.md`|`efc1da9364bf8937228deb360ef6375cf010104e`|
|`docs/tasks/SP_INTEGRATION_01/FALLBACK_POLICY.md`|`b78ba4d018066411d13ff69ecb18afbeaf8dd952`|
|`docs/tasks/SP_INTEGRATION_01/HARDWARE_PREFLIGHT_INTEGRATION.md`|`10a33fc1058039670640a4114fdf6d4618613029`|
|`docs/tasks/SP_INTEGRATION_01/IMPLEMENTATION_REPORT.md`|`5f96c8505c143bedab31b3117a13d6cec98232cd`|
|`docs/tasks/SP_INTEGRATION_01/INTEGRATION_INVENTORY.md`|`1ebb1e1dc8f1518e9ee822deacd8060967c614b5`|
|`docs/tasks/SP_INTEGRATION_01/OPEN_CONTRACT_GAPS.md`|`5ef07bd6675d1ace7b9033b98c1947205df124af`|
|`docs/tasks/SP_INTEGRATION_01/READINESS_AND_RELEASE_POLICY.md`|`c3baf08573d260dec9e51736ea12f472fb08f1c7`|
|`docs/tasks/SP_INTEGRATION_01/ROUTING_AND_JOB_MATRIX.md`|`9d999a93aefb17bfff4cf3b38c92eb5bd4ab7b82`|
|`docs/tasks/SP_INTEGRATION_01/TECHNICAL_GATES_CONTRACT.md`|`3d9348e2ed6e18069815c021f8ebe519bc04e671`|
|`docs/tasks/SP_INTEGRATION_01/TEST_ORACLES.md`|`9e5033b37affc768c9cd808a994e9fa2b0f79e99`|
|`docs/tasks/SP_INTEGRATION_01/TOPIC_TO_FILM_CONTRACT.md`|`66cc464e774617df3fb75d7922db15d78644e1e8`|
|`schemas/topic-to-film-v1/artifact_manifest.schema.json`|`ee372d472a8c51661df986844cf46e1dc43c7c2a`|
|`schemas/topic-to-film-v1/job_intent.schema.json`|`17d7e14c99e271dc4222c02cf16c6428082ef343`|
|`schemas/topic-to-film-v1/jobs.schema.json`|`7fd600d302c3611fa34b6ec80540ecb88cfeaed1`|
|`schemas/topic-to-film-v1/production_readiness_report.schema.json`|`2dca55a10a52d5e5f6b70d5b7f017e348d483bfa`|
|`schemas/topic-to-film-v1/readiness.schema.json`|`b2aa609059a74427d300ca0770147268af94e965`|
|`schemas/topic-to-film-v1/route.schema.json`|`3840a30264a556e86efd9423fd33f535502f2901`|
|`schemas/topic-to-film-v1/technical_gate_report.schema.json`|`b99386959ae02ccfbca438eded619881ab267a81`|
|`scripts/topic_to_film.py`|`a52e29fd474163cdc0b20e44b1d88bd27e0e2e14`|
|`tests/test_topic_to_film.py`|`dff5bff31074ebe604578b1966987e16c2013d19`|


Raw SHA256, byte counts and exact snapshots are in external candidate-manifest.json/candidate/. Git blob SHA1 is not raw SHA256 and not a PG binding. All22 source additions remain byte-for-byte unchanged by this docs branch.
