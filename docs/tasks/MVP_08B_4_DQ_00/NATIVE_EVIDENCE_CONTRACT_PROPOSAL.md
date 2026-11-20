# DQ-01 — Native Evidence and Data Compatibility Proposal

## RESOLVE-01 — текущая редакция

**DOCS_ONLY / CONTRACT_RESOLUTION; PROPOSAL / NOT_APPROVED.** Source commit `0b61892fc4156251b19e5c529c71a6ce783b838d`, tree `7119aa23c700e484cb5c69e24063be67ddef6c6b`; дата 2026-11-20 (Europe/Kiev). Цель — DQ-F01/F02/F03. Native evidence/data draft теперь **version 2**, SQLite layout/schema/user_version остаётся **1**. Это явное versioning уточнённой ранее неутверждённой native-семантики, не изменение G1–G6/OD4 и не implementation grant. Упоминания DQ.LAB v1 в неизменённом старом OWNER_DECISION_PACKAGE — прежняя proposal-рекомендация; актуальные native правила для review задаёт эта RESOLVE-01 редакция и её exact Git SHA.

Никакой SQLite/native execution не выполнялся. Canonical литералы ниже — **DOCUMENT_ARITHMETIC_ONLY**; поля profile/checks/custody являются заданными условными fixture-входами, а не измеренными native facts. Вычисление SHA локальным верификатором **не является независимой проверкой**. Реальная qualification/approval остаётся впереди.

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

## 1. Domain, encoding и границы authority

**PROPOSAL / NOT_APPROVED.** Новый domain: `DQ.LAB`, версия 2, scope `DQ_PROCESS_KILL_LAB_ONLY`. Это native **storage-lab** наблюдения после будущего разрешения, не production permissions, не execution rights и не замена PURE. Сам факт валидной схемы/хеша не квалифицирует SQLite/profile: для этого нужны реальные тесты и независимая приёмка.

Все hashable records закрыты: общие обязательные поля `kind: "DQ.LAB.<Name>"`, `version:2`, `scope: "DQ_PROCESS_KILL_LAB_ONLY"` плюс ровно поля своей строки ниже. Unknown/missing fields/versions/scopes запрещены. Nullable означает required key со значением null либо указанным типом, а не optional key. Никаких hidden defaults/exclusions/self-digests.

C = UTF-8 строгого JSON с ASCII-key sort, ensure_ascii=False, separators=(', ', ': '), без trailing newline, Unicode normalization или BOM. Это локальная space-separated convention, не RFC JCS. Только JSON null/bool, integers 0..2^63−1 (bool не int), Unicode scalar strings, lists, closed objects; float/NaN/duplicate keys/surrogates запрещены. H = lowercase SHA-256 **всех C(record)** bytes, включая kind/version/scope. Raw payload SHA-256 и H(wrapper) — разные величины.

UUID — lowercase canonical 8-4-4-4-12 hex; Digest — ровно 64 lowercase hex; U — 0..9223372036854775807; Pos — 1..MAX; Text — 1..100000 Unicode scalars; Bool — ровно JSON true/false. `?T` = null or T. ListA..B = inclusive length. Ref<K> — закрытый объект `{kind:"DQ.LAB.K",version:2,scope:"DQ_PROCESS_KILL_LAB_ONLY",digest:Digest}`. Проверяется kind/version/scope/digest, bytes и **вся** closure; нет alias к PURE ref или raw hash. Циклы/неразрешимые refs и kind mismatch отклоняются.

Version policy: любое изменение поля/типа/семантики/канонизации требует новой schema/evidence version и review; другая measured конфигурация требует нового profile_id/digest, даже при schema_version=1. Неизвестные версии отклоняются без implicit migration; forensic read не даёт write/absence authority.

Идентичность = typed domain + version + scope + verified canonical bytes/digest. Смена profile/schema/store/epoch/root/runtime не «совместимый hash»; отказ/HOLD, без автоматического преобразования. Модель не является tamper-proof signature/attestation system.

## 2. Закрытый реестр hashable records

Общие поля выше входят в каждый preimage. Перечисленные ниже inline types закрыты в следующих разделах; сокращение Ref означает ровно четырёхполевую структуру выше.

| Name | Все дополнительные обязательные поля |
|---|---|
| QualificationProfile | profile_id:UUID; python_version:Text; python_build:Text; sqlite_version:Text; sqlite_source_id:Text; compile_options:List0..256<Text>; platform:LINUX_LOCAL или WINDOWS_NTFS; os_build:Text; filesystem:Text; configuration:Config; fault_envelope=WRITER_KILL_COORDINATOR_SURVIVES; schema_version=1 |
| RootAnchor | run_id:UUID; store_id:UUID; namespace_id:UUID; store_epoch=1; schema_version=1; profile_ref:Ref<QualificationProfile>; root_identity:PhysicalIdentity; database_identity:PhysicalIdentity |
| DataObject | binding_ref:Ref<RootAnchor>; object_id:UUID; role:DataRole; owner_job_id:?UUID; payload_hex:lowercase even-length hex; byte_length:Pos; raw_sha256:Digest |
| AdmissionKey | binding_ref:Ref<RootAnchor>; project_id:UUID; purpose_id:UUID; request_ref:Ref<DataObject>; batch_id:UUID; batch_revision:Pos; manifest_ref:Ref<DataObject> |
| WriteSet | binding_ref:Ref<RootAnchor>; mutation_id:UUID; job_id:UUID; key_ref:Ref<AdmissionKey>; expected_revision:U; resulting_revision:Pos; target_state:LabState; members:List1..16<Ref<DataObject>>; job_ref:Ref<DataObject>; event_ref:Ref<DataObject>; receipt_ref:?Ref<DataObject>; slot_ref:Ref<DataObject>; slot_action:ACQUIRE или RETAIN или RELEASE; outbox_ref:?Ref<DataObject>; read_reservation_ref:?Ref<DataObject>; terminal_proof_ref:?Ref<DataObject> |
| MutationIntent | binding_ref:Ref<RootAnchor>; mutation_id:UUID; mutation_kind:ADMIT или ADVANCE_MODEL или ENQUEUE_MODEL или RESERVE_READ_MODEL или TERMINAL_MODEL; job_id:UUID; expected_head_ref:?Ref<CommitMarker>; write_set_ref:Ref<WriteSet> |
| ProjectionRoot | binding_ref:Ref<RootAnchor>; application_sequence:U; committed_objects:List0..4096<Ref<DataObject>>; jobs:List0..16<JobIndex>; admissions:List0..16<AdmissionIndex>; active_slots:List0..16<SlotIndex>; events:List0..128<Ref<DataObject>>; outbox:List0..32<Ref<DataObject>>; read_reservations:List0..128<Ref<DataObject>>; member_links:List0..4096<MemberLink> |
| CommitMarker | binding_ref:Ref<RootAnchor>; mutation_ref:Ref<MutationIntent>; write_set_ref:Ref<WriteSet>; application_sequence:Pos; previous_marker_ref:?Ref<CommitMarker>; resulting_root_ref:Ref<ProjectionRoot> |
| ControlRoot | binding_ref:Ref<RootAnchor>; control_generation:U; pending_mutation_id:?UUID; registry:List0..128<RegistryIndex>; staged_links:List0..4096<StagedLink>; proof_acks:List0..128<Ref<ProofAck>> |
| SnapshotEvidence | binding_ref:Ref<RootAnchor>; snapshot_id:UUID; observed_head_ref:?Ref<CommitMarker>; projection_root_ref:Ref<ProjectionRoot>; control_root_ref:Ref<ControlRoot>; control_generation:U; custody:Custody; integrity_checks:Checks |
| OperationTicket | binding_ref:Ref<RootAnchor>; ticket_id:UUID; coordinator_run_id:UUID; mutation_ref:Ref<MutationIntent>; phase:P или A или R; expected_application_head_ref:?Ref<CommitMarker>; expected_control_generation:U; expected_ack_ref:?Ref<ProofAck> |
| PrepareEvidence | binding_ref:Ref<RootAnchor>; mutation_ref:Ref<MutationIntent>; write_set_ref:Ref<WriteSet>; snapshot_ref:Ref<SnapshotEvidence>; staged_member_refs:List1..16<Ref<DataObject>>; pending_mutation_id:UUID; prepared_control_generation:Pos |
| CommitProof | binding_ref:Ref<RootAnchor>; mutation_ref:Ref<MutationIntent>; marker_ref:Ref<CommitMarker>; write_set_ref:Ref<WriteSet>; snapshot_ref:Ref<SnapshotEvidence> |
| AbsenceProof | binding_ref:Ref<RootAnchor>; mutation_ref:Ref<MutationIntent>; write_set_ref:Ref<WriteSet>; snapshot_ref:Ref<SnapshotEvidence>; marker_present=false; any_apply_member_present=false; any_apply_projection_change_present=false; intent_source:REGISTERED_DB или COORDINATOR_TICKET; registry_present:Bool; ticket_sha256:Digest; expected_previous_head_ref:?Ref<CommitMarker> |
| HoldEvidence | binding_ref:Ref<RootAnchor>; mutation_id:UUID; intent_ref:?Ref<MutationIntent>; phase:P или A или R; reason:HoldReason; last_qualified_head_ref:?Ref<CommitMarker>; observed_snapshot_ref:?Ref<SnapshotEvidence>; outcome=UNKNOWN |
| RecoveryEvidence | binding_ref:Ref<RootAnchor>; mutation_id:UUID; ticket_sha256:Digest; prior_hold_ref:Ref<HoldEvidence>; resolution:COMMITTED или NOT_COMMITTED или UNKNOWN; commit_proof_ref:?Ref<CommitProof>; absence_proof_ref:?Ref<AbsenceProof>; remaining_hold_ref:?Ref<HoldEvidence> |
| ProofAck | binding_ref:Ref<RootAnchor>; mutation_ref:Ref<MutationIntent>; outcome:COMMITTED или NOT_COMMITTED; commit_proof_ref:?Ref<CommitProof>; absence_proof_ref:?Ref<AbsenceProof>; observed_application_head_ref:?Ref<CommitMarker>; control_generation:Pos |

QualificationProfile/config exact values ещё не измерены/не утверждены. Примерный version string в документе не должен использоваться как native measurement. До write cases required runtime/config fields заполняются фактическими данными и freeze; placeholders не являются валидным запускаемым profile.

## 3. Inline types

