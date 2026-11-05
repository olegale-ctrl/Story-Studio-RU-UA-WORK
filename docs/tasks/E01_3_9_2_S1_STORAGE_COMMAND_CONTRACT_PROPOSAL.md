# E01.3.9.2 / S1 — Storage & Command Protocol v1

**Статус: PROPOSAL — НЕ УТВЕРЖДЁН.** Дата: 2026-11-05.
Документ определяет предлагаемый wire/state contract, не реализацию и не
разрешение реализовать S2–S8. D1–D12 уже утверждены; новые schemas, limits,
golden vectors и параметры этого S1 требуют отдельного решения владельца.

## 1. Нормативная база и область

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base: `docs/editorial-e01-3-9-1b-approved-storage-architecture`,
  `0eb694f9a8f1c744799a3ae99c1f38c4707e0379`.
- Branch: `docs/editorial-e01-3-9-2-s1-storage-command-contract`.
- Приоритет: [E01.3.9.1b](E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md),
  E00 из `e520648411b99264688ff66dc61ad0e974201ed3`,
  [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md),
  [O1–O10/schema 2](E01_3_8_1_APPROVED_CONTRACT.md), затем этот S1.
- [E01.3.9.1a proposal](E01_3_9_1_ATOMIC_STORAGE_PROPOSAL.md) применяется в части,
  принятой E01.3.9.1b; его старые «awaiting decision» подписи не отменяют approval D1–D12.
- [Story Intelligence decision](../architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md):
  Discovery/Evaluation/Creative/Production Brief передают proposals и references,
  но не permissions, authenticated approvals или команды обхода blockers.
- GitHub policy прочитана **из отдельного** коммита
  `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`, путь
  `docs/GITHUB_REPOSITORY_STORAGE_POLICY.md`. Наличие/merge policy в этой ветке
  не предполагается. В Git помещается только этот документ и синтетические
  текстовые примеры внутри него, не реальные keys/anchors/journals/PII/media.

Primary — canonical editorial JSON. Storage metadata живёт отдельно в managed
ProgramData под service SID; snapshot schema 1/2 и их hashes/digests неизменны.
Без service доступны пользовательские drafts и безопасная диагностика, но не
protected commit. OS identity/policy/session validators остаются отдельными
необходимыми service dependencies, а не реализованными здесь механизмами.

## 2. Общие типы, закрытость и сериализация

Все перечисленные поля обязательны, включая nullable; неизвестные поля,
неизвестные enum/version, duplicate JSON keys и coercion запрещены. Формы ниже —
**декларативная запись schemas**, не исполняемый код. Ссылки на утверждённые
editorial wire types включают их точные closed schemas, без расширений.

| Тип | Точное правило |
|---|---|
| UUID | Canonical lowercase hyphenated UUID string по существующим моделям; формат не доказывает происхождение |
| Hex | 64 lowercase hex characters |
| U64 | Integer 0..18446744073709551615, не bool/float; overflow → SEQUENCE_EXHAUSTED, без wrap/new epoch по умолчанию |
| Generation | Integer ≥1 по existing codec; искусственный 64-bit cap не добавляется |
| UTC | Valid calendar `YYYY-MM-DDTHH:MM:SSZ`, descriptive time, не ordering proof |
| Text | Exact valid Unicode, без surrogates/NFC/trim/case change; ≤100,000 code points; пустота допустима только где явно указана |
| Label | Nonempty ASCII `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}` |
| Principal | Существующий canonical Windows SID / POSIX UID+machine tagged string; первый adapter — Windows |
| BlobRef | `{sha256:Hex, byte_length:integer 1..33554432}`; hash **полных bytes** blob, не filename/path/URL |
| JournalRef | `{record_index:U64, record_mac:Hex}` в machine/epoch контексте содержащего объекта |
| PolicyRef | `{policy_id:UUID, policy_version:nonempty Text ≤128, policy_sha256:Hex}`; authority policy, не editorial policy |
| DecisionKey | `{gate:SCRIPT|SCENES|HANDOFF, policy_version:nonempty Text, object_ref:existing RevisionRef wire, dependency_digest:Hex}` |

`C(x)` — строго UTF-8 без BOM от
`json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)`.
Integers должны обрабатываться без IEEE-754 потери точности; floats/NaN/Infinity
запрещены рекурсивно. JSON nesting ≤64. Byte length — UTF-8 bytes, не code points.
Object keys сортируются по Unicode code points; здесь все schema keys ASCII.
Массивы сохраняют заданный порядок, не сортируются автоматически.

Протокольные предлагаемые границы: editorial file/blob ≤32 MiB, frame payload
≤1 MiB, Request ≤1 MiB, FrozenCommand ≤2 MiB, любой metadata blob ≤32 MiB.
Frame ссылается на большие command/guard blobs по hash, не встраивает их.
Превышение отклоняется **до PREPARE**, без truncation; existing editorial codec
limits сохраняются дополнительно. Эти wire bounds не равны disk quotas §14.
Количество retained records не ограничивается silent eviction: при quota/IO
недостатке новая запись блокируется. Blob chain проверяется итеративно целиком;
cycle/unknown ref/missing proof не обходятся лимитом глубины или cached index.

## 3. Криптографические правила и отсутствие циклов

Производственный storage key K: ровно 32 случайных bytes, создаётся trusted
provisioning adapter, service-only ACL + DPAPI. Здесь K не приводится и не
создаётся. Key lookup по `key_id` только из protected key registry; неизвестный
key/потеря доступа блокируют, не запускают auto-regeneration. Key rotation,
compaction и передача MAC keys между ПК в v1 не определены и не допускаются.

Все domain strings — точные ASCII bytes с **одним конечным 0x00**, без LF:

| Значение | Формула |
|---|---|
| Request digest | SHA256(`story-studio-storage-request-v1\x00` + C(Request)) |
| Frozen command MAC | HMAC-SHA256(K, `story-studio-storage-command-v1\x00` + C(FrozenCommand)) |
| Frame MAC | HMAC-SHA256(K, `story-studio-storage-journal-v1\x00` + frame_header + C(JournalRecord)) |
| Anchor MAC | HMAC-SHA256(K, `story-studio-storage-anchor-v1\x00` + C(AnchorBody)) |
| Receipt MAC | HMAC-SHA256(K, `story-studio-storage-receipt-v1\x00` + C(ReceiptBody)) |
| Initialization authorization MAC | HMAC-SHA256(K, `story-studio-storage-initialize-v1\x00` + C(InitializationBody)) |
| Approval wire digest | SHA256(`story-studio-storage-approval-v1\x00` + C(full ApprovalRecord wire)) |
| Blob/file digest | SHA256(exact full bytes); no domain, value scoped by BlobRef/field type |

SHA/MAC представлены Hex; сравнение MAC constant-time. Не заменять storage MAC
Ed25519 fields или attestation digest из E01.3.8.4. Формат MAC не доказывает
identity: доверие зависит от protected key/service/OS/policy boundary.

Порядок зависимостей без self-reference:
Request → assigned IDs/time + canonical B/ContentHead → FrozenCommand/MAC →
ledger/barrier deltas + ReceiptCore → TransactionPlan/BlobRef → PREPARE MAC →
INTENT MAC → COMMIT MAC → CommittedHead → Anchor/Receipt MAC.
ReceiptCore и blobs **не содержат** ссылку на будущий собственный terminal MAC.
Unreferenced prepared blobs не имеют authority. Все их hashes проверяются
перед использованием; typed BlobRef не позволяет подменить один blob type другим.

## 4. Head, guard и proof blobs

### 4.1 ContentHead и CommittedHead

```text
ContentHead = {
  content_head_version:1, production_id:UUID, machine_binding_id:UUID,
  storage_epoch_id:UUID, editorial_schema_version:1|2, generation:Generation,
  snapshot_checksum:Hex, snapshot_file_sha256:Hex,
  snapshot_file_length:integer 1..33554432, tx_seq:U64
}
CommittedHead = {committed_head_version:1, content_head:ContentHead, commit_ref:JournalRef}
```

`snapshot_file_sha256` включает корневой snapshot_checksum; сам snapshot checksum
считается прежним API соответствующей schema. В pending B `tx_seq` reserved,
не committed. CommittedHead появляется только после valid GENESIS/COMMIT.
Payload этого record содержит ContentHead, не собственную commit reference.
Repair сохраняет исходный CommittedHead, включая original commit_ref.

### 4.2 HistoryGuard

```text
HistoryGuard = {
  guard_version:1, continuity:CONTINUOUS|BASELINE_UNVERIFIED|CONTINUITY_LOST,
  baseline_ref:BlobRef|null, ledger_tip:BlobRef|null,
  barrier_tip:BlobRef|null, lineage_tip:BlobRef|null
}
```

Guard — authenticated anchor/journal state, не поле schema 2 и не checkbox.
CONTINUOUS допускается для empty local genesis/доказанной complete lineage.
Imported pre-genesis history → BASELINE_UNVERIFIED; утрата ранее известной
непрерывности → CONTINUITY_LOST. Последнее блокирует новые effective decisions,
не снимается admin acknowledgement, epoch/key/UUID/date change. Если anchor
недоступен, diagnostics выводит uncertainty, а не пишет новый trusted guard.

