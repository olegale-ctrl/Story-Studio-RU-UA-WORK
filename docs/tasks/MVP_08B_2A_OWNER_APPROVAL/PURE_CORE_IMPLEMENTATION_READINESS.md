# Pure core implementation readiness

Mode: **DOCS_ONLY / OWNER_APPROVAL**. Recorded date: 2026-11-20 (Europe/Kiev). This records a decision supplied by the project owner in the current conversation; no identity/signature infrastructure is claimed. **Implementation is NOT authorized.** No code, models, SQLite, provider API, CI, main, merge, release, production storage or production permissions.

## Readiness decision

**READY_FOR_IMPLEMENTATION_AUTHORIZATION**, for the bounded PURE contract only, using the existing closed rules plus the mechanically derived vector erratum. **Not IMPLEMENTATION_AUTHORIZED.** No unresolved architectural choice is silently assigned to Codex. The example inconsistency found during this task is explicitly preserved and corrected by derivation in VECTOR_ERRATUM_AND_CHECKS.md; no schema extension is made.

Independent confirmation of exact bytes/shapes and the erratum remains the approved G2 entry condition. Future implementation authorization must explicitly adopt the pinned task and its evidence/limits. If that review rejects the erratum, or another contradiction is found, STOP with BLOCKED_CONTRACT rather than implementing a workaround. Unexecuted future conformance tests are not existing PASS results.

## Requirements and future tests

| Requirement | Contract obligation | Future oracle / acceptance evidence |
|---|---|---|
| G1 prefix | DRAFT -> AWAITING_APPROVAL -> APPROVED -> QUEUED -> SUBMITTING -> RUNNING -> fake RESULT_AVAILABLE; guarded uncertainty/cancel paths only | A01–A10, R01–R16; no COMPLETED/import/save claims |
| G2 closed values | 25 hashable types plus nonhashable boundary types; exact JCS-LOCAL-1 expression, not RFC JCS | E01–E06; all 36 historical hashes, old V030 negative, corrected vector positive |
| G2 identity | Full immutable key and separate HELD(store,project,purpose); terminal historical receipt replay never reacquires | A01–A10, E13–E15 |
| G3 fake transaction | Stable mutation identity and complete atomic write set before fake effect; unknown is namespace hold | R01–R06, R15; corrupt/unavailable never NOT_FOUND/rollback |
| G4 fencing | Current fake owner/current CAS applies unchanged old receipts; no stale callback writes or TTL theft | R07–R11, R16, E07–E08 |
| G4 restart | Harness-preserved unresolved mutation and ledger, same clock epoch or hold; no real process/disk proof | R02–R06, R10–R12 |
| G5 reads | Initial+two retries=three committed reservations; duplicate cursor/restart cannot reset | R12–R13, E09–E12 |
| G5 errors | Exact code/message/action/precedence; external_effect spelling; response-only rejection | E17, E20 and corrected V030 mapping |
| G5 finite model | 16 jobs/one worker/one batch entry/one attempt/three reads/128 events/32 outbox/1MiB/64 script events/10000 ticks | E19; boundary and overflow inputs, no effects after exhaustion |
| G6 observe | Single-shot consistent snapshot with explicit barrier; no wait | Observer tests; P019 NOT_RUN |
| No effects | No product filesystem, DB, network, models, subprocess/render, Library/save or real clock access | E16/E18, no_effects tests; test-loader ordinary imports are not product I/O permission |
| SP/1.1 | Detached metadata/ports only; do not wire Route D or alter diagnostic contract | Read-only SP baseline and targeted regressions after separate authorization |

Every future runtime oracle above is **NOT_RUN** in this task. A01–A10, R01–R16 and E01–E20 are 46 named contract obligations, not a claimed pytest count; parameterization may produce a different actual test count. Report real counts/skips/exit codes, failures and timeouts after implementation. In the historical crosswalk P003/P004/P012 use B.1 identity semantics and T005 for active intent; no T001/T004 substitution. P011 distinguishes unavailable handler from unqualified profile.

## Exact SP/1.1 path compatibility

Implementation baseline is `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`. Read Git objects, not a later working-tree reconstruction. SP pytest.ini selects tests/; the six proposed test files fit that collection root. experimental_mvp/ and tests/ are existing tree directories, and docs/tasks/ exists. The new offline_execution/ package will contain its own __init__.py. Python import/runtime compatibility has not been executed or inferred from this static result.

| Approved proposed path | Exact SP state | Static conclusion |
|---|---|---|
| `experimental_mvp/offline_execution/__init__.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `experimental_mvp/offline_execution/contracts.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `experimental_mvp/offline_execution/policy.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `experimental_mvp/offline_execution/controller.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `experimental_mvp/offline_execution/observer.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `experimental_mvp/offline_execution/simulator.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `tests/test_offline_generation_job_contracts.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `tests/test_offline_generation_job_controller.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `tests/test_offline_generation_job_observer.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `tests/test_offline_generation_job_simulator.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `tests/test_offline_generation_job_faults.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `tests/test_offline_generation_job_no_effects.py` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |
| `docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md` | ABSENT; no casefold/file-ancestor collision | ADDITIVE; historical allowlist member |

13/13 are compatible as new tracked files. This does not mean the implementation exists, that all SP tests pass, or that namespace/package behavior is qualified on Windows. All other historical 22-path entries are deferred, especially job_store.py, CLI and real fixture files. No pytest.ini/workflow/source changes are needed or allowed by this scope.

## Qualification boundaries and blockers

| Layer | Current finding | Gate |
|---|---|---|
| Contract recording | OWNER_APPROVED_CONTRACT_ONLY G1–G6, bounded scope | Complete recording; no execution permission |
| Historical V030 | Invalid INSPECT example; deterministic RELOAD erratum supplied | Independent confirmation before implementation; no enum widening |
| Pure implementation | Does not exist under this task | Separate explicit owner authorization and G2 review |
| Durable local storage | Deferred, not a dependency of pure fake tests | Separate store/commit/fsync/restore qualification |
| Windows | WINDOWS_NOT_RUN; no native lock/reparse/clock claims | Separate platform qualification |
| Asset ingestion/save | Deferred; metadata result only | Actual bytes/path/TOCTOU/decoder/rights and save checks later |
| SP Route D execution | Deferred; only contract compatibility here | Separate integration permission |
| Live/production | Not authorized, $0 | Explicit future owner permission; no automatic promotion |

The first fake RESULT_AVAILABLE result must retain its active slot and pipeline_complete=false. COMPLETED is recognized vocabulary for seeded historical replay/terminal guard tests only, not a successful prefix exit. Test-local fixture data may model historical terminal records only with their required coherent proof references; they are not implementation of the downstream Library/save pipeline.
