# MVP-08B.3 — Pure Offline GenerationJob Core: Implementation Gate

**Предложение следующего ограниченного этапа; сейчас NOT_AUTHORIZED / BLOCKED_CONTRACT.** Проверен [target c5cd33023880fd6726b74f5631eb766cc0959892][target], tree `7df9167d43018eb2685ba6ea674afb85a7d21263`, parent [04ea194e4d57c8a0550d7412281da58d4ba252c5][b2].

## Короткий ответ

**Да, pure contracts / FakeStore / FakeClock можно отделить от долговременной SQLite-квалификации.** Нельзя отделить их от точных identity/hash/error/fence semantics, необходимых для проверки модели. FakeStore не доказывает fsync, NTFS, межпроцессный lock, crash recovery настоящих DB, legal authority, media validity или provider exactly-once.

[B.1 plan][b1_plan] исторически называет .2 Offline Core, .3 Local Result Pipeline. Название новой задачи `.3 — Pure Offline GenerationJob Core` должно быть явно закреплено как новый этап. Оно не означает, что исторический core либо local pipeline выполнен. D08 полного MVP-08B остаётся будущим обязательством.

## Минимальные решения для начала pure этапа

|Пакет|Что должен зафиксировать владелец|EC / условие|
|---|---|---|
|G1: узкий продуктовый scope|Одна fixed synthetic operation; RESULT_AVAILABLE только как fake proof-consumer state; import/save/Route D/live deferred|EC-01A, EC-09A, EC-10A; не всё D08|
|G2: identity freeze|Exact preimages/versions/bytes, active-purpose projection/lifetime, historical replay и conflict behavior|Исправленные F01/F02 и EC-02|
|G3: pure fault boundary|Только FakeStore и fake simulator acceptance ledger; tri-state commit outcome в модели; никаких реальных DB/locks|EC-03B, EC-05B, F03/F04|
|G4: виртуальная ownership model|Controller/worker fence separation, exact claim/restart/cancel/clock semantics; no native owner-lock claim|Исправленный EC-04A, F04|
|G5: fixture/errors/limits|Synthetic metadata only, no verified F01 claim; exact errors, read/retry counters, finite bounds и no-effect guards|Исправленные EC-07B/EC-08A, F05/F06|
|G6: наблюдение и delivery|Single-shot observer, exact proposed base/tree, stage allowlist, test time/resource limits и новый STOP|EC-06B; wait deferred или отдельно явно выбран|

Это шесть согласуемых пакетов, охватывающих десять EC, а не шесть автоматических утверждений. Если выбран wait, его FakeClock deadline tests добавляются в exact scope; иначе P019 остаётся NOT_RUN. Любой unresolved item из G2/G4/G5 блокирует соответствующее pure API, даже если SQLite отложен.

## Что НЕ требуется замораживать для pure этапа

- SQLite DDL, journal/flush implementation, backup/restore, actual OS lock и реальные Windows clock mechanics.
- F01 MP4 bytes/tool evidence для проверки pure type/hash/identity/CAS model. Для положительного настоящего fixture result он по-прежнему обязателен.
- OD01 live profile, OD02 Library receipt extension, OD03 project/save CAS, OD04 decoder policy, OD06 GUI lifecycle, real authority/retention qualification.

Эти пункты остаются открытыми и блокируют свои операции. Они не становятся выполненными на основании fake traces. Синтетический input может тестировать реакцию потребителя на proof object; он не квалифицирует производителя proof и не выдаёт право на внешнее действие. Пример UUID/hash — test data, не receipt настоящего media результата.

## База и allowlist

[Предложение автора][task] рекомендует future base `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`. Она действительно содержит experimental Library и SP code; tree текущей docs branch отличается и не подменяет эту базу. Владелец должен назвать exact accepted future base/tree. Ни исходная experimental ветка, ни code из неё не вливаются в main этим обзором.

Для pure этапа требуется сокращённый, явно принятый allowlist внутри предложенных 22 paths: pure exports/contracts/policy/controller/observer и ports fixed simulator, соответствующие pure/fake/no-effects tests, один RESULT.md. Реальный `job_store.py` SQLite adapter, CLI runner, MP4 fixture, media tools и новые production dependencies из первого этапа исключаются. Если нужен отдельный helper path для fakes, его следует назвать в owner task; не расширять allowlist молча. Встроенные test fakes не становятся вторым production store/controller.

Existing `asset_library.encoded` — reference JCS-LOCAL-1. Зависимость от его импорта нельзя использовать для запуска media/Library effects. Exact bytes должны быть закреплены conformance vectors; если reuse без forbidden import effects невозможен в принятой базе, STOP с конкретным import gap, без изменения прежнего кода или silent codec substitution.

## Короткий план с конкретными результатами

### Этап 0 — узкая правка документов и owner freeze

