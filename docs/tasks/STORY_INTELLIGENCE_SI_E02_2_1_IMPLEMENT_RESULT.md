# SI-E02.2.1-IMPLEMENT — Bounded Pure EVALUATE V1

Дата: 2026-11-12. Статус: IMPLEMENTED / PENDING INDEPENDENT ACCEPTANCE.
Квалификация: PURE_BOUNDED_EVALUATE_ONLY; не production integration/owner approval.

## Git и разрешённый объём

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Exact source: `docs/story-intelligence-si-e02-2-1f-base-classifier-approval`.
- Base и единственный parent нового implementation commit:
  `6c0f390ada6c8c3d2100e3f83e6fbfce697660dc`.
- Feature: `feat/story-intelligence-si-e02-2-1-implement-pure-evaluate`.
- До редактирования проверены remote source HEAD, local HEAD, clean worktree и
  отсутствие unmerged paths; exact base совпал.
- Main baseline: `e1f4efb0fb5ff290bb198349213c004b4667ef0f`.
- Полный commit SHA и remote HEAD сообщаются в публикационном ответе после создания
  коммита. Сам документ входит в этот commit; его собственный SHA не вставляется
  в его содержимое. Проверяемая identity: commit, добавляющий этот файл, и его parent.

Diff: пять новых файлов (A), 1861 добавленная строка, 0 удалений; существующие файлы не изменены:

| Файл | Назначение |
| --- | --- |
| `story_intelligence/evaluate_v1.py` | Pure entry point, закрытая local validation, semantic source/claim/risk projection, scoring/classifier |
| `tests/test_story_intelligence_evaluate_v1.py` | Numeric/findings/binding/locale/purity/Q1/Q2/Q3 regression tests |
| `tests/test_story_intelligence_evaluate_oracles_v1.py` | C01–C48, exact T25 и его bounded regressions |
| `tests/story_intelligence_evaluate_fixture_support.py` | Независимо построенные content-addressed graphs/local bindings; не test module |
| `docs/tasks/STORY_INTELLIGENCE_SI_E02_2_1_IMPLEMENT_RESULT.md` | Этот отчёт |

## Entry point и результаты

```python
evaluate_si(records, semantic_input_refs, observed_context, ratings,
            expected_context, human_findings,
            required_current_premise=None, *, ui_locale=None)
```

`records` — список существующих полных SI/1 records; `semantic_input_refs` — точный
ordered список roots с однозначными Idea/Angle/Audience/Channel/Rubric roles и
дополнительными явно переданными domain roots. Оба context arguments — существующие
полные `ContextSnapshot`: active refs, selection heads и editorial snapshot marker.
Это сохраняет explicit context без нового request/operation/wire envelope.
`human_findings` и premise используют утверждённые closed local contracts.
Locale определяется exact Audience/Idea Intake (`ru`/`uk`); optional `ui_locale`
проверяется на совпадение, не переводит содержимое.

Возвращается detached plain dict:

- При успехе: `status="OK"`, `currentness="CURRENT"`, locale, исходные detached
  ratings, `aggregate_tenths` Known/Unknown, `eligibility={state,reason_codes}`,
  ordered `diagnostics` с existing code/path/ref/message.
- При отказе: `status/currentness="INVALID"|"STALE"`, `locale=null`,
  `eligibility=null`, `aggregate_tenths=null`, `ratings=[]`, lexical unique
  `reason_codes`, safe diagnostics. Accepted eligibility при отказе отсутствует.

Canonical SI validation/refs/graph/provenance/currentness переиспользуются без
изменений. Local schemas опираются на read-only grammar принятых SI validators;
новые SI/1 типы, error codes или canonical protocol не вводятся. При изменении
этой внутренней grammar нужна совместимость нового evaluator, а не скрытая копия
полного codec. Никаких patch/mock accepted-success путей нет.

## Реализованная проверка

1. Закрытые shapes, exact refs/hashes, complete audit/provenance и локальные bindings
   проверяются до eligibility. Неполные/повреждённые данные — INVALID. Genuine
   старый frozen context — STALE; relevant ERef INVALID имеет приоритет над STALE.
2. Main semantic projection отделена от audit `H.previous`/Run snapshots. Обычный
   HUMAN_EDIT использует current payload; исходный CREATIVE сохраняет G01/G02
   substantive constraints. Actual producer ERefs не обходятся через HUMAN_EDIT.
