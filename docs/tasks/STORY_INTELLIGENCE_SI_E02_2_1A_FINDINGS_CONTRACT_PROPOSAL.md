# SI-E02.2.1a — Non-persisted human findings contract proposal

Дата: 2026-11-10. **PROPOSAL / NOT APPROVED / NOT IMPLEMENTED.**
Base: `24cbe823574489f7f7450af1a662203a164efbcf`.
Только [EVAL-D01–D03](STORY_INTELLIGENCE_SI_E02_2_1A_OWNER_APPROVAL_2026_11_10.md)
нормативны. Все поля, enums и правила ниже — конкретная рекомендация для отдельного
review. Ни нового SI/1 wire schema, persisted record, operation envelope, transport,
права или public API текущей библиотеки этим документом не вводится.

## 1. Граница и существующие types

Предлагается один обязательный caller-supplied plain-value argument будущей pure
функции. Он существует только во время вызова; не получает H/SIRef, не записывается
в RunRecord/EvaluationReport, не прячется JSON в reason и не порождает Selection.
Caller обеспечивает явное человеческое решение. Pure verification не доказывает
личность, фактическое чтение, научную истину, компетенцию или права. SHA — binding,
не подпись: владелец недоверенного workspace может переписать все значения.

Reuse без изменений: [SI/1/R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md)
Text, Hash, SIRef, ContextSnapshot, Rating; [records](../../story_intelligence/records_v1.py),
[codec](../../story_intelligence/codec_v1.py), [resolver](../../story_intelligence/resolver_v1.py),
[provenance](../../story_intelligence/provenance_v1.py), [currentness](../../story_intelligence/currentness_v1.py).
Text — непустой exact Unicode; Hash — 64 lowercase hex; index — plain int≥0, не bool.
Objects plain dict, arrays plain list; все поля required, без coercion/unknown fields.
Текущие canonical limits применяются к каждому хэшируемому plain value; новых квот
или bundle limits не предлагается. Hash inputs не содержат будущий output/run.

## 2. Предлагаемая закрытая структура — EVAL-P01

Нотация ниже — локальный value contract, **не JSON wire registration**.

```text
HumanFindingsInput = {
 contract_tag: "si-evaluate-findings/proposal-1",
 binding: EvaluationBinding,
 confidence_findings: List<ConfidenceFinding>,
 duplicate_findings: List<DuplicateFinding>
}
EvaluationBinding = {
 idea_ref: SIRef<StoryIdea>, angle_ref: SIRef<Angle>,
 audience_ref: SIRef<AudienceHypothesis>, channel_ref: SIRef<ChannelContext>,
 rubric_ref: SIRef<Rubric>, semantic_input_refs: List<SIRef>,
 context_snapshot: ContextSnapshot, ratings_sha256: Hash
}
ConfidenceFinding = {
 binding_sha256: Hash, criterion_key: Text, rating_sha256: Hash,
 outcome: SUFFICIENT | INSUFFICIENT, reason: Text
}
DuplicateFinding = {
 binding_sha256: Hash, portfolio_entry_index: Int0Plus,
 portfolio_entry_sha256: Hash,
 candidate_ref: SIRef<StoryIdea|ProductionBrief>,
 outcome: DISTINCT | DUPLICATE | UNRESOLVED, reason: Text
}
```

Закрытые local enums: tag ровно как выше; confidence ровно SUFFICIENT/INSUFFICIENT;
duplicate ровно DISTINCT/DUPLICATE/UNRESOLVED. criterion_key — ровно один из девяти
approved SI-D04 keys, не произвольная строка. No reviewer credential, permission,
request_id, time, UUID, signature или confidence replacement field.

`binding` должен byte-for-byte по C совпасть с одноимёнными explicit evaluation
arguments и frozen expected ContextSnapshot; не назначает observed context.
`semantic_input_refs` — полный явно переданный ordered список roots **этого вызова**,
включая relevant claim/check/source/risk/visual roots при наличии. Не только пять
основных refs. Exact roots сравниваются буквально, без сортировки/dedup/autofill.
Новый Run builder order здесь не утверждается: будущий persisted operation contract
остаётся вне scope. Resolver Closure — отдельный canonical set, не этот массив.

Существующие Angle.idea_ref/audience_ref и ChannelContext.audience_ref должны
совпасть с соответствующими binding refs; конфликт — INVALID/REF_TYPE_MISMATCH
для wrong role либо INVALID/PROVENANCE_MISMATCH для несовместимых exact bindings.
Ни совпадающий label/id, ни latest не заменяют full SIRef.

