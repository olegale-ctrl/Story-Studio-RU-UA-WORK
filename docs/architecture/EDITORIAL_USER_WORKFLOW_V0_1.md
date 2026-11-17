# Story Studio RU/UA — Editorial User Journey and Screen Specification
**Version:** 0.1 | **Date:** 2026-11-04 | **Status:** proposed UX, not implemented
**Product direction:** universal multi-genre editor with human-controlled automation; Windows 10/11 first; RU/UA UI/content/voice/subtitles configurable independently.

## 1. UX objective

A user should be able to start with **a single idea, URL or topic**, choose a genre/content mode, examine the evidence and script, approve scenes, and send a compatible package to the existing local video pipeline. Users who want more control can open the underlying sources, revisions, provider choices, rights and technical settings.

The UI must not present speculative editorial scores as verified retention probabilities, imply that a model has checked facts when it has not, or show unavailable video-generation integrations as working.

## 2. Recommended navigation

Primary tabs (proposed):
1. **Projects** — list, stage, language, last saved, warnings, resume.
2. **Stories** — topic intake, candidates, deduplication and editorial comparison.
3. **Evidence** — factual claims, supporting/conflicting sources, review actions.
4. **Script** — original RU/UA writing, alternative openings, versions and approvals.
5. **Scenes** — storyboard, narration, timing estimates, image/video briefs and continuity.
6. **Production** — assets, providers, credits, render/QA/export (current functionality and future features clearly marked).
7. **Results** — optional own-channel analytics and recommendations, not available before authorized integration.
8. **Settings** — UI/content/TTS/subtitle locales, project paths, privacy, provider approvals, limits and rights.

For MVP, show a **guided workflow with a persistent stage rail**; the advanced tabs can progressively expose detail without overwhelming first-time users.

## 3. New-project screen

Minimum fields:
- Project title (can be generated from topic; editable).
- **Genre:** history/biography; science/technology; education; culture; fiction; current events; custom. Genre is not a permanent lock; changing it prompts review of affected rules.
- **Content mode:** factual / fictional / hybrid. Display contextual explanation and source requirements.
- **Content language:** Russian / Ukrainian.
- **Narration language** and **subtitle language:** explicit; default to content language but editable, with mismatch warning.
- **Output goal:** 9:16 vertical, 16:9 landscape or custom; target duration (estimate).
- **Audience and style:** optional presets; editable editorial angle.
- **Intended use:** personal test / commercial intended; commercial intent triggers stronger rights gate, not automatic clearance.
- **Start from:** topic text, manual URL, user files (with permission), or a future approved source connector.

Suggested defaults for the **first vertical slice**, not yet a user-approved format: local processing, factual mode for factual genres, human approval at editorial gates, vertical 9:16 short, no cloud calls and no publication. A fiction genre may default to fictional mode but the user sees and confirms it.

## 4. Screen-by-screen flow

### Screen S1 — Candidate discovery and shortlist
- Input: `What should this video be about?` / paste URL / import permitted source.
- Cards show: title, one-line angle, genre, source count (not credibility score), freshness date if known, duplicates, rights/research warnings and six-factor **editorial** rubric.
- Actions: `Add idea`, `Research`, `Compare`, `Reject`, `Select for review`.
- If offline/no search: manual intake and provided sources work; do not show invented internet results.
- Empty state: “Нет кандидатов. Добавьте тему или ссылку”; unavailable connector marked `Not connected`, not “0 results” if never queried.

### Screen S2 — Evidence review
- Left: atomic factual claims, each with status `Unreviewed/Supported/Disputed/Unverified/Qualified/Removed`.
- Right: exact source metadata, links, relevant permitted excerpts, for/against relationship, dates, missing information.
- Actions: `Open source`, `Mark for verification`, `Qualify`, `Remove claim`, `Approve evidence review`.
- Prominent warning when a material claim has no source or contradictions remain. AI suggestions must be labelled **suggested**, not confirmed.
- Fiction mode: no fabricated citations; real-world factual assertions remain reviewable.

