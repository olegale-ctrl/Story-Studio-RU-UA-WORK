# G3.0 — решения владельца и границы следующего задания

Дата: 2026-11-17 (Europe/Kyiv). **READY_FOR_OWNER_REVIEW / DOCS ONLY.**

Approved main `7166902820731984ceb56d79275a70f83f665b23`, tree `504881fec0b293fa1eb0808f666e63cd30bf5c7c`. Investigated source PR #11 `6cfa7b4b535b0171ae2871b7e68e545b48ba332a`. Ни одна рекомендация ниже не объявляется принятой. Все новые choices имеют статус **PROPOSAL / PENDING OWNER DECISION**; таблица не создаёт полномочия сама по себе.

## Предлагаемые решения

| ID / статус | Конкретное решение | Рекомендация PROPOSAL | Альтернатива / последствия | Что будет разрешено только после отдельного решения |
|---|---|---|---|---|
| OD-G3-01 / PROPOSAL | Что считается ближайшим результатом G3? | Отдельный synthetic D1 baseline с четырьмя source files; назвать его тестом Evaluation/Projection→Synthetic Render, без заявления полной цепочки | Сразу проектировать Preview→Production Gate bridge: больше scope, новые interfaces и trust/rights requirements; это отдельный design task, source не готов | Точный будущий implementation task после independent audit; сейчас только docs |
| OD-G3-02 / PROPOSAL | Утвердить точные source paths/blobs для минимального baseline? | Только scripts/topic_to_video.py, examples/topic_d1_synthetic.json, tests/test_topic_to_video_d1.py и permit document, по [реестру](G3_0_FILE_REGISTRY.md) | Изменить состав — сначала новый registry/dependency review. Не merge/cherry-pick всего source/PR #11 | Перенос точных четырёх файлов в отдельную ветку от утверждённой актуальной базы с entry/tree checks и no-repeat G1/G2 |
| OD-G3-03 / PROPOSAL | Какой path threat model допустим для D1? | Ограничить тест полностью подконтрольным private local temporary parent; явно не обещать hostile concurrent-write safety | Заказать отдельное source hardening до переноса: POSIX symlink/Windows reparse/relative/dangling/output collision tests. Даже V07-like path checks сохраняют TOCTOU, абсолютная защита требует отдельного дизайна | Scope-limited synthetic runs либо отдельная исправляющая implementation ревизия; G3.0 не вносит исправления |
| OD-G3-04 / PROPOSAL | Менять ли workflow вместе с D1? | Нет: текущий main уже ставит FFmpeg и discovers новые tests на Python3.10/3.13. Source workflow DEFER | Отдельный минимальный CI-hardening change после review: permissions, credentials, versions/SHA logging/actions. Не связывать с upload автоматически | Только явно перечисленные CI-only изменения отдельной задачей; сейчас workflow immutable |
| OD-G3-05 / PROPOSAL | Нужны ли загружаемые CI артефакты и кто их читает? | Пока не upload: пройти synthetic tests и сохранить доступные CI logs. Local source tests удаляют временные MP4 | Если владелец хочет artifacts, заранее определить private/public scope, exact content allowlist (cards/evaluation/projects/MP4 отдельно), readers/fork PR policy, custody, срок хранения и удаление; сверить запрет публикации permit | Отдельный ограниченный evidence export, только после точного разрешения. Разрешение сборки не равно разрешению публикации |
| OD-G3-06 / PROPOSAL | Как проверяется Windows CPU-only? | Отдельный user-level synthetic run на выбранном Windows10/11 host, actual Python/FFmpeg/ffprobe/libass/fonts, fresh private path; Linux CI оставить отдельно | Пока Linux-only experimental baseline, с явным NOT_RUN для Windows; не заявлять Windows-ready | Только scoped synthetic Windows test на названном host. Не SCM/service/ACL/admin/native storage operations |
| OD-G3-07 / PROPOSAL | Нужен ли Storage S3 для первого synthetic MVP? | Нет, DEFER pure transaction/LAB modules и весь native track; прямой runtime graph D1 их не использует | Требовать protected persistence для реального production — новое архитектурное scope решение, отдельный S3 host/native project и gates; production до него заблокирован | Отдельный design/readiness task, не implicit storage implementation или production permissions |
| OD-G3-08 / PROPOSAL | Как проектировать полную Preview→Gate→Render цепочку? | Сначала отдельный contract-only task: входы/выходы, exact byte/value bindings, human approval/identity/intended use/freshness/revocation, closed failures, private evidence и non-bypass boundary | Смешать D1 permit с Production Gate нельзя; ограничиться synthetic baseline и отложить real production | Только новый PROPOSAL-контракт; реализация после следующего явного owner approval |
| OD-G3-09 / PROPOSAL | Переносить ли исторические docs/status/config из source? | DEFER193, EXCLUDE4 source snapshots. Читаемый source SHA сохраняет provenance без массового копирования | Точечное включение конкретного контракта/новой записи допустимо только по отдельному allowlist, с проверкой scope/status и ссылок | Новые узкие docs changes по фактическому результату. Source WORKLOG/README/ROADMAP не подменяют G3 acceptance |
| OD-G3-10 / PROPOSAL | Какая evidence достаточна для интеграционной приёмки? | Exact integrated commit/tree + target/full tests на Linux3.10/3.13; actual versions/counts/skips/exits; Windows отдельно; независимый review и решение владельца | Source target pass/старые отчёты/наличие MP4 alone не достаточны. MP4 binary determinism, OCR и production rights не выводить из brightness test | Техническая scoped acceptance будущего candidate, никогда автоматический merge/release/production grant |

