# Story Studio RU/UA — Natural Narration & Anti-Template Editor (proposal)

**Date:** 2026-11-06  
**Status:** RESEARCHED DESIGN PROPOSAL — NOT OWNER-APPROVED; NO IMPLEMENTATION AUTHORIZATION.  
**Branch base:** `d816f1b94a71e04363371d9bc05b06f52a7fc0d6` (S2.3 adversarial verification).  
**Request:** make RU/UA video scripts sound like a human narrator rather than generic AI prose; review the original Chinese project and selectively adapt ideas from `fendouai/free-ai-humanizer`.  
**Scope:** script drafting and editorial style only; no protected-storage changes.

## 1. Verified source findings and provenance

### Upstream `konlu/story-studio`

- `modules/history-writing/references/Writing-DNA.md`: grounded spoken narration, specific action instead of abstractions, variable pacing, no invented sensory details, multiple narrative structures rather than one fixed formula.
- `modules/history-writing/references/语言DNA.md`: measurable sentence rhythm, conversational connectors, concrete verbs and a **limited** final de-AI pass. Explicitly remove empty summaries, gratuitous moral uplift, parallel filler, repetitive intensifiers and unanswered chains of rhetorical questions, **not** all questions or contrasts.
- `modules/history-writing/GUIDE.md` and `references/fact-and-style.md`: fact/source timeline first; factual validation of hook and body; no invented quotations, numbers, dates, motives, scenes; user requirements override style.
- `modules/characterstory-writing/Writing-DNA.md`: strong hooks and scene-oriented storytelling, but also repeated fixed formulas (`您说` 3–6 times, mandatory emotional closers, compulsory sharing CTA) which can themselves create a templated voice. Do **not** transfer these as global requirements.
- Upstream research corpora and Writing-DNA remain **REPLACE or BLOCKED** under the RU/UA project policy. Abstract craft ideas may inform independent design, but original transcripts, templates, fixed passages and unverified rights are not approved for inclusion in distributable RU/UA assets. Upstream README advertises CC BY-NC-SA 4.0; separate rights review remains necessary for any copying.

Source URLs:
- https://github.com/konlu/story-studio/blob/main/modules/history-writing/references/Writing-DNA.md
- https://github.com/konlu/story-studio/blob/main/modules/history-writing/references/%E8%AF%AD%E8%A8%80DNA.md
- https://github.com/konlu/story-studio/blob/main/modules/history-writing/GUIDE.md
- https://github.com/konlu/story-studio/blob/main/references/fact-and-style.md
- https://github.com/konlu/story-studio/blob/main/modules/characterstory-writing/Writing-DNA.md

### `fendouai/free-ai-humanizer` and same-author open source

- Exact `github.com/fendouai/free-ai-humanizer` repository was not found (404 on 2026-11-06). External listings describe `fendouai/free-ai-humanizer` as a Hugging Face Space; its precise source revision and license were **not independently audited**, so do not copy its code or claim its implementation has been verified.
- The same author publishes the inspectable GitHub repository `fendouai/humanize-text-skill` (MIT license, checked 2026-11-06), aimed at **Chinese and English**, not RU/UA. Useful architecture: `detect/rewrite/edit`; subtraction (remove AI residue) + addition (target voice); protect factual spans first; separate AI-pattern score, voice drift and fidelity; scene-aware action policy; minimal edit; second-pass residue audit.
- No claim that a humanizer can prove human authorship, guarantee AI-detector results, or create distinctive writing by vocabulary substitution alone.
- Do not import its JS runtime into the Windows/CPU-only Python pipeline by default. If copying any MIT code, preserve license/copyright notice and separately review dependencies; prefer independently authored RU/UA rules and tests.

Source URLs:
- https://github.com/fendouai/humanize-text-skill
- https://github.com/fendouai/humanize-text-skill/blob/main/SKILL.md
- https://github.com/fendouai/humanize-text-skill/blob/main/references/voice-contract.md
- https://github.com/fendouai/humanize-text-skill/blob/main/references/quick-checklist.md
- https://github.com/fendouai/humanize-text-skill/blob/main/LICENSE
- https://huggingface.co/spaces/fendouai/free-ai-humanizer (listed externally; primary page not verified)