Результат: versioned preimage/error/active-intent/restart таблицы по F01–F05, разделённые oracle cases и G1–G6 owner choices. Exact implementation branch/base/tree/allowlist и пределы выполнения указаны до кода. STOP при несовпадении источников. Новый широкий architecture audit не требуется.

### Этап 1 — pure values / admission / identity

Результат: strict closed value contracts; exact canonical byte/hash vectors; accept/reuse/conflict model через FakeStore; active-intent/terminal replay; immutable receipts; typed no-authority errors. Ни database file, ни provider/model/media operation. Применимые P001–P007/P011/P012/P020/P022/P024 реализуются и проверяются как pure cases; конкретные skipped/partial subsets перечисляются, не превращаются в «24 passed» автоматически.

### Этап 2 — pure state / fault / observer model

Результат: finite scripted fake traces под FakeClock для guarded prefix, fenced CAS, tri-state commit model, lost ACK/lookup, cancel flag, immutable effect identity и read-only observe. Negative no-effect counters. P008–P010/P013–P018/P021/P023 выполняются только в допущенной metadata/model трактовке; producer/media qualification не следует из результата. P019 только если wait отдельно включён. Общий source count 66 не равен числу фактически запущенных unit cases.

Отчёт: exact commands, interpreter/platform, wall-time/deadline, counts/skips/exit codes, failed attempts, current hashes/diff, список injected assumptions и непроверенных свойств. **STOP для независимой проверки pure core; D/W/A/L остаются NOT_RUN.**

### Этап 3 — отдельная долговременная local qualification

Только после нового разрешения и принятого EC-03A/EC-05A: real private JobStore + SimulatorStore, identity/schema/version refusal, atomic admission/CAS/event/outbox/receipt, bounded commit/reopen/interrupt faults D001–D018. Получить настоящий reviewed F01 перед соответствующим positive fixture run. Реализовать три исхода commit и current-owner recovery старого effect. Никаких repairs/recreates/migrations старых user stores. D-results не наследуются от FakeStore.

### Этап 4 — отдельная Windows qualification

Только после нового разрешения: реальные названные Windows 10 и/или Windows 11 builds, NTFS roots, Python/SQLite/clock и owner-lock/junction/path/flush fault evidence W001–W008. Проверенный build перечислить точно, непроверенный оставить NOT_RUN. CPU-only означает отсутствие модельных/GPU требований для ядра; не обещание скорости inference на 8 ГиБ ПК. Не менять ACL/system policy/permissions.

Asset ingestion/save и live/production не входят ни в один указанный шаг. Они остаются отдельными A/L gates с новым scope.

## Безусловные STOP

- Любая попытка объявить fake-store tests доказательством persistent/recoverable queue или SIM18 durability.
- Неоднозначные hashes, active intent, stale/current fences, commit outcome, error/counter rules.
- Ожидаемый existing store отсутствует/повреждён; неизвестный исход нельзя заменить пустым store или NOT_FOUND.
- Нужны edits прежнего кода, main/merge, production schema, model/render/download/live/paid/provider/Library/Tk/project save.
- F01 отсутствует для настоящего positive media run; никаких изготовленных «verified» hashes.
- Новая имплементация незаметно требует DAG, второй dispatcher, собственную CLI queue или retry scheduler.

**Текущий итог: implementation gate CLOSED / BLOCKED_CONTRACT.** Это предложение последующей задачи. Сам факт его публикации не разрешает MVP-08B.3.


## Точные источники

[target]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/commit/c5cd33023880fd6726b74f5631eb766cc0959892
[b2]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/commit/04ea194e4d57c8a0550d7412281da58d4ba252c5
[job]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_JOB_CONTRACT.md
[state]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_STATE_MACHINE.md
[sim]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_OFFLINE_SIMULATOR.md
[recovery]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_RECOVERY_MATRIX.md
[handoff]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_ASSET_HANDOFF.md
[open]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_OPEN_DECISIONS.md
[b1_oracles]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_TEST_ORACLES.md
[b1_plan]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_IMPLEMENTATION_PLAN.md
[owner]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08_OWNER_APPROVAL.md
[a_limits]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08A_LIMITATIONS.md
[a_owner]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08A_OWNER_ACCEPTANCE.md
[freeze]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/CONTRACT_FREEZE_PROPOSAL.md
[oracles]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/ACCEPTANCE_ORACLES.md
[scope]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/MINIMAL_EXECUTION_SCOPE.md
[task]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/IMPLEMENTATION_TASK_PROPOSAL.md
[dossier]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/OWNER_DECISION_DOSSIER.md
[sp]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/16d28ec0376c8c28f879c8aacb18d5378fea83a3/docs/tasks/SP_INTEGRATION_01B/DIAGNOSTIC_CONTRACT_V1_1.md
[b2_sp]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/04ea194e4d57c8a0550d7412281da58d4ba252c5/docs/tasks/MVP_08B_2_IMPLEMENTATION_AUDIT/MVP_08B_2_SP_INTEGRATION_READINESS.md
[encoder]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/asset_library.py
