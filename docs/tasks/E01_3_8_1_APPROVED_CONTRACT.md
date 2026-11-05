# E01.3.8.1a — Approved Schema 2 Authority Evidence Contract

Status: **APPROVED — OWNER DECISION RECORDED**

This document is the normative schema contract for future implementation of
`ApprovalAuthorityEvidence`. Schema 2 is not implemented by this document. No
existing project is migrated, no authority evaluation is enabled, and schema 1
remains unchanged.

## 1. Purpose and approval source

Schema 2 adds immutable evidence needed to associate a stored ApprovalRecord
with an OS-derived principal, authority policy, review session, idempotent
request, human declarations, and reconsideration history.

The owner explicitly approved O1–O10 from
[`E01_3_8_1_AUTHORITY_SCHEMA_PROPOSAL.md`](E01_3_8_1_AUTHORITY_SCHEMA_PROPOSAL.md),
commit `c69cea506d25fbc9c2ff30c46082816f4ff4c335`, in the project working dialogue.
The owner also approved the additional O8 and O10 restrictions recorded in
§4. This statement records project governance only. It is not a digital
signature, certificate, owner identifier, or cryptographic proof.

Normative dependencies remain E00, the approved E01.3.4a package contract, the
approved E01.3.7.3a authority contract, and E01.3.7.1–E01.3.7.2 exact
consistency/history semantics.

## 2. Approved decisions O1–O10

| ID | Approved decision |
|---|---|
| O1 — Evidence placement | Schema 2 has a mandatory root `approval_authority_evidence` array, present even when empty. |
| O2 — Principal identifiers | Use canonical tagged strings for Windows SID and POSIX UID plus machine identifier, exactly as §6.1 defines. The string alone is not identity proof. |
| O3 — Non-APPROVE declarations | REJECT, REVISE, and REVOKE evidence has exactly `["NO_UNSUPPORTED_REVIEW_CLAIM"]`; its nonempty ApprovalRecord reason carries rationale. |
| O4 — Evidence order | Evidence follows ApprovalRecord array order, skipping records without evidence. UUID/timestamp sorting and implicit reordering are forbidden. |
| O5 — Migration event | A committed schema-1→2 migration increments generation once, appends `schema_migrated`, preserves history, and recomputes snapshot checksum. Re-running on schema 2 is an idempotent no-op. |
| O6 — Signature extension | Schema 2 has nullable `signing_key_id`, `signature_algorithm`, and `signature`; all are null or all present. Initial algorithm is Ed25519. Signatures remain optional in the offline MVP. |
| O7 — Signed bytes | Sign domain-separated canonical attestation bytes from §8. Signature presence is not trust without a separate trusted key registry. |
| O8 — Legacy evidence | Missing evidence is structurally allowed for preserved history and yields `UNAUTHENTICATED_LEGACY`, but does not prove historical origin. New write commands must atomically create ApprovalRecord and evidence. |
| O9 — Downgrade | Automatic schema-2→1 downgrade is forbidden. Any compatibility export requires a separate explicit lossy-export contract and warning. |
| O10 — Reconsideration | `reconsiders_record_id` links the latest applicable decision of the same exact key. Cross-key, self, dangling, arbitrary UUID/array-order resolution, and ambiguous-history resolution are invalid. Verified transaction sequence is a future storage requirement. |

No O1–O10 alternative remains open for implementation. Changes require a new
owner decision and, where wire behavior changes, a later schema version.

## 3. Schema 2 envelope

`editorial_schema_version` is integer `2`. Schema 2 contains every schema-1 root
field with unchanged meaning plus:

```text
approval_authority_evidence: array<ApprovalAuthorityEvidence>
```

The array is mandatory and never null. It is logically adjacent to approvals;
JSON object key order remains semantically irrelevant because canonical JSON
sorts object keys.

Schema 2 uses closed objects: unknown or missing fields are rejected. Nullable
fields are present with explicit null. Strings preserve exact Unicode code
points and whitespace without NFC/NFD, trimming, translation, case conversion,
or implicit timezone conversion.

Existing limits remain:

- snapshot bytes: at most 32 MiB;
- JSON nesting: at most 64;
- evidence records: at most 10,000 and no more than approvals;
- general string cap: 100,000 code points, subject to narrower rules below;
- declaration codes per evidence: at most 16.

