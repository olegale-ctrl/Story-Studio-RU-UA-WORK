# P2 — Reference & Schema decision package

**DECISION_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0c; 2026-11-17 (Europe/Kyiv).
Base `0d6d9076ab535c1b258206beb4e4fe9c005e79e1`, tree `e55c00d0e7a95218e0978dd9677172608395ff5f`.

Primary: OP-09/22 (PURE). Secondary: OP-08 reference/cycle semantics (primary numeric/accounting P3); pure OP-24 namespace projection (primary P4). Classification и exact source requirements — [dossier](G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md). X03/X04 OWNER_APPROVED; не permission для production migration. Весь concrete schema/version adoption остаётся PROPOSAL.

## 1. OP-09 exact typed identities

Предлагается сохранить separate reference domains, не превращать их в взаимозаменяемый generic hash:

| Reference | Exact identity / bytes | Pure invariant | Outside pure |
|---|---|---|---|
| PG ObjectRef | contract,id,revision,binding_sha256; target exact PG envelope under its version | Target schema tag/id/revision/digest match; root local hash stage3, dependencies stage4 | Authenticity/currentness/authority не вытекают из digest |
| ByteRef | object_id,raw sha256,byte_length,media_type | Hash actual bytes/length; no reserialization or path-based substitution | Immutable resolver/actual opened file identity OP-17 |
| ImmutableBindingRef (B proposal) | schema_id,object_id,revision,raw sha256,byte_length | Exact typed BoundToolchain or BoundExecutorProfile target header/bytes | Profile/runtime/host qualification OP-17/20/23 |
| PolicyRef | id,version,sha256 within explicit role | Exact role-sensitive tuple, no latest/default fallback | Actual registry legitimacy/current grant OP-15/24 |
| HeadRef | stream_id,epoch_id,sequence,head_sha256 | Supplied shape/equality/history link constraints | Provider proves latest/authentic head/anti-rollback, not JSON |

Schema identity/class determines which digest definition applies: PG domain-separated binding versus raw content SHA256. Revision is exact positive integer, not global time/order; same text/bytes under another object/revision does not inherit approval. Cross-event PG02 predecessor revision numbers are not a universal monotonic clock. Do not infer chronological order from UUID, timestamp, list order or numeric revision alone.

### Registry and conflicts

Recommended registry: exact typed identity key. For PG: `(contract,id,revision)`; for versioned binding objects: `(schema_id,object_id,revision)`; for raw refs use their explicit object identity+raw digest+length under resolver namespace. Same exact object repeated may be deduplicated for validation work; conflicting bodies/hashes under same identity deny, never choose first/last/latest. Different identities with same bytes still distinct policy/approval subjects. Для unversioned raw ByteRef один immutable object_id в namespace не может объявлять разные hashes/lengths: это conflict, а не новая допустимая запись только потому, что hash включён в comparison tuple.

Deterministic reference walk follows declared schema fields and original array order, not arbitrary discovered JSON keys or URLs. Opaque ByteRef evidence is **not** recursively scanned for inferred references; only a separately selected typed payload profile defines additional edges. Registry size/edge occurrences counted by P3 before unbounded growth. Same-stage error tie details OP-06 stay explicit proposal; X02 earliest failed stage unchanged.

Alternatives: (A) exact closed reference family per version (recommended); (B) explicitly versioned adapters with separately reviewed acceptance semantics. Not acceptable: latest fallback, silently broadened unions or inferred schema/version. Owner can adopt pure identity/conflict model without connecting a content store; real immutable storage remains operational gate.

## 2. OP-08 secondary semantics and X03

Approved split remains:

1. Abstract stable-ID graph with typed declared dependency edges, useful for cycle/reachability/revision oracles. It makes no PG cryptographic validity claim.
2. Content-addressed PG closure: actual local/target bindings must match before claiming a valid resolved graph. Earlier digest/ref failure is not isolated cycle coverage.

Pinned V043 remains historically blocked end-to-end; V043-S through V043-S6 are structural fixtures only. Self-loop/2-cycle/3-cycle cannot be promoted to hash-valid ObjectRef examples by dummy/stale SHA. Shared child counted once for distinct-node work, each edge occurrence separately counted. V043-S5 is exact target-revision mismatch, not a new chronological revision rule. V043-S6 cap2 is conditional test metadata, not approved OP-08 numeric limit.

Numeric closure selection belongs primary P3, which uses OP-09 typed identity units. This avoids P2 requiring a qualified provider to describe a graph, or P1 waiting for graph/native runtime. Actual state-history reconciliation/head authenticity remains P5.

