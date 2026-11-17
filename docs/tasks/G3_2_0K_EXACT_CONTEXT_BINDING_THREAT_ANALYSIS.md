# Exact context binding threat analysis

Keep the exact request and exact reference occurrence distinct. The occurrence contributes its asserted family, declared stable identity and explicit version or revision where present. Expected digest and length remain separate from independently observed bytes and headers. Preserve the policy role, registry observation and chronology, and provider/custody evidence independently. SubjectKey and exact plan/toolchain/executor bindings retain X04 scope. A change in a render-affecting binding changes the exact plan and SubjectKey. A label-only change has unresolved semantics.

K-BIND-A studies explicit supplied coordinates as documentary association. K-BIND-B studies a future authenticated association requiring approved provenance, authority, currentness and custody. K-BIND-C defers binding and preserves the separate assertions. No candidate selects a concrete tuple, wire field, signature domain, cryptographic preimage, algorithm or runtime disposition.

| Risk | K-BIND-A | K-BIND-B | K-BIND-C |
|---|---|---|---|
| Detached reference | Record only the surviving assertions and their source | Evidence would have to cover the original exact occurrence | Preserve the evidence gap or ambiguity and defer binding |
| Namespace swapping | Expose contradictory supplied associations | Qualified evidence would have to distinguish the two associations | Preserve the evidence gap or ambiguity and defer binding |
| Cross-family substitution | Keep the family assertion distinct | Evidence would have to support family-specific use | Preserve the evidence gap or ambiguity and defer binding |
| Same digest, different namespace | Preserve both labels and expected integrity metadata | Digest alone supplies no issuer or association evidence | Preserve the evidence gap or ambiguity and defer binding |
| Wrong role | Record the semantic slot separately | Evidence would have to cover the specific role | Preserve the evidence gap or ambiguity and defer binding |
| Wrong revision | Preserve the stated revision and any mismatch | Evidence would have to refer to the exact revision | Preserve the evidence gap or ambiguity and defer binding |
| Stale observation | Retain source and chronology | A separately qualified currentness model would be required | Preserve the evidence gap or ambiguity and defer binding |
| Cache aliasing | Flag an observation detached from its context | Evidence would have to retain association across reuse | Preserve the evidence gap or ambiguity and defer binding |
| Context stripping | Mark absent context explicitly | Remaining evidence would have to establish the exact association independently | Preserve the evidence gap or ambiguity and defer binding |
| Replay | Record chronology without assuming freshness | Independent currentness evidence would be required | Preserve the evidence gap or ambiguity and defer binding |
| Missing context | Leave the coordinate unknown | No authenticated association earned from missing evidence | Preserve the evidence gap or ambiguity and defer binding |
| Conflicting context | Keep both claims with their provenance | Evidence would have to resolve the specific contradiction | Preserve the evidence gap or ambiguity and defer binding |
| Historical namespace-free record | Preserve historical bytes and absence | Any new association would require separate evidence and migration approval | Preserve the evidence gap or ambiguity and defer binding |

The evidence questions advance independently. Supplied association identifies what was claimed. Deterministic comparison describes agreement under a domain. Authenticated binding requires evidence of the exact association. Authorized issuance additionally requires scoped issuer authority. Trusted currentness requires qualified chronology and custody. Permission requires a separate use decision. No stage establishes the next.

P1-05 distinguishes PG canonical bytes from complete raw bytes. P1-06 retains the seven ordered stages of bounded input and decoding, format, local binding, reference and closure validation, mode and subject consistency, trusted state/product/rights, and execution/evidence. P1-DIAG-01 only orders same-code/same-stage private diagnostics for the historical root fields. These inherited rules supply neither a namespace encoding nor authority. X01 through X04, F-D02/A root accounting and F-D03/A report scope remain in force.

RECOMMENDATION — NOT APPROVED. Preserve ambiguity under K-BIND-C while studying documentary provenance under K-BIND-A.
