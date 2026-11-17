# H-D02 — separately answerable registry identity/namespace proposals

**DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. H-D02: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0i; 2026-11-17 (Europe/Kyiv). H-D01/A APPROVED_LIMITED_SCOPE for documentary direction only. F-D01 NOT APPROVED.

## Decision status and limited approval scope

[APPROVED_LIMITED_SCOPE] Direct I owner decision approves H-D01/A only as closed exact typed-family documentary direction separating stable key, integrity metadata and observed bytes. [PROPOSED] H-D02 remains unapproved; I-Q IDs below identify its **subquestions**, not new H-D nodes, new OP numbers or approvals. Existing full F-D01/OP-09 admission unapproved. Source [H owner dossier](G3_2_0H_OWNER_DECISION_DOSSIER.md) H-D01–H-D10; [I owner approval](G3_2_0I_OWNER_APPROVAL_HD01_A.md).

[PROPOSED] I-A/I-B/I-C key/namespace alternatives are compared in [options](G3_2_0I_REGISTRY_KEY_AND_NAMESPACE_OPTIONS.md). **RECOMMENDATION — NOT APPROVED:** I-A for a narrow documentary candidate because explicit context/family/stable slots expose alias/metadata ambiguity without assuming global uniqueness. I-B needs independently specified global identity/authority/collision semantics; I-C retains concrete keys unresolved. No I-A tuple or wire schema adopted.

## Exact subquestion register