### Screen S3 — Editorial brief
- Inputs: central idea, audience promise, what is known/unknown, tone, format, duration target, genre profile, style, visual feasibility, source/rights limitations.
- Show **editorial score breakdown** separately from evidence confidence and production cost.
- Actions: `Change angle`, `Save brief version`, `Approve brief`.

### Screen S4 — Script editor
- Main panel: structured script segments, word/character counts and estimated duration.
- Side panel: linked claim IDs and evidence status, alternative openings, pronunciation, locale and version history.
- Actions: `Generate draft` (only through an approved configured provider/local model), `Rewrite segment`, `Compare versions`, `Edit manually`, `Request factual review`, `Approve script`.
- A rewritten sentence that changes a material claim invalidates only dependent factual approvals. No invisible overwriting of approved text.
- Draft variants are not labelled “A/B winner”; they are alternatives pending actual testing.

### Screen S5 — Storyboard / scene planner
- Per-scene card: scene number/stable ID, narration, claim links, estimated duration, visual description, still/AI video/imported video option, reference images, characters and rights.
- Actions: `Split scene`, `Merge`, `Reorder`, `Choose media strategy`, `Approve scenes`.
- Show actual **Sprint 26 compatibility**: current `first_video.py` accepts 1–20 scenes, RU/UA, still images and WAV/Silero; AI MP4 scene requests need a future renderer or explicit still-image fallback.
- Character consistency and multi-scene continuity are future checks, not claims of current capability.

### Screen S6 — Production handoff
- Preflight table: editorial approvals, content language, narration voice, number of scenes, image filenames, WAV/local TTS readiness, asset rights, output path, cloud consent, estimated spend.
- Actions: `Export editorial package`, `Prepare Sprint 26 plan`, `Render locally` (only when compatible and supported), `Return to scenes`.
- If provider quota unavailable: offer `Import manually generated media` or `Use approved still-image fallback`, never secretly switch to paid.
- Preserve existing overwrite protection: new output directory by default.

### Screen S7 — Quality review and results
- Review: video playback, narration, subtitles, factual/rights status, output metadata, watermark, codec, rendering warnings.
- Actions: `Approve export`, `Save for later`, `Export MP4/SRT`, `Publish manually`.
- Platform publishing and analytics tabs remain labelled **planned/unavailable** until explicitly implemented, tested and authorized.
- Future results: own-channel metrics with collection date, source, missingness, comparison limitations and human-reviewed improvement suggestions.

## 5. Persistent UX components

**Stage rail:** `Idea → Evidence → Brief → Script → Scenes → Production → QA` with status: `not started`, `draft`, `needs review`, `approved`, `blocked`. Clickable prior stages preserve data.

**Evidence badge:** count of unresolved material claims, source conflicts and reviewer decisions. Never compress this into an unexplained “trust percentage.”

**Approval drawer:** what is being approved, exact revision, remaining warnings, effect of approval and a clear `Approve / Return / Reject` choice.

**Rights & costs panel:** intended commercial use, asset source, current rights verification, selected provider, free quota verification timestamp and spend estimate. Unknown remains unknown.

**Activity history:** version changes, stage transitions, generation jobs, manual overrides and reasons; avoid recording private secrets.

**Offline indicator:** separate `local ready`, `online services unavailable` and `source search not configured`; don't block local workflow.

## 6. Interaction modes

| Mode | Intended behavior | Approval policy |
|---|---|---|
| **Manual** | user writes, sources, selects and imports; assistant optional | all editorial decisions explicit |
| **Guided (recommended MVP)** | system proposes candidates, source links, script variants and scenes | user approves story, evidence/script and production |
| **Automatic draft (future opt-in)** | system may progress through reversible draft stages using approved local tools | must stop for factual/rights gates, external uploads, new provider, spending and publication |

**No “one-click autonomous publishing” in first version.** If users later request automation, add a policy editor with explicit limits, preview, dry-run and revocation.

