# SI-PRODUCT-01.0 — Independent projection test oracles

Дата: 2026-11-13. **PROPOSAL / NOT APPROVED / DOCS ONLY.**
Projection implementation и executable projection tests отсутствуют. Таблицы ниже —
requirements/ожидаемые результаты, не PASS. Existing evaluator preflight запускался
отдельно; его фактический результат указан в [RESULT](STORY_INTELLIGENCE_SI_PRODUCT_01_0_RESULT.md).
Authority proposed strings/shape: [CONTRACT](STORY_INTELLIGENCE_SI_PRODUCT_01_0_CONTRACT_PROPOSAL.md).

## 1. Independent witness construction

Pinned source: `35451f6441bd5428e132ae65f2080209b51fe009`.
Использовать existing `tests/story_intelligence_evaluate_fixture_support.py` Fixture,
его independent stdlib JSON/SHA-256 Graph и existing evaluator tests. Fixture helper
не импортирует evaluator. Не mock accepted validator/resolver/provenance/currentness,
не объявлять fake all-zero hash валидным. Inputs для success — genuine canonical
records/refs и exact accepted evaluator output. Expected card strings/ordering
автор теста берёт из этого документа/Contract, не из future renderer output.

B: `Fixture().arguments()` с nine KNOWN5/HIGH, known empty portfolio, valid NOT_REQUIRED
premise/NA source. T25: existing `Fixture(t25=True).arguments()` — 11-record approved
four-condition graph. K: B с `require(); establish()` до `arguments()`, genuine proof.
Любое изменение record/payload/revision требует пересборки exact descendants,
manifests, ratings/bindings; helper `revise`/`arguments` делает это на искусственных
данных. Currentness не freshness/truth. Не перетаскивать старый положительный finding.

Сравнивать целые proposed Card values, порядок списков и точные Unicode strings,
не только наличие ключевого слова. No UI screenshot test вместо semantic assertions. Optional API defaults сохраняются:
отсутствующий required_current_premise означает None и не мешает admission genuine
NEEDS_INPUT result; отсутствующий ui_locale означает None, не guessed display_locale.
Contract §8 задаёт base/score/reasons/gaps/actions/L1..L6; short selectors ниже
раскрываются буквально по его словарю. Every original diagnostic slot должен иметь
ровно одну reason/gap/action строку; одинаковый visible text не сокращает cardinality.
Для mutable result дополнительно проверить детachment и nonmutation всех inputs.

## 2. Status and decision oracles

| ID | Independent input/witness | Expected oracle (both locales unless noted) |
| --- | --- | --- |
| P01 | B, exact `evaluate_si` result | DISPLAYABLE; status private OK, decision ELIGIBLE_FOR_CREATIVE, exact eligible summary §5; score «1000 из 1000» / «1000 із 1000»; scoped absence line; gaps=[]; one human continuation action; all L1..L6 |
| P02 | B with Audience knowledge_level UNKNOWN; revise exact Channel/Angle audience refs coherently | OK/NEEDS_INPUT, not evaluator status NEEDS_INPUT; Q01 explanation/action A8; no fabricated audience demographics/demand |
| P03 | B rating0.value UNKNOWN, regenerate bindings | OK/NEEDS_RESEARCH; F01 с private slot 1 и label «Интерес аудитории» / «Інтерес аудиторії»; exact unknown score string, never 0/850/renormalized1000; no UNKNOWN.reason |
| P04 | `Fixture(portfolio='one')`, pair0 UNRESOLVED | OK/REVIEW_DUPLICATE; F05 / Сравнение 1 / Порівняння 1; do not assert confirmed plagiarism/global duplicate; A11 |
| P05 | Same as P04 with exact DUPLICATE finding | Same advisory primary and F05 wording; preserve private human outcome unchanged, not auto REJECT/merge/selection |
| P06 | B explicit SCIENTIFIC blocking Risk true, otherwise complete score1000 | OK/BLOCKED; K01/A6 despite maximum score; score not permission; no automatic CAPABILITY_BLOCKED/RIGHTS_BLOCKED |
| P07 | Old valid B args, then genuine Source revision; new records/observed context, frozen expected/findings intact | STALE; null accepted eligibility/aggregate and [] ratings; fixed stale summary/actions, no old decision/score; no source labels from invalidated context |
| P08 | B minus declared exact Source record | INVALID/REF_MISSING; fixed missing-link explanation; do not claim source is nonexistent or identify hidden ERef from code-only result |
| P09 | Invalid result from a supported/qualified Check with UNKNOWN evidence_refs | INVALID/EVIDENCE_NEEDED is validation failure; use §7 validation message, never NEEDS_RESEARCH/accepted score |
| P10 | Invalid Visual DOCUMENTED with UNKNOWN licence_basis | INVALID/RIGHTS_BLOCKED, no accepted eligibility. Do not reuse OK/V01 condition summary as an accepted BLOCKED decision |
| P11 | B with no claims and permitted UNKNOWN region/interests/analytics | Same eligible scope allowed; no new threshold/minimum-source-count or scientific approval statement |
| P12 | Numerics 0,1000,510 on otherwise B; then UNKNOWN case | Exact literal integer display, no percent/threshold/color/ranking. The same supplied eligibility is unchanged at all known scores; UNKNOWN remains explicit |

