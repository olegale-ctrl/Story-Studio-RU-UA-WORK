# Recovery plan — FROM_CONTRACT, not execution

**2026-11-19 · READ_ONLY_AUDIT / DOCS_ONLY · no implementation or production authorization.**

No qualified MVP08B.2 implementation recovered in verified scope. This is the required **FROM_CONTRACT** option. Related LAB/S2/Library code is preserved and catalogued,not automatically imported. Plan is PROPOSAL;current task forbids implementing it.

## Reuse and mismatch

- Keep unchanged D01–D08,accepted08A primitives and their limitations,exact SI/raw/PG/S1 domains. Existing S1/S2 and RAM LAB tests can supply isolated test patterns/reference checks without becoming a persistent job engine.
- Keep Library resolve/revision/import/attach/save APIs only within their actual accepted contracts. Autonomous import idempotency or saved-project CAS still require qualified receipts/API changes,not optimistic reuse.
- Keep SP1.1 validators for local diagnostics. No direct payload migration,registry aliasing or new queue there.
- LAB cannot be used unchanged as durable JobStore:RAM/run scope,finite storage-command whitelist,mock principals,MOCK_* outcomes,no leases/outbox/persistent jobs. S2 virtual durability cannot certify OS durability. Upstream thread pools and GUI queues must not become hidden secondary schedulers.
- Olderb27a cold-admission defect is already fixed in13ed;do not independently reimplement or restore old snapshot. Any proposed reuse must pin latest approved blob and its qualification scope.

## Minimal proposed completion sequence

R0: owner reviews this evidence and supplies any missing private/original .2 artifact or exact prior implementation authorization. If none exists,approve a **separate bounded offline-only** implementation task fromB.1 with selected unresolved details. Do not rewrite prior approvals or reopen zero-budget restrictions.

R1: reconcile narrow specialized GenerationJob API/state/error/idempotency/observer/receipt contracts against original B.1. Decide minimum required handlers;no universal DAG unless independently justified. Publish source/API/authority allowlist before coding under a separate task.

R2: implement one authoritative controller/store under that new authorization,with durable request+CAS revisions+fence+event/outbox before any effect. Keep simulator identity synthetic and$0;no actual provider. This step is **not executed here**.

R3: deterministic finite tests:immutable request,duplicate/conflicting submit,lost ACK,stale worker,exact22-state/38-edge guards,crash before/after committed outbox,unknown outcome held. Use fake/in-memory layers to test logic,then separately qualify actual local durable storage. Fake-store PASS is not durability.

R4: bounded ingestion/Library/save protocol after OD02/OD03 choices;original OD04 decoded-evidence policy and OD06 GUI-lifetime qualification are additional prerequisites before their corresponding effects;test ambiguous import,changed input/project/hash/rights,crash across file/DB/editor/save/receipt,no stale overwrite or regeneration after attachment failure. Keep unresolved outcomes quarantined/reconciliation-required.

R5: only after API/source/tests accepted,consider separate thin SP bridge for the narrowest useful route/operation. No direct build bypass;accepted IDs≠completion;--wait authoritative only. Re-run SP legacy/new diagnostic vectors without changing semantics.

R6: separate platform/storage/native/decoder/runtime/live-provider/production qualification if ever authorized. Windows requires real environment;no synthetic grant or pure model can substitute. Stop before production/release until all independent permissions and verifier gates exist.

Testing order follows78original B.1 oracles and26recovery scenarios as **specifications**,not current successes. Use explicit time/resource limits;the audit's expensive historical LAB bulk-test interruption is not a reason to weaken receipts/identity. Risks of duplicate development:ignoring65existing LAB carriers,copying old blob,duplicating queues,confusing catalog with JobStore,renaming mock outcomes,discarding unknown acceptance or overbuilding a DAG. Preserve source provenance and distinct domains to avoid these errors.
