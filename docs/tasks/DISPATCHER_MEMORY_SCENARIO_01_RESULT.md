# Dispatcher Memory Scenario 01 — результат

Дата — 2026-11-25. Статус — READY_FOR_REVIEW, PURE_FAKE_ONLY.

## Реализованный результат

Добавлен developer-only запуск `python -B scripts/dispatcher_memory_demo.py`. Он показывает исходные APIOutcome, ObserverSnapshot и JobRecord существующего Controller/FakeStore. Состояния и receipts читаются из единственного fake store. В начале отдельно показан исходный SP/1.1 diagnostic, который сохраняет BLOCKED_DISPATCHER_CONTRACT и пустой accepted_job_ids.

Обычный сценарий принимает один job, повторяет исходную команду, отменяет job и повторяет исходную команду после terminal state. Receipt остаётся прежним, состояние CANCELLED видно в JobRecord, commit выполняется только для приёма и отмены. Lost-ACK сценарий сохраняет один уже committed job, показывает HOLD и barrier, блокирует повтор до сверки, заменяет только объект Controller над тем же store и разрешает исходный mutation. После сверки повтор возвращает исходный receipt. Новый commit и dispatch отсутствуют.

Для сценариев используются Lab/FakeStore/fixtures из существующих тестов. pytest требуется для импорта этого developer-only harness. Новые продуктовые API, native JobStore и перенос SP intent в AdmissionCommand не добавлены. Это технический выбор минимального шага, зафиксированный в [задании и основании](DISPATCHER_MEMORY_SCENARIO_01.md).

## Проверки

Windows 10 build 19044, Python 3.12.10, pytest 9.2.0.

| Проверка | Результат |
|---|---|
| Новые tests/test_dispatcher_memory_demo.py | 12 PASS |
| Все шесть существующих offline_generation_job suites и новый suite под audit guard | 215 PASS, AUDIT_BLOCKED_EVENTS [] |
| SP/1 и SP/1.1 через существующий unittest | 69 методов, 68 PASS, 1 skip |
| Реальный запуск demo CLI | Exit 0, существующие records и оба model сценария на stdout |
| git diff --check и проверка allowlist | Выполняются перед commit |

Guard запускает Python -B с отключёнными внешними pytest plugins, fd capture, cache/tmpdir/logging. Он запрещает write-mode open, SQLite connect, subprocess, socket connect/bind, mkdir/remove/rename/link и другие эффекты. Дополнительный тест перехватывает native opens/writes, сеть, SQLite, subprocess, randomness и wall clock во время run_demo. Разрешены read-only обращения SP validator к собственным schema-файлам. Источник guard — локальный проверочный инструмент из пакета PROJECT_VALIDATION_20261125. Audit-hook не является утверждением syscall isolation.

Новые сценарные проверки подтверждают idempotency, terminal replay, mutation reconciliation без recommit, CAS и namespace mismatch, подмену запроса при том же ключе, отказ при отсутствии fake authority, HOLD на повреждённом fake store, неизменность golden fixtures, детерминизм, отсутствие dispatch и корректное поведение CLI. Диагностические данные SP не выдают authority для fake job.

Единственный skip исходного SP-прогона вызван отсутствием привилегии создания symlink в ограниченной среде. Отдельная проверка причины получила WinError 1314. По вопросу владельца тест `python -m unittest tests.test_topic_to_film.TopicToFilmTests.test_symlink_rejected -v` повторён с разрешённым доступом вне ограниченной среды — 1 PASS, 0 skips, exit 0. Создан настоящий файловый symlink во временном каталоге; read_local отклонил его с ValueError. Прежний skip сохранён в исходном журнале, отдельный успешный запуск — в `symlink-native.log`. Это проверка конечной файловой ссылки, а не квалификация всех junction, ACL, родительских reparse points и TOCTOU. Исходные Controller/policy/observer/simulator/contracts, core SP, схемы и fixtures не меняются. Новые тесты добавлены для сценарного входа и его ограничений.

## Ревизии и доказательства

Base — `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree `9a01050b07482eed304ae388e886f77eb48d6ff9`. Рабочая ветка `feat/dispatcher-memory-scenario-01`. Полный итоговый commit/tree сообщаются после commit в handoff, чтобы исключить self-reference.

Локальные логи и transcript — `../DISPATCHER_MEMORY_01_EVIDENCE/`. SHA256SUMS.json хранит raw hashes файлов evidence, включая проверочный harness. Сгенерированные логи и сторонние инструменты в Git не включаются.

## Границы и следующий шаг

Проверка Linux, Python 3.10/3.13 и отдельный GitHub CI этого итогового SHA — NOT_RUN. Общие render/GUI suites не запускались, поскольку изменение ограничено developer test path. Реальные провайдеры, render, сохранение файлов задания, SQLite, restart recovery, process kill и fault injection на нативном storage не выполнялись. В модели используется только существующая подмена исхода fake commit в памяти.

Результат требует отдельного review. Следующий возможный шаг — оценить полноту выбранного synthetic пути и решить, нужен ли ограниченный интерфейс адаптера или сначала долговечный store. Для произвольного SP запроса, native хранения и производственного допуска остаются соответствующие открытые решения SP/DQ. Main, PR, merge и release в этом пакете не меняются.
