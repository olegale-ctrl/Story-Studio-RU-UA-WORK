# MVP-08B.3 — Pure Offline GenerationJob Core — RESULT

Status: **PENDING_INDEPENDENT_ACCEPTANCE**. Date: 2026-11-20 (Europe/Kiev).

## Authorization and exact revisions

Owner explicitly authorized implementation in the current conversation, superseding the earlier documentation-only execution boundary. G1–G6 remain contract-only approval scoped to PURE; implementation authorization is this separate user task. No independent acceptance/signature is fabricated by this report. Current tests and review are Codex's implementation verification, not independent acceptance.

Repository: olegale-ctrl/Story-Studio-RU-UA-WORK.
Branch: `feat/mvp-08b-3-pure-offline-generation-job-core`.
Implementation base: `16d28ec0376c8c28f879c8aacb18d5378fea83a3`.
Base tree: `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`.
Contract/task commit: `cdadb11d5d28ed22af88bb6570da64b5b6aaa6e7`, tree `269fc02ae3af71c8023fe4bc9039a4ade2fce189`.
FIX-01: `79feb212650df435274998dfb40aed01656a2044`, tree `35812c305495012c1648b14de4c4a04cea6bdf9e`.

**Tested implementation checkpoint commit:** `31e43e801ea31430a940a0ae3e2aaf3326b7bcab`.
**Checkpoint tree:** `711cd43d0cc9621fe5cb2950e4aeabf15c237ac6`.
This checkpoint contains the 12 code/test additions; the publication commit adds only this RESULT.md. Its exact final commit/tree and all 13 file SHA-256/Git blobs are in the accompanying `publication-manifest.json` and final handoff. Self-embedding a final commit/tree into this same file would be recursive; do not substitute checkpoint tree for publication tree.

## Implemented bounded behavior

- 25 closed hashable PURE record types and seven closed nonhashable boundary types; strict scalars, nullable-required fields, unknown-field rejection, duplicate JSON-key rejection, typed transitive closure and association checks. Canonical UTF-8 hashing preserves the approved space-separated local JSON convention, not RFC JCS. Immutable Record stores checked bytes; detached value copies and immutable string/hash caches do not change hash inputs.
- GenerationJob admission and guarded synthetic prefix through fake RESULT_AVAILABLE; immutable request/key/initial receipt and an independent HELD(store_id,project_id,purpose_id) slot. Historical terminal replay returns its original receipt even while a newer job owns the slot. No permission refresh from replay. RESULT_AVAILABLE retains the slot and never implies completion.
- Injected StorePort; **FakeStore exists only in the allowlisted controller test module**. Test harness models one atomic visibility swap, CAS/active uniqueness, immutable event/write-set/receipt history, outbox-before-effect, stable mutation identity, complete committed/absence evidence and a namespace hold on UNKNOWN_COMMIT_OUTCOME. Faults cover before, during, partial/corrupt and after-commit/lost-ACK boundaries. This is not a SQLite or durable storage implementation.
- Virtual ownership, current controller/worker fences, bounded lease claim/renewal, explicit old-owner death/release qualification in the fake port, conservative clock-epoch/rollback hold, preserved cancel intent, SM07/SM08/SM30 containment and SM31 recovery. Recovered old evidence requires a fresh current fenced CAS; no retokenization or authority from receipts.
- One metadata-only simulator facade over a test-local scripted ledger. One immutable generation attempt/effect; repeat dispatch cannot regenerate. Validated, trusted scripted evidence is distinct from merely possessing a matching digest. A submitted effect with no qualified returned receipt reports RESULT_BINDING_MISMATCH with external_effect=UNKNOWN; it is contained/reconciled using the same effect. This is separate from **local StoreMutation COMMIT uncertainty**, which uses UNKNOWN_COMMIT_OUTCOME and a namespace hold. No absence/rollback is inferred from either lost ACK.
- Three **total** committed read reservations per checkpoint (initial plus two retries), consuming interrupted calls conservatively; one read per reservation; no restart/duplicate/same-cursor reset. Known nonacceptance cannot bypass the one-attempt cap; without cancellation it returns ATTEMPT_LIMIT and retains reconciliation, rather than promising an ineligible SM10 retry. Qualified no-acceptance/settlement can complete explicit cancellation, atomically releasing the active slot. Contradictory NO_EFFECT after known acceptance is rejected.
- Single-shot observer with explicit barriers, authoritative cursor and pipeline_complete=false. Error precedence, exact safe messages/actions, external_effect spelling, response-only rejection, no stale/CAS incident writes; no wait or automatic incident append. Fixed profile and all approved finite limits remain unchanged.

