# SI-E02.0 — Owner decision proposal for SI-E02.1

Дата: 2026-11-10 (Europe/Kyiv). **PROPOSAL / OWNER REVIEW — НЕ УТВЕРЖДЕНО.**
Base: `9a631ebca2bccdd8e0157528b20080380ba8dcfe`.
Это вопросы/варианты следующего этапа, **не начало SI-E02.1**, не новый wire contract
и не разрешение SI-E02.2. Основание: [inventory](STORY_INTELLIGENCE_SI_E02_0_ARCHITECTURE_INVENTORY.md),
[gap matrix](STORY_INTELLIGENCE_SI_E02_0_CONTRACT_GAP_MATRIX.md),
[Planning Proposal](STORY_INTELLIGENCE_SI_E02_PLANNING_PROPOSAL_2026_11_10.md).

Уже решены и повторного approval не требуют: девять SI-D04 criteria/веса, UNKNOWN
не 0, blockers before scores, human intent не authority, существующий SI ProductionBrief,
G01/G02/F1-D1 freshness, ru/uk wire locales, independent rights/release gates.
Документ не предлагает ослабить их. Ниже — только оставшиеся product/contract choices.

## E02-P01 — A. Topic Scoring: сравнение и приоритизация

Основа: [SI-D04 approval](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md),
[R1 §3](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md), existing Rubric/EvaluationReport.
Оценка — explainable human/rule heuristic, не объективный факт или прогноз успеха.

| Вариант | Преимущество | Риск/последствие |
| --- | --- | --- |
| 1. Сначала criterion-by-criterion comparison; authored ratings, existing aggregate только при всех KNOWN ratings; человек задаёт приоритет | Повторно использует schema/веса, показывает evidence/confidence/UNKNOWN | Не даёт автоматической очереди и не устраняет субъективность judgment |
| 2. Дополнительно проектировать автоматический cross-candidate rank/tie policy | Удобно сравнивать большой список | Нужны approved comparability/ordering rules и oracle; unknown/context differences могут дать ложную точность |

**Рекомендуется 1 для первого ограниченного шага.** Не менять веса, не изобретать
threshold. Наличие aggregate не снимает UNKNOWN confidence/evidence или blockers. Если выбран 2, сравнение допустимо только при определённой одинаковой
Rubric/method и совместимом audience/channel/context; blockers и incomplete scores
не компенсируются aggregate, ties не разрешаются скрытым временем/UUID.
Без выбора остаются заблокированы automatic ranking/priority executor; хранить
объяснённые ratings в существующих типах уже можно на уровне data validation.

## E02-P02 — B. Editorial Authority: нужен ли durable topic intent

Основа: R1 §4.1 Selection допускает exact CreativeAlternative/ProductionBrief,
не StoryIdea; [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md)/[O1–O10](E01_3_8_1_APPROVED_CONTRACT.md)
относятся к editorial SCRIPT/SCENES/HANDOFF. SI evaluator не получает их полномочий.

| Вариант | Преимущество | Риск/последствие |
| --- | --- | --- |
| 1. Пока оставить topic research choice вне persisted SI decision; применять только существующие Creative/Brief selections позже | Нет schema changes, быстрый advisory путь | Нет durable evidence выбора/отклонения/приоритета самой темы |
| 2. Заказать отдельный узкий proposal для человеческого topic intent на базе existing identities | Закрывает реальную потребность отбора темы и exact revision binding | Потребует owner-approved scope/operation extension и lifecycle; это не existing SI Selection и не editorial APPROVE |

Если продукт должен сохранять **решение именно о теме**, рекомендуется **2 как
проектирование отдельного proposal**, а не немедленное добавление типа. Сначала
доказать minimum extension existing Selection semantics; новый параллельный Approval
не нужен. Авто-APPROVE/reviewer identity по label запрещены в обоих вариантах.
Без решения durable topic reject/priority заблокированы. Queue/assignee/deadline/
assignment ack не включать по умолчанию; это отдельная operational потребность.
До durable записи также нужен concrete SI-D03 lifecycle contract.

## E02-P03 — C. Production Brief: граница следующего deliverable

Тип выбирать заново не требуется: existing ProductionBrief уже содержит нужные
pre-script данные; editorial BriefValue — другое, вложенное значение. Основа —
[R1 §2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md), [R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md).

