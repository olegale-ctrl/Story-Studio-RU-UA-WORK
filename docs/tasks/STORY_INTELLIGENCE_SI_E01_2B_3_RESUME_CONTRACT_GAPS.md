# SI-E01.2b.3-RESUME — G02: roles of direct CREATIVE claim inputs

Дата: 2026-11-10. **BLOCKED_CONTRACT / NO IMPLEMENTATION.**
Base: `e735d729f6dad8ff874a92d52b37f4a95bb8fc20`.

## Что утверждено и не пересматривается

[Owner approval G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md)
утверждает D1–D5. Исторический edit-base не required-current; exact ancestry всё
равно проверяется. Original CREATIVE Run C и его EvaluationReport/ChannelContext
не заменяются. Source S3 не требует active S1/S2, text-only K3 не требует active K1/K2.
Это больше не открытый вопрос. Новый G02 касается только сопоставления **нескольких
прямых ClaimItem входов C** с заменяемыми hook/chapter roles, а не D1.

[RESUME task](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CODEX_TASK.md) §3 прямо задаёт:

> If typed schema and approved R1/R1a/G01 do not determine how to inherit or override a particular substantive ref (e.g. multiple same-type claims, original evaluation versus revised angle), STOP and record the exact ambiguous fixture, competing results, and minimal owner choice.

§5 при повторном BLOCKED_CONTRACT разрешает только RESUME_RESULT + RESUME_CONTRACT_GAPS,
без partial currentness code/tests. Эта ветка следует указанной границе.

## Точная граница недоопределённости

| Норма | Что известно | Что не задано |
| --- | --- | --- |
| [R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) §1.2/§2 | C.semantic_input_refs — List<SIRef>; CREATIVE roots включают Angle/Idea/Audience/Channel/Evaluation и claim/check/source roots | У элемента списка нет field/role; порядок не кодирует соответствие hook/chapter или независимому ограничению |
| [G01 proposal](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_DECISION_PROPOSAL.md) D2 | Current payload field заменяет старое значение **той же роли** | Как установить эту роль для прямого ClaimItem в C.semantic_input_refs |
| G01 D3 | hook_claim_refs и chapters.claim_refs управляют соответствующими ролями; still-applicable source/claim/check/evaluation bindings сохраняются exact | Является ли совпадение C-root с genesis hook/chapter достаточным и исключительным доказательством заменяемой роли, либо root может дополнительно оставаться ограничением генерации |
| [R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md) §4 | Immutable C; HUMAN_EDIT roots = base + current payload refs; claim qualifications сохраняются | Нет C input-role map; previous/genesis payload показывает использование claim, но не исключительность producer-root роли |
| Accepted [records schema](../../story_intelligence/records_v1.py) | Закрытые payload; у C generic ref list, у K отдельные hook/chapter fields | Нельзя добавить role annotations/новый field или трактовать Text как скрытую machine-readable карту |

Typed `ClaimItem` определяет вид записи, но не различает роли «использован в hook»
и «самостоятельный frozen input генерации». Чтение K1.payload может показать первое,
но не доказывает отсутствие второго. Подстановка по позиции C-root, по типу или по
совпадению с первым найденным claim была бы новым алгоритмом mapping.

## Настоящий ERef-free counterexample

Синтетический bundle построен заново стандартными JSON/SHA-256 helpers существующих
тестов; accepted resolver/hash/provenance не подменяются. Все 19 записей доступны,
все exact hashes и Run snapshots проверены. Применено D1: K1/K2 и C не active.
Angle, Idea, E1, Channel и все их domain bindings **не меняются**.

- C.semantic_input_refs = `[Angle, Idea, Audience, Channel, E1, Qa, Qb]`.
- K1.hook_claim_refs = `[Qa]`; K1.chapters[0].claim_refs = `[Qb]`.
- K2/K3.hook_claim_refs = `[Qc]`; chapters сохраняют `[Qb]`; angle_ref прежний.
- C остаётся тем же exact payload.run_ref у K1/K2/K3. R2/R3 — настоящие REVISION Runs
  с base-first roots и полной canonical audit Closure.
- Qa/Qb/Qc — разные fictional ClaimItem, CONTEXT, без ERefs/qualifications. Они не
  объявлены фактами/reviewed evidence. E1/Angle не содержат claim bindings; E1 ratings
  не ссылаются на эти claims. Нет отдельного retained Check/Risk, который сам по себе
  однозначно требовал бы Qa и разрешал вопрос независимо от роли C-root.
E1 имеет NEEDS_RESEARCH; это не ошибка provenance и не запрет на проверку
currentness. CURRENT не означал бы eligibility/выбор/разрешение производства.

