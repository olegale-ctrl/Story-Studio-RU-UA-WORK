# Namespace representation alternatives — no convention selected

**OWNER_AUTHORIZED_DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. Implementation FORBIDDEN.**

SI-INTEGRATION-G3.2.0j; 2026-11-17 (Europe/Kyiv). I-Q02 and I-Q03: **PROPOSED — NOT APPROVED**. H-D02 and full F-D01: **NOT APPROVED**.

## Four separately unselected alternatives

J-R1 is an explicitly supplied opaque identifier with an independently specified exact equality rule. Byte equality and decoded scalar-text equality are different candidates: distinct escape spellings may decode alike, while malformed UTF-8 has no valid scalar decoding. This document selects neither comparison domain nor encoding.

J-R2 is an explicit versioned structured-descriptor principle. Candidate type/context dimensions would need separate specification; no actual fields, accepted schema or wire version are introduced.

J-R3 is a qualified globally scoped identifier principle requiring issuer, uniqueness, collision and binding semantics. URI/UUID appearance supplies neither authority nor global uniqueness evidence.

J-R4 defers representation and preserves only the approved separation principles. It supplies no runtime fallback or admission capability.

| Dimension | J-R1 exact opaque | J-R2 structured | J-R3 qualified global | J-R4 defer |
|---|---|---|---|---|
| Identity ambiguity | Exact comparison domain must be chosen; visual sameness is insufficient | Component scope, unknown/duplicate interpretation and comparison order unresolved | Construction, issuer scope, collision and type qualification unresolved | Ambiguity retained explicitly; no identity verdict |
| Unicode normalization | No NFC/NFKC default; composed/decomposed values may differ under future exact convention | Per-dimension rules require a separate contract | Scheme rules cannot be assumed from appearance | No normalization selected |
| Case sensitivity | Exact case treatment still must be specified | Component-specific treatment could disagree | Scheme-specific case assumptions require explicit qualification | OPEN |
| UTF-8 validity | Byte candidate can expose invalid bytes; text candidate requires a decoder/validity policy | Transport and descriptor text validity separately needed | Global spelling/transport validity separately needed | No new accepted encoding |
| NUL/control characters | Equality, display/log safety and admissibility are distinct questions | Delimiter/escaping and display ambiguity need review | Scheme syntax cannot be guessed | No new admissibility decision |
| URI/UUID interpretation | Treating opaque input as parsed URI/UUID would change the candidate | Explicit semantics needed before interpretation | Qualified scheme/canonical spelling/issuer semantics required | No interpretation |
| Collision and aliasing | Unequal assertions not automatically aliases; exact match not proof of legitimate issuance | Duplicate/conflicting descriptors and equivalence need resolution | Duplicate issuance and spoofed issuer still possible | No alias mapping accepted |
| Version migration | No silent rewrite; continuity separately decided | Unknown descriptor versions need explicit compatibility policy | Scheme/issuer migration requires provenance | Migration deferred |
| Equality versus authority | Determinism compares supplied assertions only | Structured completeness is not authentication | Global appearance is not authority | Authoritative claims withheld |
| Backward compatibility | External context does not insert fields into old references | No descriptor retrofit into historical envelopes | Local IDs do not become global by string wrapping | Historical evidence preserved |
| Missing context | No cwd/user/path/env/tenant/profile/alias inference | No implicit descriptor defaults | No inferred global qualifier | Missing remains unresolved |
| Resource accounting | Comparison/decoding/alias work not free; OP-07/08 OPEN | Nested/duplicate/version work needs future accounting | Parsing/provenance/currentness work needs separate budgets | No resource enforcement claimed |
| Future conformance | Pin byte/text domain, encoding, admissibility, equality and negative evidence first | Pin shape/version/comparison/duplicate semantics separately | Pin global scheme, qualification, issuance and authority evidence separately | Audit open gaps before later task |

## Recommendation — not a selection

**RECOMMENDATION — NOT APPROVED:** study J-R1 as the smallest representation principle while explicitly deferring byte versus decoded-text equality and admissibility. J-R4 remains the appropriate separate answer if even that principle lacks owner support. This does not select concrete namespace encoding/equality, a registry tuple, or H-D02. J-R2/J-R3 require more unresolved schema/authority/migration commitments.

No default NFC, NFKC, casefold, trimming, URI normalization, UUID canonicalization or implicit tenant/user/path namespace. PG-C14N-1 remains unchanged; its scalar/JSON rules do not define equality for an unselected external namespace representation. NUL escaped inside valid historical JSON is different from a raw invalid JSON control byte; neither observation decides namespace admissibility.

Sources: [I options](G3_2_0I_REGISTRY_KEY_AND_NAMESPACE_OPTIONS.md), [I authority analysis](G3_2_0I_NAMESPACE_AUTHORITY_AND_CONFLICT_ANALYSIS.md), [D P1-03/05](G3_2_0D_P1_NORMATIVE_CONTRACT.md). Dependency: I-Q02 under H-D02; OP-09/22 and CM-071 remain open qualification gates.

**STOP. Await independent ChatGPT audit and separate owner approval. No merge, G3.2.1 or production permissions.**
