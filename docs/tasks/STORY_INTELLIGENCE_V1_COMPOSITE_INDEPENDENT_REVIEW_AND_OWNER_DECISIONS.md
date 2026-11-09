# Story Intelligence V1 — composite specification independent acceptance and owner decision package

**Date:** 2026-11-09. **Independent review outcome:** **READY_FOR_OWNER_DECISION — SPEC_ONLY**.
This document records an independent technical finding and recommended owner choices, **not the owner's approval** and **not permission to implement**.

## Provenance and observed GitHub state

- Original specification: `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` at `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412` (683 added lines).
- R1 contract corrections: `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` at `978fbed45513a00e851201a9018d17c7da4752be` (691 added lines).
- R1a lifecycle clarifications: `docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md` at `b3f16984edc8daad364f356aa51aeddc2ac0b5b8` (237 added lines).
- R1a exact base `5f31b4aedc4916573300d204b5f3f52e1369ef80` verified; one commit ahead, zero behind, exactly one added file. Remote branch HEAD matched published SHA; no matching PR observed; `main` observed unchanged at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`.
- Source comparison was a **static GitHub document review**; neither tests nor Windows runtime were rerun independently. Codex-reported `git diff --check` and clean worktree are not claimed to be independently executed.

## Closed review findings

**SI-R01 RESOLVED** in R1: BRIEF_ASSEMBLY and PACKET_EXPORT have typed generating RunRecords; HUMAN_EDIT has distinct REVISION run; no derived→manual provenance laundering; exact replay and closure are explicit.

**SI-R02 RESOLVED** in R1: evaluation eligibility is independent of later user Selection, and `BriefReviewState` projects later explicit selections. Withdrawals do not rewrite earlier evaluation or confer authority.

**SI-R03 RESOLVED** in R1: immutable persisted discussion-only ReviewPacket, with ref-only output, frozen closure, privacy grants, redaction and currentness. Privacy design is a proposal; no proof of security/PII detection is claimed.

**SI-R04-A RESOLVED** in R1a: `RevisableRecordSet` includes StoryIdea, `CreateableRecordSet` excludes StoryIdea; Discovery produces initial revision and HUMAN_EDIT/REVISION maintains exact same id/previous and original provenance.

**SI-R04-B RESOLVED** in R1a: `CreateableRecordSet` excludes CreativeAlternative, first creation requires template CREATIVE run; `RevisableRecordSet` includes CreativeAlternative, with `payload.run_ref` preserving the original CREATIVE run and `H.origin.run_ref` referring to the current REVISION run. No fabricated manual creative run is accepted.

R1a defines 10 additional proposed acceptance cases and maps impacts to R1-T01–20 and SI-T01–26. The three proposal documents together form the **composite specification**. R1 supersedes exactly its declared original clauses; R1a supersedes exactly the two R1 operation rows/RecordSet rules; all other clauses retain their previous scope. No outstanding **blocking contradiction within SI-R01–R04** was identified in the reviewed contracts. This is not exhaustive proof that future executable implementation will need no further clarification.

## Proposed owner decisions — SI-D01–SI-D10

These are explicitly **recommendations requiring owner approval**, not defaults already in force.

| ID | Recommended approval scope | Exclusions/conditions |
|---|---|---|
| **SI-D01** | Offline-first, manual/local, CLI-first V1: Discovery → Evaluation → Creative → pre-script Brief → private discussion packet. | No live trends/crawling, published ranking, autonomous fact-checking, automatic render/publish. |
| **SI-D02** | Separate versioned SI/1 draft model with typed SIRef and exact immutable revisions, UNKNOWN semantics, provenance modes/stages and closed operation sets **as revised by R1/R1a**; strict canonical hashes and literal vector acceptance. | No editorial schema2 changes, no silent derived→manual conversion, no protected authority, no automatic manual Candidate export. |
| **SI-D03** | User-owned private local SI workspace outside repository/protected storage, with explicit versioning, integrity/idempotency and privacy boundaries. | Before persistence implementation: separately specify permissible root, file format, atomicity, backup/retention/cleanup and concurrent writer behavior; do not guess security/durability guarantees. |
| **SI-D04** | Proposed nine criteria, ratings0–5, weights **15/10/10/20/15/10/10/5/5**, unknown distinct from 0, aggregate only on fully known scores, blockers override ratings. | Heuristic rubrics, not calibrated predictive statistics or a probability of virality. |
| **SI-D05** | Human authorship/research/claims review, explicit selection and withdrawal with scoped immutable chains; `EvaluationEligibility` separate from `BriefReviewState`. | Human labels are not OS identity, editorial approval, rights grant, or a bypass of review/history. |
| **SI-D06** | Three genuinely distinct safe RU/UK creative approaches when feasible, qualitative 0–30s hooks, evidence-linked facts/qualifiers and natural voice. | No invented dramatic facts, false citation, model-driven change of checked claims. |
| **SI-D07** | Separate pre-script ProductionBrief and immutable local discussion-only, privacy-redacted ReviewPacket, ref-only output, explicit private grants. | No external/network export, automatic editorial writes, machine Candidate mapping, or render permission. Packet persistence/privacy lifecycle requires SI-D03 details. |
| **SI-D08** | Windows 10/11 CPU-only and local WAV/stills/FFmpeg fallback planning; locales `ru`/`uk`; explicit 9:16/16:9 target presets and production capability checks. | Targets not claims that native platform, timing, TTS licenses or renderer readiness is certified. |
| **SI-D09** | All network/paid/GPU/LLM/provider integrations deferred to separately authorized phases. External EXT-03/04 may inform independently written ideas only, subject to later specific rights review. | No import of code/models/Chinese corpora, no commercial release before licensing checkpoint; EXT candidates remain unapproved. |
| **SI-D10** | Accept the composite V1 contract and proposed test matrices **SI-T01–26 + R1-T01–20 + R04-T01–10**, then only separate, limited implementation assignments with independent evidence/owner gates. | This approval (if granted) would approve the specification, **not** automatically authorize source edits, deployment, merge/main, network calls or later implementation stages. |

## Implementation sequence after explicit separate authorization

1. **SI-E01**: pure SI value types, canonical codec, refs/provenance, run/record operation semantics and golden vectors; safe Python 3.12 CPU-only tests; no persistence/write path.
2. **SI-E02**: manual intake, local Discovery and transparent dedup with offline semantics.
3. **SI-E03**: rubric, evaluation and blocker precedence, strict unknown semantics.
4. **SI-E04**: creative alternatives, human selection and pre-script Brief assembly.
5. **SI-E05**: local private workspace persistence and redacted discussion packet after detailed SI-D03/07 decisions.
6. **SI-E06**: separate approved editorial adapter/interface, review/rights verification and explicit production boundary; no implicit protected write privileges.

Each milestone has its own bounded branch, file allowlist, test matrix, exact base SHA, independent review and owner gate. Phase 1 should not introduce a permanent user workspace or reimplement S1/S2. Do not start SI-E01 until the owner explicitly approves both the composite design and the separately scoped implementation task.

## Storage and release boundaries unchanged

- S3.2a accepted **PURE_ONLY**. S3.2b `BLOCKED_HOST_NOT_PROVIDED`; no VM or native install approval.
- `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF. E00/A1–A14/O1–O10/D1–D12, S1/S2/golden/rights/approval untouched.
- `ru`/`uk`, CPU-only Windows-first, optional paid/GPU only by later approval. Commercial model/voice/input/output rights reviewed before any release.
- No PR, merge, release or `main` change authorized by publication of this review.

**Next gate:** request explicit owner decision `APPROVE SI-D01–SI-D10 as recommended, including original+R1+R1a` or enumerate changes. Then prepare separately scoped SI-E01 Codex task. Until that decision, STOP.
