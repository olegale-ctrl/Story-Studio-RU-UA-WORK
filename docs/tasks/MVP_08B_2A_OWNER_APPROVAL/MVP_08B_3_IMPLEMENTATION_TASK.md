# MVP-08B.3 — Pure Offline GenerationJob Core

Mode: **DOCS_ONLY / OWNER_APPROVAL**. Recorded date: 2026-11-20 (Europe/Kiev). This records a decision supplied by the project owner in the current conversation; no identity/signature infrastructure is claimed. **Implementation is NOT authorized.** No code, models, SQLite, provider API, CI, main, merge, release, production storage or production permissions.

## Activation status

**PREPARED TASK / NOT AUTHORIZED TO EXECUTE**. Owner G1–G6 contract approval does not activate this task. Entry requires separate explicit implementation authorization, independent confirmation of FIX-01 byte/shape contracts and VECTOR_ERRATUM_AND_CHECKS.md, and an exact pinned revision of this task. Until then: STOP.

## Exact implementation baseline and branch

Use a new isolated implementation worktree at SP/1.1 commit `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`. Proposed branch: `feat/mvp-08b-3-pure-offline-generation-job-core`; if already occupied, inspect and STOP rather than reset/overwrite. Do not substitute main, the docs branch or a later implementation branch.

Contract reference baseline is FIX-01 `79feb212650df435274998dfb40aed01656a2044` / tree `35812c305495012c1648b14de4c4a04cea6bdf9e`, together with this owner-recording commit and its derived V030 erratum. Its exact final SHA/tree is in the publication manifest/final handoff; the authorization must pin them explicitly. Read those documents via pinned Git objects if absent in SP/1.1; do not copy historical contract files into the implementation branch outside the allowlist. Hash source files before execution.

## Exact 13-path allowlist

Only the following new files may be tracked by the implementation diff; no existing file edits/deletions/renames, workflow/dependency/configuration changes, or extra helper modules. Do not widen the list to satisfy an import or missing fixture.

| Path | Required responsibility |
|---|---|
| `experimental_mvp/offline_execution/__init__.py` | Minimal side-effect-free package exports |
| `experimental_mvp/offline_execution/contracts.py` | Closed types, validation and exact canonical bytes/hash; no I/O |
| `experimental_mvp/offline_execution/policy.py` | Fixed fake authority/profile/limit checks and clock/ownership ports |
| `experimental_mvp/offline_execution/controller.py` | Admission, active slot, state guards, transaction/fence/recovery orchestration through fake ports |
| `experimental_mvp/offline_execution/observer.py` | Single-shot authoritative observe with explicit barriers; no wait |
| `experimental_mvp/offline_execution/simulator.py` | One scripted metadata-only simulator interface; no native provider |
| `tests/test_offline_generation_job_contracts.py` | Schema/hash/key/permit/error vector tests |
| `tests/test_offline_generation_job_controller.py` | Guarded admission/state/fence/cancel tests with test-local fakes |
| `tests/test_offline_generation_job_observer.py` | One-shot observer/scope/unavailable/hold tests |
| `tests/test_offline_generation_job_simulator.py` | Scripted ledger/acceptance/result/lost ACK tests |
| `tests/test_offline_generation_job_faults.py` | Finite commit/restart/cancel/read reservation fault matrix |
| `tests/test_offline_generation_job_no_effects.py` | Forbidden effect and finite limit guards |
| `docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md` | Actual implementation result and validation/limitations/handoff report |

Test-local FakeStore/FakeClock/OwnerLock/ledger are defined inside the listed test modules and injected through pure ports. No disk-backed JobStore or persistent dispatcher is implemented. Fake retained snapshots across simulated controller restart are harness data, not durable process storage. The simulator module must not construct a real Wan client or use a network-shaped backdoor. Production requests are invalid, not “disabled by default.”

## Required behavior and invariants

Implement the existing PURE profile only: OFFLINE_SIMULATOR_V1 / SIM_WAN_PROFILE_V1 / version 1 / LOCAL_ONLY / T2V / synthetic.video_anchor; spending zero. Schema recognition of I2V is not permission to run it. Use exact closed records, typed reference closure, canonical hashing and current error rules. Old V030 is negative; OA-V030-CORRECTED-1 is the conforming positive example, with exact digest in the erratum.

