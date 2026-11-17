# G3.2.0a — contract freeze proposal and disposition

**FREEZE_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0a; 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Pinned discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c`.
Только docs/offline vectors. Направление OD-PG-01–12 принято владельцем, но численные значения, роли, trust policies и operational protocols не утверждены. Нет validators/providers, permissions или qualification.

## Итог

**BLOCKED_CONTRACT** для окончательного freeze. Подготовлены семь docs/offline-vector deliverables для независимого review; направление принято, но нельзя объявлять READY при обнаруженных X01–X04 и неподтверждённых profiles. Это не отказ от выполненного анализа: literal arithmetic/canonical byte controls выполнены, все58 source oracles сохранены, unresolved decisions явно перечислены.

## Preflight и provenance

Fetch подтвердил origin/main exact base/tree. Discovery commit/tree совпали с заданием, его пять документов существуют, source blob IDs проверены, в base все пять отсутствуют. Checkout чистый, target remote branch отсутствовала. Создана отдельная `docs/g3-2-0a-contract-freeze-vectors` от exact approved main, не от discovery. Existing files не изменяются, rebase/cherry-pick не выполняются.

| Source discovery file | Git blob SHA1 |
|---|---|
| G3_2_0_ARCHITECTURE_INVENTORY.md | 42b7c5533188a0226a6e562e46872651f16c0a9b |
| G3_2_0_PRODUCTION_GATE_CONTRACT_PROPOSAL.md | 348be4fc69d8a44abadeb30d947885afacff3e60 |
| G3_2_0_SECURITY_AND_RIGHTS_MATRIX.md | e829c06503c99cd13816dbdc37d89bb49fa82054 |
| G3_2_0_TEST_ORACLES_AND_GATES.md | 4b79e1de9e3cb3b57e3fd221403d4ae5a925139d |
| G3_2_0_OWNER_DECISIONS.md | 2726049371c4b3e0522e3e31b194e9764d9138f5 |

## Contract direction and exact scope

PG01 immutable Preview Snapshot: raw/source/version/context/full result/card/plan/dossier bindings; redacted G2 export не full result. PG02 Human Approval: exact subject+kind+principal/policy/session/history, no false human identity. PG03 Asset Rights Evidence: complete actual asset/use/license layers и real reviewer basis. PG04 Render Authorization **Candidate**: strict request bindings, no grant/single-use proof from JSON. PG05 Execution Evidence: actual inputs/tools/outputs/hashes, failure/unknown completion semantics.

Сохраняются IDs pg-01/proposal-1…pg-05/proposal-1 и conceptual SYNTHETIC_TEST_ONLY/PREVIEW_ONLY/PRODUCTION_CANDIDATE. Ни mode, ни STRUCTURALLY_VALID annotation не production permission. Proposed pure verdict namespace не расширен: CONSISTENT_NO_AUTHORITY/DENY; no ALLOW_RENDER. Все subtype fields/enums/ref edges раскрыты в schema matrix; final semantic contradictions и provider payloads не подменены фиктивными значениями.

## Четыре блокирующих findings

| ID | Конфликт/gap | Recommendation (NOT APPROVED) |
|---|---|---|
| X01 | Nonempty Text schema vs P01-07 empty why_film product-gap error | Явно выбрать schema-stage PG_FORMAT для пустого Text и оставить PG_PRODUCT_GAP для непустого, но недостаточного dossier; обновить oracle открыто после owner решения |
| X02 | Mode subset/schema vs PG_MODE semantic checks и stale binding PG_DIGEST precedence | Зафиксировать одну stage policy: known enum lexical check, local hash, then contract-mode subset; либо иной explicit owner выбор. V039 до этого BLOCKED |
| X03 | Isolated cyclic content-addressed refs требуют valid mutually-bound hashes; fake zero/stale hashes тестируют другое | Выбрать abstract structural-graph fixture или доказуемо достижимый malformed graph case; не считать stale hash rejection isolated cycle coverage. В этой версии V043 BLOCKED |
| X04 | Toolchain/executor claimed part of SubjectKey via plan, но в RenderPlan нет обязательных соответствующих bindings | Явно добавить immutable toolchain/executor bindings в plan либо пересмотреть reapproval scope; schema/version и policy только после owner решения |

Opaque provider receipts/manifest/environment/inspection schemas и all28 parameters также не frozen. Даже урегулирование X01–X04 не выдаёт real authority и не квалифицирует OS/storage/trusted executor. Existing A1–A14/O1–O10/G1/G2/G3.1 сохраняются. Human product suitability/rights/native properties не pure PASS.

## Package

1. [Canonicalization spec](G3_2_0A_CANONICALIZATION_SPEC.md): exact proposed byte rules/domain/self-hash/pre-digest errors.
2. [Independent vectors](G3_2_0A_INDEPENDENT_VECTORS.md):70 records с exact bytes/recipes;33 canonical-positive,34 proposed DENY,3 BLOCKED; conditional profiles помечены.
3. [Schema/reference matrix](G3_2_0A_SCHEMA_AND_REFERENCE_MATRIX.md):36 Record declarations из pinned discovery, enum sets/SubjectKey/closure и compatibility gaps.
4. [Error/oracle matrix](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md): все58 source oracles verbatim, isolation/dependencies/offline limits и readiness.
5. [Open parameters](G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md):28 unapproved choices с consequences/dependent vectors/owner decisions.
6. [Acceptance packet](G3_2_0A_ACCEPTANCE_PACKET.md): offline evidence, file blobs и final disposition.
7. Этот freeze proposal.

Все семь файлов mode100644 и только docs/tasks. Temporary scripts/byte files находятся вне repo и не committed. Не выполнялись application test suite, D1/production render, network/license verification, real identity/grants, Windows services/native/security, CI changes, S3 changes, merge/release или G3.2.1. **STOP — независимый ChatGPT review и решение владельца.**
