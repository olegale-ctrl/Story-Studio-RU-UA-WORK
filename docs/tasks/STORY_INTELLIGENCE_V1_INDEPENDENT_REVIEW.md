# Story Intelligence V1 — independent specification review

**Date:** 2026-11-09. **Outcome:** **CHANGES_REQUIRED (SPEC_ONLY)** before owner approval or implementation. This is a review, not an owner decision or code authorization.

## Exact provenance and GitHub verification

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Proposed contract: `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` at `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
- Exact proposal base: `e8b1b0347853a6f6a62910c65ceb17691fb1dab2`.
- GitHub comparison: one commit ahead, zero behind; exactly **one added Markdown document, 683 lines**. Branch remote HEAD matched published SHA, no PR found, `main` observed unchanged at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`.
- Reviewer examined proposal and selected actual code boundaries in `editorial/model.py` and `scripts/first_video.py`. No executable tests were rerun. Codex reports docs consistency/diff checks; these are not independently rerun by this reviewer.
- Storage scope: S3.2a accepted PURE_ONLY, S3.2b `BLOCKED_HOST_NOT_PROVIDED`; neither changes here.

## Correct overall direction

The document separates manual/offline topic intake, transparent local dedup, explainable evaluation, creative alternatives and a pre-script Production Brief. It preserves unknown/missing evidence, provenance, source/claim exact refs, rights and editorial review boundaries. RU/UK examples do not fabricate sources or claim verified facts; proposed weights sum to 100 and the score formula ranges 0..1000 rubric tenths (0..100 display points). It defers external providers, crawling, protected writes, renderer/approval and licensing decisions. The compatibility table acknowledges existing `CandidateRevision`, `BriefValue` and `RevisionRef` limitations instead of changing schema2. These foundations are suitable for V1 once the following contract contradictions are corrected.

## SI-R01 — Derived-output provenance not closed (must fix)

**Conflicting clauses:** §2.1 H.Origin requires `run_ref: SIRef` for every `RULE_DERIVED`/`TEMPLATE_DERIVED`/`MODEL_DERIVED`; `RunRecord.stage` in §3 is only `DISCOVERY|EVALUATION|CREATIVE`. Yet §8 commands `ASSEMBLE_BRIEF` and `EXPORT_REVIEW_PACKET` create outputs, respectively `ProductionBrief` and `ReviewPacket`, from already-recorded input data, without a corresponding run/stage and without an alternative exact provenance rule. A user clicking assemble/export does not make a deterministic derived output `MANUAL_INPUT`.

**Impact:** no internally consistent `H.origin` for derived/assembled records; future serializer would either reject a legitimate output or silently mislabel its origin.

**Required clarification:** specify how each operation creates/does not create a recorded SI object; exact provenance for assembly and packet; versioned deterministic method and explicit run/input refs where needed; stable output identity/idempotency; avoid circular run/output hashes. Choose either additional explicit `RunRecord.stage` modes or a rigorously specified non-record projection/explicit authored record distinction. Do not use false manual provenance or loosen `run_ref` globally.

## SI-R02 — Evaluation recommendation depends on later selection (must fix)

**Conflicting clauses:** §3 `EvaluationReport` stores `Recommendation`, created by §8 `EVALUATE`; the product journey is Evaluation → Creative → explicit Selection → Brief. However §5.2 says `PROCEED_TO_BRIEF_REVIEW` is possible **only with manual choice**. At the time of `EVALUATE`, a later creative alternative/brief selection may not exist. Recorded evaluation cannot both be immutable and infer a future choice retroactively.

**Impact:** a fully evidenced, nonblocked evaluation has no reproducible successful recommendation at evaluation time, or would acquire success after a later human action without a new revision.

**Required clarification:** separate stage-specific evaluator recommendation/eligibility from post-selection projection for brief review; specify which type stores which status and on which exact refs; preserve `BLOCKED`/unknown precedence and forbid any implication of editorial approval or render permission. Add an acceptance example for evaluation before selection, explicit selection afterward, and changed input/withdrawal.

## SI-R03 — ReviewPacket record vs read-only projection unresolved (must fix)

**Conflicting clauses:** §3 declares **every** table entry a record with H and `SIRef`; `ReviewPacket` is one of these and is `DISCUSSION_ONLY`. §8 `EXPORT_REVIEW_PACKET` describes a read-only projection with `output_refs` and idempotent request semantics but no clear recorded/non-recorded behavior, snapshot closure rule, lifetime, or package privacy boundary. This is distinct from SI-R01: resolving run provenance alone does not define what an exported packet *is*.

**Impact:** unpredictable persistence and stale semantics; reviewers could receive a packet that references a different set of revisions, or mistakenly treat a transient view as an immutable recorded item.

**Required clarification:** decide stored immutable record with content hash and closure, or ephemeral deterministically reconstructible read-only packet. Define output shape/ref if applicable, exact dependency closure/snapshot, current vs stale rule and export privacy filtering for local locators/labels. In either choice `DISCUSSION_ONLY` never grants authority, editorial write, rendering or rights.

## Owner decision gate — not approved here

SI-D01–SI-D10 remain **proposed, unapproved**. Reviewer recommends the following **for owner consideration after R1**:
- D01: offline/manual CLI-first V1, no live trends, model/provider runtime, protected write or renderer.
- D02: separate strict SI/1 and immutable exact revisions/provenance, provided SI-R01/03 are resolved and codec vectors specified before code.
- D03: local user-owned draft workspace outside Git/protected storage; private paths/redaction, backup/retention/cleanup to be specified. Never commit drafts, sources, identifiers or personal data.
- D04: nine-criterion 0..5 proposal, weights 15/10/10/20/15/10/10/5/5, UNKNOWN never zero, hard blockers precede scores; treat weights as heuristic, not calibrated.
- D05: explicitly human-selected/annotated research, with human labels not equivalent OS principal, editorial approval or grants.
- D06: RU/UK creative templates and 3 distinct hook strategies when safe, qualitative 0–30s, fact-preserving language pass.
- D07: separate pre-script Brief and discussion-only read-only handoff. Do not authorize automatic editorial Candidate/production export until independently reviewed adapter.
- D08: CPU-only Windows10/11, local WAV/stills/FFmpeg planning and visible capability limits; not auto-render.
- D09: no provider opt-ins or EXT code transfer in V1; separate scope/rights/region/privacy/cost approvals later.
- D10: specification re-review after R1; then staged, bounded implementation approvals, never via concept decision alone.

**No owner approval is inferred** merely by publishing this review or R1 erratum. S3.2b remains blocked.

## Recommended next step

Codex should do a **documentation-only R1 contract reconciliation** on a new feature branch, using exact base SHA of this review branch after publication. Do not edit the original proposal; publish a separate complete clarification/erratum with updated types, operation table and acceptance cases, explicitly stating its priority relative to the proposal. Review both documents as one composite proposal. Do not modify existing code/schema/tests/contracts, `main`, PR or merge. STOP and request owner approval after independent R1 review.
