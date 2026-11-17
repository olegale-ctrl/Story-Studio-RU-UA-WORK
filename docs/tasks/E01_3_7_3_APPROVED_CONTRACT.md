# E01.3.7.3a — Approved Approval Authority and Human Review Contract

Status: **APPROVED — OWNER DECISION RECORDED**

This document is a normative project decision for future implementation. It
records approved architecture; it does not claim that authority, authentication,
review sessions, rollback protection, or effective approval evaluation already
exist.

## 1. Purpose and applicability

The contract defines the minimum authority and human-review evidence required
before a stored `ApprovalRecord` may be recognized as an effective editorial
decision. It applies after the existing integrity, dependency-consistency, and
decision-history checks.

The exact decision key remains:

`(gate, editorial_policy_version, full object_ref, dependency_digest)`.

Authority does not repair or bypass an invalid checksum, graph, revision hash,
rights binding, active chain, package, digest, or ambiguous decision history.
Authority evaluation is editorial only. It does not establish copyright,
rights-policy compliance, production readiness, or permission to render,
export, publish, distribute, or use content commercially.

## 2. Source of approval

The owner explicitly approved all recommended decisions A1–A14 from
[`E01_3_7_3_AUTHORITY_CONTRACT_PROPOSAL.md`](E01_3_7_3_AUTHORITY_CONTRACT_PROPOSAL.md),
commit `c176fd88a1017b7c9bd7ab23b55118761bcb9dd7`, in the project working dialogue.

The owner additionally clarified A11: a missing, unavailable, or mismatched
protected head anchor must block recognition of an editorial approval as
effective until trust is restored explicitly. Draft reading, diagnostics, and
safe history inspection must remain available.

This record is a project-governance statement. It is not a legal signature,
certificate, cryptographic attestation, user identifier, or proof of the
owner's identity.

## 3. Approved decisions A1–A14

| ID | Approved decision |
|---|---|
| A1 — Identity | Obtain identity from the operating system: Windows SID on Windows; POSIX UID plus machine identifier on compatible Unix systems. `ApprovalRecord.actor` remains a display name and is not identity evidence. |
| A2 — Authority | Use an explicit versioned allow-list with permissions for particular gates and decisions. Missing policy, principal mapping, or permission denies effective authority. The current OS user receives no automatic all-gate authority. |
| A3 — Evidence | Add a separate `ApprovalAuthorityEvidence` type in a future versioned schema. Do not overload `actor`, `reason`, or `review_declarations` with identity or authority proof. |
| A4 — Cryptographic signatures | Signatures are optional in the basic offline MVP, but the architecture must permit later addition. Without signatures and an external trusted anchor, the system must not claim cryptographic authenticity. |
| A5 — Review declarations | Use closed machine-readable declaration codes separated by SCRIPT, SCENES, and editorial HANDOFF. Present localized Russian and Ukrainian text. A human must explicitly confirm every required item. |
| A6 — Equal timestamps | Preserve E01.3.7.2 semantics. Equivalent decisions at one timestamp may project one state without choosing a record. Different decisions or materially different metadata are ambiguous. |
| A7 — REVOKE authority | Configure REVOKE permission explicitly per gate and support a separate revoker permission. Do not grant revocation to every user automatically. |
| A8 — Re-approval after REVOKE | Require a new review session, all declarations again, a link to the latest corresponding REVOKE, authority verification, repeated integrity/current checks, and a new decision sequence. A later timestamp alone is insufficient. |
| A9 — REJECT/REVISE reconsideration | APPROVE of the same exact key after REJECT or REVISE requires a new review session and link to the reconsidered record. A new key still requires a complete ordinary review. |
| A10 — Idempotency | Use separate request ID and review-session ID. Same request ID and identical content returns the existing result; the same request ID with different content is a conflict. |
| A11 — Rollback detection | Maintain an OS-protected last-seen generation/head anchor outside editable snapshot state. Missing, unavailable, or mismatched anchor blocks effective authority evaluation but not safe read-only access. Trust initialization, migration, and recovery are explicit future procedures. |
| A12 — Policy separation | Keep editorial review policy and authority policy as independent identifiers and versions. One must never be inferred from the other. |
| A13 — Legacy approvals | Preserve schema-1 approvals as history with `UNAUTHENTICATED_LEGACY` semantics. They receive no effective authority automatically. |
| A14 — HANDOFF | Current HANDOFF remains editorial only. HANDOFF approval or authority evaluation does not establish render/export/publication/commercial readiness. |

