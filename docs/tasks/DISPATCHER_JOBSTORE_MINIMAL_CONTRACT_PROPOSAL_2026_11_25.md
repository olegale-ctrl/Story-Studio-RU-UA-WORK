# Минимальный Dispatcher/JobStore — предложение для решения владельца

Статус — PROPOSAL, 2026-11-25. Подготовлено по поручению продолжать план. Область первого кандидата — один синтетический сценарий в памяти на CPU с проверкой повторов, отказов и наблюдения. OWNER decisions DJ-01–05 заполняются отдельно по [подготовленному заданию](DISPATCHER_JOBSTORE_NEXT_TASK_2026_11_25.md).

## Проверенная совместимость исходных линий

На `8a2164c54c97ba97d7d3a321cf4084a0926dc48c` существует `experimental_mvp/offline_execution/` с Controller, observer, policy, simulator и замкнутыми PURE records. На SP-ревизии `16d28ec0376c8c28f879c8aacb18d5378fea83a3` это поддерево отсутствует. Эти два источника нельзя считать одной уже интегрированной системой. До реализации необходимо выбрать точную базу и разрешённый набор переносимых файлов, затем повторить регрессии на итоговом дереве.

## Поверхность существующего API

| Операция | Источник и форма | Условие минимального кандидата |
|---|---|---|
| Приём | `Controller.admit(command, mutation_id)` | command — существующий `PURE.AdmissionCommand`, полная typed closure и fake authority |
| Переход | `Controller.advance(job_id, revision, mutation_id, target)` | Существующие переходы DRAFT → AWAITING_APPROVAL → APPROVED → QUEUED, действующие проверки permit/CAS |
| Наблюдение | `observer.observe(namespace, store, authority, job_id, clock=None, epoch=None)` | Один snapshot из единственного store, без собственного цикла ожидания |
| Отмена | `Controller.cancel(job_id, revision, mutation_id, worker=None)` | Существующие правила до/после отправки и terminal state |
| Неизвестный commit | `Controller.resolve_commit(mutation_id)` | Оригинальный mutation и сохранённое proof, без повторной отправки по таймауту |
| Исполнение модели | `prepare_submit`, `dispatch`, `apply_proof` | Только существующий ScriptedLedger и fake receipt при отдельном разрешении этого тестового объёма |

Controller возвращает существующий `PURE.APIOutcome`. Observer возвращает `PURE.ObserverSnapshot` либо существующий ошибочный outcome. В snapshot `pipeline_complete=False`. Эти объекты сохраняют version=1 и scope=PURE_FAKE_ONLY. Дополнительный wire-конверт и новая иерархия состояний для первого кандидата не предлагаются.

## Данные и смысл

SP/1.1 intent сохраняет свой локальный digest и диагностические blockers. Он не подставляется вместо AdmissionCommand, key или permit. Для первого проверяемого сценария берётся зафиксированная synthetic фикстура существующего pure harness, а связь с SP показывается отдельной таблицей сравнения полей. Реальный перевод произвольного SP запроса в исполняемое задание остаётся открытым до утверждения mapping.

Приём, revision, idempotency key, active slot, mutation и receipt принадлежат существующей модели Controller/store. Экран и CLI читают её snapshot. Диагностические bool-поля не создают authority и не переводят job в APPROVED. Терминальные COMPLETED/CANCELLED/FAILED следуют существующему контракту. При неопределённости сохраняются HOLD/UNKNOWN и требование reconciliation, а не новый запрос под другим ключом.

Текущие ограничения модели из contracts.py — 16 jobs, 1 worker, 1 batch entry, 1 attempt, 3 чтения на checkpoint, 128 events, 32 outbox entries, 1 MiB request, 64 scripted events, 10000 virtual ticks. Для первой интеграционной фикстуры предлагается дополнительно ограничиться одним job. Эти значения описывают pure модель и не являются измеренным ресурсным профилем нативного работника.

## Оракулы первого кандидата

| Сценарий | Проверяемое ожидание |
|---|---|
| Допустимая synthetic closure | Один admitted job и связанные существующие records, без файлов/сети/SQLite |
| Повтор идентичного запроса | Существующая idempotency-семантика, отсутствие второго job или второго эффекта |
| Подмена входа при том же ключе | Существующий IDEMPOTENCY_CONFLICT или связанная ошибка контракта |
| Устаревшая revision / чужой namespace | CAS_CONFLICT / NAMESPACE_MISMATCH, состояние сохранено |
| Отсутствующая authority | Отказ действующего policy слоя, diagnostic flags его не обходят |
| Отмена до dispatch | Существующий terminal cancel, отсутствует новый dispatch |
| Потерянное подтверждение commit | HOLD/UNKNOWN, исходный mutation сохранён, blind retry отсутствует |
| Barrier/неполное store evidence | Observer отражает barrier, pipeline_complete остаётся false |
| Повтор после terminal state | Действующий отказ или исторический read, отсутствие нового исполнения |

Конкретные полные wire-примеры должны извлекаться из существующего harness и проверяться неизменёнными validators. Придумывание новых разрешений, ключей и успешных receipts вместо закрытых fixtures запрещается условиями кандидата.

## Предложение отдельного задания реализации после решений

Цель — воспроизвести один pure синтетический lifecycle через существующий Controller и показать snapshot в диагностическом интерфейсе. Сначала владелец утверждает DJ-01–05, выбранную базу, mapping или его сознательное откладывание и allowlist. Затем задача фиксирует точный base/tree, переносимость зависимостей, файлы адаптера/тестов/отчёта, оракулы из таблицы и предел времени теста.

Критерии приёмки — один источник состояния, все отрицательные сценарии, отсутствие эффектов под audit guard, воспроизводимость на Windows и согласованной CI-матрице, отсутствие изменений действующих контрактов. Проверка source/target tree обязательна, поскольку SP и Controller сейчас находятся в разных линиях. Native JobStore, restart recovery и реальный render требуют последующего отдельного допуска и при необходимости завершённого DQ этапа.
