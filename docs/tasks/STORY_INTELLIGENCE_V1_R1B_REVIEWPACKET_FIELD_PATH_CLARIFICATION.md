# Story Intelligence V1 — R1b ReviewPacket field namespace and projection mapping

**Date:** 2026-11-09. **Status: PROPOSAL / AWAITING OWNER APPROVAL — CONTRACT-ONLY.**
**Blocker:** SI-E01.2a-G01, `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md` at `18163478f2204c3dd3d3f9bd742c49ea8253506e`.
**Base:** `18163478f2204c3dd3d3f9bd742c49ea8253506e` (blocked feature; exactly two docs, 190 added lines).
**Binding predecessor:** composite original+R1+R1a, approved SI-D01–SI-D10; this **proposed R1b** overrides only R1 §5.2/§5.3 field-path wire spelling and projection STATE mapping after explicit owner approval. Until then **STOP** on SI-E01.2a full record validation.

## 1. Decision scope and exclusions

R1 already defines a recorded, immutable `ReviewPacket`, its typed `FieldGrant`, `FieldView`, `Omission`, `DisplayItem`, `review_state_at_capture:BriefReviewState`, closed semantic text/state whitelists, and privacy grants. This amendment proposes **only exact path syntax/mapping**, not new data/permissions/records, a new privacy profile, automatic export, evidence approval, or any persistence/security guarantee.

### R1b-P01 — exact grammar

Every `FieldGrant.field_path`, `FieldView.field_path` and `Omission.field_path` denotes a **source record PAYLOAD-relative path**, never H, `payload.`, a type prefix, JSONPath or a display label.

Canonical grammar:

```text
field_path := segment ("." segment)*                 ; only explicitly enumerated paths below
segment    := identifier | identifier "[" index "]"
identifier := [a-z][a-z0-9_]*                         ; literal approved payload key
index      := "0" | [1-9][0-9]*                        ; zero-based decimal, no leading zeros
```

No leading `$`, slash, whitespace, `payload`, type prefix, backticks, aliases, negative/plus signs, wildcard, slice, range, empty brackets, escaped identifier, or syntactic normalization. Dots only for approved nested fields; index only immediately after its array member. `field_path` must match one of the exact closed **record-type-and-kind** combinations below; generic grammar validity alone is insufficient. A large index is syntactically well formed but invalid if not inside the exact source snapshot array; no fabricated array element. At local schema-validation time, path syntax/approved combination is checked; exact source field existence/value/record SHA and grant binding need the later resolver/packet export checks.

`source_ref` is always an **existing SIRef from `source_closure_refs`** at full packet validation, never a virtual ref and never the Packet/export Run itself.

### R1b-P02 — TEXT whitelist mapping (all require matching FieldGrant)

| source_ref.type | Exact field_path(s) |
| --- | --- |
| StoryIdea | `title`, `summary`, `viewer_question` |
| SourceItem | `title.value` only if `title.state=KNOWN` |
| ClaimItem | `statement` |
| ClaimCheck | `qualification` only if non-null |
| Angle | `question`, `thesis`, `distinction` |
| CreativeAlternative | `hook_text`, `title_options[i]`, `thumbnail_notes`, `chapters[i].heading`, `chapters[i].purpose`, `retention_0_30` |
| VisualRequirement | `description`, `fallback.value` only if KNOWN |
| Risk | `description`, `mitigation` |
| ProductionBrief | `promise`, `must_avoid[i]`, `required_reviews[i]` |

Here `[i]` is a placeholder in this **documentation table only**, not a literal wire token; canonical actual field paths substitute `[0]`, `[1]`, etc. No automatic normalization from alternate spellings. The semantic whitelist and qualification/PII rules from R1 remain mandatory.

### R1b-P03 — STATE whitelist mapping

STATE uses `FieldView(kind=STATE)` and no `FieldGrant` (unless separately required by an independent TEXT field); `text` is the exact closed scalar value in source payload, with lowercase `true` / `false` for booleans.

