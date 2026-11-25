# Dispatcher Memory Scenario 01

Дата — 2026-11-25. Область — один синтетический job в памяти на каждый независимый сценарий. Статус перед реализацией — AUTHORIZED_LIMITED_SYNTHETIC_SCENARIO.

## Основание и выбранная база

Владелец ответил «начинай» после предложения выполнить первый сценарий Dispatcher в памяти по документу `DISPATCHER_JOBSTORE_MINIMAL_CONTRACT_PROPOSAL_2026_11_25.md` на `28abeb1e7c061c43d997700222dfdeae307d3ce9`. Это разрешение на данный ограниченный шаг. Технический выбор базы и тестового интерфейса ниже сделан исполнителем и подлежит проверке вместе с результатом.

База feature-ветки — `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree `9a01050b07482eed304ae388e886f77eb48d6ff9`. В ней уже есть готовый Controller и SP/1.1. `git diff` подтверждает отсутствие различий с SP-ревизией `16d28ec0376c8c28f879c8aacb18d5378fea83a3` в трёх core/topic_to_film модулях, CLI, schemas/topic-to-film-v1-1 и tests/test_topic_to_film_v1_1.py. Перенос исходников и объединение историй не требуются.

## Ограниченные решения для этого шага

| Пункт | Выбранный объём |
|---|---|
| DJ-01 | Существующие Controller.admit/cancel/resolve_commit и observer.observe, готовый Lab/FakeStore из тестового harness |
| DJ-02 | SP/1.1 сохраняется diagnostic. Автоматическое преобразование его intent в AdmissionCommand откладывается. В демонстрации видны оба разных результата |
| DJ-03 | Только неизменённые synthetic records/permit из существующих golden fixtures, fake authority и namespace. Production/render/release допуска не возникает |
| DJ-04 | Значения Python сохраняются только в памяти. Долговечность и нативная очередь для этого сценария не требуются |
| DJ-05 | Операции admit/replay/cancel и model commit fault/reconciliation. Максимум один admitted job на экземпляр Lab, ноль dispatch/provider calls. Без новых worker/model/resource профилей |

Это выбор минимального тестового объёма по поручению владельца. Остальные SP-OD01–09 и DQ native условия сохраняют свои отдельные области и открытые решения.

## Задание и allowlist

Добавить `scripts/dispatcher_memory_demo.py` как developer-only средство существующей тестовой среды. Оно использует Lab из `tests/test_offline_generation_job_controller.py`; pytest требуется как уже существующая зависимость harness. Продуктовые CLI и core API не получают зависимости от тестов. Показать существующие APIOutcome/ObserverSnapshot и независимый SP diagnostic на stdout.

Добавить `tests/test_dispatcher_memory_demo.py` для проверки обычного входа, повтора, отмены и terminal replay, неизвестного commit/barrier/resolve, подмены запроса при том же ключе, namespace/CAS, отказа без authority, неизменности исходных fixtures и отсутствия побочных эффектов. Полные wire-данные берутся из существующего harness.

Разрешённые изменения относительно базы — этот документ, `scripts/dispatcher_memory_demo.py`, `tests/test_dispatcher_memory_demo.py`, `docs/tasks/DISPATCHER_MEMORY_SCENARIO_01_RESULT.md`, а также точечные записи в пяти `project-log/{WORKLOG,NEXT_SESSION,ROADMAP_STATUS,LICENSE_REVIEW_LOG,DECISIONS}.md`. Изменение существующих core/controller/store/schema/fixture файлов потребует отдельного обоснования.

## Проверки

1. Новый сценарий через CLI и целевые тесты.
2. Все существующие offline_generation_job suites и SP/1.1 tests на итоговом дереве.
3. Guarded execution без записи файлов, SQLite, сети, subprocess и wall clock. Инструмент загрузки модулей и stdout логирование отделяются от защищённой области.
4. Сравнение исходных core/fixtures с базой, git diff --check, allowlist и контроль ровно одного job на Lab.

Сначала Windows Python 3.12. Доступность Python 3.10/3.13 и CI проверяется отдельно, отсутствующая среда обозначается NOT_RUN. Общий render/GUI набор не относится к изменённому test-only пути. Решение о приёмке и следующий этап следуют по результату.

## Реестр внешних идей

Перечитан реестр на `28abeb1e7c061c43d997700222dfdeae307d3ce9`. EXT-02/03 сопоставлены с имеющейся очередью и наблюдением. Для этого шага достаточно существующего проекта, применимых заимствований нет. Все EXT-01–04 остаются CANDIDATE. Источники, права и конкретные интеграции заново не утверждаются.
