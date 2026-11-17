# G3.2.0 — PG-01–PG-05: Production Gate contract discovery

**PROPOSAL — OWNER REVIEW REQUIRED.** Дата: 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

Это типизированные схемы и правила для review, **не реализация, не новые approved enums и не выдача permissions**. Имена `pg-*/proposal-1` намеренно не объявляют production wire V1. Нет реальных grant, principal credentials, ключей, policy значений или примерных нулевых SHA. Любая будущая реализация требует отдельного поручения после owner approval контрактов и trust dependencies.

## 1. Режимы, границы и результат проверки

| Режим | Разрешённое назначение | Что не следует из режима |
|---|---|---|
| SYNTHETIC_TEST_ONLY | Только существующая exact зарегистрированная D1 fixture через неизменённый SyntheticRenderPermitV1 | Не источник PG Human Approval, rights evidence или production grant. Нельзя загрузить произвольный Preview в D1 |
| PREVIEW_ONLY | Private editor diagnostics, drafts, планы и PG-01 snapshot candidate | INPUT_COMPLETE/DRAFT_PLAN_VALID/DISPLAYABLE не authority и не готовность production |
| PRODUCTION_CANDIDATE | Проверка комплекта PG-01–PG-05 и проектирование заявки на строго ограниченный render | Ни наличие JSON, ни CONSISTENT результат не разрешают production execution |

Предлагаемый pure verdict: `CONSISTENT_NO_AUTHORITY` либо `DENY` с ошибками. Даже полное совпадение всех digest не возвращает `ALLOW_RENDER`. Режим future authorised production **не выбран**: потребуется отдельный owner-approved execution contract/profile и квалифицированный issuer/executor. В этом discovery нет обхода через «локальный trusted=True», CLI flag, score или поле `permissions_granted`.

PG-04 ниже описывает содержимое **кандидата render authorization** и требования будущего runtime admission. Он не является новым действующим permit. Будущий доверенный issuer должен независимо принять решение, привязанное к exact candidate и состоянию; executor должен проверить его и atomically consume. Формат реального grant, доверенные корни/ключи и production mode остаются OD-PG-04/05/06 BLOCKED, а не подставляются как dummy provider.

## 2. Общая схема — предлагаемая, закрытая

Нотация: `Record{a:T,b:U}` — ровно перечисленные ключи, **все обязательны**. `T|null` означает явный null, а не пропуск. `List<T>` сохраняет порядок; duplicates запрещены там, где указана uniqueness. Ссылки разрешаются по exact id/revision/hash без latest fallback. Это спецификация для будущего schema compiler/tests, не созданный JSON Schema или Python validator.

| Тип | Схема / ограничение PROPOSAL |
|---|---|
| Id | Канонический lowercase UUID; не доказательство уникальности в мире или identity |
| Hash | Ровно64 lowercase hex, SHA-256; не password/capability/signature |
| GitSha1 | Ровно40 lowercase hex; использовать только в Git source identity |
| Text | Непустая последовательность Unicode scalar values, без surrogate; без Unicode normalization, trim/coercion |
| Int | Exact JSON integer, не bool/float; диапазон signed64-bit. Count/size/revision/time дополнительно неотрицательны, revision≥1 |
| Instant | UTC epoch seconds, целое0…253402300799; expiry exclusive; локальная строка timezone не authority clock |
| Mode | Ровно SYNTHETIC_TEST_ONLY / PREVIEW_ONLY / PRODUCTION_CANDIDATE; допустимый subset ограничен типом PG, как ниже |
| Contract | Один из `pg-01/proposal-1` … `pg-05/proposal-1` |
| ObjectRef | `Record{contract:Contract,id:Id,revision:Int,binding_sha256:Hash}` |
| ByteRef | `Record{object_id:Id,sha256:Hash,byte_length:Int,media_type:Text}`. Immutable bytes в приватном content store; URI/path не является resolver. Type/size подтверждаются реальными bytes |
| PolicyRef | `Record{id:Id,version:Text,sha256:Hash}`. Hash точных policy bytes; JSON не утверждает policy действующей |
| HeadRef | `Record{stream_id:Id,epoch_id:Id,sequence:Int,head_sha256:Hash}`. Состояние должно быть независимо проверено у authoritative provider |
| ActorRef | `Record{principal_id:Text,identity_evidence:ByteRef,authority_policy:PolicyRef,review_session_id:Id}`. Principal syntax следует A1/O2, evidence не принимается от caller как доказательство OS identity |
| UseScope | `Record{purpose:Text,operations:List<Text>,channels:List<Text>,territories:List<Text>,commercial:bool,valid_from:Instant,valid_until:Instant,attribution:List<Text>}` |
| SubjectKey | `Record{snapshot:ObjectRef,plan_sha256:Hash,asset_manifest_sha256:Hash,use_scope_sha256:Hash,policy:PolicyRef}`; exact equality всех полей |
| Check | `Record{code:Text,basis:List<ByteRef>,outcome:Text,reason:Text}`; допустимые code/outcome определены для каждой коллекции ниже, не free-form allow flags |

