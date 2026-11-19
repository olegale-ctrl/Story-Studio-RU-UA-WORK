# Independent Contract Acceptance — MVP-08B.2a

**19 ноября 2026 · DOCS_ONLY / INDEPENDENT_REVIEW · STOP: BLOCKED_CONTRACT.**

Приёмка формы и происхождения шести документов пройдена. Приёмка как однозначно замороженного исполнительного контракта требует исправлений F01–F05. Решения EC-01–EC-10 не утверждены этим обзором. MVP-08B.3 не разрешён к реализации.

## Точная ревизия и метод

- Репозиторий: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Проверяемая ветка: `docs/mvp-08b-2a-offline-execution-contract-freeze`.
- [Проверяемый commit][target]: `c5cd33023880fd6726b74f5631eb766cc0959892`.
- Tree: `7df9167d43018eb2685ba6ea674afb85a7d21263`.
- Единственный parent / base: [MVP-08B.2][b2], `04ea194e4d57c8a0550d7412281da58d4ba252c5`, tree `661e8307a36d56860aa67407ea8bc4d4f0a1c997`.
- Исходный B.1: [контракты][job], commit `f0bce140451bf00a86f3939330e77ed63b2c98be`, tree `0b5238611cc84ef0a665f75b552757666935516e`.
- SP/1.1: [диагностический контракт][sp], commit `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`.

Использован подключённый GitHub и Git Data API. Обычный Git fetch завершился ошибкой TLS `SEC_E_NO_CREDENTIALS`; разрешения и TLS-настройки не менялись. Получены исходные Git metadata, полные нетранкированные деревья и 37 текстовых blobs. Для четырёх commit воспроизведена сериализация Git commit и пересчитан SHA-1; для четырёх корней пересчитаны все 206 tree objects; для 37 прочитанных файлов пересчитаны Git blob SHA-1 и raw SHA-256. Все совпали. Commit имеют `verification.verified=false`: совпадение SHA подтверждает идентичность, но не подпись владельца.

Содержимое исходных B.1, B.2 и SP прочитано отдельно. Утверждения автора о внешнем `ACCEPTANCE_PACKET.json`, его 37 snapshots и прежних тестовых запусках не заменяют эту проверку: тот внешний packet не представлен среди шести blobs и его прежние логи здесь не заверялись.

## Diff parent → target

|Файл в docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/|Mode|Git blob SHA-1|Bytes|
|---|---|---|---:|
|[ACCEPTANCE_ORACLES.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/ACCEPTANCE_ORACLES.md)|100644|`a683a067e795f816d50905d645c9d64cba936b61`|14153|
|[CONTRACT_FREEZE_PROPOSAL.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/CONTRACT_FREEZE_PROPOSAL.md)|100644|`30190d9b04b60fc476c79680ffdaf7780a39457b`|20726|
|[FINAL_HANDOFF.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/FINAL_HANDOFF.md)|100644|`660615be729a11e1be531aa7d63fe4161d4d1bb1`|6210|
|[IMPLEMENTATION_TASK_PROPOSAL.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/IMPLEMENTATION_TASK_PROPOSAL.md)|100644|`83327ef9bc16d7ff78f74a048b409d60ec6501dd`|11381|
|[MINIMAL_EXECUTION_SCOPE.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/MINIMAL_EXECUTION_SCOPE.md)|100644|`d3b582aea2e36327f97c212ceafd95198d689c83`|5769|
|[OWNER_DECISION_DOSSIER.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/OWNER_DECISION_DOSSIER.md)|100644|`c31ff2a1a5d07f9581fb92177f93b1de4306c40a`|14670|


Итого: ровно шесть добавлений `100644`, без изменений/удалений прежних blobs, symlinks, submodules или executable modes. Все остальные нетерминальные tree SHA изменяются только по пути к новой директории документов. Код, CI, конфигурации и прежние контракты не изменены. Наличие неизменённого кода не означает его корректность или прохождение тестов.

## Результаты десяти проверок

