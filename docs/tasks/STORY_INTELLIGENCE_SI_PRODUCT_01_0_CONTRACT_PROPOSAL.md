# SI-PRODUCT-01.0 — Editorial Decision Projection V1

Дата: 2026-11-13 (Europe/Kyiv). **CONTRACT PROPOSAL / NOT APPROVED / DOCS ONLY.**
Каждое новое правило ниже — предложение для owner review, не изменение evaluator.
Exact runtime base: `35451f6441bd5428e132ae65f2080209b51fe009`.

## 1. Authority, sources and scope

Нормативные границы: [SI-E02.1 P01–P05](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md),
[TI/SR principles](STORY_INTELLIGENCE_SI_E02_1A_OWNER_APPROVAL_2026_11_10.md),
[EVAL-P01–P04 approval](STORY_INTELLIGENCE_SI_E02_2_1B_OWNER_APPROVAL_2026_11_10.md),
[frozen findings](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md),
[RC approval](STORY_INTELLIGENCE_SI_E02_2_1E_RC_OWNER_APPROVAL_2026_11_12.md),
[frozen RC-P01–P06](STORY_INTELLIGENCE_SI_E02_2_1D_REQUIRED_CURRENT_FINAL_PROPOSAL.md),
[Q approval](STORY_INTELLIGENCE_SI_E02_2_1F_OWNER_APPROVAL_2026_11_12.md),
[Q1–Q3 mappings](STORY_INTELLIGENCE_SI_E02_2_1E_BASE_CLASSIFIER_DECISION_PROPOSAL.md),
[readiness](STORY_INTELLIGENCE_SI_E02_2_1F_READINESS_RESULT.md),
[final T25](STORY_INTELLIGENCE_SI_E02_2_1F_T25_FINAL_ORACLE.md).
Historical PROPOSAL wording этих источников superseded только соответствующими approvals.
Original SI/1, R1/R1a/R1b, G01/G02/F1-D1 и editorial/storage contracts сохраняются.

Предмет — private human-reviewable explanation существующего bounded EVALUATE.
Это не consumer ProductionBrief, не Topic Intent operation, не scientific approval,
не UI и не новый SI record/Request/RunRecord/EvaluationReport. P03 reuse существующего
ProductionBrief не означает, что EVALUATE output уже содержит Brief. Его здесь нет.
Рекомендации не выполняют операции, не создают approvals/Selection и не меняют priority.
Тестовые требования: [TEST_ORACLES](STORY_INTELLIGENCE_SI_PRODUCT_01_0_TEST_ORACLES.md).
Все новые choices: [OWNER_DECISIONS](STORY_INTELLIGENCE_SI_PRODUCT_01_0_OWNER_DECISIONS.md).

## 2. Observed runtime, not a historical response schema

Actual API в [evaluate_v1.py](../../story_intelligence/evaluate_v1.py):

```text
evaluate_si(records, semantic_input_refs, observed_context, ratings,
            expected_context, human_findings,
            required_current_premise=None, *, ui_locale=None)
```

| Explicit input | Actual role; projection boundary |
| --- | --- |
| records | Plain list полных existing SI/1 records; source of exact internal diagnostic bindings, never automatic display content |
| semantic_input_refs | Ordered exact domain roots; unambiguous Idea/Angle/Audience/Channel/Rubric plus explicit applicable roots |
| observed_context / expected_context | Existing ContextSnapshot: context_version=1, active_input_refs, selection_head_refs, editorial_snapshot_sha256 Known/Unknown |
| ratings | Nine ordered Rating values: key, Known int0..5/Unknown, exact basis_refs, explanation, confidence level/basis |
| human_findings | Approved non-persisted closed tag `si-evaluate-findings/proposal-1`, binding, confidence_findings, duplicate_findings |
| required_current_premise | None or approved non-persisted closed tag `si-required-current/proposal-1`, exact binding/determination/requirements/source assessments |
| ui_locale | Optional evaluator locale assertion; not projection-language selection |

Exactly two result shapes at this base; no condition-class or positive-evidence field:

```text
OK = {status:"OK", currentness:"CURRENT", locale:"ru"|"uk",
      eligibility:{state:Eligibility, reason_codes:List<Code>},
      aggregate_tenths:Known<Int0..1000>, ratings:List<Rating>,
      diagnostics:List<Diagnostic>}
Rejected = {status:"STALE"|"INVALID", currentness:same_as_status,
      locale:null, eligibility:null, aggregate_tenths:null, ratings:[],
      reason_codes:List<Code>, diagnostics:List<Diagnostic>}
Diagnostic = {code, field_path, input_ref:SIRef|null, message:Text}
```

`Known<T>` включает UNKNOWN с reason, не только KNOWN(value). Actual statuses:
**OK, STALE, INVALID**. Eligibility только внутри OK: **BLOCKED, NEEDS_INPUT,
NEEDS_RESEARCH, REVIEW_DUPLICATE, ELIGIBLE_FOR_CREATIVE**. Это не пять дополнительных
status values. CURRENT не scientific/rights/production clearance. No top-level
reason_codes в OK; нет score/eligibility при STALE/INVALID. Null не UNKNOWN score.

OK codes (closed observed emitter set): CENTRAL_CLAIM_UNSUPPORTED, EVIDENCE_NEEDED,
RIGHTS_BLOCKED, DUPLICATE_REVIEW_NEEDED. STALE: INPUT_STALE. INVALID допускает inherited
validation codes: TYPE, LIMIT, UNKNOWN_FIELD, MISSING_FIELD, VERSION_UNSUPPORTED,
REF_MISSING, REF_TYPE_MISMATCH, REF_HASH_MISMATCH, DEPENDENCY_CYCLE,
PROVENANCE_MISMATCH, LOCALE_MISMATCH, SELECTION_CONFLICT, EVIDENCE_NEEDED,
RIGHTS_BLOCKED, PRIVACY_REVIEW_REQUIRED, PRIVACY_BLOCKED. Последние privacy codes
могут прийти из shape validation supplied ReviewPacket даже без его domain применения.
Code EVIDENCE_NEEDED либо RIGHTS_BLOCKED при INVALID не является accepted eligibility gap.

Existing broader SI code enum не делает HOOK_FACT_CONFLICT, CAPABILITY_BLOCKED,
UNAVAILABLE_OFFLINE, HANDOFF_ADAPTER_UNAVAILABLE, REQUEST_CONFLICT,
REDACTED_CONTEXT_INCOMPLETE или RECORD_UNAVAILABLE поддержанными OK conditions
этого evaluator. Они не получают guessed product mappings.

## 3. Proposed admission and result association — PD-01

Локальный conceptual interface: exact `evaluation_inputs`, exact `evaluation_result`,
explicit `display_locale` (ru/uk). Это описание private function boundary, не новый
transport/schema, persistent envelope, credential или binding field внутри SI/1.
Всё caller-supplied; result сам по себе не имеет signature/input digest/trusted provenance.
Invocation frame содержит шесть mandatory arguments API; два optional arguments
`required_current_premise` и `ui_locale` могут быть опущены, что означает ровно
existing API default None. Другие пропуски/extra arguments не принимаются. Это
применение существующих defaults, не coercion/исправление данных. None premise
остаётся valid evaluator input с возможным NEEDS_INPUT, не missing projection result.

Рекомендуется проверять связь повторным вызовом **того же pinned pure evaluate_si**
с точно теми же inputs и byte-for-byte по existing canonical JSON сравнивать output
с supplied result. Это только admission verification: не новая оценочная политика,
не alternative scoring, не исправление inputs и не принятие другого результата.
Mismatch, исключение, недостающий input, unsupported shape/extra field/version →
UNAVAILABLE; не подменять результат на recomputed value. Допустимая будущая оптимизация
trusted same-invocation handoff требует отдельного owner choice; не считать произвольный
dict «принятым» по его status. Ни hash, ни повтор вычисления не доказывает real authority.
Cost такого bounded read-only verification пока не performance-qualified.

На OK проверить exact result shape, locale/currentness, nine detached ratings,
Known aggregate, valid enum, code union, unique ordered diagnostics и полное покрытие
каталогом §6. Decision остаётся исходной, не определяется заново по translated text.
На Rejected проверить exact null/[] fields и статусную форму codes. Не разыменовывать
непроверенные refs для labels в INVALID/STALE. No latest lookup/automatic rebase.