**Envelope для всех PG:** `Record{contract:Contract,id:Id,revision:Int,mode:Mode,body:Body,binding_sha256:Hash}`. PG-01 mode всегда PREVIEW_ONLY; PG-02/03/04/05 mode всегда PRODUCTION_CANDIDATE. Legacy D1 evidence остаётся SYNTHETIC_TEST_ONLY вне PG envelope и не импортируется как PG-05. `Body` определяется только соответствующим PG. Envelope id/revision/contract/mode включаются в digest, поэтому перенос body между типами/режимами/ревизиями меняет binding.

### 2.1. Hash/canonicalization proposal PG-C14N-1

Raw files: SHA-256 **точных bytes**, byte_length обязателен. PG envelope digest:

`SHA256(UTF8("StoryStudio/PG-C14N-1") || 0x00 || canonical_json(envelope без binding_sha256))`.

Это исключает self-hash. Не исключать другие поля; не hash строкового представления Hash; не смешивать Git blob SHA-1, raw SHA-256, G2 input_sha256, SI canonical hash и PG digest. ObjectRef.binding_sha256 означает полный envelope binding; алгоритм и bounds должны быть утверждены в OD-PG-01 до implementation, без serializer fallback.

Canonical JSON: UTF-8, no BOM/newline/whitespace outside strings; object keys sorted lexicographically по Unicode scalar codepoint; arrays unchanged; true/false/null literals; integers minimal base10 (0 вместо -0, no +/leading zeros). Strings: `"` и backslash escape, short escapes b/f/n/r/t, оставшиеся U+0000…001F как lowercase `\u00xx`; остальные scalar values literal UTF-8, `/` не escape. Duplicate keys, floats/exponents/NaN/Infinity, invalid UTF-8/surrogates, unknown members, missing/null required values, alias keys отвергаются **до** digest. No silent normalization или преобразование существующих SI records.

Предлагаемые parser bounds: envelope≤8MiB, nesting≤64, string≤65536 UTF-8 bytes, list≤10000. Большие assets/evidence хранятся как ByteRef, не inline/base64. Bounds — OD-PG-01 PROPOSAL, не новые production constants. Verifier читает bounded stream до лимита+1; oversized prefix не получает whole-file hash.

Reference typing: SubjectKey.snapshot → PG-01; PG-02 predecessor → PG-02 того же subject/review_kind; PG-04 approvals → PG-02, rights → PG-03; PG-05 authorization_candidate → PG-04, previous_evidence → PG-05 того же execution/attempt. ID/revision/contract/digest всех refs сверяются с resolved envelope, conflicting bytes под одним id/revision и cyclic/dangling links deny. linked_decisions PG-01 — только historical context, не замена PG-02 authority. Stored heads/receipts не выбирают themselves latest; provider verification обязательна.

UseScope операции допускаются из закрытого proposal набора `LOCAL_RENDER`, `REPRODUCE_ASSET`, `SYNCHRONIZE_AUDIO`, `ADAPT`, `PUBLISH`, `DISTRIBUTE`. Это описание **запрашиваемого usage**, не набор выданных прав. В PG-04 render request operation только LOCAL_RENDER; публикация/распространение требуют отдельной будущей авторизации. Territory/channel vocabularies задаются точной policy; неизвестное значение deny, `*` не означает worldwide. Ограничение license всегда пересекается с requested use, никогда не расширяется. `valid_from < valid_until`; `[from,until)`; `now==until` уже expired, clock uncertainty deny.

## 3. PG-01 — Preview Snapshot

**Цель:** immutable binding exact editor inputs, результатов, scene content, product rationale и limitations. Это не копия directory path и не production grant.

