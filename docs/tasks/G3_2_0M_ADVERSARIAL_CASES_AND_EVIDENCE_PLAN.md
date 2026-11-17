# Adversarial cases and evidence plan

All cases are synthetic plans. Evidence requirements and interpretations are proposed.

## M-C001 — Valid approval row

- Synthetic setup. Dossier recommendation presents valid approval row in a synthetic packet.
- Expected ambiguity or failure. Recommendation copied as approval.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. L-D02/A unapproved.
- Open owner decision. Authority mapping.
- Required future evidence. Compare status with owner scope.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C002 — Immutable pin

- Synthetic setup. Historical index presents immutable pin in a synthetic packet.
- Expected ambiguity or failure. Identity mistaken for authority.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Decision-level authority unselected.
- Open owner decision. Authority granularity.
- Required future evidence. Pin bytes and authorization separately.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D03. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C003 — Later one-field amendment

- Synthetic setup. Explicit limited owner statement presents later one-field amendment in a synthetic packet.
- Expected ambiguity or failure. Partial change applied to whole row.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Named field only.
- Open owner decision. Supersession granularity.
- Required future evidence. Compare both versions and changed field.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C004 — Conflicting status rows

- Synthetic setup. Two plausible sources presents conflicting status rows in a synthetic packet.
- Expected ambiguity or failure. Newest selected silently.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No precedence approved.
- Open owner decision. Conflict handling.
- Required future evidence. Cite both scopes and chronology.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D03. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C005 — Quoted historical approval

- Synthetic setup. Historical owner record presents quoted historical approval in a synthetic packet.
- Expected ambiguity or failure. Quote read as present decision.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Original scope only.
- Open owner decision. Historical status.
- Required future evidence. Record quote boundaries and provenance.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C006 — Fenced register

- Synthetic setup. Example labeled as source presents fenced register in a synthetic packet.
- Expected ambiguity or failure. Fence contents become live rows.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No example authority.
- Open owner decision. Fence model.
- Required future evidence. Inspect delimiter boundaries.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C007 — Published status differs

- Synthetic setup. Expected source register presents published status differs in a synthetic packet.
- Expected ambiguity or failure. Local pass substituted for fetched data.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Published verification research only.
- Open owner decision. Artifact binding.
- Required future evidence. Exact local and fetched blob comparison.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. Any live retrieval or ref claim requires separate provider observations.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C008 — Moving branch

- Synthetic setup. Mutable branch alias presents moving branch in a synthetic packet.
- Expected ambiguity or failure. Ref changes between reads.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Exact source pin required.
- Open owner decision. Currentness evidence.
- Required future evidence. Record immutable commits for each observation.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. Any live retrieval or ref claim requires separate provider observations.
- Proposed disposition. L-D03. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C009 — Complete source with no authority

- Synthetic setup. Unattributed assertion presents complete source with no authority in a synthetic packet.
- Expected ambiguity or failure. Completeness treated as provenance.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No delegation approved.
- Open owner decision. Missing authority.
- Required future evidence. Record complete object and authority gap.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D03. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C010 — Duplicate ATX heading

- Synthetic setup. Both sections claim same register presents duplicate atx heading in a synthetic packet.
- Expected ambiguity or failure. First heading wins.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Scope belongs to explicit record.
- Open owner decision. Heading identity.
- Required future evidence. Inspect section ancestry and occurrence.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C011 — Empty table

- Synthetic setup. Expected authoritative register presents empty table in a synthetic packet.
- Expected ambiguity or failure. Header mistaken for full table.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Required rows must be evidenced.
- Open owner decision. Empty register grammar.
- Required future evidence. Check declared cardinality and actual body.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C012 — Escaped pipe

- Synthetic setup. Pinned row prose presents escaped pipe in a synthetic packet.
- Expected ambiguity or failure. Delimiter split shifts status cell.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No parser approved.
- Open owner decision. Delimiter grammar.
- Required future evidence. Dialect-labeled column boundaries.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C013 — Inline code