Нет новой проекции для EvaluationReport record: он отличается от этого runtime dict.
Отсутствующий result не превращать в evaluator INVALID; это UNAVAILABLE presentation.
Исключение evaluator не переводить в придуманный reason code/достоверное решение.

## 4. Proposed private card shape and language — PD-02/03

```text
Card = {projection_version:"editorial-decision-projection/1",
        display_locale:"ru"|"uk", availability:"DISPLAYABLE"|"UNAVAILABLE",
        sections:{decision_summary:Text, reasons:List<Text>,
                  blocking_risks_and_gaps:List<Text>, next_actions:List<Text>,
                  limitations:List<Text>}}
```

Эти local presentation labels/version — **PROPOSAL**, не SI/1 enums/error codes.
Редактору показываются пять sections; технические keys/version/availability не текст UI.
Поле topic/title отсутствует: title/raw_input не экспортируется автоматически.
DISPLAYABLE означает только возможность показать объяснение, включая INVALID/STALE.
Нельзя превращать его в флаг permission. UNAVAILABLE: summary U0, reasons=[], gaps=[],
next_actions=[A0], limitations=[L1..L6]. Нет fabricated evaluator status/score/approval.

| Item | RU literal | UK literal |
| --- | --- | --- |
| U0 | Пояснение оценки недоступно. Не используйте эту карточку для решения о продолжении работы. | Пояснення оцінки недоступне. Не використовуйте цю картку для рішення про продовження роботи. |
| A0 | Проверьте полноту и совместимость данных для пояснения. | Перевірте повноту й сумісність даних для пояснення. |
| Section 1 | Редакционное решение | Редакційне рішення |
| Section 2 | Основания решения | Підстави рішення |
| Section 3 | Блокирующие риски и пробелы | Блокувальні ризики та прогалини |
| Section 4 | Следующие действия редактора | Наступні дії редактора |
| Section 5 | Ограничения и решения человека | Обмеження та рішення людини |

Explicit display_locale обязателен, без platform/default/language detection; `ua`,
пустой или неизвестный locale → UNAVAILABLE. Для отсутствующего/неподдерживаемого
locale human-readable RU/UK card не создаётся вообще: закрытый
AdmissionFailure={availability:"UNAVAILABLE"}, без sections/locale. Это admission failure до Card, не второй язык по умолчанию.
При известном locale остальные admission failures дают полный UNAVAILABLE Card выше.
Допускается UK explanation при evaluator.locale=ru и наоборот: переводятся только
фиксированные presentation templates, не содержание records; evaluator ui_locale и
исходные inputs не изменяются. Нет LLM/внешнего переводчика/Unicode normalization.
Output values — fixed Unicode strings плюс decimal ordinals/известные numeric values;
для текстового представления LF, UTF-8 без BOM, без locale-dependent number grouping.
Это не новый canonical hash/storage format. Все strings ниже буквальные proposed oracles.

## 5. Decision summaries and score — PD-04

| Evaluator condition | RU summary | UK summary |
| --- | --- | --- |
| OK / ELIGIBLE_FOR_CREATIVE | Можно продолжить творческую разработку в пределах этой оценки. Эта оценка не предоставляет допуска к производству. | Можна продовжити творчу розробку в межах цієї оцінки. Ця оцінка не надає допуску до виробництва. |
| OK / NEEDS_INPUT | Сначала уточните необходимые исходные данные. | Спочатку уточніть необхідні вихідні дані. |
| OK / NEEDS_RESEARCH | Сначала закройте отмеченные исследовательские пробелы. | Спочатку усуньте зазначені дослідницькі прогалини. |
| OK / REVIEW_DUPLICATE | Нужна редакционная проверка пересечения с портфелем. | Потрібна редакційна перевірка перетину з портфелем. |
| OK / BLOCKED | Продолжение творческой разработки заблокировано отмеченными условиями. | Продовження творчої розробки заблоковане зазначеними умовами. |
| STALE | Оценка устарела относительно переданного контекста. Использовать прежнее решение нельзя. | Оцінка застаріла щодо переданого контексту. Використовувати попереднє рішення не можна. |
| INVALID | На основании переданных данных нельзя принять результат оценки. | На підставі переданих даних не можна прийняти результат оцінки. |