Ниже каждый blob — C(object), hash/length через BlobRef. Все поля закрыты.
Массив entries — непустой, ≤10,000; oversized delta делится до admission либо
отклоняется, никогда не теряется. `previous_ref` указывает только на тот же type
и production; переход epoch сохраняет проверенные parent refs через lineage.

```text
InheritedApproval = {
  approval_id:UUID, decision_key:DecisionKey, decision:approve|reject|revise|revoke,
  approval_record_sha256:Hex, evidence_attestation_digest:Hex|null
}
BaselineBlob = {
  blob_version:1, blob_type:BASELINE, production_id:UUID, storage_epoch_id:UUID,
  source_schema_version:1|2, source_snapshot_ref:BlobRef,
  inherited_approvals:[InheritedApproval]
}
LedgerEntry = {
  request_id:UUID, review_session_id:UUID|null, request_sha256:Hex,
  command_mac:Hex, key_id:Label, tx_seq:U64|null,
  outcome:INITIALIZED|COMMITTED|ABORTED_PRECOMMIT|REPAIRED,
  receipt_core_sha256:Hex
}
LedgerBlob = {
  blob_version:1, blob_type:LEDGER_DELTA, production_id:UUID, storage_epoch_id:UUID,
  previous_ref:BlobRef|null, entries:[LedgerEntry]
}
DecisionSource =
  {source_kind:LOCAL_TX, storage_epoch_id:UUID, tx_seq:U64,
   approval_id:UUID, approval_record_sha256:Hex}
  or {source_kind:BASELINE, baseline_ref:BlobRef,
      approval_id:UUID, approval_record_sha256:Hex}
BarrierEntry = {
  decision_key:DecisionKey, barrier_kind:REJECT|REVISE|REVOKE|UNVERIFIED_HISTORY,
  source:DecisionSource
}
BarrierBlob = {
  blob_version:1, blob_type:BARRIER_DELTA, production_id:UUID, storage_epoch_id:UUID,
  previous_ref:BlobRef|null, entries:[BarrierEntry]
}
LineageEntry = {
  production_id:UUID, machine_binding_id:UUID|null, storage_epoch_id:UUID|null,
  source_snapshot_ref:BlobRef, parent_head:CommittedHead|null,
  parent_guard:HistoryGuard|null, parent_terminal_ref:JournalRef|null,
  order_status:UNVERIFIED|VERIFIED_LOCAL_PARENT
}
LineageBlob = {
  blob_version:1, blob_type:LINEAGE_DELTA, production_id:UUID, storage_epoch_id:UUID,
  previous_ref:BlobRef|null, entries:[LineageEntry]
}
```

Baseline imported_approvals может быть пустым и сохраняет source approval order,
но не назначает sequence. Empty new genesis имеет baseline_ref null. Подлинность
foreign parent_head/MAC не выводится из синтаксиса; foreign order_status всегда
UNVERIFIED без отдельно утверждённого transfer proof contract. LOCAL_TX source
проверяется по authenticated replay и exact record digest, не по editable claim.
Old barriers и ledger entries не удаляются при новой epoch/import. Отмена
REVOKE не выражается удалением barrier: новый допустимый APPROVE — отдельный
verified commit с fresh review; вся предыдущая история остаётся.

Ledger терминален; pending reservations выводятся из PREPARE/anchor и union
с complete journal extension. `receipt_core_sha256=SHA256(C(ReceiptCore))`, без
финального Receipt MAC. Commit delta blobs готовятся до intent, но действуют
только после соответствующего COMMIT/anchor binding. Abort delta строится при
доказанном pre-intent ABORT и сохраняет consumed request/session IDs.

## 5. Command и admission

### 5.1 Request envelope

```text
Request = {
  request_version:1, request_id:UUID, production_id:UUID,
  storage_epoch_id:UUID|null, expected_head:CommittedHead|null,
  review_session_id:UUID|null, operation:Operation, parameters:Parameters
}
```

| Operation | Закрытый Parameters | Предусловие/результат |
|---|---|---|
| INITIALIZE_EMPTY | `{draft_ref:BlobRef}` | Новый managed production; schema 2 generation 1, approvals/evidence пусты; explicit initialize permission |
| IMPORT_BASELINE | `{source_ref:BlobRef}` | Strict source schema 1/2 integrity; existing records буквальны, guard unverified |
| TRANSFER_BASELINE | `{source_ref:BlobRef, manifest_ref:BlobRef}` | Explicit destination initialization, foreign claims не становятся verified order |
| PUBLISH_REVISION | `{proposal_ref:BlobRef, reason:nonempty Text}` | Registered schema 2, existing approvals/evidence неизменны; revisions immutable, append-only; service добавляет revision/selection event |
| RECORD_DECISION | `{decision_key:DecisionKey, decision:approve|reject|revise|revoke, reason:nonempty Text, reconsiders_record_id:UUID|null}` | Schema 2, READY session + authority/current/history checks; ровно одна новая approval/evidence pair и approval_recorded event |
| MIGRATE_SCHEMA | `{}` | Registered verified schema 1; existing pure migration, generation +1 ровно один раз |
| RESTORE_EXACT_HEAD | `{image_ref:BlobRef, expected_observation:FileObservation}` | Explicit recovery permission, valid existing anchor/chain; target **current** exact head, не старый backup |

Для первых трёх operations request epoch/expected_head/session null; epoch
выделяет broker один раз, genesis tx_seq=0, generation исходного baseline
сохраняется (кроме INITIALIZE_EMPTY, где 1). Обычные requests несут matching epoch
и exact expected_head. Session non-null только RECORD_DECISION. Client не
передаёт principal/actor/trust flags/assigned approval IDs; unknown fields rejected.
Operation — ровно семь строк таблицы, Parameters выбирается только этим tag.
Snapshot refs в этих requests указывают на **canonical** bytes. Если исходный
portable JSON имеет иное whitespace/escaping, read-only preflight может явно
декодировать/проверить и предложить canonical export с новым full-file digest,
сохраняя значения/Unicode/порядок. Request фиксирует именно принятый canonical
artifact; неcanonical bytes при admission отклоняются WIRE_FORMAT, не скрыто
переименовываются в другой hash. Исходная копия не считается trusted head.
Уже ACTIVE/CONTINUITY_LOST production нельзя bootstrap заново в другом каталоге
или поверх прежней регистрации: v1 не содержит команды reset/merge active epochs.
Новая попытка после INITIALIZATION_ABORTED требует отдельной authorization,
сохранения старого ledger и новой epoch; прежняя terminal reservation не стирается.

FileObservation — `{state:MISSING}` или
`{state:PRESENT, file_ref:BlobRef}`. Это fingerprint bytes, не integrity proof.
Broker сам повторяет observation по native handles. Для regular publication
она равна existing A; для exact-head repair — quarantine/C или MISSING.
Oversized/неподдерживаемые files требуют отдельной диагностики, не blind overwrite.

TransferManifest закрыт:
`{transfer_manifest_version:1, production_id:UUID, source_ref:BlobRef,
source_machine_id:UUID|null, source_epoch_id:UUID|null,
source_head:CommittedHead|null, source_guard:HistoryGuard|null}`.
Ссылки bounded/checked, но не source authenticity; local keys не экспортируются.

### 5.2 Frozen command и review snapshot

```text
Authorization = {
  policy_ref:PolicyRef, permission:INITIALIZE|RECOVERY|DRAFT_WRITE|REVIEW_DECISION,
  authenticated_connection_id:UUID
}
ReviewSnapshot = {
  session_id:UUID, principal_id:Principal, policy_ref:PolicyRef,
  decision_key:DecisionKey, confirmed_codes:[existing declaration code],
  review_declarations:[nonempty Text], reconsiders_record_id:UUID|null,
  server_incarnation_id:UUID, state:READY
}
AssignedIds = {approval_id:UUID|null, event_id:UUID|null}
FrozenCommand = {
  command_version:1, request:Request, request_sha256:Hex, key_id:Label,
  principal_id:Principal, actor:nonempty Text, at:UTC,
  authorization:Authorization, assigned_ids:AssignedIds,
  storage_epoch_id:UUID, expected_result:ContentHead,
  review_snapshot:ReviewSnapshot|null
}
```

Principal берётся из Windows TokenUser/проверенного local connection, policy —
из protected provider. Authorization/READY как присланные клиентом JSON не
принимаются. Grant проверяет service dependency; MAC фиксирует принятый контекст,
но его формат не реализует authentication. Отсутствие provider → fail closed.
PolicyRef независим от editorial decision_key.policy_version (A12).

RECORD_DECISION требует exact session/principal/policy/key/reconsideration
binding, закрытый **порядок** declaration codes по schema-2 §6.2 и отдельный
REVOKE permission. Approval actor/timestamp/review declarations и evidence
principal/policy/session/request/declarations формирует service из frozen context;
input score/Creative output не считается review confirmation.

Assigned approval/event IDs non-null только там, где создаются новые records:
decision — оба; revision/migration — только event; genesis/repair — оба null.
Все metadata/IDs/at фиксируются до PREPARE и не пересоздаются при retry/replay.
MIGRATE_SCHEMA не получает второе generation increment от writer. Если source
уже schema 2, после existing-request lookup возвращается non-admitted
ALREADY_MIGRATED observation: нет PREPARE, reservation, receipt или storage write.
Это не durable transaction receipt и не integrity/authority result.

