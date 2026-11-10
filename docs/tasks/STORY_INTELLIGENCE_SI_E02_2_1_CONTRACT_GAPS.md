# SI-E02.2.1 — Contract gaps

Дата: 2026-11-10. **BLOCKED_CONTRACT / PRE_IMPLEMENTATION.**
Base: `9f636d3650b7e5eda4b6f6b7cfa90e43fba12744`.
Task: owner handoff «SI-E02.2.1 — Bounded Pure EVALUATE Engine — First Implementation».
Это evidence и вопросы для owner review, не изменение утверждённых правил.
EVAL-G01 — локальный ID finding этого этапа, не прежний approved currentness G01.

## EVAL-G01 — Не определена машинная граница качественных eligibility findings

### Утверждённые требования и существующие данные

[R1 §3.2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) требует:

- п.4: «UNKNOWN confidence без достаточного обоснования → NEEDS_RESEARCH»;
- п.5: «Неразрешённый duplicate → REVIEW_DUPLICATE»;
- п.6: достаточные inputs/объяснённые ratings/assumptions и отсутствие unresolved duplicate → ELIGIBLE_FOR_CREATIVE.

Scoring и порядок этих правил однозначны. Пробел находится в вычислении двух
предикатов, а не в весах, formula или статусах.

[Original §4](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md) задаёт dedup/1 lookup hints,
включая NFC+casefold+space collapse для title lookup, и отдельно требует человеческого
сравнения разных вопросов/периодов/audience/angles. Совпадение материала не равняется
одной истории. Distinct-story decision описан как новая Angle/Selection с reason.
Но existing Selection предназначен для Creative/Brief, не обязательный input EVALUATE;
Topic Intent сейчас не valid SI/1 и не должен становиться prerequisite.
Angle.distinction и PortfolioEntry.angle_notes — свободный Text, не закрытый статус
человеческого разрешения конкретной duplicate pair.

[R1 §1.2/§3](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) задаёт
Confidence = {level:LOW|MEDIUM|HIGH|UNKNOWN,basis:Text}.
[records_v1](../../story_intelligence/records_v1.py) проверяет nonempty Text, но не
«достаточность» basis. Новое задание не задаёт deterministic predicate достаточности,
способ передачи явного человеческого finding либо правило для неоценимого basis.

### Две конкретные нерешённые границы

| Вход | Что однозначно | Что нельзя самостоятельно выбрать |
| --- | --- | --- |
| Девять KNOWN ratings с UNKNOWN confidence и непустым human-authored basis | Aggregate вычисляется; confidence сохраняется UNKNOWN | Любой nonempty basis достаточен? UNKNOWN всегда NEEDS_RESEARCH? Нужен отдельный human finding? Эти варианты дают разный eligibility |
| Exact локальный portfolio содержит совпадающий normalized title; Angle.distinction содержит человеческое объяснение другого вопроса | Это duplicate candidate, не доказательство одинаковой истории; exact graph остаётся валиден | Как проверить, что human comparison разрешил именно эту pair? Считать любой distinction разрешением, всегда unresolved либо принимать явный finding? |

Всегда считать UNKNOWN confidence «необоснованной» — тоже новая политика, а не
нейтральный fail-closed validation: R1 различает случаи с достаточным обоснованием.
Считать любой непустой Text достаточным позволяет формальному заполнению поля снять
research gap. Парсить magic words/hidden JSON в basis/distinction/reason нельзя.
Всегда unresolved при title match игнорирует возможность human distinct-story review.

## Воспроизводимое evidence на exact base

Ниже диагностический script, **не evaluator и не новый runtime API**. Использует
существующие синтетические test builders и настоящие SHA-256, без mocks. Никаких
файлов/сети/production writes. Выполнен в `.venv/bin/python` (Python 3.12.14), exit 0.
Он доказывает только structural/graph/provenance/currentness validity и однозначную
арифметику, а не scientific/rights sufficiency или expected eligibility.