3. Q1 добавляет все применимые явно active checks/evidence exact claim; Q2 — active
   Risk с basis в main projection. Independent disputed/removed/unreviewed review
   не исчезает от positive Check другой identity. Old declared main Check требует
   exact active выбора; implicit latest отсутствует.
4. Источники формируют exact canonical sorted set. Proof-only material отдельно
   graph/provenance/currentness-проверяется и не запускает рекурсивную freshness
   coverage. Current evidence path сохраняет источник после изменения Idea source.
5. Required-current: REQUIRED/NOT_REQUIRED/UNDETERMINED, ordinary applicability,
   missing/partial specs, exact digests, coherent support, inclusive Q ⊇ R и
   один E ⊇ Q. Stitching/TTL/clock inference отсутствуют. D01–D16 paths/messages
   сохранены; unique declared reference failures нормализуются к local fields.
   Для ERef в proof-material C34 не дублирует одну failure на enclosing check/evidence
   queries: остаётся независимо проверенный exact material-ref diagnostic.
6. Девять keys/weights и профиль `(si-rubric,1,1)` обязательны. All KNOWN:
   `2 * sum(weight * rating)`; UNKNOWN не превращается в zero/renormalized score.
   Confidence findings не меняют rating/confidence/score. Portfolio проверяется
   exhaustively по exact entry index/digest/candidate, без title matching.
7. Q2 generic Risk использует EVIDENCE_NEEDED/class BLOCKED по alternative A;
   Visual RIGHTS_BLOCKED остаётся отдельной diagnostic. Prose/fallback/high score
   не снимают блокировки; MITIGATED требует genuine human revision/coherent review.
8. Q3 knowledge_level/motivation/capability_notes UNKNOWN дают NEEDS_INPUT только
   в bounded EVALUATE. Optional hypotheses могут оставаться UNKNOWN. Все applicable
   nonfatal diagnostics сохраняются по class/code/path/C(ref)/message, codes dedup
   отдельно от diagnostic tuples. Private local reason/unknown key не копируются
   в generated messages или paths; существующие SI validators не изменялись.

## Независимые тесты и покрытие

Expected numeric values, eligibility, diagnostics и локальные binding bytes строятся
независимо от evaluator. Fixture helper использует stdlib JSON/SHA-256 и existing
independent test Graph; не импортирует evaluator. Только искусственные данные.
Accepted resolver/provenance/currentness действительно выполняются.

| Требования | Исполненное покрытие |
| --- | --- |
| N01–N04 | Literal 0 / 1000 / 510 / UNKNOWN; high score не clearance |
| T01–T09, T36–T37 | UNKNOWN confidence, SUFFICIENT/INSUFFICIENT/missing, duplicate identical/conflicting findings, exact rating/list/binding hashes, invalid Rubric, stale genuine Rubric |
| T10–T22 | DISTINCT/DUPLICATE/UNRESOLVED/missing, three entries, duplicate index, repeated candidate across entries, out-of-range/bool index, wrong candidate/entry digest, stale Channel/candidate, KNOWN[] versus UNKNOWN portfolio |
| T23–T26 | Central blocker despite score/findings, combined research+duplicate, exact T25, deterministic detached repeat/changed reason |
| T27 | DEFERRED / NOT IMPLEMENTED — outer request integration EVAL-P05 OPEN |
| T28–T30 | Unapproved request_id, missing target, wrong hash/type/shape, genuine wrong generator accepted by resolver but rejected by provenance, self-input cycle |
| T31–T33 | Historical-only versus relevant actual producer ERefs; original/current/historical Creative Run boundary; original C direct claim; INVALID over STALE |
| T34–T35, T38 | Closed schemas/order/tags, privacy-safe unknown keys including nested/dotted names and invalid value, malformed contexts, ru/uk/exact Unicode, unrelated Selection-head context change |
| C01–C48 | Named independent executable tests for every RC row; multiple temporal/duplicate/malformed subcases |
| Q1 matrix | 81 graph evaluations: 3 kinds × 3 materialities × 9 review conditions (including no Check and supported/qualified insufficient support) |
| Q2 matrix | 144 graph evaluations: 6 categories × 4 severities × 3 resolutions × 2 blocking values; independent mitigation/rights/fallback tests additionally |
| Q3 | Essential UNKNOWN versus permissible hypotheses, source scope, supported exact profile |