PUBLISH_REVISION proposal не может менять старые revision payloads, approvals,
evidence или events. Предложение содержит прежние events; service сам добавляет
ровно один supported event, выбирает explicit new/active refs и generation A+1.
Пустая по смыслу операция отклоняется COMMAND_NO_CHANGE до admission. Registered
schema 1 в v1 доступна для read/migration, не для новых decision writes.

## 6. Plan, anchor и receipts

### 6.1 TransactionPlan

```text
ApprovalBinding = {
  approval_id:UUID, decision_key:DecisionKey, decision:approve|reject|revise|revoke,
  approval_record_sha256:Hex, evidence_attestation_digest:Hex
}
TransactionPlan = {
  plan_version:1, kind:GENESIS|PUBLISH|REPAIR_EXACT,
  request_id:UUID, review_session_id:UUID|null, tx_seq:U64|null,
  key_id:Label, command_ref:BlobRef, command_mac:Hex,
  base_head:CommittedHead|null, observed_primary:FileObservation,
  new_content_head:ContentHead, image_ref:BlobRef,
  guard_before:HistoryGuard, guard_commit:HistoryGuard,
  expected_commit_receipt:ReceiptCore, new_approvals:[ApprovalBinding],
  initialization_ref:BlobRef|null, storage_profile_id:Label
}
```

Command_ref — C(FrozenCommand); plan_ref — C(TransactionPlan). Их refs и все
images/guard blobs проверяются на exact length/hash/type. Для PUBLISH base_head
non-null, tx_seq=high_watermark+1 и generation A+1; для GENESIS base_head null,
tx_seq=0, initialization_ref non-null; для REPAIR_EXACT tx_seq null,
new_content_head=base_head.content_head без изменения generation/sequence.
Image_ref совпадает с full-file hash/length new_content_head.

New_approvals: ровно одна binding только для RECORD_DECISION, иначе пусто.
Imported history не записывается как introduced approvals. Binding digest
проверяется по полному schema-2 wire record и matching evidence; attestation
проверяет existing API. Guard_commit обновляет ledger и необходимые barriers,
сохраняет все прежние roots/entries, не повышает continuity по пользовательскому
acknowledgement. Exact repair меняет только metadata ledger, не историю decisions.

Для каждого terminal результата ledger_tip обязан указывать на **один новый**
LedgerBlob с previous_ref=guard_before.ledger_tip и ровно одной entry принятого
request с правильным status/command MAC/receipt digest. Это правило относится
также к ABORT/repair. В обычных PUBLISH/ABORT/repair baseline_ref, lineage_tip и
continuity неизменны. Barrier_tip либо прежний, либо новая delta с previous_ref
прежнего tip и exact отрицательным ApprovalBinding; APPROVE не удаляет старую
barrier. Genesis/import фиксирует baseline и UNVERIFIED_HISTORY entries всех
inherited approval keys до admission; empty genesis без inherited history
сохраняет null baseline/barrier. Retained parent ledger/barriers не заменяются
пустыми refs. Нарушение link/entry equality — JOURNAL_TRANSITION_INVALID,
даже при correct MAC: service key не оправдывает ошибочный state transition.

### 6.2 Anchor wire

```text
Pending = {
  pending_version:1, phase:PREPARED|PUBLISH_INTENT,
  plan_ref:BlobRef, prepare_ref:JournalRef, intent_ref:JournalRef|null
}
AnchorBody = {
  anchor_version:1, production_id:UUID, machine_binding_id:UUID,
  storage_epoch_id:UUID, activation:INITIALIZING|ACTIVE|INITIALIZATION_ABORTED,
  stable_head:CommittedHead|null, reserved_tx_high_watermark:U64,
  journal_tail:JournalRef, pending:Pending|null,
  history_guard:HistoryGuard, key_id:Label
}
AnchorState = {body:AnchorBody, mac:Hex}
```

INITIALIZING допускает stable_head null только с pending GENESIS. ACTIVE требует
stable_head non-null. PREPARED → intent_ref null; PUBLISH_INTENT → matching
non-null intent_ref. Stable head commit_ref и journal_tail — разные pointers:
после ABORT/repair tail продвигается без смены original snapshot commit_ref.
High watermark никогда не уменьшается; tx_seq 0 только genesis, ordinary
reservations не переиспользуются после ABORT. Guard_before активен до terminal
record, pending reservations дополнительно учитываются из PREPARE. После
COMMIT/ABORT активируется terminal guard. Anchor — один replaceable authenticated
file; snapshots/keys/registry/journal не объявляются атомарной файловой группой.
INITIALIZATION_ABORTED: stable_head/pending null, tail — valid ABORT genesis,
guard содержит consumed IDs; обычные writes/authority недоступны. Повтор request
возвращает прежний abort. Новый genesis требует explicit authorization/new epoch
с сохранением прежних reservations, не повторного использования tx_seq 0 в этой epoch.

### 6.3 Receipt

```text
ReceiptCore = {
  receipt_core_version:1, request_id:UUID, request_sha256:Hex,
  storage_epoch_id:UUID, operation:Operation, tx_seq:U64|null,
  status:INITIALIZED|COMMITTED|ABORTED_PRECOMMIT|REPAIRED,
  result_content_head:ContentHead|null,
  approval_ids:[UUID], event_ids:[UUID], abort_code:AbortCode|null
}
ReceiptBody = {
  receipt_version:1, core:ReceiptCore, terminal_ref:JournalRef,
  result_head:CommittedHead|null, key_id:Label
}
Receipt = {body:ReceiptBody, mac:Hex}
```

Terminal payload включает только ReceiptCore. Final Receipt вычисляется после
terminal MAC и stable anchor, не хранится циклически в COMMIT/ledger. Retry
восстанавливает те же canonical receipt bytes из frozen values и key_id, не
добавляя текущее время. ABORT core возвращает прежний content head (null при
неактивированном genesis), IDs новых approvals/events пусты; approval/event IDs
из aborted plan остаются reserved, но не объявляются созданными.

Protocol response — закрытый union:
`{response_version:1, type:RECEIPT, receipt:Receipt}`;
`{response_version:1, type:PENDING, request_id:UUID, prepare_ref:JournalRef,
state:PREPARED|INTENT|COMMITTED_PENDING_FINALIZATION|ABORTED_PENDING_FINALIZATION,
manual_recovery_required:bool}`;
`{response_version:1, type:OBSERVATION, code:ALREADY_MIGRATED,
observed_head:CommittedHead}`; либо `{response_version:1, type:ERROR, error:ProtocolError}`.
Ни один ответ не содержит authorized/approved/ready/trusted_origin flag.

## 7. Журнал, framing и bootstrap authorization

### 7.1 Frame и record

Frame bytes: ASCII `SSJ1` (4 bytes) + payload length N (unsigned 32-bit big-endian,
4 bytes) + C(JournalRecord) (ровно N bytes) + raw 32-byte frame MAC. N=1..1048576;
header — первые 8 bytes. Payload length входит в MAC. Никаких BOM/newline/JSON
array wrappers, outer MAC hex text или padding между frames. Unknown magic,
invalid length, noncanonical payload и extra trailing bytes не пропускаются.
Reader сначала bounded header/strict JSON/schema/C(payload)==bytes, затем key
lookup и MAC; только после успешного MAC разрешено доверенное dereference plan/
guard/images. Неверный MAC не обходится поиском другого key или следующего magic.

```text
JournalRecord = {
  journal_record_version:1, production_id:UUID, machine_binding_id:UUID,
  storage_epoch_id:UUID, record_index:U64, previous_record_mac:Hex|null,
  key_id:Label, record_type:RecordType, payload:RecordPayload
}
```

Первый record epoch — PREPARE kind GENESIS, index 0, previous_record_mac null.
Следующие index = previous+1, MAC связывает exact предыдущий frame. Все IDs/key
и данные загруженного plan соответствуют record context. Сегментация — только
physical container: имя/mtime сегмента не определяют порядок, пропуск запрещён.

| RecordType | Закрытый RecordPayload |
|---|---|
| PREPARE | `{plan_ref:BlobRef}` |
| PUBLISH_INTENT | `{prepare_ref:JournalRef, plan_ref:BlobRef}` |
| SNAPSHOT_COMMIT | `{prepare_ref:JournalRef, intent_ref:JournalRef, plan_ref:BlobRef, receipt_core:ReceiptCore}` |
| GENESIS | Та же closed форма, что SNAPSHOT_COMMIT; только kind GENESIS/tx_seq 0 |
| REPAIR_COMMIT | Та же closed форма; только kind REPAIR_EXACT/tx_seq null |
| ABORT | `{prepare_ref:JournalRef, plan_ref:BlobRef, abort_code:AbortCode, receipt_core:ReceiptCore, result_guard:HistoryGuard}` |

AbortCode — CANCELLED_BEFORE_INTENT, SESSION_INVALIDATED, REVALIDATION_FAILED,
RECOVERY_PREINTENT_ABORT. ABORT после полного valid intent запрещён. Его
ReceiptCore status ABORTED_PRECOMMIT, abort_code совпадает с payload; result_guard
добавляет terminal ledger entry, сохраняет known barriers/continuity и consumed
IDs. Commit receipt_core обязан буквально совпадать с plan.expected_commit_receipt.
Commit guard берётся из того же plan. Complete duplicate terminal запрещён;
replay существующего terminal не append второго. Никаких generic/freeform
journal events, administrative overrides или неизвестных payload fields в v1.