### Current RU/UA gap

- `locales/ru/prompts/script_system.txt` and `locales/uk/prompts/script_system.txt` currently only request an original script in the given language; no full anti-template or voice-quality contract.
- Story Intelligence architecture at `docs/architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md` (separate branch `docs/story-intelligence-architecture-decision-2026-11-05`, commit `aeef7435e85538ed2b83c0cb6e6513b999b8c062`) defines Creative Engine and Production Brief conceptually; it does not yet implement script generation or this editor.
- This proposal must not imply those branches are merged, or modify approved E00/A1–A14/O1–O10/D1–D12/S1.

## 2. Proposed editorial pipeline

`Verified fact pack + audience + channel voice + production brief` → `script architecture / narrator angle` → `draft` → `protected-span and claims snapshot` → `RU/UA anti-template detect` → `minimal editorial rewrite` → `fact/fidelity recheck` → `voice and read-aloud QA` → `human review` → `approved script version` → `TTS / storyboard`.

**Important:** script style changes are non-authoritative suggestions. A rewrite cannot alter source-backed claims, their epistemic status, quotes, identities, dates, rights, editorial decisions or approval gates. Any change that affects meaning returns to claim/source verification. Do not silently replace an already approved script or create a new protected publication revision; `PUBLISH_REVISION` remains DISABLED.

## 3. Core functions (future, not implemented)

1. **Draft voice control:** specify RU or UK, intended viewer, genre (history, science, biography, explanatory), narrator distance (conversational, investigative, calm), and a short independently owned voice profile. Avoid forcing every genre into the same colloquial style.
2. **Detect:** annotate only concrete problems with span, category, explanation and suggested operation. No opaque “AI percentage” or detector-pass promise. Context and genre determine severity.
3. **Edit:** minimum local change preserving original facts and story logic; permit audit-only if evidence is missing or the text is already natural. Never auto-fabricate emotional scenes, quotes or author experiences.
4. **Rewrite:** optional second pass when the structure is consistently generic; preserve chapter/claim anchors and return change summary for review. Never rewrite factual uncertainty into certainty.
5. **Voice alignment:** measure approximate sentence-length distribution, variation, repeated connectors, empty rhetorical questions, over-regular paragraph endings, narrator distance, unnatural code-switching and TTS speakability. Style metrics are diagnostics, not absolute acceptance thresholds.
6. **Read-aloud QA:** ensure RU/UK morphology, inflection, natural pauses, pronunciation of abbreviations, dates and units, tongue-twisters and breathing space. TTS preview may be optional; CPU-only text checks must work without audio generation.
7. **Second-pass audit:** check whether edits introduced new clichés, meaning drift, language mixing, invented claims, flattened emotional tone or unnatural repetition. Stop once the passage reads naturally and protected facts remain unchanged.

## 4. Contextual RU/UA problem families

Examples to **flag for review, not blanket-ban**:

- Generic opener: RU «В современном мире…», «Давайте погрузимся…»; UK «У сучасному світі…», «Давайте зануримося…».
- Narrator filler: RU «Важно отметить, что…», «Стоит подчеркнуть…»; UK «Варто зазначити, що…», «Слід підкреслити…».
- Empty significance: RU «Это событие навсегда изменило историю» without evidence; UK «Ця подія назавжди змінила історію» without evidence.
- Mechanical contrast: RU «Это не просто X, а Y»; UK «Це не просто X, а Y» when repeated or unsupported, but keep meaningful factual contrasts.
- Manufactured suspense: «Но самое удивительное было впереди», «Вы не поверите» with no immediately substantiated payoff.
- Generic ending: «История учит нас…», «Именно поэтому важно помнить…» when no specific conclusion is earned.
- Repeated questions, identical transition phrases, over-symmetric paragraphs, long stacks of adjectives and excessive exclamation marks.
- Russianisms in Ukrainian, Ukrainianisms in Russian, unnatural literal translation, wrong cases and numerals, stilted TTS phrasing.

