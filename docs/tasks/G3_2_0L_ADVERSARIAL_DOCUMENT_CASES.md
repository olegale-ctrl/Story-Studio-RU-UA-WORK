# Adversarial documentary cases

These synthetic plans have no execution or conformance result. Proposed classifications are conditional on acquiring the listed evidence.

## L-C001 — Nested PowerShell string array

- Setup and failure. Type name occupies a required row block.
- Detection and classification. V3, GENERATION_DEFECT.
- Required evidence. Compare emitted bytes with expected rows.
- False-positive or false-negative risk. Quoted discussion could be mistaken for a placeholder.
- Proposed response. Repair emission and reparse.
- **NOT_RUN**

## L-C002 — Nested PowerShell object array

- Setup and failure. Multiple row blocks become one type name apiece.
- Detection and classification. V3, GENERATION_DEFECT.
- Required evidence. Exact rendered lines and source row counts.
- False-positive or false-negative risk. Checking input object count misses defect.
- Proposed response. Repair emission and reparse.
- **NOT_RUN**

## L-C003 — Empty rendered table

- Setup and failure. Required separator has no body.
- Detection and classification. V3, INCOMPLETE_RENDERING.
- Required evidence. Complete artifact and required cardinality.
- False-positive or false-negative risk. Optional empty tables may be legitimate.
- Proposed response. Block required-table claim.
- **NOT_RUN**

## L-C004 — Correct source count, missing rendered rows

- Setup and failure. Extracted count agrees while emitted IDs are absent.
- Detection and classification. V4, FALSE_POSITIVE_CHECK.
- Required evidence. Compare parsed ID sets.
- False-positive or false-negative risk. Count-only checks miss substitutions.
- Proposed response. Repair and compare all rows.
- **NOT_RUN**

## L-C005 — Duplicate row IDs

- Setup and failure. A repeated ID masks another record.
- Detection and classification. V3, INCOMPLETE_RENDERING.
- Required evidence. Parse before indexing.
- False-positive or false-negative risk. Names in distinct scopes can legitimately repeat.
- Proposed response. Report duplicate in its table.
- **NOT_RUN**

## L-C006 — Missing row IDs

- Setup and failure. A required record has no rendered counterpart.
- Detection and classification. V4, INCOMPLETE_RENDERING.
- Required evidence. Expected and actual ID sets.
- False-positive or false-negative risk. Wrong source scope overstates omissions.
- Proposed response. Recheck source scope and repair.
- **NOT_RUN**

## L-C007 — Wrong decision status

- Setup and failure. Rendered status differs from scoped authority.
- Detection and classification. V5, UNAUTHORIZED_SCOPE_CHANGE.
- Required evidence. Pin decision and applicable status.
- False-positive or false-negative risk. Historical status can be valid in its original setting.
- Proposed response. Withhold approval claim.
- **NOT_RUN**

## L-C008 — Correct IDs, incorrect dependencies

- Setup and failure. Known IDs carry different edges.
- Detection and classification. V4, SOURCE_DATA_DEFECT.
- Required evidence. Compare full adjacency with pinned sources.
- False-positive or false-negative risk. Count-only check misses edge swap.
- Proposed response. Locate source or rendering discrepancy. EXPECTED_RESULT_OPEN until cause, dialect or scope is established.
- **NOT_RUN**

## L-C009 — Cyclic dependency graph

- Setup and failure. Proposed prerequisites form a cycle.
- Detection and classification. V5, CONTRACT_AMBIGUITY.
- Required evidence. Complete graph and cycle path.
- False-positive or false-negative risk. External gates may be confused with local nodes.
- Proposed response. Stop affected graph conclusion. EXPECTED_RESULT_OPEN until cause, dialect or scope is established.
- **NOT_RUN**

## L-C010 — Unknown dependency target

- Setup and failure. An edge points to an undeclared node.
- Detection and classification. V5, EVIDENCE_GAP.
- Required evidence. Exact edge and node inventory.
- False-positive or false-negative risk. Omitted external scope may look unresolved.
- Proposed response. Investigate scope and require provenance.
- **NOT_RUN**

## L-C011 — Missing Markdown separator

- Setup and failure. Table-shaped lines have no divider.
- Detection and classification. V3, INCOMPLETE_RENDERING.
- Required evidence. Rendered block boundaries.
- False-positive or false-negative risk. Code or prose may resemble a table.
- Proposed response. Report required table absent.
- **NOT_RUN**

## L-C012 — Incorrect cell count

