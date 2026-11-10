# SI-E02.0 — Contract gap matrix

Дата: 2026-11-10 (Europe/Kyiv). **ANALYSIS ONLY / NO NEW CONTRACT APPROVAL.**
Base: `9a631ebca2bccdd8e0157528b20080380ba8dcfe`.
Связанные документы: [inventory](STORY_INTELLIGENCE_SI_E02_0_ARCHITECTURE_INVENTORY.md),
[owner questions](STORY_INTELLIGENCE_SI_E02_0_OWNER_DECISION_PROPOSAL.md).

## 1. Повторное использование: все 18 SI типов, без нового TopicScore/Brief wire

[records_v1._SCHEMAS](../../story_intelligence/records_v1.py) и validate_si_record /
si_record_ref / validate_si_record_ref уже реализуют закрытые структуры. Основание —
[original SI/1](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md),
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[R1b approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md) и
[composite owner approval](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md).

| Existing SI records | Повторное применение | Чего наличие schema не даёт |
| --- | --- | --- |
| Intake, StoryIdea | Тема, viewer_question, intake/source provenance, optional candidate_binding | Discovery executor/дедупликация; manual creation StoryIdea запрещено R1a, genesis только DISCOVERY |
| SourceItem, ClaimItem, EvidenceItem, ClaimCheck | Exact sources/claims/evidence links, review assertions и qualifications | Fetch, чтение материала, human identity, истинность или действительные права |
| AudienceHypothesis, ChannelContext, Angle, Rubric | Явная аудитория/канал/локальный портфель/ракурс/версия критериев | Аналитика аудитории, live competition, calibrated ranking |
| RunRecord, EvaluationReport | Frozen method/input lineage, ratings/eligibility/risk refs/aggregate representation | Фактическое выполнение method или вычисленный evaluator result |
| CreativeAlternative, VisualRequirement, Risk | Hook/title/chapter refs, визуальные приоритеты/fallback/effort, блокеры | Генерация, clearance материалов, реальная стоимость/retention |
| ProductionBrief, Selection, ReviewPacket | Existing pre-script Brief, human intent по Creative/Brief, private discussion capture | Assignment queue, topic APPROVE, editor authority, exporter/persistence/renderer |

Editorial counterparts в [model.py](../../editorial/model.py): CandidateRevision,
GenreProfile/RubricCriterion/CriterionRating, SourceRevision/SourceDetails,
ClaimRevision/EvidenceLink/ClaimReview, RightsReview/RightsDetails, ProductionRevision,
ScriptRevision/BriefValue/ScriptSegment, ScenePlanRevision/AssetRevision,
ApprovalRecord/ActiveSelections. Их закрытые schema-1/2 codec и digest не меняются.
SIRef не взаимозаменяем с editorial RevisionRef/ERef; общий title не связывает объекты.

## 2. Карта требований и реальных границ