| Subquestion | Statement | A — explicit contextual candidate | B — alternative requiring separate semantics | C — defer | Recommendation | Local hard prerequisites | Consequences / external gates | Required future evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| I-Q01 | Stable key composition | Candidate explicit namespace context + family discriminator + stable declared identity slots, with a declared revision/version slot only where present | Globally scoped identity only after uniqueness/authority/collision/type binding defined | Defer concrete key composition | Prefer A as documentary comparison candidate only | H-D01/A limited direction only | H-D02 key principle; concrete family admission still OPEN; no new wire field | Future same-key/cross-family/namespace prose and separate owner selection | PROPOSED — NOT APPROVED |
| I-Q02 | Namespace representation and comparison | Explicit comparison context bound to exact request/reference location; representation/equality specified separately | Globally qualified ID encapsulates namespace only under independently fixed semantics | Defer representation/comparison | Prefer explicit contextual comparison analysis; no default normalisation | I-Q01 | No accepted text encoding, URI/UUID interpretation, casefolding or new namespace wire field | Future detached/context-swapped/Unicode/case namespace case plans | PROPOSED — NOT APPROVED |
| I-Q03 | Namespace authority boundary | Treat supplied namespace as an assertion; require separately qualified provenance for authoritative claims | Globally scoped issuer model only after actual authority/uniqueness evidence | Keep authority claims blocked and compare supplied data only | Prefer separate assertion versus authority labels, no issuer/trust root chosen | I-Q02 | Pure equality does not authenticate registry/storage/OS identity or currentness | Later actual authorised namespace/registry/custody/OS evidence; no provider now | PROPOSED — NOT APPROVED |
| I-Q04 | Version and revision treatment | Use only exact explicitly declared revision/version slots; unversioned raw family does not gain a synthetic revision | Separately proposed future globally scoped/versioned identity model with migration contract | Defer family-specific version semantics | Prefer declared-only analysis; do not infer latest or chronological meaning | I-Q01 | Concrete supported versions and raw immutable-change rules remain H-D03/04/05 and OP-09/22 gates | Future exact/missing/wrong/unsupported version plans after schema decision | PROPOSED — NOT APPROVED |
| I-Q05 | Stable key versus integrity metadata | Keep expected digest/length as associated constraints and observed bytes/header separate from candidate key | Explicit future content-addressed family only after type/preimage/collision/version semantics selected | Defer concrete registry while preserving approved separation principle | Prefer stable-key/metadata/bytes triad; hash change is not a silent new version | I-Q01 | Does not select immutable raw conflict rule H-D04 or PG raw-artifact rule H-D03 | Future same-key changed digest/length/header observations; no hash calculation | PROPOSED — NOT APPROVED |
| I-Q06 | Cross-family identity isolation | Explicit comparison discriminator even where reference shapes/bytes match | Globally scoped ID binds family only under explicit accepted semantics | Defer family universe/admission | Prefer separate typed comparison context, not a new accepted family set | I-Q01, I-Q02 | Toolchain and executor profile remain different roles; no automatic schema/type interchange | Future same-ID/same-byte/wrong-family plans; actual target identity separately qualified | PROPOSED — NOT APPROVED |
| I-Q07 | Same-key inconsistent observations | Preserve contradictory metadata/header/observed-byte claims for review; do not silently pick first/last or re-key by changed hash | Future explicit globally scoped/versioned conflict protocol after family policies selected | Keep registry disposition and exact error EXPECTED_RESULT_OPEN | Prefer conflict visibility only; final disposition waits H-D03/04/05 | I-Q05, I-Q06 | PG canonical wire equivalence and raw immutable-byte policy not collapsed; no admission/error code chosen | Future pure comparison cases; operational reconciliation requires authenticated evidence | PROPOSED — NOT APPROVED |
| I-Q08 | Equal-content aliases | Keep semantic identities/roles/subjects distinct despite equal observed bytes | Separately reviewed explicit alias mapping with provenance and no review/rights transfer | Defer alias/dedup admission | Prefer no implicit semantic merging; no cache policy selected | I-Q05, I-Q06 | Logical validation reuse remains H-D07; physical reads/allocations/retries not free | Future same-digest/different-ID/namespace/role plans; runtime resource evidence later | PROPOSED — NOT APPROVED |
| I-Q09 | Policy-role context | Document role-sensitive comparison as external context while concrete PolicyRef target/role admission stays OPEN | Separate future role-tagged/versioned contract after H-D05/OP-24 decision | Exclude policy admission until role/preimage decisions | Prefer context-bound questions only; do not adopt H-D05 | I-Q06 | Same bytes in rights/issuer/reviewer/output roles do not establish authority/rights or shared review | Future cross-role/namespace plans; actual grants/competence/current policy require trust evidence | PROPOSED — NOT APPROVED |
| I-Q10 | Unsupported or missing identity information | Do not silently complete missing namespace/type/version/target; record unresolved supplied facts | Only a separately reviewed explicit adapter/version bridge could interpret them later | Defer all admission and public error mapping | Prefer no inferred latest/default identity; retain EXPECTED_RESULT_OPEN for unselected families | I-Q02, I-Q04, I-Q06 | No new PG code or supported-family/version set; resolver unavailability is not authenticated absence | Future missing/wrong header/version/target plans; actual provider evidence separate | PROPOSED — NOT APPROVED |

## Explicit owner questions — approve/reject/defer one scope at a time

### I-Q01 — Stable key composition

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Candidate explicit namespace context + family discriminator + stable declared identity slots, with a declared revision/version slot only where present), B (Globally scoped identity only after uniqueness/authority/collision/type binding defined) либо C (Defer concrete key composition)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: H-D02 key principle; concrete family admission still OPEN; no new wire field. Evidence: Future same-key/cross-family/namespace prose and separate owner selection.

### I-Q02 — Namespace representation and comparison

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Explicit comparison context bound to exact request/reference location; representation/equality specified separately), B (Globally qualified ID encapsulates namespace only under independently fixed semantics) либо C (Defer representation/comparison)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: No accepted text encoding, URI/UUID interpretation, casefolding or new namespace wire field. Evidence: Future detached/context-swapped/Unicode/case namespace case plans.

### I-Q03 — Namespace authority boundary

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Treat supplied namespace as an assertion; require separately qualified provenance for authoritative claims), B (Globally scoped issuer model only after actual authority/uniqueness evidence) либо C (Keep authority claims blocked and compare supplied data only)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: Pure equality does not authenticate registry/storage/OS identity or currentness. Evidence: Later actual authorised namespace/registry/custody/OS evidence; no provider now.

