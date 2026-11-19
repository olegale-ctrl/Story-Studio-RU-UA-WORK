# Contract Findings — независимая проверка MVP-08B.2a

**DOCS_ONLY / INDEPENDENT_REVIEW · BLOCKED_CONTRACT.** Проверяемая ревизия [c5cd33023880fd6726b74f5631eb766cc0959892][target], tree `7df9167d43018eb2685ba6ea674afb85a7d21263`; parent [04ea194e4d57c8a0550d7412281da58d4ba252c5][b2].

Все замечания относятся к будущему контракту, не к обнаруженным дефектам реализованного GenerationJob: такой runtime здесь не создавался и не тестировался. HIGH означает, что две разумные реализации могут несовместимо трактовать безопасность/identity/recovery. MEDIUM — неоднозначность API, теста или границы этапа. Это не утверждение, что уже доказан duplicate effect.

## F01 — Не все хешируемые preimages заданы побайтно — HIGH / EC-02

**Факт.** [Freeze §2][freeze] задаёт порядок InputManifest/CapabilityProfile → RequestIntent → batch → permit → event/receipt и устраняет явные циклы. Но batch добавляет неопределённый `bounded policy`; permit имеет словесный список полей; EffectPayload и event body перечислены в прозе. Для них нет полного закрытого versioned shape, точных field names/types, null/absent policy и единого перечня исключаемых digest fields. Поля RequestIntent описаны точнее, но нужны детальные scalar/array constraints. [B.1 Schema conventions][job] требует versioning и rejection неизвестных полей.

**Контрпример по спецификации, не runtime test.** Два автора могут сериализовать срок действия как `expires_at` и как вложенный `validity.expires_at`, оба сохранив предложенный acyclic graph. Хеши различны, хотя prose-смысл совпадает. Ацикличность сама по себе не задаёт canonical bytes.

**Исправление.** До pure кода закрепить registry всех публично хешируемых записей, включая InputManifest, CapabilityProfile, FixtureRegistry projection, RequestIntent, batch manifest, BatchPermit, AcceptanceEvent/Receipt, EffectPayload, envelope/event/result projections. Для каждого: domain/version, exact fields/types, preimage exclusions, encoding, null/order policy, equality rule. Если внешний record не поддерживается первым этапом — явно запретить его построение, не заполнять guessed hash. Не менять B.1 JCS-LOCAL-1 на compact JSON/RFC8785.

**Приёмка.** Два независимых codec получают одни байты и digest на fixed vectors; raw-file SHA/SP compact hash не принимаются как request hash без точного recomputation/binding; каждый preimage DAG проверяем без будущего digest. P001/P002/P020 остаются NOT_RUN до реализации. Само наличие векторов не является авторизацией или медиаверификацией.

## F02 — Полная idempotency tuple не заменяет active-intent uniqueness — HIGH / EC-02/03

**Факт.** [B.1 Identity/idempotency][job] требует `unique active-intent constraint`; [T005][b1_oracles] требует одну queue item per purpose/key. [Freeze §2, steps 4–5, §3–4][freeze] явно закрепляет unique полную tuple `(project,purpose,request_hash,batch,revision,manifest)` и новый job при новой одобренной области, но не определяет дополнительную active-intent projection, точный набор active состояний и момент снятия ограничения.

**Конструктивная неоднозначность.** J1 и J2 имеют одинаковые project/purpose, разные request hash и новые подходящие permits/batches. Полные ключи различны; одно tuple-ограничение разрешает оба. Один worker лишь сериализует их, не предотвращая две активные заявки на одно намерение. Иной автор может запрещать J2. Обе трактовки укладываются в часть prose.

**Исправление.** Выбрать точную active-purpose projection и поведение replacement. Рекомендуется отдельный атомарный active slot для `(store namespace, project_id, purpose_id)`; при существующем несовместимом active job — типизированный конфликт и отсутствие admission mutations. Иной scope допустим только как явное owner-approved уточнение. RESULT_AVAILABLE неterminal: слот не освобождать только потому, что prefix закончил вычисления; отдельные результаты одного содержания требуют разных purpose IDs. Исторические dedup keys/receipts сохранять после освобождения active slot.

