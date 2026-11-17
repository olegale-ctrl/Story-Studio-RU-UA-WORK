# Conformance and evidence plan — planned work is NOT_RUN

**PROPOSED — NOT APPROVED. OWNER_AUTHORIZED_DOCS_ONLY.**

SI-INTEGRATION-G3.2.0f; 2026-11-17 (Europe/Kyiv). No implementation, merge or production authority.

No new vectors, hash fixtures, validators or runtime tests are created in this stage. F-PLAN labels below are plan identifiers only, not claimed existing tests. Existing evidence is indexed by [inventory](G3_2_0F_SEVEN_PARTIAL_GAPS_INVENTORY.md); normative anchors per row are the approved D P1 IDs/X01–X04/P1-DIAG-01 there. Future scenarios do not establish new expected digests or undocumented error mappings.

| Evidence class | Meaning here | Current task execution |
|---|---|---|
| DOCUMENTARY_EVIDENCE | Pin sources, compare scope/IDs/status/alternatives/dependency graph | Performed for dossier only |
| OFFLINE_VECTOR_EVIDENCE | Future independently checked exact finite bytes/counts/hashes under selected contracts | NOT_RUN in F; historical source results only |
| RUNTIME_TEST_REQUIRED | Actual parser/IO/cache/result effects/output consumption | NOT_RUN |
| TRUSTED_PROVIDER_EVIDENCE_REQUIRED | Real identity/time/currentness/revocation/ledger/custody truth | NOT_RUN; blocked where absent |
| WINDOWS_NATIVE_QUALIFICATION_REQUIRED | Actual selected Windows10/11 CPU-only/NTFS/reparse/access/durability boundary | NOT_RUN; Linux/model evidence cannot substitute |

## F-PLAN-006 — CM-006: Aggregate byte limits after approved identity/accounting selection