`Body01 = Record{source_identity:SourceIdentity,raw_editor_input:ByteRef,editor_values_sha256:Hash,evaluation_inputs:ByteRef,full_evaluation:ByteRef,evaluation_derivation:Text,evaluation_observation:Observation,projection_cards:List<LocaleArtifact>,preview_export:List<NamedArtifact>,render_plan:ByteRef,asset_manifest:ByteRef,product_dossier:Dossier,linked_decisions:List<ByteRef>,editorial_constraints:List<Text>,created_at:Instant,policy:PolicyRef}`.

| Подтип | Все обязательные поля |
|---|---|
| SourceIdentity | `Record{repository:Text,commit_sha1:GitSha1,tree_sha1:GitSha1,code_manifest:ByteRef}`; manifest содержит exact path/blob/raw SHA256 используемых evaluator/Projection/Preview/reader, Python/runtime profile |
| Observation | `Record{observed_context:ByteRef,expected_context:ByteRef,required_current_premise:ByteRef|null,observed_at:Instant,context_head:HeadRef,valid_until:Instant}` |
| LocaleArtifact | `Record{locale:Text,artifact:ByteRef}`; locale ровно ru либо uk; две уникальные записи в порядке ru,uk для предлагаемых двух видео |
| NamedArtifact | `Record{name:Text,artifact:ByteRef}`; name из exact G2 generated file allowlist, без path/URL, uniqueness |
| Dossier | `Record{topic_question:Text,audience_need:Text,why_film:Text,angle:Text,novelty_basis:List<ByteRef>,claim_links:List<ClaimLink>,required_visuals:List<VisualNeed>,risks:List<Risk>,constraints:List<Text>,research_limits:List<Text>}` |
| ClaimLink | `Record{claim_id:Id,script_span:ByteRef,kind:Text,central:bool,sources:List<SourceFragment>,scientific_review:Text,qualification:Text|null}`; kind FACTUAL/FICTIONAL/HYPOTHESIS; review REQUIRED/REVIEWED/REJECTED/NOT_APPLICABLE |
| SourceFragment | `Record{source:ByteRef,retrieved_at:Instant,locator:Text,fragment:ByteRef,relation:Text}`; relation SUPPORTS/CONTRADICTS/CONTEXT/INSUFFICIENT |
| VisualNeed | `Record{id:Id,scene_id:Id,meaning:Text,required:bool,asset_ids:List<Id>,feasibility_basis:List<ByteRef>}` |
| Risk | `Record{id:Id,category:Text,severity:Text,blocking:bool,basis:List<ByteRef>,mitigation:Text|null,resolution_basis:List<ByteRef>}`; category SCIENTIFIC/EDITORIAL/LEGAL/PRODUCTION/REPUTATION; severity LOW/MEDIUM/HIGH/CRITICAL |

**Проверки:** все ByteRef пересчитать по доступным exact bytes; разобрать original input без исправления; вычислить editor_values_sha256 по **неизменённому G2 wire(data)**, не PG-C14N. Повторный exact pinned evaluator call должен совпасть с полным full_evaluation; сохраняется обязательная PD-01 verification Projection, вызываемая с полным результатом и original invocation. Все cards/output/source/version/context bindings проверяются; read_plan остаётся format validator, не approver. Будущий pure byte-validator должен сохранять его format rules без файлового IO; существующий read_plan(path) является IO API collector/executor, не pure authority operation. Не делать `saved flag CURRENT=true` trust source.

**Критический base gap:** G2 export `evaluation.json` сокращает diagnostics до code-only. Нельзя восстанавливать private field_path/input_ref/message по догадкам или передавать этот export как full result. Snapshot collector будущего этапа должен заново вычислить полный result из exact original inputs на pinned code; `evaluation_derivation` ровно RECOMPUTED_FROM_EXACT_INPUTS. Отдельный redacted export остаётся NamedArtifact. Если inputs/pinned runtime/контекст недоступны — DENY, не реконструкция. Если результат/досье изменились — новый snapshot/review, не замена уже approved bytes.

**Fail closed:** malformed/INCOMPLETE input, evaluation INVALID/STALE/FAILED/NOT_RUN, currentness≠CURRENT, eligibility≠ELIGIBLE_FOR_CREATIVE, UNAVAILABLE/missing card, partial/missing/invalid plan, unmatched context head, expired observation, unresolved required visual или blocking risk → не допускать дальнейшее authorization candidacy. Диагностическое private чтение остаётся возможно отдельно. ELIGIBLE_FOR_CREATIVE — лишь necessary proposal precondition, не sufficient rights/scientific/production condition.

