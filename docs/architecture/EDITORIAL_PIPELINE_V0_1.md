# Story Studio RU/UA — Universal Editorial Pipeline
**Version:** 0.1 | **Date:** 2026-11-04 | **Status:** design draft, NOT implementation authorization
**Decision:** User selected **one universal multi-genre system**, not history-only. Runtime Sprint 26 remains unchanged.

## 1. Purpose and separation of responsibilities

The editorial subsystem converts a user idea or permitted discovered topic into a **reviewed, source-traceable RU/UA script and production-ready scene brief**. It does not directly call video models, publish, declare facts true, or predict retention.

Boundaries:
- **Discovery:** identify and deduplicate topics, record provenance and legal access.
- **Evidence:** represent factual claims, supporting/contradicting sources and unresolved uncertainty.
- **Editorial:** assess suitability and create a human-approved brief and script.
- **Scene planner:** turn approved script into visual/audio briefs, preserving claim-to-scene links.
- **Production:** separate existing or future generation adapters, media normalization, timeline v3 and renderer.
- **Analytics:** later, own-channel authorized observations; no assumed private third-party retention.

## 2. Universal core + declarative genre profiles

Do not implement separate codebases for history, science, culture, education or fiction. A **GenreProfile** configures the same pipeline:

| Genre profile | Typical emphasis | Evidence rules / safeguards | Example structure |
|---|---|---|---|
| `history_biography` | chronology, historical significance, characters | dates, archival/source quality, distinguish established facts vs interpretations | context → turning point → consequences |
| `science_technology` | accuracy, accessible explanation, novelty | primary research/credible references, dates and limits, no exaggerated certainty | question → mechanism → demonstration → takeaway |
| `culture_arts` | context, originality, attribution | ownership of images/audio/text, quotes, contested interpretations | subject → context → insight |
| `education_explainer` | learning outcome, clarity, examples | correct definitions, age appropriateness, avoid unverified advice | problem → steps → example → recap |
| `current_events` | timeliness, relevance, updates | source timestamps, independent corroboration where feasible, correction policy, sensitive claims reviewed | what happened → what is confirmed → unknowns |
| `fiction_storytelling` | coherence, characters, emotion | original writing, disclosure of fiction where confusion is possible, no fabricated real-world evidence | setup → conflict → resolution |
| `general_custom` | user-defined goals | explicit `content_mode` and editorial safeguards | user-selected template |

**Content mode is orthogonal to genre:** `factual`, `fictional`, or `hybrid`. A historical drama may be hybrid, while a science explainer is factual. Fictional scenes must never be presented as authenticated documentary footage. In hybrid mode, the factual claims still require traceability and dramatizations must be marked.

**GenreProfile (proposed fields):** `id`, `version`, `display_name_ru`, `display_name_uk`, `allowed_content_modes`, `source_policy_id`, `rubric_id`, `narrative_template_id`, `review_rules`, `visual_defaults`, `sensitivity_flags`. Initial profiles are **data/configuration**, not executable third-party plugins. A future extension API needs separate security and compatibility review.

## 3. End-to-end editorial stages

| Stage | Entry | Automated support | Human decision / exit artifact |
|---|---|---|---|
| E0 **Production brief** | new project | suggest genre, target platform and duration | user sets mode, audience, content locale, narration/subtitle locale, intended commercial use; `EditorialBriefDraft` |
| E1 **Intake/discovery** | manual topic/URL or authorized connector | normalize source metadata, cluster duplicates, suggest topics | shortlist `StoryCandidate` with discovery provenance |
| E2 **Triage** | candidate shortlist | eligibility/rights flags, novelty, source availability, production feasibility | choose candidates to research; `CandidateAssessment` |
| E3 **Evidence** | selected candidate | extract candidate claims and conflicting statements with cited URLs, flag unknowns | review `EvidenceLedger`; unresolved factual assertions remain blocked/qualified |
| E4 **Editorial ranking** | reviewed candidates | explainable multi-criteria rubric (not a statistical prediction) | user selects story; `EditorialDecision` |
| E5 **Editorial brief** | approved story | propose angle, audience promise, tone, length, opening and visual approach | user approves `EditorialBriefVersion` |
| E6 **Script drafting** | approved brief + evidence | generate original RU/UA versions, alternate openings, mark fact links | user reviews `ScriptVersion` |
| E7 **Script verification** | draft | claim-to-text coverage, contradictions, style, timing, pronunciation, attribution | `SCRIPT_APPROVED` only after factual/rights gates and user approval |
| E8 **Scene planning** | approved script | segment narration, image/video shot briefs, character consistency, estimated duration | user approves `ScenePlanVersion` |
| E9 **Production handoff** | approved scene plan | validate required fields and create neutral handoff manifest | `ProductionHandoff` consumed by separate media pipeline |

