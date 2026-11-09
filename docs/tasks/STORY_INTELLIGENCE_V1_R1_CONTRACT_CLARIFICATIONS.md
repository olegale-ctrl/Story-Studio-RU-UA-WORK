# Story Intelligence V1 — R1 Contract Clarifications

**PROPOSAL / AWAITING OWNER APPROVAL.** Дата: 2026-11-09 (Europe/Kyiv).
Документационное устранение SI-R01–SI-R03. Не approval архитектуры, не executable
schema, не разрешение программной реализации или запуска следующего этапа.

## 0. Provenance и точный приоритет

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-v1-independent-review`.
Exact base: `9ce417c81c532255185c200aebcff6cf628983a6`;
FETCH_HEAD и remote HEAD сверены с handoff до создания output branch.
Output: `docs/story-intelligence-v1-r1-contract-clarifications` (новая ветка,
без reset/force). Final HEAD сообщается в handoff, не встраивается в собственный hash.

Composite proposal состоит из:

1. [Исходной спецификации](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md) на
   `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412` (не изменена).
2. [Independent review](STORY_INTELLIGENCE_V1_INDEPENDENT_REVIEW.md) и
   [задания R1](STORY_INTELLIGENCE_V1_R1_CODEX_TASK.md) на exact base.
3. Настоящих замен только для перечисленных ниже clauses. **После принятия
   composite proposal владельцем** R1 имеет приоритет именно в этих местах.
   До этого оба документа остаются PROPOSAL; публикация не означает approval.

| Issue | Original clause / формулировка | Точная замена R1 | Сохраняется |
|---|---|---|---|
| SI-R01 | §2.1 Origin; §3 RunRecord.stage=DISCOVERY/EVALUATION/CREATIVE; §8 ASSEMBLE_BRIEF и EXPORT без полного provenance | Полные H.Origin/RunRecord §1; операция→output/run таблица §2; stages BRIEF_ASSEMBLY/PACKET_EXPORT/REVISION, mandatory run для автоматического output | Exact refs, no machine→manual, immutable revisions, no circular hashes |
| SI-R02 | §3 EvaluationReport.recommendation; §5.2 п.7 «при ручном выборе — PROCEED_TO_BRIEF_REVIEW»; §3.1/§6 selection projection; §8 RECORD_SELECTION | EvaluationReport.eligibility без будущего выбора (§3); отдельный BriefReviewState (§4), явные selection heads и withdrawal. Нет PROCEED_TO_BRIEF_REVIEW в EvaluationReport | Blockers/UNKNOWN, rubric/weights, ordinary editorial review, no permission from score |
| SI-R03 | §3 «каждая строка — record», ReviewPacket; §8 «read-only projection» без lifetime/privacy | Только persisted immutable ReviewPacket с H/SIRef (§5); EXPORT записывает RunRecord+Packet, возвращает refs, не inline packet (§2/§6) | DISCUSSION_ONLY; exact closure; no editorial write/rights/render/export authority |
| Все три | §8 generic idempotency/status; §11 SI-T01–26 | Уточнения identity/replay/currentness §6 и amendments §8 этого R1 | Остальные операции/records не получают неописанных возможностей |

Не меняются [согласованная концепция](../architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md),
[ревизия выполненного](STORY_INTELLIGENCE_COMPLETED_STAGES_REVIEW.md), E00/A1–A14/O1–O10,
существующие editorial types/codec/hash/rights/approval contracts и работающий pipeline.
Read-only сверка actual `model.py`, `current_package.py`, `versioned_codec.py`,
`first_video.py` подтверждает прежние границы: Candidate discovery_method закрыт
manual_topic/manual_url/manual_local; BriefValue вложен в ScriptRevision;
current package не даёт authority; renderer не проверяет editorial approvals.
R1 не добавляет поля в них и не помещает metadata в reason/rationale.

S3.2a-R1 остаётся ACCEPTED/PURE_ONLY; S3.2b BLOCKED_HOST_NOT_PROVIDED.
PUBLISH_REVISION DISABLED, partial COMMIT reconstruction OFF. Historical wording
2026-11-05 не отменяет поздние D/S1/S2 decisions; нового native approval нет.

## 1. Полные исправленные provenance types

### 1.1 Общие типы и H

`Text` — непустой exact Unicode; `UUID` — canonical lowercase hyphenated;
`PosInt` — integer≥1, не bool; `Hash` —64 lowercase hex; `UTC` — UTC seconds,
только descriptive. `Locale=ru|uk`, не ua.
`SIRef={type:Text,id:UUID,revision:PosInt,sha256:Hash}` — exact SI revision;
`ERef` — прежний editorial `{kind,id,revision,content_hash}`.
`T?` — поле обязательно, значение nullable. `Known<T>` — ровно
`{state:KNOWN,value:T}` либо `{state:UNKNOWN,reason:Text}`. UNKNOWN не0/false/empty.
Все перечисленные поля required, unknown fields/implicit coercion запрещены.

Closed RecordType: Intake, StoryIdea, SourceItem, ClaimItem, EvidenceItem, ClaimCheck,
AudienceHypothesis, ChannelContext, Angle, Rubric, RunRecord, EvaluationReport,
CreativeAlternative, VisualRequirement, Risk, ProductionBrief, Selection, ReviewPacket.
SIRef.type использует этот же vocabulary; ERef.kind не расширяется.

Полный H каждого persisted SI record, включая Packet:

```text
H = {si_version:1, type:RecordType, id:UUID, revision:PosInt,
     previous:SIRef?, created_at:UTC, creator_label:Text,
     origin:Origin, input_refs:List<SIRef>, editorial_refs:List<ERef>}
Origin = {mode:MANUAL_INPUT|USER_IMPORT|RULE_DERIVED|TEMPLATE_DERIVED|
               MODEL_DERIVED|HUMAN_EDIT|RUN_METADATA,
          run_ref:SIRef?, imported_from:Known<Text>?}