## 3. Exhaustive condition families and preservation

| ID | Input family | Full independent assertion |
| --- | --- | --- |
| P13 | Each RC01..RC09; genuine approved C01–C48 constructions in existing oracle suite | Match exact selector/class/source role from Contract §6. D01 missing premise gives only missing-determination reason absent unrelated conditions, not fabricated per-source reviews. D05+D08+D09 retain all three |
| P14 | C01..C05 claim/check/evidence families, including every kind/materiality/state from existing matrix | Central factual blocker survives another supported independent Check. Contradictory evidence stays visible. Fictional claims do not gain guessed evidence gaps; no translator scientific finding |
| P15 | K01..K06 × `.blocking`/`.resolution_basis_refs`; all severity values | Six localized category templates, never classification by EVIDENCE_NEEDED alone. No risk disappears on high score, MITIGATED prose, or category MARKET/PRODUCTION |
| P16 | Visual V01 + generic LEGAL K02, approved C14 | Exactly both blocked explanations plus RC02. RU order: K02 then V01 then RC02; UK same diagnostic order, not alphabetical order |
| P17 | Approved C44: K02+V01 and source2 insufficient review | All three explanations/actions; source2 Source alias assigned by first diagnostic appearance. Rights cannot be hidden by lower-class evidence text |
| P18 | Q01..Q04 and F01..F05 individually | Every row has exactly one proposed translation and action, matching expected private subject/slot. Knowledge/motivation/capability requirements apply only to bounded EVALUATE, not early Discovery |
| P19 | Multiple UNKNOWN-confidence criteria without sufficient findings | One F02 line per criterion, private slots 1..9 и literal criterion labels from approved key order, despite same path/ref; never collapse by EVIDENCE_NEEDED or by translated string |
| P20 | Three portfolio entries DISTINCT/DUPLICATE/UNRESOLVED; then DISTINCT/DISTINCT/missing | Two pair lines in first case, one missing-pair line in second; same candidate ref in two entries still separate pair slots; private portfolio titles/locators never copied |
| P21 | T25 exact four conditions | Four explanations, four gaps, four actions, in K01→RC02→F01→F05 order. Primary BLOCKED unchanged, aggregate UNKNOWN, private codes exactly DUPLICATE_REVIEW_NEEDED/EVIDENCE_NEEDED. Three EVIDENCE_NEEDED diagnostics do not become one |
| P22 | T25, pair DISTINCT; then complete NOT_REQUIRED; then rating0=KNOWN5 in separately coherent fixtures | Only corresponding condition disappears; unrelated blockers/limitations remain. KNOWN score1000 never clears K01 |
| P23 | Genuine old context plus proof-source relevant ERef, as C34 | Evaluator INVALID wins over STALE; explain validation failure, no accepted stale decision or unsupported reconstruction of underlying ERef path |
| P24 | Historical-only source/Run ERef under accepted G01/F1-D1; coherent current payload | Do not create projection blocker from full audit Closure. Only actual evaluator diagnostics rendered; do not rescan ancestry to add required-current conditions |
| P25 | Each of 16 inherited fatal codes in Contract §2 with genuinely accepted Rejected witness where applicable | Exact §7 safe family wording, null eligibility/aggregate, no raw paths/private labels, no claim that validation proves false science/illegal conduct |