При OK reasons начинается только scoped statement:
RU «Основание — условия, зафиксированные оценкой переданных данных.»;
UK «Підстава — умови, зафіксовані оцінкою переданих даних.» Затем score line и все
mapped explanations в исходном diagnostic order. При eligible/no diagnostics добавить
RU «В этой оценке не осталось отмеченных условий, препятствующих творческой разработке.» /
UK «У цій оцінці не залишилося зазначених умов, що перешкоджають творчій розробці.»
Это отсутствие local gaps, не positive proof of historical truth/novelty/audience demand.

KNOWN n: «Баллы по заданной рубрике: n из 1000.» / «Бали за заданою рубрикою: n із 1000.»
UNKNOWN: «Итоговый балл не определён.» / «Підсумковий бал не визначений.»
Не показывать UNKNOWN.reason. Нет percent, grades, traffic-light thresholds, ranking,
rounding/renormalization либо перевода score/confidence в probability. При Rejected
score/ratings вообще не показываются. Missing score в supposed OK → UNAVAILABLE.

Если в будущем нужны criterion rows, это отдельный presentation extension; V1 не
рендерит ratings.explanation/confidence.basis/basis_refs и не делает новые похвальные
утверждения из высоких девяти чисел. Исходные ratings и weights не изменяются.

## 6. Closed OK condition catalog — PD-05

Только private matching использует code/path/ref/fixed producer message. Не копировать
message пользователю и не переводить arbitrary Text. Каждый row ниже должен совпасть
ровно с соответствующим emitter в pinned evaluate_v1.py и проверенным typed subject.
Проверяются all selectors совместно: code, canonical path family, exact typed input_ref
или null, ожидаемая fixed message и связь с exact invocation context. Path indices —
неотрицательные canonical decimal без ведущих нулей; они должны адресовать именно тот
элемент inputs, который использовал evaluator. Подстановка regex в произвольный
private message запрещена. Ноль или несколько matches → UNAVAILABLE, не generic success.

Shorthand: P=`$.required_current_premise`, F=`$.human_findings`, R[i]=`$.records[i].payload`.
S=SourceItem, I=StoryIdea, G=Rubric, H=ChannelContext, AU=AudienceHypothesis, Q=ClaimItem,
C=ClaimCheck, E=EvidenceItem, V=VisualRequirement, K=Risk. These are typed roles, not labels.
Code E=EVIDENCE_NEEDED в таблице; CC=CENTRAL_CLAIM_UNSUPPORTED; DR=DUPLICATE_REVIEW_NEEDED;
RB=RIGHTS_BLOCKED. B/I/R/D — existing condition classes BLOCKED/NEEDS_INPUT/
NEEDS_RESEARCH/REVIEW_DUPLICATE, не новые output enums. Fixed message authority —
RC D01–D09, Q tables, runtime `_scoring_findings`; новые локализованные тексты ниже — proposal.

