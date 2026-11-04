# Технический аудит Universal Editorial Engine

Дата: 2026-11-04. Статус: архитектурная проверка, не разрешение реализации.

Дополнение E00: владелец принял шесть решений; их нормативные уточнения и закрытие F01–F14 находятся в [EDITORIAL_E00_FINAL_SPEC.md](EDITORIAL_E00_FINAL_SPEC.md). Ниже сохранён исходный аудит; прежний список требующих согласования defaults читать с учётом E00. Код по-прежнему не разрешён.

## Объект и метод

Проверены все четыре документа ветки docs/codex-handoff-audit-20261104 на commit **8e037d34391aaf3ed8b8c8d82f1d93c5b734cfae**: GLOBAL_ARCHITECTURE_BLUEPRINT_V0_1, EDITORIAL_PIPELINE_V0_1, EDITORIAL_DATA_CONTRACTS_V0_1, EDITORIAL_USER_WORKFLOW_V0_1. Они доступны и не подменялись предположениями. AGENTS прочитан. Рабочая база кода — **e1f4efb0fb5ff290bb198349213c004b4667ef0f**, Sprint 26. Прочитаны код, тесты и примеры; полный набор тестов, рендер, модели и API в этой проверке не запускались. Аудит внешних проектов не повторялся.

Ссылки на контекст: [blueprint](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8e037d34391aaf3ed8b8c8d82f1d93c5b734cfae/docs/GLOBAL_ARCHITECTURE_BLUEPRINT_V0_1.md), [pipeline](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8e037d34391aaf3ed8b8c8d82f1d93c5b734cfae/docs/architecture/EDITORIAL_PIPELINE_V0_1.md), [contracts](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8e037d34391aaf3ed8b8c8d82f1d93c5b734cfae/docs/architecture/EDITORIAL_DATA_CONTRACTS_V0_1.md), [workflow](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8e037d34391aaf3ed8b8c8d82f1d93c5b734cfae/docs/architecture/EDITORIAL_USER_WORKFLOW_V0_1.md).

## Вердикт

Архитектура реализуема как небольшой локальный модуль рядом со Sprint 26. Универсальность обеспечивается данными GenreProfile и отдельным content_mode, а не отдельными движками жанров. Ручной ввод, ручной фактчекинг и ручной сценарий достаточны для первого сквозного MVP; LLM, интернет-поиск, provider discovery, AI-видео, analytics и publishing не являются его зависимостями.

Документы верно описывают sidecar и still-only renderer, но пока недостаточно определяют транзакционность, зависимые утверждения версий, полноту текста и языковые границы. Начинать реализацию без исправления этих контрактов рискованно.

## Реализовано и предложено

| Компонент | Факт кода | Ограничение |
|---|---|---|
| Project/timeline | [project_schema.py](../core/project_schema.py), строки 115–140, 202–234: typed v3, ru/uk, точные поля, миграция старых версий в памяти | Нет production, claim, approval, genre; frozen dataclass не заменяет editorial persistence |
| CLI | [cli.py](../core/cli.py), 14–65: check/preview/bundle/verify/render-mp4 | Нет редакционных команд или общего проекта-редактора |
| Первый ролик | [first_video.py](../scripts/first_video.py), 25–39, 72–152 | 1–20 сцен, текст до 2000 Python-символов; WAV либо Silero; это входной план, не timeline v3 |
| Рендер | [mp4_render.py](../core/mp4_render.py), 42–74, 85–139 | Только последовательные still images; clips video отклоняются; четные размеры 2–8192; subtitle burn-in одной дорожки |
| Озвучка | [silero_local.py](../integrations/silero_local.py), 19–53 | Нет загрузки весов; конкретные имя/hash модели, явное доверие PyTorch pickle, CPU; ASCII-путь модели на Windows; нельзя обещать произвольный голос |
| Субтитры | [subtitles.py](../core/subtitles.py), 13–24; first_video 140–142 | Есть SRT exporter, но first_video всегда вшивает сценовый текст; не отдельный перевод и не word alignment |
| Editorial UI | Есть Voice Studio, но не предложенные S1–S7 | Вкладки проекта, evidence, script versions и approvals не реализованы |
| Locale prompts | locales/ru и locales/uk содержат короткие инструкции оригинального текста | Это не готовая жанровая библиотека, LLM или Narrative Engine |
| Тесты | [test_sprint26.py](../tests/test_sprint26.py): пять методов, в том числе no-render с синтетическими WAV | Не проверяют редакционные gates, crash recovery или реальную Windows озвучку |

