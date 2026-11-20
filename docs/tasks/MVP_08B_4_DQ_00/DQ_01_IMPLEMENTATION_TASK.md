# MVP-08B.4-DQ-01 — Implementation Task Proposal

## RESOLVE-01 — текущая редакция

**DOCS_ONLY / CONTRACT_RESOLUTION; PROPOSAL / NOT_APPROVED.** Source commit `0b61892fc4156251b19e5c529c71a6ce783b838d`, tree `7119aa23c700e484cb5c69e24063be67ddef6c6b`; дата 2026-11-20 (Europe/Kiev). Цель — DQ-F01/F02/F03. Native evidence/data draft теперь **version 2**, SQLite layout/schema/user_version остаётся **1**. Это явное versioning уточнённой ранее неутверждённой native-семантики, не изменение G1–G6/OD4 и не implementation grant. Упоминания DQ.LAB v1 в неизменённом старом OWNER_DECISION_PACKAGE — прежняя proposal-рекомендация; актуальные native правила для review задаёт эта RESOLVE-01 редакция и её exact Git SHA.

Никакой SQLite/native execution не выполнялся. Canonical литералы ниже — **DOCUMENT_ARITHMETIC_ONLY**; поля profile/checks/custody являются заданными условными fixture-входами, а не измеренными native facts. Вычисление SHA локальным верификатором **не является независимой проверкой**. Реальная qualification/approval остаётся впереди.

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

## Activation / immutable inputs

**PREPARED TASK — PROPOSAL / NOT_APPROVED / DO NOT EXECUTE.** OD4-01–OD4-07 не являются implementation authorization. Вход: независимая техническая проверка этого DQ-00 пакета, принятие owner category C, exact root/settings/version/bounds и отдельная команда владельца начать код. До этого запрещены sqlite3 connections, создание DB, worker spawn/kill и программирование.

Предлагаемый implementation base: `162a5ff109358625c25ff92402064d214fa50bc0`, tree `4c4bf6405e9dec6d707a1c6928b6068222469041`. Это точная ревизия исходного architecture/baseline, **PROPOSAL для будущего task**, не молчаливый выбор latest main. Contract snapshot — точный DQ-00 publication commit/tree из внешнего manifest. Будущая авторизация должна закрепить обе пары; DQ-00 docs читаются через pinned Git objects, если отсутствуют в implementation base, и не копируются в другие paths.

Предлагаемая branch: `feat/mvp-08b-4-dq-01-durable-storage-lab`. Если занята или base/tree не совпадает — STOP, не reset/force-push. Не использовать live existing projects/database.

## Поимённый proposed allowlist — 10 новых файлов

| Path | Единственная ответственность |
|---|---|
| experimental_mvp/durable_storage_lab/__init__.py | Side-effect-free exports; не открывать DB при import |
| experimental_mvp/durable_storage_lab/contracts.py | Закрытые DQ.LAB records, canonical bytes/hash/ref closure, role/index/proof validation |
| experimental_mvp/durable_storage_lab/store.py | stdlib sqlite3 adapter: exact profile, InitializeNew/OpenExisting, P/A/R, consistent snapshots/proofs |
| experimental_mvp/durable_storage_lab/root_guard.py | Owner-approved root/physical identity/path/cap/owned-cleanup guards для разрешённой OS строки |
| experimental_mvp/durable_storage_lab/harness.py | Coordinator tickets + bounded owned writer/contender workers, handshake/fault evidence, никаких execution providers |
| tests/test_dq01_contracts.py | Pure codec/version/closure/error/data/proof negative oracles |
| tests/test_dq01_store.py | Native positive/CAS/slot/replay/atomic graph/PRAGMA qualification |
| tests/test_dq01_faults.py | FI-01–FI-22 process/control/commit/error/reopen cases |
| tests/test_dq01_security.py | Root/path/limits/forbidden-effect/no-admin/cleanup guards |
| docs/tasks/MVP_08B_4_DQ_01/RESULT.md | Реальные versions/counts/exits/NOT_RUN/limits/SHA и independent handoff |

