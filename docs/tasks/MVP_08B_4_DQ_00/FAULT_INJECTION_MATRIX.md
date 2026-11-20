# DQ-01 — Fault-Injection Matrix

## RESOLVE-01 — текущая редакция

**DOCS_ONLY / CONTRACT_RESOLUTION; PROPOSAL / NOT_APPROVED.** Source commit `0b61892fc4156251b19e5c529c71a6ce783b838d`, tree `7119aa23c700e484cb5c69e24063be67ddef6c6b`; дата 2026-11-20 (Europe/Kiev). Цель — DQ-F01/F02/F03. Native evidence/data draft теперь **version 2**, SQLite layout/schema/user_version остаётся **1**. Это явное versioning уточнённой ранее неутверждённой native-семантики, не изменение G1–G6/OD4 и не implementation grant. Упоминания DQ.LAB v1 в неизменённом старом OWNER_DECISION_PACKAGE — прежняя proposal-рекомендация; актуальные native правила для review задаёт эта RESOLVE-01 редакция и её exact Git SHA.

Никакой SQLite/native execution не выполнялся. Canonical литералы ниже — **DOCUMENT_ARITHMETIC_ONLY**; поля profile/checks/custody являются заданными условными fixture-входами, а не измеренными native facts. Вычисление SHA локальным верификатором **не является независимой проверкой**. Реальная qualification/approval остаётся впереди.

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

**PROPOSAL / NOT_APPROVED. Все проверки сейчас NOT_RUN.** Здесь ожидаемые oracles, а не выполненные SQLite результаты. Обозначения фаз P/A/R — Prepare / application Apply / proof Resolution+Ack из durable contract. UNKNOWN означает unresolved application outcome либо неразрешённую control phase; поле phase сохраняется, чтобы не смешивать их.

## Общий oracle

Для каждого case сохранять run/binding/profile/M/WriteSet/ticket identities, точную фазу и последнее квалифицированное head/ack, checkpoints child/coordinator, raw exit/kill observations, bytes/hashes snapshot/proof и целый projection graph. Исключение или exit code процесса не определяет COMMIT outcome.

До qualified proof — namespace HOLD; после него release только через R/ACK readback. Pending control records и staged bytes не A-members. Повтор unknown M означает только read-only inspection/resolution, не повтор A. После окончательного R с NOT_COMMITTED старая M остаётся immutable terminal outcome/read-only replay; новая application попытка допускается только как отдельная явно разрешённая операция с новой M и заново проверенными CAS/key/slot. Автоматических SQL retries нет. COMMITTED replay возвращает original marker/receipt без дополнительных projections.

