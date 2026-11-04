# E01 — план реализации модели и проверок

Дата: 2026-11-04. Основание: [E00/1](EDITORIAL_E00_FINAL_SPEC.md). **Только план; код E01 не написан и разрешения реализации пока нет.** Шесть решений владельца зафиксированы, повторно спрашивать о CLI/JSON/языках/aspect/offline-first не требуется.

## Граница E01

Pure sidecar model, strict JSON encode/decode, canonical hashes, exact references, declarative profiles и контрактные тесты. Никаких persistent save/lock, CLI workflow, renderer/TTS вызовов, LLM, API, новых dependencies или изменений существующих core/scripts/locales. JSON snapshot и функции модели не означают готовое атомарное хранилище: это E02.

## Будущие файлы

| Файл | Назначение |
|---|---|
| editorial/__init__.py | Небольшой public API без side effects |
| editorial/model.py | Immutable values/revisions, enums, Envelope, RevisionRef, RightsReview, ApprovalRecord, errors |
| editorial/validation.py | Типы, bounds, integrity, text spans, refs; separation draft-valid и handoff-compatible |
| editorial/codec.py | Strict decode/encode bytes, canonical payload/hash/dependency digest; стандартная библиотека |
| editorial/profiles/history_biography.json, science_technology.json, fiction_storytelling.json, general_custom.json | Оригинальные versioned profiles, минимум полей E00; данные без plugins |
| tests/test_editorial_model.py | Domain constraints и references |
| tests/test_editorial_codec.py | Canonicalization, strict JSON, Unicode, hashes |
| tests/test_editorial_profiles.py | Общий контракт разных жанров |
| tests/fixtures/editorial/*.json | Малые оригинальные synthetic данные; никаких скачанных corpora/медиа |

Перечень не даёт права сейчас создавать эти файлы. В E01 не реализовывать store/service/handoff/GUI и не расширять schema v3.

## Предлагаемые интерфейсы

- decode_snapshot(raw: bytes) -> EditorialSnapshot: caps/strict parse/structural+referential validation; без записи, сети и исполнения plugins.
- encode_snapshot(snapshot) -> bytes: deterministic canonical JSON для interchange; не save и не durability promise.
- canonical_payload(revision) -> bytes; content_hash(revision) -> hex64: правила E00 §3, без автоматической правки содержимого.
- validate_snapshot(snapshot) -> tuple[Violation,...]: stable code, object_ref, field_path, message; no partial success при corrupted refs.
- dependency_digest(snapshot, gate, target_ref) -> hex64: exact graph closure, сортировка refs, policy и relevant production/profile refs.
- validate_text_partition(script, plan) -> tuple[Violation,...]: Unicode code point ranges, полное точное покрытие.
- check_first_video_compatibility(snapshot, plan_ref) -> tuple[Violation,...]: pure capability validation, не утверждение фактов/прав и не экспорт/запуск.

Approval decision semantics полным сервисом реализуются E04. E01 проверяет форму/ссылки/digests и предоставляет пригодные primitives, но не создаёт approved records автоматически. Hash и статус supported не доказывают фактическую истину. Renderer compatibility не равна editorial readiness.

## Малые задачи E01

| ID | Действие | Зависимость | Acceptance |
|---|---|---|---|
| E01.1 | Типы, enums, immutable revision envelope и violations | Утверждение E01 | Plain values без I/O/import side effects; bool не принимается как revision/int |
| E01.2 | Strict codec и лимиты | .1 | Duplicate keys, NaN/Infinity, unknown fields/schema, surrogate и oversized input отклоняются; UTF-8 и round-trip |
| E01.3 | Hash/ref graph | .1–.2 | Key order не меняет digest, текст/права/profile revision меняют relevant digest; отсутствующие/cross-production/cyclic/conflicting refs rejected |
| E01.4 | Profiles и locales/presets | .1–.3 | Три жанра+custom, три modes; ru и uk; UI locale отдельно; default720×1280, explicit1280×720; unsupported mismatch не «исправляется» |
| E01.5 | Pure ranges/capability validators | .1–.4 | Exact coverage, 20/21 scenes, 2000/2001 code points; no executable media calls |
| E01.6 | Fixtures, regression review и документация API | .1–.5 | Focused tests реально выполняются; существующие v3 bytes/CLI behavior не изменены; результаты и scope PR явно описаны |

Задачи согласуются как один ограниченный E01 scope либо отдельными небольшими commits; merge не выполняется без отдельного указания. Любое обнаруженное требование изменить runtime/core выносится за E01.

## Матрица тестов

| Случай | Ожидание |
|---|---|
| RU historical factual draft с неподтверждёнными claims | Структура draft допустима; capability не объявляет editorial approval |
| UK science с qualification и contradictory evidence | Обе связи сохраняются, exact source/claim refs; истина не решается codec |
| RU fiction без factual claims | Нет fabricated evidence; mode/profile не создают автоматического factual exemption для реально typed fact |
| Hybrid с factual и fictional segments | Раздельные типы/disclosure не теряются |
| revision0, bool, unknown mode/locale/schema | Структурная ошибка без coercion |
| Duplicate JSON key/id/ref, foreign production, missing source revision | Однозначная ошибка, без выбора последнего значения |
| Латинские/Cyrillic/emoji/combining code points | Exact text и offsets сохраняются, не NFC и не UTF-16 |
| Перестановка JSON keys | Тот же canonical hash |
| Изменение text/claim/source/policy/profile | Новый соответствующий hash/digest; старый approval не соответствует новому digest |
| Некорректный/подставленный content_hash | Ошибка integrity; не принимается из внешнего JSON на доверии |
| Scene gap/overlap/duplicate/reorder/additional text | Покрытие rejected, narration не переписывается |
| 0/20/21 сцен; whitespace-only; 2000/2001 символ | Явный compatibility result; большой draft не удаляется |
| script/narration/subtitle mismatch | Handoff несовместим; UI ru + script uk допустим при narration/subtitle uk |
| Указанное MP4 вместо still | Capability rejected; schema v3 не расширяется |
| Rights unknown/test-only с commercial intent | Данные сохраняются, readiness не получает grant от declared intent |
| Changed unrelated image vs changed material claim | Dependency selection различает factual SCRIPT и asset HANDOFF scope; политика фиксирована E00 |

Оригинальные fixtures — тестовые данные модели, не реальные источники и не одобренные сценарии. Нельзя назвать E01 полноценным fact-checker или production workflow по одному passing codec test.

## Проверки после отдельного разрешения реализации

Запустить targeted tests новых pure modules, затем текущие tests/test_project_schema.py, tests/test_sprint26.py, tests/test_cli.py как relevant compatibility checks. Полный existing suite — перед готовностью implementation PR, если это требуется общей проверкой. Не заявлять Windows/Silero/MP4 validation по Linux model tests. Никаких новых установок: использовать готовую среду; отсутствующие prerequisites сначала диагностировать.

На Windows проверить pure UTF-8/paths/import behavior; реальный lock/atomicity и interrupted-save tests принадлежат E02, WAV/TTS/FFmpeg — E08/E09. Для E01 portability сохраняется отсутствием OS-specific imports и файловых side effects домена.

## Definition of done и откат

E01 завершён только если разрешённый file allowlist соблюдён, model/codec/refs/profiles документированы, focused tests фактически прошли с точными counts, старый code/v3/CLI не изменён, нет сетевых/model/install side effects и private assets в Git. Reviewer проверяет хэширование без самоссылок и distinction draft/capability/approval.

Откат E01 — revert только новых изолированных model/fixture файлов/коммитов; старые пользовательские outputs/projects не удаляются. Не создавать persistent editorial workspace в E01, поэтому migrations/recovery пока не нужны. До store E02 нельзя обещать save/resume редакционного проекта.

## Следующий gate

Перед началом E01 требуется отдельное разрешение владельца на реализацию именно этого scope. E00 документально уточнён; это не запуск E01, не merge, не release и не публикация видео/облачной среды.
