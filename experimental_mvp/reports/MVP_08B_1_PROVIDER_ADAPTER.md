**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. All future behavior below is NOT_IMPLEMENTED / NOT_RUN.

**Evidence labels used throughout:** EXISTING = inspected at base `1ff403e47d35adb34139278de1d056fbbc563e6d`, not re-executed here; APPROVED = owner task plus unchanged D01–D08 in [owner record](MVP_08_OWNER_APPROVAL.md); PROPOSED = this new contract, not implementation authority; OPEN = unresolved gates in [decision register](MVP_08B_1_OPEN_DECISIONS.md). Windows qualification remains WINDOWS_NOT_RUN. No runtime, live adapter, downloader, executable tests, API calls, payments or production permissions are introduced.

# Provider-neutral adapter contract v1

EXISTING: no Dispatcher adapter or provider account qualification in MVP-08A. D01 targets Wan then extensibility for Runway/MiniMax; it does not approve an exact Wan version. Historical research trial examples do not select that version. All operations below are PROPOSED and NOT_IMPLEMENTED.

|Operation|Input → output|Contract and safe failure|
|---|---|---|
|capabilities|Pinned local QualificationProfile → CapabilitySnapshot|No discovery network call. Profile exact provider/model/version/region, modes/duration/resolution/output/stream limits, schema/price/terms hashes, expiry and qualifier. Missing/stale → CAPABILITY_UNQUALIFIED|
|validate|Immutable request+capabilities+permit → ValidationReport|Pure/local checks, no credentials/request submission. Joint duration/ratio/resolution/parameters and exact input bytes; unsupported field rejected, not ignored|
|submit|Validated request,attempt token,approved permit/reservation → SubmitOutcome|Durable intent required; ACCEPTED with associated ID,REJECTED known no-acceptance, or UNKNOWN. Timeout/reset/malformed acknowledgement may beUNKNOWN; no automatic resubmit|
|status|Namespaced provider job ref+sequence cursor → StatusObservation|Read/poll only; pending/running/succeeded/failed/cancelled plus artifact claims,identity,model,sequence/observed time. Duplicate/out-of-order observation cannot regress ledger; inconsistent identity → reconcile|
|retrieve|Validated ArtifactRef+bounded transfer policy → ArtifactReceipt/local staged object|Adapter describes allowed route; ingestion enforces network/identity separately. Offline simulator returns approved managed fixture, no URL/network. Expired/changed reference error, no new generation|
|cancel|Known remote job ID+cancel intent → CancelOutcome|Supported/unsupported/requested/confirmed plus billing uncertainty; acknowledgement does not prove stop/refund. Unsupported remains explicit, no fabricated cancellation|
|normalize_error|Provider response/exception → JobError|Sanitized typed error with external/billing uncertainty; only qualified no-acceptance proof allows submit retry|

Profile separates **capability** (model can do a thing), **entitlement** (this account can call it), **availability** (channel operational and permitted), **price** (dated estimate/upper bound), **rights** (intended-use grant/restrictions), and **technical limits** (measured/output rules). None implies the others. A UI subscription/free web quota is not API entitlement. All six require evidence and freshness; absence blocks relevant operation.

## Exact Wan configuration — OPEN OD01

Future live QualificationProfile requires official model ID/version, endpoint/region/account binding, documented modes/limits, idempotency and lookup semantics, error/billing/refund/cancel rules, terms/rights/data retention, price currency+ceiling, expiry and qualified reviewer. **No exact live Wan model is established by owner-approved evidence here.** Field remains UNSELECTED in planning, all live submit/retrieve disabled. There is no executable Wan implementation or network discovery in this branch.

Offline identity OFFLINE_SIMULATOR_V1 / SIM_WAN_PROFILE_V1 /1 /LOCAL_ONLY is distinct from live WAN. Future Runway/MiniMax profiles may satisfy the same interface without pretending to share quotas, pricing or cancellation semantics. A profile change is material and triggers reapproval; no advertised ranking/router silently switches models.

## Retry and idempotency boundaries

Adapter must expose booleans/qualification refs for submit_idempotency_supported,lookup_by_client_key,read_retry_safe,cancel_supported,refund_observable,result_identity_validator. Unknown=false for permission purposes, not an assertion that provider lacks the feature. A local uniqueness key cannot enforce provider exactly-once semantics. Multiple workers/expired lease cannot safely resubmit an UNKNOWN outcome even under$0; preserve evidence and reconcile. A successful statusHTTP or cancelHTTP is not enough.

Automatic repeated status/retrieval after known identity is bounded and uses deterministic jitter policy in simulator; new submit requires known non-acceptance/settled prior attempt, valid batch/rights and remaining reservation/attempt cap. No hidden endpoint/browser/token workaround. Live qualification and credential storage require separate authorization; production credential storage out of scope.