### I-Q04 — Version and revision treatment

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Use only exact explicitly declared revision/version slots; unversioned raw family does not gain a synthetic revision), B (Separately proposed future globally scoped/versioned identity model with migration contract) либо C (Defer family-specific version semantics)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: Concrete supported versions and raw immutable-change rules remain H-D03/04/05 and OP-09/22 gates. Evidence: Future exact/missing/wrong/unsupported version plans after schema decision.

### I-Q05 — Stable key versus integrity metadata

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Keep expected digest/length as associated constraints and observed bytes/header separate from candidate key), B (Explicit future content-addressed family only after type/preimage/collision/version semantics selected) либо C (Defer concrete registry while preserving approved separation principle)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: Does not select immutable raw conflict rule H-D04 or PG raw-artifact rule H-D03. Evidence: Future same-key changed digest/length/header observations; no hash calculation.

### I-Q06 — Cross-family identity isolation

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Explicit comparison discriminator even where reference shapes/bytes match), B (Globally scoped ID binds family only under explicit accepted semantics) либо C (Defer family universe/admission)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: Toolchain and executor profile remain different roles; no automatic schema/type interchange. Evidence: Future same-ID/same-byte/wrong-family plans; actual target identity separately qualified.

### I-Q07 — Same-key inconsistent observations

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Preserve contradictory metadata/header/observed-byte claims for review; do not silently pick first/last or re-key by changed hash), B (Future explicit globally scoped/versioned conflict protocol after family policies selected) либо C (Keep registry disposition and exact error EXPECTED_RESULT_OPEN)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: PG canonical wire equivalence and raw immutable-byte policy not collapsed; no admission/error code chosen. Evidence: Future pure comparison cases; operational reconciliation requires authenticated evidence.

### I-Q08 — Equal-content aliases

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Keep semantic identities/roles/subjects distinct despite equal observed bytes), B (Separately reviewed explicit alias mapping with provenance and no review/rights transfer) либо C (Defer alias/dedup admission)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: Logical validation reuse remains H-D07; physical reads/allocations/retries not free. Evidence: Future same-digest/different-ID/namespace/role plans; runtime resource evidence later.

### I-Q09 — Policy-role context

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Document role-sensitive comparison as external context while concrete PolicyRef target/role admission stays OPEN), B (Separate future role-tagged/versioned contract after H-D05/OP-24 decision) либо C (Exclude policy admission until role/preimage decisions)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: Same bytes in rights/issuer/reviewer/output roles do not establish authority/rights or shared review. Evidence: Future cross-role/namespace plans; actual grants/competence/current policy require trust evidence.

### I-Q10 — Unsupported or missing identity information

**PROPOSED — NOT APPROVED.** Для H-D02 выбрать A (Do not silently complete missing namespace/type/version/target; record unresolved supplied facts), B (Only a separately reviewed explicit adapter/version bridge could interpret them later) либо C (Defer all admission and public error mapping)? Если ответ A/B, зафиксировать только выбранный documentary scope и явно назвать остающиеся OPEN детали; не считать его принятием конкретного wire tuple/schema/family/admission/implementation. Последствия: No new PG code or supported-family/version set; resolver unavailability is not authenticated absence. Evidence: Future missing/wrong header/version/target plans; actual provider evidence separate.

## Boundary against implicit H-D03/04/05 adoption

[OPEN_CONTRACT_DETAIL] I-Q01/02 describe candidate key/context coordinates, not final PG canonical/raw equivalence. I-Q05 keeps metadata visible but does not decide whether raw artifact variance conflicts; that is H-D03 for PG wire policy and H-D04 for raw integrity/version/media. I-Q07 must retain uncertainty in disposition until those separately decided policies exist. I-Q09 names role-sensitive comparison questions without choosing the PolicyRef schema/preimage/admission of H-D05/OP-24. No selected outcome of an I-Q would automatically approve one of those H-D decisions or a new supported family universe.