### 7.2 Initialization authorization/registration

```text
InitializationBody = {
  initialization_version:1, request_id:UUID, request_sha256:Hex,
  production_id:UUID, machine_binding_id:UUID, storage_epoch_id:UUID,
  managed_root_token:UUID, source_ref:BlobRef, principal_id:Principal,
  actor:nonempty Text, at:UTC, policy_ref:PolicyRef,
  guard_before:HistoryGuard, key_id:Label
}
InitializationAuthorization = {body:InitializationBody, mac:Hex}
RegistrationBody = {
  registration_version:1, storage_protocol_version:1,
  production_id:UUID, machine_binding_id:UUID, storage_epoch_id:UUID,
  managed_root_token:UUID, initialization_ref:BlobRef,
  storage_profile_id:Label, key_id:Label
}
Registration = {body:RegistrationBody, mac:Hex}
```

Registration MAC: HMAC-SHA256(K,
`story-studio-storage-registration-v1\x00` + C(RegistrationBody)).
Registration — immutable descriptor, не второй mutable head. Managed root token
разрешается только trusted native adapter; client path не принимается. Mutable
registry lifecycle/cache не подтверждает authority и не создаёт третий CP.
Initialization_ref указывает на canonical authorization wrapper; её MAC не
содержит будущий plan/COMMIT/anchor MAC и потому не образует cycle.

Первые registration/authorization создаются лишь по явному initialize permission,
не при missing anchor у известной production. Для genesis guard/source hash,
request, IDs, epoch и policy должны совпадать между authorization, plan и
FrozenCommand. Историческая authorization не даёт право автоматически
пересоздать исчезнувший anchor. Current caller permission проверяется отдельно
для explicit operator continuation. При неизвестной initial persistence — block,
не повтор genesis по одному найденному JSON. ACTIVE storage никогда не проходит
first-time bootstrap повторно из-за reinstall/удалённого файла.

## 8. Нормативные переходы W0–W9

Под lock допускается одна nonterminal transaction. До admission: authenticate
connection → проверить доступ principal к request lookup → проверить existing
request/consumed session across retained epochs → только для нового request
сверить exact head/CAS и live policy/session/current package. Source strict
codec/round-trip и full integrity обязательны. Actual proofs, а не числовое
совпадение generation, определяют stable head.

| Шаг | Обязательная операция и persistence barrier | Разрешённое состояние |
|---|---|---|
| W0 | Validate source/command/current policy/session/history; выделить S/IDs/at, построить exact B и FrozenCommand; проверить output integrity/round-trip и все proposed limits; подготовить plan/guard/receipt blobs | Stable A; source не изменён. S пока не durable reservation |
| W1 | Archive exact A/B/metadata blobs write-new/flush/reread; sibling temp B на volume primary; проверить ACL/path identity, hash/length | Stable A + unreferenced prepared artifacts |
| W2 | Проверенный A → backup temp/flush/atomic backup replace; append/flush complete PREPARE | S/request/session/assigned IDs reserved при complete authenticated PREPARE, даже если response/anchor update потерян |
| W3 | Replace/flush anchor: stable A, unchanged guard_before, pending PREPARED, high watermark S, tail PREPARE; reread/MAC | PREPARED; authority/new writes blocked |
| W4 | Append/flush PUBLISH_INTENT **сначала**; затем replace/flush anchor pending PUBLISH_INTENT, tail INTENT; reread | Полный valid intent — irreversible barrier. Обычный writer не идёт к W5 до обеих подтверждённых записей |
| W5 — CP | Under native handles/CAS atomically replace primary exact B, не in-place write | Snapshot committed в момент namespace publication B; ещё не ACK |
| W6 | Reread primary exact B; hash/length/checksum/full integrity; flush published file handle | PUBLISHED / finalization pending |
| W7 | Append/flush ровно один terminal SNAPSHOT_COMMIT/GENESIS/REPAIR_COMMIT с frozen receipt | Data committed, terminal MAC известен; anchor может отставать |
| W8 | Replace/flush/reread anchor: terminal guard, pending null, tail terminal. PUBLISH/GENESIS → CommittedHead B с terminal ref; repair → прежний CommittedHead. Cross-check entire state | Finalized stable state |
| W9 | Release lock, вернуть canonical Receipt; cleanup orphan temps не влияет на CP | Повтор — тот же receipt, без нового event/generation |

File flush не доказывает atomic multi-file commit. Native Windows adapter имеет
те же proof/ACL/handle requirements E01.3.9.1a; no cross-volume copy, reboot
move, silent sharing-violation workaround или presumed POSIX directory fsync.
Flush/replacement error после возможного intent/CP → OUTCOME_UNKNOWN/PENDING,
не «точно не committed». Under lock reread и §9, не blind new request.

### 8.1 ABORT

Только complete verified prefix без полного intent **и без uncertain tail**,
primary exact A, valid existing anchor/protection. Создать abort ReceiptCore,
ledger delta/result_guard, append/flush ABORT, затем replace/flush anchor pending
null, same stable A и preserved high watermark. До terminal anchor finalization
ответ pending; после — durable abort receipt. Data CP не происходит, generation
не меняется. Reserved IDs не освобождаются. При replay complete ABORT заканчивается
тот же metadata transition; новый request не скрывает старый abort/intent.

### 8.2 Genesis

GENESIS — авторизованный первый baseline, не automatic recovery. W0 проверяет
initialize authorization и отсутствие active registered lineage для этого пути;
allocated epoch новая, tx_seq 0. Источник draft/import целиком проверен, generation
сохраняется по §5.1. Before head null, observed primary MISSING. W1/W2 сохраняют
source/guard/plan/PREPARE без backup несуществующего A. W3 создаёт первый anchor
INITIALIZING; W4 intent; W5 публикует primary; W7 terminal GENESIS; W8 ACTIVE
CommittedHead seq 0. Imported records не получают локальных approval tx_seq.

Pre-intent ABORT genesis даёт INITIALIZATION_ABORTED и consumed IDs. Успешный
повтор возвращает INITIALIZED receipt прежней epoch, не создаёт baseline снова.
Missing/invalid anchor после restart не автосоздаётся из registration/PREPARE.
Explicit operator recovery требует сохранённых initialize/protection proofs;
если нельзя доказать допустимое продолжение, оно заблокировано. Новая epoch
не стирает failed request reservations и не снимает continuity guard.

### 8.3 Exact-head repair

Это отдельная recovery-authorized operation, не content rollback. Valid current
anchor/chain указывают на repair target H, current file может быть C/missing.
Сначала сохранить forensic C; request.expected_observation сравнивается с реальным
fingerprint. Plan kind REPAIR_EXACT, base/result H, tx_seq null, new approvals/IDs
пусты, history continuity/barriers прежние. W2 резервирует request/session IDs,
но **не** увеличивает tx high watermark. W3/W4 такие же metadata barriers;
W5 заменяет C exact H bytes под observation CAS; W7 REPAIR_COMMIT; W8 сохраняет
original H.commit_ref, обновляет только terminal ledger/anchor tail.

Это physical repair CP, не новый snapshot generation/approval order. При
pre-intent ABORT C остаётся untrusted; ReceiptCore result H — желаемый recorded
head, не утверждение, что C исправлен. Anchor может быть stable при mismatch
primary, поэтому normal writes/authority остаются blocked. Automatic replay
после accepted repair intent разрешает только recorded observation либо exact
H, не произвольно изменившийся C. Без valid anchor/chain этот endpoint недоступен.

## 9. Reconciliation и partial records

Проверка: native protection/key → **existing** anchor MAC/registration binding →
full prefix до anchor tail и stable commit_ref → contiguous authenticated
extension → loaded plans/guard/blob proofs → exact primary observation. Проверять
index/previous MAC/epoch/transition, не только valid HMAC. Порядок берётся из
проверенной chain, никогда из имени сегмента, UUID, timestamp или max generation.

| Observed state | Единственное допустимое решение |
|---|---|
| Stable matching head/tail, pending null, full proofs и primary exact | Stable storage result; authority отдельно |
| Anchor lag matching prefix, extension PREPARE без intent/uncertain suffix, primary A | Durable ABORT и consumed IDs; anchor advance, не discard PREPARE |
| ABORT complete, anchor ещё pending | Довести terminal guard/tail, без повторной reservation |
| Complete INTENT, anchor stable A/PREPARED/INTENT, B image valid, primary A/B | Довести pending anchor и exact B forward/finalization; после intent нельзя ABORT |
| Complete terminal после matching PREPARE/INTENT, anchor отстаёт | Проверить B и finalize existing transaction/receipt. Отсутствующие frames или COMMIT без intent — block |
| Anchor ahead of full valid journal / different MAC at referenced index | ANCHOR_MISMATCH / JOURNAL_PREFIX_MISMATCH; не уменьшать anchor |
| Missing anchor | ANCHOR_MISSING; нет automatic replay/new genesis |
| Invalid/unreadable key/ACL/anchor/journal, unknown/partial payload | ANCHOR_UNAVAILABLE с precise reason; read-only/authorized manual recovery |
| Stable B, primary старый A/backup/unknown C, pending отсутствует | ANCHOR_MISMATCH; только explicit exact-head repair, не normal replay |
| Pending publication, missing/unknown primary | Block; forensic/manual recovery, не overwrite чужих данных |

