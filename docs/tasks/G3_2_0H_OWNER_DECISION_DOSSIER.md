# F-D01 owner decision dossier —10 proposed questions

**DOCS_ONLY. F-D01 and every H-D decision: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0h; 2026-11-17 (Europe/Kyiv). Analysis only; no adoption, implementation, merge or production authority.

## A/B/C and precise recommendation

[PROPOSED] Full comparison in [family options](G3_2_0H_TYPED_REFERENCE_FAMILY_OPTIONS.md). A=closed exact typed candidate; B=explicit version-specific adapters; C=defer admission. **RECOMMENDATION — NOT APPROVED:** prefer A only for staged documentary analysis because explicit type/namespace/key/integrity boundaries expose conflict and alias errors with a smaller transformation surface than B. C is the safe fallback **decision alternative**, not automatic runtime fallback, if required byte/namespace choices cannot yet be made. B remains a separate high-cost migration/provenance/reapproval design requiring explicit need and review.

[OPEN_CONTRACT_DETAIL] No A/B/C selection occurs in H. A historical preference is not adoption. Especially unresolved: PG canonical-equivalent wire artifacts versus raw-immutable identity; PolicyRef/HeadRef/use-scope target recipes; namespace authority/binding; family/role discrimination; header/admission/version/edge order. Their concrete alternatives follow; no new schema or wire fields are supplied.

## Proposed decision register

| Decision ID | Decision statement | Alternatives | Recommendation | Hard H-D prerequisites | Consequences | Required evidence | Status |
|---|---|---|---|---|---|---|---|
| H-D01 | Whether to use closed typed families as the next documentary candidate, with explicit separation of identity key/integrity metadata/observed bytes only | A staged closed-family analysis; B explicit adapter-first design; C defer admission and retain approved constraints only | RECOMMENDATION — NOT APPROVED: A as a narrowly bounded candidate; C if unresolved key/preimage policy is unacceptable | None; inherited scope only | Enables precise later documentary questions, not actual family admission, full F-D01 or implementation | Independent source review and owner scope choice; no provider required | PROPOSED — NOT APPROVED |
| H-D02 | Select candidate family/namespace registry keys independent of digest metadata, and explicit context-to-namespace binding | Separate namespace/family keys; globally scoped IDs with explicit immutable namespace authority; defer key selection | Prefer namespace+family+stable declared ID/version slots, with no new wire field implied | H-D01 | Changed hash must not automatically legitimise same allegedly immutable object; cross-namespace IDs not auto aliases | Future same-ID/conflict/namespace prose and separately authorised finite vectors; no lookup performed | PROPOSED — NOT APPROVED |
| H-D03 | Select PG canonical-equivalence versus additional raw-wire artifact identity policy without changing PG-C14N-1 | Canonical PG identity with separately tracked raw artifacts; strict raw artifact freeze per registry; defer | Prefer preserving canonical PG equality plus separately modelled raw artifacts; no automatic same-raw conflict rule | H-D02 | Whitespace/key-order variants may share binding while raw hashes differ; cache/distribution policy must be explicit | Future V019/020/021-style paired wire/canonical correspondence; no new hashes in H | PROPOSED — NOT APPROVED |
| H-D04 | Select raw ByteRef and immutable-binding metadata/header consistency policy, media-type interpretation boundary and immutable change procedure | Stable key plus associated digest/length; explicitly versioned raw object IDs in a future schema; defer | Prefer stable unversioned raw key with no hash-as-version loophole; new content needs explicit identity/version policy | H-D02 | Hash/length constraints and independently observed bytes compared separately; media interpretation not guessed | Future changed hash/length/header/media cases and actual custody later | PROPOSED — NOT APPROVED |
| H-D05 | Select role-sensitive PolicyRef comparison and supplied HeadRef shape boundaries while keeping target preimages/authenticity open | Role from closed slot; new version with explicit role tags; exclude these families from initial admission pending contracts | Prefer slot-context analysis only; defer target preimage/currentness admission until OP-22/24/23 choices | H-D02 | No rights/authority transfer or latest selection from equal policy/head hashes | Exact role-to-profile and target byte contracts later; real head/registry evidence independently qualified | PROPOSED — NOT APPROVED |
| H-D06 | Choose explicit declared edge vocabulary and traversal-order specification scope, separately from closure admission | Closed schema/field declared edges with opaque ByteRef; selected typed expansion profile; defer | Prefer no inferred edges and explicitly selected order; do not extend P1-DIAG-01 to graph/nested records | H-D02 | Array-edge occurrences and shared nodes remain distinguishable; schema/version/edge profiles stay unapproved until chosen | Future repeated/shared/opaque/missing edge cases; no graph traversal executed/authorised | PROPOSED — NOT APPROVED |
| H-D07 | Choose logical integrity-validation reuse prerequisites distinct from physical read/allocation/retry accounting | Reuse only exact validated family/identity/metadata under selected equivalence; no logical reuse; defer | Prefer separate accounting layers after byte-equivalence decision; no free physical work | H-D03, H-D04, H-D06 | May enable F-D04/F-D05 units; cannot choose caps or create cache design | Future alias/cache reset/accounting plans after separate approval; runtime measurement later | PROPOSED — NOT APPROVED |
| H-D08 | Choose whether adapters/migration/reapproval are a separate future contract and what must never be inherited | Separate version-specific adapter and fresh subject/review decisions; reject legacy for new profile; defer all migration | Prefer separate future F-D06/F-D07 scope; no silent upgrade or inherited review | H-D03, H-D04, H-D05, H-D06 | Retains X04 mandatory bindings and changed subject; concrete versions/types and continuity still open | Future version transform/provenance/subject mutation controls; actual review/rights evidence later | PROPOSED — NOT APPROVED |
| H-D09 | Decide future closure conformance plan scope after identity/edge choices, preserving X03 layers and resource prerequisites | Separate real acyclic crypto closure and abstract-cycle tests; defer crypto admission until complete contract; no fake cycle option | Prefer two distinct evidence layers; OP-07/08/09 and F-D04/05 still require their own decisions | H-D06, H-D07 | An F-D01 subdecision does not approve complete closure, resource budgets or traversal implementation | Separately authorised later literal/vector plan; no executable or digest values produced now | PROPOSED — NOT APPROVED |
| H-D10 | Decide what resolver/provider evidence must be separately commissioned or remain blocked, without choosing/integrating one now | Separate qualified immutable resolver and trusted-state scope; independent qualified alternative; retain blocked claims | Prefer explicit qualification requirements or defer, never supplied digest-as-authority | H-D02 | Pure lookup/content equality never proves actual identity/currentness/OS enforcement or permission | Actual host/provider/access/custody/replay/TOCTOU qualification only under later explicit authorisation | PROPOSED — NOT APPROVED |