## 3. Frozen binding и изменения — EVAL-P01

`C` — existing SI canonical JSON, `D(x)=SHA256(C(x))` без нового separator/domain.
Это локальные контрольные digests, не изменение existing record hash protocol.

- `ratings_sha256 = D(всего supplied ordered List<Rating>)`.
- Каждый `rating_sha256 = D(полного соответствующего Rating)`; включены key/value,
  basis_refs в исходном порядке, explanation и confidence.level/basis.
- Каждый `binding_sha256 = D(полного EvaluationBinding)`; связан весь context,
  roots, Rubric и все ratings, не только один criterion.
- `portfolio_entry_sha256 = D(ChannelContext.payload.portfolio.value[index])`;
  включает story_ref, title, locator, date, angle_notes и basis_ref.
- `candidate_ref` обязан точно равняться entry.story_ref, index находится в KNOWN
  portfolio exact channel_ref. Запрещены index lookup в другом Channel или title-only match.

Каждое изменение StoryIdea/Angle/Audience/Rubric/Channel/root/context/ratings требует
нового соответствующего human input; findings не переносятся автоматически. Даже
изменение explanation/confidence basis или порядка ratings/root arrays существенно.

Различать два случая:

1. Binding внутренне соответствует genuine старым refs/ratings/context, но explicit
   expected/observed context сменился → STALE/INPUT_STALE, нет current результата.
2. Finding digest не соответствует **переданным** bytes, candidate hash неверен или
   ref отсутствует → INVALID/REF_HASH_MISMATCH либо REF_MISSING; это не обычная STALE.
   Нельзя угадывать, был ли это старый finding или подделка. Malformed hash → TYPE.

Внутренне целый binding с другими exact refs, чем explicit arguments текущего вызова,
после graph проверки даёт STALE/INPUT_STALE; с неверными typed role/ref bytes — INVALID.
Не чинить digest, не перепривязывать автоматически и не принимать один положительный
finding как доказательство актуальности остальных roots.

## 4. Полнота human findings — EVAL-P02 и EVAL-P03

### Confidence

Одна запись для каждого Rating с confidence.level=UNKNOWN, в approved Rubric order.
Для известных confidence findings запрещены (INVALID/TYPE); это не механизм смены
LOW/MEDIUM/HIGH. SUFFICIENT означает только human consideration неопределённости.
INSUFFICIENT добавляет research gap. Missing required confidence finding также
предлагается трактовать как NEEDS_RESEARCH/EVIDENCE_NEEDED, а не implicit SUFFICIENT.
Это fail-closed по отношению к positive eligibility, **не** structural acceptance
отсутствующего mandatory поля: само поле confidence_findings required.

Rating.value=UNKNOWN остаётся UNKNOWN и требует NEEDS_RESEARCH независимо от
SUFFICIENT; aggregate остаётся UNKNOWN. UNKNOWN confidence не делает KNOWN rating
UNKNOWN и не меняет арифметику, но отсутствие consideration может остановить eligibility.
Run confidence не создаётся этой функцией: отдельный будущий harness не должен
выдавать per-rating finding за human consideration несуществующего Run metadata.

### Duplicate coverage

Рекомендация для первого bounded варианта: при KNOWN portfolio сравнить **каждую
entry** с exact current Idea+Angle. Expected pair set = все индексы 0..len−1 в
exact ChannelContext. Это сознательно консервативная proposed coverage policy,
а не утверждение, что все entries являются найденными duplicate stories.
Отдельного dedup executor, title normalization или caller-controlled shortlist нет.
Таким образом caller не может скрыть matching entry, передав пустой candidate list.

- DISTINCT снимает только duplicate gap этой exact pair; не research/rights/risk gaps.
- DUPLICATE оставляет REVIEW_DUPLICATE/DUPLICATE_REVIEW_NEEDED. Нет auto reject/merge.
  Это установленное человеком совпадение, но ещё не решение о дальнейшей разработке.
- UNRESOLVED и missing pair finding также оставляют REVIEW_DUPLICATE с тем же code.
- Для ELIGIBLE по duplicate ветке все expected pairs должны иметь DISTINCT.
- KNOWN empty portfolio: expected pair set пуст; это только local coverage, не
  доказательство глобальной novelty или отсутствии конкуренции.