Для GENESIS A=MISSING допустим только в authorizеd initialization state; для
repair A — exact recorded FileObservation. При полном intent и потерянном ACK
нельзя решать, что операция отменена, даже если primary снова A. Valid old anchor
допускает только verified same-chain extension, не произвольный новый journal.

### 9.1 Optional terminal COMMIT reconstruction — OFF

**Базовая capability отключена.** Любой partial terminal, PREPARE/INTENT, bad-MAC
frame, gap, reference beyond readable prefix → blocked/manual recovery. Никакого
общего «truncate after last good frame». Владелец должен отдельно принять exact
capability implementation и exhaustive fault tests; client flag, reinstall или
сам факт утверждения D4/S1 её не включает.

Предлагаемая отдельно gated capability `TERMINAL_COMMIT_RECONSTRUCTION_V1` может
в будущем разрешить только один **unreferenced terminal suffix** после complete
anchored intent. Условия все одновременно: existing valid anchor/chain; frozen
plan/receipt/metadata; проверенный допустимый A/B и B image; exact known next
index/previous MAC; весь имеющийся fragment — буквальный prefix единственного
восстановимого полного frame, длина строго меньше ожидаемой. Record type только
SNAPSHOT_COMMIT при plan.kind PUBLISH. Partial GENESIS, REPAIR_COMMIT,
PREPARE, INTENT или ABORT не покрываются этой capability и остаются blocked;
расширение потребовало бы отдельного owner decision.
Не должно существовать другого complete terminal или последующих bytes.

После quarantine raw fragment под lock сначала довести exact publication B,
затем восстановить только этот suffix, flush, проверить весь prefix, закончить
W8. Отсутствие хоть одного proof → block. Whole bad-MAC frame не чинится, referenced
bytes не перезаписываются. Ни один ID/time/generation не создаётся повторно.
Специальная приёмка должна покрывать все prefix lengths, bit flips, extra bytes,
missing blobs, wrong index/MAC, repeated recovery crashes и ключевые отрицательные
сценарии. До неё этот переход отсутствует в executable state machine.

## 10. Idempotency, sessions, verified approval order

Durable admission начинается complete authenticated PREPARE; до него запрос
может быть NOT_ADMITTED и live session после restart недействительна. После него
request/session/assigned IDs consumed независимо от ABORT. Lookup объединяет
terminal ledger, pending и full valid journal extension, включая preserved
parent epochs. Сравнение request digest плюс canonical Request защищает от
случайной reuse; cryptographic collision/mismatching bytes → block, не успех.

| Повтор/сбой | Ответ |
|---|---|
| Тот же request/principal/session/content, terminal finalized | Прежний canonical Receipt, lookup до current head CAS |
| Тот же ID, иные bytes/principal/session/epoch | IDEMPOTENCY_CONFLICT либо denied, без утечки чужого receipt |
| PREPARE до intent | Pending или прежний ABORT; не новая approval |
| Intent/CP без ACK | Exact same transaction reconciliation; затем прежний receipt |
| Old consumed request в новой epoch | Historical receipt/epoch mismatch; не новый write |
| Unbound session после restart | SESSION_INVALIDATED; новый review/new IDs, не client восстановление confirmations |

Frozen READY snapshot bound request переживает restart только как proof ранее
принятой операции, не как активная session для другого key/request. Unbound
timeouts могут использовать monotonic process clock; wall-clock expiry не
задаёт transaction order. Изменившаяся policy не отменяет accepted intent
задним числом, но влияет на последующее current authority evaluation.

Verified order map строится по committed PUBLISH plans/ApprovalBinding:
`approval_id → (epoch, tx_seq, decision_key, decision, record/evidence digests)`.
Проверяются full current record equality, graph/current package, matching
attestation, append-only history и complete local lineage. GENESIS/repair/ABORT
не присваивают historical approval order. В одном RECORD_DECISION ровно одна
новая approval: array position не заменяет sequence; batch decisions v1 запрещены.

Latest applicable для exact key внутри epoch — maximum **verified committed
tx_seq**. Сырые tx_seq разных epoch не сравниваются численно. Если retained
VERIFIED_LOCAL_PARENT proofs действительно образуют единственную проверенную цепь,
order задаётся `(позиция epoch в этой цепи, tx_seq)`; позиция определяется только
parent commit/terminal proofs, не UUID/датой/порядком LineageEntry в массиве.
Parent должен быть final stable boundary, его ledger/barriers сохранены целиком.
Multiple local predecessors/fork, отсутствующий link или foreign UNVERIFIED
parent не дают total order и блокируют dependent target. V1 не создаёт active
epoch merge/reset, даже если грамматика позволяет хранить inherited references.
После REJECT/REVISE/REVOKE новый APPROVE требует exact latest
negative target, fresh review/session/request, всех declarations и policy/current
checks. Старый APPROVE не возрождается от selection/backup/retry. Все negative
records/proofs сохраняются. Existing same-time ambiguity semantics A6 не
переписываются; если её допустимое разрешение не установлено approved authority
contract, authority остаётся blocked. Если target зависит от pre-genesis или
утраченного order, остаётся UNVERIFIED_ORDERING/CONTINUITY_LOST.

## 11. Import, transfer, backup и утрата истории

- **Import:** full existing integrity до принятия baseline. Все source records,
  evidence/signatures, UUID/Unicode/order буквально сохраняются; old evidence
  не становится authenticated из-за нового journal. BASELINE_UNVERIFIED и
  inherited key barriers сохраняются, synthetic historical order не создаётся.
- **Transfer:** explicit new local epoch; source MAC keys не экспортируются.
  Manifest hash не доказывает source authority. Existing local barriers/IDs
  нельзя затереть foreign claims. Locally verified parent proofs наследуются
  только при фактической доступности key/chain; foreign mappings unverified.
- **Consistent backup:** только stable state под lock, canonical primary,
  complete required journal/guard/image proofs и отдельный manifest. Git/Git LFS/
  Releases/Actions artifacts не backup. Raw secret/key export запрещён; disaster
  recovery key policy требует отдельного решения, не подразумевается этим S1.
- **Old backup restore:** только content proposal на current proven head;
  ни старый generation, ни удаление поздних approvals/evidence/REVOKE не принимаются.
  Если нельзя сохранить весь known history, операция blocked. Exact-head repair
  — отдельный ограниченный endpoint §8.3, а не rollback к backup.
- **Lost history:** surviving APPROVE не признаётся последним при недостающих
  negative proofs. CONTINUITY_LOST не снимается admin acknowledgement/new epoch/
  key/date/checksum. Доступны drafts/forensics; proof restore проверяет именно
  прежнюю current lineage. Когда доказательств недостаточно, безопасное
  восстановление authority по этому v1 невозможно. Recovery permission не
  означает право забыть REVOKE или переписать исторический order.

Полное privileged восстановление согласованного старого snapshot+anchor+journal+
registry+keys может быть локально неотличимо от прошлого корректного состояния.
S1 не обещает защиту от этого без дополнительного witness/hardware contract.

## 12. Errors, инварианты и обязательная блокировка

```text
ProtocolError = {
  error_version:1, code:ErrorCode, field_path:ASCII path beginning '$' ≤1024,
  phase:RECEIVE|ADMISSION|PREPARE|INTENT|PUBLISH|FINALIZE|RECONCILE|GENESIS|REPAIR,
  request_id:UUID|null, diagnostic_id:UUID|null,
  detail:{reason:nonempty Text ≤256, expected_sha256:Hex|null,
          observed_sha256:Hex|null, tx_seq:U64|null},
  source_violation:{code:Label, field_path:nonempty Text,
                    message:nonempty Text, object_ref:existing RevisionRef|null}|null
}
```

Source_violation сохраняет original validator code/path/object_ref, не скрывая
причину за INVALID_SNAPSHOT. Верхний ASCII JSONPath отображает Unicode неизвестных
имён полей через escapes; это presentation пути, не normalization payload или
original source path. Сообщения не содержат keys/private text; raw requests
не логируются. Ответ ограничен frame-size bound; oversized diagnostic возвращает
LIMIT с публичным phase/path и diagnostic_id для разрешённой локальной диагностики,
а не truncated валидный snapshot или успешный receipt.

ErrorCode — только строки таблицы (не произвольные расширения). Для failed
editorial checks nested source code остаётся прежним; это transport wrapper,
не изменение existing Violation или codec.

