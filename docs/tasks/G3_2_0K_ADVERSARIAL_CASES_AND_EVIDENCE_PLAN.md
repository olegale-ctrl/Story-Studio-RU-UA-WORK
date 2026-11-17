# Documentary adversarial cases and evidence plan

V denotes a future vector proposal. All scenarios are synthetic, prose-only and unexecuted. Concrete namespace outcomes remain open.

## K-V001 — Equal explicit octets

**Setup and ambiguity.** Consider equal explicit octets in two supplied contexts. Byte evidence agrees; scalar interpretation depends on decoding.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** carrier. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V002 — Equal decoded scalars

**Setup and ambiguity.** Consider equal decoded scalars in two supplied contexts. Scalar candidate agrees; wrapper octets may differ.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** domain. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V003 — Distinct UTF-8 byte spellings

**Setup and ambiguity.** Consider distinct UTF-8 byte spellings in two supplied contexts. Strict UTF-8 has a unique encoding per scalar sequence; non-shortest bytes are malformed in that domain.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** decoding. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V004 — Literal versus escaped JSON

**Setup and ambiguity.** Consider literal versus escaped JSON in two supplied contexts. Transport spelling differs; decoded scalar can coincide.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** escape treatment. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V005 — Composed versus decomposed text

**Setup and ambiguity.** Consider composed versus decomposed text in two supplied contexts. Exact scalar comparison distinguishes NFC/NFD spellings.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** normalization. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V006 — Compatibility forms

**Setup and ambiguity.** Consider compatibility forms in two supplied contexts. Exact comparison distinguishes forms compatibility mapping might collapse.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** normalization. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V007 — Case variation

**Setup and ambiguity.** Consider case variation in two supplied contexts. Exact equality differs from a fold.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** case. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V008 — Empty asserted label

**Setup and ambiguity.** Consider empty asserted label in two supplied contexts. Zero length can still be a supplied assertion.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** empty admissibility. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V009 — Invalid UTF-8

**Setup and ambiguity.** Consider invalid UTF-8 in two supplied contexts. Byte comparison remains possible; no strict scalar decoding.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** invalid input. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V010 — BOM present

**Setup and ambiguity.** Consider bOM present in two supplied contexts. Marker ownership can change the label boundary.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** BOM. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V011 — Embedded NUL

**Setup and ambiguity.** Consider embedded NUL in two supplied contexts. Truncation can collapse distinct labels at an interface.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** NUL. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V012 — Control scalar

**Setup and ambiguity.** Consider control scalar in two supplied contexts. Display can hide distinction despite exact comparison.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** controls. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V013 — ASCII and non-ASCII space

**Setup and ambiguity.** Consider aSCII and non-ASCII space in two supplied contexts. Whitespace handling can collapse distinct labels.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** whitespace. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V014 — Visual confusables

**Setup and ambiguity.** Consider visual confusables in two supplied contexts. Human similarity does not establish equality.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** repertoire. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V015 — URI-like spelling

**Setup and ambiguity.** Consider uRI-like spelling in two supplied contexts. Scheme canonicalization can collapse opaque spellings.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** URI interpretation. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V016 — UUID-like spelling

**Setup and ambiguity.** Consider uUID-like spelling in two supplied contexts. Case and separator normalization can collapse spellings.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** UUID interpretation. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V017 — Unsupported version

**Setup and ambiguity.** Consider unsupported version in two supplied contexts. No approved common interpretation exists.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** profile. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V018 — Duplicate descriptor keys

**Setup and ambiguity.** Consider duplicate descriptor keys in two supplied contexts. Different duplicate handling can yield different assertions.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** descriptor. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V019 — Excessive length

**Setup and ambiguity.** Consider excessive length in two supplied contexts. Work estimates differ for wire bytes and decoded scalars.

**Candidate interpretation and constraint.** Compare K-CMP-A octets with K-CMP-B scalars under their own domain assumptions. J-R1 leaves selection open.

**Open decision and result.** measurement and limits. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary or future conformance evidence: record both input representations and compare independent domain interpretations. Operational evidence would be needed for actual transport, logs or resource claims. **NOT_RUN.**

## K-V020 — Same digest across namespaces

**Setup and ambiguity.** Consider same digest across namespaces in two supplied contexts. Matching integrity metadata does not bind namespace.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** cross-namespace isolation. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of cross-namespace isolation where applicable. **NOT_RUN.**

