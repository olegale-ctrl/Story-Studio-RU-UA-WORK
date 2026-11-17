# E01.3.5.2 — canonical dependency digest historical package

## Scope и база

Ветка: `feat/editorial-e01-3-5-2-dependency-digest`.
База: `d407c25ad802506e1843d7cc85c0717513f5f240` (E01.3.5.1).

Реализованы только canonical serialization и SHA-256 dependency digest уже
проверенного historical package. Current package, approval matching,
snapshot checksum, rights policy, readiness и handoff manifest не добавлены.

## API и защита integrity

```python
from editorial.dependency_digest import (
    DependencyDigestError,
    canonical_dependency_bytes,
    compute_dependency_digest,
)

canonical = canonical_dependency_bytes(snapshot, gate, exact_target_ref, policy_version)
digest = compute_dependency_digest(snapshot, gate, exact_target_ref, policy_version)
```

Обе публичные функции принимают ContractSnapshot, gate, внешний exact target_ref
и literal policy_version. API намеренно не принимает HistoricalPackage: перед
каждым результатом он внутри вызывает `build_historical_package()`, поэтому
невозможно незаметно передать произвольно собранную непроверенную структуру.

`PackageValidationError` из E01.3.5.1 проходит вызывающему коду без подмены и
без фиктивного digest. `DependencyDigestError(ModelError)` используется только
для digest-specific входов (`POLICY_VERSION`) и невозможности canonical JSON
serialization (`CANONICAL_JSON`).

`policy_version` должен быть строкой с хотя бы одним непробельным символом, но
после проверки сохраняется буквально: пробелы, Unicode, регистр и combining
characters не изменяются.

## Canonical payload

Payload имеет ровно шесть обязательных keys:

```json
{
  "dependency_digest_schema_version": 1,
  "gate": "SCRIPT",
  "policy_version": "policy-v1",
  "target_ref": {
    "kind": "script",
    "id": "...",
    "revision": 1,
    "content_hash": "..."
  },
  "production_refs": [],
  "profile_refs": [],
  "dependencies": []
}
```

Все refs полные. Target не повторяется в dependencies. Production/profile refs
остаются самостоятельными role arrays и одновременно присутствуют в closure.
E01.3.5.1 гарантирует exact deduplication, version-conflict rejection и
сортировку всех arrays по `(kind.value, id, revision)`.

Canonical bytes вычисляются строго:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
).encode('utf-8')
```

Digest — lowercase SHA-256 hex этих bytes. Никакой Unicode normalization,
trim, latest selection или сортировки domain arrays не выполняется.

HANDOFF результат является только **editorial HANDOFF dependency digest**. В
payload нет frozen media/config manifest, approval, allowed или ready.

## Golden vectors

Векторы построены на synthetic fixture с настоящими E01.3.1 content hashes и
успешной E01.3.2/E01.3.3/E01.3.5.1 integrity-проверкой.

| Gate | Target | policy_version | SHA-256 |
| --- | --- | --- | --- |
| SCRIPT | ScriptRevision r1 | `policy-v1` | `b966e03318f4b3f9f486f80196df93e327a16e7daaafa691bfb3ee80aae7e934` |
| SCENES | ScenePlanRevision r1 | `policy-v1` | `bb40e9c27dacff469e1380a9037a57c3aa6aafb7040f8eeffa9fe9e34268e9b8` |
| HANDOFF | тот же ScenePlanRevision r1 | `policy-v1` | `c42fcbcaba3535abb3c937861d13310fec7d73e5d0ea74a7e0b814bbfdeba161` |

Полные SCRIPT canonical bytes закреплены как literal golden fixture в тесте,
а не восстанавливаются тем же production helper.

## Тестирование

Проверены:

- exact golden SCRIPT bytes и SHA-256;
- golden SCENES и editorial HANDOFF hashes;
- повторяемость bytes/digest;
- независимость от JSON object-key insertion order;
- literal policy_version и изменение digest при его смене;
- различие SCENES/HANDOFF при одном target/closure;
- изменения referenced Source, Claim, Profile и RightsReview;
- отсутствие влияния неиспользуемой historical revision;
- отсутствие влияния исключённого audit timestamp;
- role arrays одновременно с dependency membership;
- отсутствие duplicate refs и canonical sorting;
- missing/wrong target и supplied root hash mismatch;
- блокировка PACKAGE_VERSION_CONFLICT;
- вычислимый UNCONFIRMED draft без authority;
- RU/UK, emoji и combining text без нормализации через content hashes и policy;
- отсутствие media/file/network/process I/O и mutation snapshot;
- все предыдущие 170 editorial tests.

Команда:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Результат: **186 tests passed in 4.695 seconds** — 16 новых digest tests и все
170 предыдущих editorial tests. Среда: Linux, Python 3.12.14, существующая
`.venv`; зависимости не устанавливались.

## Файлы и границы

Добавлены только:

- `editorial/dependency_digest.py`;
- `tests/test_editorial_dependency_digest.py`;
- `docs/tasks/E01_3_5_2_RESULT.md`.

Модели, codec, integrity, graph, rights_binding, package builder, Sprint 26,
timeline v3, renderer и FFmpeg pipeline не изменены.

Открытых вопросов E01.3.5.2 нет. Отдельного разрешения требуют current package,
approval/staleness authority, snapshot checksum, policy/expiry/readiness и
handoff manifest. E01.3.5.3 не начат.
