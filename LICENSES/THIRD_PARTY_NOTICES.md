# THIRD-PARTY NOTICES

Generated 2026-11-16 (Sprint 27 License Audit). This document summarizes third-party components used by Story Studio RU/UA and their licensing status for redistribution and commercial use.

---

## 1. Python Runtime Dependencies (vendored via pip)

All runtime dependencies are installed in the project's virtual environment and **not bundled** with the project source. They are listed here for compliance documentation.

| Package | Version | License | Commercial Use | Notes |
|---------|---------|---------|----------------|-------|
| aiohappyeyeballs | 2.7.1 | MIT | Yes | aiohttp dependency |
| aiohttp | 3.14.5 | MIT | Yes | Used by edge-tts |
| aiosignal | 1.4.0 | MIT | Yes | aiohttp dependency |
| async-timeout | 5.0.1 | MIT | Yes | aiohttp dependency |
| attrs | 26.1.0 | MIT | Yes | Various |
| certifi | 2026.10.23 | MIT | Yes | SSL certs |
| charset-normalizer | 3.x | MIT | Yes | aiohttp dependency |
| edge-tts | 7.3.1 | MIT | **BLOCKED** | Package MIT, but Microsoft Edge Read Aloud output has **no commercial grant**; see row 3 |
| filelock | 4.1.0 | MIT | Yes | Various |
| frozenlist | 1.8.0 | MIT | Yes | aiohttp dependency |
| fsspec | 2026.9.0 | MIT | Yes | Filesystem abstraction |
| idna | 3.20 | MIT | Yes | Domain handling |
| multidict | 7.1.0 | MIT | Yes | aiohttp dependency |
| networkx | 3.4.2 | BSD-3 | Yes | Graph algorithms (unused in current RU/UA code) |
| numpy | 2.2.6 | BSD-3 | Yes | Array operations (used by torch) |
| omegaconf | 2.4.0 | BSD-3 | Yes | Configuration (unused in current RU/UA code) |
| packaging | 26.3 | BSD-2/Apache-2 | Yes | Version parsing |
| pillow | 12.3.0 | HPND | Yes | Image processing (unused in current RU/UA code) |
| Pygments | 2.21.0 | BSD-2 | Yes | Syntax highlighting (unused) |
| PyYAML | 6.0.3 | MIT | Yes | YAML parsing (unused in current RU/UA code) |
| sympy | 1.14.0 | BSD-3 | Yes | Symbolic math (unused in current RU/UA code) |
| tabulate | 0.10.0 | MIT | Yes | Table formatting (unused) |
| tomli | 2.5.0 | MIT | Yes | TOML parsing (unused) |
| torch | 2.14.1+cpu | BSD-3 | Yes | PyTorch for Silero local inference |
| typing_extensions | 4.16.0 | PSF | Yes | Type hints |
| yarl | 1.25.1 | MIT | Yes | URL handling (aiohttp dependency) |

**Total runtime Python dependencies:** 25 packages (all permissive licenses: MIT/BSD/Apache/PSF/HPND). No GPL or copyleft dependencies in the Python runtime.

---

## 2. AI Models and Services

| Provider / Model | Version | Source | Terms / License | Commercial Use | Data Handling | Status |
|------------------|---------|--------|-----------------|----------------|---------------|--------|
| **Silero v5_cis_base_nostress** | 0.5 | silero-models (github.com/snakers4/silero-models) | CC BY-NC-SA 4.0 (model weights); MIT (python wrapper) | **Non-commercial only** | Local inference only; no network traffic | **REVIEW REQUIRED** — user must download `.pt` weights separately; code requires `trusted=True`; SHA256 pinned |
| **Microsoft Edge TTS** (via `edge-tts` package) | 7.3.1 | Microsoft (consumer Read Aloud endpoint) | Package: MIT; Output: Microsoft ToS | **COMMERCIAL BLOCKED** — Microsoft does not publicly confirm commercial redistribution rights for Edge Read Aloud audio output | Cloud API; text sent to Microsoft endpoint | **COMMERCIAL BLOCKED** — experimental personal prototype only; for paid commercial use, evaluate Azure Speech paid tier |
| **PyTorch** | 2.14.1+cpu | PyTorch Foundation | BSD-3-Clause | Yes | Local only | **APPROVED** |

---

## 3. FFmpeg Binary

