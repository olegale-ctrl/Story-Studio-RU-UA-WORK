# Error and 58-oracle preservation matrix

**FREEZE_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0a; 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Pinned discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c`.
Только docs/offline vectors. Направление OD-PG-01–12 принято владельцем, но численные значения, роли, trust policies и operational protocols не утверждены. Нет validators/providers, permissions или qualification.

## G3.2.0b effective precedence / historical scope

X01–X04 choices OWNER_APPROVED. [Owner decisions](G3_2_0B_OWNER_DECISIONS_X01_X04.md) и [resolution evidence](G3_2_0B_RESOLUTION_AND_VECTOR_EVIDENCE.md) задают действующие уточнения. Сохранённые формулировки G3.2.0a ниже, помеченные historical, отражают prior blocked analysis, а не конфликтующую текущую норму. Исходный pinned reference никогда не изменяется. Ни один новый status marker проверки не является machine PG verdict или permission.

## Effective owner-approved overrides and traceability

| Source oracle / vector | Previous (historical) | Effective owner-approved clarification | Dependency / verification |
|---|---|---|---|
| P01-07 / V051 | source discovery says PG_PRODUCT_GAP for metadata/missing why_film; A notes PG_FORMAT conflict | Empty required why_film → PG_FORMAT(stage2). Nonempty insufficient dossier → PG_PRODUCT_GAP(stage6) after successful prior stages | X01 OWNER_APPROVED; V072 proposed substantive example, human/product policy OPEN. PG_SEMANTIC_NOT_RUN |
| COMMON-05 / P04-01 / V039 | A left mode/schema/hash primary error blocked | Unknown enum PG_FORMAT(stage2); known+bad binding PG_DIGEST(stage3); known+correct binding+forbidden pair PG_MODE(stage5) after refs | X02 OWNER_APPROVED; V071 paired correct binding, V073 unknown enum. BYTES/HASH verified, semantic NOT_RUN |
| P02-04 / V043 | A isolated content-addressed cycle fixture blocked | Preserve historical V043 block. Abstract V043-S…S6 are separate structural oracles, no crypto proof | X03 OWNER_APPROVED; seven STRUCTURAL_ORACLE_VERIFIED annotations, end-to-end closure unproven |
| P01-05 / P04-02/08 | Source claimed tools/profiles bound via plan though fields absent | New versioned plan proposal mandates both immutable binding refs; new SubjectKey on any binding change | X04 OWNER_APPROVED direction; V074…080 bytes/hashes verified, reapproval/migration policy OPEN |

All58 original source premise/expectation strings remain verbatim below. Their `Exact isolated-cause codes / result` lines are **A historical analysis**, superseded only for named branches by this explicit table; no deletion of historical expected error. Other branches and all HUMAN/PROVIDER/NATIVE limitations retained. New verification labels describe evidence work, not new PG result/error enums.

## Ошибки и результаты: без расширения namespace

Machine results pure discovery: CONSISTENT_NO_AUTHORITY либо DENY. STRUCTURALLY_VALID — explanatory stage annotation, **не** новый enum/status. CANONICAL_BYTES_VERIFIED в описании vector check — факт offline арифметики, не возвращаемое PG API значение. SUCCEEDED/FAILED/CANCELLED/INDETERMINATE — Body05.outcome, не admission verdict. BLOCKED_CONTRACT — статус задания/неопределённого expectation, не новый Error.code.

Proposed Error = contract,stage,code,subject_id|null,retry,outcome=DENY (все обязательны). Закрытые21 кода: PG_FORMAT, PG_DIGEST, PG_REFERENCE, PG_EVALUATION, PG_STALE, PG_PRODUCT_GAP, PG_IDENTITY, PG_AUTHORITY, PG_HISTORY, PG_REVOKED, PG_EXPIRED, PG_RIGHTS, PG_SCOPE, PG_MODE, PG_REPLAY, PG_PATH, PG_TOOLCHAIN, PG_EXECUTION, PG_INCOMPLETE, PG_EVIDENCE, PG_DEPENDENCY_UNAVAILABLE. No ALLOW_RENDER/PG_VERSION/new SI codes. Error ordering proposed C14N spec stages; X01/X02/X03/X04 не разрешены скрытой сменой priority.

Каждая строка ниже сохраняет **verbatim** source case и source expectation pinned discovery. После этого дано уточнение по **изолированным подслучаям**, не результат выполнения validator. Когда source объединяет разные причины, единственный error для всей строки выдумывать нельзя: перечислены exact code на каждый named cause, оставшиеся неоднозначности BLOCKED_CONTRACT. HUMAN/NATIVE/PROVIDER кейсы не записаны pure PASS.

### COMMON-01

- Source premise: Duplicate keys, unknown/missing keys, null mandatory value, float/exponent/NaN, bool вместо Int, invalid UTF-8/surrogate
- Source oracle (unchanged): DENY/PG_FORMAT до digest или provider IO; ни coercion, ни normalization
- Type: PURE.
- Exact isolated-cause codes / result: PG_FORMAT.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### COMMON-02

- Source premise: PG-C14N key order/whitespace вариации JSON; alternate input encoding после parse
- Source oracle (unchanged): Fixed canonical bytes одинаковы для равных values, arrays order preserved. Envelope contract/id/revision/mode меняются → digest меняется
- Type: PURE.
- Exact isolated-cause codes / result: NONE (canonical bytes control).
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### COMMON-03

- Source premise: `é` против `e`+combining accent, escaped controls/backslash/quote, empty/oversize string
- Source oracle (unchanged): Никакого Unicode normalization; raw files хешируются как raw; invalid/oversize deny, валидно разные values дают разные canonical bytes
- Type: PURE.
- Exact isolated-cause codes / result: PG_FORMAT for invalid/oversized; NONE for distinct valid normalization forms.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### COMMON-04

- Source premise: Limits ровно boundary, boundary+1, deep/huge input и oversized ByteRef stream
- Source oracle (unchanged): Boundary allowed только при других valid условиях; overflow PG_FORMAT. Prefix hash не выдаётся за whole-file digest
- Type: PURE.
- Exact isolated-cause codes / result: PG_FORMAT at +1; NONE at boundary under approved profile.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### COMMON-05

- Source premise: Перемешать Git SHA1, G2 wire hash, raw SHA256 и PG envelope digest; self-hash inclusion
- Source oracle (unchanged): PG_DIGEST/PG_REFERENCE. Fixed domain prefix/NUL и исключение только binding_sha256 проверены independently
- Type: PURE.
- Exact isolated-cause codes / result: PG_DIGEST for own local binding mismatch; PG_REFERENCE for wrong target.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### COMMON-06

- Source premise: Исключения/provider unavailable/произвольные exception strings/paths с private input
- Source oracle (unchanged): DENY/PG_DEPENDENCY_UNAVAILABLE либо stage-specific fixed code; без private echo, без permission/render side effects
- Type: PURE.
- Exact isolated-cause codes / result: PG_DEPENDENCY_UNAVAILABLE for provider failure; stage mapping OPEN.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-01

- Source premise: Полный snapshot: exact original bytes, pinned source/tools/context, реальные evaluator/Projection, оба плана и досье
- Source oracle (unchanged): CONSISTENT_NO_AUTHORITY; exact hashes/refs, исходный input неизменен; ноль render calls
- Type: PURE.
- Exact isolated-cause codes / result: NONE only if full admissibility context specified; otherwise BLOCKED_CONTRACT.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-02

- Source premise: Передать G2 code-only diagnostics export как full_evaluation; оригинальные inputs отсутствуют
- Source oracle (unchanged): PG_EVALUATION/PG_REFERENCE; нельзя угадывать поля, выдавать реконструкцию за original result или обходить PD-01
- Type: PURE.
- Exact isolated-cause codes / result: PG_EVALUATION for redacted full result; PG_REFERENCE for missing original.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-03

- Source premise: Реальные INVALID/STALE/FAILED/NOT_RUN, missing ratings/findings, CURRENT несогласован с context
- Source oracle (unchanged): PG_EVALUATION либо PG_STALE; no fake eligibility/score, no authorization candidate
- Type: PURE.
- Exact isolated-cause codes / result: PG_STALE for STALE; PG_EVALUATION for other rejected states.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-04

- Source premise: Full result изменён по одному полю/diagnostic slot; устаревший head/expiry; UNAVAILABLE card
- Source oracle (unchanged): Association/PG_STALE failure, trusted head mismatch не «исправляется» recomputed replacement внутри approved snapshot
- Type: PURE.
- Exact isolated-cause codes / result: PG_EVALUATION tampered result; PG_STALE head/expiry; PG_REFERENCE missing card.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-05

- Source premise: Изменить один source byte, authored text/whitespace, plan, asset, policy или source commit при старом snapshot ref
- Source oracle (unchanged): PG_DIGEST/PG_REFERENCE; новый snapshot identity и новое review, no inherited approval
- Type: PURE.
- Exact isolated-cause codes / result: PG_DIGEST changed bytes; PG_REFERENCE wrong bound ref.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-06

- Source premise: Частичный/malformed draft, missing UK, неподготовленный required visual
- Source oracle (unchanged): PG_PRODUCT_GAP/PG_REFERENCE; форматная валидность одного RU плана не достаточна
- Type: PURE.
- Exact isolated-cause codes / result: PG_PRODUCT_GAP partial plan; PG_REFERENCE missing dependency.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-07

**OWNER_APPROVED EFFECTIVE ADDENDUM:** Empty Text branch effective PG_FORMAT(stage2), nonempty insufficient branch PG_PRODUCT_GAP(stage6), X01 owner-approved; old source expectation preserved.

- Source premise: Metadata topic/audience не соответствует SI claim/evidence; why_film пуст/досье формально заполнено без central evidence
- Source oracle (unchanged): PG_PRODUCT_GAP при проверяемом missing/mismatch; substantive suitability требует PRODUCT human tests, не invented semantic judgment
- Type: PURE.
- Exact isolated-cause codes / result: BLOCKED_CONTRACT X01: PG_FORMAT versus PG_PRODUCT_GAP for empty Text.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P01-08

- Source premise: Same original invocation дважды, разные timestamps/контекст; отсутствует pinned evaluator runtime
- Source oracle (unchanged): Deterministic same inputs/context; revision/time changes bind новый envelope. Unavailable dependency → deny, no fallback runtime/latest
- Type: PURE.
- Exact isolated-cause codes / result: PG_DEPENDENCY_UNAVAILABLE missing runtime; NONE for deterministic exact repeat.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P02-01

- Source premise: Authentic review receipt exact SubjectKey; потом сменить snapshot/plan/asset/use/policy
- Source oracle (unchanged): Первый pure case consistent only; изменение key → PG_REFERENCE/PG_AUTHORITY, no перенос approval
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_REFERENCE changed SubjectKey; NONE only with specified context.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-02

- Source premise: Valid SID/UID/display actor/signature-shaped fields без trusted identity receipt; другой OS principal
- Source oracle (unchanged): PG_IDENTITY; строка/подпись без trusted key/identity не доказательство, no local-user all-rights default
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_IDENTITY.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-03

- Source premise: Missing per-gate/per-decision permission, неверный review kind/session, unchecked declarations/показан другой текст
- Source oracle (unchanged): PG_AUTHORITY/PG_PRODUCT_GAP; human-only acknowledgment нельзя автоматически дорисовать
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_AUTHORITY missing grant/session; PG_PRODUCT_GAP missing explicit review.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-04

**OWNER_APPROVED EFFECTIVE ADDENDUM:** Cycle test model now X03 separated; revision mismatch does not establish crypto-valid cycle coverage.

- Source premise: Неполный predecessor graph, cross-key/self/dangling ref, одинаковые timestamps, conflicting heads
- Source oracle (unchanged): PG_HISTORY; timestamp/UUID/array order не выбирают latest
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_HISTORY (isolated history), cycle fixture staging X03 OPEN.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-05

- Source premise: Old APPROVE против текущего REVOKE/REJECT/REVISE, rollback head, недоступен protected anchor
- Source oracle (unchanged): PG_REVOKED/PG_HISTORY/PG_DEPENDENCY_UNAVAILABLE, render zero
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_REVOKED negative latest; PG_HISTORY rollback; PG_DEPENDENCY_UNAVAILABLE outage.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-06

- Source premise: Истёк отрицательный event либо actor grant отозван; попытка resurrect prior APPROVE
- Source oracle (unchanged): PG_REVOKED/PG_AUTHORITY; expiry tombstone не восстанавливает старое решение
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_REVOKED tombstone; PG_AUTHORITY revoked actor grant.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-07

- Source premise: New authentic APPROVE с exact predecessor после revoke, неизменный subject; legacy evidence missing
- Source oracle (unchanged): Первый case требует explicit verified new history и нового admission, no auto retry; legacy не получает authority от migration
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_AUTHORITY for unauthenticated legacy; new valid event conditional NONE.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P02-08

- Source premise: Identity/history/session service outage, недоказанная scientific competence при required review
- Source oracle (unchanged): DENY, не cached approved=true. Scientific review и editorial role независимо соответствуют policy
- Type: PROVIDER.
- Exact isolated-cause codes / result: PG_DEPENDENCY_UNAVAILABLE unavailable provider; competence decision BLOCKED_CONTRACT.
- Dependencies: PG01, exact subject, identity/policy/session/history.
- Offline checkable: receipt fields/digests/exact references with explicit supplied context.
- Cannot prove offline: OS identity, latest head, authenticity, real human action.
- Implementation readiness: BLOCKED_CONTRACT / PROVIDER_POLICY_OPEN; no implementation authorized.

### P03-01

- Source premise: Полный actual asset manifest, все требуемые layers, authentic reviewer receipt и exact requested use
- Source oracle (unchanged): CONSISTENT_NO_AUTHORITY, no legal/production grant; exact coverage всех visual/audio/font/model assets
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: NONE only under explicit rights policy/context; BLOCKED_CONTRACT now.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-02

- Source premise: Подмена bytes при том же имени/id, omitted asset, лишний render asset/изменённое сценовое использование
- Source oracle (unchanged): PG_DIGEST/PG_RIGHTS/PG_REFERENCE; проверяется фактический closure, не caller subset
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_DIGEST changed bytes; PG_REFERENCE missing manifest ref; PG_RIGHTS wrong use.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-03

- Source premise: UNKNOWN/PENDING/REJECTED/DISPUTED, missing license copy/provenance/holder consent, report-only VERIFIED_EXTERNALLY
- Source oracle (unchanged): PG_RIGHTS; stored CONFIRMED digest не подменяет grant
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_RIGHTS.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-04

- Source premise: License разрешает только другое channel/territory/noncommercial/operation или не разрешает adaptation
- Source oracle (unchanged): PG_RIGHTS; intersection всех required layers, не union наиболее удобных условий
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_RIGHTS.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-05

- Source premise: Music composition без master/sync; voice без consent; model name без exact weights/terms; generated label без basis
- Source oracle (unchanged): PG_RIGHTS. Required layers задаёт reviewed policy, не пустой список или N/A от caller
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_RIGHTS if policy requires missing layer; applicability BLOCKED_CONTRACT.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-06

- Source premise: now==valid_until, clock rollback/uncertainty, срок не покрывает выбранный use, поздний dispute
- Source oracle (unchanged): PG_EXPIRED/PG_RIGHTS/PG_DEPENDENCY_UNAVAILABLE; expiry exclusive, fail closed
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_EXPIRED at expiry; PG_DEPENDENCY_UNAVAILABLE uncertain clock; PG_RIGHTS dispute.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-07

- Source premise: Attribution заявлена, но отсутствует в plan/output; публикация по render-only scope
- Source oracle (unchanged): PG_RIGHTS/PG_SCOPE; итоговый attribution и intended-use coverage проверяются отдельно
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_RIGHTS attribution; PG_SCOPE publication by render-only request.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P03-08

- Source premise: Wrong reviewer role/session/head/receipt либо старый rights review при новом asset/use
- Source oracle (unchanged): PG_AUTHORITY/PG_HISTORY/PG_RIGHTS; review не наследуется и не выдумывается
- Type: HUMAN / PROVIDER.
- Exact isolated-cause codes / result: PG_AUTHORITY role/receipt; PG_HISTORY wrong head; PG_RIGHTS stale scope.
- Dependencies: asset bytes, license layers/intended-use policy, rights reviewer.
- Offline checkable: hash/coverage/subset относительно supplied policy.
- Cannot prove offline: юридическая действительность/согласие/current dispute.
- Implementation readiness: BLOCKED_CONTRACT / RIGHTS_POLICY_OPEN; no implementation authorized.

### P04-01

**OWNER_APPROVED EFFECTIVE ADDENDUM:** Mode error precedence now X02 seven stages; use V039/V071/V073 for isolated early/mode causes. No production effects.

- Source premise: SyntheticRenderPermitV1/D1 manifest под видом PG grant; PREVIEW_ONLY или PRODUCTION_CANDIDATE flags сами по себе
- Source oracle (unchanged): PG_MODE/PG_SCOPE, ноль production renders. Даже valid PG request даёт pure consistency only
- Type: PURE.
- Exact isolated-cause codes / result: PG_MODE/PG_SCOPE selection BLOCKED_CONTRACT X02; production effects always forbidden.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P04-02

**OWNER_APPROVED EFFECTIVE ADDENDUM:** X04 explicit plan refs mandatory in proposed new version; old SubjectKey differs when either changes; purely technical reapproval remains OPEN.

- Source premise: Смена locale/scene/text/assets/audio/tools/config/profile/output set/operation после approval
- Source oracle (unchanged): PG_REFERENCE/PG_SCOPE/PG_TOOLCHAIN; новое bound request/review, no implicit widening/delegation
- Type: PURE.
- Exact isolated-cause codes / result: PG_REFERENCE subject mismatch; PG_SCOPE scope widening; PG_TOOLCHAIN mismatch; placement X04 OPEN.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P04-03

- Source premise: Revoked/expired approvals/rights, changed policy/head, future not_before или истёкший request
- Source oracle (unchanged): DENY before reserve/spawn; проверка actual trusted latest state до запуска и перед final commit
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_REVOKED revoked; PG_EXPIRED time; PG_HISTORY changed head; clock/provider assumptions OPEN.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P04-04

- Source premise: Два одновременных consume одного full request; request_id повторно с другими bytes
- Source oracle (unchanged): Не более одного admitted attempt; второй conflict/replay deny. Это ledger/OS test, не доказуемо pure dict
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_REPLAY rejected duplicate/conflict; at-most-one reserve requires actual ledger.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P04-05

- Source premise: Crash после reserve/до spawn, во время render, после outputs/до commit; restart с lost ACK
- Source oracle (unchanged): UNKNOWN/INDETERMINATE или verified terminal lookup; no automatic rerender, no reclaimed single-use token
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: INDETERMINATE evidence outcome, not error code; operational handling BLOCKED_CONTRACT.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P04-06

- Source premise: Expiry/revocation/потеря freshness provider в процессе render
- Source oracle (unchanged): Cancel/quarantine, no SUCCEEDED commit/publish; observed state сохранён, неопределённое не превращается в успех
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_REVOKED/PG_EXPIRED by observed cause; INDETERMINATE when observation lost.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P04-07

- Source premise: POSIX symlink, Windows reparse/junction, dangling/ancestor redirect, parent swap после hash, UNC/device/mount changes
- Source oracle (unchanged): Qualified executor отказывает/держит правильные identities; no out-of-scope reads/writes. Native tests обязательны, повторные string checks не закрывают oracle
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_PATH for path qualification denial; PG_DIGEST substituted content.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P04-08

**OWNER_APPROVED EFFECTIVE ADDENDUM:** Actual binary/config/toolchain must equal exact plan-bound target; X04 no caller override. Operational NOT_QUALIFIED.

- Source premise: Другой binary с тем же version string, PATH/cwd tool swap, font/libass/config substitution
- Source oracle (unchanged): PG_TOOLCHAIN, no spawn; actual binary+configuration bytes должны совпасть profile
- Type: PURE.
- Exact isolated-cause codes / result: PG_TOOLCHAIN.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P04-09

- Source premise: Попытка напрямую вызвать first_video после pure consistency
- Source oracle (unchanged): Не заявлять enforced production boundary без guarded executor/profile. Разработать separate enforcement/test plan; existing CLI не считается защищённым
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: BLOCKED_CONTRACT: no guarded endpoint exists; no pure enforceability verdict.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P04-10

- Source premise: Все bytes consistent, но нет approved issuer/executor/clock/ledger/trust root
- Source oracle (unchanged): CONSISTENT_NO_AUTHORITY для pure, operational DENY/PG_DEPENDENCY_UNAVAILABLE. No fake provider, no production mode inferred
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: pure CONSISTENT_NO_AUTHORITY only when explicit context complete; operational PG_DEPENDENCY_UNAVAILABLE.
- Dependencies: PG01–03, issuer/clock/revocation/atomic ledger/executor.
- Offline checkable: request consistency/negative supplied-context model.
- Cannot prove offline: single-use, real paths/time/revocation/endpoint enforcement.
- Implementation readiness: BLOCKED_CONTRACT / OPERATIONAL_PROTOCOL_OPEN; no implementation authorized.

### P05-01

- Source premise: Actual input closure/toolchain и все RU/UK outputs; raw hashes и profile checks соответствуют
- Source oracle (unchanged): Structurally consistent evidence; trusted future production success требует admission/completion witness, не одного JSON
- Type: PURE.
- Exact isolated-cause codes / result: NONE for consistent evidence assertions, never authenticity/production permission.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P05-02

- Source premise: RU успешно, UK отсутствует/failed, wrong codecs/duration/subtitles, missing required project/attribution
- Source oracle (unchanged): FAILED/INCOMPLETE, no terminal SUCCEEDED; partial outputs не accepted deliverables
- Type: PURE.
- Exact isolated-cause codes / result: PG_INCOMPLETE missing output; PG_EXECUTION failed media profile; FAILED record may be consistent.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P05-03

- Source premise: Forced renderer error/cancel/диск full; capture/log/inspection failure
- Source oracle (unchanged): Actual failure/NOT_RUN checks, безопасные errors, private quarantine, no invented hashes/results
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_EXECUTION observed render failure; evidence may record FAILED/CANCELLED, NOT_RUN checks.
- Dependencies: actual execution/output/index/ledger, privacy policy.
- Offline checkable: assertion/reference consistency.
- Cannot prove offline: real terminal commit/custody/atomicity.
- Implementation readiness: BLOCKED_CONTRACT / EVIDENCE_PROTOCOL_OPEN; no implementation authorized.

### P05-04

- Source premise: Truncated evidence JSON/index, missing completion marker/witness, orphan output files
- Source oracle (unchanged): INDETERMINATE/PG_EVIDENCE; no success по MP4 существованию
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_EVIDENCE malformed index; PG_INCOMPLETE missing terminal set; INDETERMINATE outcome.
- Dependencies: actual execution/output/index/ledger, privacy policy.
- Offline checkable: assertion/reference consistency.
- Cannot prove offline: real terminal commit/custody/atomicity.
- Implementation readiness: BLOCKED_CONTRACT / EVIDENCE_PROTOCOL_OPEN; no implementation authorized.

### P05-05

- Source premise: Crash между write/flush/index/head и restart; mismatched authoritative ledger/evidence head
- Source oracle (unchanged): Reconcile к verified terminal либо INDETERMINATE; не создать success receipt задним числом, no auto retry
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_HISTORY inconsistent ledger/head; INDETERMINATE until reconciled.
- Dependencies: actual execution/output/index/ledger, privacy policy.
- Offline checkable: assertion/reference consistency.
- Cannot prove offline: real terminal commit/custody/atomicity.
- Implementation readiness: BLOCKED_CONTRACT / EVIDENCE_PROTOCOL_OPEN; no implementation authorized.

### P05-06

- Source premise: Изменить MP4 после inspection или выдать JSON equality за binary equality
- Source oracle (unchanged): PG_DIGEST/PG_EVIDENCE; actual raw output read-back и immutable binding обязательны
- Type: PURE.
- Exact isolated-cause codes / result: PG_DIGEST changed actual bytes; PG_EVIDENCE unsupported manifest claim.
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### P05-07

- Source premise: Sensitive script/card/license/identity/raw stderr в public logs/upload; forged output_id/path
- Source oracle (unchanged): PG_SCOPE/PG_EVIDENCE; нет export без отдельного owner scope, no credentials/private exception echo
- Type: PROVIDER / NATIVE.
- Exact isolated-cause codes / result: PG_SCOPE forbidden disclosure; PG_EVIDENCE forged output identity.
- Dependencies: actual execution/output/index/ledger, privacy policy.
- Offline checkable: assertion/reference consistency.
- Cannot prove offline: real terminal commit/custody/atomicity.
- Implementation readiness: BLOCKED_CONTRACT / EVIDENCE_PROTOCOL_OPEN; no implementation authorized.

### P05-08

- Source premise: Evidence correction/retry выдать за старый execution; synthetic D1 manifest передать как PG05
- Source oracle (unchanged): PG_HISTORY/PG_MODE; immutable predecessor/revision и exact attempt, no type promotion и удаления failed history
- Type: PURE.
- Exact isolated-cause codes / result: PG_HISTORY wrong attempt/history; PG_MODE synthetic promotion (precedence X02 OPEN).
- Dependencies: exact bytes/schema/profile/context, source semantics.
- Offline checkable: canonical/reference/structural/model predicates.
- Cannot prove offline: authority/world truth/provider authenticity.
- Implementation readiness: CONDITIONAL SPEC READY; params/X issues remain NOT APPROVED; no implementation authorized.

### PRODUCT-01

- Source premise: Высокий SI score и все JSON поля, но неясно зачем тема аудитории
- Source oracle (unchanged): Editor не утверждает без why_film/audience rationale и grounds; score не автоматический green light
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### PRODUCT-02

- Source premise: Ссылки на источники без точных фрагментов, неверное support отношение/central contradiction
- Source oracle (unchanged): Claim-source review отклоняет неподтверждённое, не просто считает количество citations
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### PRODUCT-03

- Source premise: Hypothesis/factual central assertion без требуемой scientific review/qualification
- Source oracle (unchanged): Blocking research/scientific gap; disclosure/fiction classification не обходят реальные claims
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### PRODUCT-04

- Source premise: Требуется редкий обязательный visual, заменён случайным gradient/непроверенным stock
- Source oracle (unchanged): Нет утверждённой feasible/rights-complete сцены; нельзя имитировать factual evidence визуально
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### PRODUCT-05

- Source premise: Критический legal/reputation/scientific риск скрыт/снят без basis
- Source oracle (unchanged): Неполный dossier/approval deny; весь blocking set видим человеку без top-N masking
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### PRODUCT-06

- Source premise: LLM/actor display string объявлен редактором или reviewer без полномочий
- Source oracle (unchanged): Identity/authority/competence отдельно проверены; no automated human review claim
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### PRODUCT-07

- Source premise: Разрешены конкретные RU/UK тексты/asset set/local render, затем поменяли voice/crop/publish channel
- Source oracle (unchanged): Новые bindings/rights/human/admission scope; прежняя форма не даёт расширения производства
- Type: HUMAN.
- Exact isolated-cause codes / result: HUMAN finding (not pure machine verdict); recorded unmet condition propagates proposed PG_PRODUCT_GAP/PG_AUTHORITY by cause.
- Dependencies: competent editor/scientific reviewer, real evidence, explicit policy.
- Offline checkable: coverage/pointers/formal completeness.
- Cannot prove offline: содержательная пригодность, competence, факт истины.
- Implementation readiness: BLOCKED_CONTRACT / HUMAN_REVIEW_REQUIRED; no implementation authorized.

### NATIVE-01

- Source premise: Реальная Windows10/11/POSIX path/runtime identity adversarial matrix
- Source oracle (unchanged): Только отдельно approved host/profile/API observations/independent observer; skip не native PASS
- Type: NATIVE.
- Exact isolated-cause codes / result: PG_PATH or PG_TOOLCHAIN by isolated failing boundary; no offline native result.
- Dependencies: qualified selected host/OS/runtime/storage/observer.
- Offline checkable: только входные bytes/relations и план проверки.
- Cannot prove offline: реальное enforcement, crash/durability/identity.
- Implementation readiness: BLOCKED_CONTRACT / HOST_NOT_QUALIFIED; no implementation authorized.

### NATIVE-02

- Source premise: Atomic single-attempt ledger и evidence durability/rollback/crash matrix
- Source oracle (unchanged): Pure RAM/fixtures не evidence реального диска/OS; process crash не power-loss qualification
- Type: NATIVE.
- Exact isolated-cause codes / result: PG_HISTORY/PG_EVIDENCE by failed invariant; outcome may be INDETERMINATE.
- Dependencies: qualified selected host/OS/runtime/storage/observer.
- Offline checkable: только входные bytes/relations и план проверки.
- Cannot prove offline: реальное enforcement, crash/durability/identity.
- Implementation readiness: BLOCKED_CONTRACT / HOST_NOT_QUALIFIED; no implementation authorized.

### NATIVE-03

- Source premise: Identity/revocation/clock/privacy/access/retention boundary
- Source oracle (unchanged): Независимый authenticated provider/audit, bounded visibility, unavailable→deny; никаких настоящих credentials в тестовых Git artifacts
- Type: NATIVE.
- Exact isolated-cause codes / result: PG_IDENTITY/PG_REVOKED/PG_DEPENDENCY_UNAVAILABLE/PG_SCOPE by cause; no pure proof.
- Dependencies: qualified selected host/OS/runtime/storage/observer.
- Offline checkable: только входные bytes/relations и план проверки.
- Cannot prove offline: реальное enforcement, crash/durability/identity.
- Implementation readiness: BLOCKED_CONTRACT / HOST_NOT_QUALIFIED; no implementation authorized.

## Conservation check и связи с vectors

Ровно58 unique IDs: COMMON6, P01=8, P02=8, P03=8, P04=10, P05=8, PRODUCT7, NATIVE3. Тексты premise/expectation сверены с source по ID, не перефразированы как будто approved resolution. Vector70 покрывают byte-level fixtures/negative probes и proposed limits; это **не**70 выполненных PG tests и не executable coverage всех58. HUMAN/provider/native coverage остаётся requirements-only; нет фиктивного offline PASS.

Связи: COMMON01–05 ↔ V001–040,V044–070; reference registry ↔ V022,V041,V042; unresolved cycle ↔ V043; P01-07 ambiguity ↔ V051; P04 mode precedence ↔ V039. P02/03/04 operational/P05/HUMAN/NATIVE требуют будущих independently designed real evidence/context fixtures после owner решения. Их отсутствие явно BLOCKED_CONTRACT, не заменяется arithmetic vectors.

## Evidence and implementation boundary

No PG semantic validator/provider run: expected error descriptions alone are not verified semantic results. BYTES_VERIFIED/HASH_VERIFIED come from full byte/canonical/hash controls. STRUCTURAL_ORACLE_VERIFIED only applies to seven abstract graph fixtures checked by actual independent DFS/Kahn and revision controls. PG_SEMANTIC_NOT_RUN, NATIVE_NOT_RUN, OPERATIONAL_NOT_QUALIFIED remain explicit. Original70 vector IDs and58 oracle IDs retained; OP document unchanged byte-for-byte. No new PG Error.code, result namespace, actual grant or final freeze.
