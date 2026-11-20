# DQ-01 — Durable Storage Contract Proposal

## RESOLVE-01 — текущая редакция

**DOCS_ONLY / CONTRACT_RESOLUTION; PROPOSAL / NOT_APPROVED.** Source commit `0b61892fc4156251b19e5c529c71a6ce783b838d`, tree `7119aa23c700e484cb5c69e24063be67ddef6c6b`; дата 2026-11-20 (Europe/Kiev). Цель — DQ-F01/F02/F03. Native evidence/data draft теперь **version 2**, SQLite layout/schema/user_version остаётся **1**. Это явное versioning уточнённой ранее неутверждённой native-семантики, не изменение G1–G6/OD4 и не implementation grant. Упоминания DQ.LAB v1 в неизменённом старом OWNER_DECISION_PACKAGE — прежняя proposal-рекомендация; актуальные native правила для review задаёт эта RESOLVE-01 редакция и её exact Git SHA.

Никакой SQLite/native execution не выполнялся. Canonical литералы ниже — **DOCUMENT_ARITHMETIC_ONLY**; поля profile/checks/custody являются заданными условными fixture-входами, а не измеренными native facts. Вычисление SHA локальным верификатором **не является независимой проверкой**. Реальная qualification/approval остаётся впереди.

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

## 1. Точная область первого lab

**PROPOSAL / NOT_APPROVED.** Один disposable database, один immutable store binding/namespace и один selected qualification profile на case-run. Только synthetic storage DTO, bounded SQL и owned writer processes после отдельной авторизации. Не подключать native lab к существующему PURE Controller/StorePort под видом drop-in замены. Не исполнять outbox. Никакой generator/renderer/Library/save.

Native data — отдельные DQ.LAB-типы из [NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md](NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md). Совместимость означает сохранение инвариантов identity/atomicity/UNKNOWN/replay, не выдачу новых DTO за прежние PURE bytes. Lab states: DRAFT, LAB_CHECKPOINT, CANCELLED, FAILED. Последние два — терминальные только внутри no-executor lab при наличии подходящего доказательства. COMPLETED и RESULT_AVAILABLE не являются состояниями этого lab и не переопределяются.

## 2. Предусловия и identity

InitializeNew допускается только по явному будущему grant в новом пустом проверенном root. Создаёт новые run_id/store_id/namespace_id и store_epoch=1; binding содержит schema version, exact runtime/settings profile и физические root/database identities. Один namespace на database; смена namespace/epoch, повторное присвоение старого store_id новой базе и implicit migration запрещены.

После initialization publish/readback RootAnchor; только затем начинаются операционные cases. Отсутствие anchor или прерывание initialization — BLOCKED_INITIALIZATION (qualification-case status, не новый transport ErrorCode), а не NOT_COMMITTED старого store. До certified anchor transport error имеет phase=INIT, mutation_id=null, application_outcome=NOT_ATTEMPTED и STORE_UNAVAILABLE либо STORE_CORRUPT по факту; фальшивый HoldEvidence/binding не создаётся. OpenExisting использует existing-only open и обязано проверить anchor/identity/version/config; оно никогда не создаёт файл. Установка journal/PRAGMA при reopen не должна молча менять profile.

Coordinator сохраняет ожидаемый anchor, mutation tickets и последний подтверждённый marker/watermark вне writer-процесса. **Fault target первого lab — writer/contender; coordinator не убивается.** Его потеря или потеря ticket/custody делает run BLOCKED, не автоматически восстанавливаемым. Это ограничение выбранного процесса-kill envelope, не заявление об автономном production recovery.

## 3. Три согласованных транзакционных шага

**P — Prepare transaction:** explicit BEGIN IMMEDIATE. Проверить binding, отсутствие чужого pending M, immutable M reuse/conflict и ожидаемую head/revision. Атомарно сохранить canonical intent + WriteSet + staged member/input bytes и установить namespace.pending_mutation_id=M. Prepare ACK тоже требует readback/proof; ошибка COMMIT не доказывает, что prepare отсутствует. Coordinator ticket существует до P.