Все утверждения в таблице — статическая проверка; наличие теста не считается его исполнением в этой сессии. Исторический baseline предыдущей настройки: 111 unittest; 124 pytest и 15 subtests; синтетический MP4 4,2 секунды. Он не доказывает работу нового ядра или реального Windows E2E.

## Находки и исправления спецификации

| ID / приоритет | Проблема и основание | Предлагаемое решение / проверка |
|---|---|---|
| F01 P0 | Workflow допускает разные narration/subtitle locales; first_video 123/140–142 использует один locale и один narration text | MVP сохраняет отдельные настройки, но handoff требует script=narration=subtitles. Другие комбинации — явный unsupported, без автоперевода |
| F02 P0 | ApprovalRecord связывает hash объекта, но нет точного snapshot зависимостей; claim/source/profile могут измениться без изменения текста | Approval связывает revision+hash и dependency digest. При любом значимом изменении доказательств/профиля/языка gate вычисляется заново |
| F03 P0 | SourceReference и Claim описаны без обязательных собственных ревизий; script_segment.claim_ids не фиксирует версию утверждения | Все редакционные сущности получают immutable revision; evidence links фиксируют claim/source revision. Script хранит точные refs, не плавающие latest |
| F04 P0 | Claim coverage невозможно автоматически доказать одним непустым claim_ids: пользователь может добавить новую фактическую фразу | Явная ручная проверка покрытия всех material assertions. Автомат проверяет связи и типы, но не объявляет семантическую истинность |
| F05 P0 | Scene narration может отличаться от утверждённого script. Ссылки segment_ids не доказывают отсутствие пропусков/добавлений | Scene хранит диапазоны текста с фиксированным порядком. Точная конкатенация narration должна покрывать утвержденный narratable text один раз. Изменение текста возвращает к новой ScriptVersion |
| F06 P0 | Proposed multi-file storage + JSONL не определяет атомарную фиксацию согласованного набора | Один authoritative editorial.json snapshot с immutable revisions, atomic replace и generation/CAS. История approvals/events внутри транзакции, JSONL лишь производный экспорт |
| F07 P0 | Передача утверждения и последующий render отделены по времени; файл/изображение могут измениться | Замороженный handoff digest, повторная проверка hashes/approvals перед запуском; никакого молчаливого принятия stale package |
| F08 P1 | Estimates сцен могут восприниматься как точный хронометраж | first_video 124–125: WAV duration +400ms, затем ceil к40ms, 25fps. Estimate не записывается как фактическая длительность; после build сохранить actual timing |
| F09 P1 | Параметры 9:16 в sidecar сами не влияют на first_video | Размеры передаются явными --width/--height. Default текущего build1280×720. Не объявлять вертикальный экспорт по одному полю aspect |
| F10 P1 | first_video создает output раньше проверки всех WAV и завершения render | Missing WAV/ошибка оставляют частичную директорию; повторный запуск отвергает existing output. Новый attempt path, статус failed, approved editorial state неизменен; не удалять пользовательскую папку |
| F11 P1 | Fiction genre может ошибочно освобождать реальные утверждения от evidence | Claim type и content mode независимы от genre. Fictional plot не требует источников; реальные факты в fiction/hybrid всё равно проверяются |
| F12 P1 | ER source принадлежит одному candidate, а текст допускает повторное использование; duplicated genre/mode есть у Production/Candidate/Brief | Источники production-scoped, многие claims/candidates ссылаются на них. Genre/mode авторитетны в production revision; версии downstream сохраняют snapshot, изменения не каскадируют молча |
| F13 P1 | Brief/ScenePlan approval_status и общий stage могут противоречить журналу approvals | Stage и readiness — вычисляемые проекции. ApprovalRecord — единственный источник решений; JSON-поле approved не открывает gate |
| F14 P1 | Rights status approved без intended-use scope может восприниматься как разрешение любых производных | Approval права фиксирует material hash, intended use, scope и reviewer; test-use не означает commercial-use. Неизвестное блокирует соответствующий выпуск |

Ссылки на основания F02–F06/F11–F14: Contracts §§3–6 и Pipeline §§5–8. F01/F09: Workflow §§3, S5–S6 против first_video. Это выявленные пробелы спецификации и интеграционные ограничения, а не утверждение о уже реализованном баге нового Engine.

## Минимальная модель

Предлагаются только четыре новых модуля: model/validation, store, service, handoff; отдельный CLI как тонкий интерфейс. JSON и стандартная библиотека достаточны. Схема sidecar editorial_schema_version=1 независима от timeline v3.

