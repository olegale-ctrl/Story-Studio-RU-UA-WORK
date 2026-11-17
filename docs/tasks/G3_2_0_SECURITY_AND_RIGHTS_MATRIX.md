# G3.2.0 — threat model, права и границы доверия

**PROPOSAL — OWNER REVIEW REQUIRED.** 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

Ниже проект требований, не доказательство их реализации. Связанные документы: [PG contracts](G3_2_0_PRODUCTION_GATE_CONTRACT_PROPOSAL.md), [test oracles](G3_2_0_TEST_ORACLES_AND_GATES.md), [owner decisions](G3_2_0_OWNER_DECISIONS.md).

## 1. Активы, субъекты и доверительные границы

Защищаемые активы: exact editor input, SI refs/context/findings, полные evaluation/private cards, утверждённые RU/UK тексты и claim-source evidence, material/license bytes, human identity/decisions/revocations, policies/heads, authorization request/consume ledger, runtime/toolchain, output bytes и evidence index. Hash связывает bytes, но не конфиденциальность или разрешение.

Недоверенные стороны: входной JSON и файловые пути, подставленные `actor`/SID/verified flags, detached cards/manifests, license labels/URLs, пользовательские executable/PATH/config, PR artifacts, mutable директории и старые copies state. Потенциальный нарушитель может менять доступные файлы, повторять request, возвращать старый state head, замещать asset/tool, прерывать процессы. Даже добросовестный пользователь может ошибиться с scientific claim, сроком/территорией license или русско-украинским смыслом.

Будущие trusted roles требуют отдельной квалификации: editor/scientific reviewer, rights reviewer, identity+authority/session provider, current-state/revocation+clock provider, issuer, executor, immutable content/evidence custodian. Нельзя назначить trusted роль полем JSON или считать локального пользователя автоматически администратором всех gates. Разделение roles и self-approval policy — OD-PG-02/03.

Уровни защиты: **PURE** — проверка supplied bytes/структуры/отношений; **HUMAN** — фактическая компетентная оценка; **PROVIDER** — аутентифицированное актуальное состояние; **OS/EXECUTOR** — реальные файловые объекты/process/runtime; **STORAGE** — durability, atomic consume, rollback resistance. PURE PASS не доказывает остальные уровни.

## 2. Threat/control matrix