```

H — часть content hash. `sha256` существует в SIRef, не внутри самого record.
Record canonical bytes C — UTF-8/no BOM, sorted object keys/no spaces, exact Unicode,
no floats/NaN/surrogates/duplicate keys. Semantic arrays сохраняются буквально.
C(H+payload) хэшируется обычным SHA-256; не editorial digest/signature/authority.

| mode | run_ref | imported_from | Допустимое происхождение |
|---|---|---|---|
| MANUAL_INPUT | null | null | Реально authored input/явный человеческий Selection. Не кнопка «assemble/export» и не принятый template result |
| USER_IMPORT | null | Known<Text> (включая UNKNOWN с reason) | Импорт с сохранением исходной provenance; неизвестное происхождение не ручная авторская работа |
| RULE_DERIVED | Exact RunRecord | null | Rule/method output; stages по §2 |
| TEMPLATE_DERIVED | Exact RunRecord CREATIVE | null | Creative template output; selection не меняет mode |
| MODEL_DERIVED | Exact RunRecord CREATIVE | null | Зарезервированное значение для separately approved provider; V1 runtime UNAVAILABLE, не permission модели |
| HUMAN_EDIT | Exact RunRecord REVISION | null | Новая revision после явной ручной правки. previous/input ancestry сохраняет manual/import/derived origin; не стирает machine ancestry |
| RUN_METADATA | null | null | Только RunRecord, создаваемый harness. Не manual discovery и не output content |

Редактирование derived Brief/Creative/другого input через REVISE_INPUT создаёт
HUMAN_EDIT + REVISION run, а не MANUAL_INPUT и не ссылку на старый run как будто
он породил новые bytes. Старые source/import сведения доступны по previous chain.
Candidate export не может игнорировать derived ancestry даже после HUMAN_EDIT.
Настоящий manual record через RECORD_INPUT допустим только как реальный authored input;
копирование/принятие engine output не имеет пути «очистить» origin. Label сам по себе
не доказывает человеческое авторство или identity; V1 не защищает от владельца,
переписывающего свой недоверенный workspace.

### 1.2 Полный RunRecord payload

RunRecord имеет H с type=RunRecord, revision1/previous=null, origin RUN_METADATA;
creator_label — фиксированный технический label `SI_ENGINE`, не OS principal.

```text
RunRecord.payload = {
 stage:DISCOVERY|EVALUATION|CREATIVE|BRIEF_ASSEMBLY|PACKET_EXPORT|REVISION,
 method_id:Text, method_version:Text, request_payload_sha256:Hash,
 semantic_input_refs:List<SIRef>, input_snapshot:List<SIRef>,
 context_snapshot:ContextSnapshot,
 editorial_snapshot_sha256:Known<Hash>, rubric_ref:SIRef?,
 provider:Provider?, started_at:UTC, finished_at:UTC,
 confidence:Confidence, fresh_trends:Known<Text>, caveats:List<Text>
}
Provider = {id:Known<Text>,version:Known<Text>,model_id:Known<Text>,
            model_version:Known<Text>,config_digest:Known<Hash>}
