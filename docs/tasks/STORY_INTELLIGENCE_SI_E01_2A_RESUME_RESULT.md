# SI-E01.2a-RESUME — Typed SI/1 Record Schemas

Дата: 2026-11-09. Реализовано в пределах **pure local typed-record validation**;
независимая приёмка этого результата ещё не выполнена.

- Ветка: `feat/story-intelligence-si-e01-2a-resume-payload-schemas`.
- Точная база: `b49230df8740a0917a461d8b4f4d8638ba792675`.
- Source remote HEAD `docs/story-intelligence-v1-r1b-approval-si-e01-2a-resume`
  проверен до создания feature branch и совпал с точной базой.
- Финальный commit/remote SHA сообщается после commit/push в handoff. Собственный
  commit hash нельзя буквально включить в содержимое этого же коммита; для проверки
  служат `git rev-parse HEAD`, exact parent/base и итоговый SHA handoff.

## Основание и приоритет

Прочитаны [owner approval SI-D01–SI-D10](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md),
[original](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md) @
`b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`,
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) @
`978fbed45513a00e851201a9018d17c7da4752be`,
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md) @
`b3f16984edc8daad364f356aa51aeddc2ac0b5b8`,
[R1b](STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md) @
`5fdd1d8f72ccec37730c8f4c271450e4e95f8de1` и его явное
[owner approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md) @
`418becfa88e4e8f5ba4a293247c293988f7d5742`.
Применены только точные overrides в порядке original → R1 → R1a → R1b.
Статус PROPOSAL внутри старого R1b перекрыт отдельным owner approval, документ не изменён.
В предоставленной базе approval note уже нормализован по trailing whitespace относительно
418becf; git diff подтвердил только это форматирование, текст решений идентичен.
Наша ветка approval note не меняет; сам R1b contract совпадает с pinned 5fdd1d8.

[Полный RESUME task](STORY_INTELLIGENCE_SI_E01_2A_RESUME_CODEX_TASK.md) наследует
[первоначальное bounded задание](STORY_INTELLIGENCE_SI_E01_2A_CODEX_TASK.md),
кроме явно заменённых entrypoint/allowlist/result names и уточнений R1b.
Прочитаны принятый SI-E01.1 @ `61886670fe6d0434df62f6346457f5812f520766`, его
[independent acceptance](STORY_INTELLIGENCE_SI_E01_1_INDEPENDENT_ACCEPTANCE.md),
исторические [GAPS](STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md) и
[BLOCKED RESULT](STORY_INTELLIGENCE_SI_E01_2A_RESULT.md) @
`18163478f2204c3dd3d3f9bd742c49ea8253506e`. Они не переписаны и не объявлены успешными.
Product Success working reference @ `d15cab43849c82f4a880f9fcb772c1c1bfc56622`
прочитан через git show отдельно, без merge/cherry-pick и без внедрения product work.

## Точный allowlist изменений

Созданы только четыре файла:

