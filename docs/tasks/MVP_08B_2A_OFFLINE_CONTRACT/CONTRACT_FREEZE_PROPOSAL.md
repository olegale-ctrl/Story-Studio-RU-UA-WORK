# Offline execution contract freeze proposal

**MVP-08B.2a · 2026-11-19 · DOCS_ONLY · PROPOSAL — NOT APPROVED FOR IMPLEMENTATION.**

## Exact sources and authority

Documentation branch `docs/mvp-08b-2a-offline-execution-contract-freeze`; base `04ea194e4d57c8a0550d7412281da58d4ba252c5`, tree `661e8307a36d56860aa67407ea8bc4d4f0a1c997`. This accepted audit branch is a child of main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`. No merge of experimental code is used to create this docs branch.

- B.1 exact commit `f0bce140451bf00a86f3939330e77ed63b2c98be`, tree `0b5238611cc84ef0a665f75b552757666935516e`. Original contracts, not SP paraphrases: JOB_CONTRACT (GenerationJob groups; Identity/idempotency; related records), STATE_MACHINE (W; registry; SM01–SM38), OFFLINE_SIMULATOR (durable ledger; SIM01–SIM18), RESULT_INGESTION (VAL/DFE), ASSET_HANDOFF (SG01–SG11), OPEN_DECISIONS (OD01–OD08), IMPLEMENTATION_PLAN and owner records, under `experimental_mvp/reports/`.
- B.2 exact commit `04ea194e4d57c8a0550d7412281da58d4ba252c5`: eight source documents under `docs/tasks/MVP_08B_2_IMPLEMENTATION_AUDIT/`. It found no compliant runtime in verified scope, while locating unrelated RAM LAB/S2/Library components. The current owner accepts **the completed audit with limitations**, not a GenerationJob implementation.
- SP/1.1 exact commit `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`: `docs/tasks/SP_INTEGRATION_01B/`, `core/topic_to_film_v1_1.py`. Its transport remains diagnostic, blocked, no submit/permission. It is not adopted as a JobStore payload.

Owner authority in this task is **APPROVED: six new Markdown documents only; B.2 audit ACCEPTED_WITH_LIMITATIONS**. Existing D01–D08 remain OWNER_APPROVED exactly at B.1 `MVP_08_OWNER_APPROVAL.md`; MVP-08A remains accepted with its existing limits/P1 issues. B.1 new execution machinery is PROPOSAL, not blanket owner approval. Every new EC decision/recommendation below remains OPEN/PROPOSAL. No real approval, signature or trusted receipt is manufactured by examples.

## 1. Minimal profile and success boundary — EC-01

Proposed profile `OFFLINE_CORE_PROFILE_1`: one specialized synthetic video-anchor GenerationJob, existing synthetic identity `OFFLINE_SIMULATOR_V1 / SIM_WAN_PROFILE_V1 / 1 / LOCAL_ONLY`; request mode restricted to T2V for this first profile, execution purpose SYNTHETIC_TEST_ONLY, cost0. This does not name a real Wan release. One serial logical worker in the controller process, no external model/process/provider, no generic job-type registry, task DAG, plugins, arbitrary callable or seven SP stage handlers.

Recommendation: implement the **prefix through RESULT_AVAILABLE**, not COMPLETED. Preserve all22 B.1 state names and38 original transition definitions; a profile can disable deferred operations, not redefine their success. SM12–SM16 (download/validate/Library/attach/save), SM23/SM24 target handoff are deferred. No import/save receipt exists at the initial boundary. Observable result receipt means an associated prequalified local fixture reference only, not current saved film, asset clearance, technical PASS or release. RESULT_AVAILABLE is nonterminal; observer reports pipeline_complete=false and HANDOFF_NOT_QUALIFIED. Retained results need no active worker.

COMPLETED remains reserved for original SG05+SG10/SG11 and SM16 proof of exact asset/import/current rights/GUI CAS/saved JSON/settled outcome. Never introduce “SYNTHETIC_COMPLETED” or alias MOCK_FINALIZED to COMPLETED. The full B.1 SIM01 end-to-end oracle remains unfulfilled by prefix success. Recognizing reserved enums is not permission to write them.

## 2. Immutable request, identity and acyclic hashes — EC-02

Proposed closed `RequestIntent/1` content, exact JSON types, no unknown keys:

|Group|Required values|Binding rule|
|---|---|---|
|content_version|integer1|Versioned proposal, not silently B.1 adopted wire|
|identity_context|project_id,scene_id,anchor_id,purpose_id (canonical UUIDs)|Explicit fixture identities, never topic-derived or inferred from a path|
|target_snapshot|project_locator_ref,expected_saved_json_sha256,expected_editor_snapshot_sha256,expected_anchor_token,generation_fingerprint,input_manifest_sha256|Exact fixture snapshot; locator resolves only via approved managed fixture registry|
|request|provider_id,model_id,model_version,region,mode,prompt_reference,prompt_sha256,duration_ms,resolution{width,height},aspect_ratio{num,den},input_assets[],provider_parameters,capability_profile_ref,capability_profile_hash|Exact synthetic allowlist; positive integers/rationals; profile permits no external input_assets,provider_parameters empty unless separately pinned fixture key allowed|

This makes intended purpose explicit, clarifying a missing field/projection in B.1; it is an owner decision, not a historical schema edit. Stored GenerationJob still has B.1 identity/target/request/authorization/execution/result/audit groups. job_id/store_id/acceptance sequence assigned by admission are immutable, as are canonical content and initial batch/authorization binding. No edit endpoint in initial profile; draft edits from general B.1 remain deferred, not silently implemented. New request/scope requires new explicitly approved intent/job. No caller updates approved bytes in place.

Acyclic dependency order:

0. InputManifest lists raw fixture input bytes/IDs only. CapabilityProfile/FixtureRegistry contain fixed handler/caps and pre-existing fixture byte references only. They contain no current RequestIntent, batch, grant, acceptance or expected-run trace. They are computed first; input_manifest_sha256 is not a batch manifest hash. Run manifests/expected traces may reference request and batch later, but are never hashed back into these prerequisite profiles.
1. Strict bounded RequestIntent content contains **no batch manifest,grant,job_id,own digest or receipt**. `request_sha256 = SHA256(UTF8(asset_library.encoded(content)))`, reusing B.1 JCS-LOCAL-1 (sorted keys,ensure_ascii=false,allow_nan=false,**default separators with spaces**,no Unicode normalization). New validator excludes floats/bool-as-int/subclasses/duplicate keys/surrogates before encoding. Canonical object bytes are retained for comparison; arrays retain declared order.
2. Batch manifest binds batch_id/revision and ordered entries `(project_id,purpose_id,request_sha256)` plus bounded policy;initial batch contains one entry. Compute its hash without an own-hash field. It references step1, not an accepted-job/authorization digest.
3. Fixture BatchPermit references that manifest/hash, exact capability/use/expiry/limits and the one configured store_id/simulator_ledger_id/managed-root qualification scope; its independent authorization hash is computed after step2. No permit is in step1 preimage. Synthetic fixture authority is explicitly not real identity/signature qualification.
4. Idempotency scope is exact tuple `(project_id,purpose_id,request_sha256,batch_id,batch_revision,batch_manifest_sha256)`; SQL uniqueness compares complete columns, not a topic or opaque digest alone. Immutable acceptance binding records request hash + batch scope + initial auth ref/hash + assigned job/store identity.
5. Events/acceptance/outbox/result receipts reference existing prior hashes. No receipt is inserted back into its own preimage or earlier request/batch. Different SP compact SI hash, raw file SHA, PG prefixed binding and S1 MAC remain distinct; none substituted.

The same acyclic rule applies inside a transaction. The acceptance event body binds job/key/request/batch/auth but does **not** contain the future receipt hash; its hash is computed first, then the AcceptanceReceipt references that event. For SM05, compute EffectPayload (request/auth/attempt/effect token, no owning event hash), then payload_sha256, then the event binding token+payload hash, then the outbox envelope referring to that event. No event hashes an outbox envelope that hashes the same event. Provider acceptance/result receipts do not contain a future JobStore acknowledgement-event hash; the later event may reference the already existing receipt hash. Atomic insertion of related rows is not a reason to define a cryptographic cycle.

This resolves the otherwise possible request→batch manifest→request-hash cycle. Choosing exact projections and lifetime key retention is EC-02 OPEN. Current proposal retains idempotency rows/tombstones for the synthetic store lifetime, including terminal jobs; no automatic pruning. Dedup scope is one qualified configured store/ledger namespace, not all project copies. Replacing a missing store with a new identity cannot reuse the old bound permit; cloning/relocating an active store or ledger needs a separately qualified restore protocol and is not automatic. Changed content with a deliberately reused supplied key is CONFLICT. A correctly new key still needs a matching new fixture permit; it is not implicit reapproval. Same-scope grant renewal is deferred; never append/replace approval on an ordinary accept/reuse call.

## 3. Acceptance versus state — EC-02/03

Proposed `accept_request(intent,key,batch_permit,fixture_context)` returns outer disposition ACCEPTED / REUSED / CONFLICT. These are **API dispositions, not new job states**.

- ACCEPTED: after one committed store transaction, exactly1job in DRAFT revision1, acceptance event1, immutable AcceptanceReceipt, no queue/outbox generation yet. No success before commit acknowledgement.
- REUSED: same key, exact canonical bytes, batch and initial authorization binding returns same job_id and **byte-identical stored receipt**; no new job/event/revision/effect. A separate observer snapshot can show later state, without altering the original receipt.
- CONFLICT: reused key with incompatible bytes/scope/binding, or supplied key inconsistent with recomputation;no mutation/no acceptance receipt. Invalid/unqualified authority yields typed denial, not accepted work.

Receipt proposal: receipt_version,store_id,job_id,key tuple,request_sha256,batch_scope,initial_authorization_sha256,accepted_job_revision,accepted_store_sequence,acceptance_event_ref,commit_profile_ref. It describes local committed acceptance, not execution/release or power-loss qualification. `lookup_acceptance(key,expected_request_hash)` is authoritative only against the exact intact store identity. Missing/unavailable/corrupt store is not proof no acceptance occurred; never recreate an empty store and deduplicate against it.

## 4. Durable JobStore and mutation protocol — EC-03

Recommend one new local SQLite JobStore, **separate from Asset Library DB**, immutable store_id/schema/profile and explicitly managed private data root. Tables: store_meta;requests (canonical bytes/hash and immutable binding);jobs (state/revisions/checkpoint/lease);acceptance_receipts;events;outbox;effect_receipts;job_errors. Internal DDL/index SQL is a future implementation detail constrained by these closed tables/fields/invariants;public contract changes require STOP. No SQL is emitted/executed here. Unique request/key,job/event/effect/receipt identities prevent duplicate logical effects. Foreign key relationships and strict row checks mandatory.

Initial SQL proposal: one writer,BEGIN IMMEDIATE,journal_mode=DELETE,synchronous=FULL,foreign_keys=ON;read back effective settings. SQLite compile/runtime/FS and fault model need separate qualification. Commit acknowledgement is not proof against every power failure,malicious writer,NFS/SMB/cloud-sync/reparse or device cache. Unknown version/profile,unexpected existing file,missing companion identity,corrupt DB/receipt/outbox contradiction → hold/STORE_UNAVAILABLE or STORE_CORRUPT,no repair/reset/migration/delete.

Each durable job mutation, including lease/checkpoint changes, is one fenced CAS plus one append-only event and any matching outbox/receipt changes **in the same transaction**. state_revision increments,per-job event sequence advances,global store sequence advances;no counter wrap/reset. Original W applies. Error before commit rolls back all;loss after commit is recoverable uncertainty of response. Event hash chain detects consistency relative to a retained checkpoint only,not authenticated audit storage.

## 5. Controller, lease and fencing — EC-04

One controller owns all transitions/dispatch/recovery. CLI never owns queue/retry. Initial runtime permits one serial same-process logical worker;no detached/asynchronous effect can survive controller death. Acquire qualified exclusive store-owner OS lock before write mode. A second owner returns LOCK_BUSY;it must not kill/steal from another process. Lease expiry alone does not override a still-held owner lock.

On qualified owner restart increment persisted controller_incarnation and invalidate old fences. Per-job lease token `(store_id,controller_incarnation,job_id,worker_id,lease_epoch)`;claim/renew require current CAS,monotone epoch,qualified clock and permitted state. Preflight/admission mutations use current controller fence+revision;worker-phase mutations also require job lease. First lease claim uses controller fence and atomically allocates epoch,not a pre-existing worker lease. Every transition/effect acknowledgement rejects stale store/incarnation/epoch;old worker cannot advance state or publish a result. Expired/unknown lease cannot dispatch. A stale token is not revalidated merely because bytes match.

LeaseClock explicitly supplies clock_epoch,monotonic observation and wall/fixture instant. Pure tests use controlled virtual clocks. Native local qualification must specify reboot/clock rollback/suspend behavior. Clock anomaly stops dispatch and exposes operational blocker;do not invent a state edge or force-expire based on guessed time. No production trusted-clock claim. Store fencing alone cannot undo a provider effect already accepted;external/multi-process workers are excluded from this profile until separately qualified. Hostile OS/process bypass and check-to-use revocation races remain open.

## 6. Outbox and simulator — EC-05

SM05 commits attempt1,reservation0,event and immutable submit effect token/outbox payload hash **before** simulator acceptance. A single effect gateway under current controller fence rechecks permit/profile/rights/cap/budget before dispatch. No user-selected handler/URL/model. Proposed separate SQLite SimulatorStore is a provider acceptance ledger,**not a second job scheduler/store of job lifecycle**. Same token+same payload gives same provider receipt;different payload conflicts. It persists accept mapping,script cursor and zero-charge ledger before replying. Exact artifact/job/model association required.

No cross-resource transaction between JobStore and SimulatorStore is claimed. Crash after send/before acknowledgement is unknown even if outbox lacks “sent”. SM07→SM08 holds reserve and attempt identity;lookup by original token only. Durable simulator lookup ACCEPTED recovers original IDs via SM09. UNKNOWN/unavailable lookup never causes a new token/submit. Authoritative NOT_ACCEPTED plus settled0 can end known failure via SM36 in initial max-attempts1 profile;new generation retry is disabled. Safe status-read retry only,recorded checkpoint and cap. Cancellation not acknowledged/settled stays CANCEL_REQUESTED/NEEDS_RECONCILIATION;observer timeout never cancels.

The simulator references one pinned self-authored F01 media fixture,not a model or renderer. **No valid F01 hash/bytes are supplied or fabricated here.** The exact fixture manifest,rights/source/hash/length and permitted trace must be supplied/frozen before any positive future run. No placeholder hash promoted to verified result. B.1 full SIM01–18 remains source:initial profile tests applicable prefixes/holds only;media decode/import/save expectations remain deferred.

## 7. Profile state restrictions

New writes use only original guarded edges:SM01,SM02,SM04–SM09,SM11;SM17/18quota;SM19budget where no acceptance is proven;SM20only preflight rights hold;SM21same valid grant/known no effect;SM25/26only SAFE_READ to saved RUNNING/RESULT_AVAILABLE checkpoint;SM27–SM33with sources limited to enabled states;SM34only to RESULT_AVAILABLE;SM35–SM37. All original guards remain,never a wildcard state picker. New generation attempts disabled (cap1),so SM10/SM38resubmit paths cannot be used. SM03draft edits and SM22rights renewal deferred. SM12–16/23/24 and their local-stage destinations disabled. COMPLETED cannot be reached in this profile.

Known permanent failures become FAILED only with known external outcome and settled liability. A timeout is not known failure. Cancellation flag survives reconciliation and late result;late payload cannot attach or silently clear cancel. Receipt/model/job mismatch invokes SM33,not normalization to expected identity. Fixed revision/attempt caps cause a typed hold/error,no forced completion.

## 8. Authoritative observer and wait — EC-06

Proposed observe returns one consistent read transaction:store identity/profile,job immutable binding,current state/revision,lease/checkpoint,high-water event,associated receipts,typed errors/operational blockers. Cursor includes store_id,job_id,state_revision,store_sequence;never compare state names by ordinal. Local mirror/GUI status has no authority. Cursor from another store or ahead of intact store history yields divergence/unqualified observation,not rollback or guessed success.

wait observes only through this API,explicit predicate/state set,bounded deadline and capped read interval. Observer timeout leaves job/lease/event/outbox unchanged and returns WAIT_TIMEOUT plus clearly scoped last authoritative snapshot (or unavailable error),not job failure/cancel/retry. Pure clock tests do not sleep. Failed storage reads cannot synthesize NOT_FOUND. Acceptance without wait returns accepted/reused ID and receipt only,not completed job. No SP CLI wait implementation is enabled by this document.

## 9. Typed error boundary — EC-08

Retain B.1 JobError fields:immutable error_id,domain/code,occurred_at,state/attempt,operation,retry_class (NONE/SAFE_READ/SAFE_LOCAL/RECONCILE_ONLY),safe_message,redacted trace,effect (NONE/KNOWN/UNKNOWN),billing (ZERO/SETTLED/RESERVED/UNKNOWN),evidence_ref,required_action. Proposed local codes:FORMAT,VERSION_UNSUPPORTED,IMMUTABLE_REQUEST,IDEMPOTENCY_CONFLICT,CAS_CONFLICT,STALE_FENCE,LEASE_EXPIRED,CLOCK_UNQUALIFIED,LOCK_BUSY,STORE_UNAVAILABLE,STORE_CORRUPT,OUTCOME_UNKNOWN,RECONCILIATION_REQUIRED,PROFILE_UNQUALIFIED,AUTHORITY_MISSING,RIGHTS_UNCLEARED,BUDGET_EXCEEDED,QUOTA_EXHAUSTED,OPERATION_NOT_AVAILABLE,RESOURCE_LIMIT,SEQUENCE_EXHAUSTED,RESULT_BINDING_MISMATCH,NOT_FOUND,CURSOR_MISMATCH,WAIT_TIMEOUT.

WAIT_TIMEOUT and CURSOR_MISMATCH are observer response errors,not persisted job mutations. NOT_FOUND is permitted only from a consistent intact-store query in the exact configured namespace;STORE_UNAVAILABLE/CORRUPT never maps to it. These responses do not grant a new effect or constitute a cross-store no-acceptance proof.

Errors preserve uncertainty/last known state;they are not new lifecycle enums. No secret prompts,credentials,URLs or user materials in logs. $0synthetic ledger does not imply acceptance is known;free charge is not proof safe resubmit. Schema/type→scope/key/authority→store/fence/time→revision/state→effect/receipt consistency is proposed public check order;store integrity failure always prevents effects. Exact mappings/oracles require EC-08approval,not silent exception swallowing.

## 10. Deferred integration — EC-09/10

Asset Library remains unchanged:resolve pinned revision immediately before any future allowed use;never trust cached status/tags/content dedup as import receipt. No import_file/attach/detach/save/Tk in initial core. OD02unique import receipt,OD03stable project/save CAS,OD04decoded evidence,OD06lifecycle remain OPEN/deferred. Current P1 limits remain.

Route D uses plan+prepared assets and whole-film render/gates;it is **not** identical to B.1video-anchor T2V/I2V generation. Minimum compatibility is a future typed boundary to accepted/reused/conflict+observer/receipts for a single separately approved operation. No direct SP payload acceptance,no hash aliasing,no arbitrary stages,no first_video.build bypass. Initial core supplies no real Route D execution mapping;SP remains BLOCKED_DISPATCHER_CONTRACT. EC-10asks whether to defer D execution or separately specify a narrow render-plan handler later. Neither implies a general DAG. Release/render authority and scientific/editorial suitability never follow from local result receipt.
