# MVP-08B.4 — Owner Decision Package

Дата записи: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / ACCEPTANCE_RECORD / ARCHITECTURE_PREPARATION**.

Точный исходный commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`. Запись приёмки ниже относится только к MVP-08B.3. Все новые решения MVP-08B.4 имеют статус **PROPOSAL / NOT_APPROVED**. Разрешения на реализацию, merge, release или production этим пакетом не создаются.

**PROPOSAL / NOT_APPROVED.** Ниже только новые решения следующего этапа. G1–G6, принятые F-08B3-01/02 и существующие PURE-контракты не переоткрываются.

## Компактное предложение

Рекомендация Codex: **C — Split Qualification**. Предлагаемый scope MVP-08B.4 — серия отдельных квалификационных пакетов, а не реализация всей локальной production pipeline. Первый исполняемый инкремент после отдельного разрешения: **MVP-08B.4-DQ-01 — Durable Storage Qualification Lab**, один выбранный storage-кандидат, synthetic data, atomicity и controlled process-restart tests, без executor и real media.

SQLite можно рекомендовать первым кандидатом, но выбор engine/settings не принят. Native proof namespace/identity должен быть отдельно согласован: PURE proof с fake-only qualification нельзя выдавать за durable evidence. Сначала Q1, затем отдельно разрешённая работа в точном test root; ни одна строка этого документа не запускает реализацию.

## Необходимые решения

| ID / точный вопрос владельцу | Альтернативы | Рекомендация Codex | Почему блокирует начало / проверяемый результат | Статус |
|---|---|---|---|---|
| OD4-01: какой вариант A/B/C и первый scope выбрать? | A storage-first; B fake-interface-first; C split | C, первым storage lab без executor | Без выбора нельзя определить входные gates/allowlist; задача должна прямо назвать storage-only и deferred layers | OPEN / PROPOSAL / NOT_APPROVED |
| OD4-02: какой storage-кандидат и целевой platform profile разрешить? | SQLite stdlib; другой обоснованный local transactional store; отложить | Сравнить SQLite как единственный первый lab-кандидат, exact driver/runtime/OS/FS/settings определить в task | Должен быть один измеримый fault envelope, без тихой смены engine/config или обещаний power-loss | OPEN / PROPOSAL / NOT_APPROVED |
| OD4-03: разрешить ли отдельную подготовку/заморозку native evidence/data compatibility profile? | Отдельный versioned profile; lab только generic opaque test-data без подключения controller; отложить | Отдельный native qualification boundary; PURE bytes хранить как test-data, не переписывая G1–G6 | До adapter integration требуется Q1; native COMMITTED/absence authority нельзя выдумать из fake proof | OPEN / PROPOSAL / NOT_APPROVED |
| OD4-04: какой тестовый root и какие bounded native операции разрешены? | Названный изолированный disposable root с обычными user rights; другой явно ограниченный sandbox; нет разрешения | Только новый owner-approved non-production root, synthetic records, bounded processes/crash probes; никаких пользовательских данных | Нужны root identity/ACL/path/cleanup/quota limits, разрешённые process kills только своих test processes; filesystem/OS effects сейчас не разрешены | OPEN / PROPOSAL / NOT_APPROVED |
| OD4-05: какая Windows-матрица и хост доступны для отдельной Q4/Q7 qualification? | Фактические Windows 10 и 11; утверждённый subset с явным ограничением; отложить | Указать реальные OS builds/CPU/user/NTFS и расположение test root; при отсутствии — WINDOWS_NOT_RUN | Облачный Linux или известный диск F пользователя не означает подключённый Windows executor/доступ к его диску | OPEN / PROPOSAL / NOT_APPROVED |
| OD4-06: какой crash/restore и durability envelope является предметом приёмки? | Process-kill/reopen only; дополнительно отдельный restore/power-loss profile; отложить | Первый lab: точные process interruption cases; unsupported power-loss/FS restore оставить NOT_RUN до отдельной qualification | Нельзя превратить отсутствующий hardware test в PASS; нужны обязательные negative cases и поведение HOLD | OPEN / PROPOSAL / NOT_APPROVED |
| OD4-07: какие exact base/tree/allowlist/limits и независимый reviewer закреплены в будущем implementation task? | Новый отдельный task после решений; продолжение без freeze не допускается | Зафиксировать точный accepted baseline, документационные SHA, пути, commands, 60s/300s или иные явно выбранные bounded limits, STOP/review | Без отдельной implementation authorization и Q1 entry review работы не начинаются; эта документационная ветка не разрешение | OPEN / PROPOSAL / NOT_APPROVED |

OD4-xx — локальные идентификаторы этого нового пакета, не автоматическое утверждение старых OD01–OD08 или EC01–EC10. Это решения владельца, не предвыбранные ответы. Рекомендация SQLite/C не является approval.

## Windows tests, которые нельзя заменить pure/Linux PASS

Фактические normal-user/no-admin launch; owner lock contention; killed/hung owner and worker; stale controller/worker after restart; qualified lock/death proof; fence/boot/clock rollback boundaries; NTFS root identity, symlink/junction/reparse substitution, traversal/UNC/device path, ACL/read-only/disk-full/partial-write/cleanup behavior. Конкретный поддерживаемый subset должен быть назван владельцем и затем реально проверен; в этом пакете **WINDOWS_NOT_RUN**.

## Новые разрешения, которых сейчас нет

Implementation/code changes для отдельного выбранного scope; native local storage/filesystem writes в названном root; bounded собственные worker processes и контролируемые crash probes; доступ к Windows test host при Q4/Q7; утверждённые native contracts и точный allowlist. Никаких admin, production roots/storage/S3, real providers/models/TTS/LLM/renderer, media ingestion, Asset Library/save, расходов, merge/release. Такие полномочия не следуют из одобрения storage lab.

## Критические риски и STOP

STOP при несовместимости с immutable identity/active slot/COMPLETED, потере M/namespace после restart, невозможности доказать COMMIT outcome, попытке повторного эффекта после lost ACK, неизвестной clock/owner authority, небезопасном root/reparse/TOCTOU, частичном result/evidence, неизвестных правах или необходимости выйти за разрешённый scope. Техническая невозможность удовлетворить обязательный контракт — BLOCKED_CONTRACT; отсутствие платформы/доступа — BLOCKED_ENVIRONMENT/NOT_RUN, а не разрешение ослабить проверку.

Владелец может выбрать вариант и заказать отдельную preparation/implementation задачу. **Ответа владельца здесь нет; реализация MVP-08B.4 не разрешена.**
