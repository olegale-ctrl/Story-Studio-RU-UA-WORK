# SI-E02.2.1-RESUME — Contract audit and blocking evidence

Дата: 2026-11-10. **BLOCKED_CONTRACT / PRE_IMPLEMENTATION.**
Base: `09bdb7c19ede15afb8d9ad57de57b79213b0fb34`.
Branch: `feat/story-intelligence-si-e02-2-1-resume-pure-evaluate`.
Аудит выполнен до production code согласно owner RESUME task §2.

[EVAL-P01–P04 и 42 requirements](STORY_INTELLIGENCE_SI_E02_2_1B_OWNER_APPROVAL_2026_11_10.md)
уже утверждены. Их не переоткрываем. EVAL-P05 OPEN не является причиной блокировки.
BC IDs взяты из [implementation boundary](STORY_INTELLIGENCE_SI_E02_2_1B_IMPLEMENTATION_BOUNDARY.md).
Новый finding **EVAL-RESUME-G01** — локальный ID этого отчёта, не прежний EVAL-G01
confidence/duplicate и не approved currentness G01.

## 1. Mandatory BC01–BC06 audit

Здесь independent expected outcomes — выводы/требования для будущих tests, не новые
выполненные unittest cases. Для каждого item указана и граница установленного predicate.

### BC01 — Essential claims/evidence: partial deterministic coverage

- **Exact fields:** Angle.claim_refs; ClaimItem.claim_kind/materiality;
  ClaimCheck.claim_ref/state/evidence_refs/qualification/reviewer_label/reviewed_at/reason;
  EvidenceItem.claim_ref/source_ref/relation/locator; supplied exact input refs/context.