## Exact tracked scope

Only these 13 NEW files (100644); no existing file edits/deletions/renames:

| Path | Responsibility |
|---|---|
| experimental_mvp/offline_execution/__init__.py | side-effect-free exports |
| experimental_mvp/offline_execution/contracts.py | closed values, codec, validation, errors |
| experimental_mvp/offline_execution/policy.py | fixed profile/authority/fence/clock ports and guards |
| experimental_mvp/offline_execution/controller.py | bounded lifecycle/transaction/effect orchestration |
| experimental_mvp/offline_execution/observer.py | single-shot authoritative observe |
| experimental_mvp/offline_execution/simulator.py | metadata-only scripted facade and proof consumer |
| tests/test_offline_generation_job_contracts.py | exact vectors and adversarial value tests |
| tests/test_offline_generation_job_controller.py | test-local FakeStore/FakeClock/OwnerLock/ledger and admission tests |
| tests/test_offline_generation_job_observer.py | observer/read scope/hold/error tests |
| tests/test_offline_generation_job_simulator.py | submit/lost ACK/result/cancel/no duplicate tests |
| tests/test_offline_generation_job_faults.py | commit/restart/fence/reservation fault oracles |
| tests/test_offline_generation_job_no_effects.py | effect containment/resource/overflow/profile tests |
| docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md | this report |

No job_store.py, native lock, CLI, fixture/media file, provider client, dependency/config/workflow modification, universal DAG or downstream Library/save integration. Historical contracts are read from pinned Git objects, not copied into this implementation diff. Contract source blob/SHA-256 provenance is in source-manifest.json.

## Actual final tests

Host: Linux-6.18.57-x86_64-with-glibc2.41. Existing interpreters used, no dependency installation. System Python 3.12.14 had no pytest (`python -m pytest --version`, exit 1), so existing pytest environments were used. Test-runner/report I/O and existing SP temporary-file tests are distinct from the guarded new product/fake execution region.

| Run | Python | pytest | PASS tests / subtests | FAIL / ERROR | SKIP | Exit | Wall seconds | Timeout |
|---|---|---|---:|---:|---:|---:|---:|---|
| pure313 | 3.13.18 | 9.2.0 | 164 / 0 | 0 / 0 | 0 | 0 | 7.138 | False |
| pure310 | 3.10.22 | 9.2.0 | 164 / 0 | 0 / 0 | 0 | 0 | 9.14 | False |
| sp_regressions313 | 3.13.18 | 9.2.0 | 69 / 110 | 0 / 0 | 0 | 0 | 0.415 | False |

All final processes were bounded by a 60-second external watchdog; combined final invocation limit 300 seconds. No timeout occurred. SP reports **69 tests passed plus 110 subtests passed** (179 JUnit records), not 179 independently collected test methods. The complete repository/media/model suite was NOT_RUN and is not represented by this limited regression count. Native Windows qualification: WINDOWS_NOT_RUN.

Exact commands (absolute interpreter/log/XML paths are additionally retained in acceptance-results.json):

