# SI-E02.1a — Contract boundary matrix

Дата: 2026-11-10. **DOCS ONLY / IMPLEMENTATION NOT AUTHORIZED.**
Base: `3e9adca8cdd17da69a3e72225a8129a8122c4311`.
Нормативные десять решений — [owner approval](STORY_INTELLIGENCE_SI_E02_1A_OWNER_APPROVAL_2026_11_10.md).
[P01–P05](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md) сохраняются.
Старые [Topic](STORY_INTELLIGENCE_SI_E02_1_TOPIC_INTENT_CONTRACT_PROPOSAL.md) и
[Scientific](STORY_INTELLIGENCE_SI_E02_1_SCIENTIFIC_REVIEW_PROFILE_PROPOSAL.md)
proposals — источник вариантов, не blanket approval всех их деталей.

## 1. Статусы

| Статус | Значение |
| --- | --- |
| APPROVED PRINCIPLE | Владелец утвердил указанное требование/направление; это не executable schema |
| EXISTING CONTRACT | Уже утверждённая норма, которую новый проект обязан сохранить |
| OPEN CONTRACT DETAIL | Требуется отдельное точное решение; здесь вариант не выбирается |
| IMPLEMENTATION NOT AUTHORIZED | Ни один принцип этого этапа не разрешает писать runtime |
| BLOCKED | Конкретный путь нельзя реализовать до закрытия указанной зависимости |

BLOCKED ниже ограничен указанным путём. Общий запрет реализации действует на весь
текущий этап независимо от того, есть ли у будущего пути дополнительные blockers.

## 2. Topic Intent boundaries

| Решение | APPROVED PRINCIPLE | EXISTING CONTRACT | OPEN CONTRACT DETAIL / BLOCKED path |
| --- | --- | --- | --- |
| TI-P01 | Минимальный versioned Selection extension; без parallel TopicIntent без доказательства | Legacy SI/1 закрыт | Schema version, dispatch, migration; блокируют новый reader/writer для topic intent |
| TI-P02 | RESEARCH/DEFER/REJECT/PRIORITIZE под conceptual TOPIC_INTENT; human intent only | Прежние Creative/Brief choices неизменны | Exact command/admission/error mapping; блокирует исполнение новых действий |
| TI-P03 | Exact Idea revision + Audience + Channel; explicit human action, exact target binding | SIRef exact type/id/revision/hash, provenance; labels не authority | Wire representation и admission context/target checks; блокирует признание нового intent |
| TI-P04 | Append-only exact-scope chain, predecessor/CAS; new context → new scope | Immutable history; нет implicit latest | Полный builder order, concurrent transition/error specification; блокируют детерминированное построение/изменение head |
| TI-P05 | R1 byte-exact retry, conflict при changed bytes, no head rollback | Existing R1 §6 request-id semantics | Новый request layout, output mapping и atomic replay integration; блокируют topic runtime replay |
| TI-P06 | Private durable integrity-preserving storage | SI-D03 private workspace boundary | Path/locking/atomicity/recovery/retention/delete/backup/privacy; блокируют durable lifecycle |

Текущий [records_v1](../../story_intelligence/records_v1.py) принимает только
Selection purposes CREATIVE_CHOICE / BRIEF_REVIEW, choices SELECT / REQUEST_CHANGES /
WITHDRAW и targets CreativeAlternative / ProductionBrief с purpose-specific binding.
TOPIC_INTENT и четыре human actions **не valid legacy SI/1 wire tokens**.
Не подставлять их в текущий parser, не расширять незаметно enum, не добавлять поле
`action`, новую команду или migration через этот документ. Exact future version не выбран.

Утверждение chain/CAS принципа не утверждает предложенный ранее H.input_refs order
или порядок admission шагов. Хранение record + request mapping + head должно получить
отдельные согласованные atomicity/recovery guarantees до durable реализации.
Нет automatic approval, ranking/tie-break, scheduler/jobs или editorial grants.

## 3. Scientific Review boundaries

| Решение | APPROVED PRINCIPLE | EXISTING CONTRACT | OPEN CONTRACT DETAIL / BLOCKED path |
| --- | --- | --- | --- |
| SR-P01 | Нормативный checklist поверх existing records, без ScientificApproval/authority | Claim/Evidence/Check/Risk/Brief schemas и exact refs | Profile version/consumer integration; блокируют executable profile |
| SR-P02 | Рассмотреть SR-C01–07: terminology, chronology, competing explanations, counter-evidence, qualifications, traceability, intended-use rights | Known/UNKNOWN, review state/evidence rules; score не truth | Completion/applicability criteria и независимые oracles; блокируют machine-complete status |
| SR-P03 | Explicit human review/escalation существенных contradictions/unsupported claims/rights gaps | Existing blockers binding; label/confidence не competence/authority | Ответственность, triggers/выход escalation и traceability границы; блокируют автоматизацию workflow/clearance |
| SR-P04 | Начать с private human-readable checklist, без hidden JSON | Existing free-text fields не machine proof; privacy/export boundaries | Durable capture, field mapping, machine completion/export; блокируют persisted machine status и экспорт новых полей |

Все семь областей обязательны для рассмотрения, но их рассмотрение не равно
положительному review. Точный критерий completion, допустимость и форма обоснования
неприменимости ещё не определены. Не вводить automatic pass из пустого списка,
новый ClaimCheck state, source-count threshold или scientific approval по score.
Source record hash не доказывает чтение material, URL не доказывает доступ, rights note
не даёт лицензию. Essential unresolved claims/rights/fallback gaps не снимаются
человеческим выбором темы или словом «проверено».

