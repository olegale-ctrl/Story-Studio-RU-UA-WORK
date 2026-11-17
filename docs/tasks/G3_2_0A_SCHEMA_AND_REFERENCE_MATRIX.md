# PG schema, SubjectKey and reference closure matrix

**FREEZE_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0a; 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Pinned discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c`.
Только docs/offline vectors. Направление OD-PG-01–12 принято владельцем, но численные значения, роли, trust policies и operational protocols не утверждены. Нет validators/providers, permissions или qualification.

## Степень freeze

Точные schema IDs сохраняются `pg-01/proposal-1`…`pg-05/proposal-1`, не объявляются approved/v1. Все Record fields обязательны; T|null — mandatory explicit nullable field, отсутствие не null. Unknown keys запрещены. Ниже **полнопольная инвентаризация именно pinned discovery**, а не новая реализация/молчаливое исправление. Нерешённые X01–X04 блокируют окончательный freeze.

| Contract | Mode | Body / dependencies | Digest / invariants | Пример и fail closed |
|---|---|---|---|---|
| PG01 Preview Snapshot | PREVIEW_ONLY | Body01; exact original bytes, full recomputed eval, cards, context, plan/assets/dossier | C10 binding всего envelope; G2 wire hash отдельно; no redacted full-result substitution | E/V019 — positive **field-shape/C14N only**, не full SI consistency; V051 negative/blocked empty Text. Invalid/stale eval → PG_EVALUATION/PG_STALE |
| PG02 Human Approval | PRODUCTION_CANDIDATE | Body02, PG01 SubjectKey, ActorRef/receipt/history, exact reviewer kind/scope | Predecessor того же subject+review_kind; latest verified state, negative tombstone не истекает в старый APPROVE | Structural template Body02 ниже; all refs populated из exact fixture closure — conditional example, full positive BLOCKED_CONTRACT. Wrong principal/scope → PG_IDENTITY/PG_AUTHORITY |
| PG03 Asset Rights Evidence | PRODUCTION_CANDIDATE | Body03, PG01 assets/use, complete layers и rights reviewer policy | Required layers/use intersection, no caller-subset, actual bytes/license evidence | Structural template Body03 + case VERIFIED_FOR_EXACT_USE не является grant. UNKNOWN layer/use mismatch → PG_RIGHTS |
| PG04 Render Authorization Candidate | PRODUCTION_CANDIDATE | Body04→PG01/PG02/PG03, full plan/toolchain/profile/state | SINGLE_ATTEMPT request, LOCAL_RENDER only; consistency не admission. Missing tool binding X04 остаётся unresolved | Structural template Body04; full positive until issuer/ledger policy BLOCKED_CONTRACT. Synthetic permit → PG_MODE/PG_SCOPE по selected stage, no allow-render |
| PG05 Execution Evidence | PRODUCTION_CANDIDATE | Body05→PG04 + actual input/output/attempt/heads/witness | SUCCEEDED asserts actual complete set/required checks and nonnull witness, but no authenticity без provider | Body05 FAILED/INDETERMINATE может быть consistent failure record; это не успешный render grant. Fake success/orphan output → PG_EVIDENCE/PG_INCOMPLETE |

STRUCTURALLY_VALID — **только descriptive annotation** уровня shape, не новый machine-readable result. CONSISTENT_NO_AUTHORITY относится ко всем cross-object semantic rules с explicit context и не даёт authority. DENY — fail-closed result с existing proposed PG error. Shape success не возвращается вместо missing provider proof. Полный positive fixture каждого PG будет окончательно определён только после owner принятия семантики, правил policies и raw dependency payload schemas. В этом пакете такие positives **BLOCKED_CONTRACT**, не fake PASS. Существующие failure records могут быть structurally/relationally consistent, не SUCCEEDED.

## Все Record поля и типы pinned discovery

Это complete field lists: каждый token field:type ниже обязателен. Вложенные Record раскрыты отдельно. Типы Text/Int/Instant/Hash/UUID и байтовые правила — [canonicalization spec](G3_2_0A_CANONICALIZATION_SPEC.md). ObjectRef не может ссылаться на latest. ByteRef — actual raw bytes, не доверенный path.

### ObjectRef

```text
Record{contract:Contract,id:Id,revision:Int,binding_sha256:Hash}
```

### ByteRef

```text
Record{object_id:Id,sha256:Hash,byte_length:Int,media_type:Text}
```

### PolicyRef

```text
Record{id:Id,version:Text,sha256:Hash}
```

### HeadRef

```text
Record{stream_id:Id,epoch_id:Id,sequence:Int,head_sha256:Hash}
```

### ActorRef

```text
Record{principal_id:Text,identity_evidence:ByteRef,authority_policy:PolicyRef,review_session_id:Id}
```

### UseScope

```text
Record{purpose:Text,operations:List<Text>,channels:List<Text>,territories:List<Text>,commercial:bool,valid_from:Instant,valid_until:Instant,attribution:List<Text>}
```

### SubjectKey

```text
Record{snapshot:ObjectRef,plan_sha256:Hash,asset_manifest_sha256:Hash,use_scope_sha256:Hash,policy:PolicyRef}
```

### Check

```text
Record{code:Text,basis:List<ByteRef>,outcome:Text,reason:Text}
```

### Body01

```text
Record{source_identity:SourceIdentity,raw_editor_input:ByteRef,editor_values_sha256:Hash,evaluation_inputs:ByteRef,full_evaluation:ByteRef,evaluation_derivation:Text,evaluation_observation:Observation,projection_cards:List<LocaleArtifact>,preview_export:List<NamedArtifact>,render_plan:ByteRef,asset_manifest:ByteRef,product_dossier:Dossier,linked_decisions:List<ByteRef>,editorial_constraints:List<Text>,created_at:Instant,policy:PolicyRef}
```

### SourceIdentity

```text
Record{repository:Text,commit_sha1:GitSha1,tree_sha1:GitSha1,code_manifest:ByteRef}
```

### Observation

```text
Record{observed_context:ByteRef,expected_context:ByteRef,required_current_premise:ByteRef|null,observed_at:Instant,context_head:HeadRef,valid_until:Instant}
```

### LocaleArtifact

```text
Record{locale:Text,artifact:ByteRef}
```

### NamedArtifact

```text
Record{name:Text,artifact:ByteRef}
```

### Dossier

```text
Record{topic_question:Text,audience_need:Text,why_film:Text,angle:Text,novelty_basis:List<ByteRef>,claim_links:List<ClaimLink>,required_visuals:List<VisualNeed>,risks:List<Risk>,constraints:List<Text>,research_limits:List<Text>}
```

### ClaimLink

```text
Record{claim_id:Id,script_span:ByteRef,kind:Text,central:bool,sources:List<SourceFragment>,scientific_review:Text,qualification:Text|null}
```

### SourceFragment

```text
Record{source:ByteRef,retrieved_at:Instant,locator:Text,fragment:ByteRef,relation:Text}
```

### VisualNeed

```text
Record{id:Id,scene_id:Id,meaning:Text,required:bool,asset_ids:List<Id>,feasibility_basis:List<ByteRef>}
```

### Risk

```text
Record{id:Id,category:Text,severity:Text,blocking:bool,basis:List<ByteRef>,mitigation:Text|null,resolution_basis:List<ByteRef>}
```

### Body02

```text
Record{subject:SubjectKey,review_kind:Text,actor:ActorRef,decision:Text,reviewed_materials:List<ByteRef>,declarations:List<Text>,reason:Text,decided_at:Instant,valid_until:Instant,predecessor:ObjectRef|null,history_head:HeadRef,authority_receipt:ByteRef}
```

### Body03

```text
Record{subject:SubjectKey,assets:List<AssetCase>,aggregate_review:Text,reviewer:ActorRef,reviewed_at:Instant,valid_until:Instant,history_head:HeadRef,authority_receipt:ByteRef,policy:PolicyRef}
```

### AssetCase

```text
Record{asset_id:Id,kind:Text,material:ByteRef,origin:Text,provenance:List<ByteRef>,rightsholders:List<Text>,license_evidence:List<ByteRef>,rights_layers:List<RightsLayer>,requested_use:UseScope,restrictions:List<Text>,attribution_obligations:List<Text>,review_status:Text,review_reason:Text}
```

### RightsLayer

```text
Record{layer:Text,basis:List<ByteRef>,allowed_operations:List<Text>,channels:List<Text>,territories:List<Text>,commercial_allowed:bool,valid_from:Instant,valid_until:Instant,adaptation_allowed:bool,sublicense_allowed:bool,attribution:List<Text>,revocation_or_dispute_ref:ByteRef|null}
```

### Body04

```text
Record{request_id:Id,subject:SubjectKey,approvals:List<ObjectRef>,rights:ObjectRef,render_plan:ByteRef,toolchain:Toolchain,executor_profile:PolicyRef,output_contract:List<ExpectedOutput>,not_before:Instant,expires_at:Instant,attempt_policy:Text,operation:Text,state_heads:List<HeadRef>,issuer_policy:PolicyRef}
```

### RenderPlan

```text
Record{locales:List<Text>,scene_plans:List<LocaleArtifact>,scene_bindings:List<SceneBinding>,asset_manifest:ByteRef,usage:UseScope,width:Int,height:Int,fps_numerator:Int,fps_denominator:Int,output_profile:PolicyRef,attribution_plan:ByteRef}
```

### SceneBinding

```text
Record{scene_id:Id,locale:Text,text:ByteRef,claim_ids:List<Id>,asset_slots:List<AssetSlot>}
```

### AssetSlot

```text
Record{slot_id:Text,asset_id:Id,usage:Text}
```

### AssetManifest

```text
Record{entries:List<ManifestEntry>}
```

### ManifestEntry

```text
Record{asset_id:Id,kind:Text,material:ByteRef}
```

### Toolchain

```text
Record{source_identity:SourceIdentity,tools:List<Tool>,environment:ByteRef}
```

### Tool

```text
Record{role:Text,version:Text,artifact:ByteRef,configuration:ByteRef}
```

### ExpectedOutput

```text
Record{output_id:Id,locale:Text,kind:Text,profile:PolicyRef,required:bool}
```

### Body05

```text
Record{execution_id:Id,authorization_candidate:ObjectRef,admission_receipt:ByteRef|null,request_id:Id,attempt_id:Id,executor:ActorRef,started_at:Instant,ended_at:Instant|null,toolchain:Toolchain,consumed_inputs:List<ConsumedInput>,outputs:List<ObservedOutput>,checks:List<Check>,outcome:Text,errors:List<Error>,previous_evidence:ObjectRef|null,state_head:HeadRef,completion_witness:ByteRef|null}
```

### ConsumedInput

```text
Record{role:Text,input:ByteRef}
```

### ObservedOutput

```text
Record{output_id:Id,artifact:ByteRef,complete:bool,inspection:ByteRef}
```

### Error

```text
Record{contract:Contract,stage:Text,code:ErrorCode,subject_id:Id|null,retry:Text,outcome:Text}
```

### Envelope

```text
Record{contract:Contract,id:Id,revision:Int,mode:Mode,body:Body,binding_sha256:Hash}
```

## Enum sets, constraints и version checks

| Поле/тип | Допустимые значения / constraint |
|---|---|
| Contract | pg-01/proposal-1, pg-02/proposal-1, pg-03/proposal-1, pg-04/proposal-1, pg-05/proposal-1; aliases/new version deny |
| Mode | SYNTHETIC_TEST_ONLY, PREVIEW_ONLY, PRODUCTION_CANDIDATE как conceptual modes; PG01 принимает PREVIEW_ONLY, PG02–05 PRODUCTION_CANDIDATE. D1 evidence вне PG envelope |
| Id / GitSha1 / Hash | lowercase UUID /40 lowercasehex /64 lowercasehex; syntax не identity/trust |
| Text/Int/Instant | nonempty scalar Text; exact signed64 Int не bool; Instant proposed0…253402300799; numerical bounds APPROVAL_REQUIRED |
| UseScope.operations | LOCAL_RENDER, REPRODUCE_ASSET, SYNCHRONIZE_AUDIO, ADAPT, PUBLISH, DISTRIBUTE; описание usage, не выданные permissions |
| Locale | ru/uk; proposed RenderPlan.locales=[ru,uk], unique scene/output IDs и ровно один scene_plan на locale |
| Body01.evaluation_derivation | RECOMPUTED_FROM_EXACT_INPUTS |
| ClaimLink.kind / scientific_review | FACTUAL/FICTIONAL/HYPOTHESIS; REQUIRED/REVIEWED/REJECTED/NOT_APPLICABLE |
| SourceFragment.relation | SUPPORTS/CONTRADICTS/CONTEXT/INSUFFICIENT |
| Risk.category / severity | SCIENTIFIC/EDITORIAL/LEGAL/PRODUCTION/REPUTATION; LOW/MEDIUM/HIGH/CRITICAL |
| Body02.review_kind / decision | EDITORIAL_SCRIPT_AND_SCENES/SCIENTIFIC_REVIEW; APPROVE/REJECT/REVISE/REVOKE |
| Body02.declarations | Editorial APPROVE: EXACT_TEXT_AND_LOCALES_REVIEWED, CLAIM_EVIDENCE_REVIEWED, REQUIRED_VISUALS_REVIEWED, BLOCKING_RISKS_ADDRESSED, NO_PRODUCTION_PERMISSION_INFERRED. Scientific APPROVE: CLAIM_EVIDENCE_REVIEWED, QUALIFICATIONS_RECORDED, NO_UNSUPPORTED_CERTAINTY. Negative: только NO_UNSUPPORTED_REVIEW_CLAIM. Actual applicability/policy OPEN |
| AssetCase.kind / ManifestEntry.kind | IMAGE/VIDEO/AUDIO/MUSIC/VOICE/FONT/MODEL/GENERATED/TOOL_RESOURCE |
| AssetCase.origin | LICENSED/OWNED/GENERATED/REPORTED_UNKNOWN |
| RightsLayer.layer | COPYRIGHT/RECORDING/COMPOSITION/SYNC/PERFORMANCE/VOICE_CONSENT/PRIVACY_MODEL_RELEASE/TRADEMARK/FONT_OR_TOOL_LICENSE |
| AssetCase.review_status | VERIFIED_FOR_EXACT_USE/UNKNOWN/PENDING/REJECTED/DISPUTED; не self-authenticating grant |
| Body03.aggregate_review | COMPLETE_FOR_EXACT_USE/INCOMPLETE |
| Body04.attempt_policy / operation | SINGLE_ATTEMPT / LOCAL_RENDER |
| AssetSlot.slot_id / usage | ASCII [A-Za-z0-9_-]{1,64}; IMAGE/AUDIO/MUSIC/SUBTITLE/FONT |
| Tool.role | PYTHON/RENDERER/FFMPEG/FFPROBE/FONT_ENGINE; unique role |
| ExpectedOutput.kind | VIDEO/PROJECT/SUBTITLES/MANIFEST |
| ConsumedInput.role | SNAPSHOT/PLAN/ASSET/RIGHTS/APPROVAL/POLICY |
| Body05.outcome | SUCCEEDED/FAILED/CANCELLED/INDETERMINATE — поле evidence, **не** pure verdict/permission |
| Check.code / outcome | PROFILE_INPUT_BINDING/PROFILE_OUTPUT_SET/PROFILE_MEDIA/PROFILE_ATTRIBUTION/PROFILE_TOOLCHAIN/PROFILE_TERMINAL_STATE; PASS/FAIL/NOT_RUN |
| Error.stage / retry / outcome | PARSE/BINDING/PRODUCT/IDENTITY/RIGHTS/ADMISSION/EXECUTION/EVIDENCE; NEVER/AFTER_REVIEW/AFTER_PROVIDER_RECOVERY; outcome DENY |

Policy-defined channels/territories/roles/rights applicability/output limits не имеют approved concrete vocabulary. Unknown selected-policy value deny, но policy невозможно сочинить для full valid fixture. CodeManifest/runtime environment/inspection/authority/admission/completion evidence ByteRefs требуют отдельного payload/profile protocol: digest bytes не означает verified claim. Эти пробелы OP-10…23 явно блокируют operational freeze, не заполняются opaque trusted=true.

## SubjectKey и directed closure

SubjectKey exact tuple: (PG01 contract/id/revision/binding, plan SHA256, asset manifest SHA256, intended UseScope SHA256, policy id/version/SHA256). Snapshot includes source/runtime/context/eval/dossier/plan/assets. Reviewer scope дополнительно связывает SubjectKey + review_kind + ActorRef.authority_policy + review_session_id и receipt. Не считать reviewer identity членом SubjectKey автоматически, не переназначать policy/version по latest.

| Edge | Exact target / restriction | Изменение означает |
|---|---|---|
| SubjectKey.snapshot | PG01 exact ObjectRef | Новый snapshot меняет все привязанные approvals/candidates |
| PG02.predecessor | PG02 того же SubjectKey и review_kind | Cross-key/self/dangling/ambiguous history deny, old negative tombstone не оживляет approve |
| PG03.subject | Тот же snapshot/plan/assets/use/root-policy key | Новый material/use требует rights review; policy namespaces надо явно freeze |
| PG04.approvals / rights | PG02 покрывает editorial+required scientific; PG03 exact same subject | Нельзя заменить копиями другого revision или неполным subset |
| PG05.authorization_candidate | PG04 same request/attempt identity | Новый attempt/evidence correction не переиспользует authorization |
| PG05.previous_evidence | PG05 того же execution/attempt, immutable chain | Не удаляет failure/unknown state; old revision не latest authority |
| ByteRefs | Все actual bytes в exact closure; opaque evidence не скрытая auto-ref | Никаких сетевых загрузок/пути из input, no latest lookup |
| Heads | stream/epoch/sequence/hash exact supplied values | Только provider доказывает currentness/ordering/anti-rollback; JSON сам нет |

Graph registry resolution proposal: index exact(contract,id,revision), reject conflicting bodies, verify local digests once, walk declared typed edges с colors/visited и resource bound. Полный closure/hash-first порядок и допустимые historical links должны быть выбраны owner (OP-08/09); это описание алгоритмических требований, **не validator implementation**. Genuine digest-bound cycles нельзя тестировать forged hashes как будто они valid; V043 отмечен BLOCKED.

## Обнаруженные противоречия и compatibility

- **X01:** nonempty Text → schema PG_FORMAT, но P01-07 на пустой why_film обещает PG_PRODUCT_GAP. Нужна owner resolution, исходный oracle сохраняется verbatim.
- **X02:** mode subset может быть schema condition (PG_FORMAT/PG_MODE before digest) либо semantic after digest (PG_DIGEST first for altered mode). Exact precedence не следует однозначно из discovery; V039 BLOCKED.
- **X03:** cycle oracle требует isolate structural graph от hash-valid content-addressed closure. Нельзя подставить фиктивные hashes и заявить cycle test; модель fixtures/edges OPEN.
- **X04:** discovery утверждает, что Toolchain/executor_profile входят SubjectKey через plan/constraints, но RenderPlan не имеет обязательных toolchain/executor_profile fields, а PG04 содержит их отдельно. Новый PG04 digest меняется, но PG02 SubjectKey может остаться прежним. Нужно explicit binding placement или узко описанная reapproval policy, без молчаливого добавления полей.

G1/SI/G2/D1 interfaces/hash algorithms не меняются. G2 redacted evaluation export не full result; Snapshot требует recomputation exact pinned inputs, без угадывания. A14 HANDOFF editorial-only; synthetic permit не PG04; existing first_video не guarded endpoint. Реальные roles, valid license evidence, latest trusted head, clock, immutable resolver/ledger и native execution не подтверждаются offline schemas. Полный contract freeze **BLOCKED_CONTRACT**, все новые field/edge/limit решения NOT APPROVED.
