# MVP-08B.4-DQ-00 — Owner Approval

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

## Источник и статус

Владелец явно передал решения в задании «MVP-08B.4-DQ-00 — Owner Approval, Contract Freeze & Implementation Preparation». Следующая таблица воспроизводит утверждённую формулировку; это запись решения из разговора, не новая рекомендация Codex и не цифровая подпись.

| ID | Утверждённое решение | Статус |
|---|---|---|
| OD4-01 | Вариант C — Split Qualification; первым storage-only lab | OWNER_APPROVED_CONTRACT_ONLY |
| OD4-02 | SQLite через стандартный Python `sqlite3` как первый лабораторный кандидат; настройки требуют отдельной квалификации | OWNER_APPROVED_CONTRACT_ONLY |
| OD4-03 | Отдельный versioned native evidence/data compatibility profile, без изменения PURE-контрактов | OWNER_APPROVED_CONTRACT_ONLY |
| OD4-04 | Только изолированный disposable test root, synthetic data и ограниченные операции; конкретные пути и лимиты ещё требуют утверждения | OWNER_APPROVED_CONTRACT_ONLY |
| OD4-05 | Windows 10/11 — отдельная квалификационная матрица; отсутствие испытаний фиксировать как WINDOWS_NOT_RUN | OWNER_APPROVED_CONTRACT_ONLY |
| OD4-06 | Первый fault envelope — process-kill/reopen; power-loss и полноценный restore вне области | OWNER_APPROVED_CONTRACT_ONLY |
| OD4-07 | Реализация только по отдельному заданию с exact base/tree/allowlist, тестами, лимитами и независимой приёмкой | OWNER_APPROVED_CONTRACT_ONLY |

Эти решения повторно не запрашиваются. Они **не разрешают** native writes, создание SQLite-файлов, запуск/kill crash-test процессов, программирование адаптера, изменение зависимостей, main/merge/release или production.

## Что не было утверждено этой таблицей

Конкретные SQLite PRAGMA/version/config, schema/evidence proposal, root path, resource limits, будущие файлы и команды, Windows host/access и начало implementation. Численные значения ниже — явные предложения для независимой проверки/будущей авторизации; отсутствующие фактические сведения не заменяются догадками.

MVP-08B.3 остаётся ACCEPTED_WITH_LIMITATIONS; G1–G6, закрытие F-08B3-01/02 и PURE-контракты не пересматриваются. Native scope не превращает PURE_FAKE_ONLY/FAKE_STORE_READ_ONLY_EVIDENCE в durable authority. RESULT_AVAILABLE ≠ COMPLETED; в первом storage lab ни один из этих статусов не создаётся как результат реальной pipeline.

Согласование разделено в [OWNER_DECISION_PACKAGE.md](OWNER_DECISION_PACKAGE.md): A — уже утверждено; B — техническая независимая проверка; C — новые конкретные разрешения владельца. **STOP после публикации документов.**
