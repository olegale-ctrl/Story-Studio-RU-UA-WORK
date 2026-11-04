# E01.3.4a — отчёт о закреплении утверждённого package contract

## Результат

Решение владельца проекта перенесено в отдельный нормативный документ:

- `docs/tasks/E01_3_4_APPROVED_CONTRACT.md`.

Исходный proposal сохранён без переписывания. E00 и E01.1a не изменены.

Утверждённый документ фиксирует:

- отдельные historical/current package operations;
- coherent active chains для SCRIPT, SCENES и HANDOFF;
- exact ScriptRevision и ScenePlanRevision roots;
- closure исключительно по E01.3.2 graph;
- editorial-only смысл текущего HANDOFF digest;
- полный шестипольный canonical payload schema 1;
- exact-ref deduplication, сортировку и version-conflict rule;
- Source/Rights/Asset composition по gate;
- допустимость digest для UNCONFIRMED draft без approval/readiness;
- historical reactivation без отмены revocations/current-rights checks;
- literal supplied policy_version без скрытого profile-policy equality.

Отдельно закреплено обязательное ограничение: `validate_reference_graph()` не
считается полной SHA-256 проверкой всей истории. Будущий package builder обязан
пересчитать E01.3.1 content hash target и каждой включённой revision, проверить
точные зависимости, companions и E01.3.3 bindings. Approval/readiness потребуют
отдельного full-integrity вызова.

Dependency digest отделён от snapshot checksum. Контракт не создаёт approval,
rights grant, коммерческое разрешение или production readiness.

## Изоляция

Ветка: `docs/editorial-e01-3-4a-approved-contract`.
База: `5d873d6c8bbf56aeb7dae4e1ad21f36bb73996bf`.

Добавлены только этот отчёт и утверждённый `.md` контракт. Python-код, тесты,
модели, codec, integrity, graph, rights binding, Sprint 26, timeline v3,
renderer и FFmpeg pipeline не изменены.

Runtime-тесты не запускались, поскольку executable behavior не менялся.
Выполнена проверка документационного patch через `git diff --check`.

Dependency digest не реализован. PR, merge и release не выполняются. После
публикации docs-only ветки работа останавливается для независимой проверки.