| Code | Путь/смысл и следствие |
|---|---|
| TYPE / WIRE_FORMAT / UNKNOWN_FIELD / MISSING_FIELD / VERSION_UNSUPPORTED / LIMIT | Exact offending JSON field/frame header; reject до trust use |
| AUTHENTICATION_REQUIRED / PERMISSION_DENIED / POLICY_UNAVAILABLE | `$.authorization`; no default grant, no private receipt leakage |
| SERVICE_UNAVAILABLE / PROTECTION_INVALID / PROFILE_UNQUALIFIED | `$.storage_profile`; drafts/diagnostics only, не unprotected writer |
| LOCK_BUSY | `$.lock`; не force unlock по PID/age |
| EXPECTED_HEAD_MISMATCH / EPOCH_MISMATCH | `$.expected_head` / `$.storage_epoch_id`; no new write; lookup admitted request выполняется раньше |
| IDEMPOTENCY_CONFLICT / SESSION_INVALIDATED / SESSION_BINDING_MISMATCH | Request/session fields; не создавать новую decision на retry |
| COMMAND_NO_CHANGE / PLAN_INVALID | Proposal/plan field; admission reject, не guessed transformation |
| SEQUENCE_EXHAUSTED / GENERATION_UNREPRESENTABLE | Counter/generation field; без wrap/reset/clamp |
| EDITORIAL_WIRE_ERROR / SNAPSHOT_CHECKSUM_MISMATCH / REFERENCE_GRAPH_ERROR / REVISION_HASH_ERROR / RIGHTS_BINDING_ERROR / ATTESTATION_DIGEST_MISMATCH | Original source_violation с точным path; pre/postvalidation failure не возвращает partial output |
| ANCHOR_MISSING / ANCHOR_UNAVAILABLE / ANCHOR_MISMATCH | Anchor/proof path; authority/writes blocked, §9 distinction |
| KEY_UNAVAILABLE / MAC_MISMATCH / JOURNAL_PREFIX_MISMATCH / JOURNAL_TRANSITION_INVALID / JOURNAL_TAIL_UNVERIFIABLE | Key/frame/ref; no key regen, guessed frame, tail skipping или older-anchor fallback |
| BLOB_MISSING / BLOB_HASH_MISMATCH / BLOB_TYPE_MISMATCH | Typed BlobRef; no filename-based selection |
| HISTORY_CONTINUITY_LOST / UNVERIFIED_ORDERING / RECONSIDERATION_MISMATCH | History/exact key; dependent decisions blocked, не выбирать UUID/time |
| QUOTA_EXCEEDED / DISK_FULL / FLUSH_FAILED / REPLACE_FAILED | IO boundary; до possible intent reject/abort only with proof; после него pending/manual recovery |
| OUTCOME_UNKNOWN / RECOVERY_REQUIRED / OPTIONAL_CAPABILITY_DISABLED | Нет definitive failure/success без reconciliation; capability OFF по умолчанию |

Фазы проверки: bounded closed parsing → authenticated connection/permission
context → existing request lookup → valid registered protection/head/history →
CAS/live session/source integrity → B/plan/metadata integrity → W1–W9. Для replay
используется приоритет §9. Несколько неисправностей диагностируются в этом
детерминированном порядке, без repair ради прохождения следующего шага.

Обязательные invariants:

1. Ни client JSON, ни MAC-shaped string, score, actor или old receipt не дают authority.
2. Каждая committed approval имеет exact verified local order и matching pair;
   imported records не получают fabricated tx_seq.
3. Record index, tx_seq и generation имеют разные смыслы; timestamp/UUID/order
   массива не разрешают transaction ordering или неоднозначность.
4. Intent необратим; CP — publication primary; ACK — только после verified W8.
5. Stable original commit_ref не меняется при ABORT/repair; tail и ledger могут продвигаться.
6. Missing/invalid proof → block, не восстановление trust из backup/old checksum.
7. Recovery/new epoch не удаляет REJECT/REVISE/REVOKE, consumed IDs или uncertainty.
8. Повтор request не создаёт новый event/ID/generation; replay не перечитывает
   wall clock для изменения frozen canonical bytes.
9. Snapshot bytes и A/O/E00 semantics не расширяются storage fields.
10. Optional partial COMMIT repair отсутствует в baseline переходах.

## 13. Синтетические проверяемые golden vectors

Векторы — **публичные искусственные данные**, не существующие production/anchor/
journal/key или реальные персональные данные. Они не разрешают operational grant.
Service key/DPAPI material в документ не включаются. Только для вычислительных
vectors применяется публично определённый mock input
`K_fixture = SHA256(ASCII("story-studio-public-test-vector-key-v1"))` (raw 32 bytes).
Его значение не является секретом, не используется provisioning и никогда не
служит default/fallback key. Label `fixture-key` не означает registered live key.

Ожидаемые значения ниже зафиксированы литералами. Они рассчитаны вне репозитория
на синтетических объектах: Python canonical JSON + hashlib/hmac, затем независимый
Node.js recursive sorted-key serializer + OpenSSL SHA-256/HMAC. Production
storage реализации ещё нет; expected не получены вызовом будущего tested API.
Все lower-level schema/hash checks и OS/policy proofs тестируются отдельно.

### 13.1 Общие определения и canonical bytes

P=`11111111-1111-4111-8111-111111111111`,
M=`22222222-2222-4222-8222-222222222222`,
E=`33333333-3333-4333-8333-333333333333`,
R=`44444444-4444-4444-8444-444444444444`,
root token=`55555555-5555-4555-8555-555555555555`,
policy ID=`66666666-6666-4666-8666-666666666666`,
connection ID=`77777777-7777-4777-8777-777777777777`.

Snapshot S: schema 2, production P, generation 1; все 12 arrays
`production_revisions,profiles,candidates,sources,claims,scripts,scene_plans,
assets,rights_reviews,approvals,events,approval_authority_evidence` пусты;
active_refs содержит production/candidate/script/scene_plan с null; других полей
нет кроме snapshot_checksum. Его checksum над C(S без snapshot_checksum):
`c557fdd9634346a6e14fb74f9507cbc89a2a58678a08b6c29cda5f18df9e25f6`.
Full C(S) length=473, SHA256=`03f8d66b009768dbba012d051ae466457f6f95903b57c4a62bdce236174d49c0`.

ContentHead H, **точная canonical строка без конечного LF**:

```json
{"content_head_version":1,"editorial_schema_version":2,"generation":1,"machine_binding_id":"22222222-2222-4222-8222-222222222222","production_id":"11111111-1111-4111-8111-111111111111","snapshot_checksum":"c557fdd9634346a6e14fb74f9507cbc89a2a58678a08b6c29cda5f18df9e25f6","snapshot_file_length":473,"snapshot_file_sha256":"03f8d66b009768dbba012d051ae466457f6f95903b57c4a62bdce236174d49c0","storage_epoch_id":"33333333-3333-4333-8333-333333333333","tx_seq":0}
```

C(H) length=458; SHA256=`38c51edfa1db01c9c3d9e4b81311dd49cadeb5b5f4d29469565035d0721036b3`.
Request Q, также exact C(Q) без LF:

```json
{"expected_head":null,"operation":"INITIALIZE_EMPTY","parameters":{"draft_ref":{"byte_length":473,"sha256":"03f8d66b009768dbba012d051ae466457f6f95903b57c4a62bdce236174d49c0"}},"production_id":"11111111-1111-4111-8111-111111111111","request_id":"44444444-4444-4444-8444-444444444444","request_version":1,"review_session_id":null,"storage_epoch_id":null}
```

C(Q) length=352; plain SHA256=`1620bcf520a6c44fe250b3178a5cb0877f632410f82a4187c9c5fefa5d6b7dba`;
**domain-separated Request digest**=
`c93b117738a670e0f117cd1acffb9a24dda7cf72f7fbb35c49ac369c3178bbe0`.

Все следующие объекты воспроизводятся по **полным** schemas выше; определения
ниже задают значения каждого поля, не допускают скрытых defaults. `ref(X)`
означает `{sha256:SHA256(C(X)),byte_length:len(C(X))}`, `jr(X)` — index/MAC
его complete frame. G0 — HistoryGuard version 1, CONTINUOUS, все четыре refs null.

### 13.2 Положительный genesis vector G

1. FrozenCommand F: version 1; request Q и digest выше; key_id fixture-key;
   principal_id `windows-sid:S-1-5-21-1000-1000-1000-1001`; actor задан JSON
   string `"Тест Ї И\u0306 😀"` (escape **декодируется до C**, combining U+0306
   сохраняется); at `2026-11-05T00:00:00Z`; authorization policy ID выше,
   version `fixture-v1`, policy_sha256 — 64 нуля, permission INITIALIZE,
   authenticated_connection_id выше. Assigned approval_id/event_id null;
   storage_epoch_id E, expected_result H, review_snapshot null.
2. ReceiptCore C0: version 1, request R/digest Q, epoch E, operation INITIALIZE_EMPTY,
   tx_seq 0, status INITIALIZED, result_content_head H; approval_ids/event_ids
   пусты, abort_code null.
3. LedgerBlob L0: version 1, type LEDGER_DELTA, production P/epoch E,
   previous_ref null; ровно одна entry: request R, review_session null, digest Q,
   command_mac MAC(F), key fixture-key, tx_seq 0, outcome INITIALIZED,
   receipt_core_sha256 SHA256(C(C0)). G1=G0, кроме ledger_tip=ref(L0).
4. InitializationBody I0: version 1, R/digest Q, P/M/E, root token выше,
   source_ref=ref(S), principal/actor/at/policy те же, guard_before G0,
   key fixture-key. I={body:I0,mac:initialization MAC(I0)}.
5. RegistrationBody T0: registration_version/storage_protocol_version 1,
   P/M/E/root token, initialization_ref=ref(I), storage_profile_id fixture-profile,
   key fixture-key. Wrapper имеет registration MAC(T0).
6. TransactionPlan T: version 1, kind GENESIS, request R/session null/tx_seq 0,
   key fixture-key, command_ref=ref(F), command_mac MAC(F), base_head null,
   observed_primary={state:MISSING}, new_content_head H, image_ref=ref(S),
   guard_before G0, guard_commit G1, expected_commit_receipt C0,
   new_approvals пусто, initialization_ref=ref(I), storage_profile_id fixture-profile.
