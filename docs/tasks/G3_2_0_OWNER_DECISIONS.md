# G3.2.0 — открытые решения владельца

**PROPOSAL — OWNER REVIEW REQUIRED.** Дата: 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

Все решения ниже **OPEN / PROPOSAL**. Наличие recommended option не означает approval. Это завершённое discovery, не запрос выдать production permissions сейчас и не поручение начать implementation. Пакет предназначен независимому ChatGPT аудиту и owner review.

## 1. Concrete alternatives

| ID / статус | Вопрос | Рекомендация PROPOSAL | Альтернативы и последствия | До какого шага обязательно решить |
|---|---|---|---|---|
| OD-PG-01 / OPEN | Как замораживать schema/hash/parser bounds? | Один closed typed envelope, domain-separated PG-C14N-1, binding всего envelope, raw ByteRef отдельно; strict no normalization/floats/unknown keys; предложенные8MiB/depth64/string64KiB/list10000 review | Использовать утверждённый canonical standard вместо PG-C14N-1 допустимо после mapping всех SI/G2 hashes и независимых vectors; не поддерживать несколько «равноправных» serializers/implicit algorithm fallback | До schema freeze и любого validator implementation |
| OD-PG-02 / OPEN | Кто и что подтверждает human approval? | Сохранить A1/A2 OS-derived identity и per-gate/decision policy; отдельные editorial/scientific roles/session/competence, exact SubjectKey, explicit declarations. A14 HANDOFF не даёт render rights | Один человек в нескольких ролях только по explicit policy/independence criteria; display actor/LLM approval без identity недопустим. Не переутверждать A1–A14/O1–O10 или делать все gates доступными current user | До PG02 effective-recognition design |
| OD-PG-03 / OPEN | Какие rights layers, jurisdictions и review obligations обязательны? | Утвердить policy по material/use, exact evidence copies, holder/consent, commercial/territory/time/channel/adaptation/attribution intersection; pending/disputed deny | Более узкий MVP без real music/TTS/external footage уменьшает checklist, но не создаёт exemption и требует конкретного lawful asset set; автоматическая верификация license text без reviewer не рекомендуется | До PG03 interpretation и real-material candidate |
| OD-PG-04 / OPEN | Где authoritative identity/grants/history/revocation/consume state? | Сначала отдельный provider-qualification contract: immutable refs, protected head/rollback, per-decision grants, durable atomic single-attempt ledger; **production BLOCKED до qualification** | (A) отдельный S3-native project после host/admin approvals; (B) иной separately approved qualified provider с эквивалентными properties; (C) оставить Preview/synthetic diagnostics и отложить production. Не объявлять S3 готовым, не делать file/SQLite substitute под видом approved storage | До operational authority или issuance |
| OD-PG-05 / OPEN | Single-use, crash recovery, expiry/revoke во время работы? | SINGLE_ATTEMPT reserve before spawn; crash/unknown → reconcile, no automatic rerender; exclusive expiry и bounded revocation monitoring, deny successful commit при revoke/expiry | Разрешать explicit bounded retry только новым reviewed grant/attempt с linkage и quota; at-least-once повтор тем же token не выбран. Числа TTL/polling/clock skew/timeout и надёжность time source должны быть отдельно обоснованы, не придуманы defaults | До PG04 admission/runtime design |
| OD-PG-06 / OPEN | Как issuer и executor доказывают полномочия и неизменные inputs? | Отдельный guarded execution endpoint на выбранном host/profile; OS-derived actor, trusted policy/receipts, fixed binaries/config, immutable object resolver, held input identities; client JSON не root of trust | Authenticated protected local broker или отдельно qualified signer/service — выбор требует protocol/key/session/custody review. Никакого allow=true/trusted=True/env override. Existing first_video оставить utility, не объявлять enforced gateway | До реального render admission и выбора production mode |
| OD-PG-07 / OPEN | Что считается завершённым execution/evidence? | PG05 exact actual inputs/tools/output hashes + profiles, private atomic index/head/completion witness; RU/UK batch all-required success, partial/orphan → INDETERMINATE/quarantine | Раздельные authorization для каждого языка возможны только как иной согласованный scope; тогда отсутствующий UK нельзя называть успешным RU/UK batch. Process crash test не power-loss qualification | До evidence protocol/implementation |
| OD-PG-08 / OPEN | Как topic worthiness/scientific review не подменяется формой? | Human editor оценивает why_film/audience/angle, exact claim-fragment relationships, required visuals/risks; central unresolved factual claims blocking; scientific competence отдельна | Advisory-only dossier можно сохранять как PREVIEW diagnostic, но не выдавать approval. Для fiction явно выделять real assertions и disclosures, не выдумывать источники и не обходить review классификацией | До product acceptance criteria PG01/PG02 |
| OD-PG-09 / OPEN | Как получать full snapshot из privacy-limited G2 exports? | Новый future collector из exact original input + pinned evaluator/Projection/runtime, отдельное хранение full private result и redacted view; новые snapshot/ref/review при изменении context/results | При отсутствии original inputs/runtime оставить export диагностикой и DENY; не восстанавливать недостающие diagnostic fields, не менять G2 export/PD-01 сейчас | До Preview→PG01 adapter design |
| OD-PG-10 / OPEN | Что можно раскрывать и сколько хранить? | Private content/license/identity/output/evidence by default; отдельные custodian/readers/retention/deletion/redaction и public-export разрешения | Минимальная публичная сводка с hashes только при explicit review scope; hashes могут раскрывать membership и тоже не анонимность. CI upload не нужен discovery и не разрешается автоматически | До persistence/evidence distribution/CI artifact design |
| OD-PG-11 / OPEN | Какой execution platform и security qualification обязательны? | Выбрать конкретный Windows10/11 CPU-only или другой explicit target и отдельный qualified profile: binaries/fonts/paths/identities/reparse/FS behavior/independent observer | Пока portable pure-only tests на Linux3.10/3.13 — ограниченный diagnostic scope, Windows/NTFS и production не заявляются. Подмена процесса native simulation неприемлема | До native/executor qualification; не разрешение установить service |
| OD-PG-12 / OPEN | Разрешать ли какой-либо следующий implementation этап? | Сначала независимый review и schema/semantic corrections docs-only; затем **при отдельном поручении** pure-only validators/oracles без permissions/IO | Отложить весь PG и пользоваться G2/D1 в их accepted limits. Сразу operational gate без принятых trust/rights/host решений — BLOCKED | До следующей задачи; этот документ её не запускает |

