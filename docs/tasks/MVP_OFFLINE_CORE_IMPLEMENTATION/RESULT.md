# MVP-08B.3 — Independent Acceptance Fix 01 — RESULT

**Current status: READY_FOR_RE_REVIEW.** Date: 2026-11-20 (Europe/Kiev).
This records the targeted fix and Codex verification, not independent closure or owner acceptance of either finding. The prior implementation report is retained below as a clearly marked historical record; its status/counts/revisions are not the current fix results.

## Exact baseline and authorization

Repository: olegale-ctrl/Story-Studio-RU-UA-WORK.
Branch: `fix/mvp-08b-3-independent-acceptance-01`.
Base commit: `ea4df639e24950cde5f925975949751f9805a8e6`.
Base tree: `2920839ee0588809e93c2ada149551542b734de1`.
Tested code checkpoint: `9a01050b07482eed304ae388e886f77eb48d6ff9`.
Checkpoint tree: `359e1cc50a52b24e696839bde5d152cf960e4b3d`.
The final publication commit adds only this RESULT.md update to that tested checkpoint; its final commit/tree, full diff and five file blob/SHA-256 values are in the accompanying publication-manifest.json and final handoff. A final commit/tree cannot be recursively embedded into the same report file.

Authorization is the owner's Independent Acceptance Fix 01 task: fix F-08B3-01 and investigate F-08B3-02 inside exactly five existing files. No full independent-review text beyond the provided finding IDs/task was supplied; this report does not invent or quote an unseen review. G1–G6, approved schemas/error vocabulary, fixed profile and limits remain unchanged. No BLOCKED_CONTRACT condition was required to implement this bounded correction.

## Findings: observed before and after

| Finding | Reproducer at exact base | Fixed behavior | Executed checks |
|---|---|---|---|
| F-08B3-01 | A has qualified acceptance; B has no generation intent. A stale-worker error for B incorrectly reports external_effect=KNOWN. | Same error for B reports NONE; foreign A receipt is not attributed to B. | 18 standalone new cases plus shared guarded no-effect case; 12-case matrix across admit/dispatch/apply_proof/resolve_commit and B=NONE/UNKNOWN/KNOWN |
| F-08B3-02 | Typed exception after terminal COMMIT plus raw snapshot outage escapes as RuntimeError; pending is not retained, and another admission is accepted before M is resolved. | Returns HOLD / UNKNOWN_COMMIT_OUTCOME, retains M and namespace barrier; next admission remains HOLD. Only bound COMMITTED proof permits progress. | 20 standalone new cases plus shared guard; 17 COMMIT/diagnostic combinations, qualified absence, hold-port failure, no-submit/stale-write containment |

`baseline-reproducer.json` and `fixed-reproducer.json` contain the actual before/after observations from separate interpreter processes loading their respective worktrees. Harness exit 0 means observations were captured; the baseline `matched=false` explicitly records failure of the required behavior, not a baseline PASS. These small reproductions use only retained Python test-model values, not a real provider or database.

## What changed

**Job-scoped attribution:** error paths now carry explicit job, immutable AdmissionCommand or StoreMutation identity. Classification requires an authorized, structurally consistent snapshot. NONE requires a proved not-yet-admitted key or target job without generation/outbox intent. KNOWN requires the target job's bound namespace/job/request/key/permit/generation/attempt/effect identities, matching outbox payload, verified acceptance record and qualified scripted-ledger attestation. A receipt elsewhere in the store, an unmatched target, an unattested matching record, or an intent alone cannot establish KNOWN. Unreadable, inconsistent or pending evidence yields UNKNOWN. Classification performs no store mutation or submit.

**COMMIT boundary:** the exact Plan remains locally latched until complete same-mutation proof and acknowledgement. Any ordinary exception from COMMIT, including ContractError after an actual commit, is not treated as rollback. A typed pre-commit exception can return NOT_COMMITTED only after complete verified absence evidence; the typed exception alone is insufficient. COMMITTED/NOT_COMMITTED ACK strings also require a complete matching proof. Unknown/malformed/missing proof, snapshot outage or corruption keeps HOLD. Diagnostic failures cannot clear a known hold or escape in place of the required error response.