## 4. Минимальный реестр оставшихся blockers

Идентификаторы B01–B08 — локальные ссылки этого документа, не wire codes.
Порядок строк показывает зависимости, а не разрешение следующего этапа.

| ID / OPEN CONTRACT DETAIL | Dependency для закрытия | Риск без контракта | Какие пути BLOCKED | Что этим не блокируется |
| --- | --- | --- | --- | --- |
| B01 Versioned Selection schema/compatibility dispatch/migration | TI-P01–03; separate owner-approved exact closed schema и old/new reader behavior | Незаметное расширение SI/1, несовместимые bytes/refs | Новый topic Selection codec/validator/reader/writer | Existing SI/1 validation; bounded pure EVALUATE на старых типах |
| B02 Exact operation/admission/error mapping | B01, TI-P03–05, R1 operations; exact context/target/predecessor/retry precedence | Разные outcomes, wrong-target intent, потеря conflict checks | Topic intent executor, admission и его command API | Pure EVALUATE без topic actions/heads |
| B03 Builder ordering/independent golden vectors | B01/B02; normative ordered inputs, literal canonical bytes/hashes/negative cases | Недетерминированные identities или self-confirming tests | Новый topic builder и его qualification | Existing vectors/current codecs и independent EVALUATE contract work |
| B04 SI-D03 persistence/CAS/recovery lifecycle | TI-P06; B02 для topic transaction; отдельно location/locking/atomic record+mapping+head, retention/delete/backup/privacy | Torn writes, head rollback, resurrection, утечка private intent | Любой durable topic writer/replay/restore и durable checklist capture | Read-only/pure in-memory computation, не обещающая durability |
| B05 Scientific completion semantics | SR-P01/02; exact scope/applicability, evidence/uncertainty/completion criteria и oracles | False scientific pass, checklist coverage выдана за truth | Machine-verifiable completed profile/automatic clearance | Human consideration checklist; general EVALUATE по existing rubric без science-complete claim |
| B06 Human escalation/traceability boundaries | SR-P03, existing review/rights; exact responsibility, material identity, unresolved outcomes | Необоснованные credentials, фиктивное resolution, непроверяемые sources | Автоматизированная escalation/clearance и утверждение полной review sufficiency | Явное human unresolved/research/blocker описание; bounded EVALUATE без таких гарантий |
| B07 Optional machine-readable review capture | B05/B06 + отдельное field mapping/version/export approval; B04 только если durable | Hidden JSON, потеря scope/privacy, stale review как current | Новые machine completion fields/projection/export и persisted checklist state | Первый private human-readable checklist; pure EVALUATE на existing SI fields |
| B08 ERef integration / production handoff | Отдельные contracts: exact validated editorial snapshot adapter; для handoff — editorial authority/rights и consumer mapping | Ложный CURRENT, privilege crossing, неподтверждённое производство | ERef-dependent validation без snapshot; automatic SI→editorial/jobs/render | Только действительно ERef-free bounded local SI path; private existing Brief card по P03 |

B08 содержит **два отдельно scoped** направления: snapshot adapter не разрешает
production handoff, а consumer mapping не решает validation snapshot. Native Windows
host/service не prerequisite для pure ERef-free вычислений; protected writer всё ещё
недоступен и не заменяется private SI persistence.

## 5. Bounded pure EVALUATE — граница зависимостей

[P01](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md) сохраняет существующие
девять SI-D04 критериев/веса, per-criterion evidence/confidence/UNKNOWN и aggregate
только при approved completeness. Human priority не automatic cross-candidate ranking.
Будущий bounded pure EVALUATE может работать на existing valid local ERef-free SI
bundles и existing records без новых Topic Intent values, durable storage, scientific
machine-completion profile, adapter, production consumer или Windows service.
B01–B07 и production часть B08 **не являются общими prerequisites этого пути**.

Это не обещание, что executor уже реализован/принят, и не разрешение implementation:
потребуется отдельное exact-base задание с allowlist, точными требованиями операции,
независимыми test oracles и приёмкой в рамках утверждённого контракта. Если такой
ограниченный executor действительно использует зависимость из B01–B08, соответствующий
gate снова обязателен. Нельзя назвать путь ERef-free, удалив existing relevant ERefs.

## 6. Неизменные freshness, review и licensing boundaries

[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md): causal/audit
ancestry и required-current semantic dependencies различаются; historical HUMAN_EDIT
edit-base не автоматически current constraint.
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md): original CREATIVE
Run direct ClaimItem inputs сохраняются как самостоятельные exact constraints.
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md): actual current
producer Run H.editorial_refs, включая текущий REVISION Run HUMAN_EDIT/CreativeAlternative,
релевантны; original C ERefs не игнорируются. Только историческое присутствие ERef в
audit Closure не делает её required-current. Relevant ERef без exact validated snapshot
→ INVALID / REF_MISSING; не STALE/UNKNOWN/CURRENT по умолчанию.

Нет implicit latest, rebasing, wire fields/error codes или изменений accepted modules.
R1/R1a/R1b, E00/A/O/storage contracts неизменны. Existing eligibility blockers нельзя
обойти score, choice, confidence или checklist. Права на intended-use материалы и
verified lawful fallback обязательны; private card не production approval.
RU/UA с wire locales `ru/uk`, CPU-only fallback и licensing requirements сохраняются.
Никакого автоматического переноса китайских корпусов/Writing-DNA.

**IMPLEMENTATION NOT AUTHORIZED. Unit tests: NOT RUN — DOCS ONLY.**
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без code/schema/test/UI/persistence/dependencies,
PR/merge/release/main changes. **STOP; SI-E02.2 не начинать.**
