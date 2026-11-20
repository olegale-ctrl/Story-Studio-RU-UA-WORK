# MVP-08B.2a-FIX-01 — Errors and acceptance oracles

Status: **PROPOSAL / DOCS_ONLY — OWNER REVIEW REQUIRED**. Date: 2026-11-20.

Project status remains **BLOCKED_CONTRACT**. This document proposes resolution of accepted findings; it does not approve EC-01–EC-10, G1–G6, implementation, real APIs, spending, storage, CI, main, merge, release or production permissions.

Source precedence: owner instruction in this conversation accepting the limited audit and F01–F05; exact independent review `3744eb5584e72e338dc51fa3a6fe7aed4882651b`; original freeze `c5cd33023880fd6726b74f5631eb766cc0959892`; original B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`; B.2 `04ea194e4d57c8a0550d7412281da58d4ba252c5`; SP/1.1 `16d28ec0376c8c28f879c8aacb18d5378fea83a3`. Historical documents remain unchanged. New PURE records below are proposals, not replacements for approved external contracts.

## F05 — response errors versus stored errors

A rejected caller receives ResponseError; it cannot write its own JobError. Failed fence/CAS/authority checks produce zero job revisions, events, outbox records and effects. Store errors may be recorded only by an already-current owner through a separate lawful INCIDENT mutation with fresh expected revision and committed event+job+JobError. Automatic incident recording is disabled in the first pure proposal, so rejection counters are deterministic. Diagnostics outside the store carry no authority and must be redacted.

The wire key is **external_effect**, never `effect`. Unsupported aliases are FORMAT. ErrorOperation, ProviderStatus and ErrorAction are closed in the record registry. The exact code/message table below is exhaustive for the proposed pure domain. Real HTTP errors, WAIT_TIMEOUT and native filesystem errors are not adopted by this scope.

| ErrorCode | Exact safe_message |
|---|---|
| `FORMAT` | Input format is invalid. |
| `VERSION_UNSUPPORTED` | Record version is unsupported. |
| `PROFILE_UNQUALIFIED` | Capability profile is not qualified. |
| `OPERATION_NOT_AVAILABLE` | Operation is not available in this scope. |
| `NAMESPACE_MISMATCH` | Namespace does not match. |
| `READ_SCOPE_DENIED` | Read scope is not authorized. |
| `UNKNOWN_COMMIT_OUTCOME` | Commit outcome is unknown. |
| `STORE_UNAVAILABLE` | Store is unavailable. |
| `STORE_CORRUPT` | Store integrity cannot be established. |
| `IDEMPOTENCY_CONFLICT` | Idempotency key conflicts with content. |
| `OPERATION_ID_CONFLICT` | Mutation identity conflicts with intent. |
| `AUTHORITY_MISSING` | Required authority is missing. |
| `AUTHORIZATION_SCOPE_MISMATCH` | Authorization scope does not match. |
| `AUTHORIZATION_EXPIRED` | Authorization is expired. |
| `AUTHORIZATION_REVOKED` | Authorization is revoked. |
| `ACTIVE_INTENT_CONFLICT` | An active job already holds this purpose. |
| `CLOCK_UNQUALIFIED` | Clock is not qualified. |
| `STALE_CONTROLLER_FENCE` | Controller fence is stale. |
| `STALE_WORKER_FENCE` | Worker fence is stale. |
| `LEASE_EXPIRED` | Worker lease is expired. |
| `CAS_CONFLICT` | Job revision has changed. |
| `ILLEGAL_TRANSITION` | State transition is not allowed. |
| `BUDGET_EXCEEDED` | Budget limit is exceeded. |
| `QUOTA_EXHAUSTED` | Quota is exhausted. |
| `READ_LIMIT_EXCEEDED` | Read checkpoint limit is exhausted. |
| `ATTEMPT_LIMIT` | Generation attempt limit is exhausted. |
| `RESULT_BINDING_MISMATCH` | Result binding does not match. |
| `NOT_FOUND` | Requested job does not exist. |
| `CURSOR_MISMATCH` | Provider cursor does not match. |
| `RESOURCE_LIMIT` | Pure execution resource bound is exceeded. |
| `SEQUENCE_EXHAUSTED` | Sequence range is exhausted. |
| `MUTATION_NOT_COMMITTED` | Mutation was not committed. |

## Deterministic precedence and disposition

For a well-formed call, select the first failing applicable check; return one public code, not a bag of competing errors. Within a row, order is left to right. A check not applicable to a read-only replay is skipped.

| Priority | Checks / codes | Default disposition |
|---|---|---|
| 1 | byte/resource envelope bound RESOURCE_LIMIT; syntax/types/closed shape FORMAT; known version VERSION_UNSUPPORTED | REJECTED |
| 2 | configured namespace NAMESPACE_MISMATCH; reader scope READ_SCOPE_DENIED | REJECTED |
| 3 | store view STORE_UNAVAILABLE then integrity STORE_CORRUPT; unresolved mutation UNKNOWN_COMMIT_OUTCOME | HOLD |
| 4 | operation OPERATION_NOT_AVAILABLE; exact capability tuple PROFILE_UNQUALIFIED | REJECTED |
| 5 | existing mutation intent OPERATION_ID_CONFLICT; recomputed key/content or historical permit IDEMPOTENCY_CONFLICT | REJECTED |
| 6 | exact historical replay -> REUSED; otherwise qualified clock CLOCK_UNQUALIFIED, grant presence AUTHORITY_MISSING, binding AUTHORIZATION_SCOPE_MISMATCH, revocation AUTHORIZATION_REVOKED, half-open validity AUTHORIZATION_EXPIRED | REUSED / REJECTED or clock HOLD |
| 7 | new admission slot ACTIVE_INTENT_CONFLICT | REJECTED |
| 8 | controller STALE_CONTROLLER_FENCE; worker STALE_WORKER_FENCE; lease LEASE_EXPIRED; revision CAS_CONFLICT; legal edge ILLEGAL_TRANSITION | REJECTED |
| 9 | budget BUDGET_EXCEEDED; quota QUOTA_EXHAUSTED; attempt ATTEMPT_LIMIT; read cap READ_LIMIT_EXCEEDED; result binding RESULT_BINDING_MISMATCH; monotonic cursor CURSOR_MISMATCH; sequence overflow SEQUENCE_EXHAUSTED | REJECTED, except read cap HOLD |
| 10 | attempted mutation proven NOT_COMMITTED -> MUTATION_NOT_COMMITTED; uncertain commit -> UNKNOWN_COMMIT_OUTCOME; committed -> ACCEPTED/APPLIED | REJECTED / HOLD / success |

For an already unresolved M, STORE_UNAVAILABLE/STORE_CORRUPT are the error codes when resolution cannot read/verify; mutation_outcome remains UNKNOWN_COMMIT_OUTCOME. On a readable intact view with no resolution yet, code is UNKNOWN_COMMIT_OUTCOME. Thus operational hold is not overwritten by an error label. A lookup for an unknown job returns NOT_FOUND only after a complete intact authorized store read and no unresolved namespace barrier. No response may infer durable absence from timeout.

Preflight rejection with a proven no-effect history has external_effect=NONE, billing=ZERO, mutation_outcome=null and no durable error. For a job with previously accepted fake effect use KNOWN/ZERO; unresolved dispatch uses UNKNOWN/ZERO only because the fixed fake simulator contract proves all billing zero, otherwise UNKNOWN/UNKNOWN. Never infer NONE from an error. Required action: FIX_INPUT for FORMAT/VERSION_UNSUPPORTED/PROFILE_UNQUALIFIED/OPERATION_NOT_AVAILABLE/IDEMPOTENCY_CONFLICT/OPERATION_ID_CONFLICT/AUTHORIZATION_SCOPE_MISMATCH/RESULT_BINDING_MISMATCH/CURSOR_MISMATCH; REAUTHORIZE for AUTHORITY_MISSING/AUTHORIZATION_EXPIRED/AUTHORIZATION_REVOKED/READ_SCOPE_DENIED/BUDGET_EXCEEDED/QUOTA_EXHAUSTED; RELOAD for ACTIVE_INTENT_CONFLICT/CAS_CONFLICT/STALE_CONTROLLER_FENCE/STALE_WORKER_FENCE/LEASE_EXPIRED/NOT_FOUND; RECONCILE for UNKNOWN_COMMIT_OUTCOME/STORE_UNAVAILABLE/MUTATION_NOT_COMMITTED; STOP for all remaining codes.

Durable JobError retry_class is RECONCILE_ONLY for UNKNOWN_COMMIT_OUTCOME/STORE_UNAVAILABLE/STORE_CORRUPT; SAFE_LOCAL for MUTATION_NOT_COMMITTED; otherwise NONE. No automatic retry is granted by this field. READ errors require separate reserved bounded read authorization; SAFE_READ is a recognized value reserved for future separately specified read diagnostics, not automatically assigned by these codes. A typed error cannot expand the profile, retry budget or authority.

## Corrected original-oracle crosswalk

The original source remains byte-for-byte unchanged. This addendum corrects interpretation, without claiming its proposed test IDs were executed or maintaining the old count as a new test result.

| Original ID | Corrected reference / split | Exact proposed oracle |
|---|---|---|
| P003 | B.1 JOB_CONTRACT Identity/idempotency; T005 active intent | identical replay -> REUSED original receipt, zero writes |
| P004 | same B.1 identity section, not T001/T004 | supplied old key + changed request -> IDEMPOTENCY_CONFLICT |
| P012-a | identity section | old key + different content -> IDEMPOTENCY_CONFLICT |
| P012-b | authorization scope; T005 only after scope passes | correct new key + old permit -> AUTHORIZATION_SCOPE_MISMATCH |
| P011-provider | exact profile tuple | unsupported provider -> PROFILE_UNQUALIFIED |
| P011-model/version | exact profile tuple | wrong model or version -> PROFILE_UNQUALIFIED |
| P011-region/mode | exact profile tuple | wrong region or I2V -> PROFILE_UNQUALIFIED |
| P011-handler | operation boundary | non-synthetic handler -> OPERATION_NOT_AVAILABLE |
| P019 | wait deferred by proposed G6 | NOT_RUN; no wait implementation |

All single-fault P011 cases presume valid wire/namespace and no higher-priority barrier; combined faults obey precedence above. For unsupported handler, operation check precedes profile tuple; do not produce two public codes.

## New finite oracle set — NOT_RUN

Alongside A01–A10 and R01–R16, require: E01 each closed shape rejects extra/missing field; E02 null differs from absent; E03 Unicode normalization variants differ; E04 integer maximum exact across codecs and overflow rejected; E05 bool-as-int/float/duplicate keys rejected; E06 same digest/wrong type fails binding; E07 stale fence+stale CAS -> fence error and zero writes; E08 valid fence+bad revision -> CAS_CONFLICT and zero writes; E09 two retries means exactly three reserved calls; E10 fourth call -> READ_LIMIT_EXCEEDED with no new effect; E11 restart/duplicate cursor never resets count; E12 unknown commit plus logical conflict -> hold before conflict; E13 operation ID reused with different intent -> conflict; E14 retained old receipt cannot write; E15 RESULT_AVAILABLE never implies COMPLETED or slot release; E16 unqualified producer metadata cannot authorize MP4 ingestion; E17 unknown errors cannot become success; E18 no wallclock/sleep/network/files/media/SQLite in pure tests; E19 every run obeys fixed event/outbox/job/read/script/tick bounds; E20 exact documented safe_message and external_effect spelling.

Document arithmetic executed: 36 byte/digest examples, 25 kinds; two independent encoders agree, exit 0. Runtime/schema/oracle/state-machine tests executed: **0**. All A/R/E tests and Windows/durable/media/provider qualifications: **NOT_RUN**. Do not convert document arithmetic into a test pass count.