| ID; selector (code/path/subject); class | RU explanation | UK explanation | Action |
| --- | --- | --- | --- |
| RC01 E / P / null; I | Не определено, нужны ли данные за конкретный период. | Не визначено, чи потрібні дані за конкретний період. | A1 |
| RC02 E / P.determination / I; I | Не решено, нужны ли данные за конкретный период. | Не вирішено, чи потрібні дані за конкретний період. | A1 |
| RC03 E / P.required_data / I; I | Не задан состав необходимых данных. | Не задано склад необхідних даних. | A2 |
| RC04 E / P.required_data.value[k].specification / S; I | Не уточнено, какие данные нужны от источника. | Не уточнено, які дані потрібні від джерела. | A2 |
| RC05 E / P.required_data.value[k].period / S; I | Не задан необходимый период данных. | Не задано необхідний період даних. | A3 |
| RC06 E / P.source_freshness / S; R | Не представлено рассмотрение свежести источника. | Не надано розгляд свіжості джерела. | A4 |
| RC07 E / P.source_freshness[i].applicability / S; R | Не решено, нужна ли проверка свежести источника. | Не вирішено, чи потрібна перевірка свіжості джерела. | A4 |
| RC08 E / P.source_freshness[i].outcome / S; R | Достаточность подтверждения свежести источника не установлена. | Достатність підтвердження свіжості джерела не встановлено. | A4 |
| RC09 E / P.source_freshness[i].review_period / S; R | Не задан рассмотренный период для источника. | Не задано розглянутий період для джерела. | A4 |
| C01 CC / R[i].materiality / Q; B | Для центрального фактического утверждения не представлена применимая проверка. | Для центрального фактичного твердження не надано застосовної перевірки. | A5 |
| C02 CC / R[i].state / C; B | Проверка центрального фактического утверждения остаётся нерешённой или недостаточной. | Перевірка центрального фактичного твердження залишається невирішеною або недостатньою. | A5 |
| C03 E / R[i].state / C; R | Проверка утверждения требует дополнительного исследования. | Перевірка твердження потребує додаткового дослідження. | A5 |
| C04 E / R[i].evidence_expectation / Q; R | Не представлена применимая проверка утверждения. | Не надано застосовної перевірки твердження. | A5 |
| C05 CC либо E / R[i].relation / E; B для factual CENTRAL, иначе R | В зафиксированных данных остаётся противоречие. | У зафіксованих даних залишається суперечність. | A5 |
| K01 E / R[i].blocking либо .resolution_basis_refs / K category SCIENTIFIC; B | В данных зафиксирован блокирующий научный риск. | У даних зафіксовано блокувальний науковий ризик. | A6 |
| K02 E / те же paths / K category LEGAL; B | В данных зафиксирован блокирующий правовой риск. | У даних зафіксовано блокувальний правовий ризик. | A6 |
| K03 E / те же paths / K category ETHICAL; B | В данных зафиксирован блокирующий этический риск. | У даних зафіксовано блокувальний етичний ризик. | A6 |
| K04 E / те же paths / K category REPUTATIONAL; B | В данных зафиксирован блокирующий репутационный риск. | У даних зафіксовано блокувальний репутаційний ризик. | A6 |
| K05 E / те же paths / K category PRODUCTION; B | В данных зафиксирован блокирующий производственный риск. | У даних зафіксовано блокувальний виробничий ризик. | A6 |
| K06 E / те же paths / K category MARKET; B | В данных зафиксирован блокирующий рыночный риск. | У даних зафіксовано блокувальний ринковий ризик. | A6 |
| V01 RB / R[i].rights_state / V; B | Для необходимого материала не установлена достаточная основа использования. | Для необхідного матеріалу не встановлено достатньої підстави використання. | A7 |
| Q01 E / R[i].knowledge_level / AU; I | Не задан уровень подготовки аудитории. | Не задано рівень підготовки аудиторії. | A8 |
| Q02 E / R[i].motivation / AU; I | Не задана мотивация аудитории. | Не задано мотивацію аудиторії. | A8 |
| Q03 E / R[i].capability_notes / H; I | Не заданы исходные производственные ограничения. | Не задано вихідні виробничі обмеження. | A9 |
| Q04 E / R[i].source_refs / I; R | Исследование источников не завершено для заявленных утверждений. | Дослідження джерел не завершено для заявлених тверджень. | A5 |
| F01 E / $.ratings[k].value / G; R | Не задана одна из обязательных оценок по рубрике. | Не задано одну з обов'язкових оцінок за рубрикою. | A10 |
| F02 E / F.confidence_findings / G; R | Рассмотрение неопределённости одной из оценок отсутствует или недостаточно. | Розгляд невизначеності однієї з оцінок відсутній або недостатній. | A10 |
| F03 E / R[i].portfolio / H; R | Исследование локального портфеля не завершено. | Дослідження локального портфеля не завершено. | A11 |
| F04 DR / F.duplicate_findings / H; D | Не представлено обязательное сравнение с записью локального портфеля. | Не надано обов'язкового порівняння із записом локального портфеля. | A11 |
| F05 DR / F.duplicate_findings[k].outcome / H; D | Редакционное решение о пересечении с локальным портфелем остаётся открытым. | Редакційне рішення про перетин із локальним портфелем залишається відкритим. | A11 |