| source_ref.type | Exact STATE field_path(s) |
| --- | --- |
| ClaimCheck | `state` |
| Risk | `category`, `severity`, `blocking`, `resolution` |
| VisualRequirement | `role`, `rights_state` |
| ProductionBrief | `locale`, `content_mode`, `workflow_state` |
| EvaluationReport | `eligibility.state` |

All values come from the **exact source record**. `Eligibility` has no own ref; the source is its enclosing `EvaluationReport` SIRef and field path `eligibility.state`. `source_ref` for a STATE is the source record shown in the containing `DisplayItem`; it cannot be the Packet ref or a generated ref.

The **projection-only** `BriefReviewState.review_state` / `BriefReviewState.currentness` are **never FieldView or DisplayItem fields**. They are represented exclusively in existing `ReviewPacket.payload.review_state_at_capture.review_state` and `.currentness` (and the remainder of that full typed projection). They have no `source_ref`, `FieldGrant`, `FieldView.field_path` or `Omission` of their own because `BriefReviewState` has no H/SIRef. This clarifies rendering without deleting any STATE information from Packet: it remains in the already required `review_state_at_capture`, scoped to capture snapshot. Existing frozen status must not be presented as current after changes.

### R1b-P04 — REDACTED and Omission rules

A `FieldView(kind=REDACTED)` has `text=null`, its source_ref inherited from containing `DisplayItem`, and exactly one corresponding `Omission` with **the same** `source_ref` and `field_path` (reason PRIVATE_FIELD or NOT_SELECTED). Explicit Omission may also cover a field not present in any `FieldView` (closed policy fields not selected) without fabricating a placeholder view.

For REDACTED/Omission, the field path must still be a syntactically valid canonical **payload-relative path with an actual source payload field**, selected from the relevant record's declared field vocabulary, including sensitive fields that cannot be shown as TEXT/STATE (e.g. SourceItem.`original_locator`, ClaimCheck.`reviewer_label`, Selection.`selector_label`). A path to H (including `creator_label`, `previous`, `origin.imported_from`), nonexisting field, unrelated record type, or virtual projection is forbidden. **Header content is withheld by omitting it entirely from views**, not by generating H-field Omission. Do not expose secrets/labels through Omission values, reason or inferred data.

For nested objects/arrays, the exact path is to the existing scalar leaf value, or to the existing field whose value is a Known union if the entire Known item is withheld; choose the actual declared payload key, not a made-up alias. REDACTED must never be a means to promote a secret to TEXT or permission to export raw payload bytes. Implementers should reject unknown nested keys and noncanonical indices. The complete mapping of all declared payload leaf paths for REDACTED/Omission derives mechanically from the **approved, closed payload schema**; it is not an open extension namespace. Local schema checking can validate declared path/type; whether it exists in a particular source revision remains the resolver's responsibility.

### R1b-P05 — matching, ordering, cross-field restrictions

- For a given `DisplayItem.source_ref`, `FieldView.field_path` values are unique; each `Omission(source_ref,field_path)` pair unique. Multiple `DisplayItem` entries for the same source_ref are rejected.
- At packet assembly, all displayed TEXT fields must have exactly matching `FieldGrant(source_ref,field_path,value_sha256)`. No grant for STATE/REDACTED/projection-only path; no grants for prohibited private fields; unknown grant/presentation paths fail closed. `value_sha256 = SHA256(C(exact source scalar/string field value))`, not hash of the full source record or displayed spelling alone.
- Text `FieldView.text` is exactly the approved source text (no paraphrase/transformation), with required qualifiers present as separately granted source values. STATE text must agree with the permitted source value and closed enum/bool. `REDACTED` requires null text.
- `FieldView` order within a `DisplayItem` and `Omission` order is the order of declared root payload fields (including nested schema order) and ascending numeric indices, not Unicode lexical string order. A path's order is established by its sequence of declared schema field positions followed by array indices. `DisplayItem` order follows `source_closure_refs` manifest order. No reordering of source records or user semantic arrays.
- For `FieldGrant`, require unique `(source_ref,field_path)` and order by `source_closure_refs` manifest, then declared path order/ascending numeric indices, matching the source snapshot canonical selection. An unselected or private field cannot be forced into TEXT by a grant.
- Any ambiguity in a `REDACTED` path whose field is a nested object/list versus scalar requires a negative validation case. The `REDACTED` kind must not permit a blanket root `payload` or `H` path.
- FieldView `kind=TEXT` requires non-null `text`, `kind=STATE` requires non-null `text` and closed scalar, `kind=REDACTED` requires null. Structural local validation does not pretend to know whether the source exists; resolver checks that later.
- Missing exact matching grant, invalid source, mismatched source text/value hash, nonexistent index, or exposure of protected private data fails closed under existing R1 diagnostics (e.g. `PRIVACY_BLOCKED`, `PRIVACY_REVIEW_REQUIRED`, `REDACTED_CONTEXT_INCOMPLETE`, `REF_MISSING`, `REF_HASH_MISMATCH`, `TYPE`); no new code vocabulary.

