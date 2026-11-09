# CODEX TASK — SI-E01.2b.1: pure read-only SI/1 exact resolver and canonical Closure

**Date:** 2026-11-09
**Status:** **BOUNDED HANDOFF ONLY / NOT STARTED**. No PR/merge/release/main.
**Gate:** SI-E01.2a-RESUME plus F1 independently accepted as **PURE_LOCAL_TYPED_RECORDS_ONLY** in `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_INDEPENDENT_ACCEPTANCE.md` @ `a6dd90ec506da737dccffdff2620889c7f4608fd`.

## 1. Exact base and branch, no silent escalation

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-si-e01-2a-f1-independent-acceptance`.
The owner handoff supplies the **exact final remote HEAD SHA** after this task is published. Compare the source branch's remote SHA with that exact SHA before changing anything. STOP if different. No silent fallback to `main`, original RESUME feature, previous blocked branch, or moving HEAD.

Create **new** feature branch:
`feat/story-intelligence-si-e01-2b-1-pure-resolver-closure`

Do not mutate source branches, historical feature branches, accepted docs/contracts, PRs or `main`. Owner forwarding is the execution authorization for **this bounded unit only**; publication here is not permission for SI-E01.2b.2 or SI-E02.

## 2. Binding contracts to read before editing

- Original V1 spec: `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md`.
- Approved R1: `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md`, especially §§1.1–1.3 (all H, payload and nested references; canonical Closure; exact ref conflict; DAG; Run input snapshot), §2 (root semantics), §4.2 (semantic vs audit distinction), and §§5.1–5.3 (Packet export scope).
- Approved R1a: `docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md` (separate creative original run from revision run; previous ancestry).
- Approved R1b: `docs/tasks/STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md` P01–P05 and `docs/tasks/STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md`.
- `docs/tasks/STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md` SI-D01–D10.
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_INDEPENDENT_ACCEPTANCE.md`, the accepted `story_intelligence/{codec_v1.py,model_v1.py,records_v1.py}`, existing tests and literal vectors.

Priority: original → precise R1 → precise R1a → precise R1b. This assignment does **not** revise any contract. If a required exact resolver wire interface is not specified, define a **pure local Python API for the new module only** without changing SI/1 wire/operation contracts, or STOP if the choice would change deterministic hashes or semantics.

## 3. Very narrow implementation goal

Produce a **pure, read-only, closed-bundle exact SIRef resolver and canonical transitive Closure verifier**. The caller supplies a finite, explicit in-memory set of complete SI records and a list of exact SIRef roots; nothing is loaded from workspace, disk, web or protected editorial storage. The resolver must verify byte identity, missing/mismatched refs, unique record identity, transitive ancestry and DAG cycles, and return canonical sorted unique exact SIRef manifest.

Suggested module: `story_intelligence/resolver_v1.py`. Suggested stable API (use these names to avoid inventing another interface):
- `resolve_si_closure(records, roots) -> list[SIRef]`: validate supplied complete records with accepted `validate_si_record`, compute `si_record_ref` for each, validate roots, traverse all **actual SIRefs** from each reachable record's H and typed payload (including nested Known values), and return a detached canonical manifest sorted by `(type,id,revision,sha256)` without modifying caller input. All used records must exist and match exact type/id/revision/content hash.
- `resolve_si_record(records, expected_ref) -> detached complete record`: validate supplied records and expected ref, resolve one exact verified record (no implicit latest), and return detached copy. This does not assert human identity/truth/rights.

If user supplies multiple records claiming same `(type,id,revision)` with different bytes/hashes, fail closed `REF_HASH_MISMATCH` rather than choosing by position. Duplicate identical records may be rejected as noncanonical duplicate bundle (`TYPE`); document chosen strict behavior and test it. Unknown/unreferenced records are not silently accepted as trusted inputs; they may be validated structurally, but only refs in verified closure are returned as closure. No persistent registry or mutable cache.

The **direct SIRef extraction** must follow the approved typed schemas, *not* arbitrary dicts that happen to resemble SIRefs: exactly H.previous, H.origin.run_ref, H.input_refs, and all typed SIRef fields in payload, including nested refs in Known<T>, PortfolioEntry, Chapter, ContextSnapshot, Rating, SelectionScope, PrivacyGrant, FieldGrant, DisplayItem, Omission, BriefReviewState, etc. Do not treat ERefs as SIRef or use source-ref strings inside displayed text to fabricate graph edges. Provenance and prior history edges are in this **audit Closure**, but semantic currentness must not treat them as present active domain inputs.

ERefs are distinct: validate their local shape using existing accepted validators. **No ERef material/hash verification without an explicitly supplied editorial snapshot adapter/contract.** Declare that limitation; no editorial runtime import, no permission to claim an ERef cryptographically verified. Do not invent editorial snapshot bytes or external resolution.

Verify `RunRecord.payload.input_snapshot` is **exactly** the canonical Closure of `semantic_input_refs + ContextSnapshot.active_input_refs + ContextSnapshot.selection_head_refs`, with `RunRecord.H.input_refs` equal to it as already locally enforced; not merely a subset. Crucial: the input snapshot excludes its own RunRecord and its outputs. For each reachable RunRecord, compare its frozen declared snapshot to recomputed closure from the supplied bundle, verifying referenced ancestors and no self/output cycles. Existing `_local` checks are necessary but insufficient. If recomputation creates dependency to a future output/Run itself, fail `DEPENDENCY_CYCLE`. Use only existing R1 `SIValidationError` codes and meaningful paths.