All fourteen decisions are approved together. Implementations must not select a
weaker alternative from the proposal without another explicit owner decision.

## 4. Offline MVP trust model

### 4.1 Identity boundary

The local operating-system session is the basic authentication boundary. A
platform adapter derives a stable principal identifier:

- Windows: Windows SID;
- compatible Unix: POSIX UID combined with a stable machine identifier.

The principal identifier must not come from a CLI argument, editable project
file, `ApprovalRecord.actor`, display name, environment boolean, or caller claim.
The adapter may provide a display name, but the display name has no authority by
itself.

The basic MVP trusts the local OS, installed application, and protected policy
files. It does not resist a system administrator, malware with equivalent
privileges, a modified executable, or complete machine compromise.

### 4.2 Authority policy

Authority policy is an offline, explicit, versioned allow-list:

`principal_id -> gate -> permitted decisions`.

The policy must support separate permissions for APPROVE, REJECT, REVISE, and
REVOKE. SCRIPT permission does not imply SCENES or HANDOFF permission. REVOKE may
use a distinct `can_revoke` grant.

Fail-closed conditions include:

- authentication adapter unavailable or unsupported;
- principal not identified;
- authority policy missing, unreadable, malformed, or unsupported;
- policy version unavailable or different from recorded evidence;
- principal absent from policy;
- gate absent from permission;
- decision absent from permission;
- authority evidence missing or inconsistent;
- protected anchor unavailable, missing, or mismatched;
- any prerequisite integrity, consistency, or history failure.

No fallback grants the current user every permission.

### 4.3 Policy separation

The editorial policy version remains part of the dependency digest and answers
which content-review rules apply. The authority policy answers which principal
may make which decision. Both identities and versions must be recorded and
checked independently. `GenreProfile.review_policy_version` does not select or
grant authority.

## 5. ApprovalAuthorityEvidence and schema direction

The current schema-1 `ApprovalRecord` is insufficient for authority. A future
versioned schema must define a separate immutable one-to-one evidence object.
Its minimum proposed contract, to be finalized in a separate schema-design
stage, must represent:

- exact `approval_id`;
- stable `principal_id` and captured display name;
- authority policy ID and version;
- unique `review_session_id`;
- unique idempotency `request_id`;
- closed declaration codes;
- attestation time;
- nullable `reconsiders_record_id`;
- canonical attestation digest;
- extension points for signing key ID and signature.

Evidence must be covered by the full snapshot checksum. A digest/checksum is not
authentication. If signatures are introduced, verification keys and trust
roots cannot be trusted merely because they appear inside the same editable
snapshot.

Schema 1 must not be changed silently. Migration rules belong to the schema
stage. Existing schema-1 ApprovalRecords remain preserved and queryable as
`UNAUTHENTICATED_LEGACY`; migration cannot manufacture missing principal,
session, declaration, signature, or authority evidence.

## 6. Human review sessions and declarations

A review session binds one authenticated principal, one authority-policy
version, and one exact decision key. It is not reusable for another key. A
retry may resume the same session; a new human review requires a new session.

Every required declaration is a closed code confirmed individually by the
human. UI strings are localized to Russian and Ukrainian without changing the
code. Unknown, duplicate, missing, or wrong-gate codes invalidate the review
evidence.

### 6.1 SCRIPT declarations

- `SCRIPT_EXACT_TEXT_REVIEWED`;
- `MATERIAL_CLAIMS_REVIEWED`;
- `EVIDENCE_AND_QUALIFICATIONS_REVIEWED`;
- `FICTION_DISCLOSURES_REVIEWED`;
- `LANGUAGE_ALIGNMENT_REVIEWED`;
- `SOURCE_RIGHTS_STATUS_ACKNOWLEDGED`;
- `NO_UNSUPPORTED_REVIEW_CLAIM`.

