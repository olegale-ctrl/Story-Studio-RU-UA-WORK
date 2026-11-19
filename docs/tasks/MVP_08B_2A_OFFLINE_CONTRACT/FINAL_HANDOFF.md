# Final handoff

**MVP-08B.2a · 2026-11-19 · DOCS_ONLY · PROPOSAL — NOT APPROVED FOR IMPLEMENTATION.**

**Final status: READY_FOR_INDEPENDENT_REVIEW**, for the documentation package only. Future execution remains blocked on independent review, applicable EC choices, exact fixture/base qualification and separate owner authorization. No technical choice is automatically approved.

## Identity and exact source boundary

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Branch: `docs/mvp-08b-2a-offline-execution-contract-freeze`.
Base commit: `04ea194e4d57c8a0550d7412281da58d4ba252c5`.
Base tree: `661e8307a36d56860aa67407ea8bc4d4f0a1c997`.
Observed main: `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Final containing commit/tree, exact full-index diff, file modes/Git blob SHA1/raw SHA256 and reproduction evidence are external in ACCEPTANCE_PACKET.json and final handoff message. A document cannot include its own containing commit hash without changing that hash.

Original sources read directly and pinned:

|Source|Exact commit|Tree|Authority/use|
|---|---|---|---|
|MVP-08B.1|`f0bce140451bf00a86f3939330e77ed63b2c98be`|`0b5238611cc84ef0a665f75b552757666935516e`|Original job/W/state/simulator/ingestion/open-decision/owner sources, not later paraphrases|
|MVP-08B.2|`04ea194e4d57c8a0550d7412281da58d4ba252c5`|`661e8307a36d56860aa67407ea8bc4d4f0a1c997`|Completed audit accepted with limitations by current owner message, not proof of a runtime|
|SP/1.1|`16d28ec0376c8c28f879c8aacb18d5378fea83a3`|`b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`|Diagnostic boundary and limited accepted code; not JobStore API or execution grant|

37 exact source snapshots with raw/Git hashes are external. No source code from those branches is merged into this docs branch. Source records of D01–D08,08A limitations and original OD01–OD08 remain unchanged.

## Owner authority versus proposals

APPROVED by the current task: B.2 accepted as a completed audit with limitations; prepare six new documents only. Existing OWNER_APPROVED D01–D08 and MVP-08A acceptance/limitations retain their original scope. No production permissions, live models, paid APIs, merge or implementation authorized.

EC-01–EC-10 remain OPEN; recommendations are PROPOSAL. They cover result/completion scope, acyclic identity/idempotency, store, lease/fencing/clock, outbox/lost ACK, observer, synthetic authority/resources/fixtures, typed errors, Library/save deferral and Route D mapping. Applicable choices must be explicitly resolved before their future operation is implemented. Original OD01–OD08 are not silently adopted or closed; deferral does not qualify the deferred component.

## Proposed minimum and material decisions

One fixed offline/synthetic video-anchor handler, one serial logical worker, persisted acceptance/CAS/events/outbox, a separate simulator acceptance ledger and an authoritative read-only observer. No universal DAG. The prefix ends at RESULT_AVAILABLE with pipeline_complete=false; it cannot fake COMPLETED, import/save or release. Acyclic core-request→batch→permit→acceptance hashes avoid circular binding and keep SP/PG/SI/raw/S1 domains distinct.

F01 exact bytes/hash/licence/source are not invented. Without a supplied reviewed fixture, positive future execution stays BLOCKED_EVIDENCE. Qualified clock/storage and explicit synthetic authority are additional implementation gates. Minimal Route D compatibility is the lifecycle/receipt boundary for a future separately approved mapping; whole-film render and anchor generation are not equivalent. No direct renderer bypass or SP CLI change proposed in initial implementation.

The future task has an exact22-path prospective allowlist; none of those runtime/test/fixture paths is created here. Future implementation base16d28ec... is a recommendation requiring explicit confirmation, not an automatic transfer or merge. Six documents below are the only repository changes.

## Exact new-document allowlist

All under `docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/`, mode100644:

- CONTRACT_FREEZE_PROPOSAL.md
- OWNER_DECISION_DOSSIER.md
- MINIMAL_EXECUTION_SCOPE.md
- ACCEPTANCE_ORACLES.md
- IMPLEMENTATION_TASK_PROPOSAL.md
- FINAL_HANDOFF.md

## Verification actually performed

Executed: `python /workspace/work/mvp08b2a-evidence/validate_documents.py` → exit0, DOC_CONSISTENCY_VERIFIED. The final detailed check count is in external document-consistency.json (source hashes/trees, six-file shape, 10 OPEN decisions, 66 NOT_RUN criteria, 22 uncreated future paths, original22states/38rules and static preimage/profile graph consistency). This is documentation inspection, not a runtime/state-machine/storage test. The static profile has27source rule rows and16structurally reachable states ignoring guards; deferred handoff/COMPLETED states have no path even in that over-approximation. Actual guard correctness remains NOT_RUN.

The first helper attempt exited1 because its parser also matched the source's two-column transition/oracle table. The helper was restricted to full transition rows and rerun; no original source changed. Failed-attempt evidence is preserved. Git diff/mode/allowlist and exact-base tree reconstruction checks are recorded separately in the external packet.

All 66 future acceptance oracles are **NOT_RUN**:24 pure,18 durable-local,8 Windows-specific,10 asset/save and6 future production/live criteria. No runtime, schema, GenerationJob, database, simulator, recovery or model test was executed in this DOCS_ONLY task. Existing B.2 historical18 pure tests and interrupted bulk run are not new passes here; no historical counts substituted. Windows/native/durability/Asset/save/live/production qualification remains NOT_RUN.

No main, CI, normative MVP-08B.1/G3, SP implementation, model, external provider, user project or production storage changed. No Dispatcher/JobStore/queue created. No actual SQLite schema, JSON job payload, permit, receipt or media fixture is generated by the documentation checks.

**STOP. Await independent ChatGPT review and a separate owner decision. No implementation, merge, release, production permission or automatic next stage.**