Список целиком **PROPOSAL / NOT_APPROVED**; owner должен утвердить точный allowlist. Все paths проверяются на отсутствие/collision в exact base до implementation. Никаких изменений PURE modules/tests, CI, dependencies, architecture contracts, project data или дополнительных scripts. Runtime DB/journals/tickets/logs только в отдельно утверждённом root, вне Git. Не добавлять реальные media fixtures.

## Конкретные interfaces

Это proposed ABI lab, не реализация StorePort PURE:

| Interface | Вход / выход / ограничения |
|---|---|
| initialize_new(root_grant, profile, ids) | Только новый approved empty root; measured profile + RootAnchor readback; нет auto fallback |
| open_existing(root_grant, expected_anchor, expected_profile) | Existing-only rw, проверка identities/config; может потребовать recovery writes, поэтому grant обязателен |
| prepare(intent, write_set, staged_objects, ticket_P) | Atomic P; exact input bytes; возвращает qualified PrepareEvidence или HOLD/error, не application COMMITTED |
| apply(prepared_evidence, ticket_A) | Atomic A с повторным head/revision/slot check; только та же M, не executor; ACK не заменяет proof |
| inspect(mutation_id, ticket, expected_anchor) | Bounded consistent read: qualified CommitProof/AbsenceProof либо HoldEvidence; не guessing/repair |
| acknowledge(proof, ticket_R) | Atomic R со сравнением exact head/control_generation; сохраняет ProofAck и pending clear; readback обязателен |
| snapshot(expected_anchor) | ProjectionRoot + ControlRoot + SnapshotEvidence после всех integrity/custody checks |
| close() | Закрыть только owned connection; не стирать pending/данные |

Результат transport: closed `DQ.LAB.Result`, common version=2/scope DQ_PROCESS_KILL_LAB_ONLY и ровно поля `phase:INIT|OPEN|P|A|R|READ`, `mutation_id:?UUID`, `disposition:PREPARED|COMMITTED|NOT_COMMITTED|REUSED|HOLD|REJECTED`, `prepare_ref:?Ref<PrepareEvidence>`, `commit_proof_ref:?Ref<CommitProof>`, `absence_proof_ref:?Ref<AbsenceProof>`, `hold_ref:?Ref<HoldEvidence>`, `ack_ref:?Ref<ProofAck>`, `snapshot_ref:?Ref<SnapshotEvidence>`, `error:?ErrorFields` (inline поля DQ.LAB.Error без common header).

PREPARED требует prepare_ref/snapshot_ref, не выдаёт application outcome. COMMITTED/NOT_COMMITTED требуют соответствующий proof; REUSED возвращает исходный proof/receipt history без write. HOLD требует hold_ref либо error с namespace_hold=true и сохранённый ticket. application_outcome относится только к A: known A proof сохраняет COMMITTED/NOT_COMMITTED при unknown R; UNKNOWN используется, пока A не доказан; отсутствие DB-derived refs при outage не заполняется поддельными hashes. REJECTED preflight не является NOT_COMMITTED прежней M. После verified final negative R повтор старой M возвращает прежний NOT_COMMITTED, не повтор A. Новый storage attempt — новая явно разрешённая M; никакой автоматической замены unknown M.

## Предлагаемый SQLite schema layout v1

Все перечисленные таблицы входят в одну DB с одним binding. Canonical BLOB всегда сравнивается с digest/kind/version/scope; SQL rows/indices не являются самостоятельным proof. Foreign keys ON; application проверяет дополнительные cross-table invariants. Не полагаться на JSON1/extensions/triggers/arbitrary SQL.