The rights acknowledgment records that rights status was displayed. It neither
creates a licence nor overrides a rights-policy result.

### 6.2 SCENES declarations

- `CURRENT_SCRIPT_DECISION_REVIEWED`;
- `SCENE_TEXT_COVERAGE_REVIEWED`;
- `SCENE_VISUAL_MEANING_REVIEWED`;
- `ASSET_PROVENANCE_VISIBLE`;
- `ASSET_RIGHTS_STATUS_ACKNOWLEDGED`;
- `DISCLOSURES_VISIBLE_IN_SCENES`;
- `NO_UNSUPPORTED_REVIEW_CLAIM`.

### 6.3 Editorial HANDOFF declarations

- `EDITORIAL_SCRIPT_AND_SCENES_REVIEWED`;
- `EDITORIAL_ASSET_SET_REVIEWED`;
- `CURRENT_RECORDED_DECISIONS_VISIBLE`;
- `RIGHTS_STATUS_ACKNOWLEDGED_NOT_GRANTED`;
- `HANDOFF_IS_EDITORIAL_ONLY`;
- `NO_RENDER_OR_EXPORT_AUTHORIZATION`;
- `NO_UNSUPPORTED_REVIEW_CLAIM`.

Production manifest/readiness declarations are outside this contract.

## 7. Decision and reconsideration semantics

### 7.1 APPROVE

An APPROVE can become an effective recorded editorial decision only when the
exact snapshot/current package is valid, dependency-consistent, history is
unambiguous, principal and authority policy are valid, the protected anchor is
trusted, and all gate declarations are attested in an eligible review session.

The result must not be named or interpreted as production readiness.

### 7.2 REJECT and REVISE

REJECT and REVISE remain immutable history for the exact decision key. Both
require gate/decision authority and a nonempty reason. Active-ref changes do not
delete or supersede them implicitly.

APPROVE after REJECT or REVISE for the same key requires a new review session
and `reconsiders_record_id` pointing to the latest relevant record. For a new
decision key, a complete ordinary review is required; history is retained under
the old key.

### 7.3 REVOKE

REVOKE requires explicit gate-specific revoker permission and a nonempty reason.
The latest effective REVOKE forms a barrier for that exact key. Earlier APPROVE
does not revive through active-ref changes, historical digest reuse, snapshot
checksum recalculation, or selection of an older coherent chain.

### 7.4 Re-approval after REVOKE

A later APPROVE for the same key requires all of:

1. a new review session;
2. repeated confirmation of every current gate declaration;
3. `reconsiders_record_id` referencing the latest effective REVOKE;
4. current authenticated-principal and authority checks;
5. fresh full integrity, dependency consistency, and history evaluation;
6. a new decision transaction sequence after the REVOKE;
7. a trusted matching protected head anchor.

A later timestamp is insufficient. It is descriptive data and may reflect a
changed system clock. The future service must not reactivate an old APPROVE.

### 7.5 Equal timestamps

E01.3.7.2 behavior remains normative:

- different latest decisions at the same timestamp are ambiguous;
- the same decision with materially different actor/reason/declarations is
  ambiguous;
- semantically equivalent latest decisions may project one recorded state,
  while all IDs are retained and no arbitrary latest record is selected.

Authority evaluation fails closed for ambiguous history.

## 8. Idempotency

Idempotency uses both request ID and review-session ID:

- same request ID, same session, and identical canonical command returns the
  existing record/evidence;
- same request ID with different content is an idempotency conflict;
- the same decision key alone is not an idempotency key;
- a different ApprovalRecord UUID does not turn a retry into a new review;
- an explicitly started new human review uses a new session and request;
- a pre-REVOKE session can never record a post-REVOKE APPROVE;
- REJECT, REVISE, and REVOKE follow the same retry rules.

Canonical command contents and persistence mechanics require a later approved
write-command contract.