- Setup and failure. A row exceeds its header width.
- Detection and classification. V3, INCOMPLETE_RENDERING.
- Required evidence. Dialect-aware cell boundaries.
- False-positive or false-negative risk. Naive splitting misreads escapes.
- Proposed response. Reparse or repair.
- **NOT_RUN**

## L-C013 — Escaped pipe

- Setup and failure. A literal delimiter may be counted as a column.
- Detection and classification. V3, CONTRACT_AMBIGUITY.
- Required evidence. Selected dialect and paired interpretations.
- False-positive or false-negative risk. Overcounts columns.
- Proposed response. Defer dialect-specific outcome. EXPECTED_RESULT_OPEN until cause, dialect or scope is established.
- **NOT_RUN**

## L-C014 — Embedded newline

- Setup and failure. A field may span physical lines.
- Detection and classification. V3, CONTRACT_AMBIGUITY.
- Required evidence. Byte boundaries and supported syntax.
- False-positive or false-negative risk. Parser may absorb adjacent rows.
- Proposed response. Defer multiline disposition. EXPECTED_RESULT_OPEN until cause, dialect or scope is established.
- **NOT_RUN**

## L-C015 — Table-like code block

- Setup and failure. Fence contains apparent required rows.
- Detection and classification. V3, FALSE_POSITIVE_CHECK.
- Required evidence. Fence-aware structural evidence.
- False-positive or false-negative risk. Regex may count non-table text.
- Proposed response. Require real table outside fence.
- **NOT_RUN**

## L-C016 — Missing or duplicate heading

- Setup and failure. Required section absent or ambiguous.
- Detection and classification. V3, INCOMPLETE_RENDERING.
- Required evidence. Heading inventory in document context.
- False-positive or false-negative risk. Quoted heading may be mistaken for section.
- Proposed response. Repair heading structure.
- **NOT_RUN**

## L-C017 — Stale source blob

- Setup and failure. Source bytes from earlier revision used.
- Detection and classification. V0, STALE_ARTIFACT.
- Required evidence. Commit, path and both Git IDs.
- False-positive or false-negative risk. Old byte-identical content can validly recur.
- Proposed response. Re-pin exact source.
- **NOT_RUN**

## L-C018 — Source commit mismatch

- Setup and failure. A different commit supplies expected values.
- Detection and classification. V0, IDENTITY_MISMATCH.
- Required evidence. Full expected and observed commit IDs.
- False-positive or false-negative risk. Abbreviations can conceal mismatch.
- Proposed response. STOP.
- **NOT_RUN**

## L-C019 — Candidate parent mismatch

- Setup and failure. Candidate starts on different base.
- Detection and classification. V6, IDENTITY_MISMATCH.
- Required evidence. Commit parent object and pinned base.
- False-positive or false-negative risk. Tree equality can mask ancestry difference.
- Proposed response. STOP.
- **NOT_RUN**

## L-C020 — Candidate tree mismatch

- Setup and failure. Candidate Git tree differs from expectation.
- Detection and classification. V6, IDENTITY_MISMATCH.
- Required evidence. Actual commit and tree IDs.
- False-positive or false-negative risk. Worktree checks can pass against wrong bytes.
- Proposed response. STOP.
- **NOT_RUN**

## L-C021 — Unapproved extra file

- Setup and failure. Candidate adds an extra path.
- Detection and classification. V6, UNAUTHORIZED_SCOPE_CHANGE.
- Required evidence. Complete recursive path diff.
- False-positive or false-negative risk. Narrow path filtering hides extra entry.
- Proposed response. STOP.
- **NOT_RUN**

## L-C022 — Modified historical file

- Setup and failure. An old path retains its name but changes blob.
- Detection and classification. V6, UNAUTHORIZED_SCOPE_CHANGE.
- Required evidence. Compare complete old entry map.
- False-positive or false-negative risk. File counts stay constant.
- Proposed response. STOP.
- **NOT_RUN**

## L-C023 — Wrong file mode

- Setup and failure. Added Markdown has executable mode.
- Detection and classification. V6, UNAUTHORIZED_SCOPE_CHANGE.
- Required evidence. Git tree mode evidence.
- False-positive or false-negative risk. Filesystem view can conceal Git mode.
- Proposed response. STOP.
- **NOT_RUN**

## L-C024 — Self-hash cycle

- Setup and failure. Packet tries to include its own final hash.
- Detection and classification. V8, SELF_HASH_CYCLE.
- Required evidence. Identify the self-reference and the authorized external slot.
- False-positive or false-negative risk. Sibling pins could be wrongly rejected.
- Proposed response. Use external self-hash.
- **NOT_RUN**

