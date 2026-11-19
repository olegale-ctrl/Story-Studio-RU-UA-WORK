# Test oracles and actual coverage

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

Implemented synthetic unit tests are in `tests/test_topic_to_film.py`. Full execution counts/exit codes are in IMPLEMENTATION_REPORT and external logs. Current tests do not implement or execute proposed Dispatcher recovery scenarios.

|Required case|Executed safe oracle|Remaining runtime qualification|
|---|---|---|
|1 A/B/C/D|test_routes|Future registered job DAG NOT_RUN|
|2 A production|test_a_production_blocked|Approved policy/authority absent|
|3 Missing artifact|test_missing_plan_c|Authoritative storage receipt absent|
|4 Locale/plan|test_bad_locale,test_bad_scene_count|Other plan dialects not supported|
|5 Unsafe image|test_unsafe_image_paths|Hostile OS/reparse races NOT_RUN|
|6 WAV missing/corrupt|test_missing_wav,test_wav_corrupt,test_wav_valid_and_truncated|Production codec/runtime qualification NOT_RUN|
|7 Production placeholder|test_placeholder_production|No placeholder execution|
|8 Degraded no policy|test_degraded_without_policy|Approved degraded release policy absent|
|9 SI vs facts|test_si_does_not_clear_facts|Authenticated reviewer unavailable|
|10 MP4 vs rights|test_mp4_does_not_clear_rights|No claim actual MP4 decode in this unit oracle|
|11 Changed SHA/policy|test_stale_sha_and_policy|Equality only; trusted grant applicability verifier NOT_RUN|
|12 Unauthorized render|test_render_intent_never_grants|No execution attempted|
|13 Same intent rerun|test_repeat_intent_deterministic_not_submitted|Dispatcher idempotency effects NOT_RUN|
|14 Mirror mismatch|test_wait_cannot_trust_local_mirror verifies API-unavailable block|Actual JobStore/local mirror mismatch injection NOT_RUN: no APIs/mirror|
|15 Job/publication gap|test_publication_failure_not_simulated_as_success verifies publication-contract block|Actual crash injection between job completion/publication NOT_RUN|
|16 Insufficient hardware|test_insufficient_hardware|Actual qualified worker resource enforcement NOT_RUN|
|17 Incomplete final|test_final_incomplete|Completed render binding validation NOT_RUN|
|18 No release permission|test_no_release_permission|Authority verification unavailable|
|19 Draft gate bypass|test_draft_no_gates_bypass,test_skip_gates_not_an_option|No draft execution authorization exists|
|20 Missing Dispatcher|test_absent_dispatcher_never_direct_render patches build/subprocess to raise if called|Real submission/observation NOT_RUN|

Additional oracles cover ambiguous/empty input, immutable copies, strict material declaration shape, equivalent fallback, installed-model≠qualified, boolean axis rejection, duplicate JSON keys, size cap, symlink rejection, intermediate≠final, and all asserted conditions≠permission. Schema meta-validation and representative fixtures are executed separately using locally installed jsonschema; it is not a new runtime dependency.

All future Dispatcher/JobStore crash/reconciliation/resume tests require the actual approved API; they are blocked, not counted as passed fault-injection tests. Pure equality testing does not establish authorization correctness. Existing regression suites may execute their own small synthetic FFmpeg tests; their success does not qualify new production workflows or imply new heavy generation authorization.
