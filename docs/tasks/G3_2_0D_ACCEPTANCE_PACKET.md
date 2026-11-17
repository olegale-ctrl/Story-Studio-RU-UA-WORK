# G3.2.0d — Acceptance packet

**P1_OWNER_DECISIONS_DOCUMENTED — DOCS_ONLY**

**READY_FOR_INDEPENDENT_REVIEW**, documentation and permitted offline arithmetic only. Not PRODUCTION_APPROVED, not full PG freeze; no implementation permission.

## Pinned identities and preflight

| Identity | Commit | Tree / parent |
|---|---|---|
| Read-only approved main | `a28277b4cb68a3db5da52edc598c37ce66314604` | tree `920713b992046dff1f8fc68e40a05bee2f0bcb29` |
| Exact accepted C base | `86ae74058c2a90b563855eac15f46ff8b3be28e4` | tree `f0f3aaf1c95a1d6400a9e65d12beff04d0159895` |
| Base parent | `0d6d9076ab535c1b258206beb4e4fe9c005e79e1` | parent identity verified |

Branch `docs/g3-2-0d-p1-owner-decisions-conformance` created directly from exact C. Fetch completed before editing; exact main/base/tree/parent, clean starting checkout, all seven C blobs, ten A/B reference documents,87 unique vector IDs,58 unique oracle IDs, actual21 error codes and target local/remote branch absence checked. Preflight exit0. No automatic recovery/rebase/merge/cherry-pick.

Owner authority for this documentary record is the direct task SI-INTEGRATION-G3.2.0d §1/§6, received as the uploaded `Вставленный текст.txt`, SHA-256 `9bad2967bf1b89027b2efd4c9726fd5794cdc621e83c5071ad4595c135c7a9a1`. This hash identifies the task text, not authenticated human/provider authority. No real approval receipt, grant, policy identity or permission was created.

## Exact five-file registry

Paths under `docs/tasks/`; exactly five new additions, all100644, existing files unchanged. Candidate commit/tree and packet self-blob are supplied in the external handoff after commit; they are not self-referential fields in this file.

| Diff | File | Mode | Git blob SHA-1 |
|---|---|---|---|
| A | [G3_2_0D_OWNER_APPROVAL_P1.md](G3_2_0D_OWNER_APPROVAL_P1.md) | 100644 | `006fb429e6499ad33a25d3892b6bc7cb5f60d5ab` |
| A | [G3_2_0D_P1_CONFORMANCE_MATRIX.md](G3_2_0D_P1_CONFORMANCE_MATRIX.md) | 100644 | `6af66c8f6471fb29c5815472e4b87ac02ba337a5` |
| A | [G3_2_0D_P1_NORMATIVE_CONTRACT.md](G3_2_0D_P1_NORMATIVE_CONTRACT.md) | 100644 | `e082c93e25ceb9fbed415becb3b47fe867ff0d1d` |
| A | [G3_2_0D_REMAINING_PARAMETERS_AND_BOUNDARIES.md](G3_2_0D_REMAINING_PARAMETERS_AND_BOUNDARIES.md) | 100644 | `6a0f46b7e007b51efc706b057b893db850d42abb` |
| A | G3_2_0D_ACCEPTANCE_PACKET.md | 100644 | Self-blob supplied externally after commit |

## Owner choices and rule inventory

Eight OWNER_APPROVED **pure-contract only**: OP-01, OP-02, OP-03, OP-04, OP-05, OP-06, OP-26, OP-27. Their exact approval record and exclusions are in the first linked document; normative contract carries these8 stable rule IDs:

- P1-01-WIRE-LIMIT — full root wire8388608 inclusive, before decode, separate ByteRef/canonical accounting.
- P1-02-DEPTH —64 containers; scalar0/root1/nested+1.
- P1-03-STRING-BYTES —65536 decoded UTF-8 bytes per key/value, scalar validation, no normalization.
- P1-04-ARRAY-CARDINALITY —10000 per array; stricter fields and independent global budgets.
- P1-05-CANONICAL-BYTES — exact PG-C14N-1, signed64/-0/Unicode/escaping/order/own-binding/domain/raw separation.
- P1-06-ERROR-PRECEDENCE — X01/X02 earliest stage, adopted residual fixed category priority, bounded safe deterministic diagnostics; unresolved provider causality/chronology OPEN_OPERATIONAL_DETAIL.
- P1-26-STATUS-BOUNDARY — descriptive STRUCTURALLY_VALID, no new enum/grant.
- P1-27-SAFE-ERRORS — exact21 code/message pairs, protected private diagnostics, no export approval.