**A — Apply transaction:** только для той же qualified prepared M. BEGIN IMMEDIATE; заново проверить state head/CAS/key/active slot. Атомарно materialize committed objects и все application projections: job/current revision, event, admission/receipt при ADMIT, slot delta, outbox/read reservation при соответствующей операции, member links и CommitMarker. Marker связывает immutable M/WriteSet, previous marker и resulting projection root; meta.head/sequence меняются в том же COMMIT. Pending M не снимается этим шагом.

**R — Resolution/ack transaction:** в полном consistent read snapshot получить и проверить CommitProof либо AbsenceProof. В отдельной BEGIN IMMEDIATE заново проверить неизменность evidence/head/generation, атомарно сохранить ProofAck и снять pending M. Acknowledgement COMMIT/lost ACK также может быть UNKNOWN: до qualified readback Ack/состояния pending coordinator продолжает HOLD и не повторяет A. Native Ack не является заявлением о внешнем эффекте.

После qualified P readback новая M по-прежнему заблокирована, но A той же M разрешён только по PrepareEvidence и ticket_A. Unresolved P/A/R HOLD запрещает A, пока соответствующее доказательство не получено.

P и R — control-only транзакции; они не являются commit application write-set. A — единственная application boundary. Fault cases маркируются phase=P/A/R, не объединяются под неоднозначным «commit». Ни одна строка staged/control metadata не является доказательством application COMMITTED.

## 4. Атомарность и idempotency

В первом lab окончательно acknowledged NOT_COMMITTED закрывает старую M: её повтор — read-only replay отрицательного исхода, не новое A. Если требуется новая application попытка, она получает новую M и заново проходит все проверки по отдельному разрешённому case. Это storage-lab restriction, не изменение поддерживаемых retries PURE Controller; direct integration отсутствует. Неизвестная M никогда не заменяется новой.

Full admission key связывает store binding, project/purpose, immutable request DataObject, batch/revision и manifest. Active projection — (store_id, namespace_id, project_id, purpose_id); namespace единственный и immutable, поэтому дополнительная координата не разрешает обход one-active-intent. Нельзя создать второй namespace, чтобы освободить purpose.

В A admission одновременно создаёт job revision=1, immutable receipt, event и HELD slot; fresh input objects тоже становятся committed в A. Повтор полного key/request/receipt history — REUSED без revision/event/outbox/effect. Old supplied key + иное содержимое — конфликт. Новый valid key при HELD slot — ACTIVE_INTENT_CONFLICT. Терминальный historical replay возвращает прежний receipt даже при новом активном job; не захватывает slot заново.

Переход требует expected_revision и resulting_revision=expected+1; одинаковый M с другими canonical intent bytes — MUTATION_ID_CONFLICT. Все changed DataObjects имеют новые immutable identities; committed bytes не обновляются/удаляются. Повтор применённой M возвращает исходный Marker/receipt, не создаёт новые projections. Версионирование M изменением payload не допускается.

HELD slot удерживается во всех nonterminal lab states. Release — только A с допустимым terminal-state data и no-executor terminal proof, event/job/released-slot data в том же write-set. Нельзя объявить release разрешением на next admission, пока pending M/неизвестный R не разрешены.

## 5. Mutation registry, HOLD и proof

До каждой P/A/R coordinator фиксирует ticket: binding/M/intent digest/phase и последнее квалифицированное head/ack состояние. Если writer потерян или ACK отсутствует — UNKNOWN, весь namespace блокирует новые prepare/apply/admission/model enqueue; разрешены bounded read-only inspection и resolution той же M. После reopen pending registry плюс coordinator ticket восстанавливают hold. Локальная память нового worker не источник истины.

**COMMITTED** для A: complete consistent existing database/custody; exact binding/profile; immutable intent/WriteSet; marker и все M-linked committed members/projection links; hash/length/role/CAS/slot consistency; marker chain/head и resulting ProjectionRoot проверены. При наличии последующих разрешённых commits проверять historical M по согласованной истории, а не требовать, чтобы его root был current root. Для каждого marker chain проверяется, что previous ProjectionRoot + exact WriteSet delta даёт recorded resulting root; актуальные indices проверяются по current root, historical job/slot versions остаются immutable objects. В первом lab новые commits сериализованы pending barrier, поэтому до R expected head однозначен.

