# E01.3.9.3 / S2.2 — Pure Transaction State Machine & Recovery

**Дата:** 2026-11-06. **Статус:** synthetic in-memory model; не production storage.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `feat/editorial-e01-3-9-3-s2-1-storage-wire-crypto`.
- Exact base: `c91c7b30ff64ce9f83702f3ecd4b2a2c92ca3335`.
- Branch: `feat/editorial-e01-3-9-3-s2-2-transaction-recovery-model`.
- Нормативная база: [approved S1b](E01_3_9_2B_S1_APPROVED_CONTRACT.md),
  точная S1a редакция `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c`,
  [D1–D12](E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md), E00/A1–A14/O1–O10.
- GitHub policy прочитана из отдельного коммита
  `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`, без merge этой ветки.

## Созданные файлы и API

Только три разрешённых новых текстовых файла:

1. `editorial/storage_transaction_model_v1.py`.
2. `tests/test_storage_transaction_model_v1.py`.
3. Этот `docs/tasks/E01_3_9_3_S2_2_RESULT.md`.

S2.1, его golden vectors, существующие модели/тесты/контракты не изменены.
Используются только стандартная библиотека и существующие чистые editorial API.
Размеры файлов проверены перед commit: каждый меньше 10 MiB. Нет binaries,
media/models, реальных ключей, персональных данных или protected artifacts.

`VirtualState` содержит primary, journal, anchor, registration, proof blobs,
prepared images, backups, forensic bytes, frozen authorization fixture evidence
и retained epoch containers. `VirtualStore` отдельно хранит visible и virtual
**durable** state. Каждая mutation и каждый flush наблюдаемы как before/after
события, независимые поля не объявляются общей атомарной транзакцией.

`TransactionInput` передаёт exact frozen command, plan, image/proof blobs,
registration и при необходимости retained parent fixtures. Модель сама не
выбирает editorial decision, ID, actor, timestamp или новый image. `FixtureAuthority`
— явные synthetic assertions principal/production/grants, review incarnation,
session и verified current-package context. При отсутствии обязательного fixture
следует отказ; grant одной production не действует для другой production.
Frozen policy evidence сохраняется отдельно от live grants для proof-bound replay.
Это test abstraction protected provider, не новый approved policy file format.

`TransactionModel.execute`, `recover`, `inspect`, `latest_verified` используют
S2.1 для strict canonical wire, closed types, framing, SHA/HMAC и constant-time MAC
checks. `Outcome` и Python dataclasses — внутренние результаты симуляции, не новые
protocol wire schemas. Возвращаемый `receipt` — exact canonical S1 Receipt bytes.

## W0–W9 и reconciliation

| Область | Реализованное поведение |
|---|---|
| W0 | Lookup admitted requests раньше current CAS/live grants; strict freeze validation, exact authorization/session/package fixtures, source/output integrity, plan/core/head/sequence/IDs/guard consistency |
| W1 | Раздельные writes/flushes blobs, frozen fixture evidence, registration/parents и exact prepared image |
| W2 | Backup exact A либо forensic C для repair; отдельные complete PREPARE append/flush; request/session/assigned IDs consumed, reserved sequence не переиспользуется |
| W3 | Отдельный replace/flush pending anchor, PREPARED с неизменным active guard_before |
| W4 | Повторный live authorization check; proven pre-intent failure → ABORT(REVALIDATION_FAILED). Полный authenticated INTENT предшествует pending-intent anchor |
| W5–W6 | Primary replacement — virtual CP; только записанная observation A либо exact B; verify published B и отдельный flush |
| W7–W9 | Ровно один terminal record; independent final anchor replace/flush/reread; exact receipt только после W8 и согласованных durable primary/journal/anchor |
| Stable | Проверка anchor MAC/registration, полного journal prefix/extension, plans/commands, typed blobs и primary; нет автоматического восстановления старого primary |
| Complete PREPARE / no intent | Только при complete verified prefix и exact A — durable ABORT, result ledger/guard, consumed IDs и preserved watermark |
| Complete intent | Только exact forward B completion/finalization либо block; не ABORT, не refreeze новых IDs/clock/policy |
| Complete terminal / anchor lag | Проверить exact B и finalize прежний terminal/receipt; не append duplicate COMMIT |
| Genesis | Explicit authorization + registration/init proofs, seq 0 и MISSING source; initial abort сохраняет reservations и INITIALIZATION_ABORTED |
| Exact-head repair | Explicit RECOVERY scope, observation CAS и forensic C; target — current recorded H, original commit_ref/generation/seq сохраняются, меняются tail/ledger |

Полный journal replay проверяет index/MAC/context, PREPARE→INTENT→terminal order,
prepare/intent/plan references, duplicate/orphan terminals, точный frozen receipt,
цепочки guard/ledger/barriers и сохранение старых roots. Source и output проходят
существующие versioned codec/round-trip/checksum/graph/hash/rights/attestation
integrity API. MIGRATE_SCHEMA дополнительно сверяется с exact output прежней
pure migration. RECORD_DECISION принимает только одну предоставленную append-only
pair/event, связанную с frozen command; unrelated revisions/active refs не меняются.
Полный production authority/current-package evaluator не создавался: его решения
представлены только явно переданными verified fixtures.

Missing anchor всегда блокирует automatic recovery, даже если найдены registration
или PREPARE. После сбоя до первого подтверждённого anchor не изобретается bootstrap
proof или operator continuation. Unknown C, missing/substituted proof, partial
frame, bad MAC, fork/gap или corrupted guard не исправляются молча.

## Idempotency, sessions и история