7. Records имеют version 1, P/M/E, key fixture-key. J0: index 0/previous null,
   type PREPARE, payload {plan_ref:ref(T)}. J1: index 1/previous MAC(J0), type
   PUBLISH_INTENT, payload {prepare_ref:jr(J0),plan_ref:ref(T)}. J2: index 2/
   previous MAC(J1), type GENESIS; payload {prepare_ref:jr(J0),intent_ref:jr(J1),
   plan_ref:ref(T),receipt_core:C0}. CH={committed_head_version:1,content_head:H,
   commit_ref:jr(J2)}.
8. Prepared AnchorBody A0: version 1, P/M/E, INITIALIZING, stable_head null,
   high watermark 0, journal_tail jr(J0); pending version 1/PREPARED/ref(T)/
   prepare_ref jr(J0)/intent_ref null; guard G0, key fixture-key. Final AnchorBody
   A1: version 1, P/M/E, ACTIVE, stable_head CH, high watermark 0,
   tail jr(J2), pending null, guard G1, key fixture-key.
9. ReceiptBody RC: receipt_version 1, core C0, terminal_ref jr(J2),
   result_head CH, key fixture-key.

OS/policy admission для G — **синтетическая precondition test harness**, не
реальный grant. Policy SHA zeros намеренно не указывает на production policy.
Отсутствие actual trusted provider в реальном вызове всё равно PERMISSION_DENIED/
POLICY_UNAVAILABLE, несмотря на mathematically matching MACs.

| C(object) | Bytes | Plain SHA-256 |
|---|---:|---|
| F | 1511 | `858b4b61ae0edf61802c2c24317579a0a47dbb847ae3325d2f06c5e40f523754` |
| C0 | 817 | `a677d7c51ecfde869cf2a0cf8711c2be35f98d27d1f364c9717b1a1e0475017e` |
| L0 | 581 | `48422b24924e9e9629ae01b9050f303b51de27db4ee2ab99181a3629b9cf63d0` |
| I0 | 963 | `000814348a486f01c28002c3773224299e1d1b3f3aacf930977df6740aecc9bc` |
| I wrapper | 1045 | `a373ea493da0880d84d9d7f58629d51a2df15a7085ecbb5e169d8863601ccb45` |
| T0 | 468 | `58a09f754b4274acc379dfe1ff17a5722a6acb4f4bdab24a24a5bbc81dd0327c` |
| T | 2365 | `de9406eb60ac486d32768e0c1ea2c41b235b6fcf9ea6f9eee27111bb6ef06e53` |
| J0 payload | 412 | `8e949848c6755ebfc11b6348f2c3582d9e97392b3ef59c02ce0ed1cd3200969e` |
| J1 payload | 594 | `f0d8ce3fd5219bee5e4a90dddcf77939d5d973d033ceee7c1d7298573240e708` |
| J2 payload | 1532 | `30808c1c7610fb6a10931f1fb09faf52a5ef7a9f088de5448db36774ef7fbe05` |
| CH | 614 | `561cebf2c9543a8db5a1410293feace9434ba97536ade5706ded5b4dc96237fb` |
| A0 body | 836 | `bec91b9eb712ccf93596ec19e0bd3fbfe3c9422d75e12f65c67462a4aba59f54` |
| A1 body | 1256 | `aae253d0d84a122399f27cce03280605a999f0fbfddcac8424cf813db333f10e` |
| RC body | 1612 | `011f780751e2c204d6ead0d729ce3598043c6d07be8e6e5f02629353bf4dba1c` |

| Domain MAC | Expected Hex |
|---|---|
| Frozen F | `d39786287caa22382353e91de044f38d4c1858a9fa2a2cb9271971646f054be7` |
| Initialize I0 | `32489eb0ea65742037d38286438f300ae6906add140f31c73759a91bbfc2c842` |
| Registration T0 | `1162e78c68e39115bde311a8abcab4f83cfdd148b50f13c8dbc10290e1839102` |
| Anchor A0 | `1f3e68f951e4f2bd9f1aa4d4f97ecb722acf767656106ae8a2f6fe2b7050f1fd` |
| Anchor A1 | `d4773fc07e67a9c56371472eccf607b9d93dac50a8957a76a9edad1a69a9daee` |
| Receipt RC | `5a09a85ca13f7cf48ec293533ab4d946e3080581084488370e6500b5a4dad6fa` |

| Frame | Header Hex | Payload bytes | Full frame bytes | Frame MAC |
|---|---|---:|---:|---|
| J0 | `53534a310000019c` | 412 | 452 | `d95894530415aa96dcafdd43aa1366e1be576f17ee4b9e76961c564dd8d8fc48` |
| J1 | `53534a3100000252` | 594 | 634 | `17cb81935040ef4cbcb53fcefafbe7c7c699346336eeb3d1da7be6ce49cacf54` |
| J2 | `53534a31000005fc` | 1532 | 1572 | `e5d986b231a0531ae17c87ab6ff661c0d968697f41bb578975b765f51f355437` |

### 13.3 Альтернативный ABORT vector A и отрицательные vectors

Это **другая test history от J0**, не разрешение fork/join в live journal.
C_abort = C0 с status ABORTED_PRECOMMIT, result_content_head null,
abort_code RECOVERY_PREINTENT_ABORT. L_abort = L0 с outcome ABORTED_PRECOMMIT
и receipt_core_sha256=SHA256(C(C_abort)); G_abort=G0 с ledger_tip=ref(L_abort).
JA имеет context J0, index 1, previous MAC(J0), type ABORT; payload
{prepare_ref:jr(J0),plan_ref:ref(T),abort_code:RECOVERY_PREINTENT_ABORT,
receipt_core:C_abort,result_guard:G_abort}. Ни J1, ни J2 в этой history нет.

| Object | Bytes | Plain SHA-256 |
|---|---:|---|
| C_abort | 391 | `30846a5bbae224f4bd1d319fcebe010b5755d16f17ba2368c1ec3903b94b3327` |
| L_abort | 587 | `2a97a62074063d4bdca1366ed695517b24a20b5dd37ac243c4c422fbee0c817f` |
| JA payload | 1260 | `f2182796685367fff6cd19f38870b884129aace04092c2084d1c4063c85e0ce8` |

JA header=`53534a31000004ec`, full frame length=1300,
MAC=`7fc0d52bf635f7217d375218c951783adb4eb3cc976240958522ed2e6d592d49`.
Ожидаемый результат — INITIALIZATION_ABORTED, generation source не меняется,
primary не публикуется, request R consumed, same-request retry даёт abort.

| Изменение synthetic input | Обязательный expected outcome |
|---|---|
| J0/J1/J2 содержат extra/missing fields или duplicate keys | WIRE_FORMAT/UNKNOWN_FIELD/MISSING_FIELD до trust use; не normalize-and-accept |
| Header length 412→413 без изменения actual bytes/MAC | Incomplete/bad frame → block, не discard suffix |
| Любой MAC bit изменён, полный frame | MAC_MISMATCH; optional reconstruction также запрещена |
| JR с plan_ref hash/length canonical `{}` (2 bytes) | Frame MAC может совпасть, но Plan schema invalid → PLAN_INVALID, никакой INITIALIZED/authority |
| Совместить JA и J1 после общего J0 | Fork/duplicate index → JOURNAL_TRANSITION_INVALID, не выбрать terminal по времени |
| Anchor A1, journal только J0 | JOURNAL_PREFIX_MISMATCH, не downgrade anchor |
| Anchor A0, journal J0+J1+J2, exact S | Verified reconciliation → A1/тот же RC, без второго GENESIS |
| J2 любой proper prefix (GENESIS), в том числе при отдельно принятой PUBLISH-only capability | JOURNAL_TAIL_UNVERIFIABLE, manual recovery; не successful receipt |
| Request reuse R с другим actor claim/unknown client principal field | Unknown field rejected; actor вообще отсутствует в Request |
| tx_seq сериализован как float или U64+1; generation bool | TYPE/LIMIT/SEQUENCE_EXHAUSTED, без rounding/wrap |
| Actor U+0419 вместо U+0418 U+0306 | Другие bytes/hash/MAC; Unicode normalization запрещена |
| Source имеет old approvals/REVOKE, затем imported как INITIALIZE_EMPTY | Admission reject либо explicit IMPORT_BASELINE с unverified history; no authority restoration |

Эти vectors проверяют canonical bytes/crypto/структуры и pure state transitions,
не подтверждают готовность Windows OS authentication или durable file adapter.

## 14. Квоты и Windows profiles — отдельные предложения владельцу

Числа и profiles этого раздела **НЕ УТВЕРЖДЕНЫ D7/D8/D12**. GitHub policy
1 GiB repository target / 10 MiB file threshold не является локальной storage
квотой. Размер этого текстового документа проверяется отдельно перед commit.

### 14.1 Предлагаемый local quota profile Q1

