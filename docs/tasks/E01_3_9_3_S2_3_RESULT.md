# E01.3.9.3 / S2.3 — Adversarial Recovery Verification

**Дата:** 2026-11-06. **Результат: НАЙДЕН ДЕФЕКТ; S3 BLOCKED.**
Production-код не исправлен. Падающий regression test оставлен без skip или
expectedFailure для независимого review и отдельного задания на исправление.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `feat/editorial-e01-3-9-3-s2-2-transaction-recovery-model`.
- Exact base: `301aed34b72b0a8bb714a41e540d7e1abdbf9e98`.
- Branch: `test/editorial-e01-3-9-3-s2-3-adversarial-recovery`.
- Источники требований: approved S1b, точная approved S1a редакция, E00/A/O/D;
  GitHub storage policy из `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`.

## Точный scope

Созданы только:

1. `tests/test_storage_recovery_adversarial_v1.py`.
2. `docs/tasks/E01_3_9_3_S2_3_RESULT.md`.

S2.1/S2.2, существующие tests, golden vectors и утверждённые документы не менялись.
Все новые тесты сначала запускались против неизменённой S2.2. Нет реализации
storage/service, filesystem persistence, сети, DPAPI, новых зависимостей, реальных
ключей/персональных данных или protected artifacts. Используются только synthetic
in-memory fixtures и публичный mock key definition S1 §13.

## D-01 — неверная epoch retained parent принимается как VERIFIED_LOCAL_PARENT

**Класс:** отсутствие проверки binding между заявленной parent epoch и
аутентифицированным контекстом parent registration/anchor/journal.
**Статус:** воспроизведён; не исправлен; требует review владельцем.

Нормативные основания:

- S1 §2: JournalRef имеет machine/epoch context содержащего объекта.
- S1 §9: reconciliation проверяет registration binding, index/MAC/epoch/transition
  и loaded parent proofs, не только корректность отдельных MAC.
- S1 §10: VERIFIED_LOCAL_PARENT должен образовывать единственную проверенную цепь
  по exact parent commit/terminal proofs; claimed UUID не создаёт ordering proof.

### Воспроизводимое входное состояние

Самодостаточный сценарий:
`AdversarialRecovery.test_13_retained_parent_epoch_must_match_authenticated_parent_context`.

1. Выполнить default synthetic genesis G до durable PREPARE + W3 anchor.
   Прервать процесс, затем recover без INTENT. Получить корректный ABORT vector A:
   parent имеет INITIALIZATION_ABORTED, stable_head null и complete ABORT tail.
2. Реальная parent epoch, аутентифицированная registration, anchor и обоими frames:
   `33333333-3333-4333-8333-333333333333`. Parent production/machine, head/guard/tail
   и MAC остаются корректными; independent oracle подтверждает это состояние.
3. Создать LINEAGE_DELTA для child epoch
   `90000000-0000-4000-8000-000000000921`. Единственная LineageEntry:
   production/machine, parent_head null, parent_guard и parent_terminal_ref взяты
   из настоящего parent; order_status — VERIFIED_LOCAL_PARENT. Но её
   **storage_epoch_id** подменён на
   `90000000-0000-4000-8000-000000000920`.
4. Передать retained container как
   `parents["90000000-0000-4000-8000-000000000920"] = actual_parent_state`.
   Содержимое container по-прежнему аутентифицирует настоящую epoch `3333…3333`;
   изменён только alias/key и заявленная epoch в LineageEntry.
5. Подготовить explicit authorized synthetic child genesis с request ID
   `90000000-0000-4000-8000-000000000922` и guard.lineage_tip, указывающим на exact
   SHA/length этого LINEAGE_DELTA. Все child refs/MAC пересчитаны корректно через
   неизменённые S2.1 primitives; нет deliberately bad MAC или wrong blob hash.
6. Вызвать `child_machine.execute(child_transaction)` на новом VirtualStore.

Это разрешённый по форме новый initialization после aborted parent, а не попытка
reset активной production. Ошибка изолирована в **несовпадении parent epoch**;
проверенные parent bytes не переписываются и parent terminal не фабрикуется.

### Ожидаемое поведение

Fail closed до W1/PREPARE: ошибка epoch/context/lineage proof mismatch, без
изменений store, terminal record или receipt. Alias контейнера не может заменить
проверку `LineageEntry.storage_epoch_id == actual_parent.registration/anchor epoch`.
Тест допускает нормативные EPOCH_MISMATCH / UNVERIFIED_ORDERING /
PROTECTION_INVALID / JOURNAL_TRANSITION_INVALID, не навязывая новый error code.

### Фактическое поведение неизменённой S2.2

```text
claimed=90000000-0000-4000-8000-000000000920
 authenticated=33333333-3333-4333-8333-333333333333
outcome=FINALIZED
journal_frames=3
receipt_present=True
```

Модель записывает child PREPARE/INTENT/GENESIS, финальный anchor и возвращает
successful receipt, хотя retained proof относится к другой epoch.

Воспроизведение из корня репозитория:

```text
.venv/bin/python -m unittest tests.test_storage_recovery_adversarial_v1.AdversarialRecovery.test_13_retained_parent_epoch_must_match_authenticated_parent_context -v
```