Confidence = {level:LOW|MEDIUM|HIGH|UNKNOWN,basis:Text}
```

EVALUATION требует rubric_ref. BRIEF_ASSEMBLY/PACKET_EXPORT получают rubric_ref из
exact EvaluationReport, не из latest defaults. У остальных stages rubric_ref null,
если по их описанной операции rubric не используется. В offline V1 provider=null;
MODEL_DERIVED остаётся недоступным runtime. started/finished — descriptive,
не доказательство порядка/authority. Metadata нельзя дополнять догадками.

ContextSnapshot — frozen read-only value, не новый persisted record/authority:
`{context_version:1, active_input_refs:List<SIRef>, selection_head_refs:List<SIRef>,
editorial_snapshot_sha256:Known<Hash>}`. Он фиксирует явно выбранные current inputs
и существующие selection heads; нет implicit resolve-latest. Read-only resolver
harness поставляет фактически наблюдаемый текущий context, а request содержит его
ожидаемый hash. Пользовательский request не назначает доверенную актуальность.

active_input_refs — полный явно выбранный domain input set этого view (включая
нужные current source/check/idea/angle/audience/channel/rubric/risk/visual и выбранные
Eval/Creative/Brief refs при наличии), без history-only previous refs, Run metadata,
Selection (heads отдельно) и ReviewPacket. Packet — terminal discussion artifact,
не current domain input следующего run.
Для (type,id) допустима одна выбранная exact revision; selection heads — отдельно.
Содержательное переключение на другой набор inputs выражается новым ContextSnapshot,
а не угадывается по «самой свежей» записи.

`context_hash=SHA256(C(ContextSnapshot))`. При ERefs нужен supplied exact validated
editorial snapshot/hash context, иначе INVALID. Если workspace/context неоднозначен,
нет нужного source/ref/hash или две конфликтующие heads для scope — INVALID,
не выбор по clock/max UUID. Это проверка SI draft context, не protected head anchor.

### 1.3 Closure и порядок без циклов

`Closure(roots)` — полный transitive set всех SIRef, встречающихся в H/payload,
включая previous, origin.run_ref, input_refs и вложенные typed refs. ERefs разрешаются
отдельно в переданном editorial snapshot. Missing/hash/type/cycle — INVALID.
Manifest сериализуется как **порождаемый** canonical set: unique exact refs в порядке
(type,id,revision,sha256); это специальный тип manifest, не сортировка chapters,
ratings или пользовательских массивов. Header input_refs сохраняет свой определённый
operation order. Разные hashes одной (type,id,revision) в closure запрещены.

Run.semantic_input_refs = direct содержательные roots операции из §2.
Run.input_snapshot = canonical Closure(semantic_input_refs + SIRefs из ContextSnapshot);
он не содержит создаваемый run или его outputs. Для audit полноты capture учитывает
и уже существовавшие selection heads, но это **не** будущий prerequisite EVALUATE. request_payload_sha256 связывает новые authored payload/options,
которые ещё не являются records, без включения output hash.
Порядок будущего построения: вычислить/проверить результат в working memory →
записать RunRecord с final metadata → записать output с origin.run_ref → вернуть refs.
У run нет output_refs/backlink. Run input_snapshot и H.input_refs не могут включать
собственный output. Вычисляемый seed не является input record с fake hash.

ClaimItem→EvidenceItem обратная ссылка не вводится: EvidenceItem ссылается на
ClaimItem/SourceItem, ClaimCheck — на них и evidence. Selection ссылается на уже
записанный target. Brief может ссылаться на creative Selection, но никогда на
**последующий Selection этого Brief**. Packet создаётся последним и не используется
как input для evaluation/brief/selection. Это сохраняет DAG и исходные SI limits;
при превышении limits — LIMIT, не truncation или скрытая потеря provenance.

## 2. Закрытая operation map (заменяет исходную §8 таблицу)

Все восемь исходных operations сохранены. Версии methods ниже — предлагаемые exact
идентификаторы, не уже утверждённые engines. Новых network/renderer/storage commands нет.
`RecordSet` RECORD_INPUT: Intake, SourceItem, ClaimItem, EvidenceItem, ClaimCheck,
AudienceHypothesis, ChannelContext, Angle, Rubric, VisualRequirement, Risk,
CreativeAlternative, ProductionBrief. RunRecord/Selection/ReviewPacket исключены.

| Operation / method_id,version | Закрытые options | Recorded outputs / mode/stage | Roots и validation |
|---|---|---|---|
| RECORD_INPUT / si.record-input,1-r1 | record_type:RecordSet; working_copy:typed payload; input_origin:MANUAL_INPUT или USER_IMPORT с imported_from | Один record / указанное действительное manual/import происхождение; run нет | Все его existing typed refs и declared provenance refs; новым derived payload этот путь не становится |
| REVISE_INPUT / si.human-revision,1-r1 | base_ref:SIRef; replacement_payload:того же RecordSet type | RunRecord REVISION + новая revision того же id / HUMAN_EDIT; previous=base_ref | base_ref + все замещённые/сохранённые refs; прежняя ancestry не удаляется; Run/Selection/Packet не reviseable здесь |
| DISCOVER_LOCAL / si.discover-local,1-r1 | portfolio_ref:SIRef? | RunRecord DISCOVERY + StoryIdea / RULE_DERIVED | Exact Intake + supplied SourceItem/ChannelContext/portfolio roots; no fetch, не «fresh trends отсутствуют» |
| EVALUATE / si.evaluate,1-r1 | rubric_ref:SIRef | RunRecord EVALUATION + EvaluationReport / RULE_DERIVED | Exact Idea,Angle,Audience,Channel,Rubric,claims/checks/sources/risks/context; **не требует Selection/Creative/Brief** |
| PROPOSE_CREATIVE / si.creative-templates,1-r1 | strategy_set:QUESTION_HUMAN_STAKES_COUNTERINTUITIVE | RunRecord CREATIVE + CreativeAlternative records / TEMPLATE_DERIVED | Existing Angle/Idea/Audience/Channel + EvaluationReport и claim/check/source roots; no invented review; blocked evaluation допускает только draft suggestions с diagnostics |
| ASSEMBLE_BRIEF / si.brief-assembly,1-r1 | production_options:ProductionOptions; base_brief_ref:SIRef?; creative_selection_ref:SIRef? | RunRecord BRIEF_ASSEMBLY + ProductionBrief / RULE_DERIVED; DRAFT | Exact выбранные Eval/Creative/Idea/Audience/Channel/claims/checks/sources/visuals/risks/profile и optional creative Selection; base ref при revision. SELECT target Brief ещё отсутствует |
| RECORD_SELECTION / si.selection,1-r1 | scope:SelectionScope; target_ref:SIRef; choice:SELECT/REQUEST_CHANGES/WITHDRAW; reason:Text; previous_selection_ref:SIRef? | Один Selection / MANUAL_INPUT, без run; создание или следующая revision одной selection chain | Exact target/context, declared current head; SELECT prerequisite §4, withdrawal не изменяет Eval или target |
| EXPORT_REVIEW_PACKET / si.review-packet,1-r1 | brief_ref:SIRef; privacy_grant:PrivacyGrant | RunRecord PACKET_EXPORT + ReviewPacket / RULE_DERIVED, только persisted record | Brief + explicit context/selection heads + вся source closure; privacy §5; нет inline/ephemeral Packet |

Для первых шести операций outputs зафиксированы в приватном SI workspace согласно
будущему approved persistence contract, не в editorial snapshot. RECORD_SELECTION
тоже записывает только SI Selection. EXPORT читает input records, но создаёт собственные
Run/Packet records: «read-only» означает отсутствие изменения **исходных** SI records,
editorial state/permissions и renderer, а не отсутствие любого SI record creation.
Само сохранение SI данных ещё требует SI-D03; этот R1 не реализует storage.

У RECORD_INPUT H.input_refs равен всем direct refs payload/provenance в schema order;
у REVISE_INPUT — base_ref затем payload refs; у stage outputs — root refs операции
в schema order, плюс previous при наличии. origin.run_ref — отдельная ссылка на run,
не output→input cycle. Run.input_snapshot всегда полная audit closure roots+ContextSnapshot по §1.3.
Run H.input_refs равен его input_snapshot. Валидация method/stage/type обязательна.

Новая assembled Brief: новый id/revision1 при base_brief_ref=null; иначе тот же
Brief id/следующая revision/previous=base. Generic human authored Brief остаётся
возможным как RECORD_INPUT, но автоматическое заполнение требует ASSEMBLE_BRIEF;
ручная правка записанной derived Brief — только HUMAN_EDIT, не ложное manual.
Run/EvaluationReport/новые CreativeAlternative outputs и каждый Packet создаются с
новым id/revision1. Identity выделяется один раз на принятый logical request;
повтор возвращает прежние refs (§6), не новые UUID/time/Run. Для операций без Run
method_id/version фиксированы таблицей interface1-r1 и сохраняются рядом с request
mapping, не в дополнительных H fields. Другой метод не подставляется на replay;
смена этих правил требует явной contract revision, не скрытого default.

ProductionBrief payload сохраняет все исходные поля §3 и добавляет только
`creative_selection_ref:SIRef?` (точный Selection CREATIVE_CHOICE либо null для DRAFT).
Его workflow_state остаётся DRAFT/IN_REVIEW/WITHDRAWN, не selected/approved.
В brief H/input refs явно присутствует использованный Selection; новый selection
head требует нового assembly/revision, не редактирования старой Brief.

## 3. SI-R02: EvaluationReport не зависит от будущего выбора

### 3.1 Полный revised payload

EvaluationReport = H(type=EvaluationReport, origin RULE_DERIVED, run EVALUATION) +:

```text
{idea_ref:SIRef, angle_ref:SIRef, audience_ref:SIRef, channel_ref:SIRef,
 rubric_ref:SIRef, run_ref:SIRef, ratings:List<Rating>, risk_refs:List<SIRef>,
 eligibility:EvaluationEligibility, aggregate_tenths:Known<Int0..1000>,
 caveats:List<Text>}
EvaluationEligibility = {
 state:BLOCKED|NEEDS_INPUT|NEEDS_RESEARCH|REVIEW_DUPLICATE|ELIGIBLE_FOR_CREATIVE,
 reason_codes:List<Code>}
Rating = {criterion_key:Text,value:Known<Int0..5>,basis_refs:List<SIRef>,
          explanation:Text,confidence:Confidence}