## 3. OP-22 and X04 — proposed versioned plan bindings

Owner has already required mandatory immutable `toolchain_ref` / `executor_profile_ref`; the option to leave them unbound outside plan is **not reopened**. The choice now concerns exact version/type/migration policy, not whether to omit those fields.

Binding path:

```text
SubjectKey.plan_sha256
  -> exact RenderPlanV2 raw bytes
    -> mandatory toolchain_ref / executor_profile_ref
      -> exact typed target schema/id/revision/raw bytes/length
```

B proposed types remain the candidate starting point: RenderPlan schema_id `render-plan/proposal-2`; `ImmutableBindingRef{schema_id,object_id,revision,sha256,byte_length}`; BoundToolchain carries full Toolchain payload; BoundExecutorProfile carries PolicyRef and exact immutable content ByteRef. These IDs/type details are still proposed, **not accepted wire IDs** simply because X04 direction is approved.

PG04 actual Toolchain payload/executor policy/content must match plan-bound targets; no caller path/PATH/config/version-string override. A changed target creates a new revision/ref/hash, new exact plan bytes, new plan digest and new SubjectKey. Same identity with changed bytes is conflict, not technical migration. Old SubjectKey cannot be declared equivalent to new.

| Change class | Required contract action | Remaining decision |
|---|---|---|
| Content-affecting text/language/visual meaning or render behavior | New human approval for new reviewed subject; new authorization candidate | How effects are classified and evidenced, not automatic technical label |
| Rights-affecting asset/license/usage/attribution/channel | New rights review and affected human review; new candidate | Real reviewer/jurisdiction/intended-use policy OP-13/14 |
| Purely technical tool/runtime/profile change | New plan/SubjectKey/candidate, apply separately approved reapproval policy | Whether new PG02 or explicit review continuity proof is required remains OPEN; never grant automatically |

### Migration/version alternatives

**A recommended:** new closed plan/profile version; legacy proposal-1 accepted only for historical diagnostics under its own rules, rejected as a new-version candidate. Rebind exact bytes and seek applicable new reviews. No in-place modification of old signed/hash-bound records.

**B alternative:** explicit compatibility adapter with its own version, raw before/after hashes, allowed transformations, retained origin/history, review invalidation rules and negative fixtures. Adapter is separate future contract/implementation, not authorized by this dossier. It cannot mark old approvals valid for changed subject merely because transformation is deterministic.

**C defer:** retain all new schema adoption OPEN and continue existing Preview/D1 bounded workflows only. This is not an alternative to approved binding direction for a future gate; it postpones the gate.

Full PG family IDs/profile combinations and receipt protocols still require owner selection. P2 pure field adoption can be reviewed without choosing/connecting runtime authority; actual policy acceptance is P4/P5. V074–V080 remain immutable source evidence: binding changes/stale plan digest/payload mismatch/override/before-after bytes, not executable PG semantic PASS.

## 4. OP-24 pure namespace projection (primary P4)

Recommended comparison context explicitly distinguishes root content/use policy, reviewer authority, rights policy, issuer, executor and output profile. A common PolicyRef shape does not mean interchangeability. Pure rule compares declared role+exact id/version/hash; resolver may not fill missing role/version from latest registry. Concrete namespace/tag encoding and profile family belong OP-24 primary decision; no new owner role assigned here.

No hard P2 dependency on a live policy registry. OP-22 can specify immutable binding objects using existing proposed PolicyRef shape; OP-24 then specifies role-typing/comparison. Live current grants/registry selection is downstream, so no P2↔P4 provider cycle is introduced.

## 5. Review/readiness and test dependencies

OP-09/22 counted as decision-ready **questions**, still PROPOSED/OPEN as source statuses specify. Exact questions, alternatives/security/product/migration implications are in dossier. OP-08 numeric choice remains unresolved P3; OP-24 whole choice MIXED and unresolved P4.

Relevant pinned cases: V022,V041,V042,V043,V043-S,V043-S4,V043-S5,V043-S6; V074–V080; P01-05,P02-04,P04-02,P04-08. No vectors, hashes, source OP statuses, schemas or expected errors edited. Reference/closure/version diagrams reviewed offline only, no validator/provider run.

Remaining blockers: final schema/profile/migration/reapproval decisions; actual immutable resolver/state/authority/host and operational qualification. **STOP, no implementation/migration or production permission.**
