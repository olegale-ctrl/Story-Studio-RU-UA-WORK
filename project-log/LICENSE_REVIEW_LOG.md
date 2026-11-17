# LICENSE REVIEW LOG

| Компонент | Источник | Лицензия | Статус | Основание/следующий шаг |
|---|---|---|---|---|
| Историческая локальная копия Story Studio (точный состав требует аудита) | https://github.com/konlu/story-studio | MIT, Copyright (c) 2026 konlu (архивная редакция) | HISTORICAL / NOT RELEASE-CLEARED | Не переносить оценку архивной лицензии на pinned 2026-11-03 версию или чужие данные |
| Pinned original Story Studio `87c2bbf...` от 2026-11-03 | https://github.com/konlu/story-studio/commit/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1 | CC BY-NC-SA 4.0 | NONCOMMERCIAL REFERENCE / COMMERCIAL BLOCKED | Нужна независимая проверка происхождения каждой части и прав на изменения, корпус и компоненты |
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


## 2026-11-04 — Codex review handoff (documentation only)
- Изучены зафиксированные исходники, локальный `history_tool.py`, метаданные 57 исторических сюжетов, файлы Writing-DNA, видеомодуля и тесты. См. `docs/UPSTREAM_DEEP_AUDIT_2026-11-04.md`.
- Chinese corpora и Writing-DNA: **REPLACE / BLOCKED** для RU/UA runtime и коммерческого релиза. Отчёт не переносит исходный контент и не меняет чьи-либо права.
- Не выполнены внешние проверки ToS новых сервисов, лицензий весов и всех зависимостей. **Никаких APPROVED** на основании аудита не выдаётся.
