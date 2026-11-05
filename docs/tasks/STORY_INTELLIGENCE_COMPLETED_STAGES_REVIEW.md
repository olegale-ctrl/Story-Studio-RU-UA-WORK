# Story Intelligence — ревизия завершённых этапов

Дата: 2026-11-05. База: `0907a64bf1331156741c8ab7de4739ba942a23dd`.
Ветка: `docs/story-intelligence-completed-stages-review`.

**Критических архитектурных противоречий с уточнённой концепцией не выявлено.
Переписывание завершённых этапов не требуется.** Есть пригодное редакционное
ядро и отдельный производственный MVP; полной системы Story Intelligence и
автоматического перехода между ними пока нет.

Ревизия основана на коде `editorial/`, отчётах завершённых E01.1–E01.3.8.6,
существующем RU/UK pipeline и лицензионных документах. E00 прочитан из
нормативного коммита `e520648411b99264688ff66dc61ad0e974201ed3`.
E00, A1–A14 и O1–O10 сохраняются. E01.3.9.1 — завершённое **написание proposal**,
а не утверждённая или реализованная storage-архитектура: service broker,
защищённый anchor и transaction journal из него не считаются доступными.

## 1. Соответствие четырём частям концепции

| Часть | Что уже поддерживается | Реальная граница завершённого |
|---|---|---|
| **Story Discovery Engine** | `CandidateRevision`: title/summary, точные source refs, manual discovery input, assessment/rationale. `SourceRevision` + `SourceDetails`: URL/local locator, автор/издатель/даты, review notes и material digest | Реализовано хранение ручных тем и источников, а не поиск. Нет retrieval/crawling, discovery ranking, дедупликации историй и глобального каталога. URL не вызывает сеть. Источники production-scoped; несколько кандидатов и повторное использование exact source refs внутри production допустимы |
| **Story Evaluation Engine** | `GenreProfile.rubric`, `RubricCriterion`, `CriterionRating`, `CandidateRevision.assessment` позволяют хранить объяснённые оценки 0–5; profile/rubric — versioned data | Нет исполняемого оценщика перспективности, новизны, достоверности, рисков или стоимости. Нет общей score calibration, подтверждённой связи assessment с конкретной rubric revision и проверки полноты оценки по её критериям. `reason`/`rationale` — пояснения, не доказательства и не прогноз успеха |
| **Creative Engine** | `GenreProfile.narrative_structure`, `BriefValue` (audience/angle/promise), ordered `ScriptSegment` с ролью/claim refs/visual notes, `Scene.visual_brief`, titles кандидата/production | Есть структуры для результатов ручной творческой работы, но нет engine для генерации/сравнения хуков, драматургии, retention, вариантов заголовков и визуальных решений. RU/UK script prompts — короткие инструкции оригинальности, а не такой engine |
| **Production Brief** | `BriefValue`: revision, audience, angle, promise, must_include_claim_refs, must_avoid, profile_ref; `ScriptRevision` замораживает его вместе с точными candidate/production refs. Есть scene plans, assets и editorial dependency packages | BriefValue — вложенная часть script, не самостоятельный pre-script production brief. Не хранит всю provenance оценки, варианты creative decisions, production constraints/budget или готовый media/config manifest. Готового adapter от него в производственный запуск нет |

Основание: [model.py](../../editorial/model.py),
[E01.1b result](E01_1B_RESULT.md),
[RU prompt](../../locales/ru/prompts/script_system.txt),
[UK prompt](../../locales/uk/prompts/script_system.txt).
Наличие подходящего поля не считается реализацией соответствующего engine.

## 2. Что сохраняем без изменений

- **Редакционные сущности.** Candidate, Source, Claim, Script и ScenePlan имеют
  разные назначения. Новый концептуальный термин «история» не требует их
  объединять или переименовывать. GenreProfile не исполняет plugins;
  factual/fictional/hybrid независимы от жанра. Fiction не требует вымышленных
  evidence; реальные факты в fiction/hybrid сохраняют требования human review.