## 9. Protected head anchor and trust recovery

### 9.1 Required evaluation behavior

The application maintains an OS-protected last-seen generation/head anchor
outside editable snapshot state. Its exact storage adapter and format remain a
future design task.

Authority evaluation behavior is fixed:

1. matching trusted anchor permits later authority checks to continue;
2. mismatched anchor blocks recognition of any approval as effective;
3. missing or unavailable anchor also blocks effective authority evaluation;
4. draft reading, structural/integrity diagnostics, and safe history inspection
   remain available in all three blocked states;
5. no error path automatically writes the current snapshot as the new anchor.

The result must distinguish at least `ANCHOR_MISSING`, `ANCHOR_UNAVAILABLE`, and
`ANCHOR_MISMATCH`. None may be converted into a warning while returning an
effective approval.

### 9.2 Future initialization, migration, and recovery

Trust establishment is always an explicit procedure:

- first initialization identifies the production and deliberately establishes
  its first trusted head;
- project transfer verifies the source package and deliberately binds it to the
  destination machine/principal policy;
- recovery presents snapshot generation/head, available backups, history, and
  consequences to an authenticated principal with recovery permission;
- successful recovery records a new trusted anchor and auditable recovery event
  atomically under a separately approved storage contract;
- failure or cancellation leaves authority blocked.

The recovery mechanism is not implemented or authorized by this document. A
local anchor cannot resist a system administrator or total machine compromise.

## 10. Security limitations

The basic unsigned offline MVP can:

- prevent ordinary free-form actor spoofing through supported commands;
- enforce explicit local gate/decision permissions;
- require structured human declarations;
- preserve revocation and reconsideration history;
- block on ambiguous history or anchor problems;
- detect accidental state corruption through existing hashes/checksum.

It cannot:

- provide non-repudiation or cryptographic authenticity of approvals;
- resist a local administrator, compromised OS, stolen authenticated session,
  modified executable, or attacker controlling policy and anchor;
- establish trusted wall-clock time;
- prove factual truth, source authenticity, legal rights, or reviewer expertise;
- guarantee that a human actually understood declarations;
- infer authority from actor, UUID, timestamp, checksum, digest, or status.

Optional future signatures must cover the exact decision key, evidence, session,
request ID, policy versions, reconsidered record, and transaction/head context.
They require protected private keys and trusted public-key lifecycle rules.

## 11. Editorial approval, rights, and readiness separation

Three independent layers remain mandatory:

1. **Editorial authority**: who recorded a reviewed editorial decision and
   whether the decision is effective under this contract.
2. **Rights compliance**: intended use, allowed actions, expiry, material
   binding, and applicable licence/legal policy. An editor cannot grant missing
   rights.
3. **Production readiness**: frozen media/config manifest, staged bytes,
   capability checks, current effective decisions, timing/audio/render
   preflight, and final revalidation.

Success at one layer never implies success at another. Current HANDOFF remains
an editorial dependency package and editorial decision only.

## 12. Compatibility with E00 and schema 1

No conflict with E00 was found. This contract refines E00 §4 requirements that
human review and authority cannot be inferred from status or caller input. It
preserves E00's exact dependencies, immutable history, revocation behavior,
offline-first operation, rights separation, and non-readiness of editorial
state.

This contract does not modify E00 or schema 1. Current schema-1 approvals remain
valid historical data but have `UNAUTHENTICATED_LEGACY` authority status. They
may still be inspected by E01.3.7.1 consistency and E01.3.7.2 history
projections. They cannot become effective merely because they are consistent or
latest.

A future schema version must define evidence representation and migration.
Migration must preserve IDs, order, decisions, actor text, timestamps, reasons,
declarations, exact decision keys, and ambiguity. It must not invent evidence.

## 13. Phased implementation plan

Each stage requires a separate task, review, and owner authorization:

1. **Schema contract**: define the versioned `ApprovalAuthorityEvidence`, closed
   declaration vocabularies, canonical attestation payload, migration, and
   optional signature extension points. No authority evaluation yet.