Результат: **1 test, 1 failure** с сообщением `S2.3 DEFECT: wrong retained parent
epoch accepted`. Непосредственный путь в S2.2 — `TransactionModel._parents`:
container выбирается по `link['storage_epoch_id']`, затем проверяется через
`_scan`, но actual epoch возвращённой registration не сравнивается с alias.
Проверки head/guard/terminal/machine/production сами по себе эту разницу не ловят.

Установлено принятие недопустимого protocol proof binding, **не** HMAC break,
кража production key или доказанная реальная privilege escalation. Virtual test
передаёт explicit synthetic trusted fixtures/MACs; production security здесь не
заявляется. Исправление, выбор окончательной диагностики и дополнительная оценка
влияния остаются отдельному review/заданию. После обнаружения D-01 исследование
новых сценариев прекращено; выполнялись только запрошенные regression checks,
фиксация отчёта и публикация двух разрешённых файлов.

## Остальные проверки и независимые assertions

Первые 12 mandatory test methods прошли до добавления D-01. Они не выводят
expected state из `model.inspect` или другого recovery method. Новый receipt
oracle самостоятельно проверяет standard-library JSON/SHA/HMAC, raw frame bytes,
indices/previous MAC, PREPARE/INTENT/terminal links, terminal ReceiptCore, ledger
hash и finalized anchor/durable state.

Для historical receipt допускается более новый current anchor, если его verified
prefix сохраняет именно тот terminal: old APPROVE receipt не становится текущим
approval. После REVOKE primary и latest verified decision должны оставаться
revoked; stale primary/backup блокирует automatic recovery и retry.

| Новый test method | Parametrized scenarios | Проверка |
|---|---:|---|
| 01 | 8 | Same request после PREPARE/INTENT/COMMIT/lost ACK, exact receipt, один terminal |
| 02 | 16 | Principal/session/request changes → conflict/denial; live policy change не отменяет accepted intent |
| 03 | 2 | Restart-invalid unbound session; bound pre-intent request завершается ABORT |
| 04 | 6 | Forward completion после intent без новых grants/session/package assertions |
| 05 | 8 | Последовательные повторные crashes внутри ABORT и forward recovery, before/after, оба survivor modes |
| 06 | 2 | Wrong typed proof при корректных hash и отдельно корректных frame/anchor MAC |
| 07 | 4 | Individually valid MAC при несовместимых guard/high-watermark/tail/head |
| 08 | 3 | Reuse approval_id / event_id / tx_seq блокируется без mutations |
| 09 | 3 | Historical APPROVE retry, отсутствие REVOKE reconsideration, old APPROVE import как unverified history |
| 10 | 2 | Primary заменён старым backup, recovery/retry не восстанавливают старое решение |
| 11 | 1592 | Все 1571 nonempty proper prefixes GENESIS; по 10 boundary prefixes SNAPSHOT_COMMIT и REPAIR_COMMIT; запрет включения reconstruction |
| 12 | 12 | Successful receipt связан с verified terminal и финальным anchor на разных crash windows |
| 13 / D-01 | 1 | Parent epoch alias/context mismatch — **FAIL** |
| **Всего** | **1659** | Новые subTest invocations, отдельно от прежних S2.2 matrices |

В method 05 один parametrized сценарий содержит несколько последовательных
recovery interruptions. Число 1659 — выполненные scenario blocks, не отдельные
unittest test methods и не число всех assertions/fixture setup операций.

## Фактически выполненные проверки

Окружение: project `.venv`, Python 3.12.14, Linux cloud workspace, CPU.

| Проверка | Результат |
|---|---|
| Первый новый набор против unchanged S2.2 | 12 tests, 1634 scenarios, OK |
| Расширение mandatory coverage до D-01 | 12 tests, 1658 scenarios, OK |
| Изолированный D-01 reproducer | 1 test, 1 failure, 0 errors |
| Новый финальный набор, `-v -f` | 13 tests, 1659 scenarios, 1 failure (D-01), 0 errors |
| S2.1, `tests.test_storage_protocol_v1 -v` | 69 tests, OK |
| S2.2, `tests.test_storage_transaction_model_v1 -v` | 79 tests, OK |
| Полный `.venv/bin/python -m unittest discover -s tests -v` | 800 tests, 1 failure (D-01), 0 errors |
| Golden vectors / production / approved docs diff | Не изменены относительно exact base |
| `git diff --check` и staged diff check | Успешно |
| File list / sizes | Только два разрешённых новых Markdown/Python файла, каждый меньше 10 MiB |

Полный набор **намеренно красный** из-за воспроизводимого дефекта; существующие
S2.1/S2.2 tests сами по себе этого дефекта не обнаруживают. Не применялись skip,
expectedFailure, правки implementation или изменение контракта ради green result.
Логи остаются вне Git. Unittest не собирает pytest-style functions; отдельный
pytest прогон не заявляется, новые зависимости не установлены.

## STOP

S3 не начинался. PUBLISH_REVISION — DISABLED, partial COMMIT reconstruction — OFF.
Нет PR/merge/release/main changes. Production security и Windows power-loss
или process-crash durability не подтверждены этими synthetic tests.

Следующий шаг требует независимого review D-01 и отдельного задания на исправление.
