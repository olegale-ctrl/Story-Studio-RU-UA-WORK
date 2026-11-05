# E01.3.8.1 — Versioned ApprovalAuthorityEvidence Schema Contract

Status: **PROPOSAL — SCHEMA APPROVAL REQUIRED**

This document proposes editorial snapshot schema 2. It does not change schema 1,
authorize migration, or implement authority evaluation.

## 1. Basis and current constraints

Normative basis:

- [approved authority contract](E01_3_7_3_APPROVED_CONTRACT.md), especially
  A1–A14;
- [authority proposal](E01_3_7_3_AUTHORITY_CONTRACT_PROPOSAL.md);
- E00 §§2–4;
- [approved package contract](E01_3_4_APPROVED_CONTRACT.md);
- implemented E01.3.7.1 consistency and E01.3.7.2 history semantics.

Actual schema-1 constraints verified in `editorial/model.py` and
`editorial/codec.py`:

- `editorial_schema_version` accepts only integer `1`;
- root keys and every nested object use closed field sets;
- `ApprovalRecord` has no principal, authority-policy, session, request,
  reconsideration, attestation, key, or signature field;
- `review_declarations` is an arbitrary ordered tuple of nonempty strings;
- UUID and hash fields are canonical lowercase forms; timestamps decoded from
  wire are UTC seconds `YYYY-MM-DDTHH:MM:SSZ`;
- snapshot size is at most 32 MiB, JSON depth 64, any general array 10,000,
  revisions total 10,000, and text fields 100,000 code points;
- duplicate keys, unknown fields, floats, NaN/Infinity, invalid UTF-8, BOM, and
  unpaired surrogates are rejected;
- snapshot checksum covers the complete canonical envelope except the checksum
  field itself;
- revision semantic hashes exclude approvals/events and must not change merely
  because schema-2 authority evidence is added.

Schema 1 therefore cannot represent authenticated approval evidence. Reusing
`actor`, `reason`, or `review_declarations` would contradict A3. No migration may
infer missing evidence from those strings.

## 2. Schema 2 envelope

Schema identifier remains the root field `editorial_schema_version`; its value
for this contract is integer `2`.

Schema 2 has exactly the schema-1 root fields plus one mandatory collection:

```text
approval_authority_evidence: array<ApprovalAuthorityEvidence>
```

The root key is mandatory even when the array is empty. It is placed logically
after `approvals` and before `events`; JSON object key order is not significant
because canonical serialization sorts keys. No schema-1 field changes meaning.

All schema-2 root and nested objects reject unknown fields. Nullable fields are
present with explicit `null`; omission is invalid. Arrays are never `null`.
Unicode strings are preserved exactly without trimming, case conversion, NFC,
NFD, translation, or whitespace normalization.

Schema 2 retains current limits unless narrowed below:

- encoded snapshot: at most 32 MiB;
- JSON nesting: at most 64 containers;
- evidence records: at most 10,000 and no more than approval records;
- all text: at most 100,000 code points, with field-specific limits below;
- declaration codes per evidence: at most 16.

Snapshot checksum uses the existing canonical rule over the entire schema-2
envelope except root `snapshot_checksum`. It includes approval evidence and all
signature extension fields, including explicit `null` values.

Schema-1 codec must continue rejecting version 2 as unsupported until a separate
implementation task adds a version-aware model and codec. Schema 2 must not be
silently decoded as schema 1.

## 3. ApprovalAuthorityEvidence wire object

Each array element has exactly these keys:

| Field | Wire type | Required rule |
|---|---|---|
| `approval_id` | UUID string | Required. Exact ID of one ApprovalRecord in the same snapshot. |
| `principal_id` | string | Required. Canonical OS-derived identifier defined in §3.1. |
| `principal_display_name` | string | Required nonempty text, 1–256 code points. Display only. |
| `authority_policy_id` | UUID string | Required stable identifier of external authority policy. |
| `authority_policy_version` | string | Required nonempty exact value, 1–128 code points. |
| `review_session_id` | UUID string | Required; globally unique within snapshot evidence. |
| `request_id` | UUID string | Required; globally unique within snapshot evidence except an idempotent retry that resolves to the existing record and adds nothing. |
| `declaration_codes` | array<string> | Required, nonempty, unique, exact gate vocabulary in canonical order, at most 16. |
| `attested_at` | UTC string | Required UTC seconds `YYYY-MM-DDTHH:MM:SSZ`. Descriptive, not trusted time. |
| `reconsiders_record_id` | UUID string or null | Required key. Exact ApprovalRecord ID or null; §7 rules apply. |
| `attestation_digest` | hash string | Required 64 lowercase hexadecimal SHA-256 per §5. |
| `signing_key_id` | string or null | Required key. Null in unsigned MVP; signature tuple rule in §6. |
| `signature_algorithm` | string or null | Required key. Null in unsigned MVP; closed value when signed. |
| `signature` | string or null | Required key. Null in unsigned MVP; base64url without padding when signed. |