## L-C025 — Incorrect sibling SHA

- Setup and failure. Packet pin differs from actual sibling object.
- Detection and classification. V6, IDENTITY_MISMATCH.
- Required evidence. Parsed sibling table and tree entries.
- False-positive or false-negative risk. Working copy may have a different hash.
- Proposed response. STOP until reconciled.
- **NOT_RUN**

## L-C026 — Local versus published discrepancy

- Setup and failure. Local render passes while fetched blob differs.
- Detection and classification. V7, IDENTITY_MISMATCH.
- Required evidence. Complete local and remote identities.
- False-positive or false-negative risk. Local success presented as publication evidence.
- Proposed response. Inspect fetched packet.
- **NOT_RUN**

## L-C027 — Remote branch moved

- Setup and failure. Ref changed after earlier check.
- Detection and classification. V7, STALE_ARTIFACT.
- Required evidence. Timestamped ref observations.
- False-positive or false-negative risk. Prior review remains valid for old immutable object.
- Proposed response. Re-fetch or report exact reviewed head only.
- **NOT_RUN**

## L-C028 — Truncated source retrieval

- Setup and failure. Transport supplies partial content with apparent success.
- Detection and classification. V1, EVIDENCE_GAP.
- Required evidence. Complete object acquisition and retrieval limits.
- False-positive or false-negative risk. Exit zero mistaken for completeness.
- Proposed response. Acquire exact bytes or withhold claims.
- **NOT_RUN**

## L-C029 — Contradictory source statuses

- Setup and failure. Two statuses appear applicable.
- Detection and classification. V5, CONTRACT_AMBIGUITY.
- Required evidence. Pin conflicting passages and scope chronology.
- False-positive or false-negative risk. Automatically choosing latest can overwrite legitimate scope.
- Proposed response. STOP affected conclusion. EXPECTED_RESULT_OPEN until cause, dialect or scope is established.
- **NOT_RUN**

## L-C030 — Competing authority for one row

- Setup and failure. Two sources assert ownership.
- Detection and classification. V1, CONTRACT_AMBIGUITY.
- Required evidence. Scoped authorization for each candidate.
- False-positive or false-negative risk. Registry index mistaken for normative source.
- Proposed response. Escalate unresolved authority. EXPECTED_RESULT_OPEN until cause, dialect or scope is established.
- **NOT_RUN**

## L-C031 — NOT_RUN reported as passed

- Setup and failure. A planned scenario is summarized as successful.
- Detection and classification. V8, FALSE_POSITIVE_CHECK.
- Required evidence. Compare execution trace with reported status.
- False-positive or false-negative risk. Pure document checks may be conflated with execution.
- Proposed response. Withdraw success claim.
- **NOT_RUN**

## L-C032 — Unexecuted check given exit zero

- Setup and failure. Exit code lacks command observation.
- Detection and classification. V8, EVIDENCE_GAP.
- Required evidence. Actual invocation trace.
- False-positive or false-negative risk. A proposed outcome may resemble result.
- Proposed response. Record NOT_RUN without a code.
- **NOT_RUN**

## L-C033 — Invented approval

- Setup and failure. Generator promotes a proposal.
- Detection and classification. V5, UNAUTHORIZED_SCOPE_CHANGE.
- Required evidence. Explicit owner scope and original status.
- False-positive or false-negative risk. Approval words in explanatory text may be misread.
- Proposed response. Restore status and disclose.
- **NOT_RUN**

## L-C034 — Valid Markdown with incorrect rows

- Setup and failure. All cells parse but facts differ.
- Detection and classification. V4, GENERATION_DEFECT.
- Required evidence. Cell-level comparison against pinned authority.
- False-positive or false-negative risk. Syntax-only validation passes.
- Proposed response. Identify divergence and repair.
- **NOT_RUN**

## L-C035 — Historical accepted packet with defect

- Setup and failure. Accepted artifact has missing rendered content.
- Detection and classification. V3, INCOMPLETE_RENDERING.
- Required evidence. Immutable historical blob and its own applicable scope.
- False-positive or false-negative risk. Documentary acceptance may be misread as blanket correctness.
- Proposed response. Record observation without changing historical approval.
- **NOT_RUN**

## L-C036 — Malformed final output receives pass

- Setup and failure. Published structure violates a claimed predicate.
- Detection and classification. V7, FALSE_POSITIVE_CHECK.
- Required evidence. Fetched blob, pass trace and counterexample.
- False-positive or false-negative risk. Source success misreported as artifact success.
- Proposed response. Block handoff and reverify.
- **NOT_RUN**