- Same request/principal/session/content возвращает тот же frozen receipt;
  different content/identity — conflict/denial до новых writes. Lost ACK не даёт
  второй terminal/decision/generation. ABORT не освобождает IDs или sequence.
- Unbound session другой process incarnation отвергается. Admitted READY context
  проверяется как frozen evidence; accepted intent переживает restart/live policy
  change без нового grant, session или review.
- Verified order строится из committed ApprovalBinding и reserved tx_seq, а не
  timestamp/UUID/array order. Тесты используют одинаковые timestamps намеренно.
- REJECT/REVISE/REVOKE barriers сохраняются. Новый APPROVE после negative decision
  требует exact latest verified target и нового request/review fixture.
- Imported records/evidence сохраняются буквально; BASELINE_UNVERIFIED и inherited
  key barriers не дают fabricated order. CONTINUITY_LOST не снимается acknowledgement,
  новой epoch или checksum.
- Retained local parent контейнеры проверяются рекурсивно по final anchor/head/
  guard/terminal proofs; multiple local predecessors/cycles/missing proofs блокируют
  порядок, epoch counters разных epoch не сравниваются напрямую. Протестирована
  разрешённая новая epoch после initialization abort с сохранением старого receipt
  и consumed request ID. Foreign UNVERIFIED link не создаёт local verified order.
- Нет endpoint reset/merge активной зарегистрированной epoch или rollback к backup.

## Fault injection и независимые assertions

`Fault` задаёт operation, before/after, occurrence и effect:
process interruption, virtual DISK_FULL либо FLUSH_FAILED. Перезапуск явно выбирает
один из двух synthetic survivor images: только flushed fields или все observed
visible writes. Это две выбранные модели, **не** предсказание поведения Windows
и не исчерпывающая модель hardware write reordering/power loss.

Пять matrix tests содержат **344 fault subcases** сверх отдельных негативных тестов:

| Матрица | Operations | Before/after и survivor modes | Subcases |
|---|---:|---|---:|
| Normal publish (schema migration) | 26 | 2 × 2 | 104 |
| Genesis | 28 | 2 × flushed-only | 56 |
| Exact-head repair, включая forensic barriers | 26 | 2 × 2 | 104 |
| Forward recovery | 12 | 2 × 2, затем дополнительный recovery crash | 48 |
| Pre-intent ABORT recovery | 8 | 2 × 2 | 32 |

Покрыты PREPARE/INTENT/COMMIT append и journal flush, pending/final anchor replace
и flush, primary CP/verification/flush, receipt ACK, proof/image/backup writes.
Проверяются повторные сбои forward recovery, ABORT recovery, pending IO errors,
exact original head при repair, immutable reserved IDs и отсутствие success до W8.
Partial frames вводятся явно как corruption fixtures; automated terminal
reconstruction отсутствует. `PUBLISH_REVISION` недоступна; попытка включить partial
COMMIT capability отвергается OPTIONAL_CAPABILITY_DISABLED.

Expected state определяется независимо по retained authenticated input records:
нет PREPARE → no admission, PREPARE без intent → A/ABORT, полный intent → exact B
либо block. Assertions проверяют буквальные record types, seq/generation,
original commit_ref, preserved negative roots, primary bytes и allowed action.
Golden genesis G воспроизводит **точные** S2.1 journal frames/anchor/receipt;
initialization ABORT воспроизводит буквальный MAC/frame vector A. Тесты не
ограничиваются round trips или сравнением двух функций tested model.

## Выполненные проверки

Окружение: Linux cloud workspace, Python 3.12.14, CPU. Новых зависимостей нет.

| Команда/проверка | Финальный результат |
|---|---|
| `python -m unittest tests.test_storage_transaction_model_v1 -v` | 79 tests, OK, 0 errors/failures; matrix subcases входят в эти test methods |
| `python -m unittest tests.test_storage_protocol_v1 -v` | 69 tests, OK, 0 errors/failures; прежние 20 SHA и 10 HMAC literals неизменны |
| `python -m unittest discover -s tests -v`, с `.venv/bin` первым в PATH | 787 tests, OK, 0 errors/failures |
| `git diff --check` и staged diff check | Успешно |
| Diff S2.1/approved S1a относительно exact sources | Пустой |
| File list / sizes / GitHub hygiene | Только три разрешённых additions; каждый меньше 10 MiB |

Для полного набора использована уже существующая `.venv`, где установлен pytest,
нужный существующему test module при import. Unittest не собирает pytest-style
functions; число 787 относится к unittest, отдельный pytest набор не заявляется.
Промежуточные успешные прогоны до последней production-scope regression содержали
78/786 tests; финальная проверка включает добавленный отрицательный тест.
Логи и временные данные тестов не включаются в Git.

## Неоднозначности, ограничения и STOP

Блокирующих неоднозначностей для этого synthetic substep не обнаружено. Новые
policy/provider deployment rules, filesystem semantics или допустимые automatic
repairs не изобретались. Существующие contracts не пересматривались.

Не реализованы реальные service/OS identity, protected policy catalog, ACL/DPAPI/
IPC, native handles/CAS/flush, filesystem storage, network, key provisioning,
backup export/import tool или production authority/readiness evaluator. Virtual
retained epoch containers — injected proof fixtures, не команда автоматического
создания или слияния active epochs. Полная потеря согласованного защищённого
состояния и privileged rollback остаются вне detection guarantees baseline S1.

**Production security, Windows crash consistency и power-loss durability не
заявляются.** Partial COMMIT reconstruction — OFF. Нужна независимая проверка
результата до S3. После commit/push — **STOP**, без PR/merge/release/main changes.
