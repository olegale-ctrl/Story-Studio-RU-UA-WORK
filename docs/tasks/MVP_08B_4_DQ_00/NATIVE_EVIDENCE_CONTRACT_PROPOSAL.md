# DQ-01 — Native Evidence and Data Compatibility Proposal

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

## 1. Domain, encoding и границы authority

**PROPOSAL / NOT_APPROVED.** Новый domain: `DQ.LAB`, версия 1, scope `DQ_PROCESS_KILL_LAB_ONLY`. Это native **storage-lab** наблюдения после будущего разрешения, не production permissions, не execution rights и не замена PURE. Сам факт валидной схемы/хеша не квалифицирует SQLite/profile: для этого нужны реальные тесты и независимая приёмка.

Все hashable records закрыты: общие обязательные поля `kind: "DQ.LAB.<Name>"`, `version: 1`, `scope: "DQ_PROCESS_KILL_LAB_ONLY"` плюс ровно поля своей строки ниже. Unknown/missing fields/versions/scopes запрещены. Nullable означает required key со значением null либо указанным типом, а не optional key. Никаких hidden defaults/exclusions/self-digests.

C = UTF-8 строгого JSON с ASCII-key sort, ensure_ascii=False, separators=(', ', ': '), без trailing newline, Unicode normalization или BOM. Это локальная space-separated convention, не RFC JCS. Только JSON null/bool, integers 0..2^63−1 (bool не int), Unicode scalar strings, lists, closed objects; float/NaN/duplicate keys/surrogates запрещены. H = lowercase SHA-256 **всех C(record)** bytes, включая kind/version/scope. Raw payload SHA-256 и H(wrapper) — разные величины.

UUID — lowercase canonical 8-4-4-4-12 hex; Digest — ровно 64 lowercase hex; U — 0..9223372036854775807; Pos — 1..MAX; Text — 1..100000 Unicode scalars; Bool — ровно JSON true/false. `?T` = null or T. ListA..B = inclusive length. Ref<K> — закрытый объект `{kind:"DQ.LAB.K",version:1,scope:"DQ_PROCESS_KILL_LAB_ONLY",digest:Digest}`. Проверяется kind/version/scope/digest, bytes и **вся** closure; нет alias к PURE ref или raw hash. Циклы/неразрешимые refs и kind mismatch отклоняются.

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

Nonhashable transport **DQ.LAB.Error**, version=1/scope тот же, ровно поля: `code:ErrorCode`, `phase:INIT|OPEN|P|A|R|READ`, `mutation_id:?UUID`, `application_outcome:COMMITTED|NOT_COMMITTED|UNKNOWN|NOT_ATTEMPTED`, `namespace_hold:Bool`, `safe_message:MessageForCode`, `executor_effect:"NOT_AUTHORIZED"`.

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

Проверки по порядку: bounded closed encoding/version -> anchor/scope/profile -> availability/integrity/custody -> pending/resolution -> immutable M/key/replay -> slot/CAS/role/bounds -> SQL outcome proof. Во время P/A/R первичный unknown outcome не исчезает из-за ошибки диагностического чтения; последний квалифицированный binding/M/ticket сохраняется, error может отражать unavailable/corrupt, но application_outcome=UNKNOWN и namespace_hold=true. NOT_ATTEMPTED описывает новый не начатый A, а не отсутствие исхода прежней M. Никаких raw secrets/stack traces в safe_message.

Открытые для независимой проверки вопросы: [OWNER_DECISION_PACKAGE.md](OWNER_DECISION_PACKAGE.md), категория B. В текущем DOCS_ONLY этапе не создаются native proof records и не заявляется native PASS.
