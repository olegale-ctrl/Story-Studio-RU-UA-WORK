# E01.3.9.3 / S2.4 — Fix D-01 Retained Parent Epoch Binding

**Дата:** 2026-11-06. **Статус:** минимальное исправление D-01 в pure in-memory
модели; требуется независимая проверка до S3.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `test/editorial-e01-3-9-3-s2-3-adversarial-recovery`.
- Exact base: `d816f1b94a71e04363371d9bc05b06f52a7fc0d6`.
- Branch: `fix/editorial-e01-3-9-3-s2-4-parent-epoch-binding`.
- Контракт: approved S1b / точная approved S1a редакция, E00/A/O/D без изменений.
- GitHub policy учтена из отдельного коммита
  `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`, без merge policy branch.

## Первопричина

`TransactionModel._parents()` выбирал retained container по
`state.parents[LineageEntry.storage_epoch_id]`, проверял внутренние parent proofs
через `_scan()`, но не сравнивал epoch возвращённой authenticated registration
с заявленной epoch/lookup key. Корректные parent bytes epoch E можно было передать
под alias E': внутренние MAC оставались valid, а неверный lineage binding
принимался. Original D-01 reproducer получал FINALIZED и receipt вместо отказа.

Ключ Python dictionary — selector, не доказательство идентичности epoch.

## Минимальное исправление и проверяемые привязки

Изменена только функция `TransactionModel._parents()` в
`editorial/storage_transaction_model_v1.py`:

- Строка 301 фиксирует `parent_epoch = link['storage_epoch_id']`; строка 302
  использует это значение для lookup контейнера.
- Существующий `_scan(parent, visited)` полностью проверяет registration/init
  MAC/binding, parent anchor MAC/context, journal MAC/index/previous/context,
  typed proofs и transition history. Поэтому возвращённая registration epoch
  уже связана с authenticated anchor и всеми frames этого parent container.
- Новая проверка на строке 308 требует
  `prev.registration['storage_epoch_id'] == parent_epoch`.
- Несовпадение возвращает существующий **EPOCH_MISMATCH**, path
  `$.lineage.storage_epoch_id`. ErrorCode enum не расширялся.

Проверка выполняется до копирования parent requests, sessions, IDs, verified
order и inherited keys в child Replay, а также до W0.freeze/W1/PREPARE и любых
persistence events нового запроса. Отдельное неподтверждённое container ID поле
не добавлялось: его lookup key сверяется с authenticated identity контейнера.

Проверки parent_head, parent_guard, parent_terminal_ref, production/machine,
finalized boundary, primary, continuity, protection и отсутствие forks/cycles
не изменялись. Inconsistent parent anchor/journal по-прежнему отвергаются через
прежние проверки `_scan`; новые проверки не подменяют и не ослабляют их.

## Файлы

Изменены:

1. `editorial/storage_transaction_model_v1.py` — один локальный patch `_parents`:
   отдельная переменная lookup и explicit authenticated epoch equality check.
2. `tests/test_storage_transaction_model_v1.py` — добавлены класс
   `ParentEpochBinding` (строка 975), synthetic fixture helpers и 8 regression
   test methods. Существующие test methods не переписаны.

Создан только этот `docs/tasks/E01_3_9_3_S2_4_RESULT.md`.

`tests/test_storage_recovery_adversarial_v1.py` **не изменён**, включая D-01,
assertions и отсутствие skip/expectedFailure. S2.1, golden literals, утверждённые
контракты и другие документы не менялись. Исторический S2.3 report остаётся
записью дефекта на прежнем exact SHA, а этот report фиксирует исправление.

## Позитивные и негативные регрессии

8 новых test methods проверяют 2 positive и 13 negative fixture cases:

| Проверка | Ожидаемый результат |
|---|---|
| Exact parent epoch после initialization ABORT | Child INITIALIZED в новой epoch, старый abort receipt и reservations сохранены |
| Два alias epoch при внутренне корректном parent E | EPOCH_MISMATCH до любых persistence events |
| Parent registration/anchor/frames согласованы с E2, LineageEntry заявляет E | EPOCH_MISMATCH; dictionary key не подтверждает identity |
| Parent anchor имеет другую epoch и корректный собственный MAC | Прежний ANCHOR_MISMATCH |
| Parent terminal frame имеет другую epoch и корректный MAC; anchor MAC пересчитан | Прежний JOURNAL_TRANSITION_INVALID |
| Parent под другим ключом / под ожидаемым ключом лежит другой authenticated container | BLOB_MISSING / EPOCH_MISMATCH соответственно |
| Correct parent с APPROVE→REJECT→REVISE→REVOKE | Все records, receipts, IDs, sessions, negative roots и verified epoch/seq/order сохранены буквально |
| Неверные head/guard/terminal/production/machine и попытка снять CONTINUITY_LOST | Прежние UNVERIFIED_ORDERING / HISTORY_CONTINUITY_LOST |

Для **каждого negative fixture case** сравниваются полные visible/durable states,
исходный TransactionInput и пустой event trace. Нет новых PREPARE/COMMIT, primary,
anchor, reservation, receipt ACK или даже W0.freeze. MAC/epoch tests намеренно
сохраняют корректность индивидуальных MAC, чтобы отличать context failure от
обычного MAC corruption.

Positive history regression проверяет точные tuples `(parent epoch, seq, id,
decision)` для seq 1..4, неизменные receipt bytes и parent container, а не только
round trip. Child seq 0 не сравнивается численно с parent seq 4. Imported snapshot
по-прежнему BASELINE_UNVERIFIED: сохранение history/order не выдаёт effective
authority и не отменяет импортные ограничения `latest_verified`.

## Порядок и фактические результаты проверок

Окружение: existing project `.venv`, Python 3.12.14, Linux cloud workspace, CPU;
новых зависимостей не установлено.

**Первым после изменения реализации** запущен неизменённый original D-01:

```text
.venv/bin/python -m unittest tests.test_storage_recovery_adversarial_v1.AdversarialRecovery.test_13_retained_parent_epoch_must_match_authenticated_parent_context -v
```

Результат: **1 test — OK**. Alias E' теперь отвергается, child store не меняется.
После этого добавлены регрессии; отдельный новый класс: **8 tests — OK**.

Затем проверки выполнены последовательно в запрошенном порядке:

| Команда (project `.venv/bin/python`) | Результат |
|---|---|
| `-m unittest tests.test_storage_recovery_adversarial_v1 -v` | 13 tests, 1659 parametrized scenarios, OK |
| `-m unittest tests.test_storage_transaction_model_v1 -v` | 87 tests, OK (79 существующих + 8 новых) |
| `-m unittest tests.test_storage_protocol_v1 -v` | 69 tests, OK; golden vectors неизменны |
| `-m unittest discover -s tests -v` | 808 tests, OK: все 800 существующих + 8 новых |
| `git diff --check` и staged diff check | Успешно |
| Original adversarial / S2.1 / approved documents diff | Пустой |
| File list / sizes / GitHub hygiene | Только три разрешённых файла, каждый меньше 10 MiB |

Финальные test runs: **0 failures, 0 errors**, без skip/expectedFailure D-01.
S2.1 сохраняет прежние literal 20 SHA-256 и 10 HMAC vectors. Логи остаются вне Git.
Unittest не собирает pytest-style functions; отдельный pytest набор не заявляется.

## Оставшиеся ограничения и STOP

Исправление закрывает подтверждённый D-01; оно не является утверждением полного
security audit. Блокирующих неоднозначностей S1 для этого equality check нет.
Authenticated parent epoch проверяется в рамках injected synthetic keys/proofs,
не реальных OS principal/protected registry или production authorization.

Pure in-memory scope сохранён. Нет service/DPAPI/ACL/IPC, filesystem persistence,
network, provisioning, реальных ключей/данных или новых protocol fields.
Production security и Windows process-crash/power-loss durability не заявляются.
PUBLISH_REVISION — DISABLED; partial COMMIT reconstruction — OFF.

После commit/push — **STOP**. PR/merge/release/main changes не выполняются.
S3 не начинать до независимой проверки исправления.