**Config**: `{driver:"PYTHON_STDLIB_SQLITE3", wrapper_control:"EXPLICIT_SQL_LEGACY", transaction_mode:"IMMEDIATE", journal_mode:"DELETE", synchronous:"FULL", foreign_keys:true, busy_timeout_ms:250, connect_timeout_ms:250, automatic_retries:0, page_size:4096, max_page_count:8192, journal_size_limit_bytes:1048576, locking_mode:"NORMAL", read_uncommitted:false, trusted_schema:false, check_same_thread:true, extension_loading:false, attach_allowed:false, temp_store:"MEMORY", mmap_size_bytes:0, cache_pages:512, auto_vacuum:"NONE", user_version:1}`. Все exact values — proposed profile vector; выбор и изменение требуют review и другого profile digest.

**PhysicalIdentity**: `{provider:"POSIX_DEVICE_INODE" или "WINDOWS_HANDLE_FILE_ID", volume_id:Text, file_id:Text}`. Значения наблюдаются по квалифицированному handle/root, не вычисляются из path. WINDOWS_HANDLE_FILE_ID не считается квалифицированным без отдельного Windows profile.

**LabState**: DRAFT, LAB_CHECKPOINT, CANCELLED, FAILED. **DataRole**: REQUEST, MANIFEST, JOB, EVENT, RECEIPT, ACTIVE_SLOT, OUTBOX, READ_RESERVATION, TERMINAL_PROOF.

**JobIndex**: `{job_id:UUID,job_ref:Ref<DataObject>}`. **AdmissionIndex**: `{key_ref:Ref<AdmissionKey>,job_id:UUID,receipt_ref:Ref<DataObject>}`. **SlotIndex**: `{project_id:UUID,purpose_id:UUID,slot_ref:Ref<DataObject>}`. **MemberLink**: `{mutation_id:UUID,member_ref:Ref<DataObject>}`.

**RegistryIndex**: `{mutation_ref:Ref<MutationIntent>,phase:PREPARED|APPLIED|RESOLVED_COMMITTED|RESOLVED_NOT_COMMITTED,marker_ref:?Ref<CommitMarker>,latest_ack_ref:?Ref<ProofAck>}`. Это закрытый enum (символы | здесь разделяют варианты, не строки). **StagedLink**: `{mutation_id:UUID,object_ref:Ref<DataObject>}`. PREPARED не имеет marker/ack; APPLIED имеет marker, но не ack; RESOLVED_COMMITTED имеет оба; RESOLVED_NOT_COMMITTED имеет ack, но не marker.

**Custody**: `{coordinator_run_id:UUID,root_identity:PhysicalIdentity,database_identity:PhysicalIdentity,expected_store_epoch:1,minimum_acknowledged_sequence:U,minimum_acknowledged_marker_ref:?Ref<CommitMarker>,exclusive_controlled_root:true,no_restore_or_replacement_observed:true}`. Эти поля — проверяемые условия ограниченного lab, не возможность доказать отсутствие произвольного скрытого tampering. Утрата custody запрещает absence proof.

**Checks**: `{sqlite_integrity:"ok",foreign_key_errors:0,canonical_closure_valid:true,projection_indices_valid:true,marker_chain_valid:true,profile_readback_matches:true,complete_snapshot:true}`. Это не self-attested shortcut: каждый true/ok должен иметь выполненную проверку и связанный raw trace в case evidence. При неизвестном/неуспешном check SnapshotEvidence не конструируется как qualified. Согласованный snapshot одновременно фиксирует application head/root и ControlRoot той же SQLite read transaction; control_generation в обоих местах совпадает.

**HoldReason**: COMMIT_ACK_LOST, PREPARE_UNRESOLVED, ACK_UNRESOLVED, STORE_UNAVAILABLE, STORE_CORRUPT, STORE_MISSING, IDENTITY_MISMATCH, PROFILE_MISMATCH, STALE_COPY, CUSTODY_LOST, PROOF_INCOMPLETE.

Все set-like arrays требуют заранее заданного ascending порядка и уникальности, несортированный вход отклоняется: compile_options ASCII order; refs по (kind,digest); jobs по job_id; admissions по key.digest; slots по (project_id,purpose_id); member_links по (mutation_id,member.digest); registry по mutation_ref.digest; staged_links по (mutation_id,object_ref.digest); proof_acks по typed ref. Event/read/outbox arrays сортируются по typed ref, не по wall clock. MAX object/member/event/outbox bounds соответствуют lab limits; graph depth <=2048, не более 8192 referenced nodes, iterative validation с cycle detection/cache (не рекурсивный workflow engine) и native record <=4 MiB, payload <=1 MiB. Это proposed safety caps, не увеличение PURE limits.

## 4. DataObject payload — закрытые synthetic DTO

payload_hex декодируется в canonical UTF-8 JSON без общего record header; decoded bytes должны совпасть с C(payload), byte_length и raw_sha256. Payload хранится как data, не исполняется. Ref edges из decoded payload также входят во всю typed closure; opaque hex не позволяет пропустить role/binding/reference validation. owner_job_id=null только REQUEST/MANIFEST; у остальных ролей совпадает с payload.job_id. Ref<DataObject> роль проверяется в каждом поле.

| Role | Ровно поля payload |
|---|---|
| REQUEST | request_id:UUID; project_id:UUID; purpose_id:UUID; synthetic_input_sha256:Digest |
| MANIFEST | batch_id:UUID; batch_revision:Pos; synthetic_label:Text |
| JOB | job_id:UUID; request_ref:Ref<DataObject> роли REQUEST; state:LabState; revision:Pos; cancel_requested:Bool |
| EVENT | event_id:UUID; mutation_id:UUID; job_id:UUID; revision_from:U; revision_to:Pos; state_from:?LabState; state_to:LabState |
| RECEIPT | receipt_id:UUID; mutation_id:UUID; job_id:UUID; key_ref:Ref<AdmissionKey>; request_ref:Ref<DataObject> роли REQUEST; accepted_revision=1 |
| ACTIVE_SLOT | store_id:UUID; namespace_id:UUID; project_id:UUID; purpose_id:UUID; job_id:UUID; status:HELD или RELEASED; occupied_since_revision:Pos; released_at_revision:?Pos |
| OUTBOX | outbox_id:UUID; job_id:UUID; effect_token:UUID; request_ref:Ref<DataObject> роли REQUEST; payload_sha256:Digest; dispatch_allowed=false |
| READ_RESERVATION | reservation_id:UUID; job_id:UUID; checkpoint_id:UUID; read_kind:MODEL_LOOKUP или MODEL_POLL; base_cursor:U; call_index:1..3 |
| TERMINAL_PROOF | proof_id:UUID; job_id:UUID; terminal_state:CANCELLED или FAILED; reason=NO_EXECUTOR_IN_LAB; executor_effect=NONE; evidence_source=STORAGE_ONLY_POLICY |

REQUEST не содержит job/M/receipt refs: admission key не цикличен и не меняется из-за worker/restart. Receipt -> Key -> Request/Manifest -> Binding; Event содержит M UUID, а не hash будущего Intent. WriteSet -> DataObjects, Intent -> WriteSet, Marker -> Intent/WriteSet/ProjectionRoot. ProjectionRoot не включает Marker, mutation/control registry, staged bytes, pending или ProofAck; integrity этих control данных проверяется отдельно по immutable intent/marker/ack links. Таким образом own hash/будущий hash не попадает в свой preimage.

## 5. Binding и validation rules

- Все binding_ref в closure совпадают. Key project/purpose равны REQUEST, batch/revision равны MANIFEST. Job/receipt/event/slot/outbox/reservation должны совпасть по job/key/request/revisions и соответствующим roles. UUID не заменяет digest и наоборот.
- WriteSet.expected_revision+1=resulting_revision; JOB и EVENT подтверждают результат, EVENT.mutation_id=WriteSet.mutation_id; Intent.job_id/M/expected_head соответствуют WriteSet и предыдущему marker. Members — только **новые A-applied DataObjects**; existing committed inputs доступны через closure, но не включаются как новые members. Staged input data не доказывает A-membership.
- ADMIT: expected_revision=0, resulting=1, DRAFT, новый job, receipt, event и HELD slot — mandatory A-members; fresh request/manifest включены, если ещё не committed. ADVANCE_MODEL: DRAFT -> LAB_CHECKPOINT; RESERVE_READ_MODEL/ENQUEUE_MODEL удерживают state, увеличивают revision/event, соответствующий data row обязателен. ENQUEUE максимум один token/job, не вызывает executor. TERMINAL_MODEL только из nonterminal lab state в CANCELLED/FAILED с terminal proof и RELEASE slot в том же A. Terminal job не переоткрывается.
- RETAIN slot_ref указывает прежний HELD slot; ACQUIRE/RELEASE создают новый slot DataObject. RELEASE.released_at_revision=resulting revision. Original admission receipt никогда не перезаписывается. Counter checkpoints не сбрасываются от reopen/duplicate; первый lab не реализует новый provider cursor или внешний retry.
- ProjectionRoot отражает **полный** application state, включая immutable history и M-member links, но без control/future marker. Хэш вычисляется до вставки marker по тому же transaction view; после commit его восстановление обязано совпасть. Marker/application_sequence увеличивается ровно на 1 от expected head. Control generation увеличивается на 1 в каждой committed P/A/R; application_sequence только в A. P/R не создают application commit.
- ControlRoot отражает авторитетный registry/staged links/ack indices и pending ID, но не произвольные unindexed evidence blobs. Canonical evidence nodes могут быть собраны для readback без изменения authoritative roots. OperationTicket находится у coordinator вне authoritative DB projections. P/A tickets имеют expected_ack_ref=null; R ticket ссылается на заранее вычисленный exact ProofAck, binding/M/head/control_generation совпадают. PrepareEvidence требует registry PREPARED, pending=M, exact staged closure и тот же qualified Snapshot/control root; только это разрешает A той же M. Unknown P не разрешает A до такого readback.
- CommitProof: exact Marker/Intent/WriteSet из полного snapshot, complete M-members/root/indices и qualified custody. AbsenceProof: ни marker, ни M-applied objects/links/projection changes, expected previous head согласован; staged/control bytes не входят в эту проверку присутствия. Если registry M не был committed в P, ожидаемый Intent/WS берётся из сохранённого coordinator ticket (intent_source=COORDINATOR_TICKET, registry_present=false); это expected input, не якобы прочитанная DB row. Для REGISTERED_DB registry_present=true и bytes проверены в DB. Ticket digest и binding всегда обязательны; отсутствие прежней DB никогда не absence proof. В одном qualified snapshot нельзя одновременно выдать оба исхода для одной M. Исторический negative replay возвращает прежний AbsenceProof/Snapshot и final ProofAck; свежий current ControlRoot должен подтвердить неизменный RESOLVED_NOT_COMMITTED и отсутствие A для M. Не подделывать новый AbsenceProof с current head вместо expected historical head.
- RecoveryEvidence: COMMITTED -> только commit_proof_ref non-null; NOT_COMMITTED -> только absence_proof_ref non-null; UNKNOWN -> только remaining_hold_ref non-null. Снятие HOLD не следует из самого RecoveryEvidence: нужен verified ProofAck/control readback.
- ProofAck: ровно один proof_ref соответствует outcome; head/control_generation связаны с тем же consistent resolution snapshot. R transaction сохраняет Ack, registry outcome и pending clear атомарно; qualified post-R Snapshot/ControlRoot должен подтвердить exact expected Ack, control_generation+1 и отсутствие pending M. Unknown R повторно выполняет только read-only inspect; после доказанного отсутствия R допустим тот же exact R Ack step без повторения A, пока original proof/head/generation остаются неизменными; после неизвестного R ACK новые A остаются запрещены до qualified reopen/readback Ack и исходного M proof. Нет «ACK строка значит всё готово».

