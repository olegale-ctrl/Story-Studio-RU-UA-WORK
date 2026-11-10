# Story Intelligence — SI-E02 planning proposal

**Date:** 2026-11-10 (Europe/Kyiv)  
**Status:** **PROPOSAL / NOT APPROVED FOR IMPLEMENTATION**  
**Planning base:** accepted SI-E01.2b.3 implementation `cd82fd654b270adcdf702eba915fd22c59aaeaff`; see [final acceptance](STORY_INTELLIGENCE_SI_E01_2B_3_FINAL_ACCEPTANCE_2026_11_10.md).  
**Purpose:** establish the next bounded stage without prematurely assuming an approved SI-E02 contract.

## 1. What is already available

Accepted SI foundation provides canonical SI records/refs and hashes, resolver, provenance/audit checks, and a pure `check_si_currentness(records, root, observed_active_input_refs, observed_selection_head_refs)` API with CURRENT / STALE / INVALID. It is **not** an authoritative eligibility, factual accuracy, rights, editorial decision, execution, or publication gate. G01/G02 and F1-D1 remain binding.

## 2. Recommended SI-E02 objective

**Proposed SI-E02 = Story Intelligence editorial decision/production-brief contract design, not a code implementation yet.**

Define how candidate topics and evidence are converted into a human-reviewable **editorial decision and Production Brief** that downstream production may consume, without weakening provenance or misrepresenting observations as authority.

Focus on the user's editorial goal: topic discovery, comparison/scoring, prioritization, and assignment to production. The initial output should be a **contract proposal and worked example**, not an automatic scoring engine or production execution.

Proposed sections of the contract:

1. **Inputs:** exact SIRefs, currentness observation and limitations, research evidence, intended audience (age/knowledge), RU/UA locale, target format/duration and editorial constraints.
2. **Candidate assessment:** relevance, audience value, novelty/competition, evidence sufficiency, feasibility, estimated visual burden and principal risks. Scores/weights are *proposals*, not invented established policy.
3. **Editorial card:** sharply formulated central question, 2–3 alternative hooks (including a high-intensity option), chapter outline, prioritized must-have vs optional visuals, evidence gaps, audience fit, and main risks. Natural RU/UA language without formulaic AI clichés.
4. **Human gate:** draft/review/approve/reject and explicit reviewer authority; distinguish recommendation from final approval and preserve exact input/revision references.
5. **Production Brief boundary:** what downstream systems receive, required proof and rights gates, versioning/frozen references, invalidation and human override rules. No promise that rendering/TTS/editor/export is implemented.
6. **Evaluation:** reproducible fixtures with conflicting claims, missing sources, changing source revisions, incompatible audience, unsupported rights, and stale editorial choices.

## 3. Recommended staging

**SI-E02.0 — Discovery & contract mapping (docs only).** Inventory existing Story Intelligence schemas/decision documents, identify which proposed concepts already have accepted record types, and produce a gap/authority matrix. Do not create parallel wire types or duplicate currentness. Confirm naming and whether SI-E02 is already reserved for another deliverable.

**SI-E02.1 — Owner decisions.** Resolve only material open questions: scoring rubric and human authority; whether Production Brief is an existing type or new contract; input snapshot and freshness behavior; editorial ERef resolution and rights proof; language/locale behavior. Recommend conservative defaults but do not invent owner approval.

**SI-E02.2 — Minimal implementation proposal (not authorized yet).** Once approved, write a closed allowlist, independent test oracles, exact base, negative cases and explicit STOP criteria. Prefer pure functions before persistence/UI/providers.

## 4. Non-goals and protected boundaries

No SI-E02 implementation in this planning step. No ERef adapter, protected writes, storage service, publishing, model/provider integration, external topic scraping, automatic approvals, UI, audio/video generation, release, merge, or changes to `main`. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Licenses, sources, TTS/ASR/media rights, offline CPU-only constraints and RU/UA localization remain mandatory gates for any future production work.

## 5. Owner review questions

1. **Scope:** approve SI-E02.0 as a documentation-only inventory/contract-mapping stage, or choose another specific SI-E02 objective?
2. **First deliverable:** prioritize topic ranking/assignment contract or Production Brief contract? Recommended: inventory both, then choose one bounded implementation path.
3. **Authority:** confirm that scores and recommendations are advisory until explicit human editorial approval (recommended).
4. **External editorial ERefs:** keep adapter outside E02.0 and fail closed until separately approved (recommended).

**Suggested next Codex task only after owner confirms E02.0:** read current accepted SI and editorial documents; create an inventory/gap matrix and a draft SI-E02 contract in a new docs-only branch from an explicitly supplied SHA; no code, schema changes, tests rewriting, or merges; STOP for independent review.
