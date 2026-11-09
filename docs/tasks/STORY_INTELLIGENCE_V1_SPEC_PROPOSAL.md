# Story Intelligence V1 — Specification Proposal

**PROPOSAL / AWAITING OWNER APPROVAL.** Дата: 2026-11-09 (Europe/Kyiv).
Только спецификация. Все новые типы, API, численные defaults и стадии ниже —
предложения, а не утверждённые executable schemas или разрешение реализации.

## 0. База, приоритеты и сохранённые границы

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-v1-resume-after-s3-2b-hold`.
Exact base: `e8b1b0347853a6f6a62910c65ceb17691fb1dab2`;
FETCH_HEAD и remote HEAD исходной ветки совпали с handoff.
Output branch: `docs/story-intelligence-v1-spec-proposal`.
Создаётся только этот документ; final commit/remote SHA сообщаются в handoff.

Основания:

- [Полное задание](STORY_INTELLIGENCE_V1_CODEX_TASK.md) и
  [возобновление workstream](STORY_INTELLIGENCE_WORKSTREAM_RESUMPTION_2026_11_09.md).
- [Согласованная концепция](../architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md)
  и [ревизия выполненного](STORY_INTELLIGENCE_COMPLETED_STAGES_REVIEW.md).
- E00/1 прочитан из `e520648411b99264688ff66dc61ad0e974201ed3`, файл
  `docs/EDITORIAL_E00_FINAL_SPEC.md` (в текущем дереве этого файла нет);
  [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md), [O1–O10](E01_3_8_1_APPROVED_CONTRACT.md).
- [D1–D12](E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md),
  [S3.2a-R1 ACCEPTED/PURE_ONLY](E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md),
  [S3.2b host hold](E01_3_9_4_S3_2B_PHASE0_HOST_READINESS.md).
- Read-only code inspection: `editorial/model.py`, `graph.py`, `current_package.py`,
  `rights_binding.py`, `approval_history.py`, `versioned_codec.py`,
  `scripts/first_video.py`; RU/UK script prompts и лицензионные gates §12.

Историческое «storage proposal не утверждён» в документах 2026-11-05 описывает
тогдашнее состояние. Позднее D/S1 утверждены, S2 и portable S3.2a-R1 приняты в своих
границах. Это не действующая native service: **S3.2b BLOCKED_HOST_NOT_PROVIDED**.
Story Intelligence не меняет этот статус. PUBLISH_REVISION DISABLED;
partial COMMIT reconstruction OFF. Нет новых storage/authority permissions.

## 1. Полезный V1 и роли

Основной путь: локальный ручной ввод темы/URL metadata/источника → Discovery card
и возможные дубликаты → объяснимая Evaluation → Creative alternatives →
версионированный **pre-script Production Brief** → отдельный editorial review.

V1 предлагает CLI-first локальный рабочий процесс: карточки и сравнение вариантов,
ручную evidence/review работу, прозрачную rubric и шаблоны творческих вопросов.
Он полезен без LLM: пользователь вводит сведения, выбирает ракурс и редактирует
шаблонные альтернативы. Наличие движка не означает автоматический фактчекинг.
Ни сеть, ни GPU, ни оплата, ни скачивание модели для базового пути не требуются.
Target: Windows10/11 CPU-only; фактическая совместимость проверяется будущими tests.

| Роль | Работа в V1 | Граница |
|---|---|---|
| Автор/исследователь | Вводит тему, локальный source snapshot, гипотезы, evidence locators; редактирует карточки | Никакое заполненное поле не создаёт verified fact/rights |
| Редактор | Проверяет central claims, qualifications и соответствие обещания; выбирает angle/brief | SI selection не равен SCRIPT/SCENES/HANDOFF APPROVE |
| Проверяющий права/продюсер | Описывает intended-use, материалы, fallback, ресурсы и недостающие разрешения | SI rights notes не предоставляют отсутствующих прав |
| SI engines | Строят suggestions и diagnostics по зафиксированным входам | Не создают editorial approval/evidence, не вызывают renderer |
| Будущий approved adapter | Предлагает совместимое отображение в editorial draft | Не имеет protected write/grants по факту существования brief |

Один человек может выполнять разные роли, но границы действий сохраняются.
Display name не является OS principal, expertise proof или authorization.
Пользователь явно выбирает варианты/редактирует draft. Творческий выбор и принятие
rubric recommendation называются **selection**, не approval.

V1 отложено: web search/crawling, live trends/YouTube analytics, embeddings/semantic
retrieval, autonomous fact review, LLM/provider runtime, GPU generation, media download,
auto TTS/ASR, editing/render/export/publishing и protected editorial writer.
Online capabilities в offline V1 возвращают UNAVAILABLE_OFFLINE, не пустой «успешный поиск».

## 2. Предлагаемые типы и общие правила SI/1

Это отдельный **SI proposal namespace**, не editorial schema3 и не расширение schema2.
Рабочие SI данные — недоверенные drafts/recommendations; они не являются вторым
editorial authoritative head и не хранят ApprovalAuthorityEvidence/keys/anchor.
Место persistence и export формат требуют решения SI-D03. Предложение: отдельный
user-owned локальный workspace вне Git/production protected roots. Сейчас он не создаётся.

### 2.1 Типы, required/optional/unknown

- `Text`: непустой Unicode, сохраняется буквально; `Locale`: ровно `ru|uk`, не `ua`.
  `UUID`: canonical lowercase hyphenated; `PosInt`: integer≥1, bool запрещён.
  `UTC`: UTC seconds, descriptive, не trusted ordering. `Hash`:64 lowercase hex.
- `SIRef={type,id:UUID,revision:PosInt,sha256:Hash}` — точная immutable SI revision.
  `ERef={kind,id,revision,content_hash}` — прежний полный editorial RevisionRef.
  Эти типы не взаимозаменяемы. SI type не добавляется в existing ObjectKind.
- `Known<T>={state:KNOWN,value:T}` либо `{state:UNKNOWN,reason:Text}`.
  Это закрытый tagged union; UNKNOWN не0/false/empty/«скорее всего». `T?` означает
  required nullable поле: null = явно отсутствующий необязательный элемент, не
  замена неизвестному обязательному факту. Все перечисленные поля присутствуют;
  unspecified fields запрещены. Опциональное содержимое имеет `?`, не скрытые defaults.
- `List<T>` упорядочен как задано, без implicit sorting/deduplication. `[]` означает
  известное отсутствие элементов; неизвестный список — `Known<List<T>>=UNKNOWN`.
- `Confidence={level:LOW|MEDIUM|HIGH|UNKNOWN,basis:Text}` — qualitative judgment,
  не вероятность истинности/успеха. Нельзя HIGH без указанного основания.

Общий header **H** каждой записи таблицы §3:
`si_version=1, type, id, revision, previous:SIRef?, created_at:UTC,
creator_label:Text, origin:Origin, input_refs:List<SIRef>, editorial_refs:List<ERef>`.
`Origin={mode:MANUAL_INPUT|USER_IMPORT|RULE_DERIVED|TEMPLATE_DERIVED|MODEL_DERIVED|RUN_METADATA,
run_ref:SIRef?, imported_from:Known<Text>?}`.
RULE_DERIVED/TEMPLATE_DERIVED/MODEL_DERIVED требуют run_ref; MANUAL_INPUT допускается только для реально ручного
содержимого. USER_IMPORT сохраняет происхождение; неизвестный автор/метод не
превращается в ручную авторскую работу импортирующего пользователя.
RunRecord — корневая запись выполнения: origin RUN_METADATA (только для этого
record type), run_ref=null; method/input provenance живёт в её собственных полях.
RUN_METADATA создаёт harness; этот mode не обозначает ручное discovery. Нужные
manual/import input refs указываются явно, сам факт нажатия «запустить» не делает
автоматический output ручным.

Создание нового объекта — revision1/previous=null; изменение создаёт следующую
revision со ссылкой на предыдущую того же type/id. Immutable recorded revisions
не редактируются. Незавершённый working copy изменяем и ещё не имеет SIRef.
Source refs/порядок/Unicode/числа не нормализуются при сохранении. SI content hash
предлагается SHA-256 canonical UTF-8 JSON с sorted keys/no spaces/no floats
по полному H+payload; сама запись не содержит собственного sha256, он только в SIRef. Это отдельный hash,
**не** editorial revision hash, checksum, attestation или signature. Exact byte vectors
потребуются до будущей реализации codec; никакой редакционный digest не меняется.

Состояние актуальности — вычисляемое `CURRENT|STALE|INVALID`, не authority.
Изменение input revision создаёт новый input set/run; старый run остаётся историей,
не пересчитывается молча. Время не выбирает «правильный» input или editorial decision.
Редактирование machine result человеком сохраняет derivation, даже после selection.

## 3. Каталог предложенных записей

В каждой строке: purpose; **H + закрытый minimal payload**; проверки и граница;
producer→consumer. Поля `?`/Known имеют точный смысл §2.1. Вложенные value types
в этой таблице не самостоятельные записи; вне перечисленных полей extensions нет.

| Record | Минимальные поля payload и проверки | Producer → consumer / purpose |
|---|---|---|
| Intake | `input_kind:TOPIC\|URL_METADATA\|LOCAL_METADATA; raw_input:Text; locale:Locale; supplied_source_refs:List<SIRef>; user_goal:Known<Text>`; URL не fetch; local locator — metadata, не разрешение читать произвольный путь | Человек → Discovery; сохраняет исходную постановку |
| StoryIdea | `intake_ref:SIRef; title:Text; summary:Text; viewer_question:Text; source_refs:Known<List<SIRef>>; candidate_binding:ERef?`; binding только kind=candidate и exact resolve | Discovery/человек → Evaluation/Creative; identity темы, не editorial CandidateRevision |
| SourceItem | `source_kind:URL\|LOCAL; original_locator:Text; title:Known<Text>; author:Known<Text>; publisher:Known<Text>; published_at:Known<UTC>; captured_at:Known<UTC>; material_sha256:Known<Hash>; editorial_ref:ERef?; rights_note:Known<Text>; freshness_requirement:Known<Text>`; ref kind=source, byte snapshot отдельно локально с правами; URL без snapshot не известный material hash | Человек → Evidence/Evaluation; точное происхождение source revision |
| ClaimItem | `statement:Text; claim_kind:factual\|interpretation\|fictional; materiality:CENTRAL\|SUPPORTING\|CONTEXT; evidence_expectation:Text; editorial_ref:ERef?`; claim ref kind=claim, fictional не получает fake evidence | Человек/Creative suggestion → ClaimCheck; тезис и его происхождение |
| EvidenceItem | `claim_ref:SIRef; source_ref:SIRef; relation:supports\|contradicts\|context\|insufficient; locator:Known<Text>; explanation:Text`; exact source revision, page/section/timecode, не просто URL | Исследователь → ClaimCheck; evidence link как предложение, без выдуманного reviewer |
| ClaimCheck | `claim_ref:SIRef; evidence_refs:Known<List<SIRef>>; state:unreviewed\|supported\|disputed\|unverified\|qualified\|removed; qualification:Text?; reviewer_label:Text?; reviewed_at:UTC?; reason:Text?`; unreviewed: вся review metadata null; остальные требуют human reviewer/time/reason; qualification только qualified; supported/qualified требуют KNOWN nonempty evidence_refs и проверенного человеком exact evidence/locator/material snapshot | Человек → Evaluation/Brief; SI human-review assertion, не trusted editorial approval |
| AudienceHypothesis | `locale:Locale; region:Known<Text>; knowledge_level:Known<Text>; motivation:Known<Text>; interests:Known<List<Text>>; age_range:Known<Text>; basis_refs:List<SIRef>; assumptions:List<Text>`; нельзя делать демографическую статистику из assumption | Человек → Evaluation/Creative; контекст, не inferred audience analytics |
| ChannelContext | `channel_alias:Text; purpose:Text; audience_ref:SIRef; constraints:List<Text>; portfolio:Known<List<PortfolioEntry>>; analytics:Known<Text>; capability_notes:Known<Text>`; PortfolioEntry=`story_ref:SIRef,published_title:Text,published_locator:Known<Text>,published_at:Known<UTC>,angle_notes:Text,basis_ref:SIRef`; story_ref — StoryIdea/Brief, basis_ref — manual Intake/source metadata; не live platform scan | Человек → Discovery/Evaluation; стратегия/известный портфель |
| Angle | `idea_ref:SIRef; audience_ref:SIRef; question:Text; thesis:Text; claim_refs:List<SIRef>; distinction:Text; limitations:List<Text>`; thesis — proposal, не автоматически факт | Creative/человек → Evaluation/Brief; альтернативная постановка |
| Rubric | `method_id:Text; method_version:Text; criteria:List<Criterion>; missing_policy:ALL_REQUIRED; blocker_policy_version:Text`; Criterion=`key,description:Text,weight_percent:Int0..100,min=0,max=5,direction=HIGH_IS_BETTER`; unique keys, сумма весов100 | Owner-defined configuration → Evaluation; все defaults §5 PROPOSAL |
| RunRecord | `stage:DISCOVERY\|EVALUATION\|CREATIVE; method_id:Text; method_version:Text; input_snapshot:List<SIRef>; editorial_snapshot_sha256:Known<Hash>; rubric_ref:SIRef?; provider:Provider?; started_at:UTC; finished_at:UTC; confidence:Confidence; fresh_trends:Known<Text>; caveats:List<Text>`; Provider=`id,version,model_id,model_version:Known<Text>,config_digest:Known<Hash>`; provider=null для правил/ручного/шаблонов; EVALUATION требует rubric_ref | Engine/harness → audit/display; замороженные входы и воспроизводимый method context |
| EvaluationReport | `idea_ref,angle_ref,audience_ref,channel_ref,rubric_ref,run_ref:SIRef; ratings:List<Rating>; risk_refs:List<SIRef>; recommendation:Recommendation; aggregate_tenths:Known<Int0..1000>; caveats:List<Text>`; Rating=`criterion_key:Text,value:Known<Int0..5>,basis_refs:List<SIRef>,explanation:Text,confidence:Confidence`; ровно rubric keys/order; агрегат по §5, не editorial assessment wire | Evaluation → человек/Brief; объяснимые раздельные суждения |
| CreativeAlternative | `angle_ref,run_ref:SIRef; hook_strategy:QUESTION\|HUMAN_STAKES\|COUNTERINTUITIVE; hook_text:Text; hook_claim_refs:List<SIRef>; title_options:List<Text>; thumbnail_notes:Text; chapters:List<Chapter>; retention_0_30:Text; style_constraints:List<Text>; omitted_strategy_reason:Text?`; Chapter=`heading,purpose:Text,claim_refs:List<SIRef>,target_seconds:PosInt`; список — план, не ScriptSegment/Scene ranges | Creative/человек → Selection/Brief; сравнимые творческие предложения |
| VisualRequirement | `chapter_index:PosInt; role:REQUIRED\|LOCAL\|OPTIONAL; description:Text; acquisition:LOCAL_CREATE\|USER_SUPPLIED\|TO_SOURCE; source_refs:List<SIRef>; material_sha256:Known<Hash>; rights_state:UNKNOWN\|NEEDS_REVIEW\|DOCUMENTED; intended_use:Text; licence_basis:Known<Text>; effort:Known<LOW\|MEDIUM\|HIGH>; fallback:Known<Text>; asset_ref:ERef?`; asset ref kind=asset; DOCUMENTED означает наличие основания, не grant; REQUIRED без usable lawful fallback блокирует | Creative/продюсер → риски/Brief; visual dependencies |
| Risk | `category:SCIENTIFIC\|LEGAL\|ETHICAL\|REPUTATIONAL\|PRODUCTION\|MARKET; severity:LOW\|MEDIUM\|HIGH\|CRITICAL; blocking:bool; basis_refs:List<SIRef>; description:Text; mitigation:Text; resolution:OPEN\|MITIGATED\|UNRESOLVED; resolution_basis_refs:List<SIRef>; owner_role:Text`; MITIGATED требует human-recorded resolution_basis_refs, mitigation text не сама по себе resolution; блокирующий unknown не скрывается | Evaluation/человек → Brief/recommendation; отдельный от score барьер |
| ProductionBrief | `idea_ref,audience_ref,channel_ref,angle_ref,evaluation_ref,creative_ref:SIRef; locale:Locale; content_mode:factual\|fictional\|hybrid; intended_use:Known<Text>; promise:Text; duration_min_s,duration_max_s:PosInt; intensity:CALM\|BALANCED\|DYNAMIC; source_refs,claim_refs,claim_check_refs,visual_refs,risk_refs:List<SIRef>; required_reviews:List<Text>; must_avoid:List<Text>; profile_ref:ERef?; production:ProductionOptions; workflow_state:DRAFT\|IN_REVIEW\|WITHDRAWN; unresolved:List<Text>`; min≤max, источники и обязательные claims перечислены точно; profile kind=genre_profile; все central claims должны иметь checks хотя бы unreviewed | Человек + explicit assembly → отдельный editorial review; самостоятельный pre-script brief |
| Selection | `target_ref:SIRef; choice:SELECT\|REQUEST_CHANGES\|WITHDRAW; selector_label:Text; reason:Text`; это immutable авторский выбор, без gate/APPROVE/grants. Brief selection требует CURRENT и отсутствия блокеров, иначе допустим только запрос правок | Человек → display/Brief selection projection; не ApprovalRecord |
| ReviewPacket | `brief_ref:SIRef; input_refs:List<SIRef>; existing_editorial_refs:List<ERef>; unresolved:List<Text>; format_version=si-review-packet/1; purpose=DISCUSSION_ONLY`; содержит всю ссылочную closure, не credentials/media binary, не render manifest | Read-only projection → будущий approved adapter/человек; draft export proposal |

`ProductionOptions` (value): `output_preset:VERTICAL_720x1280|HORIZONTAL_1280x720;
script_locale,narration_locale,subtitle_locale:Locale; tts:LOCAL_WAV|OPTIONAL_SILERO;
asr:NONE|FUTURE_OPTIONAL; editing:LOCAL_STILLS_FFMPEG_PLAN;
voice_ref:Known<Text>; resource_budget:Known<Text>; cpu_fallback:Text;
optional_provider_notes:List<Text>`.
Языки script/narration/subtitles обязаны совпадать с Brief.locale; UI locale отдельно
в интерфейсном request. Нельзя передать модель/голос как «разрешённые» из одного имени.

### 3.1 Целостность предложенной модели

Для non-circular hashes ClaimItem **не** содержит refs на EvidenceItem/ClaimCheck:
EvidenceItem ссылается на уже записанные ClaimItem и SourceItem, ClaimCheck — на
них и EvidenceItem. Adapter позднее сможет собрать existing ClaimRevision с
EvidenceLink (который сам содержит только source_ref), без изменения его схемы.
RunRecord содержит только inputs/method/final timing/confidence, **не output refs**.
Сначала вычисляется результат в working memory, затем записывается RunRecord,
затем output revisions с его SIRef. Ответ/packet перечисляет outputs отдельно.
Это сохраняет DAG; link к run не требует cyclic content hashes. Run input_snapshot
не может включать результаты этого же run. До codec implementation нужны literal
vectors именно для этого порядка, не выдуманные hash placeholders.

Brief.workflow_state не содержит выбранность. `selection_state` — read-only
projection NOT_SELECTED или SELECTED_FOR_EDITORIAL_REVIEW по Selection.target_ref
того же exact Brief. Brief bytes от SELECT не меняются. Новый Brief revision требует
нового SELECT; старое решение не переносится. `editorial_approval_state` в V1
показывается отдельно как NOT_EVALUATED (не stored permission): SI не оценивает
эффективность существующих editorial approvals и не выдаёт новых.

Все ссылки должны resolve exact type/id/revision/hash в переданном SI input set;
no dangling/self refs и циклов derivation. Lists evidence/claims/chapters сохраняют
порядок. Review state и Selection — отдельные записи с provenance, не мутируемые
поля «verified/approved» в Idea. Изменение claim/source/angle/audience/profile/rights
input делает зависимые отчёты, creative и brief STALE для новой current selection.
Старые results остаются доступными с exact refs, но не переносятся на новые inputs.
После изменения требуется новый run/review/selection; старый SELECT не оживляет
старый editorial APPROVE/REVOKE. Права дополнительно проверяются на intended-use
и дату использования, даже если frozen source bytes прежние.

Предлагаемые ограничения SI/1 для owner approval: текстовое поле≤100000 code points,
объект≤1000000 UTF-8 bytes, один переданный bundle≤16MiB/1000 records/depth32,
не более50 источников/100 claims на Idea,20 chapters/20 visual requirements на Brief.
Превышение — LIMIT без truncation. Это **SI proposal limits**, не изменение E00/S1
и не обещание скорости/памяти. Derived provider output не обходит лимиты.

## 4. Discovery offline и дедупликация

1. Человек задаёт locale, viewer question и topic либо source metadata. Сохранить
   original input отдельно от поискового ключа. URL не fetch; local metadata не
   открывает файл. Чтение выбранного локального материала — отдельное явное действие
   после согласования import/privacy interface. Без bytes digest=UNKNOWN.
2. Discovery создаёт карточку и список missing sources. Нет сети: `RunRecord.fresh_trends=UNKNOWN`
   с пояснением в caveats/diagnostics, не «трендов нет». Если задача требует сегодняшних
   данных — NEEDS_INPUT; для evergreen допустима работа с caveat о свежести.
3. Versioned `dedup/1` предлагает сравнение только локального supplied portfolio:
   exact material digest; lookup-title key (NFC+casefold+collapse spaces только для
   поиска, никогда для record/hash); URL lookup key lowercases scheme/host и default
   port, сохраняет path/query/fragment и original URL. Не объединять http/https,
   разные query или локальные пути только по filename.
4. Совпадение материала — possible shared source, не одинаковая история. Совпадение
   нормализованного title — DUPLICATE_CANDIDATE suggestion. Разные вопросы/периоды/
   audience/angles требуют человеческого сравнения. Ничего не удалять/сливать автоматически.
   Portfolio=UNKNOWN не доказывает novelty. Решение о distinct story фиксируется
   новой Angle/Selection с reason; auto decision не маскируется под ручной discovery.

V1 не обещает embeddings или мультиязычную семантическую дедупликацию; RU и UK title
без lexical match могут быть одной темой. Пользователь может явно связать их через
общую Idea и разные localized Angle revisions; переведённый текст — новый input,
а не автоматическое подтверждение facts/review на другом языке.

## 5. Evaluation: отдельные критерии и блокеры

### 5.1 Предложенная rubric `si-rubric/1` — НЕ УТВЕРЖДЕНА

Все ratings0..5, выше=лучше для разработки в заданном контексте. Общие anchors:
0 — обоснованно непригодно;1 — серьёзные ограничения;2 — слабое соответствие;
3 — приемлемо с указанными ограничениями;4 — хорошо обосновано;5 — особенно сильное
соответствие **в этой rubric**, не прогноз аудитории. UNKNOWN не оценивается нулём.

| Критерий | Вес, proposal | Основание конкретной оценки |
|---|---:|---|
| audience_interest |15| Чёткая человеческая мотивация/вопрос, evidence либо помеченная owner hypothesis; не выдуманная статистика |
| channel_fit |10| Exact ChannelContext цель/язык/ограничения |
| angle_novelty |10| Что нового в framing относительно предоставленного portfolio; unknown portfolio → UNKNOWN |
| evidence_quality |20| Exact sources/locators, противоречия и human ClaimChecks; много URL не означает высокий балл |
| narrative_potential |15| Понятный вопрос, объяснимая последовательность/контрасты без искажения claims |
| visual_feasibility |10| Законно доступные обязательные visuals, local alternatives, отдельно от красоты |
| resource_fit |10| Реальные ограничения человека/CPU/доступных материалов; LOW effort лучше HIGH при прочих равных |
| risk_manageability |5| Научные/правовые/этические/репутационные mitigation с основаниями; не отменяет blockers |
| portfolio_distinctness |5| Отличие и баланс известного портфеля; duplication, а не обещание спроса |

Повышенный evidence weight отражает цену неподтверждённого factual сценария;
интерес/fit и narrative раздельны, novelty и portfolio не заменяют друг друга.
Весам нельзя приписывать эмпирическую калибровку. Effort=qualitative band с объяснением
шагов; неизвестная цена не становится «бесплатно». Часы/бюджет — только явный
user-supplied resource_budget с units, не измеренная производительность движка.

Rating требует explanation, basis refs и confidence; если источником суждения
является AudienceHypothesis, это видно. Нет данных → UNKNOWN(reason), не guessed3.
При всех известных ratings aggregate_tenths = 2 × сумма(weight_percent × rating),
целое0..1000, UI показывает /10 как rubric points0..100. Это не проценты успеха.
При любом UNKNOWN aggregate=UNKNOWN; известные критерии показываются раздельно,
без renormalization весов или сравнения с complete scores. Unknown confidence
и актуальность inputs отображаются независимо. У V1 нет score threshold,
автоматически разрешающего следующую стадию; rank — подсказка редактору.

### 5.2 Строгий приоритет рекомендаций

`Recommendation` — ровно `BLOCKED|NEEDS_INPUT|NEEDS_RESEARCH|REVIEW_DUPLICATE|
REVISE_CREATIVE|PROCEED_TO_BRIEF_REVIEW`; у каждого результата сохраняются все reasons,
primary reason выбирается по порядку ниже, не по score.

1. Неверная schema/ref/hash/locale или STALE inputs: validation failure/STALE diagnostic,
   без current recommendation/rank. Никакого частичного «готового brief».
2. Open blocking Risk: BLOCKED, независимо от полного высокого score.
   Обязательные blockers: unsupported/disputed/unqualified central factual claim;
   неясные/запрещённые права на незаменимый материал; существенный scientific/ethical
   риск без проверенной mitigation; обязательная capability без CPU fallback.
3. Нет постановки/audience/required current-data/context: NEEDS_INPUT.
4. Нет non-central evidence/точного locator/freshness determination: NEEDS_RESEARCH.
   Central missing evidence также BLOCKED по пункту2, next action — research.
5. Possible/exact duplicate без человеческого различения: REVIEW_DUPLICATE.
6. Несовместимый hook/creative с facts либо отсутствуют пригодные alternatives:
   REVISE_CREATIVE. Если hook уже утверждает unsupported central fact, пункт2 выше.
7. Только при достаточных inputs/reviews, без blocker/stale/duplicate uncertainty и
   при ручном выборе — PROCEED_TO_BRIEF_REVIEW. Это review suggestion, не permission.

Removed claim, остающийся фактической фразой в hook/brief, продолжает блокировать.
Qualified claim допускается только с человечески проверенной qualification, видимой
в exact text; disputed не «перевешивается» sources count.
Описание возможного fallback само по себе не разрешает Risk: нужна проверенная
человеком feasibility/rights basis в resolution_basis_refs и новая current revision.
План будущего локального изготовления не выдаётся за существующие staged bytes. Unknown rights essential
блокируют; optional visual можно исключить явно новой revision, не объявив его licensed.

## 6. Creative и самостоятельный pre-script brief

Для пригодной постановки — минимум3 разных strategies, а не три перестановки слов:
вопрос/объяснительная задача, human stakes без вымышленных фактов, контринтуитивная
проверяемая гипотеза. Если стратегия искажает evidence, вместо fake third hook
зафиксировать omitted_strategy_reason и NEEDS_RESEARCH/REVISE_CREATIVE.
Каждую альтернативу можно выбрать только явно, сохранив rejected alternatives.

Hook/title/thumbnail/chapters связываются с ClaimItem и exact evidence context.
Не вводить новый central factual тезис ради драматургии. 0–30s retention — текстовая
гипотеза о ясности обещания/вопроса/перехода; никаких fictitious retention/viral rates.
Natural RU/UK: конкретный вопрос, короткие связи, человеческий ритм; убрать пустые
«в этом невероятном путешествии», угрозы «вы всё знали неправильно», неподтверждённые
сенсации и кальки. Сохранять числа, имена, даты, цитаты и qualifiers; расхождение
возвращается на ClaimCheck, не исправляется незаметно языковым проходом.
Существующие locale prompts требуют оригинальности; они не реализуют Creative Engine.

Brief собирает audience/channel/angle/evaluation/creative exact revisions, promise,
целевые duration/intensity/locale, source/claim/check refs, required reviews,
chapters через creative_ref, visual priorities/rights/fallbacks, resource constraints
и production options. В DRAFT допускаются unresolved refs только как working copy;
recorded refs должны resolve (§2). Проекция SELECTED_FOR_EDITORIAL_REVIEW — current human
selection при отсутствии blockers, не APPROVED, не frozen production manifest.
8–12 минут — цель, не обещанная длительность: фактическое WAV timing — позже.

## 7. Совместимость с существующими типами и pipeline

| Существующий executable тип/граница | Допустимое соответствие после отдельного adapter approval | Неподдержанная часть / отказ |
|---|---|---|
| CandidateRevision | title/summary/source_refs; только явно ручные input поля → manual_topic/manual_url/manual_local и discovery_input; совместимые ручные CriterionRating0..5 по exact profile rubric | Нет machine discovery/run/provenance поля. Derived data нельзя маркировать manual; автоматический Candidate export **UNAVAILABLE_V1**, пока не утверждён provenance mapping. User selection не очищает derivation |
| GenreProfile / RubricCriterion | profile_ref,0..5, weight_percent total100; сравнить exact keys/profile version | SI rubric/run не заменяют review_policy_version/authority policy. Existing constructors не проверяют полный evaluation-run contract |
| SourceRevision + SourceDetails | title/locator + right-bound source ref; author/publisher/dates/notes и material_digest в своих существующих полях | Source production-scoped; SI workspace не глобальный editorial catalogue. Без полного RightsReview/companion/subject binding adapter не выпускает partial SourceRevision |
| ClaimRevision / EvidenceLink / ClaimReview | statement/type/materiality, exact source ref и locator/relation; настоящий human review metadata/qualification отдельно | SI evidence suggestion без reviewer/time не EvidenceLink. Unreviewed не заполняется фиктивным reviewer; machine report не supported fact |
| RightsReview + RightsDetails / AssetRevision | future exact subject(kind/id/revision), material digest, intended-use/actions/expiry/review basis; real staged bytes для asset | CONFIRMED rights_binding означает только material match; не licence/expiry/rights grant. SI rights DOCUMENTED не равно existing approved или разрешению |
| BriefValue | revision,audience,angle,promise,must_include_claim_refs,must_avoid,profile_ref | Это вложенный script value, не самостоятельный pre-script brief. Duration/resource/runs/options/variants не помещаются в него и не кодируются JSON внутри rationale/reason |
| ScriptRevision / ScriptSegment | После отдельного script task exact production_ref/candidate_ref/brief/locale; segments с existing roles opening/body/closing/other и claim refs | Brief chapters не готовый script. Script claim_refs — sorted unique union segment refs, не произвольный набор всех research claims |
| ScenePlanRevision / Scene | После точного script: continuous ranges0..len(approved text), narration=exact slice, still visual_kind; actual assets/rights | Brief outline/time estimates не Scene ranges. estimate_ms не измеренный бюджет; paraphrase narration требует новой ScriptRevision |
| graph/current_package/versioned_codec | Existing full RevisionRef resolution, no missing/hash/cycle/foreign-production; coherent active SCRIPT(root script), SCENES/HANDOFF(root scene_plan) | Coherent package и checksum не truth/authority. SIRef/new SI fields не принимаются strict schema1/2 codec |
| approval_history + schema2 evidence | Сохранить existing decision keys, negative history, ambiguity и distinct policy versions | Ни время SI run, ни SI Selection не ApprovalRecord/effective authority; old APPROVE не воскресает после REVOKE |
| scripts/first_video.py | При будущем approved production adapter: title,locale,scenes[{text,image?}],1..20 scenes,≤2000 code points/scene,PNG/JPG/JPEG/PPM basename; local WAV либо trusted local Silero | Не читает editorial authority/approval; прямой build не является handoff gate. Нет генерации произвольных AI video assets |

Существенная **интерфейсная несовместимость**, а не дефект работающего кода:
полный SI Brief/run/machine provenance нельзя без потерь выразить текущими
CandidateRevision/BriefValue. Нужен отдельный утверждённый SI draft/adapter contract;
переписывание завершённых этапов не требуется. Неподдержанные payloads отклоняются,
а не размещаются в `reason`/`rationale` и не добавляются в editorial snapshot.

Будущий handoff: read-only ReviewPacket → явно авторизованная редакционная работа
с полноценными production/profile/candidate/source/claim refs → script/review → scenes/
review → editorial HANDOFF → **отдельные** rights/capability/staging/config readiness
и pre-render revalidation. Даже editorial HANDOFF не разрешает render/export/commercial.
При отсутствии approved protected write path — HANDOFF_ADAPTER_UNAVAILABLE,
без fallback local writer; PUBLISH_REVISION не открывается этой спецификацией.
Manual editorial workflow существующих структур не объявляется operational protected service.

E00 default нового production9:16,720×1280; explicit16:9,1280×720. У first_video остаётся
его default1280×720, поэтому adapter должен передавать dimensions явно. Длительный
editorial draft возможен, даже если production adaptation не помещается в1..20/2000:
нужны явное новое разбиение/версия или CAPABILITY_BLOCKED, не скрытое обрезание.
Сценическое WAV timing и subtitles делаются на exact final text. ASR — deferred,
не источник fictional factual approval и не исправляет текст молча.

## 8. Предлагаемый interface `story-intelligence/1`

Это **декларативный shape**, не CLI/HTTP server, не исполняемый код и не S1 Request.
Transport/JSON schema/persistence утверждаются отдельно. Никакого сетевого endpoint V1.

H.type равен имени Record из §3, с тем же регистром. Resolver получает от локального
harness read-only input set и, при наличии ERefs, exact validated editorial snapshot
с его checksum/full-file hash context; это не произвольный path/URL из Request.
Нет неявного resolve-latest. ERef без supplied snapshot → REF_MISSING; hash context
неизвестен при ERefs → INVALID. Input set/run фиксируют все используемые exact refs.
UI current selection задаётся явно; проверка STALE сравнивает новые выбранные inputs
с frozen run/brief inputs, не переписывает старые refs. Import/export файлов и trusted
local path policy — отдельная часть SI-D03/SI-D07, не автоматическое чтение locator.

```text
Request = {interface_version:1, request_id:UUID, operation:Operation,
           input_refs:List<SIRef>, editorial_refs:List<ERef>,
           ui_locale:ru|uk, options:OperationOptions}
