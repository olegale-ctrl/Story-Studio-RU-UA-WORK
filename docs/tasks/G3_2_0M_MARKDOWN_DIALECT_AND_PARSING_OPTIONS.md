# Markdown dialect and parsing options

V2 emits bytes, V3 checks structure, V4 checks source correspondence and V7 checks the fetched artifact. The original K packet shows why these steps need separate evidence. A readable table can still contain the wrong status. A quoted diagnostic can be legitimate while the same spelling occupying a required row is evidence of incomplete rendering.

| Option | Reproducibility and ambiguity | Dependencies, Windows and CPU | Portability and backward compatibility | Maintenance and visibility | Trust boundary and prerequisites |
|---|---|---|---|---|---|
| M-PARSE-A closed subset | Reproducible only with documented grammar and unsupported constructs | Future minimal parser or manual subset check, tested on Windows and other hosts; CPU-only design feasible | Narrow subset travels as text; older packets may exceed it | Grammar maintenance and explicit unsupported diagnostics | Bound emitted bytes to grammar revision; require paired fixtures and evidence of rejection boundaries |
| M-PARSE-B named dialect/version/extensions | Reproduce only with pinned version, extensions and normalization choices | Candidate engine dependencies require separate Windows and portability evidence; CPU-only is a requirement to verify | Wider notation can aid old packets, with version drift risk | Engine updates and extension tests; expose dialect-dependent results | Separate rendering from validation; require versioned grammar, independent parser agreement and escaped-delimiter evidence |
| M-PARSE-C evidence manifest and Markdown rendering | Structured fields can strengthen reproducibility; generated Markdown remains a second representation | Future schema and serializers, with CPU-only and Windows round-trip evidence | Dual formats add portability work; historical imports need scoped treatment | Maintain two forms and show divergences explicitly | Neither file confers authority; require manifest-to-row mapping and fetched-render verification |
| M-PARSE-D defer selection | Manual judgments need written observations and independent replay | Ordinary text inspection can be CPU-only; review line endings and terminal rendering on Windows | Broad readability with limited repeatability of judgments | Review effort grows with packet size; record ambiguous constructs | Use exact object bytes and cite lines; defer automatic conclusions pending owner selection |

| Construct | Documentary question and needed evidence |
|---|---|
| ATX and duplicate headings | Compare heading level, section identity and occurrences. Require a specimen with the same title in two sections. |
| Table and separator | Compare header, separator and body independently. Test the distinction between an optional empty table and a required empty or malformed register. |
| Escaped pipe, inline code and backslashes | Different grammars may tokenize the same text differently. Compare cell boundaries before interpreting IDs, including odd/even escape contexts. |
| Fences and nested-looking fences | Record opening/closing delimiters and code-region boundaries. Compare literal table examples with actual section tables. |
| HTML fragments | Determine whether they are literal, rendered or unsupported. Treat active rendering as a separate boundary from documentary extraction. |
| Unicode and normalization | Distinguish byte identity, scalar equality and display similarity. No normalization rule is selected. |
| CRLF, LF and BOM | Pin complete bytes first. Independently study line splitting and marker handling without changing Git object identity. |
| Whitespace and multiline cells | Separate visual layout from cell content and same-row continuation. Compare trim and preserve interpretations. |
| Repeated IDs and missing or extra cells | Count raw rows before indexing; compare scoped identity and expected column membership. |
| Diagnostic strings | Compare quoted examples such as `System.String[]` with standalone row-block placeholders and scope the detection to actual emitted structure. |
| Valid syntax, wrong data | Compare complete status and dependency cells against applicable authority. A syntax pass supplies no authority verdict. |

All four options remain open. No library, dialect, extension list or accepted grammar is selected.