| Case | Boundary / negative input | Ожидаемый outcome | Active slot | Namespace HOLD / повтор | Необходимое доказательство и PASS |
|---|---|---|---|---|---|
| FI-01 | До BEGIN P, child не начал SQL | NOT_COMMITTED для A только после qualified absence; до read UNKNOWN | Исходный | Ticket pending до подтверждения отсутствия; A не запускать | Parent checkpoint + existing same-store consistent snapshot без M marker/members и с прежним root |
| FI-02 | После BEGIN P, до записи registry | UNKNOWN, затем квалифицированное отсутствие или подготовленный intent | Исходный | HOLD; inspect same M | Отсутствие application changes; P commit status проверяется отдельно от A |
| FI-03 | После записи intent/staged в P, до P COMMIT | UNKNOWN P; A не мог законно начаться | Исходный | HOLD до проверки P/absence | Registry/staged полностью committed либо отсутствуют; partial control/corruption остаётся UNKNOWN |
| FI-04 | P COMMIT вернулся, ACK потерян | UNKNOWN P | Исходный | HOLD; никакого нового intent/M | Qualified P readback/ticket binding; P presence не равно A COMMITTED |
| FI-05 | После BEGIN A, частичные member/projection writes до COMMIT | UNKNOWN при kill, ожидается rolled-back A после qualified reopen | Исходный; не частично новый | HOLD до absence proof | Полное отсутствие A marker/members/changes, прежний application root; любое partial authoritative set = FAIL |
| FI-06 | До вызова A COMMIT, все SQL statements исполнены | UNKNOWN до evidence | Исходный либо целиком итоговый только если commit доказан | HOLD; не повторять A | Complete Marker+WriteSet либо qualified absence; SQL statements до COMMIT сами не proof |
| FI-07 | Только наблюдаемое COMMIT_RACE_WINDOW, отдельные event/kill/ACK факты | UNKNOWN до qualified A proof; затем COMMITTED или NOT_COMMITTED по exact proof | Целиком прежний либо целиком новый | Barrier до qualified R; lost ACK не repeat A | Нужны reached checkpoint + owned kill/exit + phase trace + полное proof. Внутренний VFS/fsync и power-loss не covered |
| FI-08 | A COMMIT физически произошёл, ACK не получен | UNKNOWN → COMMITTED по proof | Итоговый, но новый admission запрещён до R | HOLD, даже если terminal slot уже физически RELEASED | Exact marker/M/WS/root и все members; zero next admission до verified R |
| FI-09 | После A ACK, до R | Кандидат COMMITTED, не success без complete proof | Итоговый | HOLD до verified R | ACK string сравнивается с actual graph; forged ACK без graph = FAIL |
| FI-10 | Во время R либо после R COMMIT до ACK | A outcome сохраняется по исходному proof; R outcome UNKNOWN | От исходного A | HOLD до Ack/pending readback; A не повторять | ProofAck и pending clear согласованны; partial ack = FAIL, недоступность сохраняет HOLD |
| FI-11 | После R ACK, повторное existing-only открытие | Исходный COMMITTED или NOT_COMMITTED outcome повторяется | Без нового изменения | Снятие HOLD только по действительному Ack+proof | Profile/anchor/root/head/ack continuity; zero duplicate job/event/receipt |
| FI-12 | Два child processes, разные valid keys одной active projection | Один ADMIT COMMITTED; другой BUSY/ACTIVE conflict/NOT_ATTEMPTED, без A changes | Только один HELD | Pending winner блокирует конкурента; loser не ретраится скрыто | DB unique/CAS constraints, losing member absence; ровно один current job/receipt/slot |
| FI-13 | Stale expected revision/head | CAS_CONFLICT до A; NOT_COMMITTED лишь после qualified absence | Не меняется | Чужой pending не очищается | CAS rowcount/current revision/root, ноль новых event/job/error/outbox rows |
| FI-14 | Повтор точного admission key/request | REUSED original COMMITTED receipt | Без нового acquisition; старый terminal replay не трогает новый slot | Read-only replay; не refresh grant/execution | Exact canonical bytes/receipt/job history, no counter/revision increase |
| FI-15 | Corrupt DB bytes/indices/canonical BLOB или недоступность | UNKNOWN + STORE_CORRUPT/UNAVAILABLE | Нельзя авторитетно объявить свободным | HOLD; no retry/new DB/repair | integrity/FK/canonical/graph checks и error trace; corrupted snapshot не AbsenceProof |
| FI-16 | Прежняя DB отсутствует / root или file identity заменены | UNKNOWN + STORE_MISSING/IDENTITY_MISMATCH | Не считать пустым | HOLD; OpenExisting не создаёт файл | Anchor/physical identity/current-root check, refusal; новый DB file = FAIL |
| FI-17 | Старый M ID с другими intent/WS bytes | MUTATION_ID_CONFLICT; original outcome не меняется | Без изменения | Не затрагивать прежний pending; no overwrite | Original canonical intent comparison, zero new members/projections |
| FI-18 | Известная stale copy, lower watermark/head, чужой profile/version | UNKNOWN/STALE_COPY или VERSION_MISMATCH | Не восстанавливать как free | HOLD/BLOCKED qualification | Parent known anchor/head/watermark + custody; никакой rebasing epoch для сокрытия restore |
| FI-19 | SQLITE_BUSY/LOCKED до BEGIN и на control/apply boundary | NOT_ATTEMPTED только для не начатого вызова; M UNKNOWN до proof при любом сомнении | Прежний/неизвестный по phase | Bounded 250ms, без hidden retries; чужой HOLD сохраняется | Exact SQLite code/phase + qualified snapshot, не exception-type rollback |
| FI-20 | SQLITE_FULL, permission/IOERR, interrupted transaction | UNKNOWN до inspection, возможен proven NOT_COMMITTED | Не объявлять свободным без evidence | HOLD при outage; no external fallback | Error/phase + full graph/absence checks после разрешённого восстановления доступа |
| FI-21 | Model outbox/reservation commit crash | UNKNOWN; затем same token/reservation COMMITTED или proven absent | Нормальная slot семантика | Никаких executor calls, нового token или сброса счётчика | Один A marker связывает job/event/outbox/reservation, duplicate/reopen не меняет identities/calls_used |
| FI-22 | Terminal A и historical replay при новом active job | COMMITTED только по terminal proof; old replay REUSED | Release в A; новый slot возможен только после R | Lost ACK не открывает admission | Terminal proof, old immutable receipt, same M resolution, exact slot index |