**Приёмка.** Два конкурирующих приёма с новыми hash/batch в одном active-purpose scope не создают два active job; terminal exact replay возвращает старый receipt; новый purpose допускает отдельный результат; RESULT_AVAILABLE не даёт неявного replacement. Fake атомарность проверяет модель; SQLite constraint/transaction требует отдельного D-этапа.

## F03 — Нужен отдельный outcome для неизвестного результата COMMIT — HIGH / EC-03/05

**Факт.** [Freeze §4][freeze] описывает rollback до commit и потерю ответа после commit. D002 разделяет только эти две точки; D018 обещает typed failure и сохранение истории при storage exhaustion. [B.1 W][state] и [R02/R25][recovery] запрещают effects при непроверенной authority/uncertainty. Не закреплены ошибочный/прерванный COMMIT с недоказанным результатом и отличие такого исхода от доказанного rollback.

**Риск.** Если любой exception из commit обработать как «ничего не записано», admission может быть повторён как новый, либо effect пойдёт без доказанного committed intent. Обратное предположение «commit был» также необоснованно. Этот обзор не заявляет конкретное поведение SQLite при конкретном I/O failure: fault classes ещё надо выбрать и испытать.

**Исправление.** Сформулировать три результата mutation: доказанный COMMITTED, доказанный NOT_COMMITTED, UNKNOWN_COMMIT_OUTCOME. Последний — операционный blocker, не новое lifecycle state; новых effects нет. Recovery читает тот же целый store/operation key и проверяет atomic records; отсутствие доступа, corruption или частичное противоречие не становится NOT_FOUND. Зафиксировать identity операции и boundary при дисковом full/I/O/flush/commit-ACK fault. DDL и индексная раскладка могут остаться implementation detail после фиксации этих инвариантов.

**Приёмка.** Отдельные finite cases до commit, во время неоднозначного commit outcome, после commit до ACK; совместная проверка job/event/receipt/outbox и отсутствия нового dispatch. FakeStore может моделировать три исхода, но не доказывает crash durability или NTFS flush semantics. Настройки DELETE/FULL/FK сами по себе qualification не заменяют.

## F04 — Recovery старого receipt нужно отделить от права старого worker на запись — HIGH / EC-04/05

**Факт.** [Freeze §5][freeze] отвергает stale incarnation/epoch на каждом acknowledgement; §6 требует lookup первоначального token после рестарта и восстановления принятого результата через SM09. [B.1 R03/R22][recovery], [SM06/SM09/SM31][state] одновременно требуют original effect identity и текущего fenced controller. В proposal не зафиксированы exact separation и restart/claim cases.

**Риск.** Если incarnation входит в immutable effect identity и меняется при lookup/retry, получится новый effect. Если recovered old provider receipt сам трактуется как stale writer token, законный SM09 навсегда блокируется. Если старый callback получает новый fence только из-за совпадения bytes, fencing обходится. Это три возможные несовместимые реализации.

**Исправление.** Immutable operation/effect/attempt identity не менять при рестарте. Старый worker command с его fence отклонять. Новый controller после lock + committed incarnation/lease acquisition может read-only lookup старого effect и записать проверенные proof data под НОВЫМ текущим CAS/fence. Receipt не предоставляет write authority. Закрепить allowed claim/renew/recovery states, expiry/clock_epoch behavior и запрет lease stealing у живого lock owner. В pure этапе это виртуальные tokens, а не доказательство OS lock.

**Приёмка.** Один trace включает accept→lost ACK→owner restart→old callback rejection→current-owner lookup→SM09 той же attempt; provider acceptance count 1, immutable payload/token те же. С cancel flag — SM31, не RUNNING. Отдельно stale/expired fence, clock anomaly и два контендера. D005/D006 и W003 требуют реальных процессов/host позже.

## F05 — Оракулы и ошибки ещё не дают единственного проверяемого outcome — MEDIUM / EC-02/07/08

**Факты по точным строкам [ACCEPTANCE_ORACLES][oracles].**

