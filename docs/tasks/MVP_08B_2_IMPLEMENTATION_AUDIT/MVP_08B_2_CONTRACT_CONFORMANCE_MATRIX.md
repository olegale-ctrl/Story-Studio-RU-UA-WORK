# Contract conformance matrix

**2026-11-19 · READ_ONLY_AUDIT / DOCS_ONLY · no implementation or production authorization.**

Original B.1 sources below are all pinned f0bce140451bf00a86f3939330e77ed63b2c98be under experimental_mvp/reports. Authority distinction is mandatory:most machinery is PROPOSAL,not a fully frozen runtime requirement. Implementation results refer to MVP08B.2 in verified scope;LAB analogues explicitly do not satisfy the full requirement.

|Contract requirement|Authority status|Source|Implementation evidence|Test evidence|Result|Gap|
|---|---|---|---|---|---|---|
|Immutable job request and target|PROPOSAL|JOB_CONTRACT / GenerationJob object|LAB immutable request bytes within run;no GenerationJob record|Bounded LAB replay/conflict test only|PARTIAL|No durable job identity/request schema/API|
|Idempotency scope project/purpose/request/batch|PROPOSAL|JOB_CONTRACT / Identity/idempotency rules|LAB requestID+actor+bytes,not project/batch scope|Same-run cached replay;no08B submit test|NOT_IMPLEMENTED|Persistent unique key/accept-reuse-conflict receipt|
|CAS/state revisions|PROPOSAL|STATE_MACHINE / W|Virtual S2 expected-head checks,not job state_revision transaction|Pure model selected tests|PARTIAL|No JobStore compare-and-swap of state+event+outbox|
|Fencing worker lease epoch|PROPOSAL|STATE_MACHINE / W;JOB_CONTRACT execution|Local threading.Lock/virtual parent epoch are distinct|No stale08B worker test|NOT_IMPLEMENTED|Durable owner/lease/fence and effect-boundary checks|
|Event/outbox before effect|PROPOSAL|STATE_MACHINE / Global transition protocol|Virtual S1 journal is not08B outbox|No outbox dispatch/crash test|NOT_IMPLEMENTED|Atomic event/revision/effect intent/receipt protocol|
|22states/38legal transitions|PROPOSAL|STATE_MACHINE / registry,SM01–38|LAB MOCK_* and S2 W0–9 are different protocols|No08B state graph replay|NOT_IMPLEMENTED|Versioned GenerationJob transition authority|
|Retry/recovery and uncertainty|PROPOSAL|RECOVERY_MATRIX;STATE_MACHINE / uncertainty rules|LAB unknown restart/pending deliberately does not resume real jobs|Bounded synthetic loss/crash/pending tests|PARTIAL|Durable reconciliation,known-no-submit proof,scoped retries|
|Result association/validation|PROPOSAL|RESULT_INGESTION / association,VAL,DFE|Library validates local assets;no job result/source receipt|No video/decode job test|NOT_IMPLEMENTED|Job/model/output identity plus qualified complete validation|
|Observer/status/--wait|PROPOSAL|JOB_CONTRACT execution;IMPLEMENTATION_PLAN|LAB LOOKUP is same-incarnation mock;SP wait BLOCKED|LAB lookup test,not08B observer|NOT_IMPLEMENTED|Authoritative revisioned observation/deadline/currentness|
|Publication/completion receipt|PROPOSAL|ASSET_HANDOFF / SG05,SG10,SG11|LAB MOCK_FINALIZED is virtual storage,Library links not saved JSON proof|No actual completion/publication fault test|NOT_IMPLEMENTED|Exact import/save/readback/settlement receipts|
|Exact input identity/hash domains|PROPOSAL plus existing narrow pure rules|JOB_CONTRACT / target,digest|Separate SP compact/SI,raw,S1MAC,PG prefix and proposed JCS-LOCAL-1|Source/domain inspection|PARTIAL|Approved cross-boundary mapping;no hash aliasing|
|Error semantics/unknown outcomes|PROPOSAL|JOB_CONTRACT JobError;RECOVERY_MATRIX|LAB typed errors are scoped mock vocabulary|Selected LAB negative tests|PARTIAL|Real persistent typed job errors/uncertainty evidence|
|No live/payments/unknown rights clearance|OWNER_APPROVED|MVP_08_OWNER_APPROVAL / D01–D05,D07|Current SP no-submit/no-grant;LAB synthetic-only|Source + bounded no-external-effect test|VERIFIED within audited paths|Does not verify real actor/licence or future executor|
|08A local Library reuse|APPROVED_WITH_LIMITATIONS|MVP_08A_OWNER_ACCEPTANCE / P1|Actual accepted catalog exists|Historical tests source only;not rerun here|PARTIAL|Import idempotency,stable project CAS,Tk/native/frame evidence open|
|Registered video jobs/general DAG|PROPOSAL specialized T2V/I2V|JOB_CONTRACT / request|No registry;LAB storage operations incompatible as direct replacement|No video-job submit test|NOT_IMPLEMENTED|Owner/API choice;generic DAG not mandatory or inferred|

Expected state names remain exactly22from baseline,not generic “created/accepted/interrupted”. No subset of LAB outcomes is re-labeled COMPLETED. No name-only function match is accepted as implementation proof. Outside inspected Git/local/PR/evidence scope remains NOT_VERIFIED,not a universal absence claim.