2. **Authority policy model**: define principal identifiers, policy file/schema,
   gate/decision grants, revoker/recovery permissions, versioning, and platform
   adapter boundaries. No implicit default authority.
3. **Read-only authority evaluation**: compose integrity, consistency, history,
   anchor status, evidence, and authority policy into structured results. No
   commands or persistence.
4. **Review sessions and declarations**: implement in-memory session state,
   exact package binding, localized presentation contract, declaration capture,
   reconsideration linkage, and expiry/cancellation rules. No durable decisions.
5. **Decision commands and idempotency**: define canonical commands, request-ID
   behavior, session consumption, revalidation, and append-only record/evidence
   creation. Still separate from production readiness.
6. **Atomic storage and head anchor**: integrate expected generation, writer
   lock, atomic snapshot save, protected anchor update, initialization, transfer,
   and explicit recovery. This stage must define commit points and failure
   recovery before implementation.
7. **Integration tests and audit**: test Windows and POSIX adapters on their
   platforms, migration, tampering, rollback, clock changes, idempotency,
   revocation, crash boundaries, and security claims. Independently review the
   threat model and documentation.

No stage may silently combine authority success with rights compliance or
production readiness.

## 14. Acceptance criteria for future implementation

The approved implementation must demonstrate:

1. free-form actor cannot grant identity or authority;
2. Windows SID and POSIX UID+machine adapters follow one documented principal
   contract;
3. missing/unknown principal, policy, permission, evidence, or anchor fails
   closed;
4. permission is both gate-specific and decision-specific;
5. authority policy identity/version is independent of editorial policy;
6. integrity, exact consistency, and unambiguous history are prerequisites;
7. every required gate declaration is present exactly once;
8. unknown, duplicate, or wrong-gate declarations are rejected;
9. SCRIPT, SCENES, and editorial HANDOFF declaration sets remain distinct;
10. APPROVE without eligible session/evidence is ineffective;
11. REJECT, REVISE, and REVOKE remain visible and are not filtered out;
12. the latest effective REVOKE blocks every older APPROVE for the exact key;
13. returning active refs to a revoked key remains revoked;
14. post-REVOKE approval requires a new session, complete declarations, exact
    link to the latest REVOKE, permission, and fresh validation;
15. same-key approval after REJECT/REVISE requires a new linked review session;
16. timestamp alone cannot establish review, authority, or reconsideration;
17. identical retry by request ID is idempotent;
18. reuse of request ID with changed canonical content is rejected;
19. same decision key or a new record UUID does not substitute for request ID;
20. conflicting or materially different same-time history fails closed;
21. semantically equivalent same-time records retain all IDs without arbitrary
    latest-record selection;
22. missing, unavailable, and mismatched anchors produce distinct blocking
    results;
23. blocked anchor states still allow draft reading, diagnostics, and safe
    history inspection;
24. anchor problems never trigger automatic trust reset;
25. initialization, transfer, and recovery require explicit trusted procedures;
26. schema-1 records remain `UNAUTHENTICATED_LEGACY` and are not grandfathered;
27. JSON plus recalculated checksum is never described as authenticated;
28. rights-policy failure cannot be overridden by editorial authority;
29. authority success exposes no readiness/render/export/commercial permission;
30. evaluation does not mutate snapshot, history, actor, timestamps, active refs,
    policy, or anchor;
31. read-only evaluation performs no file or network writes;
32. optional signatures can be added without changing decision-key semantics;
33. platform compatibility claims are supported by actual Windows/POSIX runs;
34. migrations preserve history without manufacturing missing evidence;
35. failure diagnostics identify the exact blocked prerequisite without a
    generic success/failure boolean replacing structured reasons.

## 15. Implementation status

Approved architecture now exists only as this contract. The following remain
unimplemented: `ApprovalAuthorityEvidence`, schema migration, principal
adapters, authority policy, declarations, review sessions, effective authority
evaluation, idempotent decision commands, protected anchor, trust recovery,
signatures, rights policy, and production readiness.

No approved decision in this document is evidence that these mechanisms have
already been executed or that any existing ApprovalRecord is authoritative.
