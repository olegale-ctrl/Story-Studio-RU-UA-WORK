# Strict Markdown evidence profile

## Candidate document structure

Every entry in this section and the comparison is CANDIDATE — NOT NORMATIVE.

- Require a declared set of headings for identity, sources, registers, actual checks and STOP. Give each register a scoped section path and an explicit table name.
- Consider a header, divider and fixed-width single-line rows with one scoped identifier per record. Preserve duplicates as evidence of ambiguity and withhold the relevant conclusion.
- Distinguish required tables with declared inventory from optional tables. Keep status cells literal and compare them separately to original owner authority.
- Pin raw bytes before any decoding. Study strict UTF-8 as an explicit assumption and keep BOM, normalization and line-ending rules open.
- Document unsupported constructs and preserve bytes for independent review. Defer interpretation when cell or section boundaries are ambiguous.

## Construct comparison

| ID | Construct | Candidate disposition | Reason | Evidence | Ambiguity | False acceptance | False rejection | Historical impact | Open question |
|---|---|---|---|---|---|---|---|---|---|
| O-MD01 | Heading hierarchy | Include explicit section paths — CANDIDATE — NOT NORMATIVE | Prevent sibling collisions | Heading ancestry | Same title in distinct sections | Wrong register selected | Legitimate repeated title rejected | L packet headings are simple | N-02 |
| O-MD02 | Repeated required heading | Exclude ambiguous duplicate — CANDIDATE — NOT NORMATIVE | One register witness per section | Occurrence inventory | Title alone may be insufficient | Second status hidden | Distinct sections collapsed | Historical headings need scoped review | N-02 |
| O-MD03 | ATX closing markers | Defer — CANDIDATE — NOT NORMATIVE | Avoid normalization assumptions | Pinned title and exact spelling | Trailing hashes may be syntax or text | Wrong section matched | Valid alternate heading refused | Unassessed | N-02 |
| O-MD04 | Register identity | Include section and named table — CANDIDATE — NOT NORMATIVE | Keep OP and CM distinct | Section-to-table mapping | Two tables under one heading | Rows mapped to wrong family | Valid nearby table missed | N preserved registers has two tables | N-02 |
| O-MD05 | Header | Include exact column names per candidate register — CANDIDATE — NOT NORMATIVE | Make fields independently reviewable | Header and expected column labels | Editorial synonyms | Approval read from wrong column | Legacy header synonym refused | K headings and headers remain available | N-03 |
| O-MD06 | Separator | Include one explicit single-line divider — CANDIDATE — NOT NORMATIVE | Distinguish table from prose | Header-divider-body evidence | Alignment variants | Prose counted as table | Aligned table refused | K FIX-1 has simple separators | N-03 |
| O-MD07 | Required table body | Include exact nonempty row inventory — CANDIDATE — NOT NORMATIVE | Prevent silent omission | Parsed IDs and source row count | Optional emptiness | Header-only false pass | Legitimate empty optional index refused | Original K lacked four bodies | N-03 |
| O-MD08 | Column cardinality | Include fixed width — CANDIDATE — NOT NORMATIVE | Avoid field displacement | Count cells before indexing | Literal delimiter | Wrong status cell accepted | Rich text rejected | K FIX-1 restored uniform decision rows | N-03 |
| O-MD09 | Duplicate row key | Exclude within register — CANDIDATE — NOT NORMATIVE | Prevent silent overwrite | All raw key occurrences | Same spelling across families | Conflicting row suppressed | Distinct scopes conflated | N local graph has distinct keyed rows | N-03 |
| O-MD10 | Literal status cell | Include explicitly scoped vocabulary — CANDIDATE — NOT NORMATIVE | Make authority comparison possible | Exact row plus owner evidence | Quoted historical label | Recommendation promoted | Legitimate quotation disallowed | N historical N-D01 remains a proposal in its own dossier | N-03 |
| O-MD11 | Escaped pipe | Defer in active tables — CANDIDATE — NOT NORMATIVE | Keep simple delimiter model inspectable | Paired escaped and literal cells | Backslash parity | Cell shift | Valid rich row refused | Possible legacy exception | N-03 |
| O-MD12 | Inline code | Defer in data cells — CANDIDATE — NOT NORMATIVE | A span may contain delimiters | Code-span boundary witness | Inline backtick pairing | Wrong cell extraction | Data citation refused | Historical prose uses inline code | N-03 |
| O-MD13 | Fenced code | Exclude as active register — CANDIDATE — NOT NORMATIVE | Examples lack register authority | Opening and closing lines | Unclosed fence | Synthetic row counted | Live table swallowed | Historical examples require separate inspection | N-05 |
| O-MD14 | Nested-looking fences | Defer interpretation — CANDIDATE — NOT NORMATIVE | Delimiter length can change region | Exact fence lengths | Example may contain fence text | Hidden active content | Legitimate specimen refused | Potential exception | N-05 |
| O-MD15 | HTML fragments | Exclude as active evidence — CANDIDATE — NOT NORMATIVE | Rendered view may diverge | Raw and display evidence | Tag versus literal text | Hidden row accepted | Literal angle text rejected | Unassessed | N-05 |
| O-MD16 | Backslash before text | Defer — CANDIDATE — NOT NORMATIVE | Avoid assumed escape semantics | Exact octets and paired interpretations | Literal versus escape | Altered cell accepted | Valid path refused | Windows examples need separate review | N-03 |
| O-MD17 | Unicode scalar text | Include as documentary content only — CANDIDATE — NOT NORMATIVE | Preserve evidence spelling | Exact bytes and decoded scalars | Confusable glyphs | Wrong identifier matched | Distinct labels collapsed | Historical dossiers contain non-ASCII text | N-04 |
| O-MD18 | BOM | Defer — CANDIDATE — NOT NORMATIVE | Decode and object identity differ | Raw marker and decoder evidence | Marker may be carrier metadata | Wrong object vouched for | Readable artifact rejected | Historical coverage incomplete | N-04 |
| O-MD19 | CRLF and LF | Defer equivalence — CANDIDATE — NOT NORMATIVE | Display identity differs from blob identity | Raw newline bytes and row observations | Editor conversion | Wrong blob accepted | Equivalent visible text refused | Cross-host qualification open | N-04 |
| O-MD20 | Leading or trailing whitespace | Defer trimming — CANDIDATE — NOT NORMATIVE | Margins and data differ | Pinned cell boundaries | Invisible suffix | Wrong identifier merged | Harmless layout rejected | Unassessed | N-03 |
| O-MD21 | Multiline cells | Exclude in strict candidate — CANDIDATE — NOT NORMATIVE | Make record boundary explicit | Physical line and cell evidence | Continuation versus next row | Second decision absorbed | Valid rich cell refused | Possible legacy migration or exception | N-03 |
| O-MD22 | Diagnostic type name | Exclude as standalone active data; permit quoted discussion outside the register candidate — CANDIDATE — NOT NORMATIVE | Retain history while catching missing emission | Line role and expected inventory | Quoted versus standalone | Missing rows accepted | FIX-1 evidence rejected | Both original K and FIX-1 demonstrate distinction | N-05 |

## Pinned historical compatibility

Original K at c038809 has recognizable headings and separators, with four bodies replaced by standalone type names. FIX-1 at 8c7468d restores single-line rows under those headings and quotes the type names as historical evidence. The quotation is outside the affected registers. N's published OP and CM tables illustrate two register identities beneath one broader heading. A literal title-only rule would need a tighter register discriminator. Historic rich prose, inline spans or multiline examples may require a scoped exception outside active registers or a separately approved migration. No historical migration is selected. N's own dossier continues to display historical proposal states even after scoped O authorization. Syntax cannot decide whether a copied state is current. This is a targeted review of pinned examples, with no exhaustive compatibility or parser conformance claim. N-D02–N-D05 remain open.