- Synthetic setup. Diagnostic paragraph presents inline code in a synthetic packet.
- Expected ambiguity or failure. Literal token classified as unresolved placeholder.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Historical evidence only.
- Open owner decision. Placeholder classification.
- Required future evidence. Compare actual row location and code span.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C014 — Backslash pairs

- Synthetic setup. Claimed Markdown escaping presents backslash pairs in a synthetic packet.
- Expected ambiguity or failure. Different escape parity changes cells.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Dialect open.
- Open owner decision. Backslash model.
- Required future evidence. Pin paired spellings and parse witnesses.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C015 — Nested-looking fences

- Synthetic setup. Historical specimen presents nested-looking fences in a synthetic packet.
- Expected ambiguity or failure. Wrong closing fence changes boundaries.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Example has no status authority.
- Open owner decision. Fence scope.
- Required future evidence. Inspect fence length and delimiter context.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C016 — HTML fragment

- Synthetic setup. Rendered status label presents html fragment in a synthetic packet.
- Expected ambiguity or failure. Visible output diverges from text.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Rendering model open.
- Open owner decision. HTML treatment.
- Required future evidence. Separate source and rendered views.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C017 — Unicode lookalike ID

- Synthetic setup. Claimed decision key presents unicode lookalike id in a synthetic packet.
- Expected ambiguity or failure. Display similarity used as identity.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No normalization approved.
- Open owner decision. Unicode identity.
- Required future evidence. Pin bytes and compare scalars separately.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C018 — CRLF or LF

- Synthetic setup. Same claimed document presents crlf or lf in a synthetic packet.
- Expected ambiguity or failure. Normalized copy substituted for Git blob.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Object identity exact.
- Open owner decision. Newline policy.
- Required future evidence. Record raw hash and line boundaries.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C019 — BOM marker

- Synthetic setup. Claimed optional header presents bom marker in a synthetic packet.
- Expected ambiguity or failure. Marker stripped before pinning.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Decode rule open.
- Open owner decision. BOM handling.
- Required future evidence. Verify raw bytes and compare decoding interpretations.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C020 — Whitespace and multiline cell

- Synthetic setup. Claimed continued status presents whitespace and multiline cell in a synthetic packet.
- Expected ambiguity or failure. Unrelated line absorbed.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No trimming or continuation selected.
- Open owner decision. Continuation grammar.
- Required future evidence. Document source lines and alternatives.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C021 — Duplicate row ID

- Synthetic setup. One source rendered twice presents duplicate row id in a synthetic packet.
- Expected ambiguity or failure. Overwrite masks discrepancy.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Decision identity scoped.
- Open owner decision. Row identity.
- Required future evidence. Count occurrences before indexing.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. both. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C022 — Extra cell

- Synthetic setup. Indexed row presents extra cell in a synthetic packet.
- Expected ambiguity or failure. Status shifts one column.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Source mapping open.
- Open owner decision. Cell cardinality.
- Required future evidence. Compare schema and exact cells.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D02. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C023 — Cross-project decision

- Synthetic setup. Foreign owner statement presents cross-project decision in a synthetic packet.
- Expected ambiguity or failure. Shared spelling transfers authorization.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. No delegation.
- Open owner decision. Cross-project provenance.
- Required future evidence. Evidence of explicit delegation.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D03. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C024 — Revoked decision

- Synthetic setup. Old packet still quotes approval presents revoked decision in a synthetic packet.
- Expected ambiguity or failure. Old decision treated as current.
- Candidate interpretation. Keep the emitted record and source authority rationale distinct under M-AUTH-A or defer under M-AUTH-D.
- Inherited constraint. Revocation only if explicitly scoped.
- Open owner decision. Revocation and history.
- Required future evidence. Pin both statements and exact effective scope.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. L-D03. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C025 — Missing cells

- Synthetic setup. A row loses its final status cell.
- Expected ambiguity or failure. An adjacent token may be taken as status.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D02 remains unapproved.
- Open owner decision. Cell count.
- Required future evidence. Compare exact header and row widths.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C026 — Extra separator

- Synthetic setup. An alignment line appears inside a body.
- Expected ambiguity or failure. It may be read as a new table or a row.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D02 remains unapproved.
- Open owner decision. Separator grammar.
- Required future evidence. Pin line boundaries and expected table identity.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C027 — ATX closing markers