**NOT_COMMITTED** для A: тот же qualified snapshot доказывает отсутствие marker **и всех A-members/links/projection changes для M**, expected previous head/revision/index остаются согласованными. Prepared/staged intent/input bytes могут присутствовать, но не считаются применёнными members. Один missing marker недостаточен. Если Prepare самой M неизвестен, coordinator ticket остаётся обязательным; нельзя подставить другую M. Отсутствующая P row не мешает проверить A absence, если expected canonical Intent/WS доступны из ticket, binding/custody проверены и application root равен expected previous root; это не утверждение, что Intent был прочитан из DB.

**UNKNOWN:** несовпадение, partial set, недоступность, missing database, неквалифицированный root/identity/config/custody, stale-copy doubt. Hash/COMMIT return/integrity_check='ok' сами по себе не меняют UNKNOWN. Проверяемый R/ProofAck снимает hold; никакого manual clear/automatic new database API нет.

## 6. Outbox и reservations — только storage data

Model ENQUEUE сохраняет один immutable outbox/effect token/payload digest в A; dispatch_allowed=false, вызова executor вообще нет. Token при recovery не меняется; token с другим payload конфликтует. Это тест хранения intent, не физическая exactly-once qualification.

Model READ_RESERVE сохраняет checkpoint/base_cursor/call_index 1..3 и job revision/event в A. Три total reservations, не три retries; interrupted reservation считается использованной. Restart/duplicate/same cursor не сбрасывают counter. Ledger/provider read не выполняется. Превышение bound отклоняется до A; UNKNOWN reservation COMMIT блокирует следующую reservation до R.

## 7. Corruption / stale copy / missing database

Проверять canonical bytes и closures, текущие projection indices, foreign keys, integrity_check и sequence/marker ancestry. Файл или journals отсутствуют/нечитаемы — HOLD; не InitializeNew. Old file identity, меньший sequence относительно coordinator watermark, другой anchor/profile/store/epoch или известный старый image — STALE_COPY/HOLD. Не «лечить» удалением journals/пересозданием registry.

Восстановление старой копии между unacknowledged COMMIT и inspection в общем случае неотличимо от rollback без внешнего nonrollbackable witness. Первый lab не заявляет такой restore/tamper-proof гарантии: требуется непрерывная контролируемая custody root/DB/journals, coordinator и ожидаемого watermark. При утрате custody/сомнении — UNKNOWN/BLOCKED, NOT_COMMITTED выдавать нельзя. Полноценный restore, coordinator crash и malicious same-account rewrite вне OD4-06 envelope и не получают PASS.

## 8. Матрица обязательств

| Обязательство / инвариант | Отрицательный сценарий | Необходимое доказательство |
|---|---|---|
| Identity immutable и existing-only open | missing/replaced DB, другой namespace/epoch | RootAnchor + physical identities + exact profile/custody; иначе HOLD |
| Version/profile exact | другая schema/runtime/settings | Header/profile bytes + version checks; нет implicit migrate |
| Request/receipt/M immutable | reuse M/key с изменёнными bytes | Canonical bytes/digest comparison и исходная history |
| A write-set atomic | process kill после subset statements | consistent snapshot: весь набор+marker либо доказанная пустота; partial=UNKNOWN |
| Active uniqueness | два процесса same purpose/new keys | native unique constraint + outcomes + отсутствие losing projections |
| CAS | stale revision | rowcount/transaction result и unchanged job/event/slot |
| Registry precedes unsafe apply | crash до/после P ACK | coordinator ticket + P readback; unknown P блокирует A |
| Marker связывает все данные | marker без member / corrupt bytes | complete member links, projection root, ancestry, structural checks |
| Outbox/reservation atomic | intent/reservation записан отдельно от job | один A marker + exact bound references/revisions |
| UNKNOWN retains HOLD | lost A/R ACK, unreadable snapshot | retained pending/ticket, zero next admission until proof |
| COMMITTED / NOT_COMMITTED | row/ACK/missing marker принят как proof | typed CommitProof/AbsenceProof complete consistent snapshot |
| Reopen recovers same M | worker restart создаёт новый id/token | ticket+registry+marker/absence+same binding |
| Corrupt/missing/stale fail closed | silently new DB / старый image | identity/watermark/custody checks и отказ, не fabricated proof |
| Terminal release / historical replay | lost release ACK затем new admit | terminal proof+atomic A; pending R barrier; old receipt unchanged |
| Permissions/full disk/interrupted tx | SQLITE_FULL/IOERR/permission/BUSY | typed response, unchanged или UNKNOWN verified; никакого guessed rollback |