## K-V021 — Same stable ID across namespaces

**Setup and ambiguity.** Consider same stable ID across namespaces in two supplied contexts. Local identity reuse does not imply one global subject.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** identity scope. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of identity scope where applicable. **NOT_RUN.**

## K-V022 — Conflicting metadata under one asserted identity

**Setup and ambiguity.** Consider conflicting metadata under one asserted identity in two supplied contexts. Expose discrepancy without inventing a replacement identity.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority. I-Q05/A separates expected metadata and observation.

**Open decision and result.** conflict policy. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of conflict policy where applicable. **NOT_RUN.**

## K-V023 — Namespace swapped between references

**Setup and ambiguity.** Consider namespace swapped between references in two supplied contexts. Supplied coordinates can reveal mismatch without proving origin.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** occurrence association. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of occurrence association where applicable. **NOT_RUN.**

## K-V024 — Detached context

**Setup and ambiguity.** Consider detached context in two supplied contexts. An isolated reference cannot prove its prior association.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** missing association. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of missing association where applicable. **NOT_RUN.**

## K-V025 — Cross-family alias

**Setup and ambiguity.** Consider cross-family alias in two supplied contexts. Equal bytes do not resolve a typed family claim.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** family isolation. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of family isolation where applicable. **NOT_RUN.**

## K-V026 — Policy role confusion

**Setup and ambiguity.** Consider policy role confusion in two supplied contexts. Role attribution requires independent support.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** role isolation. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of role isolation where applicable. **NOT_RUN.**

## K-V027 — SubjectKey/X04 change

**Setup and ambiguity.** Consider subjectKey/X04 change in two supplied contexts. Changed toolchain or executor binding affects the exact plan and SubjectKey under X04.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority. X04 retains exact plan binding.

**Open decision and result.** review and regrant. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of review and regrant where applicable. **NOT_RUN.**

## K-V028 — Historical namespace-free reference

**Setup and ambiguity.** Consider historical namespace-free reference in two supplied contexts. No owner decision supports retroactive labeling.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** migration. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of migration where applicable. **NOT_RUN.**

## K-V029 — Untrusted caller alias

**Setup and ambiguity.** Consider untrusted caller alias in two supplied contexts. Caller assertion is separate from mapping authority.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** issuer. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of issuer where applicable. **NOT_RUN.**

## K-V030 — Provider unavailable

**Setup and ambiguity.** Consider provider unavailable in two supplied contexts. Unavailability establishes no fact about authority or denial.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** availability policy. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of availability policy where applicable. **NOT_RUN.**

## K-V031 — Claimed issuer without provenance

**Setup and ambiguity.** Consider claimed issuer without provenance in two supplied contexts. Issuer text does not establish a trusted issuer.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** issuer trust. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of issuer trust where applicable. **NOT_RUN.**

## K-V032 — Signature-shaped text

**Setup and ambiguity.** Consider signature-shaped text in two supplied contexts. Formatting supplies no authenticated evidence.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** provenance. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of provenance where applicable. **NOT_RUN.**

## K-V033 — Stale or replayed observation

**Setup and ambiguity.** Consider stale or replayed observation in two supplied contexts. Historical observation cannot establish currentness.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** chronology. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of chronology where applicable. **NOT_RUN.**

## K-V034 — Cache collision

**Setup and ambiguity.** Consider cache collision in two supplied contexts. A matching digest or cached result cannot supply missing provenance.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** cache semantics. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of cache semantics where applicable. **NOT_RUN.**

## K-V035 — Windows reparse or TOCTOU

**Setup and ambiguity.** Consider windows reparse or TOCTOU in two supplied contexts. An observation can cease to describe the object later used.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority.

**Open decision and result.** custody. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of custody where applicable. **NOT_RUN.**

## K-V036 — Missing exact target

**Setup and ambiguity.** Consider missing exact target in two supplied contexts. An alternative revision cannot discharge existing exact PG target obligations.

**Candidate interpretation and constraint.** K-BIND-A can describe supplied coordinates, while K-BIND-B would require independently qualified provenance. J-A1 separates assertion and authority. X03 retains exact target obligations.

**Open decision and result.** namespace-layer handling. EXPECTED_RESULT_OPEN.

**Evidence.** Pure documentary evidence: track which assertion or observation belongs to each context. Operational evidence would require independently qualified records of namespace-layer handling where applicable. **NOT_RUN.**