Remaining20 **OPEN — NOT APPROVED**, each explicitly listed and original class/package preserved in remaining-boundaries document: OP-07, OP-08, OP-09, OP-10, OP-11, OP-12, OP-13, OP-14, OP-15, OP-16, OP-17, OP-18, OP-19, OP-20, OP-21, OP-22, OP-23, OP-24, OP-25, OP-28. Previously decision-ready OP-09/22 are not approved. Total classification remains PURE12/MIXED7/OPERATIONAL9; P1–P5 primary ownership8/2/2/7/9. P1 approval has no dependency on connecting production providers.

## Conformance statistics and actual verification

**95 documentation rows**: **60 COVERED_BY_VECTOR /7 PARTIAL /28 MISSING**. These measure existence/scope of documentary fixtures, not executed test outcomes. All eight approved OP mapped.28 missing rows comprise7 streaming/depth/key/own-binding/multi-error fixture specifications plus21 safe-message/private-leakage fixture specifications. Additional partial gaps cover resource aggregation, trusted cause classification, X03/X04, result status/authority and privacy qualification. No new vectors or expected digests invented.

Reference universe87 vectors/58 oracles; exact cited IDs resolve. Cited vector IDs:

V001, V002, V003, V004, V005, V006, V007, V008, V009, V010, V011, V012, V013, V014, V015, V016, V017, V019, V020, V021, V022, V023, V024, V025, V026, V027, V028, V029, V030, V031, V032, V033, V035, V036, V037, V039, V040, V043, V043-S, V043-S1, V043-S2, V043-S3, V043-S4, V043-S5, V043-S6, V044, V045, V046, V047, V048, V049, V051, V052, V053, V054, V055, V056, V057, V058, V059, V064, V065, V066, V067, V068, V071, V072, V073, V074, V075, V076, V077, V078, V079, V080.

Cited oracle IDs:

COMMON-02, COMMON-03, COMMON-04, COMMON-05, COMMON-06, NATIVE-03, P01-01, P01-05, P01-07, P02-04, P04-01.

Actual independent recalculation: **20 vector records,40 SHA-256 comparisons**, CPython3.12.14 hashlib, exit0, all expected=actual. Representative IDs:

V001, V003, V005, V006, V007, V009, V011, V012, V013, V017, V019, V022, V046, V047, V052, V054, V056, V058, V066, V067.

Conformance matrix includes the exact recipe/length/RAW/DOMAIN actual digests and algorithm. Input is published literal canonical bytes/recipes; no JSON/PG serializer or validator. Domain prefix includes final00. Own-binding exclusion reconstructed via published E/C_ENV recipe, with nested REF binding retained. Raw ByteRef V066 is distinct from envelope domain. Recalculation is new digest work in this task, not merely reading historical hashes; backend or reviewer independence is not asserted. No mismatch detected; otherwise STOP BLOCKED_VECTOR_VERIFICATION, no adjusting source bytes.

| Offline activity | Result / exit code | Limit |
|---|---|---|
| Git preflight and pinned source blob checks | Completed /0 | Main/base identities and17 A/B/C docs |
| Literal-byte SHA-256 recalculation |40 comparisons matched /0 | Not canonicalizer/semantic validation |
| Rule/OP/row uniqueness and class/package coverage | Completed /0 |8 rules,8 approved,20 open,95 rows |
| Exact vector/oracle IDs and21 code/message pairs | Completed /0 | References and fixed text, not behavioral execution |
| Boundary arithmetic and Markdown consistency/links | Completed /0 | Byte/depth/list recipes, no benchmarks |
| Final five-file modes/diff/unchanged-tree entries, whitespace and remote identities | Verified at publication, external handoff | Candidate commit/tree/self-blob supplied externally |

Temporary helpers/results live outside repository; no source modules imported. Final staged/committed `git diff --check` and tree equality outside five added paths are publication gates. Working-tree cleanliness and remote branch/main are checked after push.

## Source ambiguities, risks and remaining blockers

No accepted P1 hash disagreement found in the representative set; no new contradiction requiring edits to existing files was identified by document inspection. Historical V039/V051 blocked wording is resolved by B X02/X01; V071/V073 preserve paired known/unknown-mode behavior. X03 abstract graph model and crypto closure remain separate (historical V043 end-to-end fixture blocked). X04 exact plan/toolchain/executor direction is preserved without implementation or migration permission.