[PROPOSED] These H-D prerequisites are **owner decision order**, not instructions to implement or connect providers. Existing OP/F-D constraints are additional external scope gates, not silently treated as approved. For example H-D06 can choose a candidate edge-policy discussion while excluding unselected policy/head/typed expansion families; actual inclusion needs H-D04/05/OP-22/24. No implicit family admission from a dependency arrow.

## Explicit questions — approve, reject or defer separately

### H-D01

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Whether to use closed typed families as the next documentary candidate, with explicit separation of identity key/integrity metadata/observed bytes only? Явные альтернативы: A staged closed-family analysis; B explicit adapter-first design; C defer admission and retain approved constraints only. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Independent source review and owner scope choice; no provider required.

### H-D02

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Select candidate family/namespace registry keys independent of digest metadata, and explicit context-to-namespace binding? Явные альтернативы: Separate namespace/family keys; globally scoped IDs with explicit immutable namespace authority; defer key selection. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Future same-ID/conflict/namespace prose and separately authorised finite vectors; no lookup performed.

### H-D03

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Select PG canonical-equivalence versus additional raw-wire artifact identity policy without changing PG-C14N-1? Явные альтернативы: Canonical PG identity with separately tracked raw artifacts; strict raw artifact freeze per registry; defer. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Future V019/020/021-style paired wire/canonical correspondence; no new hashes in H.

### H-D04

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Select raw ByteRef and immutable-binding metadata/header consistency policy, media-type interpretation boundary and immutable change procedure? Явные альтернативы: Stable key plus associated digest/length; explicitly versioned raw object IDs in a future schema; defer. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Future changed hash/length/header/media cases and actual custody later.

### H-D05

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Select role-sensitive PolicyRef comparison and supplied HeadRef shape boundaries while keeping target preimages/authenticity open? Явные альтернативы: Role from closed slot; new version with explicit role tags; exclude these families from initial admission pending contracts. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Exact role-to-profile and target byte contracts later; real head/registry evidence independently qualified.

### H-D06

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Choose explicit declared edge vocabulary and traversal-order specification scope, separately from closure admission? Явные альтернативы: Closed schema/field declared edges with opaque ByteRef; selected typed expansion profile; defer. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Future repeated/shared/opaque/missing edge cases; no graph traversal executed/authorised.

### H-D07

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Choose logical integrity-validation reuse prerequisites distinct from physical read/allocation/retry accounting? Явные альтернативы: Reuse only exact validated family/identity/metadata under selected equivalence; no logical reuse; defer. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Future alias/cache reset/accounting plans after separate approval; runtime measurement later.

### H-D08

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Choose whether adapters/migration/reapproval are a separate future contract and what must never be inherited? Явные альтернативы: Separate version-specific adapter and fresh subject/review decisions; reject legacy for new profile; defer all migration. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Future version transform/provenance/subject mutation controls; actual review/rights evidence later.

### H-D09

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Decide future closure conformance plan scope after identity/edge choices, preserving X03 layers and resource prerequisites? Явные альтернативы: Separate real acyclic crypto closure and abstract-cycle tests; defer crypto admission until complete contract; no fake cycle option. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Separately authorised later literal/vector plan; no executable or digest values produced now.

### H-D10

