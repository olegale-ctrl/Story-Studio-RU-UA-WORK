# E01.3.7.3 — Approval Authority and Human Review Contract Proposal

Status: **PROPOSAL — OWNER DECISION REQUIRED**. This document does not amend
E00, authorize implementation, or make any recorded approval authoritative.

Basis: E00 §4, the approved E01.3.4a package contract, and implemented
E01.3.7.1–E01.3.7.2 consistency/history projections. The proposal preserves
their exact decision key:

`(gate, policy_version, full object_ref, dependency_digest)`.

## 1. Purpose and boundaries

The future authority layer must decide whether a dependency-consistent recorded
decision may be treated as an effective editorial decision. It must establish:

1. which locally authenticated principal initiated the command;
2. whether the applicable policy authorizes that principal for the gate and
   decision;
3. whether the required human review was explicitly completed for the exact
   package;
4. whether decision history, especially REVOKE, permits the requested state.

The authority layer consumes the existing full integrity, current package,
dependency consistency, and history results. It never replaces them. It does
not establish factual truth, copyright ownership, rights-policy compliance,
production readiness, or permission to render/export.

This proposal covers a local, offline-first, single-user MVP. It does not design
an organization-wide identity provider, remote authorization server, PKI,
multi-user workflow, or legal electronic signature.

## 2. Terms

- **Actor**: the display string stored in `ApprovalRecord.actor`. Under the
  current model it is an assertion, not identity evidence.
- **Authenticated principal**: a stable local identifier obtained from a
  trusted authentication adapter, such as a Windows SID or POSIX uid plus the
  local machine identity. A display name is metadata, not the identifier.
- **Authorized reviewer**: an authenticated principal to which a trusted,
  versioned policy grants a specific action for a specific gate.
- **Decision key**: exact gate, literal policy version, full `RevisionRef`, and
  dependency digest.
- **Review session**: one explicit human examination of one decision key under
  one authority policy version. Retrying a command does not create a new review
  session.
- **Review attestation**: immutable evidence that a principal explicitly made
  the required declarations for a decision key during a review session.
- **Effective recorded decision**: a decision that passes integrity,
  consistency, history, authority, and attestation checks. It remains an
  editorial result, not production readiness or a rights grant.
- **Revocation barrier**: the latest effective REVOKE for a decision key. It
  prevents any earlier APPROVE from becoming effective again.

## 3. Trust model

### 3.1 Recommended MVP boundary

The recommended minimum is a **trusted local workstation boundary**:

- the operating system authenticates the current user;
- an adapter derives a stable principal identifier without accepting it as a
  CLI parameter;
- a locally provisioned authority policy, stored outside editable production
  JSON and protected by OS permissions, maps principal identifiers to allowed
  `(gate, decision)` actions;
- the command displays the exact current package identity and declarations;
- the human confirms each declaration explicitly;
- the service writes an immutable record and attestation in one future atomic
  snapshot transaction.

This prevents accidental actor substitution through normal application flows.
It does not resist a machine administrator, modified executable, compromised OS,
or attacker who can replace both policy and state.

`ApprovalRecord.actor` should be generated from the authenticated principal's
configured display name. Free-form actor input must not be an authority source.
The stable principal identifier must be retained in separate authority evidence;
overloading `actor` would break display-name compatibility and still provide no
proof.

### 3.2 Current schema limitation

The current `ApprovalRecord` cannot prove authentication or a new review after
REVOKE. It has no principal identifier, authority-policy reference, review
session identifier, attestation digest, revocation link, key identifier, or
signature. `review_declarations` is an arbitrary tuple of strings and can be
edited together with the checksum.

The recommended future contract therefore adds an immutable
`ApprovalAuthorityEvidence` companion in a versioned editorial schema rather
than silently changing schema 1. Proposed fields are:

- `approval_id`: exact one-to-one link to `ApprovalRecord.id`;
- `principal_id`: stable local principal identifier;
- `principal_display_name`: captured display value;
- `authority_policy_id` and `authority_policy_version`;
- `review_session_id`: UUID unique to an explicit review session;
- `declaration_codes`: ordered or canonically sorted closed vocabulary;
- `attested_at`: recorded UTC time;
- `reconsiders_record_id`: nullable exact REVOKE/REJECT/REVISE ID;
- `attestation_digest`: SHA-256 of the canonical attestation payload;
- optional future `signing_key_id` and `signature` for the stronger threat
  model.

The companion must be covered by snapshot checksum. Hashing it is useful for
consistency but is not authentication. Cryptographic signature verification
requires a trusted public-key registry outside the attacker-editable snapshot.

## 4. MVP authority model

### 4.1 Policy

Recommended policy form: an offline, versioned allow-list with entries:

`principal_id -> allowed gates -> allowed decisions`.

Policy version used for authority is separate from the editorial
`policy_version` included in dependency digest. The former answers “who may
decide”; the latter identifies the review rules used by the package. Both must
be recorded and checked. Neither is inferred from `GenreProfile`.

Minimum defaults should grant no authority when the policy, principal mapping,
or authentication adapter is missing. There must be no “current OS user is
automatically reviewer for every gate” fallback.

Suggested action defaults for a single configured owner-reviewer:

- APPROVE, REJECT, and REVISE require reviewer authority for that gate;
- REVOKE requires the same gate authority or a separately configured revoker
  permission;
- authority for SCRIPT does not imply SCENES or HANDOFF authority;
- authority never overrides rights-policy or integrity failures.

### 4.2 Evaluation order

A future effective-decision evaluator should fail closed in this order:

1. full snapshot/current package integrity;
2. exact dependency consistency;
3. unambiguous decision history for the exact key;
4. authenticated principal evidence;
5. authority policy existence, version, and gate/decision permission;
6. required gate declarations and review-session evidence;
7. revocation/reconsideration rules;
8. return an editorial authority result with explicit reasons.

It must not return `ready`, `commercial_allowed`, or `render_allowed`.

## 5. Gate-specific review declarations

Declarations should be closed machine-readable codes with localized UI text.
The human must confirm each code individually for the exact decision key. A
single generic checkbox such as “everything checked” is insufficient.

### 5.1 SCRIPT

Recommended required declarations:

- `SCRIPT_EXACT_TEXT_REVIEWED`: exact script and locale were read;
- `MATERIAL_CLAIMS_REVIEWED`: all material factual assertions were reviewed;
- `EVIDENCE_AND_QUALIFICATIONS_REVIEWED`: evidence, contradictions, disputed
  claims, and qualifications were visible and considered;
- `FICTION_DISCLOSURES_REVIEWED`: fictional/reconstructed content is disclosed
  where required by content mode;
- `LANGUAGE_ALIGNMENT_REVIEWED`: script, narration, and subtitle locale contract
  was checked;
- `SOURCE_RIGHTS_STATUS_ACKNOWLEDGED`: current source rights results were seen,
  without claiming that human acknowledgment creates a licence;
- `NO_UNSUPPORTED_REVIEW_CLAIM`: reviewer is not asserting checks that were not
  actually performed.

### 5.2 SCENES

Recommended required declarations:

- `CURRENT_SCRIPT_DECISION_REVIEWED`: the exact referenced script decision and
  staleness state were visible;
- `SCENE_TEXT_COVERAGE_REVIEWED`: scene narration/ranges match the exact script;
- `SCENE_VISUAL_MEANING_REVIEWED`: visual briefs and selected assets do not add
  misleading factual assertions;
- `ASSET_PROVENANCE_VISIBLE`: asset source/provenance metadata was presented;
- `ASSET_RIGHTS_STATUS_ACKNOWLEDGED`: current asset-rights results were seen;
- `DISCLOSURES_VISIBLE_IN_SCENES`: required fiction/reconstruction disclosures
  remain represented;
- `NO_UNSUPPORTED_REVIEW_CLAIM`.

### 5.3 HANDOFF

The current HANDOFF digest is editorial only. Recommended declarations must say
so explicitly:

- `EDITORIAL_SCRIPT_AND_SCENES_REVIEWED`;
- `EDITORIAL_ASSET_SET_REVIEWED`;
- `CURRENT_RECORDED_DECISIONS_VISIBLE`;
- `RIGHTS_STATUS_ACKNOWLEDGED_NOT_GRANTED`;
- `HANDOFF_IS_EDITORIAL_ONLY`: no frozen media/config manifest or production
  readiness is being asserted;
- `NO_RENDER_OR_EXPORT_AUTHORIZATION`: this decision alone does not permit
  render, export, distribution, or commercial use;
- `NO_UNSUPPORTED_REVIEW_CLAIM`.

Future production HANDOFF declarations belong to the separate frozen
media/config manifest and readiness contract, not this proposal.

## 6. APPROVE, REJECT, REVISE, and REVOKE

### APPROVE

APPROVE requires exact current integrity/consistency, an unambiguous history,
gate authority, and all required declarations in a new or idempotently resumed
review session. Its result is `EFFECTIVE_RECORDED_APPROVE`, not readiness.

### REJECT

REJECT requires authority for the gate and a nonempty reason. It remains bound
to the exact decision key. Later active-ref changes do not erase it. A later
APPROVE must be a separate record and must identify the REJECT it reconsidered
when the exact key is unchanged.

### REVISE

REVISE requires authority and a reason describing required changes. A new
package key naturally leaves the old REVISE as history. APPROVE of the same key
requires a new review session linked through `reconsiders_record_id`; otherwise
the system cannot distinguish review from retry.

### REVOKE

REVOKE requires gate/revoker authority, a nonempty reason, and an exact key. It
creates a revocation barrier. It is not removed by active-ref switching,
rollback to an old digest, later checksum recalculation, or restoring an older
APPROVE record to current visibility.

Rights or safety services may need separate emergency-block semantics later.
This proposal does not make editorial REVOKE a substitute for rights expiry or
legal takedown policy.

## 7. Re-approval after REVOKE

A new APPROVE after an effective REVOKE should require all of the following:

1. a newly generated `review_session_id`;
2. a complete new set of current gate declarations;
3. `reconsiders_record_id` equal to the latest effective REVOKE ID;
4. an authenticated and authorized principal at the time of the new review;
5. exact integrity and consistency re-evaluation immediately before writing;
6. a later transaction sequence than the REVOKE.

The timestamp is descriptive only. A later clock value does not prove that a
human reviewed anything, and system time can be changed. The future transaction
should also preserve snapshot generation/event linkage. In the stronger model,
the attestation is signed and includes the prior REVOKE ID.

Returning active refs to a previously revoked coherent chain continues to
project `RECORDED_REVOKE` until a distinct compliant re-approval record and
attestation exist. Old APPROVE is never reactivated automatically.

## 8. Idempotency

Idempotency must use a command/request identity and review session, not merely
the decision key:

- retrying the same write with the same request ID and identical payload returns
  the existing record and does not append a duplicate;
- retrying with the same request ID but different payload is a conflict;
- repeating APPROVE for the same key and same review session returns the same
  record;
- starting an explicit new review for the same key creates a new session and,
  after confirmation, a new record even when the decision is also APPROVE;
- after REVOKE, the old review session is permanently ineligible for APPROVE;
  a new session linked to that REVOKE is mandatory;
- REJECT, REVISE, and REVOKE retries follow the same request-ID rule.

`ApprovalRecord.id` alone is not sufficient as a client retry token because a
caller can generate a different UUID. The future command contract needs an
explicit `request_id` retained in authority evidence or a transaction receipt.

## 9. Threats and limitations

