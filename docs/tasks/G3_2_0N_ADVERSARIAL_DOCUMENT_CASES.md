# Adversarial documentary cases

All cases are proposals with no execution evidence. Candidate interpretations depend on future owner decisions.

## N-C001 — Required heading

- Setup. Consider a synthetic acceptance packet containing required heading and a separately supplied source.
- Expected ambiguity or failure. Repeated title masks the required section.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D02.
- Required future evidence. Compare heading hierarchy and scope.
- False-positive/false-negative risk. Repeated title masks the required section. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C002 — Duplicate heading

- Setup. Consider a synthetic acceptance packet containing duplicate heading and a separately supplied source.
- Expected ambiguity or failure. Same title at same level leaves register ambiguous.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D02.
- Required future evidence. Check occurrence and parent section.
- False-positive/false-negative risk. Same title at same level leaves register ambiguous. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C003 — Missing separator

- Setup. Consider a synthetic acceptance packet containing missing separator and a separately supplied source.
- Expected ambiguity or failure. Row-like prose mistaken for a table.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Check header and separator shape.
- False-positive/false-negative risk. Row-like prose mistaken for a table. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C004 — Extra separator

- Setup. Consider a synthetic acceptance packet containing extra separator and a separately supplied source.
- Expected ambiguity or failure. A separator inside data changes row boundaries.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Inspect exact rendered block.
- False-positive/false-negative risk. A separator inside data changes row boundaries. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C005 — Escaped pipe

- Setup. Consider a synthetic acceptance packet containing escaped pipe and a separately supplied source.
- Expected ambiguity or failure. Delimiter interpreted as field boundary.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Compare escape-aware column observations.
- False-positive/false-negative risk. Delimiter interpreted as field boundary. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C006 — Pipe in code span

- Setup. Consider a synthetic acceptance packet containing pipe in code span and a separately supplied source.
- Expected ambiguity or failure. Literal content shifts status column.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Compare candidate inline code semantics.
- False-positive/false-negative risk. Literal content shifts status column. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C007 — Backslash parity

- Setup. Consider a synthetic acceptance packet containing backslash parity and a separately supplied source.
- Expected ambiguity or failure. Escape introducer and literal slashes confused.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Pin exact slash counts and boundary interpretations.
- False-positive/false-negative risk. Escape introducer and literal slashes confused. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C008 — Fenced register

- Setup. Consider a synthetic acceptance packet containing fenced register and a separately supplied source.
- Expected ambiguity or failure. Example counted as active evidence.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D05.
- Required future evidence. Pin opening and closing delimiters.
- False-positive/false-negative risk. Example counted as active evidence. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C009 — Nested-looking fence

- Setup. Consider a synthetic acceptance packet containing nested-looking fence and a separately supplied source.
- Expected ambiguity or failure. Closing delimiter chosen at wrong depth.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D05.
- Required future evidence. Compare delimiter length and context.
- False-positive/false-negative risk. Closing delimiter chosen at wrong depth. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C010 — HTML fragment

- Setup. Consider a synthetic acceptance packet containing html fragment and a separately supplied source.
- Expected ambiguity or failure. Visible and extracted statuses disagree.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D05.
- Required future evidence. Separate rendered view and source object.
- False-positive/false-negative risk. Visible and extracted statuses disagree. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C011 — Unicode confusable

- Setup. Consider a synthetic acceptance packet containing unicode confusable and a separately supplied source.
- Expected ambiguity or failure. Display similarity merges IDs.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D04.
- Required future evidence. Compare code points and pinned bytes.
- False-positive/false-negative risk. Display similarity merges IDs. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C012 — Unicode normalization

- Setup. Consider a synthetic acceptance packet containing unicode normalization and a separately supplied source.
- Expected ambiguity or failure. Canonical-equivalent forms merged without a rule.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D04.
- Required future evidence. Record raw and scalar identities independently.
- False-positive/false-negative risk. Canonical-equivalent forms merged without a rule. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C013 — Initial BOM