P25 evidence discipline: code-family catalog coverage by fixture/mapping inspection
не считается доказательством реальной достижимости каждого error branch. Для
executable follow-up нужны genuine malformed/graph witnesses для заявленных runtime
cases, без manually marking a forged dict accepted. Existing records validator может
вернуть privacy failure до любой domain evaluation; это также validation, не domain verdict.

## 4. Admission, determinism and privacy adversaries

| ID | Input delta | Exact expected presentation behavior |
| --- | --- | --- |
| P26 | Missing result; missing mandatory invocation inputs; result exception instead of dict | UNAVAILABLE, U0/A0 with explicit valid locale; no fabricated evaluator INVALID/NEEDS_INPUT |
| P27 | Unsupported display_locale `ua`, null, missing, arbitrary string | AdmissionFailure={availability:UNAVAILABLE}, no Card/sections/guessed RU default; this is not evaluator locale mutation |
| P28 | Same accepted result, requested RU then UK, including evaluator.locale=ru | Semantic decision/score/slot cardinality identical; exact separate strings from dictionary; evaluator.ui_locale/context/record text unchanged |
| P29 | `status='BLOCKED'` top-level, status='OK' with top-level reason_codes, STALE with non-null eligibility, missing/extra field, UNKNOWN score replaced by null | Unsupported shape → UNAVAILABLE; no alias statuses/coercion/fallback or plausible partial accepted card |
| P30 | Alter only score/eligibility/code/message/ref/path or remove one T25 diagnostic while inputs unchanged | Same-invocation recomputation equality fails; UNAVAILABLE, not repaired copy of evaluator output. Original input/result byte values unchanged |
| P31 | Insert CAPABILITY_BLOCKED or other broader SI code as supposed OK condition | Current pinned result cannot match; UNAVAILABLE. New code enum membership does not authorize projection condition |
| P32 | Genuine accepted human reason contains synthetic `PRIVATE_TOKEN_731`, private names, URL, local path, UUID-like text; no semantic change | No substring of private values in any section/label/exception/log. Changing reason alone must not affect projected decision; no source title rendering |
| P33 | Genuine record title/reviewer label/locator changed and complete hashes/refs rebuilt | Only accepted semantic outcome matters; same condition slots give same generic aliases/templates. Do not insert those text fields even if they look harmless or are in requested locale |
| P34 | Malformed field named `PRIVATE.KEY_731`, including invalid float value, with genuine evaluator INVALID result | Render only safe validation family, never raw path/key/message. Do not log input or exception automatically |
| P35 | Unexpected/private text in supplied diagnostic.message or additional markdown/HTML/link | Equality/closed-catalog admission refuses. No echo, markdown interpretation, string interpolation or URL creation |
| P36 | Two Source refs share a title/id but different exact revisions where graph result valid for tested status | Never unify aliases merely by title/id. For Rejected no source aliases; no raw revision/hash in product card |
| P37 | Same exact inputs repeated; dict insertion order varied without array edits | Exact same Card by value and, for a chosen deterministic text fixture, exact UTF-8/LF bytes. No time/UUID/random/language-service state |
| P38 | UNKNOWN free reason composed `é` vs decomposed `e`+combining acute, coherent inputs | Preserve exact private input bytes, no normalization. Neither reason copied to Card; when evaluator outcome identical, Card identical |
| P39 | Mutate returned reason/action/limitation lists and call again | Original inputs, accepted result and second Card unchanged; no retained mutable state/cache/replay |
| P40 | Long list of repeated condition messages, different genuine subjects/slots | No top-N/collapse/translation-alphabetic sort. Every material reason and all L1..L6 survive. Unsupported output constraint returns UNAVAILABLE, not truncated accepted card |
| P41 | ELIGIBLE with KNOWN capability_notes/licence-related recorded basis and high confidence | No actual CPU availability, scientific truth, licence validity, reviewer authority, production/publication permission claims |
| P42 | Already existing human approvals outside evaluator | Card does not claim approval exists or is absent; it says its scope does not verify/grant approval. No authority lookup/integration added |

