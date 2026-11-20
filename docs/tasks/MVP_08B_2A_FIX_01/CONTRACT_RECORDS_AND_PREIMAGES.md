# MVP-08B.2a-FIX-01 — Exact records and hash preimages

Status: **PROPOSAL / DOCS_ONLY — OWNER REVIEW REQUIRED**. Date: 2026-11-20.

Project status remains **BLOCKED_CONTRACT**. This document proposes resolution of accepted findings; it does not approve EC-01–EC-10, G1–G6, implementation, real APIs, spending, storage, CI, main, merge, release or production permissions.

Source precedence: owner instruction in this conversation accepting the limited audit and F01–F05; exact independent review `3744eb5584e72e338dc51fa3a6fe7aed4882651b`; original freeze `c5cd33023880fd6726b74f5631eb766cc0959892`; original B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`; B.2 `04ea194e4d57c8a0550d7412281da58d4ba252c5`; SP/1.1 `16d28ec0376c8c28f879c8aacb18d5378fea83a3`. Historical documents remain unchanged. New PURE records below are proposals, not replacements for approved external contracts.

## F01 resolution and type language

Every hashable record has exactly `kind`, `version: 1`, `scope: "PURE_FAKE_ONLY"` and the fields listed below. All fields are REQUIRED. `?T` means required key with either null or T; it never means absent. Unknown fields, omitted fields, duplicate JSON keys and unknown versions are rejected. `=X` denotes a literal, not a free string. Object order on input is irrelevant; array order is meaningful. No implicit normalization/coercion, default insertion or conversion of missing to null is allowed.

`UUID`: lowercase canonical 8-4-4-4-12 hexadecimal string. `Digest`: exactly 64 lowercase hex characters. `U`: integer 0..9223372036854775807; `Pos`: 1..that maximum. Booleans are not integers. `Bool`: JSON boolean. `Text`: 1..100000 Unicode scalar values, no unpaired surrogates. `Opaque`: Text, not a filesystem path, URL permission or verified locator. Enum members are exact strings. All strings preserve Unicode, including normalization form. Floats, NaN, infinity, BOM and non-JSON values are invalid. Keys in these schemas are ASCII.

`ListN` has exactly N items; `ListA..B<T>` has inclusive bounds. `List0` is exactly `[]`. `Ref<X>` is the closed object `{"kind":"PURE.X","digest":Digest}`; `Ref<HashKind>` must name one of the 25 registered kinds. Resolve the entire transitive reference closure, check each expected kind/version/scope, recompute bytes and digest, reject missing references, cycles or inconsistent bindings. A digest alone is never proof of provenance, rights or authority. Equality uses kind, exact canonical bytes and verified digest; a digest collision/inconsistent stored bytes fails closed as STORE_CORRUPT. Raw file SHA-256, SP/S1/PG identities and PURE typed references are not interchangeable.

Canonical function C is the existing B.1 local encoding convention, **not RFC 8785 JCS**: UTF-8 of Python `json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)` with default separators `", "` and `": "`, no final newline. Integers are base-10 without leading zeros; zero is `0`. Strings use JSON escapes for quote, backslash and controls, retain other Unicode scalars including `/` and non-ASCII. Sort ASCII field names lexicographically. H(X) is lowercase SHA-256 of **all** C(X) bytes, including kind/version/scope. No record contains its own digest. There are no optional exclusion lists. A change to any declared field changes the preimage. Numeric ranges are checked before encoding, never round through IEEE-754.

An unordered collection is represented only by its specified sorted array and is rejected if unsorted; implementations must not silently rearrange input. Registry fixtures sort by resolved fixture_id; input items by (role,object_id); write-set members by (kind,digest), all ascending ASCII. Other arrays retain their stated input order.

## Closed hashable record registry

### PURE.FixtureDescriptor / version 1

| Required field | Exact type |
|---|---|
| `fixture_id` | `UUID` |
| `label` | `Text` |
| `content_class` | `=SYNTHETIC_METADATA` |
| `producer_qualification` | `=UNQUALIFIED_FAKE_ONLY` |

No media bytes,format,licence or actual producer proof declared.

### PURE.FixtureRegistry / version 1

| Required field | Exact type |
|---|---|
| `registry_id` | `UUID` |
| `fixtures` | `List1..16<Ref<FixtureDescriptor>>` |

References unique and sorted by referenced fixture_id;closure must resolve;no requests/traces inside registry.

### PURE.InputManifest / version 1

| Required field | Exact type |
|---|---|
| `manifest_id` | `UUID` |
| `inputs` | `List1..16<InputItem>` |

InputItem={role:PROMPT|PROJECT|REFERENCE,object_id:UUID,revision:Pos,locator:Opaque,raw_sha256:Digest,byte_length:U}.Unique role/object_id;sorted by(role,object_id).These are declarations,not verified file observations.

### PURE.CapabilityProfile / version 1

| Required field | Exact type |
|---|---|
| `profile_id` | `UUID` |
| `handler_id` | `Text` |
| `provider_id` | `Text` |
| `model_id` | `Text` |
| `model_version` | `Text` |
| `region` | `Text` |
| `mode` | `T2V|I2V` |
| `registry_ref` | `Ref<FixtureRegistry>` |
| `limits` | `Limits` |

Supported profile exact handler=synthetic.video_anchor,OFFLINE_SIMULATOR_V1/SIM_WAN_PROFILE_V1/1/LOCAL_ONLY,T2V.Limits={jobs:16,workers:1,batch_entries:1,attempts:1,total_reads_per_checkpoint:3,events:128,outbox:32,request_bytes:1048576,script_events:64,virtual_ticks:10000}.Values are proposed pure bounds,not hardware qualification.

### PURE.NamespaceBinding / version 1

| Required field | Exact type |
|---|---|
| `store_id` | `UUID` |
| `ledger_id` | `UUID` |
| `root_scope_id` | `UUID` |
| `profile_ref` | `Ref<CapabilityProfile>` |

One configured namespace;root_scope_id is opaque fake scope,not a filesystem/security qualification.

### PURE.RequestIntent / version 1

| Required field | Exact type |
|---|---|
| `identity_context` | `IdentityContext` |
| `target_snapshot` | `TargetSnapshot` |
| `request` | `GenerationSpec` |

IdentityContext={project_id,scene_id,anchor_id,purpose_id:UUID}.TargetSnapshot={project_locator_ref:Opaque,expected_saved_json_sha256:Digest,expected_editor_snapshot_sha256:Digest,expected_anchor_token:Digest,generation_fingerprint:Digest,input_manifest_sha256:Digest}.GenerationSpec={provider_id:Text,model_id:Text,model_version:Text,region:Text,mode:T2V|I2V,prompt_reference:Opaque,prompt_sha256:Digest,duration_ms:Pos,resolution:{width:Pos,height:Pos},aspect_ratio:{num:Pos,den:Pos},input_assets:List0,provider_parameters:{fixture_id:UUID},capability_profile_ref:UUID,capability_profile_hash:Digest}.Limits duration1..120000,width/height even2..8192,ratio equals width/height;first profile exact cp and fixture membership.No batch,permit,job,fence,event or receipt in preimage.

### PURE.BatchManifest / version 1

| Required field | Exact type |
|---|---|
| `batch_id` | `UUID` |
| `batch_revision` | `Pos` |
| `entries` | `List1<BatchEntry>` |
| `policy` | `BatchPolicy` |

BatchEntry={project_id:UUID,purpose_id:UUID,request_ref:Ref<RequestIntent>}.BatchPolicy={max_jobs:1,max_attempts:1,currency:USD,max_job_spend_minor:0,max_batch_spend_minor:0,retention:KEEP_TEST_METADATA}.No permit or acceptance references.

### PURE.BatchPermit / version 1

| Required field | Exact type |
|---|---|
| `permit_id` | `UUID` |
| `grant_revision` | `Pos` |
| `manifest_ref` | `Ref<BatchManifest>` |
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `operation` | `=SYNTHETIC_GENERATION` |
| `authority_mode` | `=FAKE_ONLY` |
| `issuer_ref` | `=TRUSTED_TEST_HARNESS` |
| `valid_from_tick` | `U` |
| `valid_until_tick` | `Pos` |
| `rights_context` | `=UNVERIFIED_SYNTHETIC_METADATA` |

valid_from_tick<valid_until_tick;half-open validity;read-only historical replay does not renew grant.This is not B.1 production BatchPermit.No signature,real rights or clock field allowed.

### PURE.AdmissionKey / version 1

| Required field | Exact type |
|---|---|
| `store_id` | `UUID` |
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `project_id` | `UUID` |
| `purpose_id` | `UUID` |
| `request_ref` | `Ref<RequestIntent>` |
| `batch_id` | `UUID` |
| `batch_revision` | `Pos` |
| `batch_manifest_ref` | `Ref<BatchManifest>` |

All fields recomputed from resolved request/manifest/namespace;exact stored bytes also compared.No full-key uniqueness can replace active(project,purpose).

### PURE.AdmissionCommand / version 1

| Required field | Exact type |
|---|---|
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `key_ref` | `Ref<AdmissionKey>` |
| `request_ref` | `Ref<RequestIntent>` |
| `permit_ref` | `Ref<BatchPermit>` |

References bind same content/scope;new-key scope checking distinct from supplied-key mismatch.

### PURE.StoreMutationIntent / version 1

| Required field | Exact type |
|---|---|
| `mutation_id` | `UUID` |
| `mutation_kind` | `ADMIT|CLAIM|RENEW|STATE_CHANGE|APPLY_PROOF|CANCEL|INCIDENT|READ_RESERVE` |
| `job_id` | `?UUID` |
| `expected_revision` | `U` |
| `target_state` | `?State` |
| `input_ref` | `?Ref<HashKind>` |
| `cancel_requested` | `Bool` |

ADMIT:job_id=null,expected_revision=0,target_state=DRAFT,input_ref AdmissionCommand,cancel=false.Other kinds require job_id and expected_revision>=1.CLAIM/RENEW target_state=null,input_ref=null;APPLY_PROOF requires provider/result/nonaccept/cancel proof;INCIDENT requires JobError.CANCEL target_state=CANCEL_REQUESTED or guarded CANCELLED;READ_RESERVE target_state=null,input_ref=null.STATE_CHANGE uses allowed original edge and corresponding permit/effect/proof ref.No current fence in logical mutation identity.

### PURE.EffectPayload / version 1

| Required field | Exact type |
|---|---|
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `job_id` | `UUID` |
| `generation_operation_id` | `UUID` |
| `attempt_id` | `UUID` |
| `attempt_number` | `=1` |
| `effect_token` | `UUID` |
| `key_ref` | `Ref<AdmissionKey>` |
| `request_ref` | `Ref<RequestIntent>` |
| `permit_ref` | `Ref<BatchPermit>` |
| `fixture_id` | `UUID` |
| `operation` | `=SUBMIT_SYNTHETIC` |

Immutable generation identity across restart;no worker/controller incarnation,lease,mutation,event,outbox or delivery hash allowed.

### PURE.StoreEvent / version 1

| Required field | Exact type |
|---|---|
| `event_id` | `UUID` |
| `job_id` | `UUID` |
| `mutation_id` | `UUID` |
| `sequence` | `Pos` |
| `previous_event_ref` | `?Ref<StoreEvent>` |
| `state_from` | `?State` |
| `state_to` | `State` |
| `revision_from` | `U` |
| `revision_to` | `Pos` |
| `event_type` | `ADMITTED|LEASE_CLAIMED|LEASE_RENEWED|STATE_CHANGED|PROOF_APPLIED|CANCEL_REQUESTED|INCIDENT_RECORDED|READ_RESERVED` |
| `input_ref` | `?Ref<HashKind>` |
| `effect_payload_ref` | `?Ref<EffectPayload>` |
| `read_reservation` | `?ReadReservation` |

revision_to=revision_from+1;genesis ADMITTED:sequence1,fromnull,0→1,DRAFT,inputAdmissionCommand.Effect payload already exists before submit event.No receipt/outbox/job-record/atomic-write-set hash in event.ReadReservation={checkpoint_id:UUID,read_kind:LOOKUP|POLL,call_index:1..3,base_cursor:U};present only READ_RESERVED.

### PURE.AcceptanceReceipt / version 1

| Required field | Exact type |
|---|---|
| `receipt_id` | `UUID` |
| `store_id` | `UUID` |
| `job_id` | `UUID` |
| `created_mutation_id` | `UUID` |
| `key_ref` | `Ref<AdmissionKey>` |
| `request_ref` | `Ref<RequestIntent>` |
| `initial_permit_ref` | `Ref<BatchPermit>` |
| `accepted_job_revision` | `=1` |
| `accepted_store_sequence` | `Pos` |
| `acceptance_event_ref` | `Ref<StoreEvent>` |
| `commit_profile` | `=FAKE_STORE_NOT_DURABILITY_PROOF` |

Event precedes receipt;receipt cannot grant writer authority.REUSED exact canonical bytes of original receipt.

### PURE.OutboxEnvelope / version 1

| Required field | Exact type |
|---|---|
| `outbox_id` | `UUID` |
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `generation_operation_id` | `UUID` |
| `attempt_id` | `UUID` |
| `effect_token` | `UUID` |
| `payload_ref` | `Ref<EffectPayload>` |
| `owner_event_ref` | `Ref<StoreEvent>` |

Immutable dispatch intent;event references payload,not envelope.No mutable sent/ACK/current-fence flags in hashed envelope.Delivery command is a different nonhashable record.

### PURE.ProviderAcceptanceReceipt / version 1

| Required field | Exact type |
|---|---|
| `provider_receipt_id` | `UUID` |
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `ledger_id` | `UUID` |
| `ledger_sequence` | `Pos` |
| `provider_job_id` | `UUID` |
| `generation_operation_id` | `UUID` |
| `attempt_id` | `UUID` |
| `effect_token` | `UUID` |
| `payload_ref` | `Ref<EffectPayload>` |
| `accepted_tick` | `U` |
| `provider_cursor` | `Pos` |
| `billed_minor` | `=0` |
| `producer_qualification` | `=UNQUALIFIED_FAKE_ONLY` |

Ledger namespace/payload/all immutable IDs must match expected job;no caller fence or future acknowledgement-event hash.Only scripted fake proof-consumer semantics.

### PURE.ProviderResultReceipt / version 1

| Required field | Exact type |
|---|---|
| `result_id` | `UUID` |
| `acceptance_ref` | `Ref<ProviderAcceptanceReceipt>` |
| `generation_operation_id` | `UUID` |
| `attempt_id` | `UUID` |
| `effect_token` | `UUID` |
| `provider_job_id` | `UUID` |
| `resolved_profile_ref` | `Ref<CapabilityProfile>` |
| `fixture_ref` | `Ref<FixtureDescriptor>` |
| `provider_cursor` | `Pos` |
| `ready_tick` | `U` |
| `producer_qualification` | `=UNQUALIFIED_FAKE_ONLY` |

All association fields exact;cursor cannot regress;fixture metadata only,not MP4/rights/decoder proof.

### PURE.ProviderNonAcceptanceProof / version 1

| Required field | Exact type |
|---|---|
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `generation_operation_id` | `UUID` |
| `attempt_id` | `UUID` |
| `effect_token` | `UUID` |
| `payload_ref` | `Ref<EffectPayload>` |
| `ledger_sequence` | `U` |
| `observed_tick` | `U` |
| `outcome` | `=NOT_ACCEPTED` |
| `billed_minor` | `=0` |
| `producer_qualification` | `=UNQUALIFIED_FAKE_ONLY` |

Injected complete fake-ledger proof only;unknown/unavailable lookup cannot construct this record.Authority/identity checked before consuming proof.

### PURE.CancellationSettlementProof / version 1

| Required field | Exact type |
|---|---|
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `generation_operation_id` | `UUID` |
| `attempt_id` | `UUID` |
| `effect_token` | `UUID` |
| `settlement` | `NO_EFFECT|CANCELLED` |
| `provider_job_id` | `?UUID` |
| `external_effect` | `NONE|KNOWN` |
| `billed_minor` | `=0` |
| `settled_tick` | `U` |
| `producer_qualification` | `=UNQUALIFIED_FAKE_ONLY` |

NO_EFFECT→provider_job_id=null/external_effect=NONE;CANCELLED→provider_job_idnon-null/external_effect=KNOWN.Unknown cannot become settlement proof.

### PURE.JobError / version 1

| Required field | Exact type |
|---|---|
| `error_id` | `UUID` |
| `domain` | `=PURE_LOCAL` |
| `code` | `ErrorCode` |
| `occurred_at` | `?FakeInstant` |
| `state` | `?State` |
| `attempt` | `?UUID` |
| `operation` | `ErrorOperation` |
| `retry_class` | `NONE|SAFE_READ|SAFE_LOCAL|RECONCILE_ONLY` |
| `safe_message` | `MessageForCode` |
| `provider_status` | `?ProviderStatus` |
| `trace_redacted` | `=null` |
| `external_effect` | `NONE|KNOWN|UNKNOWN` |
| `billing` | `ZERO|SETTLED|RESERVED|UNKNOWN` |
| `evidence_ref` | `?Ref<HashKind>` |
| `required_action` | `ErrorAction` |

Wire field is external_effect,never effect.FakeInstant={clock_epoch_id:UUID,tick:U};null only CLOCK_UNQUALIFIED.Durable model error only via current-owner separate lawful mutation,not by rejected caller.

### PURE.ActiveSlot / version 1

| Required field | Exact type |
|---|---|
| `store_id` | `UUID` |
| `project_id` | `UUID` |
| `purpose_id` | `UUID` |
| `job_id` | `UUID` |
| `key_ref` | `Ref<AdmissionKey>` |
| `status` | `HELD|RELEASED` |
| `occupied_since_revision` | `Pos` |
| `released_at_revision` | `?Pos` |

HELD requiresnullrelease;RELEASED requires terminal proof andsame atomic set withterminal job revision>=occupied.UniqueHELD(store_id,project_id,purpose_id);history retained.RESULT_AVAILABLE holds slot.

### PURE.JobRecord / version 1

| Required field | Exact type |
|---|---|
| `job_id` | `UUID` |
| `created_mutation_id` | `UUID` |
| `last_mutation_id` | `UUID` |
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `key_ref` | `Ref<AdmissionKey>` |
| `request_ref` | `Ref<RequestIntent>` |
| `initial_permit_ref` | `Ref<BatchPermit>` |
| `state` | `State` |
| `revision` | `Pos` |
| `cancel_requested` | `Bool` |
| `generation_operation_id` | `?UUID` |
| `attempt_id` | `?UUID` |
| `effect_token` | `?UUID` |
| `last_event_ref` | `Ref<StoreEvent>` |
| `last_error_ref` | `?Ref<JobError>` |
| `result_ref` | `?Ref<ProviderResultReceipt>` |
| `active_slot_ref` | `Ref<ActiveSlot>` |
| `controller_incarnation` | `U` |
| `worker_id` | `?UUID` |
| `lease_epoch` | `U` |
| `lease_until_tick` | `?U` |
| `clock_epoch_id` | `?UUID` |
| `provider_cursor` | `U` |
| `read_checkpoint` | `?ReadCheckpoint` |

No fake authority from metadata.ReadCheckpoint={checkpoint_id:UUID,read_kind:LOOKUP|POLL,base_cursor:U,calls_used:0..3,max_calls:3}.Job/controller/workerfields may change only under current fenced CAS;never enter EffectPayload hash.Gen/attempt/effect all null before submit,allnon-null after submit.

### PURE.AtomicWriteSet / version 1

| Required field | Exact type |
|---|---|
| `mutation_ref` | `Ref<StoreMutationIntent>` |
| `job_id` | `UUID` |
| `base_revision` | `U` |
| `result_revision` | `Pos` |
| `members` | `List1..8<Ref<HashKind>>` |
| `active_slot_action` | `ACQUIRE|RETAIN|RELEASE` |
| `store_sequence` | `Pos` |

Members unique/sorted by(kind,digest).ADMIT exact Event+Receipt+SlotHELD+JobRecord;transition exact Event+JobRecord pluschangedSlot/Error/Outbox as declared.One original mutation links all members;no member includes this write-set hash.No own marker digest/commit result.

### PURE.MutationAbsenceProof / version 1

| Required field | Exact type |
|---|---|
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `mutation_ref` | `Ref<StoreMutationIntent>` |
| `snapshot_generation` | `U` |
| `lookup_complete` | `=true` |
| `marker_present` | `=false` |
| `members_for_mutation_present` | `=false` |
| `qualification` | `=FAKE_STORE_READ_ONLY_EVIDENCE` |

All mutation-linked memberschecked inonecompleteconsistent fakeview;missing marker alone insufficient.Native absence qualification unsupported.

### PURE.CommitResolutionProof / version 1

| Required field | Exact type |
|---|---|
| `namespace_ref` | `Ref<NamespaceBinding>` |
| `mutation_ref` | `Ref<StoreMutationIntent>` |
| `outcome` | `COMMITTED|NOT_COMMITTED` |
| `write_set_ref` | `?Ref<AtomicWriteSet>` |
| `absence_ref` | `?Ref<MutationAbsenceProof>` |
| `snapshot_generation` | `U` |
| `qualification` | `=FAKE_STORE_READ_ONLY_EVIDENCE` |

COMMITTED→write_setref only;NOT_COMMITTED→absenceref only;allbindingssame mutation.UNKNOWN hasno proofrecord.Contradictory/incomplete set gives STORE_CORRUPT/UNKNOWN,not rollback.

## Additional closure rules

`State` is exactly the B.1 22-state vocabulary: DRAFT, AWAITING_APPROVAL, APPROVED, QUEUED, SUBMITTING, SUBMISSION_UNCERTAIN, RUNNING, RESULT_AVAILABLE, DOWNLOADING, VALIDATING, ASSET_COMMITTED, ATTACH_PENDING, COMPLETED, PAUSED_QUOTA, PAUSED_BUDGET, PAUSED_RIGHTS, STALE_TARGET, RETRY_WAIT, CANCEL_REQUESTED, CANCELLED, FAILED, NEEDS_RECONCILIATION. Recognizing a state does not authorize a transition or implement deferred stages.

Inline shapes in the registry are closed too. TargetSnapshot's `input_manifest_sha256` must equal H(resolved InputManifest); capability_profile_hash equals H(resolved CapabilityProfile), capability_profile_ref equals its profile_id; all fixture references resolve within its registry. Request project/purpose must match the sole BatchEntry and AdmissionKey; batch IDs/revisions and all namespace references must match. Ratio numerator/denominator must be reduced positive integers and width*den=height*num. Mode I2V is recognized by schema but not allowed by the sole proposed T2V capability profile. No input media ingestion is provided.

StoreMutationIntent is a logical mutation identity, not writer authority. Reusing mutation_id with a different intent is OPERATION_ID_CONFLICT. ADMIT's allocated job_id is recorded in its AtomicWriteSet. CLAIM/RENEW retain state and cancellation flag; input_ref is null. READ_RESERVE retains state and flag; reservation details live in the linked READ_RESERVED event. CANCEL sets cancel_requested=true. APPLY_PROOF takes exactly ProviderAcceptanceReceipt, ProviderResultReceipt, ProviderNonAcceptanceProof or CancellationSettlementProof. INCIDENT takes exactly JobError and retains state. STATE_CHANGE takes BatchPermit on approval/queue, EffectPayload on submit, or a relevant verified proof on settlement; other generic transitions are not enabled in the initial pure scope.

Every mutation except ADMIT has expected_revision>=1 and exact current job_id. Event input_ref matches mutation input_ref; from/to and revisions match the job transition. Every event increments job revision by one, including claim/renew/read-reserve; a same-state event is not an unguarded lifecycle edge. Sequence increases by one from the prior event; revision_from matches its revision_to. Event/mutation/job IDs and store sequence must be consistent across the entire write set. ADMIT members are exactly event, original receipt, HELD slot and initial job. A normal mutation includes event and new job; add a changed slot only on acquisition/release, JobError only for INCIDENT, and OutboxEnvelope only on first submit. The immutable payload is already resolved before submit; submit atomically records event/job/outbox before any fake effect. Acceptance receipt is never rewritten. Every member links to the same job/mutation by its declared references/IDs; a stale unchanged ActiveSlot is a referenced historical record, not a new member. Marker visibility without all required members is corruption, never committed proof.

JobError auxiliary enums: ErrorOperation = ADMIT|OBSERVE|CLAIM|RENEW|SUBMIT|LOOKUP|POLL|APPLY_PROOF|CANCEL|RESOLVE_COMMIT|INCIDENT; ProviderStatus = ACCEPTED|RUNNING|RESULT_AVAILABLE|NOT_ACCEPTED|CANCELLED|FAILED|UNKNOWN; ErrorAction = FIX_INPUT|REAUTHORIZE|RELOAD|RECONCILE|STOP. ErrorCode and MessageForCode are closed by ERROR_AND_ORACLE_MATRIX.md. A durable JobError requires known state and operation; attempt is null only before generation identity exists, provider_status null if no provider observation, evidence_ref null if none. occurred_at is null only for CLOCK_UNQUALIFIED. No secrets/raw provider traceback are permitted.

## Nonhashable boundary records

These are transport/observation objects, have no H and must never be substituted into Ref<HashKind>. Each has common kind=`PURE.<name>`, version=1, scope=PURE_FAKE_ONLY; exactly the additional keys below. Nested inline tokens have only listed keys, no common header.

| Name | Required fields and types |
|---|---|
| ControllerFence | store_id:UUID, controller_id:UUID, incarnation:Pos, clock_epoch_id:UUID |
| WorkerFence | controller: inline ControllerFence fields, job_id:UUID, worker_id:UUID, lease_epoch:Pos, lease_until_tick:U |
| DeliveryCommand | outbox_ref:Ref<OutboxEnvelope>, payload_ref:Ref<EffectPayload>, fence:inline WorkerFence fields, expected_revision:Pos |
| ReadRequest | payload_ref:Ref<EffectPayload>, effect_token:UUID, checkpoint_id:UUID, read_kind:LOOKUP or POLL, cursor:U, reserved_call_index:1..3, fence:inline WorkerFence fields, expected_revision:Pos |
| ResponseError | code:ErrorCode, operation:ErrorOperation, safe_message:MessageForCode, external_effect:NONE or KNOWN or UNKNOWN, billing:ZERO or SETTLED or RESERVED or UNKNOWN, required_action:ErrorAction |
| APIOutcome | disposition:ACCEPTED or REUSED or APPLIED or REJECTED or HOLD or OBSERVED, mutation_outcome:null or COMMITTED or NOT_COMMITTED or UNKNOWN_COMMIT_OUTCOME, receipt_ref:?Ref<AcceptanceReceipt>, job_ref:?Ref<JobRecord>, error:?inline ResponseError fields |
| ObserverSnapshot | namespace_ref:Ref<NamespaceBinding>, job_ref:?Ref<JobRecord>, cursor:U, barriers:List0..1<UNKNOWN_COMMIT_OUTCOME or STORE_UNAVAILABLE or STORE_CORRUPT or CLOCK_UNQUALIFIED>, pipeline_complete:false |

APIOutcome ACCEPTED requires COMMITTED and original receipt; REUSED has mutation_outcome=null and original receipt; APPLIED requires COMMITTED; REJECTED has ResponseError and null if no mutation attempted or NOT_COMMITTED if conclusively attempted without commit. HOLD has error; UNKNOWN commit always disposition HOLD and mutation_outcome UNKNOWN_COMMIT_OUTCOME. OBSERVED is read-only with null mutation_outcome. Observer cannot report success while hiding a barrier; no job may be returned as NOT_FOUND on an unreadable store. Null mutation_outcome means no mutation was attempted, not a fourth store commit outcome. Only currently authorized transport commands can carry a fence; a hashed receipt cannot mint one.

Unsupported construction: real BatchPermit/signatures, PG authorizations, native clock/OS locks, live provider receipts, MP4 fixture/decoder/rights proofs, asset/save completion receipts, wait results and native absence proofs. They must fail OPERATION_NOT_AVAILABLE or PROFILE_UNQUALIFIED; do not synthesize hashes, use null stand-ins or reinterpret metadata as qualification.

## Fixed byte vectors

36 document value examples cover 25 kinds and an acyclic submit prefix. Each canonical block below has **no trailing newline in the hash input**. Nonacceptance/settlement and absence examples describe alternative fake histories; they do not assert a single ledger simultaneously accepted and rejected the same effect. These are value/arithmetic examples, not executed state-machine traces or valid production evidence.

### V001 — PURE.FixtureDescriptor

Bytes: 247; SHA-256: `ef3fe6b9923c54f1871d5f05a346ee370993edf90b5203aa984ceb0ed7418044`.

```json
{"content_class": "SYNTHETIC_METADATA", "fixture_id": "00000000-0000-0000-0000-000000000014", "kind": "PURE.FixtureDescriptor", "label": "Рынок 🎞", "producer_qualification": "UNQUALIFIED_FAKE_ONLY", "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V002 — PURE.FixtureRegistry

Bytes: 256; SHA-256: `971fc3e55dd7736fcf1395097bb7ecce7646e1679b4f521a04ef5def105ae07f`.

```json
{"fixtures": [{"digest": "ef3fe6b9923c54f1871d5f05a346ee370993edf90b5203aa984ceb0ed7418044", "kind": "PURE.FixtureDescriptor"}], "kind": "PURE.FixtureRegistry", "registry_id": "00000000-0000-0000-0000-000000000015", "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V003 — PURE.InputManifest

Bytes: 356; SHA-256: `17407dea37613a0c5537e03a682a8243c959ac64257e6ed0dae09f70c7d4b205`.

```json
{"inputs": [{"byte_length": 21, "locator": "fixture:prompt", "object_id": "00000000-0000-0000-0000-000000000017", "raw_sha256": "e722948a4d8676a6e44cf9825f17d6eb9189a64055557ee9ab46ec049a644152", "revision": 1, "role": "PROMPT"}], "kind": "PURE.InputManifest", "manifest_id": "00000000-0000-0000-0000-000000000016", "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V004 — PURE.CapabilityProfile

Bytes: 637; SHA-256: `a08c2c0e7d65fe05e571ac9aabfd5d6db21e2be4e07caf45234dae0bb8afb9c8`.

```json
{"handler_id": "synthetic.video_anchor", "kind": "PURE.CapabilityProfile", "limits": {"attempts": 1, "batch_entries": 1, "events": 128, "jobs": 16, "outbox": 32, "request_bytes": 1048576, "script_events": 64, "total_reads_per_checkpoint": 3, "virtual_ticks": 10000, "workers": 1}, "mode": "T2V", "model_id": "SIM_WAN_PROFILE_V1", "model_version": "1", "profile_id": "00000000-0000-0000-0000-000000000018", "provider_id": "OFFLINE_SIMULATOR_V1", "region": "LOCAL_ONLY", "registry_ref": {"digest": "971fc3e55dd7736fcf1395097bb7ecce7646e1679b4f521a04ef5def105ae07f", "kind": "PURE.FixtureRegistry"}, "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V005 — PURE.NamespaceBinding

Bytes: 365; SHA-256: `5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda`.

```json
{"kind": "PURE.NamespaceBinding", "ledger_id": "00000000-0000-0000-0000-000000000002", "profile_ref": {"digest": "a08c2c0e7d65fe05e571ac9aabfd5d6db21e2be4e07caf45234dae0bb8afb9c8", "kind": "PURE.CapabilityProfile"}, "root_scope_id": "00000000-0000-0000-0000-000000000019", "scope": "PURE_FAKE_ONLY", "store_id": "00000000-0000-0000-0000-000000000001", "version": 1}
```

### V006 — PURE.RequestIntent

Bytes: 1484; SHA-256: `b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518`.

```json
{"identity_context": {"anchor_id": "00000000-0000-0000-0000-000000000005", "project_id": "00000000-0000-0000-0000-000000000003", "purpose_id": "00000000-0000-0000-0000-000000000006", "scene_id": "00000000-0000-0000-0000-000000000004"}, "kind": "PURE.RequestIntent", "request": {"aspect_ratio": {"den": 1, "num": 1}, "capability_profile_hash": "a08c2c0e7d65fe05e571ac9aabfd5d6db21e2be4e07caf45234dae0bb8afb9c8", "capability_profile_ref": "00000000-0000-0000-0000-000000000018", "duration_ms": 1000, "input_assets": [], "mode": "T2V", "model_id": "SIM_WAN_PROFILE_V1", "model_version": "1", "prompt_reference": "fixture:prompt", "prompt_sha256": "e722948a4d8676a6e44cf9825f17d6eb9189a64055557ee9ab46ec049a644152", "provider_id": "OFFLINE_SIMULATOR_V1", "provider_parameters": {"fixture_id": "00000000-0000-0000-0000-000000000014"}, "region": "LOCAL_ONLY", "resolution": {"height": 512, "width": 512}}, "scope": "PURE_FAKE_ONLY", "target_snapshot": {"expected_anchor_token": "4b2e9155795f3a7b24d30852760ff1e20858af45783850ecd6fc0f4ae6fd85ed", "expected_editor_snapshot_sha256": "ff964a29eec122e5cc481a3fd68e42ab6356130fbe90ede46dfaad784f8a1178", "expected_saved_json_sha256": "64d54f9fbe4dc269e6ea16ff74dd2fed71c078247c400ae4a7c3fc0db31fd648", "generation_fingerprint": "044c34fd40b0b1f4c0ab7dca7a5ea4724fe9974698b5b6efbb6fdbfd04dae0d5", "input_manifest_sha256": "17407dea37613a0c5537e03a682a8243c959ac64257e6ed0dae09f70c7d4b205", "project_locator_ref": "fixture:project"}, "version": 1}
```

### V007 — PURE.BatchManifest

Bytes: 546; SHA-256: `7c163ff84509145ee4dadd3d76e3df998493dd5db68890478fe361da7109d546`.

```json
{"batch_id": "00000000-0000-0000-0000-000000000020", "batch_revision": 1, "entries": [{"project_id": "00000000-0000-0000-0000-000000000003", "purpose_id": "00000000-0000-0000-0000-000000000006", "request_ref": {"digest": "b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518", "kind": "PURE.RequestIntent"}}], "kind": "PURE.BatchManifest", "policy": {"currency": "USD", "max_attempts": 1, "max_batch_spend_minor": 0, "max_job_spend_minor": 0, "max_jobs": 1, "retention": "KEEP_TEST_METADATA"}, "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V008 — PURE.BatchPermit

Bytes: 603; SHA-256: `5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432`.

```json
{"authority_mode": "FAKE_ONLY", "grant_revision": 1, "issuer_ref": "TRUSTED_TEST_HARNESS", "kind": "PURE.BatchPermit", "manifest_ref": {"digest": "7c163ff84509145ee4dadd3d76e3df998493dd5db68890478fe361da7109d546", "kind": "PURE.BatchManifest"}, "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "operation": "SYNTHETIC_GENERATION", "permit_id": "00000000-0000-0000-0000-000000000021", "rights_context": "UNVERIFIED_SYNTHETIC_METADATA", "scope": "PURE_FAKE_ONLY", "valid_from_tick": 0, "valid_until_tick": 100, "version": 1}
```

### V009 — PURE.AdmissionKey

Bytes: 690; SHA-256: `738406ef1cac9fad9d9904d05d5fbae7a98ae1f3246bd65ebdf0f198d0a81d38`.

```json
{"batch_id": "00000000-0000-0000-0000-000000000020", "batch_manifest_ref": {"digest": "7c163ff84509145ee4dadd3d76e3df998493dd5db68890478fe361da7109d546", "kind": "PURE.BatchManifest"}, "batch_revision": 1, "kind": "PURE.AdmissionKey", "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "project_id": "00000000-0000-0000-0000-000000000003", "purpose_id": "00000000-0000-0000-0000-000000000006", "request_ref": {"digest": "b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518", "kind": "PURE.RequestIntent"}, "scope": "PURE_FAKE_ONLY", "store_id": "00000000-0000-0000-0000-000000000001", "version": 1}
```

### V010 — PURE.AdmissionCommand

Bytes: 571; SHA-256: `10f4bab943161eee53ad4bfc626a5b65ab06f3dba3f18c2aa365144416c0e872`.

```json
{"key_ref": {"digest": "738406ef1cac9fad9d9904d05d5fbae7a98ae1f3246bd65ebdf0f198d0a81d38", "kind": "PURE.AdmissionKey"}, "kind": "PURE.AdmissionCommand", "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "permit_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "request_ref": {"digest": "b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518", "kind": "PURE.RequestIntent"}, "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V011 — PURE.StoreMutationIntent

Bytes: 376; SHA-256: `a7f03bbcaa2198337870f4f1e50c60954b9ac035085ebef7e038e0aad121bd83`.

```json
{"cancel_requested": false, "expected_revision": 0, "input_ref": {"digest": "10f4bab943161eee53ad4bfc626a5b65ab06f3dba3f18c2aa365144416c0e872", "kind": "PURE.AdmissionCommand"}, "job_id": null, "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000008", "mutation_kind": "ADMIT", "scope": "PURE_FAKE_ONLY", "target_state": "DRAFT", "version": 1}
```

### V012 — PURE.EffectPayload

Bytes: 903; SHA-256: `ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b`.

```json
{"attempt_id": "00000000-0000-0000-0000-000000000012", "attempt_number": 1, "effect_token": "00000000-0000-0000-0000-000000000013", "fixture_id": "00000000-0000-0000-0000-000000000014", "generation_operation_id": "00000000-0000-0000-0000-000000000011", "job_id": "00000000-0000-0000-0000-000000000007", "key_ref": {"digest": "738406ef1cac9fad9d9904d05d5fbae7a98ae1f3246bd65ebdf0f198d0a81d38", "kind": "PURE.AdmissionKey"}, "kind": "PURE.EffectPayload", "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "operation": "SUBMIT_SYNTHETIC", "permit_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "request_ref": {"digest": "b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518", "kind": "PURE.RequestIntent"}, "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V013 — PURE.StoreEvent

Bytes: 553; SHA-256: `cabc72ffd5cd030d7d8af2d59cfab72bccda4ef760b297059d16ffe3e454efb8`.

```json
{"effect_payload_ref": null, "event_id": "00000000-0000-0000-0000-000000000022", "event_type": "ADMITTED", "input_ref": {"digest": "10f4bab943161eee53ad4bfc626a5b65ab06f3dba3f18c2aa365144416c0e872", "kind": "PURE.AdmissionCommand"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreEvent", "mutation_id": "00000000-0000-0000-0000-000000000008", "previous_event_ref": null, "read_reservation": null, "revision_from": 0, "revision_to": 1, "scope": "PURE_FAKE_ONLY", "sequence": 1, "state_from": null, "state_to": "DRAFT", "version": 1}
```

### V014 — PURE.AcceptanceReceipt

Bytes: 911; SHA-256: `9cc2b8e9eb5209721b2ebfe0ae81d23199ec93c4e2a5b7dc0399ee8380df7dc7`.

```json
{"acceptance_event_ref": {"digest": "cabc72ffd5cd030d7d8af2d59cfab72bccda4ef760b297059d16ffe3e454efb8", "kind": "PURE.StoreEvent"}, "accepted_job_revision": 1, "accepted_store_sequence": 1, "commit_profile": "FAKE_STORE_NOT_DURABILITY_PROOF", "created_mutation_id": "00000000-0000-0000-0000-000000000008", "initial_permit_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "key_ref": {"digest": "738406ef1cac9fad9d9904d05d5fbae7a98ae1f3246bd65ebdf0f198d0a81d38", "kind": "PURE.AdmissionKey"}, "kind": "PURE.AcceptanceReceipt", "receipt_id": "00000000-0000-0000-0000-000000000023", "request_ref": {"digest": "b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518", "kind": "PURE.RequestIntent"}, "scope": "PURE_FAKE_ONLY", "store_id": "00000000-0000-0000-0000-000000000001", "version": 1}
```

### V_EXTRA_MUT_2 — PURE.StoreMutationIntent

Bytes: 424; SHA-256: `b66085fe6708c7fb896ca9823fefefe3ae019dc842f6050ae90dfa403bc4cf98`.

```json
{"cancel_requested": false, "expected_revision": 1, "input_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000102", "mutation_kind": "STATE_CHANGE", "scope": "PURE_FAKE_ONLY", "target_state": "AWAITING_APPROVAL", "version": 1}
```

### V_EXTRA_EVENT_2 — PURE.StoreEvent

Bytes: 669; SHA-256: `05c9b566865f9d927e093e2069a866584b3ca7425acce16bf7423d9aea579a00`.

```json
{"effect_payload_ref": null, "event_id": "00000000-0000-0000-0000-000000000202", "event_type": "STATE_CHANGED", "input_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreEvent", "mutation_id": "00000000-0000-0000-0000-000000000102", "previous_event_ref": {"digest": "cabc72ffd5cd030d7d8af2d59cfab72bccda4ef760b297059d16ffe3e454efb8", "kind": "PURE.StoreEvent"}, "read_reservation": null, "revision_from": 1, "revision_to": 2, "scope": "PURE_FAKE_ONLY", "sequence": 2, "state_from": "DRAFT", "state_to": "AWAITING_APPROVAL", "version": 1}
```

### V_EXTRA_MUT_3 — PURE.StoreMutationIntent

Bytes: 415; SHA-256: `f9c38e9ee00805cd78d89e1cb0bc78920b00720c7c34a9a7cb61f83664bbcc25`.

```json
{"cancel_requested": false, "expected_revision": 2, "input_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000103", "mutation_kind": "STATE_CHANGE", "scope": "PURE_FAKE_ONLY", "target_state": "APPROVED", "version": 1}
```

### V_EXTRA_EVENT_3 — PURE.StoreEvent

Bytes: 672; SHA-256: `db20a86b5377181b6d568cc5e6b8deb9ec146c01346c5b790c9192a54cc60f54`.

```json
{"effect_payload_ref": null, "event_id": "00000000-0000-0000-0000-000000000203", "event_type": "STATE_CHANGED", "input_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreEvent", "mutation_id": "00000000-0000-0000-0000-000000000103", "previous_event_ref": {"digest": "05c9b566865f9d927e093e2069a866584b3ca7425acce16bf7423d9aea579a00", "kind": "PURE.StoreEvent"}, "read_reservation": null, "revision_from": 2, "revision_to": 3, "scope": "PURE_FAKE_ONLY", "sequence": 3, "state_from": "AWAITING_APPROVAL", "state_to": "APPROVED", "version": 1}
```

### V_EXTRA_MUT_4 — PURE.StoreMutationIntent

Bytes: 413; SHA-256: `44efd8ac27c5ab06df0c5cd5c293c0c3019db5451458d4714caa03889b4babd2`.

```json
{"cancel_requested": false, "expected_revision": 3, "input_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000104", "mutation_kind": "STATE_CHANGE", "scope": "PURE_FAKE_ONLY", "target_state": "QUEUED", "version": 1}
```

### V_EXTRA_EVENT_4 — PURE.StoreEvent

Bytes: 661; SHA-256: `5979279173f441780f03f03443f3cb56b9fa87dc8f24c5b9a31bf04a794702b4`.

```json
{"effect_payload_ref": null, "event_id": "00000000-0000-0000-0000-000000000204", "event_type": "STATE_CHANGED", "input_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreEvent", "mutation_id": "00000000-0000-0000-0000-000000000104", "previous_event_ref": {"digest": "db20a86b5377181b6d568cc5e6b8deb9ec146c01346c5b790c9192a54cc60f54", "kind": "PURE.StoreEvent"}, "read_reservation": null, "revision_from": 3, "revision_to": 4, "scope": "PURE_FAKE_ONLY", "sequence": 4, "state_from": "APPROVED", "state_to": "QUEUED", "version": 1}
```

### V_EXTRA_MUT_5 — PURE.StoreMutationIntent

Bytes: 300; SHA-256: `64e70ffd067a073123748da7af320925b43821bc307398dce2eaae614669b6bf`.

```json
{"cancel_requested": false, "expected_revision": 4, "input_ref": null, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000105", "mutation_kind": "CLAIM", "scope": "PURE_FAKE_ONLY", "target_state": null, "version": 1}
```

### V_EXTRA_EVENT_5 — PURE.StoreEvent

Bytes: 557; SHA-256: `af11e2528538b49ca44e93d8e2477699f016661c94b736ab1307866c86af0449`.

```json
{"effect_payload_ref": null, "event_id": "00000000-0000-0000-0000-000000000205", "event_type": "LEASE_CLAIMED", "input_ref": null, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreEvent", "mutation_id": "00000000-0000-0000-0000-000000000105", "previous_event_ref": {"digest": "5979279173f441780f03f03443f3cb56b9fa87dc8f24c5b9a31bf04a794702b4", "kind": "PURE.StoreEvent"}, "read_reservation": null, "revision_from": 4, "revision_to": 5, "scope": "PURE_FAKE_ONLY", "sequence": 5, "state_from": "QUEUED", "state_to": "QUEUED", "version": 1}
```

### V_EXTRA_MUT_6 — PURE.StoreMutationIntent

Bytes: 419; SHA-256: `af43149e0f78bc06befe55ba306016b60c037d26d0e6f161e435778bc9bb6556`.

```json
{"cancel_requested": false, "expected_revision": 5, "input_ref": {"digest": "ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b", "kind": "PURE.EffectPayload"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000106", "mutation_kind": "STATE_CHANGE", "scope": "PURE_FAKE_ONLY", "target_state": "SUBMITTING", "version": 1}
```

### V_EXTRA_EVENT_6 — PURE.StoreEvent

Bytes: 769; SHA-256: `c48c2104df51eba7e50e11a4fb8d8e3ebadd4512c42c8b48f8cc28c592618fff`.

```json
{"effect_payload_ref": {"digest": "ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b", "kind": "PURE.EffectPayload"}, "event_id": "00000000-0000-0000-0000-000000000206", "event_type": "STATE_CHANGED", "input_ref": {"digest": "ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b", "kind": "PURE.EffectPayload"}, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.StoreEvent", "mutation_id": "00000000-0000-0000-0000-000000000106", "previous_event_ref": {"digest": "af11e2528538b49ca44e93d8e2477699f016661c94b736ab1307866c86af0449", "kind": "PURE.StoreEvent"}, "read_reservation": null, "revision_from": 5, "revision_to": 6, "scope": "PURE_FAKE_ONLY", "sequence": 6, "state_from": "QUEUED", "state_to": "SUBMITTING", "version": 1}
```

### V025 — PURE.OutboxEnvelope

Bytes: 683; SHA-256: `951248ed11204fd86af959aee9f9513c43ef0bf0ef5acded6c3a0fb5bda712af`.

```json
{"attempt_id": "00000000-0000-0000-0000-000000000012", "effect_token": "00000000-0000-0000-0000-000000000013", "generation_operation_id": "00000000-0000-0000-0000-000000000011", "kind": "PURE.OutboxEnvelope", "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "outbox_id": "00000000-0000-0000-0000-000000000024", "owner_event_ref": {"digest": "c48c2104df51eba7e50e11a4fb8d8e3ebadd4512c42c8b48f8cc28c592618fff", "kind": "PURE.StoreEvent"}, "payload_ref": {"digest": "ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b", "kind": "PURE.EffectPayload"}, "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V026 — PURE.ProviderAcceptanceReceipt

Bytes: 824; SHA-256: `70d151ac3a194b631943ee71c690f1dde43dbc04698163edcb580dfdd88d6a32`.

```json
{"accepted_tick": 1, "attempt_id": "00000000-0000-0000-0000-000000000012", "billed_minor": 0, "effect_token": "00000000-0000-0000-0000-000000000013", "generation_operation_id": "00000000-0000-0000-0000-000000000011", "kind": "PURE.ProviderAcceptanceReceipt", "ledger_id": "00000000-0000-0000-0000-000000000002", "ledger_sequence": 1, "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "payload_ref": {"digest": "ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b", "kind": "PURE.EffectPayload"}, "producer_qualification": "UNQUALIFIED_FAKE_ONLY", "provider_cursor": 1, "provider_job_id": "00000000-0000-0000-0000-000000000026", "provider_receipt_id": "00000000-0000-0000-0000-000000000025", "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V027 — PURE.ProviderResultReceipt

Bytes: 865; SHA-256: `8e85eb640050eadd395b1131cd9bea80eabef45f466354c720c8b724c9a74dc0`.

```json
{"acceptance_ref": {"digest": "70d151ac3a194b631943ee71c690f1dde43dbc04698163edcb580dfdd88d6a32", "kind": "PURE.ProviderAcceptanceReceipt"}, "attempt_id": "00000000-0000-0000-0000-000000000012", "effect_token": "00000000-0000-0000-0000-000000000013", "fixture_ref": {"digest": "ef3fe6b9923c54f1871d5f05a346ee370993edf90b5203aa984ceb0ed7418044", "kind": "PURE.FixtureDescriptor"}, "generation_operation_id": "00000000-0000-0000-0000-000000000011", "kind": "PURE.ProviderResultReceipt", "producer_qualification": "UNQUALIFIED_FAKE_ONLY", "provider_cursor": 2, "provider_job_id": "00000000-0000-0000-0000-000000000026", "ready_tick": 2, "resolved_profile_ref": {"digest": "a08c2c0e7d65fe05e571ac9aabfd5d6db21e2be4e07caf45234dae0bb8afb9c8", "kind": "PURE.CapabilityProfile"}, "result_id": "00000000-0000-0000-0000-000000000027", "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V028 — PURE.ProviderNonAcceptanceProof

Bytes: 655; SHA-256: `cf41849733cab4bbc7c21d71acc6a3451b0d26e7670e6eaa11a0c661044f83b6`.

```json
{"attempt_id": "00000000-0000-0000-0000-000000000012", "billed_minor": 0, "effect_token": "00000000-0000-0000-0000-000000000013", "generation_operation_id": "00000000-0000-0000-0000-000000000011", "kind": "PURE.ProviderNonAcceptanceProof", "ledger_sequence": 0, "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "observed_tick": 2, "outcome": "NOT_ACCEPTED", "payload_ref": {"digest": "ab7e33c2d52c3da6841598a48c082909bd01ad4db796337bbc7b4d3f70a6b23b", "kind": "PURE.EffectPayload"}, "producer_qualification": "UNQUALIFIED_FAKE_ONLY", "scope": "PURE_FAKE_ONLY", "version": 1}
```

### V029 — PURE.CancellationSettlementProof

Bytes: 595; SHA-256: `650416657101e112f1fc67d22dbb248393754980c4886b103eecd5844acf2f08`.

```json
{"attempt_id": "00000000-0000-0000-0000-000000000012", "billed_minor": 0, "effect_token": "00000000-0000-0000-0000-000000000013", "external_effect": "KNOWN", "generation_operation_id": "00000000-0000-0000-0000-000000000011", "kind": "PURE.CancellationSettlementProof", "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "producer_qualification": "UNQUALIFIED_FAKE_ONLY", "provider_job_id": "00000000-0000-0000-0000-000000000026", "scope": "PURE_FAKE_ONLY", "settled_tick": 3, "settlement": "CANCELLED", "version": 1}
```

### V030 — PURE.JobError

Bytes: 530; SHA-256: `4f029054d2ddcfab31ce93c4f428fcd198cc9eb1fd20f71136cf6fd0f30c8374`.

```json
{"attempt": null, "billing": "ZERO", "code": "STALE_WORKER_FENCE", "domain": "PURE_LOCAL", "error_id": "00000000-0000-0000-0000-000000000031", "evidence_ref": null, "external_effect": "NONE", "kind": "PURE.JobError", "occurred_at": {"clock_epoch_id": "00000000-0000-0000-0000-000000000009", "tick": 2}, "operation": "INCIDENT", "provider_status": null, "required_action": "INSPECT", "retry_class": "NONE", "safe_message": "Worker fence is stale.", "scope": "PURE_FAKE_ONLY", "state": "DRAFT", "trace_redacted": null, "version": 1}
```

### V031 — PURE.ActiveSlot

Bytes: 476; SHA-256: `1d1f9b1b7b0197efe5d2e55cc5dc6e3b52fdbb1b4c584655c7cffda7e5e6941e`.

```json
{"job_id": "00000000-0000-0000-0000-000000000007", "key_ref": {"digest": "738406ef1cac9fad9d9904d05d5fbae7a98ae1f3246bd65ebdf0f198d0a81d38", "kind": "PURE.AdmissionKey"}, "kind": "PURE.ActiveSlot", "occupied_since_revision": 1, "project_id": "00000000-0000-0000-0000-000000000003", "purpose_id": "00000000-0000-0000-0000-000000000006", "released_at_revision": null, "scope": "PURE_FAKE_ONLY", "status": "HELD", "store_id": "00000000-0000-0000-0000-000000000001", "version": 1}
```

### V032 — PURE.JobRecord

Bytes: 1338; SHA-256: `560aeeeba5e49a92a04006161ed86385d4e13a423de50c464cf68f18f6a7f5c5`.

```json
{"active_slot_ref": {"digest": "1d1f9b1b7b0197efe5d2e55cc5dc6e3b52fdbb1b4c584655c7cffda7e5e6941e", "kind": "PURE.ActiveSlot"}, "attempt_id": null, "cancel_requested": false, "clock_epoch_id": null, "controller_incarnation": 1, "created_mutation_id": "00000000-0000-0000-0000-000000000008", "effect_token": null, "generation_operation_id": null, "initial_permit_ref": {"digest": "5126d369992c15385edfef0f7fcfdaf4ad7e9d0f39dc157a8de8cbc138769432", "kind": "PURE.BatchPermit"}, "job_id": "00000000-0000-0000-0000-000000000007", "key_ref": {"digest": "738406ef1cac9fad9d9904d05d5fbae7a98ae1f3246bd65ebdf0f198d0a81d38", "kind": "PURE.AdmissionKey"}, "kind": "PURE.JobRecord", "last_error_ref": null, "last_event_ref": {"digest": "cabc72ffd5cd030d7d8af2d59cfab72bccda4ef760b297059d16ffe3e454efb8", "kind": "PURE.StoreEvent"}, "last_mutation_id": "00000000-0000-0000-0000-000000000008", "lease_epoch": 0, "lease_until_tick": null, "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "provider_cursor": 0, "read_checkpoint": null, "request_ref": {"digest": "b3e0113ceac77064c1bcb44a11cca49c86cd740cff29f5d5bd8608ad5a34f518", "kind": "PURE.RequestIntent"}, "result_ref": null, "revision": 1, "scope": "PURE_FAKE_ONLY", "state": "DRAFT", "version": 1, "worker_id": null}
```

### V033 — PURE.AtomicWriteSet

Bytes: 797; SHA-256: `3c8c4f29c683ec36b4347a11dffd276f520c5f1a32cf73ef9dadd3581c513551`.

```json
{"active_slot_action": "ACQUIRE", "base_revision": 0, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "PURE.AtomicWriteSet", "members": [{"digest": "9cc2b8e9eb5209721b2ebfe0ae81d23199ec93c4e2a5b7dc0399ee8380df7dc7", "kind": "PURE.AcceptanceReceipt"}, {"digest": "1d1f9b1b7b0197efe5d2e55cc5dc6e3b52fdbb1b4c584655c7cffda7e5e6941e", "kind": "PURE.ActiveSlot"}, {"digest": "560aeeeba5e49a92a04006161ed86385d4e13a423de50c464cf68f18f6a7f5c5", "kind": "PURE.JobRecord"}, {"digest": "cabc72ffd5cd030d7d8af2d59cfab72bccda4ef760b297059d16ffe3e454efb8", "kind": "PURE.StoreEvent"}], "mutation_ref": {"digest": "a7f03bbcaa2198337870f4f1e50c60954b9ac035085ebef7e038e0aad121bd83", "kind": "PURE.StoreMutationIntent"}, "result_revision": 1, "scope": "PURE_FAKE_ONLY", "store_sequence": 1, "version": 1}
```

### V_EXTRA_MUTATION — PURE.StoreMutationIntent

Bytes: 376; SHA-256: `9707d812ee6c4cbbc6cf1ae7fd304129775826e90d9166e3246f695e1dba43fc`.

```json
{"cancel_requested": false, "expected_revision": 0, "input_ref": {"digest": "10f4bab943161eee53ad4bfc626a5b65ab06f3dba3f18c2aa365144416c0e872", "kind": "PURE.AdmissionCommand"}, "job_id": null, "kind": "PURE.StoreMutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000032", "mutation_kind": "ADMIT", "scope": "PURE_FAKE_ONLY", "target_state": "DRAFT", "version": 1}
```

### V035 — PURE.MutationAbsenceProof

Bytes: 505; SHA-256: `f94ee455de5912c650f5f6f8583ab0dcbfba4dfcaac5e3ff313fb8ac401f960c`.

```json
{"kind": "PURE.MutationAbsenceProof", "lookup_complete": true, "marker_present": false, "members_for_mutation_present": false, "mutation_ref": {"digest": "9707d812ee6c4cbbc6cf1ae7fd304129775826e90d9166e3246f695e1dba43fc", "kind": "PURE.StoreMutationIntent"}, "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "qualification": "FAKE_STORE_READ_ONLY_EVIDENCE", "scope": "PURE_FAKE_ONLY", "snapshot_generation": 2, "version": 1}
```

### V036 — PURE.CommitResolutionProof

Bytes: 590; SHA-256: `79b3a7d845f32bb301e64f8d76636258583b7607df89fc3a9b3b8382a16e5bac`.

```json
{"absence_ref": null, "kind": "PURE.CommitResolutionProof", "mutation_ref": {"digest": "a7f03bbcaa2198337870f4f1e50c60954b9ac035085ebef7e038e0aad121bd83", "kind": "PURE.StoreMutationIntent"}, "namespace_ref": {"digest": "5942eec6e26f728ac548103918607fc970f57d3c2e6742917bf5c6d40cb13eda", "kind": "PURE.NamespaceBinding"}, "outcome": "COMMITTED", "qualification": "FAKE_STORE_READ_ONLY_EVIDENCE", "scope": "PURE_FAKE_ONLY", "snapshot_generation": 2, "version": 1, "write_set_ref": {"digest": "3c8c4f29c683ec36b4347a11dffd276f520c5f1a32cf73ef9dadd3581c513551", "kind": "PURE.AtomicWriteSet"}}
```

The external review packet includes exact UTF-8 hex and independent Python/Node arithmetic comparison for all 36 vectors. Agreement validates only these byte/digest calculations. It is neither a production codec implementation nor schema/state-machine/durability qualification. All future runtime conformance oracles remain NOT_RUN.