All evidence values are immutable after creation. Correction creates a new
ApprovalRecord/evidence pair; it does not edit evidence already in history.

### 3.1 Principal ID grammar

Proposed canonical strings:

- Windows: `windows-sid:<SID>`, where SID matches
  `S-[0-9]+(-[0-9]+)+`, uses uppercase `S`, and contains no whitespace;
- compatible Unix: `posix-uid:<uid>@machine:<machine_id>`, where `uid` is a
  canonical unsigned decimal without leading zero except `0`, and `machine_id`
  is exactly 32 lowercase hexadecimal characters.

The value is produced by a platform adapter, never accepted as authority from
free-form user input. Other schemes require a later schema version or an
explicitly versioned extension; unknown prefixes are structural errors in
schema 2.

### 3.2 One-to-one and uniqueness rules

- At most one evidence record exists per `approval_id`.
- Every evidence `approval_id` resolves to exactly one ApprovalRecord.
- Evidence may be absent for an ApprovalRecord only to preserve migrated
  schema-1 history; such a record is `UNAUTHENTICATED_LEGACY`.
- A future schema-2 write command must atomically create a new ApprovalRecord and
  its evidence. It must never create a new unauthenticated approval.
- `review_session_id` and `request_id` are unique across the collection.
- `principal_id` and authority policy may repeat across records.
- Evidence order follows the referenced ApprovalRecord order in `approvals`.
  Records without evidence are skipped. Any other evidence order is rejected,
  not automatically sorted.

This ordering preserves approval history and gives deterministic joins without
claiming that array order is chronology.

## 4. Closed declaration vocabulary

Schema 2 defines declaration vocabulary version 1 implicitly through
`editorial_schema_version=2` and the gate on the linked ApprovalRecord. No
localized text is stored in code identity. Russian/Ukrainian presentation is a
UI resource keyed by the code.

All listed codes are mandatory for APPROVE evidence for their gate and appear
exactly in the order below. Unknown, missing, duplicate, additional,
out-of-order, or wrong-gate codes are rejected for APPROVE.

### SCRIPT, vocabulary 1

1. `SCRIPT_EXACT_TEXT_REVIEWED`
2. `MATERIAL_CLAIMS_REVIEWED`
3. `EVIDENCE_AND_QUALIFICATIONS_REVIEWED`
4. `FICTION_DISCLOSURES_REVIEWED`
5. `LANGUAGE_ALIGNMENT_REVIEWED`
6. `SOURCE_RIGHTS_STATUS_ACKNOWLEDGED`
7. `NO_UNSUPPORTED_REVIEW_CLAIM`

### SCENES, vocabulary 1

1. `CURRENT_SCRIPT_DECISION_REVIEWED`
2. `SCENE_TEXT_COVERAGE_REVIEWED`
3. `SCENE_VISUAL_MEANING_REVIEWED`
4. `ASSET_PROVENANCE_VISIBLE`
5. `ASSET_RIGHTS_STATUS_ACKNOWLEDGED`
6. `DISCLOSURES_VISIBLE_IN_SCENES`
7. `NO_UNSUPPORTED_REVIEW_CLAIM`

### Editorial HANDOFF, vocabulary 1

1. `EDITORIAL_SCRIPT_AND_SCENES_REVIEWED`
2. `EDITORIAL_ASSET_SET_REVIEWED`
3. `CURRENT_RECORDED_DECISIONS_VISIBLE`
4. `RIGHTS_STATUS_ACKNOWLEDGED_NOT_GRANTED`
5. `HANDOFF_IS_EDITORIAL_ONLY`
6. `NO_RENDER_OR_EXPORT_AUTHORIZATION`
7. `NO_UNSUPPORTED_REVIEW_CLAIM`