## 5. Worked example W01 — «Почему исчезли древние цивилизации?»

**Только синтетические данные.** Вопрос — название искусственной редакционной темы,
а не доказательство исчезновения всех цивилизаций, конкретной причины события,
научного консенсуса, качества источника или спроса. Ни одного verified historical
finding в fixture нет. Никакие drought/war/other cause, hook, asset или Brief не выдумываются.

Воспроизводимая подготовка только existing test helper, не projection implementation:

```text
f = Fixture(t25=True)
f.revise('I', title='Почему исчезли древние цивилизации?')
f.revise('A', idea_ref=f.n['I'])
f.revise('R', basis_refs=[f.n['A']])
args = f.arguments()
result = evaluate_si(**args)
```

Каждая revise создаёт genuine new REVISION Run и exact HUMAN_EDIT record; всего 17
records. Это синтетическая описательная metadata, не доказательство действия реального
reviewer/engine. Expected evaluator tuples **authored before invocation** по frozen T25
и точным новым индексам: K01 records[16].blocking, RC02 premise.determination,
F01 ratings[0].value, F05 duplicate_findings[0].outcome. Existing real evaluator
при preflight подтвердил именно их, primary BLOCKED, UNKNOWN score, два unique codes.

Independent stdlib fixture hashes (input identities only, не новый approved engine vector):

```text
records 2731777fb111efe84005ddb0e324c394849161ceaa1fe0aa5f601a20d291d9c7
ratings 4353e9fecd711ba3391f79fa37149d31f558218be487150c1fa4dc331cf0e87d
```

Topic heading существует только в этом документе; V1 Card не извлекает/не отображает
StoryIdea.title. Ниже — **ожидаемая proposed Card**, не результат implemented renderer.
В reasons base line и score precede diagnostic lines. В gaps копируются ровно четыре
diagnostic строки из reasons; это отображение четырёх условий, не четыре новых факта.

### W01-RU — пять sections

**Редакционное решение**

Продолжение творческой разработки заблокировано отмеченными условиями.

**Основания решения**

1. Основание — условия, зафиксированные оценкой переданных данных.
2. Итоговый балл не определён.
3. Риск 1: В данных зафиксирован блокирующий научный риск.
4. Тема 1: Не решено, нужны ли данные за конкретный период.
5. Рубрика 1 / Оценка «Интерес аудитории»: Не задана одна из обязательных оценок по рубрике.
6. Контекст канала 1 / Сравнение 1: Редакционное решение о пересечении с локальным портфелем остаётся открытым.

**Блокирующие риски и пробелы**

1. Риск 1: В данных зафиксирован блокирующий научный риск.
2. Тема 1: Не решено, нужны ли данные за конкретный период.
3. Рубрика 1 / Оценка «Интерес аудитории»: Не задана одна из обязательных оценок по рубрике.
4. Контекст канала 1 / Сравнение 1: Редакционное решение о пересечении с локальным портфелем остаётся открытым.

**Следующие действия редактора**

