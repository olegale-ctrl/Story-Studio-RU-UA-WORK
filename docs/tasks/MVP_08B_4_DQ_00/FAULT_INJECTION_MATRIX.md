# DQ-01 — Fault-Injection Matrix

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
| FI-07 | COMMIT race window / process termination вокруг вызова COMMIT | UNKNOWN; после reopen допускается COMMITTED или NOT_COMMITTED только с соответствующим proof | Целиком прежний либо целиком новый | HOLD до R | Stage trace и полный исход; partial = FAIL. Software window не доказывает kill внутри конкретной SQLite/VFS flush-инструкции |
| FI-08 | A COMMIT физически произошёл, ACK не получен | UNKNOWN → COMMITTED по proof | Итоговый, но новый admission запрещён до R | HOLD, даже если terminal slot уже физически RELEASED | Exact marker/M/WS/root и все members; zero next admission до verified R |
| FI-09 | После A ACK, до R | Кандидат COMMITTED, не success без complete proof | Итоговый | HOLD до verified R | ACK string сравнивается с actual graph; forged ACK без graph = FAIL |
| FI-10 | Во время R либо после R COMMIT до ACK | M outcome определяется исходным proof; control outcome UNKNOWN | От исходного A | HOLD до Ack/pending readback; A не повторять | ProofAck и pending clear согласованны; partial ack = FAIL, недоступность сохраняет HOLD |
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
