# Codex handoff — Story Studio RU/UA
**Prepared:** 2026-11-04. **Scope:** read-only onboarding and future technical audit, *not* an implementation Sprint.

## Canonical repositories and current status
- Private working repository: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK
- Main Windows baseline: **Sprint 26**. User retains **Sprint 25.1** as a backup; do not make Sprint-specific replacement directories.
- Original Chinese source: https://github.com/konlu/story-studio at **`87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1`**, isolated as Git submodule `upstream/konlu-full`; 40 reference files separately preserved under `upstream/konlu-story-studio/`.
- Full license/rights clearance is NOT complete; original pinned source CC BY-NC-SA 4.0; see `docs/UPSTREAM_TECHNOLOGY_IMPORT.md` and `LICENSES/IMPORT_LICENSE_GATE.md`.
- Sprint 25.1 Windows Silero Voice Studio preview with `ukr_igor` was user-verified. Sprint 26 `scripts/first_video.py` prepares RU/UA scene-plan -> voice/WAV -> storyboard media -> MP4 with scene-level captions; Windows end-to-end verification must be independently checked, not assumed.
- **Experimental Sprint 27** exists only in OPEN PR [#5](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/pull/5) (`feature/sprint27-cpu-lipsync`). External Wav2Lip/checkpoint, compatible CPU environment, real inference and Windows tests are **not delivered/verified**. No Sprint 27 archive exists as an accepted installer.

## User-approved direction
The most valuable Chinese concept is **finding candidate stories, evaluating them for an audience, offering a human selection, and writing a compelling but factual narrative**. Before proceeding to talking faces and other expensive media experiments, perform a deep design/engineering review of that editorial pipeline and plan an original Russian/Ukrainian implementation. The overall Story Studio development is on pause until approval; preparing Codex documents is authorized, runtime changes are not.

## Key finding to verify
- Original `modules/history-writing/scripts/history_tool.py` ranks **local** `corpus/catalog.json` records by keyword relevance plus account/cluster diversity. It does not directly crawl the internet or compute a retention predictor.
- The historical catalog has **57 records**, all with null `source_url` and `published_at` in the reviewed pinned snapshot. There are **296 biography Markdown files** in the newer corpus. Writing-DNA documents contain editorial hypotheses about attention, not controlled retention studies.
- Original also has strong protection patterns in audio alignment, versioned media handoff, FFmpeg render and Jianying export. Do not characterize the whole original as a mere mock-up.
- See `docs/UPSTREAM_DEEP_AUDIT_2026-11-04.md` for evidence, candidate bugs, and uncertainty markers.

## Important files
- Product policy and releases: `MASTER_PROMPT.md`; project log: `project-log/WORKLOG.md`, `project-log/DECISIONS.md`.
- Windows first-video run: `docs/SPRINT26_FIRST_VIDEO_WINDOWS.md`; source: `scripts/first_video.py`.
- Neutral model and renderer: `core/project_schema.py`, `core/mp4_render.py`, `core/cli.py`.
- Locale/providers: `locales/ru/`, `locales/uk/`, `integrations/`, `scripts/run_voice_studio.ps1`.
- Source audit: `docs/UPSTREAM_DEEP_AUDIT_2026-11-04.md`, `docs/UPSTREAM_TECHNOLOGY_IMPORT.md`.
- Older `project-log/NEXT_SESSION.md` contains chronological entries from prior Sprints; **read the topmost current section first**. When modernizing this file, retain history or archive it, never silently delete it.

## First Codex task — READ ONLY
1. Inspect Git branch/working tree/submodule pointer and the code governing main status. Inventory user-facing functionality versus code and tests; distinguish implemented/scripted/agent-dependent/unverified.
2. Audit `history_tool.py`, biography selection DNA, original `SKILL.md`, evidence rules and corpus metadata. Map *discovery -> evidence -> editorial ranking -> human choice -> script -> validation -> media* with exact file/line references.
3. Try to falsify each major finding and identify actual code defects separately from architectural gaps. If tests cannot run, give precise blockers; do not install packages or touch external APIs just for this task.
4. Compare proposed approaches against existing local-first RU/UA implementation, constraints and licenses.
5. Deliver a ranked findings report: severity, evidence, reproduction or counterexample, risk, minimal remedy, and acceptance test; plus staged plan and issues/questions. **Do not change runtime code, merge PRs, create Sprint ZIPs, perform paid calls or publish.**

## For the user
Reply in Russian; report what was actually inspected and tested. Keep user choices to product priorities and approval gates. The future workflow is one main GitHub repo and incremental Windows overlays, not duplicate projects.
