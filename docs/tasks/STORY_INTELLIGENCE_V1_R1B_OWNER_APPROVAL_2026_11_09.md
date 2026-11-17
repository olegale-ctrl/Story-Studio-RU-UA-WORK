# Story Intelligence V1 — owner approval of R1b-P01–P05

**Date:** 2026-11-09
**Decision status:** **APPROVED — R1b-P01–P05 (contract-only clarification)**
**Implementation status:** **SI-E01.2a-RESUME TASK PREPARATION; NOT STARTED**
**Owner instruction (verbatim):** «Утверждаю R1b-P01–P05 в предложенной редакции. Зафиксируй решение в GitHub и подготовь ограниченное задание Codex на возобновление SI-E01.2a. Без merge/main.»

## 1. Exact approved clarification

The owner explicitly approves **all five proposed decisions without modification** in:

- `docs/tasks/STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md`, proposal commit `5fdd1d8f72ccec37730c8f4c271450e4e95f8de1`.
- The blocker evidence remains `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md` and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESULT.md`, blocked commit `18163478f2204c3dd3d3f9bd742c49ea8253506e`. Those documents remain historical and **are not edited or retroactively declared successful**.

This approval **supersedes the proposal's AWAITING OWNER APPROVAL / STOP gate solely for R1b-P01–P05**. The proposal document itself is not rewritten; this approval note is the binding owner decision.

## 2. Approved R1b-P01–P05

1. **R1b-P01 — wire namespace:** `FieldGrant.field_path`, `FieldView.field_path`, `Omission.field_path` are exact **source-record payload-relative** paths. No `H`, `payload.`, type prefix, aliases, JSONPath, wildcard, whitespace, implicit normalization. Decimal zero-based indices with no leading zeros. Only approved record-type/kind paths.
2. **R1b-P02 — TEXT mapping:** exact closed source type/path whitelist, including `title`, `title.value` for KNOWN, `title_options[0]`, `chapters[1].purpose`, etc. TEXT requires matching explicit FieldGrant and unchanged reviewed text; no permission for private fields.
3. **R1b-P03 — STATE mapping:** exact source-record scalar states, including `EvaluationReport` source_ref and `eligibility.state`; booleans rendered as lowercase ASCII `true`/`false`. `BriefReviewState.review_state` and `currentness` remain only in `ReviewPacket.payload.review_state_at_capture`, never as FieldView, synthetic SIRef or independent record.
4. **R1b-P04 — REDACTED/Omission:** source-record payload fields only; header fields excluded from views, not projected through virtual H paths. REDACTED text=null with corresponding Omission; sensitive payload fields may be named only for withholding, not released.
5. **R1b-P05 — matching and ordering:** unique source/path grants/views/omissions, exact source-field-value hashes, manifest order and declared schema field order with ascending array indices; no invented source resolution or implicit privacy approval.

## 3. Composite precedence and limits

The binding composite is **original specification + precise R1 overrides + precise R1a overrides + this precise R1b ReviewPacket path/projection clarification**. SI-D01–SI-D10 remain approved and unchanged. The new R1b is narrower than the rest of the contract; it does **not** authorize changing existing SI-E01.1 code, editorial/storage authority, new RecordTypes, privacy profile, persistence, external export, network, provider, paid/LLM/GPU use, production, renderer or publication.

SI-E01.1 stays **ACCEPTED / PURE_FOUNDATION_ONLY**. SI-E01.2a prior attempt stays **BLOCKED_CONTRACT** as an immutable result. Approval of R1b removes the documented G01 specification obstacle **for a new bounded attempt**, not evidence that all remaining schema questions are resolved or that any tests have passed. If another blocking ambiguity is found, Codex must STOP and document it.

## 4. Implementation handoff gate

Prepare a **separate, bounded SI-E01.2a-RESUME Codex task** based on the branch containing this approval, with a fresh feature branch and distinct result/gap filenames. The existing blocked result and original task remain read-only. The owner must hand the exact task and base SHA to Codex; this approval does not itself execute implementation. Do not authorize SI-E01.2b or SI-E02.

All work remains on feature/documentation branches. **No PR, merge, release or main changes.** S3.2b remains BLOCKED_HOST_NOT_PROVIDED; `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF.

**STOP after publishing the approval note and bounded resumption task.**
