# SI-E02.2.1b — Frozen findings contract and implementation boundary

Дата: 2026-11-10. **DOCS ONLY / IMPLEMENTATION NOT AUTHORIZED.**
Base: `78285d35e7a816dd9f98430613a518ee1dda90c1`.
Нормативное решение: [OWNER_APPROVAL](STORY_INTELLIGENCE_SI_E02_2_1B_OWNER_APPROVAL_2026_11_10.md).
Exact approved sources на этом base:
[findings contract](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md) и
[42 test requirements](STORY_INTELLIGENCE_SI_E02_2_1A_TEST_ORACLES.md).
Ниже — границы handoff, не новые classifier policies и не реализация.

## 1. Что закрыто и что остаётся отдельным

| Категория | Binding requirements | Implementation impact |
| --- | --- | --- |
| APPROVED PURE FINDINGS CONTRACT | EVAL-P01–P04: closed local structure, exact roots/context/ratings/entry bindings, exhaustive portfolio, missing/conflicting behavior, mappings/order | Не требуется повторное архитектурное решение по confidence consideration/duplicate coverage; код писать только после отдельного resume handoff |
| EXISTING ACCEPTED SI/1 REQUIREMENTS | Original + R1/R1a/R1b, SI-D04, accepted resolver/provenance/currentness, exact graph/hash/locale/previous checks | Reuse, не копирование/изменение accepted modules; dictionary shape не proof valid bundle |
| REMAINING BASE-CLASSIFIER DETAILS | Полные executable predicates и independent literal outcomes для остальных base conditions, в том числе T25 | Exact implementation там, где approved rules однозначны; при material ambiguity — clarification, без invented defaults |
| DEFERRED EVAL-P05 | Request bytes/envelope/request_payload_sha256/request_id/replay/operation version integration | Только outer command integration; не блокирует pure no-request evaluator |
| FORBIDDEN CHANGES | Новые SI records/wire fields/operations/dependencies, изменение accepted code/contracts/vectors, persistence/authority/providers | В текущем docs этапе запрещён любой runtime; будущий allowlist отдельно |

Missing required finding приводит к соответствующему research/pair-review gap,
не к отказу graph validation. Wrong digest/ref/shape/conflicting findings — INVALID.
INVALID приоритетнее STALE. Missing **exact SIRef** — REF_MISSING, не человеческая
неопределённость. No SUFFICIENT/DISTINCT снимает другие risks/rights/research conditions.

Literal `si-evaluate-findings/proposal-1` сохраняется в local value. Не переименовывать
его при реализации из-за исторического названия source proposal. Не добавлять H,
SIRef, Request option или Run/EvaluationReport field для findings. Privacy/export и
durable capture не следуют из approved local argument.

## 2. Неизменный base scoring и validation

[R1 §3.2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) и
[original rubric](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md) задают девять keys/weights:

| key | weight_percent |
| --- | ---: |
| audience_interest | 15 |
| channel_fit | 10 |
| angle_novelty | 10 |
| evidence_quality | 20 |
| narrative_potential | 15 |
| visual_feasibility | 10 |
| resource_fit | 10 |
| risk_manageability | 5 |
| portfolio_distinctness | 5 |

Все ratings 0–5. Только все KNOWN → aggregate_tenths=2×Σ(weight×rating), диапазон
0–1000; любой UNKNOWN → aggregate UNKNOWN. Нет zero-fill, weight renormalization,
score threshold, automatic ranking/approval или viral prediction. Values/basis_refs/
explanation/confidence сохраняются; engine не выдумывает ratings/evidence.

Использовать принятые validators, resolver, provenance и currentness. Root/graph/
hash/type/cycle/provenance/locale/invalid context failures исключают accepted current
output. Expected-context mismatch и valid changed dependencies не исправляются latest.
EVALUATE не требует будущих Creative/Selection/Brief; existing unrelated head change
может дать expected-context STALE без добавления новой semantic dependency Evaluation.

[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md) отделяет audit
ancestry от required-current; [G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md)
сохраняет original CREATIVE direct ClaimItem constraints;
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md) сохраняет actual
current producer и original C relevant ERefs. Relevant unresolved ERef без exact validated
snapshot → INVALID/REF_MISSING, даже вместе со STALE root. Historical-only ERefs не
становятся relevant только из-за audit Closure. Findings эти правила не меняют.

## 3. Remaining base-classifier detail register

Эти BC IDs — documentary references, не wire/error codes. Таблица различает
реализацию уже заданной нормы и необходимость clarification, если точного вывода
из accepted contracts нет. Это **не** заявление, что каждая строка — новый дефект
архитектуры или требует нового owner decision перед любым вычислением.

