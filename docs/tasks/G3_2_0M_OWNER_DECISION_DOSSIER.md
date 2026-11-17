# Owner decision dossier

Each decision is independently answerable within its documentary scope. All alternatives remain open. Only the local M prerequisite graph is described here.

## M-D01 — Markdown representation

**PROPOSED — NOT APPROVED**

- A. Study a closed subset.
- B. Study dialect or dual representation.
- C. Defer to manual review.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. none.
- Risk. Grammar drift.
- Evidence. Paired byte and structural evidence.
- Possible limited approval. Study competing representation models.
- Unresolved normative questions. Dialect, library and schema.

## M-D02 — Table grammar and delimiters

**PROPOSED — NOT APPROVED**

- A. Study explicit separators and escape rules.
- B. Study dialect-specific table extensions.
- C. Defer table grammar.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D01.
- Risk. Column drift.
- Evidence. Escaped, missing and extra cell evidence.
- Possible limited approval. Analyze table boundaries.
- Unresolved normative questions. Accepted grammar and diagnostics.

## M-D03 — Unicode, BOM and newlines

**PROPOSED — NOT APPROVED**

- A. Study raw-byte provenance and explicit decode boundary.
- B. Study separately scoped normalization candidates.
- C. Defer text treatment.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D01.
- Risk. Invisible byte changes.
- Evidence. Paired raw bytes and scalar observations.
- Possible limited approval. Separate identity from presentation.
- Unresolved normative questions. Encoding and normalization rules.

## M-D04 — Unsupported syntax

**PROPOSED — NOT APPROVED**

- A. Study explicit unsupported disposition.
- B. Study dialect fallback with provenance.
- C. Defer status mapping.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D02, M-D03.
- Risk. Silent fallback.
- Evidence. Fences, HTML and multiline ambiguity.
- Possible limited approval. Study conservative claim withholding.
- Unresolved normative questions. Runtime handling.

## M-D05 — Source granularity

**PROPOSED — NOT APPROVED**

- A. Study row-family mapping.
- B. Study owner manifest or qualified chain.
- C. Defer automatic selection.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. none.
- Risk. Object pin confused with authority.
- Evidence. Scoped claims with pinned provenance.
- Possible limited approval. Study authority rationale per record.
- Unresolved normative questions. Authority schema and delegation.

## M-D06 — Supersession and history

**PROPOSED — NOT APPROVED**

- A. Study named-field supersession.
- B. Study explicit qualified chain.
- C. Defer classification.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D05.
- Risk. Partial amendment becomes blanket approval.
- Evidence. Chronology with preserved old statements.
- Possible limited approval. Study field scope.
- Unresolved normative questions. Supersession and revocation rules.

## M-D07 — Conflicting authority

**PROPOSED — NOT APPROVED**

- A. Study owner resolution with both claims recorded.
- B. Study explicitly scoped precedence.
- C. Defer affected conclusion.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D05, M-D06.
- Risk. Recency mistaken for authority.
- Evidence. Conflicting alternatives and exact scopes.
- Possible limited approval. Document conflict without guessing precedence.
- Unresolved normative questions. Universal tie breaker.

## M-D08 — Source-to-rendered-row binding

**PROPOSED — NOT APPROVED**

- A. Study cell-level correspondence.
- B. Study dual record mapping.
- C. Defer automatic binding.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D02, M-D05, M-D07.
- Risk. Valid structure masks wrong status.
- Evidence. Pinned source and emitted row pairs.
- Possible limited approval. Study comparisons on both representations.
- Unresolved normative questions. Identity, ordering and matching contract.

## M-D09 — Publication and currentness

**PROPOSED — NOT APPROVED**

- A. Study fetched Git object and observed head.
- B. Study immutable commit evidence with no branch claim.
- C. Defer currentness inference.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D06, M-D08.
- Risk. Moved ref treated as stable.
- Evidence. Timestamped ref and blob evidence.
- Possible limited approval. Study publication provenance.
- Unresolved normative questions. Provider qualification and automation.

## M-D10 — Future qualification

**PROPOSED — NOT APPROVED**

- A. Keep qualification separately authorized.
- B. Study staged evidence gates on paper.
- C. Defer qualification research.
- Recommended research direction — NOT APPROVED. A for the next documentary review.
- Prerequisites. M-D04, M-D08, M-D09.
- Risk. Documentary checks conflated with conformance.
- Evidence. Independent scope assessment.
- Possible limited approval. Permit design review only.
- Unresolved normative questions. Implementation and operational policy.
