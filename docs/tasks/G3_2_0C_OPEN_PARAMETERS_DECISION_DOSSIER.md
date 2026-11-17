# G3.2.0c — Open Parameters Decision Dossier

**DECISION_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0c; 2026-11-17 (Europe/Kyiv).
Accepted docs parent `0d6d9076ab535c1b258206beb4e4fe9c005e79e1`, tree `e55c00d0e7a95218e0978dd9677172608395ff5f`; its parent `2610dcfd0a304c4fb8f4d71812b80e52f6ce3bb5`.
Approved main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
X01–X04 choices OWNER_APPROVED; G3.2.0b ACCEPTED_DOCS_ONLY. OP values/protocols NOT APPROVED; G3.2.1 NOT AUTHORIZED; production permissions BLOCKED.

## 1. Scope, provenance and disposition

**READY_FOR_INDEPENDENT_REVIEW** для этого decision dossier, не implementation readiness или final freeze. Только семь новых Markdown, ни один existing file не изменён. Fetch main/base/tree/parent, clean checkout, десять A/B reference docs и отсутствие target branch проверены до создания `docs/g3-2-0c-open-parameters-decision-dossier` от exact accepted B parent. No merge/rebase/cherry-pick/fallback.

Exact source requirements берутся из pinned `docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`, и дополняются approved B adjudication. Source OP-06/08/22 historical conflict language **не** переоткрывает X01–X04; priority/graph split/mandatory bindings B имеют явный приоритет. Parent docs читаются, не переписываются.

## 2. Coverage and decision-ready meaning

| Classification | Count | Primary packages |
|---|---:|---|
| PURE | 12 | P1:8, P2:2, P3:2 |
| MIXED | 7 | P4:7 |
| OPERATIONAL | 9 | P5:9 |
| Total unique OP | 28 | One class and one primary package each |

P2 additionally examines OP-08 structural semantics (primary P3 numeric/accounting) and pure OP-24 namespace projection (primary P4). Это secondary coverage, не дублирование владения. [P1](G3_2_0C_P1_CANONICAL_FOUNDATION.md), [P2](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md), [P3](G3_2_0C_P3_RESOURCE_MODEL.md), [P4](G3_2_0C_P4_POLICY_CONTRACTS.md), [P5](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md).

**10 decision-ready pure choices**: OP-01…06, OP-09, OP-22, OP-26, OP-27. Здесь ready означает: изложен bounded pure выбор, который можно рассмотреть без реального provider/benchmark. Это не approval и не разрешение кодировать. **18 unresolved whole-parameter choices**: OP-07/08, семь MIXED и девять OPERATIONAL. Их pure projections представлены, но полного выбора чисел/политик/доказательств нет. Все28 по-прежнему NOT APPROVED. Source OPEN/PROPOSED statuses сохранены; ready ортогонален этому статусу.

Implementation prerequisite Yes/No ниже относится **только к гипотетическому отдельно разрешённому pure-only этапу**, который сейчас NOT AUTHORIZED. Yes: требуется explicit owner choice/schema до соответствующего pure component; No: operational реализация не prerequisite standalone pure schema/bytes work, но всегда обязательный gate до production. No не означает optional безопасность или разрешение операции.

## 3. Complete dependency/approval matrix

Source rule — exact quoted Proposed value/options из pinned OP record; полный исходный блок в §4. Dependency IDs — **decision-order hard prerequisites**, не assertions о текущей availability provider. Operational realization gates отдельно в P4/P5; они не создают backward dependency P1→provider.

