# MVP-08B.4 — Qualification Gates

Дата записи: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / ACCEPTANCE_RECORD / ARCHITECTURE_PREPARATION**.

Точный исходный commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`. Запись приёмки ниже относится только к MVP-08B.3. Все новые решения MVP-08B.4 имеют статус **PROPOSAL / NOT_APPROVED**. Разрешения на реализацию, merge, release или production этим пакетом не создаются.

**PROPOSAL / NOT_APPROVED.** Gates — будущие критерии, не результаты выполненных native тестов. В этом задании все новые runtime qualification проверки **NOT_RUN**. FakeStore PASS не переносится на durable store.

## Общая семантика статусов

- **PASS**: все обязательные условия выбранного инкремента фактически выполнены в указанной конфигурации; есть commands, versions, case counts, raw logs/exit codes, input/output hashes и независимая оценка в требуемом объёме.
- **FAIL**: есть выполненный тест с нарушением инварианта, timeout, необоснованным success, вторым эффектом, stale write или неверным доказательством. Не скрывать его уменьшением scope после прогона.
- **BLOCKED**: обязательная предпосылка — owner decision, контракт, доступ, платформа, доказательство — отсутствует/противоречит. Указать точную причину; время ожидания не разрешение.
- **NOT_RUN**: проверка не запускалась. Это не PASS и не доказательство, что функция не существует. Разделять deferred layer и невыполненный обязательный тест уже выбранного scope.

PASS всегда ограничен OS/FS/runtime/engine/config/fault model. Незаявленное power loss, hardware caching, network filesystem, backup/restore и перенос между ОС остаются NOT_RUN. Исходные PURE результаты — только reference/model evidence.

## Q1 — Contract Compatibility

**PASS:** для выбранного инкремента закреплены base/tree, allowlist, owner scope и native data/evidence identity; согласовано, как не подменять PURE_FAKE_ONLY/native qualification. Request/key/receipt bytes, active projection, token, COMPLETED и UNKNOWN semantics не ослаблены. Созданы и проверены положительные/отрицательные совместимые векторы, version/namespace mismatch запрещён. Все необходимые новые решения явно утверждены владельцем.

**FAIL:** synthetic permit/receipt используется как native authority; автоматическое преобразование данных меняет approved identity; RESULT_AVAILABLE считается COMPLETED; adapter обходит pure guards.

**BLOCKED:** нет выбранного варианта/engine/evidence profile/точного будущего task. **NOT_RUN:** compatibility suite и независимая проверка нового profile ещё не выполнены.

Выход: compatibility matrix и явный список вне scope. Текущее состояние: **BLOCKED_OWNER_DECISION** для входа в implementation; native suite **NOT_RUN**. Это не противоречие принятому G1–G6.

## Q2 — Durable Atomicity

**PASS:** на выбранной native конфигурации атомарно сохраняются job/revision, event, mutation intent/marker, receipt, slot и относящиеся outbox/read reservation; конкурирующие процессы не получают два HELD для одной projection. CAS/stale writes отвергаются без частичных job/event/error writes. Qualified snapshot доказывает весь write set, не только marker. Ошибки прав/диска/записи/transaction boundaries не дают success.

**FAIL:** частичный authoritative набор, duplicate admission/slot, потеря immutable receipt, outbox после эффекта или разные revision roots. **BLOCKED:** Q1, test-root policy или доступ к кандидату отсутствует. **NOT_RUN:** native writes/competing-process suite не запускалась.

Выход: exact engine/driver/OS/FS/settings + raw transaction/fault evidence. Только storage-specific PASS; никакого executor/Windows promotion. Текущее состояние: **NOT_RUN**.

## Q3 — Crash Recovery

**PASS:** контролируемые process interruptions до/во время COMMIT, после физического COMMIT до ACK и после ACK воспроизведены с известными case identities. После нового процесса same M и namespace восстанавливаются; полный qualified набор даёт COMMITTED, полная доказанная пустота даёт NOT_COMMITTED, иначе HOLD/UNKNOWN. Unavailable/corrupt/partial store не становится NOT_FOUND/пустым новым store. Restore/stale copy/root replacement распознаются в заявленном fault model. Terminal release не открывает admission при неизвестном исходе.

**FAIL:** unknown M потеряна, создан новый token, retry/slot release по timeout, лишний submit, ложный success после reopen. **BLOCKED:** Q2 или разрешение на bounded native crash tests отсутствует. **NOT_RUN:** конкретный boundary/OS/power-loss класс не проверен.

Выход: fault matrix, preserved operation IDs и before/after evidence. Process kill PASS не считается power-loss PASS. Текущее состояние: **NOT_RUN**.

## Q4 — Windows Ownership and Fencing

**PASS:** на фактических Windows 10/11 в утверждённой матрице обычный пользователь запускает bounded test setup без admin. Два owner-process не владеют одновременно; stale controller/worker не пишет и не выполняет новый эффект. При kill/hang/restart текущая incarnation/fence и qualified death/lock evidence проверяются; TTL/PID не подменяют ownership proof. Clock rollback/boot change вызывают hold до допустимой переквалификации. Проверены NTFS root identity, ACL и относящийся Q7.

**FAIL:** takeover живого owner по TTL, stale effect/write, повтор fence/boot lease, необоснованные admin requirements или небезопасное продолжение после lock error. **BLOCKED:** нет Windows-хоста, выбранного lock/clock protocol либо permissions. **NOT_RUN:** конкретная версия ОС/FS/clock/crash ветка не испытана.

Выход: OS build, architecture, filesystem, user privilege level, process IDs/epochs (как evidence, не authority сами по себе), raw traces. Linux не закрывает gate. Текущее состояние: **WINDOWS_NOT_RUN**.

## Q5 — Exactly-once Effect Safety

Название gate не обещает exactly-once для произвольной внешней операции.

**PASS:** для одного точно описанного synthetic operation доказана persistent uniqueness acceptance по original token + payload digest; mismatch конфликтует. Durable intent до вызова; qualified ledger или общая transaction boundary позволяет восстановить прежний результат. Lost ACK/restart/cancel/stale-owner races не создают второй effect. Если принятие/непринятие не доказано — HOLD и ноль повторных generation submissions. Разделены absence proof и timeout.

**FAIL:** новый token после uncertainty; второй effect; cache/local counter принят как authority; неидемпотентный executor слепо повторён. **BLOCKED:** executor не предоставляет необходимую durable/idempotent/lookup гарантию либо нет разрешения на выбранный bounded synthetic effect. **NOT_RUN:** physical effect-boundary fault suite не выполнена.

Выход: точный заявленный guarantee/failure envelope и ledger/effect identities. Недоказуемые случаи остаются HOLD, не называются exactly-once PASS. Никаких real generator/provider вызовов. Текущее состояние: **NOT_RUN**.

## Q6 — Result Integrity and Provenance

**PASS:** для разрешённого result class фактически зафиксированы inputs/versions/identity, полные bytes/hash/length и применимые validation receipts; partial/truncated/mismatched/подменённый result не публикуется как готовый. Связь с исходным effect/plan проверена; provenance/rights evidence оцениваются отдельно от content hash. Для media потребовались бы отдельные decode/quality/rights проверки; они не входят в storage lab.

**FAIL:** metadata/существование файла считается полноценным result, hash принят за лицензию, unknown rights очищены, import/save/COMPLETED объявлены без отдельных receipts. **BLOCKED:** неизвестны result class, validation policy, provenance/rights или нет разрешения на import/save. **NOT_RUN:** bytes/decoder/rights/import квалификация не выполнена.

Выход: immutable result evidence без автоматического разрешения на Asset Library/production. Текущее состояние: **NOT_RUN / DEFERRED**.

## Q7 — Security and Path Safety

**PASS:** задан изолированный test root и ordinary-user access policy; unsafe/absolute/traversal/UNC/device paths отвергаются в поддерживаемом профиле; root и file identity проверяются по квалифицированным handles. Reparse/symlink/root replacement/permission denial/disk full/partial write и TOCTOU races испытаны в фактической OS/FS матрице. Утечки секретов/доступ к пользовательским материалам и production roots запрещены. Restore/cleanup не следуют подменённым links.

**FAIL:** check-then-reopen race, silent fallback outside root, ложный успех при отказе доступа, небезопасное cleanup или публикация partial evidence. **BLOCKED:** native primitive/ACL/test-root/path policy не утверждены или не могут обеспечить envelope. **NOT_RUN:** соответствующий OS/path/race класс не проверен.

Выход: capability/path threat matrix, rights/cleanup bounds и реальные результаты. Минимальная root policy нужна до первого разрешённого native write; полный PASS определяется scope, не откладывается до production. Текущее состояние: **NOT_RUN**.

## Q8 — Independent Acceptance

**PASS:** независимый проверяющий получил exact commit/tree/diff/sources/commands/raw logs/counts/skips/errors/limits и явно принял конкретный инкремент с указанными ограничениями; отмечено, был ли собственный независимый test rerun. После этого владелец отдельно решает следующий шаг.

**FAIL:** скрытые ошибки, подмена тестовых данных реальными правами, неверные SHA/scope/counts или отказ в приёмке из-за нарушений. **BLOCKED:** пакет/доступ/решение отсутствуют. **NOT_RUN:** независимая проверка следующего инкремента ещё не состоялась.

Принятие MVP-08B.3 не является Q8 PASS для ещё не реализованного MVP-08B.4. Текущее состояние: **NOT_RUN**. Никакой gate не даёт merge/production permissions автоматически.

## Последовательность

Предлагается C из [вариантов](INCREMENT_OPTIONS.md): Q1 → storage-specific Q2/Q3 → отдельный Q4 с Q7 → bounded synthetic adapter Q5/Q6/Q7 → Q8 по каждому пакету. Q7 minimum test-root prerequisites действуют уже до storage writes. Для storage-only пакета Q4–Q6 остаются явно DEFERRED/NOT_RUN; это не ложный end-to-end PASS. Все переходы требуют решения владельца; автоматической реализации нет.
