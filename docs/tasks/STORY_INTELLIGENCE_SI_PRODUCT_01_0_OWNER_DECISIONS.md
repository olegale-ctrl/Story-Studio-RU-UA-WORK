# SI-PRODUCT-01.0 — Owner decision register

Дата: 2026-11-13. **PROPOSAL / NOT APPROVED.**
Ни одно новое решение ниже ещё не утверждено. Подготовка четырёх документов и
исправление base не являются approval дизайна или authorization реализации/push.
[Contract](STORY_INTELLIGENCE_SI_PRODUCT_01_0_CONTRACT_PROPOSAL.md),
[proposed oracles](STORY_INTELLIGENCE_SI_PRODUCT_01_0_TEST_ORACLES.md).

| Decision / status | Recommendation | Alternative / consequences | Acceptance condition |
| --- | --- | --- | --- |
| PD-01 — **PROPOSAL / NOT APPROVED** | Exact invocation inputs+result; verify association повторным pinned pure evaluator call, refuse mismatch без replacement | Trusted same-invocation handoff возможен только с отдельно определённой trust boundary. Произвольный detached dict не имеет input binding. Повтор проверки дороже; performance пока не квалифицирована | Explicit owner choice; P26/P29–P31, no new Request/receipt/hash field, no evaluator changes |
| PD-02 — **PROPOSAL / NOT APPROVED** | Private local Card с пятью sections, DISPLAYABLE/UNAVAILABLE; strict actual OK vs Rejected shapes | Неструктурированный текст проще, но труднее проверить полноту. Все schemas/enums presentation-only; SI/1 неизменен | Утвердить closed Card/admission failure, P01–P10/P26–P27; missing input не fake evaluator status |
| PD-03 — **PROPOSAL / NOT APPROVED** | Explicit display_locale ru/uk независимо от evaluator locale; фиксированный полный bilingual dictionary; no fallback | Только язык evaluator ограничит usability INVALID(locale=null). Автоопределение/перевод не рекомендуется и не разрешено | Owner review обеих literal translations; P27–P28/P37–P38; evaluator ui_locale/context не меняются |
| PD-04 — **PROPOSAL / NOT APPROVED** | Exact integer n из/із1000 либо unknown string; никогда probability/threshold/production signal | Полностью скрывать score допустимо как другое owner решение; percentages/ranking требуют иной контракт и не предлагаются | P01/P03/P06/P12/P41; подтверждение absence-of-gap wording, no fabricated positive reasons |
| PD-05 — **PROPOSAL / NOT APPROVED** | Closed 30-family catalog с exact path/typed subject/fixed message matching, separate validation explanations | Code-only translation теряет различие BLOCKED/NEEDS_INPUT/NEEDS_RESEARCH у EVIDENCE_NEEDED. Free-form translation может раскрыть private content и выдумать причины | Owner approve catalog coverage/strings; P13–P25/P31/P35, no new reason code/condition/classifier |
| PD-06 — **PROPOSAL / NOT APPROVED** | Preserve all diagnostic slots/order; one explanation/gap/action per slot; no top-N/dedup by text | Short summary может скрыть lower-priority blockers/gaps. Pagination/aggregation только отдельным future display contract с доказательством losslessness | P16–P24/P40 и полный W01 RU/UK; no decision recomputation or automatic jobs |
| PD-07 — **PROPOSAL / NOT APPROVED** | Generic per-type aliases by first diagnostic occurrence; no titles/URLs/labels/reviewer/reason text/raw technical fields | Имена источников полезнее, но требуют exact display grants/retention/redaction contract. Generic labels ограничивают usability и не обеспечивают anonymity/public export | P32–P36/P39; review privacy trade-off, no new approval/persistence/public sharing implied |
| PD-08 — **PROPOSAL / NOT APPROVED** | Six fixed limitations always; advisory creative eligibility distinct from scientific/rights/editorial/production authority | Убирать limitations ради компактности нельзя без нового owner решения; external approvals не объявлять missing/present по умолчанию | P41–P42, W01 и no invented findings/hooks/assets/Brief; SR principles сохранены |

Все восемь рекомендаций требуют явного решения владельца; отсутствие ответа не approval.
Они образуют согласованный proposed V1: выбор alternative требует пересмотра связанных
орacles до реализации. Если owner меняет язык/card fields/capture, это не разрешение
самостоятельно менять evaluator или существующие утверждённые контракты.

## Existing decisions that this register does not reopen

SI-E02.1 P01–P05 и TI-P01–P06/SR-P01–P04 утверждены в своих исходных пределах.
EVAL-P01–P04, RC-P01–P06, Q1–Q3/F1-D1/G01/G02 неизменны. Девять criteria/weights,
UNKNOWN completeness, source temporal inclusion, explicit context/currentness и
provenance не пересматриваются. Рекомендации next actions — текст для человека,
не внедрение TOPIC_INTENT wire operation, scientific checklist completion либо writer.

Никакого approval scientific truth, reviewer authority, rights clearance, actual
asset/CPU availability или production readiness. Exact missing data/error не становится
ordinary research gap ради более дружелюбного текста. Предлагаемый presentation
failure не подменяет existing evaluator INVALID/STALE.

## Deferred, not silently added to V1

- Approved display grants для human-friendly source titles/labels и external export.
- UI design, pagination, accessibility delivery, private persistence/retention и logging.
- Trusted invocation integration/оптимизация verification cost после explicit choice PD-01.
- Реализация projection и её independent acceptance; только последующее отдельное задание.
- Topic discovery/research/Creative/ProductionBrief consumer и execution integrations.

EVAL-P05 OPEN; PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. **STOP FOR INDEPENDENT REVIEW.**
Никакой push/PR/merge/tag/release или implementation этим register не разрешён.