Snapshot checksum covers the complete schema-2 canonical envelope except only
root `snapshot_checksum`. Evidence, null signature fields, and non-null
signature fields are included. Evidence never enters revision content hashes,
the E01.3.2 dependency graph, or dependency digest.

Schema-1 decoding behavior stays unchanged and rejects version 2. Future codec
dispatch must select a version-specific closed contract; it must never discard
schema-2 fields to obtain a schema-1 object.

## 4. Approved O8 and O10 clarifications

### 4.1 O8: missing evidence and legacy status

Schema 2 structurally permits an ApprovalRecord with no evidence so migrated
schema-1 history is preserved. Every such record has authority status
`UNAUTHENTICATED_LEGACY` and cannot become effective automatically.

Absence of evidence does **not** prove that a record actually came from schema
1. Therefore:

1. legacy records remain readable by consistency and history projections;
2. authority evaluation fails closed for them;
3. migration creates no evidence and makes no origin/authenticity claim;
4. schema-2 decision commands must append ApprovalRecord and matching evidence
   in the same atomic transaction;
5. a new approval without evidence is a service/write-contract violation even
   though the resulting JSON shape remains structurally readable;
6. trusted transaction history and head-anchor state are required to distinguish
   legitimate migration history from fabricated no-evidence records;
7. no boolean or synthetic `is_legacy` field may manufacture provenance.

### 4.2 O10: latest applicable reconsideration

`reconsiders_record_id` is nullable but, when required, must resolve to the
latest applicable ApprovalRecord with the same exact decision key:

`(gate, editorial policy_version, full object_ref, dependency_digest)`.

- APPROVE after REVOKE links the latest applicable REVOKE.
- APPROVE after REJECT links the latest applicable REJECT.
- APPROVE after REVISE links the latest applicable REVISE.
- Initial decisions normally use null.
- Cross-key, dangling, and self references are invalid.
- Immutable prior history is never rewritten.

E01.3.7.2 timestamp projection continues to detect same-time ambiguity, but a
timestamp is not trusted transaction proof. UUID and array order cannot resolve
a tie. A future write/storage contract must provide a verified transaction
sequence bound to the protected head anchor. Until that sequence can establish
the latest applicable record, ambiguous reconsideration blocks effective
authority. This schema stores the link; it does not itself prove transaction
order or define conflict resolution.

## 5. ApprovalAuthorityEvidence wire contract

Every evidence object has exactly these keys:

| Field | Type and rule |
|---|---|
| `approval_id` | Required canonical lowercase UUID. Resolves one ApprovalRecord in this snapshot. |
| `principal_id` | Required canonical tagged string from §6.1. |
| `principal_display_name` | Required nonempty Unicode text, 1–256 code points; display only. |
| `authority_policy_id` | Required canonical lowercase UUID. |
| `authority_policy_version` | Required nonempty exact string, 1–128 code points. |
| `review_session_id` | Required canonical lowercase UUID, unique in evidence collection. |
| `request_id` | Required canonical lowercase UUID, unique in evidence collection. A retry adds no second record. |
| `declaration_codes` | Required nonempty array, at most 16, exact closed set/order for linked gate and decision. |
| `attested_at` | Required valid UTC seconds `YYYY-MM-DDTHH:MM:SSZ`; descriptive, not trusted time. |
| `reconsiders_record_id` | Required nullable canonical UUID, subject to §4.2 and §9. |
| `attestation_digest` | Required 64 lowercase hexadecimal SHA-256 from §8. |
| `signing_key_id` | Required nullable string; signature tuple rules apply. |
| `signature_algorithm` | Required nullable string; signature tuple rules apply. |
| `signature` | Required nullable canonical base64url string; signature tuple rules apply. |

Evidence is immutable. Correction creates a new ApprovalRecord/evidence pair;
it never edits old evidence.

### 5.1 Uniqueness and order

- At most one evidence object per `approval_id`.
- Every evidence links exactly one existing ApprovalRecord.
- Evidence-free ApprovalRecords are skipped when deriving evidence order.
- Remaining evidence sequence must match ApprovalRecord sequence exactly.
- `review_session_id` and `request_id` are unique across evidence.
- Principal and authority-policy identifiers may repeat.
- Arrays are validated as supplied; no decoder sorts or deduplicates them.

