# Closed Markdown profile proposal

| Variant | Determinism and ambiguity | Portability and compatibility | Maintenance, evidence and error risks |
|---|---|---|---|
| N-MD-A | Restrict semantic registers to simple headings and single-line tables. Explicit section identity is needed. | CPU-only text processing is feasible in principle. Windows PowerShell round-trip and CRLF evidence are required. Older free-form packets can fall outside the subset. | Small grammar surface. False rejection of richer historical syntax and false acceptance of plausible wrong statuses require separate structure and source checks. |
| N-MD-B | Extend A with scoped escapes, code spans and controlled multiline constructs. Token precedence must be specified. | Broader legacy coverage adds dialect drift. CPU-only effort and Windows/Linux parity need independent evidence. | More complex boundary analysis. Require ambiguous delimiter and continuation specimens, independent column comparisons and explicit unsupported outcomes. |
| N-MD-C | Structured records carry separately modeled evidence. Verify Markdown correspondence independently. | Text records and Markdown should round-trip across hosts with future CPU-only evidence. Legacy import would require a scoped mapping. | Two representations increase maintenance and false-pass risk if only the records are inspected. Require exact fetched Markdown and record-to-row evidence. |

The labels below describe candidates, with no approved grammar or runtime result. In C the profile of the human-readable rendering remains independently reviewable.

| Construct | N-MD-A | N-MD-B | N-MD-C | Boundary to study |
|---|---|---|---|---|
| Headings and hierarchy | CANDIDATE_SUPPORTED | CANDIDATE_SUPPORTED | CANDIDATE_SUPPORTED | Require scoped section identity rather than title substring. |
| Duplicate headings | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS | Distinguish duplicate required headings from equal titles under different parents. |
| Tables and separators | CANDIDATE_SUPPORTED | CANDIDATE_SUPPORTED | CANDIDATE_SUPPORTED | Check width and data rows independently. |
| Escaped pipes | CANDIDATE_REJECTED | CANDIDATE_SUPPORTED | DEFERRED | Require explicit precedence and parity evidence for B. |
| Inline code | CANDIDATE_REJECTED | CANDIDATE_SUPPORTED | DEFERRED | Test whether a delimiter within a span can split a cell. |
| Fenced blocks | CANDIDATE_REJECTED | CANDIDATE_SUPPORTED | DEFERRED | B may allow example blocks outside active registers. |
| Nested-looking fences | CANDIDATE_REJECTED | AMBIGUOUS | DEFERRED | Different delimiter lengths can move the active boundary. |
| Backslashes | CANDIDATE_REJECTED | CANDIDATE_SUPPORTED | DEFERRED | Distinguish literal backslashes and escape introducers. |
| Unicode and normalization | DEFERRED | DEFERRED | DEFERRED | Compare raw identity and scalar interpretations; no normalization selected. |
| BOM | DEFERRED | DEFERRED | DEFERRED | Preserve raw bytes and study decode boundary. |
| CRLF and LF | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS | Displayed equivalence supplies no raw Git identity. |
| Whitespace | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS | Separate margins from cell data. |
| Empty or malformed tables | CANDIDATE_REJECTED | AMBIGUOUS | AMBIGUOUS | A required empty register needs different evidence from a deliberately empty optional index. |
| Missing or extra cells | CANDIDATE_REJECTED | CANDIDATE_REJECTED | CANDIDATE_REJECTED | Reject shape in these proposals; no automatic padding or truncation. |
| Multiline cells | CANDIDATE_REJECTED | CANDIDATE_SUPPORTED | DEFERRED | B would need explicit continuation boundaries. |
| HTML fragments | CANDIDATE_REJECTED | CANDIDATE_REJECTED | DEFERRED | Rendered HTML and documentary extraction have distinct trust boundaries. |
| Duplicate row IDs | CANDIDATE_REJECTED | CANDIDATE_REJECTED | CANDIDATE_REJECTED | Check scoped identity before indexing. |
| Diagnostic placeholders | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS | A quoted observation differs from an array type name occupying a required row. |
| Syntax versus source correspondence | CANDIDATE_SUPPORTED | CANDIDATE_SUPPORTED | CANDIDATE_SUPPORTED | Require separate structural and semantic evidence. |

Historical example. The original K packet has four standalone placeholders in required table bodies. FIX-1 restored rows from pinned sources and quoted the diagnostic strings in its assessment. The L architecture separates V3 structural checks, V4 source correspondence and V7 checks of the published artifact. Synthetic example. A valid status cell marked APPROVED can still conflict with the scoped owner record. Any future qualification would need paired valid and invalid artifacts, exact bytes and independent cross-host observations. No parser or profile is selected.