1. Риск 1: Передайте отмеченный риск на рассмотрение ответственному человеку; текст плана сам по себе риск не снимает.
2. Тема 1: Решите, нужны ли данные за конкретный период, и явно задайте это условие.
3. Рубрика 1 / Оценка «Интерес аудитории»: Представьте недостающую оценку или рассмотрите её неопределённость, сохраняя неизвестные значения явно.
4. Контекст канала 1 / Сравнение 1: Сравните тему с указанными записями локального портфеля и примите редакционное решение.

**Ограничения и решения человека**

1. Карточка поясняет только оценку переданного контекста; полнота внешних данных не установлена.
2. Баллы и уверенность не доказывают научную истинность, достоверность источников или спрос аудитории.
3. Рассмотрение научных выводов человеком и всех семи областей научной проверки этой карточкой не удостоверяется.
4. Права на материалы, фактическая доступность и выполнимость производства требуют отдельной проверки.
5. Карточка не удостоверяет личность, компетентность или полномочия проверяющего и не предоставляет редакционного утверждения.
6. Допуск к творческой разработке не является разрешением на производство или публикацию.

### W01-UK — ті самі рішення та умови

**Редакційне рішення**

Продовження творчої розробки заблоковане зазначеними умовами.

**Підстави рішення**

1. Підстава — умови, зафіксовані оцінкою переданих даних.
2. Підсумковий бал не визначений.
3. Ризик 1: У даних зафіксовано блокувальний науковий ризик.
4. Тема 1: Не вирішено, чи потрібні дані за конкретний період.
5. Рубрика 1 / Оцінка «Інтерес аудиторії»: Не задано одну з обов'язкових оцінок за рубрикою.
6. Контекст каналу 1 / Порівняння 1: Редакційне рішення про перетин із локальним портфелем залишається відкритим.

**Блокувальні ризики та прогалини**

1. Ризик 1: У даних зафіксовано блокувальний науковий ризик.
2. Тема 1: Не вирішено, чи потрібні дані за конкретний період.
3. Рубрика 1 / Оцінка «Інтерес аудиторії»: Не задано одну з обов'язкових оцінок за рубрикою.
4. Контекст каналу 1 / Порівняння 1: Редакційне рішення про перетин із локальним портфелем залишається відкритим.

**Наступні дії редактора**

1. Ризик 1: Передайте зазначений ризик на розгляд відповідальній людині; текст плану сам собою ризик не усуває.
2. Тема 1: Вирішіть, чи потрібні дані за конкретний період, і явно задайте цю умову.
3. Рубрика 1 / Оцінка «Інтерес аудиторії»: Надайте відсутню оцінку або розгляньте її невизначеність, зберігаючи невідомі значення явно.
4. Контекст каналу 1 / Порівняння 1: Порівняйте тему із зазначеними записами локального портфеля й ухваліть редакційне рішення.

**Обмеження та рішення людини**

1. Картка пояснює лише оцінку переданого контексту; повноту зовнішніх даних не встановлено.
2. Бали й упевненість не доводять наукової істинності, достовірності джерел або попиту аудиторії.
3. Розгляд наукових висновків людиною й усіх семи сфер наукової перевірки цією карткою не засвідчується.
4. Права на матеріали, фактична доступність і здійсненність виробництва потребують окремої перевірки.
5. Картка не засвідчує особу, компетентність або повноваження перевіряльника й не надає редакційного затвердження.
6. Допуск до творчої розробки не є дозволом на виробництво або публікацію.

Переход к production не следует ни из исправления одного поля, ни из hypothetical
score1000. После человеческого исследования/изменений необходима новая оценка exact
контекста; научные/правовые/редакционные approvals рассматриваются отдельно.
Projection не создаёт исторические объяснения причин исчезновения цивилизаций.

## 6. Verification boundary

Будущая implementation acceptance должна выполнить P01..P42, family expansions,
полные literal W01 RU/UK comparisons, input/result nonmutation и all blocker retention.
До её отдельного authorization executable renderer/golden output bytes не создаются.
Markdown example не выдаётся за runtime rendering или scientific review completion.
**STOP: только proposed test requirements; реализация и публикация не разрешены.**