Детальные ожидаемые исходы — [FAULT_INJECTION_MATRIX.md](FAULT_INJECTION_MATRIX.md). Схемы и SQL layout — native evidence и DQ_01 task. Все эти положения ещё требуют независимой проверки; implementation не начинается автоматически.

## RESOLVE-01 / DQ-F01 — qualification envelope, не whole-app recovery

Условный NOT_COMMITTED требует retained **полного ticket bundle** и непрерывного coordinator run плюс qualified identity/custody/complete snapshot, expected previous head/root и отсутствие **всех** A-members/links/changes/marker. Prepared/staged intent без A — допустимый положительный absence case, но не rollback P. Нет ticket/coordinator/custody — нет absence proof, даже если SQL rows/flags выглядят правдоподобно. DB/root identity mismatch или writer kill без qualified reopen дают UNKNOWN/HOLD.

**Первый DQ-01 не квалифицирует восстановление после падения всего приложения.** Coordinator/run loss не чинится новым run ID или реконструкцией ticket из DB. Missing existing DB не считается empty authoritative state. Положительные и отрицательные literal vectors, включая partial members при missing marker, заданы в native v2 catalogue F01-P01–P03/N01–N06; это вычисленные документы, не native PASS.

Если P отсутствовала, coordinator ticket является expected input, не DB-derived intent. После квалифицированного A absence возможна negative R closure: atomically persist expected immutable control/input closure, registry RESOLVED_NOT_COMMITTED, Ack и pending=null без application rows. Guard — exact original ticket/binding/head/control_generation и отсутствие чужого pending. Это разрешает закрыть M без заявления, что P или A committed; повтор старой M read-only.

## RESOLVE-01 / DQ-F02 — P/A/R readiness

Native evidence/data version **2** — текущий proposal. SQLite layout/user_version остаётся 1. P известен только по PrepareEvidence и canonical staged/control readback. A известен только по complete CommitProof/AbsenceProof; ни факт вызова COMMIT, ни ACK не заменяют proof. Namespace reservation после P не равна uncertainty: другие M блокированы, A той же M разрешён только после qualified P.

Для R точные generation правила: pre-R G/h; Ack.target control_generation=G+1; ticket_R.expected_control_generation=G; post-R generation=G+1/head=h, latest_ack/exact ack index/pending clear подтверждены вместе. Known A outcome сохраняется при unknown R; HOLD не снимается. R absence проверяется fresh qualified snapshot против exact pre-R roots/head/G и expected Ack absence. Только затем same-M/exact-Ack R retry; A не повторять. Fresh Snapshot UUID не даёт права перестроить оригинальный Ack preimage.

Original A proof/ack не ссылаются на post-R roots; post-R ControlRoot ссылается на Ack, который ссылается на pre-R proof/snapshot. Никакого self/cyclic hash. Любой corrupt/foreign Ack, wrong generation или stale head запрещает release/retry.

## RESOLVE-01 / DQ-F03 — точка наблюдения не гарантия физической точки

COMMIT_RACE_WINDOW — единственный proposed lab scope: наблюдаемый вход в вызов, controlled kill в доступном software window, ACK observation и последующий qualified reopen/proof. Не объявлять это kill внутри SQLite VFS/fsync и не приравнивать process kill к power loss. Не достигнутый requested checkpoint — NOT_RUN/BLOCKED, не PASS. Exact FI-oracles и STOP — в обновлённой FAULT_INJECTION_MATRIX.md. Ни одна из этих уточняющих proposals не даёт разрешения запускать DQ-01.