| Threat | Local offline MVP response | Residual limitation |
|---|---|---|
| Manually supplied actor | Do not accept actor as authority input; derive display name from authenticated principal | JSON editor/admin can still forge state without signatures and protected keys |
| Forged declarations | Closed codes, per-item confirmation, attestation digest, atomic write | Digest/checksum alone does not authenticate; compromised application can forge |
| JSON changed and checksum recalculated | Full integrity detects accidental edits; optional signed attestations verify against protected public keys | Current checksum cannot stop a capable editor; unsigned schema cannot prove origin |
| System clock changed | Treat timestamp as ordering data; use transaction generation/event link; equal times remain ambiguous | Trusted chronology needs protected monotonic counter or external timestamp authority |
| Old snapshot restored | Compare against OS-protected last-seen generation/head anchor; show rollback error | If attacker controls snapshot and anchor, local MVP cannot detect rollback |
| Conflicting decisions at same timestamp | Existing history projection returns `AMBIGUOUS_HISTORY`; authority fails closed | Human resolution needs a new later reviewed decision, never array-order tie-break |
| Invalid image/audio rights | Separate rights-policy/expiry/intended-use/action checks must block downstream operation | Authorized editor cannot manufacture a licence; legal assessment remains external |
| Stolen local session | OS lock/session controls and explicit confirmation reduce accidental use | No offline application can defeat a fully compromised logged-in account |
| Modified executable/policy | OS permissions, signed distribution/config where available | Local administrator or malware remains outside the basic trust boundary |
| Snapshot copied to another machine | Machine-bound principal/policy identifiers reveal mismatch | Portability needs an explicit trust migration procedure |

The MVP can prevent ordinary UI/CLI spoofing, fail closed on missing policy,
detect inconsistent history, and document review. It cannot prove legal rights,
resist a machine administrator, provide non-repudiation, or establish secure
time without stronger external trust.

## 10. Proposed future API

Names are proposals, not approved implementation:

```text
authenticate_local_principal() -> AuthenticatedPrincipal
load_authority_policy(policy_ref) -> AuthorityPolicy
begin_review(snapshot, gate, policy_version, principal) -> ReviewSession
record_review_declaration(session, declaration_code) -> ReviewSession
evaluate_approval_authority(snapshot, approval_id, authority_context)
    -> ApprovalAuthorityResult
evaluate_current_editorial_decision(snapshot, gate, policy_version,
                                     authority_context)
    -> EffectiveEditorialDecisionResult
record_approval_decision(snapshot, command, expected_generation)
    -> SaveResult
```

`AuthorityContext` should contain authenticated principal evidence and trusted
authority-policy material supplied by adapters, not fields copied from the
snapshot. Pure evaluation should accept no caller boolean such as
`authenticated=True`, `authorized=True`, or `human_reviewed=True`.

The write command is a later storage/service task. It must revalidate the exact
package under the writer lock, apply idempotency, append ApprovalRecord plus
authority evidence and event atomically, increment generation, and recompute
checksum. None of that is implemented here.

## 11. Testable acceptance criteria

A future implementation should demonstrate at least:

1. free-form actor cannot grant authority;
2. missing/unknown principal or policy fails closed;
3. permission is gate- and decision-specific;
4. exact integrity, consistency, and history are mandatory prerequisites;
5. every required declaration code is present exactly once;
6. unknown, duplicate, or wrong-gate declaration codes are rejected;
7. SCRIPT, SCENES, and editorial HANDOFF use distinct declaration sets;
8. APPROVE without a complete attestation is ineffective;
9. REJECT/REVISE/REVOKE are not filtered out;
10. latest effective REVOKE blocks every older APPROVE for the exact key;
11. active-ref return to a revoked key remains revoked;
12. re-approval after REVOKE requires a new review session linked to that
    REVOKE and all declarations repeated;
13. timestamp alone cannot satisfy re-review;
14. same request ID plus identical payload is idempotent;
15. same request ID plus different payload is rejected;
16. conflicting same-time history fails closed;
17. rights-policy failure cannot be overridden by reviewer authority;
18. authority success has no readiness/render/export/commercial flag;
19. snapshot, records, timestamps, actor strings, and active refs are not mutated
    during evaluation;
20. evaluation performs no network or file writes;
21. forged JSON plus recomputed checksum is not described as authenticated;
22. rollback detection behavior is explicit when the protected head anchor is
    missing or mismatched;
23. Linux and Windows principal adapters have contract tests, while platform
    compatibility claims require actual platform runs;
24. schema migration preserves historical schema-1 records as unauthenticated
    history rather than silently granting or deleting them.

