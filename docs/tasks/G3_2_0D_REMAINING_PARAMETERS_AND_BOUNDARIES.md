# Remaining parameters and authority boundaries

**P1_OWNER_DECISIONS_DOCUMENTED — DOCS_ONLY**

SI-INTEGRATION-G3.2.0d; 2026-11-17 (Europe/Kyiv). Только документация; не PRODUCTION_APPROVED и не полный PG freeze.

Only OP-01–06/26/27 are OWNER_APPROVED pure-contract by this task. G3.2.0c acceptance was docs-only. Its ten decision-ready questions were not ten approvals: **OP-09 and OP-22 remain unapproved**. Existing historical registry is unchanged; the table below explicitly records current task status for all remaining20.

| OP | Exact C classification | Primary package | Current status | Dependency/boundary |
|---|---|---|---|---|
| OP-07 | PURE | P3 | OPEN — NOT APPROVED | Three logical counter profiles; CPU/time/RAM coefficients remain OPEN pending separate measurements |
| OP-08 | PURE | P3 | OPEN — NOT APPROVED | Typed closure counters+dedup rules; profile limits in P3 PROPOSED, actual selection OPEN |
| OP-09 | PURE | P2 | OPEN — NOT APPROVED | Exact typed identity/revision/hash refs, conflict reject, no latest fallback, separate semantic payload profiles |
| OP-10 | MIXED | P4 | OPEN — NOT APPROVED | Pure Instant signed domain0…253402300799 epochsec; external time authority/skew OPEN |
| OP-11 | MIXED | P4 | OPEN — NOT APPROVED | Pure [from,until) intersection; TTL/render margin OPEN until profile+clock evidence |
| OP-12 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Design lease/checkpoints or bounded poll protocol; no selected polling number |
| OP-13 | MIXED | P4 | OPEN — NOT APPROVED | Pure exact asset/use/layer coverage; required legal layers/jurisdictions and competent reviewer OPEN |
| OP-14 | MIXED | P4 | OPEN — NOT APPROVED | Pure role/scope/decision/session/declaration fields; real assignments/competence/independence OPEN |
| OP-15 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Define required provider properties; choose qualification project or remain production-blocked |
| OP-16 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Durable single-attempt admission before spawn; unknown→reconcile, no automatic rerender |
| OP-17 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Opaque immutable IDs plus held verified file identities; actual OS/store protocol OPEN |
| OP-18 | MIXED | P4 | OPEN — NOT APPROVED | Pure closed expected RU/UK outputs/tools/config/attribution profile refs; actual media limits/quality OPEN |
| OP-19 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Specify invariant ledger↔index↔actual outputs; actual durable commit/witness protocol OPEN |
| OP-20 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Separate exact authorized host/profile selection and native qualification task |
| OP-21 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Private content/evidence by default, per-purpose access/export/retention/erase policy OPEN |
| OP-22 | PURE | P2 | OPEN — NOT APPROVED | Proposed RenderPlanV2 mandates immutable toolchain/executor refs; new plan/SubjectKey on any change |
| OP-23 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Enumerate versioned identity/grant/admission/completion/inspection/manifest payload contracts; real protocol OPEN |
| OP-24 | MIXED | P4 | OPEN — NOT APPROVED | Pure role-separated PolicyRef namespaces with exact id/version/hash comparison; current registry OPEN |
| OP-25 | MIXED | P4 | OPEN — NOT APPROVED | Pure original-bytes/code/runtime/context/full-result binding contract; actual collector/recomputation OPEN |
| OP-28 | OPERATIONAL | P5 | OPEN — NOT APPROVED | Immutable negative history/tombstones; no expiry revival of prior approve; actual authority/recovery protocol OPEN |

## Preserved package and classification ownership

P1 approved8 PURE. Remaining: P2 OP-09/22 (2 PURE); P3 OP-07/08 (2 PURE); P4 OP-10/11/13/14/18/24/25 (7 MIXED); P5 OP-12/15/16/17/19/20/21/23/28 (9 OPERATIONAL). Total remains PURE12/MIXED7/OPERATIONAL9,28 parameters, one primary package each. P2 secondary OP-08/OP-24 coverage does not change ownership.

OP-07/08 resource/global node/token/object-member and closure budgets remain OPEN;8MiB,depth64,string65536,array10000 do not prove full DoS/memory safety or total referenced bytes. P3 illustrative unsupported numbers remain OPEN, not default constants. OP-09/22 typed references/schema versions and migration are still proposals; X03/X04 architectural direction does not grant production migration, RenderPlanV2 implementation or approve those OP.

MIXED policy schemas and trusted predicates remain open: trusted clock, reviewer competence and authority, rights/licences, full evaluation recomputation and actual RU/UK output qualification cannot be inferred from format validity. No G2 missing diagnostics reconstruction, inferred rights, self-approval or scientific/editorial judgment by JSON validity. Product readiness still requires evidence for why film, scientific claims, visual proof, editorial alternatives and real decision responsibility.

OPERATIONAL authority provider → durable admission → guarded executor → completion evidence remains unqualified. Revocation, trusted state-head/rollback resistance, single-attempt admission, lost ACK and crash/restart recovery, immutable handles, TOCTOU/reparse protection, evidence atomicity, privacy/retention/tombstones and historical approvals require separate protocols and tests. Exactly-once physical execution is not established. Storage S3 is not production-qualified and was not changed. Windows10/11 CPU-only native qualification, NTFS/reparse and real output tests were not performed.

Public/private diagnostics publication/access policies OP-21/23 remain open despite approved safe messages. No real reviewer identity, trust registry, timestamp provenance, rights grant or permit was created. SyntheticRenderPermitV1 remains SYNTHETIC_TEST_ONLY; neither PREVIEW_ONLY nor PRODUCTION_CANDIDATE grants production permission. No new production mode exists from this record.

No implicit migration/reapproval, no inherited approval on changed raw plan/toolchain/executor or scope. G1/G2/G3.1 and CI unchanged. **G3.2.1 NOT AUTHORIZED; production permissions BLOCKED; complete PG freeze NOT COMPLETE.**

**STOP — independent ChatGPT audit, then separate owner decisions/authorization.**