## 6. Principal and declaration vocabularies

### 6.1 Principal ID

Canonical forms are:

- Windows: `windows-sid:<SID>`, with SID matching
  `S-[0-9]+(-[0-9]+)+`, uppercase `S`, no whitespace;
- compatible Unix:
  `posix-uid:<uid>@machine:<machine_id>`, where uid is canonical unsigned
  decimal without leading zeros except `0`, and machine ID is exactly 32
  lowercase hexadecimal characters.

Unknown prefixes and noncanonical spellings are rejected. The platform adapter,
not user text, produces the identifier. Its presence in JSON remains an
assertion until trusted OS/policy/anchor evaluation verifies its context.

### 6.2 Declaration vocabulary version 1

Vocabulary version 1 is fixed by `editorial_schema_version=2` and the linked
ApprovalRecord gate/decision. Codes are machine identity; RU/UK localized labels
are external presentation resources.

APPROVE for SCRIPT requires exactly, in this order:

1. `SCRIPT_EXACT_TEXT_REVIEWED`
2. `MATERIAL_CLAIMS_REVIEWED`
3. `EVIDENCE_AND_QUALIFICATIONS_REVIEWED`
4. `FICTION_DISCLOSURES_REVIEWED`
5. `LANGUAGE_ALIGNMENT_REVIEWED`
6. `SOURCE_RIGHTS_STATUS_ACKNOWLEDGED`
7. `NO_UNSUPPORTED_REVIEW_CLAIM`

APPROVE for SCENES requires exactly:

1. `CURRENT_SCRIPT_DECISION_REVIEWED`
2. `SCENE_TEXT_COVERAGE_REVIEWED`
3. `SCENE_VISUAL_MEANING_REVIEWED`
4. `ASSET_PROVENANCE_VISIBLE`
5. `ASSET_RIGHTS_STATUS_ACKNOWLEDGED`
6. `DISCLOSURES_VISIBLE_IN_SCENES`
7. `NO_UNSUPPORTED_REVIEW_CLAIM`

APPROVE for editorial HANDOFF requires exactly:

1. `EDITORIAL_SCRIPT_AND_SCENES_REVIEWED`
2. `EDITORIAL_ASSET_SET_REVIEWED`
3. `CURRENT_RECORDED_DECISIONS_VISIBLE`
4. `RIGHTS_STATUS_ACKNOWLEDGED_NOT_GRANTED`
5. `HANDOFF_IS_EDITORIAL_ONLY`
6. `NO_RENDER_OR_EXPORT_AUTHORIZATION`
7. `NO_UNSUPPORTED_REVIEW_CLAIM`

REJECT, REVISE, and REVOKE for every gate require exactly:

1. `NO_UNSUPPORTED_REVIEW_CLAIM`

Their `ApprovalRecord.reason` must be nonempty and carries rationale. Unknown,
missing, extra, duplicate, wrong-gate, wrong-decision, or out-of-order codes are
rejected. Vocabulary meaning, membership, requiredness, or order changes require
a later schema version. Localization changes do not.

## 7. Exact decision and evidence binding

Evidence binds to the complete linked ApprovalRecord, whose exact decision key
contains:

- `gate`;
- editorial `policy_version`;
- full `object_ref`, including content hash;
- `dependency_digest`.

Evidence additionally binds principal, authority policy ID/version, review
session, request, declarations, attestation time, and reconsideration target.
Authority policy version remains independent of editorial policy version.

`principal_display_name` and `ApprovalRecord.actor` may be compared by future
policy, but neither proves identity. The attestation digest detects changes; it
does not authenticate their original values.

## 8. Canonical attestation and signature extension

### 8.1 Canonical payload

The attestation payload has exactly three top-level keys:

```text
approval_authority_evidence_schema_version = 1
approval_record = full schema-2 wire ApprovalRecord object
authority_evidence = all core evidence fields except digest/signature tuple
```

`approval_record` contains exactly `id`, `gate`, `object_ref`,
`dependency_digest`, `policy_version`, `actor`, `timestamp`, `decision`,
`reason`, and `review_declarations`.

