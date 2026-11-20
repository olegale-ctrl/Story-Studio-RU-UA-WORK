# MVP-08B.2a-FIX-01 — G1–G6 decision handoff and minimal future scope

Status: **PROPOSAL / DOCS_ONLY — OWNER REVIEW REQUIRED**. Date: 2026-11-20.

Project status remains **BLOCKED_CONTRACT**. This document proposes resolution of accepted findings; it does not approve EC-01–EC-10, G1–G6, implementation, real APIs, spending, storage, CI, main, merge, release or production permissions.

Source precedence: owner instruction in this conversation accepting the limited audit and F01–F05; exact independent review `3744eb5584e72e338dc51fa3a6fe7aed4882651b`; original freeze `c5cd33023880fd6726b74f5631eb766cc0959892`; original B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`; B.2 `04ea194e4d57c8a0550d7412281da58d4ba252c5`; SP/1.1 `16d28ec0376c8c28f879c8aacb18d5378fea83a3`. Historical documents remain unchanged. New PURE records below are proposals, not replacements for approved external contracts.

## Decisions remain open

The owner accepted preparation and independent remarks, not EC01–EC10 or the following gates. Each entry is **PROPOSAL / OWNER_DECISION_PENDING**. No signature or timestamp in this package represents owner approval. D01–D08 and MVP-08A restrictions remain unchanged: $0; no live provider calls, browser automation, subscriptions, paid requests, production rights/storage or release. OD01–OD08 are not adopted implicitly.

| Gate from review | Concrete proposal / alternative | Recommendation and acceptance condition |
|---|---|---|
| G1 / EC01,09,10 | One synthetic operation through fake RESULT_AVAILABLE; alternative defer all implementation | Narrow pure prefix only; no real fixture/import/save/Route D execution. Owner must explicitly choose it. |
| G2 / EC02 | Adopt exact PURE typed registry, historical full key plus independent active slot; alternative request different projection/schema | Adopt only after independent byte/shape review and explicit decision; A/E oracles must then pass. |
| G3 / EC03,05 | FakeStore and scripted ledger with three commit outcomes; alternative qualify durable store first | Pure only, no SQLite/native locks. R01–R06 must pass; no durability claim. |
| G4 / EC04 | Virtual ownership/fencing and conservative epoch hold; alternative defer all recovery | Require R07–R16 and stale-writer no-write proof before any later durable stage. |
| G5 / EC07,08 | Synthetic metadata, finite errors/read caps; alternative require real media and separate qualification now | Metadata only; first stage must not depend on absent F01 MP4. E01–E20 apply. |
| G6 / EC06 | Single-shot observe; future exact base/tree/allowlist and limits frozen separately; alternative separately specify wait | Observe only, no wait, P019 NOT_RUN. No implementation until owner approves a complete task. |

These alternatives do not reopen Wan-first future adapter planning or budget decisions: they concern only the unapproved offline execution contract.

## F06/F07 scope clarification

The B.1 historical stages remain `.2 Offline Core` and `.3 Local Result Pipeline`. The proposed future task name `MVP-08B.3 — Pure Offline GenerationJob Core` is a new owner's task label, **not** evidence that either historical stage is implemented or that its original full scope was approved. No renamed completion claim is made.

First pure scope may define typed values, ports, controller, single-shot observer, scripted fake simulator and test-local FakeStore/FakeClock/ledger. No real storage or provider adapter implementation. Fakes can only validate consumer behavior against scripted facts; they do not qualify a producer, signer, clock, fixture or filesystem. A real MP4 F01 and the old full 22-file task are not prerequisites for pure value tests.

## Proposed future file allowlist — NOT CREATED

Subject to G6, use a fresh implementation branch from `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`, unless owner explicitly chooses another verified base. Never silently substitute latest main. The following 13 paths are a strict subset of the original freeze implementation-plan allowlist; all omitted paths are deferred:

- `experimental_mvp/offline_execution/__init__.py`
- `experimental_mvp/offline_execution/contracts.py`
- `experimental_mvp/offline_execution/policy.py`
- `experimental_mvp/offline_execution/controller.py`
- `experimental_mvp/offline_execution/observer.py`
- `experimental_mvp/offline_execution/simulator.py`
- `tests/test_offline_generation_job_contracts.py`
- `tests/test_offline_generation_job_controller.py`
- `tests/test_offline_generation_job_observer.py`
- `tests/test_offline_generation_job_simulator.py`
- `tests/test_offline_generation_job_faults.py`
- `tests/test_offline_generation_job_no_effects.py`
- `docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md`

This proposes narrowing the historical 22-file plan to these 13 paths; it does not approve that narrowing. Test fakes stay inside these tests. No `job_store.py`, SQLite, CLI, FFmpeg, asset mutation or MP4 fixture. Interface proposals: canonical_bytes/hash/validate as pure functions; admit/transition/resolve_commit on a fake transaction port; claim/renew guarded by fake ownership; lookup/poll using persisted reservation model; observe once with explicit barrier. Interface spellings are not an approved ABI.

Pure limits: at most 16 jobs, one worker, one-entry batch, one generation attempt, three total reads/checkpoint, 128 events, 32 outbox records, 1 MiB request envelope, 64 scripted events and 10000 virtual ticks. No real sleeps or elapsed-time assumptions. Future test command wall timeout proposed 60 seconds per process and 300 seconds total, returning explicit TIMEOUT; no model launch. Counters/overflow fail closed before effects.

## Qualification separation / STOP

1. Pure values and scripted port tests: future G1–G6 authorization required; NOT_RUN now.
2. Durable local store: explicit later design/authorization and real commit/crash/restore/CAS/outbox qualification; NOT_RUN.
3. Windows: native lock/reparse/symlink/clock/NTFS and no-admin restart qualification; WINDOWS_NOT_RUN.
4. Asset ingestion/save: secure bytes/path/TOCTOU, actual media decode/rights and save receipt, independent permission; NOT_RUN.
5. Live provider/production: separate explicit qualification, budget, rights/security and permissions; STOP.

STOP on any unclear field/preimage/transition, missing exact base, out-of-allowlist path, unresolved commit, missing fake evidence, attempted filesystem/network/media/database operation, unapproved wait, or scope expansion. Stop after independent review and owner decisions; no automatic implementation.
