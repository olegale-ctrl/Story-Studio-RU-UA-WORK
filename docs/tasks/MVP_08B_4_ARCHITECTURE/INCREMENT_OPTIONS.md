# MVP-08B.4 — Increment Options

Дата записи: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / ACCEPTANCE_RECORD / ARCHITECTURE_PREPARATION**.

Точный исходный commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`. Запись приёмки ниже относится только к MVP-08B.3. Все новые решения MVP-08B.4 имеют статус **PROPOSAL / NOT_APPROVED**. Разрешения на реализацию, merge, release или production этим пакетом не создаются.

**Все варианты: PROPOSAL / NOT_APPROVED.** Выбор владельца не сделан. Предыдущие исторические названия `.2 Offline Core / .3 Local Result Pipeline / .4 Qualification` не означают, что новый scope MVP-08B.4 автоматически утверждён. Здесь сравниваются только следующие ограниченные варианты.

## Сопоставление

| Критерий | A — Durable Store First | B — Execution Adapter First | C — Split Qualification |
|---|---|---|---|
| Объём | Один кандидат storage adapter и его transaction/recovery suite; executor отключён | Уточнение executor port и synthetic consumer tests исключительно с fake infrastructure | Отдельные принимаемые пакеты: storage, Windows ownership/fencing, затем adapter |
| Зависимости | Q1: data/native proof identity, engine/OS/FS/settings и тестовый root | Замороженная семантика токена/receipt/cancel, test-only authority; durable store не нужен для fake tests | Q1 для каждого пакета, затем явные входные результаты предыдущей квалификации |
| Главный риск | Получить хороший database test без доказательства OS/effect safety; рано назвать JobStore готовым | Повторно получить pure PASS без реального закрытия durability/restart gap; будущая интеграция меняет предпосылки | Больше явно версионируемых handoff/evidence; дрейф identity между пакетами |
| Тестовые доказательства | Native transaction/CAS/slot/outbox/mutation consistency; failure до/во время/после COMMIT, reopen/restore; отдельная честная оценка power-loss gap | Scripted ledger, old token/new fence, lost ACK, conflict, no second effect; только модель | Storage evidence отдельно от Windows process tests; затем ограниченный synthetic effect/ledger recovery suite |
| Готовность пакета | Q1–Q3 по точной platform/config матрице; Q4–Q7 явно не закрыты этим PASS | Только interface/model compatibility; никакого durable/Windows PASS | Каждый пакет независимо принят с точным входным baseline и оставшимися NOT_RUN |
| Запрещено после этого PASS | Executor/provider/media/production и перенос Linux PASS на Windows | Native processes, durable storage claims, real generator, production | Автоматический переход к следующему пакету, real providers/media/Library/save/production |
| Независимая приёмка | Возможна как storage-only qualification | Возможна как дополнительный pure/interface contract, но не как infrastructure qualification | Наиболее чётко разделяет предмет и предел каждой приёмки |
| Примерный размер, без сроков | Один infra adapter/probe, небольшой versioned data layout, migration/identity policy и существенная fault suite; средний самостоятельный инкремент | Небольшой interface/model инкремент, но с низким приростом реальной квалификации | Три небольших/средних самостоятельных инкремента; суммарно больше handoff-документации, меньше одновременных неизвестных |

Оценки размера — границы ответственности, не обещание количества строк/файлов или календарной даты. Точный allowlist и команды должны появиться только в отдельном задании после выбора владельца.

## Рекомендация Codex

**Рекомендуется C — Split Qualification**, с storage-only лабораторным пакетом первым. Принятый baseline уже содержит pure ports и scripted executor; вариант B сам по себе почти не уменьшает наиболее критичный разрыв — долговременное сохранение неизвестной операции и доказательство после настоящего restart. Вариант A полезен как первый компонент C, но его самостоятельный PASS нельзя превращать в готовность Windows/executor.

Предлагаемая последовательность, каждый шаг требует собственной авторизации и STOP:

1. Q1: выбрать bounded storage qualification profile и native evidence boundary. Не менять существующие G1–G6/PURE-типы. Выбрать engine-кандидат, runtime/FS, recovery fault model, test-root policy и точный scope.
2. Первый исполняемый инкремент **MVP-08B.4-DQ-01 — Durable Storage Qualification Lab** (предлагаемое имя): synthetic canonical data, один storage-кандидат, атомарность и recovery probes, отсутствие executor/Library/media. Q2/Q3 принимаются только для фактически испытанной конфигурации. Это не готовый production JobStore.
3. Отдельный Windows Ownership/Fencing Qualification: Q4 и относящийся к нему Q7, ordinary user, NTFS/reparse/clock/process matrix. Если Windows недоступен — BLOCKED_ENVIRONMENT/NOT_RUN, без имитации PASS на Linux.
4. Отдельный synthetic Local Adapter Qualification: только после требуемых storage/ownership/path gates и нового разрешения на bounded process/effect. Q5/Q6/Q7 проверяются на точно оговорённом эффекте. Никаких реальных TTS/LLM/генераторов/renderer.
5. Q8 на каждом самостоятельном пакете. После независимой приёмки — отдельное решение владельца, а не автоматическое выполнение следующего пункта.

Для самого первого lab Q4–Q6 могут оставаться NOT_RUN / DEFERRED и не быть ложными блокерами storage-only приёмки. Но базовая безопасность test-root/доступа из Q7 обязательна до любых разрешённых будущих native writes. End-to-end adapter нельзя запустить до его собственных квалификационных входных условий.

## Неутверждённый технический кандидат

SQLite со стандартным Python driver можно предложить первым storage-кандидатом из-за небольшого deployment surface. Это **рекомендация для решения владельца, не выбор**. Нужно явно выбрать допустимые engine/runtime versions, transaction/isolation/journal/sync settings, файловую систему и semantics ошибок/restore. Нельзя назвать default settings квалифицированными или менять зависимости в текущем DOCS_ONLY-задании.

Уточнения и вопросы для решения: [OWNER_DECISION_PACKAGE.md](OWNER_DECISION_PACKAGE.md). Gates: [QUALIFICATION_GATES.md](QUALIFICATION_GATES.md).
