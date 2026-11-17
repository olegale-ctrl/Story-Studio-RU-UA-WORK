# SI-E02.1 — Scientific review profile/checklist proposal

Дата: 2026-11-10 (Europe/Kyiv).
**PROPOSAL / NOT APPROVED / NOT IMPLEMENTED.**
Base: `a577746f308828d75d2ea7262eaa94ab18a523c1`.
[P05 owner approval](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md)
утверждает **requirements design**, семь областей coverage и запрет score-derived
scientific readiness. Детальные SR-Cxx/SR-Pxx ниже — proposals, не approved gate,
wire schema, permission/declaration codes или implementation contract.

## 1. Назначение и неизменные основы

Для science/science-popular карточки человек должен иметь возможность отличить
наблюдение, объяснение, неизвестное и неподтверждённый тезис по конкретным источникам,
а также проверить использование материалов. Это не automatic fact-checking,
экспертная сертификация, авторизация или production handoff.

Сохраняются [original SI/1 §§3/5–7](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
[R1 §§3–5](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md),
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[R1b approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md),
[SI-D01–D10](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md).
Девять SI-D04 criteria/веса, ratings 0–5, UNKNOWN/aggregate и blocker precedence
не изменяются. High score не свидетельствует о проверенной науке или лицензии.

## 2. Reuse и альтернативы SR-P01

| Вариант | Польза | Цена/ограничение |
| --- | --- | --- |
| A. Только general eligibility без предметного checklist | Existing general policy остаётся доступной | Не выполняет approved P05 design scope; нет явной science coverage |
| B. Requirements profile + private human checklist, exact evidence в existing records | Минимум новых сущностей; science review объясним, references/provenance сохраняются | Machine-verifiable completion mapping ещё требует отдельного решения; free text не proof |
| C. Новый ScientificApproval record/автоматический score gate | Может выглядеть единым «готово» | Дублирует authority/approval, не доказывает truth/competence; необходимость не доказана |

**SR-P01 recommendation: B.** Не создавать отдельный ScientificApproval, новый score
или parallel authority. Existing SI ProductionBrief остаётся первым private consumer.
Предложенный profile identifier/version и точный capture format должны быть отдельно
утверждены; здесь никакого нового value/RecordType в SI/1 не определяется.

| Existing type/field | Роль в science review | Граница |
| --- | --- | --- |
| ClaimItem.statement/claim_kind/materiality/evidence_expectation | Что проверяется, насколько существенно; factual/interpretation/fictional | Сам тип factual не доказывает истинность; нельзя переименовать неподтверждённый факт в fiction для скрытого обхода |
| SourceItem, Known metadata/material_sha256/freshness_requirement | Версия, происхождение, locator, неизвестные данные | URL не fetch; record SHA не material digest и не license |
| EvidenceItem.claim_ref/source_ref/relation/locator | Supports/contradicts/context/insufficient с exact refs и объяснением | Количество supports не голосование об истинности, relation — supplied assertion |
| ClaimCheck.state/evidence_refs/qualification/reviewer metadata | Конкретное человеческое рассмотрение exact claim/evidence | Label/time не authenticated identity/credentials; accepted schema не выполняет review |
| Risk.basis_refs/resolution_basis_refs/mitigation | Нерешённые science/legal/reputation/production risks и основания решения | Mitigation text не сама по себе verified resolution |
| EvaluationReport.ratings/basis_refs/confidence/eligibility | Раздельные эвристические оценки и причины блокировки | Aggregate не scientific readiness; confidence qualitative, не вероятность |
| CreativeAlternative + VisualRequirement | Проверяемые hook/chapter claims, visuals, права/fallback | Интересный hook не вправе менять scientific qualifiers или очищать original C constraints |
| ProductionBrief.claim_check_refs/risk_refs/required_reviews/unresolved | Private карточка с review tasks и exact результатами | required_reviews — Text list, не зарегистрированные machine codes/authority flags |

## 3. Proposed coverage SR-C01–SR-C07

Каждая проверка относится к точной теме/ракурсу/claims и source revisions.
«Не применимо» — только human scope justification в checklist после проверки,
не automatic pass из отсутствующих данных, не новый ClaimCheck.state.

| ID — proposed checklist label | Что должен проверить человек | Требуемое основание | Если coverage недостаточно |
| --- | --- | --- | --- |
| SR-C01 Terminology | Определения ключевых слов, единицы/масштаб; например город/государство/население не одно «исчезновение» | Exact SourceItem/EvidenceItem locators, bounded claim/Angle и объяснение области термина | Если от определения зависит central claim — blocker до уточнения; не подставлять бытовой смысл |
| SR-C02 Chronology | Календарь, интервалы, последовательность, границы датировок и степень точности | Источник конкретной датировки/метода, qualifications и явные UNKNOWN | Не выдумывать точные даты; unresolved essential chronology блокирует утверждение |
| SR-C03 Competing explanations | Действительно относящиеся к scope объяснения, их основания/ограничения; без false balance | Раздельные exact claims/evidence relations и reason, почему версии сравнимы | Нет исследованного набора → research gap, не «альтернатив нет» |
| SR-C04 Counter-evidence | Противоречия, контрпримеры, границы выборки, отрицательные/неподтверждающие результаты | Explicit contradicts/context/insufficient links; ClaimCheck/Risk, видимое объяснение несогласия | Нельзя перевесить central contradiction числом sources или высоким rating |
| SR-C05 Qualifications | Не превращены ли hypothesis/conditional вывод в факт; preserved scope/числа/цитаты в hook/title/chapters | ClaimCheck qualified с non-null qualification; exact Creative/Brief refs, human текстовая проверка | Unsupported essential factual wording — blocker; новая формулировка/claim требует explicit review/revision |
| SR-C06 Source traceability | Реально доступные reviewer exact version/edition, locator, происхождение и материал, на который опирается вывод | Source/Evidence refs, lawful material access, version/locator; verified material digest если доступен/обязателен для данного материала | Один URL/record hash не proof; неизвестные essential version/locator/material identity — blocker, не fake hash |
| SR-C07 Intended-use rights | Что именно используется: текст/цитата/карта/изображение/аудио/font; разрешён ли intended use, срок/условия, attribution/fallback | Existing SI notes/visual requirements + реальные license/review основания; editorial RightsReview bindings при отдельной integration | Essential material без прав или проверенного lawful fallback — blocker; score/selection не grant |

Это предлагаемая детализация утверждённых областей P05. Exact checklist wording,
допустимость scope justification и material-digest requirements требуют отдельного
owner approval перед кодированием. Никакого «не менее N источников» по умолчанию.

## 4. SR-P02 — evidence, interpretation, uncertainty и confidence

- **Established evidence** в человеческом представлении — ограниченное наблюдение
  из реально рассмотренного материала с provenance/locator. Это не новая wire enum
  и не абсолютная истинность. Human supported review должен иметь exact evidence.
- **Interpretation** связывает вывод с основаниями/альтернативами; existing
  claim_kind=interpretation не превращается в факт из-за согласия нескольких авторов.
- **Uncertainty** сохраняется Known/UNKNOWN, qualifications, confidence и явным
  scope. UNKNOWN не ноль и не known empty evidence list. Незнание counter-evidence
  не означает проверенное отсутствие противоречий.
- **Unsupported** central/essential factual claim не получает supported от creator
  label, neural output, количества источников, агрегата или human priority action.

Reuse closed ClaimCheck states из [records_v1](../../story_intelligence/records_v1.py):
`unreviewed` требует null reviewer_label/reviewed_at/reason; у reviewed states эти
поля присутствуют. `supported/qualified` требуют KNOWN nonempty evidence_refs;
`qualification` обязателен ровно для `qualified`, не для `disputed`/`unverified`.
`removed` не удаляет immutable claim и не оправдывает фактическую фразу, оставшуюся
в hook/Brief. Review state changes — новые legal revisions, не in-place overwrite.

Confidence LOW/MEDIUM/HIGH/UNKNOWN с basis — qualitative statement. HIGH не
переводит ClaimCheck в supported; UNKNOWN не LOW автоматически. Проверка всех
положенных fields/references необходима, но не заменяет фактическое прочтение
и предметную оценку человеком. Contradiction не разрешается majority vote.

## 5. SR-P03 — blockers, escalation и человеческая ответственность

Сохранять порядок [R1 §3.2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md):

1. Schema/hash/missing/cycle/provenance failures → INVALID; valid outdated domain
   refs/current-context mismatch → STALE. Ни scientific checklist, ни label не чинят их.
2. Essential unreviewed/unsupported/disputed factual claim, blocking scientific
   risk или essential rights/fallback gap → existing BLOCKED. Qualified wording
   требует нового честного review с корректным state/qualification; поле qualification
   нельзя просто заполнить при state=disputed и считать противоречие разрешённым.
3. Missing required framing/context → NEEDS_INPUT; другие missing evidence →
   NEEDS_RESEARCH; unresolved duplicate → REVIEW_DUPLICATE по действующему policy.
4. ELIGIBLE_FOR_CREATIVE возможно только при выполненных existing prerequisites,
   не означает scientific certificate/выбор Brief/production approval.

Указанные outcomes — reuse existing eligibility rules; новая SCIENCE_APPROVED state
не предлагается. Coverage-scoring, автоматические expert badges и source-count
thresholds отсутствуют. High aggregate при essential blocker остаётся BLOCKED.

Human reviewer отвечает за доступ к материалу, применимость/границы выводов,
видимость противоречий и честность записи своей работы. reviewer_label и timestamp
не доказывают OS identity, competence или независимость. Нельзя автоматически
выдать credentials/новую роль/grant из scientific profile. [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md)
и [O1–O10](E01_3_8_1_APPROVED_CONTRACT.md) остаются отдельной editorial authority boundary.

При недостаточном доступе, понимании метода, спорной central chronology/claim или
неясных правах — оставить unresolved/blocker, сузить формулировку и запросить
предметное human рассмотрение. Дополнительный reviewer/консультация — явный
человеческий шаг, не сгенерированный «эксперт». Конкретные escalation criteria и
responsibility checklist предлагается утвердить отдельно; автоматическое снятие
blocker после такого запроса запрещено. Фактический внешний контакт здесь не выполняется.

## 6. SR-P04 — capture/compatibility и freshness

Рекомендуется начать с private requirements checklist. Existing ClaimCheck/Evidence/
Risk refs фиксируют конкретные данные; ProductionBrief.required_reviews/unresolved
могут **человечески описывать** задания/пробелы. Нельзя трактовать наличие слова
«проверено» в Text как machine-complete SR-Cxx или кодировать hidden JSON в reason.
Если нужна machine-verifiable per-check completion/traceability matrix, точный
nonpersisted projection либо дополнительный versioned capture contract должен быть
отдельно утверждён. Virtual checklist не имеет H/SIRef и не должен получать fake ref.
ReviewPacket export новых profile fields/labels также не разрешается автоматически.

Currentness API и [G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md)/
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md)/
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md) остаются unchanged:
точные refs, immutable history, original C constraints, current actual producer ERefs.
Изменение source/check/Angle создаёт новое состояние inputs; старая review assertion
не переносится latest на новое содержимое. Historical-only Run ERef не становится
required-current сам по себе. Relevant ERef без exact validated snapshot →
INVALID/REF_MISSING, не UNKNOWN-as-validated.