Dossier может описывать неизвестное для draft review, но пустой sources у central factual claim, unresolved scientific review, contradicted central thesis, missing why_film/required visuals не становятся пригодными от наличия заполненной формы. Human/editor/scientific review в PG-02 обязателен по policy; policy не может объявить fictional реальное factual assertion ради обхода. Scientific REVIEWED в dossier — заявка, не свидетельство компетентного проверяющего.

**Зависимости:** G1 APIs, G2 original bytes, trusted current-context provider, PG-C14N, immutable resolver, render-plan proposal из PG-04. **Ошибки:** PG_FORMAT, PG_DIGEST, PG_REFERENCE, PG_EVALUATION, PG_STALE, PG_PRODUCT_GAP, PG_DEPENDENCY_UNAVAILABLE. **Оракулы:** P01-01…P01-08. **Безопасность:** digest связывает bytes, не identity/world truth; snapshot creation time не защищает rollback, no public card export grant.

## 4. PG-02 — Human Approval

`Body02 = Record{subject:SubjectKey,review_kind:Text,actor:ActorRef,decision:Text,reviewed_materials:List<ByteRef>,declarations:List<Text>,reason:Text,decided_at:Instant,valid_until:Instant,predecessor:ObjectRef|null,history_head:HeadRef,authority_receipt:ByteRef}`.

review_kind EDITORIAL_SCRIPT_AND_SCENES либо SCIENTIFIC_REVIEW; decision APPROVE/REJECT/REVISE/REVOKE. Новые PG роли не расширяют существующий editorial HANDOFF. `authority_receipt` — immutable evidence доверенного identity/authority/session provider, а не JSON от клиента с display_name. Для данных разрешён opaque ByteRef; формат operational receipt и trust anchors должны быть отдельно утверждены (OD-PG-02/04/06), до этого effective approval **BLOCKED**.

**Проверки:** SubjectKey exact snapshot/plan/assets/use/policy; actor identity аутентифицирована provider по A1, allowlist gate+decision проверяется отдельно, display name не identity. Review session показала exact bytes языка/сцен/досье/risks/limitations и зафиксировала explicit declarations; не auto-check boxes/LLM approval. Proposed editorial declarations: EXACT_TEXT_AND_LOCALES_REVIEWED, CLAIM_EVIDENCE_REVIEWED, REQUIRED_VISUALS_REVIEWED, BLOCKING_RISKS_ADDRESSED, NO_PRODUCTION_PERMISSION_INFERRED. SCIENTIFIC_REVIEW требует CLAIM_EVIDENCE_REVIEWED, QUALIFICATIONS_RECORDED, NO_UNSUPPORTED_CERTAINTY. Требуемый набор, полномочия и competence rules фиксируются policy, не произвольным Text. Для REJECT/REVISE/REVOKE — только NO_UNSUPPORTED_REVIEW_CLAIM и непустой reason. Отрицательное решение не требует принять content пригодным, но требует authentic history/actor binding.

PG-02 decided_at < valid_until; PG-03 reviewed_at < valid_until; PG-01 created_at/observed_at не позже trusted now с выбранной uncertainty policy, observation observed_at < valid_until. Future timestamps или непроверяемое время не разрешают admission. Эти limits не удаляют negative history и не возрождают прежние approvals.

`predecessor` указывает предыдущий event **того же SubjectKey и review_kind**; первый event null только при доказанном отсутствии предыдущего в trusted history. Timestamp/UUID/array order не выбирают latest. Current history head/epoch должен быть проверен provider, conflict/ambiguous history deny. REVOKE/REJECT/REVISE в latest trusted state запрещают использование старого APPROVE; вернуть одобрение может только новый authentic event с predecessor, не редактирование истории. Истечение valid_until отрицательного event не оживляет старый APPROVE: tombstone остаётся в verified history до нового решения. Refresh expiry, смена scope/asset/text/use/policy требует нового subject approval; нельзя автоматически переносить prior approval.

**Fail closed:** missing identity mapping/authority/session/history, unknown policy, expired approval/actor grant, rollback/mismatched head, legacy unauthenticated record, revoked/negative latest decision, непоказанный exact материал, disputed scientific review → DENY для recognition/authorization. Чтение истории не блокируется как способ заявить approval. Provider outage не переводится в cached APPROVE.