| ID | Class / primary | Exact source requirement | Recommendation | Alternatives | Security consequence | Product consequence | Dependency IDs | Oracle/vector IDs | Owner approval question | Implementation prerequisite | Status / decision-ready |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OP-01 | PURE / P1 | 8388608 full wire bytes, inclusive. | 8MiB=8388608 inclusive full wire bytes before decode; ByteRef content отдельно | 4MiB conservative;16MiB large dossier | Reject before unbounded buffer growth; wire cap alone not memory proof | Large dossiers move media/excerpts to refs, whitespace counts against cap | None | V058, V059, COMMON-04 | Утвердить8MiB inclusive wire cap с отдельным canonical accounting, без утверждения memory safety? | Yes | PROPOSED / ready question |
| OP-02 | PURE / P1 | 64; scalar0, root container1. | 64 containers; scalar0/root container1; nested container+1, arrays=objects | 32 for conservative parsing;96 only separately profiled | Explicit counter avoids off-by-one/stack assumptions | Deep dossiers may need flatter refs; no implicit normalization | None | V054, V055, COMMON-04 | Утвердить depth64 и указанный counting model, без native stack qualification? | Yes | PROPOSED / ready question |
| OP-03 | PURE / P1 | 65536 UTF8 bytes, keys and values. | 65536 decoded UTF8 bytes for each key/value string, normalization forbidden | 32768 conservative;131072 separately bounded profile | Count emitted decoded bytes before append, escaped wire still cap W | Long quotations use ByteRef; codepoint count is not byte count | OP-05 | V052, V053, COMMON-03 | Утвердить65536 bytes для decoded keys/values и separate raw wire accounting? | Yes | PROPOSED / ready question |
| OP-04 | PURE / P1 | 10000 per list plus explicit field minima/uniqueness. | 10000 elements per array; tighter per-field limits; global node/token bounds independent | 2000 conservative;20000 only separate large profile | Nested many-array attack still needs OP-07, object members separate | Large asset arrays may need bounded partitions, never silent truncation | None | V056, V057, COMMON-04 | Утвердить per-array10000 без утверждения global parser budget? | Yes | PROPOSED / ready question |
| OP-05 | PURE / P1 | Signed64, -0→0; decoded paired surrogate allowed, no normalization; codepoint sort. | Signed64/no float; -0→0; Unicode scalars/codepoint keys/exact escaping/domain C14N-1 | External canonical standard with explicit compatibility map; current byte model with approved independent conformance set | No SI/G2 hash interchange, duplicate keys after unescape reject | Stable cross-language snapshots, authored Unicode untouched | None | V001, V003, V005, V011, V017, V046, V047, V067, COMMON-02, COMMON-05 | Утвердить полный finite canonical rule set P1, включая -0 и paired escapes, не меняя existing vectors? | Yes | PROPOSED / ready question |
| OP-06 | PURE / P1 | Explicit schema→local hash→refs→semantics; choose empty Text/mode error mapping. | Retain X01/X02 exactly; add deterministic within-stage tie policy and missing-error mappings | First canonical field/identity order; fixed code-priority within earliest failed stage | Never later semantic/provider error supersedes earlier approved stage | Stable corrections without coercion or masking product gaps | OP-27 | V039, V051, V071, V073, COMMON-06 | Утвердить proposed residual tie matrix P1, сохраняя X01/X02 без пересмотра? | Yes | OPEN / ready question |
| OP-07 | PURE / P3 | Separate CPU/time/memory/object-count/token budget; no number approved. | Three logical counter profiles; CPU/time/RAM coefficients remain OPEN pending separate measurements | Streaming/bounded builder; arena/DOM with explicit logical budgets and qualification | Bound nodes/tokens/decoded data before growth; no fabricated runtime ceilings | Some legitimate large dossiers rejected, explicit retry with reviewed profile only | OP-01, OP-02, OP-03, OP-04, OP-09 | V052, V058, V059, COMMON-04 | Какой logical profile выбрать для будущего тестового scope и какие evidence нужны до выбора CPU/RAM/time caps? | Yes | OPEN / unresolved whole parameter |
| OP-08 | PURE / P3 | Options bounded nodes/edges/ref depth; define abstract graph fixture vs digest-valid closure. | Typed closure counters+dedup rules; profile limits in P3 PROPOSED, actual selection OPEN | Conservative ref cap; balanced/large profiled cap, no unbounded traversal | Count edges even shared/repeated, distinct identities once; abstract cycle≠crypto closure | Deep historical graphs may need explicit bounded slices | OP-07, OP-09 | V041, V042, V043, V043-S, V043-S4, V043-S6, P02-04 | Утвердить closure accounting и выбрать numeric profile только после OP-07 review, не признавая crypto-cycle coverage? | Yes | OPEN / unresolved whole parameter |
| OP-09 | PURE / P2 | Local hash-first, conflict registry, exact typed edges; clarify opaque ByteRef decoding. | Exact typed identity/revision/hash refs, conflict reject, no latest fallback, separate semantic payload profiles | Strict exact closed family; explicitly versioned compatibility adapters after separate approval | No duplicate identity substitution or hidden ref discovery in arbitrary JSON | Reproducible snapshot/history diagnostics without authority claims | OP-05, OP-06 | V022, V041, V042, P01-05, P02-04 | Утвердить pure reference model P2 без подтверждения latest head/OS/store? | Yes | PROPOSED / ready question |
| OP-10 | MIXED / P4 | 0…253402300799 epochsec; skew/uncertainty/time authority not selected. | Pure Instant signed domain0…253402300799 epochsec; external time authority/skew OPEN | Whole-second fixed domain; explicit precision/version extension, no local-time fallback | Uncertain clock denies operation, timestamp syntax not authenticity | Diagnostics can remain offline; real scheduling needs authority | OP-05 | V060, V061, V062, V063, V069, P03-06 | Утвердить pure timestamp domain отдельно от выбора clock source/uncertainty? | Yes | OPEN / unresolved whole parameter |
| OP-11 | MIXED / P4 | Exclusive [from,until); max TTL/expected render margin not approved. | Pure [from,until) intersection; TTL/render margin OPEN until profile+clock evidence | Narrow per-attempt lease; bounded approved batch window, no auto extension | Expiry at equality; negative tombstone persistence not TTL | Expired queued jobs need explicit new candidate, no bypass | OP-10 | V063, P04-03, P04-06 | Утвердить pure interval algebra, оставив TTL/margin и admission timing отдельному решению? | Yes | OPEN / unresolved whole parameter |
| OP-12 | OPERATIONAL / P5 | Synchronous lease/checkpoint or bounded polling; interval unapproved. | Design lease/checkpoints or bounded poll protocol; no selected polling number | Synchronous trusted lease; bounded poll with conservative fail-stop on outage | Revoked/unknown state cannot become successful commit; bounded detection must be proven | Cancellation latency versus provider availability | OP-10, OP-11, OP-15, OP-23 | P02-05, P02-06, P04-06 | Какой revocation protocol/lag/outage policy выбрать для последующего отдельного qualification task? | No | OPEN / unresolved whole parameter |
| OP-13 | MIXED / P4 | Versioned required layers per asset/use/jurisdiction; generated not exemption. | Pure exact asset/use/layer coverage; required legal layers/jurisdictions and competent reviewer OPEN | Narrow no-external-media scope; reviewed licensed asset policy by actual usage | No inferred rights/public-domain/generated exemption, commercial/territory/time intersection | Scientific/creative suitability distinct from license permission | OP-14, OP-18, OP-24 | P03-01, P03-03, P03-04, P03-05, P03-07, PRODUCT-02 | Какие jurisdictions/layers/intended-use policy и reviewer evidence требуется отдельно утвердить? | Yes | OPEN / unresolved whole parameter |
| OP-14 | MIXED / P4 | OS-derived identity + per-role authority; explicit self-review/dual-role policy. | Pure role/scope/decision/session/declaration fields; real assignments/competence/independence OPEN | Separate reviewer roles; explicit controlled dual-role policy with conflict evidence | No current-user all-rights, auto self-approval or title-as-competence | Small-team feasibility versus actual independent scrutiny | OP-24 | P02-02, P02-03, P02-08, PRODUCT-06 | Какие роли/конфликты/qualification evidence разрешены policy, без назначения конкретных лиц сейчас? | Yes | OPEN / unresolved whole parameter |
| OP-15 | OPERATIONAL / P5 | Qualified S3, separately qualified alternative, or production remains blocked. | Define required provider properties; choose qualification project or remain production-blocked | Dedicated S3-native qualification; separate qualified provider; diagnostics-only defer | Need authenticated grants/heads/anti-rollback, pure S3 model insufficient | Provider can be deferred without disabling safe previews | OP-14, OP-24 | P02-05, P04-04, P04-10, NATIVE-03 | Выбрать отдельный provider-design/qualification scope или оставить production заблокированным? | No | OPEN / unresolved whole parameter |
| OP-16 | OPERATIONAL / P5 | Reserve before spawn; unknown→reconcile, no rerender; exact durable protocol pending. | Durable single-attempt admission before spawn; unknown→reconcile, no automatic rerender | Protected local ledger; separately qualified transactional authority, not RAM-only state | At-most-one admission not exactly-once physical execution; lost ACK lookup safe | Manual recovery/new grant may be needed after uncertain crash | OP-08, OP-15, OP-23 | P04-04, P04-05, P05-05 | Утвердить recovery semantics и требования ledger-протокола без запуска/выдачи grant? | No | PROPOSED / unresolved whole parameter |
| OP-17 | OPERATIONAL / P5 | Opaque content IDs, held qualified identities/handles; no caller paths/PATH/network. | Opaque immutable IDs plus held verified file identities; actual OS/store protocol OPEN | Qualified broker/content store handles; qualified private snapshot/package with anchored opens | No caller path/PATH override, TOCTOU/reparse/mount behavior needs OS proof | Availability/staging cost explicit, no network material recovery | OP-22, OP-23 | P04-07, NATIVE-01 | Какой resolver threat model/OS evidence contract выбрать для отдельного review? | No | OPEN / unresolved whole parameter |
| OP-18 | MIXED / P4 | Exact RU/UK batch, codecs, dimensions/fps, subtitle/attribution/tool/font checks; numeric profile unapproved. | Pure closed expected RU/UK outputs/tools/config/attribution profile refs; actual media limits/quality OPEN | One exact RU/UK batch; explicitly separate per-locale authorizations after scope review | No success by file existence; no tool/font override | Readability/Cyrillic/playback/content quality still human/host checks | OP-22, OP-24 | P04-02, P04-08, P05-01, P05-02, P05-06 | Утвердить profile fields/coverage отдельно от codecs/duration thresholds и real runtime qualification? | Yes | OPEN / unresolved whole parameter |
| OP-19 | OPERATIONAL / P5 | Atomic index/head/output binding + independent completion witness; storage protocol unselected. | Specify invariant ledger↔index↔actual outputs; actual durable commit/witness protocol OPEN | Qualified single-store atomic protocol; qualified journal/commit+reconciliation protocol | Orphan/truncated evidence INDETERMINATE, not success; no rollback acceptance | Accepted output may await reconciliation; preserve actual failure | OP-16, OP-17, OP-18, OP-23 | P05-03, P05-04, P05-05, P05-06, NATIVE-02 | Какой durable completion/witness protocol и qualification evidence нужны до реализации? | No | OPEN / unresolved whole parameter |
| OP-20 | OPERATIONAL / P5 | Exact authorized isolated Windows10/11 CPU-only or other chosen platform. | Separate exact authorized host/profile selection and native qualification task | Isolated Windows10/11 CPU-only profile; another explicitly chosen platform profile | No Linux→Windows inference, SCM/ACL/DPAPI not implied | Actual FFmpeg/fonts/subtitles/path/playback must be observed later | OP-12, OP-17, OP-19 | NATIVE-01, NATIVE-02, NATIVE-03 | Какой isolated host/profile и bounded admin/test scope будет разрешён отдельно, без установки сейчас? | No | OPEN / unresolved whole parameter |
| OP-21 | OPERATIONAL / P5 | Private by default; export/readers/custodian/retention/erase separate. | Private content/evidence by default, per-purpose access/export/retention/erase policy OPEN | Local private custodian only; reviewed redacted disclosure with exact allowlist | No public cards/licenses/identities/MP4 by default, hashes not anonymity | Controlled reviewer access versus leakage and retention cost | OP-14, OP-19, OP-23 | P05-07, NATIVE-03 | Кто custodian/readers, какие сроки/удаление и отдельное export scope требуются? | No | OPEN / unresolved whole parameter |
| OP-22 | PURE / P2 | Add explicit plan bindings for toolchain/executor OR narrow reapproval rules with exact references. | Proposed RenderPlanV2 mandates immutable toolchain/executor refs; new plan/SubjectKey on any change | New closed schema family/profile, no implicit migration; explicit versioned compatibility route after independent approval | No caller overrides or old SubjectKey equivalence; technical reapproval not grant | Content/rights changes need corresponding review; technical changes policy still open | OP-05, OP-09 | V074, V075, V076, V077, V078, V079, V080, P04-02 | Утвердить pure V2 field/ref delta и reject-legacy policy как proposal baseline, оставив reapproval protocol отдельному решению? | Yes | OPEN / ready question |
| OP-23 | OPERATIONAL / P5 | Freeze separate schemas for code manifest/environment/identity/grant/admission/completion/inspection receipts. | Enumerate versioned identity/grant/admission/completion/inspection/manifest payload contracts; real protocol OPEN | Protected broker receipts; trusted signed receipts with qualified registry/channel; neither selected | ByteRef/signature format not trust; no trusted=true fixture grant | Full valid semantic examples depend on these contracts | OP-09, OP-15, OP-24 | P01-01, P02-01, P03-01, P04-10, P05-01 | Какие concrete payload protocols/trust roots должны быть отдельным design scope до freeze? | No | OPEN / unresolved whole parameter |
| OP-24 | MIXED / P4 | Distinguish SubjectKey root content/use policy, actor authority, rights policy, issuer/executor/output profiles. | Pure role-separated PolicyRef namespaces with exact id/version/hash comparison; current registry OPEN | Explicit typed role fields; role-tagged versioned policy references, no implicit interchange | A rights policy cannot masquerade as issuer/authority/output policy | Clear review invalidation without forcing runtime before schema review | OP-09, OP-22 | P02-01, P03-08, P04-03 | Утвердить pure policy-role mapping отдельно от actual registry/authority/currentness? | Yes | OPEN / unresolved whole parameter |
| OP-25 | MIXED / P4 | Exact original input+pinned full recomputation; never guess redacted diagnostics. | Pure original-bytes/code/runtime/context/full-result binding contract; actual collector/recomputation OPEN | New collector preserving G2; unavailable original→diagnostics-only deny, no reconstruction | G2 redacted diagnostics cannot become full evaluator result by guessing | Editor may need new snapshot/review; no hidden replacement | OP-05, OP-09 | P01-02, P01-04, P01-08 | Утвердить exact snapshot collection interface requirements без запуска recomputation/providers? | Yes | PROPOSED / unresolved whole parameter |
| OP-26 | PURE / P1 | Keep STRUCTURALLY_VALID descriptive only; no new machine enum. | STRUCTURALLY_VALID descriptive only; API remains CONSISTENT_NO_AUTHORITY/DENY | Keep descriptive annotation; any future machine status only separate explicit version decision | Shape cannot be mistaken for grant or operation permission | Clear report/UI separation, no misleading green light | None | COMMON-02, P01-01, P04-10 | Утвердить descriptive-only structural label без нового machine enum? | Yes | PROPOSED / ready question |
| OP-27 | PURE / P1 | 21 existing proposed codes; fixed localized messages; deterministic branch precedence. | Preserve actual21-code proposed catalogue, safe fixed messages and stage/tie policy | Single public primary code+private trace; ordered safe error list with same earliest-stage primary | No raw paths/IDs/secrets/exception dumps; do not leak role/credential details | Actionable fixed messages, private review detail separate | None | COMMON-06, P05-07 | Утвердить fixed safe public-message proposal и separation private details, не меняя21 codes? | Yes | PROPOSED / ready question |
| OP-28 | OPERATIONAL / P5 | Negative tombstone does not expire into old approve; current history authentic. | Immutable negative history/tombstones; no expiry revival of prior approve; actual authority/recovery protocol OPEN | Protected append-only history with reconciliation; qualified externally anchored history | Grant expiry not history deletion; compromised/rollback state denies recognition | New authentic decision restores only exact reviewed scope | OP-12, OP-15, OP-16, OP-23 | P02-04, P02-05, P02-06, P02-07 | Утвердить tombstone/history semantics отдельно от trusted event protocol и retention policy? | No | PROPOSED / unresolved whole parameter |