## 12. Decisions requiring owner approval

Every item below is unresolved until explicitly approved. Recommended choices
are not current project rules.

| ID | Decision | Recommended option | Alternative | Consequences |
|---|---|---|---|---|
| A1 | MVP identity boundary | OS-authenticated principal using Windows SID/POSIX uid plus machine identity; actor display derived | Manual local reviewer name/PIN | Recommended blocks ordinary actor spoofing but trusts OS; manual name/PIN is simpler and offers weak identity evidence |
| A2 | Default authority | Explicit versioned allow-list; missing entry denies | Current OS user automatically owns all gates | Allow-list is fail-closed and supports gate separation; automatic ownership is simpler but makes authentication equal unrestricted authority |
| A3 | Evidence storage | New versioned `ApprovalAuthorityEvidence` companion inside authoritative snapshot | Encode conventions only in existing actor/review_declarations/reason | Companion is explicit and round-trippable but requires schema/model work; conventions are backward-looking but cannot prove sessions or authority |
| A4 | Strong tamper evidence | Make signature fields optional in basic MVP, mandatory only for stronger profile | Require local asymmetric signatures immediately | Optional signatures keep MVP smaller but cannot resist JSON+checksum forgery; mandatory signatures improve provenance but require key lifecycle, recovery, and migration |
| A5 | Declaration vocabulary | Closed gate-specific codes from §5 with localized presentation | Free-form declaration strings | Closed codes are testable/versioned; free text is flexible but cannot reliably prove which checks were acknowledged |
| A6 | Same-time identical decisions | Collapse only when decision and actor/reason/declarations match; retain all IDs and no selected record | Treat every timestamp tie as ambiguous | Recommended preserves safe idempotent duplicates; strict ambiguity is simpler and safer but creates more manual resolution |
| A7 | REVOKE permission | Same gate authority with optional separate `can_revoke` permission | Any authenticated local user may revoke | Configurable revoker supports separation; open revocation helps emergency blocking but permits denial-of-service and weak audit meaning |
| A8 | Re-approval after REVOKE | New review session, repeated declarations, and exact link to latest REVOKE | Later APPROVE timestamp alone | Recommended prevents digest rollback from reviving approval; timestamp-only cannot demonstrate human reconsideration |
| A9 | REJECT/REVISE reconsideration | Same new-session and `reconsiders_record_id` rule when approving unchanged key | Require link only after REVOKE | Uniform linkage is auditable but more ceremony; REVOKE-only linkage is simpler and leaves same-key rejection/revision transitions less explicit |
| A10 | Idempotency key | Explicit request ID plus review-session ID retained in authority evidence | Deduplicate by exact decision key or ApprovalRecord UUID | Explicit IDs distinguish retry from re-review; key/UUID deduplication either suppresses legitimate review or permits duplicate retries |
| A11 | Rollback detection | OS-protected last-seen generation/head anchor outside snapshot, with explicit unavailable state | Rely on snapshot generation/checksum only | Anchor detects ordinary rollback but complicates portability/recovery; snapshot-only cannot detect coordinated restore |
| A12 | Authority policy vs editorial policy | Store and evaluate separate authority policy ID/version | Reuse dependency `policy_version` for both | Separation avoids conflating reviewer permission with review rules; reuse is simpler but couples unrelated lifecycle and semantics |
| A13 | Schema-1 history migration | Preserve as recorded but `UNAUTHENTICATED_LEGACY`; require new review for effective approval | Grandfather old consistent APPROVE | Re-review is fail-closed; grandfathering avoids work but assigns authority evidence that was never recorded |
| A14 | HANDOFF scope | Keep authority result explicitly “editorial HANDOFF only” until manifest/readiness contracts exist | Treat effective HANDOFF approval as production-ready | Editorial-only matches E01.3.4a; readiness interpretation would contradict current package scope and bypass media/rights checks |

Implementation must wait for owner decisions on at least A1–A5, A7–A10, A12–A14.
A6 and A11 also affect deterministic behavior and security claims and should be
resolved before final acceptance criteria are frozen.