**Зависимости:** PG-01, A1–A14/O1–O10 semantics, qualified identity/grants/review-session/current-head provider. Existing ApprovalRecord/ApprovalAuthorityEvidence string fields не реализуют это. **Ошибки:** PG_IDENTITY, PG_AUTHORITY, PG_HISTORY, PG_REVOKED, PG_EXPIRED, PG_PRODUCT_GAP. **Оракулы:** P02-01…P02-08. **Ограничения:** signature/digest без trusted registry не аутентификация; approval editorial/scientific отдельно от asset rights и render permissions. REVOKE при текущем executing run описан в PG-04; исторические факты не удаляются.

## 5. PG-03 — Asset Rights Evidence

`Body03 = Record{subject:SubjectKey,assets:List<AssetCase>,aggregate_review:Text,reviewer:ActorRef,reviewed_at:Instant,valid_until:Instant,history_head:HeadRef,authority_receipt:ByteRef,policy:PolicyRef}`.

`AssetCase = Record{asset_id:Id,kind:Text,material:ByteRef,origin:Text,provenance:List<ByteRef>,rightsholders:List<Text>,license_evidence:List<ByteRef>,rights_layers:List<RightsLayer>,requested_use:UseScope,restrictions:List<Text>,attribution_obligations:List<Text>,review_status:Text,review_reason:Text}`.

`RightsLayer = Record{layer:Text,basis:List<ByteRef>,allowed_operations:List<Text>,channels:List<Text>,territories:List<Text>,commercial_allowed:bool,valid_from:Instant,valid_until:Instant,adaptation_allowed:bool,sublicense_allowed:bool,attribution:List<Text>,revocation_or_dispute_ref:ByteRef|null}`.

kind IMAGE/VIDEO/AUDIO/MUSIC/VOICE/FONT/MODEL/GENERATED/TOOL_RESOURCE; origin LICENSED/OWNED/GENERATED/REPORTED_UNKNOWN. layer COPYRIGHT/RECORDING/COMPOSITION/SYNC/PERFORMANCE/VOICE_CONSENT/PRIVACY_MODEL_RELEASE/TRADEMARK/FONT_OR_TOOL_LICENSE. review_status VERIFIED_FOR_EXACT_USE/UNKNOWN/PENDING/REJECTED/DISPUTED; aggregate_review COMPLETE_FOR_EXACT_USE либо INCOMPLETE. Эти статусы — assertion к проверке provider, не self-declared license grant.

**Проверки:** полное равенство inventory asset IDs/hash/bytes с manifest и RenderPlan; недостающие/лишние/caller-selected subsets deny. Каждый required layer определяется утверждённой rights policy по типу/intended use, не пустым list или строкой N/A. Для GENERATED нужны generator/source identity, exact result bytes и rationale применимой policy, а не освобождение от прав по generated=true. Public domain/ownership требуют evidence и jurisdiction review; доступный URL/факт оплаты не license. Terms/specimen/согласие/expiry/attribution доказательства должны быть immutable available bytes, не только текст «лицензия проверена».

Requested_use должен быть subset **каждого** required layer; intersection, не union между разными licenses. Проверять commercial, territory/channel, срок всего render/use и attribution в плане/выходе. Изменённый crop/музыка/voice/model/сценовое использование — новая scope review. Rights holder/reviewer identity и его полномочия проверяются отдельно от PG-02 editorial role. Onward publishing права можно описывать, но PG-04 LOCAL_RENDER их не исполняет и не выдаёт.

Для каждого asset requested_use выводится из **всех** его actual bound plan usages и глобального SubjectKey use scope, а не выбирается caller для удобной license проверки. Непокрытое использование хотя бы в одной сцене означает deny. Applicability каждого required layer должна быть обоснована policy/reviewer, нельзя пропустить layer пустым списком.

**Fail closed:** UNKNOWN/PENDING/DISPUTED/REJECTED, missing license copy/holder consent/layer, denied intended use, expired/disputed/revoked rights, missing visual, subject/material/use mismatch, provider unreachable → PG_RIGHTS/PG_EXPIRED/PG_REFERENCE/PG_DEPENDENCY_UNAVAILABLE и DENY authorization candidacy. Отсутствующее согласие нельзя подменить generic acknowledgment. Если срок должен покрывать будущую публикацию, а её дата/территория не выбраны — нет blanket worldwide grant.