| ID / область | Уже обязательная норма | Что требуется в bounded resume specification/tests | Реальный блокируемый путь при отсутствии точности |
| --- | --- | --- | --- |
| BC01 Essential claims/evidence | Missing/disputed/unsupported central factual claim блокирует; qualifiers/human review не обходятся score | Exact claim/check/evidence role coverage, соответствие refs и treatment применимых reviewed states; достаточность human premises не выводить из количества URL или nonempty Text | Claim-based base eligibility; при неоднозначном выборе authoritative check/coverage нужен отдельный вопрос, не latest |
| BC02 Risks/rights/capability | Открытые blocking scientific/legal/ethical/rights/capability risks → BLOCKED; lawful verified fallback/mitigation не возникают из описания | Exact применимые Risk/Visual/source inputs, state predicates и existing code/path mapping; не вводить новые severity thresholds/автоматический clearance | Соответствующие blocker branches; approved findings сами их не реализуют |
| BC03 Framing/required current input | Недостаточная постановка/audience/channel/required current data → NEEDS_INPUT; broken refs/schema → INVALID, changed valid context → STALE | Какие supplied values означают semantic shortage, а какие ошибка; требование current-data не угадывать по строке/clock/network | NEEDS_INPUT classifier и полная concrete T25 premise |
| BC04 Other research/freshness | Остальные missing evidence/locators/freshness → NEEDS_RESEARCH; UNKNOWN не 0/known empty | Проверяемые predicates и explicit human/data premises для adequacy/freshness; если значение Text не определяет решение, не добавлять magic words/default expiry | Только соответствующие research branches; findings confidence/portfolio уже определены EVAL-P02/P03 |
| BC05 Complete output/diagnostics oracles | R1 precedence, all applicable reasons, existing code vocabulary; findings diagnostics уже frozen | Для base conditions зафиксировать code/path/message/complete expected outcome до вызова engine; string wording — routine implementation choice, но отсутствующий semantic code mapping нельзя выдать за утверждённый | Полный independent base oracle/T25; не arithmetic и не approved findings validation сами по себе |
| BC06 Pure call boundary | Только явные exact local inputs; no clocks/random/provider/writes/authority | Exact pure API/result shape и root roles в рамках allowlist, detached values, no fabricated Run/Report metadata; не расширять область до operation writer | Публикация executable pure API до отдельного bounded task; не требуется EVAL-P05 для no-request call |

BC01–BC04 не разрешают создать новый generic policy record, conditions wire schema,
LLM classifier или фальшивый human review. Если значения однозначно определяются
approved rules, это implementation work, не причина останавливаться ради формальности.
Если точного поведения действительно нет, представить минимальный valid graph,
расходящиеся outcomes и узкий вопрос владельцу; не выбирать произвольную политику.

Никаких решений BC01–BC06 в этом документе не принимается сверх existing contracts.
Approval 42 сценариев не превращает общие premises «framing достаточно» или
«открыт blocker» в полный алгоритм извлечения этих условий из произвольного Text.

## 4. Oracle freeze and limitations

Нормативны все **N01–N04 (4) + T01–T38 (38) = 42** requirements на exact source,
включая fixture discipline, nonmutation/determinism и declared limitations.
Часть rows содержит несколько subcases: 42 — число требований, не будущий точный
unittest count и не доказательство исполнения.

- N01–N04 фиксируют 0/1000/510/UNKNOWN без использования evaluator как oracle.
- T01–T24/T26/T28–T38 применяются в stated scope; ограничения G01/G02/F1-D1 и pure roots сохраняются.
- T25 требует сохранения all applicable base reasons/precedence, но **не complete literal oracle** classifier. BC01–BC05 должны дать exact premises/outputs для полноценного independent теста.
- T27 — условное future Request requirement, **не executable requirement текущего pure evaluator**. Не создавать request wrapper только ради PASS этого row; EVAL-P05 остаётся OPEN.
- Existing G01/G02/F1-D1 и все accepted golden vectors неизменны. Новые literal fixtures следует независимо построить и заморозить в будущем implementation task; сейчас hashes/records не выдумываются.

Ни один из 42 cases этим approval не запущен. Нет engine readiness, scientific truth,
rights, authenticated identity или native Windows qualification claims.

## 5. SI-E02.2.1-RESUME preconditions

1. Independent review этой docs ветки; отдельный явный owner handoff на exact SHA,
   новая feature branch и минимальный code/test/result allowlist. Текущий этап
   **не** создаёт RESUME task и не разрешает код.
2. Handoff использует frozen EVAL-P01–P04 и 42 requirements с исходными limitations;
   exact pure inputs/outputs и supported condition coverage описаны проверяемо.
3. Там, где BC register требует только exact implementation, применить existing
   нормы и independent tests. Если обнаружена material contract ambiguity, сначала
   минимальный reproducer/clarification/owner decision; нет fake default или обхода.
4. Независимые genuine content-addressed fixtures, explicit literal ожидаемые
   scores/eligibility/reasons, positive/negative findings и accepted graph checks;
   no mocked hash/provenance success. Target/full tests с фактическими exit codes.
5. Pure no-request scope: нет Request/operation changes, persistence/replay/Run writer,
   fabricated UUID/time, provider/LLM/network/GPU, automatic ranking/authority или
   production handoff. Exact refs/locale/provenance и nonmutation обязательны.

SI-D03 persistence, Topic Intent, Scientific Review automation, ERef adapter для
ERef-free inputs, editorial production handoff и Windows protected writer не
prerequisites bounded pure evaluator. Не удалять existing ERefs, чтобы назвать
путь ERef-free. Native host не нужен для pure Linux/Python tests и не квалифицируется ими.
EVAL-P05 блокирует только request/persistent command integration, а не no-request call.

## 6. STOP and compatibility

No new SI records/wire fields/operations/dependencies. Existing EvaluationReport,
RunRecord, field order, canonical hash, exact refs/provenance и E00/A/O/storage contracts
unchanged. RU/UA wire `ru/uk`, CPU-only fallback и licensing constraints сохраняются.
**Unit tests: NOT RUN — DOCS ONLY.**
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes.
**STOP. SI-E02.2.1-RESUME не начинать.**