Source status **PARTIAL unchanged**. Source/normative anchors: [D normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-01/P1-05; [C resource model](G3_2_0C_P3_RESOURCE_MODEL.md) §§1–5; [C reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §1; [E overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) CM-006. Existing IDs: COMMON-04, V058, V059, V066, E-V001.

- **Missing oracle and exact boundary conditions:** Selected L_Bunique/L_Bread/L_Wj at L−1,L,L+1; metadata length vs actual EOF; first excess byte; root8388608 separate from referenced bytes. No L selected now.
- **Required positive/negative fixtures:** Positive exact immutable reused object charged per selected policy; negative same identity changed bytes/length, repeated reread beyond budget, many small binaries, metadata lies and partial read.
- **Hash/domain controls:** Whole raw ByteRef length/SHA256 vs own-envelope DOMAIN; no prefix accepted as whole hash.
- **Adversarial cases:** Alias namespace churn, cache eviction/retry resets, large binary descriptor with tiny root.
- **Independent verification route:** Independent count/read transcript calculations and literal whole-byte hash checks after fixture authorisation; no generic resolver now.
- **Conditions for future complete status:** Approve F-D01/04 and numerical profile, publish boundary fixtures with independent results; require actual IO/cache/resource/resolver gates before whole requirement acceptance.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## F-PLAN-022 — CM-022: Global parsed-work limits

Source status **PARTIAL unchanged**. Source/normative anchors: [D normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-02/03/04; [C resource model](G3_2_0C_P3_RESOURCE_MODEL.md) §§1–4; [RESOLVE-1 narrow contract](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md) scope predicate; [E overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) CM-022. Existing IDs: COMMON-04, V052, V054, V056, V057, E-V002, E-V003.

- **Missing oracle and exact boundary conditions:** Selected N/T/D/M caps at L−1,L,L+1 across root+typed docs; empty/nonempty container formulas; duplicate/invalid prefix spent work; per-array10000 remains local.
- **Required positive/negative fixtures:** Positive exact counted trees; negative many individually small arrays, massive members/keys, escaped controls, long common-prefix keys and per-document budget reset.
- **Hash/domain controls:** No novel domain needed for arithmetic; if literal accepted value bytes later hashed, exact PG/raw domains only; denied malformed case not an accepted digest.
- **Adversarial cases:** Key/value node ambiguity, bool as Int, early rejected input still consumes huge unmetered state.
- **Independent verification route:** Two independent token/tree arithmetic derivations on published recipes, then separately instrumented runtime CPU/RSS/cancellation tests.
- **Conditions for future complete status:** Approve F-D02/04 profile units/numbers and separately qualify parser enforcement; arithmetic alone cannot make whole CM complete.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## F-PLAN-070 — CM-070: Established operational causes and chronology

Source status **PARTIAL unchanged**. Source/normative anchors: [D normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-06 residual stage6/7; [C operational governance](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md) §§2–6,9–10; [A/B oracle matrix](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md) COMMON-06/P04-05/P05-05; [RESOLVE-1 narrow contract](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md) preserved boundaries. Existing IDs: COMMON-06, P04-04, P04-05, P05-03, P05-05, NATIVE-02, NATIVE-03, E-V005, E-V006.

- **Missing oracle and exact boundary conditions:** For supplied claims, earliest stage wins; verify stage6/7 category boundaries, outage vs authenticated negative, missing/stale head, equal/uncertain time and crash event ordering. TTL/lag/uncertainty numbers remain OPEN.
- **Required positive/negative fixtures:** Positive supplied complete lineage and separately real verified terminal lookup; negatives forged/replayed provider evidence, rollback, lost ACK, crash before/after spawn/commit, partial causal logs.
- **Hash/domain controls:** Hash/ref equality on declared receipts binds bytes only; no digest proves actual clock/authority.
- **Adversarial cases:** Cached APPROVE during outage, unavailable misreported revoked, reordered timestamps and automatic rerender after uncertainty.
- **Independent verification route:** Future supplied-model oracles separately from actual authenticated provider/ledger/witness observations and independent fault audit.
- **Conditions for future complete status:** Pure F-D08 can close only claim model; whole CM needs F-D10 qualified provider/chronology protocol and actual evidence. BLOCKED_OPERATIONAL_EVIDENCE.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## F-PLAN-071 — CM-071: Typed closure and graph coverage

Source status **PARTIAL unchanged**. Source/normative anchors: [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X03; [B resolution evidence](G3_2_0B_RESOLUTION_AND_VECTOR_EVIDENCE.md) X03 fixture section; [C reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§1–2; [C resource model](G3_2_0C_P3_RESOURCE_MODEL.md) OP-08; [E overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) CM-071. Existing IDs: V022, V041, V042, V043, V043-S, V043-S1, V043-S2, V043-S3, V043-S4, V043-S5, V043-S6, P02-04.

- **Missing oracle and exact boundary conditions:** Selected U/E_occ/d_ref at L−1,L,L+1; repeated shared child counts1U/multipleE; JSON depth64 separate; exact target_revision equality, no inferred chronology.
- **Required positive/negative fixtures:** Positive literal real acyclic digest-valid closure; negatives dangling/conflicting/duplicate/wrong target raw/domain/revision; abstract self/2/3 cycles remain separate.
- **Hash/domain controls:** Independent local and exact target PG domain hashes; raw refs whole SHA256/length; no fake crypto-valid cycle literals.
- **Adversarial cases:** Opaque JSON secretly scanned as refs, latest fallback, alias identity collision and cycles disguised by stale hashes.
- **Independent verification route:** Separate structural graph oracle checks and independent hash equations for real supplied acyclic closures; never conflate labels.
- **Conditions for future complete status:** Approve F-D01/04/05 including numeric/profile semantics; documented real closure and abstract tests under selected scope, plus runtime resolver/resource gates for full enforcement.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## F-PLAN-072 — CM-072: Plan/schema/version/reapproval boundaries

Source status **PARTIAL unchanged**. Source/normative anchors: [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X04; [B resolution evidence](G3_2_0B_RESOLUTION_AND_VECTOR_EVIDENCE.md) X04 before/after; [C reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §3; [C policy projections](G3_2_0C_P4_POLICY_CONTRACTS.md) OP-13/14/18/24; [E overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) CM-072. Existing IDs: V074, V075, V076, V077, V078, V079, V080, P01-05, P04-02, P04-08.

- **Missing oracle and exact boundary conditions:** Every render-affecting change→new exact plan/SubjectKey; each mandatory ref present; old/new/unknown version acceptance explicit; content/rights/technical/unknown classes.
- **Required positive/negative fixtures:** Positive new profile literal with both bound targets; negatives missing refs, caller override, wrong target/header/hash, legacy passed as new, adapter drops provenance/reuses old approval.
- **Hash/domain controls:** Raw plan/toolchain/executor digests and lengths; PG envelope binding separately; one-byte/one-ref change propagates plan digest/subject.
- **Adversarial cases:** Version-string-only equality, technical misclassification, cross-role PolicyRef substitution.
- **Independent verification route:** Future independent literal-byte/hash/version matrix after schema selection; actual consumption/review/rights proof separate.
- **Conditions for future complete status:** Approve F-D06 exact types/versions/migration and F-D07 reapproval; whole CM additionally needs qualified consumption/identity and actual reviews where applicable.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## F-PLAN-073 — CM-073: Pure reporting and runtime no effects

Source status **PARTIAL unchanged**. Source/normative anchors: [D normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-26/27; [A/B oracle matrix](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md) P01-01/COMMON-06; [E overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) CM-073; [RESOLVE-1 narrow contract](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md) public/private boundary. Existing IDs: P01-01, COMMON-05, COMMON-06, V019, V058.

- **Missing oracle and exact boundary conditions:** Exact existing verdict values; STRUCTURALLY_VALID never machine enum; no grant/allow/production fields; DENY and incomplete context cannot claim whole-PG CONSISTENT.
- **Required positive/negative fixtures:** Positive external report byte fixture with fixed safe message; negatives hidden grant fields, schema-only E claimed whole-PG pass, malformed/unknown result version; later independently observed success/deny/failure no-effect cases.
- **Hash/domain controls:** Hash of report if selected is just integrity, no authority; no new domain invented here.
- **Adversarial cases:** Effect happens before correct DENY or is undone before inspection; self-reported zero calls masks filesystem/network/store operations.
- **Independent verification route:** Pure exact bytes/key/enum tests later; separately independent OS/process/network/file/state observer, not result-object assertions alone.
- **Conditions for future complete status:** Approve F-D03 output scope; report-only fixtures close subpart; whole CM requires F-D09 actual no-effects evidence with authorised OS boundary.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## F-PLAN-095 — CM-095: Publication/access/privacy/retention

Source status **PARTIAL unchanged**. Source/normative anchors: [D normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-27; [C operational governance](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md) OP-21/23/28; [A/B oracle matrix](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md) P05-07/NATIVE-03; [E overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) CM-095; [RESOLVE-1 narrow contract](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md) public/private boundary. Existing IDs: P05-07, NATIVE-03, COMMON-06.

- **Missing oracle and exact boundary conditions:** Exact code/message and allowlist under chosen purpose; absent export/reader/retention policy does not authorise disclosure; selected expiry/hold/delete/tombstone boundaries remain numerical/policy OPEN.
- **Required positive/negative fixtures:** Positive authorised private access/redacted projection later; negative private script/license/identity/stderr leaks, unauthorised reader/upload, hidden backups, retention erase resurrects old approve.
- **Hash/domain controls:** Hashes of private materials can leak membership; integrity digest never publication licence/anonymity proof.
- **Adversarial cases:** Cross-log correlation, forged output identity, unqualified retention timer and deletion removing negative-history anchor.
- **Independent verification route:** Future synthetic field/marker model checks separately from real authenticated ACL/channel/custody/backup/erase/history observations.
- **Conditions for future complete status:** F-D11 can close minimised schema subpart only; full CM requires F-D12 actual policy/enforcement plus history qualification. BLOCKED_OPERATIONAL_EVIDENCE.
- **Gates:** DOCUMENTARY_EVIDENCE now only; OFFLINE_VECTOR_EVIDENCE later under separately approved contract/task; RUNTIME_TEST_REQUIRED for real enforcement; TRUSTED_PROVIDER_EVIDENCE_REQUIRED for actual authority/currentness/rights/custody claims; WINDOWS_NATIVE_QUALIFICATION_REQUIRED for corresponding Windows claims. All planned runtime/provider/OS work **NOT_RUN**. No documentary subpart silently changes the source row status.

## Entry, stop and completion gates

Before future numeric profile fixtures: choose units and exact numbers with explicit OP-07/08/09 decisions; symbolic L is not a selected bound. Before schema/version compatibility fixtures: pin exact F-D06/OP-22/24 subchoices. Before operational probes: select and separately authorise actual provider, host, observer, access/purpose/rights and allowed failure operations. No such operations occur now.

For a future row-complete proposal require reproducible input/source/profile identities, actual expected/observed values, honest skips/exit codes and independent evidence for every claimed layer. Skipped/unavailable Windows/provider case is not PASS. Report contradictions/mismatched literals without adjusting content or retroactively approving new schemas. A row with only a pure subpart complete stays partial for its runtime/operational remainder until separately accepted.

All7 PARTIAL remain;20 OP remain OPEN. Full PG freeze and production permissions remain blocked even after any later documentary subpart closure. **STOP — roadmap/evidence planning only; G3.2.1 NOT AUTHORIZED.**
