# Open parameters and owner decisions

**FREEZE_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0a; 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Pinned discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c`.
Только docs/offline vectors. Направление OD-PG-01–12 принято владельцем, но численные значения, роли, trust policies и operational protocols не утверждены. Нет validators/providers, permissions или qualification.

Все строки OPEN/PROPOSED, **ни одна не APPROVED**. Архитектурное направление принято, а конкретные parameters/protocols не становятся нормой от наличия в discovery. Rule/parameter-dependent vectors отмечены APPROVAL_REQUIRED; намеренно не заполнены real roles/credentials/licenses/hosts.

## OP-01 — Envelope bytes

- Proposed value/options: 8388608 full wire bytes, inclusive.
- Rationale: Bound IO before decode; whitespace counts.
- Security impact: Prevents unbounded inputs, not total memory proof.
- Product impact: Very large docs via ByteRef.
- Dependent vectors/oracles: V058,V059.
- Owner decision required: Утвердить число и input-vs-canonical accounting.
- Status: **PROPOSED**, NOT APPROVED.

## OP-02 — Nesting

- Proposed value/options: 64; scalar0, root container1.
- Rationale: Remove off-by-one ambiguity.
- Security impact: Bound recursion; do not rely on stdlib default.
- Product impact: Deep real dossier may require flattening.
- Dependent vectors/oracles: V054,V055.
- Owner decision required: Утвердить depth/counting semantics.
- Status: **PROPOSED**, NOT APPROVED.

## OP-03 — String bytes

- Proposed value/options: 65536 UTF8 bytes, keys and values.
- Rationale: Unicode bytes versus characters/escape text.
- Security impact: Avoid memory amplification; escaped wire still bounded separately.
- Product impact: Large excerpts stored immutable ByteRef.
- Dependent vectors/oracles: V052,V053.
- Owner decision required: Утвердить size и decoded measurement.
- Status: **PROPOSED**, NOT APPROVED.

## OP-04 — Lists

- Proposed value/options: 10000 per list plus explicit field minima/uniqueness.
- Rationale: No root-only shortcut.
- Security impact: Total object count remains separate.
- Product impact: Large evidence inventories need budgets.
- Dependent vectors/oracles: V056,V057.
- Owner decision required: Утвердить numeric list cap и per-field cardinalities.
- Status: **PROPOSED**, NOT APPROVED.

## OP-05 — Canonical edge cases

- Proposed value/options: Signed64, -0→0; decoded paired surrogate allowed, no normalization; codepoint sort.
- Rationale: One exact byte sequence.
- Security impact: Avoid hash ambiguity/SI interchange.
- Product impact: Interoperability across languages.
- Dependent vectors/oracles: V003–018,V046–050,V067.
- Owner decision required: Утвердить proposed lexical rules/edge vectors, not implicit serializer defaults.
- Status: **PROPOSED**, NOT APPROVED.

## OP-06 — Error priority X01/X02

- Proposed value/options: Explicit schema→local hash→refs→semantics; choose empty Text/mode error mapping.
- Rationale: Source expectations inconsistent.
- Security impact: Ambiguous denial classification may break clients/tests.
- Product impact: Clear corrective messages without unsafe repair.
- Dependent vectors/oracles: V039,V051.
- Owner decision required: Выбрать primary codes; пересмотреть исходный oracle явно.
- Status: **OPEN**, NOT APPROVED.

## OP-07 — Parser resources

- Proposed value/options: Separate CPU/time/memory/object-count/token budget; no number approved.
- Rationale: 8MiB is not enough to bound allocations.
- Security impact: DoS protection per parser/executor.
- Product impact: Avoid arbitrary rejection of legitimate dossiers.
- Dependent vectors/oracles: V052–059; new probes after decision.
- Owner decision required: Назвать numeric resource budget and accounting model.
- Status: **OPEN**, NOT APPROVED.

## OP-08 — Closure bound/cycle fixtures X03

- Proposed value/options: Options bounded nodes/edges/ref depth; define abstract graph fixture vs digest-valid closure.
- Rationale: Cannot fake content-addressed cyclic hashes.
- Security impact: Limit traversal, reject duplicates and malicious graphs.
- Product impact: Large histories need explicit separate bounded reads.
- Dependent vectors/oracles: V041–043.
- Owner decision required: Утвердить limits/edge model и cycle test design without forged hashes.
- Status: **OPEN**, NOT APPROVED.

## OP-09 — Reference stages

- Proposed value/options: Local hash-first, conflict registry, exact typed edges; clarify opaque ByteRef decoding.
- Rationale: No latest fallback; avoid hidden schema edges.
- Security impact: Resolve closure exactly before trusting metadata.
- Product impact: Readable immutable history remains separate.
- Dependent vectors/oracles: V022,V041–043.
- Owner decision required: Утвердить target key/closure order and historical edges.
- Status: **PROPOSED**, NOT APPROVED.

## OP-10 — Instant/clock

- Proposed value/options: 0…253402300799 epochsec; skew/uncertainty/time authority not selected.
- Rationale: Timestamp syntax not clock trust.
- Security impact: Rollback/uncertainty must deny admission.
- Product impact: Offline diagnostics may remain available.
- Dependent vectors/oracles: V060–063,V069.
- Owner decision required: Утвердить range, precision, uncertainty and provider.
- Status: **OPEN**, NOT APPROVED.

## OP-11 — Expiry window

- Proposed value/options: Exclusive [from,until); max TTL/expected render margin not approved.
- Rationale: Boundary predictable.
- Security impact: Avoid expiry during long render or auto extension.
- Product impact: May require new request after delay.
- Dependent vectors/oracles: V063; P04-03/06.
- Owner decision required: Утвердить TTL/duration/margin and lifecycle rules.
- Status: **OPEN**, NOT APPROVED.

## OP-12 — Revocation freshness

- Proposed value/options: Synchronous lease/checkpoint or bounded polling; interval unapproved.
- Rationale: No stale cached APPROVE.
- Security impact: Detect revoke/outage before successful commit.
- Product impact: Cancellation/review latency tradeoff.
- Dependent vectors/oracles: P02-05/06,P04-06.
- Owner decision required: Выбрать monitoring protocol, deadlines and outage behavior.
- Status: **OPEN**, NOT APPROVED.

## OP-13 — Rights applicability

- Proposed value/options: Versioned required layers per asset/use/jurisdiction; generated not exemption.
- Rationale: Actual legal/consent review.
- Security impact: Missing rights layer denies use.
- Product impact: May exclude music/voices/stock from first bounded scope.
- Dependent vectors/oracles: P03-01…08.
- Owner decision required: Утвердить competence/jurisdiction/layer and intended-use policy.
- Status: **OPEN**, NOT APPROVED.

## OP-14 — Reviewer independence

- Proposed value/options: OS-derived identity + per-role authority; explicit self-review/dual-role policy.
- Rationale: Separate competence/editorial/rights.
- Security impact: Do not assume user is all-gate admin.
- Product impact: Small team workflow versus independent scrutiny.
- Dependent vectors/oracles: P02-02/03/08; PRODUCT01–07.
- Owner decision required: Назвать allowed roles, conflicts, mandatory declarations/competence.
- Status: **OPEN**, NOT APPROVED.

## OP-15 — Authority/state provider

- Proposed value/options: Qualified S3, separately qualified alternative, or production remains blocked.
- Rationale: Existing source PURE_ONLY not service.
- Security impact: Need authenticated heads, grants, rollback protection.
- Product impact: Preview/D1 remain usable without production.
- Dependent vectors/oracles: P02-05,P04-04/10,NATIVE03.
- Owner decision required: Выбрать project/profile; no implementation permission implied.
- Status: **OPEN**, NOT APPROVED.

## OP-16 — Single attempt recovery

- Proposed value/options: Reserve before spawn; unknown→reconcile, no rerender; exact durable protocol pending.
- Rationale: At-most-one admission not exactly-once physical work.
- Security impact: Prevent replay after crash/lost ACK.
- Product impact: Manual new grant may be needed.
- Dependent vectors/oracles: P04-04/05,P05-05.
- Owner decision required: Утвердить ledger/event/retry/reconciliation semantics.
- Status: **PROPOSED**, NOT APPROVED.

## OP-17 — Immutable resolver

- Proposed value/options: Opaque content IDs, held qualified identities/handles; no caller paths/PATH/network.
- Rationale: JSON hash check not TOCTOU control.
- Security impact: OS/symlink/reparse/mount protection needs host proof.
- Product impact: Private staging and asset availability.
- Dependent vectors/oracles: P04-07,NATIVE01.
- Owner decision required: Выбрать actual resolver/store/OS proof model.
- Status: **OPEN**, NOT APPROVED.

## OP-18 — Output profiles

- Proposed value/options: Exact RU/UK batch, codecs, dimensions/fps, subtitle/attribution/tool/font checks; numeric profile unapproved.
- Rationale: Expected outputs not invented hashes.
- Security impact: Reject partial/wrong toolchain outputs.
- Product impact: Real readability/language/playback still human checks.
- Dependent vectors/oracles: P04-02/08,P05-01/02/06.
- Owner decision required: Утвердить closed profile schema/versions and constraints.
- Status: **OPEN**, NOT APPROVED.

## OP-19 — Evidence durability

- Proposed value/options: Atomic index/head/output binding + independent completion witness; storage protocol unselected.
- Rationale: No success from existing MP4/marker alone.
- Security impact: Crash/rollback/partial evidence→unknown.
- Product impact: May delay accepted results until reconciliation.
- Dependent vectors/oracles: P05-03…06,NATIVE02.
- Owner decision required: Утвердить durable protocol/qualification, not RAM model.
- Status: **OPEN**, NOT APPROVED.

## OP-20 — Windows/host qualification

- Proposed value/options: Exact authorized isolated Windows10/11 CPU-only or other chosen platform.
- Rationale: No Linux→Windows inference.
- Security impact: Services/ACL/DPAPI/native writer need separate approval.
- Product impact: Actual codecs/fonts/Cyrillic/playback/path compatibility.
- Dependent vectors/oracles: NATIVE01…03.
- Owner decision required: Назвать host/profile/admin scope only in separate task.
- Status: **OPEN**, NOT APPROVED.

## OP-21 — Privacy/retention/disclosure

- Proposed value/options: Private by default; export/readers/custodian/retention/erase separate.
- Rationale: Hashes also not anonymity.
- Security impact: No public cards/licenses/identities/raw stderr/upload by default.
- Product impact: Review access without leaking material.
- Dependent vectors/oracles: P05-07,NATIVE03.
- Owner decision required: Утвердить exact content/access/retention/export boundary.
- Status: **OPEN**, NOT APPROVED.

## OP-22 — Toolchain SubjectKey X04

- Proposed value/options: Add explicit plan bindings for toolchain/executor OR narrow reapproval rules with exact references.
- Rationale: Current discovery statement not backed by fields.
- Security impact: Auth changes but old human SubjectKey may otherwise persist.
- Product impact: May trigger review on tool/profile change.
- Dependent vectors/oracles: P01-05,P04-02/08.
- Owner decision required: Утвердить concrete schema change/version; not silently freeze.
- Status: **OPEN**, NOT APPROVED.

## OP-23 — Opaque evidence payloads

- Proposed value/options: Freeze separate schemas for code manifest/environment/identity/grant/admission/completion/inspection receipts.
- Rationale: ByteRef syntax not evidence semantics.
- Security impact: No fake trusted=true receipts or keys.
- Product impact: Full positive fixtures depend on these profiles.
- Dependent vectors/oracles: P01-01,P02-01,P03-01,P04-10,P05-01.
- Owner decision required: Утвердить protocol schemas/providers before full consistent examples.
- Status: **OPEN**, NOT APPROVED.

## OP-24 — Policy namespaces

- Proposed value/options: Distinguish SubjectKey root content/use policy, actor authority, rights policy, issuer/executor/output profiles.
- Rationale: Same PolicyRef type does not imply same authority.
- Security impact: Prevent wrong-policy reuse and scope confusion.
- Product impact: Explicit revisions invalidate related decisions.
- Dependent vectors/oracles: P02-01,P03-08,P04-03.
- Owner decision required: Утвердить comparison/equality/expiry rules per policy role.
- Status: **OPEN**, NOT APPROVED.

## OP-25 — G2 snapshot collection

- Proposed value/options: Exact original input+pinned full recomputation; never guess redacted diagnostics.
- Rationale: Current G2 preserved.
- Security impact: Avoid forged complete result/currentness.
- Product impact: Unavailable inputs mean diagnostics-only.
- Dependent vectors/oracles: P01-02/04/08.
- Owner decision required: Утвердить collector contract and code/runtime manifest, docs-only now.
- Status: **PROPOSED**, NOT APPROVED.

## OP-26 — Structural status

- Proposed value/options: Keep STRUCTURALLY_VALID descriptive only; no new machine enum.
- Rationale: No namespace expansion by docs.
- Security impact: Prevent shape success treated as grant.
- Product impact: Clear user reporting versus API verdict.
- Dependent vectors/oracles: COMMON02,P01-01,P04-10.
- Owner decision required: Если нужен machine status — отдельное explicit owner решение/version.
- Status: **PROPOSED**, NOT APPROVED.

## OP-27 — Errors/privacy

- Proposed value/options: 21 existing proposed codes; fixed localized messages; deterministic branch precedence.
- Rationale: No raw caller path/exception echo.
- Security impact: Fail closed on unknown provider error.
- Product impact: Useful corrections without invented automatic repairs.
- Dependent vectors/oracles: COMMON06,P05-07.
- Owner decision required: Утвердить safe catalog and exact branch/order semantics.
- Status: **PROPOSED**, NOT APPROVED.

## OP-28 — Review validity/tombstones

- Proposed value/options: Negative tombstone does not expire into old approve; current history authentic.
- Rationale: valid_until effect must be distinct from history permanence.
- Security impact: Prevent revival/replay.
- Product impact: New authentic decision restores only exact reviewed scope.
- Dependent vectors/oracles: P02-04…07.
- Owner decision required: Утвердить event validity/authority/history interaction.
- Status: **PROPOSED**, NOT APPROVED.

## Blocking contradictions, not permission requests

X01–X04 в schema matrix требуют explicit owner adjudication и обновления expectations без потери source oracle history. Они блокируют окончательный contract freeze и full-consistency golden examples. Векторы с APPROVAL_REQUIRED — conditional evidence арифметики/границ, не нормативное утверждение чисел. V043 отдельно не supplies genuine isolated cycle input; нельзя считать coverage закрытой.

После review возможна только отдельно порученная docs correction/schema freeze. G3.2.1/validators/providers/native qualification/production renders не начаты и автоматически не разрешаются. Production remains BLOCKED. Ни main/CI/G1/G2/G3.1/Storage S3, ни existing docs не меняются.