**PROPOSED — NOT APPROVED.** Утвердить ли только исследуемое направление: Decide what resolver/provider evidence must be separately commissioned or remain blocked, without choosing/integrating one now? Явные альтернативы: Separate qualified immutable resolver and trusted-state scope; independent qualified alternative; retain blocked claims. Ответ должен отдельно определить выбранную альтернативу или defer. Это не принятие всех OP-09/F-D01, не approval конкретных schema/key/edge/limit/migration решений вне вопроса, не разрешение реализации или provider operations. Evidence needed: Actual host/provider/access/custody/replay/TOCTOU qualification only under later explicit authorisation.

## Registry, integrity and namespace alternatives requiring separate answers

| Question | Candidate choice | Competing choice / still OPEN |
|---|---|---|
| [PROPOSED] Raw immutable identity | Namespace+raw-family+stable object_id, with hash/length as expected integrity constraints | Explicit future versioned object schema or defer; do not silently use changed hash as legitimate version |
| [PROPOSED] PG object identity | Namespace+PG-family+exact contract/id/revision; matching canonical binding/preimage separately | Additional strict raw artifact freeze is a distinct distribution policy; never change PG-C14N-1 to enforce it |
| [PROPOSED] Binding identity | Separate toolchain/executor family+schema/id/revision, raw integrity/header constraints | Explicit cross-family adapter only in new reviewed contract; no structural-shape interchange |
| [PROPOSED] Namespace | Explicit pure comparison context with later actual namespace authority separately qualified | Global IDs only if their uniqueness/trust/collision semantics are explicitly fixed; missing namespace is not guessed |
| [PROPOSED] Policy roles | Role derived from selected closed slot/profile, distinct semantic comparison | Explicit role-tagged new version, or exclude role-dependent admission until OP-24 chosen |
| [OPEN_CONTRACT_DETAIL] Policy/head/use-scope hash metadata | Separately pin exact target/byte/domain/profile recipe first | No guessed raw/PG-domain default; matching supplied string is only supplied equality |

[APPROVED] SubjectKey changes under X04 are not an identity-key loophole: a reviewed subject is intentionally a compound exact binding, not the raw object registry key. Equal content in another subject/role does not transfer approvals/rights. [OPEN_CONTRACT_DETAIL] Details of compound comparison and policy/reapproval remain unadopted; H-D08 does not choose migration or continuity.

## Minimal independent owner scope

[PROPOSED] Prefer **H-D01 alone** as the smallest first answer: may closed typed separation of key, metadata and observed bytes be developed as the next documentary candidate, with no concrete family/registry/admission/edge/version/limit/resolver/cache/migration adopted? Rejection/defer (C) is legitimate. No live provider, F-D04/05 or resource number is needed merely to discuss that direction.

[PROPOSED] If owner wants concrete future documentary progress, decide H-D02 namespace/key principles next, then H-D03 PG equivalence and H-D04 raw integrity/header policy separately. H-D05's policy/head target preimages can remain excluded/open while narrower families are researched; do not pretend all families are ready. This package does not request implementation, exact numeric caps or full OP-09 acceptance.

## Decision dependency graph and sequence

[PROPOSED] Exact hard prerequisite adjacency list:

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

[PROPOSED] Sequence: independent audit→owner H-D01→H-D02→H-D03/04/05/06 as applicable→H-D07 logical reuse→H-D08 separately scoped migration research/H-D09 closure evidence plan. H-D10 can define future operational evidence requirements after key/namespace scope, without connecting a provider. Graph is checked for cycles; no hard prerequisite for H-D01 and no pure decision depends on actual provider availability. External OP-07/08/09/F-D04/05, OP-22/24/F-D06/07 and operational qualification gates remain distinct.

## Security and Story Studio product consequences

[PROPOSED] Explicit IDs/roles prevent an RU/UK plan, source/evaluation fragment, asset/licence, toolchain or reviewer-policy record from being substituted merely because bytes/hash happen to match. Separate exact subject binding preserves which topic, evidence, rendering inputs and intended use were actually reviewed. More explicit types can reject legitimate legacy documents until versions are selected; adapters may improve compatibility but multiply hidden-transform/provenance/review risks. Deferral retains safe existing diagnostic/Preview scope without claiming a new gate.

[OPERATIONAL_EVIDENCE_REQUIRED] A reproducible reference registry still cannot answer whether a topic is editorially worthwhile/scientifically sound, a material is licensed for actual use, reviewer is competent/authorised, history current or files/tools immutable during use. No real rights/reviewer assignments or production permissions follow from any pure comparison. H-D10/OP-15/17/20/23/28 require separately authorised actual evidence; Storage S3 remains unqualified and Windows native tests NOT_RUN.

[OPEN_CONTRACT_DETAIL] All20 OP stay OPEN;7 CM stay PARTIAL; F-D01/F-D04–F-D12 stay PROPOSED — NOT APPROVED. F-D02/A and F-D03/A stay APPROVED_LIMITED_SCOPE; G accepted status does not promote its fixture wrappers/token conventions. X01–X04/P1/P1-DIAG-01 unchanged. **STOP after publication — independent audit and separate owner decision.**
