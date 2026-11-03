# Upstream Story Studio — technology import (2026-11-03)

## Provenance and frozen baseline

Source repository: https://github.com/konlu/story-studio

Source revision: `87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1` (upstream `main` at import time).

Imported files: **40**, preserved byte-for-byte under `upstream/konlu-story-studio/` without modifying upstream logic. Git blob SHA comparison against the source confirmed **40/40 exact matches** at the time of import.

## Included

- `modules/render-history-video/`: review, timing, speech alignment, motion, rendering, Jianying export and tests
- `modules/history-image/scripts/`: transcription and image/speech balance checks
- Selected technical documentation from `modules/history-image/references/`
- `scripts/`: runtime, voice settings, dependency installation and bootstrap tooling, diagnostics, Doubao voice adapter and related tests
- Top-level README, SKILL and selected workflow guidance
- Original upstream `LICENSE`, without alteration

## Excluded intentionally

- Chinese scenario corpora (`corpus/`), Writing-DNA files and large Chinese-language content examples
- Stock and example images, historically styled visual reference assets and sponsor/payment images
- Other third-party binaries, model weights and generated media
- Nonselected writing-specific files remain available in the **original upstream repository** for technical study; exclusion does not mean their workflow is irrelevant.

## License and commercialization gate — IMPORTANT

The current upstream `LICENSE` at the pinned revision is **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International** with `Copyright (c) 2026 konlu`, **not MIT**. It restricts commercial exploitation of licensed material and imposes attribution and share-alike conditions on sharing adaptations. Earlier local archives in this project label the original license as MIT; that older assessment **does not apply automatically** to this pinned source version. Research and noncommercial development only until the license conflict is resolved.

Status: **UPSTREAM REFERENCE / NONCOMMERCIAL-ONLY / NOT APPROVED FOR PROFESSIONAL OR COMMERCIAL RELEASE**. No implication that code or output may be monetized. A separate written license from the rights holder or independently developed replacement is required before commercial use of covered upstream components. Dependent tools (pyJianYingDraft, Coli/sherpa-onnx, FFmpeg, Pillow, NumPy, Doubao TTS etc.) have separate terms and must be audited.

## Integration precautions

All imported code is isolated inside `upstream/konlu-story-studio/`, **not automatically executed, installed, packaged or loaded** by the RU/UA application. In particular, bootstrap scripts may install/download external dependencies or use region-specific services; do not invoke without a separate review.

Next steps:
1. **DONE (2026-11-03):** Imported the verified local Sprint 25 RU/UA source into the main project tree without overwriting it with upstream code.
2. Compare interfaces of FFmpeg rendering, JSON timeline, TTS, subtitle alignment, Jianying/CapCut, and identify reusable designs/allowed modules.
3. Perform dependency/license review and implement RU/UA adapters with tests.
4. Keep Sprint 25.1 Voice Studio preview fix independent from this upstream import.