| Table | Колонки и ключи/инварианты |
|---|---|
| store_meta | singleton PK=1; store_id/namespace_id/store_epoch/schema_version/profile_digest/anchor_digest; application_sequence U; head_marker_digest nullable; control_generation U; pending_mutation_id nullable. Binding immutable, counters не уменьшаются |
| control_nodes | digest PK; kind/version/scope; canonical_blob; immutable. Profile/anchor/key/intent/WS/marker/ack/evidence nodes; unindexed blob presence не authoritative outcome |
| mutation_registry | mutation_id PK; intent_digest UNIQUE FK control_nodes; write_set_digest FK; phase PREPARED/APPLIED/RESOLVED_COMMITTED/RESOLVED_NOT_COMMITTED; marker_digest nullable; latest_ack_digest nullable. Canonical intent не обновляется |
| staged_objects | (mutation_id,object_digest) PK; canonical_blob/kind/version/scope/role; expected byte length/hash. Retained plan/input bytes, **не committed A-members**; не удалять до evidence retention/cleanup grant |
| committed_objects | object_digest PK; object_id UNIQUE; role; owner_job_id nullable; canonical_blob; created_by_mutation_id FK registry. Immutable data-only rows, duplicate digest с другими bytes — corruption |
| mutation_members | (mutation_id,object_digest) PK; object_digest FK committed_objects; только новые A-members; exact WriteSet membership |
| jobs | job_id PK; key_digest UNIQUE FK control_nodes; current_job_digest FK committed_objects; state/revision/cancel_requested. Совпадение с canonical JOB и allowed lab transitions |
| admissions | key_digest PK FK control_nodes; job_id UNIQUE FK jobs; receipt_digest UNIQUE FK committed_objects; immutable REQUEST ref и receipt mapping |
| events | event_id PK; job_id FK jobs; revision_to Pos; data_digest UNIQUE FK committed_objects; mutation_id FK registry; UNIQUE(job_id,revision_to). Append-only |
| active_slots | (store_id,namespace_id,project_id,purpose_id) PK; job_id UNIQUE FK jobs; slot_digest FK committed_objects; только current HELD. Release удаляет current index, но RELEASED immutable slot data/history остаются |
| outbox | effect_token PK; outbox_id UNIQUE; job_id UNIQUE FK jobs; data_digest UNIQUE FK committed_objects; payload_digest; dispatch_allowed CHECK false. Никакого delivery/executor |
| read_reservations | (job_id,checkpoint_id,call_index) PK; data_digest UNIQUE FK committed_objects; base_cursor; read_kind; call_index 1..3. Append-only, reset от reopen запрещён |
| proof_acks | mutation_id PK FK registry; ack_digest UNIQUE FK control_nodes; control_generation; outcome COMMITTED/NOT_COMMITTED. В первом lab один окончательный Ack/M; immutable |

В P атомарно insert registry/control/staged и set pending/control_generation+1. В A атомарно insert committed members, projections/member-links/marker и update registry(APPLIED)/head/application_sequence+1/control_generation+1; pending остаётся. В R атомарно insert proof_acks, registry resolved outcome, clear pending и control_generation+1. Object/projection/member constraints rechecked внутри tx. Marker может быть control_node, но попадает в authority только через согласованный registry/head/readback.

Read-only inspect не пишет новые authoritative rows: может собрать canonical evidence в coordinator memory/artifacts. Для R необходимые proof/snapshot/root nodes сохраняются вместе с Ack как immutable evidence; ControlRoot отражает только indexed registry/staged links/ack indices, не произвольные nodes. Ack ссылается на pre-R Snapshot/ControlRoot; post-R ControlRoot содержит Ack — chronological DAG без self hash.

При ADMIT fresh request/manifest/input closure копируется из staging в committed_objects в том же A; уже committed immutable inputs не входят в new members. Terminal proof/released slot остаются в history. Absence проверяет actual committed/projection/member tables, а не наличие planned bytes в staging.

## Порядок реализации после отдельного разрешения

1. Freeze технических B вопросов и owner C grants; exact native runtime/settings/root/allowlist. Без этого STOP.
2. Native records/closed DTOs/codec/ref closure и in-memory conformance vectors. Не использовать PURE fake proofs как native authority.
3. Root/InitializeNew/OpenExisting/profile measurement/readback. Не открывать прежнюю DB в create mode, не менять config на reopen.
4. P/A/R и complete snapshot/proof validators. Отдельные tests byte equality/M conflict/CAS/slot/history/absence; no executor.
5. Coordinator-owned tickets и bounded workers/contender; FI cases с фактическими checkpoints и hard timeout. Никакого killing arbitrary PID/process name.
6. Security/limits/negative cases; full test/report/independent acceptance packet. STOP, не переходить к Windows adapter или Q5 physical execution.

