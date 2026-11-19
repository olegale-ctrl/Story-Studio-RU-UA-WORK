# EC Decision Matrix — пакет рекомендаций владельцу

**Общий STOP: BLOCKED_CONTRACT. Implementation не разрешён.**

**DOCS_ONLY / INDEPENDENT_REVIEW.** Target [c5cd33023880fd6726b74f5631eb766cc0959892][target], tree `7df9167d43018eb2685ba6ea674afb85a7d21263`; base [04ea194e4d57c8a0550d7412281da58d4ba252c5][b2]. Источник десяти вопросов — [OWNER_DECISION_DOSSIER на target][dossier]. Ниже независимая оценка исходных альтернатив, а не утверждение от имени владельца.

`RECOMMEND_APPROVAL` рекомендует конкретный вариант с указанным ограничением. `REVISE` требует точной правки до утверждения применимого контракта. `BLOCKED` означал бы отсутствие необходимого источника/внешнего evidence; для самой оценки вариантов такого отсутствия нет. Реальное исполнение F01, durable/Windows и live остаётся отдельно заблокированным.

|EC|Вердикт|Предпочтение|Owner decision|
|---|---|---|---|
|01|RECOMMEND_APPROVAL|A — prefix RESULT_AVAILABLE|PENDING|
|02|REVISE|A после F01/F02/F05|PENDING|
|03|REVISE|B для pure; A только после F03 и отдельной qualification|PENDING|
|04|REVISE|A после exact restart/fence/clock rules F04|PENDING|
|05|REVISE|B для pure; A как будущий durable target после F03/F04|PENDING|
|06|RECOMMEND_APPROVAL|B — observe only на первом этапе|PENDING|
|07|REVISE|B для pure, A только с frozen F01/profile; уточнить cap|PENDING|
|08|REVISE|A после exact code/field/precedence table F05|PENDING|
|09|RECOMMEND_APPROVAL|A — исключить import/attach/save|PENDING|
|10|RECOMMEND_APPROVAL|A — отложить Route D execution mapping|PENDING|

## EC-01 — Граница результата

**Проблема и исходное подтверждение.** [SM11–SM16][state] и [SG05/SG10/SG11][handoff] требуют разные доказательства для provider result и завершённого сохранённого проекта. Нельзя назвать synthetic provider result целым завершённым pipeline.

**A/B.** A: prefix до RESULT_AVAILABLE, поздние операции disabled. B: ждать квалифицированной полной saga, прежде чем выпускать core.

**Рекомендация / вердикт.** A, **RECOMMEND_APPROVAL**. Сохранить nonterminal result, pipeline_complete=false и HANDOFF_NOT_QUALIFIED; не вводить альтернативный COMPLETED.

**Уточнения.** Срок хранения результата и active slot по F02; отсутствие активного worker не превращает state в terminal. Название partial core не должно означать весь D08.

**Риски / зависимости.** Ошибочное чтение resultavailable UI/CLI; EC-06 observer и EC-09 deferral. Исторические P1 и OD02/03/04/06 остаются открыты.

**Приёмка.** P008/A001/A007: no import/attach/save, нет пути к SM16 без SG receipts, исходные 22 states/38 rules сохранены. Статический graph check есть; runtime NOT_RUN.

## EC-02 — Identity, canonical hashes и idempotency

**Проблема и исходное подтверждение.** [B.1 Schema/Identity][job] фиксирует JCS-LOCAL-1, request/purpose/batch scope, unique active intent, retained identity и отличия от raw/editor hashes. [Freeze §2–3][freeze] предлагает acyclic graph и full tuple, но оставляет F01/F02/F05.

**A/B.** A: явные закрытые projections, purpose, retained full keys. B: отложить принятие схемы до другого точного совместимого проекта.

**Рекомендация / вердикт.** A после исправления, **REVISE**. Не менять encoder на compact JSON. Добавить отдельную active-purpose uniqueness и exact historical REUSED rules; не включать текущий batch/permit в RequestIntent.

**Необходимые уточнения.** Полный hash-preimage registry/version/domain; immutable effect identity; active scope и состояния; replay старого receipt после expiry/termination не выдаёт новый grant; exact conflict vs authority denial.