```

Payload.run_ref = H.origin.run_ref; rubric/method refs совпадают с RunRecord.
`recommendation:Recommendation` и `PROCEED_TO_BRIEF_REVIEW` **не входят** в этот record.
EvaluationEligibility — суждение именно по frozen evaluation inputs, не eligibility
человека/production. Изменение UI selection не меняет его bytes/hash.

### 3.2 Приоритет при EVALUATE

1. Неверные schema/hash/refs/locale/невалидный context — INVALID; изменившийся expected
   context — STALE. Нет accepted current outputs. Replay прежних refs — отдельно §6.
2. Любой открытый blocking scientific/legal/ethical/rights/capability risk → BLOCKED,
   в том числе missing/disputed central evidence. High score его не компенсирует.
3. Недостающая постановка/audience/channel или обязательные current data → NEEDS_INPUT.
4. Остальная missing evidence/locators/freshness, обязательные UNKNOWN ratings или
   UNKNOWN confidence без достаточного обоснования → NEEDS_RESEARCH. UNKNOWN не0;
   при UNKNOWN rating aggregate UNKNOWN, не среднее известных. Portfolio UNKNOWN
   не доказывает novelty и не становится empty portfolio.
5. Неразрешённый duplicate → REVIEW_DUPLICATE.
6. При достаточных inputs, отсутствии открытых blocking risks, объяснённых ratings/assumptions и
   отсутствии нерешённого duplicate → **ELIGIBLE_FOR_CREATIVE**, даже если ещё нет
   CreativeAlternative/Selection/Brief. Нет score threshold и automatic approval.

Сохраняются девять предложенных criteria/веса15/10/10/20/15/10/10/5/5 и formula
aggregate_tenths=2×Σ(weight×rating). Это rubric points, не viral/factual probability;
confidence qualitative. Manual hypotheses не выдаются за audience statistics.

`REVISE_CREATIVE` относится к проверке уже созданной creative alternative (§4),
не к EVALUATE, который ещё не имеет такого output. Hook не может менять факты;
unsupported central hook остаётся BLOCKED, qualifiers сохраняются буквально.

## 4. Явный выбор и BriefReviewState (не новый record)

### 4.1 Selection scope и цепочка

У Selection H/type/поля selector_label/reason остаются; closed payload R1:
`{scope:SelectionScope,target_ref:SIRef,choice:SELECT|REQUEST_CHANGES|WITHDRAW,
selector_label:Text,reason:Text}`.
SelectionScope=`{purpose:CREATIVE_CHOICE|BRIEF_REVIEW,idea_ref:SIRef,
audience_ref:SIRef,channel_ref:SIRef}`. Первый purpose имеет target CreativeAlternative,
второй ProductionBrief. Angle/context выбираются explicit input refs, не требуют
будущего creative/brief Selection до EVALUATE.

Одна логическая chain на exact scope. Initial head — новый Selection id/revision1,
previous=null; следующий human action того же scope — тот же id/revision+1,
previous=предыдущий exact head, target может быть другим вариантом того же scope.
`previous_selection_ref` и expected_context_hash должны совпадать с наблюдаемым head
workspace context. Нет текущего head → initial; неизвестный/конфликтующий predecessor
→ SELECTION_CONFLICT, без нового Selection. Две объявленные heads одного scope
или fork — INVALID; нельзя разрешать их по timestamp/UUID.

Это обычная lineage недоверенного SI workspace, **не trusted editorial sequence**,
не A8 reconsideration/REVOKE и не защищённая авторизация. Даты human actions не
выбирают head. Workspace resolver явно supplies heads и проверяет previous chain;
клиент не выбирает старый SELECT как current после WITHDRAW.
Повтор старого request возвращает old record refs, **не переставляет head назад**.

SELECT Creative требует current exact EvaluationReport ELIGIBLE_FOR_CREATIVE и
совместимый current Creative с проверенными claim/qualification/risk inputs.
SELECT Brief требует current brief, его exact creative_selection_ref=активному
SELECT Creative, no blockers и всех review prerequisites. До этого разрешён
REQUEST_CHANGES или WITHDRAW; они не дают положительного readiness.
Selection остаётся человеческим intent/label, не evidence OS principal/rights.

### 4.2 Domain currentness не равен hash всего UI context

semantic_input_refs явны; `SemanticClosure` следует содержательным refs payload и
origin Run.semantic_input_refs, **не** H.previous, Run.input_snapshot/context_snapshot
или декоративным audit labels/times. Для EVALUATE это Idea/Angle/Audience/Channel/
Rubric/claims/checks/sources/risks, не Selection/Creative/Brief. Для Creative — эти
inputs и exact EvaluationReport. Для assembled Brief — они плюс выбранный Creative,
production options и **использованный creative Selection**, если он non-null.

CURRENT для domain record означает: все его semantic refs разрешены и совпадают с
explicit active input set текущего view; changed/удалённая из current set dependency
даёт STALE, dangling/wrong hash/type даёт INVALID. Не относящиеся к этим dependencies
новые записи/current heads сами по себе не делают record stale. На ERefs применяется
отдельный exact validated snapshot context, без доверия plain status.

Изменение creative/brief selection head **не меняет currentness EvaluationReport**
или CreativeAlternative, когда facts/context/rubric не изменились. Selection heads
в Run.context_snapshot — историческая audit metadata, не semantic inputs EVALUATE.
Brief может стать STALE при изменении **его** creative_selection_ref/head;
такой semantic Selection ref сравнивается с context.selection_head_refs, не
с active_input_refs. Остальные semantic refs сравниваются с active_input_refs.
WITHDRAW самого Brief меняет review projection, а не его содержательное состояние.
Packet проверяет **полный** snapshot/context hash §5.3 и потому может стать STALE
после любого изменения head, даже если E1 по-прежнему CURRENT. Запрещено переносить
packet freshness rule на evaluation: иначе вновь возникает SI-R02.

Это не автоматическое semantic truth inference: typed dependency comparisons и
human checks/risk data сохраняют исходные границы. Content и selection меняются
явными действиями; полная closure остаётся для provenance, не для auto-resolve-latest.

### 4.3 ProjectionValue

BriefReviewState — вычисляемое read-only value, без H/id/SIRef/persistence:

```text
{projection_version:1, context_hash:Hash,
 evaluation_ref:SIRef, creative_ref:SIRef?, brief_ref:SIRef?,
 selection_head_refs:List<SIRef>,
 currentness:CURRENT|STALE|INVALID,
 review_state:BLOCKED|NEEDS_INPUT|NEEDS_RESEARCH|REVIEW_DUPLICATE|
              REVISE_CREATIVE|AWAITING_CREATIVE|AWAITING_CREATIVE_SELECTION|
              AWAITING_BRIEF|AWAITING_BRIEF_SELECTION|READY_FOR_BRIEF_REVIEW|
              CHANGES_REQUESTED|WITHDRAWN,
 reason_codes:List<Code>, editorial_approval_state:NOT_EVALUATED}