- Observed active = `[I, S, Idea, Audience, Channel, Angle, Rubric, E1, Qb, Qc, K3]`
  (в canonical SIRef order); observed heads = `[]`. Qa исторически resolve, но не active.
  Одна exact revision на (type,id); нет отсутствующих/повреждённых/невалидных refs.

Aliases здесь сопровождаются реальными wire identities. Общий suffix всех UUID:
`-2222-4222-8222-222222222222`; prefix ниже — полные первые 8 hex digits.

| Alias | type | UUID prefix | revision | literal sha256 |
| --- | --- | --- | --- | --- |
| Qa | ClaimItem | 00000003 | 1 | `0ff944d7642a3a186b1bf8cdb1859c400c2a4d30adb24ade8edb67cd83a9e42a` |
| Qb | ClaimItem | 00000004 | 1 | `0056012219cff431ed11f703acc14800bb289a1465140531881cdfe31a89224d` |
| Qc | ClaimItem | 00000005 | 1 | `d575f44dced484725385525a6d379472521abf66465c789a6b76915ddd48214a` |
| Angle | Angle | 0000000a | 1 | `c4a00a5cf74b16cc27d500f75c4059fc571e205ab7bf88e7c197475f585fdefd` |
| E1 | EvaluationReport | 0000000d | 1 | `4b5efb71963cccc40fef2b9977366c076765bd4bf03371f7fc43231585b2d98d` |
| C | RunRecord | 0000000e | 1 | `0099be3529a8f7266f1673abb9b102fceb09061fde6a39fb7f5ff3ab3f84dd58` |
| K1 | CreativeAlternative | 0000000f | 1 | `5689b6bb5d48f613fd50c5637f9735f01c952b4ced8f8fdd44353003b58956f2` |
| K2 | CreativeAlternative | 0000000f | 2 | `684661bfed9c4b483330628428684cb86297f1bfb4ed4113c5ac9bea106efb4c` |
| K3 | CreativeAlternative | 0000000f | 3 | `7a88b9dadaa313c51e910752a908582e03b1d3c3dcf954640cf38c42e5d8a967` |

`SHA256(C(g.records))` in construction order:
`d8f2a8439f9ce3cfa6db385382eb07cbe296e1edc29ccfac5f52a07090be0975`.
`SHA256(C({'active_input_refs': active, 'selection_head_refs': []}))`:
`2e29b4a85cb640df76ffdbad34214f95f53a5e8fd58d5a298746be2e7ef8be0d`.
Это test observation value, **не** новый wire ContextSnapshot или trusted-current proof.

### Воспроизведение без изменения репозитория

Запустить следующий фрагмент через `.venv/bin/python -` из root. Это construction/
validation reproducer, не currentness implementation. Helpers Graph/data_refs —
только независимый test-fixture oracle; production API занимается проверкой.