- **Норма:** [original §3/§5.2](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
  [R1 §3.2 п.1–2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md).
- **Установленный predicate:** dangling/corrupt ref — validation failure; valid
  CENTRAL factual claim без supporting human review либо с unresolved disputed
  evidence — BLOCKED. Nonempty explanation/подсчитанные URL не human verification.
  `unreviewed` с null metadata — valid shape, не reviewed truth.
- **Mapping:** REF_MISSING/REF_HASH_MISMATCH/REF_TYPE_MISMATCH/PROVENANCE_MISMATCH
  для соответствующих exact validation failures; CENTRAL_CLAIM_UNSUPPORTED для
  установленного central unsupported blocker. Malformed ClaimCheck metadata → TYPE.
- **Independent expected oracle:** valid central factual claim, unreviewed check и
  отсутствующее подтверждение → BLOCKED/CENTRAL_CLAIM_UNSUPPORTED даже при score1000;
  отсутствующая сама ClaimItem по заявленному ref → INVALID/REF_MISSING, не BLOCKED.
- **Ambiguity boundary:** full check applicability/coherence/qualifier adequacy для
  произвольного human text не выводятся из local schema; не создавать автоматическое
  scientific judgment. В этом отчёте отдельный competing-outcome defect BC01 не
  доказывается. Известные explicit cases реализуемы; они не закрывают весь classifier.

### BC02 — Explicit risks/rights/capability: established explicit blocker, partial mapping

- **Exact fields:** Risk.category/severity/blocking/resolution/basis_refs/
  resolution_basis_refs/mitigation; VisualRequirement.role/rights_state/licence_basis/
  fallback/acquisition/source_refs; SourceItem.rights_note и applicable exact refs.
- **Норма:** original §5.2 п.2, R1 §3.2 п.2; existing Risk/Visual shapes в
  [records_v1](../../story_intelligence/records_v1.py).
- **Установленный predicate:** explicit applicable `blocking=true`, `resolution=OPEN`
  → BLOCKED. Нельзя вывести новое blocking=true только из scientific/legal description
  или severity threshold, который не утверждён. MITIGATED требует непустые exact
  resolution_basis_refs структурно; это не самостоятельное доказательство реальной
  lawful mitigation. Fallback Text не выдаётся за проверенный материал/права.
- **Mapping:** established essential rights gap → RIGHTS_BLOCKED; established
  capability gap → CAPABILITY_BLOCKED; central unsupported → CENTRAL_CLAIM_UNSUPPORTED.
  Generic scientific/ethical Risk без такого основания не получает выдуманный новый
  code: полный base mapping должен быть задан, findings mapping его не заменяет.
- **Independent expected oracle:** явно essential rights gap/нет usable lawful fallback
  → BLOCKED/RIGHTS_BLOCKED, даже с SUFFICIENT/DISTINCT и aggregate1000. Broken
  resolution_basis_ref → INVALID/REF_MISSING до использования Risk.
- **Ambiguity boundary:** exact role of intended use/fallback adequacy и generic Risk
  reason mapping не закрываются nonempty Text. Это область BC02/BC05 exact coverage;
  новый blocker на основании guessed scientific judgment не вводится.

### BC03 — Framing / required current input: BLOCKING EVAL-RESUME-G01

- **Exact fields:** Intake.raw_input/user_goal; StoryIdea.viewer_question;
  Angle.question/thesis; AudienceHypothesis Known fields/assumptions;
  ChannelContext.purpose/constraints; SourceItem.freshness_requirement/captured_at/
  published_at; frozen vs observed ContextSnapshot.
- **Норма:** original §4 п.2 («если задача требует сегодняшних данных»),
  R1 §3.2 п.3 (required current data → NEEDS_INPUT), п.4 (остальная freshness →
  NEEDS_RESEARCH); BC03 table explicitly запрещает угадывать requiredness по Text/clock.
- **Установленный predicate:** missing exact audience/channel/source ref → INVALID;
  genuine changed expected/observed context → STALE/INPUT_STALE. Эти случаи не
  означают semantically missing framing/current-data в otherwise valid records.
- **Незакрытый predicate:** по каким exact данным определить, что shortage относится
  к **обязательным current data**, а не ordinary freshness research? Source
  `freshness_requirement` — Known<Text>, не closed requiredness/as-of rule.
- **Mapping:** INPUT_STALE и validation codes установлены; research EVIDENCE_NEEDED
  установлен для findings/обычного evidence gap. Для конкретного required-current
  shortage нет утверждённого полного predicate + code/path mapping. Не подставлять
  MISSING_FIELD для присутствующего поля с честным UNKNOWN и не выдумывать code.
- **Independent expected oracle:** поменянный exact active Source dependency → STALE;
  well-shaped UNKNOWN requirement в неизменном graph → развилка §2 ниже. Для неё
  сейчас нельзя независимо зафиксировать один complete NEEDS_INPUT/NEEDS_RESEARCH output.
- **Ambiguity:** material, касается самого eligibility state. T25 не устраняет её.

### BC04 — Other research/freshness: partly closed, same blocking boundary

- **Exact fields:** SourceItem.freshness_requirement/captured_at/published_at;
  EvidenceItem.locator; Rating.value/confidence и approved confidence_findings;
  ChannelContext.portfolio и approved duplicate_findings.
- **Норма:** R1 §3.2 п.4; approved EVAL-P02/P03, frozen findings §§3–5.
- **Установленные predicates:** UNKNOWN rating → aggregate UNKNOWN/research;
  required confidence finding absent/INSUFFICIENT → research; UNKNOWN portfolio →
  research. KNOWN empty portfolio ≠ UNKNOWN; pair coverage known entries exhaustive.
- **Mapping:** EVIDENCE_NEEDED для этих research gaps;
  DUPLICATE_REVIEW_NEEDED для missing/DUPLICATE/UNRESOLVED pair; findings malformed
  → existing TYPE/UNKNOWN_FIELD/MISSING_FIELD/VERSION_UNSUPPORTED; bad binding digest
  → REF_HASH_MISMATCH. Отсутствующий SIRef не research gap.
- **Independent expected oracle:** KNOWN empty portfolio + все KNOWN/HIGH ratings
  не создают confidence/pair gap; UNKNOWN portfolio → NEEDS_RESEARCH/EVIDENCE_NEEDED;
  SUFFICIENT не превращает UNKNOWN rating в KNOWN.
- **Ambiguity:** общая data freshness ещё требует различения required-current и
  ordinary research (тот же EVAL-RESUME-G01), не новой политики confidence/duplicate.
  Captured date/exact hash сами по себе не доказывают фактическую свежесть.

### BC05 — Complete output/diagnostics oracles: findings closed, base oracle incomplete

- **Exact fields:** все вышеперечисленные conditions; generated eligibility.state/
  reason_codes и existing Diagnostic(code,field_path,input_ref,message) plain values.
- **Норма:** R1 §3.2/closed Code; approved findings §5/EVAL-P04; approved T25 limitation.
- **Установленный predicate:** INVALID перед STALE; valid conditions выбирают highest
  R1 precedence; applicable lower-priority reasons сохраняются. Findings reason_codes
  lexical unique union, diagnostics имеют frozen deterministic ordering.
- **Mapping:** approved findings exact mappings не требуют нового решения; у base
  shortage из BC03 остаётся unspecified semantic code/path mapping. Localized wording
  — routine implementation choice, не отдельная архитектурная блокировка.
- **Independent expected oracle:** research + unresolved pair → NEEDS_RESEARCH с
  [DUPLICATE_REVIEW_NEEDED,EVIDENCE_NEEDED]; invalid ERef root вместе со STALE root
  → INVALID/REF_MISSING. Для full T25 нужны установленные exact base premises/codes.
- **Ambiguity:** полный literal T25 нельзя получить из одного precedence assertion;
  часть незакрыта из-за BC03, не из-за отсутствия golden hash generator.

### BC06 — Pure call boundary: implementable routine choices, not blocker

- **Exact inputs:** records, exact domain roots, supplied ordered ratings, frozen
  binding/context, observed input/head refs и approved HumanFindingsInput. Metadata
  Run/previous refs graph-verified, не объявляются current domain inputs автоматически.
- **Норма:** RESUME task §§3–6, EVAL-P01–P04; original/R1/R1a/R1b and G01/G02/F1-D1.
- **Установленный predicate:** stable explicit values → deterministic detached
  in-memory result, без input mutation, records/writes/clock/random/request_id.
  Appropriate module/function signature/result representation — routine design в
  пределах allowlist после прохождения semantic audit.
- **Mapping:** existing SIValidationError codes/paths и approved findings diagnostics;
  no new vocabulary. Никаких Request conflicts/replay для pure call.
- **Independent expected oracle:** identical inputs → equal result; originals exact
  bytes unchanged, output detached; historical-only edit-base не required-current;
  relevant unresolved actual producer/original C ERef → INVALID/REF_MISSING.
- **Ambiguity:** нового material gap BC06 не найдено. EVAL-P05, persistence, Topic
  Intent, science automation, ERef adapter для ERef-free inputs, Windows host и
  production handoff **не** blockers этой pure границы.

## 2. EVAL-RESUME-G01 — required-current vs ordinary freshness shortage

### Exact clauses and competing interpretations

R1 §3.2 п.3: «Недостающая постановка/audience/channel или обязательные current data
→ NEEDS_INPUT». П.4: «Остальная missing evidence/locators/freshness … → NEEDS_RESEARCH».
Original §4 п.2 различает сегодняшние данные и evergreen. Нет закрытого machine-readable
правила определения required-current, as-of/horizon или обработки UNKNOWN requirement.
Approved findings input предназначен для confidence и duplicate pair, не общего
framing/freshness judgment; добавлять туда flags или JSON в reason нельзя.

Для **одного и того же** well-shaped graph из §3:

| Интерпретация ещё не выбранной политики | Возможный primary eligibility | Почему это не разрешено выбрать самостоятельно |
| --- | --- | --- |
| Неизвестно, какие current data обязательны; required-input specification надо получить от человека | NEEDS_INPUT, R1 п.3 | Нужно правило, что UNKNOWN freshness requirement относится к незаданным обязательным input requirements |
| Неизвестна freshness applicability; это обычная исследовательская неопределённость источника | NEEDS_RESEARCH, R1 п.4 | Нужно правило, что такой UNKNOWN относится к «остальной» freshness, без implicit required-current |

Контракт задаёт **что делать после классификации**, но не выбирает одну из этих
классификаций. Это competing contract interpretations, не два результата запущенного
engine. Показанный input не даёт права заявлять ELIGIBLE, scientific sufficiency
или проверенную актуальность. Exact graph CURRENT не равен data freshness.

Разница материальна: меняется state/primary next action и условия достижения T25.
Обе интерпретации fail closed относительно ELIGIBLE, но одна из них всё равно была бы
новой default policy. UNKNOWN requirement не равен KNOWN «не требуется», но также
не является утверждением обязательной current-data роли. Нельзя молча выбрать «все UNKNOWN → research» или «все → input»,
парсить ключевые слова из user_goal/freshness_requirement либо брать системные часы.

## 3. Минимальный воспроизводимый valid input

8 synthetic records, 8-ref canonical Closure, 6 exact domain roots; нет claims,
risks, ERefs, duplicate candidates, Creative/Selection/Brief. Один Source имеет
UNKNOWN freshness_requirement; прочие его Known fields заданы. Все ratings KNOWN5,
HIGH confidence. Поэтому required confidence/pair findings count=0; обе arrays пусты
**по уже утверждённым правилам**, не из-за обхода missing-findings checks.

Этот diagnostic script выполнен на exact base в project `.venv/bin/python`
(Python 3.12.14), exit 0. Existing helpers строят настоящие content-addressed bytes;
нет resolver/hash mocks, production evaluator/нового findings validator или SI output.

```python
from copy import deepcopy
import hashlib
from tests.test_story_intelligence_records_v1 import fixtures, known, unknown, AT
from tests.test_story_intelligence_resolver_v1 import Graph, digest
from tests.test_story_intelligence_provenance_v1 import data_refs
from story_intelligence.resolver_v1 import resolve_si_closure
from story_intelligence.provenance_v1 import verify_si_provenance
from story_intelligence.currentness_v1 import check_si_currentness

T, g = fixtures(), Graph()
def put(kind, **updates):
    value = deepcopy(T[kind]); value['payload'].update(updates)
    return g.add(value, data_refs(value))

i = put('Intake', user_goal=known('Учебная история науки'))
s = put('SourceItem', title=known('Синтетический материал'), author=known('Fixture'),
    publisher=known('Fixture'), published_at=known(AT), captured_at=known(AT),
    material_sha256=known(hashlib.sha256(b'synthetic fixture only').hexdigest()),
    rights_note=known('Искусственные данные; не основание реальных прав'),
    freshness_requirement=unknown())
d = g.run('DISCOVERY', [i, s]); v = deepcopy(T['StoryIdea'])
v['H']['origin']['run_ref'] = d; v['H']['input_refs'] = [i, s]
v['payload'].update(intake_ref=i, source_refs=known([s]))
idea = g.add(v, data_refs(v))
a = put('AudienceHypothesis', region=known('Fixture'), knowledge_level=known('Начальный'),
    motivation=known('Изучение'), interests=known(['История']), age_range=known('Взрослые'),
    assumptions=['Явная учебная гипотеза, не статистика'])
k = put('ChannelContext', audience_ref=a, portfolio=known([]),
    analytics=known('Учебная гипотеза, не статистика'), capability_notes=known('CPU-only'))
an = put('Angle', idea_ref=idea, audience_ref=a, claim_refs=[])
r = put('Rubric'); roots = [idea, an, a, k, r, s]
active = [ref for ref in g.closure(roots) if ref['type'] != 'RunRecord']
ctx = dict(context_version=1, active_input_refs=active, selection_head_refs=[],
           editorial_snapshot_sha256=unknown())
ratings = [dict(criterion_key=x['key'], value=known(5), basis_refs=[a, s],
    explanation='Синтетическая эвристика, не подтверждение свежести',
    confidence=dict(level='HIGH', basis='Учебное суждение, не truth certificate'))
    for x in T['Rubric']['payload']['criteria']]
binding = dict(idea_ref=idea, angle_ref=an, audience_ref=a, channel_ref=k, rubric_ref=r,
    semantic_input_refs=roots, context_snapshot=ctx, ratings_sha256=digest(ratings))
findings = dict(contract_tag='si-evaluate-findings/proposal-1', binding=binding,
                confidence_findings=[], duplicate_findings=[])
before = deepcopy((g.records, ratings, findings, ctx))
assert resolve_si_closure(g.records, roots) == g.closure(roots)
assert verify_si_provenance(g.records, roots) == g.closure(roots)
for root in roots:
    assert check_si_currentness(g.records, root, active, []) == {
        'currentness': 'CURRENT', 'reason_codes': []}
assert binding['ratings_sha256'] == digest(ratings)
assert len(ratings) == 9 and len({x['criterion_key'] for x in ratings}) == 9
assert all(x['value'] == known(5) and x['confidence']['level'] == 'HIGH' for x in ratings)
assert 2 * sum(x['weight_percent'] * 5 for x in T['Rubric']['payload']['criteria']) == 1000
assert before == (g.records, ratings, findings, ctx)
assert digest(g.records) == 'd0629b82eeb589253199ac0dcd9a8ee71bf76a942780dde5fd45bd41c46a8b61'
assert digest(ratings) == '3a3e6fe51ce5715364ba7d7fe83c612749a2528ce44f472c8802e796cec987fd'
assert digest(findings) == 'cff2c041ed8a348e52727ea47a26c088aa8aae1b56184fed06ddbe6b304d7eeb'
assert digest(ctx) == '89c43e0d9c54cb16d749c5acc19f133549c1512fe4effa5de65a335da8a67e5b'
```

Source exact ref: type=SourceItem, id=`00000002-2222-4222-8222-222222222222`,
revision=1, sha256=`977e459bdf72343c4d2adb8e1d434ee8d6b9ef5b422eee83fe91552b265f7b63`.
Frozen expected context равен observed context; нет STALE или broken refs.
Перечисленные hashes — diagnostic input identities, не новые approved engine golden
vectors и не подтверждение фактических прав/свежести синтетического источника.

**Eligibility не вычислялся.** Исходный graph/refs/ratings/findings/context не менялись.
Production evaluator и новые unit tests не создавались.

## 4. Smallest required owner decision

Определить узкий deterministic predicate, отделяющий required-current/input shortage
от ordinary freshness research для explicitly supplied valid SI inputs:

1. Какие exact fields/values/roles либо separately approved non-persisted human
   premise устанавливают required-current для этой оценки; как трактовать UNKNOWN
   freshness_requirement без keyword inference, clock/network и fabricated recency.
2. Для описанного exact input выбрать правило и primary state: NEEDS_INPUT либо
   NEEDS_RESEARCH; задать existing reason code/path mapping и independent expected
   outcome. Это требует только bounded base-classifier clarification, не нового code.
3. Тот же explicit predicate должен позволять составить полные premises/outcomes T25;
   не исчезать NEEDS_INPUT branch из scope молча ради реализации.

Возможны rule-only clarification на existing fields или узкий explicit human premise,
но ни один вариант здесь не утверждается. Approved closed HumanFindingsInput не
расширять самостоятельно. Новый SI record/wire/operation, EVAL-P05, persistence,
Topic Intent/science automation/Windows или ERef adapter для ERef-free inputs не нужны.

**STOP — BLOCKED_CONTRACT.** Следовать blocked allowlist: только этот документ и
[RESUME_RESULT](STORY_INTELLIGENCE_SI_E02_2_1_RESUME_RESULT.md).
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes/SI-E02.2.2.