| ID | Угроза и последствие | Pure contract mitigation | Требует доверия вне pure | Fail-closed / оракулы |
|---|---|---|---|---|
| T01 | STALE/INVALID либо неправильный input/result association | PG01 exact invocation/full result, PD-01 re-evaluation, deny rejected/currentness mismatch | Trusted latest context и pinned runtime | PG_EVALUATION/PG_STALE; P01-02/03/04 |
| T02 | G2 redacted evaluation выдать за complete verified result | PG01 хранит distinct full result и redacted export; no reconstruction | Доступ к original bytes/approved evaluator | PG_REFERENCE/PG_EVALUATION; P01-02 |
| T03 | Изменить текст/topic/plan после approval | SubjectKey включает snapshot/plan/assets/use/policy; byte/hash mismatch deny | Immutable resolver и проверка consumed bytes в executor | PG_DIGEST/PG_REFERENCE; P01-05, P02-01, P04-02 |
| T04 | Подменить asset с тем же filename или license другого файла | PG03 exact material bytes, complete manifest, coverage и layers | Trusted opened content objects, actual legal provenance | PG_RIGHTS/PG_DIGEST; P03-01/02, P04-07 |
| T05 | Непроверенный URL/VERIFIED_EXTERNALLY/CONFIRMED принять за rights | Запрет label-as-authority, required evidence refs и usage intersection | Competent rights reviewer; actual holder/consent/terms verification | PG_RIGHTS; P03-03/04/05 |
| T06 | Поддельный actor/SID/signature или клик «approve» | Структура actor/session/policy, receipt binding, exact subject | OS identity, trusted grants, protected review session; ключевой registry для signatures | PG_IDENTITY/PG_AUTHORITY; P02-02/03 |
| T07 | Использовать отменённый APPROVE/старый policy head | Exact predecessor/head/epoch и отсутствие latest fallback | Authoritative revocation/history, anti-rollback anchor, outage deny | PG_REVOKED/PG_HISTORY; P02-04/05/06, P04-03 |
| T08 | Negative event expired → оживить более старое APPROVE | Tombstone semantics; no resurrection без нового trusted event | Durable complete history, authenticated ordering | PG_REVOKED; P02-06 |
| T09 | Replay/параллельный duplicate render или retry после crash | SINGLE_ATTEMPT, full request binding, scope invariants | Atomic durable reserve/consume, executor identity, restart reconciliation | PG_REPLAY/PG_HISTORY; P04-04/05 |
| T10 | Time rollback, expired rights/approval/auth, race срока | `[from,until)` и intersection, reject uncertain supplied clock | Trusted clock + freshness/revocation monitoring; real finish-time check | PG_EXPIRED/PG_DEPENDENCY_UNAVAILABLE; P03-06, P04-03/06 |
| T11 | TOCTOU между check/hash/open/read/rename | Contract запрещает менять bindings и разрешать по пути | Handle/descriptor anchoring, private namespace, protected immutable objects, host qualification | PG_PATH/PG_DIGEST; P04-07 |
| T12 | Windows junction/reparse/UNC/device path/alternate stream | Не принимать caller paths как resolver, require qualified profile | Windows handle/reparse identity checks, ACL/runtime, approved local NTFS host | PG_PATH; P04-07, NATIVE-01 |
| T13 | Подмена FFmpeg/Python/fonts/config через PATH/cwd | PG04 exact artifacts/config hashes и closed profile | Pinned runtime/search paths/code integrity, version read от actual binary | PG_TOOLCHAIN; P04-08 |
| T14 | Сбой после RU до UK, out-of-space, partial output | PG05 exact required output set, complete flags, no partial success | Isolated staging/process supervision/cleanup, native failure observations | PG_INCOMPLETE/PG_EXECUTION; P05-02/03 |
| T15 | Частичный/truncated evidence index, orphan MP4, crash after consume | PG05 head/index/bytes consistency, INDETERMINATE outcome | Atomic durable index/ledger commit и independent completion witness | PG_EVIDENCE/PG_INCOMPLETE; P05-04/05, NATIVE-02 |
| T16 | SyntheticRenderPermitV1 выдать за PG04/production authority | Separate type/mode/domain; не конвертировать registered digest | Guarded executor и новая production policy; existing renderer bypass остаётся | PG_MODE/PG_SCOPE; P04-01 |
| T17 | Формально полный dossier скрывает ложный central thesis/непригодную тему | PG01 требует claims→fragments, visual/risk coverage; block unresolved gaps | Human editorial/scientific review с компетенцией; schema не truth oracle | PG_PRODUCT_GAP; PRODUCT-01…07 |
| T18 | Fake success manifest, изменённый MP4 после инспекции | PG05 raw hash/byte length/output ID и actual inspect refs | Authentic executor evidence, immutable committed outputs, independent verification | PG_EVIDENCE/PG_DIGEST; P05-01/06 |
| T19 | Выгрузка private cards/identity/licenses/MP4 в CI/public logs | Privacy classification и fixed errors; нет auto upload/export | Explicit reader/custody/retention/redaction/access controls | PG_SCOPE; P05-07, NATIVE-03 |
| T20 | Disabled provider/failure fallback доверяет cached «verified» | Explicit missing/unavailable provider → DENY, no bool override | Реальная доступность qualified providers/anchors | PG_DEPENDENCY_UNAVAILABLE; P02-08, P04-10 |
| T21 | Scope widening: render permission превратить в publish/commercial | PG04 только LOCAL_RENDER, no delegation/autorenewal; UseScope intersection | Independent usage enforcement/export authorization | PG_SCOPE/PG_RIGHTS; P03-04/07, P04-02 |
| T22 | Parser/canonical ambiguity, resource exhaustion, hostile errors | Duplicate/unknown keys, limits, no float/coercion/normalization; domain-separated hashes; fixed errors | Bounded resolver/process memory/file IO; privacy-safe logs | PG_FORMAT/PG_DIGEST; COMMON-01…06 |