## 4. Exact source, migration and detailed decision cards

Следующие цитаты — исходные literal records pinned A file в accepted B tree. Они не новые approvals. Для OP-06/08/22 resolved architectural subchoices следует читать вместе с B decisions, не возвращать историческое BLOCKED как актуальное решение X01–X04.

### OP-01 — Envelope bytes

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-01`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: 8388608 full wire bytes, inclusive.
> - Rationale: Bound IO before decode; whitespace counts.
> - Security impact: Prevents unbounded inputs, not total memory proof.
> - Product impact: Very large docs via ByteRef.
> - Dependent vectors/oracles: V058,V059.
> - Owner decision required: Утвердить число и input-vs-canonical accounting.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: 8MiB=8388608 inclusive full wire bytes before decode; ByteRef content отдельно.
- Alternatives: 4MiB conservative;16MiB large dossier.
- Security / product: Reject before unbounded buffer growth; wire cap alone not memory proof; Large dossiers move media/excerpts to refs, whitespace counts against cap.
- Hard dependencies: None.
- Related exact IDs: V058, V059, COMMON-04.
- Migration/version impact: Profile/hash unchanged, acceptance boundary versioned.
- Exact owner question (not answered here): **Утвердить8MiB inclusive wire cap с отдельным canonical accounting, без утверждения memory safety?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-02 — Nesting

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-02`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: 64; scalar0, root container1.
> - Rationale: Remove off-by-one ambiguity.
> - Security impact: Bound recursion; do not rely on stdlib default.
> - Product impact: Deep real dossier may require flattening.
> - Dependent vectors/oracles: V054,V055.
> - Owner decision required: Утвердить depth/counting semantics.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: 64 containers; scalar0/root container1; nested container+1, arrays=objects.
- Alternatives: 32 for conservative parsing;96 only separately profiled.
- Security / product: Explicit counter avoids off-by-one/stack assumptions; Deep dossiers may need flatter refs; no implicit normalization.
- Hard dependencies: None.
- Related exact IDs: V054, V055, COMMON-04.
- Migration/version impact: Boundary policy version changes, no input rewrite.
- Exact owner question (not answered here): **Утвердить depth64 и указанный counting model, без native stack qualification?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-03 — String bytes

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-03`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: 65536 UTF8 bytes, keys and values.
> - Rationale: Unicode bytes versus characters/escape text.
> - Security impact: Avoid memory amplification; escaped wire still bounded separately.
> - Product impact: Large excerpts stored immutable ByteRef.
> - Dependent vectors/oracles: V052,V053.
> - Owner decision required: Утвердить size и decoded measurement.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: 65536 decoded UTF8 bytes for each key/value string, normalization forbidden.
- Alternatives: 32768 conservative;131072 separately bounded profile.
- Security / product: Count emitted decoded bytes before append, escaped wire still cap W; Long quotations use ByteRef; codepoint count is not byte count.
- Hard dependencies: OP-05.
- Related exact IDs: V052, V053, COMMON-03.
- Migration/version impact: Profile boundary version, no Unicode rewriting.
- Exact owner question (not answered here): **Утвердить65536 bytes для decoded keys/values и separate raw wire accounting?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-04 — Lists

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-04`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: 10000 per list plus explicit field minima/uniqueness.
> - Rationale: No root-only shortcut.
> - Security impact: Total object count remains separate.
> - Product impact: Large evidence inventories need budgets.
> - Dependent vectors/oracles: V056,V057.
> - Owner decision required: Утвердить numeric list cap и per-field cardinalities.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: 10000 elements per array; tighter per-field limits; global node/token bounds independent.
- Alternatives: 2000 conservative;20000 only separate large profile.
- Security / product: Nested many-array attack still needs OP-07, object members separate; Large asset arrays may need bounded partitions, never silent truncation.
- Hard dependencies: None.
- Related exact IDs: V056, V057, COMMON-04.
- Migration/version impact: List-policy version, arrays preserve order.
- Exact owner question (not answered here): **Утвердить per-array10000 без утверждения global parser budget?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-05 — Canonical edge cases

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-05`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Signed64, -0→0; decoded paired surrogate allowed, no normalization; codepoint sort.
> - Rationale: One exact byte sequence.
> - Security impact: Avoid hash ambiguity/SI interchange.
> - Product impact: Interoperability across languages.
> - Dependent vectors/oracles: V003–018,V046–050,V067.
> - Owner decision required: Утвердить proposed lexical rules/edge vectors, not implicit serializer defaults.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: Signed64/no float; -0→0; Unicode scalars/codepoint keys/exact escaping/domain C14N-1.
- Alternatives: External canonical standard with explicit compatibility map; current byte model with approved independent conformance set.
- Security / product: No SI/G2 hash interchange, duplicate keys after unescape reject; Stable cross-language snapshots, authored Unicode untouched.
- Hard dependencies: None.
- Related exact IDs: V001, V003, V005, V011, V017, V046, V047, V067, COMMON-02, COMMON-05.
- Migration/version impact: No silent algorithm/namespace fallback; any canonical byte change new version.
- Exact owner question (not answered here): **Утвердить полный finite canonical rule set P1, включая -0 и paired escapes, не меняя existing vectors?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-06 — Error priority X01/X02

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-06`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Explicit schema→local hash→refs→semantics; choose empty Text/mode error mapping.
> - Rationale: Source expectations inconsistent.
> - Security impact: Ambiguous denial classification may break clients/tests.
> - Product impact: Clear corrective messages without unsafe repair.
> - Dependent vectors/oracles: V039,V051.
> - Owner decision required: Выбрать primary codes; пересмотреть исходный oracle явно.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Retain X01/X02 exactly; add deterministic within-stage tie policy and missing-error mappings.
- Alternatives: First canonical field/identity order; fixed code-priority within earliest failed stage.
- Security / product: Never later semantic/provider error supersedes earlier approved stage; Stable corrections without coercion or masking product gaps.
- Hard dependencies: OP-27.
- Related exact IDs: V039, V051, V071, V073, COMMON-06.
- Migration/version impact: Error-selection policy version; do not reopen approved X decisions.
- Exact owner question (not answered here): **Утвердить proposed residual tie matrix P1, сохраняя X01/X02 без пересмотра?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-07 — Parser resources