## 2. Illustrative future golden / negative cases (not executable yet)

Each snippet is a **path string / source-ref mapping expectation**, not a full typed-record vector.

| Case | Input / context | Expected |
| --- | --- | --- |
| P-T01 | `StoryIdea` TEXT `title` | Allowed; `payload.title`, `H.title`, `$.title` rejected |
| P-T02 | `CreativeAlternative` first title `title_options[0]` | Allowed if index 0 exists; `title_options[1]` addresses second; `title_options[00]`, `title_options[*]`, `title_options[-1]` rejected |
| P-T03 | `CreativeAlternative` chapter2 purpose `chapters[1].purpose` | Allowed if index1 exists; `chapters[1].heading` distinct |
| P-T04 | `SourceItem` title KNOWN TEXT `title.value` | Allowed when KNOWN, matches value digest and grant; UNKNOWN cannot be TEXT |
| P-T05 | `EvaluationReport` STATE `eligibility.state` | source_ref.type=EvaluationReport, no grant; `EvaluationEligibility.state` rejected |
| P-T06 | `Risk` STATE `blocking` | Displays lowercase ASCII `true`/`false`, no matching text grant |
| P-T07 | Projection review_state/currentness | In `review_state_at_capture` only, not FieldView; no imaginary BriefReviewState SIRef |
| P-T08 | `ClaimCheck` REDACTED/Omission `reviewer_label` | Allowed withheld payload field; never TEXT/STATE even if field grant is present |
| P-T09 | `SourceItem` REDACTED/Omission `original_locator` | Allowed as withheld payload field; no text grant or locator leakage |
| P-T10 | Any H field `creator_label` or `origin.imported_from` | Cannot occur in FieldGrant, FieldView or Omission; header never in projection paths |
| P-T11 | Same source/path in FieldView twice, duplicate omission/grant | Rejected; no duplicate privacy permissions/view items |
| P-T12 | Literal `ReviewPacket.payload.review_state_at_capture.review_state` vs changed observed context | Frozen source review state remains historical; currentness recalculated externally, never silent upgrade |

R1b requires at least these cases plus literal canonical bytes and `SHA256(C(FieldGrant))` for `title`, `title_options[0]`, `eligibility.state` (where applicable as STATE FieldView), and rejected alternate strings after owner approval; do not fabricate expected hashes in this document.

## 3. Decision requested and resumption gate

**Proposed owner choices:** approve **R1b-P01–P05 as one bounded clarification**, or return specific changes. Approval adds deterministic ReviewPacket path spelling and separates source-record STATE from projection-only state; **no existing approved decisions SI-D01–SI-D10 change**, no new record types, storage authority, permissions or network export.

After owner approval, write an explicit acceptance note and issue **a new, bounded SI-E01.2a-RESUME Codex task on the exact approved erratum SHA**. Existing blocked branch remains historical evidence; do not rewrite the blocked result. The implementation must honor all 18 record types and retain the original STOP limits. Do not automatically start code from this proposal.

**STOP.** No source/tests/merge/main changes in this documentation clarification.
