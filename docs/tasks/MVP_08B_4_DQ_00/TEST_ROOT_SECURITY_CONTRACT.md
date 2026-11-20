# DQ-01 — Test Root Security Contract

Дата: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / CONTRACT_PREPARATION**.

Base: `162a5ff109358625c25ff92402064d214fa50bc0`; tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`. OD4-01–OD4-07 — **OWNER_APPROVED_CONTRACT_ONLY** в пределах OWNER_APPROVAL.md. Технические схемы, настройки, лимиты и будущий task в этом пакете — **PROPOSAL / NOT_APPROVED**, пока не прошли независимую проверку и требуемое согласование. Native writes, SQLite connections/files, crash processes и реализация сейчас не разрешены.

**PROPOSAL / NOT_APPROVED.** Конкретный disposable root: **NOT_SELECTED / OWNER_APPROVAL_REQUIRED**. Никакой путь на компьютере владельца не назначен, доступ к Windows-хосту/диску F не предполагается. Текущая задача не создаёт root или DB и не разрешает native operations.

## Выбор и identity

Будущий grant должен назвать один абсолютный dedicated root, OS/user/filesystem и правило владения/очистки. Он новый и пустой либо содержит только собственный однозначно идентифицированный run; запрещены repository root, home/projects/Downloads, production/S3 paths, пользовательские проекты, shared/network/removable roots и system directories. Нет fallback на cwd/temp/F-диск при отсутствии выбранного root.

Перед InitializeNew проверить origin/parent/root identities по квалифицированным handles, отсутствие links/reparse components и ordinary-user permissions; не запрашивать admin. Имена DB/контрольных файлов фиксированы в manifest. RootAnchor связывает run/store/namespace/profile и физические identities. Путь — locator, не identity. OpenExisting не создаёт root/database/manifest и не мигрирует их.

Лабораторное permission envelope защищает от случайного выхода из scope и выявляемой подмены, но не заявляет tamper-proof защиту от злонамеренного процесса того же пользователя/admin. Потеря exclusive controlled custody, handle identity или parent watermark — HOLD/BLOCKED, не absence proof.

## Предлагаемые caps, ещё не утверждённые

| Ресурс | PROPOSAL | Проверка / превышение |
|---|---|---|
| Main DB | 32 MiB при 4096-byte pages / 8192 max pages | PRAGMA readback + actual size; SQLITE_FULL test, не raise cap |
| Весь run root | 128 MiB | До/после операций учитывать DB/journal/control/evidence/log files; overflow RESOURCE_LIMIT/HOLD |
| Отдельный raw payload | 1 MiB | До staging/SQL bind; no unbounded read |
| Native canonical record | 4 MiB | До parsing/staging/evidence; payload hex overhead учитывается |
| Run-owned regular files | 256 | Только allowlisted basenames/patterns; journal временно входит в cap |
| Jobs / application commits | 16 jobs / 128 A commits | Счётчики persistent, reopen не сбрасывает |
| Control transactions | 512 total P/R mutations | Отдельный budget, не бесконечные recovery loops |
| Outbox / read records | 32 / 128, максимум 3 calls/checkpoint | Это data storage model, executor/remote read запрещены |
| Processes | 1 coordinator + до 2 owned children | Точный процесс identity/handle и token от собственного spawn, не произвольный PID |
| Case child wait/kill/reopen | До 5 s на child stage, до 2 s на handshake | Timeout = FAIL/BLOCKED по причине, не PASS и не увеличение лимита |
| Native test command | До 60 s | External watchdog; child cleanup только собственных processes |
| Весь acceptance run | До 300 s | При исчерпании STOP, оставшиеся NOT_RUN, никакого скрытого parallel rerun |
| Case matrix repetition | До 3 COMMIT race-window trials/case | Недостигнутую internal point не считать выполненной |

SQLite journal_size_limit — retention setting, не hard active-journal cap; общий root budget включает все companions. Лимиты должны быть явно согласованы вместе с root/process grant, не активируются этой таблицей.

## Файловая поверхность и доступ

Предложенные basenames: `dq01.sqlite3`, `dq01.sqlite3-journal`, `root-anchor.json`, `run-plan.json`, `ticket-<uuid>.json`, `evidence/`, `logs/`; WAL/SHM не разрешены в первом DELETE profile. Непредусмотренный companion, absolute/UNC/device/traversal name, separator в object ID или неожиданное nested directory — отказ. Run manifest перечисляет собственные created files и their identities/hash/role; журнал может создаваться SQLite, но его происхождение/boundary учитывается.

Не доверять `resolve/check/reopen` как закрытию TOCTOU. Открывать/проверять root/object по qualified anchored handles; не следовать symlink/junction/reparse points при доступе, enumeration или cleanup. Python open mocks не наблюдают все C-level file operations SQLite: одного monkeypatch недостаточно для native path qualification. Нужны фактические file/capability observations либо явно ограниченная OS isolation; недоступность нужного evidence — BLOCKED_SECURITY_QUALIFICATION, а не выдуманный native PASS. Для будущего Linux candidate нужны реальные проверяемые primitive/capability tests; Windows требует отдельного handle/ACL/reparse profile и остаётся WINDOWS_NOT_RUN. Не имитировать эти гарантии одной строковой проверкой пути.

## RootGrant ABI metadata — не сертификат разрешения

Proposed boundary input `RootGrant` — закрытая metadata структура: `{grant_reference:Text, approved_task_commit:GitCommit40, root_absolute_locator:Text, profile_ref:Ref<QualificationProfile>, run_id:UUID, allow_initialize:Bool, allow_existing_rw:Bool, allow_owned_process_kill:Bool, allow_cleanup:Bool, limits:RootLimits}`. GitCommit40 = 40 lowercase hex; RootLimits — закрытый object `{db_bytes:33554432,root_bytes:134217728,payload_bytes:1048576,record_bytes:4194304,files:256,jobs:16,application_commits:128,control_transactions:512,outbox_records:32,read_records:128,reads_per_checkpoint:3,coordinators:1,children:2,child_stage_ms:5000,handshake_ms:2000,command_ms:60000,total_ms:300000,commit_race_trials:3}`; все числа proposal, не runtime defaults. Значения allow_* и root сейчас NOT_APPROVED/NOT_SELECTED; runtime не подставляет true/путь по умолчанию. Metadata/hash не создают authority: grant_reference должен соответствовать отдельному фактическому решению владельца и exact будущему task. Не использовать RootGrant как production/native permit.

## Операции и отказы

| Ситуация | Обязательное поведение |
|---|---|
| Access denied/read-only root | Никакого другого root/DB; STORE_UNAVAILABLE/HOLD для unknown M; no admin fallback |
| Нехватка места/SQLITE_FULL | Не удалять чужие файлы/не расширять cap; outcome доказывается после квалифицированного reopen, иначе UNKNOWN |
| DB/root identity поменялась | Немедленный HOLD; запрет new initialize/epoch bump и NOT_COMMITTED proof |
| Неожиданный link/reparse/unsafe path | Отказ до native operation; cleanup также не следует link |
| Неполные root-anchor/ticket/evidence bytes | Не считать authority/proof; run BLOCKED, не «восстановить по содержимому БД» |
| Native diagnostic не удалось записать | Сохранить uncertainty/coordinator ticket; stdout/error не превращает COMMIT в rollback |
| Child hung/crashed | Только owned process handle/token в утверждённом run; kill ограничен grant, не process-name/PID search |
| Coordinator lost / custody неизвестна | Вне первого envelope: STOP/BLOCKED; нельзя самовольно resume по уцелевшему path |

RootAnchor/run-plan/tickets должны быть полностью подготовлены/read back до writer unsafe boundary. На процесс-kill cases coordinator сохраняет ожидаемые canonical bytes/digests в живой памяти и контролируемых artifacts; это не nonrollbackable witness против произвольного restore.

## Очистка

Только после закрытия connections/own children и сохранения review evidence, по отдельному разрешённому cleanup rule того же grant. Проверить root/run identity и каждый собственный файл; неизвестные identities/links — STOP без recursive deletion. Никаких wildcard cleanup вне manifest/root, следования link, удаления родительских каталогов или попыток починить чужую базу. При UNKNOWN нельзя удалять последнюю recovery/evidence копию ради успешного завершения теста.

Новая реализация не должна менять production storage permissions, пользовательские материалы, Asset Library или main. Никакой установки пакетов, запуска моделей, API, renderer или Windows-specific implementation в первом Linux proposal.
