# E01.1 — типизированная модель редакционного ядра

Дата: 2026-11-04. Статус: готово к проверке владельцем, не разрешение E01.2.
База ветки feat/editorial-e01-1-model — main Sprint26, e1f4efb0fb5ff290bb198349213c004b4667ef0f. История документационной ветки не переносилась.

## Вход и scope

Прочитаны утверждённые E00/1 и E01 plan, feasibility audit и MVP plan из docs/editorial-e00-2026-11-04, commit e520648411b99264688ff66dc61ad0e974201ed3. Пользователь разрешил только E01.1 и четыре файла: editorial/__init__.py, editorial/model.py, tests/test_editorial_model.py и этот отчёт. Существующие журналы не редактировались, чтобы соблюдать этот allowlist.

## Реализация и публичный API

- ContentMode, Locale, ObjectKind, ApprovalDecision, RightsStatus, ClaimType, EvidenceRelation — enum со значениями контракта E00.
- RevisionRef — kind, UUID id, positive integer revision, supplied hash. Проверяется только формат hash, он не вычисляется и не сверяется с payload.
- EditorialRevision — общий immutable заголовок, не универсальный полноценный payload любого kind.
- ProductionRevision, SourceRevision, ClaimRevision, EvidenceLink, RightsReview, ApprovalRecord — небольшой первый набор typed values; обязательные базовые поля и типы проверяются конструкторами.
- EditorialSnapshot — минимальный in-memory envelope с production_id, generation, editorial_schema_version=1 и immutable tuples revisions/approvals/active_refs.
- Violation(code, field_path, message, object_ref) и ModelError(ValueError) с полем violation — структурированная диагностика. Конструктор Violation для некорректной самой диагностики поднимает ValueError/TypeError.
- Открытый список __all__ в editorial/__init__.py; импорт не вызывает I/O, сеть, процессы, модели или существующий видеоконвейер.

Enums передаются как enum instances; raw strings не преобразуются неявно. UUID — canonical lowercase hyphenated string. Номер revision/generation строго int>=1, bool/float/строки не принимаются. Tuple-поля не принимают mutable list/dict. Все редакционные dataclasses frozen; строки и вложенные значения не нормализуются молча.

Это обычная неизменяемость Python frozen dataclasses для поддерживаемого API, не security boundary против object.__setattr__ или привилегированного изменения процесса.

## Намеренно минимальный контракт и вопросы интеграции

E00 не пересматривался. Полной реализации всех полей E00 в этой подзадаче нет, что разрешено заданием при чрезмерном размере модели. Текущий envelope — внутренняя модель, **не JSON wire schema**. Перед codec нужно явно отобразить revisions по kind в отдельные коллекции envelope E00; нельзя незаметно заменить нормативный формат одной общей JSON-коллекцией.

Перенесены на отдельное согласование модели: конкретные Candidate/GenreProfile/Script/ScenePlan/Asset payloads, Event и active selection slots, дополнительные source metadata, claim review/qualification, optional rights expiry. Их kind уже именуется enum, но EditorialRevision(ref) не означает полноту объекта. Source.locator — минимальное значение; будущая wire-модель должна явно различить URL и local locator, без автоматического fetch.

Даты, intended_use/output_preset/materiality пока проверяются как обязательные строки; их полная семантика, временные/профильные/языковые policy checks не считаются реализованными. В частности модель может представить language mismatch для последующей диагностики, но не утверждает его пригодность к handoff. Полный material claim review и grant rights не реализованы.

RightsReview содержит subject_id/revision и material_digest, без обратной полной хэш-ссылки на source/asset; это сохраняет E00 решение об исключении цикла. Hashes/digests пока supplied values. Не реализованы graph integrity, approvals authority/invalidation, source verification, stage, hash вычисление, JSON, store, CLI, render или AI.

Вопрос перед E01.2: утвердить минимальные concrete payloads и wire mapping. Если codec планируется для полного E00 envelope, сначала нужна отдельная небольшая задача дополнения типов. Не выдавать incomplete header-only objects за готовые сериализованные Script/ScenePlan. Это отложенная полнота, а не новое решение архитектуры.

## Выполненные проверки

Команда: `.venv/bin/python -m unittest discover -s tests -p test_editorial_model.py -v`.
Результат: **22 tests, OK**, 0 failures/errors. Покрыты valid values, invalid enums, обязательные поля/типы, zero/negative/bool revisions, UUID/hash shape, immutable nested tuples, diagnostics, empty fictional evidence и отсутствие преждевременной graph/gate логики.

Import test запускает новый interpreter с -B и audit hook: запрещает writes, socket/process/filesystem mutations; разрешает read файлов для импорта. Проверяется отсутствие core/scripts/torch/numpy/requests/ffmpeg/silero/json/hashlib среди импортов. Это проверка данного import path, не формальное доказательство поведения любого будущего кода.

Совместимость проверена отдельно через unittest discovery трёх конкретных существующих файлов:

| Файл | Tests |
|---|---:|
| tests/test_project_schema.py | 21 |
| tests/test_sprint26.py | 5 |
| tests/test_cli.py | 5 |
| Итого | **31, OK** |

Существующий Sprint26 test создаёт временный project из синтетических WAV без render. Полный suite, реальный MP4, Silero, GUI и Windows запуск не выполнялись и не объявляются успешными. Новые зависимости не устанавливались.

## Изоляция и откат

Изменены только четыре разрешённых файла. core, scripts, integrations, locales, зависимости, lockfiles, CI, schema v3 и upstream gitlink сохранены. Полные задачи E01.2–E01.6 не выполнялись; тесты текущих конструкторов относятся к E01.1, не к будущему codec.

Откат — revert изолированного коммита этой ветки; пользовательские проекты и outputs не трогаются. Merge main/PR5/PR6, изменения E00-ветки, релиз и публикация видео не выполняются. После результата остановиться и ждать проверки владельца.
