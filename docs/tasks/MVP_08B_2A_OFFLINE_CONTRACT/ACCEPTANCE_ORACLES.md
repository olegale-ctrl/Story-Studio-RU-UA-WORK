# Acceptance oracles

**MVP-08B.2a · 2026-11-19 · DOCS_ONLY · PROPOSAL — NOT APPROVED FOR IMPLEMENTATION.**

**All 66 oracles below are NOT_RUN.** This task verifies document/source/hashconsistency only;it creates no runtime,schema test,state-machine test,fixture orqualification result. They are executable-ready criteria for a separately authorizedtask,not test code.

Source abbreviations refer to originalB.1f0bce140451bf00a86f3939330e77ed63b2c98be underexperimental_mvp/reports/,B.2audit04ea194e...,SP1.116d28ec.... ECclarifications remainOPEN. Pure/fakestore success cannot be promoted to actual durability/Windows/asset/live qualification. SourceT001–T078/SIM01–18/R01–R26are prior specifications,not already passedtests.

## PURE_OFFLINE

|ID|Given|When|Exactexpectedinvariant/result|Source|Status|
|---|---|---|---|---|---|
|P001|strict canonical values|Encode same keys in different insertion order;then float/bool-as-int/surrogate/unknown field|Equal valid bytes/hash;invalid forms rejected,no admission|JOB_CONTRACT Schema conventions|NOT_RUN|
|P002|request→manifest→permit→acceptance hash graph|Inspect exact declared preimages and recompute in topological order|No earlier manifest/profile includes current request/batch/receipt;acceptance event excludes future receipt hash;effect payload excludes event hash;entire typed preimage graph acyclic/recomputable|JOB_CONTRACT Identity/idempotency + EC-02 clarification|NOT_RUN|
|P003|empty fake store;valid exact fixture scope|Accept identical intent twice|ACCEPTED then REUSED,same job/receipt bytes,job count1,event count1,no submit|T001,T004;JOB_CONTRACT|NOT_RUN|
|P004|existing acceptance key and bytes|Change request but keep supplied key or initial auth binding|CONFLICT;job/event/outbox counts unchanged|T001;JOB_CONTRACT Identity/idempotency|NOT_RUN|
|P005|changed purpose or batch scope|Reuse old permit;then supply a newly matching scoped fixture permit|Old scope denied;only independently matching new intent may create a distinct job|D07;JOB_CONTRACT|NOT_RUN|
|P006|caller flags claiming approval|Attempt SM02 without trusted synthetic fixture context|AUTHORITY_MISSING;no APPROVED/QUEUED/submit from a flag|T002,T003,D05,D07|NOT_RUN|
|P007|nonzero estimate or unknown liability under budget0|Attempt submit|No SimulatorStore call,outbox dispatch0;PAUSED_BUDGET only under original legal guards|T006,T025,D02;SM19|NOT_RUN|
|P008|valid generation fixture result|Advance through prefix;attempt SM12/14/16 directly|RESULT_AVAILABLE,pipeline_complete=false;deferred effects/import/save0;COMPLETED denied|SM11–SM16;SG05/SG10|NOT_RUN|
|P009|old controller incarnation or lease epoch|Return result or try new effect under stale token|STALE_FENCE;no new state/event/outbox/effect|T025,T063;W|NOT_RUN|
|P010|two contenders with same expected revision|Attempt two allowed CAS mutations|Exactly1commit/event;other CAS_CONFLICT;no duplicate effect|W;T059–T063|NOT_RUN|
|P011|live provider/model/region,production or unknown handler|Try accept/dispatch|PROFILE_UNQUALIFIED/OPERATION_NOT_AVAILABLE before any provider effect|D01,D02;SIM guard|NOT_RUN|
|P012|acceptance commit but lost caller reply in fake store|Lookup/repeat same key|Original immutable receipt and job ID;not a new job or grant|T001;JOB_CONTRACT|NOT_RUN|
|P013|fake simulator accept then response dropped|Reconcile original effect token|Same provider receipt/attempt;submit acceptance count1;lookup recovers only original result|SIM09,SIM18;SM07–09|NOT_RUN|
|P014|no JobStore transaction commit yet|Invoke effect gateway|Effect calls0;only committed outbox can dispatch|W;SM05|NOT_RUN|
|P015|unknown send outcome and no authoritative lookup proof|Recover repeatedly|SM07→SM08hold,attempt1,submit count not increased,no queue reset|SIM08;SM07,SM08|NOT_RUN|
|P016|accepted lookup proof vs wrong job/model/stale event|Process duplicate/out-of-order observations|Exact proof→SM09same attempt;duplicate no effect;conflict→SM33,no state rollback|SIM10,11,15,16,17|NOT_RUN|
|P017|quota/budget exhausted or permit expired|Try resume/alternate profile|Hold,no paid/provider/model fallback,submit count0if never accepted|D02,D04;SM17–21|NOT_RUN|
|P018|cancel before dispatch or during uncertain outcome|Request cancellation,then observe unknown/settled evidence|CANCELLED only with no-effect/terminal+settlement proof;otherwise retain cancel flag/hold|SM27–31,SM37;SIM12|NOT_RUN|
|P019|observer has no satisfying predicate before deadline|Wait expires|WAIT_TIMEOUT;job/revision/lease/events/outbox unchanged;no retry/cancel|JOB_CONTRACT execution;EC-06|NOT_RUN|
|P020|SP compact hash/raw SHA/PG binding passed as job request hash|Validate domain/bytes and binding|Reject mismatched identity;do not normalize/relabel hashes|JOB_CONTRACT Schema conventions;SP1.1|NOT_RUN|
|P021|missing/unavailable store vs intact authoritative empty store|Lookup acceptance/job|Unavailable returns STORE_UNAVAILABLE,not NOT_FOUND/no-acceptance proof|RECOVERY_MATRIX;EC-03|NOT_RUN|
|P022|SP readiness alltrue or existing D1 synthetic permit|Try create real authority/release capability|No grant;SP release false;original D1 scope cannot execute this job|D05,D07;SP1.1 boundaries|NOT_RUN|
|P023|fake fixture wrong hash/length/unsafe or nonlocal ref|Resolve provider result association|RESULT_BINDING_MISMATCH before result acceptance/any I/O to unapproved location|F05,SIM15/16;RESULT_INGESTION association|NOT_RUN|
|P024|proposed cap16retained fixture jobs/events counters at bound|Admit17th/exhaust sequence|RESOURCE_LIMIT/SEQUENCE_EXHAUSTED;no deletion,wrap,or reset of prior key rows|OD07/OD08;EC-03/07|NOT_RUN|

