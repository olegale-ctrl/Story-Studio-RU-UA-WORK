**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. EXISTING behavior is source-inspected at base1ff403e; APPROVED decisions are the unchanged D01–D08 and [new owner acceptance](MVP_08A_OWNER_ACCEPTANCE.md). Everything newly specified here is PROPOSED / NOT_IMPLEMENTED / NOT_RUN. OPEN gates are in [decision register](MVP_08B_1_OPEN_DECISIONS.md). No runtime or live API tests performed; WINDOWS_NOT_RUN.

# Deterministic offline simulator contract

APPROVED product sequencing: first future executable stage must be offline. EXISTING MVP-08A has no simulator. This specifies one only: no code, fixtures, media generation, network calls or charges created here.

## Determinism and durable fixture schema

FixtureManifest schema1 contains fixture_id/version/hash,simulator_profile_version,seed,virtual_clock_epoch,tick_unit_ms,stable job/attempt/remote/artifact IDs,event script ordered by(tick,sequence,event_id),request validation profile,quota ledger,zero monetary ledger,result fixture refs+SHA/bytes/DFE expectations,rights/retention evidence,expected trace digest. Event delivery perturbations are scripted, not random wall-clock races. A seeded PRNG may only produce a recorded schedule/jitter, never conceal nondeterministic behavior. Clock advances only via explicit Tick(n); tests never rely on sleep timing. Maximum events/ticks/jobs bounded; queue/deadline policy consumes this same clock.

Provider facade uses OFFLINE_SIMULATOR_V1 / SIM_WAN_PROFILE_V1 /1 /LOCAL_ONLY. These identifiers are not a guessed Wan release or claim of API qualification. Capability,entitlement,availability,price,rights and limits are separate fixture records. Submit acceptance and mapping(client attempt key→remote ID) commit in SimulatorStore before acknowledgement. Same key+same request returns same receipt; same key+different request is an idempotency conflict. Durable zero-charge ledger is observable even when response is dropped. Reopening preserves accepted outcomes; rebuilding an empty store to “recover” unknown jobs is forbidden.

F01 will be a small self-authored local MP4 with fixed bytes/hash/decoded counts/audio metadata; F02 intentionally corrupt/truncated bytes; F03 conflicting header/count fixture; F04 duplicate/out-of-order event payload; F05 unsafe/nonlocalreference that must be rejected before any I/O. **These are fixture specifications, not generated files or asserted current hashes.** Exact bytes/rights/tool versions must be frozen and qualified in an authorized later stage. No placeholder hash is treated as verified. No external credentials/URLs/accounts allowed; network API attempts are fatal fixture/test failures.

Simulator trace equality compares canonical requests/events/ledger/artifact bytes/known zerocharges and semantic saga outcomes. Existing Library UUID/import timestamps use real local values and aren't claimed bit-identical across runs; tests compare bijective receipt relationships and byte equality, not invented deterministic wall-clock metadata. Runtime decoder/tool versions must be pinned when qualifying fixtures.

|Scenario|Name|Virtual event sequence|Fixture / fault|Expected outcome|
|---|---|---|---|---|
|SIM01|success|accepted@0,running@1,result@2|Exact approved fixture MP4 F01|Normal saga; charge0,oneproviderjob|
|SIM02|delay|accepted@0,running@1,result@30|Virtual ticks; no sleeping/network|No premature timeout/completion before scripted tick|
|SIM03|reject|known request_rejected@0|No acceptance receipt|FAILED or explicit eligible correction-new job; no remote effect|
|SIM04|quota|quota_rejected@0 before acceptance|Finite fixture balance0|PAUSED_QUOTA, no hidden refill|
|SIM05|budget|nonzero estimate injected at guard|No simulator submit event allowed|PAUSED_BUDGET; no monetary or provider ledger entry|
|SIM06|transient|status read fails@1 then running@2|Original accepted ID persists|RETRY_WAIT safe status only,onegeneration|
|SIM07|permanent|accepted@0,known permanent_failed@2,billing0|No output|FAILED after known settlement|
|SIM08|timeout|submit result hidden until reconciliation@5|Outcome remains UNKNOWN at deadline|SUBMISSION_UNCERTAIN then reconcile,not new submit|
|SIM09|lost response|provider ledger accepts once@0,reply dropped|lookup(key) returns exact durable originalID|Recover RUNNING originalattempt,no duplicateproviderjob|
|SIM10|duplicate callback|result event delivered twice sameeventID|Both identify same artifact|One event effect/import/handoff|
|SIM11|out of order|resultseq3 then runningseq2|Prior state/result receipt retained|Ignore stale regression; conflict evidence not rollback|
|SIM12|late after cancel|cancel requested@1,result@3,billing0settles@4|cancel supported/unsupported fixture variant|No attach; lawful quarantine then settled cancellation/reconcile|
|SIM13|corrupt media|result points to approved intentionally truncated F02|Receipt hash matches corrupt bytes|Validation rejects; never ACTIVE/COMPLETED from receipt alone|
|SIM14|expired ref|artifact expires@3,retrieve@4|Same artifact may or may not support refresh perfixture|No generation; safe refresh same identity or reconcile|
|SIM15|model mismatch|receipt resolvedmodel SIM_OTHER@2|Requested SIM_WAN_PROFILE_V1|Quarantine/reconcile; never relabel|
|SIM16|wrong job|result associated to another job/attempt|Good MP4 but identity wrong|Reject association; no import/attachment fortarget|
|SIM17|duplicate remote ID|two submissions claim sameproviderID|Samejob duplicate vs differentjob conflict cases|Samejob dedup; differentjob needs reconciliation|
|SIM18|restart|kill/reopen simulator store between accept and reply|Fixture ledger acceptance durable|lookup identical receipt; no regenerate after worker restart|

Every script includes exact expected submit count,lookup/poll/retrieve/cancel counts,ledger entries,terminal/recoverable state,asset and save effects. Inject unexpected socket open/nonzerocharge/unknowncredential field → fail, not fallback. Budget-refusal tests are guard tests (simulator submit count0), not a simulator capable of charging money. A fixture with price>0 must be refused under cap0 before acceptance.

Simulated success validates mechanics only. It doesn't qualify live Wan behavior,provider terms,real outputquality,Windows,Tk lifecycle or protected storage. OPEN OD04/OD06/OD07 apply to later local validation/GUI qualification; no need to choose a live model to specify/test an offline contract in a future authorized stage.