- UNKNOWN portfolio: duplicate_findings должен быть пуст; NEEDS_RESEARCH/EVIDENCE_NEEDED,
  не «дубликатов нет». Индекс без KNOWN portfolio → INVALID/TYPE.
- Одна и та же exact candidate ref в разных entries проверяется по каждому индексу
  отдельно. Индекс и entry digest различают их; ничего не схлопывается по title/id.

Это не Topic Intent, не выбор StoryIdea для производства и не новый scientific profile.
Coverage всех entries требует отдельного owner approval EVAL-P03; альтернативный
bounded candidate detector/coverage attestation потребует своего точного контракта.
До выбора не реализовывать ни exhaustive policy, ни silent shortlist.

## 5. Validation и deterministic diagnostics — EVAL-P04

Предлагаемый порядок фаз; никаких positive eligibility до их завершения:

1. Shape всех explicit arguments/records, typed ratings/Rubric и local envelope,
   включая nested ref syntax, required fields, tag/enums/index type. Девять keys,
   approved order/weights и completeness обязательны. SI errors сохраняют accepted
   validator paths/order. Local fields проверяются в порядке §2, arrays по индексу;
   unknown local keys — sorted Unicode, затем missing fields в declared order.
2. Graph/type/hash/cycle и provenance всех explicit refs и refs из binding/findings
   через accepted APIs, включая previous и Run.input_snapshot. Shape ref проверен
   до lookup; missing/hash-corrupt ref не превращается в research gap.
3. Проверить KNOWN portfolio/index range, затем digest/candidate-entry equality,
   уникальность и порядок findings. Required
   bindings проверяются в порядке §2; затем confidence list и duplicate list.
   Один criterion_key либо portfolio_entry_index не может встретиться дважды:
   identical и contradictory duplicates → INVALID/TYPE по второму item. Повтор ключа
   проверяется до digest/outcome этого второго item; нет last-wins. После uniqueness
   проверить approved criterion order / ascending portfolio indices (иначе TYPE).
4. Проверить binding vs explicit call и frozen expected vs observed context;
   вызвать accepted currentness для соответствующих domain roots. Проверить все
   relevant roots до выбора результата: INVALID важнее STALE, включая unresolved
   ERefs. Domain semantic roles не переопределять; metadata roots проверяет graph,
   не передавать RunRecord как domain root в check_si_currentness.
5. Только для valid CURRENT inputs собрать все findings и остальные existing
   eligibility conditions; missing required finding не заменяет отсутствующий SIRef.
6. Применить R1 precedence к объединению условий, сохранить все relevant reasons.

При multiple fatal errors вернуть первый по phase/traversal order, сохраняя accepted
API diagnostics для SI bundle; no accepted result. На фазе 4 любая INVALID diagnostic
подавляет STALE независимо от порядка roots. При valid inputs собрать **все** eligibility
diagnostics, включая lower-priority reasons при BLOCKED/NEEDS_INPUT. Findings никогда
не используются при structural failure. Это не требование менять accepted validators.

| Условие | Existing code / proposed effect |
| --- | --- |
| Unknown/missing local field | UNKNOWN_FIELD / MISSING_FIELD, INVALID |
| Wrong enum/type/tag, index/order/duplicate key | TYPE; неподдерживаемый contract_tag → VERSION_UNSUPPORTED; INVALID |
| Missing/wrong type/hash SIRef; cycle; provenance; locale | REF_MISSING / REF_TYPE_MISMATCH / REF_HASH_MISMATCH / DEPENDENCY_CYCLE / PROVENANCE_MISMATCH / LOCALE_MISMATCH; INVALID |
| Binding/rating/entry digest mismatch | REF_HASH_MISMATCH, INVALID |
| Pair candidate differs from resolved entry.story_ref | PROVENANCE_MISMATCH, INVALID |
| Valid frozen binding/context outdated | INPUT_STALE, STALE; no accepted current evaluation |
| Required confidence absent/INSUFFICIENT, any UNKNOWN rating, UNKNOWN portfolio | EVIDENCE_NEEDED; research condition |
| Pair absent/DUPLICATE/UNRESOLVED | DUPLICATE_REVIEW_NEEDED; duplicate condition |
| Positive confidence/DISTINCT | Не добавляют code и не удаляют другие причины |