```

При currentness=STALE/INVALID review_state не используется как положительное
состояние; диагностики обязательны. Если head WITHDRAW отражает отказ текущего scope,
review_state=WITHDRAWN даже при ранее READY; RequestChanges → CHANGES_REQUESTED.
Перед ними validation/currentness, а blockers сохраняются в reason_codes даже при
withdrawal (никакой отмены fact/rights проблем этим действием).

При валидном current context: blocking/unknown/duplicate eligibility сохраняют свои
состояния и precedence; затем hook/claim conflict → REVISE_CREATIVE либо BLOCKED для
central unsupported claim. Если препятствий нет: нет Creative → AWAITING_CREATIVE;
есть unselected Creative → AWAITING_CREATIVE_SELECTION; есть SELECT Creative, но нет
Brief → AWAITING_BRIEF; есть Brief без его SELECT → AWAITING_BRIEF_SELECTION;
оба exact SELECT актуальны и совместимы → READY_FOR_BRIEF_REVIEW.
Это review worklist, **не** editorial authority/readiness для renderer.

В obsolete фразе «только при ручном выборе PROCEED_TO_BRIEF_REVIEW» исходной §5.2
смешаны два шага: EVALUATE теперь заканчивается ELIGIBLE_FOR_CREATIVE; только эта
projection после selections может показать READY_FOR_BRIEF_REVIEW. Record Evaluation
не приобретает будущего значения retroactively.

### 4.4 Полный путь успешного примера и изменений

Все aliases ниже illustrative, не реальные UUID/hashes или verified research:
`I1/A1/C1/G1/S1/Q1/Rub1` — recorded synthetic current inputs с complete review;
`E1` — EvaluationReport, `K1` — CreativeAlternative, `B1` — Brief,
`SC1/SB1` — selection heads. Предположены действительные test fixture evidence/rights,
не реальные исторические факты из RU/UK примеров исходной proposal.

| Шаг | Новые records | Stored eligibility E1 / derived projection |
|---|---|---|
| EVALUATE до выбора | EvalRun1,E1 | E1=ELIGIBLE_FOR_CREATIVE; AWAITING_CREATIVE, не требуется будущий SELECT |
| PROPOSE_CREATIVE | CreativeRun1,K1 | E1 bytes/CURRENT те же; AWAITING_CREATIVE_SELECTION |
| Explicit SELECT K1 | SC1 | E1 bytes/CURRENT те же; AWAITING_BRIEF |
| ASSEMBLE_BRIEF(K1,SC1,E1) | AssemblyRun1,B1 DRAFT, origin RULE_DERIVED | E1 не изменён и CURRENT; AWAITING_BRIEF_SELECTION |
| Explicit SELECT B1 | SB1 | READY_FOR_BRIEF_REVIEW; editorial_approval_state NOT_EVALUATED |
| WITHDRAW B1 | SB2(previous=SB1,choice=WITHDRAW) | E1/B1/SB1 bytes прежние; E1 CURRENT, текущая projection WITHDRAWN |
| Изменить источник S1→S2 | Новые source/check inputs, новый explicit context | Старые E1/K1/B1 STALE для нового context; их stored fields не меняются; нужен новый evaluation/creative/assembly/выбор |

WITHDRAW не требует переоценки неизменных facts для сохранения old E1; но без нового
явного SELECT не восстанавливает review-ready projection. Новые input refs не
получают старых selections автоматически. Генерация новых output refs и linkage
не разрешают восстановить старый editorial APPROVE после REVOKE.

## 5. SI-R03: только persisted immutable ReviewPacket

### 5.1 Identity и полный payload

**Выбран один вариант: ReviewPacket — recorded SI object. Эфемерного ReviewPacket
в composite contract нет.** Экран может read-only отображать record; это не другой
тип packet. BriefReviewState (§4) — отдельное UI value, не альтернативный packet.

Packet H: type=ReviewPacket, новый id/revision1/previous=null, creator_label=`SI_EXPORTER`
(технический label), origin RULE_DERIVED с RunRecord PACKET_EXPORT. Header не содержит
human selector/reviewer name; actual source records/run context приватны.

```text
ReviewPacket.payload = {
 format_version:si-review-packet/1-r1, purpose:DISCUSSION_ONLY,
 brief_ref:SIRef, context_snapshot:ContextSnapshot,
 source_closure_refs:List<SIRef>, existing_editorial_refs:List<ERef>,
 source_snapshot_digest:Hash, redaction_profile:si-packet-redact/1,
 privacy_grant:PrivacyGrant, display_items:List<DisplayItem>,
 omissions:List<Omission>, unresolved:List<Code>,
 review_state_at_capture:BriefReviewState
}
PrivacyGrant = {reviewed_snapshot_digest:Hash,
 allowed_text_fields:List<FieldGrant>, confirmed:true}