**Риски / зависимости.** Несовместимые bytes между producers, два активных job для одного purpose, потеря dedup при reset. Связано с EC-03/05/08. Hash consistency не является подписью или юридической authority.

**Приёмка.** Fixed byte/hash vectors, no cycles; terminal replay возвращает тот же receipt; changed content under old key — conflict; новый неподходящий permit — typed denial; concurrent same-purpose admission atomic. P001–P005/P012/P020 нуждаются в применимых правках/дополнениях.

## EC-03 — Store / transaction / fault model

**Проблема и исходное подтверждение.** [W][state], [R25][recovery], [OD07][open] требуют собственного durable authority, а не RAM LAB или Library DB. Предложенные DELETE/FULL/FK и один writer не являются результатами испытаний.

**A/B.** A: отдельный managed SQLite JobStore с explicit create/open, store identity и atomic W. B: только pure FakeStore до отдельной durable qualification.

**Рекомендация / вердикт.** **REVISE** A по F03; для первого pure этапа рекомендовать B. Выбор B не утверждает будущий SQLite profile и не обещает persistence.

**Уточнения.** COMMITTED / NOT_COMMITTED / UNKNOWN_COMMIT_OUTCOME; one-operation evidence; store-open errors и forbid auto-recreate/migration; активная uniqueness в той же транзакции admission. DDL остаётся внутренним только после фиксации этих свойств.

**Риски / зависимости.** False rollback/ACK, половина job/event/outbox, неправильный NOT_FOUND. EC-02/05; durable gate требует exact runtime/SQLite/FS и bounded faults, без power-loss вывода из process kill.

**Приёмка.** Pure tests доказывают только модель atomicity/CAS. Отдельно D001–D004/D007/D009/D010/D018 на новых private DB: close/reopen, commit fault classes, no mixed rows/reset. Windows и actual disk/page/flush remain NOT_RUN сейчас.

## EC-04 — Owner, leases, fencing и clock

**Проблема и исходное подтверждение.** [W/SM05/SM25/SM26][state] и [R22][recovery] требуют current authority и stale rejection, но не делают lease expiry доказательством прекращения старого эффекта. Proposal уточняет controller-only preflight/first claim; это новая явная profile rule, не историческое свойство реализованного кода.

**A/B.** A: один same-process serial worker, exclusive owner lock, incarnation/epoch, fail-closed clock. B: отдельно квалифицировать multiprocess/external workers и их fencing.

**Рекомендация / вердикт.** A после F04, **REVISE**. Для pure разрешима только виртуальная модель tokens/clock; OS lock implementation и квалификация откладываются.

**Уточнения.** Exact claim/renew/restart states, bootstrap без старого worker lease, acquisition transaction, release semantics, clock_epoch, expiry exclusive, rollback/suspend/reboot hold. Не украсть живой lock и не завершать чужой процесс.

**Риски / зависимости.** Stale callback может незаконно изменять job; законный recovery может навсегда блокироваться. Нужны EC-02 immutable token и EC-05 lookup; native locks/time не наследуются от FakeClock.

**Приёмка.** F04 combined restart trace, P009/P010 и отдельные negative clock cases. D005/D006/W001–W004/W007 проверяются позже на точно названных OS/Python/NTFS; один tested Windows build не квалифицирует автоматически другой.

## EC-05 — Outbox / SimulatorStore / recovery

**Проблема и исходное подтверждение.** [SIM08/09/18][sim] и [R02/R03][recovery] требуют provider acceptance before ACK и lookup исходного ключа при неизвестном результате. [W][state] требует committed intent before effects. Общая транзакция между двумя ресурсами не обещана.

**A/B.** A: отдельный durable simulator ledger и immutable effect token, outbox, lookup-only unknown recovery, generation cap 1. B: pure fake ledger до квалификации durable protocol.

**Рекомендация / вердикт.** B для pure, A как последующий target после F03/F04, **REVISE**. Это не выбор второго scheduler.

**Уточнения.** Token/payload сохраняются через incarnation; текущий controller принимает старый receipt как data; authoritative NOT_ACCEPTED означает exact intact ledger proof, не недоступность/пустой новый store. Cap1 остаётся после known rejection, quota pause и restart; новый generation intent запрещён.

**Риски / зависимости.** Duplicate acceptance после lost ACK; бесконечный hold при неправильном fence mapping; ошибочная liability release. Нужны EC-02/03/04/07/08.