- P003/P004/P012 ссылаются на T001 (missing exact model/hash), а P003 также на T004 (draft edit), которые не специфицируют accepted/reused API. Основное происхождение — B.1 Identity/idempotency; T005 относится к active intent. Исправить ссылки, не переписать исходные T001/T004.
- P004 объединяет «новый request со старым supplied key» и «сохранён initial auth binding». Первый — conflict; корректный новый key со старым permit не покрывает новый request и должен получить authority/scope denial по freeze §3. Точные входные случаи и precedence не разделены.
- P011 использует `PROFILE_UNQUALIFIED/OPERATION_NOT_AVAILABLE` для нескольких входов, не привязав код к каждому входу. Оба могут безопасно запретить effect, но это ещё не exact API oracle.
- [MINIMAL_EXECUTION_SCOPE][scope] задаёт **2 retries** safe-read per checkpoint; D015 говорит «at most 2 safe reads». Не определено, это 2 общих вызова или исходный + 2 retry, и что сбрасывает counter.
- P009 ожидает отсутствие events при stale command; [B.1 test conventions][b1_oracles] допускает sanitised rejection audit. Нужно отделить отказ stale caller без job mutation от отдельного incident, записываемого текущим owner.
- [Freeze §9][freeze] говорит «Retain B.1 fields», но использует `effect`, тогда как [JobError][job] — `external_effect`. Нужны exact wire field/version и distinction response-only denial vs durable job error. Failed CAS/stale fence не даёт вызывающему права дописать JobError в тот же job без нового законного mutation.

**Исправление и приёмка.** Таблица input case → ровно один public code/disposition → разрешённая audit mutation → effect/billing class; отдельные total calls/retries/checkpoint lifetime; freeze field names; golden positive/negative error vectors. Тест не проходит по принципу «любой из двух кодов подошёл». При неопределённом COMMIT приоритет сохраняет F03 hold.

## F06 — Pure gate связан с ещё несуществующим F01 и всем 22-path пакетом — MEDIUM / EC-03/05/07

**Факт.** [Implementation task][task] сначала требует все 22 paths и hashes fixture, затем pure P001–P024; [Scope][scope] допускает pure placeholders, а положительный fixture run требует точный F01. Реального F01 нет. Это не дефект отсутствующего файла в DOCS_ONLY-предложении; это неоднозначная граница следующей задачи.

**Решение.** Разделить будущую авторизацию: (1) pure values, ports, FakeStore/FakeClock и scripted fake outcomes без SQLite/media I/O; (2) настоящее принятие F01 + долговременные store tests; (3) Windows qualification. Для pure использовать явно synthetic, не producer-qualified proof objects. Даже зелёный trace до RESULT_AVAILABLE в FakeStore — только проверка потребителя такого proof, не доказательство настоящего результата или authority.

**Приёмка.** Owner task pure этапа имеет узкий file allowlist, exact base/tree, ноль sqlite/provider/model/FFmpeg/Library/save calls, отчёт eligible P cases и всех неисполненных cases. D/W/A/L остаются NOT_RUN. Ни настоящее media decoding, ни SQLite-квалификация не требуются для проверки equality/hash/CAS model. См. отдельный implementation gate.

## F07 — Номер следующего этапа нужно сопоставить с историческим планом — MEDIUM / граница scope

[B.1 IMPLEMENTATION_PLAN][b1_plan] называет `.2` Offline Core, а `.3` Local Result Pipeline. Новая задача владельца называет `MVP-08B.3 — Pure Offline GenerationJob Core`; B.2 теперь является аудитом, а не выполненным core. Это допустимое новое планирование, но не основание считать исторические `.2` или `.3` реализованными.

В следующем owner task явно закрепить новый stage ID/scope и отметить, что он не закрывает исторические local validation/Library/save deliverables. Не требуются переименование исходных документов, merge веток или широкое архитектурное перепланирование.

## Поштучная проверка 66 оракулов

`SPEC_USABLE` — пригодный критерий для заявленной узкой цели после общих входных gates, не runtime PASS и не обещание полной fixture expansion. `REVISE_*` — указана конкретная нужная правка. Все исходные execution statuses сохранены **NOT_RUN**. Добавления для F02–F04 потребуются сверх формального количества 66 либо как явно разделённые cases; сохранение числа 66 не является целью приёмки.

