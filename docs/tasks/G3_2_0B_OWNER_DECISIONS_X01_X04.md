# G3.2.0b — owner decisions X01–X04 and normative scope

**DOCS_ONLY / resolution package — independent acceptance pending.** SI-INTEGRATION-G3.2.0b; 2026-11-17 (Europe/Kyiv).
X01–X04: **OWNER_APPROVED** по текущему заданию. Новые schemas/profiles и OP-01–28 остаются **PROPOSAL / NOT APPROVED**; это не final PG freeze.
Parent `2610dcfd0a304c4fb8f4d71812b80e52f6ce3bb5`, tree `425972e157e017eb20615a4ea0fa6ba216a7923d`.
Approved main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

## Source of authority and exact scope

Owner instruction in the current task explicitly approves X01–X04. This is architectural/docs-only authorization, not a signature, real identity proof, production grant, schema freeze, implementation permission, numeric-policy approval or merge instruction.

- Approved main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
- Discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c` (reference only, unchanged).
- Documentation parent G3.2.0a `2610dcfd0a304c4fb8f4d71812b80e52f6ce3bb5`, tree `425972e157e017eb20615a4ea0fa6ba216a7923d`.
- Branch `docs/g3-2-0b-contract-contradictions-resolution` created exactly from G3.2.0a; no rebase/cherry-pick/merge.

All seven A source file Git blobs checked before creation; clean checkout, remote main exact, target remote branch absent. Four modified + three added only; other A docs, including all28 parameters, remain immutable. Three unchanged A docs describe their historical blocked phase; this B document is the explicit adjudication, not a claim they were never blocked.

## Decision matrix — OWNER_APPROVED architectural choices

| ID | Historical conflict | Effective owner-approved rule | What remains unapproved |
|---|---|---|---|
| X01 | Empty Text was both schema and product-gap condition | Required Text nonempty scalar sequence; empty why_film → PG_FORMAT(stage2). Nonempty but substantively insufficient → PG_PRODUCT_GAP(stage6) after prior stages. No coercion/default/length-only human judgment | Product policy, reviewer competence and actual finding; no PG semantic PASS |
| X02 | Mode/schema/hash ordering ambiguous | Exactly seven stages below; unknown mode PG_FORMAT; known+wrong binding PG_DIGEST; known+valid binding+forbidden contract pair PG_MODE after references | Other policies/resource numbers/provider protocols remain OP; no new error/result enum |
| X03 | Hash-valid cycle fixture was replaced by unverifiable/fake hashes | Separate abstract stable-ID typed graph oracle from real content-addressed PG closure. Actual ObjectRef still needs valid exact local and target bindings; early hash/ref rejection not isolated cycle proof | OP-08 numbers and full end-to-end crypto closure fixture coverage; V043 remains historically blocked |
| X04 | SubjectKey allegedly included tools/profile but plan lacked mandatory fields | Proposed new RenderPlan version must bind toolchain_ref/executor_profile_ref immutably; any binding change changes plan bytes/hash and SubjectKey. PG04 checks actual payload/profile equality; no caller overrides | Concrete new types/schema IDs/version/migration/reapproval policy, role assignment and operational qualification |

## X01 normative requirements

Text is nonempty Unicode scalar sequence, not nonempty-after-trim. No normalization/trim/null/omission/default substitution. Empty required why_film is structural error before digest/product stage. Nonempty rationale can be insufficient: a competent policy-driven review/finding is needed, not a pure length heuristic or fabricated scientific conclusion. Original P01-07 wording/expected error remain verbatim in oracle matrix; explicit owner-approved override applies only to empty branch. V051 input bytes remain unchanged; its previous BLOCKED expectation is historical, new effective PG_FORMAT. V072 supplies a proposed isolated nonempty insufficient rationale probe, **not full PG PASS**.

## X02 normative order and isolated fixture requirements

1. Bounded input and UTF-8 decode.
2. JSON grammar, duplicate keys, closed schema, field types, known enum lexical values.
3. Local envelope canonical binding SHA-256.
4. Reference registry, closure and dependency validation.
5. Contract-specific mode and subject consistency.
6. Product, rights and trusted-state predicates.
7. Execution/evidence checks where applicable.

Use first applicable denial; do not compute/return accepted canonical output when earlier stage fails. Unknown mode enum fails stage2 even with stale binding. Known enum does not mean permitted contract pair: if local binding wrong, stage3 PG_DIGEST; if correct and refs otherwise valid, forbidden pair fails stage5 PG_MODE. Wrong reference PG_REFERENCE when no earlier rejection; product gap only after successful stages1–5. Current byte fixtures E/C0 have mandatory field shape and exact raw reference metadata for these early-stage expectations, but no claim full SI/product/provider validity. Semantic PG validation itself NOT_RUN.

V039 source input retains known PRODUCTION_CANDIDATE with original PREVIEW_ONLY binding → PG_DIGEST. V071 uses exactly same body/known mode with correctly recomputed binding → expected PG_MODE. V073 unknown enum → PG_FORMAT. No new PG error code, no new machine verdict or operational grant.

## X03 approved model split

Abstract fixtures use stable local IDs, revision labels, typed declared edges, no asserted ObjectRef digest. DFS and Kahn actually check directed-cycle outcomes. Seven fixtures cover DAG, self-loop,2-cycle,3-cycle,shared-child,predecessor target-revision mismatch and conditional traversal exhaustion. Structural results are evidence annotations, not PG Error.code. V043-S5 does not impose new chronological ordering on cross-event PG02 revision numbers: it fails exact target_revision lookup only. V043-S6 budget2 is a fixture parameter under still-open OP-08, not production bound.

Real PG closure still requires exact target envelope/hash/revision, no fake/stale binding, no latest fallback. A synthetic cycle diagram does not demonstrate a reachable mutually hash-valid PG cycle. V043 remains historical BLOCKED end-to-end fixture. Therefore architectural choice X03 is resolved, while native/provider/full closure qualification is not earned.

## X04 immutable binding and review separation

The proposed new version is fully described in [schema delta](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md), with before/after V079/V080 and negatives V074–078. New RenderPlan has mandatory toolchain_ref and executor_profile_ref; each includes schema_id/object_id/revision/raw SHA256/byte_length, resolves to exact immutable typed target. Toolchain target binds full Toolchain payload; executor target binds versioned PolicyRef plus exact profile-content ByteRef. Real binaries/profile/paths never come from caller override or arbitrary version labels. Target version/header/bytes/hash/length must match, no reserialization substitute or latest fallback.

`SubjectKey.plan_sha256 → exact RenderPlanV2 raw bytes → immutable target identities/bytes`. A changed target is a new revision, changed ref, new plan raw digest and a different SubjectKey. PG04 must compare actual toolchain payload/executor profile to the resolved bound targets. It is insufficient to place an unbound toolchain outside plan in PG04. Hashes prove byte correspondence, not OS/runtime authority.

Content-affecting change requires new human approval. Rights-affecting change requires new rights review and any affected human review. Purely technical change requires a new authorization candidate and evaluation under **separately approved reapproval policy**: no automatic old-SubjectKey equivalence, no inferred grant, no implicit continuity approval carrier. OP-22 remains OPEN; classifying uncertain effect as technical is not allowed by default.

RenderPlanV2 schema ID and proposed PG04 consumer version are new **PROPOSAL**. Legacy proposal-1 envelopes/approvals are not automatically valid under this profile, no migration or production compatibility assumed. Actual migration/version acceptance policy remains explicit future decision. No implementation, current render script or G1/G2/G3.1 changed.

## Unchanged open parameters and prohibitions

All OP-01–OP-28 retain original OPEN/PROPOSED entries and exact original file blob. Approving X01/X02 clarifies the named subdecisions, not every OP-06 issue. Approving X04 binding direction does not freeze OP-22 type/policy details or approve technical regrant. OP-08 budget2 test does not pick real closure limits. No roles/TTL/parser budget/license/host/provider/evidence durability/retention values promoted to APPROVED.

Full PG freeze, semantic validators/providers, trusted authority, Windows/native/S3, real identity/rights, application integration/render, MP4/private evidence publication, main/CI edits, merge/release and G3.2.1 remain prohibited. This package awaits independent acceptance. **STOP.**