- Setup. Consider a synthetic acceptance packet containing initial bom and a separately supplied source.
- Expected ambiguity or failure. Marker stripping masks byte difference.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D04.
- Required future evidence. Verify complete blob before decode.
- False-positive/false-negative risk. Marker stripping masks byte difference. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C014 — CRLF versus LF

- Setup. Consider a synthetic acceptance packet containing crlf versus lf and a separately supplied source.
- Expected ambiguity or failure. Normalized copy mistaken for exact Git bytes.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D04.
- Required future evidence. Compare both byte streams and line structure.
- False-positive/false-negative risk. Normalized copy mistaken for exact Git bytes. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C015 — Whitespace

- Setup. Consider a synthetic acceptance packet containing whitespace and a separately supplied source.
- Expected ambiguity or failure. Trimming changes cell content.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Compare structural margins with payload.
- False-positive/false-negative risk. Trimming changes cell content. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C016 — Multiline cell

- Setup. Consider a synthetic acceptance packet containing multiline cell and a separately supplied source.
- Expected ambiguity or failure. Continuation consumes next decision.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Review explicit scope of continuation.
- False-positive/false-negative risk. Continuation consumes next decision. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C017 — Empty required table

- Setup. Consider a synthetic acceptance packet containing empty required table and a separately supplied source.
- Expected ambiguity or failure. Header mistaken for evidence.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Confirm required body count.
- False-positive/false-negative risk. Header mistaken for evidence. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C018 — Missing cell

- Setup. Consider a synthetic acceptance packet containing missing cell and a separately supplied source.
- Expected ambiguity or failure. Status inferred from adjacent text.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Compare header and row widths.
- False-positive/false-negative risk. Status inferred from adjacent text. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C019 — Extra cell

- Setup. Consider a synthetic acceptance packet containing extra cell and a separately supplied source.
- Expected ambiguity or failure. Status shifted by unmodeled cell.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D03.
- Required future evidence. Verify exact field bindings.
- False-positive/false-negative risk. Status shifted by unmodeled cell. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C020 — Duplicate row ID

- Setup. Consider a synthetic acceptance packet containing duplicate row id and a separately supplied source.
- Expected ambiguity or failure. Later occurrence overwrites first.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Count before indexing and compare scopes.
- False-positive/false-negative risk. Later occurrence overwrites first. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C021 — Quoted diagnostic

- Setup. Consider a synthetic acceptance packet containing quoted diagnostic and a separately supplied source.
- Expected ambiguity or failure. Historical array type label flagged as active placeholder.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Synthetic register author. Specific authority unknown.
- Open decision. N-D05.
- Required future evidence. Check quote context and row location.
- False-positive/false-negative risk. Historical array type label flagged as active placeholder. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C022 — Standalone diagnostic

- Setup. Inspect the pinned original K and FIX-1 packets.
- Expected ambiguity or failure. Required register contains type name instead of rows.
- Candidate interpretation. Compare N-MD-A with N-MD-B using the exact emitted row boundaries.
- Authority assumption. Pinned K source and repair evidence. K repair grants no new scope.
- Open decision. N-D09.
- Required future evidence. Compare original K and FIX-1.
- False-positive/false-negative risk. Required register contains type name instead of rows. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C023 — Wrong approval in valid table

- Setup. Consider a synthetic acceptance packet containing wrong approval in valid table and a separately supplied source.
- Expected ambiguity or failure. Recommendation promoted to owner approval.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Dossier or owner instruction as claimed. M-D01/A and M-D05/A are documentary only.
- Open decision. N-D07.
- Required future evidence. Compare current owner scope and historical dossier.
- False-positive/false-negative risk. Recommendation promoted to owner approval. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C024 — Authorized source malformed in render

- Setup. Consider a synthetic acceptance packet containing authorized source malformed in render and a separately supplied source.
- Expected ambiguity or failure. Correct source treated as proof of complete output.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Pinned K source and repair evidence. K repair grants no new scope.
- Open decision. N-D09.
- Required future evidence. Check exact emitted rows and original decision separately.
- False-positive/false-negative risk. Correct source treated as proof of complete output. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C025 — Limited approval expanded

