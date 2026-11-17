# Worklog Sprint 27 — License Audit (этап 1)

**Started:** 2026-11-16 (after Sprint 26 Windows validation passed)

## Sprint 26 Status Confirmation
- ✅ Full first-video pipeline executed on Windows with local Silero for both locales (RU/UK)
- ✅ 116/116 unit tests pass in .venv and system Python 3.15
- ✅ FFmpeg MP4 rendering with burned subtitles verified (h264 1280×720 @25 fps, AAC 48 kHz stereo)
- ✅ User-media (`--audio-dir` + `--images-dir`) run passed
- ✅ Vertical 1080×1920 render produced and verified
- ✅ Test suite: **352+6=358 tests pass** (350 unittest + 356 pytest with ASCII basetemp)
- ✅ Pipeline defect fixed: failed run no longer leaves partial output tree

## License Audit (этап 1) — Scope and Initial Findings

### Components Reviewed

| Component | Source | License | Status | Notes |
|---|---|---|---|---|
| **Root code Story Studio RU/UA** | Local project files | MIT (archived) vs CC BY-NC-SA 4.0 (upstream) | **ISOLATED** — upstream as git submodule, RU/UA code separate | 0001-0008 ADRs documented |
| **Silero Local TTS** | `integrations/silero_local.py` + user `.pt` model | Model weights: user-provenance; Provider terms: CC BY-NC-SA 4.0 (upstream) | **REVIEW REQUIRED** — model path ASCII-only on Windows, SHA256 verified, `trusted=True` mandatory | No model weights bundled |
| **edge-tts** | `scripts/first_video.py` / Voice Studio UI | MIT (package) / Microsoft ToS | **COMMERCIAL BLOCKED** — Microsoft Edge Read Aloud output rights not confirmed; experimental personal prototype only | Not for commercial distribution |
| **FFmpeg** | User-installed `tools/ffmpeg/bin/ffmpeg.exe` | GPL/other (user-provided) | **USER RESPONSIBLE** — not redistributed, not bundled | See `LICENSES/ARCHIVED_UPSTREAM_MIT_LICENSE.txt` |
| **Python dependencies** | pipenv/`requirements.txt` (implicit) | Various (PyTorch BSD-3, etc.) | **OK** — runtime deps are stdlib-only glue code; no third-party code in scene/timeline/MP4 glue | 349/356 passed tests stdlib |
| **Assets — sponsor QR codes** | `assets/sponsor/alipay.png`, `wechat-pay.png` | User-provided | **USER CLEARANCE REQUIRED** — not upstream, not for redistribution | README instructions included |
| **Gradient PPM frames** | `scripts/first_video.py` → `make_background()` | Original project | **APPROVED** — new project material | Now generates 540×960 for vertical, 640×360 for default |
| **Sample texts (RU/UA)** | `examples/first_video_plan_*.json` | Original project | **APPROVED** | New RU/UA prompts, not corpora |
| **FFmpeg render output** | `output/first-video-uk/first-video.mp4` | User-side result | **OK** — one-off MP4, not redistributed | |

### BLOCKED / REPLACE Items (per LICENSE_REVIEW_LOG.md)

| Item | Current Status | Next Step |
|---|---|---|
| Chinese Writing-DNA/corpora | BLOCKED — LICENSE REVIEW | Установить первоисточники и разрешения (не импортировать) |
| Upstream CC BY-NC-SA 4.0 | BLOCKED for commercial | Per-component provenance required before Professional/Cloud |
| Silero model weights | Subject to model provenance/terms | User loads `.pt` from trusted source; no bundling |
| edge-tts commercial use | BLOCKED | Azure Speech paid tier recommended for commercial |

### Action Items — Sprint 27 (License Audit)

1. **Fill DEPENDENCY_LICENSES.csv** — populate all runtime dependencies
2. **Complete ASSET_REGISTER.csv** — fill remaining `REVIEW REQUIRED` rows
3. **Generate THIRD_PARTY_NOTICES.md** — formal notices per component
4. **Document licensing decisions** in LICENSE_REVIEW_LOG.md (already in progress)
5. **Verify Silero model SHA256** matches known good copy (already in code)
6. **Audit edge-tts integration** — document experimental status and commercial gate
7. **Check if pytest/silero/binaries** need explicit licensing entries

### Deliverables
- [ ] DEPENDENCY_LICENSES.csv — complete with all packages + versions
- [ ] ASSET_REGISTER.csv — all media assets reviewed
- [ ] THIRD_PARTY_NOTICES.md — formal copyright/license notices
- [ ] Updated LICENSE_REVIEW_LOG.md — all decisions documented
- [ ] Roadmap status: Stage 1 Лицензии → update to COMPLETED or next pending item

### Roadmap Impact
Upon completing этап 1 лицензий: переход к этапу 2 (Архитектура) с документацией контрактов и ADR-0009 (License and Compliance).