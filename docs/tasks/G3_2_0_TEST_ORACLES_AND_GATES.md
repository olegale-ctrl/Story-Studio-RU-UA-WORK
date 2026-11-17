# G3.2.0 — test oracles, qualification gates и STOP

**PROPOSAL — OWNER REVIEW REQUIRED.** 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

Это требования к будущим независимым тестам; **все PG executable tests — NOT_RUN, реализация отсутствует**. Таблицы не являются новым PASS report и не разрешают следующий этап. [Schemas и ErrorCode](G3_2_0_PRODUCTION_GATE_CONTRACT_PROPOSAL.md), [threats/rights](G3_2_0_SECURITY_AND_RIGHTS_MATRIX.md), [owner choices](G3_2_0_OWNER_DECISIONS.md).

## 1. Общий oracle protocol

Каждый negative case меняет ровно указанную предпосылку независимо от других valid данных. Expected error указан при остальных valid prerequisites; при нескольких дефектах действует порядок ошибок из PG contract. Во всех pure tests: no filesystem/network/subprocess/clock/identity reads или writes; explicit immutable inputs/context, detached deterministic output, zero render/permission effects. Positive pure result — **CONSISTENT_NO_AUTHORITY**, никогда grant/ALLOW_RENDER. В operational tests проверять **нулевой spawn/render/consume** на отказе, а не только возвращённый error string.

Независимые fixed expected bytes/digests формируются после утверждения PG-C14N и schema, не вычисляются тем же production serializer под видом golden oracle. Не использовать нулевые/выдуманные hashes как proof. Сравнивать exact codes, порядок, refs, privacy и counts; каждый skipped case явно отдельно. Provider test doubles доказывают только protocol control flow, не native identity/storage/clock qualification.

| ID | Будущая проверка | Expected oracle PROPOSAL |
|---|---|---|
| COMMON-01 | Duplicate keys, unknown/missing keys, null mandatory value, float/exponent/NaN, bool вместо Int, invalid UTF-8/surrogate | DENY/PG_FORMAT до digest или provider IO; ни coercion, ни normalization |
| COMMON-02 | PG-C14N key order/whitespace вариации JSON; alternate input encoding после parse | Fixed canonical bytes одинаковы для равных values, arrays order preserved. Envelope contract/id/revision/mode меняются → digest меняется |
| COMMON-03 | `é` против `e`+combining accent, escaped controls/backslash/quote, empty/oversize string | Никакого Unicode normalization; raw files хешируются как raw; invalid/oversize deny, валидно разные values дают разные canonical bytes |
| COMMON-04 | Limits ровно boundary, boundary+1, deep/huge input и oversized ByteRef stream | Boundary allowed только при других valid условиях; overflow PG_FORMAT. Prefix hash не выдаётся за whole-file digest |
| COMMON-05 | Перемешать Git SHA1, G2 wire hash, raw SHA256 и PG envelope digest; self-hash inclusion | PG_DIGEST/PG_REFERENCE. Fixed domain prefix/NUL и исключение только binding_sha256 проверены independently |
| COMMON-06 | Исключения/provider unavailable/произвольные exception strings/paths с private input | DENY/PG_DEPENDENCY_UNAVAILABLE либо stage-specific fixed code; без private echo, без permission/render side effects |

## 2. PG-01 оракулы

| ID | Case | Expected oracle PROPOSAL |
|---|---|---|
| P01-01 | Полный snapshot: exact original bytes, pinned source/tools/context, реальные evaluator/Projection, оба плана и досье | CONSISTENT_NO_AUTHORITY; exact hashes/refs, исходный input неизменен; ноль render calls |
| P01-02 | Передать G2 code-only diagnostics export как full_evaluation; оригинальные inputs отсутствуют | PG_EVALUATION/PG_REFERENCE; нельзя угадывать поля, выдавать реконструкцию за original result или обходить PD-01 |
| P01-03 | Реальные INVALID/STALE/FAILED/NOT_RUN, missing ratings/findings, CURRENT несогласован с context | PG_EVALUATION либо PG_STALE; no fake eligibility/score, no authorization candidate |
| P01-04 | Full result изменён по одному полю/diagnostic slot; устаревший head/expiry; UNAVAILABLE card | Association/PG_STALE failure, trusted head mismatch не «исправляется» recomputed replacement внутри approved snapshot |
| P01-05 | Изменить один source byte, authored text/whitespace, plan, asset, policy или source commit при старом snapshot ref | PG_DIGEST/PG_REFERENCE; новый snapshot identity и новое review, no inherited approval |
| P01-06 | Частичный/malformed draft, missing UK, неподготовленный required visual | PG_PRODUCT_GAP/PG_REFERENCE; форматная валидность одного RU плана не достаточна |
| P01-07 | Metadata topic/audience не соответствует SI claim/evidence; why_film пуст/досье формально заполнено без central evidence | PG_PRODUCT_GAP при проверяемом missing/mismatch; substantive suitability требует PRODUCT human tests, не invented semantic judgment |
| P01-08 | Same original invocation дважды, разные timestamps/контекст; отсутствует pinned evaluator runtime | Deterministic same inputs/context; revision/time changes bind новый envelope. Unavailable dependency → deny, no fallback runtime/latest |