Diagnostic — existing {code,field_path,input_ref,message} value из R1, без нового
wire envelope. input_ref — relevant exact existing record либо null, не fake rating ref.
Local paths начинаются `$.human_findings`; rating paths — `$.ratings[i]`.
Missing consideration: `$.human_findings.confidence_findings`, input_ref=Rubric ref,
message называет criterion_key. Missing pair: `$.human_findings.duplicate_findings`,
input_ref=Channel ref, message называет index. Existing unsupported ERef diagnostic
сохраняется; findings не дают snapshot adapter.

Список reason_codes — unique sorted ASCII lexical union всех applicable existing codes.
Diagnostics unique по (code,field_path,C(input_ref),message), упорядочены по
(precedence class, code, field_path, C(input_ref), message exact Unicode codepoints).
Классы: BLOCKED, NEEDS_INPUT, NEEDS_RESEARCH, REVIEW_DUPLICATE; они не wire fields.
Не определять класс по одному code: классифицировать условие, code может совпадать.
Fields/keys перечисления не сортировать ради «починки» authored inputs; сортируется
только generated diagnostic list. Locale текста сохраняется, нет автоперевода.

## 6. Request bytes, идемпотентность и privacy — EVAL-P05

Pure call не имеет request_id/cache/replay/durability. Любые разные findings bytes
(даже только reason) — разные explicit inputs; повтор с теми же inputs даёт тот же
result. Два findings одного ключа внутри вызова — INVALID/TYPE независимо от reason.
Никакой «последний запрос победил», selection chain или timestamp ordering.

Если будущий persisted operation/harness имеет request_id, сохраняется R1 §6:
identical canonical Request bytes → historical replay; same id/different bytes →
REQUEST_CONFLICT. Чтобы findings реально участвовали в Request/request_payload_sha256,
нужно отдельно утвердить exact inclusion/mapping, не менять existing closed options
или исключать findings из request identity. Это блокирует **outer command integration**,
не проектирование/отдельную будущую pure функцию без request_id. Новых request bytes
или operation version здесь нет. Никакой replay map/persistence реализации.

Human reason может содержать private сведения; input не предназначен для логирования,
Run caveats, ReviewPacket/export либо отправки внешним сервисам. Durable capture,
privacy/retention и provenance фактического human action — отдельные contracts.

## 7. Неизменные boundaries и решения до реализации

[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md),
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md) unchanged.
Ни binding, ни positive findings не делают historical H.previous/current input_snapshot
required-current сами по себе. Exact audit/provenance graph сохраняется полностью.
Original CREATIVE direct claims/ERefs и actual current producer REVISION ERefs не
игнорируются; relevant ERef без exact validated snapshot → INVALID/REF_MISSING.
ERef-free путь означает отсутствие relevant ERef, а не удаление существующих refs.
Новых wire fields/error codes, implicit latest/rebasing или canonical hash changes нет.

| Решение, требующее отдельного approval | Recommendation | Какую реализацию блокирует |
| --- | --- | --- |
| EVAL-P01 Structure/binding | §2–3 closed local argument/full rating+context digests | Pure findings validator и использование findings |
| EVAL-P02 Missing confidence/fail-closed | §4: missing/INSUFFICIENT → research; conflicts → INVALID | Confidence eligibility branch |
| EVAL-P03 Pair coverage/outcomes | §4: exhaustive KNOWN portfolio; DUPLICATE/UNRESOLVED/missing → duplicate review | Duplicate eligibility branch; shortlist alternative тоже не утверждена |
| EVAL-P04 Diagnostics/validation order | §5 exact existing-code mappings/order, all eligibility reasons | Детерминированный complete pure result и тестовые ожидания |
| EVAL-P05 Outer request integration | §6 separate exact canonical Request inclusion contract | Только operation/harness с request_id; не pure no-request call |

[Test oracles](STORY_INTELLIGENCE_SI_E02_2_1A_TEST_ORACLES.md) — NOT APPROVED, NOT RUN.
Ни одно EVAL-Pxx не утверждено принципами EVAL-D01–D03 автоматически. После review
потребуется отдельный bounded implementation handoff. Нет SI-D03 writer/Topic Intent/
Scientific Review automation/ERef adapter для ERef-free inputs/editorial handoff/
Windows writer/network/LLM/GPU/provider prerequisites.
Девять SI-D04 criteria/weights, aggregate и SI/1 schemas/field order неизменны.
RU/UA wire `ru/uk`, CPU-only и licensing gates сохранены.
**Unit tests: NOT RUN — DOCS ONLY.** `PUBLISH_REVISION` DISABLED; partial COMMIT
reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
**STOP. Implementation NOT AUTHORIZED; без PR/merge/release/main changes.**