|ID|Execution status исходника|Независимая оценка спецификации|Уточнение|
|---|---|---|---|
|P001|NOT_RUN|REVISE_F01|Нужны fixed canonical bytes/hash и разделённые invalid-value cases.|
|P002|NOT_RUN|REVISE_F01|DAG проверяем, но точные preimages ещё не заморожены.|
|P003|NOT_RUN|FIX_SOURCE_F05|Invariant пригоден; T001/T004 не задают accepted/reused API.|
|P004|NOT_RUN|SPLIT_F05|Старый supplied key и старый permit при новом key дают разные cases/codes.|
|P005|NOT_RUN|SPEC_USABLE|Scope denial/new matching permit пригодны; active-intent counterexample F02 добавляется отдельно.|
|P006|NOT_RUN|SPEC_USABLE|Trusted fake context, не настоящий issuer/rights proof.|
|P007|NOT_RUN|SPEC_USABLE|Раскрыть pre-submit и qualified no-acceptance случаи по SM19.|
|P008|NOT_RUN|SPEC_USABLE|Prefix не разрешает SM12–16 или pipeline_complete=true.|
|P009|NOT_RUN|CLARIFY_F04_F05|Stale caller ничего не пишет; current-owner rejection audit определить отдельно.|
|P010|NOT_RUN|SPEC_USABLE|Pure CAS model; реальная concurrency/transaction отдельно D/W.|
|P011|NOT_RUN|SPLIT_F05|Привязать один code к каждому exact profile/handler input.|
|P012|NOT_RUN|CLARIFY_F02_F05|Исправить T001 reference; lookup/replay не обновляет authority, expiry policy явная.|
|P013|NOT_RUN|SPEC_USABLE|Fake ledger lost-ACK criterion; не durable SIM18.|
|P014|NOT_RUN|SPEC_USABLE|Committed intent обязателен до effect gateway.|
|P015|NOT_RUN|SPEC_USABLE|Unknown lookup удерживает original attempt/token.|
|P016|NOT_RUN|SPEC_USABLE|Разделить exact/duplicate/stale/conflicting observations по fixed cases.|
|P017|NOT_RUN|SPEC_USABLE|Нет fallback или implicit permit renewal.|
|P018|NOT_RUN|SPEC_USABLE|Раскрыть no-effect/uncertain/settled cancellation cases.|
|P019|NOT_RUN|SPEC_USABLE|Только при отдельно включённом wait; иначе NOT_RUN/deferred.|
|P020|NOT_RUN|SPEC_USABLE|Проверять bytes/binding/domain, не только hex syntax.|
|P021|NOT_RUN|SPEC_USABLE|Недоступность не означает авторитетное отсутствие.|
|P022|NOT_RUN|SPEC_USABLE|Readiness/synthetic scope не создают real authority.|
|P023|NOT_RUN|SPEC_USABLE|Pure descriptor checks не квалифицируют фактические F01 bytes или OS path safety.|
|P024|NOT_RUN|SPEC_USABLE|No reset/prune/wrap; exhausted mutation не создаёт нелегальный error event.|
|D001|NOT_RUN|SPEC_USABLE|Настоящий close/reopen, не FakeStore.|
|D002|NOT_RUN|EXTEND_F03|Кроме before/after commit нужен UNKNOWN_COMMIT_OUTCOME fault case.|
|D003|NOT_RUN|CLARIFY_F04|После reopen original receipt обрабатывает current fence, token неизменен.|
|D004|NOT_RUN|SPEC_USABLE|SQL fault injection; одна atomic mutation, не multi-resource transaction.|
|D005|NOT_RUN|SPEC_USABLE|Реальные independent processes/lock; без termination чужих приложений.|
|D006|NOT_RUN|EXTEND_F04|Добавить current-owner lookup и успешное recovery при отказе old callback.|
|D007|NOT_RUN|SPEC_USABLE|No auto repair/recreate/migration; preserve evidence.|
|D008|NOT_RUN|SPEC_USABLE|Missing/unavailable ledger не NOT_ACCEPTED.|
|D009|NOT_RUN|SPEC_USABLE|Integrity incident, no overwrite/replay shortcut.|
|D010|NOT_RUN|SPEC_USABLE|Нужны effective settings/versions и реальный FS evidence.|
|D011|NOT_RUN|SPEC_USABLE|Process interruption не power-loss qualification.|
|D012|NOT_RUN|SPEC_USABLE|Clock epoch/rollback/reboot unknown → no new effect.|
|D013|NOT_RUN|SPEC_USABLE|Local-root qualification; syntax checks не protected handle guarantee.|
|D014|NOT_RUN|SPEC_USABLE|Consistent actual SQL snapshot отдельно от pure observer.|
|D015|NOT_RUN|REVISE_F05|2 total reads или initial + 2 retries; exact checkpoint/reset policy.|
|D016|NOT_RUN|SPEC_USABLE|Terminal history retained; reuse не reopen.|
|D017|NOT_RUN|SPEC_USABLE|Точные trusted-snapshot assumptions, без hostile TOCTOU claim.|
|D018|NOT_RUN|EXTEND_F03|При storage fault разделить доказанный rollback и unknown commit; hold без effects.|
|W001|NOT_RUN|SPEC_USABLE|Записать конкретный Windows build; непроверенные версии остаются NOT_RUN.|
|W002|NOT_RUN|SPEC_USABLE|Реальные NTFS/path cases; residual races явные.|
|W003|NOT_RUN|SPEC_USABLE|Native lock/restart test, не simulated token proof.|
|W004|NOT_RUN|SPEC_USABLE|Actual suspend/reboot/clock profile; не FakeClock qualification.|
|W005|NOT_RUN|SPEC_USABLE|Bounded local paths/errors, без ACL/admin settings changes.|
|W006|NOT_RUN|SPEC_USABLE|Scoped actual journal/flush/disk fault; не universal power loss.|
|W007|NOT_RUN|SPEC_USABLE|No orphan effect-capable worker; Tk не квалифицируется автоматически.|
|W008|NOT_RUN|SPEC_USABLE|Semantic/canonical equality, без выдуманной media byte equivalence.|
|A001|NOT_RUN|SPEC_USABLE|Negative boundary применим prefix; positive Library qualification не выполнена.|
|A002|NOT_RUN|SPEC_USABLE|Lost import ACK требует exact receipt/reconcile.|
|A003|NOT_RUN|SPEC_USABLE|Asset/provenance/rights identity не content SHA.|
|A004|NOT_RUN|SPEC_USABLE|Project identity/disk CAS остаются отдельным gate.|
|A005|NOT_RUN|SPEC_USABLE|Current exact rights/revision recheck; in-flight limit явный.|
|A006|NOT_RUN|SPEC_USABLE|Required decoded evidence не заменять header count.|
|A007|NOT_RUN|SPEC_USABLE|GUI/history link не SG10/SG11 saved proof.|
|A008|NOT_RUN|SPEC_USABLE|Read current JSON, never overwrite later user edit.|
|A009|NOT_RUN|SPEC_USABLE|Native/session/Tk qualification остаётся отдельной.|
|A010|NOT_RUN|SPEC_USABLE|Existing asset/result reuse, generation count unchanged.|
|L001|NOT_RUN|SPEC_USABLE|Запрет live/paid сохраняется даже при advertised $0.|
|L002|NOT_RUN|SPEC_USABLE|Unknown legal rights остаются hold.|
|L003|NOT_RUN|SPEC_USABLE|Material scope change требует new explicit approval.|
|L004|NOT_RUN|SPEC_USABLE|No inherited SSRF/native/transport qualification.|
|L005|NOT_RUN|SPEC_USABLE|Retention/deletion authority не выводится из recovery.|
|L006|NOT_RUN|SPEC_USABLE|Technical/all-true record не release authorization.|


## Что не признано дефектом

- RESULT_AVAILABLE оставлен неterminal, pipeline_complete=false, handoff disabled. Это честный partial stage при явном owner scope, не изменение COMPLETED.
- Раздельные JobStore и SimulatorStore без distributed transaction — допустимая saga при exact effect token и квалифицированном recovery. Здесь не предлагается второй scheduler.
- Отсутствие F01/DDL/runtime в исходной DOCS_ONLY ветке ожидаемо. Дефект — лишь попытка начать неопределённый следующий этап без их применимых gates.
- Отложенные Windows/NTFS/ACL, hostile TOCTOU, power loss, real legal authority, P1-01/02/03 и live profile не объявлены закрытыми. Нет требования решать их все в pure этапе.

**STOP: BLOCKED_CONTRACT.** Исправления ограничить перечисленными интерфейсами/оракулами; implementation остаётся отдельным разрешением владельца.


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