```text
/workspace/work/venv313/bin/python -m pytest -q -p no:cacheprovider --junitxml=/workspace/work/mvp08b3-evidence/pure313.xml tests/test_offline_generation_job_contracts.py tests/test_offline_generation_job_controller.py tests/test_offline_generation_job_observer.py tests/test_offline_generation_job_simulator.py tests/test_offline_generation_job_faults.py tests/test_offline_generation_job_no_effects.py
/workspace/work/venv310/bin/python -m pytest -q -p no:cacheprovider --junitxml=/workspace/work/mvp08b3-evidence/pure310.xml tests/test_offline_generation_job_contracts.py tests/test_offline_generation_job_controller.py tests/test_offline_generation_job_observer.py tests/test_offline_generation_job_simulator.py tests/test_offline_generation_job_faults.py tests/test_offline_generation_job_no_effects.py
/workspace/work/venv313/bin/python -m pytest -q -p no:cacheprovider --junitxml=/workspace/work/mvp08b3-evidence/sp_regressions313.xml tests/test_topic_to_film.py tests/test_topic_to_film_v1_1.py
```

## Mandatory-oracle traceability

46 A/R/E requirement labels map to actual executed PASS cases on both interpreters in oracle-coverage.json. They are not a fabricated test count: parametrization produces 164 collected pure tests on each interpreter. Groups below identify the test functions; exact parameterized names and per-case status are in JUnit XML/acceptance-results.json.

| Obligation | Executed test-function family |
|---|---|
| A01 | `test_A01_A02_A07_A08_A09*` |
| A02 | `test_A01_A02_A07_A08_A09*` |
| A03 | `test_A03_A05*` |
| A04 | `test_A04_E15*` |
| A05 | `test_A03_A05*` |
| A06 | `test_A06_unknown_terminal*`, `test_A06_terminal_committed*` |
| A07 | `test_A01_A02_A07_A08_A09*` |
| A08 | `test_A01_A02_A07_A08_A09*` |
| A09 | `test_A01_A02_A07_A08_A09*`, `test_A09_expired*` |
| A10 | `test_A10_interleaved*` |
| R01 | `test_R01_*` |
| R02 | `test_R02_*` |
| R03 | `test_R03_*` |
| R04 | `test_R04_*` |
| R05 | `test_R05_*` |
| R06 | `test_R06_*` |
| R07 | `test_R07_*` |
| R08 | `test_R08_*` |
| R09 | `test_R09_*` |
| R10 | `test_R10_*` |
| R11 | `test_R11_*` |
| R12 | `test_R12_*` |
| R13 | `test_R13_*` |
| R14 | `test_R14_*` |
| R15 | `test_R15_*` |
| R16 | `test_R08_*`, `test_lost_submit_ACK*` |
| E01 | `test_E01_E02_*`, `test_exact_source_arithmetic*` |
| E02 | `test_E01_E02_*` |
| E03 | `test_E03_*` |
| E04 | `test_E04_*`, `test_E04_E05_*` |
| E05 | `test_E05_*`, `test_E04_E05_*` |
| E06 | `test_E06_*` |
| E07 | `test_R07_E07_E08_*` |
| E08 | `test_R07_E07_E08_*` |
| E09 | `test_R12_E09_E10_E11_*` |
| E10 | `test_R12_E09_E10_E11_*`, `test_each_committed_reservation*` |
| E11 | `test_R12_E09_E10_E11_*`, `test_R13_*` |
| E12 | `test_E12_*` |
| E13 | `test_E13_*` |
| E14 | `test_R08_E14_*` |
| E15 | `test_A04_E15_*` |
| E16 | `test_E16_*` |
| E17 | `test_E17_*` |
| E18 | `test_E18_*`, `test_import_surface_*` |
| E19 | `test_E19_*`, `test_sequence_overflow_*` |
| E20 | `test_E20_*`, `test_corrected_v030_*`, `test_exact_source_arithmetic_*` |

All 36 historical fixed preimages have their exact bytes/digests checked. Old V030 is rejected as FORMAT. OA-V030-CORRECTED-1 validates with SHA-256 `1ee3123931b2fdac839858cc79d20bd05342c778c2855fb2cef3a26c7bf4fe58`. A separate handwritten encoder independently matches all fixed preimage bytes and the exact 63-bit integer maximum; it does not delegate encoding to json.dumps. No enum/hash was silently rewritten.