| Параметр | Рекомендация для согласования | Последствие |
|---|---|---|
| Protected retained bytes per production | 32 GiB hard admission quota; считать все archive/images, journal, guard/command/plan blobs, ledger и recovery quarantine | При достижении нельзя silently prune; owner увеличивает quota/диск либо ждёт отдельно approved compaction |
| Предупреждение | 80% quota и любое failed capacity preflight; показывать exact retained bytes/причину | Предупреждение не становится разрешением потерять историю |
| Admission свободного места | Свободно не меньше calculated peak incremental bytes +64 MiB reserve +2 GiB free-space floor | Peak включает все ещё не существующие blobs, sibling B, backup temp A и anchor/journal writes; check advisory, не гарантия против других процессов |
| После intent | Reconciliation не считается новым admission и не отклоняется только из-за warning/quota threshold | Actual DISK_FULL/flush failure оставляет pending/block; освободить unrelated space, не защищённую историю |
| Backup destination | Explicit owner-registered independent local storage, service/authorized backup-agent access; не Git/repo/LFS/облачная публикация по умолчанию | Только data backup; destination/root и privacy policy нужно утвердить |
| Backup schedule | Предложение: weekly consistent full bundle и перед service maintenance, плюс manual on-demand | Часы управляют только расписанием, не transaction order |
| External backup retention | Предложение: последние 4 **validated complete** bundles, старый не удалять до проверки нового полного bundle | Это копии вне active store; active journal/ledger/images никогда не pruning. Numeric schedule/retention требует approval |

Нормальный admission не гарантирует, что другой writer/OS не заполнит диск позже.
Quota update — protected administrative maintenance, не изменение editorial
policy или grant. Никаких auto-uploads, key export, LFS enablement, archive в Git
или больших actual protected fixtures при реализации тестов.

### 14.2 Предлагаемые qualification templates

| ID | OS/аппаратная основа для выбора владельцем | Что не считается уже проверенным |
|---|---|---|
| W11-N | Windows 11 Pro 25H2, build family 26200, pinned UBR/security update; Intel CPU/integrated graphics, 16 GiB RAM, local NTFS, NVMe с указанными driver/firmware/cache settings | Actual UBR, модель/firmware/controller, power-loss qualification должны быть зафиксированы перед tests |
| W10-S | Windows 10 Pro 22H2, build family 19045, pinned UBR и поддерживаемая ESU configuration; Intel CPU/iGPU, 8 GiB RAM, local NTFS, SATA/AHCI | ESU/licensing и maintenance support не предполагаются автоматически; unmaintained OS не production-security profile |
| VM-F | Windows 11 edition/build/UBR pinned в VM, virtual NTFS drive с controlled fault injection | VM reset/write-order simulation не доказывает durability физического SSD/controller |

Это templates, а не fully qualified configurations. Отчёт каждого будущего
profile обязан указать edition/version/**full build+UBR**, patches, NTFS/volume
layout, storage/controller/driver/firmware, volatile cache/flush settings,
service/adapter versions и test evidence digest. Serial numbers, machine private
IDs, keys и actual journal не публикуются в Git. Первое qualification ограничить
одним local NTFS volume для managed primary/temp/protected state; другие layouts
получают отдельный profile. SMB/sync/removable active roots не поддерживаются.

Profile levels: PROCESS_QUALIFIED и отдельно POWER_LOSS_QUALIFIED. Первый не
включает второй. Для power-loss нужны соответствующие physical tests, не только
kill/VM reset. До выбора exact profiles/успешных evidence нет production durability
claim. Никакого NVIDIA/CUDA/cloud/постоянного интернета или дополнительного TPM
anti-rollback witness protocol; требования самой Windows отделены от storage.

## 15. Критерии будущих tests и traceability

| Набор | Обязательный критерий, не claim о текущем запуске |
|---|---|
| Wire/crypto | Literal §13 bytes/length/hash/MAC совпадают; unknown/missing/duplicate/version rejected; U64 >2^53 точен, generation без invented cap; Unicode composed/decomposed различается |
| Dependency graph | Нет self-referential MAC/hash; wrong blob type/hash/length, circular refs, missing prior chain/key fail closed |
| W0–W9 | Kill/fail до/после каждого write/flush/replace/ACK, затем repeated recovery kill; результат только предписанный A/B/pending/block, никаких partial successful receipts |
| Reconciliation | Anchor lag matching prefix допускается; ahead/fork/invalid MAC/unknown primary blocked; нельзя discard complete authenticated tail |
| Default D4 | При capability OFF каждый incomplete terminal block; partial PREPARE/INTENT всегда block. Optional tests/owner acceptance — отдельно, не запуск по client flag |
| Request/session | Lost ACK, conflicting retry, restart, aborted/old epoch reuse, principal mismatch, policy change; один terminal receipt и максимум одна новая decision |
| Order/REVOKE | All negative decisions/latest target checks, legacy gaps, same-time ambiguity, restored old APPROVE, missing negative history, import/transfer/new epoch — без fabricated order/authority |
| Genesis/repair | INITIALIZING/INITIALIZATION_ABORTED/ACTIVE transitions, missing anchor не recreated; repair сохраняет original head/gen/seq и не публикует backup как current |
| Capacity/platform | Quota/disk-full/flush/sharing violation на каждом boundary; no proof eviction; CPU-only offline; unsupported roots rejected; actual Windows ACL/IPC/native tests |
| Qualification | Process crash и power loss раздельно. Потеря ACKed B/receipt при заявленных qualified assumptions — failure durability gate, даже если блокировка безопасна |
| Compatibility | Existing editorial golden bytes/APIs неизменны; pure migration generation/event/evidence semantics прежние; нет hidden fields/automatic network/media execution |

Нужны actual artifacts и independent expected state; mock successful returns
недостаточны. На один finalized PUBLISH request: generation +1, не более одной
approval/evidence pair, один terminal record и стабильный Receipt. ABORT/repair
не увеличивают snapshot generation; genesis сохраняет baseline generation.
Safe block после corruption не доказывает recoverability/durability. Весь
privileged store rollback явно остаётся вне обнаружения baseline протокола.

| Нормативная граница | Где отражена |
|---|---|
| D1/D9 | §1, §5, §7: service-only writes, explicit principals/permissions, draft mode, no default all-gate grant |
| D2/E00 | §8: primary replacement CP, writer lock, backup/temp/CAS, no multi-file atomicity claim |
| D3/A4 | §3/§7: HMAC domains/DPAPI+ACL, separate optional editorial signatures |
| D4 | §9: proof-bound replay; optional partial terminal repair OFF |
| D5/A6/A8–A10/O8/O10 | §4/§10/§11: continuity, exact key, retained negative history, no manufactured legacy order |
| D6 | §5/§11: foreign baseline unverified, new local epoch, no MAC-key export |
| D7 | §14.1: retain all proofs, proposed quotas/backup numbers not approved |
| D8/D12 | §14.2/§15: offline Windows NTFS/CPU target, actual profiles and qualification outstanding |
| D10 | §2–§7/§13: separate closed v1 wire, bounded framing, noncyclic canonical/MAC values |
| D11 | §10: restart-invalid unbound sessions, immutable admitted context, no clock ordering |
| A1–A3/A5/A7/A11–A14 | OS principal/provider boundary, declarations, distinct REVOKE/recovery permissions, missing anchor block, policy separation, no rights/readiness grants |
| O1–O7/O9 | Existing schema-2 arrays/order/event/signature/attestation semantics preserved; no downgrade introduced |
| Story Intelligence | Proposals/Brief не privileged commands или editorial/rights authorization |

## 16. Проверки S1 и решения владельцу

Сейчас выполняются только документационные проверки и воспроизводимость
синтетических vectors, не runtime/storage/service implementation tests.
Один новый документ, no existing-file edits. Проверяются closed field lists,
matching recipes/vectors, SHA/MAC cross-check двумя независимыми подходами,
ссылки, numbering/fences, diff whitespace, размер нового файла и отсутствие
реальных секретов/PII/protected artifacts. `.gitignore` проверяется как часть
policy hygiene, но не изменяется и не заменяет inspection staged file list.

На решение владельца остаются:

1. **Сам S1 v1 contract:** exact schemas/types, operation set, framing, domains,
   counter/payload bounds, metadata roots, errors и literal vectors. Approval
   D1–D12 не является approval этих деталей.
2. **Q1:** numeric quota/floor/reserve/warning thresholds, weekly/pre-maintenance
   backup, independent destination/access и retention 4 validated bundles либо
   указанные владельцем альтернативы. Ни одно число не считается принятым.
3. **Windows profiles:** выбрать actual builds/UBR/editions/hardware/cache
   configurations, including поддерживаемый Windows 10 security maintenance,
   и отдельные process/power-loss qualification evidence requirements.
4. **Optional terminal reconstruction:** оставить OFF в первой реализации;
   enabled implementation потребует отдельного approval и exhaustive acceptance.
   Сейчас approval на неё не запрашивается и не подразумевается.
5. **Legacy-resolution/disaster recovery keys:** не входят в v1. Если proofs
   потеряны, legacy key остаётся blocked; нельзя трактовать этот открытый вопрос
   как разрешённый administrative override/secret export.

Эта публикация не изменяет E00/A/O/D и не утверждает S1 самостоятельно. Она не
создаёт Windows service, filesystem writer/journal/anchor, policy, authority
evaluator, Story Intelligence module, media/model/key или protected data в Git.
Коммит/remote SHA и фактические проверки передаются в итоговом ответе.
После публикации E01.3.9.2/S1 — **STOP**, без PR/merge/release/main changes и без S2.