```python
from copy import deepcopy
from tests.test_story_intelligence_records_v1 import fixtures, known
from tests.test_story_intelligence_resolver_v1 import Graph, digest
from tests.test_story_intelligence_provenance_v1 import data_refs
from story_intelligence.provenance_v1 import verify_si_provenance
from story_intelligence.currentness_v1 import check_si_currentness
from story_intelligence.resolver_v1 import resolve_si_closure

T, g = fixtures(), Graph()
def put(kind, **updates):
    v = deepcopy(T[kind]); v['payload'].update(updates)
    return g.add(v, data_refs(v))

i = put('Intake', user_goal=known('Синтетическая evergreen постановка'))
d = g.run('DISCOVERY', [i])
v = deepcopy(T['StoryIdea'])
v['H']['origin']['run_ref'] = d; v['H']['input_refs'] = [i]
v['payload'].update(intake_ref=i, title='Синтетическая тема', source_refs=known([]))
idea = g.add(v, data_refs(v)); prior = g.add(v, data_refs(v))
a = put('AudienceHypothesis', region=known('Синтетический регион'),
        knowledge_level=known('Начальный'), motivation=known('Изучение'),
        interests=known(['История']), age_range=known('Взрослые'),
        assumptions=['Не статистика'])
k = put('ChannelContext', audience_ref=a, portfolio=known([dict(
        story_ref=prior, published_title='Синтетическая тема',
        published_locator=known('synthetic:portfolio'),
        published_at=known('2026-11-09T00:00:00Z'),
        angle_notes='Ранее рассмотренный вопрос', basis_ref=i)]),
        analytics=known('Синтетическая гипотеза, не статистика'),
        capability_notes=known('CPU-only'))
an = put('Angle', idea_ref=idea, audience_ref=a, claim_refs=[],
         distinction='Человек отметил иной вопрос; требуется ли ещё distinct-story review?')
r = put('Rubric'); roots = [idea, an, a, k, r]
active = [x for x in g.closure(roots) if x['type'] != 'RunRecord']
closure = resolve_si_closure(g.records, roots)
assert closure == verify_si_provenance(g.records, roots)
for root in roots:
    assert check_si_currentness(g.records, root, active, []) == {
        'currentness': 'CURRENT', 'reason_codes': []}
ratings = [dict(criterion_key=x['key'], value=known(5), basis_refs=[an],
    explanation='Явное синтетическое суждение человека', confidence=dict(
        level='UNKNOWN', basis='Количественная уверенность не установлена; ограничения рассмотрены человеком'))
    for x in T['Rubric']['payload']['criteria']]
assert 2 * sum(x['weight_percent'] * 5 for x in T['Rubric']['payload']['criteria']) == 1000
assert digest(g.records) == '0b8357be81a1d7a8ff44d1172ac3025d9fa3759e2253301c870d0820f1553f2f'
assert digest(ratings) == '5efe1d16a0d4d941a33324d5320af7bea9b899817b27a292648727e90abd5581'
```

Фактически: 8 records, canonical Closure из 8 refs, все 5 domain roots CURRENT;
нет ERefs, Creative/Selection/Brief или missing/hash/provenance failure.
Все девять supplied values KNOWN 5, independent arithmetic = 1000.
UNKNOWN confidence basis и совпадающий portfolio title присутствуют одновременно.

**Eligibility не вычислялся.** Потенциально различающиеся NEEDS_RESEARCH /
REVIEW_DUPLICATE / ELIGIBLE_FOR_CREATIVE здесь показывают проблему предикатов;
это не три доказанно допустимых результата и не утверждение, что все прочие
eligibility conditions этого synthetic graph достаточны. Нельзя выбрать один из них
по одному CURRENT/1000 или presence of Text. Это contract gap, не дефект принятых APIs.

## Минимальное решение владельца для resume

Нужен узкий контракт входных findings и их отображения в existing eligibility:

1. Кто оценивает достаточность UNKNOWN confidence basis; какое exact явное значение
   получает pure decision function, его scope/binding к supplied ratings/inputs,
   validation и поведение при отсутствии/противоречии finding.
2. Как передаются duplicate candidate/pair и результат человеческого distinct-story
   comparison; exact binding к Idea/Angle/portfolio refs, unresolved/missing behavior.
3. Какие existing reason codes и deterministic ordering используются для этих
   findings и всех одновременно присутствующих причин. Не вводить новый vocabulary.

Возможный **неутверждённый** путь: caller-supplied non-persisted human findings для
bounded in-memory функции, с закрытой формой и exact binding; либо точная разрешённая
интерпретация существующих полей. Выбор не сделан. Новый persisted record, Topic Intent,
ERef adapter, Scientific Review automation или SI-D03 writer для этого не требуются.
Если желателен только arithmetic component, это отдельное явное сужение задания:
текущий этап требует всю eligibility precedence и соответствующие tests.

## STOP

Реализация, focused evaluator tests и новые vectors не создавались. Принятые API,
контракты и golden vectors не изменены. Не объявлять schema limitations новой wire
архитектурой и не переносить эту блокировку на все будущие ERef-free вычисления.
См. [RESULT](STORY_INTELLIGENCE_SI_E02_2_1_RESULT.md).
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes.
**BLOCKED_CONTRACT; STOP для independent review.**