## Не открываем заново и не расширяем

- Утверждённые G1/G2 и их51 entry остаются byte-identical; current main/tree — заданная база. Source общих runtime deps совпадает; повторный перенос не нужен.
- Creative eligibility/score/Projection DISPLAYABLE и Preview INPUT_COMPLETE не заменяют редакционное решение, права, научную проверку или Production Gate. Preview остаётся NOT_ASSESSED / permissions_granted=false.
- SyntheticRenderPermitV1 ограничен одной зарегистрированной fixture и SYNTHETIC_TEST_ONLY; exact digest не secret и не authentication. Не расширять его на real materials/коммерческие голоса/публикацию.
- Source документы с historical OWNER_APPROVED отражают только свой original scope. Этот аудит не выбирает новые trust/storage/security policies и не утверждает любые старые предложения скопом.
- Source S3/PURE_ONLY не разрешает service install, accounts/ACL/DPAPI, protected writer или NTFS durability claims; отдельная VM/admin/runtime/observer qualification остаётся закрытым треком.
- Merge, release, main updates, production permissions и G3 implementation не выполняются в G3.0. Принятие аудита само по себе их не разрешает.

## Что уже известно и чего ещё нет

| Вопрос | Проверенный факт | Открытая часть |
|---|---|---|
| Доступен ли source? | Exact source commit/tree и все201 remaining Git entries прочитаны | Ничего не восстанавливалось по догадкам |
| Совпадает ли актуальный main? | В начале аудита origin/main = approved SHA/tree | Любая последующая смена базы требует нового compare перед implementation, не молчаливого rebase утверждённых blobs |
| Минимальный source D1 работает? | Target source tests Linux3.10.22/3.13.18:3/3, no skip, exit0 на каждой | Это не execution exact future integration tree. Его ещё нет |
| Editor Preview подключён к D1? | Нет imports/calls; schemas различаются, duplicate evaluation path | Нужны purpose/authority/binding решения для bridge; сам converter пока не утверждён |
| Общий Production Gate существует? | Не найден в actual call graph; synthetic allowlist — другой scope | Contract, interface, identity/rights/human/revocation tests не выбраны |
| Готов Windows CPU-only? | Static CPU path без TTS/GPU/network; Linux render PASS | Actual Windows host/tools/fonts/render/playback и paths NOT_RUN |
| Можно ли публиковать CI videos/cards? | Source предлагает upload, но synthetic permit не разрешает общее распространение | Exact exposure/access/retention/custodian scope не задан; upload не выполнять |
| Нужен ли S3 для D1? | Нет runtime dependency; только отдельные pure models/LAB design | Выбор protected production persistence требует отдельного решения; не объявлен одобренным |

## Следующее задание — шаблон для владельца, не выполнение

После независимого review владелец может отдельно утвердить OD-G3-01/02/03/04/06/07/10 и сформулировать exact G3.1 scope. Задание должно назвать новую утверждённую базу, exact include blobs, path assumption, платформы/команды и допустимые synthetic outputs. Оно должно отдельно сказать, разрешены ли push/Draft PR и CI evidence publication; отсутствие выбора OD-G3-05 означает не создавать upload authorization. Ни одно поле этого шаблона не заполнено фиктивными approvals.

Предлагаемые bounded шаги:

1. Независимый ChatGPT audit этих пяти документов, сверка source SHA, registry201 и no-repeat51. Owner фиксирует решения/ограничения отдельным сообщением или документом.
2. Если выбран только synthetic baseline: отдельный implementation task на exact четыре INCLUDE, без source workflow и прочих paths; проверить entry hashes/modes/parent/tree. При необходимости hardening source — сначала отдельная согласованная ревизия, затем новый allowlist.
3. Target и full tests на exact integrated candidate; Linux CI без изменения current workflow, Windows отдельно с честным NOT_RUN до запуска. Повторить no-repeat и forbidden path diff checks.
4. Подготовить отдельный acceptance packet и STOP. Merge/release/production authorization остаются отдельным решением, даже при всех PASS.
5. Для полной product цепочки: сначала OD-G3-08 contract design. Не выдавать baseline D1 за реализацию отсутствующих research/bridge/general gate/rights/evidence custody.

## Пакет независимого аудита

Пять файлов в одной documentation branch, sole parent — approved main:

- [G3_0_ARCHITECTURE_AUDIT.md](G3_0_ARCHITECTURE_AUDIT.md): вывод, SHA, source tests, CI review, последовательность.
- [G3_0_FILE_REGISTRY.md](G3_0_FILE_REGISTRY.md): все201 remaining paths, source blobs/modes, purpose/deps/tests/risks/recommendations, отдельные51 G1/G2 entries.
- [G3_0_DEPENDENCY_MATRIX.md](G3_0_DEPENDENCY_MATRIX.md): каждый переход цепочки, runtime/test/document dependencies, уже присутствующие shared blobs.
- [G3_0_RISK_AND_GATES.md](G3_0_RISK_AND_GATES.md): permit/rights/Windows/S3/CI и gates.
- Этот документ: новые решения только PROPOSAL и владельческие вопросы.

Commit SHA и ссылки передаются во внешнем handoff после commit/push; self-SHA в файлы не записывается. Это пакет **для** независимого аудита ChatGPT, не утверждение, что такой аудит уже выполнен. Итог G3.0 — **READY_FOR_OWNER_REVIEW**. **STOP.**
