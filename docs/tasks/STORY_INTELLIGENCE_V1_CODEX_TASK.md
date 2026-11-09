# CODEX TASK — Story Intelligence V1 specification proposal (documentation only)

**Date:** 2026-11-09.
**Scope:** architecture-to-contract proposal / examples / acceptance criteria. **No implementation.**
**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`.

## 0. Exact handoff and branch discipline

Read this task on branch `docs/story-intelligence-v1-resume-after-s3-2b-hold`. Verify the remote HEAD and report the **exact SHA** used as base. If the branch has advanced since handoff, STOP for reconciliation; do not silently switch to `main`.

Create a new branch based on that exact SHA:
`docs/story-intelligence-v1-spec-proposal`.

No PR/merge/release or `main` changes. Do not alter S3.2b status, contracts, production code or tests. Publish only the single document allowed below and STOP for owner review.

## 1. Read the binding context before writing

Read:
1. `docs/tasks/STORY_INTELLIGENCE_WORKSTREAM_RESUMPTION_2026_11_09.md`.
2. `docs/architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md` (concept approved; **not** implementation approval).
3. `docs/tasks/STORY_INTELLIGENCE_COMPLETED_STAGES_REVIEW.md` (implemented vs missing capabilities).
4. `docs/tasks/E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md` and current storage acceptance/hold records, only to respect separation and authority.
5. Relevant E00/A1–A14/O1–O10 editorial requirements, `editorial/model.py`, `editorial/graph.py`, `editorial/current_package.py`, `editorial/rights_binding.py`, `editorial/approval_history.py`, `editorial/versioned_codec.py`, and `scripts/first_video.py` (read-only; inspect actual types and boundaries).
6. `locales/ru/prompts/script_system.txt`, `locales/uk/prompts/script_system.txt`, `LICENSES/IMPORT_LICENSE_GATE.md` and `docs/UPSTREAM_TECHNOLOGY_IMPORT.md`.
7. External-ideas register at **separate branch** `docs/external-ideas-adoption-register`, exact SHA `4ad198a095b155a57d6d0b162fc977260119962b`, path `docs/architecture/EXTERNAL_IDEAS_AND_ADOPTION_REGISTER.md`. Do not merge/cherry-pick or copy third-party code.

Do not interpret older historical 'storage proposal unapproved' wording in the 2026-11-05 Story Intelligence concept as overriding later, separately approved D1–D12/S1/S2 decisions.

## 2. Deliverable: proposed Story Intelligence V1 contract

Write one **self-contained** specification, with explicit `PROPOSAL / AWAITING OWNER APPROVAL` status, that covers:

### A. Product use-case and boundaries
- Main journey: local/manual topic intake → Discovery → Evaluation → Creative alternatives → structured pre-script Production Brief → separately authorized editorial handoff.
- Roles and responsibilities, what the user edits/approves, which operations are merely suggestions.
- Offline-first Windows 10/11 CPU-only; ru/uk locale handling; network search/provider integrations are optional future adapters and must be explicitly marked unavailable in offline V1 unless supported.
- A short, realistically useful V1 scope, explicit deferred features, and phased implementation order.

### B. Conceptual model and provenance
- Candidate/idea identity, exact source references, claims/evidence and review state, audience hypothesis, channel context, angles, evaluation runs, creative alternatives, risk and visual requirements, pre-script brief revisions.
- For every proposed record: purpose, minimal fields and types, required/optional/unknown, ID/revision provenance, validation, producer/consumer, immutable vs editable, and compatibility mapping to **actual existing** `CandidateRevision`, `SourceRevision`, `ClaimRevision`, `BriefValue`, `ScriptRevision`, etc.
- Distinguish existing executable schema fields from **new conceptual proposal**. Do not put unsupported data into existing `reason`/`rationale` fields or silently extend schema 2. Automatic provenance must never masquerade as manual `discovery_method`.
- Versioned run metadata: method/rubric version, source snapshot, model/provider if used, time and confidence/uncertainty; do not confuse clock time with editorial authority/order.

### C. Discovery and evaluation
- Offline intake from user-supplied topic/URLs/local sources, normalization, transparent dedup candidate logic, and 'no fresh trend data' behavior.
- Explicit, explainable separate criteria: audience interest/channel fit, novelty, evidence quality, narrative potential, visual feasibility, resource cost, legal/ethical/scientific/reputational risks, portfolio duplication.
- Define rubric scale/weights only as **proposed** values; include rationale, missing data semantics, blocker precedence and conservative fail-closed recommendation. No invented 'viral probability' or ungrounded audience statistics.
- Score is not claim verification, rights authorization or publication permission.

### D. Creative and Production Brief
- At least 3 different hook strategies when appropriate, alternative angles, chapters, 0–30 s retention hypothesis (qualitative), visuals classified required/local/optional, sourcing/rights/fallbacks and production effort.
- Human-readable natural RU/UK writing without generic AI clichés; creative claims remain traceable to evidence, unsupported central claims flagged.
- Production Brief: audience, locale, promise, duration, exact source/claim refs, required review and blocking risks, chapters, visual priorities, rights and licensing state, TTS/ASR/editing options, CPU-only fallback, version/approval status.
- Explicit interface from **proposed** brief to existing editorial structures; no direct authorization of renderer or bypass of editorial/rights gates. Explain what would need an approved adapter later.

### E. Validation, examples and acceptance gates
- One full **illustrative** RU case: `Почему исчезли древние цивилизации?`, science, 8–12 minutes, balanced intensity, with audience assumption, 3 hooks, chapter outline, evidence-needed labels, visual priorities, scientific/production risks, explicit unknowns. This is a sample, not verified factual research.
- One compact UK case with different audience/angle and localized text.
- Negative cases: missing critical evidence; unlicensed essential visual; duplicate topic; absent internet/current trends; stale source; changed candidate/source revision; high score but blocking rights; conflict between hook and verified facts; unavailable GPU/paid provider.
- For each case, define expected status/recommendation and no false editorial approval.
- A proposed versioned API/interface shape, no executable code, no third-party dependency, and a test matrix ready for later Codex tasks.
- List all **owner decisions** needed before implementing schema/data interfaces/scoring (e.g. rubric defaults, scope, persistence location, provider opt-ins, production-brief export boundaries).

### F. External ideas and licensing gate
- Evaluate EXT-01–EXT-04 against **this** phase. Mark each `APPLICABLE_AS_IDEA`, `LATER` or `NOT_APPLICABLE` with explanation and explicit owner approval needed before code reuse. Do not claim any candidate is already approved.
- Reuse no upstream Chinese Writing-DNA, corpus, model weights, media, voices or code without documented rights. Preserve release-license checkpoint for Edge/Silero and any new provider.

## 3. File allowlist and QA

Create **only**:
`docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md`

No other changed files. No implementation, schema edits, test edits, dependency changes, network crawling, API calls, model downloads, paid requests, storage or Windows-native work. No speculative performance or viral metrics.

Run document consistency checks, `git diff --check`, verify exact one-file allowlist, branch base and remote HEAD, and clean worktree after push. Python tests are not required for docs-only work; do not claim them run if not.

## 4. Report and STOP

Report base SHA, branch, commit SHA, remote HEAD, file path, concise scope, open owner decisions, external register gate and any incompatibilities found. If a true incompatibility is found, document it rather than changing working code.

**STOP after publishing the proposal.** Owner + independent review must approve the specification before any implementation task.