## 6. Errors и fail-closed

Nonhashable transport **DQ.LAB.Error**, version=2/scope тот же, ровно поля: `code:ErrorCode`, `phase:INIT|OPEN|P|A|R|READ`, `mutation_id:?UUID`, `application_outcome:COMMITTED|NOT_COMMITTED|UNKNOWN|NOT_ATTEMPTED`, `namespace_hold:Bool`, `safe_message:MessageForCode`, `executor_effect:"NOT_AUTHORIZED"`.

| ErrorCode | Exact safe_message |
|---|---|
| INVALID_RECORD | Record is invalid. |
| IDENTITY_MISMATCH | Store identity does not match. |
| VERSION_MISMATCH | Schema or profile version does not match. |
| STORE_MISSING | Expected database is missing. |
| STORE_UNAVAILABLE | Store is unavailable. |
| STORE_CORRUPT | Store integrity cannot be established. |
| STALE_COPY | Store continuity cannot be established. |
| MUTATION_ID_CONFLICT | Mutation identity conflicts with content. |
| IDEMPOTENCY_CONFLICT | Admission identity conflicts with content. |
| ACTIVE_INTENT_CONFLICT | An active slot already holds this purpose. |
| CAS_CONFLICT | Job revision has changed. |
| BUSY | Database is busy. |
| RESOURCE_LIMIT | Lab resource limit is exceeded. |
| UNKNOWN_COMMIT_OUTCOME | Mutation outcome is unknown. |
| SCOPE_DENIED | Operation is outside the lab scope. |

Проверки по порядку: bounded closed encoding/version -> anchor/scope/profile -> availability/integrity/custody -> pending/resolution -> immutable M/key/replay -> slot/CAS/role/bounds -> SQL outcome proof. Во время P/A/R uncertainty текущей control phase не исчезает из-за ошибки диагностического чтения; qualified binding/M/ticket/proofs сохраняются. application_outcome описывает только A: UNKNOWN до qualified A proof, COMMITTED/NOT_COMMITTED после него. При unknown R phase=R, namespace_hold=true и disposition=HOLD сохраняются даже при application_outcome=COMMITTED. Известное A не понижается из-за lost R ACK; это не разрешение повторять A. NOT_ATTEMPTED описывает новый не начатый A, а не отсутствие исхода прежней M. Никаких raw secrets/stack traces в safe_message.

Открытые для независимой проверки вопросы: [OWNER_DECISION_PACKAGE.md](OWNER_DECISION_PACKAGE.md), категория B. В текущем DOCS_ONLY этапе не создаются native proof records и не заявляется native PASS.

## 7. DQ-F01 — qualified custody и absence

NOT_COMMITTED запрещён без **всех** предпосылок: исходный coordinator жив в том же непрерывном run; точный retained ticket bundle (canonical ticket и вся expected immutable closure), binding/profile/physical identities совпадают; controlled root/database/journals не теряли custody; known head/watermark не откатились; полный consistent snapshot и все native checks действительно выполнены; ни marker, ни один A-member/link/projection change для M не присутствуют; application root равен expected previous root. Проверка отсутствия — в committed/projection tables, не в staged/control cache. Строка registry PREPARED со staged members может присутствовать и не означает A COMMITTED.

Поле true в Checks/Custody само не доказывает выполнение проверки: нужны provenance и доступные квалифицированные наблюдения. Старый SnapshotEvidence не подтверждает текущую custody после потери ticket/coordinator. Из DB нельзя заново назначить ожидаемую identity или синтезировать утраченную историю coordinator. Неизвестные предпосылки означают UNKNOWN/HOLD; отрицательная fixture не «ремонтируется» чтением других positive literals из каталога.

**Первый DQ-01 не квалифицирует восстановление после падения всего приложения.** Он рассматривает writer/contender kill при живом coordinator. Потеря coordinator, его ticket bundle/continuity или custody — BLOCKED_WHOLE_APPLICATION_RECOVERY/UNKNOWN; новый coordinator не выдаёт absence proof даже если database читается. Общий restore/power-loss/malicious rollback не квалифицируются.

При доказанном отсутствии P registry AbsenceProof использует intent_source=COORDINATOR_TICKET и registry_present=false. Отсутствие DB целиком никогда не становится таким proof. Negative R может атомарно зафиксировать immutable expected intent/WS/input closure из ticket, RESOLVED_NOT_COMMITTED и Ack при pending=null, если qualified pre-R C0/head/generation неизменны и нет чужого pending. Это не утверждение, что P ранее committed, и не применение A. Повтор закрытой M — только historical read-only result.

## 8. DQ-F02 — точные поколения и два outcome axis

Одинаковая M связывает P/A/R, но application outcome A и control outcome R не синонимы. Следующие определения применяются до запуска native tests и не могут зависеть от класса исключения:

- Qualified pre-P ControlRoot имеет generation g. P commit увеличивает generation до g+1; application_sequence не меняется. Ticket_P.expected_control_generation=g. PrepareEvidence.prepared_control_generation=g+1 и snapshot generation=g+1. После qualified P известен PREPARED и A ещё NOT_ATTEMPTED; namespace barrier блокирует **другие** M, но позволяет A той же M по ticket_A.
- Ticket_A.expected_control_generation=g+1. A commit увеличивает control_generation до g+2 и application_sequence на 1. A COMMIT call/ACK без proof не устанавливает COMMITTED. Qualified CommitProof фиксирует A COMMITTED, но pending M остаётся до R.
- Пусть qualified **pre-R** SnapshotEvidence/control root имеет G и head h. ProofAck.control_generation **равно G+1**, не G. Ack.observed_application_head_ref=h. Его A proof ссылается на pre-R Snapshot, а не на будущий post-R snapshot. Ticket_R.expected_control_generation=G, expected_application_head_ref=h, expected_ack_ref=H(exact Ack G+1).
- R транзакция сравнивает binding/M/h/G и actual pre-R control root, сохраняет exact Ack, registry resolved state и pending clear, увеличивает generation ровно до G+1. Application head/root/sequence не меняются. Qualified **post-R** Snapshot.control_generation=ControlRoot.control_generation=Ack.control_generation=G+1; head=h; pending=null; registry.latest_ack_ref и proof_acks указывают exact expected Ack и outcome.
- Пока post-R readback отсутствует/невалиден, control outcome R=UNKNOWN и namespace barrier/HOLD остаются true, даже если A уже COMMITTED. RecoveryEvidence.resolution описывает **A**, а не доказательство R: один RecoveryEvidence(COMMITTED) не снимает HOLD. HoldEvidence.outcome=UNKNOWN относится к незавершённой phase P/A/R; RecoveryEvidence.remaining_hold_ref относится к A-uncertainty, не к отдельному R barrier. Нулевой remaining_hold_ref после доказанного A не разрешает снять namespace barrier без post-R Ack readback.
- R absence — не application AbsenceProof. Это закрытый predicate проверки уже существующих typed inputs: retained ticket_R + exact expected Ack bytes + original qualified A proof + fresh qualified Snapshot. Требуются ControlRoot == pre-R ControlRoot (точные bytes/ref), generation=G, head=h, pending=M (либо null для unprepared-negative close), отсутствие expected Ack в registry/proof_acks, unchanged A state и custody. После этого допустим только **тот же R с теми же M/Ack bytes/ref**. Нельзя пересчитать новый Ack от fresh Snapshot, повторить A, сменить M или считать отсутствие Ack само по себе proof.
- При fresh Snapshot с другим UUID/custody watermark, но теми же authoritative application/control roots, original Ack сохраняется неизменным: он связывает original A proof/pre-R Snapshot. Свежий snapshot служит guard для retry, не новым preimage original Ack. Если exact Ack bundle утрачен, поколение/head/identity stale, read partial или DB недоступна — R retry запрещён.

Именованный predicate R_ABSENT_FOR_TICKET — условие над существующими закрытыми records, **не новый hashable proof kind**. DQ.LAB v2 сохраняет те же 17 record field sets, но устраняет прежнюю неоднозначность generations/A-vs-R. SQLite schema_version/user_version=1 не меняются. Native v1 refs не принимаются как v2 refs.

### Acyclic dependency order

DataObject/Key → WriteSet → MutationIntent; application ProjectionRoot не содержит Marker/control/Ack; Marker → Intent/WS/application root. Pre-R ControlRoot не содержит будущий Ack. Pre-R Snapshot → этот pre-R ControlRoot; CommitProof/AbsenceProof → pre-R Snapshot; ProofAck → этот proof; ticket_R → expected Ack. **Только post-R** ControlRoot → Ack; post-R Snapshot → post-R ControlRoot. Никакое поле Ack или original proof не ссылается на post-R Snapshot/ControlRoot. Иначе graph отвергается до использования, без попытки найти «циклический expected SHA».

## 9. Canonical fixture catalogue — не native execution

Общие version/scope в каждом literal обязательны; bytes между fenced block delimiters не включают завершающий newline. SQLite version 3.35.0 и DOCUMENT_FIXTURE* здесь синтетические константы для арифметики, не измерение или qualified profile. Положительные oracles условны на реально подтверждённых runtime-предпосылках; отрицательные specimens могут иметь корректный hash/shape и всё равно быть недопустимыми evidence.

Каталог содержит 58 literal entries, 57 различных canonical preimages: HT и HC намеренно совпадают как HoldEvidence(CUSTODY_LOST), а их разные обстоятельства заданы отдельными case facts. Это alias одинаковых bytes, не разные bytes с одинаковым hash. Каталог содержит альтернативные истории (commit branch, negative close без P, negative close после P) и ошибочные specimens. Одинаковый binding/M в этих литералах не означает, что все их ControlRoot одновременно существовали в одной DB. Только inputs/facts выбранного case доступны его oracle; нельзя использовать missing ticket/Ack из другой записи каталога.