## 2. Что не является открытым разрешением

- Approved base зафиксирован; existing G1/G2/G3.1 contracts/implementations/CI не меняются. Doc branch не implementation base для будущего этапа без отдельного owner выбора exact SHA.
- A1–A14/O1–O10/PD-01–PD-08 не переопределяются. Их normative original scope сохраняется: exact references/history; actor не identity; optional signatures без trusted registry не authenticity; HANDOFF editorial-only/no render/export authorization; no partial/latest fallback.
- SYNTHETIC_TEST_ONLY, PREVIEW_ONLY и PRODUCTION_CANDIDATE **не предоставляют production permissions автоматически**. PG04 в этом discovery — candidate request, не действующий permit. Название/contract version будущего authorised production mode ещё не выбраны; его включение требует отдельного approval и qualifier evidence.
- SyntheticRenderPermitV1 не конвертируется в human/rights/render grant. D1 всегда fixed registered fixture, no real materials/publication/commercial rights. Его проход не считается qualification future PG05.
- G2 INPUT_COMPLETE/DRAFT_PLAN_VALID, Projection DISPLAYABLE, evaluator CURRENT/ELIGIBLE_FOR_CREATIVE, schema2 attestation digest и RightsBinding CONFIRMED не разрешают production.
- S3 internal protected-storage track не Amazon S3; historical PURE_ONLY не native qualifier. Нельзя запускать service/SCM/accounts/ACL/DPAPI/NTFS writer/observer без отдельного machine/admin/profile scope. Этот пакет таких операций не разрешает.
- Merge/release/main update, workflow/upload changes, реальные materials/licenses approvals, production renders и автоматический следующий этап запрещены текущим scope.

## 3. Обнаруженные блокировки

