**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. All future behavior below is NOT_IMPLEMENTED / NOT_RUN.

**Evidence labels used throughout:** EXISTING = inspected at base `1ff403e47d35adb34139278de1d056fbbc563e6d`, not re-executed here; APPROVED = owner task plus unchanged D01–D08 in [owner record](MVP_08_OWNER_APPROVAL.md); PROPOSED = this new contract, not implementation authority; OPEN = unresolved gates in [decision register](MVP_08B_1_OPEN_DECISIONS.md). Windows qualification remains WINDOWS_NOT_RUN. No runtime, live adapter, downloader, executable tests, API calls, payments or production permissions are introduced.

# GenerationJob v1 — proposed data contract

## Schema conventions

A record is a JSON object, schema_version integer1, unknown fields rejected except a namespaced provider_parameters object with an allowlist from the pinned capability profile. IDs are namespaced UUID strings; SHA256 lowerhex64; timestamps UTCISO with timezone; durations/byte counts/revisions/nonnegative minor currency units strict integers (bool not int); rational rates use numerator/denominator integers with denominator>0. NaN/Infinity/duplicate JSON keys rejected. Optional unknown values are null with reason, not fabricated zero/empty entitlement. Required execution safety fields cannot be UNKNOWN at submission.

Canonical request digest profile JCS-LOCAL-1 is explicitly **base-compatible Python encoded()**, not claimed RFC8785: json.dumps with sort_keys=True,ensure_ascii=False,allow_nan=False and default separators, UTF8, no Unicode normalization. Pin encoder profile/version; distinguish1 from1.0; restrict new job numeric request fields to strict integers/rationals. Saved-file SHA hashes raw bytes. Editor snapshot uses full encoded dictionary including approved, unlike generation-only storyboard.fingerprint or UI helpers dropping approved.

## GenerationJob object (all top-level groups required)

|Group|Required fields / types|Immutability / validation|
|---|---|---|
|identity|job_id, schema_version, project_id, scene_id, anchor_id, created_at, idempotency_key|Immutable from creation; globally distinct project ID not inferred from topic|
|target_snapshot|project_locator_ref, expected_saved_json_sha256, expected_editor_snapshot_sha256, expected_anchor_token, generation_fingerprint, input_manifest_sha256|Immutable request target; exact content snapshots, not a monotonic edit counter or authenticated owner ID. New target approval is separate HandoffIntent, never edits submitted request|
|request|provider_id,model_id,model_version,region,mode(T2V/I2V),prompt_reference,prompt_sha256,duration_ms,resolution{width,height},aspect_ratio{num,den},input_assets[],provider_parameters,capability_profile_ref/hash|Draft revisions are append-only until approval; the approved snapshot is immutable; provider/model/region exact, allowlisted and bound to capability digest; resolution/ratio/duration positive and jointly supported. Prompt ref must resolve to approved bytes/hash|
|input_assets[] items|asset_id,revision,sha256,usage_role,rights_evidence_ref|Exact immutable revisions verified before use; source paths/URLs not authoritative identity; no silent latest asset|
|authorization|batch_id,batch_revision,batch_manifest_sha256,approval_ref,approved_provider/model/version/region,rights_review_ref,data_transfer_authorization_ref,valid_from,expires_at,max_job_spend,cost_estimate,price_snapshot_ref,execution_mode|Initial grant plus append-only same-request reapproval_grants; each grant snapshot immutable, active reference in execution. Material request/scope/ceiling change creates a new job. Referenced live revocation ledger consulted at every side-effect boundary; consent not a secret. max_job_spend and estimate include currency+minor_units and input/output/retry ceilings. expiry exclusive, trusted-clock anomaly blocks|
|execution|state,state_revision,draft_revision,attempt_number,attempts[],provider_job_id,polling{next_due,deadline,last_sequence},retry_eligibility,cancellation{requested,reason,ack,settlement},last_error,continuation_checkpoint,lease_owner,lease_epoch,lease_expiry,active_authorization_ref|Mutable only by fenced CAS transitions; nullable remote ID before acknowledgement. state_revision increments on every transition; attempt number increments only when a new authorized submit attempt is actually durably prepared|
|attempts[] append-only|attempt_id,number,request_hash,idempotency_key,submit_intent_ref,provider_job_id,submit_outcome,billing_outcome,reservation_ref,started_at,finished_at|No deletion/reuse of attempt identity. Poll/download retry does not create a generation attempt; ambiguous submit retains same identity pending reconciliation|
|result|artifacts[],selected_artifact_id,result_reference,download_state,sha256,byte_size,media_validation_ref,rights_evidence_ref,asset_id,asset_revision,ingestion_token,handoff_status,handoff_intent_ref,project_save_receipt_ref|Mutable by saga checkpoints; previous versions retained in event history. Separate per-artifact state/hash/asset pin for multiple outputs; one primary chosen only by declared policy/explicit review|
|audit|request_sha256,authorization_sha256,event_sequence,last_event_ref,integrity_manifest_ref|Immutable request/auth hashes plus append-only event chain; local hash chain detects changes only against trusted checkpoint, not an authenticated production audit store|

