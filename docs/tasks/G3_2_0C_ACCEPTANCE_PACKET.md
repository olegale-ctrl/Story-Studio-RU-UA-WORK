# G3.2.0c — Acceptance Packet

**DECISION_PROPOSAL — NOT APPROVED**

**READY_FOR_INDEPENDENT_REVIEW** — documentation dossier only. No contract freeze, implementation authority, production permission or qualification is asserted.

## Pinned identities and scope

| Identity | Commit | Tree / parent |
|---|---|---|
| Approved main | `a28277b4cb68a3db5da52edc598c37ce66314604` | tree `920713b992046dff1f8fc68e40a05bee2f0bcb29` |
| Exact accepted G3.2.0b base | `0d6d9076ab535c1b258206beb4e4fe9c005e79e1` | tree `e55c00d0e7a95218e0978dd9677172608395ff5f` |
| Base parent | `2610dcfd0a304c4fb8f4d71812b80e52f6ce3bb5` | identity checked against base commit |

Branch: `docs/g3-2-0c-open-parameters-decision-dossier`, directly from that exact base. Fetch, clean starting checkout, remote main identity/tree, base identity/tree/parent, ten A/B reference documents and absence of the target remote branch were checked before preparation. No rebase, merge, source substitution or deferred PR #11 transfer.

The exact OP source is `G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md`, blob `8df767ab375ff312c6ac723072e58d64e53969c9`. Its 28 original records, including historical wording, are reproduced in the dossier. X01–X04 approved B adjudications take precedence over superseded historical conflict wording. A/B files remain unchanged.

## Exact seven-file registry

All paths below are under `docs/tasks/`; all are new additions. Commit/tree and this packet's self-blob are external handoff fields to avoid recursive self-hashing.

| File | Mode | Git blob SHA-1 |
|---|---|---|
| [G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md](G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md) | 100644 | `700a9bce47b6c79a45cb65fce1b8a09d84903dab` |
| [G3_2_0C_P1_CANONICAL_FOUNDATION.md](G3_2_0C_P1_CANONICAL_FOUNDATION.md) | 100644 | `8905865ed0f41b363d39993408a78605d3a829df` |
| [G3_2_0C_P2_REFERENCE_AND_SCHEMA.md](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) | 100644 | `9d39e41a9dc729f83ff91ee6a29b84668a327a42` |
| [G3_2_0C_P3_RESOURCE_MODEL.md](G3_2_0C_P3_RESOURCE_MODEL.md) | 100644 | `8787738852f4b9a15ad3d33f1c57ec52a5dc3441` |
| [G3_2_0C_P4_POLICY_CONTRACTS.md](G3_2_0C_P4_POLICY_CONTRACTS.md) | 100644 | `a875fa0ee36748f41a0b89cd6c2f9b80ece89bcd` |
| [G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md) | 100644 | `d9b94e875442d57d7e71cc0d84a4936eceb1bff0` |
| G3_2_0C_ACCEPTANCE_PACKET.md | 100644 | Self-blob supplied externally after commit |

## Coverage and decision readiness

| Primary package | Parameters | Class | Count |
|---|---|---|---:|
| P1 | OP-01–06, OP-26–27 | PURE | 8 |
| P2 | OP-09, OP-22 | PURE | 2 |
| P3 | OP-07–08 | PURE | 2 |
| P4 | OP-10–11, OP-13–14, OP-18, OP-24–25 | MIXED | 7 |
| P5 | OP-12, OP-15–17, OP-19–21, OP-23, OP-28 | OPERATIONAL | 9 |

Coverage **28/28 unique parameters**, exactly one class and primary package each: PURE12 / MIXED7 / OPERATIONAL9. P2 additionally covers structural OP-08 and pure OP-24; these are secondary coverage, not duplicate ownership. Each main-dossier record includes exact source, recommendation, alternatives, security/product consequences, exact dependencies and vector/oracle references, migration impact, exact owner question and OPEN/PROPOSED status.

**Decision-ready10**: OP-01–06, OP-09, OP-22, OP-26–27. This means a bounded pure question is ready for discussion without trusted-provider operations, not that its answer is approved or implementation authorized. **Unresolved18 whole-parameter choices**: OP-07–08, seven MIXED and nine OPERATIONAL parameters. All28 remain unapproved. Original statuses remain 11 PROPOSED /17 OPEN, orthogonal to decision-readiness. Implementation prerequisite Yes/No concerns only a hypothetical separately authorized pure-only stage; No never waives a production gate.