## DURABLE_LOCAL_QUALIFICATION

|ID|Given|When|Exactexpectedinvariant/result|Source|Status|
|---|---|---|---|---|---|
|D001|real experimental SQLite transaction commits before ACK|Close/reopen and resubmit same key|REUSED same receipt/job bytes;exact store identity preserved|JOB_CONTRACT;SIM18|NOT_RUN|
|D002|fault before commit and separately after commit/before reply|Reopen under qualified owner|Before:0rows/events/outbox;after:1durable acceptance and same receipt,no mixed partial mutation|W;RECOVERY_MATRIX|NOT_RUN|
|D003|SimulatorStore acceptance committed separately;reply lost|Reopen both DBs,lookup original effect token|One accepted provider effect,one attempt;no new token/submit|SIM09/SIM18|NOT_RUN|
|D004|failure between jobs/event/outbox SQL statements|Rollback/reopen|Atomic all-or-none job revision/event/effect intent;no half-state|W|NOT_RUN|
|D005|two independent controller processes|Acquire owner lock concurrently|One owner;other LOCK_BUSY;never forcibly kill user/other controller|EC-04;OD07|NOT_RUN|
|D006|owner stopped and new qualified owner started|Replay old callback/token|New persisted incarnation;old writes/effects rejected;no generic lease stealing|W;OD07|NOT_RUN|
|D007|missing/corrupt/wrong-version JobStore or missing identity|Open existing path|No empty replacement/repair/schema migration;hold with intact evidence|RECOVERY_MATRIX;OD07|NOT_RUN|
|D008|simulator ledger missing/unavailable|Reconcile unknown send|No authoritative ABSENT inference;hold,no duplicate provider effect|SIM08/09;EC-05|NOT_RUN|
|D009|duplicate effect/event ID or contradictory stored receipt|Read/advance under current fence|Integrity incident,not blind replay or overwrite|JOB_CONTRACT related contracts|NOT_RUN|
|D010|SQLite implementation and FS under test|Read effective PRAGMAs/version/transaction and reopen evidence|Pinned settings and actual platform reported;no universal power-loss claim|OD07|NOT_RUN|
|D011|ordinary process interruption test|Claim durability level|Only stated process-crash evidence;SIGKILL≠power loss;real power tests need separate scope|OD07;B.2 audit|NOT_RUN|
|D012|clock rollback/reboot/epoch mismatch/lease expiry|Attempt dispatch or automatic recovery|No guessed expiry/reapproval;CLOCK_UNQUALIFIED hold/no new effect|OD05/OD07|NOT_RUN|
|D013|network/synced/unqualified/reparse data root|Open writable store|PROFILE_UNQUALIFIED before effect;pure syntax not OS protection|OD07;08A limitations|NOT_RUN|
|D014|job revision,event and receipt committed concurrently|Observe snapshot and compare cursor|One consistent transaction;mirror/cursor divergence cannot override store|EC-06;W|NOT_RUN|
|D015|known no-acceptance after attempt1;safe read failed|Apply retry policy|No generation attempt2;at most2safe reads per proposed cap,known checkpoint only|SM25/26;EC-07|NOT_RUN|
|D016|terminal failed/cancelled or retained result key|Restart and accept same exact key|Same historical job,never reopen/reset/dedup-prune;distinct purpose needs new scope|JOB_CONTRACT Idempotency|NOT_RUN|
|D017|fixture modified between registry check and use|Exercise approved trusted-snapshot/host assumptions|Mismatch/unknown blocks;no claim hostile TOCTOU solved by hashes|RESULT_INGESTION;OD07|NOT_RUN|
|D018|store/disk/event capacity exceeded|Fail operation/reopen|Typed failure,prior committed history retained,no user cleanup/overwrite|OD07/OD08|NOT_RUN|