**Зависимости:** PG-01 manifest/plan/dossier, approved rights policy, квалифицированный rights reviewer и current-dispute/revocation state. **Оракулы:** P03-01…P03-08. **Безопасность:** existing RightsBinding CONFIRMED подтверждает digest только; G2 VERIFIED_EXTERNALLY — reported data. Pure validator устанавливает coverage/subset/expiry относительно supplied verified context, но не создаёт юридическую истинность, согласие или identity. Asset bytes и license copies приватны; disclosure отдельно.

## 6. PG-04 — Render Authorization candidate и будущий admission

`Body04 = Record{request_id:Id,subject:SubjectKey,approvals:List<ObjectRef>,rights:ObjectRef,render_plan:ByteRef,toolchain:Toolchain,executor_profile:PolicyRef,output_contract:List<ExpectedOutput>,not_before:Instant,expires_at:Instant,attempt_policy:Text,operation:Text,state_heads:List<HeadRef>,issuer_policy:PolicyRef}`.

attempt_policy ровно SINGLE_ATTEMPT; operation LOCAL_RENDER; approvals должны покрывать editorial и все требуемые scientific reviews. Это **заявка**, которая всегда остаётся PRODUCTION_CANDIDATE в этом proposal. Поля `allow=true`, command string, произвольный executable path/URL, делегирование, автопродление и production permission отсутствуют и отвергаются.

| Подтип | Закрытая schema |
|---|---|
| RenderPlan (ByteRef JSON) | `Record{locales:List<Text>,scene_plans:List<LocaleArtifact>,scene_bindings:List<SceneBinding>,asset_manifest:ByteRef,usage:UseScope,width:Int,height:Int,fps_numerator:Int,fps_denominator:Int,output_profile:PolicyRef,attribution_plan:ByteRef}` |
| SceneBinding | `Record{scene_id:Id,locale:Text,text:ByteRef,claim_ids:List<Id>,asset_slots:List<AssetSlot>}` |
| AssetSlot | `Record{slot_id:Text,asset_id:Id,usage:Text}`; slot_id safe ASCII `[A-Za-z0-9_-]{1,64}`, usage IMAGE/AUDIO/MUSIC/SUBTITLE/FONT |
| AssetManifest (ByteRef JSON) | `Record{entries:List<ManifestEntry>}`; entries уникальны по asset_id, sorted by canonical Id; полный набор прямо/косвенно используемых материалов |
| ManifestEntry | `Record{asset_id:Id,kind:Text,material:ByteRef}`; kind тот же enum, что PG-03 |
| Toolchain | `Record{source_identity:SourceIdentity,tools:List<Tool>,environment:ByteRef}` |
| Tool | `Record{role:Text,version:Text,artifact:ByteRef,configuration:ByteRef}`; role PYTHON/RENDERER/FFMPEG/FFPROBE/FONT_ENGINE, unique role; версии не заменяют binary hashes |
| ExpectedOutput | `Record{output_id:Id,locale:Text,kind:Text,profile:PolicyRef,required:bool}`; kind VIDEO/PROJECT/SUBTITLES/MANIFEST, locale ru/uk; unique output_id |

Размеры/fps/codec/subtitle/scene-count limits определяются pinned output_profile с явными bounds; неизвестный/unapproved profile deny. Сохраняются ограничения read_plan при адаптации; PG не меняет текущий renderer. Готовый output SHA заранее не придумывается: ExpectedOutput определяет критерии и количество, PG-05 связывает **реальные** bytes. ScenePlan/asset slots/toolchain/attribution/executor profile/use целиком входят в SubjectKey через plan digest и snapshot constraints. Изменение любого render-affecting байта/config/tools/profile требует новой авторизации и повторной проверки релевантных human/rights bindings, без scope widening.

**Pure проверки:** PG-01–PG-03 exact consistency; нужные latest approvals/rights полны и valid в supplied verified state; mode не synthetic; epoch/heads согласованы; complete approved requested plan; time window intersection со всеми approvals/rights/policies; output set точно RU/UK и обязательные evidence artifacts. Эти проверки дают только CONSISTENT_NO_AUTHORITY. Поле state_heads не является доказательством latest head.

not_before < expires_at; effective window — пересечение request, всех положительных approvals, rights и trusted policies. RenderPlan.locales ровно [ru,uk], scene_plans ровно по одной записи на каждую; output IDs/scene IDs/slot assignments уникальны в своих областях. No unknown locale/asset/output fallback. Proposed profile обязан задать длительность/операционные пределы, чтобы deadline мог покрывать run; неизвестная возможность завершить в окне не продлевает grant.