## Test entry и acceptance

Предлагаемые Python: 3.10.22 и 3.13.18, каждое с exact measured stdlib SQLite/native profile. Exact SQLite/source-id/compile-options/OS/filesystem **NOT_MEASURED**, должны быть pinned до write cases. Если другая версия — отдельное согласование, не auto-install. First implementation platform proposal — Linux local test root; Windows 10/11 profile WINDOWS_NOT_RUN, не писать Windows-native adapter в этот increment.

Обязательные tests: все 4 listed dq01 modules, FI-01–FI-22 и их P/A/R subcases; positive/negative native schemas, byte/hash/ref/domain mismatch, immutable conflicts, namespace identity/missing DB/stale image, competing writers, CAS, key/slot/history, outbox/reservation data, unknown-after-ACK и diagnostic failure. Root/path/caps/no-executor assertions обязательны. Existing шесть pure modules и SP regressions запускаются как ограниченная compatibility regression, отдельно от native PASS.

Future commands: approved interpreter `-m pytest -q -p no:cacheprovider` с exact listed modules; fixture root передаётся явным mandatory owner-approved parameter, не default temp path. Каждый test command ≤60 s, overall acceptance ≤300 s; max 2 owned children, 5 s/stage, handshake ≤2 s, FI-07 ≤3 race trials. Указанные значения PROPOSAL и требуют C approval. Ненаступивший checkpoint — NOT_RUN/BLOCKED, timeout — FAIL; не снижать oracle и не повышать caps для зелёного прогона.

FI-07 standard sqlite3 scope — COMMIT_RACE_WINDOW, не доказанный internal VFS kill. Если reviewer требует внутреннюю engine-точку, case BLOCKED_INSTRUMENTATION до отдельной поддержки. Kill не доказывает power-loss. Full restore и coordinator death вне envelope; custody loss → HOLD.

Acceptance: exact base/tree/allowlist, measured matching profile, все обязательные выбранные native cases фактически PASS, нет hidden retries/partial projections/fake absence/extra admission, no executor/provider/files outside root, raw logs/SQLite codes/exits/timeouts/counts/skips и SHA evidence, независимый review и owner decision. Failed/skipped mandatory case блокирует принятие; NONE/NOT_RUN не маскируется под PASS. Lab qualification не production JobStore readiness.

RESULT должен содержать actual branch/base/commit/tree (внешний manifest для self hashes), exact diff/file SHAs, native config/readback, реальные counts/exits/fault checkpoints, лимиты/NOT_RUN/Windows gaps. Публикация только отдельной ветки без merge/CI/main/dependency changes.

## Ещё необходимые разрешения / STOP

Owner C: exact allowlist; конкретный disposable root/platform; native writes/init/reopen/recovery/cleanup; owned spawn/kill process operations; caps и fault limits; отдельное начало программирования. Technical B: independent contract/native proof/SQLite/negative oracle review. **Ни одного из этих разрешений этот task себе не выдаёт.**

STOP при неразрешённом profile/root, missing source version, идентичности/closure/atomicity contradiction, UNKNOWN без same-M recovery, неполной evidence, необходимости добавить file/dependency/реальный executor или выйти за caps. Не менять G1–G6/COMPLETED/PURE ради адаптера. После реализации — STOP для independent acceptance; не переходить автоматически к Windows/Q5/production.

## RESOLVE-01 — обязательные implementation entry и tests

Текущий authoritative contract snapshot для review — exact RESOLVE-01 publication commit/tree из внешнего manifest, а не старый DQ-00 native v1. Предлагаемый implementation base остаётся 162a5ff... / 4c4bf640... в полной записи выше; будущий owner task обязан закрепить обе полные пары. Allowlist ровно прежние 10 paths; он всё ещё PROPOSAL, actual root/caps/native/process grants не выданы. Никакого Native/PURE adapter coding сейчас.