FieldGrant = {source_ref:SIRef,field_path:Text,value_sha256:Hash}
DisplayItem = {source_ref:SIRef,fields:List<FieldView>}
FieldView = {field_path:Text,kind:TEXT|STATE|REDACTED,text:Text?}
Omission = {source_ref:SIRef,field_path:Text,reason_code:PRIVATE_FIELD|NOT_SELECTED}
```

TEXT содержит ровно выбранный reviewed text; STATE — только ниже перечисленные
closed scalar states как ASCII text. REDACTED требует text=null и Omission;
не подставляет UNKNOWN в raw source object и не превращается в SourceItem/ClaimItem.
Packet unresolved — только Code из закрытого списка §6,
не сырые paths/names/error messages или пользовательские short labels. No raw source payload/draft bundle/media.

**Source snapshot**: roots = Brief + Context.active_input_refs + selection heads;
source_closure_refs = canonical Closure(roots). Он включает использованные Eval,
Creative, source/claim/check/rights-note/Risk/Selection/Run/previous ancestry.
Это полная closure **ссылок**, не публикация всех их raw bytes. Она исключает
новый Packet и создающий его export Run. Packet не является input ни для того Run,
ни для Brief. `source_snapshot_digest=SHA256(C({context_snapshot,source_closure_refs,
existing_editorial_refs}))`; key names ровно как здесь, порядок manifest §1.3.
Export Run.semantic_input_refs — эти roots; его input_snapshot равен source_closure_refs; source snapshot и все ERefs
проверяются до capture. Missing dependency/extra contradictory hash → INVALID,
не implicit fetch/resolve-latest или частичный «успешный» packet.

Получатель redacted Packet может проверить Packet record hash, но **не** восстановить
raw source hashes из redacted views. SIRef/manifest digest обозначают local exact
provenance, не доказательство truth/rights/identity. Для raw source review нужен
отдельный явный приватный доступ; packet не является editable SI workspace import,
authority evidence, production manifest или blob upload API.

### 5.2 Privacy/redaction profile (proposal, не security certification)

По умолчанию raw locators и human labels не копируются. Всегда запрещены, даже
при FieldGrant: H.creator_label исходных records, reviewer_label, selector_label,
original_locator/local file paths, imported_from, access credentials/token/query
strings, raw Provider config, private free-form actor/owner labels. Source/Evidence
locators не экспортируются; их проверяемые raw версии остаются в приватном workspace.
Packet H labels выше — фиксированные технические constants, не реальные identities.
Raw previous records не inline-встраиваются для обхода этих правил.

Closed разрешённые TEXT fields **только с matching FieldGrant**:
StoryIdea(title,summary,viewer_question); SourceItem(title.value при KNOWN);
ClaimItem(statement); ClaimCheck(qualification при non-null); Angle(question,thesis,distinction);
CreativeAlternative(hook_text,title_options[i],thumbnail_notes,
chapters[i].heading/chapters[i].purpose,retention_0_30);
VisualRequirement(description,fallback.value при KNOWN);
Risk(description,mitigation); ProductionBrief(promise,must_avoid[i],required_reviews[i]).
Индекс — существующий элемент array, не wildcard. Все остальные text fields redacted.
STATE без human label: ClaimCheck.state, Risk(category,severity,blocking,resolution),
VisualRequirement(role,rights_state), Brief(locale,content_mode,workflow_state),
EvaluationEligibility.state и projection review_state/currentness. Значения только
из закрытых enum/bool типов, без произвольного текста. Factual/rights qualifications
не теряются незаметно: если видимая factual формулировка/hook/promise требует
qualifier, export должен включать его точный approved-for-display text с отдельным
matching Grant. Иначе INVALID/REDACTED_CONTEXT_INCOMPLETE, без Packet. Полностью
redacted claim вместо видимой формулировки допустим; он не становится checked fact.

Grant привязан к source_snapshot_digest и exact source field value hash C(value),
не к будущему Packet hash. Harness запрашивает явное human privacy review по этим
полям; username/OS identity не публикуется и не становится grant/editorial permission.
Изменение value/source revision/manifest делает Grant невалидным. Confirmed=false,
отсутствующий grant или попытка разрешить private field → INVALID/PRIVACY_REVIEW_REQUIRED
или PRIVACY_BLOCKED, без Packet. confirmed:true — explicit local user intent,
не assertion от произвольного machine output.

Проверка typed fields и явный просмотр текста не являются безошибочным PII detector:
историческое имя в claim не равно private reviewer label, а секрет может оказаться
в произвольном text. При обнаруженном private path/credential/user label в выбранном
тексте — PRIVACY_BLOCKED; отсутствие обнаружения не называется гарантией privacy.
Поэтому Packet предназначен для **приватного локального обсуждения**, не для Git,
публичного сайта, автоматического network/file share или release. Перенос наружу и
дополнительные profiles требуют SI-D03/SI-D07 и отдельного owner/privacy решения.
Этот R1 ничего не скачивает и не открывает locator.

### 5.3 Bytes, lifetime, currentness

Bytes Packet — C(H+payload) по §1; content hash = SHA-256 этих bytes, SIRef внешний.
Deterministic payload определяется exact source snapshot, selected fields/grant,
redaction/method version и projection at capture. Semantic list order сохраняется;
DisplayItems следуют manifest order, FieldViews/Omissions — перечисленным schema
field order и ascending array index. UTC/id не вставляются в payload из «текущего»
clock при чтении; H metadata фиксируется один раз при создании. Новый logical request
может создать другой id/H/hash, даже при одинаковом payload; это не replay.

Packet существует как immutable snapshot, пока сохранён в приватном workspace по
будущей SI-D03 retention policy. TTL/backup destination/автоматическая очистка здесь
**не выбираются**. Read/render view существующего Packet не изменяет его bytes.
При изменении current inputs/selection head/editorial snapshot/privacy profile он
показывается как HISTORICAL/STALE через отдельную currentness проверку. Его frozen
review_state_at_capture не означает текущее READY, даже если тогда был SELECT.
Изменение snapshot или redaction создаёт новый Packet id, не переписывает старый.

Снимок, captured с blockers, может быть записан для обсуждения с BLOCKED/NEEDS_REVIEW
и видимыми diagnostics, если все refs валидны и privacy rules выполнены. Missing raw
source research content может быть честно UNKNOWN в валидном SourceItem; **missing SIRef**
не заменяется UNKNOWN, это INVALID. Невалидный/STALE expected context не экспортируется
как current; существующий исторический Packet остаётся доступен с явной пометкой.

Удаление по будущей approved retention policy не разрешает пересоздать прежний
Packet/персональные данные из retry. Если output/idempotency mapping утрачен,
UNAVAILABLE/RECORD_UNAVAILABLE; не выдавать новый id за прежний receipt. Новое
согласованное создание — новый explicit request. Нет crash-durable promise,
protected journal/anchor, immutable-storage или криптографического доверия.
Обнаруженная потеря mapping блокирует повтор как UNAVAILABLE, но обнаружение полного
согласованного владельческого rollback недоверенного workspace не обещается.
Перед implementation SI-D03 должен определить integrity/retention lifecycle mapping;
нельзя заявлять сохранность idempotency через потерю всего этого состояния.

## 6. Исправленный interface и идемпотентность

Полный revised response shape сохраняет ref-only договор:

```text
Request = {interface_version:1, request_id:UUID, operation:Operation,
           expected_context_hash:Hash,
           input_refs:List<SIRef>, editorial_refs:List<ERef>,
           ui_locale:ru|uk, options:OperationOptions}
Response = {interface_version:1, request_id:UUID,
            result:OK|NEEDS_REVIEW|STALE|INVALID|UNAVAILABLE,
            output_refs:List<SIRef>, diagnostics:List<Diagnostic>}