| Объект | Минимум MVP |
|---|---|
| Production | id, schema_version, revision, title, genre/profile snapshot, mode, раздельные locales, intended_use, created_at, active candidate/script/scene refs |
| GenreProfile | id/version, названия ru/uk, разрешённые modes, простая структура/рубрика/review rules. Только данные, без Python plugins |
| StoryCandidate | id/revision, title/summary, source refs, manual provenance. Один выбранный кандидат достаточен; assessment/rationale встроены |
| SourceReference | id/revision, title, URL либо local locator, known/null author/dates, rights scope, access/review notes; URL не скачивается автоматически |
| Claim | id/revision, statement, factual/interpretation/fictional, materiality, decision/qualification, reviewer; статус с основанием |
| EvidenceLink | Вложен в Claim: source revision, relation, locator, explanation, reviewer/time; противоречия сохраняются |
| EditorialBriefVersion | Небольшой snapshot внутри ScriptVersion: angle/audience/promise/must_include/must_avoid/profile ref; отдельный repository/service не нужен |
| ScriptVersion | id/revision, exact locale/text segments, exact claim refs, frozen brief, content hash; ручное редактирование достаточно |
| ScenePlanVersion | id/revision, exact script ref, ordered stable scenes/text spans, still brief, optional approved image refs, estimate, plan digest |
| ApprovalRecord | gate, exact object revision/hash, dependency digest, actor/time, decision/reason, policy version; append-only история |

Source и Claim не объединять: один источник подтверждает/оспаривает несколько утверждений. Script и ScenePlan не объединять: творческая редакция и техническая совместимость имеют разные gates. Production и v3 Project различать именами и путями. EventRecord не требует отдельного event-sourcing subsystem.

## Сохранение, восстановление и gates

Будущий storage: immutable revision payloads и approvals внутри одного JSON snapshot; сериализация UTF-8 с фиксированными правилами хэширования и сохранением точного текста. Hash без временных полей; policy/genre/dependency revisions входят в approval digest. Это не цифровая подпись и не защита от привилегированного изменения диска.

Save(expected_generation): validate → lock → проверить generation → записать temp в том же каталоге → flush/fsync где поддержано → atomic replace → увеличить generation. Не молчаливый last-writer-wins. Snapshot previous валидной generation — backup; startup проверяет целостность и предлагает восстановление, не объявляет его свежим без проверки. Media hashes потоковые; файлы не размещаются в Git. Network shares и crash/power-loss guarantees проверяются отдельно.

Для первого single-user MVP запретить параллельные writer sessions с понятным owner-lock; межпроцессный lock и stale recovery требуют тестов Windows. Не доверять одному generation check без lock — TOCTOU остаётся. Shared/network workspace и distributed jobs вне MVP.

Gate script проверяет refs, material claims, сохранённые противоречия/квалификацию, rights, locale, явную human coverage review. Gate scenes требует точную передачу текста и поддерживаемый media kind. Gate handoff повторно проверяет dependency digest, asset hashes, voice/locale и output path. Исправление claim/source/profile создаёт новую ревизию и блокирует затронутый export; старое approval хранится как историческое, не переносится автоматически.

## Windows и независимость от платформы

Pathlib, UTF-8, subprocess argument list, без shell/PowerShell-зависимости домена. UUID как folder id вместо пользовательского заголовка; ограничить длину, reserved names, traversal, drive/UNC absolute refs, junction/symlink escapes. Внешние разрешённые assets импортировать в managed staging с hashes, не ссылаться без контроля на меняющиеся файлы.

Silero требует уже установленную доверенную модель и PyTorch; модель не скачивается и права на неё не предполагаются. Для проекта с кириллицей путь к весам на Windows может требовать ASCII: это ограничение текущего adapter, не запрет Unicode для editorial data. Реальное качество RU/UA голоса и Win10/11 playback отдельно UNTESTED в этой сессии.

## Решения владельца

1. Утвердить ручной, offline-first vertical slice и CLI-first интерфейс; полноценный wizard отложить либо поставить отдельной задачей.
2. Принять ограничение script=narration=subtitles для первой передачи, сохранив отдельные поля.
3. Выбрать default формата: нейтральный/явный либо 9:16; renderer поддерживает размеры, но не принимает editorial aspect автоматически.
4. Подтвердить единый JSON snapshot/single-writer MVP и conservatively stale approvals по dependency digest.
5. Подтвердить роль человека: квалифицированные material facts, disputed claims и fiction disclosures требуют осмысленного решения, не автоматического supported по URL.
6. Разрешение реализации выдавать по задачам из [плана](EDITORIAL_MVP_IMPLEMENTATION_PLAN.md). Эта документация его не заменяет.

Ничего из этих решений не требует сейчас менять schema v3, устанавливать зависимости, объединять PR5/PR6 или подключать новые внешние компоненты.
