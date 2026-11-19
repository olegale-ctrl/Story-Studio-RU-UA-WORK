# MVP08B.1 contract baseline and authority classification

**2026-11-19 · READ_ONLY_AUDIT / DOCS_ONLY · no implementation or production authorization.**

Source of truth is **f0bce140451bf00a86f3939330e77ed63b2c98be**, tree0b5238611cc84ef0a665f75b552757666935516e. Documents under experimental_mvp/reports are pinned byte-for-byte in external sources/baseline/ and source-manifest.json. Later SP descriptions are not substituted. This document classifies original requirements for audit;it is not a new normative approval.

|Requirement / decision|Authority status|Exact original source atf0bce / section|Audit interpretation|
|---|---|---|---|
|D01target Wan/Runway/MiniMax;one exact initial adapter/model;no live calls|OWNER_APPROVED|MVP_08_OWNER_APPROVAL.md / Approved decisions,D01|Direction,not implemented adapter or live authorization|
|D02zero budget;future10USD/month requires explicit approval;no payments/subscriptions|OWNER_APPROVED|same / D02|Cannot infer authority from free marketing or a queue flag|
|D03written provider permission+qualified browser integration;none for08A|OWNER_APPROVED|same / D03|No browser automation activated|
|D04quota exhaustion pauses;no automatic paid transition|OWNER_APPROVED|same / D04|Existing permitted fallback only within scope|
|D05document intended-use/source/voice/music/territory/time/attribution/watermark rights|OWNER_APPROVED|same / D05|Unknown rights do not clear usage|
|D06rejection assumption30%,sensitivity10–50%pending measurements|OWNER_APPROVED|same / D06|Planning assumption,not measured performance|
|D07bounded batch/budget;renew material provider/model/region/spend/data-transfer changes|OWNER_APPROVED|same / D07|Not unlimited unattended grants|
|D08future adapter,persistent queue,spend controls,secure retrieve/validate,Library,fault tests|OWNER_APPROVED|same / D08|Future scope;implementation/live qualification have separate gates|
|MVP08A acceptance and retained P1 issues|APPROVED_WITH_LIMITATIONS|MVP_08A_OWNER_ACCEPTANCE.md / APPROVED;EXISTING accepted limitations|Existing Library accepted;frame-count,Tk lifecycle,JSON receipt limitations not closed|
|MVP08B.1 documentation preparation authority|OWNER_APPROVED|same / Authorization boundary|CONTRACT_PREPARATION_ONLY,not blanket runtime permission|
|GenerationJob required identity,target,request,authorization,execution,result,error groups|PROPOSAL|MVP_08B_1_JOB_CONTRACT.md / GenerationJob object;Related contracts|Immutable accepted request and explicit scoped receipts;no object added to runtime|
|Idempotency projectUUID+purpose+requestdigest+batch scope|PROPOSAL|same / Identity/idempotency rules|Same SHA alone never asset/job identity|
|JCS-LOCAL-1 digest uses existing encoded default separators|PROPOSAL|same / Schema conventions|Not RFC8785,not SP compact SI hash or PG prefix binding|
|22states/38transitions + W CAS/event/outbox/fence before effects|PROPOSAL|MVP_08B_1_STATE_MACHINE.md / Global transition protocol,State registry,SM01–SM38|Approved documentary preparation does not approve every transition for implementation|
|VAL-v1 association/limits and DFE-v1 decoded evidence|PROPOSAL|MVP_08B_1_RESULT_INGESTION.md / Trusted association;Validation manifest;P1-01|Reported nb_frames is not decoded-count qualification|
|SG01–SG11 ingestion/attach/save saga|PROPOSAL|MVP_08B_1_ASSET_HANDOFF.md / Saga checkpoints;import_file mapping;P1-03|COMPLETED requires exact import+saved JSON receipt,not GUI/file presence|
|Simulator18scenarios and zero-charge ledger|PROPOSAL|MVP_08B_1_OFFLINE_SIMULATOR.md|Specifications,not an implemented simulator|
|78acceptance oracles and26recovery scenarios|PROPOSAL|MVP_08B_1_TEST_ORACLES.md;MVP_08B_1_RECOVERY_MATRIX.md|All original runtime oracles NOT_RUN,not counted as tests in this audit|
|OD01exact live profile;OD02import receipt;OD03project/save identity;OD04media count;OD05authority;OD06Tk;OD07durability/resources;OD08retention|OPEN_DECISION|MVP_08B_1_OPEN_DECISIONS.md / OD01–OD08|Recommendations explicitly NOT_APPROVED;none settled here|
|Runtime Dispatcher/JobStore/simulator/ingestion|NOT_IMPLEMENTED|MVP_08B_1_ACCEPTANCE.md / Evidence labels,STOP;MVP_08B_1_IMPLEMENTATION_PLAN.md|Original source explicitly excludes runtime implementation;later .2 authorization alone would not prove execution|

Exact future states: DRAFT,AWAITING_APPROVAL,APPROVED,QUEUED,SUBMITTING,SUBMISSION_UNCERTAIN,RUNNING,RESULT_AVAILABLE,DOWNLOADING,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING,COMPLETED,PAUSED_QUOTA,PAUSED_BUDGET,PAUSED_RIGHTS,STALE_TARGET,RETRY_WAIT,CANCEL_REQUESTED,CANCELLED,FAILED,NEEDS_RECONCILIATION. Generic created/accepted/interrupted names in audit task are search hints,not replacement enums. W0–W9/FINALIZED/ABORTED and LAB MOCK_* belong to separate S1/S2/LAB protocols.

Additional authority is separate: portable LAB owner record at13ed35d docs/tasks/E01_3_9_4_S3_2A_OWNER_DECISION.md permits pure RAM LAB on Linux,not native protected storage or08B jobs. SP01b task-supplied ACCEPTED_WITH_LIMITATIONS and SP-OD10/A record at16d28ec permit limited diagnostics/corrections,not JobStore or production. No unseen owner implementation decision is declared revoked/nonexistent;its exact source was not located in verified evidence. Current audit instruction independently prohibits implementing it now.