|Предмет|Вывод|Основание / граница|
|---|---|---|
|Git, SHA, tree, modes, docs-only|VERIFIED_STATIC|Воспроизведены объекты и полный leaf diff|
|D01–D08 и MVP-08A|Сохранены с оговоркой D08|Prefix не является всем MVP-08B; ограничения и P1 остаются|
|Identity / canonical hashing / idempotency|REVISE|F01: полные preimages; F02: active-intent uniqueness|
|RESULT_AVAILABLE / COMPLETED|Рекомендуется EC-01A|22 исходных состояния/38 правил; COMPLETED структурно недостижим в prefix|
|JobStore / CAS / fencing / outbox / recovery|REVISE|F03–F04; SQL-настройки являются предложением, долговременная работа не проверена|
|Второй диспетчер / очередь / DAG|Не обнаружен в предлагаемом профиле|Один controller; JobStore хранит lifecycle; outbox хранит effect intents; SimulatorStore не планирует jobs|
|JobStore / SimulatorStore / Library / SP|Границы в основном корректны|Раздельные ресурсы, без общей транзакции и без прямого SP submit|
|66 оракулов / ложный PASS|Счёт и статусы верны; полнота требует правки|24 P + 18 D + 8 W + 10 A + 6 L, все NOT_RUN; F05 и поштучная таблица в CONTRACT_FINDINGS|
|Windows 10/11, NTFS, CPU-only, local|Ограничения сохранены; qualification NOT_RUN|Наличие Windows shell не квалифицирует locks/SQLite/NTFS/clock; модели и native media tools не запускались|
|Live / paid / production|Запреты сохранены|Не выполнялись model/provider/render/Library/save/production эффекты|

## Сверка с точными решениями владельца

Источник каждого D — [MVP_08_OWNER_APPROVAL.md на B.1][owner], а не более ранняя таблица предложений.

|D|Проверка предложения|
|---|---|
|D01|Синтетические OFFLINE_SIMULATOR_V1 / SIM_WAN_PROFILE_V1 не объявлены настоящей Wan-версией. Выбор live модели не выполнен|
|D02|Бюджет 0; будущие $10/месяц, платные запросы, подписки и пополнения не разрешены|
|D03|Автоматизация провайдера через браузер не предлагается. GitHub-чтение документов не является исполнением provider workflow|
|D04|Квота ведёт к паузе; автоматического платного fallback нет. Цикл возобновления не может обойти attempt cap|
|D05|SyntheticFixtureContext не объявлен доказательством реальных прав. F01 ещё не предоставлен, права на него не проверены|
|D06|30% и чувствительность 10–50% остаются плановыми предположениями. Синтетический core не измеряет качество или rejection rate модели|
|D07|Новая область request/batch/permit требует точного согласования; REUSED не обновляет grant. F02 требует уточнить active-purpose scope|
|D08|Постоянная очередь, spending controls, MP4 validation, Library и fault tests остаются обязательным будущим объёмом. Pure prefix — отдельный подэтап, не выполнение всего D08|

[MVP-08A limitations][a_limits] и [owner acceptance][a_owner] сохраняют trusted-user local storage, residual TOCTOU/hardlink/reparse, отсутствие power-loss/OS sandbox/legal attestation, историческую природу links, bounded cancellation и P1-01/02/03. EC-09 не закрывает эти вопросы отсрочкой.

## Что действительно проверено

1. Локальный `verify_acceptance_evidence.py`: exit 0, Python 3.12.10. Проверка объектов, leaf diff, числа оракулов, их NOT_RUN, AST точного `asset_library.encoded`, статическая проекция исходного state graph.
2. Источник encoder действительно содержит `json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)` с default separators. Модуль не импортировался и код репозитория не запускался. Совпадение AST не доказывает готовность закрытого нового schema validator.
3. Статическая over-approximation дала 27 включённых строк исходных правил и 16 достижимых состояний. Guards не исполнялись. Это подтверждает отсутствие пути к COMPLETED в ограниченной модели графа, но не доказывает правильность будущей машины состояний.
4. Один вспомогательный inline-вызов печати сводки завершился SyntaxError из-за кавычек. Он не был тестом контракта; затем основной сохранённый verifier повторно завершился exit 0. Неуспех не учитывается как PASS.
5. Ни один из 66 будущих runtime-оракулов не исполнялся. Исторические 18 RAM LAB passes и незавершённый bulk-run B.2 остаются чужим ограниченным историческим evidence, не результатами этой приёмки.

Внешнее evidence этого обзора содержит исходные object metadata/hashes, diff, команды и exit status. Commit/tree самого обзора записываются после публикации в отдельном handoff packet: самоссылающийся commit hash в собственном документе не используется.

## Вердикт и STOP

**BLOCKED_CONTRACT** относится к freeze, пригодному для прямого программирования. Это не отсутствие доступа к источникам и не требование нового широкого аудита. Нужны узкие правки F01–F05 и поэтапные решения F06–F07. Четыре EC рекомендуются к одобрению, шесть — к доработке; ни одно не считается утверждённым.

После исправлений возможен отдельный owner-approved pure этап с FakeStore/FakeClock, без SQLite-квалификации и без настоящего F01 media run. Условия и точные результаты заданы в [MVP_08B_3_IMPLEMENTATION_GATE.md](MVP_08B_3_IMPLEMENTATION_GATE.md). Сейчас: **STOP; никакой реализации, merge, main change или автоматического перехода к MVP-08B.3**.


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