## 3. PG-02 оракулы

| ID | Case | Expected oracle PROPOSAL |
|---|---|---|
| P02-01 | Authentic review receipt exact SubjectKey; потом сменить snapshot/plan/asset/use/policy | Первый pure case consistent only; изменение key → PG_REFERENCE/PG_AUTHORITY, no перенос approval |
| P02-02 | Valid SID/UID/display actor/signature-shaped fields без trusted identity receipt; другой OS principal | PG_IDENTITY; строка/подпись без trusted key/identity не доказательство, no local-user all-rights default |
| P02-03 | Missing per-gate/per-decision permission, неверный review kind/session, unchecked declarations/показан другой текст | PG_AUTHORITY/PG_PRODUCT_GAP; human-only acknowledgment нельзя автоматически дорисовать |
| P02-04 | Неполный predecessor graph, cross-key/self/dangling ref, одинаковые timestamps, conflicting heads | PG_HISTORY; timestamp/UUID/array order не выбирают latest |
| P02-05 | Old APPROVE против текущего REVOKE/REJECT/REVISE, rollback head, недоступен protected anchor | PG_REVOKED/PG_HISTORY/PG_DEPENDENCY_UNAVAILABLE, render zero |
| P02-06 | Истёк отрицательный event либо actor grant отозван; попытка resurrect prior APPROVE | PG_REVOKED/PG_AUTHORITY; expiry tombstone не восстанавливает старое решение |
| P02-07 | New authentic APPROVE с exact predecessor после revoke, неизменный subject; legacy evidence missing | Первый case требует explicit verified new history и нового admission, no auto retry; legacy не получает authority от migration |
| P02-08 | Identity/history/session service outage, недоказанная scientific competence при required review | DENY, не cached approved=true. Scientific review и editorial role независимо соответствуют policy |

## 4. PG-03 оракулы

| ID | Case | Expected oracle PROPOSAL |
|---|---|---|
| P03-01 | Полный actual asset manifest, все требуемые layers, authentic reviewer receipt и exact requested use | CONSISTENT_NO_AUTHORITY, no legal/production grant; exact coverage всех visual/audio/font/model assets |
| P03-02 | Подмена bytes при том же имени/id, omitted asset, лишний render asset/изменённое сценовое использование | PG_DIGEST/PG_RIGHTS/PG_REFERENCE; проверяется фактический closure, не caller subset |
| P03-03 | UNKNOWN/PENDING/REJECTED/DISPUTED, missing license copy/provenance/holder consent, report-only VERIFIED_EXTERNALLY | PG_RIGHTS; stored CONFIRMED digest не подменяет grant |
| P03-04 | License разрешает только другое channel/territory/noncommercial/operation или не разрешает adaptation | PG_RIGHTS; intersection всех required layers, не union наиболее удобных условий |
| P03-05 | Music composition без master/sync; voice без consent; model name без exact weights/terms; generated label без basis | PG_RIGHTS. Required layers задаёт reviewed policy, не пустой список или N/A от caller |
| P03-06 | now==valid_until, clock rollback/uncertainty, срок не покрывает выбранный use, поздний dispute | PG_EXPIRED/PG_RIGHTS/PG_DEPENDENCY_UNAVAILABLE; expiry exclusive, fail closed |
| P03-07 | Attribution заявлена, но отсутствует в plan/output; публикация по render-only scope | PG_RIGHTS/PG_SCOPE; итоговый attribution и intended-use coverage проверяются отдельно |
| P03-08 | Wrong reviewer role/session/head/receipt либо старый rights review при новом asset/use | PG_AUTHORITY/PG_HISTORY/PG_RIGHTS; review не наследуется и не выдумывается |

## 5. PG-04 оракулы