Pure проверки stale/expiry/revocation выполняются **относительно supplied verified context**, не сами доказывают, что context свежий/подлинный. Test doubles/providers в unit tests не квалифицируют реальные доверительные границы. Не объявлять TOCTOU или native Windows проблему закрытой от lstat/recheck loop.

## 3. Asset rights: что требуется до real-material render

| Материал | Необходимые evidence/проверки PROPOSAL | Что не является разрешением |
|---|---|---|
| Фото/видео/иллюстрации | Exact bytes, provenance/holder, license copy, channel/territory/time/commercial/adaptation, model/property/privacy releases где применимы, attribution в output plan | Найдено в интернете; source citation; existing source/asset digest; «картинка для теста» |
| Музыка | Раздельно composition/master/recording/performance/sync и конкретный intended use/territory/term, атрибуция | Доступный MP3, покупка файла или одна general license label |
| Recorded voice/человек | Exact recording, speaker consent/privacy/personality/usage scope и license, where applicable | Технически валидный WAV, согласие на запись без согласия на использование |
| TTS/model/voice weights | Exact model/weights/hash/voice/version/terms, allowed commercial/domain/languages, source provenance, generated-output rights/restrictions | Optional Silero/Edge provider уже есть; модель называется commercial; известный license текста без проверки weights |
| Генерируемые фон/тишина/assets | Source/generator/config/actual output bytes, policy применимых rights layers и provenance; чужие основы/шрифты не скрывать | synthetic=true или GENERATED label сами по себе |
| Fonts/runtime/FFmpeg binaries | Exact tool/font bytes/config и применимые redistribution/use obligations; selected target fonts/codec support | Linux fallback font доказал доступность Windows Arial или право bundle/redistribute |
| Тексты/источники/фрагменты | Provenance, точные цитаты/claims, права на воспроизведение используемого текста; scientific review отдельно | Достоверный факт автоматически даёт права на фото/перевод/цитирование в любом объёме |

Scope проверяется по пересечению всех обязательных layers; UNKNOWN, dispute, expired или недоступная license copy блокируют соответствующий exact use. Human/legal judgment не заменяется алгоритмом. Copyright exceptions/public-domain claims требуют компетентного основания и jurisdiction policy, а не автоматического exemption flag. Территории и будущие способы распространения должны быть выбраны, не default worldwide.

Existing G2 rights states — reported-only; `editorial.rights_binding.MaterialBindingState.CONFIRMED` — matching stored digest only. PG-03 не переопределяет A14: HANDOFF остаётся editorial-only. Editorial approval, scientific review, rights review и render issuance — разные полномочия; возможное совмещение человеком требует explicit policy, не silent self-approval.

## 4. Продуктовый критерий: форма не заменяет пригодность