Admission, receipt history and independent active slot must be atomic in the fake transaction model. Same exact accepted command returns original receipt, no writes/effect/permission refresh. Old supplied key plus changed request conflicts; correctly recomputed new key with old permit is scope denial; a valid new key on HELD purpose is active conflict. RESULT_AVAILABLE retains slot. Preserve the original source state-machine guards, event ordering and cancellation via SM31.

Persisted-in-fake-state outbox intent precedes any scripted effect. Unknown commit is a namespace HOLD; same stable mutation is resolved against complete matching or complete-absence fake evidence. Corrupt/unavailable is never absence. New owner applies old immutable evidence under a new current fenced CAS; receipt never supplies write authority. Current owner-lock and clock qualification are required; TTL is not owner death. Claim/renew/reclaim cannot clear cancellation, transfer stale authority or retokenize generation identity.

Reserve each read before call; two retries means three total calls per checkpoint; interrupted reservations count. No reset on restart/duplicate/stale/same cursor. All failures use the exact single code/message/action and no stale job/event/error writes. Observe is one shot. No wait or real-clock retry loop. First happy-path exit is fake RESULT_AVAILABLE with pipeline_complete=false; no MP4, Library, attachment, save, production or COMPLETED claim.

## Finite limits and validation plan

Fixed upper bounds: 16 jobs, one worker, one-entry batch, one attempt, three calls/checkpoint, 128 events, 32 outbox, 1048576 request bytes, 64 scripted events, 10000 virtual ticks. Check overflow/caps before effects. Positive fake lease interval L<=10000 is fixed by the fixture; clock epoch mismatch/rollback holds. No tuning these bounds silently to make tests pass.

After separate authorization, run the six allowlisted test modules explicitly with the available Python interpreter and pytest (`python -m pytest -q -p no:cacheprovider` followed by those six exact paths), with external watchdog <=60 seconds per process and <=300 seconds total for the pure acceptance run. Record actual interpreter/pytest/OS versions, collected/passed/failed/skipped counts and exit codes; TIMEOUT is a failure/limit result. Do not install dependencies or change configuration without scope resolution if pytest is unavailable. Standard test collection/import/report tooling may access its own code files; product core and fake execution have zero filesystem/network/SQLite/subprocess/media effects. Test harness timeout control is external, not a product subprocess capability.

Cover all A01–A10, R01–R16, E01–E20 obligations and the corrected historical P crosswalk. Separately run applicable existing SP diagnostic/Topic-to-Film regressions under their existing environment if available; record failures or NOT_RUN rather than implying compatibility. No full FFmpeg/model/native/SQLite suite is required to prove the pure subset, and no such suite may be launched automatically under this task. Do not claim Windows PASS from Linux; WINDOWS_NOT_RUN stays explicit until qualified separately.

## Acceptance and delivery

Acceptance requires: exact base/tree; only 13 allowlisted additions; no forbidden effect; immutable identities/receipts and active uniqueness proven; complete commit uncertainty/restart/cancel/read-boundary tests; exact schema/vector/error behavior; all required pure checks PASS with real evidence; known platform/durable/media/live limitations reported. Failure/skipped required pure oracle blocks acceptance. Runtime conformance counts must be actual, not the 46 requirement labels.

Populate the allowlisted RESULT.md with branch/base/commit/tree, exact diff/file SHAs, actual commands/versions/counts/skips/exits/timeouts, defects/fixes, NOT_RUN qualifications and STOP. Publish an isolated branch for independent review only; no main modification, CI change, merge, release or subsequent stage. Commit self-hashes belong in the external manifest rather than recursive self-embedding.

## STOP conditions

STOP on inconsistent canonical/schema/error rules; rejection of the derived erratum; missing exact source revision; unresolved UNKNOWN_COMMIT_OUTCOME; missing fake authority/ownership proof; need for an extra tracked file; attempted native lock/storage/SQLite/filesystem/provider/model/FFmpeg/Library/save/network/paid operation; waiting requirement; new provider/profile/model/region; or need to reinterpret evidence as rights/production permission. Report BLOCKED_CONTRACT/ENVIRONMENT with the exact cause. Do not patch a contract in implementation or broaden this approved profile.

**STOP after this documentation publication. No implementation work is authorized by this task text itself.**
