# План реализации первого Universal Editorial MVP

Дополнение E00 от 2026-11-04: принятые владельцем defaults закреплены в [финальной спецификации](EDITORIAL_E00_FINAL_SPEC.md). Ближайший ограниченный scope — [план E01](EDITORIAL_E01_IMPLEMENTATION_PLAN.md). Исторические альтернативы CLI/формата/хранения ниже не отменяют решений E00; реализация всё ещё требует отдельного разрешения.

Дата: 2026-11-04. Статус: **PROPOSED, реализация не разрешена**. Основание: [технический аудит](CODEX_EDITORIAL_FEASIBILITY_AUDIT.md), четыре архитектурных документа commit8e037d34391aaf3ed8b8c8d82f1d93c5b734cfae, код Sprint26 e1f4efb0fb5ff290bb198349213c004b4667ef0f. Ниже будущие файлы/команды/тесты, они не созданы этим заданием.

## Результат вертикального среза

Одна локальная production: профиль+mode+ru/uk → ручная тема/URL metadata → reviewed claims → ручной brief/script → approvals → сцены → immutable handoff → существующие WAV/изображения или уже установленный разрешённый Silero → MP4 с озвучкой и сценовыми субтитрами. Публикация видео не входит. Автогенерация текста и поиск не обязательны.

В первом handoff script/narration/subtitles должны совпадать. Иные языковые сочетания сохраняются как intent, но блокируют этот adapter. Factual/hybrid/fictional — отдельная ось от genre. Один pipeline для истории, науки и fiction.

## Предлагаемые файлы и интерфейсы

