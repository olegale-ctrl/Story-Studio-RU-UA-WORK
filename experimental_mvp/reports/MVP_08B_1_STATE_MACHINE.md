**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. EXISTING behavior is source-inspected at base1ff403e; APPROVED decisions are the unchanged D01–D08 and [new owner acceptance](MVP_08A_OWNER_ACCEPTANCE.md). Everything newly specified here is PROPOSED / NOT_IMPLEMENTED / NOT_RUN. OPEN gates are in [decision register](MVP_08B_1_OPEN_DECISIONS.md). No runtime or live API tests performed; WINDOWS_NOT_RUN.

# GenerationJob state machine v1

## Global transition protocol — applies to every row

Only listed pairs are legal; comma-separated source/destination sets are explicit finite shorthand, not wildcard permission. For SM22/SM26/SM34 destination must equal the proven persisted continuation checkpoint. C=controller holding current durable lease epoch; H=qualified human/batch authority; A=associated adapter observation verified by C (adapter never writes job state); G=GUI-thread/session broker; Q=qualified reconciliation evidence, human if no qualified deterministic proof. Every authority checks current authorization/rights/cancellation before side effect; this documentation grants none.

**W applies to every transition:** one JobStore transaction CAS expected state_revision+lease epoch, append immutable event ID/hash/reason/evidence and new state_revision, update checkpoint/reservation/effect outbox as specified, commit before external/local resource side effect. Side-effect result is a separate receipt+transition; retries replay same event/effect token and cannot manufacture acceptance. Crash before W commit leaves prior state; crash after W consults outbox/receipt and corresponding recovery row. No outbox non-dispatch proof after crash means submission uncertainty, not safe resend. Errors are durable typed JobError, never success; W failure means no new side effect.

Job request draft snapshots may be versioned in DRAFT/AWAITING_APPROVAL; request change invalidates the old approval request. The approved immutable snapshot is frozen by SM02. After approval a material generation change creates a new linked job, not edits to the sent request. Terminal states COMPLETED/CANCELLED/FAILED cannot be reused; duplicate observations may append read-only incident evidence but don't reopen work. COMPLETED means a verified saved JSON version, not just an asset/file/link/GUI acknowledgement. Later user changes create divergence observations, no automatic restoration.

Recoverable states: all other states. STALE_TARGET/PAUSED_RIGHTS/NEEDS_RECONCILIATION require explicit evidence/authority; SUBMISSION_UNCERTAIN forbids new submit. PAUSED_QUOTA/BUDGET are pre-submit/known-no-acceptance holds, not hidden states of a still-running chargeable request. CANCEL_REQUESTED is not CANCELLED. A cancelled/failed job may retain assets under permitted retention; terminal doesn't mean physically deleted. Idle pauses don't extend approval validity.

Fenced progress/receipt events may update a phase checkpoint without changing the enum; they still use CAS/event identity and cannot trigger an additional generation or bypass an edge guard. They are not implicit self-loop submission transitions.

## State registry

`DRAFT` | `AWAITING_APPROVAL` | `APPROVED` | `QUEUED` | `SUBMITTING` | `SUBMISSION_UNCERTAIN` | `RUNNING` | `RESULT_AVAILABLE` | `DOWNLOADING` | `VALIDATING` | `ASSET_COMMITTED` | `ATTACH_PENDING` | `COMPLETED` | `PAUSED_QUOTA` | `PAUSED_BUDGET` | `PAUSED_RIGHTS` | `STALE_TARGET` | `RETRY_WAIT` | `CANCEL_REQUESTED` | `CANCELLED` | `FAILED` | `NEEDS_RECONCILIATION`