| Blocker | Фактическое основание | Что нужно вместо обхода |
|---|---|---|
| B-PG-01 — bridge отсутствует | G2 не создаёт authenticated immutable snapshot, PG01–PG05 не реализованы | Утверждённый контракт, затем отдельный adapter/validator task; no guessing saved full diagnostics |
| B-PG-02 — effective identity/authority/history не реализованы этим набором | Base evidence fields structural; approved A contracts требуют external trust/anchor | Выбор/qualification provider и roles/session policy; missing anchor deny |
| B-PG-03 — real asset rights/product reviews отсутствуют | Не предоставлены exact real sources/assets/consents/intended use/scientific/editorial decisions | Компетентная проверка real bounded dossier/usage; labels/hash не замена |
| B-PG-04 — single-use/revocation/time/rollback не обеспечены | Нет qualified consume ledger/current-state/time provider; deferred RAM model не durable service | Отдельные operational protocols/OS/storage qualification, trusted receipts/clock and heads |
| B-PG-05 — executor не guarded production boundary | first_video.build вызываем напрямую; нет qualified input-handle/issuer enforcement | Отдельный trusted endpoint/profile и adversarial native evidence, не rename CLI |
| B-PG-06 — evidence atomicity/custody не квалифицированы | D1 manifest ограничен media inspection; нет authentic atomic output/index/head commit | PG05 completion protocol, failure/recovery/custody/retention policy и qualified implementation |
| B-PG-07 — Windows/native не предоставлен/не проверен здесь | Linux executor; старые test reports не actual selected production host | Exact authorised isolated host/runtime/profile и scoped qualification task; не обещать ready Windows |
| B-PG-08 — новая production authority не утверждена | Все PG/new policies PROPOSAL; mode/name/issuer/grant protocol не выбраны | Независимый review, owner contract decisions и отдельное exact-scope production authorization в будущем |

Эти blockers не препятствуют owner review завершённого документационного discovery. Они препятствуют утверждению «можно отправлять real plan в production». Формальная schema validation не снимает product/legal/human/native blockers.

## 4. Возможный следующий docs-only запрос, не исполнение

После независимого ChatGPT review владелец может отдельно зафиксировать OD-PG-01…12: выбранный вариант, ограничения, exact source/schema revision и открытые зависимости. До полной trust-stack qualification любой pure implementation scope должен прямо запрещать реальные grants, disk/native/network integration и render.

Будущее implementation поручение, если оно вообще будет, должно назвать exact approved base/tree, изменяемые файлы, contract versions, allowed side effects, test matrix, runtime bounds и STOP criteria. Отдельные подпроекты нужны для provider/host qualification и guarded executor/evidence. Нельзя автоматически разрешить всё через фразу «архитектура принята» или считать будущие tests уже пройденными.

Согласование production режима должно отдельно ответить: чей exact script/asset/use утверждён; какой editor/scientific/rights reviewer имеет соответствующие полномочия; какой trust provider доказал latest state; какой issuer/executor/profile допущен; какая attempt/expiry/revocation политика; как private outputs/evidence protected и кто разрешает публикацию. Эти данные сейчас не заполнены и полномочия не выданы.

## 5. Независимый пакет и STOP

Пять новых Markdown в одной documentation branch от exact base:

- [G3_2_0_ARCHITECTURE_INVENTORY.md](G3_2_0_ARCHITECTURE_INVENTORY.md) — actual APIs/limitations и30 pinned blob refs, current/historical evidence.
- [G3_2_0_PRODUCTION_GATE_CONTRACT_PROPOSAL.md](G3_2_0_PRODUCTION_GATE_CONTRACT_PROPOSAL.md) — PG01–PG05 typed schemas, mandatory fields, validation/denial/error/dependency/security rules.
- [G3_2_0_SECURITY_AND_RIGHTS_MATRIX.md](G3_2_0_SECURITY_AND_RIGHTS_MATRIX.md) — threats, trust-layer separation, real rights и product criteria.
- [G3_2_0_TEST_ORACLES_AND_GATES.md](G3_2_0_TEST_ORACLES_AND_GATES.md) — planned pure/product/native oracles, phase gates и NOT_RUN declaration.
- Этот документ — alternatives/recommendations/open decisions и blockers.

Commit/tree и exact five-path diff передаются после commit во внешнем handoff; self-hashes в файлы не встраиваются. Это пакет **для** независимого ChatGPT аудита, не утверждение, что аудит уже состоялся. **READY_FOR_OWNER_REVIEW — PROPOSAL. STOP.**