- Classification / primary: PURE / P3.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-07`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Separate CPU/time/memory/object-count/token budget; no number approved.
> - Rationale: 8MiB is not enough to bound allocations.
> - Security impact: DoS protection per parser/executor.
> - Product impact: Avoid arbitrary rejection of legitimate dossiers.
> - Dependent vectors/oracles: V052–059; new probes after decision.
> - Owner decision required: Назвать numeric resource budget and accounting model.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Three logical counter profiles; CPU/time/RAM coefficients remain OPEN pending separate measurements.
- Alternatives: Streaming/bounded builder; arena/DOM with explicit logical budgets and qualification.
- Security / product: Bound nodes/tokens/decoded data before growth; no fabricated runtime ceilings; Some legitimate large dossiers rejected, explicit retry with reviewed profile only.
- Hard dependencies: OP-01, OP-02, OP-03, OP-04, OP-09.
- Related exact IDs: V052, V058, V059, COMMON-04.
- Migration/version impact: Resource-profile version; no fallback to unbounded parser.
- Exact owner question (not answered here): **Какой logical profile выбрать для будущего тестового scope и какие evidence нужны до выбора CPU/RAM/time caps?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-08 — Closure bound/cycle fixtures X03

- Classification / primary: PURE / P3.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-08`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Options bounded nodes/edges/ref depth; define abstract graph fixture vs digest-valid closure.
> - Rationale: Cannot fake content-addressed cyclic hashes.
> - Security impact: Limit traversal, reject duplicates and malicious graphs.
> - Product impact: Large histories need explicit separate bounded reads.
> - Dependent vectors/oracles: V041–043.
> - Owner decision required: Утвердить limits/edge model и cycle test design without forged hashes.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Typed closure counters+dedup rules; profile limits in P3 PROPOSED, actual selection OPEN.
- Alternatives: Conservative ref cap; balanced/large profiled cap, no unbounded traversal.
- Security / product: Count edges even shared/repeated, distinct identities once; abstract cycle≠crypto closure; Deep historical graphs may need explicit bounded slices.
- Hard dependencies: OP-07, OP-09.
- Related exact IDs: V041, V042, V043, V043-S, V043-S4, V043-S6, P02-04.
- Migration/version impact: Closure profile version; X03 fixed separation, no fake digests.
- Exact owner question (not answered here): **Утвердить closure accounting и выбрать numeric profile только после OP-07 review, не признавая crypto-cycle coverage?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-09 — Reference stages