For REJECT, REVISE, and REVOKE, `declaration_codes` is proposed as exactly
`["NO_UNSUPPORTED_REVIEW_CLAIM"]`; their nonempty `ApprovalRecord.reason` carries
the decision rationale. This keeps every schema-2 decision explicitly attested
without falsely claiming the APPROVE review set. Owner approval of this detail
is requested in O3.

Changing code membership, requiredness, meaning, or canonical order requires a
new editorial schema version. Adding localized strings does not.

## 5. Canonical attestation and digest

### 5.1 Joined payload

Attestation digest binds evidence to the full linked ApprovalRecord, exact
decision key, principal, authority policy, session, request, declarations, and
reconsideration. The payload has exactly three top-level keys:

```json
{
  "approval_authority_evidence_schema_version": 1,
  "approval_record": {
    "id": "...",
    "gate": "SCRIPT",
    "object_ref": {"kind":"script","id":"...","revision":1,"content_hash":"..."},
    "dependency_digest": "...",
    "policy_version": "editorial-policy-v1",
    "actor": "Display Name",
    "timestamp": "2026-11-05T10:00:00Z",
    "decision": "approve",
    "reason": "Reviewed",
    "review_declarations": []
  },
  "authority_evidence": {
    "approval_id": "...",
    "principal_id": "posix-uid:1000@machine:...",
    "principal_display_name": "Display Name",
    "authority_policy_id": "...",
    "authority_policy_version": "1",
    "review_session_id": "...",
    "request_id": "...",
    "declaration_codes": ["..."],
    "attested_at": "2026-11-05T10:00:00Z",
    "reconsiders_record_id": null
  }
}
```

The linked ApprovalRecord is included in full, including actor, timestamp,
reason, and legacy `review_declarations`. This prevents those values from being
changed while retaining the same attestation digest. The evidence subobject
excludes `attestation_digest`, `signing_key_id`, `signature_algorithm`, and
`signature`.

### 5.2 Canonical bytes and SHA-256

