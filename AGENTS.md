# AGENTS.md — Story Studio RU/UA

This is the repository-wide instruction file for Codex and other coding agents. The source of truth is **the actual code and Git history**, not a previous chat summary. See [project-log/CODEX_HANDOFF.md](project-log/CODEX_HANDOFF.md) for the current handoff.

## Goal and scope
Develop a Windows 10/11-first, local-first Russian/Ukrainian video-creation tool. It is a **substantial adaptation and independent rework**, not a literal translation, of [konlu/story-studio](https://github.com/konlu/story-studio). Support macOS/Linux is a future goal. Preserve working RU/UA functionality before replacing it. Separate UI locale, narration language, TTS language and subtitles; never silently substitute one language for another.

## Read according to the task
- First onboarding, architectural work or uncertainty about current state: `project-log/CODEX_HANDOFF.md`, `MASTER_PROMPT.md`, `project-log/DECISIONS.md`, and the relevant recent part of `project-log/WORKLOG.md`.
- Study of Chinese original: `docs/UPSTREAM_DEEP_AUDIT_2026-11-04.md`, `docs/UPSTREAM_TECHNOLOGY_IMPORT.md`, and the pinned `upstream/konlu-full` submodule. Read only relevant upstream files for the current question.
- Development tasks: relevant `core/`, `scripts/`, `integrations/`, `locales/` and `tests/`; check `README.md` for the current supported workflow.
- Releases, provider changes or licensing: `LICENSES/IMPORT_LICENSE_GATE.md`, `project-log/LICENSE_REVIEW_LOG.md`, and affected licenses/ToS.

Do **not** read the entire history for each small change. When documents disagree with working code, check the code and Git state and document the discrepancy. Never treat a prior claimed test as a test performed in this run.

## Non-negotiable safety and rights boundaries
- The pinned original revision `87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1` declares **CC BY-NC-SA 4.0**. An older archived MIT copy is NOT permission for all current content. Do not assume commercial-use rights. Verify provenance per file, model weights, dataset, API and transitive dependency. Preserve notices.
- `upstream/konlu-full` and `upstream/konlu-story-studio/` are **isolated reference material, not executable production dependencies**. Do not import, run, translate wholesale, redistribute or package Chinese corpora, Writing-DNA, visual examples, proprietary binaries or original scripts without rights and explicit approval. Reimplement general techniques independently with original RU/UA materials and tests.
- Never commit credentials, API keys, personal local paths, downloaded model weights, generated/private media, `.venv` or FFmpeg binaries. Do not perform paid requests, publish, release, merge to `main`, change licenses or install remote executables without explicit user authorization.

## Engineering and review standards
- Prefer minimal, reversible changes on a feature branch. Keep `main` and Sprint 26 functional. Existing PR #5 (`feature/sprint27-cpu-lipsync`) is an **unmerged experimental CPU/Wav2Lip adapter**; do not describe it as integrated or verified on Windows.
- Windows paths may contain Cyrillic characters. Use pathlib, UTF-8, safe quoting and PowerShell-native syntax. CPU-only execution must be supported where promised; GPU-dependent work is opt-in, never assumed.
- Use neutral project schema (v3) and explicit clip/media relationships. Keep local TTS and MP4 path stable. For any provider track version, code/weight license, price, output rights, regions and reproducibility. Do not silently switch providers.
- Validate untrusted inputs, path containment, duration, subtitles, overwrites and artifact provenance. Do not infer semantics or historical truth from a passing file hash.
- Keep tests focused and deterministic; run the applicable tests and report exact commands, outcomes and limitations. For Python: `python -m unittest discover -s tests -v` (but check whether a task also needs `python -m pytest -q tests`). Never claim successful Windows/media/GUI tests without actually running them.
- Document changes and unresolved gates in `project-log/WORKLOG.md`, `project-log/NEXT_SESSION.md`, `project-log/ROADMAP_STATUS.md`, `project-log/LICENSE_REVIEW_LOG.md` when substantively relevant; avoid rewriting old history. Add ADRs for decisions.

## User workflow
- There is ONE primary Windows installation (Sprint 26 baseline); Sprint 25.1 is backup. Future updates are **small incremental ZIP overlays for the existing project folder**, with `INSTALL_SPRINT_XX.txt` and changed-file list, never a new working folder per Sprint. Preserve `.venv`, `.tools`, weights and user output. Do not assert a downloadable ZIP exists unless created and verified.
- User currently requested an **audit/transition to Codex, not coding or installation**. First Codex assignment is read-only technical due diligence: verify upstream claims, compare to RU/UA baseline, test only safe offline paths if explicitly in scope, propose a staged modernization plan. Do not edit runtime code until a later explicit implementation task.
- Prefer concise Russian explanations to the user. Separate FACT (file+line/evidence), INFERENCE (plausible), and UNTESTED (requires execution).