```python
from copy import deepcopy as cp
from tests.test_story_intelligence_resolver_v1 import Graph, key, digest
from tests.test_story_intelligence_records_v1 import fixtures, known
from tests.test_story_intelligence_provenance_v1 import data_refs
from story_intelligence.provenance_v1 import verify_si_provenance
from story_intelligence.resolver_v1 import resolve_si_closure

t = fixtures()
g = Graph()
def put(kind, **updates):
    v = cp(t[kind])
    v['payload'].update(updates)
    return g.add(v, data_refs(v))

i = put('Intake')
s = put('SourceItem')
qa = put('ClaimItem', statement='Синтетична гіпотеза A', claim_kind='fictional')
qb = put('ClaimItem', statement='Синтетична гіпотеза B', claim_kind='fictional')
qc = put('ClaimItem', statement='Синтетична гіпотеза C', claim_kind='fictional')
d = g.run('DISCOVERY', [i, s])
v = cp(t['StoryIdea'])
v['H']['origin']['run_ref'] = d
v['H']['input_refs'] = [i, s]
v['payload'].update(intake_ref=i, source_refs=known([s]))
idea = g.add(v, data_refs(v))
au = put('AudienceHypothesis')
ch = put('ChannelContext', audience_ref=au)
a = put('Angle', idea_ref=idea, audience_ref=au, claim_refs=[])
ru = put('Rubric')
eroots = [idea, a, au, ch, ru]
er = g.run('EVALUATION', eroots, rubric=ru)
v = cp(t['EvaluationReport'])
v['H']['origin']['run_ref'] = er
v['H']['input_refs'] = eroots
v['payload'].update(idea_ref=idea, angle_ref=a, audience_ref=au,
                    channel_ref=ch, rubric_ref=ru, run_ref=er)
e = g.add(v, data_refs(v))
croots = [a, idea, au, ch, e, qa, qb]
c = g.run('CREATIVE', croots)
v = cp(t['CreativeAlternative'])
v['H']['origin']['run_ref'] = c
v['H']['input_refs'] = croots
v['payload'].update(angle_ref=a, run_ref=c, hook_claim_refs=[qa])
v['payload']['chapters'][0]['claim_refs'] = [qb]
prior = g.add(v, data_refs(v))
for revision in (2, 3):
    v = cp(g.refs[key(prior)])
    v['payload']['hook_claim_refs'] = [qc]
    v['payload']['hook_text'] = f'Уявний сюжет, редакція {revision}'
    roots = [prior] + data_refs(v['payload'])
    r = g.run('REVISION', roots)
    v['H'].update(revision=revision, previous=prior, input_refs=roots,
        origin={'mode':'HUMAN_EDIT', 'run_ref':r, 'imported_from':None})
    prior = g.add(v, data_refs(v), keep_identity=True)
active = sorted([i, s, idea, au, ch, a, ru, e, qb, qc, prior], key=key)
manifest = verify_si_provenance(g.records, [prior])
assert manifest == resolve_si_closure(g.records, [prior]) == g.closure([prior])
verify_si_provenance(g.records, [prior] + active)
assert len(g.records) == len(manifest) == 19
assert len({(r['type'], r['id']) for r in active}) == 11
assert digest(g.records) == 'd8f2a8439f9ce3cfa6db385382eb07cbe296e1edc29ccfac5f52a07090be0975'
assert digest({'active_input_refs':active, 'selection_head_refs':[]}) == '2e29b4a85cb640df76ffdbad34214f95f53a5e8fd58d5a298746be2e7ef8be0d'
print('19 exact audit refs and provenance OK; currentness NOT IMPLEMENTED')
```

### Два возможных правила дают разные результаты

Это **варианты для решения владельца**, не результаты существующего API:

| Вариант | Проекция | Результат для exact observed set выше |
| --- | --- | --- |
| A: root, совпавший с genesis hook/chapter ref, считается заменяемым input этой роли | Qa был hook-only, текущий hook содержит Qc; Qb сохраняется для chapter; остальные E1/context constraints неизменны | CURRENT |
| B: direct claim root C также сохраняется самостоятельным producer constraint, пока контракт явно не снимает эту роль | Qa заменён в hook, но original C всё ещё требует exact Qa как generation input | STALE / INPUT_STALE, поскольку Qa отсутствует в active |

Нельзя вывести исключительность hook-only роли из самого факта, что Qa был в
K1.hook_claim_refs. Нельзя объявлять все direct C ClaimItem заменяемыми по типу:
так потеряются независимые context constraints. Нельзя и требовать все старые C
claims безусловно, игнорируя разрешённые same-role overrides. C не содержит outputs
или input-role annotations; его request_payload_sha256 — opaque commitment, не
декодируемая карта ролей. Generic previous обход и timestamps также ответа не дают.

Этот пример не утверждает STALE из-за нового текста/fictional claim, не вводит fact
checker и не обходит qualifications. Вопрос только в required-current membership
exact Qa; integrity обеих версий интерпретации одинакова. INVALID «на всякий случай»
скрыл бы неопределённую семантику; valid SHA сам по себе её не разрешает.

## Минимальное решение владельца

Нужна одна точная policy для прямых C claim roots:

1. Установить, достаточен ли genesis typed hook/chapter membership для назначения
   заменяемой роли C-root; как обрабатываются shared claims нескольких ролей и
   claims, не встретившиеся в genesis output. Иначе определить conservative retained
   constraint policy и явно ограничить допустимые overrides.
2. Зафиксировать expected CURRENT или STALE для приведённого graph/context, затем
   для случая, когда Qa одновременно требуется retained E1/Check/Risk. Во втором
   случае payload override не должен удалять независимую exact constraint.
3. Если выбранному правилу необходимы новые annotations/inputs, оформить отдельное
   утверждение scope/shape; в текущем allowlist их нет. Новый wire field не предлагается
   как обязательное решение, достаточно явно одобренного алгоритма для существующих bytes.

D1–D5 и прежние acceptances остаются действующими. ERef snapshot отсутствие не
используется как дополнительный блокер; пример имеет 0 ERefs. Ни один вариант A/B
не утверждён агентом. До определения mapping — STOP без partial evaluator и тестов,
которые выдали бы выбранную самим агентом семантику за owner-approved oracle.