C16/C17 воспроизводят исходный EVAL-RESUME-G01 graph/ratings/findings/context без
изменения старых bytes. Четыре независимых literal hashes совпадают с опубликованным
CONTRACT_GAPS §3:

```text
records  d0629b82eeb589253199ac0dcd9a8ee71bf76a942780dde5fd45bd41c46a8b61
ratings  3a3e6fe51ce5715364ba7d7fe83c612749a2528ce44f472c8802e796cec987fd
findings cff2c041ed8a348e52727ea47a26c088aa8aae1b56184fed06ddbe6b304d7eeb
context  89c43e0d9c54cb16d749c5acc19f133549c1512fe4effa5de65a335da8a67e5b
```

T25 — exact approved 11-record fixture, genuine canonical refs; четыре diagnostic
словари сравниваются полностью, включая input_ref hashes, порядок и fixed messages.
Буквальные independent fixture digests дополнительно зафиксированы в новом тесте:

```text
records 684e05d29daf0900b1e8579cba4afe8367a8261f2effc6bfee4af3cce7900b8f
ratings 46b559566d812d98e593aceaf1c118cca51e8fecdd8b6bf855d0f0db7772a6f6
binding 7edbcb32f1abcfb3e801eb009ca367f90a3e063ccacc7af317b0723c647b34f8
```

T25: BLOCKED, aggregate UNKNOWN с approved reason, codes ровно
`[DUPLICATE_REVIEW_NEEDED,EVIDENCE_NEEDED]`, четыре tuples в approved порядке.
Также exact composed LEGAL+Visual tuples C14/C44; удаление одного condition T25
в новом coherent fixture не удаляет остальные diagnostics.
Existing golden vectors/approved contracts не изменялись.

## Фактические проверки

Python 3.12.14, проектная `.venv`, Linux CPU-only. Окончательные команды:

| Команда | Tests | Exit | Результат |
| --- | ---: | ---: | --- |
| `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_evaluate*.py' -v` | 78 | 0 | OK (46.962 s) |
| `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v` | 222 | 0 | OK (64.474 s) |
| `.venv/bin/python -m unittest discover -s tests -v` | 1064 | 0 | OK (823.073 s) |
| `.venv/bin/python -m compileall -q story_intelligence tests` | — | 0 | OK |
| `git diff --check` и staged diff check | — | 0 | OK |

Unit-test counts — collected methods, не число subcases. Одни Q1/Q2 matrices дают
225 graph evaluations сверх этой интерпретации count; они не выдаются за 225 методов.
Development iterations выявили неверные исходные test fixture enum/MITIGATED basis,
исправленные только в новых fixtures; initial 49-oracle run имел один failure C32,
исправленный в новом evaluator. Дополнительная privacy regression сначала показала
раскрытие unknown key до closed shape validation; теперь closed schema проверяется
первой, canonical failure path rebased к explicit argument. Полные development
прогоны, прерванные для завершения этих изменений, не считаются PASS. Итоговые
counts/exits выше относятся к окончательной версии, не к промежуточным файлам.

## Ограничения и STOP

Новых blocking contract gaps не обнаружено. Чистая функция проверяет consistency
предоставленного view, а не completeness внешнего реестра отрицательных решений,
реальную научную истину, выполнение DISCOVER/EVALUATE, identity/authority reviewer,
материальную доступность, подлинность лицензии или production permission. UNKNOWN
не заменяется предположением. Snapshot hash не заменяет отсутствующий ERef adapter.

Не реализованы persisted operation/RunRecord/EvaluationReport/Selection creation,
request_id/cache/replay, clock/randomness, I/O/network/LLM/GPU/provider, UI, Discovery,
Creative, Brief, ERef adapter, protected storage или Windows native integration.
Нет dependency additions. Существующие SI/editorial/storage, contracts, schemas,
tests/golden vectors и configuration сохранены.

EVAL-P05 **OPEN**; PUBLISH_REVISION **DISABLED**; partial COMMIT reconstruction **OFF**;
Windows S3.2b **BLOCKED_HOST_NOT_PROVIDED**. PR/merge/release/main changes отсутствуют.
После публикации feature branch — **STOP FOR INDEPENDENT ACCEPTANCE REVIEW**.