- Synthetic setup. A heading includes trailing hashes.
- Expected ambiguity or failure. A title match may depend on dialect.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D02 remains unapproved.
- Open owner decision. Heading grammar.
- Required future evidence. Compare parsing witnesses for the same bytes.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C028 — Unterminated fence

- Synthetic setup. An example opens before the required register.
- Expected ambiguity or failure. The live register may be swallowed.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D02 remains unapproved.
- Open owner decision. Unsupported syntax.
- Required future evidence. Identify the last unambiguous line.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C029 — Optional empty table

- Synthetic setup. An optional index has no records.
- Expected ambiguity or failure. A blanket nonempty rule rejects valid absence.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D02 remains unapproved.
- Open owner decision. Cardinality.
- Required future evidence. Identify scoped cardinality evidence.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C030 — Valid Markdown wrong dependency

- Synthetic setup. Two valid IDs have swapped prerequisite cells.
- Expected ambiguity or failure. Structural success hides semantic divergence.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Row binding.
- Required future evidence. Compare exact edge sets.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C031 — Repeated identical assertion

- Synthetic setup. Two pinned sources repeat the same status.
- Expected ambiguity or failure. Agreement may be treated as independent authority.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Duplicate provenance.
- Required future evidence. Trace common origin and scope.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C032 — Historical original vs repair

- Synthetic setup. Two Git commits hold original and repaired K packets.
- Expected ambiguity or failure. Repair may be mistaken for new approval.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Historical provenance.
- Required future evidence. Compare changed rows and owner record.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C033 — Stale authority manifest

- Synthetic setup. A complete manifest pins an old scoped statement.
- Expected ambiguity or failure. Completeness may conceal a later amendment.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Manifest currentness.
- Required future evidence. Document authority timeline.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C034 — Unavailable pinned blob

- Synthetic setup. The declared source cannot be fetched.
- Expected ambiguity or failure. A summary may be substituted silently.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Missing source.
- Required future evidence. Obtain complete original or record evidence gap.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. Any live retrieval or ref claim requires separate provider observations.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C035 — Truncated source output

- Synthetic setup. A transport displays only first rows.
- Expected ambiguity or failure. Partial retrieval appears complete.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Retrieval completeness.
- Required future evidence. Compare retrieved bytes to Git object.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. Any live retrieval or ref claim requires separate provider observations.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C036 — Manifest and Markdown mismatch

- Synthetic setup. Structured status differs from published row.
- Expected ambiguity or failure. Readers may assume generated render inherits truth.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Dual artifact binding.
- Required future evidence. Compare both forms on exact revisions.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C037 — Lookalike owner title

- Synthetic setup. A report bears an owner-like heading.
- Expected ambiguity or failure. Title may be promoted into authorization.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Role evidence.
- Required future evidence. Locate separate explicit owner decision.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C038 — Stale remote packet

- Synthetic setup. A reviewed commit remains available after branch relocation.
- Expected ambiguity or failure. Immutable review is mistaken for current branch evidence.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Publication currentness.
- Required future evidence. Pin timestamped ref and candidate.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. Any live retrieval or ref claim requires separate provider observations.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C039 — Approval scope wording

- Synthetic setup. A scoped research approval shares an identifier with a binding contract.
- Expected ambiguity or failure. Approval may be expanded to implementation.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Scope correspondence.
- Required future evidence. Compare exact scope clauses.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## M-C040 — Cross-project revocation

- Synthetic setup. One repository changes a similarly named decision.
- Expected ambiguity or failure. A same-spelling key may be assumed revoked elsewhere.
- Candidate interpretation. Preserve complete exact bytes and record the competing readings before resolving status or structure.
- Inherited constraint. L-D01/A authorizes only documentary research.
- Open owner decision. Project scope.
- Required future evidence. Trace explicit delegation and affected decision.
- Evidence boundary. Offline evidence can assess pinned bytes and claims. No live provider or implementation behavior follows from that comparison.
- Proposed disposition. Defer the affected claim pending evidence. EXPECTED_RESULT_OPEN.
- **NOT_RUN**