| Требование | Уже есть / exact contract basis | Реальный пробел и минимальный путь |
| --- | --- | --- |
| Exact refs и передача currentness | [resolver_v1.resolve_si_record/resolve_si_closure](../../story_intelligence/resolver_v1.py), [provenance_v1.verify_si_provenance](../../story_intelligence/provenance_v1.py), [currentness_v1.check_si_currentness](../../story_intelligence/currentness_v1.py) | Caller передаёт полный bundle, один root SIRef и explicit active/head lists. Возвращаемое {currentness,reason_codes} — detached local value, не новый persisted record/authority token. Нет workspace/harness поставщика наблюдаемого context; его runtime контракт нужен отдельно |
| Freshness/provenance | Exact type/id/revision/sha256; immutable previous, actual Run; accepted G01/G02/F1-D1 | G01: history не current сам по себе. G02: direct original C ClaimItems retained. F1-D1: actual producer Run ERefs + original C relevant, history-only ERefs не promoted. Это закрытые принятые правила, не повод для нового resolver/role map |
| INVALID vs STALE | Broken/missing/hash-conflicting graph → INVALID; valid historical dependency absent/replaced active → STALE/INPUT_STALE | Нельзя лечить dangling ref через UNKNOWN/«latest». CURRENT не доказывает recency по clock, truth, license или соответствие freshness_requirement; такой review не реализован |
| Рекомендация → человек | R1 §§3–4: eligibility advisory, Selection SELECT/REQUEST_CHANGES/WITHDRAW по exact Creative/Brief scopes | Нет SI topic approval/reject operation. Human intent не OS identity; editorial SCRIPT/SCENES/HANDOFF authority задаётся [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md), [O1–O10](E01_3_8_1_APPROVED_CONTRACT.md), не SI score |
| Критерии/ratings | Rubric exact ref; EvaluationReport ratings с criterion_key/value Known/basis refs/explanation/confidence; actual EVALUATION Run Rubric binding уже проверяется provenance | Нет EVALUATE executor. Будущий method должен проверить exact referenced Rubric keys/order/coverage, correct aggregate и deterministic blockers; local validator не является полным semantic evaluator |
| Research, evidence, UNKNOWN | SourceItem provenance/locator/material hash Known; ClaimItem type/materiality; EvidenceItem relation; ClaimCheck state/evidence/qualification/reviewer metadata | Нужен реальный человеческий review/material access, не новые generic wire fields. UNKNOWN не 0/[]/verified; reviewer_label не authentication. Cross-record evidence coherence/coverage должны быть проверены будущим оценщиком |
| Аудитория/язык | AudienceHypothesis assumptions/basis_refs, ChannelContext; wire locales ru/uk; Brief locale и production locales | Нет автоматических audience statistics/translation. User RU/UA соответствует существующему uk; новый ua enum не нужен. Audience/region/age hypothesis не становится утверждённой настройкой |
| Duration/intensity/resources | ProductionBrief.duration_min_s/duration_max_s/intensity; production resource_budget/CPU fallback; Creative chapters.target_seconds | Оценки длительности не measured WAV timing. Intensity CALM/BALANCED/DYNAMIC уже закрыт; новый intensity type не нужен. Реальные staging/time/resource gates остаются downstream |
| Визуальная сложность | VisualRequirement.role/acquisition/source_refs/material_sha256/rights_state/effort/fallback; Risk(PRODUCTION/LEGAL); criteria visual_feasibility/resource_fit | Qualitative estimate, не автоматически существующий asset или цена. Essential unknown rights/fallback — blocker. Достаточно existing refs/оценок; не требуется отдельный VisualComplexity record |
| Новизна/конкуренция | Angle.distinction, ChannelContext.portfolio Known, Rubric angle_novelty/portfolio_distinctness, Evidence/Source basis | Live competitor/trend metrics MISSING и offline V1 не обещаны. UNKNOWN portfolio не empty. Новый обоснованный показатель потребует отдельной method/Rubric revision, не скрытого score default |
| Данные Production Brief | Exact idea/audience/channel/angle/evaluation/creative/used selection refs, source/claim/check/visual/risk refs, locale/mode/promise, duration/intensity/options, reviews/must_avoid/unresolved | Schema уже достаточна для pre-script card. Нет builder, selection prerequisites/assembly execution, реальной передачи в production; новый Brief wire не обоснован |
| SI → editorial | Candidate binding/ERefs возможны; editorial model имеет production-scoped candidates/sources/rights, frozen script BriefValue | Automatic derived Candidate export нельзя назвать manual discovery_method. BriefValue неполон для SI Brief/run metadata. Нужен отдельный provenance-preserving adapter contract; не JSON внутри reason/rationale |
| Rights/license boundary | SI rights notes и Visual rights_state, editorial material binding, exact intended use; [rights_binding.validate_rights_binding](../../editorial/rights_binding.py) | CONFIRMED означает material match, не rights grant/expiry policy. [Import gate](../../LICENSES/IMPORT_LICENSE_GATE.md), [release checklist](../../LICENSES/RELEASE_COMPLIANCE_CHECKLIST.md), [voice gate](../../COMMERCIAL_VOICE_LICENSE_GATE.md) обязательны, score/Selection их не снимают |
| ReviewPacket/privacy | Approved R1 §5/R1b; recorded DISCUSSION_ONLY Packet, field paths, grants/redaction | Schema не реальный privacy-reviewed exporter. Packet snapshot freshness не domain currentness E1; нельзя превратить public report в raw workspace export |
| Production Assignment | ProductionRevision хранит контекст; ScriptRevision.production_ref/candidate_ref связывают готовый script; S1 grants/VirtualStore — тестовая transaction модель | Existing links достаточны для простой связи script/candidate/production. Для assignee/queue/deadline/reservation/ack и job runner нужен отдельный operational contract только при owner demand, не дополнительный флаг Brief |
| Durable SI commands | R1 §2/§6 operation names/options/idempotency и SI-D03 principle утверждены | Private workspace exact path, atomicity, concurrency, retention/privacy/mapping lifecycle не закрыты; нужен отдельный persistence contract до durable writing. Native protected storage не заменяет SI private draft workspace |

