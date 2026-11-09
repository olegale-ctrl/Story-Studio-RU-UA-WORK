# SI-E01.1 — Pure SI/1 Foundation: результат

Дата: 2026-11-09. Объём: только первая pure foundation часть SI-E01.
Ветка: `feat/story-intelligence-si-e01-1-pure-foundation`.
Точная база: `db41738b8135735c281b5cf4d18a5eb1f15b8a62`.
Remote HEAD `docs/story-intelligence-v1-owner-approval-si-e01-task` проверен перед
созданием ветки и совпал с базой. SHA результирующего коммита сообщается после
публикации отдельно: self-referential HEAD в содержимое коммита не включается.

## Нормативное основание

Прочитаны [owner approval](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md),
[composite review](STORY_INTELLIGENCE_V1_COMPOSITE_INDEPENDENT_REVIEW_AND_OWNER_DECISIONS.md)
и [точное bounded задание](STORY_INTELLIGENCE_SI_E01_1_CODEX_TASK.md).
SI-D01–SI-D10 утверждены; это не разрешает следующие этапы.
Исходный [proposal](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md) @
`b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`,
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) @
`978fbed45513a00e851201a9018d17c7da4752be` и
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md) @
`b3f16984edc8daad364f356aa51aeddc2ac0b5b8` применены с точечным приоритетом errata.
Согласованная [концепция](../architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md),
[ревизия завершённых этапов](STORY_INTELLIGENCE_COMPLETED_STAGES_REVIEW.md),
editorial/model.py, storage_protocol_v1.py и существующие storage tests использованы
только как read-only источники. Старые статусы proposal в документах не отменяют
новое явное утверждение владельца.

## Точный состав изменений — шесть новых файлов

| Файл | Назначение |
|---|---|
| `story_intelligence/__init__.py` | Минимальный чистый namespace SI/1 |
| `story_intelligence/codec_v1.py` | Canonical byte codec и SHA-256 |
| `story_intelligence/model_v1.py` | Структурные validators и SIValidationError |
| `tests/test_story_intelligence_codec_v1.py` | 14 literal vectors, parity и негативные codec cases |
| `tests/test_story_intelligence_model_v1.py` | Структура, diagnostics, provenance/header constraints, копирование |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_1_RESULT.md` | Этот отчёт |

Существующие файлы, approved contracts, editorial/Storage, старые тесты и golden
vectors, зависимости и package config не изменены. Сгенерированные caches/logs,
reference generator и host identifiers в коммит не включены.

## Публичный API и предел проверки

Codec экспортирует `canonical_si_json(value) -> bytes`,
`decode_canonical_si_json(data: bytes) -> plain JSON value`,
`canonical_si_sha256(value) -> str`.
Canonical JSON: UTF-8/no BOM, sorted keys по codepoints, no spaces, exact Unicode,
сохранённый порядок массивов, только exact dict/list/str/int/bool/None.
Floats, subclasses, surrogates, duplicate/escaped-equivalent keys и любые
неканонические bytes отклоняются, а не исправляются.

Single-object limits: <=1_000_000 UTF-8 bytes, <=100_000 codepoints в каждом
string/key, <=32 контейнера с включением корневого. Decimal integer conversion
выполняется порциями, без float/U64 narrowing и без sys.set_int_max_str_digits.
Тестируется exact integer >2^53, >U64 и 5001-значный integer. Bundle limits
16 MiB/1000 records не реализованы и не объявляются проверенными.

Model экспортирует SIValidationError (code/path), validate_si_ref, validate_eref,
validate_known, validate_origin, validate_header. Validators возвращают **отдельную
изменяемую plain-value копию**, одинаково для всех API, и не меняют входы.
Known callback получает копию T, должен проверить его и бросить исключение при
ошибке; его return игнорируется, не используется для coercion. UNKNOWN callback
не вызывает. SIValidationError callback paths переведены под $.value; другие
callback exceptions остаются ошибками вызывающего кода.

Проверяются закрытые поля, 18 SI types, точные 9 значений editorial ObjectKind,
canonical UUID/hash, positive int без bool, UTC seconds с реальным календарём,
Known union, mode-dependent required nullable fields. Header проверяет same
identity/точный preceding revision, initial previous=null; RunRecord только
revision1/RUN_METADATA/SI_ENGINE; Packet revision1/RULE_DERIVED/SI_EXPORTER.
Initial StoryIdea — RULE_DERIVED, initial CreativeAlternative — TEMPLATE_DERIVED;
их поздние версии — HUMAN_EDIT. MANUAL_INPUT/USER_IMPORT сохраняются для допустимых
initial input types, Selection — MANUAL_INPUT, Brief допускает свой approved
rule-assembly путь. MODEL_DERIVED распознаётся как reserved Origin structure,
но не делает provider runtime доступным и не допускается как initial V1 Creative.
Все surfaced собственные error codes — из разрешённого R1 vocabulary.

**Структура не подтверждает содержимое.** Header не включает payload и не проверяет
реальные записи по refs. Run stage/method/ancestry, Creative payload original run,
полный DAG/closure, actual content hashes, currentness, selection, replay и typed
record payloads отложены. SHA-256 — byte primitive, не сертификат provenance,
истины, author identity, прав или authority. validate_record/record_ref отсутствуют.

## Независимые golden vectors

В тесте зафиксированы **14** буквальных пар canonical bytes/SHA-256, без вычисления
expected значений production codec при определении тестов:
null, bool, empty object, RU, UK (ї/є/і/ґ), emoji, nested sorted keys,
ordered array, NFC, NFD, large positive integer, negative >U64 integer, escapes,
синтетический H+payload JSON. Последний явно **не** typed record validation.

Ожидаемые bytes получены отдельным одноразовым reference расчётом stdlib
json.dumps(sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False),
без импорта SI/S1; порядок ключей и Unicode/escape представления просмотрены.
Все 14 digest независимо сверены через `openssl dgst -sha256` на этих exact bytes
и сравнены с hashlib reference. Generator находится вне репозитория; OpenSSL не
является runtime/test dependency: executable tests используют только hardcoded
literals и Python stdlib. Это независимая сверка всех SHA, включая `{}`:
`44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`.

Тест-only parity импортирует существующий S1 canonical_json только на общем
валидном подмножестве. Проверено также, что S1 допускает объект 1_000_001 bytes
и depth33, а SI отвергает их. Runtime SI не импортирует editorial или Storage.
Отрицательные случаи покрывают UTF-8/BOM/canonical forms/duplicate keys/floats,
subclasses/bool-as-int, surrogates, лимиты, malformed refs/UTC, unknown/missing
fields, Known/origin binding, previous chain, initial Creative provenance и
неизменность исходных values/порядка. Это не выполнение всех 56 domain cases.

## Фактическая проверка

Среда: Linux x86_64, Python 3.12.14, проектный `.venv/bin/python`.
Целевой запуск:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
```