| Файл | Назначение |
|---|---|
| `story_intelligence/records_v1.py` | Закрытые схемы 18 типов, nested values, local constraints, byte-derived SIRef |
| `tests/test_story_intelligence_records_v1.py` | Positive/negative structure, R1/R1a/R1b, local identity и privacy syntax |
| `tests/test_story_intelligence_record_vectors_v1.py` | Буквальные independent record/value byte/hash oracles |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_RESULT.md` | Этот отчёт |

Новых существенных contract gaps не найдено; optional `_RESUME_CONTRACT_GAPS.md`
не создавался. Все изменения — new/A-only, без deletions. Exact diff: **4 новых файла, 1282 additions, 0 deletions**. Размер каждого
файла проверен (<10 MiB); line/byte counts выведены при проверке allowlist.
SI-E01.1, approved contracts, старые BLOCKED reports, editorial/Storage, существующие
тесты/golden vectors, config/dependencies/CI и main не изменены.

## API и реализованные проверки

- `validate_si_record(value)` проверяет ровно `{H:header,payload:typed payload}` и
  возвращает detached plain-value copy. Header проверяется принятым model_v1;
  primitive types/Unicode/size/depth — принятым codec_v1. Input не меняется.
- `si_record_ref(value)` сначала валидирует полный record, затем возвращает
  `{type,id,revision,sha256}`: supplied H identity и SHA256 exact C({H,payload}).
- `validate_si_record_ref(value, expected_ref)` валидирует record/ref, сравнивает
  все четыре поля, возвращает detached expected SIRef либо SIValidationError.
  Type mismatch → REF_TYPE_MISMATCH; id/revision/digest mismatch → REF_HASH_MISMATCH
  с path `$.expected_ref.<field>`.

Закрытые payload schemas охватывают Intake, StoryIdea, SourceItem, ClaimItem,
EvidenceItem, ClaimCheck, AudienceHypothesis, ChannelContext, Angle, Rubric,
RunRecord, EvaluationReport, CreativeAlternative, VisualRequirement, Risk,
ProductionBrief, Selection, ReviewPacket. Нет generic unknown-type fallback.
Все required/nullable/enum/primitive поля и nested Known<T>, Criterion, Rating,
Confidence, Provider, ContextSnapshot, PortfolioEntry, Chapter, ProductionOptions,
EvaluationEligibility, SelectionScope, BriefReviewState и privacy structures закрыты.
Origin/SIRef/ERef/H используют принятые foundation validators; Known payload fields
имеют реальные typed validators, без no-op callbacks.

Проверяются rubric unique keys/weights sum100/min0/max5/direction, rating bounds и
UNKNOWN aggregate при UNKNOWN rating; точное соответствие rubric keys/order и
сам численный aggregate требуют внешнего Rubric и здесь не вычисляются. В fixtures
использована утверждённая девятка criteria/весов; generic Criterion.key остаётся
Text, как в approved owner-defined Rubric, не неутверждённый новый enum.
ClaimCheck проверяет reviewer/time/reason/qualification/null правила и required
known nonempty evidence для supported/qualified. Наличие evidence не объявляется
его проверкой. DOCUMENTED visual требует supplied Known licence_basis, не rights grant;
MITIGATED risk — nonempty resolution_basis_refs, не доказательство human review.

RunRecord проверяет шесть approved stage/method pairs с method_version=1-r1,
V1 provider=null, требуемый rubric ref, canonical input manifest и наличие явно
заданных roots в нём, равенство H.input_refs/input_snapshot и frozen editorial
snapshot полей. Никакого выполнения Run и транзитивной closure проверки нет.
Provider shape закрыта; MODEL_DERIVED остаётся распознаваемым reserved Origin в
неизменённом foundation model, не становится новым V1 provider/output path.
UTC остаётся descriptive: clock/order authority не выводится.

StoryIdea/Creative initial/edit modes и previous chain проверяются foundation;
HUMAN_EDIT input roots начинаются с exact previous. У initial Creative payload
run_ref равен origin.run_ref; при edit original creative ref не равен current
Revision ref. Сохранение **того же** исходного CREATIVE run через все предыдущие
records и actual stages этих refs потребует resolver. Selection target type зависит
от scope purpose. Brief проверяет RU/UK alignment, positive min<=max durations,
nullable creative_selection_ref только для DRAFT и его явное присутствие в H inputs,
если он использован. Choice/scope фактического Selection здесь не разрешаются.

Внутри одного объекта одинаковые declared ref identity (namespace/type/id/revision)
не могут иметь разные hashes, включая H и payload. Это equality consistency
переданных значений, **не** cross-record hash verification. SI и editorial ERef
имеют отдельные namespace; одинаковый exact unresolved ref повторять допустимо.

## R1b-P01–P05

| Решение | Реализация/проверка |
|---|---|
| P01 | Только payload-relative exact paths; dot fields, zero-based decimal brackets без leading zero; reject payload/H/type/JSONPath prefixes, aliases, wildcard и неизвестные поля |
| P02 | TEXT whitelist по source_ref.type; text nonnull; exact source/path FieldGrant; local C(display text) согласован с grant digest |
| P03 | STATE whitelist/closed scalar values; EvaluationReport / eligibility.state; blocking только ASCII true/false; STATE grant запрещён; projection review_state/currentness только в typed capture value |
| P04 | REDACTED text=null, matching exact Omission; omission-only permitted; sensitive payload leaf/whole-Known paths только withholding; H и blanket object/list paths исключены |
| P05 | Unique views/items/grants/omissions; manifest/schema traversal/ascending numeric index order без сортировки inputs; локальные membership/matching проверки |

REDACTED/Omission vocabulary механически получается из тех же ordered closed schemas,
включая scalar leaves nested values/refs и whole Known fields. Non-scalar object/list
пути отвергаются. SourceItem.title.value и индексы проверяются структурно; реальная
KNOWN branch/nonnull field/index existence в **исходном source record** здесь неизвестны.
Numeric path order вычисляется без int-conversion произвольно длинного index.

Packet проверяет source manifest uniqueness/order, explicit roots и display/grant/
omission source membership, исключение текущего Packet/export Run из source closure,
локальный snapshot digest и grant snapshot digest, capture context hash и heads,
согласованность captured Brief ref. Эти проверки **не** доказывают полноту closure.
TEXT digest consistency означает только согласованность переданных display text/grant;
подлинность source bytes, user privacy consent и отсутствие секретов/PII не доказаны.
Никакой export/file/network action не выполняется.

## Независимые literal vectors и тесты

В новом vectors файле зафиксированы **18 complete record** byte/SIRef literal vectors
(по одному на каждый тип), включая все семь обязательных типов RunRecord, StoryIdea,
CreativeAlternative, EvaluationReport, ProductionBrief, Selection, ReviewPacket.
Packet vector содержит granted TEXT, STATE и REDACTED/Omission, а не только empty view.
Дополнительно **3** byte/hash literals: FieldGrant `title`, FieldGrant
`title_options[0]`, STATE FieldView `eligibility.state` — последний без grant.

Expected bytes/refs сформированы отдельным одноразовым reference script через stdlib
JSON (sort_keys, ensure_ascii=False, separators без пробелов) и hashlib. Все 21 SHA
независимо сверены `openssl dgst -sha256`; production si_record_ref/SI/S1 codec не
вызывались для вычисления expected values. Fixtures используют собственный stdlib
canonical helper. В test definition expected values буквальные, не production-derived.
Generator/logs остаются вне Git; OpenSSL не runtime/test dependency.
В executable tests есть byte parity с S1 только на общем valid subset.

Это независимые синтетические **single-object** fixtures с unresolved refs, не единый
согласованный record graph/workspace и не утверждения о фактах/правах/human identity.
Проверяется точный hash объекта, не cryptographic verification чужого source record.
Прежние 14 SI-E01.1 vectors и storage golden vectors не изменены.

P-T01–P-T12 имеют отдельные тестовые методы, покрывающие spelling/indexes/STATE/
private fields/duplicates/order и frozen capture. P-T04/source existence и P-T12
observed currentness явно разделяют local syntax от будущего resolver/export.
Positive/negative cases охватывают все 18 types, каждый required payload field,
wrong primitive/unknown fields и более 500 вложенных missing/unknown-field cases,
Known/nullable/UTC/bool/typed-ref constraints, locale/duration, ref tampering, limits
и input/copy independence. Это не выполнение всех 56 operation/domain acceptance cases.

### Фактические прогоны

Среда: Linux x86_64, Python 3.12.14; проектный `.venv/bin/python`.
Финальный целевой command:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

Целевой окончательный запуск: **61 OK**, 1.330 s, exit0:
31 принятый foundation + 30 новых methods (27 record + 3 vector).
Полный окончательный запуск: **903 OK**, 846.622 s, exit0; failures=0,
errors=0, skipped=0, expectedFailures=0. Это 873 прежних + 30 новых test methods.
Все существующие S1/S2/D-01/golden/LAB regressions прошли. S2.3 дополнительно
сообщил 1659 параметризованных сценариев (не дополнительные unittest methods).
`test_sprint23_2.Sprint232Tests.test_env_override` прошёл на Linux; baseline ошибок
окружения не выявлено. Windows-specific qualification этим не заявляется.

Перед commit выполнены `git diff --check`, staged diff check, exact четырёхфайловый
A-only allowlist, syntax и local Markdown links/fences checks. Повторная независимая
AST-literal/std JSON/hashlib/OpenSSL сверка всех 21 vectors прошла без production
imports. Все шесть принятых SI-E01.1 файлов и оба исторических BLOCKED reports
побайтно совпали с frozen commits; R1b contract совпал с pinned proposal. Нормализация
trailing spaces approval note уже присутствует в предоставленной базе, текст
решений совпадает; мы её не меняли. Post-push exact HEAD/parent/remote equality и
clean worktree проверяются в handoff после публикации.

Development evidence сохранено честно: первый temporary generator запуск не имел
workspace в PYTHONPATH (ModuleNotFoundError); последовавший incomplete vectors-module
targeted run дал 58 executed/1 import error. Temporary import path исправлен,
получены все literal vectors, повторные targeted runs — 60 OK. Это не baseline failure.
Дополнительный regression test обнаружил локальное принятие двух hashes одной ref
identity: исходно 1 FAIL, после исправления только records_v1.py — 1 OK, затем
61 OK всей SI suite. Предварительный полный discovery прерван SIGINT (exit130) до
этого исправления и **не объявляется PASS**; после исправления запущен заново.
Существующие tests/source не менялись и failure/skip suppression не применялось.

## Ограничения и STOP

Runtime — только stdlib и принятые SI-E01.1 модули, без editorial/storage imports,
I/O, subprocess/network, clock/UUID/key generation, provider, renderer или persistence.
Single-record SI limits 1_000_000 UTF-8 bytes / 100_000 codepoints / 32 containers
сохранены. Bundle limits/1 MB integer latency benchmark не выполнялись;
SI-F01 остаётся nonblocking, новый digit cap не введён.
Нет execution Discovery/Evaluation/Creative/Brief/Packet операций, replay/currentness
engine, trusted author/reviewer/rights/privacy authority или production handoff.
S1/S2/D-01/S3 не менялись; S3.2b BLOCKED_HOST_NOT_PROVIDED,
PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF. Linux tests не
квалифицируют native Windows.

Перед SI-E01.2b нужны независимая приёмка и отдельное bounded задание: настоящий
resolver/exact external hashes, транзитивный DAG/closure, stage/method binding через
refs, R1a original run retention, operation prerequisites, source field/value/index
и qualification matching, semantic currentness. Ни один из этих механизмов не
подменён локальными hashes/labels. SI-E01.2b/SI-E02 не начинались.
PR/merge/release/main изменений нет. После публикации — STOP.