**C-A01 — строго case-local inputs.** Доступные bytes каждого DOC.ORACLE ограничены его явными `inputs` и полной проверенной closure их типизированных ссылок, включая refs из decoded DataObject payload. Каталог служит только resolver для этих явных ссылок; implicit global catalogue lookup, поиск подходящего ticket по UUID/M или превращение поля Digest в дополнительный input запрещены. Для qualified absence обязательны фактические canonical bytes исходного ticket в case-local input set, проверка его typed ref/полной closure и совпадение H(ticket) с `AbsenceProof.ticket_sha256`, binding/M и соответствующим исходным phase/head/generation. В F01-P03 `original_ticket` явно указывает на V-TP; в F02-P07 — на V-TA. Поле `ticket` в этих двух cases остаётся отдельным ticket_R и не заменяет исходный ticket.

`ticket_retained=true` — только условная fixture-предпосылка, не самостоятельное доказательство наличия bytes, custody или authority. Missing/mismatched original ticket, `ticket_retained=false`, потеря непрерывности coordinator, custody либо требуемых native checks запрещают qualified absence и снятие HOLD по нему. Добавленный input не доказывает custody и не заменяет остальные conjunctive prerequisites раздела 7. В отрицательных missing-ticket cases отсутствующие bytes не восстанавливаются из соседних entries даже при читаемой DB или известном digest. Эти уточнения меняют только nonhashable fixture inputs/правило доступности: все 58 canonical preimages, их lengths/SHA-256 и 23 expected outcomes неизменны; native version 2 и SQLite schema/user_version 1 сохраняются.

### V-Q — DQ.LAB.QualificationProfile

Length: 1128 UTF-8 bytes. SHA-256: `3b6eecf71e4c6a0780e7ea010f067f915bb7e2577025189522beffc97304603a`.

```json
{"compile_options": [], "configuration": {"attach_allowed": false, "auto_vacuum": "NONE", "automatic_retries": 0, "busy_timeout_ms": 250, "cache_pages": 512, "check_same_thread": true, "connect_timeout_ms": 250, "driver": "PYTHON_STDLIB_SQLITE3", "extension_loading": false, "foreign_keys": true, "journal_mode": "DELETE", "journal_size_limit_bytes": 1048576, "locking_mode": "NORMAL", "max_page_count": 8192, "mmap_size_bytes": 0, "page_size": 4096, "read_uncommitted": false, "synchronous": "FULL", "temp_store": "MEMORY", "transaction_mode": "IMMEDIATE", "trusted_schema": false, "user_version": 1, "wrapper_control": "EXPLICIT_SQL_LEGACY"}, "fault_envelope": "WRITER_KILL_COORDINATOR_SURVIVES", "filesystem": "DOCUMENT_FIXTURE_LOCAL", "kind": "DQ.LAB.QualificationProfile", "os_build": "DOCUMENT_FIXTURE", "platform": "LINUX_LOCAL", "profile_id": "00000000-0000-0000-0000-000000000001", "python_build": "DOCUMENT_FIXTURE_NOT_MEASURED", "python_version": "3.10.22", "schema_version": 1, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "sqlite_source_id": "DOCUMENT_FIXTURE_NO_ENGINE_EXECUTION", "sqlite_version": "3.35.0", "version": 2}
```

### V-B — DQ.LAB.RootAnchor

Length: 670 UTF-8 bytes. SHA-256: `0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d`.

```json
{"database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "kind": "DQ.LAB.RootAnchor", "namespace_id": "00000000-0000-0000-0000-000000000004", "profile_ref": {"digest": "3b6eecf71e4c6a0780e7ea010f067f915bb7e2577025189522beffc97304603a", "kind": "DQ.LAB.QualificationProfile", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "run_id": "00000000-0000-0000-0000-000000000002", "schema_version": 1, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "store_epoch": 1, "store_id": "00000000-0000-0000-0000-000000000003", "version": 2}
```

### V-D_REQ — DQ.LAB.DataObject

Length: 982 UTF-8 bytes. SHA-256: `09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "byte_length": 256, "kind": "DQ.LAB.DataObject", "object_id": "00000000-0000-0000-0000-000000000014", "owner_job_id": null, "payload_hex": "7b2270726f6a6563745f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303035222c2022707572706f73655f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303036222c2022726571756573745f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303135222c202273796e7468657469635f696e7075745f736861323536223a202237633631633463653065326534646134393663613162376632303230393034653763336232306535616139313836663732653431346430316661646138653265227d", "raw_sha256": "332e9675ce3139410f9c7645609caec19cc5361c475f36f17aa55a86caf98295", "role": "REQUEST", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-D_MAN — DQ.LAB.DataObject

Length: 689 UTF-8 bytes. SHA-256: `40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "byte_length": 109, "kind": "DQ.LAB.DataObject", "object_id": "00000000-0000-0000-0000-000000000016", "owner_job_id": null, "payload_hex": "7b2262617463685f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303137222c202262617463685f7265766973696f6e223a20312c202273796e7468657469635f6c6162656c223a2022444f43554d454e545f4f4e4c59227d", "raw_sha256": "eee2eb34224cf4e4347d6b15ad84fb4cfc0aed9e3d578117c687ab0a68586052", "role": "MANIFEST", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-K — DQ.LAB.AdmissionKey

Length: 789 UTF-8 bytes. SHA-256: `3c3edc405623f149d33fd71770f4db42ab4410a8c20902729286b5af0d9ec8cf`.

```json
{"batch_id": "00000000-0000-0000-0000-000000000017", "batch_revision": 1, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.AdmissionKey", "manifest_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "project_id": "00000000-0000-0000-0000-000000000005", "purpose_id": "00000000-0000-0000-0000-000000000006", "request_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-D_JOB — DQ.LAB.DataObject

Length: 1070 UTF-8 bytes. SHA-256: `de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "byte_length": 285, "kind": "DQ.LAB.DataObject", "object_id": "00000000-0000-0000-0000-000000000018", "owner_job_id": "00000000-0000-0000-0000-000000000007", "payload_hex": "7b2263616e63656c5f726571756573746564223a2066616c73652c20226a6f625f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303037222c2022726571756573745f726566223a207b22646967657374223a202230396334373166326132303936313630613263373061326666653432383936336236346635313666356162666238643734323738633333636562303932393235222c20226b696e64223a202244512e4c41422e446174614f626a656374222c202273636f7065223a202244515f50524f434553535f4b494c4c5f4c41425f4f4e4c59222c202276657273696f6e223a20327d2c20227265766973696f6e223a20312c20227374617465223a20224452414654227d", "raw_sha256": "49d94b8afa2549ac39a09d816bfc109dde1cd49f4c9615465738602971449808", "role": "JOB", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-D_EV — DQ.LAB.DataObject

Length: 974 UTF-8 bytes. SHA-256: `dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "byte_length": 236, "kind": "DQ.LAB.DataObject", "object_id": "00000000-0000-0000-0000-000000000019", "owner_job_id": "00000000-0000-0000-0000-000000000007", "payload_hex": "7b226576656e745f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303161222c20226a6f625f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303037222c20226d75746174696f6e5f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303038222c20227265766973696f6e5f66726f6d223a20302c20227265766973696f6e5f746f223a20312c202273746174655f66726f6d223a206e756c6c2c202273746174655f746f223a20224452414654227d", "raw_sha256": "f65c77fb6700d3cee52a23f27e448dd04b015c8e67af906aed17ebd3cf364a05", "role": "EVENT", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-D_REC — DQ.LAB.DataObject

Length: 1566 UTF-8 bytes. SHA-256: `cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "byte_length": 531, "kind": "DQ.LAB.DataObject", "object_id": "00000000-0000-0000-0000-00000000001b", "owner_job_id": "00000000-0000-0000-0000-000000000007", "payload_hex": "7b2261636365707465645f7265766973696f6e223a20312c20226a6f625f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303037222c20226b65795f726566223a207b22646967657374223a202233633365646334303536323366313439643333666437313737306634646234326162343431306138633230393032373239323836623561663064396563386366222c20226b696e64223a202244512e4c41422e41646d697373696f6e4b6579222c202273636f7065223a202244515f50524f434553535f4b494c4c5f4c41425f4f4e4c59222c202276657273696f6e223a20327d2c20226d75746174696f6e5f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303038222c2022726563656970745f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303163222c2022726571756573745f726566223a207b22646967657374223a202230396334373166326132303936313630613263373061326666653432383936336236346635313666356162666238643734323738633333636562303932393235222c20226b696e64223a202244512e4c41422e446174614f626a656374222c202273636f7065223a202244515f50524f434553535f4b494c4c5f4c41425f4f4e4c59222c202276657273696f6e223a20327d7d", "raw_sha256": "44d794682a5ce41ee910926c6f0cbb78906cf5db5a86448d0a12dd9f1fc9c3fd", "role": "RECEIPT", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-D_SLOT — DQ.LAB.DataObject