| Вопрос продукта | Proposed binding / human responsibility | Blocking пример |
|---|---|---|
| Почему стоит снимать? | PG01 why_film + audience_need + novelty basis; PG02 editor reason/review exact dossier | Хорошо сформированный plan не отвечает на зрительский вопрос; высокий SI score единственное основание |
| Что поддерживает сценарий? | ClaimLink с exact script span, SourceFragment locator/retrieved_at/bytes/отношением, explicit contrary evidence | «Источники есть» без фрагментов/claim mapping; источник поддерживает другое утверждение |
| Что требует научной проверки? | kind/central/review requirements, qualifications, competent PG02 SCIENTIFIC_REVIEW по policy | Central factual/hypothesis assertion unresolved; caption выдаёт гипотезу за факт |
| Какие визуальные материалы обязательны? | VisualNeed→scene→asset IDs, feasibility evidence, PG03 exact rights coverage | Требуемый archive shot отсутствует/нет прав; random gradient выдан за выполненный historical visual |
| Какие риски остаются? | Full Risk list, blocking/severity/basis/mitigation; человек видит unresolved ограничения | Неудобный risk удалён из карточки, скрыт top-N или mitigation — только красивый текст |
| Кто принял решение? | PG02 exact ActorRef/session/authority receipt/history и reason; trusted identity | actor display string/LLM report автоматически объявлен human approval |
| Что отправляется в производство? | SubjectKey + PG04 full plan/assets/tools/use/output set + separate runtime admission | Любые новые файлы/язык/voice/scene/tools после approval; разрешение одного render использовано для публикации |

Pure validator может проверить, что поля/refs полны и взаимно согласованы. Он не должен автоматически «согласовать» тему, судить компетентность reviewer по строке или создавать недостающий научный вывод. Нужны содержательные human review процедуры, policy критериев и negative product oracles, а не схема с mandatory `why_film` как единственный gate. Fiction освобождает от выдумывания научных источников для явно fictional сцен, но не от review реальных утверждений и необходимых disclosures.

## 5. Storage/ОС/исполнитель — нерешённые обязательства

**S3 означает внутренний Windows protected-storage трек E01.3.9, не Amazon S3.** Base содержит protocol/model structures; deferred source имеет pure RAM transaction/LAB modules и исторический PURE_ONLY acceptance. Ни то ни другое не реализует authenticated current head, protected identity authority, anti-rollback ledger, NTFS writer/evidence atomicity или service trust.

Для future production требуется выбрать qualified state provider. Альтернативы OD-PG-04: отдельная квалификация S3; иной отдельно утверждённый provider с эквивалентными properties; либо **production остаётся BLOCKED**, а доступен лишь diagnostic/synthetic scope. Выбор не сделан; нельзя автоматически начать S3-native coding или file/SQLite workaround. Квалификация должна отдельно доказать identity/grants/revocation history/atomic consume/rollback handling, not just disk persistence.

Windows service, SID/token/SCM/ACL/SDDL/named pipes/DPAPI/native NTFS/recovery/observer требуют exact isolated host, admin approval, runtime/source/artifact hashes и approved profile. Historic LAB L-01–L-04 не разрешают установку на неизвестной машине. PROCESS_QUALIFIED/POWER_LOSS_QUALIFIED не заработаны. PUBLISH_REVISION disabled и partial COMMIT reconstruction OFF не пересматриваются этим PROPOSAL.

Existing G2 path checks сохраняют окна check→open/cleanup/rename; D1 даже не вызывает G2 helper. Future executor должен различать descriptor identity, reparse object itself и child traversal; отказаться от UNC/device/alternate streams/unqualified mounts по выбранной policy, не полагаться на string prefix. Конкретные API/ACL и handle lifecycle здесь не реализуются и не объявлены достаточными без native adversarial tests.

## 6. Evidence и публикация

PG05 INDETERMINATE/partial outputs сохраняются приватно и не называют accepted production result. Hash/manifest может быть структурно корректен и при подделанном signer/runtime; нужны completion witness/ledger/head и read-back actual bytes. Attempt admission не очищается ради «повторить ещё раз» после crash. Расхождение index и ledger — quarantine/reconcile, no auto rerender.

CI logs/артефакты из непроверенного PR — недоверенные входы, не authority provider. Current workflow не меняется и не получает upload. Future export/redaction/retention/access/custodian должны быть owner-approved отдельно; private license copies, script/card/medical/scientific source fragments, identities и raw stderr не публикуются по факту технического успеха.

**Production execution остаётся BLOCKED; пакет документации готов к owner review. Новые controls и policies — PROPOSAL, без реализации/permissions/merge/release.**