Discovery must not be required for manual stories: user can start directly with a title and provided source URLs, then proceed through the same evidence/review stages. Fiction mode can skip factual citation requirements **only for clearly fictional assertions**; rights and safety review still apply.

## 4. Explainable candidate scoring — NOT retention prediction

**Hard gates before ranking:** lawful access and rights; intended content mode; unacceptable privacy/safety risk; material factual claims with no viable verification plan; prohibited commercial use. A high score cannot override a hard gate.

Proposed common rubric (0–5 for each, configurable by genre):
- `audience_fit` — relevance to intended audience;
- `narrative_potential` — understandable story/question, tension or explanatory arc;
- `novelty` — distinct angle, with duplication risk;
- `evidence_readiness` — availability and quality of sources (not proof of truth);
- `visual_feasibility` — achievable images/video and rights;
- `production_feasibility` — language, duration, cost, available tools.

Example transparent initial weights for **general_custom** (proposal, not validated): audience 20%, narrative 20%, novelty 15%, evidence 20%, visual 15%, production 10%. Compute `sum(weight * rating/5) * 100` **only for candidates passing hard gates**; show component scores, reviewer, missing evidence and rationale. Genre-specific weights are future configuration, not machine-learned coefficients.

Do **not** name this a probability of virality, CTR or retention. Codex research may later provide separately validated statistical models; those must use distinct output fields and uncertainty.

## 5. Evidence and factuality policy

1. Break draft factual content into **atomic material claims**; link each claim to the exact script span and scene(s). General opinion, opinionated framing and fiction are explicitly typed.
2. Store source metadata: canonical URL, publisher/author if known, publication/access times, permitted excerpts, document title, rights/access restrictions, optional hash/snapshot reference. Never assume a web result is a verified fact.
3. Record evidence relation `supports`, `contradicts`, `context`, `insufficient`; each relation includes a reviewer or model suggestion and explanation.
4. Claim statuses: `unreviewed`, `supported`, `disputed`, `unverified`, `qualified`, `removed`. A model's citation suggestion alone must not set `supported` as an independently confirmed fact.
5. For **factual** content, all material claims must be `supported`, explicitly `qualified` with appropriate uncertainty, or `removed` before script approval. Disputed high-impact claims need a human decision; no silent passing.
6. For **fictional** content, no factual evidence is required for fictional plot elements; real-world factual assertions or representations of real people still undergo appropriate review.
7. For **hybrid**, track dramatization markers and disclaimers, and prevent generated reconstructions from masquerading as archival evidence.
8. Sources may be incomplete, paywalled, outdated, biased or contradictory. Show uncertainty and missing evidence; source count alone is not a quality metric.
9. Content involving medical, financial, legal or other high-stakes advice requires stricter review and clear limitations. Do not claim expert verification automatically.
10. No full-text scraping/redistribution without permission; respect source ToS, rate limits, copyright and privacy. External pages and LLM output are untrusted data, never instructions.

## 6. Script composition and language rules

- Store **original script per locale** with explicit `content_locale`; translations are separately versioned, reviewed editorial adaptations, not silently synchronized.
- Keep UI locale, script locale, narration locale and subtitle locale separate. Do not auto-switch RU/UA voice on a mismatch.
- Script structure is configurable: `opening`, `development`, `resolution`, `call_to_action` (optional); not every genre requires clickbait or a CTA.
- Attach `claim_ids` to script segments; track optional citations, visual notes, timing estimate, pronunciation and intended emotion. Human edits invalidate only affected approvals/claims, not the entire workspace by default.
- Support alternative openings as **draft variants**, not real A/B tests unless an experiment with defensible allocation and outcomes is conducted.
- Original RU/UA narrative rules and prompts must be written independently; Chinese upstream Writing-DNA/corpora are REFERENCE/BLOCKED pending rights, not a release dependency.