**31 тест — OK**, 14 literal golden vectors совпали. Ни одного skip/expectedFailure.

Полный запуск окончательной версии:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

**873 теста — OK**, 984.361 s, exit 0; errors=0, failures=0, skipped=0,
expectedFailures=0. Это 842 существующих теста + 31 новый. Все существующие
S1/S2/D-01/golden и LAB suites прошли; S2.3 дополнительно сообщил 1659
параметризованных сценариев (не дополнительные unittest methods).
Существующий `test_sprint23_2.Sprint232Tests.test_env_override` прошёл на Linux;
baseline ошибок окружения в данном запуске нет. Прежний Windows-specific failure
не скрывался и тест не изменялся; нативный Windows здесь не проверялся.

Фактически был также промежуточный полный прогон до добавления отдельной проверки
Packet technical label: 872 теста OK, 992.542 s, exit 0. После этой правки целевой
прогон повторён: 31 OK, 0.399 s; полный прогон повторён с итогом 873 OK выше.
Это отдельные запуски, их counts не суммируются. Буквальные vectors не менялись.

`git diff --check` и `git diff --cached --check`: exit 0. Проверены точный base,
source remote HEAD, ровно шесть A-only файлов allowlist, размеры каждого <10 MiB,
Python syntax, runtime imports и Markdown links/fences. Commit parent, опубликованный
remote HEAD и чистота worktree проверяются после публикации и сообщаются в handoff.
Никакой PASS Windows/native/persistence или всех 56 domain acceptance cases
из этого результата не следует.

## Исключения и следующий gate

Нет persistence/дисковых записей/clock reads/ID generation/сетевых обращений при
импорте или вызове production API; нет нового dispatcher/Run execution, Discovery,
Evaluation, Creative, Selection, Brief/Packet реализации, UI/CLI, renderer,
providers, ключей или protected writer. Только stdlib, CPU-only, exact RU/UK Unicode.
A/E/O/D/S1/S2/S3 и D-01 не меняются. PUBLISH_REVISION DISABLED, partial COMMIT
reconstruction OFF. S3.2a PURE_ONLY; S3.2b BLOCKED_HOST_NOT_PROVIDED.

Перед SI-E01.2 необходимы независимая проверка этого результата и новое bounded
задание: полные payload schemas, cross-record type/stage/method binding, original
creative run retention, closure, operation semantics/currentness/replay и их
literal fixtures пока не реализованы. Детальный persistence/privacy lifecycle
по SI-D03/07 требует отдельного контракта. Linux pure tests не квалифицируют
Windows native integration. PR, merge, release и main не выполняются.

После публикации — STOP; SI-E01.2/SI-E02 не начинались.
