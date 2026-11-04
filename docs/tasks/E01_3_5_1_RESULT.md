# E01.3.5.1 — historical package и package-level integrity

## Scope и база

Ветка: `feat/editorial-e01-3-5-1-historical-package`.
База: `de48cefde21b747cac8165e7a307b06ea518b9b6` — утверждённый E01.3.4a
package contract.

Добавлен только historical package builder. Dependency digest, canonical
dependency payload, current package, active coherence, approval matching,
snapshot checksum, policy/readiness и handoff manifest не реализованы.

## API

```python
from editorial.package import (
    HistoricalPackage,
    PackageGate,
    PackageValidationError,
    build_historical_package,
)

package = build_historical_package(snapshot, 'SCRIPT', exact_script_ref)
```

Gate принимает только SCRIPT, SCENES или HANDOFF. SCRIPT требует exact
ScriptRevision root; SCENES/HANDOFF — exact ScenePlanRevision root. Внешний
target_ref самостоятельно сравнивается с target ref целиком, включая
content_hash; `ReferenceGraph.resolve()` для этого не используется.

`HistoricalPackage` — frozen dataclass:

- `gate: PackageGate`;
- `target_ref: RevisionRef`;
- `dependencies: tuple[RevisionRef, ...]`;
- `production_refs: tuple[RevisionRef, ...]`;
- `profile_refs: tuple[RevisionRef, ...]`;
- `material_bindings: tuple[RightsBindingResult, ...]`;
- `integrity_verified: bool`, всегда true у успешно возвращённого объекта.

Структура не содержит dependency digest, approved, allowed, ready, policy
решение, active state или handoff manifest.

## Closure и role refs

Builder сначала вызывает `validate_reference_graph(snapshot)`, затем строит
closure только по возвращённым `DependencyEdge`. Обход начинается с exact root;
root не входит в dependencies. Exact identities дедуплицируются, результат
сортируется по `(kind.value, id, revision)`.

SCRIPT closure содержит production, candidate, production/brief profiles,
claims, sources и их RightsReview. ScenePlan/Asset не добавляются.

SCENES и HANDOFF closure начинается с ScenePlan, содержит referenced script и
весь SCRIPT closure, non-null scene assets и их RightsReview. HANDOFF здесь
означает только editorial closure; media/config manifest отсутствует.

Для SCRIPT role refs извлекаются из root script. Для SCENES/HANDOFF script
разрешается через `scene_plan.script_ref`. `production_refs` содержит exact
`script.production_ref`; `profile_refs` — дедуплицированное объединение
`production.profile_ref` и `script.brief.profile_ref`. Каждый role ref обязан
также находиться в closure и точно совпадать с target.

Active refs не используются для выбора или расширения historical package.
Пустые active refs допустимы. Базовая E01.3.2 structural graph validation
сохраняется, но current coherence не проверяется.

## Full package integrity

До возврата выполняются:

1. exact root kind/existence/full-ref validation;
2. полная E01.3.2 graph validation;
3. closure только по нормативным edges;
4. version-conflict check для target + closure по `(kind,id)`;
5. независимый E01.3.1 SHA-256 пересчёт root и каждой dependency;
6. обязательный companion join для Source, Claim и RightsReview;
7. exact role-ref validation;
8. E01.3.3 binding для каждого включённого Source/Asset.

`validate_reference_graph()` не считается полной проверкой всей snapshot
history. Builder явно пересчитывает каждый объект своего пакета. Revisions вне
target/closure не входят в package hash checks и version conflicts, хотя их
базовая структура остаётся предметом обязательного graph validation.

Source binding `UNCONFIRMED` сохраняется в `material_bindings` и не блокирует
структурный draft package. Никакого rights grant из него не выводится.

## Conflict и errors

Несколько revisions одного `(kind,id)` вне package разрешены. Внутри target +
closure разные revision дают `PACKAGE_VERSION_CONFLICT`. Повтор одного exact
dependency дедуплицируется и не является конфликтом.

`PackageValidationError` совместим с ModelError/Violation и содержит стабильный
code, JSON-style path, message и при наличии object_ref.

| Code | Значение |
| --- | --- |
| `GATE` | gate не входит в закрытый vocabulary |
| `ROOT_KIND` | gate/root kind или payload type не совпадает |
| `ROOT_NOT_FOUND` | exact root отсутствует в snapshot |
| `ROOT_HASH_MISMATCH` | внешний target_ref hash отличается от exact target |
| `GRAPH_INVALID` | обязательная E01.3.2 проверка не прошла; исходный code сохранён в message |
| `PACKAGE_HASH_INVALID` | собственный E01.3.1 hash включённой revision неверен |
| `PACKAGE_VERSION_CONFLICT` | target/closure содержит разные revisions одного `(kind,id)` |
| `ROLE_REF` / `ROLE_REF_OUTSIDE_CLOSURE` | production/profile role binding некорректен |
| `PACKAGE_RIGHTS_BINDING` | включённый Source/Asset не прошёл E01.3.3 binding |

Если неверный dependency hash уже обнаруживается обязательной graph validation,
builder возвращает `GRAPH_INVALID` с исходным `TARGET_HASH_INVALID` в message.
Root без входящих ссылок дополнительно проверяется собственным package-level
пересчётом и даёт `PACKAGE_HASH_INVALID`.

## Тестирование

Позитивные fixtures пересчитывают настоящие E01.3.1 hashes в dependency order.
Source и Asset используют разные RightsReview UUID, чтобы корректный SCENES
package не содержал запрещённые две revisions одного `(kind,id)`.

Проверены:

- SCRIPT, SCENES и editorial HANDOFF closure;
- package без active refs;
- missing root, wrong gate/root kind и внешний root hash mismatch;
- неверный вычисленный hash root и dependency;
- отсутствующий/неверный companion;
- version conflict внутри closure и разрешённая история вне closure;
- dedup повторной exact dependency;
- UNCONFIRMED без grant/readiness;
- deterministic sorting, frozen result и повторяемость;
- отсутствие filesystem/network/process access и mutation snapshot;
- все предыдущие 153 editorial tests.

Команда:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Результат: **170 tests passed in 4.032 seconds** — 17 новых package tests и все
153 предыдущих editorial tests. Среда: Linux, Python 3.12.14, существующая
`.venv`; новые зависимости не устанавливались.

## Файлы и оставшиеся вопросы

Добавлены только:

- `editorial/package.py`;
- `tests/test_editorial_package.py`;
- `docs/tasks/E01_3_5_1_RESULT.md`.

Модели, codec, integrity, graph, rights_binding, Sprint 26, timeline v3,
renderer и FFmpeg pipeline не изменены.

Открытых вопросов E01.3.5.1 нет. Отдельного разрешения требуют current package,
canonical dependency payload/digest, approval matching, snapshot checksum,
policy/expiry/readiness и handoff manifest. E01.3.5.2 не начат.
