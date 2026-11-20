# DQ-01 — SQLite Qualification Profile

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

**PROPOSAL / NOT_APPROVED.** OD4-02 выбирает stdlib sqlite3 как первый лабораторный кандидат, но не квалифицирует настройки. В этом задании sqlite3 не импортировался/не запускался, SQLite version не измерялась, connections и DB files не создавались.

## Предлагаемый первый профиль

**DQ-SQLITE-DELETE-FULL-1** — один proposed profile, local filesystem, process-kill/reopen, coordinator survives, no executor. Python 3.10.22 и 3.13.18 предлагаются как две отдельные матричные строки. Они известны по принятому PURE baseline, но **не подтверждают текущую native SQLite конфигурацию**.

SQLite exact version/source-id/compile-options сейчас **NOT_MEASURED / NOT_SELECTED**. Предлагается compatibility floor 3.35.0 без автоматического upgrade. После отдельного разрешения preflight фиксирует фактические engine/driver/runtime/build/FS значения; до write cases точная матричная строка должна быть закреплена и пройти технический review. Если установленная версия вне выбранного профиля — BLOCKED, не установка зависимостей и не молчаливое изменение floor.

| Параметр | Предложение первого lab | Обоснование | Альтернатива / последствия отказа |
|---|---|---|---|
| Driver | Python standard sqlite3, никаких сторонних wrappers | Меньше deployment переменных; exact Python/SQLite всё равно измеряются | Иной driver — новый profile/review, не автоматическая замена |
| Wrapper transaction control | Explicit SQL BEGIN IMMEDIATE/COMMIT/ROLLBACK; isolation_level=None. На Python с autocommit parameter — явно LEGACY_TRANSACTION_CONTROL, не зависеть от default | Одинаковая понятная граница на 3.10/3.13; не смешивать implicit context-manager commits | autocommit=False/DEFERRED — отдельная qualification; несовпадение readback BLOCKED |
| Transaction mode | BEGIN IMMEDIATE для P/A/R; bounded read snapshot для inspect | Early writer-lock contention; повторная проверка CAS/head внутри tx | BEGIN DEFERRED/EXCLUSIVE — иные contention/reader guarantees, не считать эквивалентом |
| journal_mode | DELETE; проверить returned value после initialization и при reopen | Первый lab без WAL/SHM lifecycle; rollback journal всё равно часть store custody | WAL — отдельная версия профиля с checkpoint/WAL/SHM tests; не fallback при отказе DELETE |
| synchronous | FULL, readback required | Более строгий кандидат для ordered writes; не доказательство power-loss durability | NORMAL/OFF меняют assumptions; mismatch BLOCKED, не «оптимизация» |
| foreign_keys | ON на каждом connection; foreign_key_check после reopen/proof | SQL-level relations плюс application invariants | OFF — FAIL profile; PRAGMA не заменяет canonical closure/CAS/slot checks |
| busy_timeout | 250 ms; явный connect timeout=0.25 s | Bounded contention; без endless retry | Другой timeout — явно согласовать; SQLITE_BUSY до tx не означает отсутствие чужого pending |
| Повтор SQL operations | 0 automatic transaction retries | Не дублировать неизвестную M; retry только после proof, тот же immutable intent | Hidden retry loop — FAIL; после окончательного NOT_COMMITTED старая M read-only; новая попытка — отдельная разрешённая новая M, не скрытый retry |
| page_size | 4096, только fresh initialization до schema; readback | Предсказуемый byte budget | Не менять существующий store ради совпадения; несовпадение BLOCKED |
| max_page_count | 8192 pages = 32 MiB основного файла при page_size 4096 | Лабораторный cap, не unlimited disk usage | SQLITE_FULL проверять как fault; journals/evidence отдельно ограничены root budget |
| journal_size_limit | 1048576 bytes как retention setting, не hard runtime cap | Не обещать, что большой active journal ограничен этим числом | Root monitoring/abort policy отдельно; превышение журнала нельзя скрывать PRAGMA |
| locking_mode | NORMAL; process-local connections | SQLite locks только для database transactions; не Windows owner lock | EXCLUSIVE меняет concurrency profile; не считать Q4 выполненным |
| read_uncommitted | OFF | Не строить proof по dirty/inconsistent visibility | Включение — FAIL выбранного proof profile |
| trusted_schema | OFF, если exact engine поддерживает и возвращает значение; отсутствие поддержки BLOCKED этого профиля | Не доверять database-defined executable schema behavior | Любое ослабление требует profile review; никаких arbitrary user SQL/extension loading |
| Extensions / ATTACH / user functions | Запрещены; фиксированный SQL, параметры значений отдельно | Lab не general SQL execution engine | Нужда в этих возможностях — STOP scope |
| temp_store | MEMORY, readback integer 2 | Минимизировать SQLite temp files вне approved root; не гарантировать это одним Python mock | FILE/default — другой security profile; native file access требует квалификационного evidence |
| mmap_size | 0, readback required | Убрать дополнительную memory-mapped I/O переменную первого lab | Неподдержанный/mismatched readback BLOCKED; не считать эквивалентом |
| cache_size | 512 pages при page_size 4096 | Бounded candidate cache configuration; это не жёсткая RAM guarantee | Другое значение — profile change, native memory failures fail closed |
| auto_vacuum | NONE, integer 0 на fresh init и reopen | Нет скрытых перемещений/maintenance profile; VACUUM/backup/restore не разрешены | Иное значение или попытка менять прежний DB — BLOCKED |
| user_version / schema cookie | user_version=1 для DQ layout; SQLite schema_version cookie только измерять/сравнивать с initialization evidence, не считать равным 1 | Разделить app schema version и внутренний SQLite counter | DDL/cookie drift после init — BLOCKED/CORRUPT, не автоматическая migration |
| WAL checkpoint pragmas | N/A, WAL запрещён в первом profile | Не публиковать фиктивное checkpoint evidence | При выборе WAL потребуется отдельная configuration/qualification |
| Connection ownership | Один connection только в создавшем его процессе/потоке; check_same_thread=True; не наследовать после fork | Исключить shared handles и неквалифицированные driver assumptions | Shared connection/fork inheritance — FAIL; child создаёт свой connection после spawn |
| Multi-process | Один coordinator + максимум два owned children (writer/contender), процессы не являются production owner | Реальная SQLite writer contention без claim native owner fencing | Больше actors/threads/native lock — другое разрешение и scope |
| Reopen | Existing-only URI mode=rw, без immutable=1/read-only обхода recovery | Missing DB не превращается в новую; hot journal recovery может писать и требует grant | mode=rwc fallback — FAIL; mode=ro может быть лишь отдельным forensic read без absence proof |
| Integrity | integrity_check и foreign_key_check, canonical hashes/closures, indices, binding/marker chain/root, M-completeness | Каждая проверка покрывает разные нарушения | 'ok' не доказывает отсутствие rollback/stale copy или все app invariants |