**Preferred positive style:** lead with an evidence-backed action, contradiction or question; explain causes and choices using concrete actors and consequences; vary sentence length according to meaning; leave room for natural pauses; allow uncertainty when sources warrant it. Distinctive voice comes from perspective and selection of detail, not synthetic “human errors” or slang injection.

Illustrative **non-factual** style contrast:

- Template: «Сегодня мы погрузимся в удивительную тайну исчезнувших цивилизаций. Эта тема заставляет задуматься о хрупкости всего человечества».
- More direct: «Почему некоторые города постепенно пустели? Чтобы разобраться, нужно отделить то, что показывают археологические находки, от догадок о причинах».  
  This is a framing example, **not** a historical claim or approved script hook.

## 5. Non-negotiable fidelity and rights gates

- Protect names, dates, quantities/units, quotations, source links, claims and qualifiers (e.g. «возможно», «по одной из версий», «ймовірно») before editing. Do not merely replace strings and assume semantic preservation; run claim-level comparison afterward.
- No fabricated evidence, quotes, eyewitness/author stance, private motives, historical dialogues, invented scenes or unsupported “first/only/never” claims.
- Preserve citation/claim IDs in metadata; script prose may omit inline citations only when an external verifiable source ledger remains.
- Do not train on, redistribute or copy Chinese creator corpora or personal voice samples without explicit documented rights; use independent licensed RU/UA exemplars or synthetic evaluation fixtures.
- Human voice quality and factual accuracy are **independent** gates. A high style score never compensates for unsupported claims.
- No claim of “AI detector bypass”; the goal is good spoken narration for human listeners.

## 6. Proposed interfaces (not an approved data schema)

Inputs: `language`, `genre`, `audience_brief`, `narrator_profile`, `draft_text`, `claim_ledger`, `protected_spans`, `approval_state`, `edit_mode`.

Outputs: `issue_spans` with severity and suggested action, `candidate_text`, `protected_span_integrity`, `claim_delta`, `voice_diagnostics`, `read_aloud_flags`, `review_required`, `diff`.

Modes: `detect` (read-only), `suggest` (non-mutating candidates), `rewrite` (candidate only, explicit human acceptance). Do not wire these into authoritative storage or change any schema2 wire contract before separate approval.

## 7. Proposed acceptance matrix

- RU and UK paired examples for each problem family; context-sensitive false-positive tests for valid rhetoric, quotations, science uncertainty and formal tone.
- Clean human-written passages pass without mandatory edits; a rule list must not erase author personality.
- Dates, numbers, units, names, quotes, citations, negations, source attribution and epistemic qualifiers remain unchanged in meaning and protected bytes where required.
- Test natural RU/UA declension, stress/abbreviation reading, code-switching and punctuation suitable for voiceover.
- At least one end-to-end science and one history script sample per language with human assessment: clarity, listenability, originality of angle, factual fidelity and repetitive phrasing. No made-up benchmark percentages.
- CPU-only/offline detector baseline with standard-library Python preferred; any optional model rewrite must have CPU-compatible execution path and documented license, cost, region and rights.
- Repeated edit/rewrite should not progressively erase information or add new content; unchanged clean text should be stable.
- No protected storage changes, no unapproved PUBLISH_REVISION, no impact on S2.4 D-01 remediation or storage tests.

## 8. Sequencing and owner decision

This is a **separate editorial track**. S2.4 D-01 remains blocking for S3; this proposal neither bypasses it nor depends on completing S3.

Proposed later sequence after owner approval:
1. Approve this independent RU/UA Natural Narration design, including its source/rights constraints.
2. Prepare a closed **editorial voice-quality specification** with independent RU/UA fixtures, claim-preservation policy and tests, aligned with Story Intelligence V1/Production Brief.
3. Implement a small CPU-only **detect-only** baseline and paired RU/UA tests on an isolated feature branch.
4. Add candidate-only style suggestions/rewrites, fidelity gates and human acceptance, with separate review.
5. Integrate with Creative Engine and TTS preview only when those engines are approved and implemented.

No automatic GitHub merge/PR/release, no changes to `main`. This file documents findings and a recommendation, **not** a completed feature or approved contract.