F01/F02 slot различается индексом criterion из exact nine-key order; F02 допустимая
producer message строится только из одного из девяти approved keys. F04 slot — exact
portfolio entry index, message только fixed literal с этим проверенным int. F05
DUPLICATE и UNRESOLVED остаются различными private inputs; общая формулировка не
объявляет каждую пару установленным дубликатом и не отменяет human DUPLICATE finding.
Одинаковый видимый текст для разных slots не даёт права их схлопнуть.
C05 class берётся из exact supplied claim kind/materiality, не Text inference.
K paths: `.blocking` при OPEN/UNRESOLVED, `.resolution_basis_refs` при недостаточно
подтверждённом MITIGATED. Категория Risk — не вывод о реальном состоянии мира.

| Action | RU literal | UK literal |
| --- | --- | --- |
| A1 | Решите, нужны ли данные за конкретный период, и явно задайте это условие. | Вирішіть, чи потрібні дані за конкретний період, і явно задайте цю умову. |
| A2 | Уточните состав и содержание необходимых данных. | Уточніть склад і зміст необхідних даних. |
| A3 | Задайте необходимый период данных. | Задайте необхідний період даних. |
| A4 | Рассмотрите свежесть источника за нужный период и достаточность зафиксированных подтверждений. | Розгляньте свіжість джерела за потрібний період і достатність зафіксованих підтверджень. |
| A5 | Исследуйте утверждение и противоречащие данные; передайте существенные разногласия на рассмотрение человеку. | Дослідіть твердження й суперечливі дані; передайте суттєві розбіжності на розгляд людині. |
| A6 | Передайте отмеченный риск на рассмотрение ответственному человеку; текст плана сам по себе риск не снимает. | Передайте зазначений ризик на розгляд відповідальній людині; текст плану сам собою ризик не усуває. |
| A7 | Рассмотрите точный материал, предполагаемое использование и права; описание замены не подтверждает её допустимость. | Розгляньте точний матеріал, передбачене використання й права; опис заміни не підтверджує її допустимості. |
| A8 | Уточните редакционную гипотезу об аудитории, не выдавая её за измеренный спрос. | Уточніть редакційну гіпотезу про аудиторію, не видаючи її за виміряний попит. |
| A9 | Уточните ограничения производства; фактическую выполнимость проверьте отдельно. | Уточніть обмеження виробництва; фактичну здійсненність перевірте окремо. |
| A10 | Представьте недостающую оценку или рассмотрите её неопределённость, сохраняя неизвестные значения явно. | Надайте відсутню оцінку або розгляньте її невизначеність, зберігаючи невідомі значення явно. |
| A11 | Сравните тему с указанными записями локального портфеля и примите редакционное решение. | Порівняйте тему із зазначеними записами локального портфеля й ухваліть редакційне рішення. |

## 7. STALE/INVALID explanation catalog

STALE: одна fixed explanation на каждый исходный diagnostic slot, сохраняя порядок:
RU «Версии или контекст оценки изменились.» / UK «Версії або контекст оцінки змінилися.»
Action: RU «После проверки точных версий и контекста заново выполните оценку.» /
UK «Після перевірки точних версій і контексту виконайте оцінку заново.»
Не называть конкретный документ устаревшим по code-only API; no auto rebase.

INVALID catalog — safe validation explanations, не новые blockers и не research verdicts:

| Existing code family | RU literal | UK literal |
| --- | --- | --- |
| TYPE, UNKNOWN_FIELD, MISSING_FIELD | Структура переданных данных не позволяет принять результат оценки. | Структура переданих даних не дає змоги прийняти результат оцінки. |
| LIMIT | Переданные данные выходят за поддерживаемые ограничения. | Передані дані виходять за підтримувані обмеження. |
| VERSION_UNSUPPORTED | Версия переданных данных не поддерживается. | Версія переданих даних не підтримується. |
| REF_MISSING | Не удалось проверить необходимые точные связи данных. | Не вдалося перевірити необхідні точні зв'язки даних. |
| REF_TYPE_MISMATCH, REF_HASH_MISMATCH | Точные связи или содержимое данных не согласованы. | Точні зв'язки або вміст даних не узгоджені. |
| DEPENDENCY_CYCLE | В зависимостях переданных данных обнаружен недопустимый цикл. | У залежностях переданих даних виявлено неприпустимий цикл. |
| PROVENANCE_MISMATCH | Заявленное происхождение данных не согласовано. | Заявлене походження даних не узгоджене. |
| LOCALE_MISMATCH | Языковые параметры оценки не согласованы. | Мовні параметри оцінки не узгоджені. |
| SELECTION_CONFLICT | Переданные сведения о выборе не согласованы. | Передані відомості про вибір не узгоджені. |
| EVIDENCE_NEEDED | Данные проверки утверждения некорректны для принятия результата. | Дані перевірки твердження некоректні для прийняття результату. |
| RIGHTS_BLOCKED | Данные об использовании материала некорректны для принятия результата. | Дані про використання матеріалу некоректні для прийняття результату. |
| PRIVACY_REVIEW_REQUIRED, PRIVACY_BLOCKED | Переданные данные не прошли проверку ограничений приватности. | Передані дані не пройшли перевірку обмежень приватності. |