P04 разрешает первый future bounded path на ERef-free local SI bundles; не удалять
existing ERefs и не ослаблять checks, чтобы research card стала CURRENT. Даже CURRENT
по accepted pure API — не доказательство научной достаточности/прав или полного
profile coverage. Private workspace persistence/retention по SI-D03 не реализуются.

## 7. Rights/license/production boundary

[Rights binding](../../editorial/rights_binding.py) CONFIRMED — material match, не
license/expiry/intended-use clearance. SI rights_note/DOCUMENTED — данные, не grants.
[Import licensing gate](../../LICENSES/IMPORT_LICENSE_GATE.md),
[unresolved items](../../LICENSES/UNRESOLVED_ITEMS.md),
[commercial voice gate](../../COMMERCIAL_VOICE_LICENSE_GATE.md) и
[release checklist](../../LICENSES/RELEASE_COMPLIANCE_CHECKLIST.md) обязательны.
Китайские корпуса/Writing-DNA и model/API weights не переносятся автоматически.

Optional visual с UNKNOWN rights можно **явно исключить новой revision** и проверить
lawful fallback; нельзя молча объявить его licensed или снять essential blocker
на основании одного текста «сделаем схему». Actual data/qualifications и права на
fonts/изображения/голоса/source excerpts всё равно проверяются. CPU-only путь local
WAV/stills — capability option, не универсальная правовая замена и не разрешение render.
RU/UA presentation использует wire ru/uk; scientific qualifiers сохраняются в обоих
языках, автоматический translation/fact correction не реализован.