## WINDOWS_QUALIFICATION

|ID|Given|When|Exactexpectedinvariant/result|Source|Status|
|---|---|---|---|---|---|
|W001|real authorized Windows10/11 NTFS host|Run lock/journal/path matrix under pinned Python/SQLite|Actual build/FS/versions+exit evidence;Linux result not substituted|OD07|NOT_RUN|
|W002|junction/reparse/ADS/UNC/hardlink or changed ancestors|Probe store/fixture open safely|Reject unqualified paths;record exact residual races;no fake path-only guarantee|08A limitations;OD07|NOT_RUN|
|W003|second controller and crash on Windows|Exercise owner lock release/incarnation invalidation|Exactlyoneowner and stale callback rejection after authorized restart|OD07;W|NOT_RUN|
|W004|Windows reboot/suspend/wall-clock anomaly|Exercise qualified clock profile|No guessed monotonic continuity or automatic grant renewal|OD05/OD07|NOT_RUN|
|W005|spaces/Cyrillic paths/permissions/read-only files|Perform bounded local store operations|Exact bytes/results or explicit typed error;no admin/system-policy changes implied|08A limitations|NOT_RUN|
|W006|SQLite journal/disk-full/flush failure|Inject scoped fault without user data|Actual effects documented,no power-loss qualification inferred|OD07|NOT_RUN|
|W007|controller closes with observer/worker pending|Test process-lifetime contract|No orphan effect-capable worker;no Tk/native integration claim|OD06/07|NOT_RUN|
|W008|same fixture/profile on Windows and Linux|Compare canonical records and permitted trace|Same semantic bindings;platform-specific timings/locks explicit;no media binary fabrication|SIM determinism;OD07|NOT_RUN|