Fields may be null in DRAFT where unresolved; APPROVED requires exact simulator/live profile, full batch permit and input/data rights. For this stage **no record executes**. Future offline fixture uses provider_id OFFLINE_SIMULATOR_V1, model_id SIM_WAN_PROFILE_V1, model_version1, region LOCAL_ONLY; these are synthetic labels, not live Wan model names. A proposed live_target field may remain unselected in planning but is never used as an executable request.

Same-scope renewal may append a new explicitly approved grant (e.g. expiry renewal) preserving the original grant/hash and all attempt-to-grant associations; it never edits an old authorization snapshot. Audit records each added grant digest. No approval automatically renews. Draft edits append draft_revision, invalidate pending approval replies and retain previous request hashes; post-approval material changes use a new job.

## Related contracts

BatchPermit: ID/revision, owner/reviewer ref, ordered job request hashes or Merkle-equivalent manifest, provider/model/region allowlist, exact data categories+recipient, max total/job/attempt spend, max attempts, validity, cancellation/expiry/revocation policy, scope of automatic local import and attachment, signature/verification method qualification ref. Current local entered metadata is not authenticated approval. Offline fixtures use explicit synthetic test authority; live authority unresolvedOD01/OD05.

HandoffIntent: job/result hash, exact asset_id/revision/SHA, target project/scene/anchor snapshots, prior binding digest, explicit replacement approval, rights review/current expiry, GUI session epoch, idempotency token. Rebase after STALE_TARGET needs a new explicitly approved intent, not a new generation or mutation of original job.

JobError: error_id,domain/code,occurred_at,state/attempt,operation,retry_class{NONE,SAFE_READ,SAFE_LOCAL,RECONCILE_ONLY},safe_message,provider_status/trace redacted,external_effect{NONE,KNOWN,UNKNOWN},billing{ZERO,SETTLED,RESERVED,UNKNOWN},evidence_ref,required_action. No raw credentials, headers, prompt body, secret URL query or provider HTML in logs. Errors preserve uncertainty; successHTTP alone isn't completion.

ProviderArtifact: artifact_id,job/attempt/provider_job association,requested/resolved model,region,source receipt,format/size claim,immutable object validator/hash if offered,expiry,transfer route. Claims and verified measurements kept separately. Missing identity or model mismatch never silently normalizes to expected values.

## Identity/idempotency rules

Job idempotency key binds project UUID + intended generation purpose + request digest + batch scope, with unique active-intent constraint; request-identical but deliberately separate outputs require distinct explicit purpose IDs. A duplicate click returns existing job. Every event/effect token unique and durable before side effect. Provider job IDs unique per provider/account namespace: same ID on same attempt is duplicate acknowledgement; same ID on different job/attempt is conflict → NEEDS_RECONCILIATION, never alias jobs. Artifact IDs and ingestion tokens cannot be substituted by SHA alone (same content may have different rights).

## Existing mismatch / unresolved

Current project has no qualified stable project registry/monotonic save revision; base anchor_token is content hash. Current Library has revisioned metadata but no exactly-once import token. Base save is atomic replace without disk CAS. Proposed related records and extra job fields are **not added** to current files/schemas. OD02/OD03 resolve future APIs/save coordination; normative PG contracts are untouched.