`authority_evidence` contains exactly `approval_id`, `principal_id`,
`principal_display_name`, `authority_policy_id`, `authority_policy_version`,
`review_session_id`, `request_id`, `declaration_codes`, `attested_at`, and
`reconsiders_record_id`.

Canonical bytes are:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
).encode('utf-8')
```

No Unicode normalization, trimming, case conversion, hidden defaults, local
timezone conversion, path/UI state, current clock lookup, or implicit array
sorting occurs.

`attestation_digest` is lowercase
`sha256(canonical_attestation_bytes).hexdigest()`. Only
`attestation_digest`, `signing_key_id`, `signature_algorithm`, and `signature`
are absent from the hashed payload.

The digest is consistency protection, not signature, authority, trusted time,
or head anchor.

### 8.2 Optional Ed25519 signature

Signature fields are all null or all non-null. Partial tuples are invalid.

When present:

- `signature_algorithm` is exactly `ed25519`;
- `signing_key_id` is 1–128 ASCII characters matching
  `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`;
- `signature` is unpadded canonical base64url decoding to exactly 64 bytes.

Signed bytes are:

```text
ASCII("story-studio-approval-attestation-v1")
+ byte 0x00
+ canonical_attestation_bytes
```

A syntactically valid signature is not trusted without a separate protected key
registry, key status/revocation, principal and authority-policy binding, and
algorithm implementation. Signatures are optional in the basic offline MVP.

## 9. Referential, reconsideration, and integrity rules

Validation must enforce:

1. exact one-to-one evidence-to-approval linkage;
2. no duplicate evidence, session ID, or request ID;
3. evidence ordering per §5.1;
4. existing ApprovalRecord object-ref graph integrity;
5. exact principal/policy/session/request/timestamp/signature shapes;
6. exact declaration set and order;
7. correct canonical attestation digest;
8. no self or dangling reconsideration reference;
9. same exact decision key for reconsideration source and target;
10. required latest applicable decision type under §4.2;
11. authority-blocking ambiguity when latest history cannot be established;
12. evidence inclusion in snapshot checksum;
13. evidence exclusion from revision hashes and dependency digest.

Structural absence of evidence is permitted but produces
`UNAUTHENTICATED_LEGACY`. It is not equivalent to successful authority evidence.

The schema has no trusted transaction-sequence field. The future atomic storage
contract must bind verified sequence/head state externally or in a separately
approved versioned transaction contract. Until then, reconsideration linkage
can be checked for shape, same-key relation, and known history, but effective
authority must block wherever “latest applicable” depends on untrusted or
ambiguous ordering.

## 10. Schema-1 to schema-2 migration

### 10.1 Preconditions

Input must pass schema-1 strict decoding and complete snapshot integrity. Any
checksum, graph, revision-hash, rights-binding, duplicate-ID, or format failure
aborts without output or repair.

Migration does not initialize, update, or restore the protected head anchor.
A11 applies independently: anchor missing/unavailable/mismatch blocks effective
authority while read-only inspection remains possible.

### 10.2 Exact transform

One committed migration:

1. preserves all existing root values and collection order;
2. changes `editorial_schema_version` from 1 to 2;
3. adds `approval_authority_evidence: []`;
4. preserves every ApprovalRecord field and array position exactly;
5. classifies every evidence-free approval as `UNAUTHENTICATED_LEGACY` without
   asserting its origin;
6. preserves revision payloads and all revision content hashes;
7. preserves exact Unicode and semantically meaningful array order;
8. increments generation exactly once;
9. appends exactly one Event with action `schema_migrated`, authenticated
   migration display actor, UTC time, empty refs, reason identifying schema 1→2,
   and null error code;
10. recomputes the complete schema-2 snapshot checksum after all changes;
11. does not create authority evidence, signature, session, request, or
    reconsideration link;
12. does not modify historical APPROVE/REJECT/REVISE/REVOKE semantics.

Schema 2 extends the closed Event action vocabulary with `schema_migrated`.

### 10.3 Idempotency and downgrade

Calling migration on schema 2 returns `ALREADY_MIGRATED` as a no-op: no
generation change, event, checksum rewrite, or byte change.

Automatic downgrade is forbidden. A future compatibility export must be an
explicit, separately specified lossy operation that never overwrites schema 2,
warns about discarded evidence/events, and cannot be called rollback or trust
recovery.

Migration does not make a snapshot a trusted head. First trust establishment,
machine transfer, and recovery remain explicit future procedures.

## 11. Error and result taxonomy

### Structural/schema errors

- `SCHEMA_VERSION_UNSUPPORTED`;
- `MISSING_FIELD`, `UNKNOWN_FIELD`;
- `EVIDENCE_DUPLICATE_APPROVAL`, `EVIDENCE_ORDER`;
- `APPROVAL_TARGET_MISSING`;
- `PRINCIPAL_ID_FORMAT`, `POLICY_ID_FORMAT`, `POLICY_VERSION_FORMAT`;
- `DUPLICATE_DECLARATION`, `DECLARATION_SET`;
- `DATE` for attestation timestamp;
- `RECONSIDERATION_TARGET_MISSING`, `RECONSIDERATION_SELF_REFERENCE`;
- `SIGNATURE_FIELDS_INCOMPLETE`, `SIGNATURE_ALGORITHM`, `SIGNATURE_FORMAT`;
- `LIMIT`.

### Integrity errors

- `ATTESTATION_DIGEST_MISMATCH` at exact digest path;
- existing snapshot checksum, graph, revision hash, and rights-binding errors;
- duplicate session/request IDs;
- same-key/reconsideration-history mismatch.

### Authority results/failures

Unknown principal, policy unavailable, permission absent, legacy evidence,
untrusted signature, or wrong authority-policy version are not malformed JSON.
They block authority with structured reasons.

### History results

`AMBIGUOUS_HISTORY` remains a history projection, blocks authority, and is never
converted to a chosen UUID/array position.

### Trust-anchor results

`ANCHOR_MISSING`, `ANCHOR_UNAVAILABLE`, and `ANCHOR_MISMATCH` are distinct
blocking trust results. They permit safe decode, diagnostics, and history
inspection and never trigger automatic anchor replacement.

## 12. Compatibility and security limits

No conflict with E00 or E01.3.7.3a was found. Schema 2 refines authority
evidence without changing `RevisionRef`, immutable revision history, dependency
closure, revision hashing, current package, consistency, decision key, rights
separation, or editorial HANDOFF scope.

Schema 1 remains supported and unchanged. E01.3.7.1 consistency and E01.3.7.2
history must produce equivalent results for preserved records before and after
migration. Evidence adds no production readiness or rights permission.

Unsigned evidence and checksum cannot provide non-repudiation or resist an
attacker able to alter snapshot, policy, application, and anchor. Principal ID,
UUID, timestamp, digest, actor, and signature-shaped bytes are not independently
trusted. A local administrator or fully compromised machine remains outside the
basic MVP trust boundary.

## 13. Acceptance criteria for future implementation

1. Schema-1 model/codec behavior and fixtures remain unchanged.
2. Version dispatch rejects unsupported versions without dropping fields.
3. Schema 2 requires `approval_authority_evidence`, including empty array.
4. Root and nested schema-2 objects enforce exact field sets and explicit nulls.
5. Strict codec rejects duplicate JSON keys, BOM, invalid UTF-8, floats,
   NaN/Infinity, invalid Unicode, unknown fields, and wrong scalar types.
6. Schema-2 encode/decode round-trip preserves all values and array order.
7. Model and nested evidence collections are immutable.
8. Evidence links exactly one existing ApprovalRecord.
9. Duplicate/dangling evidence has stable codes and exact paths.
10. Evidence order follows approvals order with no implicit sort.
11. Principal IDs accept only canonical approved Windows/POSIX forms.
12. Authority policy, session, request, and reconsideration IDs enforce exact
    shape and uniqueness.
13. APPROVE declaration set is exact for SCRIPT, SCENES, and HANDOFF.
14. REJECT/REVISE/REVOKE set is exactly
    `NO_UNSUPPORTED_REVIEW_CLAIM`.
15. Unknown, missing, duplicate, extra, wrong-gate, and out-of-order declaration
    codes are rejected.
16. RU/UK localized labels do not affect code identity or digest.
17. Canonical attestation bytes match independently produced literal golden
    vectors.
18. Attestation digest is lowercase SHA-256 over exactly §8.1 payload.
19. Every linked ApprovalRecord/core-evidence change changes the digest.
20. Exact Unicode, emoji, combining characters, whitespace, and array order are
    preserved without normalization.
21. Signature tuple enforces all-null/all-present.
22. Ed25519 identifier, key ID, and base64url signature shape are strict.
23. Signature presence without trusted registry never yields authenticated
    authority.
24. Snapshot checksum covers evidence and all signature fields.
25. Evidence changes never alter revision content hashes or dependency digest.
26. Reconsideration rejects dangling, self, cross-key, and wrong-type links.
27. Ambiguous latest history blocks reconsideration and authority.
28. No timestamp, UUID, or array position resolves ambiguous transaction order.
29. Missing evidence remains readable as `UNAUTHENTICATED_LEGACY` but cannot
    become effective.
30. Write-service contract forbids committing a new approval without evidence.
31. Migration preserves every schema-1 ApprovalRecord field and position.
32. Migration creates no evidence or retroactive authenticity.
33. Migration preserves revision payloads/content hashes and history projection.
34. Migration increments generation once and appends one `schema_migrated`
    event.
35. Migration computes a valid schema-2 checksum.
36. Re-running migration on schema 2 is a byte-preserving no-op.
37. Corrupt source produces no output or partial migration.
38. Migration never initializes or updates protected anchor.
39. Missing/unavailable/mismatched anchor blocks authority but not read-only
    decode, diagnostics, consistency, or history.
40. Automatic downgrade is unavailable.
41. Structural, integrity, authority, history, and anchor failures stay separate.
42. Limits fail explicitly without truncation.
43. Read-only codecs/validators/hashers perform no file/network/subprocess I/O.
44. Migration core is pure in-memory; persistence belongs to a later atomic
    storage stage.
45. E01.3.7.1 produces the same consistency for preserved legacy records.
46. E01.3.7.2 preserves record grouping, order, state, and ambiguity.
47. New schema-2 records include unique request/review-session IDs.
48. Same request retry does not add evidence or history; changed content with the
    same request ID conflicts.
49. Actual Windows and POSIX runs precede platform compatibility claims.
50. Authority success exposes no readiness, render, export, publication,
    distribution, rights, or commercial-use permission.

## 14. Implementation plan and control points

Every stage requires a separate assignment and review:

1. **E01.3.8.2 — immutable schema-2 models**: local value types and invariants;
   no codec, migration, authority evaluator, or storage.
2. **E01.3.8.3 — strict versioned codec**: explicit schema dispatch, schema-2
   round-trip, limits, and real fixtures; preserve schema-1 behavior.
3. **E01.3.8.4 — canonical attestation digest**: joined payload, golden bytes,
   SHA-256, signature field shape; no trusted signature registry.
4. **E01.3.8.5 — schema-2 integrity**: evidence joins, order, declarations,
   reconsideration checks to the extent supported by verified history; no
   authority policy.
5. **E01.3.8.6 — pure in-memory migration**: verified schema-1 input to schema 2,
   migration event, generation, checksum, idempotency; no file writes/anchor.
6. **Atomic storage design and implementation**: writer lock, expected
   generation, commit point, snapshot/anchor ordering, retry, transfer, recovery,
   and verified transaction sequence. Design approval precedes code.
7. **Authority policy and read-only evaluation**: OS principal adapters,
   allow-list, anchor status, evidence/policy/history composition; no readiness.
8. **Review/write commands**: sessions, declarations, request idempotency,
   atomic ApprovalRecord+evidence creation, reconsideration barriers.
9. **Integration/security audit**: platform runs, rollback/tamper/crash tests,
   migration compatibility, threat-model review.

Approval of this plan is not authorization to execute stages consecutively.

## 15. Implementation status

Schema 2, `ApprovalAuthorityEvidence`, migration, Ed25519 verification, authority
policy, principal adapters, protected anchor, transaction sequence, review
sessions, decision commands, trust recovery, and authority evaluation are not
implemented.

This document does not modify E00, schema 1, existing snapshots, Python code, or
tests. It records the approved target contract only.