**Предлагаемые runtime обязанности, пока BLOCKED:** до issuer decision получить независимые authenticated identity/policy/currentness/revocation/time/state; до исполнения снова сверить и atomically reserve single attempt в rollback-resistant authoritative ledger для full request bytes + issuer/grant/executor identity + epoch. Existing protocol/RAM model не принимается как ledger. Параллельный consume → не более одного START; conflict bytes under request_id deny; restart/unknown after reservation не rerender автоматически, stale token deny. Recovery может лишь узнать уже признанный outcome; новый render — новый owner-scoped grant/attempt после reconciliation. Предполагаемая exactly-once физическая работа не обещается: crash может оставить UNKNOWN.

Исполнитель открывает/удерживает immutable проверенные inputs в qualified private namespace, проверяет реальные binary/config/asset bytes, не выбирает по untrusted filename/PATH и не восстанавливает files по сети. Перепроверка path strings не заменяет descriptor/handle anchoring и OS qualification. Проверки time/identity/head до spawn и перед commit evidence обязательны; expiry/revocation во время run → cancel/quarantine, не publish/commit SUCCEEDED, затем reconciliation. Задержка обнаружения revoke должна быть bounded approved policy; потеря доступа к revocation/time service → deny start, активный run не объявлять successful.

**Ошибки:** PG_SCOPE, PG_MODE, PG_REPLAY, PG_REVOKED, PG_EXPIRED, PG_PATH, PG_TOOLCHAIN, PG_AUTHORITY, PG_DEPENDENCY_UNAVAILABLE. **Оракулы:** P04-01…P04-10. **Зависимости:** все предыдущие PG + qualified clock/issuer/executor/ledger/path resolver. **Безопасность:** никакой JSON-only валидатор не может гарантировать single-use, recent revocation, отсутствие TOCTOU, unbypassable rendering или protected state. SyntheticRenderPermitV1 никогда не конвертируется в этот admission; существующий first_video напрямую не является guarded production endpoint.

## 7. PG-05 — Execution Evidence

`Body05 = Record{execution_id:Id,authorization_candidate:ObjectRef,admission_receipt:ByteRef|null,request_id:Id,attempt_id:Id,executor:ActorRef,started_at:Instant,ended_at:Instant|null,toolchain:Toolchain,consumed_inputs:List<ConsumedInput>,outputs:List<ObservedOutput>,checks:List<Check>,outcome:Text,errors:List<Error>,previous_evidence:ObjectRef|null,state_head:HeadRef,completion_witness:ByteRef|null}`.

`ConsumedInput = Record{role:Text,input:ByteRef}`; role SNAPSHOT/PLAN/ASSET/RIGHTS/APPROVAL/POLICY. Полный exact closure, duplicates roles допустимы только для разных approved objects. `ObservedOutput = Record{output_id:Id,artifact:ByteRef,complete:bool,inspection:ByteRef}`. outcome SUCCEEDED/FAILED/CANCELLED/INDETERMINATE. Proposed candidate evidence может существовать для diagnostic review без admission, но **не** как trusted SUCCEEDED production result. D1 manifest — другой контракт, не PG-05 и не источник его admission receipt.

**Проверки:** input hashes реально прочитанных bytes, versions+binary/config hashes, exact authorization/request/attempt/executor linkage и policy; реальные output bytes и byte lengths, stream codecs/duration/frame/subtitle checks по output_profile. `Check.code` из PROFILE_INPUT_BINDING/PROFILE_OUTPUT_SET/PROFILE_MEDIA/PROFILE_ATTRIBUTION/PROFILE_TOOLCHAIN/PROFILE_TERMINAL_STATE; outcome PASS/FAIL/NOT_RUN. Все required checks PASS и outputs complete — necessary, не sufficient без authentic completion_witness для future production. JSON manifests не подменяют реальные hashes MP4; metadata-only или pixel-brightness тест не подтверждает научный смысл/права/читаемость всех кадров.

SUCCEEDED structurally requires non-null admission_receipt/completion_witness/ended_at, started_at ≤ ended_at, unique exact required output set, all complete=true и все required checks PASS; подлинность этих refs всё равно отдельно проверяется qualified provider. Missing witness не «исправляется» fake ByteRef: INDETERMINATE/deny. Предварительный отказ до admission возвращает Error, не вымышленный execution record со started_at. FAILED/CANCELLED не требуют успешного output set и не публикуют результаты.