The C P1 residual table did not specify all provider-specific distinctions, same-group operational ties or execution chronology. These are recorded OPEN_OPERATIONAL_DETAIL, not guessed; no trusted negative can be inferred from an unavailable dependency. Unknown internal exception never becomes success; no invented universal error or provider protocol.

OP-07/08 global resource/closure budgets, full schemas/references/migration, trusted identities/roles/clock/history, rights, scientific/editorial suitability, revocation/admission/replay/lost ACK/crash recovery, guarded execution/TOCTOU, evidence durability and privacy/publication remain open. Storage S3 is not production-qualified. Windows10/11 NTFS/reparse/CPU-only native qualification was not performed. Fixed safe messages do not authorize public export. Pure consistency cannot supply authority, rights, editorial suitability or production approval.

**NOT_RUN:** application tests, PG validators, serializer, integration, render, trusted provider operations, native Windows tests, performance/production qualification. No CI/workflow or existing file changed. No G3.2.1 and no full PG contract freeze.

## STOP conditions and next decision

- Wrong pinned identity/reference or pre-existing target branch: BLOCKED_BASE_MISMATCH; no substitution/recovery.
- Required existing-file correction or out-of-allowlist change: BLOCKED_SCOPE.
- Conflicting literal hash: BLOCKED_VECTOR_VERIFICATION with expected/actual, no content adjustment.
- Unresolved pure contradiction preventing a rule: BLOCKED_CONTRACT; failed offline consistency check: BLOCKED_VERIFICATION.
- Current documented missing vectors and operational/resource dependencies remain explicit gaps; readiness here means independent **documentation** review only.

Recommended next owner action: independent ChatGPT audit of the eight normative rules, adopted residual ordering,95-row evidence classification and hash ledger; then a separate decision about missing conformance fixtures and still-open parameters. No implementation stage follows automatically.

**STOP — await independent ChatGPT audit and separate owner decision.** No merge, release, migration, grants, render, provider access, production qualification/permissions or G3.2.1.

## Pinned source blob registry

All below read at exact C base, retained unchanged; this allows independent source inspection without substituting current branch content.

| Source path under docs/tasks | Git blob SHA-1 |
|---|---|
| G3_2_0C_ACCEPTANCE_PACKET.md | `8c04f2ca43370a7cf59140f1639556184daf678a` |
| G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md | `700a9bce47b6c79a45cb65fce1b8a09d84903dab` |
| G3_2_0C_P1_CANONICAL_FOUNDATION.md | `8905865ed0f41b363d39993408a78605d3a829df` |
| G3_2_0C_P2_REFERENCE_AND_SCHEMA.md | `9d39e41a9dc729f83ff91ee6a29b84668a327a42` |
| G3_2_0C_P3_RESOURCE_MODEL.md | `8787738852f4b9a15ad3d33f1c57ec52a5dc3441` |
| G3_2_0C_P4_POLICY_CONTRACTS.md | `a875fa0ee36748f41a0b89cd6c2f9b80ece89bcd` |
| G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md | `d9b94e875442d57d7e71cc0d84a4936eceb1bff0` |
| G3_2_0A_ACCEPTANCE_PACKET.md | `ecbdb6f708cd46d59a0793c797ef066ecf5eb7fd` |
| G3_2_0A_CANONICALIZATION_SPEC.md | `c81bc868e856070cd3fe93644f1179332ad3ce96` |
| G3_2_0A_CONTRACT_FREEZE_PROPOSAL.md | `eab93c30493d2502da8ce5e551bed23e58210283` |
| G3_2_0A_ERROR_AND_ORACLE_MATRIX.md | `64d1e82989f052a63e0684450f72f94a54137ae5` |
| G3_2_0A_INDEPENDENT_VECTORS.md | `1035c8a50dbb3c943ba17a9eb8c9fd8781f3e427` |
| G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md | `8df767ab375ff312c6ac723072e58d64e53969c9` |
| G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md | `b9978d3712748a987bf9574450a3fd10ffa319b6` |
| G3_2_0B_ACCEPTANCE_PACKET.md | `388e6438fdb59159d8cac790f33841cba8668c2b` |
| G3_2_0B_OWNER_DECISIONS_X01_X04.md | `41564c598830c605d82041746bdd6fd74e21eb59` |
| G3_2_0B_RESOLUTION_AND_VECTOR_EVIDENCE.md | `89ee64a3176ab2f9aca41626e8a8b930f2f9cecb` |
