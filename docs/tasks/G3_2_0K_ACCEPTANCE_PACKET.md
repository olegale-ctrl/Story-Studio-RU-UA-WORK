# G3.2.0k acceptance packet

**DOCS_ONLY — proposals for independent review**

- Base commit `698cbb0e2d8e5a66dc832cd964172244f08b4b19`
- Base tree `db8314c40b2f91af7e5b975701a1ea5b3ec4f804`
- Base parent `7f0a8b04500ca6dc8166c1738633d27653a05f66`
- Read-only main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`
- Branch `docs/g3-2-0k-opaque-namespace-comparison-context-binding`

## Exact allowlist

| Path | Mode | Git blob SHA-1 |
|---|---|---|
| docs/tasks/G3_2_0K_ADVERSARIAL_CASES_AND_EVIDENCE_PLAN.md | 100644 | 81ddf87d97f117c06d0eb59e991350653e1fa06b |
| docs/tasks/G3_2_0K_ENCODING_NORMALIZATION_ADMISSIBILITY_MATRIX.md | 100644 | ac18f4647874a82e1773497cc7c3c11536d618c4 |
| docs/tasks/G3_2_0K_EXACT_CONTEXT_BINDING_THREAT_ANALYSIS.md | 100644 | 2bd20b43debc7f2c99a2a0636a6ae9a81ddda5f6 |
| docs/tasks/G3_2_0K_OPAQUE_NAMESPACE_COMPARISON_OPTIONS.md | 100644 | ccb9b9fca9a755db85c65b63e080e7efb2f6c6be |
| docs/tasks/G3_2_0K_OWNER_APPROVAL_LIMITED_SCOPE.md | 100644 | 9c1a81283c8a2f8903d0d42aed1a4c4230134ae9 |
| docs/tasks/G3_2_0K_OWNER_DECISION_DOSSIER.md | 100644 | b905055ca041e67959a4292b2de4c3a45abbd5e2 |
| docs/tasks/G3_2_0K_ACCEPTANCE_PACKET.md | 100644 | SELF_HASH_EXTERNAL_HANDOFF |

ACCEPTANCE-SHA-01 places the seventh hash and final commit/tree/parent in the external handoff.

## Actual verification

Git fetch, remote lookup, identity checks and clean checkout exited 0. Main matched and target ref and paths were absent. All 63 historical source pins matched. Diff check first exited 2 for whitespace, then exited 0 after correction. Recursive Git tree comparison matched every old path, mode, type and object ID. Inherited graph, proposal status, case and local topological-order checks passed. Final commit and published ref checks belong to the external handoff.

## Owner authorization

G3.2.0j is ACCEPTED_DOCS_ONLY. J-R1, J-A1 and ACCEPTANCE-SHA-01 are APPROVED_LIMITED_SCOPE. See the linked [owner record](G3_2_0K_OWNER_APPROVAL_LIMITED_SCOPE.md). Equality, binding, actual authority, H-D02 and full F-D01 remain NOT APPROVED.

## Cases, all NOT_RUN

K-V001, K-V002, K-V003, K-V004, K-V005, K-V006, K-V007, K-V008, K-V009, K-V010, K-V011, K-V012, K-V013, K-V014, K-V015, K-V016, K-V017, K-V018, K-V019, K-V020, K-V021, K-V022, K-V023, K-V024, K-V025, K-V026, K-V027, K-V028, K-V029, K-V030, K-V031, K-V032, K-V033, K-V034, K-V035, K-V036

## K decision register and local dependency graph

| Decision | Question | Prerequisites | Status |
|---|---|---|---|
| K-D01 | Comparison domain | none | PROPOSED — NOT APPROVED |
| K-D02 | Decoding and BOM | K-D01 | PROPOSED — NOT APPROVED |
| K-D03 | Normalization and case | K-D01 | PROPOSED — NOT APPROVED |
| K-D04 | Admissibility | K-D02, K-D03 | PROPOSED — NOT APPROVED |
| K-D05 | Profile principle | K-D01 | PROPOSED — NOT APPROVED |
| K-D06 | Request association | none | PROPOSED — NOT APPROVED |
| K-D07 | Occurrence association | K-D06 | PROPOSED — NOT APPROVED |
| K-D08 | Family and role isolation | K-D07 | PROPOSED — NOT APPROVED |
| K-D09 | Authority and currentness | K-D06 | PROPOSED — NOT APPROVED |
| K-D10 | Missing or ambiguous context | K-D07, K-D08, K-D09 | PROPOSED — NOT APPROVED |

The listed topological order is acyclic.

## Unchanged H-D and I-Q graphs

| Decision | Prerequisites |
|---|---|
| H-D01 | none |
| H-D02 | H-D01 |
| H-D03 | H-D02 |
| H-D04 | H-D02 |
| H-D05 | H-D02 |
| H-D06 | H-D02 |
| H-D07 | H-D03, H-D04, H-D06 |
| H-D08 | H-D03, H-D04, H-D05, H-D06 |
| H-D09 | H-D06, H-D07 |
| H-D10 | H-D02 |
| I-Q01 | none |
| I-Q02 | I-Q01 |
| I-Q03 | I-Q02 |
| I-Q04 | I-Q01 |
| I-Q05 | I-Q01 |
| I-Q06 | I-Q01, I-Q02 |
| I-Q07 | I-Q05, I-Q06 |
| I-Q08 | I-Q05, I-Q06 |
| I-Q09 | I-Q06 |
| I-Q10 | I-Q02, I-Q04, I-Q06 |

## Unchanged register

| OP | Status |
|---|---|
| OP-07 | OPEN — NOT APPROVED |
| OP-08 | OPEN — NOT APPROVED |
| OP-09 | OPEN — NOT APPROVED |
| OP-10 | OPEN — NOT APPROVED |
| OP-11 | OPEN — NOT APPROVED |
| OP-12 | OPEN — NOT APPROVED |
| OP-13 | OPEN — NOT APPROVED |
| OP-14 | OPEN — NOT APPROVED |
| OP-15 | OPEN — NOT APPROVED |
| OP-16 | OPEN — NOT APPROVED |
| OP-17 | OPEN — NOT APPROVED |
| OP-18 | OPEN — NOT APPROVED |
| OP-19 | OPEN — NOT APPROVED |
| OP-20 | OPEN — NOT APPROVED |
| OP-21 | OPEN — NOT APPROVED |
| OP-22 | OPEN — NOT APPROVED |
| OP-23 | OPEN — NOT APPROVED |
| OP-24 | OPEN — NOT APPROVED |
| OP-25 | OPEN — NOT APPROVED |
| OP-28 | OPEN — NOT APPROVED |

| CM | Status |
|---|---|
| CM-006 | PARTIAL |
| CM-022 | PARTIAL |
| CM-070 | PARTIAL |
| CM-071 | PARTIAL |
| CM-072 | PARTIAL |
| CM-073 | PARTIAL |
| CM-095 | PARTIAL |

## Source blob registry

Every source row is pinned at the exact K base above.

| Path | SHA-1 |
|---|---|
| docs/tasks/G3_2_0A_ACCEPTANCE_PACKET.md | ecbdb6f708cd46d59a0793c797ef066ecf5eb7fd |
| docs/tasks/G3_2_0A_CANONICALIZATION_SPEC.md | c81bc868e856070cd3fe93644f1179332ad3ce96 |
| docs/tasks/G3_2_0A_CONTRACT_FREEZE_PROPOSAL.md | eab93c30493d2502da8ce5e551bed23e58210283 |
| docs/tasks/G3_2_0A_ERROR_AND_ORACLE_MATRIX.md | 64d1e82989f052a63e0684450f72f94a54137ae5 |
| docs/tasks/G3_2_0A_INDEPENDENT_VECTORS.md | 1035c8a50dbb3c943ba17a9eb8c9fd8781f3e427 |
| docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md | 8df767ab375ff312c6ac723072e58d64e53969c9 |
| docs/tasks/G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md | b9978d3712748a987bf9574450a3fd10ffa319b6 |
| docs/tasks/G3_2_0B_ACCEPTANCE_PACKET.md | 388e6438fdb59159d8cac790f33841cba8668c2b |
| docs/tasks/G3_2_0B_OWNER_DECISIONS_X01_X04.md | 41564c598830c605d82041746bdd6fd74e21eb59 |
| docs/tasks/G3_2_0B_RESOLUTION_AND_VECTOR_EVIDENCE.md | 89ee64a3176ab2f9aca41626e8a8b930f2f9cecb |
| docs/tasks/G3_2_0C_ACCEPTANCE_PACKET.md | 8c04f2ca43370a7cf59140f1639556184daf678a |
| docs/tasks/G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md | 700a9bce47b6c79a45cb65fce1b8a09d84903dab |
| docs/tasks/G3_2_0C_P1_CANONICAL_FOUNDATION.md | 8905865ed0f41b363d39993408a78605d3a829df |
| docs/tasks/G3_2_0C_P2_REFERENCE_AND_SCHEMA.md | 9d39e41a9dc729f83ff91ee6a29b84668a327a42 |
| docs/tasks/G3_2_0C_P3_RESOURCE_MODEL.md | 8787738852f4b9a15ad3d33f1c57ec52a5dc3441 |
| docs/tasks/G3_2_0C_P4_POLICY_CONTRACTS.md | a875fa0ee36748f41a0b89cd6c2f9b80ece89bcd |
| docs/tasks/G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md | d9b94e875442d57d7e71cc0d84a4936eceb1bff0 |
| docs/tasks/G3_2_0D_ACCEPTANCE_PACKET.md | f661ed3fbee2e752cd48050bc9a2073d91ab4106 |
| docs/tasks/G3_2_0D_OWNER_APPROVAL_P1.md | 006fb429e6499ad33a25d3892b6bc7cb5f60d5ab |
| docs/tasks/G3_2_0D_P1_CONFORMANCE_MATRIX.md | 6af66c8f6471fb29c5815472e4b87ac02ba337a5 |
| docs/tasks/G3_2_0D_P1_NORMATIVE_CONTRACT.md | e082c93e25ceb9fbed415becb3b47fe867ff0d1d |
| docs/tasks/G3_2_0D_REMAINING_PARAMETERS_AND_BOUNDARIES.md | 6a0f46b7e007b51efc706b057b893db850d42abb |
| docs/tasks/G3_2_0E_ACCEPTANCE_PACKET.md | ee5df0cca19224014aace0663db9ff93698f9cd6 |
| docs/tasks/G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md | a6651f0f2b0c0d3947a3b14797abbb8be8fdc3de |
| docs/tasks/G3_2_0E_P1_BOUNDARY_AND_PRECEDENCE_VECTORS.md | c15cc8d8e5f2e67bbf0e153a082f5c37b3bfdcce |
| docs/tasks/G3_2_0E_RESOLVE_1_ACCEPTANCE_PACKET.md | aae2521f859e9aced897afb059faad04ac5b07fd |
| docs/tasks/G3_2_0E_RESOLVE_1_CM069_CONFORMANCE_EVIDENCE.md | 8cb1d5b2efd28fa59919ef08e6510254cc0e9ef3 |
| docs/tasks/G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md | ad062fb02968f1d6e2b45758fb463c50743b6a92 |
| docs/tasks/G3_2_0E_RESOLVE_1_OWNER_APPROVAL_P1_DIAG_01.md | 733ea983fa7d278166fb2e64c054d5520f5282ef |
| docs/tasks/G3_2_0E_SAFE_ERROR_MESSAGE_VECTORS.md | d71f92fbc25d62820c3027f42c7d33a76b3651d0 |
| docs/tasks/G3_2_0E_VECTOR_FIXTURE_SPEC.md | 75507d98beab2da2cecb65d5b2126e62ea36cccd |
| docs/tasks/G3_2_0F_ACCEPTANCE_PACKET.md | a641ff1d4488b85ae8d9089daac12e89a108face |
| docs/tasks/G3_2_0F_CONFORMANCE_AND_EVIDENCE_PLAN.md | 85937b0d2a2b0000f81528e2bc3ad4c677af9175 |
| docs/tasks/G3_2_0F_OPERATIONAL_AND_RESOURCE_DEPENDENCIES.md | dfedf15283ed121d07c5c576367aea13f5965b29 |
| docs/tasks/G3_2_0F_OWNER_DECISION_DOSSIER.md | a71e03f527ec907257966e9b6b9110d20724ce42 |
| docs/tasks/G3_2_0F_PURE_CONTRACT_DECISION_OPTIONS.md | e371a41b6ebb45f3fff990c24e67b574e804e72e |
| docs/tasks/G3_2_0F_SEVEN_PARTIAL_GAPS_INVENTORY.md | 25480c979480657ddffa81df4e072d01883f3dd3 |
| docs/tasks/G3_2_0G_ACCEPTANCE_PACKET.md | 1b1087abc0b571ea85ec317048da7e5979c85416 |
| docs/tasks/G3_2_0G_NON_AUTHORITY_REPORT_CONTRACT.md | 7d42784da8944ac7d32c8a6872bde57573b28248 |
| docs/tasks/G3_2_0G_OWNER_APPROVAL_FD02_FD03.md | 1b239686307f6215fc4f176c58bb2cacf9488feb |
| docs/tasks/G3_2_0G_REPORT_OFFLINE_VECTORS.md | eaa78d21b22dc5241bfe39e68d1489e06b8126c2 |
| docs/tasks/G3_2_0G_ROOT_ACCOUNTING_CONTRACT.md | 567104deb84e78b63861b629ed24e0b71811eca6 |
| docs/tasks/G3_2_0G_ROOT_ACCOUNTING_OFFLINE_VECTORS.md | 802f63c7e836ca1c7099bdebd049919240c527f9 |
| docs/tasks/G3_2_0H_ACCEPTANCE_PACKET.md | f81fa9ebd32941ec376cc59aefe2dfee1160d6a4 |
| docs/tasks/G3_2_0H_ADVERSARIAL_CASES_AND_FUTURE_VECTORS.md | 74e8725de055f4c02fce93dcf76677b97d045d0c |
| docs/tasks/G3_2_0H_FD01_SOURCE_AND_BOUNDARY_INVENTORY.md | b0bed16636c88a785034fede8bfa6e14678196e5 |
| docs/tasks/G3_2_0H_IDENTITY_CONFLICT_AND_DEDUP_ANALYSIS.md | d4a0468db9bdfe43a0493d90a83de2bc47609b7b |
| docs/tasks/G3_2_0H_OWNER_DECISION_DOSSIER.md | 4af8d303e2e62b4aa005f271a07d75595a54ceff |
| docs/tasks/G3_2_0H_REFERENCE_EDGE_AND_CLOSURE_BOUNDARIES.md | f7e9d7314572bb8e15ce4b490d4e90b90cef3b21 |
| docs/tasks/G3_2_0H_TYPED_REFERENCE_FAMILY_OPTIONS.md | d9eb77efece635e4a01ee0e0452b53c334a89185 |
| docs/tasks/G3_2_0I_ACCEPTANCE_PACKET.md | c848cb7d14611930df2d9e7a635f106a64569212 |
| docs/tasks/G3_2_0I_ADVERSARIAL_CASES_AND_EVIDENCE_PLAN.md | 20015715a0fb20dae69588465eb83f599d201b09 |
| docs/tasks/G3_2_0I_HD02_OWNER_DECISION_DOSSIER.md | 7e4576360fe82b0ddb546b397143130f887f42b7 |
| docs/tasks/G3_2_0I_IDENTITY_METADATA_OBSERVATION_MATRIX.md | 128e192cab5af462f67c372964db4befdd149d2f |
| docs/tasks/G3_2_0I_NAMESPACE_AUTHORITY_AND_CONFLICT_ANALYSIS.md | 69b34beefdb809bcbee8682314edc4ff4a543622 |
| docs/tasks/G3_2_0I_OWNER_APPROVAL_HD01_A.md | 42bda2370825739e84e3a537b4974826e9b05445 |
| docs/tasks/G3_2_0I_REGISTRY_KEY_AND_NAMESPACE_OPTIONS.md | da4ee411d3dd2ade568eadd944f0af78849c98e8 |
| docs/tasks/G3_2_0J_ACCEPTANCE_PACKET.md | e1fc8e05b790b268275f12e154cf92b470b46525 |
| docs/tasks/G3_2_0J_ADVERSARIAL_CASES_AND_EVIDENCE_PLAN.md | 20c4030b4cf3cc7a50b8e4bb258aac7e9bdba876 |
| docs/tasks/G3_2_0J_CONTEXT_BINDING_AND_COMPARISON_BOUNDARIES.md | a7e861a0fee66135ed087de431b9ecf889d2d5e4 |
| docs/tasks/G3_2_0J_IQ02_IQ03_OWNER_DECISION_DOSSIER.md | d2c2479471755cf369d832b039e6983f4b8a2ef4 |
| docs/tasks/G3_2_0J_NAMESPACE_ASSERTION_AUTHORITY_MATRIX.md | 3a094eb155f5737773168bc382bf04fb8fa61755 |
| docs/tasks/G3_2_0J_NAMESPACE_REPRESENTATION_OPTIONS.md | ec391e5caf9085e41bdd0a3342b8edd06bb8748e |
| docs/tasks/G3_2_0J_OWNER_APPROVAL_LIMITED_SCOPE.md | 52caffeb32ff09a3147ac297c10ad10a5a0eb283 |

## NOT_RUN and remaining decisions

All K-V cases, executable conformance, cryptography, runtime, provider/OS qualification, replay, TOCTOU, resource, admission, migration and production tests are NOT_RUN. Equality domain, representation, admissibility, exact association, authority, currentness and missing-context handling remain open.

RECOMMENDATION — NOT APPROVED. After independent review, answer K-D01 separately from K-D06. Defer a concrete domain pending paired representation evidence. Consider a documentary study of supplied request association.

## G3.2.0k-FIX-1 Root Cause and Impact Assessment

| Field | Assessment |
|---|---|
| Observed defect | Line 41 rendered `System.String[]`. Lines 49, 55 and 59 rendered `System.Object[]`, each as a standalone line where table rows belonged. |
| Reproduction | The recorded PowerShell command put the K rows, inherited graph rows and filtered OP/CM rows into a comma-built outer array, then joined the outer array with newlines. With synthetic string and object arrays the same construction reproduced both exact type names. Concatenating line collections before joining emitted individual rows. |
| Root cause | GENERATION_DEFECT. The comma-built array preserved those four row collections as nested elements. The final shallow join stringified each nested collection. The source registry was appended as individual rows through array concatenation and did not share this defect. No transformation of the underlying member values was required to reproduce it. |
| Source-data integrity | Verified. Ten K decisions and their statuses recover from the committed K dossier. Both ten-node inherited graphs match the original H and I dossiers, with I's external H-D01/A prerequisite note preserved in its original source. The pinned J packet supplies 20 OPEN OP and seven PARTIAL CM in their original order. The complete source registry matches Git object identities and order. |
| Contract impact | None proven. Four rendered tables were unavailable for review. No source contradiction, changed approval, prerequisite or normative conclusion was found. |
| Validation gap | VALIDATION_GAP. The original checks examined source headings, decision counts, graph inputs and Git metadata. They did not parse the emitted packet or compare its table rows with source. The handoff counts and graph results described those inputs and did not establish that the packet rendered them. |
| Useful findings | USEFUL_IMPROVEMENT. Compare parsed output with source rows as well as checking graph and Git integrity. A shared generator or validator would require separate owner authorization. |
| Recurrence risk | A repository-wide search for the two exact literals in Markdown at the original published tip found only these four locations. That targeted check does not establish general historical table correctness. Any generator that joins nested values could repeat the failure. |
| Corrective action | Restored ten K-D, twenty H-D/I-Q, twenty OP and seven CM rows, including original ordering and explicit status where applicable. Kept the complete source registry and six sibling blob pins. |
| Preventive recommendation | For a separately approved future workflow, emit one row per string and validate the rendered packet's table structure, exact row counts, source correspondence and graph references before publication. |


**STOP. Await independent audit and separate owner approval. No merge, G3.2.1 or production permissions.**