## ASSET_INGESTION_SAVE_QUALIFICATION

|ID|Given|When|Exactexpectedinvariant/result|Source|Status|
|---|---|---|---|---|---|
|A001|new pipeline qualification absent|Offer result to Asset Library|Initial core refuses import/attach/save;remains RESULT_AVAILABLE|OD02/03/04;SM12–16|NOT_RUN|
|A002|future import committed but response missing|Reconcile exact ingestion receipt|No blind re-import or regenerate;unknown→NEEDS_RECONCILIATION|OD02;SG04/05|NOT_RUN|
|A003|same content SHA with different asset provenance/rights|Map result to asset|Distinct identity/receipt maintained;tags/search not exactly-once proof|ASSET_HANDOFF|NOT_RUN|
|A004|project identity/disk bytes changed|Apply future handoff/save|No stale overwrite;qualified stable UUID/disk CAS required|OD03;P1-03|NOT_RUN|
|A005|asset revision/rights changed after result|Use/attach pinned asset|Recheck exactrevision/currentrights;no implicit latest;inflight revocation limit explicit|D05;08A resolve|NOT_RUN|
|A006|nb_frames vs decoded evidence mismatch|Validate future media|Required DFE missing/mismatch never ASSET_COMMITTED/COMPLETED|OD04;P1-01|NOT_RUN|
|A007|GUI ack or historical DB link without saved JSON proof|Request COMPLETED|Deny;SG05+SG10/11/current rights/settlement required|SM16;P1-03|NOT_RUN|
|A008|qualified save occurred but ACK missing|Read current exact JSON and reconcile|Historical receipt onlyif proven;never rewrite newer user edits|ASSET_HANDOFF SG10|NOT_RUN|
|A009|GUI closes/Undo/session replaced|Observe late attachment result|No off-thread Tk/no stale apply;OD06qualification still required|P1-02;OD06|NOT_RUN|
|A010|attach/save failure after valid asset receipt|Recover local pipeline|Reuse exact existing result/asset;generation count unchanged|ASSET_HANDOFF;RECOVERY_MATRIX|NOT_RUN|

## FUTURE_PRODUCTION_LIVE

|ID|Given|When|Exactexpectedinvariant/result|Source|Status|
|---|---|---|---|---|---|
|L001|only offline acceptance or$0marketing available|Try live/paid API|Denied;exact separate owner scope/model/account/region/budget required|D01–D04,OD01|NOT_RUN|
|L002|unknownsource/image/music/voice use rights|Request production operation|Hold until documented intended-use/territory/time/attribution proof|D05|NOT_RUN|
|L003|real provider/data recipient or limits materially changed|Reuse old batch|Reapproval needed;no widened scope or unattended spending|D07,OD05|NOT_RUN|
|L004|real URL/media fetch/decoder/native boundary|Qualify future transport|Separate SSRF/resource/native/storage/decoded proof,no inherited local qualification|OD04/07|NOT_RUN|
|L005|sensitive/revoked data vs recovery retention|Retain/delete/transfer|Explicit retention/deletion authority;no automatic cleanup of user originals|OD08|NOT_RUN|
|L006|complete technical MP4 or alltrue diagnostic assertions|Publish/release|No release without independent verifier/human suitability/current exact version/use scope|SP1.1;production boundaries|NOT_RUN|

## Evidence and STOP

Eachfutureexecution record must pin source/base/tree,Python/OS/SQLite/FS/clock/fixture versions,command,exitcode,actualcounts/skips,duration,redacted errorandstage limit. Finite testselection andwall/resourcebounds first;unknown timeout isnotPASS. Reuse18historicalLABtestsuccess onlyas scopedRAMevidence,not theseoracles. HistoricalB.2bulkinterruptionexit-2remainsnotapass. No actualmodel/provider/productionrender/publication oruser-data deletion isauthorized by anyoracle. Windowsrequiresrealhost;otherwiseNOT_RUN. Stop aftereachqualifiedstage forindependent review andscopepermission.