- **Evidence и facts.** `ClaimRevision`, `EvidenceLink` и `ClaimReview` сохраняют
  точные утверждения, отношения supports/contradicts/context/insufficient,
  locator, reviewer и qualification. Это пригодная база проверки человеком,
  без обещания автоматического фактчекинга или истинности источника.
- **Rights bindings.** Сохраняем exact Source/Asset → RightsReview, subject
  kind/id/revision и material digest. `CONFIRMED` подтверждает совпадение
  сохранённых digest, но не лицензию, expiry/intended-use compliance или grant.
  Подтверждённый источник факта не предоставляет права на его изображение/текст.
- **Версии и целостность.** Immutable revisions, full RevisionRef, строгие
  schema-1/schema-2 codec, canonical hashes, reference graph, dependency digest
  и checksum пригодны для фиксации отобранной истории и её зависимостей.
  Изменения создают новые revisions; совпадение текста не переносит approvals.
- **Согласования.** Сохраняем immutable ApprovalRecord, exact decision key,
  consistency/history projections, REJECT/REVISE/REVOKE и ambiguity diagnostics.
  Attestation SHA-256, schema-2 integrity и pure migration используются в своих
  прежних границах. Migration не создаёт evidence; legacy approvals не становятся
  authenticated/effective. Подтверждённого transaction order пока нет.
- **Производственный MVP.** Сохраняем `scripts/first_video.py`, timeline v3,
  FFmpeg renderer и local WAV/trusted Silero integration. Они уже принимают
  scene plan и собирают MP4; это отдельная утилита, не реализация editorial
  authorization, Production Brief exporter или полного handoff gate.

Проверенные границы отражены в
[rights binding result](E01_3_3_RESULT.md),
[current package result](E01_3_5_3_RESULT.md),
[schema-2 integrity result](E01_3_8_5_RESULT.md),
[migration result](E01_3_8_6_RESULT.md) и
[first_video.py](../../scripts/first_video.py).

## 3. Что действительно требует уточнения для совместимости

**Доказанной необходимости менять работающий код в этой ревизии нет.**
Нужны точные границы интеграции; обнаруженные недостающие возможности нельзя
объявлять дефектами завершённых codec/hash/integrity этапов.

| Уточнение | Почему необходимо | Минимальная рекомендация, без реализации |
|---|---|---|
| Оценка истории отделена от проверки фактов и approval | Высокий score перспективности не подтверждает claims, права или review; отсутствие assessment не равно нулевой оценке | Использовать existing ratings/rationale для совместимых ручных оценок; сохранять unknown как отсутствие данных. Не вычислять authority/readiness из score |
| Автоматическая provenance не должна маскироваться под manual | `discovery_method` — закрытый vocabulary: manual_topic/manual_url/manual_local. У Candidate нет автоматического discovery/evaluator-run contract | Не добавлять hidden fields/enum values и не маркировать машинный результат ручным. Подтверждённые человеком текущие данные можно вводить прежними способами; отдельный machine provenance contract пока отсутствует |
| Production Brief не равен BriefValue или HANDOFF | BriefValue уже встроен в script; HANDOFF digest — editorial dependency package, не media manifest | На уровне согласования интерфейса явно сопоставлять совместимые поля с existing brief/candidate/source/claim refs. Не упаковывать неподдержанные структурированные результаты в reason/rationale ради обхода strict codec |
| Передача в производство требует отдельной проверки границы | Renderer принимает простой title/locale/scenes, не читает editorial approvals/evidence. Coherent package не проверяет понимание material facts и не разрешает render | Сохранить renderer API; не считать direct render вызов approved handoff. Export/adaptation отсутствует, его нельзя объявить готовым или заменить переименованием полей |