Native evidence/data **version 2**, physical SQLite layout/schema/user_version **1**. Ранее неутверждённый v1 уточнён явно, без изменения OD4/G1–G6 и без редактирования запрещённых этим task файлов. Старые v1 упоминания в unchanged OWNER_DECISION_PACKAGE — historical proposal, не текущая authority. Новая реализация обязана отказать при v1 ref под v2 profile.

### DQ-F01 acceptance oracles

Сначала pure contract tests на literal catalogue F01-P01–P03/N01–N06: exact retained ticket bundle, prepared/staged без A, qualified absence, partial members, lost ticket/coordinator и identity changes. No ticket/full closure/continuous coordinator/custody — UNKNOWN, не NOT_COMMITTED. Нельзя восстановить потерянный runtime evidence из публичного каталога fixture. **Восстановление после падения всего приложения первым DQ-01 не квалифицируется**; coordinator crash — BLOCKED_WHOLE_APPLICATION_RECOVERY.

R negative closure при P absent использует exact ticket canonical input, может atomic insert RESOLVED_NOT_COMMITTED control/expected closure/Ack с pending=null при G/head compare. Никаких A rows и никакого заявления о committed P. После final negative R old M read-only; unknown M не заменяется новой.

### DQ-F02 acceptance oracles

В tests/test_dq01_contracts.py встроить неизменённые literal preimages/digests/ref tuples из этого proposal (или прочитать pinned Git docs как review input вне tracked paths); не создавать дополнительный fixture file в Git. Проверить все F02-P01–P07/N01–N07 и original closed schemas/role bindings/cycle detection, включая refs в payload_hex. Current external verifier не является native adapter implementation и не доказывает native PASS.

Explicit generation arithmetic: P 0→1, A 1→2, R 2→3 для committed branch; prepared-negative R 1→2; unprepared-negative R 0→1. General rule pre-R G → Ack.target G+1 → post-R root/snapshot G+1. Ack/application head exact, no changing A root/sequence in R. У A-known/R-unknown сохранить known A proof и HOLD; не повторять A.

R_ABSENT_FOR_TICKET: retained exact ticket_R/Ack+original A proof, fresh qualified snapshot with exact pre-R control root/head/G, pending=M (или null unprepared-negative), no expected Ack in registry/index, unchanged custody/state. Только тот же M и exact original Ack permitted; fresh Snapshot ID не разрешает recompute original Ack. Если bytes/ref missing, wrong generation/head/binding, corrupt Ack или changed roots — HOLD, no R retry.

ProofAck → original pre-R proof/Snapshot/ControlRoot; only post-R ControlRoot → Ack; no Ack → post-R root/snapshot edge. Реализация с циклическим preimage или «пока нулевым digest» — FAIL/STOP.

### DQ-F03 acceptance / STOP

FI-01–FI-22 сохраняются, FI-07/CW-01–CW-05 из matrix обязательны. Разделять BEFORE_CALL/REQUESTED_ONLY, qualified SQLite COMMIT trace или post-call return как invocation evidence, ACK receive/loss, controlled kill in software window и qualified reopen outcome. До trace/return событие BEFORE_CALL не считается наблюдаемым вызовом; фактический checkpoint не переименовывается ради PASS. Requested checkpoint не достигнут — NOT_RUN/BLOCKED_CHECKPOINT, не PASS, даже если соседний case успешно открыл DB. В стандартном первом lab **COMMIT_RACE_WINDOW** — только заявленная coverage; actual internal VFS/fsync checkpoint и power loss NOT_RUN/OUT_OF_SCOPE. Нужда в engine hooks/других dependencies, whole-app restart или большем scope — STOP, отдельная авторизация.

Current conformance vectors/expected outcomes — locally calculated **not independently validated**. После независимой контрактной re-review нужны прежние CP grants и новая отдельная implementation authorization; этот task не запускает DQ-01.