**Приёмка.** P013–P018 плюс combined restart/cancel/unknown-commit cases; D003/D008 позже на обоих реальных stores. Никакой fake test не доказывает D003 или SIM18 process durability.

## EC-06 — Observer / cursor / wait

**Проблема и исходное подтверждение.** [B.1 execution revisions][job], [B.2 SP readiness][b2_sp] и [SP diagnostics][sp] не позволяют зеркалу/CLI объявлять lifecycle truth.

**A/B.** A: consistent snapshot + bounded read-only wait с точным predicate/deadline. B: сначала только single-shot observe.

**Рекомендация / вердикт.** B, **RECOMMEND_APPROVAL** для минимального этапа. A можно выбрать позже либо добавить virtual wait отдельным явным scope; timeout никогда не retry/cancel.

**Уточнения.** Exact snapshot/cursor version, store/job namespace, ahead/divergent cursor responses; недоступность store не NOT_FOUND. При B P019 wait не объявлять выполненным.

**Риски / зависимости.** Stale snapshot принят за текущую истину; hidden scheduler внутри wait. Нужны EC-02/03 и EC-08 codes.

**Приёмка.** Read-only FakeStore observer не изменяет revision/lease/events/outbox. D014 consistent SQL snapshot отдельно позже. No CLI queue/retry/renderer.

## EC-07 — Synthetic authority / fixture / resources / retention

**Проблема и исходное подтверждение.** [OD05/07/08][open] и [F01 specification][sim] требуют точной области authority, limits и настоящих fixture bytes для положительного media run. Эти bytes отсутствуют по замыслу DOCS_ONLY.

**A/B.** A: reviewed self-authored F01/project/prompt и trusted synthetic scope с limits. B: pure-only metadata/placeholders, без положительного durable/media execution.

**Рекомендация / вердикт.** B для pure после F05/F06, затем отдельно A; **REVISE** текущую смешанную entry gate и retry cap.

**Уточнения.** Два retry или два total reads; counter lifetime; limits на bytes/depth/text/ticks/events/jobs и exhaustion behavior; fake metadata не producer proof; no user data deletion/retention cleanup. Cap16/128/32/1MiB/8MiB/10000ticks — proposals, не замеры ноутбука.

**Риски / зависимости.** Placeholder объявлен проверенным MP4, synthetic principal принят за реального владельца, counters silently reset. Зависит от EC-02/04/05/08. F01 и native tool evidence нужны следующему применимому этапу, не для отрицательного codec test.

**Приёмка.** P006/P007/P011/P017/P023/P024 по реально разрешённым cases; positive F01 cases явно NOT_RUN без bytes/rights. D017/D018 — отдельные physical/snapshot/fault tests. Никаких моделей/рендеринга для изготовления missing fixture в этом scope.

## EC-08 — Typed errors / uncertainty

**Проблема и исходное подтверждение.** [JobError][job] и [recovery][recovery] различают NONE/KNOWN/UNKNOWN effect и billing. Нельзя общим exception преобразовать uncertainty в безопасный retry.

**A/B.** A: closed local codes с сохранением B.1 retry/effect/billing classes и check precedence. B: другая полная mapping до реализации.

**Рекомендация / вердикт.** A после F05, **REVISE**. Не переименовывать молча `external_effect` в `effect`; response-only refusal и durable error mutation различать.

**Уточнения.** Exact public error envelope, field/version и mappings; P004/P011 cases, stale denial audit, expired historical replay, F03 unknown commit. Integrity failure всегда запрещает effects, даже если снаружи возвращается более ранняя format error.

**Риски / зависимости.** False PASS по любому безопасному коду, незаконная запись из stale caller, потеря исходной uncertainty, утечка prompt/URL/credentials. Зависит от EC-02/03/04/05.

**Приёмка.** На каждом fixed input ровно один expected result/code и точные allowed counters; no swallowed errors. Все ключевые negative cases должны сохранять байты прежнего job/receipt и forbidden-effect counters.

## EC-09 — Asset Library / project save

**Проблема и исходное подтверждение.** [SG04–SG11][handoff], [OD02/03/04/06][open] и [MVP-08A limits][a_limits] показывают, что tags, links, raw SHA и GUI ACK не заменяют unique import receipt / saved JSON CAS.