**Snapshot integrity:** the current job/receipt/outbox graph and HELD-slot index must be consistent. Missing job bytes, missing receipts and contradictory slot indices are rejected rather than qualifying absence or releasing an intent. Raw snapshot/proof exceptions are contained. The local latch is a fail-closed fallback when the hold port itself is unavailable; it is not durable storage.

**Faithful test model:** FakeStore retains the immutable operation intent before the unsafe boundary and keeps pending until verified proof acknowledgement, using the already-existing ports. Intent/input reference closure is retained separately from actual committed write-set members; that cache cannot prove member presence. The A10 interleaving uses independent controller facades sharing the same qualified owner/store, so the local in-flight latch does not serialize away the competing atomic uniqueness check. No mandatory case, schema guard or resource bound was removed.

## Exact permitted diff

Only these five existing files are modified; no new/deleted/renamed repository files:

- experimental_mvp/offline_execution/controller.py
- tests/test_offline_generation_job_controller.py
- tests/test_offline_generation_job_faults.py
- tests/test_offline_generation_job_no_effects.py
- docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md

contracts.py, policy.py, observer.py, simulator.py, all other tests, historical contracts, workflows and dependencies are unchanged from the pinned base. Supporting logs/scripts/packet files are outside the repository worktree. Source SHA and diff scope are checked independently of test pass counts.

## Actual final verification

All six pure test modules were run explicitly on each interpreter. Existing SP/Topic-to-Film regressions were also run on each interpreter. Environments were already installed; no dependencies or system settings changed. Linux-6.18.57-x86_64-with-glibc2.41; pytest 9.2.0.

| Run | Python | PASS tests | PASS subtests | FAIL / ERROR | SKIP | Exit | Wall seconds | Timeout |
|---|---|---:|---:|---:|---:|---:|---:|---|
| pure313 | 3.13.18 | 203 | 0 | 0 / 0 | 0 | 0 | 16.362 | False |
| pure310 | 3.10.22 | 203 | 0 | 0 / 0 | 0 | 0 | 20.175 | False |
| sp_regressions313 | 3.13.18 | 69 | 110 | 0 / 0 | 0 | 0 | 0.416 | False |
| sp_regressions310 | 3.10.22 | 69 | 110 | 0 / 0 | 0 | 0 | 0.466 | False |

Total final harness wall time: 38.073 seconds, within 300 seconds overall and 60 seconds per process. No timeout. SP has 69 collected test methods plus 110 passing subtests (179 JUnit records), not 179 independently collected methods. Pure has 203 collected tests: all 164 baseline test identifiers are retained plus 39 new cases. No required pure test is skipped.

Commands are retained verbatim in acceptance-results.json and JUnit/log pairs. Each pure command uses the appropriate existing interpreter, `-m pytest -q -p no:cacheprovider`, external 60-second watchdog, and these exact six paths:

```text
tests/test_offline_generation_job_contracts.py
tests/test_offline_generation_job_controller.py
tests/test_offline_generation_job_observer.py
tests/test_offline_generation_job_simulator.py
tests/test_offline_generation_job_faults.py
tests/test_offline_generation_job_no_effects.py
```

Each SP command uses `tests/test_topic_to_film.py tests/test_topic_to_film_v1_1.py`. The complete repository/media/model suite was NOT_RUN. Existing SP temporary-file tests and runner log/XML I/O are outside the guarded new core execution region; no actual core filesystem/network/SQLite/model/renderer operation occurred.

## Exact finding-to-test traceability

The complete parameterized case names, per-interpreter PASS results and the preservation of all baseline cases are in findings-map.json and acceptance-results.json. Function families below are navigable in the allowed test files.