| ID | Case | Expected oracle PROPOSAL |
|---|---|---|
| P04-01 | SyntheticRenderPermitV1/D1 manifest под видом PG grant; PREVIEW_ONLY или PRODUCTION_CANDIDATE flags сами по себе | PG_MODE/PG_SCOPE, ноль production renders. Даже valid PG request даёт pure consistency only |
| P04-02 | Смена locale/scene/text/assets/audio/tools/config/profile/output set/operation после approval | PG_REFERENCE/PG_SCOPE/PG_TOOLCHAIN; новое bound request/review, no implicit widening/delegation |
| P04-03 | Revoked/expired approvals/rights, changed policy/head, future not_before или истёкший request | DENY before reserve/spawn; проверка actual trusted latest state до запуска и перед final commit |
| P04-04 | Два одновременных consume одного full request; request_id повторно с другими bytes | Не более одного admitted attempt; второй conflict/replay deny. Это ledger/OS test, не доказуемо pure dict |
| P04-05 | Crash после reserve/до spawn, во время render, после outputs/до commit; restart с lost ACK | UNKNOWN/INDETERMINATE или verified terminal lookup; no automatic rerender, no reclaimed single-use token |
| P04-06 | Expiry/revocation/потеря freshness provider в процессе render | Cancel/quarantine, no SUCCEEDED commit/publish; observed state сохранён, неопределённое не превращается в успех |
| P04-07 | POSIX symlink, Windows reparse/junction, dangling/ancestor redirect, parent swap после hash, UNC/device/mount changes | Qualified executor отказывает/держит правильные identities; no out-of-scope reads/writes. Native tests обязательны, повторные string checks не закрывают oracle |
| P04-08 | Другой binary с тем же version string, PATH/cwd tool swap, font/libass/config substitution | PG_TOOLCHAIN, no spawn; actual binary+configuration bytes должны совпасть profile |
| P04-09 | Попытка напрямую вызвать first_video после pure consistency | Не заявлять enforced production boundary без guarded executor/profile. Разработать separate enforcement/test plan; existing CLI не считается защищённым |
| P04-10 | Все bytes consistent, но нет approved issuer/executor/clock/ledger/trust root | CONSISTENT_NO_AUTHORITY для pure, operational DENY/PG_DEPENDENCY_UNAVAILABLE. No fake provider, no production mode inferred |

## 6. PG-05 оракулы

| ID | Case | Expected oracle PROPOSAL |
|---|---|---|
| P05-01 | Actual input closure/toolchain и все RU/UK outputs; raw hashes и profile checks соответствуют | Structurally consistent evidence; trusted future production success требует admission/completion witness, не одного JSON |
| P05-02 | RU успешно, UK отсутствует/failed, wrong codecs/duration/subtitles, missing required project/attribution | FAILED/INCOMPLETE, no terminal SUCCEEDED; partial outputs не accepted deliverables |
| P05-03 | Forced renderer error/cancel/диск full; capture/log/inspection failure | Actual failure/NOT_RUN checks, безопасные errors, private quarantine, no invented hashes/results |
| P05-04 | Truncated evidence JSON/index, missing completion marker/witness, orphan output files | INDETERMINATE/PG_EVIDENCE; no success по MP4 существованию |
| P05-05 | Crash между write/flush/index/head и restart; mismatched authoritative ledger/evidence head | Reconcile к verified terminal либо INDETERMINATE; не создать success receipt задним числом, no auto retry |
| P05-06 | Изменить MP4 после inspection или выдать JSON equality за binary equality | PG_DIGEST/PG_EVIDENCE; actual raw output read-back и immutable binding обязательны |
| P05-07 | Sensitive script/card/license/identity/raw stderr в public logs/upload; forged output_id/path | PG_SCOPE/PG_EVIDENCE; нет export без отдельного owner scope, no credentials/private exception echo |
| P05-08 | Evidence correction/retry выдать за старый execution; synthetic D1 manifest передать как PG05 | PG_HISTORY/PG_MODE; immutable predecessor/revision и exact attempt, no type promotion и удаления failed history |

## 7. Product, native и независимые проверки

