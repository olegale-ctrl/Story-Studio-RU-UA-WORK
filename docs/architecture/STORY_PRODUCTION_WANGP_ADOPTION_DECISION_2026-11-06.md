# Story Studio RU/UA — архитектурное принятие идей WanGP

**Дата:** 2026-11-06. **Статус:** APPROVED CONCEPT (владелец согласовал все перечисленные направления). Это не утверждение новых JSON/API контрактов, реализации, коммерческой лицензии или выпуска.

**Основание:** самостоятельный анализ [WanGP](https://github.com/deepbeepmeep/WanGP) на commit `bd1ff5903cbc18b46c3cce3b75bd140870b536a2`, документация [Showrunner](https://github.com/deepbeepmeep/WanGP/blob/bd1ff5903cbc18b46c3cce3b75bd140870b536a2/docs/SHOWRUNNER.md), [Media Flow](https://github.com/deepbeepmeep/WanGP/blob/bd1ff5903cbc18b46c3cce3b75bd140870b536a2/docs/MEDIA_FLOW.md), [API/MCP](https://github.com/deepbeepmeep/WanGP/blob/bd1ff5903cbc18b46c3cce3b75bd140870b536a2/docs/API.md), [Workspaces](https://github.com/deepbeepmeep/WanGP/blob/bd1ff5903cbc18b46c3cce3b75bd140870b536a2/docs/WORKSPACES.md), [LICENSE.txt](https://github.com/deepbeepmeep/WanGP/blob/bd1ff5903cbc18b46c3cce3b75bd140870b536a2/LICENSE.txt), blob `8e51ce4143ab472e3835ccc5e5f3e71e385f8770`. **Перенимаются идеи и требования, не код/модели/веса/оформление WanGP.**

## 1. Постоянные ограничения и границы

- Основная среда: Windows 10/11, Intel integrated graphics, **CPU-only обязателен**; NVIDIA/GPU, интернет, платные API и WanGP — только необязательные ускорители. Никакого обещания практической WanGP video inference на базовом ПК.
- `ru` и `uk`, независимые локали/промпты; TTS Edge/Silero и все иные голоса — только по их отдельным правам, с повторным license gate перед коммерческим выпуском. Китайские Writing-DNA/корпуса не переносятся.
- Story Intelligence рекомендует, Creative Engine готовит, Production Brief передаёт, но никто из них не выдаёт editorial approval, права, publish permission, CommandGrant/GateDecisionGrant. UI-кнопка «утвердить дубль» не эквивалентна защищённому RECORD_DECISION(APPROVE).
- E00, A1–A14, O1–O10, D1–D12, approved S1 и S2.1–S2.4 неизменны. `PUBLISH_REVISION` DISABLED, partial COMMIT reconstruction OFF. S3.1 на `2cd694ece9fa3806bcfbdd1e92f34a9c773b7aef` остаётся **design-only PROPOSAL**; Q1/Windows profiles/S3.2 не утверждены.
- Media, кэши, модели, веса, защищённые артефакты, голоса, токены и ключи — вне Git. Черновое media/workspace storage физически и логически отделено от protected editorial storage.
- Offline/missing provider/rights denied → ясный отказ или легальный CPU fallback, но не silent substitution и не fabricated success.

## 2. Целевая цепочка

```text
Discovery → Evaluation → Creative Engine → Production Brief (versioned)
  → Shot Production Manager (storyboard, chapters, human plan review)
  → Cast / Place / Voice / Style references
  → Provider Preflight → Queue → Shot Takes → Review
  → Timeline + FFmpeg → Deep Review → Versioned Deliverable
  → separate editorial/publication authorization
```

Production Brief должен сохранять идентификаторы источников, утверждений, rights status, audience, language, duration, visual requirements и редакционные блокеры. Изменение фактов/прав возвращается на проверку, а не маскируется творческим монтажом.

## 3. Принятые направления WP-01–WP-16

**WP-01 — Showrunner/Storyboard.** Группировка по главам/сценам, этапы Brief → Plan → Review → Generate → Edit → Deliver. Человек видит и корректирует раскадровку, реплики, длительности, референсы и визуальные риски до генерации. Ручной режим без LLM обязателен. Утверждение плана — только creative review.

**WP-02 — Shot/Take model.** Stable shot ID, версии спецификации и промпта, planned/actual duration, selected take, hashes и provenance; несколько immutable дублей, preview, compare, approve-for-edit, redo, exclude и lock. Состояния/переходы и undo определяются отдельным закрытым контрактом. Locked shot не отменяет права или safety gates.

**WP-03 — Cast/Place/Voice/Style Bible.** Версионированные референсы персонажей, мест, объектов, костюмов/состояний, голосов и произношения; привязка конкретных ревизий к сценам. При изменении референса показывать затронутые сцены, не переснимать всё молча. Реальные лица, голоса, образцы и изображения требуют consent/rights checks.

**WP-04 — Точечная регенерация.** Граф `brief → shot spec → prompt/reference → media take → voice/subtitles → timeline → export`. При изменении инвалидируются только зависимые результаты, одобренные неизменённые сцены остаются. Кэш привязан к content hash, provider/model/settings и разрешениям. Новая длительность пересчитывает offsets. SHA доказывает идентичность bytes, но не права/достоверность.

**WP-05 — Video Quality Review / Deep Review.** Отдельные `FAULT` (измеряемый дефект), `CHECK` (подозрение), `EDITORIAL_REVIEW` (человеческая оценка). CPU-first: ffprobe/file/hash, длительность/размер, чёрные/зависшие кадры, silence/loudness/peaks, subtitle coverage/timing, cut joins и текст против утверждённого сценария. Visual continuity, lip-sync, face/voice similarity — опциональные анализаторы; not measurable ≠ fault. Каждая находка: shot/time, method, evidence, severity, remediation/retest. AI-визуальный анализ не удостоверяет научную истинность.

**WP-06 — Timeline/звук/титры.** Несколько дорожек, trim, transitions, fades, ducking, loudness, sync при сдвигах. Текст рисуется детерминированно, не поручается генеративной модели. Soft subtitles и burn-in как осознанные варианты, сохранение SRT. Preview/proxy не заменяет финальный export. Развивать имеющийся FFmpeg/v3 timeline, не вводить обязательный платный редактор.

**WP-07 — Версии и non-destructive restore.** Manifest каждого экспорта: ID, shots/takes, голоса, титры, параметры, provenance, hashes, фактические размеры/длительность. Compare v1/v2, выбор старого дубля, duplicate/restore как новая рабочая ревизия без стирания истории. Creative undo не может восстановить REVOKED editorial approval.

**WP-08 — Media Flow.** Длинные файлы: chunks, overlap, bounded RAM, batch, checkpoints, stop/resume, без перезаписи исходника; хранить intermediate/final и оригинальный soundtrack. Сверять source hash, tool version и settings перед resume. CPU FFmpeg фильтры в базе; outpaint/refocus/uncompress/HDR/AI upscale/interpolate — опционально через provider. Автоочистка не удаляет referenced/approved assets.

**WP-09 — Preflight/dry-run.** До дорогостоящего запуска проверять hardware, provider/model, inputs, locale/voice, rights/license, resolution/duration, disk/RAM, estimated cost/ETA (только при наличии данных), network/privacy, output adjustments. Dry-run не скачивает модели, не делает inference, не расходует кредиты и не пишет в protected storage. Повторять critical validation при submit; planned ≠ actual.

**WP-10 — Media Provider Registry.** Независимый versioned contract `capabilities/validate/submit/status/cancel/outputs` для stills, image edit, video, TTS/audio, postprocess и ручного импорта. CPU local stills/FFmpeg обязательны, внешние API/GPU — опциональны. Для provider/model вести версии, license, weights/ToS, region, costs, privacy, rights на outputs, supported hardware. Никакого скрытого выбора другой модели.

**WP-11 — Queue/recovery.** Job ID + exact request_id/payload binding, progress, cancel, receipts, final artifact identity. Повтор того же запроса после lost ACK возвращает прежнюю задачу; изменённые bytes → conflict. После restart допускается явный `unknown_after_restart`, но не silent paid resubmit. Progress/preview не является доказательством финального результата. Creative queue не заменяет защищённый S1 W0–W9.

**WP-12 — Workspaces/media bin.** Проектные пространства, галерея дублей, shared refs и dedicated folders, safe eject, явное delete, missing-file references без тихого удаления, переносимость проверенных relative paths, opt-in archive/protect, backup/restore с manifests. Автоархив выключен по умолчанию; retention не наследует неутверждённые Q1 quotas.

**WP-13 — Windows Manager/rollback.** Отдельная будущая возможность: pin Python/FFmpeg/TTS/optional model versions, checksums, CPU profile, offline setup без обязательного winget, диагностика, сохранение предыдущего runtime и rollback. Installer не откатывает protected editorial history и не обходит отдельные S3 service/update gates.

**WP-14 — Agent/API security.** Потенциальный versioned local API/MCP/CLI: opt-in, localhost/off by default, authentication/scopes, workspace isolation, safe path/size bounds, controlled upload/download, audit, credentials вне Git/logs. Агент не может отменять/читать чужие jobs без полномочия или делать generic protected writes. Skill templates — guidance, не authority; обновление по expected_revision. Remote hosting/Python sandbox требуют отдельного security review.

**WP-15 — WanGP optional provider.** Исследовать самостоятельный `WanGPProvider` через документированный API/MCP без vendoring, только после license/hardware/security/privacy проверки и реального Windows теста. WanGP не нужен для CPU-only MVP; отсутствие WanGP не нарушает работу. Совместимость API и моделей должна быть проверена на зафиксированной версии.

**WP-16 — Лицензии/коммерческие права.** WanGP Community License 2.0 — не MIT/Apache. Внутреннее использование и outputs допускаются по условиям; платное embedding, white-label, paid API/SaaS/OEM требуют отдельной письменной лицензии. При прямой продаже outputs действует правило атрибуции. §7.4 описывает, что независимая интероперабельность сама по себе не перелицензирует наш код. Все сторонние веса, модели, голоса и материалы имеют собственные условия. До коммерческого выпуска — актуальный provenance/rights/region/ToS audit и письменные разрешения где нужно. Это не юридическое заключение.

## 4. Приоритет и отдельное утверждение реализации

**P0 (CPU production MVP):** WP-01, 02, 04, 05 (technical subset), 06, 09, 10 (CPU), 11, 16. **P1:** WP-03, 07, 08, 12. **P2:** WP-13, 14, 15 и GPU/AI улучшения; не блокируют CPU-only MVP.

Полная разбивка на будущие задания и acceptance scenarios: [STORY_PRODUCTION_WANGP_IMPLEMENTATION_BACKLOG_2026-11-06.md](../tasks/STORY_PRODUCTION_WANGP_IMPLEMENTATION_BACKLOG_2026-11-06.md).

До любого кода или schema change нужен отдельно утверждённый Production Brief handoff, shot/take state machine, dependency graph, provider/job API и review/rights/security contract. Этот документ **не** разрешает Codex начать реализацию, не изменяет `main`, S3.1 или S1, не создаёт PR/merge/release.