Diagnostic = {code:Code,field_path:Text,input_ref:SIRef?,message:Text}
```

Context поставляется read-only harness (§1), expected_context_hash — CAS/check
в пределах недоверенного SI workspace. Он не OS authorization и не editorial anchor.
При новом request несовпадение observed/expected context → STALE, outputs=[].
Для RECORD_INPUT также существует явный пустой начальный context (не guessed hash).
Interface version1 остаётся предложением до первого owner approval; это не изменение
уже реализованного wire protocol. Approved S1/schema2 не меняются.

**Output ordering:** stage operations → `[RunRecord ref, output refs в declared order]`;
RECORD_INPUT/RECORD_SELECTION → `[record ref]`; EXPORT → `[export Run ref, Packet ref]`.
В Response нет inline_packet, ни ephemeral ReviewPacket. Получение/ref display —
через локальный read-only resolver; EXPORT сам не пишет file/network destination.
Все recorded outputs проходят shape/ref/hash checks до регистрации результата.
INVALID/UNAVAILABLE не создают accepted records/partial outputs. NEEDS_REVIEW может
вернуть явно draft outputs/blocked Packet; это не successful selection.

Одному logical request назначаются ids/time/output slots один раз. Сохраняется
соответствие request_id→exact canonical Request bytes→assigned output refs.
Повтор тех же bytes возвращает те же refs, без нового Run/Packet/Selection revision
или backward head update; другие bytes с тем же id → REQUEST_CONFLICT, outputs=[].
Результат OK подтверждает создание/получение immutable records, не их currentness.
Current UI отдельно проверяет domain dependencies по §4.2, а Packet — полный frozen snapshot против observed context.
Cached old Packet/SELECT не может автоматически выглядеть current после WITHDRAW.
Новые requests с новым expected context получают новые outputs либо STALE; старые
record fields/recommendations никогда не меняются из-за нового выбора.

Idempotency гарантируется только пока целы outputs и mapping valid workspace;
повреждение/потеря → INVALID/RECORD_UNAVAILABLE, не guessed reconstruction. Никакой
новый storage writer/persistence protocol не реализуется этим описанием.

Closed Code R1 (полный список): TYPE, UNKNOWN_FIELD, MISSING_FIELD,
VERSION_UNSUPPORTED, LIMIT, REF_MISSING, REF_HASH_MISMATCH, REF_TYPE_MISMATCH,
DEPENDENCY_CYCLE, LOCALE_MISMATCH, INPUT_STALE, EVIDENCE_NEEDED,
CENTRAL_CLAIM_UNSUPPORTED, RIGHTS_BLOCKED, DUPLICATE_REVIEW_NEEDED,
HOOK_FACT_CONFLICT, CAPABILITY_BLOCKED, UNAVAILABLE_OFFLINE,
HANDOFF_ADAPTER_UNAVAILABLE, REQUEST_CONFLICT, PROVENANCE_MISMATCH,
SELECTION_CONFLICT, PRIVACY_REVIEW_REQUIRED, PRIVACY_BLOCKED,
REDACTED_CONTEXT_INCOMPLETE, RECORD_UNAVAILABLE. Первые20 сохранены из исходной §8;
последние6 добавлены только для R1. Method/stage/mode mismatch — PROVENANCE_MISMATCH.
Shape/unknown field/ref/hash/limits используют прежние codes.
Qualification/diagnostic code не превращает пользователя в reviewer с полномочиями.

## 7. Table-driven acceptance R1 (не выполненные executable tests)

Все aliases — illustrative synthetic refs. Future tests используют настоящие UUID,
Hash, immutable fixtures и exact bytes, не эти сокращения. Все cases проверяют
отсутствие editorial write/approval/rights/render и неизменность исходных records.

| ID | Input / действие | Ожидаемые records/status/invariant |
|---|---|---|
| R1-T01 | ASSEMBLE current E1/K1, manual click | Assembly Run BRIEF_ASSEMBLY и DRAFT Brief RULE_DERIVED с run_ref; не MANUAL_INPUT |
| R1-T02 | EXPORT валидного B1, complete privacy grant | Persisted export Run PACKET_EXPORT+Packet, Response.output_refs2; inline отсутствует |
| R1-T03 | Derived Brief/Packet origin.run_ref=null либо wrong stage | INVALID/PROVENANCE_MISMATCH; нет accepted output |
| R1-T04 | Human edit derived Brief | REVISION run + HUMAN_EDIT next Brief revision; previous/machine ancestry сохранены, не manual export |
| R1-T05 | Run содержит output refs / cyclic origin или Packet в собственном source manifest | UNKNOWN_FIELD/DEPENDENCY_CYCLE, INVALID; no self-hash |
| R1-T06 | Complete EVALUATE до всякого Creative/Selection | Stored ELIGIBLE_FOR_CREATIVE, projection AWAITING_CREATIVE; old future human choice не требуется |
| R1-T07 | K1 затем SELECT K1, assemble B1, SELECT B1 | AWAITING_CREATIVE_SELECTION→AWAITING_BRIEF→AWAITING_BRIEF_SELECTION→READY_FOR_BRIEF_REVIEW; E1 bytes/CURRENT те же |
| R1-T08 | Score высокий, essential rights blocked | E1 eligibility BLOCKED и projection BLOCKED; SELECT Brief отказан, не grants |
| R1-T09 | UNKNOWN rating/confidence/portfolio без blocker | aggregate UNKNOWN при rating UNKNOWN; NEEDS_INPUT/NEEDS_RESEARCH по причине; никакой zero-fill/renormalization |
| R1-T10 | WITHDRAW SB2 после SB1 SELECT | E1/B1/SB1 hashes неизменны; current projection WITHDRAWN, E1 CURRENT при прежних facts; old request replay не возвращает active head назад |
| R1-T11 | Source/Idea/profile/locale revision изменена | E1/K1/B1/Packet historical STALE в новом context; re-evaluate/reassemble/reselect, не implicit upgrade refs |
| R1-T12 | Two selection heads/fork/stale predecessor | INVALID/SELECTION_CONFLICT; не resolve по timestamp/max UUID |
| R1-T13 | Packet source closure missing entry/wrong hash | INVALID/REF_MISSING или REF_HASH_MISMATCH; no partial Packet/fetch |
| R1-T14 | В source local path, human label и raw provider config | Не появляются в views/H labels; forbidden grant → PRIVACY_BLOCKED; output не raw source bundle |
| R1-T15 | Text grant не соответствует value/manifest, отсутствует или не покрывает обязательный qualifier | INVALID/PRIVACY_REVIEW_REQUIRED либо REDACTED_CONTEXT_INCOMPLETE, без Packet; no implicit privacy consent от SELECT Brief |
| R1-T16 | Redacted FieldView пытаются принять как исходный Claim/Source с прежним hash | INVALID/TYPE/REF_HASH_MISMATCH; projection не raw record, source ref/hash не переписываются |
| R1-T17 | Exact retry EXPORT/ASSEMBLE/Selection и changed payload same ID | Тот же набор refs/no new Run/head; changed payload REQUEST_CONFLICT; new explicit request после изменения snapshot — новый Packet |
| R1-T18 | Packet читает новый context после withdrawal | Bytes/at_capture unchanged; display HISTORICAL/STALE, не current READY/permission |
| R1-T19 | Packet/output mapping удалён/повреждён | RECORD_UNAVAILABLE/INVALID без reconstructed old output; новый request не автоматический |
| R1-T20 | RU/UK draft aliases из original examples, central evidence UNKNOWN | Только working preview, BLOCKED; strict SIRef validation не пропускает aliases. Runtime/provider/renderer не вызывается |

Нужны будущие literal codec/provenance/closure/redaction vectors и независимые
expected bytes/status assertions до implementation acceptance; эта таблица их не
объявляет выполненными. Native tests и Python unit tests сейчас не запускались.

## 8. Совместимость всех SI-T01–SI-T26

| Original case | R1 disposition |
|---|---|
| SI-T01 | RETAIN: offline manual intake, no locator fetch |
| SI-T02 | RETAIN+точное правило: HUMAN_EDIT/SELECT не очищают derived ancestry |
| SI-T03 | RETAIN: центральная missing evidence → evaluation/projection BLOCKED |
| SI-T04 | RETAIN: essential visual rights blocker выше баллов |
| SI-T05 | RETAIN: unresolved duplicate → eligibility REVIEW_DUPLICATE |
| SI-T06 | RETAIN: no fresh data, UNAVAILABLE_OFFLINE; no fabricated trends |
| SI-T07 | RETAIN: stale/freshness diagnostic; новые exact inputs/review |
| SI-T08 | RETAIN: changed refs → STALE current projection, не mutation старого record |
| SI-T09 | RETAIN: high score не отменяет risk/rights |
| SI-T10 | AMEND: REVISE_CREATIVE теперь в BriefReviewState по existing Creative; central false claim остаётся BLOCKED |
| SI-T11 | RETAIN: optional GPU/paid unavailable, lawful CPU fallback; essential без fallback блокирует |
| SI-T12 | RETAIN: UNKNOWN не0; confidence/portfolio не выдумываются |
| SI-T13 | RETAIN: ru/uk alignment, ua invalid |
| SI-T14 | RETAIN: strict scalar/field/size/UTF-8 checks, R1 shapes вместо старых в затронутых местах |
| SI-T15 | AMEND: Packet — record с complete closure manifest и views; missing refs/cycle не допускаются; redacted view не raw record |
| SI-T16 | RETAIN: machine suggestion не human check/approved; role labels не identity |
| SI-T17 | AMEND: stable recorded refs включает Run/Packet/Selection; replay не означает current и не rewinds selection head |
| SI-T18 | AMEND: ref-only persisted DISCUSSION_ONLY Packet; нет direct editorial/renderer export, adapter UNAVAILABLE |
| SI-T19 | RETAIN: material binding не licence/expiry/intended-use grant |
| SI-T20 | RETAIN: нет влияния на editorial REJECT/REVISE/REVOKE/history/ambiguity |
| SI-T21 | RETAIN: факт/число/дата/qualification не меняются стилистическим проходом |
| SI-T22 | RETAIN: local WAV/optional model licence gate; Edge offline unavailable |
| SI-T23 | RETAIN: pipeline20 scenes/2000 code points и capabilities, без truncation |
| SI-T24 | AMEND: source/profile/locale/intended-use change → new eval/brief selection; Selection/Packet currentness отдельно от frozen status |
| SI-T25 | RETAIN: все existing S1/S2/D-01/golden unchanged; protected write отсутствует |
| SI-T26 | RETAIN: исходные RU/UK примеры illustrative, NOT EXPORTABLE; aliases не реальные refs |

Исходные RU/UK примеры остаются DRAFT/BLOCKED из-за evidence/rights unknown; им не
присваивается ELIGIBLE/READY этим erratum. Остальные исходные records, критерии,
limits и production options не расширяются. Выходные statuses меняются только
там, где прямо помечено SI-R02 или AMEND выше.

## 9. Оставшиеся решения владельца и неизменённые gates

**SI-D01–SI-D10 не утверждены.** Owner + independent review должны рассмотреть
исходный документ и R1 как composite proposal до implementation. Особо требуется:

| Связанные решения | Что именно предлагается утвердить/изменить |
|---|---|
| SI-D02 / SI-R01 | Новые stages/HUMAN_EDIT, fixed method versions и provenance DAG; Run/record ordering, exact vectors и strict mode/stage checks |
| SI-D04–05 / SI-R02 | ELIGIBLE_FOR_CREATIVE независимо от выбора; separate BriefReviewState и explicit Selection scopes/chains/withdrawal, без прав/grants |
| SI-D03 / SI-R03 | Только persisted private Packet; workspace persistence/idempotency lifetime, access/retention/cleanup; никаких выдуманных TTL/backup/security defaults |
| SI-D07 / SI-R03 | Ref-only Packet с redacted views/complete reference manifest, privacy grant scope и запрет raw locator/labels; external sharing остаётся unavailable без отдельного approval |
| SI-D10 | Повторное independent review R1-T01–20 + amended SI-T01–26, затем отдельные bounded задачи |

Эти рекомендации не выбирают production storage policy и не дают native permissions.
R1 не переутверждает D1–D12, E00/A/O и не переписывает работающее editorial ядро.
Automatic machine Candidate export по-прежнему UNAVAILABLE_V1: существующий
manual discovery_method не расширяется, BriefValue не получает hidden SI metadata.

RU/UK, Windows10/11 CPU-only, offline-first, local WAV/stills fallback сохраняются.
Нет live search/model/provider runtime, paid calls, GPU requirements или renderer.
Chinese Writing-DNA/corpora/media/voices/code/weights не переносятся; действуют
[IMPORT_LICENSE_GATE](../../LICENSES/IMPORT_LICENSE_GATE.md),
[UPSTREAM_TECHNOLOGY_IMPORT](../UPSTREAM_TECHNOLOGY_IMPORT.md) и отдельный
release-license checkpoint Edge/Silero/models/fonts/FFmpeg/API/output rights.

Реестр внешних идей остаётся отдельным на
`4ad198a095b155a57d6d0b162fc977260119962b`,
`docs/architecture/EXTERNAL_IDEAS_AND_ADOPTION_REGISTER.md`.
R1 не меняет applicability исходной §12: EXT-01/02 LATER, EXT-03/04
APPLICABLE_AS_IDEA, **не APPROVED**; ничего не merge/cherry-pick/adopt.

## 10. Документационные проверки и STOP

Проверены original/review/task provenance, actual code boundaries read-only,
закрытые modes/stages и coverage всех8 operations, отсутствие circular run/output
и Brief/own-Selection refs, различие stored eligibility/projection и Packet/views,
coverage20 R1 cases и26 original cases, локальные ссылки/таблицы и one-file allowlist.
Выполнены `git diff --check`, exact base/source remote checks; после push проверяются
remote SHA и clean worktree. Это static/document checks, не executed implementation tests.

Создан только `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md`.
Original proposal/review/approved architecture/source/schema/tests/dependencies/CI/
S1/S2/golden/main не изменены. Нет storage/Windows native/model/web/paid operations,
PR/merge/release. S3.2b/S3.3 и программная реализация Story Intelligence не начаты.

**STOP после публикации. PROPOSAL / AWAITING OWNER APPROVAL.**