[PROPOSED] Slot/context comparison versus globally scoped IDs needs concrete external authority evidence only to claim authentic identity, not merely to compare supplied assertions. I-Q03 can specify that distinction without appointing a trust root, issuer, signer, ACL or resolver. Exact public error handling remains existing P1 rules where applicable; unresolved admission does not authorise a new code/default success. H-D06 expansion/traversal, H-D07 dedup/caching, H-D08 migration, H-D09 closure and H-D10 real qualification remain separate.

## Existing H-D graph — reproduced, not amended

The adjacency list below is copied from exact base H owner dossier. Node IDs and edges unchanged. H-D01/A's new limited documentary approval is recorded separately; it does not adopt the registry or rewrite historical H files.

- H-D01 ← none.
- H-D02 ← H-D01.
- H-D03 ← H-D02.
- H-D04 ← H-D02.
- H-D05 ← H-D02.
- H-D06 ← H-D02.
- H-D07 ← H-D03, H-D04, H-D06.
- H-D08 ← H-D03, H-D04, H-D05, H-D06.
- H-D09 ← H-D06, H-D07.
- H-D10 ← H-D02.

[PROPOSED] Local I-Q question-order graph is separate from the H-D graph:

- I-Q01 ← none; inherited H-D01/A direction only.
- I-Q02 ← I-Q01.
- I-Q03 ← I-Q02.
- I-Q04 ← I-Q01.
- I-Q05 ← I-Q01.
- I-Q06 ← I-Q01, I-Q02.
- I-Q07 ← I-Q05, I-Q06.
- I-Q08 ← I-Q05, I-Q06.
- I-Q09 ← I-Q06.
- I-Q10 ← I-Q02, I-Q04, I-Q06.

Both graphs are checked acyclic independently. No local subquestion grants implementation or requires a live provider before discussing supplied-context rules. Downstream hard H graph prerequisites remain exactly as before: H-D03/04/05/06/10 depend on H-D02; H-D07 depends03/04/06; H-D08 depends03/04/05/06; H-D09 depends06/07. OP-07/08 resources, complete OP-09 and OP-22/24 schemas/roles/qualification are external gates, not silently satisfied nodes.

## Recommended next owner decision and evidence sequence

1. [PROPOSED] Independently audit the exact owner boundary,7-family matrix and30 future cases. No registry outcomes or tests are claimed.
2. [PROPOSED] Owner explicitly selects I-A/I-B/I-C as **documentary candidate direction** and separately answers I-Q01/I-Q05 if desired; these identify key slots versus metadata without approving concrete tuples or H-D03/04/05. I-C is legitimate if namespace/identity facts insufficient.
3. [PROPOSED] Separately answer I-Q02/03/04/06 representation/authority-boundary/version/family questions. Do not infer authority from namespace equality, UUID shape or a supplied digest. Missing context is not repaired with a default.
4. [OPEN_CONTRACT_DETAIL] Before disposition/alias/role/admission decisions I-Q07/08/09/10, separately resolve implicated H-D03/04/05 and selected schema/preimage roles; later H-D06/07/08/09 choices remain explicit. No auto-expanded traversal, migrated review or cache reuse.
5. [PROPOSED] Only after exact contracts and a new owner-authorised task may finite offline vectors be prepared. Real namespace/currentness/storage/OS/rights claims require separate qualified providers/host/custody/evidence scope; no such work begins here.

[APPROVED] X03 prohibits treating abstract cycle diagrams as real hash-valid closure; X04 preserves exact plan/subject propagation and no inherited grants. [APPROVED_LIMITED_SCOPE] Root metrics do not qualify resource enforcement and reports do not prove zero effects. [OPERATIONAL_EVIDENCE_REQUIRED] Story Studio RU/UA needs actual editorial/scientific review and material rights independent of key/namespace byte correspondence; no hash equality or global-ID declaration supplies them.

All I-Q alternatives remain **PROPOSED — NOT APPROVED**. H-D02/F-D01 remain NOT APPROVED;20 OP OPEN,7 CM PARTIAL, previous limited approvals unchanged. **STOP after publication — independent ChatGPT audit and separate owner decision. No implementation, merge, G3.2.1 or production permissions.**
