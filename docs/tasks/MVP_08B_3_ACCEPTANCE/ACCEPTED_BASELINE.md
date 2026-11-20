# MVP-08B.3 — Accepted Technical Baseline

Дата записи: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / ACCEPTANCE_RECORD / ARCHITECTURE_PREPARATION**.

Точный исходный commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`. Запись приёмки ниже относится только к MVP-08B.3. Все новые решения MVP-08B.4 имеют статус **PROPOSAL / NOT_APPROVED**. Разрешения на реализацию, merge, release или production этим пакетом не создаются.

## Закреплённый baseline

Приёмка и её ограничения: [INDEPENDENT_ACCEPTANCE_RECORD.md](INDEPENDENT_ACCEPTANCE_RECORD.md). Источник реализации и тестовых результатов — [RESULT на принятом commit](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8a2164c54c97ba97d7d3a321cf4084a0926dc48c/docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md). Это техническая инвентаризация принятого состояния, не повторный аудит замечаний и не новый запуск тестов.

| Компонент | Реализовано | Подтверждено тестовой моделью | Реальная среда не подтверждена / нельзя считать production-ready |
|---|---|---|---|
| PURE-контракты и canonical hashing | 25 закрытых hashable PURE-типов, 7 boundary-типов, typed references, локальная JSON-канонизация; immutable bytes | Фиксированные векторы, отрицательный V030 и corrected V030, типы/nullable/closed fields | Не native attestation, подпись, rights clearance или production permit |
| Admission / active slot | Неизменяемые request/key/initial receipt; отдельный HELD(store,project,purpose); исторический replay | A01–A10, межоперационное interleaving и multi-job ошибки | Не native uniqueness, межпроцессная транзакция или право повторно выполнить эффект |
| GenerationJob lifecycle | Ограниченный guarded prefix до fake RESULT_AVAILABLE, cancel/uncertainty containment | Переходы и запреты в pure-модели, сохранение cancellation intent | Не downstream Library/attach/save; не вся 22-state pipeline и не COMPLETED |
| FakeStore / COMMIT | Тестовый atomic swap, retained intent, COMMITTED / NOT_COMMITTED / UNKNOWN, namespace HOLD | Fault matrix, полное/неполное доказательство, simulated controller replacement | Не SQLite, WAL/fsync, power-loss durability, backup/restore или native concurrency |
| Fencing / lease / clock | Инъецированные ownership/clock ports, текущие виртуальные fences и CAS | Stale writer zero writes, qualified fake owner death, epoch/rollback hold | Не OS lock, процесс-владелец, reboot clock или Windows job containment |
| Outbox / effect token / ledger | Immutable intent перед scripted effect; original generation/attempt/effect identity | Порядок записи до submit, lost ACK, отсутствие повторной генерации в модели | Не физический exactly-once эффект и не реальный idempotency ledger |
| Attempts / reads / bounds | Одна generation attempt; три total read reservations/checkpoint; конечные лимиты | Interrupted reservation consumption, duplicate cursor/restart не сбрасывают счётчики | Не квоты/стоимость/тайминг реального provider и не новый grant |
| Single-shot observer | Авторитетный в модели snapshot/cursor, явные barriers, pipeline_complete=false | Read scope, unavailable/corrupt/pending, отсутствие write side effects | Не durable observer, watch/wait service, filesystem mirror или readiness authority |
| Errors / fail-closed | Привязка external_effect к target и qualified evidence; локальный uncertainty latch | F-08B3-01/02 приняты по переданному решению; generic/typed exceptions и graph corruption | Локальный latch не переживает process death самостоятельно; не универсальная security isolation |

## Реальные границы модулей

`contracts.py` определяет закрытые значения и проверку reference closure. `policy.py` содержит ClockPort, OwnershipPort, StorePort и fake-authority/profile guards. `controller.py` управляет admission/lifecycle, передаёт Plan через StorePort и удерживает неизвестный исход до доказательства. `simulator.py` — metadata-only facade над инъецированным LedgerPort. `observer.py` выполняет single-shot чтение. **FakeStore/FakeClock/OwnerLock/ScriptedLedger определены в тестовом модуле**, не как инфраструктурные адаптеры.

StorePort: snapshot, commit, hold, inspect_mutation, acknowledge_resolution. LedgerPort: submit, attests, lookup, poll. Наличие этих ports — точка архитектурного отделения, не доказательство того, что native-адаптер можно безопасно подставить без нового квалификационного контракта. PURE_FAKE_ONLY и FAKE_STORE_READ_ONLY_EVIDENCE нельзя переименовать в native evidence с сохранением прежних утверждений.

## Неизменяемые инварианты

- **RESULT_AVAILABLE ≠ COMPLETED.** Fake result — связанная metadata, не проверенное MP4, импорт, GUI acknowledgement или сохранённый JSON.
- COMPLETED нельзя получить ослаблением guard, переименованием synthetic receipt или отсутствием ошибки. Будущий downstream требует квалифицированных подтверждений фактического импорта/привязки/сохранения и прочих исходных условий; здесь это не реализовано и не разрешено.
- Request/key/receipt и generation_operation_id/attempt_id/effect_token не меняются из-за crash, lost ACK или смены владельца. Новые fences не меняют identity эффекта; receipt не даёт write authority.
- UNKNOWN — hold, а не rollback, NOT_FOUND, свободный active slot или разрешение заново submit. Отсутствие доказательства не является доказательством отсутствия эффекта.
- RESULT_AVAILABLE удерживает active slot. Смена scope/provider/model/платформы не является способом обойти прежний active intent или spending/rights guards.
- Две retries означают три total calls; interrupted reservation расходуется. Это не разрешение на второй generation attempt.

Фиксированный профиль: OFFLINE_SIMULATOR_V1 / SIM_WAN_PROFILE_V1 / 1 / LOCAL_ONLY / T2V / synthetic.video_anchor. Лимиты: 16 jobs, 1 worker, 1-entry batch, 1 attempt, 3 reads/checkpoint, 128 events, 32 outbox records, 1 MiB request, 64 script events, 10000 virtual ticks. G1–G6 и D01–D08 сохраняются; $0 и отсутствие live/production permissions неизменны.

## Состояние квалификации

| Слой | Состояние |
|---|---|
| Pure model / принятое исправление | ACCEPTED_WITH_LIMITATIONS |
| Собственный независимый запуск pytest ChatGPT | NOT_RUN |
| Новый pytest в этом DOCS_ONLY-задании | NOT_RUN |
| Durable storage / настоящий crash recovery | NOT_RUN / NOT_APPROVED |
| Windows native boundary | WINDOWS_NOT_RUN |
| Реальный executor / media / Asset Library / save | NOT_RUN / NOT_APPROVED |
| Production / merge / release | NOT_AUTHORIZED |

Воспроизведение baseline начинается с точного accepted commit/tree и закреплённых версий/команд старого RESULT. При отсутствии этих объектов не следует восстанавливать реализацию по этому описанию. Новая ветка добавляет только документы, поэтому принятые code/test blobs остаются неизменными.