## 7. Two representative user journeys

### Journey A — Factual science explainer
1. User chooses `science_technology`, `factual`, `uk`, 9:16, manual topic.
2. Adds one or more permitted references; source metadata appears in Evidence.
3. AI proposes claims; user reviews source relations and qualifies uncertainty.
4. System drafts original Ukrainian script; user adjusts wording and approves the version.
5. Scenes are planned with still images and Ukrainian narration; current Sprint 26 compatibility checked.
6. User chooses approved local TTS or supplies WAV and images; exports through existing pipeline after a future integration adapter is built.
7. Video QA checks subtitles, rights and media; manual publishing is separate.

### Journey B — Original fictional short
1. User chooses `fiction_storytelling`, `fictional`, `ru`.
2. Enters plot and characters directly; factual research can be skipped for purely fictional elements.
3. System helps structure conflict and resolution; user approves script and scene plan.
4. Fictional framing is preserved; if real persons/events are referenced, corresponding claims/rights receive review.
5. Media strategy can fall back to still images; user manually imports generated media from a permitted service.
6. Local export and review follow the same pipeline as Journey A.

These are **proposed workflows**, not claims of existing end-to-end GUI functionality.

## 8. UX error handling and recovery

| Event | UI behavior |
|---|---|
| Source link unavailable | mark source unavailable, preserve metadata, request alternative; don't invent evidence |
| Contradictory factual sources | show both, block unsupported certainty, offer qualification or human review |
| User edits approved script | create new revision; display affected approval invalidations |
| Cloud quota unknown/exhausted | display unknown/exhausted separately, offer manual or local fallback |
| Genre switched mid-project | preserve content, re-evaluate genre rubric and affected approvals |
| 21 scenes for Sprint 26 | explain current 20-scene limit, offer manual split into separate productions or revise plan; no silent deletion |
| Video clip in still-only renderer | mark unsupported and offer approved still-image alternative |
| Wrong TTS language | explicit mismatch warning/block; no silent voice substitution |
| Windows path with Cyrillic | preserve original text, validate safe relative references, show actionable path errors |
| Process interrupted | resume last saved valid state; do not duplicate paid requests or overwrite files |
| Rights unknown for commercial use | block commercial approval until reviewed |

## 9. Accessibility and localization requirements

- All UI strings and editorial templates use separate RU and UK locale packs; test pluralization, Unicode, long titles and error messages.
- Keyboard navigation, readable labels and visible focus; no critical state indicated by color alone.
- Clear distinctions between `not implemented`, `not configured`, `not authorized`, `unverified` and `failed`.
- Provide user-readable explanations for scoring and evidence flags; allow manual override with audit record where legally permissible.
- Never make the user re-enter already saved sources, approved versions or manually imported media after an unrelated failure.

## 10. MVP UX acceptance tests (future)

1. A user starts from manual topic without any cloud API or internet access.
2. Changing genre changes rubric/templates but does not change production identity or delete content.
3. An unverified factual claim blocks script approval; fictional plot does not require fake citations.
4. User can compare script revisions and see exactly which approvals need renewal.
5. RU/UA narration/subtitle language settings remain explicit; wrong-language TTS cannot silently proceed.
6. A compatible 1–20-scene still-image plan is exportable via a future adapter without modifying schema v3.
7. User can see when AI video is **not yet supported** by current renderer.
8. A provider with unknown terms cannot be activated for commercial generation; paid calls require approval.
9. Local files, edits and project state survive offline interruption; publication is never automatic.
10. Results/analytics never display invented retention values or imply access to other creators' private data.

## 11. Design decisions awaiting user approval

- Initial UI: guided workflow (recommended) versus advanced dashboard first.
- Whether default video format should be 9:16 or project-selectable with no default.
- Which optional genres appear on the first screen; all remain supported by the universal model.

**Implementation status:** UX design only. No GUI screens, adapters, source connectors or analytics integrations have been implemented as a result of this document.