| Будущий файл | Ответственность / интерфейс |
|---|---|
| editorial/model.py и editorial/__init__.py | Typed sidecar data, decode/encode, strict validation, safe IDs, digest; без imports из upstream |
| editorial/store.py | load/save(expected_generation), single-writer lock, temp+replace, backup/recovery; только persistence |
| editorial/service.py | create/intake/review/version/approve/readiness; pure functions где возможно; логика mode/profile/gates |
| editorial/handoff.py | prepare_handoff(snapshot, media_inputs, target), validate_handoff; emit старого first_video plan и отдельного provenance manifest |
| scripts/editorial.py | Тонкий локальный CLI: будущие create/intake/check/save-script/approve/plan/export; разбор аргументов, structured errors |
| editorial/profiles/*.json | Версионные оригинальные history/science/fiction/custom profiles; литература/примеры не копируются из upstream |
| tests/test_editorial_*.py | Models, storage, evidence, revisions, handoff, CLI и focused integration |
| tests/fixtures/editorial/* | Только оригинальные малые synthetic fixtures; отрицательные evidence fixtures явно помечены |

JSON/SQLite/GUI одновременно не вводить. Для MVP authoritative JSON snapshot; SQLite лишь после измеренной потребности. Встроенный json/hashlib/uuid/pathlib/subprocess достаточен; schema validators сторонних библиотек не обязательны. Export first_video plan не является изменением timeline v3.

## Задачи с отдельными gates

| ID / приоритет | Работа | Зависимость | Проверки / критерий приёмки | Откат |
|---|---|---|---|---|
| E00 P0 | Согласовать F01–F14, model, locales, storage и формат | Review документов | Письменно определены default/profile/mode и границы approvals; нового кода нет | Исправить только спецификацию |
| E01 P0 | Sidecar model, profiles, canonical digest | E00 | round-trip UTF-8; unsupported version, duplicate IDs, invalid refs/types/NaN rejected; ru/uk, все три modes; неизвестные dates/rights сохраняются | Отдельный новый package не влияет на Sprint26 |
| E02 P0 | Atomic single-writer store + recovery | E01 | Fault injection до/после replace; stale generation; два writer процесса; corrupt primary/backup; old state остаётся readable, approval не меняется от неуспешного save | Открыть предыдущий проверенный snapshot, не понижать данные молча |
| E03 P1 | Ручной intake и evidence service | E01–E02 | Topic без sources разрешён как draft; URL не означает fetch/verify; supported требует human basis; dangling/contradicting evidence видимы; fiction не требует fake citations | Данные остаются в переносимом sidecar |
| E04 P1 | Brief+ScriptVersion, approvals и invalidation | E03 | Exact revision/hash и dependency digest; edit claim/source/profile/locale инвалидирует затронутый gate; текст без покрытия нельзя утвердить лишь по наличию claim_ids | Сохранить старые immutable revisions/decisions, выбрать старый coherent set только явно |
| E05 P1 | Ручное деление сценария на сцены, estimates | E04 | Exact ordered text spans, no omission/duplication; стабильные scene IDs; reordering/narration rewrite требуют новой script revision; still briefs и rights | Старый approved plan остаётся историческим |
| E06 P1 | Production handoff и media preflight | E05 | Только title/locale/scenes{text,image?}; 1–20 сцен, <=2000символов; safe image name; WAV index mapping; fresh output; unsupported MP4/locale rejected; v3 unchanged | Удалить только управляемый неутверждённый staging либо оставить failed attempt для review |
| E07 P1 | CLI-first guided flow и dry-run | E03–E06 | Все действия явны, bounded input; JSON error codes+human explanation; reopening/resume; offline без API; export не запускает render автоматически | CLI отдельный, существующие команды прежние |
| E08 P1 | Render bridge к существующему first_video.py | E06–E07 | subprocess argv с sys.executable, явные width/height/audio-or-model/voice; digest recheck; timeout/failure сохраняют editorial state; новые output attempt paths | Отсоединить wrapper, прямой старый first_video workflow работает |
| E09 P1 | Три cross-genre acceptance runs и Win10/11 | E08 | История RU, наука UK, fiction RU; source-backed факты, intelligible narration, captions, PNG/PPM fallback; actual durations/check/ffprobe; Unicode paths; без публикации | Доработка отдельной задачи, не merge всего пакета автоматически |
| E10 P2 | GUI wizard и optional drafting/ASR | Только новое разрешение после E09 | Отдельная UX/API/security/terms/model evaluation; не условие первого MVP | Новые adapters отключаемы |

Каждая задача — небольшой отдельный PR/коммит по согласованию; не объединять автоматом всю программу работ. Одобрение E00 не означает разрешения paid calls, моделей или publishing.

## Точные правила handoff

1. Load coherent approved snapshot и проверить production/policy/profile/claim/source/script/scene dependency digest. Snapshot IDs и approvals должны относиться к одной production.
2. Narratable text — точный утверждённый текст. Сцены ссылаются на segment ranges с определёнными offset units: Python Unicode code points, end exclusive, без неявной NFC-нормализации. UI UTF-16 offsets в будущем конвертируются явно; это требует тестов emoji/комбинируемых знаков.
3. Strict plan состоит только из существующих полей: title, locale, scenes с text и optional image. В sidecar остаются IDs, genre, claims, rights, visual briefs и estimates; extra fields не полагаются на permissive read_plan.
4. WAV files ожидаются voice1.wav, voice2.wav... по текущему порядку сцен. Manifest связывает scene_id/text hash/audio hash; после reorder старое audio нельзя автоматически принять. Существующий first_video не проверяет смысл WAV, поэтому человек подтверждает язык/соответствие.
5. Для изображений staging содержит уникальные safe filenames; один images_dir. Отсутствие картинки допускает текущий gradient fallback только как явное выбранное поведение. Video clips не передаются этому adapter.
6. Audio source ровно один: existing WAV либо уже установленная доверенная Silero model с совместимым voice. Не устанавливать torch, не скачивать веса. Параметр --silero-model в старом CLI означает фактическое доверенное исполнение; wrapper требует явное доверие пользователя до такого запуска.
7. Вызов существующего scripts/first_video.py argument list, без shell. Для target 9:16 задать, например, width720/height1280; прежний default landscape не менять. CLI никогда не получает неподдерживаемый --duration или translated subtitles.
8. Actual timing формируется из WAV плюс400ms, с выравниванием40ms/25fps. Сохранить project/output hashes и actual durations после успеха; estimate не заменяет измерение.
9. При отказе approved editorial snapshot остаётся неизменным; новый attempt directory для retry. Не удалять чужие output, не объявлять partial MP4 готовым; cleanup касается только файлов конкретного управляемого attempt после review.

## Три контрольных примера

| Пример | Данные и редакционный gate | Production acceptance |
|---|---|---|
| Документальная историческая история RU: начало книгопечатания | Оригинальный короткий текст, 3–4 сцены; каждый факт/дата с точным source locator и human review. Если источники пока не проверены — fixture остаётся draft, не выдаётся за completed evidence | Готовые лицензированные RU WAV либо разрешённый local voice; stills/градиенты, caption text соответствует утверждённому script |
| Научно-популярное объяснение UK: принцип термоса | 3–4 сцены, разделение теплопроводности/конвекции/излучения с источниками; запрет абсолютной фразы «тепло совсем не проходит»; условия/пределы отражены | UK narration/subtitles, measurement WAV durations, проверка произношения и смысла; без LLM/API |
| Оригинальная художественная история RU: потерянное письмо робота | 3–4 сцены, вымышленные персонажи и сюжет, no fake citations; вымысел обозначен. Если добавлен реальный научный факт — обычный evidence gate | Тот же renderer/контракт, original still briefs; никакой отдельный fiction engine не нужен |

Сюжеты — будущие acceptance specifications, не уже проверенные источники или готовые ролики. Synthetic tones годятся только для технического smoke, не для критерия понятной озвучки. Дополнительно обязателен hybrid отрицательный/положительный gate test: dramatization отмечена, factual claims проверены.

## Набор focused tests после разрешения кода

- Model: unknown enums/version; ids; cycle/foreign production refs; null vs0; texts; canonical hashes, Unicode exactness.
- Evidence: unsupported material fact blocks; qualified claim требует approved formulation; disputed claim не проходит от одного URL; fiction не создаёт доказательств вымыслу; claim removal не оставляет скрытый факт в script.
- Revisions: edit source evidence с неизменным script text; profile/mode/locale switch; stale approvals/scene plans; latest pointer против одобренной старой ревизии; no implicit reapproval.
- Store: full transaction under interruption, writer lock, stale recovery, backup validation, disk full/permission errors; latest manifest не ссылается на незаписанную revision.
- Handoff: 0/20/21 scenes, 2000/2001 code points, wrong media kind, missing/renumbered WAV, traversal/junction, existing output, odd dimensions, no TTS weights, wrong voice; exact scene text coverage.
- Render: small synthetic WAV offline smoke, schema check и полный MP4 decode. Это отдельно от реальных RU/UK audio acceptance. Failure после partial output не теряет сценарий и не перезаписывает прежний export.
- Existing regression: focused tests/test_sprint26.py, test_project_schema.py, test_mp4_render.py, test_subtitles.py, test_cli.py; полный existing suite один раз перед готовностью implementation PR, не повторять ради документации.
- Windows10/11: Cyrillic profiles/project path, длинные имена, reserved filenames, file-in-use при replace, rename/backup, FFmpeg path with spaces, locale UTF-8, реальные audio/video playback. macOS/Linux portability — без OS-specific imports домена; платформенные smoke отдельно.

## Минимальный UX

Сначала CLI или тонкий guided интерфейс: Create → Intake → Evidence → Script → Approve → Scenes → Export → явный Render. Показ exact revision, reason blocked, unsaved edits, current approval scope. «Не настроено», «не поддержано», «не проверено» и «ошибка» — разные состояния. Wizard S1–S7 и редактирование long-running jobs отдельны; Voice Studio не объявляется уже существующим редакционным GUI.

## Решения перед первой реализацией

Нужно согласовать E00: CLI-first или дополнительный GUI scope; single-writer JSON snapshot; язык subtitle=narration в первом adapter; explicit/default aspect; правила квалификации/допуска спорных facts и approvals; выбранные разрешённые WAV/voice assets для human acceptance. При отсутствии разрешённой реальной озвучки можно завершить технический smoke, но весь E09 не считается passed.

## Границы поставки

Никаких изменений core/project_schema.py v3 или existing renderer для этого MVP не требуется. Никаких внешних компонентов из прежнего исследования, новых зависимостей, paid API, интернет-поиска, AI clips, provider discovery, metrics/ML или upload adapters в первый slice не включать. Сохраняется одна Windows-установка, будущие updates только после проверки; Sprint ZIP сейчас не создаётся.

После review этих двух документов остановиться и дождаться отдельного разрешения на конкретные задачи реализации. Merge PR5/PR6, main merge, релиз и публикация видео этим планом не разрешены.