## Dependencies and source contradictions

The exact decision-order DAG is in the main dossier; offline traversal found no cycle and no P1 hard prerequisite outside P1. Operational realization prerequisites are separately identified and cannot be treated as already available. P2 reference vocabulary precedes numeric OP-08 closure limits, and pure OP-24 namespace projection does not require a live registry.

No unresolved contradiction with X01–X04 was identified by pinned document/vector inspection. This is a document review conclusion, not executable conformance evidence:

- X01 empty required Text and substantive product insufficiency remain different approved cases.
- X02 seven-stage ordering, known-mode stale-binding versus corrected-binding cases and unknown-mode format failure remain intact. Only residual within-stage ties are proposed.
- X03 abstract graph-cycle tests and cryptographic closure are distinct; historical V043 remains blocked, and synthetic cap2 does not approve OP-08 limits.
- X04 exact plan bytes bind mandatory toolchain/executor refs; no caller overrides, inherited old approval or production migration permission.

Remaining source ambiguity, unsupported resource capacity and operational protocols are explicitly OPEN. No existing canonical vectors were changed. All21 actually listed proposed error codes were extracted from the pinned catalogue and compared to P1; no new error codes, machine statuses or grants were introduced.

## Offline verification evidence

Scratch inspection helpers are outside the repository and are not a PG validator. Completed checks: Git pinned identities and source blob reads; full original OP-record preservation; 28 unique IDs/classes/primary packages; decision DAG; exact references against the pinned catalogue of **87 vector IDs and58 oracle IDs**; exact21-code table; Markdown fences, line endings and trailing whitespace; deterministic byte/counter arithmetic. Helper exit code **0**. Arithmetic includes 4/8/16MiB, escaped-string bound `6*65536+2=393218`, array/token counts and conditional aggregate-byte scenarios. These are calculations, not parser or performance benchmarks.

Final publication checks comprise the exact seven A-only paths/modes, unchanged parent entries, relative Markdown targets, `git diff --cached --check` and committed-tree/blob verification; their exit codes and candidate identities are supplied externally after commit. This packet does not embed its own future commit identity.

**NOT RUN:** PG validators, application tests, integration, rendering, native Windows qualification, trusted provider operations, CPU/RAM benchmarks or production qualification. No new vectors were generated/executed; vector/oracle ID validation does not mean their behavioral tests passed. CI and implementation remain unchanged.

## Risks, remaining blockers and owner sequence

Resource profiles are proposals, not proven capacity. Unsupported node/token/closure/aggregate limits are OPEN with clearly conditional arithmetic examples; CPU, peak memory, timing and output budgets require a separately authorized measured qualification. Input caps do not prove allocation safety.

Provider identity/roles, trusted time/head and rollback prevention, rights/licences, durable admission, revocation, replay control, lost ACK recovery, guarded native execution, evidence durability, privacy/retention and tombstones remain unresolved. Storage S3 is not production-qualified; Windows NTFS/reparse-point and CPU-only claims have not been qualified. Pure contracts cannot eliminate TOCTOU or replace trusted OS/storage/executor guarantees. SyntheticRenderPermitV1 cannot authorize production. Schema validity cannot establish editorial/scientific merit or actual asset rights.

Recommended owner sequence, without blanket approval:

1. Independently audit the packet, source quotations and X01–X04 consistency.
2. Consider the eight P1 questions individually in dependency order (OP-05 before03; OP-27 before06). This selects document rules only, unless separately stated authorization follows.
3. Consider P2 reference/schema identities and migration alternatives; retain exact-plan binding and no implicit compatibility.
4. Resolve P3 numerical unknowns with a separately authorized qualification plan; no fabricated measurements.
5. Decide P4 pure policy projections and identify actual competent editorial/scientific/legal authorities.
6. Decide P5 trust model and operational protocols in the Authority Provider → Durable Admission → Guarded Executor → Completion Evidence chain, then separately authorize any implementation/qualification work.

G3.2.1 is NOT AUTHORIZED. Production permissions remain BLOCKED. Contract freeze is not complete. This docs-only package has no publication-blocking base/scope defect identified by offline review; operational blockers explicitly prevent claims of production readiness.

**STOP — await independent ChatGPT audit and owner decision.** No automatic next stage, merge or release.
