# LICENSE REVIEW LOG

| Компонент | Источник | Лицензия | Статус | Основание/следующий шаг |
|---|---|---|---|---|
| Корневой код Story Studio | https://github.com/konlu/story-studio | MIT, Copyright (c) 2026 konlu | PRELIMINARY | Сохранить notices, проверить охват и другие лицензии |
| Китайские корпуса сценариев | Внутри исходного ZIP | Не подтверждена для каждого текста | BLOCKED — LICENSE REVIEW | Установить первоисточники и разрешения |
| Изображения и референсы | Внутри исходного ZIP | Не подтверждена для каждого файла | BLOCKED — LICENSE REVIEW | Реестр и проверка происхождения |
| Python/бинарные зависимости | Скрипты проекта | Не проверены | REVIEW REQUIRED | Извлечь manifests и версии |
| AI модели/облачные сервисы | Скрипты проекта | ToS и лицензии не проверены | REVIEW REQUIRED | Проверить отдельно веса и API |

## Sprint 04 update — 2026-10-30
- New `core/project_schema.py` and `core/subtitles.py` require only Python standard library. No third-party runtime dependency introduced by Sprint 04.
- No new APPROVED license decisions. `pyJianYingDraft`, `@marswave/coli`, `sherpa-onnx`, `websockets`, FFmpeg/MediaInfo and their transitive/downloaded components still require version-pinned primary-source evidence before redistribution.
- Chinese Writing-DNA/corpora and media remain REPLACE or BLOCKED for release; no copying into this update.

## Sprint 14
- New Python/PowerShell code and gradient images are original project additions. Windows SAPI voices are accessed from the user installation; voice availability and use terms depend on Windows/voice provider.
- Do not package third-party TTS voices, FFmpeg binaries or model weights. Commercial distribution remains gated on legal review.

## Sprint 15
- No third-party voice, FFmpeg binary, model weights or external media added. Existing release gates unchanged.

## Sprint 16: Edge TTS provider — OPEN / COMMERCIAL BLOCKED
- `edge-tts` Python package invokes the Microsoft Edge consumer Read Aloud endpoint. Package licensing and voice-output usage rights are separate issues.
- Microsoft does not publicly confirm commercial redistribution rights for Edge Read Aloud output. No commercial grant is inferred. See https://learn.microsoft.com/en-us/answers/questions/6007729/commercial-use-of-microsoft-edge-text-to-speech-vi and https://www.microsoft.com/licensing/terms/product/MicrosoftAzure/all .
- Experimental personal prototype only pending legal/provider review. For paid commercial use, evaluate Azure Speech paid tier or appropriately licensed local voices.

## 2026-11-03 — Upstream source license inconsistency
- The currently pinned upstream revision of `konlu/story-studio` carries CC BY-NC-SA 4.0, with noncommercial and share-alike terms.
- The local Sprint 25 archive carried an MIT license copy. Archived as historical evidence in `LICENSES/ARCHIVED_UPSTREAM_MIT_LICENSE.txt`; it is **not** a clearance for the pinned current upstream revision.
- Decision: isolate full upstream as Git submodule, keep separately imported technology files and provenance, BLOCKED for Professional/Cloud commercialization until valid rights are documented or new implementation replaces them.
- Third-party dependencies, model weights and output rights remain separately reviewable.



## Sprint 26 first-video MVP (2026-11-03)
- No additional Chinese upstream code, corpora or visual assets imported into RU/UA runtime. Original upstream remains isolated under the existing CC BY-NC-SA license gate.
- Generated gradient PPM frames and RU/UA sample texts are new project material; user-provided local images remain user's responsibility to clear for distribution.
- Local Silero weights and trusted PyTorch model execution remain subject to model provenance/terms; no model weights bundled. FFmpeg remains user-provided, not redistributed.
- No new third-party Python runtime dependency in the scene/timeline/MP4 glue code.

## Sprint 27 License Audit (2026-11-16) — этап 1
- **DEPENDENCY_LICENSES.csv populated** — 25 runtime Python packages catalogued (all MIT/BSD/Apache/PSF/HPND permissive). No GPL or copyleft dependencies in Python runtime.
- **ASSET_REGISTER.csv updated** — local project assets: `assets/sponsor/alipay.png` and `wechat-pay.png` (user QR codes, USER CLEARANCE REQUIRED, not for project redistribution). Upstream media assets remain BLOCKED/REPLACE per Sprint 04.
- **AI_MODELS_AND_SERVICES.csv populated** — three entries: Silero v5_cis_base_nostress (CC BY-NC-SA 4.0, non-commercial, local inference), Microsoft Edge TTS via edge-tts (package MIT, output COMMERCIAL BLOCKED), PyTorch 2.14.1 (BSD-3, APPROVED).
- **THIRD_PARTY_NOTICES.md written** — formal notices per component for redistribution compliance.
- **Silero model SHA256 verified in code** — `integrations/silero_local.py` pins `0405777e332906f0644e08a680f7cfdc2137ea864090079c1fdd30a43c1b8761` and enforces `trusted=True` + ASCII-only path on Windows.
- **edge-tts commercial gate confirmed** — Microsoft ToS does not grant commercial redistribution rights for Edge Read Aloud output; marked COMMERCIAL BLOCKED in all registries.
- **FFmpeg remains user-provided** — no binary redistribution; GPL concerns delegated to user.
- **Next:** BLOCKED items — Silero weights need commercial license or replacement; edge-tts needs licensed TTS alternative (Azure Speech or local); upstream CC BY-NC-SA materials need per-component provenance or replacement.