| Вариант | Преимущество | Риск/последствие |
| --- | --- | --- |
| 1. Existing SI Brief + private human-reviewable card; downstream пока ручной editorial draft workflow | Нет дублирующего Brief wire; сохраняются provenance и границы прав | Нет автоматического переноса или задания исполнителю |
| 2. Сразу приоритизировать отдельный SI→editorial/production-assignment contract | Ближе к сквозной передаче | Нельзя выразить machine Candidate происхождение manual discovery_method; нужен отдельный mapping/authority/readiness contract, protected writer недоступен |

**Рекомендуется 1.** Owner choice — целевой consumer и порядок работ, не re-approval
существующего типа. Structured private Brief не является render plan/job/разрешением
публикации. Без отдельного решения по 2 automation handoff и assignment остаются
заблокированы; нельзя скрывать payload/run metadata в rationale/reason.

## E02-P04 — D. Freshness & Provenance: порядок интеграции ERefs

Основа: [G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md),
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md),
[final acceptance](STORY_INTELLIGENCE_SI_E01_2B_3_FINAL_ACCEPTANCE_2026_11_10.md).
Правила exact refs и INVALID/STALE/CURRENT уже приняты; голосование за rebasing не предлагается.

| Вариант | Преимущество | Риск/последствие |
| --- | --- | --- |
| 1. Первый bounded deliverable использует unbound local SI drafts/ERef-free fixtures; adapter отдельным этапом | Повторно использует accepted pure APIs, не зависит от Windows service | Реально ERef-bound records без validated snapshot остаются INVALID; это не production clearance |
| 2. Сначала отдельный read-only exact editorial snapshot adapter contract | Позволит проверять реальные editorial bindings | Дополнительная identity/hash/coverage/current-observation boundary; сейчас adapter не реализован/не разрешён |

**Рекомендуется 1, затем отдельно согласованный 2.** Нельзя очищать или заменять
существующие ERefs ради CURRENT, принимать UNKNOWN/hash как validated snapshot,
выбирать latest или заново писать принятый resolver. Без решения adapter path остаётся
закрыт; pure consistency supplied SI bundles остаётся доступной без native storage.

## E02-P05 — E. Rights & Evidence: science review coverage следующего контракта

Основа: original §5/§7, R1 §3.2/§4, SI-D05/06/07 и действующие
[license unresolved items](../../LICENSES/UNRESOLVED_ITEMS.md),
[release checklist](../../LICENSES/RELEASE_COMPLIANCE_CHECKLIST.md),
[voice gate](../../COMMERCIAL_VOICE_LICENSE_GATE.md). Базовые evidence/rights blockers
обязательны, бездоказательная «готовность» не является вариантом.

| Вариант | Преимущество | Риск/последствие |
| --- | --- | --- |
| 1. Сначала общий evaluator/selection contract по approved базовым blockers; human review coverage явно перечисляется | Повторное использование ClaimCheck/Risk/required_reviews | Предметная scientific adequacy останется человеческой ответственностью, без обещания expert verification |
| 2. Дополнительно заказать science-specific review profile/checklist до разрешения таких production briefs | Явные проверки терминов, датировок, counter-evidence, qualifications и legal intended-use | Нужны owner-defined coverage/escalation criteria; нельзя выдумать универсальное «2 источника = истина» или trusted expert role |

Для научно-популярного примера рекомендуется **2 как отдельное уточнение требований**,
без новых approval/grant wire типов в E02.0. Нужен выбор mandatory scientific review
coverage, а не разрешение проигнорировать existing blockers. Непроверенный central
claim либо essential material без прав/fallback остаётся BLOCKED при любом score.
До решения нельзя обещать научную production readiness; research card допускается
только с явными gaps, без SELECT/APPROVE и без раскрытия приватных raw данных.

## Конкретный пример: «Почему исчезли древние цивилизации?»

**ILLUSTRATIVE / НЕ ПРОВЕДЁННОЕ ИССЛЕДОВАНИЕ / НЕ WIRE FIXTURE.**
Ни records, ни SIRefs, ни сценарий, ни production job здесь не создаются. Ниже
Topic Candidate/Research/Editorial Decision — названия стадий представления,
не новые RecordTypes; условные I/Q/S/E/K/B — planning labels, не допустимые SIRefs.

**Вход карточки.** Русский язык (`ru`), научно-популярный стиль, 8–12 минут
(480–720 s), BALANCED. Audience hypothesis: русскоязычный взрослый зритель без
специальной археологической подготовки, интересующийся проверяемыми объяснениями.
Это **явное предположение**, не approved channel/audience setting; возрастной
диапазон, регион, analytics и portfolio UNKNOWN. Цель — научиться различать
наблюдение, объяснение и ограничения данных, а не получить универсальную причину.