Для воспроизводимой автоматической оценки нужен explicit run/method/rubric
version и связь с exact candidate/sources; для самостоятельного pre-script brief
нужен отдельный согласованный контракт. Это **выявленные пробелы**, а не
предписание сейчас расширить schema 2 или начать новые модули.

## 4. Какие возможности пока не реализованы

1. Discovery/retrieval engine, проверяемая provenance автоматического поиска,
   novelty/deduplication и межпроизводственный knowledge/catalog layer.
2. Исполняемая evaluation/ranking logic, versioned evaluation-run attribution,
   проверка assessment против выбранной rubric, достоверные risk/cost estimates.
3. Creative generation/selection и метрики retention; множество versioned
   creative alternatives как самостоятельный structured result.
4. Самостоятельный Production Brief до script и готовый Brief → editorial →
   production adapter. Существующий `Scene.estimate_ms` не является оценщиком
   бюджета и не заменяет фактический timing WAV.
5. Полные semantic fact-review gates и проверка соответствия scene narration
   exact script slices: данные claims/ranges и structural integrity уже есть,
   но это не завершённая проверка всех содержательных требований E00.
6. Effective authority, OS principal/policy/session integration, protected
   transaction ordering, durable atomic storage/head anchor; а также
   rights-policy/expiry authorization и полный production readiness gate.
   Их отсутствие не разрешает ослабить A1–A14/O1–O10.

Этот перечень фиксирует границу завершённого; план следующих этапов, storage
решение и реализация Story Intelligence в ревизию не входят.

## 5. Обязательные ограничения повторного использования

- **RU/UK:** wire locale `ru`/`uk`, не `ua`; для первого editorial handoff язык
  script/narration/subtitles совпадает, UI locale независим. Unicode, whitespace
  и порядок смысловых массивов сохраняются буквально.
- **Windows CPU-only:** existing renderer использует `libx264`, Silero adapter
  загружает модель на CPU. Не добавляются обязательные NVIDIA, cloud, paid API
  или постоянный интернет. Локальные WAV остаются независимым offline входом;
  наличие pipeline не заменяет фактической Windows/model/playback проверки.
- **Production capabilities:** 1–20 сцен, непустой текст до 2,000 code points
  на сцену, local PNG/JPG/JPEG/PPM stills и отдельный audio input. Существующий
  renderer не превращается в генератор произвольных AI-video assets.
  E00 default 9:16 передаётся явно через width/height; прежний 16:9 default
  утилиты не требует переписывания. Editorial plan может быть шире renderer limits.
- **Лицензии:** действуют
  [IMPORT_LICENSE_GATE](../../LICENSES/IMPORT_LICENSE_GATE.md) и
  [UPSTREAM_TECHNOLOGY_IMPORT](../UPSTREAM_TECHNOLOGY_IMPORT.md).
  Pinned upstream CC BY-NC-SA 4.0 не получает коммерческое разрешение из старой
  MIT-копии. Китайские корпуса/Writing-DNA не переносятся автоматически.
  Код, model weights, голоса, media и FFmpeg distribution проверяются отдельно;
  score/approval не отменяют этот gate.

## 6. Итог ревизии

Уточнённая концепция совместима с уже завершённым редакционным фундаментом.
Минимально необходимы корректная терминология и явное сопоставление входных/
выходных данных, без смешения recommendation, evidence, approval и production
permission. Для имеющихся ручных сценариев существующие модели и проверки
сохраняются; автоматические engines и полный Production Brief ещё не реализованы.

**Переписывание завершённых этапов не требуется.** Утверждённые контракты,
работающий код, тесты, pipeline и лицензионные ограничения не изменены.
E01.3.9.1 остаётся неутверждённым proposal. Новые архитектурные решения этой
ревизией не принимаются.

Изменение ограничено этим документом. Runtime tests не запускались: это
архитектурная docs-only ревизия, не новое подтверждение platform/runtime
готовности. Выполняются diff checks и проверка совпадения опубликованного SHA.
