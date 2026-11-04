# LICENSE REVIEW LOG

## 2026-11-04 — Codex research: evidence, без новых разрешений на интеграцию

- Сводка версий/прав: [EXTERNAL_TECHNOLOGY_MATRIX.md](../docs/research/EXTERNAL_TECHNOLOGY_MATRIX.md). Статус ADOPT не присвоен ни одному внешнему компоненту.
- Текущий upstream объявляет CC BY-NC-SA 4.0, но LICENSE сокращён/изменён относительно стандартного текста. Коммерческий перенос покрытых материалов BLOCKED; историческая MIT-запись ниже не является clearance текущего snapshot. Подробности и первоисточники: [UPSTREAM_AUDIT.md](../docs/research/UPSTREAM_AUDIT.md).
- ViralIQ: all rights reserved для кода, заявленные NC-условия данных/derived artifacts; коммерческий перенос требует разрешения.
- У YosukM, retention-clipper, C09 и D²Co в проверенных trees не найден LICENSE; публичная доступность не даёт подтверждённого grant. C01/C07 заявляют MIT только в README, полный grant/provenance не подтверждён.
- MIT/Apache исходников keepwatching, Analytics, packaging helpers, Beyond Views, GrowthBook SDK/stats и других кандидатов не распространяется автоматически на данные, веса, изображения, шрифты, API/output. GrowthBook Enterprise directories имеют отдельные условия.
- Оригинальные неподтверждённые названия не включены в интеграционные рекомендации. Китайские корпуса/DNA/референсы сохраняют REPLACE/BLOCKED policy.
- Публикуются только оригинальные Markdown-отчёты с citations; чужие корпуса, данные, веса, медиа и библиотеки в эту ветку не добавляются. Это исследовательская оценка, не юридическое заключение.

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