**Центральный вопрос:** что именно исчезло — город, политический порядок, язык
или население — и какие данные позволяют это различить? Angle: сравнить понятия
и конкурирующие объяснения в одном проверенном кейсе, второй добавить только если
есть сопоставимые evidence. Майя/поздняя бронза — возможные направления research,
не утверждённые selected cases, факты/даты/обобщения здесь не приписываются.

| Стадия | Existing data / planned работа | Честный результат сейчас |
| --- | --- | --- |
| Topic Candidate | Intake + StoryIdea: тема, viewer_question, source refs Known/UNKNOWN | Есть только conceptual input, Discovery не выполнен |
| Research/Evidence | SourceItem → ClaimItem/EvidenceItem/ClaimCheck; найти academic terminology review, региональные исследования и counter-evidence с exact locator/material rights | Авторы/версии/URL/страницы/hashes UNKNOWN; references не выдумываются |
| Evaluation | Existing Rubric/EvaluationReport: все девять критериев, basis/confidence; проверить central claims и essential rights | Ratings/aggregate UNKNOWN; ожидаемый policy outcome BLOCKED, не вызванный evaluator result |
| Editorial Decision | Человек сначала выбирает scope research/сужение темы; после доказательств — выбор exact Creative/Brief по approved scopes | Ни topic APPROVE wire, ни SELECT готового Brief, ни editorial gate не создан |
| Production Brief | Existing B: exact idea/audience/channel/angle/E/K, source/claim/check/visual/risk refs, длительность/intensity/locales/options/reviews | Пока working discussion card с unresolved inputs, не valid recorded Brief/handoff/job |

**Hooks — варианты framing, не полный сценарий:**

1. QUESTION: «Что должно исчезнуть, чтобы мы сказали: цивилизация закончилась?»
2. HUMAN_STAKES: «Представьте, что знакомый город меняется до неузнаваемости.
   Исчезла ли жизнь людей — или привычный нам порядок?» Явный мысленный пример,
   не документальная реконструкция.
3. COUNTERINTUITIVE: «А если слово “исчезла” скрывает несколько разных историй?
   Проверим, где данные, где объяснение и где остаётся спор».

0–30 s — qualitative hypothesis: короткий вопрос → различение понятий → обещание
проверки альтернатив. Не измеренный retention и не прогноз viral probability.
Title options: «Что значит “исчезла цивилизация”?» / «Как проверять объяснения древних перемен».

| Глава / цель | Target s, не WAV timing | Визуальный приоритет |
| --- | --- | --- |
| Уточнить вопрос | 30 | LOCAL типографика: город / власть / люди |
| Разделить термины и критерии | 60 | REQUIRED собственная схема после проверки терминов |
| Показать, какие данные нужны | 90 | LOCAL таблица источник / вывод / неизвестное |
| Один выбранный после research кейс | 120 | REQUIRED lawful карта/хронология по проверенным данным |
| Конкурирующие объяснения | 120 | LOCAL сравнительная схема, без придуманных измерений |
| Второй кейс либо углубление первого | 120 | OPTIONAL museum image только после rights review; иначе содержательный lawful fallback |
| Границы вывода | 60 | LOCAL сводка Known/UNKNOWN и qualifications |

Всего 600 s target внутри 480–720 s; это не готовый script/scene plan.
Q1 — рабочая central hypothesis: политическая перемена не обязательно равна
исчезновению населения **в выбранном кейсе**. Q2 — сравнимость разных объяснений.
Обе требуют точных источников, counter-evidence и human review; supported/qualified
сейчас не присваиваются. Точные SourceItem hashes/locators и material permissions
будут получены отдельно, не из текста этого примера.

Основные риски: scientific — universal cause/неверные термины; evidence — central
claims unreviewed; legal — карта/музейные изображения/fonts без clearance;
production — essential visual fallback ещё не проверен; reputational — sensational
hook; market — novelty/competition неизвестны. Высокий интерес не снимает blockers.
Возможный CPU-only путь — lawful local WAV + собственные still/text diagrams;
название голоса/наличие FFmpeg не даёт licence/permission. Формат и конкретные assets
ещё не выбраны. Brief должен перечислить scientific/rights/language/capability reviews,
must_avoid и unresolved; currentness не вычислялась, approved gate/передачи в производство нет.

## STOP

Владельцу предлагается выбрать P01–P05, после review — отдельный точный scope/SHA
для следующей стадии. SI-E02.1/E02.2, код, схемы, UI, providers, ERef adapter,
persistence/assignment не реализуются этим proposal. `PUBLISH_REVISION` DISABLED;
partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