Canonical bytes are exactly:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
).encode('utf-8')
```

`attestation_digest = hashlib.sha256(canonical_bytes).hexdigest()`.

No Unicode normalization, trimming, case conversion, timezone conversion,
locale fallback, array sorting, or hidden defaults occur. Declaration codes
must already be in their normative canonical order. Local paths, UI state,
localized labels, current clock, environment variables, and policy file paths
are absent.

The digest is a consistency check, not a signature, identity proof, trusted
timestamp, authority grant, or rollback anchor.

## 6. Optional signature extension

The three signature fields obey an all-null or all-present rule:

- unsigned: all three are `null`;
- signed: all three are non-null;
- every partial combination is `SIGNATURE_FIELDS_INCOMPLETE`.

For schema 2, the only proposed signed algorithm identifier is `ed25519`.
`signing_key_id` is 1–128 ASCII characters matching
`[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`. `signature` is canonical base64url without
padding and decodes to exactly 64 bytes.

The signature covers the exact canonical attestation bytes from §5, prefixed by
the ASCII domain separator and NUL byte:

`story-studio-approval-attestation-v1\x00`.

Presence and shape do not make a signature valid. Verification requires a
separate trusted key registry, key status/revocation rules, algorithm support,
and principal/policy binding outside the editable snapshot. Without them the
authority result is not cryptographically authenticated.

New algorithms require a later schema version unless an approved algorithm
registry contract explicitly versions them.

## 7. Referential and semantic integrity

Schema/integrity validation must enforce:

1. evidence `approval_id` resolves exactly and uniquely;
2. evidence order follows approvals order;
3. ApprovalRecord object refs still satisfy existing exact graph rules;
4. attestation digest recomputes from the joined exact record/evidence;
5. principal, policy, session, request, declaration, timestamp, and signature
   field shapes are valid;
6. declaration set and order match the linked gate and decision;
7. `reconsiders_record_id` is not the same as `approval_id`;
8. a non-null reconsideration target exists in the same snapshot;
9. reconsideration target has the same exact decision key;
10. APPROVE after REVOKE links the latest applicable REVOKE; same-key APPROVE
    after REJECT/REVISE links the latest applicable record;
11. initial APPROVE and REJECT/REVISE/REVOKE normally use null reconsideration;
12. session and request IDs are unique;
13. evidence does not create revision dependency-graph edges;
14. evidence is included in snapshot checksum but never in revision content
    hashes or dependency digest.

Items 9–11 are cross-record authority/history integrity checks, not JSON grammar
checks. A structurally valid legacy approval without evidence remains readable
but cannot pass authority evaluation.

## 8. Migration from schema 1

### 8.1 Preconditions

Migration accepts only a schema-1 snapshot that passes the schema-1 strict
decoder and complete snapshot integrity validation. Corrupt checksum, graph,
revision hash, rights binding, duplicate ID, or malformed record aborts with no
output. Migration does not repair input.

The source does not become a trusted head merely because it passed integrity.
Missing/unavailable/mismatched protected anchor remains authority-blocking under
A11. Migration never initializes or updates the anchor.

### 8.2 Transform

The schema-1 to schema-2 transform:

1. preserves every existing root value and collection order;
2. changes `editorial_schema_version` from `1` to `2`;
3. adds `approval_authority_evidence: []`;
4. preserves every ApprovalRecord field and its exact position;
5. treats every migrated approval as `UNAUTHENTICATED_LEGACY`;
6. preserves all revision payloads and `RevisionRef.content_hash` values;
7. preserves exact Unicode code points and array order;
8. increments `generation` exactly once for the committed migration;
9. appends one schema-2 Event with proposed action `schema_migrated`, actor from
   the migration command's authenticated display context, exact UTC time, empty
   refs, reason identifying schema 1→2, and null error code;
10. recomputes only the full schema-2 snapshot checksum after all changes.

The proposed new Event action is a schema-2 vocabulary change and needs owner
approval in O5. It does not establish authority.

### 8.3 Idempotency and reversibility

- Running the migration operation on schema 2 returns an explicit
  `ALREADY_MIGRATED` no-op; it does not increment generation, append an event, or
  change bytes.
- Retrying after an uncertain write belongs to the future atomic-storage
  contract and must reread generation/checksum before deciding.
- Automatic downgrade is lossless only when evidence is empty and no schema-2
  event/action or other schema-2-only state must be discarded. Because the
  proposed migration event itself is schema-2-only, ordinary migrated snapshots
  are not automatically downgradeable.
- Exporting a schema-1 compatibility copy, if later allowed, is a separate
  explicit lossy operation and never overwrites schema 2.

### 8.4 History behavior

APPROVE, REJECT, REVISE, REVOKE, equal-timestamp ambiguity, actor text, reasons,
legacy declarations, and exact decision keys remain unchanged. A historical
REVOKE is not removed or weakened. No legacy APPROVE receives generated
evidence, authority, a new review session, or effective status.

## 9. Error taxonomy

Errors retain exact JSON field paths and stable codes. Categories remain
separate.

### 9.1 Structural/schema errors

| Code | Example path | Meaning |
|---|---|---|
| `SCHEMA_VERSION_UNSUPPORTED` | `$.editorial_schema_version` | Version is not implemented/supported. |
| `MISSING_FIELD` / `UNKNOWN_FIELD` | exact missing/extra path | Closed object contract violated. |
| `EVIDENCE_DUPLICATE_APPROVAL` | `$.approval_authority_evidence[i].approval_id` | More than one evidence record links one approval. |
| `EVIDENCE_ORDER` | `$.approval_authority_evidence[i]` | Evidence does not follow approval order. |
| `APPROVAL_TARGET_MISSING` | `...approval_id` | Evidence links no ApprovalRecord. |
| `PRINCIPAL_ID_FORMAT` | `...principal_id` | Unknown scheme or invalid canonical grammar. |
| `POLICY_ID_FORMAT` / `POLICY_VERSION_FORMAT` | policy field | Invalid UUID or nonempty/version length rule. |
| `DUPLICATE_DECLARATION` | `...declaration_codes[i]` | Code repeats. |
| `DECLARATION_SET` | `...declaration_codes` | Missing, extra, wrong-gate, wrong-decision, or out-of-order code. |
| `DATE` | `...attested_at` | Not valid UTC seconds. |
| `RECONSIDERATION_TARGET_MISSING` | `...reconsiders_record_id` | Linked record is absent. |
| `RECONSIDERATION_SELF_REFERENCE` | `...reconsiders_record_id` | Evidence references its own approval. |
| `SIGNATURE_FIELDS_INCOMPLETE` | first inconsistent signature field | Signature tuple is partial. |
| `SIGNATURE_ALGORITHM` / `SIGNATURE_FORMAT` | exact signature field | Unsupported identifier or malformed bytes. |
| `LIMIT` | exact collection/string path | Size/count/depth cap exceeded. |

### 9.2 Integrity errors

- `ATTESTATION_DIGEST_MISMATCH` at `...attestation_digest`;
- existing snapshot checksum mismatch;
- existing graph, revision hash, rights binding, and current package errors;
- duplicate session/request IDs;
- reconsideration key/history mismatch.

### 9.3 Authority policy failures

Missing policy, unknown principal, absent gate/decision permission, revoked key,
or invalid signature trust are authority results/failures, not corrupt JSON.
They must not be reported as `MISSING_FIELD` or checksum errors.

### 9.4 History ambiguity

E01.3.7.2 `AMBIGUOUS_HISTORY` and its diagnostics remain history results. They
block effective authority but do not imply malformed serialization.

### 9.5 Trust-anchor failures

`ANCHOR_MISSING`, `ANCHOR_UNAVAILABLE`, and `ANCHOR_MISMATCH` remain distinct
blocking trust results. They do not prevent safe draft decode, integrity
diagnostics, migration analysis, or history inspection, and never auto-reset
trust.

## 10. Non-executable JSON examples

All examples below are **schema fragments, not executable fixtures**. Ellipses,
abbreviated inherited collections, and angle-bracket digest/checksum markers are
intentionally invalid JSON values or unverified placeholders. They must never be
used as golden vectors. Future implementation tests must compute and publish
real literal vectors independently.

### 10.1 Schema 2 without approvals

```json
{
  "editorial_schema_version": 2,
  "production_id": "10000000-0000-0000-0000-000000000001",
  "generation": 1,
  "production_revisions": [], "profiles": [], "candidates": [],
  "sources": [], "claims": [], "scripts": [], "scene_plans": [],
  "assets": [], "rights_reviews": [],
  "approvals": [],
  "approval_authority_evidence": [],
  "events": [],
  "active_refs": {"production":null,"candidate":null,"script":null,"scene_plan":null},
  "snapshot_checksum": "<COMPUTE_SCHEMA2_CHECKSUM>"
}
```

### 10.2 Migrated legacy approval without evidence

```json
{
  "editorial_schema_version": 2,
  "approvals": [{
    "id":"10000000-0000-0000-0000-000000000001",
    "gate":"SCRIPT", "object_ref":{"kind":"script","id":"...","revision":1,"content_hash":"..."},
    "dependency_digest":"...", "policy_version":"editorial-v1",
    "actor":"Legacy name", "timestamp":"2026-11-05T10:00:00Z",
    "decision":"approve", "reason":"Legacy record", "review_declarations":[]
  }],
  "approval_authority_evidence": []
}
```

Authority interpretation: `UNAUTHENTICATED_LEGACY`, never effective automatically.

### 10.3 New approval with unsigned evidence

```json
{
  "approvals": [{"id":"10000000-0000-0000-0000-000000000001","gate":"SCRIPT","...":"..."}],
  "approval_authority_evidence": [{
    "approval_id":"10000000-0000-0000-0000-000000000001",
    "principal_id":"posix-uid:1000@machine:0123456789abcdef0123456789abcdef",
    "principal_display_name":"Редактор",
    "authority_policy_id":"20000000-0000-0000-0000-000000000002",
    "authority_policy_version":"1",
    "review_session_id":"30000000-0000-0000-0000-000000000003",
    "request_id":"40000000-0000-0000-0000-000000000004",
    "declaration_codes":["SCRIPT_EXACT_TEXT_REVIEWED","...canonical remaining SCRIPT codes..."],
    "attested_at":"2026-11-05T10:00:00Z",
    "reconsiders_record_id":null,
    "attestation_digest":"<COMPUTE_JOINED_ATTESTATION_SHA256>",
    "signing_key_id":null,"signature_algorithm":null,"signature":null
  }]
}
```

### 10.4 APPROVE → REVOKE → APPROVE

```json
{
  "approvals": [
    {"id":"10000000-0000-0000-0000-000000000001","decision":"approve","timestamp":"2026-11-05T10:00:00Z","...":"same exact key"},
    {"id":"20000000-0000-0000-0000-000000000002","decision":"revoke","timestamp":"2026-11-05T11:00:00Z","...":"same exact key"},
    {"id":"30000000-0000-0000-0000-000000000003","decision":"approve","timestamp":"2026-11-05T12:00:00Z","...":"same exact key"}
  ],
  "approval_authority_evidence": [
    {"approval_id":"10000000-0000-0000-0000-000000000001","review_session_id":"...1","reconsiders_record_id":null,"...":"..."},
    {"approval_id":"20000000-0000-0000-0000-000000000002","review_session_id":"...2","reconsiders_record_id":null,"...":"..."},
    {"approval_id":"30000000-0000-0000-0000-000000000003","review_session_id":"...3","reconsiders_record_id":"20000000-0000-0000-0000-000000000002","...":"all declarations repeated"}
  ]
}
```

The final record is only eligible for authority evaluation after all integrity,
policy, session, declaration, reconsideration, and anchor checks.

### 10.5 Ambiguous historical sequence

```json
{
  "approvals": [
    {"id":"10000000-0000-0000-0000-000000000001","decision":"approve","timestamp":"2026-11-05T10:00:00Z","...":"same exact key"},
    {"id":"20000000-0000-0000-0000-000000000002","decision":"revoke","timestamp":"2026-11-05T10:00:00Z","...":"same exact key"}
  ],
  "approval_authority_evidence": ["<corresponding evidence fragments>"]
}
```

History result remains `AMBIGUOUS_HISTORY`; evidence cannot select a winner by
array order, UUID, actor, or authority permission.

## 11. Acceptance criteria for future implementation

1. Schema 1 remains readable through its unchanged version-1 codec path.
2. Schema 1 rejects schema 2 rather than dropping evidence.
3. Schema 2 requires the evidence root array, including when empty.
4. Every schema-2 object rejects unknown and missing fields.
5. Encode/decode round-trip preserves every value, null, Unicode code point, and
   semantically significant array order.
6. In-memory schema-2 values and evidence collections are immutable.
7. Evidence links exactly one existing ApprovalRecord.
8. Duplicate evidence and dangling approval IDs have exact structured paths.
9. Evidence ordering follows approval ordering and is never silently repaired.
10. Principal ID accepts only approved Windows/POSIX canonical forms.
11. Authority policy, session, request, and reconsideration identifiers validate
    exact type/shape and uniqueness.
12. Gate-specific APPROVE declaration sets are complete, unique, closed, and in
    canonical order.
13. REJECT/REVISE/REVOKE declaration rule is implemented only after O3 approval.
14. Localized RU/UK text does not change machine declaration identity.
15. Canonical attestation bytes match independent literal golden vectors.
16. `attestation_digest` is lowercase SHA-256 and excludes itself/signature
    fields only as specified.
17. Changes to any joined ApprovalRecord or core evidence field change digest.
18. Unicode is not normalized; combining characters and emoji round-trip.
19. Signature fields enforce all-null/all-present and reject malformed encoding.
20. Signature presence alone never produces trusted authority.
21. Snapshot checksum covers evidence and signature fields.
22. Revision content hashes and dependency digests remain unchanged when only
    authority evidence is added.
23. Reconsideration rejects dangling, self, wrong-key, and wrong-history links.
24. Legacy approvals migrate in original order with every field unchanged.
25. Migration creates no evidence and classifies all legacy approvals as
    `UNAUTHENTICATED_LEGACY`.
26. Migration preserves APPROVE/REJECT/REVISE/REVOKE and ambiguity semantics.
27. Migration preserves all revision content hashes exactly.
28. Migration increments generation once, appends only the approved migration
    event, and computes a valid new checksum.
29. Re-running migration on schema 2 is an idempotent no-op.
30. Corrupt schema-1 input produces no schema-2 output or partial state.
31. Migration never creates or updates a trusted head anchor.
32. Missing/unavailable/mismatched anchor still blocks effective authority while
    decode, diagnostics, and history remain available.
33. Schema-2 approvals without evidence remain readable legacy history but
    cannot pass authority evaluation.
34. A future schema-2 decision command cannot commit approval without matching
    evidence in the same atomic transaction.
35. Existing E01.3.7.1 consistency gives the same result for preserved legacy
    ApprovalRecords before and after migration.
36. Existing E01.3.7.2 history gives the same key grouping, record order,
    decision state, and ambiguity before and after migration.
37. Size, item, declaration, string, and nesting limits fail explicitly without
    truncation.
38. Structural, integrity, authority, history, and anchor failures remain
    separate result/error categories.
39. No decoder, validator, hash function, or migration performs network access,
    file writes, UI actions, or implicit authority decisions.
40. Windows and POSIX principal grammar/adapters receive platform-specific tests
    before compatibility is claimed.

## 12. Open decisions requiring schema approval

| ID | Decision needed | Recommended choice | Alternative and consequence |
|---|---|---|---|
| O1 | Root placement | Mandatory `approval_authority_evidence` array in schema 2 | Embedding evidence in each approval simplifies lookup but changes ApprovalRecord wire shape and weakens clean legacy preservation |
| O2 | Principal wire form | Tagged canonical string grammars in §3.1 | Structured object is more extensible but adds nested schema and changes canonical payload; opaque string cannot reject ambiguous identities |
| O3 | Non-APPROVE declarations | Require only `NO_UNSUPPORTED_REVIEW_CLAIM`, with reason carrying rationale | Empty list is simpler but provides no explicit human attestation; full gate APPROVE declarations falsely claim review not needed for rejection/revocation |
| O4 | Evidence order | Approval-array order with legacy gaps skipped | Lexicographic approval ID is simple but disconnects evidence order from preserved decision history; arbitrary order weakens deterministic joins |
| O5 | Migration event | Add schema-2 `schema_migrated` Event action and increment generation once | No event avoids vocabulary change but leaves migration less auditable; reuse of `recovery_recorded` misstates the operation |
| O6 | Signature extension | Three explicit nullable fields; initial closed algorithm `ed25519` | Omit fields until schema 3, which delays extension; open algorithm strings make validation and security claims ambiguous |
| O7 | Signed bytes | Sign domain-separated canonical attestation bytes | Sign raw digest bytes, which is compact but requires separate unambiguous digest-algorithm/domain contracts |
| O8 | Legacy/no-evidence distinction | Structurally allow missing evidence for any approval, classify it legacy, and prohibit new missing evidence at service transaction layer | Requiring evidence for all schema-2 approvals makes migration fabricate evidence or introduce a second legacy collection |
| O9 | Migration downgrade | No automatic downgrade after migration event/schema-2 state | Allow lossy export explicitly, risking accidental loss of evidence if confused with rollback |
| O10 | Reconsideration integrity | Require same exact decision key and latest applicable REVOKE/REJECT/REVISE | Permit links across keys for narrative traceability, which cannot serve the approved barrier semantics and needs a separate relation |

No schema-2 implementation or migration should begin until O1–O10 are approved
or replaced by explicit owner decisions.

## 13. Proposed implementation sequence

After schema approval, use separate reviewable stages:

1. add immutable schema-2 model types and local invariants only;
2. add strict version-dispatched decoder/encoder and real golden JSON fixtures;
3. implement canonical attestation bytes/digest and independent golden vectors;
4. add schema-2 referential/integrity checks without authority policy;
5. implement pure schema-1→2 in-memory migration with idempotency tests;
6. specify and separately implement migration persistence/atomicity;
7. add read-only authority-policy evaluation in a later approved authority
   stage;
8. run independent compatibility/security review before enabling decision writes.

Each stage must preserve schema-1 behavior and must not infer production
readiness or rights compliance from authority evidence.

## 14. Conflict review

No contradiction with E00 or E01.3.7.3a was found. Schema 2 is required because
silently extending schema 1 would contradict strict versioning and closed-field
rules. The proposed evidence does not alter `RevisionRef`, revision hashes,
dependency graph edges, dependency digest, decision-history chronology, or
editorial HANDOFF scope.

The proposed `schema_migrated` Event action and the precise non-APPROVE
declaration set are new schema details not fixed by E01.3.7.3a; they are clearly
listed as O5 and O3 rather than asserted as approved rules.