- Classification / primary: PURE / P2.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-09`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Local hash-first, conflict registry, exact typed edges; clarify opaque ByteRef decoding.
> - Rationale: No latest fallback; avoid hidden schema edges.
> - Security impact: Resolve closure exactly before trusting metadata.
> - Product impact: Readable immutable history remains separate.
> - Dependent vectors/oracles: V022,V041–043.
> - Owner decision required: Утвердить target key/closure order and historical edges.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: Exact typed identity/revision/hash refs, conflict reject, no latest fallback, separate semantic payload profiles.
- Alternatives: Strict exact closed family; explicitly versioned compatibility adapters after separate approval.
- Security / product: No duplicate identity substitution or hidden ref discovery in arbitrary JSON; Reproducible snapshot/history diagnostics without authority claims.
- Hard dependencies: OP-05, OP-06.
- Related exact IDs: V022, V041, V042, P01-05, P02-04.
- Migration/version impact: No silent migration; reference/schema version explicit.
- Exact owner question (not answered here): **Утвердить pure reference model P2 без подтверждения latest head/OS/store?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-10 — Instant/clock

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-10`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: 0…253402300799 epochsec; skew/uncertainty/time authority not selected.
> - Rationale: Timestamp syntax not clock trust.
> - Security impact: Rollback/uncertainty must deny admission.
> - Product impact: Offline diagnostics may remain available.
> - Dependent vectors/oracles: V060–063,V069.
> - Owner decision required: Утвердить range, precision, uncertainty and provider.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Pure Instant signed domain0…253402300799 epochsec; external time authority/skew OPEN.
- Alternatives: Whole-second fixed domain; explicit precision/version extension, no local-time fallback.
- Security / product: Uncertain clock denies operation, timestamp syntax not authenticity; Diagnostics can remain offline; real scheduling needs authority.
- Hard dependencies: OP-05.
- Related exact IDs: V060, V061, V062, V063, V069, P03-06.
- Migration/version impact: Time precision/domain version; no auto convert trust.
- Exact owner question (not answered here): **Утвердить pure timestamp domain отдельно от выбора clock source/uncertainty?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-11 — Expiry window

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-11`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Exclusive [from,until); max TTL/expected render margin not approved.
> - Rationale: Boundary predictable.
> - Security impact: Avoid expiry during long render or auto extension.
> - Product impact: May require new request after delay.
> - Dependent vectors/oracles: V063; P04-03/06.
> - Owner decision required: Утвердить TTL/duration/margin and lifecycle rules.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Pure [from,until) intersection; TTL/render margin OPEN until profile+clock evidence.
- Alternatives: Narrow per-attempt lease; bounded approved batch window, no auto extension.
- Security / product: Expiry at equality; negative tombstone persistence not TTL; Expired queued jobs need explicit new candidate, no bypass.
- Hard dependencies: OP-10.
- Related exact IDs: V063, P04-03, P04-06.
- Migration/version impact: Window policy version and fresh refs, not edit old approval.
- Exact owner question (not answered here): **Утвердить pure interval algebra, оставив TTL/margin и admission timing отдельному решению?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-12 — Revocation freshness

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-12`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Synchronous lease/checkpoint or bounded polling; interval unapproved.
> - Rationale: No stale cached APPROVE.
> - Security impact: Detect revoke/outage before successful commit.
> - Product impact: Cancellation/review latency tradeoff.
> - Dependent vectors/oracles: P02-05/06,P04-06.
> - Owner decision required: Выбрать monitoring protocol, deadlines and outage behavior.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Design lease/checkpoints or bounded poll protocol; no selected polling number.
- Alternatives: Synchronous trusted lease; bounded poll with conservative fail-stop on outage.
- Security / product: Revoked/unknown state cannot become successful commit; bounded detection must be proven; Cancellation latency versus provider availability.
- Hard dependencies: OP-10, OP-11, OP-15, OP-23.
- Related exact IDs: P02-05, P02-06, P04-06.
- Migration/version impact: Protocol epoch/version, no cached APPROVE fallback.
- Exact owner question (not answered here): **Какой revocation protocol/lag/outage policy выбрать для последующего отдельного qualification task?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-13 — Rights applicability

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-13`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Versioned required layers per asset/use/jurisdiction; generated not exemption.
> - Rationale: Actual legal/consent review.
> - Security impact: Missing rights layer denies use.
> - Product impact: May exclude music/voices/stock from first bounded scope.
> - Dependent vectors/oracles: P03-01…08.
> - Owner decision required: Утвердить competence/jurisdiction/layer and intended-use policy.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Pure exact asset/use/layer coverage; required legal layers/jurisdictions and competent reviewer OPEN.
- Alternatives: Narrow no-external-media scope; reviewed licensed asset policy by actual usage.
- Security / product: No inferred rights/public-domain/generated exemption, commercial/territory/time intersection; Scientific/creative suitability distinct from license permission.
- Hard dependencies: OP-14, OP-18, OP-24.
- Related exact IDs: P03-01, P03-03, P03-04, P03-05, P03-07, PRODUCT-02.
- Migration/version impact: Rights policy version changes invalidate affected scope, never auto transfer.
- Exact owner question (not answered here): **Какие jurisdictions/layers/intended-use policy и reviewer evidence требуется отдельно утвердить?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-14 — Reviewer independence

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-14`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: OS-derived identity + per-role authority; explicit self-review/dual-role policy.
> - Rationale: Separate competence/editorial/rights.
> - Security impact: Do not assume user is all-gate admin.
> - Product impact: Small team workflow versus independent scrutiny.
> - Dependent vectors/oracles: P02-02/03/08; PRODUCT01–07.
> - Owner decision required: Назвать allowed roles, conflicts, mandatory declarations/competence.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Pure role/scope/decision/session/declaration fields; real assignments/competence/independence OPEN.
- Alternatives: Separate reviewer roles; explicit controlled dual-role policy with conflict evidence.
- Security / product: No current-user all-rights, auto self-approval or title-as-competence; Small-team feasibility versus actual independent scrutiny.
- Hard dependencies: OP-24.
- Related exact IDs: P02-02, P02-03, P02-08, PRODUCT-06.
- Migration/version impact: Authority/review policy versions, preserve A1–A14/O1–O10.
- Exact owner question (not answered here): **Какие роли/конфликты/qualification evidence разрешены policy, без назначения конкретных лиц сейчас?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-15 — Authority/state provider

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-15`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Qualified S3, separately qualified alternative, or production remains blocked.
> - Rationale: Existing source PURE_ONLY not service.
> - Security impact: Need authenticated heads, grants, rollback protection.
> - Product impact: Preview/D1 remain usable without production.
> - Dependent vectors/oracles: P02-05,P04-04/10,NATIVE03.
> - Owner decision required: Выбрать project/profile; no implementation permission implied.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Define required provider properties; choose qualification project or remain production-blocked.
- Alternatives: Dedicated S3-native qualification; separate qualified provider; diagnostics-only defer.
- Security / product: Need authenticated grants/heads/anti-rollback, pure S3 model insufficient; Provider can be deferred without disabling safe previews.
- Hard dependencies: OP-14, OP-24.
- Related exact IDs: P02-05, P04-04, P04-10, NATIVE-03.
- Migration/version impact: Provider/epoch trust transition explicit, no data-only upgrade.
- Exact owner question (not answered here): **Выбрать отдельный provider-design/qualification scope или оставить production заблокированным?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-16 — Single attempt recovery

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-16`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Reserve before spawn; unknown→reconcile, no rerender; exact durable protocol pending.
> - Rationale: At-most-one admission not exactly-once physical work.
> - Security impact: Prevent replay after crash/lost ACK.
> - Product impact: Manual new grant may be needed.
> - Dependent vectors/oracles: P04-04/05,P05-05.
> - Owner decision required: Утвердить ledger/event/retry/reconciliation semantics.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: Durable single-attempt admission before spawn; unknown→reconcile, no automatic rerender.
- Alternatives: Protected local ledger; separately qualified transactional authority, not RAM-only state.
- Security / product: At-most-one admission not exactly-once physical execution; lost ACK lookup safe; Manual recovery/new grant may be needed after uncertain crash.
- Hard dependencies: OP-08, OP-15, OP-23.
- Related exact IDs: P04-04, P04-05, P05-05.
- Migration/version impact: Incarnation/attempt IDs and recovery epoch changes explicit.
- Exact owner question (not answered here): **Утвердить recovery semantics и требования ledger-протокола без запуска/выдачи grant?**
- Implementation prerequisite: No (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-17 — Immutable resolver

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-17`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Opaque content IDs, held qualified identities/handles; no caller paths/PATH/network.
> - Rationale: JSON hash check not TOCTOU control.
> - Security impact: OS/symlink/reparse/mount protection needs host proof.
> - Product impact: Private staging and asset availability.
> - Dependent vectors/oracles: P04-07,NATIVE01.
> - Owner decision required: Выбрать actual resolver/store/OS proof model.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Opaque immutable IDs plus held verified file identities; actual OS/store protocol OPEN.
- Alternatives: Qualified broker/content store handles; qualified private snapshot/package with anchored opens.
- Security / product: No caller path/PATH override, TOCTOU/reparse/mount behavior needs OS proof; Availability/staging cost explicit, no network material recovery.
- Hard dependencies: OP-22, OP-23.
- Related exact IDs: P04-07, NATIVE-01.
- Migration/version impact: Resolver/profile version; old path-based assumptions not migrated silently.
- Exact owner question (not answered here): **Какой resolver threat model/OS evidence contract выбрать для отдельного review?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-18 — Output profiles

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-18`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Exact RU/UK batch, codecs, dimensions/fps, subtitle/attribution/tool/font checks; numeric profile unapproved.
> - Rationale: Expected outputs not invented hashes.
> - Security impact: Reject partial/wrong toolchain outputs.
> - Product impact: Real readability/language/playback still human checks.
> - Dependent vectors/oracles: P04-02/08,P05-01/02/06.
> - Owner decision required: Утвердить closed profile schema/versions and constraints.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Pure closed expected RU/UK outputs/tools/config/attribution profile refs; actual media limits/quality OPEN.
- Alternatives: One exact RU/UK batch; explicitly separate per-locale authorizations after scope review.
- Security / product: No success by file existence; no tool/font override; Readability/Cyrillic/playback/content quality still human/host checks.
- Hard dependencies: OP-22, OP-24.
- Related exact IDs: P04-02, P04-08, P05-01, P05-02, P05-06.
- Migration/version impact: Output profile version plus new plan/candidate, X04 binding retained.
- Exact owner question (not answered here): **Утвердить profile fields/coverage отдельно от codecs/duration thresholds и real runtime qualification?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-19 — Evidence durability

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-19`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Atomic index/head/output binding + independent completion witness; storage protocol unselected.
> - Rationale: No success from existing MP4/marker alone.
> - Security impact: Crash/rollback/partial evidence→unknown.
> - Product impact: May delay accepted results until reconciliation.
> - Dependent vectors/oracles: P05-03…06,NATIVE02.
> - Owner decision required: Утвердить durable protocol/qualification, not RAM model.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Specify invariant ledger↔index↔actual outputs; actual durable commit/witness protocol OPEN.
- Alternatives: Qualified single-store atomic protocol; qualified journal/commit+reconciliation protocol.
- Security / product: Orphan/truncated evidence INDETERMINATE, not success; no rollback acceptance; Accepted output may await reconciliation; preserve actual failure.
- Hard dependencies: OP-16, OP-17, OP-18, OP-23.
- Related exact IDs: P05-03, P05-04, P05-05, P05-06, NATIVE-02.
- Migration/version impact: Evidence schema/protocol/profile version and retained history.
- Exact owner question (not answered here): **Какой durable completion/witness protocol и qualification evidence нужны до реализации?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-20 — Windows/host qualification

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-20`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Exact authorized isolated Windows10/11 CPU-only or other chosen platform.
> - Rationale: No Linux→Windows inference.
> - Security impact: Services/ACL/DPAPI/native writer need separate approval.
> - Product impact: Actual codecs/fonts/Cyrillic/playback/path compatibility.
> - Dependent vectors/oracles: NATIVE01…03.
> - Owner decision required: Назвать host/profile/admin scope only in separate task.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Separate exact authorized host/profile selection and native qualification task.
- Alternatives: Isolated Windows10/11 CPU-only profile; another explicitly chosen platform profile.
- Security / product: No Linux→Windows inference, SCM/ACL/DPAPI not implied; Actual FFmpeg/fonts/subtitles/path/playback must be observed later.
- Hard dependencies: OP-12, OP-17, OP-19.
- Related exact IDs: NATIVE-01, NATIVE-02, NATIVE-03.
- Migration/version impact: Host/build/runtime/artifact changes require requalification.
- Exact owner question (not answered here): **Какой isolated host/profile и bounded admin/test scope будет разрешён отдельно, без установки сейчас?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-21 — Privacy/retention/disclosure

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-21`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Private by default; export/readers/custodian/retention/erase separate.
> - Rationale: Hashes also not anonymity.
> - Security impact: No public cards/licenses/identities/raw stderr/upload by default.
> - Product impact: Review access without leaking material.
> - Dependent vectors/oracles: P05-07,NATIVE03.
> - Owner decision required: Утвердить exact content/access/retention/export boundary.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Private content/evidence by default, per-purpose access/export/retention/erase policy OPEN.
- Alternatives: Local private custodian only; reviewed redacted disclosure with exact allowlist.
- Security / product: No public cards/licenses/identities/MP4 by default, hashes not anonymity; Controlled reviewer access versus leakage and retention cost.
- Hard dependencies: OP-14, OP-19, OP-23.
- Related exact IDs: P05-07, NATIVE-03.
- Migration/version impact: Disclosure/retention version, old private data not automatically public.
- Exact owner question (not answered here): **Кто custodian/readers, какие сроки/удаление и отдельное export scope требуются?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-22 — Toolchain SubjectKey X04

- Classification / primary: PURE / P2.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-22`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Add explicit plan bindings for toolchain/executor OR narrow reapproval rules with exact references.
> - Rationale: Current discovery statement not backed by fields.
> - Security impact: Auth changes but old human SubjectKey may otherwise persist.
> - Product impact: May trigger review on tool/profile change.
> - Dependent vectors/oracles: P01-05,P04-02/08.
> - Owner decision required: Утвердить concrete schema change/version; not silently freeze.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Proposed RenderPlanV2 mandates immutable toolchain/executor refs; new plan/SubjectKey on any change.
- Alternatives: New closed schema family/profile, no implicit migration; explicit versioned compatibility route after independent approval.
- Security / product: No caller overrides or old SubjectKey equivalence; technical reapproval not grant; Content/rights changes need corresponding review; technical changes policy still open.
- Hard dependencies: OP-05, OP-09.
- Related exact IDs: V074, V075, V076, V077, V078, V079, V080, P04-02.
- Migration/version impact: Explicit schema/version/migration refusal, new raw plan digest.
- Exact owner question (not answered here): **Утвердить pure V2 field/ref delta и reject-legacy policy как proposal baseline, оставив reapproval protocol отдельному решению?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-23 — Opaque evidence payloads

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-23`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Freeze separate schemas for code manifest/environment/identity/grant/admission/completion/inspection receipts.
> - Rationale: ByteRef syntax not evidence semantics.
> - Security impact: No fake trusted=true receipts or keys.
> - Product impact: Full positive fixtures depend on these profiles.
> - Dependent vectors/oracles: P01-01,P02-01,P03-01,P04-10,P05-01.
> - Owner decision required: Утвердить protocol schemas/providers before full consistent examples.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Enumerate versioned identity/grant/admission/completion/inspection/manifest payload contracts; real protocol OPEN.
- Alternatives: Protected broker receipts; trusted signed receipts with qualified registry/channel; neither selected.
- Security / product: ByteRef/signature format not trust; no trusted=true fixture grant; Full valid semantic examples depend on these contracts.
- Hard dependencies: OP-09, OP-15, OP-24.
- Related exact IDs: P01-01, P02-01, P03-01, P04-10, P05-01.
- Migration/version impact: Receipt/profile versions and trust-root transition explicit.
- Exact owner question (not answered here): **Какие concrete payload protocols/trust roots должны быть отдельным design scope до freeze?**
- Implementation prerequisite: No (pure-only definition above); status OPEN, NOT APPROVED.

### OP-24 — Policy namespaces

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-24`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Distinguish SubjectKey root content/use policy, actor authority, rights policy, issuer/executor/output profiles.
> - Rationale: Same PolicyRef type does not imply same authority.
> - Security impact: Prevent wrong-policy reuse and scope confusion.
> - Product impact: Explicit revisions invalidate related decisions.
> - Dependent vectors/oracles: P02-01,P03-08,P04-03.
> - Owner decision required: Утвердить comparison/equality/expiry rules per policy role.
> - Status: **OPEN**, NOT APPROVED.

- Recommended decision: Pure role-separated PolicyRef namespaces with exact id/version/hash comparison; current registry OPEN.
- Alternatives: Explicit typed role fields; role-tagged versioned policy references, no implicit interchange.
- Security / product: A rights policy cannot masquerade as issuer/authority/output policy; Clear review invalidation without forcing runtime before schema review.
- Hard dependencies: OP-09, OP-22.
- Related exact IDs: P02-01, P03-08, P04-03.
- Migration/version impact: Namespace/tag changes require schema version; no fallback.
- Exact owner question (not answered here): **Утвердить pure policy-role mapping отдельно от actual registry/authority/currentness?**
- Implementation prerequisite: Yes (pure-only definition above); status OPEN, NOT APPROVED.

### OP-25 — G2 snapshot collection

- Classification / primary: MIXED / P4.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-25`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Exact original input+pinned full recomputation; never guess redacted diagnostics.
> - Rationale: Current G2 preserved.
> - Security impact: Avoid forged complete result/currentness.
> - Product impact: Unavailable inputs mean diagnostics-only.
> - Dependent vectors/oracles: P01-02/04/08.
> - Owner decision required: Утвердить collector contract and code/runtime manifest, docs-only now.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: Pure original-bytes/code/runtime/context/full-result binding contract; actual collector/recomputation OPEN.
- Alternatives: New collector preserving G2; unavailable original→diagnostics-only deny, no reconstruction.
- Security / product: G2 redacted diagnostics cannot become full evaluator result by guessing; Editor may need new snapshot/review; no hidden replacement.
- Hard dependencies: OP-05, OP-09.
- Related exact IDs: P01-02, P01-04, P01-08.
- Migration/version impact: New collector/snapshot refs; G2 output and SI/PD-01 unchanged.
- Exact owner question (not answered here): **Утвердить exact snapshot collection interface requirements без запуска recomputation/providers?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-26 — Structural status

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-26`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Keep STRUCTURALLY_VALID descriptive only; no new machine enum.
> - Rationale: No namespace expansion by docs.
> - Security impact: Prevent shape success treated as grant.
> - Product impact: Clear user reporting versus API verdict.
> - Dependent vectors/oracles: COMMON02,P01-01,P04-10.
> - Owner decision required: Если нужен machine status — отдельное explicit owner решение/version.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: STRUCTURALLY_VALID descriptive only; API remains CONSISTENT_NO_AUTHORITY/DENY.
- Alternatives: Keep descriptive annotation; any future machine status only separate explicit version decision.
- Security / product: Shape cannot be mistaken for grant or operation permission; Clear report/UI separation, no misleading green light.
- Hard dependencies: None.
- Related exact IDs: COMMON-02, P01-01, P04-10.
- Migration/version impact: No wire/status namespace change now.
- Exact owner question (not answered here): **Утвердить descriptive-only structural label без нового machine enum?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-27 — Errors/privacy

- Classification / primary: PURE / P1.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-27`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: 21 existing proposed codes; fixed localized messages; deterministic branch precedence.
> - Rationale: No raw caller path/exception echo.
> - Security impact: Fail closed on unknown provider error.
> - Product impact: Useful corrections without invented automatic repairs.
> - Dependent vectors/oracles: COMMON06,P05-07.
> - Owner decision required: Утвердить safe catalog and exact branch/order semantics.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: Preserve actual21-code proposed catalogue, safe fixed messages and stage/tie policy.
- Alternatives: Single public primary code+private trace; ordered safe error list with same earliest-stage primary.
- Security / product: No raw paths/IDs/secrets/exception dumps; do not leak role/credential details; Actionable fixed messages, private review detail separate.
- Hard dependencies: None.
- Related exact IDs: COMMON-06, P05-07.
- Migration/version impact: Message/catalogue selection version; no new PG/SI error codes.
- Exact owner question (not answered here): **Утвердить fixed safe public-message proposal и separation private details, не меняя21 codes?**
- Implementation prerequisite: Yes (pure-only definition above); status PROPOSED, NOT APPROVED.

### OP-28 — Review validity/tombstones

- Classification / primary: OPERATIONAL / P5.
- Exact source: `0d6d9076ab535c1b258206beb4e4fe9c005e79e1:docs/tasks/G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, heading `OP-28`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`.

> - Proposed value/options: Negative tombstone does not expire into old approve; current history authentic.
> - Rationale: valid_until effect must be distinct from history permanence.
> - Security impact: Prevent revival/replay.
> - Product impact: New authentic decision restores only exact reviewed scope.
> - Dependent vectors/oracles: P02-04…07.
> - Owner decision required: Утвердить event validity/authority/history interaction.
> - Status: **PROPOSED**, NOT APPROVED.

- Recommended decision: Immutable negative history/tombstones; no expiry revival of prior approve; actual authority/recovery protocol OPEN.
- Alternatives: Protected append-only history with reconciliation; qualified externally anchored history.
- Security / product: Grant expiry not history deletion; compromised/rollback state denies recognition; New authentic decision restores only exact reviewed scope.
- Hard dependencies: OP-12, OP-15, OP-16, OP-23.
- Related exact IDs: P02-04, P02-05, P02-06, P02-07.
- Migration/version impact: History/epoch migration preserves negative records and provenance.
- Exact owner question (not answered here): **Утвердить tombstone/history semantics отдельно от trusted event protocol и retention policy?**
- Implementation prerequisite: No (pure-only definition above); status PROPOSED, NOT APPROVED.

## 5. Approval sequence without circularity

1. Review P1 together: canonical/size/depth/string/list/error/status choices, X01/X02 unchanged. No real clock/state/issuer/provider needed to accept these **contract choices**; no test/runtime qualification implied.
2. Review P2 reference/version/mandatory-binding schema choices OP-09/22 and secondary OP-24 pure role typing. OP-08 abstract graph split remains X03, numbers left P3.
3. Review P3 logical profiles OP-07/08 with P1/P2 counting units. CPU/RAM/time ceilings remain OPEN until separately authorized measured evidence; no invented benchmark.
4. Review P4 pure projections and separate actual policy/roles/rights/clock/collector decisions. Partial schema acceptance does not create trusted facts.
5. Review P5 governance alternatives; only a later scoped host/provider/executor/evidence project could seek qualification. Production and G3.2.1 remain blocked until separate owner tasks.

Decision graph is acyclic. Topological order computed from matrix hard edges (not a command to execute work):

OP-01, OP-02, OP-05, OP-03, OP-04, OP-27, OP-06, OP-09, OP-07, OP-08, OP-10, OP-11, OP-22, OP-24, OP-14, OP-15, OP-23, OP-12, OP-18, OP-13, OP-16, OP-17, OP-19, OP-20, OP-21, OP-25, OP-26, OP-28.

No primary P1 dependency outside P1 and no P1 requirement for operational provider. P2/P3/P4/P5 coverage is not a permission pipeline: design dependencies and real trust dependencies are different. P5 runtime observations can invalidate a later implementation/profile but do not retroactively require connecting a provider before discussing P1.

## 6. Evidence, conflicts and remaining blockers

Pinned source catalogue actually contains21 proposed codes; extracted from its explicit catalogue, excluding verification annotations/mentions of nonexistent PG_VERSION.87 vector IDs and58 oracle IDs in accepted B used as cross-references, not re-executed semantic tests. P1 recommendations compared by inspection against -0, Unicode, key order, bounds and B error-pair vectors; no existing vectors/hashes/expected results changed.

No new normative contradiction found: A open-record phrases about choosing X01–X04 are historical and explicitly superseded by accepted B; profiles with different limits are named alternatives, not conflicting universal expectations. Resource figures are **proposal workload caps**, not measurements or safe native thresholds. Remaining blockers: owner selections, parser accounting/CPU/RAM qualification, real policy/product/scientific/rights review, provider/revocation/time/ledger/resolver/executor/evidence/host qualification, version/migration/reapproval and disclosure. S3 not production-qualified; exactly-once physical execution not claimed.

Only offline Git/docs/counter arithmetic/cross-reference checks performed. No validators, rendering, application integration/native tests, provider/real identity/license operations or production qualification. [Acceptance packet](G3_2_0C_ACCEPTANCE_PACKET.md) records checks and final external handoff identity. **STOP — independent ChatGPT review and owner decision, no automatic next stage.**