| Finding / invariant | Tests |
|---|---|
| F-08B3-01: independent job statuses in four error APIs | test_F08B3_01_error_attribution_is_target_scoped (12 parameterized cases) |
| New admission cannot inherit old active effect | test_F08B3_01_new_admission_does_not_inherit_active_foreign_effect |
| Foreign proof cannot bind to current job | test_F08B3_01_foreign_receipt_cannot_bind_to_current_apply_proof (2 cases) |
| Missing mutation target cannot borrow known receipt | test_F08B3_01_missing_mutation_target_is_not_foreign_known_effect |
| Matching but unattested receipt is insufficient | test_F08B3_01_unattested_matching_receipt_does_not_establish_known |
| Qualified no-commit admission has no foreign effect | test_F08B3_01_admit_proven_not_committed_has_no_foreign_effect |
| F-08B3-02: COMMIT exception/ACK and diagnostic boundary matrix | test_F08B3_02_commit_exception_diagnostics_preserve_namespace_hold (17 cases) |
| Typed exception needs complete absence proof | test_F08B3_02_typed_exception_only_proven_absence_can_report_not_committed |
| Hold-port outage does not erase retained uncertainty | test_F08B3_02_failure_of_hold_port_does_not_clear_retained_uncertainty |
| Pending outage cannot permit submit/stale write/release | test_F08B3_02_pending_diagnostic_failure_cannot_enable_submit_or_stale_write |
| Both findings: forbidden effects and stale writes | test_F08B3_01_02_diagnostics_add_no_effects_or_stale_writes |

The 17-case boundary matrix includes raw/typed exceptions before/after COMMIT, successful ACK followed by unavailable/corrupt snapshot, OSError/RuntimeError/typed diagnostic outages, malformed snapshot shape, missing job bytes, contradictory HELD-slot index, missing receipt index, unavailable/bad/empty proof. It asserts HOLD/UNKNOWN, physical state consistency, zero additional submit/read calls, no extra admission before resolution, barrier retention across controller replacement, and correct resolution of the same M. A physically committed terminal slot release never authorizes a new job while its outcome is unresolved.

All original A01–A10 / R01–R16 / E01–E20 obligation tests remain in the full run, including active uniqueness/interleaving, lost ACK, restart, cancellation, one-attempt/read/resource caps, corrected V030 positive/old V030 negative, no native effects and stale-writer zero writes. Passing model tests do not independently close either finding.

## Development checks retained

The first updated full run had 163 PASS / 1 FAIL: the new in-flight latch blocked the old A10 test's reentrant invocation of the same controller. The test now models two independent facades sharing the actual store/owner, retaining the original winning/losing atomic-slot assertions. The first added controller/fault run had 58 PASS / 1 FAIL: a test expected a secondary malformed-snapshot code to replace the primary unknown COMMIT error. Its exact expectation was corrected to UNKNOWN_COMMIT_OUTCOME while retaining all HOLD, state and no-effect assertions. Later targeted runs: 70 PASS, then 74 PASS. Final full results above supersede these development counts; raw failed logs are retained. A standalone reproducer initially lacked the repository root in sys.path; the external harness import path was corrected before recording before/after evidence, without changing product code or tests.

## Qualification limits and STOP

No approved contract or G1–G6 expansion was required. The correction uses the same PURE schemas, ports, fake-only authority and fixed bounds. Restart guarantees remain those of the approved retained **test harness** operation registry and scripted ledger; the local latch alone is not a disk-backed or process-survival mechanism. Losing the qualified registry is not repaired by guessing (baseline R06 remains covered). No actual database crash/power-loss, native lock/clock/NTFS/Windows/reparse or TOCTOU qualification is claimed.

Windows: WINDOWS_NOT_RUN. SQLite, models, provider APIs, real render, real media/Asset Library/save, production storage and production permissions: NOT_RUN / NOT_AUTHORIZED. Main, CI and dependencies remain unchanged; no merge, release or next stage.

**READY_FOR_RE_REVIEW. STOP after publication.** Await independent ChatGPT review and owner decision. F-08B3-01/F-08B3-02 are implemented/verified within the qualified pure model, not self-declared independently ACCEPTED.

---

# Historical baseline report — reproduced from the exact pre-fix commit

The following body is retained for provenance only. Its branch/status/counts/checkpoint describe MVP-08B.3 before Fix 01 and are superseded by the current report above. Raw baseline report SHA-256: `31e41c833d688e61d2a28f25718d52acccb20a1bc781014a5c25efdf9db0527d`.

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
