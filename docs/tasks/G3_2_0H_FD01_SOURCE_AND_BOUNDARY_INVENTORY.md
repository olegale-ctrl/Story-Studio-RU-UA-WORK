# F-D01 — source and boundary inventory

**DOCS_ONLY. F-D01 and every H-D decision: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0h; 2026-11-17 (Europe/Kyiv). Analysis only; no adoption, implementation, merge or production authority.

**READY_FOR_INDEPENDENT_REVIEW** for this research dossier only. Exact base `7c509e8951e125704b301d18e9c474312f7fd848`, tree `b4dfe2649afede23254f32461799ef5857bd0a66`, parent `85952f8b55965da5b9bb4fc3c23144b6f35fa1f8`. Read-only main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`. Actual source blob registry and checks: [acceptance packet](G3_2_0H_ACCEPTANCE_PACKET.md).

## Authority hierarchy and mandatory labels

Hierarchy: **OWNER_APPROVED > APPROVED_LIMITED_SCOPE > PROPOSAL > FIXTURE_LOCAL_NON_NORMATIVE**. Applicability matters: an owner-approved byte rule does not approve a proposed reference record; a limited root counter rule does not adopt dependency accounting. FIXTURE_LOCAL_PROPOSAL token conventions are also proposals, never promoted by G acceptance.

| Label used for significant statements | Exact interpretation / source |
|---|---|
| APPROVED | Only inherited X01–X04, OP-01–06/26/27 and P1-DIAG-01 in their exact scope; [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X01–X04, [D P1 normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1 rule IDs, [RESOLVE narrow order](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md) P1-DIAG-01-ORDER |
| APPROVED_LIMITED_SCOPE | Only F-D02/A root occurrence-unit direction and F-D03/A external no-authority report direction; [G limited owner record](G3_2_0G_OWNER_APPROVAL_FD02_FD03.md) §1 and approved-principle boundaries |
| PROPOSED | Historical declared types, keys, reference family/edge/migration choices, F-D01 and H-D options; [A schema/reference inventory](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md), [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) OP-09/22/24 |
| OPEN_CONTRACT_DETAIL | Unselected exact identity namespace/byte-equivalence/target preimage/version/order/admission/error detail; not a default |
| OPERATIONAL_EVIDENCE_REQUIRED | Actual immutable object identity/custody/currentness/authority/rights/OS enforcement; supplied hashes are not proof; [A/B error/oracles](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md) NATIVE-01/02/03 |

[APPROVED_LIMITED_SCOPE] G3.2.0g is ACCEPTED_DOCS_ONLY_WITH_OFFLINE_VECTORS by direct H task §1. It does not approve F-D01. [PROPOSED] All new H options and future cases are research only; no schema/version/key/edge/resolver/migration rule adopted. Owner authorisation is direct task H §1, not real provider identity/grant evidence.

## Declared reference families and occurrences

[PROPOSED] The following fields are quoted **historical declarations**, not new production schemas. Source [A schema/reference inventory](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md) exact named records/X04 schema delta; [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§1–4. Id/Hash/etc are the source's type names; no runtime representation or field is added here.

| Family / source record | Exact declared field inventory | Existing occurrences | Applicability / authority boundary |
|---|---|---|---|
| PG ObjectRef | contract:Contract,id:Id,revision:Int,binding_sha256:Hash | SubjectKey.snapshot; Body02.predecessor; Body04.approvals/rights; Body05.authorization_candidate/previous_evidence | PROPOSED fields; A schema ObjectRef/SubjectKey/Body02/Body04/Body05; C P2 §1; B X03 |
| Raw ByteRef | object_id:Id,sha256:Hash,byte_length:Int,media_type:Text | Raw input/evaluation/plan/asset/evidence/tool bytes throughout Body01–05; arbitrary raw payloads | PROPOSED fields; A schema ByteRef; D P1-05/B01; C P2 §1 registry paragraph |
| Immutable toolchain binding reference | ImmutableBindingRef{schema_id:Text,object_id:Id,revision:Int,sha256:Hash,byte_length:Int}; target BoundToolchain{schema_id:"toolchain-binding/proposal-1",object_id:Id,revision:Int,payload:Toolchain} | Proposed RenderPlanV2.toolchain_ref; proposed PG04 comparison with actual Toolchain | PROPOSED fields; A X04 schema delta; B X04; C P2 §3 |
| Immutable executor-profile binding reference | ImmutableBindingRef{schema_id:Text,object_id:Id,revision:Int,sha256:Hash,byte_length:Int}; target BoundExecutorProfile{schema_id:"executor-profile-binding/proposal-1",object_id:Id,revision:Int,policy:PolicyRef,content:ByteRef} | Proposed RenderPlanV2.executor_profile_ref; PG04 executor policy/content/profile comparison | PROPOSED fields; A X04 schema delta; B X04; C P2 §3/§4 |
| PolicyRef with role-sensitive context | id:Id,version:Text,sha256:Hash | SubjectKey.policy; ActorRef.authority_policy; Body03.policy; Body04.issuer_policy/executor_profile; ExpectedOutput.profile; BoundExecutorProfile.policy | PROPOSED fields; A schema PolicyRef/ActorRef/SubjectKey/Body03/04/ExpectedOutput; C P2 §4; C policy OP-24 |
| HeadRef and trusted chronology | stream_id:Id,epoch_id:Id,sequence:Int,head_sha256:Hash | Observation.context_head; Body02/03.history_head; Body04.state_heads; Body05.state_head | PROPOSED fields; A schema HeadRef/Observation/Body02–05; C operational OP-15/23/28; P02-04 |
| SubjectKey and plan-bound references | snapshot:ObjectRef,plan_sha256:Hash,asset_manifest_sha256:Hash,use_scope_sha256:Hash,policy:PolicyRef | Body02.subject; Body03.subject; Body04.subject; approvals/rights/candidate consistency | PROPOSED fields; A schema SubjectKey; B X04; C P2 §3/§4 |

## Inherited constraints versus unresolved selection

- [APPROVED] P1-05-CANONICAL-BYTES/C10/B01 binds canonical whole PG envelope excluding only own top-level binding and binds raw ByteRef to whole raw bytes separately; Git SHA-1/G2/SI digest namespaces are not interchangeable. [D P1 normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-05; [A canonicalization](G3_2_0A_CANONICALIZATION_SPEC.md) C09/C10/B01.

- [OPEN_CONTRACT_DETAIL] A PG tuple can have multiple wire encodings with equal canonical binding; whether a registry also freezes one raw artifact is not decided by canonicalization. Do not apply raw ByteRef conflict logic blindly to PG wire variants. Historical examples V019/V020/V021 support equality layer only, not an approved registry policy. [A/B vectors](G3_2_0A_INDEPENDENT_VECTORS.md) named cases; [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §1.

- [APPROVED] X03 separates abstract stable-ID graph proof from digest-valid actual closure; no fake hashes produce a mutually hash-valid cycle. [PROPOSED] Exact registry/edge profile and OP-08/09 budgets/admission remain unapproved. [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X03; [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §2.

- [APPROVED] X04 binds mandatory toolchain/executor information through exact plan bytes; change propagates new plan/hash/SubjectKey/candidate with affected review requirements. [PROPOSED] ImmutableBindingRef/BoundToolchain/BoundExecutorProfile wire schemas, IDs, OP-22 migration and OP-24 role rules are not adopted. [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X04; [A schema/reference inventory](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md) X04 schema delta; [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§3–4.

- [OPEN_CONTRACT_DETAIL] PolicyRef.sha256, HeadRef.head_sha256 and SubjectKey asset/use/policy subfield preimages require their applicable exact target/profile definitions; field names/example hashes do not authorise guessing raw versus PG-domain encoding. X04 exact raw plan binding and P1 raw/PG definitions remain fixed. [A schema/reference inventory](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md) PolicyRef/HeadRef/SubjectKey; [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§1/3/4; [D P1 normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-05.

- [APPROVED_LIMITED_SCOPE] F-D02/A counts root value/key/member/token/decoded occurrences; no dependency-level identity dedup or physical free-work claim. F-D03/A reports no authority; private reference is not disclosure permission. [G root accounting](G3_2_0G_ROOT_ACCOUNTING_CONTRACT.md) G-AC-01/04/05; [G report direction](G3_2_0G_NON_AUTHORITY_REPORT_CONTRACT.md) G-RP-01/02/L01.

- [OPEN_CONTRACT_DETAIL] Future F-D04/F-D05 must decide aggregate accounting/graph units and caps after identity interpretation; F-D01 alone cannot set them. Exact traversal/expansion schema and F-D06 versioning remain separate. [F owner dossier](G3_2_0F_OWNER_DECISION_DOSSIER.md) F-D01/04/05/06.

- [OPERATIONAL_EVIDENCE_REQUIRED] Real resolver lookup, immutable held bytes, protected namespace identity, latest/authenticated head, rights, reviewer competence, revocation and cache/OS effects require actual qualification. A digest match is byte correspondence, not authority. [C operational governance](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md) OP-15/17/20/21/23/28; [A/B error/oracles](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md) NATIVE-01/02/03.

## Resource, product and trust consequences

[PROPOSED] Candidate logical identity reuse may avoid duplicate validation, while edges, physical reads, parsing/allocation/retries remain separate costs. Namespace/type/role distinctions preserve provenance and stop equal-content reuse from substituting a different Story Studio review, RU/UK plan, asset use or policy. Exact semantics analysed in [identity/dedup](G3_2_0H_IDENTITY_CONFLICT_AND_DEDUP_ANALYSIS.md); all status changes and concrete caps remain OPEN.

[OPERATIONAL_EVIDENCE_REQUIRED] Editorial/scientific appropriateness and lawful material licences do not follow from identical bytes or plan identity. Storage S3 is not production-qualified; Windows10/11 CPU-only/NTFS/reparse qualification NOT_RUN. Existing Preview/D1 synthetic evidence remains scoped; no production permits or provider integration.

[APPROVED_LIMITED_SCOPE] 27 G-N/12 G-R examples and earlier87 V/58 oracle/28 E IDs remain historical evidence, not new tests in H. [PROPOSED] This stage creates only30 H-C **future case plans**, not vectors/executable inputs. All7 PARTIAL and20 OPEN unchanged. **STOP.**