## Статусы и полнота

**PASS** case: фактический checkpoint действительно достигнут, interruption/data fault выполнен в заявленном envelope, outcome соответствует qualified evidence, graph/slot/HOLD/replay и no-executor assertions проверены, raw logs/counts/exits сохранены. Допустимые COMMITTED/NOT_COMMITTED исходы FI-07 не означают «принимаем любой результат»: соответствующее полное proof обязательно.

**FAIL**: partial authoritative set, ложный NOT_COMMITTED/empty database, второй admission/effect, stale write, освобождение slot/HOLD без proof, timeout/превышение caps или неверная identity. **BLOCKED**: нет owner grant/root/host/instrumentation/qualified evidence; указать конкретную причину. **NOT_RUN**: boundary реально не исполнялся; нельзя считать его PASS из соседнего теста.

P/A/R варианты FI-02/03/06/07/08/10 явно параметризуются и получают разные case IDs. В control P/unknown-R application root не меняется; это не новый A. Parent/coordinator crash, power-loss, storage hardware cache и полноценный restore — OUT_OF_SCOPE / NOT_RUN. Известная подмена проверяется как отказ, не как успешное restore recovery.

Стандартный sqlite3 trace/handshake может доказать только окно вокруг COMMIT, не точную внутреннюю VFS точку. Первый lab должен честно назвать FI-07 coverage COMMIT_RACE_WINDOW. Если независимая проверка требует доказательства kill внутри engine, этот subcase BLOCKED_INSTRUMENTATION/NOT_RUN до отдельного разрешения; не писать «mid-fsync PASS». Разрешение на дополнительное instrumentation или зависимости сейчас отсутствует.

## RESOLVE-01 — DQ-F01/F02 обязательные additions к FI-oracles

FI-01–FI-22 выше сохраняются; следующие fixture/oracle subcases обязательны как contract conformance, а будущие native executions всех этих subcases остаются NOT_RUN:

| FI | Exact document vectors | Обязательный oracle |
|---|---|---|
| FI-01–FI-04, FI-11 | F01-P01–P03, F01-N01–N04 | Ticket bundle/custody/coordinator/identity — conjunctive prerequisites. Registry PREPARED/staged != A applied. Missing ticket/coordinator/DB/identity continuity запрещает NOT_COMMITTED |
| FI-05–FI-09, FI-15 | F01-N05/N06; F02-P01–P03 | Writer kill/COMMIT call/ACK без complete native proof дают UNKNOWN. Partial committed member при missing marker — не absence. После qualified proof A может стать COMMITTED при pending R |
| FI-10–FI-11 | F02-P04–P07, F02-N01–N07 | pre-R G; Ack=G+1; post-R G+1; exact Ack/ticket/M/head binding. R unknown сохраняет barrier, не понижает known A. R absence допускает только same-M/exact-Ack R retry по fresh proof predicate |
| FI-16–FI-18 | F01-N01–N04; F02-N02/N05/N06 | Не reconstruct anchor/ticket после app crash; чужой Ack/head/identity/version не лечится reset/init/новой M |
| FI-21–FI-22 | F02-P05/P06/P07; F02-N01–N07 | Ноль новых A/effect/token/slot release при unknown R; только qualified post-R readback разрешает новую application M |

