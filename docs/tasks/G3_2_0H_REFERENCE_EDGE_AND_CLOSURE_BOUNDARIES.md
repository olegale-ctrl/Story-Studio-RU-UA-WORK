# Reference edges and closure — unadopted boundaries

**DOCS_ONLY. F-D01 and every H-D decision: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0h; 2026-11-17 (Europe/Kyiv). Analysis only; no adoption, implementation, merge or production authority.

## Closed edges versus inferred links

[PROPOSED] Option A would require a selected exact schema/version to declare which fields are typed dependency edges, their family/target interpretation and whether optional/nullable slots contribute an edge. An opaque ByteRef's payload content, URL-like string, media_type or reference-looking JSON does not itself select an expansion profile. Explicit typed expansion is a **separate** H-D06/OP-09/22 decision; no profile is approved now. Sources: [A schema/reference inventory](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md) ObjectRef/ByteRef and X04 delta; [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§1–2/4.

[OPEN_CONTRACT_DETAIL] Complete supported edge vocabulary/field order/profile universe is not supplied by historical DEPENDENCY/PREDECESSOR graph-fixture tags. They are structural fixture metadata, not automatically new PG wire edge kinds. In particular policy/head/receipt blobs cannot become trusted edges merely by decoding their bytes.

## Target matching, missing/conflicting/unknown data

[APPROVED] X03 real PG closure still requires exact local/target binding/revision matching; a diagram with placeholder/stale hashes is not isolated crypto-cycle coverage. [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X03; [B resolution evidence](G3_2_0B_RESOLUTION_AND_VECTOR_EVIDENCE.md) X03 fixtures.


[PROPOSED] A selected family would compare requested target key/version/header/integrity constraints and actually observed bytes, not whichever object has a matching display ID or convenient hash. Missing target, conflicting records and unsupported version remain explicit cases; no latest/default fallback or heuristic adapter. Hash-matching but wrong type/header cannot be declared exact requested identity by assumption. Detailed admission/error mappings are OPEN_CONTRACT_DETAIL unless already a fixed P1/X02 rule.

## Repeated edges, shared children and traversal order

[PROPOSED] Candidate counters distinguish distinct typed nodes U from edge occurrences E and physical bytes/read/retry work. Shared child may be one identity but multiple declared edges. Repeated edge occurrences cannot be assumed free merely because integrity can be reused. Numerical U/E/path-depth/aggregate-byte bounds and reset/cache policies are not selected. [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §2; [C resource model](G3_2_0C_P3_RESOURCE_MODEL.md) §§1–5; [G root accounting](G3_2_0G_ROOT_ACCOUNTING_CONTRACT.md) G-AC-05.

[OPEN_CONTRACT_DETAIL] Exact graph traversal order needs a selected edge/record/schema ordering policy. Earlier C suggests declared fields and original array order; this is still proposed for graph traversal. P1-DIAG-01 only fixes same-code/same-stage private diagnostics of its historical pg-01 root fields; it cannot be expanded to nested/new records, edge traversal, cache scheduling or policy/head chronology. Existing OP-06 array diagnostic index order is preserved, not a complete graph-order algorithm. [RESOLVE narrow order](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md) scope predicate/P1-DIAG-01-ORDER.

## Root versus dependency discovery and fixed error stages

[APPROVED] X02 and P1-06 fix earliest stage:1 root bounded decode,2 root grammar/schema/types/known enums,3 own local envelope binding,4 reference registry/closure/dependencies,5 mode/subject,6 product/rights/trusted-state,7 execution/evidence. A malformed target discovered in stage4 is not retrospectively a root-stage2 finding; target byte/hash checks take place at its discovery layer. Same-stage established-category priorities remain fixed by D P1-06, but new family cause selection/detail does not follow merely from choosing an ID tuple. [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X02; [D P1 normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-06-ERROR-PRECEDENCE.

[OPEN_CONTRACT_DETAIL] No H case assigns a new exact public error code where family/schema/edge admission is unresolved. Actual unavailable provider cannot be represented as authenticated absent/revoked; unknown internal exception is never success. Logical resource guards and their numeric selected profiles still need F-D04/F-D05/OP-07/08/09. Root F-D02/A units are not closure accounting approval.

## X03 — graph evidence is not crypto constructibility

[APPROVED] V043 remains a historical blocked end-to-end crypto cycle fixture. V043-S/V043-S1/V043-S2/V043-S3/V043-S4/V043-S5/V043-S6 are the separate abstract DAG/cycle/shared-child/revision/budget layer; cap2 is fixture metadata, not OP-08 bound. No mutually hash-valid cyclic closure is fabricated or claimed constructible here. Earlier hash rejection is not an isolated cycle test. Sources [A/B vectors](G3_2_0A_INDEPENDENT_VECTORS.md) named cases; [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X03.

[PROPOSED] Future evidence could independently cover real **acyclic** exact byte/target correspondence and abstract negative-cycle structures in separate suites after decisions, without claiming both suites prove a real cyclic content-addressed graph. Full closure admission still requires selected identity/edge/schema/resource rules and explicit task authorisation.

## X04 — mandatory exact plan direction, not schema adoption

[APPROVED] SubjectKey.plan_sha256→exact raw plan bytes→mandatory toolchain/executor immutable bindings; render-affecting target change changes plan/hash/subject/candidate. No caller tool/path/config override and no old-subject equivalence. Content/rights changes require affected review, technical continuity separately approved. [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X04.

[PROPOSED] Concrete RenderPlanV2/ImmutableBindingRef/BoundToolchain/BoundExecutorProfile IDs/types/compatibility and policy-role mapping remain OP-22/24/F-D06/F-D07 questions; H neither accepts them nor creates adapters. Historical V074–080 are source byte/predicate evidence, not newly executed or operational qualification.

## What F-D01 could enable later

| Later work | Status / dependency boundary |
|---|---|
| Precise key/metadata/byte family comparisons | PROPOSED H-D01/02/03/04; no approval now |
| Role/header/preimage-specific comparisons | OPEN_CONTRACT_DETAIL H-D05; OP-22/24/23 still needed |
| Explicit edge profile/order and closure specification | PROPOSED H-D06; full OP-09/F-D05 still separate |
| Aggregate work/dedup/caching accounting units | PROPOSED H-D07; F-D04/05/OP-07/08 decisions and runtime evidence still needed |
| Schema migration/adapters/reapproval | PROPOSED H-D08; separate F-D06/F-D07 decisions, no inherited authority |
| New offline literal/vector scope | PROPOSED H-D09 only future planning; no fixtures or hash computation in H |
| Immutable object access/currentness/runtime authority | OPERATIONAL_EVIDENCE_REQUIRED H-D10 and separate authorised qualification |

[OPEN_CONTRACT_DETAIL] F-D01 cannot itself approve full closure, graph limits/traversal, a resolver/cache, policy registry, migration, real rights or production permission. [APPROVED_LIMITED_SCOPE] G reporting cannot prove zero runtime effects from no grant fields. **STOP.**
