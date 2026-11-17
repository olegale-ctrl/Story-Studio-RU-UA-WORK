# Owner decision dossier

Every decision is independently answerable as approve a documentary scope, reject or defer. No choice is selected. Prerequisites express evidence dependencies only.

## K-D01 — Comparison domain

**PROPOSED — NOT APPROVED**

- A. Study exact bytes.
- B. Study exact scalars.
- C. Defer selection.
- Recommendation — NOT APPROVED. C for the next documentary review.
- Prerequisites. none.
- Risk. Cross-domain aliases.
- Evidence. Independent paired carriers and scalar evidence.
- Possible limited approval. Choose a study direction only.
- Still unapproved. carrier, comparator and admissibility.

## K-D02 — Decoding and BOM

**PROPOSED — NOT APPROVED**

- A. Study strict scalar decode and separate marker rejection.
- B. Study byte preservation with explicit carrier boundaries.
- C. Defer decoding choice.
- Recommendation — NOT APPROVED. C for the next documentary review.
- Prerequisites. K-D01.
- Risk. Marker stripping and decoder disagreement.
- Evidence. Malformed, supplementary and BOM cases.
- Possible limited approval. Bound the decoding question.
- Still unapproved. encoding and malformed-input policy.

## K-D03 — Normalization and case

**PROPOSED — NOT APPROVED**

- A. Study exact comparison without transforms.
- B. Study explicit transforms and collision costs.
- C. Defer transform selection.
- Recommendation — NOT APPROVED. C for the next documentary review.
- Prerequisites. K-D01.
- Risk. Unexpected aliases.
- Evidence. NFC/NFD, NFKC and fold pairs.
- Possible limited approval. Approve collision investigation only.
- Still unapproved. transforms and Unicode data version.

## K-D04 — Admissibility

**PROPOSED — NOT APPROVED**

- A. Study restricted repertoire.
- B. Study broader repertoire with independent display rules.
- C. Defer admissibility.
- Recommendation — NOT APPROVED. C for the next documentary review.
- Prerequisites. K-D02, K-D03.
- Risk. Truncation and hidden labels.
- Evidence. Empty, control, whitespace and NUL evidence.
- Possible limited approval. Scope admissibility research.
- Still unapproved. grammar, bounds and error behavior.

## K-D05 — Profile principle

**PROPOSED — NOT APPROVED**

- A. Study a versioned comparison profile.
- B. Study one separately specified domain.
- C. Defer profile selection.
- Recommendation — NOT APPROVED. C for the next documentary review.
- Prerequisites. K-D01.
- Risk. Cross-version and downgrade confusion.
- Evidence. Compatibility and unknown profile cases.
- Possible limited approval. Approve profile feasibility review.
- Still unapproved. IDs, schema and migration.

## K-D06 — Request association

**PROPOSED — NOT APPROVED**

- A. Record supplied request association.
- B. Study authenticated request association.
- C. Defer association design.
- Recommendation — NOT APPROVED. A for the next documentary review.
- Prerequisites. none.
- Risk. Request substitution.
- Evidence. Detached and contradictory assertion cases.
- Possible limited approval. Approve study of supplied provenance.
- Still unapproved. wire fields and source of request identity.

## K-D07 — Occurrence association

**PROPOSED — NOT APPROVED**

- A. Study attachment to individual occurrence.
- B. Study separately authenticated attachment.
- C. Defer occurrence mapping.
- Recommendation — NOT APPROVED. A for the next documentary review.
- Prerequisites. K-D06.
- Risk. Detached or copied reference.
- Evidence. Repeated identical references in distinct slots.
- Possible limited approval. Permit documentary occurrence comparison.
- Still unapproved. tuple and cryptographic binding.

## K-D08 — Family and role isolation

**PROPOSED — NOT APPROVED**

- A. Study distinctions as separate coordinates.
- B. Study restricted explicit role/family relationships.
- C. Defer concrete isolation policy.
- Recommendation — NOT APPROVED. A for the next documentary review.
- Prerequisites. K-D07.
- Risk. Cross-family and role confusion.
- Evidence. Equal-byte cross-family and wrong-role cases.
- Possible limited approval. Preserve documentary distinctions.
- Still unapproved. family/role admission and conversions.

## K-D09 — Authority and currentness

**PROPOSED — NOT APPROVED**

- A. Study separately qualified authority and observation history.
- B. Record untrusted claims with provenance only.
- C. Defer any authority model.
- Recommendation — NOT APPROVED. C for the next documentary review.
- Prerequisites. K-D06.
- Risk. Replay and unjustified trust.
- Evidence. Independent chronology, issuer and provider evidence.
- Possible limited approval. Require distinct evidence questions.
- Still unapproved. issuer, trust root and currentness rules.

## K-D10 — Missing or ambiguous context

**PROPOSED — NOT APPROVED**

- A. Study withholding positive documentary conclusions.
- B. Study separate documentary absence and conflict findings.
- C. Defer disposition classification.
- Recommendation — NOT APPROVED. A for the next documentary review.
- Prerequisites. K-D07, K-D08, K-D09.
- Risk. Default inference or silent conflict resolution.
- Evidence. Missing, conflicting and historical records.
- Possible limited approval. Limit documentary claim strength.
- Still unapproved. runtime denial, diagnostics and migration.
