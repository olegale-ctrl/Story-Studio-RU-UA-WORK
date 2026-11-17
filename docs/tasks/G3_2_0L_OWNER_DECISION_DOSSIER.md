# Owner decision dossier

Each decision may be approved in a limited documentary scope, rejected or deferred. No alternative has been selected. The prerequisite column defines a local graph, independent of H-D, I-Q and K-D.

## L-D01 — Validation scope

**PROPOSED — NOT APPROVED**

- A. Check inputs and independently checked final artifacts.
- B. Check published artifact structure only.
- C. Defer scope.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. none.
- Risk. Input success mistaken for published success.
- Required evidence. FIX-1 reproduction and proposed stage map.
- Possible approval scope. Study artifact-level gates.
- Remains unapproved. Mandatory runtime tooling.

## L-D02 — Markdown model

**PROPOSED — NOT APPROVED**

- A. Study named Markdown subset and explicit unsupported syntax.
- B. Study general dialect compatibility.
- C. Defer dialect.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D01.
- Risk. Escapes and fences misparsed.
- Required evidence. Paired delimiter and fence cases.
- Possible approval scope. Select a study direction.
- Remains unapproved. Dialect and parser library.

## L-D03 — Source authority

**PROPOSED — NOT APPROVED**

- A. Study row-family authority and scoped supersession.
- B. Study an owner-maintained manifest.
- C. Defer authority mapping.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D01.
- Risk. Indexes mistaken for authority.
- Required evidence. Conflicting provenance examples.
- Possible approval scope. Study explicit provenance mapping.
- Remains unapproved. Tie-breaking policy.

## L-D04 — Semantic correspondence and ordering

**PROPOSED — NOT APPROVED**

- A. Compare full cells and normative order.
- B. Compare scoped sets with editorial order.
- C. Defer ordering rules.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D02, L-D03.
- Risk. Count-only acceptance.
- Required evidence. Missing, duplicated and reordered examples.
- Possible approval scope. Distinguish identity from order.
- Remains unapproved. Normalization and comparison rule.

## L-D05 — Graph verification

**PROPOSED — NOT APPROVED**

- A. Study closed adjacency and cycle evidence.
- B. Study separately typed external prerequisites.
- C. Defer graph rules.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D03, L-D04.
- Risk. Silently altered prerequisites.
- Required evidence. Known nodes, edges and cycles.
- Possible approval scope. Require independent graph evidence in study.
- Remains unapproved. Graph schema and execution.

## L-D06 — Git identity and remote verification

**PROPOSED — NOT APPROVED**

- A. Study fetched-object checks pinned to branch head.
- B. Study detached immutable-commit checks only.
- C. Defer publication verification design.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D01.
- Risk. Stale remote ref.
- Required evidence. Blob, parent, full-tree and ref evidence.
- Possible approval scope. Study publication evidence boundary.
- Remains unapproved. Workflow and automation.

## L-D07 — Self-hash handling

**PROPOSED — NOT APPROVED**

- A. Retain ACCEPTANCE-SHA-01 in design.
- B. Study external manifests with same boundary.
- C. Defer tooling around external handoff.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D06.
- Risk. Circular or unbound claims.
- Required evidence. Candidate and external hash linkage.
- Possible approval scope. Retain existing documentary boundary.
- Remains unapproved. Manifest format.

## L-D08 — Severity and STOP

**PROPOSED — NOT APPROVED**

- A. Study explicit scope and evidence blockers.
- B. Study per-stage independent dispositions.
- C. Defer severity mapping.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D04, L-D05, L-D06.
- Risk. Warning described as approval.
- Required evidence. Failed and incomplete scenarios.
- Possible approval scope. Study withholding completion claims.
- Remains unapproved. Runtime policy or new codes.

## L-D09 — Historical audit

**PROPOSED — NOT APPROVED**

- A. Study scoped read-only sampling.
- B. Study comprehensive separate retrospective.
- C. Defer historical work.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D02, L-D03.
- Risk. Retroactive approval assumptions.
- Required evidence. Pinned historical witnesses and sampling limits.
- Possible approval scope. Define scope of an audit proposal.
- Remains unapproved. Reclassification of prior work.

## L-D10 — Implementation and rollout

**PROPOSED — NOT APPROVED**

- A. Keep implementation separately authorized.
- B. Study phased rollout conditions on paper.
- C. Defer rollout discussion.
- Recommendation — NOT APPROVED. A for documentary review.
- Prerequisites. L-D07, L-D08, L-D09.
- Risk. Proposal mistaken for action.
- Required evidence. Owner scope and future independent review.
- Possible approval scope. Approve design review only.
- Remains unapproved. Any implementation, CI or rollout.