Length: 1196 UTF-8 bytes. SHA-256: `f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "byte_length": 344, "kind": "DQ.LAB.DataObject", "object_id": "00000000-0000-0000-0000-00000000001d", "owner_job_id": "00000000-0000-0000-0000-000000000007", "payload_hex": "7b226a6f625f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303037222c20226e616d6573706163655f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303034222c20226f636375706965645f73696e63655f7265766973696f6e223a20312c202270726f6a6563745f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303035222c2022707572706f73655f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303036222c202272656c65617365645f61745f7265766973696f6e223a206e756c6c2c2022737461747573223a202248454c44222c202273746f72655f6964223a202230303030303030302d303030302d303030302d303030302d303030303030303030303033227d", "raw_sha256": "a262490fc486feea26c1da6508af32a575c3598185a9587740ef6880b5739429", "role": "ACTIVE_SLOT", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-W — DQ.LAB.WriteSet

Length: 2373 UTF-8 bytes. SHA-256: `73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "event_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_revision": 0, "job_id": "00000000-0000-0000-0000-000000000007", "job_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "key_ref": {"digest": "3c3edc405623f149d33fd71770f4db42ab4410a8c20902729286b5af0d9ec8cf", "kind": "DQ.LAB.AdmissionKey", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.WriteSet", "members": [{"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "mutation_id": "00000000-0000-0000-0000-000000000008", "outbox_ref": null, "read_reservation_ref": null, "receipt_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "resulting_revision": 1, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "slot_action": "ACQUIRE", "slot_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "target_state": "DRAFT", "terminal_proof_ref": null, "version": 2}
```

### V-I — DQ.LAB.MutationIntent

Length: 592 UTF-8 bytes. SHA-256: `eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_head_ref": null, "job_id": "00000000-0000-0000-0000-000000000007", "kind": "DQ.LAB.MutationIntent", "mutation_id": "00000000-0000-0000-0000-000000000008", "mutation_kind": "ADMIT", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```

### V-P0 — DQ.LAB.ProjectionRoot

Length: 434 UTF-8 bytes. SHA-256: `b39a29ebb164083b86d6daae49da663bd0e12666431f021b9b6467831c20e0bb`.

```json
{"active_slots": [], "admissions": [], "application_sequence": 0, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "committed_objects": [], "events": [], "jobs": [], "kind": "DQ.LAB.ProjectionRoot", "member_links": [], "outbox": [], "read_reservations": [], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-C0 — DQ.LAB.ControlRoot

Length: 364 UTF-8 bytes. SHA-256: `a0dc2da4497bb9ce63806b336a7224d0c8b233c33d346151ea7c854c97ad4bc5`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 0, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": null, "proof_acks": [], "registry": [], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [], "version": 2}
```

### V-C1 — DQ.LAB.ControlRoot

Length: 2027 UTF-8 bytes. SHA-256: `6b1c2284ebc5e121b5a83e9b833b37d71fa427dd59256624a704bc8364a6ee90`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 1, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": "00000000-0000-0000-0000-000000000008", "proof_acks": [], "registry": [{"latest_ack_ref": null, "marker_ref": null, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "PREPARED"}], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [{"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "version": 2}
```

### V-S0 — DQ.LAB.SnapshotEvidence

Length: 1431 UTF-8 bytes. SHA-256: `ba912087eaab64cb2dd57fa2a6dd1e1bdc77e4522a3ebb8bb41d17099507b050`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 0, "control_root_ref": {"digest": "a0dc2da4497bb9ce63806b336a7224d0c8b233c33d346151ea7c854c97ad4bc5", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": null, "minimum_acknowledged_sequence": 0, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": null, "projection_root_ref": {"digest": "b39a29ebb164083b86d6daae49da663bd0e12666431f021b9b6467831c20e0bb", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-00000000001e", "version": 2}
```

### V-SP — DQ.LAB.SnapshotEvidence

Length: 1431 UTF-8 bytes. SHA-256: `a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 1, "control_root_ref": {"digest": "6b1c2284ebc5e121b5a83e9b833b37d71fa427dd59256624a704bc8364a6ee90", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": null, "minimum_acknowledged_sequence": 0, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": null, "projection_root_ref": {"digest": "b39a29ebb164083b86d6daae49da663bd0e12666431f021b9b6467831c20e0bb", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-00000000001f", "version": 2}
```

### V-TP — DQ.LAB.OperationTicket

Length: 668 UTF-8 bytes. SHA-256: `07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "expected_ack_ref": null, "expected_application_head_ref": null, "expected_control_generation": 0, "kind": "DQ.LAB.OperationTicket", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "P", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_id": "00000000-0000-0000-0000-000000000020", "version": 2}
```

### V-TA — DQ.LAB.OperationTicket

Length: 668 UTF-8 bytes. SHA-256: `4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "expected_ack_ref": null, "expected_application_head_ref": null, "expected_control_generation": 1, "kind": "DQ.LAB.OperationTicket", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "A", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_id": "00000000-0000-0000-0000-000000000021", "version": 2}
```

### V-PE — DQ.LAB.PrepareEvidence

Length: 1878 UTF-8 bytes. SHA-256: `53c7cf684335adfdfedbdae9183af8adbe4bc5b28a85e69e2304c3c4a7ba2ca2`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.PrepareEvidence", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "pending_mutation_id": "00000000-0000-0000-0000-000000000008", "prepared_control_generation": 1, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_ref": {"digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9", "kind": "DQ.LAB.SnapshotEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "staged_member_refs": [{"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```

### V-AP — DQ.LAB.AbsenceProof

Length: 1081 UTF-8 bytes. SHA-256: `19d83bcf3e9f47ac97c36c52244685e339848b5b1663a3b1e208165472ff263c`.

```json
{"any_apply_member_present": false, "any_apply_projection_change_present": false, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_previous_head_ref": null, "intent_source": "REGISTERED_DB", "kind": "DQ.LAB.AbsenceProof", "marker_present": false, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "registry_present": true, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_ref": {"digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9", "kind": "DQ.LAB.SnapshotEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "ticket_sha256": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a", "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```

### V-AP0 — DQ.LAB.AbsenceProof

Length: 1087 UTF-8 bytes. SHA-256: `2d7659daaa09a3cde2479a7d72001c3e336c2b1cdf2e134e235ab32abaf02bc9`.

```json
{"any_apply_member_present": false, "any_apply_projection_change_present": false, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_previous_head_ref": null, "intent_source": "COORDINATOR_TICKET", "kind": "DQ.LAB.AbsenceProof", "marker_present": false, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "registry_present": false, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_ref": {"digest": "ba912087eaab64cb2dd57fa2a6dd1e1bdc77e4522a3ebb8bb41d17099507b050", "kind": "DQ.LAB.SnapshotEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "ticket_sha256": "07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831", "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```

### V-ACKN1 — DQ.LAB.ProofAck

Length: 734 UTF-8 bytes. SHA-256: `379071bf39c8f7ea8115d2b9c97830ffd0e5ee409ab342d0cefacf647191a843`.

```json
{"absence_proof_ref": {"digest": "2d7659daaa09a3cde2479a7d72001c3e336c2b1cdf2e134e235ab32abaf02bc9", "kind": "DQ.LAB.AbsenceProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": null, "control_generation": 1, "kind": "DQ.LAB.ProofAck", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "observed_application_head_ref": null, "outcome": "NOT_COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-TRN0 — DQ.LAB.OperationTicket

Length: 820 UTF-8 bytes. SHA-256: `4c5190b1c469b2c1ad69896a645bdd6af6196f1033f154256684cd00ae77b6a1`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "expected_ack_ref": {"digest": "379071bf39c8f7ea8115d2b9c97830ffd0e5ee409ab342d0cefacf647191a843", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_application_head_ref": null, "expected_control_generation": 0, "kind": "DQ.LAB.OperationTicket", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "R", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_id": "00000000-0000-0000-0000-00000000002a", "version": 2}
```

### V-CN1 — DQ.LAB.ControlRoot

Length: 2315 UTF-8 bytes. SHA-256: `66b15ecc3593d1a9bca643266f56dd5d338007d53084bd26c2611bdda2e9e84a`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 1, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": null, "proof_acks": [{"digest": "379071bf39c8f7ea8115d2b9c97830ffd0e5ee409ab342d0cefacf647191a843", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "registry": [{"latest_ack_ref": {"digest": "379071bf39c8f7ea8115d2b9c97830ffd0e5ee409ab342d0cefacf647191a843", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "marker_ref": null, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "RESOLVED_NOT_COMMITTED"}], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [{"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "version": 2}
```

### V-SN1 — DQ.LAB.SnapshotEvidence

Length: 1431 UTF-8 bytes. SHA-256: `ef0663d0862997715fa43b83cfd7280e28013088f5d290cc82a207694d6ed4e1`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 1, "control_root_ref": {"digest": "66b15ecc3593d1a9bca643266f56dd5d338007d53084bd26c2611bdda2e9e84a", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": null, "minimum_acknowledged_sequence": 0, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": null, "projection_root_ref": {"digest": "b39a29ebb164083b86d6daae49da663bd0e12666431f021b9b6467831c20e0bb", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-00000000002b", "version": 2}
```

### V-P1 — DQ.LAB.ProjectionRoot

Length: 3833 UTF-8 bytes. SHA-256: `8c53151c9e0879e66bfa4d14d6b3e977d9e46be992a8df179286e7b483ec1f3b`.

```json
{"active_slots": [{"project_id": "00000000-0000-0000-0000-000000000005", "purpose_id": "00000000-0000-0000-0000-000000000006", "slot_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "admissions": [{"job_id": "00000000-0000-0000-0000-000000000007", "key_ref": {"digest": "3c3edc405623f149d33fd71770f4db42ab4410a8c20902729286b5af0d9ec8cf", "kind": "DQ.LAB.AdmissionKey", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "receipt_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "application_sequence": 1, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "committed_objects": [{"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "events": [{"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "jobs": [{"job_id": "00000000-0000-0000-0000-000000000007", "job_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "kind": "DQ.LAB.ProjectionRoot", "member_links": [{"member_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008"}, {"member_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008"}, {"member_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008"}, {"member_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008"}, {"member_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008"}, {"member_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008"}], "outbox": [], "read_reservations": [], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-MK — DQ.LAB.CommitMarker

Length: 854 UTF-8 bytes. SHA-256: `64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1`.

```json
{"application_sequence": 1, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.CommitMarker", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "previous_marker_ref": null, "resulting_root_ref": {"digest": "8c53151c9e0879e66bfa4d14d6b3e977d9e46be992a8df179286e7b483ec1f3b", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```

### V-C2 — DQ.LAB.ControlRoot

Length: 2182 UTF-8 bytes. SHA-256: `6e1e5c001d3c9277dcb759d493e17068d3adf179ef8a2f43b51246e07a3658cb`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 2, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": "00000000-0000-0000-0000-000000000008", "proof_acks": [], "registry": [{"latest_ack_ref": null, "marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "APPLIED"}], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [{"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "version": 2}
```

### V-SA — DQ.LAB.SnapshotEvidence

Length: 1587 UTF-8 bytes. SHA-256: `2c59d8302a371d81d2ca858b319f46ef7095e4b22de7b6425cee5c81db31748e`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 2, "control_root_ref": {"digest": "6e1e5c001d3c9277dcb759d493e17068d3adf179ef8a2f43b51246e07a3658cb", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": null, "minimum_acknowledged_sequence": 0, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "projection_root_ref": {"digest": "8c53151c9e0879e66bfa4d14d6b3e977d9e46be992a8df179286e7b483ec1f3b", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-000000000022", "version": 2}
```

### V-CP — DQ.LAB.CommitProof

Length: 969 UTF-8 bytes. SHA-256: `3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.CommitProof", "marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_ref": {"digest": "2c59d8302a371d81d2ca858b319f46ef7095e4b22de7b6425cee5c81db31748e", "kind": "DQ.LAB.SnapshotEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```

### V-ACK3 — DQ.LAB.ProofAck

Length: 885 UTF-8 bytes. SHA-256: `0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae`.

```json
{"absence_proof_ref": null, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": {"digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1", "kind": "DQ.LAB.CommitProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 3, "kind": "DQ.LAB.ProofAck", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "observed_application_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "outcome": "COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-TR — DQ.LAB.OperationTicket

Length: 976 UTF-8 bytes. SHA-256: `45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "expected_ack_ref": {"digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_application_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_control_generation": 2, "kind": "DQ.LAB.OperationTicket", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "R", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_id": "00000000-0000-0000-0000-000000000023", "version": 2}
```

### V-C3 — DQ.LAB.ControlRoot

Length: 2467 UTF-8 bytes. SHA-256: `4b7b989795efd24554ed3777790c33a86765315dccb5d5c76340a7890e688cf4`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 3, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": null, "proof_acks": [{"digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "registry": [{"latest_ack_ref": {"digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "RESOLVED_COMMITTED"}], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [{"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "version": 2}
```

### V-SR — DQ.LAB.SnapshotEvidence

Length: 1743 UTF-8 bytes. SHA-256: `d93a8a4b4df65b05d0d56d3f57800e08be463cc4309106553bf0202357e8bb62`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 3, "control_root_ref": {"digest": "4b7b989795efd24554ed3777790c33a86765315dccb5d5c76340a7890e688cf4", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "minimum_acknowledged_sequence": 1, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "projection_root_ref": {"digest": "8c53151c9e0879e66bfa4d14d6b3e977d9e46be992a8df179286e7b483ec1f3b", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-000000000024", "version": 2}
```

### V-SRA — DQ.LAB.SnapshotEvidence

Length: 1743 UTF-8 bytes. SHA-256: `10aaf5ee0b08c5ae6638301ce933256f296593a2c0604d565116c52c9a108358`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 2, "control_root_ref": {"digest": "6e1e5c001d3c9277dcb759d493e17068d3adf179ef8a2f43b51246e07a3658cb", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "minimum_acknowledged_sequence": 1, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "projection_root_ref": {"digest": "8c53151c9e0879e66bfa4d14d6b3e977d9e46be992a8df179286e7b483ec1f3b", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-000000000025", "version": 2}
```

### V-ACKN2 — DQ.LAB.ProofAck

Length: 734 UTF-8 bytes. SHA-256: `16d866cf0096216a6f35aa9d424b8cb0089ca7874860633667042efa1ef49856`.

```json
{"absence_proof_ref": {"digest": "19d83bcf3e9f47ac97c36c52244685e339848b5b1663a3b1e208165472ff263c", "kind": "DQ.LAB.AbsenceProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": null, "control_generation": 2, "kind": "DQ.LAB.ProofAck", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "observed_application_head_ref": null, "outcome": "NOT_COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-TRN — DQ.LAB.OperationTicket

Length: 820 UTF-8 bytes. SHA-256: `1a9d07ade8de7cb512ccaa61ca7cb5700c786a82c7e6cf10eae74fd93539ce87`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "expected_ack_ref": {"digest": "16d866cf0096216a6f35aa9d424b8cb0089ca7874860633667042efa1ef49856", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_application_head_ref": null, "expected_control_generation": 1, "kind": "DQ.LAB.OperationTicket", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "R", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_id": "00000000-0000-0000-0000-000000000026", "version": 2}
```

### V-CN2 — DQ.LAB.ControlRoot

Length: 2315 UTF-8 bytes. SHA-256: `9a18109c3bf469c1b7e91afdf07c4cf45897f4f90f7ae6a2a6e1c332847627e1`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 2, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": null, "proof_acks": [{"digest": "16d866cf0096216a6f35aa9d424b8cb0089ca7874860633667042efa1ef49856", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "registry": [{"latest_ack_ref": {"digest": "16d866cf0096216a6f35aa9d424b8cb0089ca7874860633667042efa1ef49856", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "marker_ref": null, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "RESOLVED_NOT_COMMITTED"}], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [{"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "version": 2}
```

### V-SN — DQ.LAB.SnapshotEvidence

Length: 1431 UTF-8 bytes. SHA-256: `0d4d2e462414289561210fe599e8dca4b317de03583e57d07b974819526d31ae`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 2, "control_root_ref": {"digest": "9a18109c3bf469c1b7e91afdf07c4cf45897f4f90f7ae6a2a6e1c332847627e1", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": null, "minimum_acknowledged_sequence": 0, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": null, "projection_root_ref": {"digest": "b39a29ebb164083b86d6daae49da663bd0e12666431f021b9b6467831c20e0bb", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-000000000027", "version": 2}
```

### V-HA — DQ.LAB.HoldEvidence

Length: 619 UTF-8 bytes. SHA-256: `141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "intent_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.HoldEvidence", "last_qualified_head_ref": null, "mutation_id": "00000000-0000-0000-0000-000000000008", "observed_snapshot_ref": null, "outcome": "UNKNOWN", "phase": "A", "reason": "COMMIT_ACK_LOST", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-HR — DQ.LAB.HoldEvidence

Length: 774 UTF-8 bytes. SHA-256: `d67045adb551d2ea0ce4dd3776124cf594f168b5c1ef38459fed614bb96c24c7`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "intent_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.HoldEvidence", "last_qualified_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_id": "00000000-0000-0000-0000-000000000008", "observed_snapshot_ref": null, "outcome": "UNKNOWN", "phase": "R", "reason": "ACK_UNRESOLVED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-HT — DQ.LAB.HoldEvidence

Length: 616 UTF-8 bytes. SHA-256: `6bcb3b6ac6e5c82afe8629605a50b127d27d64ce6d1d0c1d6ac027072936c3ea`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "intent_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.HoldEvidence", "last_qualified_head_ref": null, "mutation_id": "00000000-0000-0000-0000-000000000008", "observed_snapshot_ref": null, "outcome": "UNKNOWN", "phase": "A", "reason": "CUSTODY_LOST", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-HC — DQ.LAB.HoldEvidence

Length: 616 UTF-8 bytes. SHA-256: `6bcb3b6ac6e5c82afe8629605a50b127d27d64ce6d1d0c1d6ac027072936c3ea`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "intent_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.HoldEvidence", "last_qualified_head_ref": null, "mutation_id": "00000000-0000-0000-0000-000000000008", "observed_snapshot_ref": null, "outcome": "UNKNOWN", "phase": "A", "reason": "CUSTODY_LOST", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-HI — DQ.LAB.HoldEvidence

Length: 621 UTF-8 bytes. SHA-256: `d8c84832c23ca9646ac0dc96b4a9c94f281f59d123d207e5269796acfc0304b6`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "intent_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.HoldEvidence", "last_qualified_head_ref": null, "mutation_id": "00000000-0000-0000-0000-000000000008", "observed_snapshot_ref": null, "outcome": "UNKNOWN", "phase": "A", "reason": "IDENTITY_MISMATCH", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-HX — DQ.LAB.HoldEvidence

Length: 617 UTF-8 bytes. SHA-256: `883c9c0bb29932954055c4ffb44ab6046f3555e258b76b79b132b03e758c3e52`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "intent_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.HoldEvidence", "last_qualified_head_ref": null, "mutation_id": "00000000-0000-0000-0000-000000000008", "observed_snapshot_ref": null, "outcome": "UNKNOWN", "phase": "A", "reason": "STORE_CORRUPT", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-RECA — DQ.LAB.RecoveryEvidence

Length: 844 UTF-8 bytes. SHA-256: `7c4d506d35c8dfbf05d317c0ec9ab83633f056c683291dfe4a2f749f357bbe51`.

```json
{"absence_proof_ref": null, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": {"digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1", "kind": "DQ.LAB.CommitProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "kind": "DQ.LAB.RecoveryEvidence", "mutation_id": "00000000-0000-0000-0000-000000000008", "prior_hold_ref": {"digest": "141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b", "kind": "DQ.LAB.HoldEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "remaining_hold_ref": null, "resolution": "COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_sha256": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a", "version": 2}
```

### V-RECN — DQ.LAB.RecoveryEvidence

Length: 849 UTF-8 bytes. SHA-256: `f0cfc561d8ec22f55aa53d9c3e04975a0948890ba1c95baeefe132288e63f0e9`.

```json
{"absence_proof_ref": {"digest": "19d83bcf3e9f47ac97c36c52244685e339848b5b1663a3b1e208165472ff263c", "kind": "DQ.LAB.AbsenceProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": null, "kind": "DQ.LAB.RecoveryEvidence", "mutation_id": "00000000-0000-0000-0000-000000000008", "prior_hold_ref": {"digest": "141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b", "kind": "DQ.LAB.HoldEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "remaining_hold_ref": null, "resolution": "NOT_COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_sha256": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a", "version": 2}
```

### V-RECU — DQ.LAB.RecoveryEvidence

Length: 843 UTF-8 bytes. SHA-256: `5b0e1bccb252d7996bda9a2d841e5d437037af42870bff74de89745f4cbc57f0`.

```json
{"absence_proof_ref": null, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": null, "kind": "DQ.LAB.RecoveryEvidence", "mutation_id": "00000000-0000-0000-0000-000000000008", "prior_hold_ref": {"digest": "141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b", "kind": "DQ.LAB.HoldEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "remaining_hold_ref": {"digest": "141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b", "kind": "DQ.LAB.HoldEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "resolution": "UNKNOWN", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "ticket_sha256": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a", "version": 2}
```

### V-B_ROOT_OTHER — DQ.LAB.RootAnchor

Length: 676 UTF-8 bytes. SHA-256: `2c28ea8a4678af1c44eb1e108a5e147eb28978167c9a58103a77df6cd7580243`.

```json
{"database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "kind": "DQ.LAB.RootAnchor", "namespace_id": "00000000-0000-0000-0000-000000000004", "profile_ref": {"digest": "3b6eecf71e4c6a0780e7ea010f067f915bb7e2577025189522beffc97304603a", "kind": "DQ.LAB.QualificationProfile", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "root_identity": {"file_id": "DOC-OTHER-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "run_id": "00000000-0000-0000-0000-000000000002", "schema_version": 1, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "store_epoch": 1, "store_id": "00000000-0000-0000-0000-000000000003", "version": 2}
```

### V-B_STORE_OTHER — DQ.LAB.RootAnchor

Length: 670 UTF-8 bytes. SHA-256: `124dde3c024f357a89b42e7f4a1545700a4cf74d8a7bdcf4b986e0cf20d8ee7c`.

```json
{"database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "kind": "DQ.LAB.RootAnchor", "namespace_id": "00000000-0000-0000-0000-000000000004", "profile_ref": {"digest": "3b6eecf71e4c6a0780e7ea010f067f915bb7e2577025189522beffc97304603a", "kind": "DQ.LAB.QualificationProfile", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "run_id": "00000000-0000-0000-0000-000000000002", "schema_version": 1, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "store_epoch": 1, "store_id": "00000000-0000-0000-0000-000000000063", "version": 2}
```

### V-ACK_FOREIGN — DQ.LAB.ProofAck

Length: 885 UTF-8 bytes. SHA-256: `9f0c7718b725338e5b4ed0674a3010bb1d0182f121dc16f69c70abaff06716c1`.

```json
{"absence_proof_ref": null, "binding_ref": {"digest": "124dde3c024f357a89b42e7f4a1545700a4cf74d8a7bdcf4b986e0cf20d8ee7c", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": {"digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1", "kind": "DQ.LAB.CommitProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 3, "kind": "DQ.LAB.ProofAck", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "observed_application_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "outcome": "COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-ACK_GEN4 — DQ.LAB.ProofAck

Length: 885 UTF-8 bytes. SHA-256: `997670f6532ab868c6d7137044492458bddc02f91a5f46f12f6b3ad739652b60`.

```json
{"absence_proof_ref": null, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": {"digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1", "kind": "DQ.LAB.CommitProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 4, "kind": "DQ.LAB.ProofAck", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "observed_application_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "outcome": "COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-ACK_HEAD0 — DQ.LAB.ProofAck

Length: 729 UTF-8 bytes. SHA-256: `288bed5590f5e5a3f56c2074486eeb2d4edd49eba60133f34da48423c249725e`.

```json
{"absence_proof_ref": null, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "commit_proof_ref": {"digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1", "kind": "DQ.LAB.CommitProof", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 3, "kind": "DQ.LAB.ProofAck", "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "observed_application_head_ref": null, "outcome": "COMMITTED", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-C4_BAD — DQ.LAB.ControlRoot

Length: 2467 UTF-8 bytes. SHA-256: `44c76475acf200ab214fd032f321e1d2339819c642119f077283b9aa23e30c35`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 4, "kind": "DQ.LAB.ControlRoot", "pending_mutation_id": null, "proof_acks": [{"digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "registry": [{"latest_ack_ref": {"digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae", "kind": "DQ.LAB.ProofAck", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "phase": "RESOLVED_COMMITTED"}], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "staged_links": [{"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "40f9489a014d2919cfe41da8cfaf3698308791aa7c0f04f3444d9b2244c44a6a", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "cb46837a5629fa6bf19c83512fd62abf281878066920c9b09ab75fd21d6d14d1", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "dbf401b086b0313f76c5d49e3f329e3e8cd71194368fdb0b90969af87560e767", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "de96d764608ad0afe281c7c2ceb59a10ddb093efc8d7dee485502d668049f9c7", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}, {"mutation_id": "00000000-0000-0000-0000-000000000008", "object_ref": {"digest": "f3095b7b6b1e218dd5f29d8b4d9a6dde2d57a3a685a89f99fd3731a90b81aa68", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}], "version": 2}
```

### V-SR4_BAD — DQ.LAB.SnapshotEvidence

Length: 1743 UTF-8 bytes. SHA-256: `588ac7c56d3b0067e26ae63adbdab812cc2f1d4f8d908b1b351af6ed77554361`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 4, "control_root_ref": {"digest": "44c76475acf200ab214fd032f321e1d2339819c642119f077283b9aa23e30c35", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "minimum_acknowledged_sequence": 1, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": {"digest": "64c1ea4fcc3a61deef88e6cc53b06b1ac74bf17a28fa7e471f22c49a4ac916a1", "kind": "DQ.LAB.CommitMarker", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "projection_root_ref": {"digest": "8c53151c9e0879e66bfa4d14d6b3e977d9e46be992a8df179286e7b483ec1f3b", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-000000000028", "version": 2}
```

### V-PX_PARTIAL — DQ.LAB.ProjectionRoot

Length: 592 UTF-8 bytes. SHA-256: `927c2a4973b6104262a113daecdc5dc488202f8c941f58c96648c86a35a01d08`.

```json
{"active_slots": [], "admissions": [], "application_sequence": 0, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "committed_objects": [{"digest": "09c471f2a2096160a2c70a2ffe428963b64f516f5abfb8d74278c33ceb092925", "kind": "DQ.LAB.DataObject", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}], "events": [], "jobs": [], "kind": "DQ.LAB.ProjectionRoot", "member_links": [], "outbox": [], "read_reservations": [], "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}
```

### V-SX_PARTIAL — DQ.LAB.SnapshotEvidence

Length: 1431 UTF-8 bytes. SHA-256: `430274d6b4f3ab426e73a1d7c048b921bcf7cacc6f88d813755e2bb9937e6b98`.

```json
{"binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "control_generation": 1, "control_root_ref": {"digest": "6b1c2284ebc5e121b5a83e9b833b37d71fa427dd59256624a704bc8364a6ee90", "kind": "DQ.LAB.ControlRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "custody": {"coordinator_run_id": "00000000-0000-0000-0000-00000000000c", "database_identity": {"file_id": "DOC-DB", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}, "exclusive_controlled_root": true, "expected_store_epoch": 1, "minimum_acknowledged_marker_ref": null, "minimum_acknowledged_sequence": 0, "no_restore_or_replacement_observed": true, "root_identity": {"file_id": "DOC-ROOT", "provider": "POSIX_DEVICE_INODE", "volume_id": "DOC-VOLUME"}}, "integrity_checks": {"canonical_closure_valid": true, "complete_snapshot": true, "foreign_key_errors": 0, "marker_chain_valid": true, "profile_readback_matches": true, "projection_indices_valid": true, "sqlite_integrity": "ok"}, "kind": "DQ.LAB.SnapshotEvidence", "observed_head_ref": null, "projection_root_ref": {"digest": "927c2a4973b6104262a113daecdc5dc488202f8c941f58c96648c86a35a01d08", "kind": "DQ.LAB.ProjectionRoot", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_id": "00000000-0000-0000-0000-000000000029", "version": 2}
```

### V-AP_PARTIAL — DQ.LAB.AbsenceProof

Length: 1081 UTF-8 bytes. SHA-256: `3caea28ce9a103edbbad8a8dbb40c074f026673ba01ee7b5ce93113cd39f3f91`.

```json
{"any_apply_member_present": false, "any_apply_projection_change_present": false, "binding_ref": {"digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d", "kind": "DQ.LAB.RootAnchor", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "expected_previous_head_ref": null, "intent_source": "REGISTERED_DB", "kind": "DQ.LAB.AbsenceProof", "marker_present": false, "mutation_ref": {"digest": "eaa446579d9f504590fcb8950edc532f2bb9a154db1583d783fca4de19bcaae2", "kind": "DQ.LAB.MutationIntent", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "registry_present": true, "scope": "DQ_PROCESS_KILL_LAB_ONLY", "snapshot_ref": {"digest": "430274d6b4f3ab426e73a1d7c048b921bcf7cacc6f88d813755e2bb9937e6b98", "kind": "DQ.LAB.SnapshotEvidence", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}, "ticket_sha256": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a", "version": 2, "write_set_ref": {"digest": "73428af215343aa7a8eddff4ccbc46d53c98015c3ea700824c8c6731785e71ee", "kind": "DQ.LAB.WriteSet", "scope": "DQ_PROCESS_KILL_LAB_ONLY", "version": 2}}
```


## 10. Exact oracle cases

Cases ниже — nonhashable DOC.ORACLE metadata, не native proof/authorization и не executed test results. Поля inputs — полные typed refs к literal preimages выше. Весь facts object — явно заданные предпосылки document oracle, не результаты native измерений. complete_snapshot относится к текущей проверяемой phase, а не к существованию старого qualified A proof. candidate_snapshot в отрицательном case не квалифицирован: декларации Checks=true в его literal должны быть отвергнуты при провале hash/binding/generation tuple. NOT_ATTEMPTED фиксирует, что A ещё не вызывалась; это совместимо с доказуемым A absence и последующим negative closure без заявления о rollback P. namespace_barrier блокирует другие M; uncertainty_hold отдельно запрещает небезопасное продолжение той же M. allowed_next задаёт единственное разрешённое дальнейшее действие в условном scenario. Для unavailable evidence control_generation=null означает неизвестное значение, не 0.

### F01-P01 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "ACK_NEGATIVE_R_ONLY",
    "application_outcome": "NOT_COMMITTED",
    "control_generation": 0,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "A absence, registry absent, expected input from retained ticket",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-P01",
  "inputs": {
    "absence": {
      "digest": "2d7659daaa09a3cde2479a7d72001c3e336c2b1cdf2e134e235ab32abaf02bc9",
      "kind": "DQ.LAB.AbsenceProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "snapshot": {
      "digest": "ba912087eaab64cb2dd57fa2a6dd1e1bdc77e4522a3ebb8bb41d17099507b050",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-P02 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "APPLY_SAME_M_OR_CLOSE_NEGATIVE",
    "application_outcome": "NOT_ATTEMPTED",
    "control_generation": 1,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "Prepared/staged is not applied; AP establishes absence without declaring P rolled back",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-P02",
  "inputs": {
    "absence": {
      "digest": "19d83bcf3e9f47ac97c36c52244685e339848b5b1663a3b1e208165472ff263c",
      "kind": "DQ.LAB.AbsenceProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "prepare": {
      "digest": "53c7cf684335adfdfedbdae9183af8adbe4bc5b28a85e69e2304c3c4a7ba2ca2",
      "kind": "DQ.LAB.PrepareEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "snapshot": {
      "digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-N01 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "UNKNOWN",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "Missing retained ticket forbids NOT_COMMITTED",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": false,
    "expected_ack_retained": true,
    "ticket_retained": false
  },
  "finding": "DQ-F01",
  "id": "F01-N01",
  "inputs": {
    "candidate_snapshot": {
      "digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "hold": {
      "digest": "6bcb3b6ac6e5c82afe8629605a50b127d27d64ce6d1d0c1d6ac027072936c3ea",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-N02 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "BLOCKED_WHOLE_APPLICATION_RECOVERY",
    "application_outcome": "UNKNOWN",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "New coordinator cannot reconstruct continuity from DB alone",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": false,
    "custody_qualified": false,
    "expected_ack_retained": true,
    "ticket_retained": false
  },
  "finding": "DQ-F01",
  "id": "F01-N02",
  "inputs": {
    "candidate_snapshot": {
      "digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "hold": {
      "digest": "6bcb3b6ac6e5c82afe8629605a50b127d27d64ce6d1d0c1d6ac027072936c3ea",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-N03 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "UNKNOWN",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "Root identity mismatch",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": false,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-N03",
  "inputs": {
    "expected_binding": {
      "digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d",
      "kind": "DQ.LAB.RootAnchor",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "hold": {
      "digest": "d8c84832c23ca9646ac0dc96b4a9c94f281f59d123d207e5269796acfc0304b6",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "observed_binding": {
      "digest": "2c28ea8a4678af1c44eb1e108a5e147eb28978167c9a58103a77df6cd7580243",
      "kind": "DQ.LAB.RootAnchor",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-N04 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "UNKNOWN",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "Store identity mismatch",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": false,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-N04",
  "inputs": {
    "expected_binding": {
      "digest": "0aa021446c8bf6ad6a2ae8adec531f311eabc02f7d1db551f5e246d78b228d9d",
      "kind": "DQ.LAB.RootAnchor",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "hold": {
      "digest": "d8c84832c23ca9646ac0dc96b4a9c94f281f59d123d207e5269796acfc0304b6",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "observed_binding": {
      "digest": "124dde3c024f357a89b42e7f4a1545700a4cf74d8a7bdcf4b986e0cf20d8ee7c",
      "kind": "DQ.LAB.RootAnchor",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-N05 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "QUALIFIED_REOPEN_INSPECT_ONLY",
    "application_outcome": "UNKNOWN",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "Writer kill gives no commit proof by itself",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-N05",
  "inputs": {
    "hold": {
      "digest": "141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-N06 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "UNKNOWN",
    "control_generation": 1,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "A-member present despite missing marker; false boolean assertions do not prove absence",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-N06",
  "inputs": {
    "candidate_snapshot": {
      "digest": "430274d6b4f3ab426e73a1d7c048b921bcf7cacc6f88d813755e2bb9937e6b98",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "hold": {
      "digest": "883c9c0bb29932954055c4ffb44ab6046f3555e258b76b79b132b03e758c3e52",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "rejected_absence": {
      "digest": "3caea28ce9a103edbbad8a8dbb40c074f026673ba01ee7b5ce93113cd39f3f91",
      "kind": "DQ.LAB.AbsenceProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F01-P03 / DQ-F01

```json
{
  "expected": {
    "allowed_next": "OLD_M_READ_ONLY",
    "application_outcome": "NOT_COMMITTED",
    "control_generation": 1,
    "namespace_barrier": false,
    "resolution_R_outcome": "COMMITTED",
    "rule": "Negative R can close a never-prepared M from exact retained ticket without claiming P committed",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F01",
  "id": "F01-P03",
  "inputs": {
    "absence": {
      "digest": "2d7659daaa09a3cde2479a7d72001c3e336c2b1cdf2e134e235ab32abaf02bc9",
      "kind": "DQ.LAB.AbsenceProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ack_observed": {
      "digest": "379071bf39c8f7ea8115d2b9c97830ffd0e5ee409ab342d0cefacf647191a843",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "original_ticket": {
      "digest": "07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "post_snapshot": {
      "digest": "ef0663d0862997715fa43b83cfd7280e28013088f5d290cc82a207694d6ed4e1",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "4c5190b1c469b2c1ad69896a645bdd6af6196f1033f154256684cd00ae77b6a1",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P01 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "APPLY_SAME_M_ONLY",
    "application_outcome": "NOT_ATTEMPTED",
    "control_generation": 1,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "P committed, A not started",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P01",
  "inputs": {
    "prepare": {
      "digest": "53c7cf684335adfdfedbdae9183af8adbe4bc5b28a85e69e2304c3c4a7ba2ca2",
      "kind": "DQ.LAB.PrepareEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "snapshot": {
      "digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P02 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "EXACT_R_ONLY",
    "application_outcome": "COMMITTED",
    "control_generation": 2,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "A proven committed, R not started",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P02",
  "inputs": {
    "ack_expected": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "proof": {
      "digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1",
      "kind": "DQ.LAB.CommitProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "snapshot": {
      "digest": "2c59d8302a371d81d2ca858b319f46ef7095e4b22de7b6425cee5c81db31748e",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P03 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "QUALIFIED_INSPECT_A_ONLY",
    "application_outcome": "UNKNOWN",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_STARTED",
    "rule": "A ACK lost before qualified readback",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P03",
  "inputs": {
    "hold": {
      "digest": "141d189513ee080a10e061609baa5549ba349afd1051489217e82a6c1f4dd98b",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P04 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "QUALIFIED_INSPECT_R_ONLY",
    "application_outcome": "COMMITTED",
    "control_generation": null,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "R ACK lost; do not downgrade proven A or reapply it",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P04",
  "inputs": {
    "ack_expected": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "hold": {
      "digest": "d67045adb551d2ea0ce4dd3776124cf594f168b5c1ef38459fed614bb96c24c7",
      "kind": "DQ.LAB.HoldEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "proof": {
      "digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1",
      "kind": "DQ.LAB.CommitProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P05 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "NEXT_NEW_M_ALLOWED",
    "application_outcome": "COMMITTED",
    "control_generation": 3,
    "namespace_barrier": false,
    "resolution_R_outcome": "COMMITTED",
    "rule": "Qualified post-R readback matches original expected ACK",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P05",
  "inputs": {
    "ack_observed": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "post_snapshot": {
      "digest": "d93a8a4b4df65b05d0d56d3f57800e08be463cc4309106553bf0202357e8bb62",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "proof": {
      "digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1",
      "kind": "DQ.LAB.CommitProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P06 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "RETRY_EXACT_R_ACK3_ONLY",
    "application_outcome": "COMMITTED",
    "control_generation": 2,
    "namespace_barrier": true,
    "resolution_R_outcome": "NOT_COMMITTED",
    "rule": "R absent: same pre-R C2, pending M, no ACK3; never refresh Ack preimage",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P06",
  "inputs": {
    "ack_expected": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "fresh_snapshot": {
      "digest": "10aaf5ee0b08c5ae6638301ce933256f296593a2c0604d565116c52c9a108358",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "proof": {
      "digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1",
      "kind": "DQ.LAB.CommitProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-P07 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "OLD_M_READ_ONLY_NEW_M_BY_GRANT",
    "application_outcome": "NOT_COMMITTED",
    "control_generation": 2,
    "namespace_barrier": false,
    "resolution_R_outcome": "COMMITTED",
    "rule": "Qualified negative closure; not retry A under old M",
    "uncertainty_hold": false
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-P07",
  "inputs": {
    "absence": {
      "digest": "19d83bcf3e9f47ac97c36c52244685e339848b5b1663a3b1e208165472ff263c",
      "kind": "DQ.LAB.AbsenceProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ack_observed": {
      "digest": "16d866cf0096216a6f35aa9d424b8cb0089ca7874860633667042efa1ef49856",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "original_ticket": {
      "digest": "4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "post_snapshot": {
      "digest": "0d4d2e462414289561210fe599e8dca4b317de03583e57d07b974819526d31ae",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "1a9d07ade8de7cb512ccaa61ca7cb5700c786a82c7e6cf10eae74fd93539ce87",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N01 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 3,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Provided ACK digest is 0*64; actual bytes hash is ACK3",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "provided_ack_digest": "0000000000000000000000000000000000000000000000000000000000000000",
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N01",
  "inputs": {
    "ack_bytes": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "candidate_snapshot": {
      "digest": "d93a8a4b4df65b05d0d56d3f57800e08be463cc4309106553bf0202357e8bb62",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N02 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 3,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Foreign binding cannot satisfy expected ACK3",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N02",
  "inputs": {
    "ack_observed": {
      "digest": "9f0c7718b725338e5b4ed0674a3010bb1d0182f121dc16f69c70abaff06716c1",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "candidate_snapshot": {
      "digest": "d93a8a4b4df65b05d0d56d3f57800e08be463cc4309106553bf0202357e8bb62",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N03 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 3,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Ack target generation must be G+1=3, not 4",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N03",
  "inputs": {
    "ack_observed": {
      "digest": "997670f6532ab868c6d7137044492458bddc02f91a5f46f12f6b3ad739652b60",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "candidate_snapshot": {
      "digest": "d93a8a4b4df65b05d0d56d3f57800e08be463cc4309106553bf0202357e8bb62",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N04 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 4,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Post control generation 4 cannot satisfy exact target 3",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N04",
  "inputs": {
    "ack_observed": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "candidate_snapshot": {
      "digest": "588ac7c56d3b0067e26ae63adbdab812cc2f1d4f8d908b1b351af6ed77554361",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N05 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 3,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Ack stale application head conflicts with proven MK",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N05",
  "inputs": {
    "ack_observed": {
      "digest": "288bed5590f5e5a3f56c2074486eeb2d4edd49eba60133f34da48423c249725e",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "candidate_snapshot": {
      "digest": "d93a8a4b4df65b05d0d56d3f57800e08be463cc4309106553bf0202357e8bb62",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N06 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 1,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Old prepared snapshot is not proof that R is absent at G=2/head MK",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": false,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": true,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N06",
  "inputs": {
    "ack_expected": {
      "digest": "0ee404128e7f9edf3ae16c32efe6e4eb5cdc5c8650122e1b42eb54e00b255fae",
      "kind": "DQ.LAB.ProofAck",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "candidate_snapshot": {
      "digest": "a9042cf0cf662981e8268b28e3eab44ff8d413a2cb8928101bc10fedd6c9bae9",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "proof": {
      "digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1",
      "kind": "DQ.LAB.CommitProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```

### F02-N07 / DQ-F02

```json
{
  "expected": {
    "allowed_next": "READ_ONLY_BLOCKED",
    "application_outcome": "COMMITTED",
    "control_generation": 2,
    "namespace_barrier": true,
    "resolution_R_outcome": "UNKNOWN",
    "rule": "Lost expected exact Ack bytes/reference forbids reconstructing another R",
    "uncertainty_hold": true
  },
  "facts": {
    "complete_snapshot": true,
    "coordinator_continuous": true,
    "custody_qualified": true,
    "expected_ack_retained": false,
    "ticket_retained": true
  },
  "finding": "DQ-F02",
  "id": "F02-N07",
  "inputs": {
    "fresh_snapshot": {
      "digest": "10aaf5ee0b08c5ae6638301ce933256f296593a2c0604d565116c52c9a108358",
      "kind": "DQ.LAB.SnapshotEvidence",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "proof": {
      "digest": "3cfe3814f50ef2ffd353eb799aec5412ad16eb26b101d29165416d70d635c4c1",
      "kind": "DQ.LAB.CommitProof",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    },
    "ticket": {
      "digest": "45521f6f5b72f0a731b574c3bfe31b4616042d59e27eea3bb82efa3507d88861",
      "kind": "DQ.LAB.OperationTicket",
      "scope": "DQ_PROCESS_KILL_LAB_ONLY",
      "version": 2
    }
  }
}
```


Локальные build_vectors.py/check_vectors.py, canonical-vectors.json с UTF-8 hex, oracle-cases.json и результаты проверки находятся вне Git в review packet. Они вычисляют/проверяют document literals/refs/generations, не реализуют adapter/SQLite/NativeStore. **Computed locally, not independently validated.** Реальное исполнение каждого будущего oracle остаётся NOT_RUN.