|ID|From|To|Preconditions|Authority|Durable addition (plus W)|Side effect after commit|Idempotency, crash recovery and error behavior|
|---|---|---|---|---|---|---|---|
|SM01|DRAFT|AWAITING_APPROVAL|Complete frozen draft revision; local schema valid|C|request hash + approval request|Notify approval UI only|Replay same request ID; invalid fields remainDRAFT with error|
|SM02|AWAITING_APPROVAL|APPROVED|Verified bounded permit exact draft hash; rights/input/region/mode scope valid|H+C|approval snapshot,permit revision/expiry|No submit|Crash reverify permit; expired/mismatched approval cannot approve|
|SM03|AWAITING_APPROVAL|DRAFT|Explicit draft edit/rejection; no approved/submitted request|H+C|new draft revision or rejection reason|No external effect|Retain old draft; old approval reply rejected by revision|
|SM04|APPROVED|QUEUED|Current permit and$0eligible simulator; no duplicate active job|C|unique queue entry + scheduling policy|Queue only|Replay no extra queue entry; revoked permit→pause/approval|
|SM05|QUEUED|SUBMITTING|Exclusive live lease/fence; request/permit/current rights valid; known liability fits budget/quota|C|attempt + reserve + submit intent/outbox before effect|One qualified simulator submit after committed intent|Crash before send still uncertain unless outbox non-dispatch provable; stale fence cannot send|
|SM06|SUBMITTING|RUNNING|Associated ACCEPTED receipt with exact job/model/attempt|A+C|providerjobID,receipt hash,poll cursor|Safe bounded status poll may be scheduled|Duplicate same receipt no effect; conflicting ID→reconcile|
|SM07|SUBMITTING|SUBMISSION_UNCERTAIN|Timeout/crash/lost or malformed reply; acceptance not disproved|C|unknown effect/billing,held reserve,last intent|No new submit|Recover as uncertain even without remote ID; preserve evidence|
|SM08|SUBMISSION_UNCERTAIN|NEEDS_RECONCILIATION|No qualified acceptance/non-acceptance proof|C|reconciliation case and blocked effects|Qualified read-only lookup or human notice|Never another potentially billable submit; missing evidence remains held|
|SM09|NEEDS_RECONCILIATION|RUNNING|Qualified lookup proves same attempt accepted and identified|Q+C|receipt/job association + retained reserve|Resume safe polling same remote job|CAS receipt replay; different job/model remains reconcile|
|SM10|NEEDS_RECONCILIATION|RETRY_WAIT|Known no-acceptance/settled prior attempt, retry eligible, permit/limits still valid|Q+C|non-acceptance/billing proof + permitted retry checkpoint|No submit yet|Unknown charge is insufficient; held until proof/new authority, not just retry click|
|SM11|RUNNING|RESULT_AVAILABLE|Qualified complete associated result receipt; output policy satisfied|A+C|artifact list/identity/expiry/model,selected output policy|No download before receipt commit|Duplicate no second result/import; contradictory terminal status→reconcile|
|SM12|RESULT_AVAILABLE|DOWNLOADING|Known immutable artifact identity and permitted retention/transfer; valid limits|C|download intent + controlled staging ref|Read simulator local fixture; future qualified transfer only|Resume/refetch same artifact only; unknown URL/identity→hold|
|SM13|DOWNLOADING|VALIDATING|Complete bounded bytes + matching hash/length and stable receipt|C|BYTES_STAGED marker,byte/hash receipt|Local decoder validation under qualified limits|Partial file staysDOWNLOADING/RETRY_WAIT; never mark success on EOF alone|
|SM14|VALIDATING|ASSET_COMMITTED|VAL/DFE valid,retention allowed,unique proven Library import receipt exact SHA/rev|C|validation + SG04/SG05 receipt and asset pin|Import at most once per resolved token; no attach yet|Lost import return→NEEDS_RECONCILIATION; currentAPI gap OD02, not blind repeat|
|SM15|ASSET_COMMITTED|ATTACH_PENDING|Current rights/asset rev valid, target/replace scope approved; GUI may be absent|C|SG06 HandoffIntent and target snapshots|Request GUI-thread application when available|No regeneration if GUI unavailable; stale/rights→specific hold|
|SM16|ATTACH_PENDING|COMPLETED|GUI CAS+exact saved JSON readback binding+settled known billing and current rights|G+C|SG07–SG11 receipts with saved-file SHA/identity|Apply/save only via separately approved broker; completion itself no new effect|Crash after save rereadJSON; historical links/GUI ack alone insufficient|
|SM17|QUEUED|PAUSED_QUOTA|Fresh quota insufficient or unavailable before submit|C|quota evidence + checkpointQUEUED|Pause/notify|No local-calendar refill/alternate provider submit|
|SM18|SUBMITTING|PAUSED_QUOTA|Qualified rejection proves not accepted, no unknown debit|A+C|rejection/settlement + quota checkpoint|Release only proved-unused reservation|Ambiguous429/timeout→uncertain, not this transition|
|SM19|APPROVED,QUEUED,SUBMITTING|PAUSED_BUDGET|Pre-submit unknown/over-ceiling liability or expired price; SUBMITTING only for qualified budget rejection proving no acceptance and settled liability|C|budget rejection/proof + safe QUEUED checkpoint; release only proved-unused reservation|Pause only|No payment/topup; retry only after valid guard|
|SM20|APPROVED,QUEUED,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING|PAUSED_RIGHTS|Input/output/data permit missing/expired/revoked; no uncontained in-flight submit|C|rights incident; preflight dequeued to APPROVED checkpoint, otherwise exact local phase|Stop new transfer/import/attach; retain only if lawful|In-flight remote generation uses cancellation protocol instead|
|SM21|PAUSED_QUOTA,PAUSED_BUDGET|QUEUED|Known no in-flight submit; explicit fresh quota/valid cost0 and same valid authorization|H/Q+C|resume evidence and new guard evaluation|Queue, not submit|If no-acceptance proof missing→reconcile; no blind resume|
|SM22|PAUSED_RIGHTS|APPROVED,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING|Fresh lawful review/permit and pinned versions; destination equals recorded safe checkpoint|H+C|review + checked checkpoint|Resume only that local/preflight phase|If scope changed new job/intent; never jump toCOMPLETED|
|SM23|ASSET_COMMITTED,ATTACH_PENDING|STALE_TARGET|Project/anchor/disk snapshot changed or target deleted/ambiguous|G/C|stale report,retained asset pin|No target mutation|History/link cleanup does not regenerate or silently rebase|
|SM24|STALE_TARGET|ATTACH_PENDING|Explicit new HandoffIntent for current target/replace scope; original request/result unchanged|H+G+C|new attach permit+snapshots+history|One newly authorized CAS candidate|No approval from old batch alone; stale again staysSTALE_TARGET|
|SM25|RUNNING,RESULT_AVAILABLE,DOWNLOADING,VALIDATING|RETRY_WAIT|Qualified safe read/local failure; or known terminal no-output/non-acceptance eligible for new attempt; notUNKNOWN|C|retry class,cost/checkpoint,deadline,next_due|No immediate repeated submit|Bad media/permanent error not retry-until-good; unknown effect→reconcile|
|SM26|RETRY_WAIT|QUEUED,RUNNING,RESULT_AVAILABLE,DOWNLOADING,VALIDATING|Clock due,attempt/deadline/permit valid; destination equals persisted retry checkpoint|C|retry consumed + guard/fence|Safe same-job read/local resume; new submission only viaQUEUED+SM05|Never directRETRY_WAIT→SUBMITTING; changed model/scope requiresnewjob|
|SM27|SUBMITTING,RUNNING,RESULT_AVAILABLE,DOWNLOADING,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING,RETRY_WAIT,SUBMISSION_UNCERTAIN,NEEDS_RECONCILIATION,STALE_TARGET,PAUSED_RIGHTS|CANCEL_REQUESTED|Explicit user/batch revocation/expiry containment action; not already terminal|H/C|cancel flag+intent,held liabilities,phase checkpoint|Stop new work; qualified cancel for known ID; retain/quarantine late results only if permitted|UnknownID/outcome cannot becomeCANCELLED; retries of cancel only same intent if safe|
|SM28|DRAFT,AWAITING_APPROVAL,APPROVED,QUEUED,PAUSED_QUOTA,PAUSED_BUDGET|CANCELLED|Known no dispatched/in-flight effect and no unsettled liability|H+C|cancel evidence + proved reserve release|No provider call|If queue/dispatch race uncertain→CANCEL_REQUESTED instead|
|SM29|CANCEL_REQUESTED|CANCELLED|Known terminal remote/no effect outcome,settled billing,local worker acknowledgement/containment|Q/C|cancel settlement + retained artifact disposition|No attach; cancellation not a file-delete command|Late duplicate observed without reopening/attaching; contradictory proof raises incident|
|SM30|CANCEL_REQUESTED|NEEDS_RECONCILIATION|Cancel unsupported/unconfirmed,unknown submit/charge or uncontrolled worker|C|open cancel/charge incident; flag retained|Only safe lookup/containment|No presumed refund or settled cancellation|
|SM31|NEEDS_RECONCILIATION|CANCEL_REQUESTED|Cancellation remains requested and qualified remote identity now recovered|Q+C|identified cancel target+same intent|Same permitted cancel operation|No generation; cannot drop original cancellation flag|
|SM32|DRAFT,AWAITING_APPROVAL,APPROVED,QUEUED,SUBMITTING,RUNNING,RESULT_AVAILABLE,DOWNLOADING,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING,RETRY_WAIT|FAILED|Proven permanent failure/policy rejection,known external outcome and settled liability|C/Q|terminal error+evidence+retained asset disposition|No further generation/attach|If external/billing outcome uncertain → reconcile, notFAILED|
|SM33|SUBMITTING,RUNNING,RESULT_AVAILABLE,DOWNLOADING,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING|NEEDS_RECONCILIATION|Wrong job/model/conflicting terminal event,terminal billing uncertainty,incomplete/conflicting validation evidence,ambiguous Library commit,save receipt ambiguity|C|incident+quarantined effects/artifacts+held reserves|No new submit/import/JSON overwrite|Human/qualified evidence resolves exact phase only|
|SM34|NEEDS_RECONCILIATION|RESULT_AVAILABLE,DOWNLOADING,VALIDATING,ASSET_COMMITTED,ATTACH_PENDING|Exact associated artifact/import/save-local checkpoint proved; scope/rights/cancel guards valid|Q+C|proof and resolved continuation checkpoint|Resume same result/saga only|Not a generic state chooser: no proof→no transition; cancel flag routesSM31/SM29|
|SM35|RUNNING|CANCEL_REQUESTED|Rights or data/permit revoked while provider job active|C|revocation event+cancel intent|Qualified cancel/stopnewtransfers|No in-flight revocation guarantee; unknown cancellation→SM30|
|SM36|NEEDS_RECONCILIATION|FAILED|Reconciled known permanent failed outcome and settled billing, no unresolved cancel|Q+C|settlement+terminal failure receipt|No further effects|Never infer failure from missing status alone|
|SM37|NEEDS_RECONCILIATION|CANCELLED|Qualified cancel/no-effect and billing settlement all proven; cancel flag present|Q+C|settlement+cancel receipt|No attach|Unknown or late uncontained effect remains reconcile|
|SM38|SUBMITTING|RETRY_WAIT|Qualified transient rejection proves no acceptance and known settled liability; same immutable request, retry/permit/attempt caps valid|A+C|non-acceptance receipt + settled reserve + retry checkpoint QUEUED/deadline|No submit now; future attempt only through SM26 then SM05|Duplicate rejection deduplicated; unknown acceptance/billing must use SM07/SM08, not this edge|

