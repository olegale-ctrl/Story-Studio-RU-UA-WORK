# Minimal execution scope

**MVP-08B.2a · 2026-11-19 · DOCS_ONLY · PROPOSAL — NOT APPROVED FOR IMPLEMENTATION.**

## Approved now vs proposed next

APPROVED now:read exact B.1f0bce140451bf00a86f3939330e77ed63b2c98be,B.2audit04ea194e4d57c8a0550d7412281da58d4ba252c5,SP1.116d28ec0376c8c28f879c8aacb18d5378fea83a3;publish six new Markdown files only. B.2 accepted as audit with limitations. All runtime entries below are PROPOSAL/NOT_IMPLEMENTED,require independent review and separate owner authorization. No model,render,DB,lease,outbox,queue,simulator or qualification test is created/run in this task.

## One specialized operation

One synthetic T2Vvideo-anchor GenerationJob under OFFLINE_SIMULATOR_V1/SIM_WAN_PROFILE_V1/version1/LOCAL_ONLY. The initial handler is fixed by capability/profile,not dynamically registered. One serial controller process and same-process logical worker;one request per fixture batch;no generic DAG,script drafting,TTS,image generation,real inference,live adapter,network downloader,arbitrary Python plugin or nested coordinator.

Successful core boundary is RESULT_AVAILABLE with exact fixture receipt andblocked handoff. No real Library import,GUI,project mutation/save orCOMPLETED. At mostone generation attempt,only bounded safe-read retries. No authority inferred from a caller flag. Former RAM LAB is reference/test context only,not silently ported into job storage.

## Proposed initial numeric envelope — EC-07 OPEN

|Quantity|Proposed value|Fail-closed consequence|
|---|---|---|
|Generation-capable logical workers|1,same controller process|No parallel/surviving effectworker allowed|
|Jobs retained per synthetic test store|16|17thadmission RESOURCE_LIMIT;no prune/reset|
|Requests per fixture batch|1|No hidden batch scheduler/DAG|
|Generation attempts per job|1|No generation resubmit afterfailure/unknown|
|Safe status-read retries per checkpoint|2|Exhaustion holds/errors;never newgeneration|
|Events per job /outbox records per job|128/32|Stop before overflow;retainhistory|
|Canonical request bytes /F01bytes|1MiB/8MiB|Rejectbeforeoversizedallocation/read;F01exacthashstillrequired|
|Script events /virtual ticks per testcase|64/10000|Finite deterministictests,nounboundedrecoveryloop|
|Initial lease TTL|30000msunder qualifiedclock|Unknown/expiredclock blocks effects;not claimnative qualification|
|Observer wait|Caller deadline,cap300s;readinterval100–1000ms|Timeout read-only,not jobfailure/cancellation|
|Monotone revisions/epoch/sequence|strict positive signed64,neverwrap|SEQUENCE_EXHAUSTED;no reset|

These are initial **proposed test/profile caps**,not measured hardware limits or approved PG/native qualification. They do not change existing Asset Library/PG caps or qualify Windows. Effective minima/intersections apply if a later qualified component has stricter bounds. Source B.1 OD07 remains OPEN.

## Resource and authority boundaries

Only new private managed testdata roots,exact store identity/profile,no unknown existing-file overwrite,automatic migration/repair/recreate or cleanup. SQLiteJobStore andSimulatorStore are separate resources;only first owns lifecycle. Nonlocal/synced/network/reparse/hostile roots unqualified. No normal user projects/materials/sensitive data in the initial profile. Runtimeoutputs DBs/journals/logs outsideGit. No automaticdeletion/retentionpruning. Testharness may clean only its own explicitly reserved temparea under future scoped authorization;never user originals.

SyntheticFixtureContext is injected by a trusted testharness,not accepted as authenticated identity from requestJSON. It pins authoredfixture/licence/testscope/price0/clock/limits. Realrights/trust/expiry/revocation/livepermissions remain separate. Absentcontext givesAUTHORITY_MISSING;closedprofile rejects production/liveevenwithsyntheticgrant. BatchPermit bytes remain immutable;no automaticrenewal. Event/receipt hashes are consistencydata,not signatures or protectedauditproof.

NoF01bytes/hash are fabricated in this package. Before a positive future test,supply reviewed self-authored localMP4fixture,projectfixture,prompt,manifest andexactrawSHA/byte lengths/tool evidence. No backend/model/FFmpeg execution tocreate them is implied. Without validfixture,positiveeffectexecution BLOCKED_EVIDENCE;purecontractnegative tests canbe specified without claimingmediavalidity.

## Qualification split

|Stage|Allowed only by future separate task|Required evidence / explicitSTOP|
|---|---|---|
|Pure offline|Closedvalue validation,FakeStore/FakeClock,deterministic scripts,fake fault outcomes|P001–P024NOT_RUN now;not persistence orrealpermissions|
|Durable local storage|Actualnewprivate SQLitestores,finite process interruption/reopen,lock/fence/outbox tests|D001–D018;pinFS/Python/SQLite/clock;commit/processcrash≠powerloss;STOP ifunknown/corruptroot|
|Windows-specific|ActualauthorizedWindows/NTFS build,path/lock/clock/resource tests|W001–W008;no settings/admin/modelchanges implied;LinuxnotWindows|
|Asset ingestion/save|OnlyafterOD02/03/04/06 decisions,newqualifiedAPIs/receipts|A001–A010;initialcoremustnotcallLibrarymutations/save|
|Future production/live|Exactseparate provider/account/model/rights/data/budget/native/releasepermission|L001–L006;allcurrentlyprohibited|

## Minimal Route D compatibility

SP1.1validation remains unchanged;routeDplan+preparedmedia/wholefilmrender is not this clipjob. Proposed shared boundary is opaque scopedintent→accepted/reused/conflict receipt→authoritativeobserver,after a separate exact mapping is approved. SPinput/hash never directly adopted asJobStoreAPI. InitialcoredoesnotexecuteRouteD;readinessBLOCKED_DISPATCHER_CONTRACT remains untilEC-10andactualAPIaccepted. No mandateduniversalDAG or first_video.buildbypass.
