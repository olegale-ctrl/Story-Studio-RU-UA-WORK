# MVP-08B.4-ARCH-00 — Architecture Boundary

Дата записи: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / ACCEPTANCE_RECORD / ARCHITECTURE_PREPARATION**.

Точный исходный commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`. Запись приёмки ниже относится только к MVP-08B.3. Все новые решения MVP-08B.4 имеют статус **PROPOSAL / NOT_APPROVED**. Разрешения на реализацию, merge, release или production этим пакетом не создаются.

## Цель и статус

**PROPOSAL / NOT_APPROVED.** Исследовать переход от принятой pure test model к ограниченным локальным infrastructure adapters. Это направление анализа и материал для решения владельца; никакой адаптер, новый native-контракт или выбор СУБД не утверждается.

Исходные инварианты: [accepted baseline](../MVP_08B_3_ACCEPTANCE/ACCEPTED_BASELINE.md). Варианты этапов: [INCREMENT_OPTIONS.md](INCREMENT_OPTIONS.md); условия квалификации: [QUALIFICATION_GATES.md](QUALIFICATION_GATES.md).

## Граница PURE и инфраструктуры

Pure controller остаётся потребителем явно инъецируемых ports. Runtime database, file handles, process ownership, OS clocks и physical executor принадлежат отдельному infrastructure boundary. Не добавлять скрытые singleton/store/retry loops или прямой вызов renderer из controller. Не строить универсальный DAG.

У текущих PURE proof records фиксированы fake-only scope/qualification. Хранить их исходные canonical bytes как синтетические тестовые данные можно предложить для storage lab. Выдавать native COMMIT за FAKE_STORE_READ_ONLY_EVIDENCE или synthetic permit за execution permission нельзя. Новый native evidence namespace, версии/identity/authority и отображение на port semantics требуют отдельного согласования Q1. Это не пересмотр G1–G6.

## A. Durable JobStore — кандидатная граница

PROPOSAL: ограниченное локальное хранилище с одной согласованной авторитетной транзакционной моделью. SQLite — кандидат для сравнения, **не утверждённый выбор**. Ни файл с JSON, ни сам SQLite, ни успешный COMMIT return сами по себе не доказывают требуемые гарантии.

Обязательства будущего адаптера:

- Неизменяемый request/receipt и стабильная store/namespace identity; атомарный JobRecord + revision/event + mutation registry + active-slot index. В ту же согласованную границу входят относящиеся к операции outbox, original receipt и read reservation; нельзя записать их отдельным неквалифицированным шагом после job update.
- Durable запись operation identity/ожидаемых связей до небезопасной COMMIT-границы. Невозможность восстановить неизвестную M после перезапуска оставляет HOLD, а не создаёт пустой store.
- COMMITTED только по полному совпадающему набору данных и marker в согласованном, проверенном snapshot. NOT_COMMITTED только по полному доказательству отсутствия marker **и всех M-linked members**. Ошибка/timeout/недоступность/частичный набор — UNKNOWN.
- CAS и уникальный HELD(store,project,purpose) должны обеспечиваться адаптером атомарно при конкурирующих процессах, а не Python check-then-write. Исторические receipts/keys не исчезают при terminal release.
- Restore, root replacement, stale copy и rollback поколения store должны обнаруживаться. Абсолютный путь не заменяет immutable store identity. Нельзя молча открыть новый пустой файл при пропаже прежнего.
- Квалификация привязывается к ОС, filesystem, driver/runtime, настройкам journal/sync, storage stack и fault model. Process kill не равен power loss; успешная Linux-проверка не доказывает Windows/NTFS.

Для первого лабораторного инкремента допустимо предложить test-only data и отсутствие executor. Контроллер не подключается к native store до Q1 и отдельного implementation scope. Никакого запуска SQLite в текущем задании.

## B. Windows execution boundary

PROPOSAL: один явно определённый process-owner и qualified межпроцессная блокировка. PID/mtime/TTL недостаточны как доказательство владельца или смерти процесса. Durable incarnation/fence монотонно меняется при квалифицированной передаче; актуальность проверяется на записи и на границе эффекта. Старая callback/worker команда не получает authority из receipt.

Нужны отдельные Windows 10/11 CPU-only проверки: обычный пользователь без администратора; одновременный запуск двух владельцев; зависший и аварийно завершённый owner/worker; crash между lock/claim/COMMIT/ACK; stale fence после restart; недоступный или read-only root; изменение clocks и boot epoch. Между boot epochs нельзя сравнить virtual ticks и насильно истечь lease. Новый clock/owner recovery protocol — отдельный кандидатный контракт, не автоматический перенос fake правил в ОС.

Для NTFS/reparse/symlinks требуется проверяемое открытие через закреплённую root/handle identity, обнаружение подмены root/links, безопасные относительные имена и верификация по открытому объекту. `resolve -> check -> reopen` не закрывает TOCTOU. Конкретные Windows API/ACL/locking primitives, поддерживаемые FS и containment ещё должны быть выбраны и квалифицированы. ACL ordinary-user test root — не production permissions; запрос admin-rights не является стандартным решением.

## C. Local execution adapter

PROPOSAL: один специализированный adapter с явным входом: точная immutable operation identity, original effect token и проверенный payload digest/scope; отдельный current fence и qualification context. Receipt — данные, не команда. Новый ABI сейчас не утверждается.

Будущий adapter обязан отличать: durable intent; известное принятие; неизвестный результат; подтверждённый result; settlement/cancel. Lost ACK восстанавливается lookup исходного токена в авторитетном ledger, а не новым submit. Повтор токена с другим payload — conflict. Worker death/timeout не доказывает отсутствия внешнего эффекта.

Нет общей exactly-once гарантии для произвольного неидемпотентного процесса. Нужны qualified idempotent acceptance/ledger либо общая транзакционная граница; иначе UNKNOWN и STOP/hold. Простой запуск subprocess и затем запись «успех» не соответствует принятой модели. Первый будущий adapter можно обсуждать только как synthetic/no-media испытание в изолированном test root, после отдельного разрешения на процессы и эффекты.

**На этом этапе не подключать TTS, LLM, видеогенераторы, FFmpeg/renderer, реальные модели или provider APIs.**

## D. Result and Asset boundary

PROPOSAL: отдельно фиксировать фактически использованные inputs/tool versions, source identities, content hash/length, completeness и validation evidence; недописанный файл не публикуется как результат. Hash подтверждает байты, но не происхождение, корректность, лицензию, научную достоверность или право использования.

Права должны быть документированы для intended use, voices/music/images и применимых attribution/territory/time/watermark условий; unknown rights не clearance. Привязка к будущей Asset Library требует собственного idempotent import/save receipt и разрешения. Наличие локального результата/пути/URL не является импортом, сохранением проекта или COMPLETED.

В storage lab нет real media result. Media/decoder/rights, Asset Library import, GUI attachment и save остаются отдельными будущими gates и не реализуются. Production/S3 storage не является зависимостью первого локального qualification lab и не разрешён.

## Условия входа в будущую реализацию

Нужны выбранный владельцем инкремент, отдельный implementation task с точными base/tree/allowlist, native evidence/data compatibility decision, test-root/process permissions и квалификационная матрица. Все эти новые решения сейчас OPEN / PROPOSAL / NOT_APPROVED. Невозможность сохранить PURE инварианты означает BLOCKED_CONTRACT; недостаток платформы — BLOCKED_ENVIRONMENT/NOT_RUN, не PASS.