No automatic edge exists from SUBMISSION_UNCERTAIN or unknown billing to SUBMITTING/QUEUED. Even a timeout before any provider job ID is received is uncertainty unless qualified non-dispatch/non-acceptance evidence proves otherwise. Simulator lookup may prove the original receipt; it doesn't authorize a live request. Retry policies never imply a new approval. Deadlines/attempt caps/cost0 and separate live gate apply on every resume.

P1-03 recovery uses SG receipts and saved JSON, not historical links. P1-02 GUI acknowledgement may disappear on close without making the job failed or saved. P1-01 no VALIDATING→ASSET_COMMITTED unless required decoded evidence passes. OPEN OD02/OD03/OD04 block affected future handoff edges until qualified; these edges remain proposed rather than silently satisfied by current APIs.

## Transition/oracle traceability (specifications, NOT_RUN)

|Rule|Future oracles|
|---|---|
|SM01|T002|
|SM02|T003|
|SM03|T004|
|SM04|T005|
|SM05|T006, T025, T063|
|SM06|T006, T032|
|SM07|T025, T026|
|SM08|T026, T028|
|SM09|T027|
|SM10|T029|
|SM11|T031, T034|
|SM12|T047, T049|
|SM13|T046, T049|
|SM14|T050, T051|
|SM15|T053, T057|
|SM16|T054, T055|
|SM17|T016, T017|
|SM18|T016, T018|
|SM19|T013, T015, T019|
|SM20|T021, T071|
|SM21|T018, T019|
|SM22|T073|
|SM23|T053, T068|
|SM24|T057|
|SM25|T030, T043|
|SM26|T024, T030|
|SM27|T020, T060, T061|
|SM28|T059|
|SM29|T023, T061|
|SM30|T023, T060|
|SM31|T074|
|SM32|T035, T043|
|SM33|T033, T040, T051|
|SM34|T075|
|SM35|T071|
|SM36|T076|
|SM37|T077|
|SM38|T078|