## Connection lifecycle

InitializeNew — единственное место установки persistent journal_mode/page_size/auto_vacuum/user_version и DDL. При OpenExisting сначала qualified root/existing-only rw, затем явно применяются выбранные **connection-local** guards/settings (включая foreign_keys, synchronous, busy_timeout, max_page_count, journal_size_limit, locking_mode, read_uncommitted, trusted_schema, temp_store, mmap_size, cache_size), затем readback и binding/schema validation до P/A/R. Нельзя предполагать, что connection-local limits сохранились после reopen. Persistent header settings при reopen только проверяются; несовпадение не ремонтируется их переустановкой. Exact approved DDL/constraints и schema cookie фиксируются до cases; эта версия app schema не равна внутреннему SQLite schema_version.

## Readback mapping и SQLITE_BUSY

Raw SQLite readback сохраняется в trace без переписывания. Canonical Config mapping v1 закрыт: synchronous integer 2 -> FULL; journal_mode exact string delete -> DELETE; locking_mode normal -> NORMAL; integer 0/1 для перечисленных boolean PRAGMA -> false/true; busy_timeout/page_size/max_page_count/journal_size_limit/mmap_size/cache_size остаются exact integers (canonical names busy_timeout_ms/page_size/max_page_count/journal_size_limit_bytes/mmap_size_bytes/cache_pages); temp_store integer 2 -> MEMORY; auto_vacuum integer 0 -> NONE. Иные значения — PROFILE_MISMATCH как HoldReason и VERSION_MISMATCH как ErrorCode (qualification BLOCKED), не normalization/fallback. 250 ms connect timeout передаётся как 0.25 s только в native driver API; canonical evidence хранит integer milliseconds, не float.

BUSY/LOCKED до успешного BEGIN: нет application write этого вызова, но неизвестный prepared/pending M не очищается. Native NOT_COMMITTED для application M возможен лишь после qualified AbsenceProof. BUSY/IOERR/FULL/permission/interrupt в P/A/R или при COMMIT: UNKNOWN соответствующей фазы до proof. Нельзя по sqlite exception type или connection.in_transaction объявить исход доказанным.

Rollback() может быть cleanup, но успешный rollback вызова не доказывает, что предшествующий COMMIT не состоялся. При connection error новый existing-only connection и qualified read нужны для resolution; повтор A без доказательства запрещён. Diagnostic outage сам не должен стереть HOLD или породить success.

## Обязательные evidence поля

Сохранить exact Python version/build, sqlite3 module/runtime details, SQLite runtime version/source-id/compile options, OS build/architecture, filesystem/root/DB identities, выбранные PRAGMA и **фактический readback каждого**, schema/profile canonical digest, process/run IDs, case/phase/timestamps как наблюдения, SQLite error codes/names (доступность отличается по Python), outcome proofs и raw logs. Никаких секретов/пользовательских материалов.

Profile должен быть одинаков до/после reopen; другая Python/SQLite строка — отдельный case-run и binding, не silent migration старого store. Если данные не удалось прочитать — NOT_MEASURED/BLOCKED, не предложенное значение, выданное за измеренное.

## Пределы платформ

Предлагаемый первый DQ-01 implementation profile — Linux local filesystem в заранее названном disposable root, **ещё не разрешённый**. Windows 10/11/NTFS — отдельные матричные строки WINDOWS_NOT_RUN; POSIX inode/permissions не являются Windows handle/ACL qualification. Network/cloud/S3/removable filesystem, malicious same-account tampering, full restore и power-loss вне первого profile.

DELETE/FULL — только техническое предложение. Qualification PASS потребует фактических results и независимой приёмки на exact profile; эта документация такого PASS не создаёт.