**A/B.** A: initial core не делает import/attach/save. B: отдельно согласовать Library/save/validation/lifecycle extensions до полной saga.

**Рекомендация / вердикт.** A, **RECOMMEND_APPROVAL**. B остаётся позже отдельной задачей, без объявления OD закрытыми.

**Уточнения.** Pure RESULT_AVAILABLE не имеет ASSET_COMMITTED/COMPLETED proof; user projects/Tk/Library DB не трогаются. Rights и exact revision recheck сохраняются для будущего разрешённого use.

**Риски / зависимости.** False completion по ссылке в каталоге, повторный import после lost return, перезапись нового JSON. EC-01 и будущие OD02/03/04/06; не блокирует отдельно разрешённые pure interfaces.

**Приёмка.** A001 как negative boundary; A002–A010 остаются будущими qualification, а не выполненными благодаря запрету вызовов. No changes в существующих production/Library interfaces.

## EC-10 — SP/1.1 / Route D

**Проблема и исходное подтверждение.** [SP/1.1][sp] валидирует fixed diagnostic stage lists и всегда блокирует dispatch/release; Route D whole-film plan+materials отличается от [B.1 T2V/I2V anchor job][job].

**A/B.** A: сохранить только будущую lifecycle/receipt boundary, execution mapping отложить. B: отдельно задать один narrow synthetic render-plan handler.

**Рекомендация / вердикт.** A, **RECOMMEND_APPROVAL**. Ни семь SP stages, ни текущий intent hash не становятся JobStore API/DAG.

**Уточнения.** Initial profile не выполняет Route D; BLOCKED_DISPATCHER_CONTRACT и release_allowed=false остаются. Нет `first_video.build` обхода. SP-OD01–09 не расширены.

**Риски / зависимости.** Второй dispatcher в CLI, прямой renderer bypass, alias compact hash→request hash, false release от all-true diagnostic. Зависит от будущего отдельного integration contract, а не от быстрого fake core pass.

**Приёмка.** P020/P022/L006 как запрет наследования authority; unchanged SP source. Новые handler/whole-film execution/runtime grants требуют отдельной задачи.

## Owner action

Владелец должен назвать вариант каждого EC, необходимые модификации, exact source/base/tree, разрешённый этап и allowlist. Можно принять рекомендованные отсрочки и вернуть F01–F05 на узкую правку. Молчание, одобрение документации или этот review не являются implementation authorization.


## Точные источники

[target]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/commit/c5cd33023880fd6726b74f5631eb766cc0959892
[b2]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/commit/04ea194e4d57c8a0550d7412281da58d4ba252c5
[job]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_JOB_CONTRACT.md
[state]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_STATE_MACHINE.md
[sim]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_OFFLINE_SIMULATOR.md
[recovery]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_RECOVERY_MATRIX.md
[handoff]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_ASSET_HANDOFF.md
[open]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_OPEN_DECISIONS.md
[b1_oracles]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_TEST_ORACLES.md
[b1_plan]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_IMPLEMENTATION_PLAN.md
[owner]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08_OWNER_APPROVAL.md
[a_limits]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08A_LIMITATIONS.md
[a_owner]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08A_OWNER_ACCEPTANCE.md
[freeze]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/CONTRACT_FREEZE_PROPOSAL.md
[oracles]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/ACCEPTANCE_ORACLES.md
[scope]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/MINIMAL_EXECUTION_SCOPE.md
[task]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/IMPLEMENTATION_TASK_PROPOSAL.md
[dossier]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/c5cd33023880fd6726b74f5631eb766cc0959892/docs/tasks/MVP_08B_2A_OFFLINE_CONTRACT/OWNER_DECISION_DOSSIER.md
[sp]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/16d28ec0376c8c28f879c8aacb18d5378fea83a3/docs/tasks/SP_INTEGRATION_01B/DIAGNOSTIC_CONTRACT_V1_1.md
[b2_sp]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/04ea194e4d57c8a0550d7412281da58d4ba252c5/docs/tasks/MVP_08B_2_IMPLEMENTATION_AUDIT/MVP_08B_2_SP_INTEGRATION_READINESS.md
[encoder]: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/asset_library.py
