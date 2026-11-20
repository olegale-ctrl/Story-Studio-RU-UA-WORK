# DQ-00 — Owner Decisions and Technical Review Package

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

## A. Уже утверждено — не запрашивать повторно

OD4-01–OD4-07 имеют статус OWNER_APPROVED_CONTRACT_ONLY в точной формулировке [OWNER_APPROVAL.md](OWNER_APPROVAL.md). C/Split Qualification, storage-only first, stdlib SQLite candidate, отдельный native profile, isolated root, Windows separate matrix, process-kill envelope и отдельная implementation authorization уже выбраны. Этот пакет не переоткрывает их и не меняет G1–G6.

## B. Требует технической независимой проверки

Все ниже **PROPOSAL / NOT_APPROVED**, а не недостающее повторное одобрение OD4.

| ID / предмет review | Рекомендованная точная трактовка | Критерий проверки / последствия отказа |
|---|---|---|
| TB-01: P/A/R atomicity и pending | Отдельный Prepare до application unsafe boundary, atomic Apply, proof-bound Ack; staged bytes отдельно от A-members | Проверить все windows и доказуемость absence. Если сам ACK/prepare outcome не разрешён — HOLD, никакого inferred rollback |
| TB-02: SQLite settings/versions | DQ-SQLITE-DELETE-FULL-1, explicit IMMEDIATE, bounded busy, readback; точные фактические SQLite/runtime ещё нужны | Проверить support/semantics driver по матрице; WAL/FULL не квалифицированы фактом выбора. Mismatch → BLOCKED profile, не auto-tune/install |
| TB-03: Native records/encoding/schema | DQ.LAB v1, отдельные domain/scope, closed DTO, acyclic typed closure, staged-vs-committed distinction | Проверить preimages/roles/root exclusions/tickets/proofs/SQL constraints. Не исправлять schema в implementation без согласованной revision |
| TB-04: Mutation recovery / stale-copy limits | Writer-kill при live coordinator; exact tickets + retained DB registry; custody обязательна для absence | Проверить continuity/watermark/root substitution cases. General restore/coordinator crash/malicious same-account rollback не заявлять квалифицированными |
| TB-05: Negative oracles и FI-07 coverage | FI-01–FI-22 с P/A/R subcases; FI-07 только честно зафиксированное COMMIT_RACE_WINDOW | Если требуется внутренний SQLite/VFS checkpoint, subcase BLOCKED_INSTRUMENTATION до отдельной поддержки; не выдумывать mid-flush PASS |
| TB-06: Windows assumptions / compatibility | Первый implementation proposal Linux local; Windows 10/11 NTFS отдельные неисполненные строки | Проверить отсутствие POSIX→Windows promotion; native lock/fencing/reparse qualification остаётся WINDOWS_NOT_RUN |
| TB-07: Stricter first-lab retry policy | После final NOT_COMMITTED Ack old M read-only; новый storage case/new M требует отдельной допустимой операции | Проверить, что это не drop-in PURE adapter и не ослабляет unknown safety; direct integration запрещена, будущий bridge требует отдельного contract review |

Техническое возражение к proposal исправляется новым согласованным contract revision до кода. READY_FOR_INDEPENDENT_CONTRACT_REVIEW означает наличие reviewable package, не прохождение этого review.

## C. Требует нового конкретного разрешения владельца

| ID / вопрос | Рекомендация | Что сейчас не утверждено / последствия |
|---|---|---|
| CP-01: утвердить ли exact 10-path allowlist и отдельное начало DQ-01 programming? | Только список и branch/base из DQ_01_IMPLEMENTATION_TASK.md после B review | Пока нет implementation authorization; нельзя начинать по этому документу |
| CP-02: какой exact disposable root/host/user/FS предоставить? | Новый выделенный non-production Linux local root обычного пользователя, без admin; путь сообщает владелец | Значение NOT_SELECTED; не угадывать Windows/F/home/temp. Без него native writes BLOCKED |
| CP-03: разрешить ли bounded init/existing-rw/recovery writes/evidence/cleanup в этом root? | Только named files и собственные data; cleanup по manifest после evidence retention, не при unresolved M | Сейчас нет native write/DB creation/cleanup grant; OP metadata не право на execution |
| CP-04: разрешить ли собственные writer/contender processes и их controlled termination? | 1 coordinator + до 2 children, shell=False/owned identity/handles, child-only kill; coordinator survives | Сейчас spawn/kill crash tests запрещены. Произвольные PIDs/process-name kill недопустимы |
| CP-05: утвердить ли proposed caps/fault limits и точную runtime/config строку для реализации? | 32MiB DB/128MiB root/256 files; child5s/handshake2s; command60s/total300s; native profile после измерений и review | Все цифры PROPOSAL. Нет права менять bounds для PASS; actual SQLite/source-id/FS фиксируются до cases |

Ни один CP ответ не считается данным по истечении времени или факту выбора SQLite. Закрепить CP grants в отдельном задании с exact implementation base/tree и DQ-00 publication commit/tree. Не расширять их до реального executor, Windows implementation, production roots/storage, provider/media/Library/save, расходов, merge или release.

## Что можно решать сейчас

Независимый reviewer может проверить этот proposal, schema/phase consistency, absence/commit/custody rules и negative oracles без SQLite execution. Владелец затем даёт конкретные CP grants либо возвращает замечания. Сам Codex не утверждает TB/CP и не запускает DQ-01.

Открытые параметры: actual SQLite/source-id/compile options/OS/FS; approved root; permission metadata; native code allowlist/bounds; принятие race-window qualification scope. Это явно обозначенные prerequisites, не молчаливые значения.

**STOP.** Дальнейшая implementation требует независимой проверки ChatGPT и отдельного разрешения владельца.