## 8. Оставшиеся решения и независимые test-oracle requirements

| Proposal choice | Recommendation | Без approval заблокировано |
| --- | --- | --- |
| SR-P01 profile form/version | Requirements document/checklist на existing records, без parallel approval type | Executable profile, version registry/consumer integration |
| SR-P02 coverage meaning | SR-C01–07 с exact evidence и explicit uncertainty; без source-count rule | Машинное определение completion/qualification adequacy |
| SR-P03 responsibility/escalation | Явный human review scope, no invented credentials | Новый human review workflow/escalation automation |
| SR-P04 capture/traceability | Human checklist сначала; machine mapping отдельным контрактом | Persisted checklist status/projection/export и durable review lifecycle |

Expected states/refs/canonical hashes независимых fixtures должны быть authored
до implementation, не скопированы из scorer/profile функции. Это requirements,
не результаты выполненных тестов. Нужны как valid graphs с semantic review отказом,
так и corruption failures accepted resolver/provenance; отсутствие hash ошибки
само по себе не PASS science review.

| Future oracle (NOT RUN) | Независимо ожидаемое свойство |
| --- | --- |
| Same ambiguous term, разные scale definitions | Нет ложного объединения claims; bounded wording/source scopes различимы |
| Chronology UNKNOWN/interval против invented precise date | Не создаётся значение/уверенность из отсутствия данных; essential gap блокирует |
| Supports плюс central contradicts | Нет majority-vote/aggregate override; human resolution/qualification required |
| Interpretation versus factual assertion | Evidence и тип не подменяются; confidence не identity/truth proof |
| Qualified claim, hook убрал qualifier | Правильные SHA/provenance не делают формулировку допустимой; требуется revision/review |
| Unreviewed/malformed ClaimCheck | Null metadata/known evidence invariants по existing schema; missing SIRef INVALID, не научный STALE |
| Максимальный aggregate_tenths=1000, central unsupported или essential unknown rights | Existing BLOCKED, без threshold исключений |
| Optional material excluded vs essential без verified fallback | Явная новая revision; отсутствие hidden licensed default |
| Source/check revision сменились | Exact old review не переносится; accepted freshness, no rebasing |
| Current producer ERef / historical-only ERef | F1-D1 retained; отсутствие adapter не ложный CURRENT и не global audit-ERef rejection |
| All seven coverage areas justified на synthetic data | Не создаются scientific approval/production permission; label остаётся untrusted |
| Private review metadata и ru/uk qualifiers | Нет нового экспортного права, hidden field path или silent translation |

**NOT RUN — DOCS ONLY.** Независимые oracles/golden vectors/new runtime tests ещё
не создавались. Детали profile/coverage/capture остаются PROPOSAL до отдельного
owner approval; production implementation NOT AUTHORIZED. SI-E02.2 не начинать.
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. STOP для independent review.