Общий action INVALID: «Проверьте состав данных и точность их связей; затем повторите оценку.» /
«Перевірте склад даних і точність їхніх зв'язків; потім повторіть оцінку.»
Нельзя обещать доступность missing source, определять culprit ERef, показывать path
или исправлять provenance из raw diagnostic. Reasons/gaps содержат safe строки выше,
без score/ratings и без ранее cached eligibility. Сам факт validation failure не
доказывает ни научную ложность темы, ни злонамеренность автора.

## 8. Deterministic composition, materiality and labels — PD-06/07

После complete admission и single-match для каждого diagnostic:

1. Сохранить original evaluator result вне Card без изменений; private context только
   на время вызова, без implicit audit log/export/persistence.
2. Reasons: base line, score (OK only), затем по одной localized строке на каждый
   original diagnostic slot. В STALE/INVALID только их explanation строки. No LLM.
3. Каждый OK reason имеет controlled prefix subject alias: `alias + ": " + explanation`;
   если input_ref=null, prefix не добавлять. Не вставлять record text. Slot F01/F02
   дополнительно имеет «Оценка «label»» / «Оцінка «label»» (label из закрытой таблицы ниже); F04/F05 «Сравнение n» /
   «Порівняння n» (index+1) после subject alias через ` / `. Не показывать criterion key.
4. Gaps: те же строки в том же относительном порядке. Все B условия присутствуют;
   все I/R/D gaps тоже остаются, включая ниже winning BLOCKED. Нельзя сортировать
   по переведённому тексту, code alone, importance score или обрезать «top N».
5. Actions: одна строка на diagnostic, тот же порядок/alias/slot, без dedup одинаковых
   текстов. Eligible/no diagnostics: единственное действие «Редактору следует решить,
   продолжать ли творческую разработку.» / «Редактору слід вирішити, чи продовжувати
   творчу розробку.» Это не Topic Intent command/permission. Rejected actions также
   по одному slot, но без subject labels. Никаких auto research/production jobs.
6. Limitations: L1..L6 всегда и точно в этом порядке. Если output должен быть сокращён,
   V1 отказывает в Card, а не скрывает blocker или limitation. Pagination/UI вне scope.

Subject aliases назначаются по первому появлению exact input_ref среди diagnostics,
отдельный counter для каждого type, начиная с 1. Повтор ref сохраняет alias; две
разные exact revisions не объединяются по id. Counters private local, не persisted
identifiers, не hashes и не результат ранжирования. Смена контекста может сменить
номера; это не continuity/identity guarantee. Same input → те же aliases.

| Type | RU alias (n decimal) | UK alias |
| --- | --- | --- |
| SourceItem | Источник n | Джерело n |
| StoryIdea | Тема n | Тема n |
| Rubric | Рубрика n | Рубрика n |
| ChannelContext | Контекст канала n | Контекст каналу n |
| AudienceHypothesis | Гипотеза об аудитории n | Гіпотеза про аудиторію n |
| ClaimItem | Утверждение n | Твердження n |
| ClaimCheck | Проверка утверждения n | Перевірка твердження n |
| EvidenceItem | Свидетельство n | Свідчення n |
| Risk | Риск n | Ризик n |
| VisualRequirement | Материал n | Матеріал n |

F01/F02 criterion labels в exact approved order; это названия критериев, не
утверждения о реальном спросе/качестве/ресурсах и не новый набор весов:

| Existing key (private match only) | RU label | UK label |
| --- | --- | --- |
| audience_interest | Интерес аудитории | Інтерес аудиторії |
| channel_fit | Соответствие каналу | Відповідність каналу |
| angle_novelty | Новизна ракурса | Новизна ракурсу |
| evidence_quality | Качество подтверждений | Якість підтверджень |
| narrative_potential | Потенциал повествования | Потенціал оповіді |
| visual_feasibility | Возможность визуального воплощения | Можливість візуального втілення |
| resource_fit | Соответствие ресурсам | Відповідність ресурсам |
| risk_manageability | Управляемость рисков | Керованість ризиків |
| portfolio_distinctness | Отличие от локального портфеля | Відмінність від локального портфеля |

Другие types для OK catalog не поддержаны. STALE/INVALID не получают record aliases.
Private exact refs нужны matching, но никогда не выводятся: никаких UUID/SIRef/hash,
internal path/code, file/URL locator, timestamp, username, reviewer label, title,
source specification/reason, rating explanation/confidence basis, credential-like
unknown key, raw diagnostic.message или exception text. Никакого кликабельного
source locator. Санитизация regex не заменяет запрет копирования free text.
Alias не удостоверяет достоверность источника. Количество строк/типов раскрывает
ограниченную структуру private оценки: V1 не обещает anonymity/public-safe export.
Human-friendly source titles, grants, public sharing и secure persistence — отдельные
контракты, не автоматически разрешены этим proposal или наличием Card.

## 9. Fixed limitations and outstanding human decisions — PD-08

| ID | RU literal | UK literal |
| --- | --- | --- |
| L1 | Карточка поясняет только оценку переданного контекста; полнота внешних данных не установлена. | Картка пояснює лише оцінку переданого контексту; повноту зовнішніх даних не встановлено. |
| L2 | Баллы и уверенность не доказывают научную истинность, достоверность источников или спрос аудитории. | Бали й упевненість не доводять наукової істинності, достовірності джерел або попиту аудиторії. |
| L3 | Рассмотрение научных выводов человеком и всех семи областей научной проверки этой карточкой не удостоверяется. | Розгляд наукових висновків людиною й усіх семи сфер наукової перевірки цією карткою не засвідчується. |
| L4 | Права на материалы, фактическая доступность и выполнимость производства требуют отдельной проверки. | Права на матеріали, фактична доступність і здійсненність виробництва потребують окремої перевірки. |
| L5 | Карточка не удостоверяет личность, компетентность или полномочия проверяющего и не предоставляет редакционного утверждения. | Картка не засвідчує особу, компетентність або повноваження перевіряльника й не надає редакційного затвердження. |
| L6 | Допуск к творческой разработке не является разрешением на производство или публикацию. | Допуск до творчої розробки не є дозволом на виробництво або публікацію. |

SR-C01..07 сохраняются: terminology/definitions, chronology/dating, competing
explanations, counter-evidence, qualifications/uncertainty, source traceability,
intended-use rights. Их approved требование consideration не означает executable
completion/approval profile. Наличие или отсутствие настоящих approvals из evaluator
не выводится; Card не объявляет все approvals отсутствующими, она их не проверяет.
Не генерируются hooks, причины исторических событий, findings, visual assets,
audience demand или Production Brief contents. Не исполняется discovery/research.

## 10. Compatibility finding and STOP

Actual implementation есть; 78 existing evaluator tests реально прошли при preflight.
Наблюдаемые отличия от conceptual docs — pure dict вместо persisted EvaluationReport,
разные code locations для OK/Rejected, отсутствие explicit condition class/positive
justifications/authority fields. Это поддерживаемые representation boundaries,
не основание дописывать SI fields. Closed catalog плюс exact invocation context
позволяют локализовать существующие условия, не выводя class из code alone.
Результат этого этапа не утверждает универсальную корректность evaluator и не является
его independent acceptance. Material projection-blocking inconsistency не обнаружена
в выполненной source/runtime проверке. Все новые presentation decisions ещё NOT APPROVED.

EVAL-P05 OPEN; PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Никаких code/schema/test/contract changes,
external publication, implementation, UI, persistence, service, provider или network
integration. **STOP FOR INDEPENDENT REVIEW; требуется явное owner approval.**