Response = {interface_version:1, request_id:UUID,
            result:OK|NEEDS_REVIEW|STALE|INVALID|UNAVAILABLE,
            output_refs:List<SIRef>, diagnostics:List<Diagnostic>}
Diagnostic = {code:Code, field_path:Text, input_ref:SIRef?, message:Text}
```

| Operation | Закрытые options / outputs |
|---|---|
| RECORD_INPUT | `record_type:Intake\|SourceItem\|ClaimItem\|EvidenceItem\|ClaimCheck\|AudienceHypothesis\|ChannelContext\|Angle\|Rubric\|VisualRequirement\|Risk\|CreativeAlternative\|ProductionBrief, working_copy:соответствующий §3 payload`; output exact ref. Это closed manual/import record set, не arbitrary JSON и не editorial write |
| REVISE_INPUT | `base_ref:SIRef,replacement_payload:тот же record type`; output следующая revision, previous=base_ref; сохраняет derivation/import ancestry. RunRecord и Selection здесь не редактируются |
| DISCOVER_LOCAL | `portfolio_ref:SIRef?`; output StoryIdea + RunRecord, diagnostics duplicate/missing/trends |
| EVALUATE | `rubric_ref:SIRef`; explicit Idea/Angle/Audience/Channel в input_refs; output EvaluationReport+RunRecord |
| PROPOSE_CREATIVE | `strategy_set:QUESTION_HUMAN_STAKES_COUNTERINTUITIVE`; output alternatives+RunRecord; только supplied claims |
| ASSEMBLE_BRIEF | `production_options:ProductionOptions`; все выбранные refs в input_refs; output DRAFT Brief |
| RECORD_SELECTION | `target_ref:SIRef,choice:SELECT\|REQUEST_CHANGES\|WITHDRAW,reason:Text`; output Selection; только user intent, не auth evidence |
| EXPORT_REVIEW_PACKET | `brief_ref:SIRef`; output discussion-only ReviewPacket, всё unresolved видно |


RECORD_INPUT/REVISE_INPUT — редактирование только SI workspace, не schema2 snapshot.
Header type/creator/provenance не принимается как authority: harness фиксирует
фактический метод записи, сохраняет previous/input ancestry и не позволяет стереть
derived origin при ручной правке. ClaimCheck требует отдельного явного human action;
PROPOSE_CREATIVE не может выдать reviewed state. UNKNOWN source/evidence сохраняется
как UNKNOWN, не изобретается из шаблона. RunRecord создаёт только stage operation,
а не generic record input. Перед будущим implementation нужно утвердить exact request
bytes/limits и provenance fixtures по SI-D02; это не готовый production command protocol.

`Code` — предложенный closed vocabulary: TYPE, UNKNOWN_FIELD, MISSING_FIELD,
VERSION_UNSUPPORTED, LIMIT, REF_MISSING, REF_HASH_MISMATCH, REF_TYPE_MISMATCH,
DEPENDENCY_CYCLE, LOCALE_MISMATCH, INPUT_STALE, EVIDENCE_NEEDED,
CENTRAL_CLAIM_UNSUPPORTED, RIGHTS_BLOCKED, DUPLICATE_REVIEW_NEEDED,
HOOK_FACT_CONFLICT, CAPABILITY_BLOCKED, UNAVAILABLE_OFFLINE,
HANDOFF_ADAPTER_UNAVAILABLE, REQUEST_CONFLICT.
Messages localized, field_path и code стабильны. No auto-fix/partial accepted output
при INVALID. NEEDS_REVIEW может вернуть только явно draft suggestions с diagnostics,
не current selected Brief. STALE не заменяет старые frozen inputs новыми.

Request idempotency предлагается для локального draft workspace: тот же request_id
и exact canonical request bytes возвращает те же записанные refs; другой payload
с тем же ID — REQUEST_CONFLICT. Никакой editorial authority/transaction sequence
или crash-durable receipt от этого не следует. Canonical bytes сохраняют Unicode/
порядок, canonical означает только описанное deterministic encoding, не исправление полей. Content operations получают caller identity только как
неавторитетный label в локальном harness; user JSON не выдаёт grants.

## 9. Полный иллюстративный RU кейс

**ILLUSTRATIVE / NOT FACTUAL RESEARCH / NOT EXPORTABLE FIXTURE.**
Тема: **«Почему исчезли древние цивилизации?»**; science_technology,
factual, locale ru; duration480..720s (8–12min), intensity BALANCED,
вертикальный720×1280, narration/subtitles ru, UI по выбору.
Ни исследования, ни источники фактически не прочитаны в этом задании.
Далее `I-RU@1`, `S-RU1@1` и т.п. — **символьные draft aliases**, не UUID/hash
и не утверждённые editorial refs. Полная product case показана для согласования;
strict API должен отклонять такие aliases как SIRef до создания реальных revisions.
Пустые ссылки не заменяются fake hashes, page numbers или bibliographic citations.

### 9.1 Input, аудитория, источники и проверки

Intake I-RU@1: manual_topic, raw title как выше; user goal — «понятно объяснить,
как разбирать разные истории перемен без единственной эффектной причины».
Idea C-RU@1: viewer question «Что именно мы называем исчезновением: город,
государственный порядок, язык, людей — и по каким данным это различаем?».
Source refs/evidence snapshot: UNKNOWN — actual research ещё не выполнено.

Audience A-RU@1 — **owner assumption**, не данные канала: русскоязычный взрослый
зритель без специальной археологической подготовки; интерес к научным объяснениям;
регион/возрастной диапазон/analytics UNKNOWN. Channel K-RU@1: спокойное science
объяснение, без мистики/сенсационности; portfolio UNKNOWN, novelty не доказана.
Angle G-RU@1: «уточнить значение исчезновения и сравнить критерии объяснения».
Альтернативы: «как проверять конкурирующие причины»; «как отличать изменение
политического устройства от исчезновения людей». Оба — research framing, не факты.
Scope — не более2 кейсов после проверки источников; возможные направления поиска:
города майя и общества позднего бронзового века. Периоды/места/сопоставимость **UNKNOWN**,
окончательный выбор не сделан. Если нельзя сравнить добросовестно — один narrowed case.

| Draft SourceItem | Нужный материал / locator / состояние |
|---|---|
| S-RU1@1 | Академический обзор терминов collapse/transformation; actual author/title/version/URL/page/hash UNKNOWN; evidence-needed |
| S-RU2@1 | Исследование выбранного региона/периода первого кейса; chronology/method/locator/hash UNKNOWN |
| S-RU3@1 | Независимый разбор альтернативных объяснений/второго кейса; bibliography/data/locator/hash UNKNOWN |

Это research tasks, не существующие проверенные SourceRevision. Права всех будущих
source extracts/изображений UNKNOWN; запись bibliographic fact не предоставляет
разрешения на screenshot/quote/illustration. Required human checks: scientific
terminology, chronology, distinction evidence/inference, counter-evidence и source rights.

| Draft ClaimItem | Review / relation / обязательное evidence |
|---|---|
| Q-RU1@1 CENTRAL factual | Предположение для проверки: «в выбранном кейсе политическая перемена не равнозначна исчезновению всего населения». UNREVIEWED; evidence-needed S-RU1/S-RU2; locator/material hash UNKNOWN |
| Q-RU2@1 CENTRAL interpretation | «Объяснения выбранных кейсов следует сравнивать по нескольким конкурирующим факторам». UNREVIEWED; supports/contradicts не присвоены, нужна проверка S-RU1/S-RU3 |
| Q-RU3@1 SUPPORTING factual | Будущая конкретная датировка/последовательность событий первого кейса — statement ещё working copy, значения UNKNOWN; нельзя вставлять дату до проверки |

EvidenceItem пока не создан: relation/точные locators нельзя изобрести. ClaimChecks
для сформулированных Q-RU1/Q-RU2 — unreviewed, reviewer/time/reason null;
Q-RU3 ещё не recorded ClaimItem. Brief.unresolved это явно перечисляет.

### 9.2 Три действительно разных hook drafts

1. **QUESTION / интеллектуальный:** «Что должно исчезнуть, чтобы мы сказали:
   цивилизация закончилась? Город, власть — или люди? Начнём с этого различия».
   Ссылка Q-RU1; финальная factual формулировка требует scientific review.
2. **HUMAN_STAKES / человеческий масштаб:** «Представьте знакомый город, из которого
   уходят привычные учреждения. Осталась ли прежней жизнь людей? Это мысленный
   пример, с которого мы подойдём к историческим данным». Это явно hypothetical
   illustration, не реконструкция конкретного древнего события; не показывать как архив.
3. **COUNTERINTUITIVE / проверяемый вопрос:** «А если слово “исчезла” скрывает несколько
   разных историй? Проверим, что известно, что предполагается и где остаётся спор».
   Не утверждает универсальное выживание/единую причину; Q-RU1/Q-RU2 evidence-needed.

Title alternatives: «Что значит “исчезла цивилизация”?»;
«Как проверять объяснения древних перемен». Thumbnail: собственная схема
«город / власть / люди» с вопросительным знаком; без fake разрушений и сенсационного
«доказано!». Выбранный working creative draft CR-RU1@1 — QUESTION, human selection
ещё отсутствует. Остальные сохраняются как альтернативы, не стираются.

0–30s hypothesis:0–8s конкретный вопрос;8–18s назвать различие понятий без fake fact;
18–30s обещать сравнение данных и границ знания. Это качественная структура,
не измеренный retention и не обещание успеха.

### 9.3 Chapters, visuals и производство

План на600s — цель10min, не измеренный WAV:

| Глава / цель | Секунды | Claims / visual priority |
|---|---:|---|
|1. Что означает вопрос |30| Q-RU1; LOCAL собственная типографическая схема |
|2. Термины и пределы сравнения |60| Q-RU1/Q-RU2; REQUIRED понятная схема определений, создание локально |
|3. Какие данные потребуются |90| Q-RU2; LOCAL таблица «источник / вывод / неизвестное» |
|4. Первый выбранный кейс |120| Q-RU1/Q-RU3 после проверки; REQUIRED собственная карта/хронология по lawful verified data |
|5. Конкурирующие объяснения |120| Q-RU2; LOCAL сравнительная диаграмма, не выдуманные измерения |
|6. Второй кейс либо углубление первого |120| Q-RU2; OPTIONAL музейное фото только после licence review; fallback собственная схема |
|7. Что мы можем и не можем заключить |60| Только проверенные/qualified claims, видимые caveats |

Visual V-RU1@1 — REQUIRED chapter2 local diagram, rights NEEDS_REVIEW для выбранных
fonts/icons, fallback plain text с разрешённым шрифтом. V-RU2@1 — REQUIRED chapter4
map/timeline: данные/точность/лицензия UNKNOWN, fallback самостоятельная schematic
map только после проверки источников; до этого blocker. V-RU3@1 — OPTIONAL museum
image: rights UNKNOWN; excluded from production пока нет оснований, не essential.
Не использовать чужую карту/screenshot как «собственную» после перерисовки.

ProductionOptions: LOCAL_WAV как независимый offline input; OPTIONAL_SILERO только
после проверки exact model/voice/license/trust. Edge в offline V1 UNAVAILABLE,
ASR NONE, editing LOCAL_STILLS_FFMPEG_PLAN, CPU fallback — собственные still diagrams
+ local WAV + captions по exact final script. Effort MEDIUM **assumption** для схем,
research effort UNKNOWN; budget UNKNOWN; никакого обещания render-time.
Текст script/segments/scenes и exact assets ещё не созданы. Chapter не обязан быть
одной сценой; будущий adapter проверяет ≤20 scenes/2000 chars и timing.

### 9.4 Evaluation и итоговый draft Brief

Run R-RU-E1 — proposed evaluation/si-rubric1 по I/C/A/K/G drafts; provider=null,
method/rubric version фиксируются при записи, confidence LOW; источник input snapshot
ещё draft, actual editorial_snapshot_sha256 UNKNOWN. В примере допустимы лишь
предварительные human judgments, не recorded executable EvaluationReport.

Предварительно audience_interest3 и channel_fit4 — основаны только на A/K assumptions;
narrative_potential3 — по outline; evidence_quality UNKNOWN,
angle_novelty/portfolio_distinctness UNKNOWN (нет portfolio), visual_feasibility/
resource_fit/risk_manageability UNKNOWN. aggregate UNKNOWN, **не0 и не среднее известных**.

Blocking risks: R-RU1 scientific — центральные claims не проверены;
R-RU2 production/legal — essential map evidence/rights/fallback ещё не определены.
Non-blocking open R-RU3 reputational — misleading disappearance framing; mitigation
explicit definitions/uncertainties и human review. Duplication status UNKNOWN.
Высокая привлекательность темы не снимает blockers.

Brief B-RU@1 working copy: audience A-RU, channel K-RU, angle G-RU, creative CR-RU1,
evaluation R-RU-E1, promise «разобрать способы проверки объяснений, не обещая одной
причины для всех случаев», ru/factual/BALANCED/480..720s, source/claim/check refs
ещё unresolved draft aliases выше, chapters и visuals как в таблицах, intended-use
образовательное (commercial use UNKNOWN), resource_budget UNKNOWN.
Must-avoid: единственная универсальная причина; неподтверждённые даты/числа;
«люди исчезли» без evidence; художественные кадры как документальные; fake citations.
Profile_ref — требуется actual science_technology GenreProfile revision, не фиктивный ERef.
Required reviews: scientific, counter-evidence/qualifications, rights/font/map,
language, capability/staging перед будущим production, ordinary editorial gates отдельно.
workflow_state DRAFT, selection_state NOT_SELECTED, editorial_approval_state NOT_EVALUATED, Recommendation **BLOCKED**, next action research/narrow scope и lawful
visual fallback. Только discussion preview; запись/экспорт валидного packet здесь
не выполняются, SELECTED_FOR_EDITORIAL_REVIEW/APPROVE не присвоены.

## 10. Компактный UK кейс з іншим глядачем і кутом

**Ілюстрація, не перевірене дослідження.** Тема: «Як відрізнити археологічну
знахідку від пояснення події?» Audience A-UK@1 — припущення: учні старшої школи,
яким потрібна навичка критичного читання, а не огляд цивілізацій. Locale uk,
science/factual,5–7хв (300..420s),CALM,720×1280; UI ru або uk незалежно.
Angle: «побудувати ланцюжок спостереження → гіпотеза → перевірка альтернатив».
Promise: «навчитися ставити запитання до висновку», без обіцянки визначати істину
за одним зображенням. Portfolio/analytics/age evidence UNKNOWN.

Hooks: QUESTION «Що ми бачимо — і що лише припускаємо?»;
HUMAN_STAKES «Ви пояснюєте знахідку однокласнику. Де закінчується опис і починається
ваша версія?»; COUNTERINTUITIVE «Чи може одна знахідка мати кілька пояснень?
Перевірмо, які дані допомагають їх розрізнити». Це навчальні запитання, не claims
про конкретну реальну знахідку. First30s — показати різницю між описом і висновком;
жодної вигаданої частки утримання.

Chapters: запитання30s; опис власної умовної схеми60s; альтернативи90s;
які свідчення потрібні90s; межі висновку60s —330s target, не фактичний timing.
Claim Q-UK1 — методологічне припущення про потребу альтернативних пояснень,
UNREVIEWED, central; потрібен exact методичний/науковий Source S-UK1 з locator/hash,
зараз UNKNOWN. Вигаданий предмет позначити «умовна схема», не археологічний документ.
Visuals: REQUIRED локальна текстова схема; LOCAL картки «опис/висновок»;
OPTIONAL фото знахідки виключене, поки licence UNKNOWN. Local WAV uk, ASR NONE,
CPU stills fallback; голос/шрифт/licence/resource budget потребують review.
Brief B-UK — workflow_state DRAFT, selection_state NOT_SELECTED, editorial_approval_state NOT_EVALUATED, recommendation BLOCKED через central evidence-needed; aggregate UNKNOWN.
Наступний крок — джерело й human review, не render/APPROVE. Символьні aliases,
як і RU example, не є serializable SIRef або editorial approval.

## 11. Негативні/негативные cases и будущая acceptance matrix

Все ниже — **ожидаемые будущие outcomes**, не запущенные tests. Общее требование:
никаких editorial approvals/rights grants/renderer invocation и скрытого обновления
protected snapshot при любом outcome.

| Test ID | Сценарий | Expected |
|---|---|---|
| SI-T01 | Ручная topic/URL/local metadata offline | Original text/provenance сохранены; no network/file dereference по locator |
| SI-T02 | Derived candidate назван manual после SELECT | Export candidate отклонён; derivation сохранена, нет нового discovery_method |
| SI-T03 | Missing critical evidence | BLOCKED/CENTRAL_CLAIM_UNSUPPORTED; aggregate UNKNOWN при unknown rating; next research |
| SI-T04 | Essential visual unlicensed, fallback UNKNOWN | BLOCKED/RIGHTS_BLOCKED; высокий score не меняет итог |
| SI-T05 | Duplicate title/source/portfolio topic | REVIEW_DUPLICATE при нерешённом совпадении; shared source не automatic merge |
| SI-T06 | Нет интернета / fresh trends для актуальной темы | UNAVAILABLE_OFFLINE + NEEDS_INPUT; не fabricated trend result. Evergreen — caveat, local work допустима |
| SI-T07 | Stale source по freshness requirement | INPUT_STALE/новый review/run; нет automatic supported; старая публикация не автоматически плоха без relevance rule |
| SI-T08 | Изменились candidate/source revision/hash или input selection | Descendants STALE; exact old refs исторические; новый run/selection, no approval transfer |
| SI-T09 | Полный высокий score и blocking rights | BLOCKED, не rank-based permission |
| SI-T10 | Hook противоречит reviewed qualification | REVISE_CREATIVE/HOOK_FACT_CONFLICT либо BLOCKED если central false claim; точная qualification не теряется |
| SI-T11 | GPU/paid provider недоступен | Optional improvement UNAVAILABLE; законный CPU fallback сохраняет offline brief. Если essential без fallback — CAPABILITY_BLOCKED |
| SI-T12 | Unknown rating / confidence / portfolio | Unknown отдельно от0, aggregate UNKNOWN; никакой renormalization или invented analytics |
| SI-T13 | Locale ua, несовпадающий narration/subtitle | INVALID/LOCALE_MISMATCH, не silent translation/coercion |
| SI-T14 | Unknown/duplicate fields, float/bool as integer, overflow/limits, surrogate/bad UTF-8 | INVALID со stable field_path; no truncation/auto-fix |
| SI-T15 | Dangling/wrong-kind/hash refs, derivation cycle | INVALID/REF_* или DEPENDENCY_CYCLE; no half-valid recorded packet |
| SI-T16 | Non-review suggestion пытается выставить supported/approved | Refuse unsupported human-review metadata/authority claim; no fake reviewer/evidence |
| SI-T17 | Одинаковый request_id: повтор bytes и изменённый payload | Повтор same ID/exact bytes — те же refs; changed bytes same ID — REQUEST_CONFLICT |
| SI-T18 | Brief → BriefValue → script/renderer | Совместимые поля только через approved adapter; лишние поля не уходят в reason/rationale; отсутствующий adapter — UNAVAILABLE |
| SI-T19 | Rights binding confirmed, expired licence/intended-use mismatch | No grant/readiness; отдельный BLOCKED rights outcome |
| SI-T20 | Существующий history REJECT/REVISE/REVOKE или ambiguous sequence | SI score/SELECT/time не меняют history/authority; ordinary review requirements сохраняются |
| SI-T21 | RU/UK natural wording меняет число/имя/дату/цитату/qualification | Явный diff и возврат на claim review, не принятие нового факта |
| SI-T22 | Local WAV / optional model / Edge offline | Без downloads/paid/network fallback; model/voice/license gate остаётся; Edge unavailable |
| SI-T23 | Render capability превышена:21scenes/2001 chars/unsupported media | Future adapter CAPABILITY_BLOCKED, явная переработка новой revision; no truncation |
| SI-T24 | Изменение source/profile/locale/intended-use после selection | Сталость/повтор review/readiness; старый SELECT не carried forward |
| SI-T25 | Сравнение old editorial bytes/S1/S2/D-01 после SI unit implementation | Existing regressions/golden unchanged; ни одного protected write/нового S1 operation |
| SI-T26 | RU/UK examples выше с draft aliases/unknown evidence | Только working preview; NOT EXPORTABLE, BLOCKED; wire invalid до actual refs |

До будущей реализации нужны независимые literal SI codec vectors, human/manual vs
derived provenance fixtures, real compatible editorial fixtures и API error-path
fixtures. Матрица задаёт проверяемые outcomes, а не разрешение сейчас писать tests.

## 12. External ideas и права

Applicability gate 2026-11-09 по отдельному реестру
`docs/external-ideas-adoption-register`, exact
`4ad198a095b155a57d6d0b162fc977260119962b`,
`docs/architecture/EXTERNAL_IDEAS_AND_ADOPTION_REGISTER.md` (git show, без merge/cherry-pick).
Статусы ниже — **применимость идеи**, не изменение CANDIDATE→APPROVED в реестре.

| ID | Gate для этой фазы | Конкретная применимость / отдельное approval |
|---|---|---|
| EXT-01 VidRusher | LATER | Идея proxy/clip selection и фактического voice timing полезна будущему production adapter; V1 только описывает visual needs/effort, без Gemini/TTS/download. Нужны owner scope и права exact source/dependencies до reuse |
| EXT-02 WanGP | LATER | Shot/take/workflow/resource preflight относится к производству; не нужен инференс или storage change. Концептуальные предыдущие решения не дают approval конкретному коду/license integration |
| EXT-03 LTX-Desktop | APPLICABLE_AS_IDEA | Явно показывать недоступные capabilities и CPU fallback в Brief вместо silent GPU/paid requirement; самостоятельное проектирование этой UX-границы. Очереди/Retake/Extend — LATER, код не переносится |
| EXT-04 Humanizer | APPLICABLE_AS_IDEA | Отдельный detect-only stylistic review с protected numbers/names/quotes и видимыми changes применим как критерий естественности RU/UK; runtime correction/model — deferred. Не применять китайские правила механически; нужен отдельный OWNER decision перед реализацией/заимствованием |

Ни одна интеграция здесь не одобрена и не реализована; стоимость/качество/privacy
провайдеров не объявляются измеренными. Для выбранного reuse будущая задача должна
указать exact upstream revision/files/symbols, способ переноса, notices, dependencies,
model/voice/media/API rights и проверку коммерческого использования.

Действуют [IMPORT_LICENSE_GATE](../../LICENSES/IMPORT_LICENSE_GATE.md) и
[UPSTREAM_TECHNOLOGY_IMPORT](../UPSTREAM_TECHNOLOGY_IMPORT.md): archived MIT copy
не снимает CC BY-NC-SA4.0 gate pinned upstream `87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1`.
Китайские Writing-DNA/corpora, чужие datasets/model weights/media/voices/code не
переносятся автоматически. Original RU/UK prompts не разрешают копировать исходники.
Rights на factual source не равны rights на изображение/цитату/голос или коммерческий output.

Release-license checkpoint сохраняется для **Edge и Silero**: exact provider/package/
model/voice revision, origin, license/ToS, commercial/distribution scope, privacy,
rights на inputs/outputs и actual optional availability должны быть проверены до
включения в release. Edge не offline; Silero не скачивается и не становится trusted
по имени. Local WAV — только с подтверждёнными правами, не универсальный обход gate.
FFmpeg build/distribution/fonts/assets проверяются отдельно. Release checklist/SBOM/
notices и unresolved items не закрываются этой документацией.

## 13. Решения владельца до implementation и порядок этапов

| ID | Требуется owner decision | Рекомендуемая ограниченная редакция (PROPOSAL) |
|---|---|---|
| SI-D01 | Scope и интерфейс V1 | Offline/manual CLI-first, четыре части концепции, read-only discussion packet; без LLM/search/render integration |
| SI-D02 | SI records/refs/provenance/codec | Утвердить отдельный SI/1 namespace, immutable revisions, explicit UNKNOWN, отсутствие machine→manual подмены, limits и literal-vector plan |
| SI-D03 | Persistence/privacy/retention | User-owned draft workspace вне Git и protected storage; approved format/location/cleanup, без keys/authority; не новый authoritative editorial head |
| SI-D04 | Rubric defaults | Подтвердить/изменить девять критериев,0..5, веса total100, confidence/unknown/aggregate и blockers precedence; без viral prediction |
| SI-D05 | Human reviews и selection | Кто вводит ClaimCheck/rights notes, какие declarations/UI нужны; Selection не APPROVE; запись human labels не trusted identity |
| SI-D06 | Creative scope/locale/style | Три стратегии или явный отказ, qualitative0–30s, RU/UK fact-preservation/diff, illustrative cases как acceptance seeds |
| SI-D07 | Brief/adapter/export boundary | Самостоятельный pre-script Brief + discussion packet; automatic machine Candidate export unavailable; отдельный approved provenance/adapter contract до editorial writes |
| SI-D08 | Production capabilities/defaults | E00 dimensions/language, local WAV/stills CPU fallback; durations/effort только targets/assumptions; не открыть renderer/readiness из brief |
| SI-D09 | Optional providers/external ideas | Network/GPU/paid opts deferred; отдельные owner/license/privacy decisions по конкретным EXT components/provider use-cases |
| SI-D10 | Приёмка и task sequence | Утвердить эту спецификацию и SI-T01–26, затем отдельные bounded задания; no implementation approval из одного concept decision |

Порядок будущих отдельно разрешаемых этапов: (1) pure SI value types/codec/provenance
и limits → (2) manual intake/local Discovery/dedup → (3) rubric/blocks с independent
fixtures → (4) шаблонные creative alternatives/selection/brief assembly → (5) локальный
review-packet interface/persistence после privacy решения → (6) отдельно согласованный
editorial adapter и production-readiness interface. Каждый шаг требует review/test
результата перед следующим. Native storage не является задачей этих стадий и остаётся
на hold; отсутствие service не разрешает обход protected-write boundary.

## 14. Проверка документа и STOP

Выполнены source/type/boundary inspection, сверка exact base/source remote, applicability
реестра, проверка локальных ссылок, суммы proposed weights, наличия RU/UK/negative
cases и consistency refs/statuses, `git diff --check`, one-file allowlist/размер.
Python unit tests, external API/search/crawling/model downloads/paid calls не выполнялись.
Ничего не утверждается как runtime или performance/Windows qualification.

**Переписывание завершённых этапов не требуется.** Нужны отдельные новые SI contracts
и adapter decisions; существующие gaps явно перечислены, а не устранены подменой полей.
Статус всего нового документа остаётся **PROPOSAL / AWAITING OWNER APPROVAL**.
После публикации — **STOP**: owner + independent review до любых implementation tasks.
Source/schema/tests/dependencies/CI/approved architecture/main не изменены;
без PR/merge/release. S3.2b/S3.3 не начинались.