- Setup. Consider a synthetic acceptance packet containing limited approval expanded and a separately supplied source.
- Expected ambiguity or failure. One documentary direction licenses adjacent implementation.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Dossier or owner instruction as claimed. M-D01/A and M-D05/A are documentary only.
- Open decision. N-D07.
- Required future evidence. Verify exact field and action scope.
- False-positive/false-negative risk. One documentary direction licenses adjacent implementation. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C026 — Partial supersession

- Setup. Consider a synthetic acceptance packet containing partial supersession and a separately supplied source.
- Expected ambiguity or failure. One amended cell changes unrelated cells.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D08.
- Required future evidence. Compare both scoped decisions field by field.
- False-positive/false-negative risk. One amended cell changes unrelated cells. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C027 — Conflicting claims

- Setup. Consider a synthetic acceptance packet containing conflicting claims and a separately supplied source.
- Expected ambiguity or failure. Newer commit chosen with no precedence.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D08.
- Required future evidence. Preserve both exact claims and scope rationales.
- False-positive/false-negative risk. Newer commit chosen with no precedence. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C028 — Unknown source authority

- Setup. Consider a synthetic acceptance packet containing unknown source authority and a separately supplied source.
- Expected ambiguity or failure. Pinned byte identity treated as authorization.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D06.
- Required future evidence. Require independent owner provenance.
- False-positive/false-negative risk. Pinned byte identity treated as authorization. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C029 — Moved Git ref

- Setup. Consider a synthetic acceptance packet containing moved git ref and a separately supplied source.
- Expected ambiguity or failure. Mutable name resolves to different versions.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Pin both ref observations and immutable commits.
- False-positive/false-negative risk. Mutable name resolves to different versions. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C030 — Published blob mismatch

- Setup. Consider a synthetic acceptance packet containing published blob mismatch and a separately supplied source.
- Expected ambiguity or failure. Local artifact pass reused for different remote blob.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Fetch and compare actual Git objects.
- False-positive/false-negative risk. Local artifact pass reused for different remote blob. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C031 — Repeated ID in different family

- Setup. Consider a synthetic acceptance packet containing repeated id in different family and a separately supplied source.
- Expected ambiguity or failure. Same key spelling treated as one decision.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D06.
- Required future evidence. Review family and decision coordinates.
- False-positive/false-negative risk. Same key spelling treated as one decision. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C032 — Historical quote

- Setup. Consider a synthetic acceptance packet containing historical quote and a separately supplied source.
- Expected ambiguity or failure. Past approval read as current scope.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D08.
- Required future evidence. Separate history, effective scope and provenance.
- False-positive/false-negative risk. Past approval read as current scope. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C033 — FIX-1 repair

- Setup. Inspect the pinned original K and FIX-1 packets.
- Expected ambiguity or failure. Restored rows assumed to grant authority.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Pinned K source and repair evidence. K repair grants no new scope.
- Open decision. N-D08.
- Required future evidence. Compare old and corrected packet with original decision sources.
- False-positive/false-negative risk. Restored rows assumed to grant authority. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C034 — Manifest stale

- Setup. Consider a synthetic acceptance packet containing manifest stale and a separately supplied source.
- Expected ambiguity or failure. Complete old manifest conceals later scoped update.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D08.
- Required future evidence. Establish chronology and scoped amendment.
- False-positive/false-negative risk. Complete old manifest conceals later scoped update. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C035 — Broken authority chain

- Setup. Consider a synthetic acceptance packet containing broken authority chain and a separately supplied source.
- Expected ambiguity or failure. Unknown link assumed valid.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D07.
- Required future evidence. Collect every claimed delegation link.
- False-positive/false-negative risk. Unknown link assumed valid. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C036 — Cross-project claim

- Setup. Consider a synthetic acceptance packet containing cross-project claim and a separately supplied source.
- Expected ambiguity or failure. Scope carried into another project.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D06.
- Required future evidence. Require explicit project authority.
- False-positive/false-negative risk. Scope carried into another project. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C037 — Revocation claim

- Setup. Consider a synthetic acceptance packet containing revocation claim and a separately supplied source.
- Expected ambiguity or failure. Revocation expanded beyond named field.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D08.
- Required future evidence. Pin revocation scope and prior decision.
- False-positive/false-negative risk. Revocation expanded beyond named field. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C038 — Unavailable source