## 3. Topic Scoring: что уже утверждено

SI-D04 composite approval распространяется на девять критериев/веса:

| criterion_key | weight_percent |
| --- | --- |
| audience_interest | 15 |
| channel_fit | 10 |
| angle_novelty | 10 |
| evidence_quality | 20 |
| narrative_potential | 15 |
| visual_feasibility | 10 |
| resource_fit | 10 |
| risk_manageability | 5 |
| portfolio_distinctness | 5 |

Сумма 100, rating 0–5; при всех known aggregate_tenths = 2 × Σ(weight × rating),
иначе UNKNOWN. Нет renormalization по известным и threshold автоматического разрешения.
R1 §3.2 precedence: invalid/stale inputs; blocking risk → BLOCKED; missing context →
NEEDS_INPUT; other missing evidence → NEEDS_RESEARCH; unresolved duplicate →
REVIEW_DUPLICATE; только достаточные inputs → ELIGIBLE_FOR_CREATIVE. Нет требования
будущего creative/selection для E1 и нет обещания «вероятности успеха».

Неоднозначное planning wording «scores/weights proposals» не отменяет SI-D04 approval.
Не утверждены **новые** SI-E02 criterion changes, competition weights/thresholds,
cross-candidate ranking/ties и job priority. Это отдельный owner choice, не дефект
существующего Rubric и не повод создать TopicScore рядом с EvaluationReport.

## 4. Какие контракты действительно потребуются

| Gap ID | Природа | Минимальное следствие, без реализации |
| --- | --- | --- |
| E02-G1 | Implementation gap существующих methods | Закрыть executable postconditions/oracles EVALUATE/RECORD_SELECTION/ASSEMBLE_BRIEF по approved contracts; не создавать параллельные record types |
| E02-G2 | Material contract gap **если нужен durable topic intent/ranking** | Existing Selection scopes/targets исключают StoryIdea; Candidate assessment не хранит такое решение. Нужен отдельный узкий owner-approved operation/scope proposal, без нового editorial APPROVE и без stuffing в reason |
| E02-G3 | Material contract gap **если нужна production assignment** | Existing Brief/ProductionRevision не job queue. Отдельные actor/lifecycle/receipt/rights boundaries должны быть спроектированы и утверждены; не считать их уже доступными |
| E02-G4 | Integration contract gap **для ERefs/автоматического handoff** | Exact validated snapshot provenance и read-only adapter, затем отдельное допустимое mapping SI→editorial draft. Сейчас relevant ERefs fail closed; сохранять их, а не очищать ради CURRENT |
| E02-G5 | Lifecycle contract gap **до durable workspace/export** | Довести SI-D03/SI-D07 до concrete privacy/storage/retry lifecycle; generic S1 protected writer не даёт этого разрешения |

Для карточки, rubric data, Research/Evidence, Creative и самого SI ProductionBrief
недостаточность типов **не доказана**: повторно использовать existing SI/1.
Для topic decision/assignment доказана ровно отсутствие нужных разрешённых
roles/operation semantics; это не утверждение конкретного нового wire shape.
Chapters Brief не готовые renderer scenes. Existing `read_plan` из `scripts/first_video.py`
принимает 1–20 scenes, до 2000 characters текста на scene, ru/uk; future adapter
должен явно проверять эти ограничения и timing, а не молча обрезать 8–12 min draft.
A/E/O/D/S1 contracts, checksums/hashes и принятый currentness не пересматриваются.
**NOT RUN — DOCS ONLY.** Следующие owner вопросы — в proposal, реализация не разрешена.