| Component | Source | License | Commercial Use | Redistribution | Status |
|-----------|--------|---------|----------------|----------------|--------|
| FFmpeg | User-installed (`tools/ffmpeg/bin/ffmpeg.exe`) | GPL/LGPL (depends on build configuration) | User responsible | **NOT REDISTRIBUTED** — user provides own binary | **USER RESPONSIBLE** — project does not bundle or redistribute FFmpeg |

**Note:** The project assumes the user has a valid FFmpeg installation. The `core/mp4_render.py` prefers a local `tools/ffmpeg/bin/ffmpeg.exe` but falls back to PATH. No FFmpeg binary is committed to this repository.

---

## 4. Project Assets (local, not upstream)

| Asset | Path | Source | License | Commercial Use | Redistribution | Status |
|-------|------|--------|---------|----------------|----------------|--------|
| Alipay QR code | `assets/sponsor/alipay.png` | User-provided | User clearance required | User clearance required | **NOT FOR PROJECT REDISTRIBUTION** | **REVIEW REQUIRED** — donation QR code, user must clear rights |
| WeChat Pay QR code | `assets/sponsor/wechat-pay.png` | User-provided | User clearance required | User clearance required | **NOT FOR PROJECT REDISTRIBUTION** | **REVIEW REQUIRED** — donation QR code, user must clear rights |

**Note:** These QR codes are user content for donation links. They are **not** part of the video production pipeline and should not be distributed with the project.

---

## 5. Generated Assets (created at runtime, not distributed)

| Asset | Description | License | Notes |
|-------|-------------|---------|-------|
| Gradient PPM frames | Generated by `scripts/first_video.py::make_background()` | Original project material (MIT) | Created on-the-fly; not committed; aspect-ratio aware (540×960 for vertical, 640×360 for 16:9) |
| RU/UA sample texts | `examples/first_video_plan_ru.json`, `examples/first_video_plan_uk.json` | Original project material (MIT) | New prompts, not from upstream corpora |
| Output MP4/SRT | `output/*/first-video.mp4`, `output/*/*.srt` | User's responsibility | One-off rendering artifacts; not bundled |

---

## 6. Upstream Reference (isolated, NOT in runtime)

| Component | Source | License | Status |
|-----------|--------|---------|--------|
| konlu/story-studio (full) | Git submodule `upstream/konlu-full` | CC BY-NC-SA 4.0 | **BLOCKED** for commercial; isolated for reference only |
| konlu-story-studio (engineering snapshot) | `upstream/konlu-story-studio/` | CC BY-NC-SA 4.0 | **BLOCKED** for commercial; design/engineering reference |

**Policy:** No upstream Chinese corpora, media assets, or modules are imported into the RU/UA runtime. The upstream is kept as a pinned submodule and a byte-identical engineering snapshot for study and adaptation of proven mechanisms. All RU/UA code is independently written.

---

## 7. Summary for Distributors

| Can we redistribute? | Answer |
|----------------------|--------|
| Python source code (this repo) | Yes — MIT license (historical), but see upstream gate |
| Python runtime deps | Yes — all permissive (MIT/BSD/Apache) |
| FFmpeg binary | No — user provides own |
| Silero model weights | No — user downloads separately; weights are CC BY-NC-SA 4.0 |
| edge-tts audio output | No — commercial rights not confirmed |
| Sponsor QR codes | No — user content, not for redistribution |
| Upstream Chinese materials | No — CC BY-NC-SA 4.0, rights not cleared |

**Current release gate:** Community/non-commercial prototype only. Professional/Cloud commercialization blocked until:
1. Silero model provenance documented with commercial license
2. Edge TTS replaced with licensed TTS (e.g., Azure Speech, local alternatives)
3. Upstream CC BY-NC-SA materials either replaced or rights cleared
4. Full SPDX/CycloneDX SBOM generated

---

## 8. Compliance Checklist (per RELEASE_COMPLIANCE_CHECKLIST.md)

- [x] Dependency inventory complete (DEPENDENCY_LICENSES.csv)
- [x] Asset register complete (ASSET_REGISTER.csv)
- [x] AI models/services registry complete (AI_MODELS_AND_SERVICES.csv)
- [x] Third-party notices documented (THIRD_PARTY_NOTICES.md)
- [x] License review log updated (LICENSE_REVIEW_LOG.md)
- [ ] BLOCKED/REPLACE items resolved (Silero weights, edge-tts commercial, upstream)
- [ ] SPDX/CycloneDX SBOM generated
- [ ] Legal sign-off for any commercial distribution

---

*End of THIRD-PARTY NOTICES*