- Setup. Consider a synthetic acceptance packet containing unavailable source and a separately supplied source.
- Expected ambiguity or failure. A summary stands in for original.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D06.
- Required future evidence. Retrieve complete source or record gap.
- False-positive/false-negative risk. A summary stands in for original. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C039 — Truncated retrieval

- Setup. Consider a synthetic acceptance packet containing truncated retrieval and a separately supplied source.
- Expected ambiguity or failure. Successful fetch assumed to deliver all source bytes.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Compare complete Git blob and retrieval trace.
- False-positive/false-negative risk. Successful fetch assumed to deliver all source bytes. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C040 — Wrong dependency

- Setup. Consider a synthetic acceptance packet containing wrong dependency and a separately supplied source.
- Expected ambiguity or failure. Table parses while an edge changes.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Compare exact prerequisite sets.
- False-positive/false-negative risk. Table parses while an edge changes. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C041 — Accepted but malformed packet

- Setup. Consider a synthetic acceptance packet containing accepted but malformed packet and a separately supplied source.
- Expected ambiguity or failure. Documentary acceptance treated as comprehensive qualification.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D10.
- Required future evidence. Pin applicable historical acceptance scope.
- False-positive/false-negative risk. Documentary acceptance treated as comprehensive qualification. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C042 — Dual representation disagreement

- Setup. Consider a synthetic acceptance packet containing dual representation disagreement and a separately supplied source.
- Expected ambiguity or failure. Manifest passes while Markdown contradicts it.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Compare same candidate bytes and record IDs.
- False-positive/false-negative risk. Manifest passes while Markdown contradicts it. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C043 — Unexpected optional empty table

- Setup. Consider a synthetic acceptance packet containing unexpected optional empty table and a separately supplied source.
- Expected ambiguity or failure. Optional absence flagged as malformed.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D05.
- Required future evidence. Verify declared cardinality.
- False-positive/false-negative risk. Optional absence flagged as malformed. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C044 — Unterminated fence

- Setup. Consider a synthetic acceptance packet containing unterminated fence and a separately supplied source.
- Expected ambiguity or failure. Real register consumed by example.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D05.
- Required future evidence. Identify last certain structural boundary.
- False-positive/false-negative risk. Real register consumed by example. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C045 — Competing source titles

- Setup. Consider a synthetic acceptance packet containing competing source titles and a separately supplied source.
- Expected ambiguity or failure. Title determines authority.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D07.
- Required future evidence. Trace actual owner statements.
- False-positive/false-negative risk. Title determines authority. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C046 — Markdown valid wrong status

- Setup. Consider a synthetic acceptance packet containing markdown valid wrong status and a separately supplied source.
- Expected ambiguity or failure. Structural pass reported as status evidence.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D09.
- Required future evidence. Compare same row to pinned applicable scope.
- False-positive/false-negative risk. Structural pass reported as status evidence. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C047 — Windows round-trip drift

- Setup. Consider a synthetic acceptance packet containing windows round-trip drift and a separately supplied source.
- Expected ambiguity or failure. Terminal displays same line after byte transformation.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D04.
- Required future evidence. Pin raw bytes across host boundaries.
- False-positive/false-negative risk. Terminal displays same line after byte transformation. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**

## N-C048 — Future conformance claim

- Setup. Consider a synthetic acceptance packet containing future conformance claim and a separately supplied source.
- Expected ambiguity or failure. Unexecuted documentary case treated as pass.
- Candidate interpretation. Compare N-MD-C's rendered record independently of the authority evidence under N-AUTH-A.
- Authority assumption. Supplied provenance claim. Specific authority unknown.
- Open decision. N-D10.
- Required future evidence. Require separate executed evidence.
- False-positive/false-negative risk. Unexecuted documentary case treated as pass. A broad exclusion may discard legitimately scoped records or examples.
- Proposed response. Withhold the affected claim and preserve separate source and rendered observations. EXPECTED_RESULT_OPEN.
- **NOT_RUN**