Avoid constructing a self-referential test graph: records with H.origin.run_ref may reference a RunRecord, but that RunRecord's `semantic_input_refs` must never include its own output. The resolved graph must be acyclic.

## 4. Boundaries and STOP cases

- No execution of RECORD_INPUT, REVISE_INPUT, DISCOVER_LOCAL, EVALUATE, PROPOSE_CREATIVE, ASSEMBLE_BRIEF, RECORD_SELECTION, EXPORT_REVIEW_PACKET; no dispatcher, request/response, idempotency, output issuance or clock/UUID allocation.
- No semantic currentness engine, selection-head authority, eligibility scoring, stage-method provenance certification of Run's actual output, human rights/author authentication or privacy review. Exact referenced Run stage/outputs will be handled in separately scoped follow-up.
- No source actual text/value/index or FieldGrant authorization/exposure checking; the accepted local R1b validation remains intact. Packet-specific source dependency completeness is covered by canonical generic closure only to the extent of its typed graph edges, not trusted export permission.
- No persistence, network/Context7, file I/O in production functions, editorial/storage imports, GPU/models/providers, UI, FFmpeg, renderer or native Windows VM. No changes to S1/S2/S3, `PUBLISH_REVISION` (disabled), or partial COMMIT reconstruction (OFF).

**Potential contract trap:** The accepted SI/1 codec has 32-container-depth and 1 MB single-record limits. This task MUST impose no unapproved bundle size/length cap or silently truncate dependencies. You may use bounded iterative graph traversal and report environment limits honestly. If closure of legitimate inputs is unbounded in a way that affects implementation correctness, STOP with an exact issue instead of guessing a contract change. No external integer parser latency benchmark claim (prior SI-F01 remains nonblocking).

## 5. Exact allowlist

Only these **new** files:
1. `story_intelligence/resolver_v1.py`
2. `tests/test_story_intelligence_resolver_v1.py`
3. `tests/test_story_intelligence_resolver_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_1_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_1_CONTRACT_GAPS.md` — optional, only if genuinely blocked.

**Never edit** existing records/codec/model code, previous tests/golden files, contracts, acceptance notes, WORKLOG, configs, CI, dependencies, protected editorial/storage files, or `main`. If a foundation bug requires existing-file modifications, STOP and report exactly; do not expand the allowlist.

## 6. Tests, independent oracles and required evidence

Build genuine **self-consistent in-memory record graphs** (not 18 independent unresolved record vectors). Include a valid initial/manual chain with real complete record SHA-256 refs; valid RunRecord→derived output graph with no cyclic refs; a multi-revision H.previous chain; and R1a CreativeAlternative K1/K2/K3 retaining the same originating CREATIVE Run while H.origin.run_ref points to distinct REVISION runs. Distinguish a reference whose lexical shape is valid from exact referenced bytes that exist.

Required negative graph cases: missing root; missing H.previous, missing origin run, missing nested payload reference, missing Run.context input; wrong SHA; duplicate conflicting identity; duplicate identical record; direct/indirect cycle; tampered Run.input_snapshot (an omitted transitive input, an extraneous ref, and wrong canonical order); attempt to include Run's own output or itself; ERef passed as SIRef; accidental auto-resolve latest; typed-ref lookalike data in free-form text is not followed; no change to input; returned objects detached.

**Literal graph vectors:** at least six independent literal `Closure(roots)` manifests with expected exact `SIRef` lists and their canonical bytes/SHA-256; include simple and multilevel, Run snapshot, revision and creative dual-run cases. Expected values generated independently from the new resolver and SI production hash methods; include a README-like description in the test source, with literal bytes/hashes embedded, not computed dynamically from the function under test. If the desired graph can't be assembled under existing contract, **STOP and document** rather than using fake refs or breaking Run snapshot rules.

Execute actual targeted:
`python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v`

And full:
`python -m unittest discover -s tests -v`.

Use project's Python venv; show OS/interpreter, exact counts/exits, vector independence, no skips/fail suppression, and distinguish prior Codex-reported **66 targeted / 908 full** baseline from actual observed results. Compare existing 18+3 SI-E01.2a vectors and 14 SI-E01.1 vectors unchanged. Run `git diff --check`; verify exact five-file-or-fewer allowlist, parent/base remote SHA, clean working tree, no PR/main changes.

## 7. Publication and next owner gate

Publish only the new feature branch, exact base/commit/remote head, A-only diff stats, genuine test evidence, limitations and STOP. If an unresolved contract ambiguity prevents a correct typed-graph resolver, publish only the optional GAPS and RESULT files and mark `BLOCKED_CONTRACT` (no partial acceptance claim).

**SI-E01.2b.2** (stage/provenance semantic currentness and selection/operation prerequisites), **SI-E02** (Discovery), persistence/privacy/export, PR/merge/release/main remain separately gated, not authorized by this task. STOP for independent review after this exact bounded unit.