**Запись и неполнота:** private execution records связываются с durable admission/attempt ledger. STARTED фиксируется до spawn как runtime event, не PG terminal outcome. Temporary files/staging не accepted evidence. SUCCEEDED terminal допускается только после обоих видео, всех required outputs/checks и atomically verified commit evidence index+state. Last marker/JSON file alone недостаточен; нужен отдельный qualified completion witness и invariant `head↔index↔actual bytes`. Читатель при отсутствующем/truncated/conflicting index, unknown terminal state или orphan outputs возвращает INDETERMINATE и quarantine, не угадывает success по наличию MP4.

FAILED/CANCELLED содержат только реально наблюдённые partial outputs с complete=false и checks FAIL/NOT_RUN; ended_at обязателен если конец наблюдался. INDETERMINATE допускает ended_at=null и недоступный completion_witness; не создаёт fabricated errors/output hashes. Коррекция evidence — новая immutable revision со ссылкой previous_evidence; исходный failure не удаляется. Retry не превращается в ту же попытку PG-04. Atomic/durability properties требуют отдельной native/storage qualification, сейчас не заработаны.

**Ошибки:** PG_EXECUTION, PG_INCOMPLETE, PG_EVIDENCE, PG_DIGEST, PG_HISTORY, PG_DEPENDENCY_UNAVAILABLE. **Оракулы:** P05-01…P05-08. **Зависимости:** PG-04 admission protocol, toolchain inspector, private immutable output store, durable qualified evidence/index/ledger. **Ограничения:** input secrets, private license copies, cards, personal reviewer IDs и raw stderr остаются приватны. Публичная redacted сводка/CI upload — отдельный export contract/owner permission, не часть SUCCEEDED и не автоматический side effect.

## 8. Общая модель ошибок

`Error = Record{contract:Contract,stage:Text,code:ErrorCode,subject_id:Id|null,retry:Text,outcome:Text}`. stage PARSE/BINDING/PRODUCT/IDENTITY/RIGHTS/ADMISSION/EXECUTION/EVIDENCE; retry NEVER/AFTER_REVIEW/AFTER_PROVIDER_RECOVERY; outcome всегда DENY. subject_id — приватный opaque ID либо null, не произвольный caller path. Нельзя echo raw exception, filesystem path, credential, имя человека или содержимое сценария. Локализованные сообщения из fixed catalog; machine code независим от языка.

Закрытый ErrorCode: PG_FORMAT, PG_DIGEST, PG_REFERENCE, PG_EVALUATION, PG_STALE, PG_PRODUCT_GAP, PG_IDENTITY, PG_AUTHORITY, PG_HISTORY, PG_REVOKED, PG_EXPIRED, PG_RIGHTS, PG_SCOPE, PG_MODE, PG_REPLAY, PG_PATH, PG_TOOLCHAIN, PG_EXECUTION, PG_INCOMPLETE, PG_EVIDENCE, PG_DEPENDENCY_UNAVAILABLE. Этот namespace не расширяет existing SI/1 error codes/enums.

Fail precedence PROPOSAL: parse/limit → digest/reference → semantic mode/product/evaluation → trusted identity/history/rights/time → admission/path/tools → execution → evidence. Можно вернуть все безопасно установленные errors в этом порядке; неизвестный provider failure только PG_DEPENDENCY_UNAVAILABLE, никогда implicit approval. Pure verifier не обращается к OS/clock/network сам: принимает explicit verified context. Отсутствие квалифицированного producer такого context блокирует execution, а не оправдывает simulated provider в production.

## 9. Нерешённые зависимости

До owner выбора нет operational provider protocols, реального authenticated issuer/grant format, trust/key roots, qualified state/clock/revocation mechanism, content resolver/path proof, native evidence commit, production mode или approved rights policy. Нельзя реализовать «временный» file-based approval/SQLite ledger/Windows service в обход этого discovery. Детальные [оракулы и gates](G3_2_0_TEST_ORACLES_AND_GATES.md), [threat/rights matrix](G3_2_0_SECURITY_AND_RIGHTS_MATRIX.md) и [owner alternatives](G3_2_0_OWNER_DECISIONS.md) — части того же PROPOSAL.