Native v2 catalogue содержит exact typed preimages/hashes всех используемых refs. namespace_barrier и uncertainty_hold различаются: PREPARED+qualified PrepareEvidence резервирует namespace для одной M и разрешает A той же M; unknown phase запрещает небезопасное продолжение. Post-R terminal state/slot в SQLite недостаточны, если expected Ack/control readback ещё неизвестен.

## RESOLVE-01 — DQ-F03 наблюдаемые и недоступные точки

| Subcase | Что можно наблюдать | Что НЕ доказано | PASS / NOT_RUN / STOP oracle |
|---|---|---|---|
| CW-01 COMMIT_INVOCATION_OBSERVED | Qualified SQLite trace event COMMIT для exact connection/phase/M либо подтверждённый post-call COMMIT_RETURNED; простой BEFORE_COMMIT_CALL доказывает только REQUESTED, не invocation | Ни VFS/fsync, ни A outcome; return также не proof | PASS invocation только с таким trace/return evidence. Если есть лишь BEFORE_CALL — REQUESTED_ONLY; target invocation NOT_RUN/BLOCKED_CHECKPOINT |
| CW-02 ACK_RECEIVED / ACK_LOST | Coordinator действительно получил exact phase/M ACK либо **не получил** его; сравнить timestamp/trace sequence, не гадать по child exit | Неполученный ACK не доказывает child failure/rollback; полученный ACK не заменяет graph proof | Потерю ACK заявлять только если target case не получил ACK. Если ACK уже получен — классифицировать AFTER_ACK, не записывать ACK_LOST PASS |
| CW-03 KILL_SOFTWARE_WINDOW | Controlled owned process termination после достигнутого window checkpoint, kill request и exit подтверждены | Kill мог попасть до/во время/после native COMMIT; точная инструкция не известна | Для FI-07 proposed scope = COMMIT_RACE_WINDOW. Проверить actual trace и qualified reopen A proof. Partial state, duplicate A или false absence — FAIL; target checkpoint не достигнут — NOT_RUN, не PASS |
| CW-04 INTERNAL_VFS_FSYNC | При стандартном sqlite3 нет доступного квалифицированного checkpoint для нужной внутренней точки | Нельзя выводить её достижение из trace callback, sleep, kill timing или COMMIT_ENTERED | Для первого lab NOT_RUN / BLOCKED_INSTRUMENTATION, никогда агрегированный native-internal PASS. Нужда в VFS hooks/dependencies — STOP и отдельное разрешение |
| CW-05 POWER_LOSS | Ничего: питание в этом envelope не отключается | Process kill не моделирует power-loss/hardware cache loss | OUT_OF_SCOPE / NOT_RUN; не создавать power-loss PASS или запускать такой fault |

Event taxonomy фиксируется заранее: BEFORE_COMMIT_CALL=REQUESTED_ONLY; SQLITE_TRACE_COMMIT=STATEMENT_INVOCATION_OBSERVED; COMMIT_RETURNED=CALL_RETURN_OBSERVED; ACK_RECEIVED=COORDINATOR_ACK_OBSERVED. Ни одно событие не подменяет другое. Kill до trace/return может быть подтверждённым software-window kill, но не наблюдаемым вызовом COMMIT; классифицировать фактическую позицию как BEFORE_CALL_OR_UNOBSERVED, не добавлять отсутствующий checkpoint.

Первый lab может получить scoped qualification для честно наблюдаемого race window только после native разрешений и фактических тестов, с внутренними точками и power loss явно NOT_RUN. Нельзя изменить название достигнутого checkpoint после прогона, чтобы скрыть недостижение requested case; результат/coverage/limitations записываются отдельно. Отсутствие подходящего native instrumentation не блокирует уже принятый PURE baseline и не разрешает расширить DQ-01.

STOP: отсутствует ticket/continuity/custody; неполная closure/proof; неправильный Ack/generation/head; нет фактического target checkpoint; требуется неизвестный VFS hook/engine modification; или требуется whole-application recovery/power loss. Никаких SQLite/process tests в текущем DOCS_ONLY задании; arithmetic case checks не FI PASS.