| ID | Содержательный case | Expected review criterion PROPOSAL |
|---|---|---|
| PRODUCT-01 | Высокий SI score и все JSON поля, но неясно зачем тема аудитории | Editor не утверждает без why_film/audience rationale и grounds; score не автоматический green light |
| PRODUCT-02 | Ссылки на источники без точных фрагментов, неверное support отношение/central contradiction | Claim-source review отклоняет неподтверждённое, не просто считает количество citations |
| PRODUCT-03 | Hypothesis/factual central assertion без требуемой scientific review/qualification | Blocking research/scientific gap; disclosure/fiction classification не обходят реальные claims |
| PRODUCT-04 | Требуется редкий обязательный visual, заменён случайным gradient/непроверенным stock | Нет утверждённой feasible/rights-complete сцены; нельзя имитировать factual evidence визуально |
| PRODUCT-05 | Критический legal/reputation/scientific риск скрыт/снят без basis | Неполный dossier/approval deny; весь blocking set видим человеку без top-N masking |
| PRODUCT-06 | LLM/actor display string объявлен редактором или reviewer без полномочий | Identity/authority/competence отдельно проверены; no automated human review claim |
| PRODUCT-07 | Разрешены конкретные RU/UK тексты/asset set/local render, затем поменяли voice/crop/publish channel | Новые bindings/rights/human/admission scope; прежняя форма не даёт расширения производства |
| NATIVE-01 | Реальная Windows10/11/POSIX path/runtime identity adversarial matrix | Только отдельно approved host/profile/API observations/independent observer; skip не native PASS |
| NATIVE-02 | Atomic single-attempt ledger и evidence durability/rollback/crash matrix | Pure RAM/fixtures не evidence реального диска/OS; process crash не power-loss qualification |
| NATIVE-03 | Identity/revocation/clock/privacy/access/retention boundary | Независимый authenticated provider/audit, bounded visibility, unavailable→deny; никаких настоящих credentials в тестовых Git artifacts |

## 8. Gates и последовательность без реализации

| Gate | Что должно быть принято/проверено | Сейчас |
|---|---|---|
| G-PG-DISCOVERY | Exact base, пять согласованных PROPOSAL документов, независимый ChatGPT review и owner choices | Пакет подготовлен к review; review/approval ещё не выполнены |
| G-PG-SCHEMA | Owner утверждает canonicalization/limits/types/error namespace/subject keys и scope | PROPOSAL; не approved wire contract |
| G-PG-PURE | Отдельное задание только на pure validators/independent goldens; COMMON/P01–P05 контракты без grants/IO | NOT_AUTHORIZED / NOT_RUN |
| G-PG-HUMAN-RIGHTS | Утверждены roles/competence/sessions, legal intended-use/layers, product acceptance procedure | Решения открыты; реальные approvals/rights не предоставлены |
| G-PG-TRUST | Выбран и qualified identity/authority/head/time/revocation/anti-replay provider, rollback semantics | BLOCKED; source S3 PURE_ONLY не закрывает |
| G-PG-EXECUTOR | Отдельный guarded endpoint/runtime/profile, input handles, immutable resources, revocation/expiry supervision | BLOCKED; existing first_video не этот endpoint |
| G-PG-EVIDENCE | Atomic index/state/output commit, failure/recovery/custody/privacy и actual hashes | BLOCKED; D1 manifest не подмена |
| G-PG-PRODUCTION | Owner отдельно утверждает production mode, exact materials/people/use/grant и профиль на qualified host | BLOCKED / NOT_AUTHORIZED |
| G-PG-EXPORT | Отдельный допуск на публикацию/распространение outputs/evidence | NOT_AUTHORIZED; no workflow/upload changes |

Возможная последовательность **PROPOSAL**: независимый review → owner фиксирует choices → отдельный schema-freeze/docs task → при явном разрешении pure-only implementation/tests → отдельная квалификация providers/OS/executor/evidence → отдельный scoped production authorization. Это не команда начать следующий шаг; переход между каждым gate требует отдельного решения. Если owner отложит trusted stack, остаются Preview/D1/diagnostics, без production.

## 9. Проверки текущего документационного задания

Выполнены Git/code/contract reads и фиксация refs; проверяются intra-package links, ID/cross-references, exact пять Markdown diff, отсутствие implementation/workflow/deferred imports, parent/tree/clean status и remote refs. Эти checks — документационная целостность, не executable PG tests. Unit/full/render/Windows/native/production tests в G3.2.0 **не запускались**. Исторический G3.1 CI указан в inventory как historical scoped evidence.

STOP: base/tree mismatch, необъяснённая schema/error/oracle ambiguity, попытка считать serialized proof trusted provider, source/deferred/G1/G2/G3.1 изменение, реальный production grant, запуск render/native/CI изменений или последующего implementation без нового поручения. При неизвестном состоянии не придумывать PASS/approval/terminal receipt.

**READY_FOR_OWNER_REVIEW относится только к пяти документам PROPOSAL. STOP для независимого ChatGPT аудита и решения владельца.**