P003/P004/P012 use the corrected identity/idempotency references and T005 for active intent. P011 has separate unsupported handler versus provider/model/version/region/mode outcomes. P019 wait is **NOT_RUN / DEFERRED**, no wait method exists. Existing SP diagnostic/Topic-to-Film tests pass while their execution/production gates remain blocked; no actual Route D renderer is invoked.

## Development failures and corrections retained

Initial targeted run: 79 PASS / 4 FAIL (exit 1): APIOutcome.error incorrectly embedded a full ResponseError header where the contract requires inline fields. Corrected without relaxing the closed schema. First complete run: 117 PASS / 4 FAIL (exit 1): claim/read-reserve while SUBMITTING incorrectly attempted creation of another outbox, and the static import guard did not recognize the legitimate `from . import policy`. Fixed the new-submit condition to QUEUED -> SUBMITTING only and allowed that exact local import form, retaining the native/dynamic-code prohibition. Focused repeat: 5 PASS, 22 deselected, exit 0; then full run 158 PASS, exit 0.

Further review added exact-expiry, unknown-terminal-after-commit and committed-outbox-before-effect cases; separated missing simulator reply from local COMMIT outcome, enforced the one-attempt eligibility guard, and rejected contradictory cancellation settlement. Intermediate complete PASS runs at 162/163 tests are retained as historical evidence, not final counts. The final runs above are the authoritative current results. Immutable Record caching/deepcopy sharing removed repeated parsing of already checked immutable bytes; no validation/oracle/finite bound was removed. Final pure runs are well within the unchanged 60-second limit. Raw failed development logs and later results are included in the review packet; no failed result was relabeled PASS.

## Limitations and remaining gates

- FakeStore/FakeClock/OwnerLock/ledger are explicitly injected trusted **test models**. Snapshot retention and modeled operation registry survive simulated controller replacement because the harness retains Python values. No actual process-kill/power-loss/SQLite/WAL/fsync/backup restoration/native concurrency qualification is claimed. The atomic swap/interleaving test is a model, not a thread/OS mutex implementation.
- Qualified fake ledger receipts establish consumer behavior only, not a real signer, provider, producer, license, commercial permission or MP4 output. Stable IDs/hashes do not grant any of these capabilities. No live API, paid operation, model or FFmpeg/real render occurred.
- Windows native ownership, reparse points/symlinks, NTFS, reboot clocks and no-admin behavior are WINDOWS_NOT_RUN. There is no native path access in the new pure core. Real filesystem/TOCTOU/asset substitution defenses remain a separate future qualification, not solved by hashing or fake lease tests.
- Durable local storage, real asset bytes/decoder/rights validation, Asset Library ingestion, GUI attach/project save, downstream completion and live/production integration are NOT_RUN / NOT_AUTHORIZED. The pure prefix retains its slot at RESULT_AVAILABLE. Recognized downstream/terminal vocabulary and terminal-history tests are not implementation of the local result pipeline.
- No main, workflow/dependency, normative contract, merge/release or production storage/permissions change. No automatic MVP-08B.4. D01–D08 and unapproved EC/OD choices outside PURE remain unchanged.

## Independent handoff / STOP

Review exact baseline/allowlist/diff, source manifest, file blobs/SHA-256, mandatory-oracle map, raw logs/JUnit and private-index tree reproduction in the accompanying packet. Pay particular attention to trust boundaries, atomicity assumptions, unknown COMMIT holds, immutable evidence/current authority, canceled recovery, finite read reservations and no additional generation attempts. Passing scripted tests does not constitute owner or independent acceptance.

**PENDING_INDEPENDENT_ACCEPTANCE. STOP.** Await independent ChatGPT review and owner decision. No MVP-08B.4, merge, release, production operation or permission expansion.