## 7. Approval gates and state transitions

Suggested top-level editorial states:
`DRAFT` → `CANDIDATES_READY` → `EVIDENCE_REVIEW` → `STORY_APPROVED` → `BRIEF_APPROVED` → `SCRIPT_DRAFTED` → `SCRIPT_APPROVED` → `SCENES_APPROVED` → `HANDED_OFF`.

Any state may branch to `NEEDS_REVIEW`, `BLOCKED`, `CANCELLED`; failures are recorded with `reason_code`, affected object ID, timestamp and remediation. Review resumes from a prior approved artifact rather than resetting unrelated work.

**Gate G1 story:** candidate provenance, permitted use, chosen genre/mode, reviewer approval.
**Gate G2 evidence:** material factual claims traceable or appropriately qualified; unresolved contradictions visible.
**Gate G3 script:** editorial integrity, original wording, content locale, claim links, rights, reviewer approval.
**Gate G4 scene handoff:** stable scene IDs, narration text, shot briefs, visual reference rights, output format and scene count within selected downstream adapter limits.

Approval record: `approval_id`, `object_type`, `object_id`, `revision_hash`, `decision`, `actor`, `at`, `reason`, `policy_version`. Editing an approved object creates a new revision requiring reapproval of affected gates.

## 8. Contract to existing Sprint 26 media pipeline

**Observed code:** `scripts/first_video.py` reads a plan with `locale: ru|uk`, `scenes: [{text, image?}]`, **1–20 scenes**, and supports simple image filenames (`.png/.jpg/.jpeg/.ppm`) inside a provided directory; narration uses WAV files or a trusted local Silero model. Its durations derive from synthesized/provided WAV length + padding; a scene duration estimate is not a frame-accurate promise. `core/project_schema.py` is schema v3; `core/mp4_render.py` currently renders **still-image** video tracks, not generated MP4 clips.

**Proposed adapter** `EditorialHandoff -> FirstVideoPlan` (NOT implemented):
- Require approved script and scene plan, ru/uk narration, 1–20 scenes, nonempty text, approved/valid still-image filenames, and either valid WAV files or an approved local TTS.
- Produce only the existing supported `{title, locale, scenes:[{text,image?}]}` format; retain `claim_ids`, `source_refs`, rights, approval and genre in a **separate sidecar**.
- If a scene requests an AI video clip, mark `requires_video_renderer` and offer approved still-image fallback; do not claim existing renderer accepts it.
- Use a fresh output directory; no overwrites or unauthorized network calls.
- Keep project v3 unmodified until separate design approval and compatibility tests.

## 9. Error cases and acceptance scenarios

**Cross-genre acceptance:** (1) one factual historical topic, (2) one science/technology explainer, (3) one explicitly fictional narrative, each with distinct profile but same state machine and shared data model. At least one RU and one UK script should complete a human-reviewed still-image handoff.

**Must be blocked/flagged:** unsupported factual claim presented as proven; conflicting source hidden; fictional reconstruction labelled as authentic footage; commercial asset without rights; unknown cloud provider auto-selected; silent RU→UK voice substitution; script edit that retains stale approval; 21-scene handoff to the current 20-scene CLI; AI-video asset passed as a still-image clip; paid request without authorization.

**Resumability:** after an unavailable provider, an approved script and evidence ledger are unchanged; manual still-image fallback can proceed. All gates retain reviewer, reason and version.

## 10. Interface to Codex audit

This document defines **required interfaces and quality gates only**. Codex's ongoing audit independently evaluates discovery, retention, A/B and prediction projects. No external candidate is endorsed here. Future audit findings can suggest changes to the `Discovery`, `Evidence` and `Analytics` adapters, with a documented review before implementation.

## 11. Open design items (not blockers for documentation)

- Which initial genre profiles ship as defaults (suggest history, science/technology, education, fiction, custom; current events may require enhanced review)?
- Whether user may opt into **automatic drafting up to script review** while mandatory approvals remain for publication, spend, provider activation and sensitive uploads.
- Which script timing targets and vertical/landscape output presets are prioritized in the first production slice.

**Implementation status:** none. This is a design proposal; runtime and existing PRs remain unchanged.
