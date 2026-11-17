# G3.2.0b — resolution and independent vector evidence

**DOCS_ONLY / resolution package — independent acceptance pending.** SI-INTEGRATION-G3.2.0b; 2026-11-17 (Europe/Kyiv).
X01–X04: **OWNER_APPROVED** по текущему заданию. Новые schemas/profiles и OP-01–28 остаются **PROPOSAL / NOT APPROVED**; это не final PG freeze.
Parent `2610dcfd0a304c4fb8f4d71812b80e52f6ce3bb5`, tree `425972e157e017eb20615a4ea0fa6ba216a7923d`.
Approved main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

## Counts and preservation

Original70 IDs V001–V070 preserved, along with all original inputs/canonical byte recipes/literal hashes. Expected-result overlays change only V039 and V051 explicitly, with historical values retained; V043 remains a historically blocked end-to-end cycle record. New10 numeric IDs V071–V080 plus7 abstract IDs V043-S,V043-S1…S6 give **87 records**. Original58 discovery oracle IDs, premise/expected strings retained verbatim. OP-01–OP-28 document unchanged.

Actual byte checks and actual semantic checks are different. Every new record has full exact hex input/canonical-control sequence and literal input-RAW/canonical-RAW/DOMAIN hashes in [full vectors document](G3_2_0A_INDEPENDENT_VECTORS.md).17×3=51 displayed new hash streams checked. For rejected schemas/unknown fields, canonical-control bytes are arithmetic only, not validator-accepted output.

| Evidence label | What actually ran | What it does not prove |
|---|---|---|
| BYTES_VERIFIED | Authored literal/fragment layouts matched independent stdlib parse+sort encoding; exact hex decoded/read back | PG schema/current-state/product/rights acceptance |
| HASH_VERIFIED | SHA256 via hashlib, OpenSSL CLI and separate pure-Python FIPS180-4; known-answer abc; displayed literals rechecked | Identity/authenticity/permissions; backend independence is not claimed just from CLI names |
| STRUCTURAL_ORACLE_VERIFIED | Seven graphs: DFS colors/backedges versus Kahn elimination; revision map check versus exact tuple registry; budget reachability conditional | Cryptographic PG closure cycle, real replay ledger or native execution |
| PG_SEMANTIC_NOT_RUN | No full PG validator exists or was executed | Described expected error is not semantic PASS |
| NATIVE_NOT_RUN | No Windows/security/native operations | No host, reparse/ACL/TOCTOU qualification |
| OPERATIONAL_NOT_QUALIFIED | No providers/grants/real render/qualification | Byte consistency is not execution authority |

These labels are human-readable verification annotations, **not new machine PG statuses**. CONSISTENT_NO_AUTHORITY/DENY namespace unchanged; no ALLOW_RENDER. Original33 canonical-positive A records and66 RAW/DOMAIN literal hashes also rechecked for preservation; old positives are bytes/shape probes, not real PG passes.

## X01 / X02 exact effective expectations

| Case | Previous | Effective expected code / stage | Verification scope |
|---|---|---|---|
| V051 empty why_film | BLOCKED_CONTRACT X01 | PG_FORMAT /2 | bytes preserved; no PG semantic validator run |
| V072 nonempty but insufficient rationale | New proposed isolated predicate | PG_PRODUCT_GAP /6, only if stages1–5 succeed and substantive unmet criterion supplied | BYTES/HASH verified; HUMAN/product-policy premise remains PROPOSED |
| V039 known forbidden mode, stale binding | BLOCKED_CONTRACT X02 | PG_DIGEST /3 | unchanged original input bytes; local binding mismatch calculable |
| V071 paired known forbidden mode, correct binding | New | PG_MODE /5 after references | local binding recomputed; exact C0 fixture context, semantic PG NOT_RUN |
| V073 unknown mode enum | New | PG_FORMAT /2 | byte/schema lexical expectation; no returned accepted digest |

All other fields used to isolate V039/V071 are field-shape/type correct under the source envelope contract; raw refs point to the actual synthetic fixture object bytes, not invented digests. Empty semantic SI/plan payloads are later-stage gaps and deliberately not claimed valid. See C0 and the full input/canonical literals in vectors. No false literal-hash changes or reference validity assertions hide earlier independent schema errors.

## X03 exact abstract graph fixtures

Graph root/edges/nodes/target_revision and fixture max_nodes are complete below. A tuple-registry mismatch is separate from directed cycle. Each fixture has matching byte/hash evidence; JSON literals are actual bytes without LF, not just diagrams. No digests are claimed inside these abstract graph inputs.

### V043-S — acyclic DAG

```json
{"edges":[{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"B"},{"from":"B","kind":"DEPENDENCY","target_revision":1,"to":"C"}],"max_nodes":null,"nodes":[{"fixture_id":"A","revision":1},{"fixture_id":"B","revision":1},{"fixture_id":"C","revision":1}],"root":"A"}
```

Expected structural annotation: **ACYCLIC**. Reachable nodes=3. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; no numeric bound selected. Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

### V043-S1 — self-loop

```json
{"edges":[{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"A"}],"max_nodes":null,"nodes":[{"fixture_id":"A","revision":1}],"root":"A"}
```

Expected structural annotation: **CYCLE**. Reachable nodes=1. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; no numeric bound selected. Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

### V043-S2 — two-node cycle

```json
{"edges":[{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"B"},{"from":"B","kind":"DEPENDENCY","target_revision":1,"to":"A"}],"max_nodes":null,"nodes":[{"fixture_id":"A","revision":1},{"fixture_id":"B","revision":1}],"root":"A"}
```

Expected structural annotation: **CYCLE**. Reachable nodes=2. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; no numeric bound selected. Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

### V043-S3 — three-node cycle

```json
{"edges":[{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"B"},{"from":"B","kind":"DEPENDENCY","target_revision":1,"to":"C"},{"from":"C","kind":"DEPENDENCY","target_revision":1,"to":"A"}],"max_nodes":null,"nodes":[{"fixture_id":"A","revision":1},{"fixture_id":"B","revision":1},{"fixture_id":"C","revision":1}],"root":"A"}
```

Expected structural annotation: **CYCLE**. Reachable nodes=3. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; no numeric bound selected. Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

### V043-S4 — shared-child DAG

```json
{"edges":[{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"B"},{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"C"},{"from":"B","kind":"DEPENDENCY","target_revision":1,"to":"D"},{"from":"C","kind":"DEPENDENCY","target_revision":1,"to":"D"}],"max_nodes":null,"nodes":[{"fixture_id":"A","revision":1},{"fixture_id":"B","revision":1},{"fixture_id":"C","revision":1},{"fixture_id":"D","revision":1}],"root":"A"}
```

Expected structural annotation: **ACYCLIC**. Reachable nodes=4. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; no numeric bound selected. Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

### V043-S5 — predecessor target-revision mismatch

```json
{"edges":[{"from":"A","kind":"PREDECESSOR","target_revision":1,"to":"B"}],"max_nodes":null,"nodes":[{"fixture_id":"A","revision":2},{"fixture_id":"B","revision":2}],"root":"A"}
```

Expected structural annotation: **REFERENCE_REVISION_MISMATCH**. Reachable nodes=2. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; no numeric bound selected. Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

### V043-S6 — conditional reachable-node budget exhaustion

```json
{"edges":[{"from":"A","kind":"DEPENDENCY","target_revision":1,"to":"B"},{"from":"B","kind":"DEPENDENCY","target_revision":1,"to":"C"}],"max_nodes":2,"nodes":[{"fixture_id":"A","revision":1},{"fixture_id":"B","revision":1},{"fixture_id":"C","revision":1}],"root":"A"}
```

Expected structural annotation: **TRAVERSAL_LIMIT**. Reachable nodes=3. Status: STRUCTURAL_ORACLE_VERIFIED with DFS/Kahn/revision controls; APPROVAL_REQUIRED on OP-08 (limit2 only fixture parameter). Applicability: abstract structure only; PG crypto closure/operational NOT_QUALIFIED.

## X04 before/after bytes and invalidation

Legacy V079 and V2 V080 exact raw/canonical bytes are complete in vectors; only the new schema adds schema_id and two mandatory binding references. Fixture target A uses revision1; B uses revision2 and different raw hash, avoiding a conflicting object identity test that could mask the intended cause.

| Fixture | Exact raw plan SHA256 | What it demonstrates |
|---|---|---|
| V079 legacy | `f428791a3be11233c2d352e49dc0c752f5317f2a378b729dc2457917d20dd2ce` | immutable raw bytes identity, not grant |
| V080 new V2 | `6973949315d8276ae3aef8bc453b31d206b0b6f9425912036d3a0f4f36a0e76d` | immutable raw bytes identity, not grant |
| V074 changed toolchain target | `94404ab684d31fdb616c00f1b8b7d73f29dcfbd0c835565c745557c574722294` | immutable raw bytes identity, not grant |
| V075 changed executor target | `7eeb20913d827cddfa3431dc5f36f91a7a93c581bc4a403b763a2cc7b1125c88` | immutable raw bytes identity, not grant |

| New negative | Isolated failure | Expected existing code/stage | Limits |
|---|---|---|---|
| V074 | Plan's toolchain ref changes revision/hash while old SubjectKey retained | PG_REFERENCE /5 subject consistency | proposed V2 predicate, semantic PG NOT_RUN |
| V075 | Plan's executor ref changes revision/hash while old SubjectKey retained | PG_REFERENCE /5 subject consistency | no real host/profile permission |
| V076 | Declared ByteRef old plan digest against new raw plan bytes | PG_DIGEST /4 raw dependency binding | no unrelated local-envelope issue in this isolated probe |
| V077 | PG04 actual Toolchain payload differs from exact plan-bound target payload | PG_TOOLCHAIN /5 | not a version-string-only comparison, no actual FFmpeg execution |
| V078 | Caller injects unknown toolchain_override field into closed V2 plan | PG_FORMAT /2 | canonical-control bytes not accepted parser output |

Purely technical changes still change plan/SubjectKey and require a new authorization candidate plus separately approved reapproval policy. Content/rights effects require their corresponding new reviews. No old envelope is promoted automatically to new schema; proposed version/profile/type details remain unapproved. All actual operational results NOT_QUALIFIED.

## Source and offline method

Parent seven source file blobs, discovery identities, original vector literals and verbatim58 rows are compared from pinned Git commits, not assumed from current worktree. All helpers and temporary fixtures remain outside repository. Canonical layout construction uses literal field ordering and fragments copied as exact bytes from pinned source; independent control uses stdlib parse/key ordering. The temporary SHA256 implementation does not call crypto libraries; hashlib/OpenSSL may share backend, therefore not two independent canonicalizers. No PG validator/provider was built; abstract graph controls process only finite fixture nodes/edges/revisions and claim no PG integrity/authenticity.

## Remaining gates

OP-01…28 retain OPEN/PROPOSED values, including numeric bounds, product/rights/roles, authority/time/revocation/ledger, immutable resolver, output/evidence profiles, Windows qualification and disclosure/retention. Full schema/profile acceptance, version/migration and technical reapproval remain PROPOSAL. V043 content-addressed cycle coverage unproven by design; new structural coverage must not be substituted for it. These are retained qualification/freeze gates, not an unapproved reopening of X01–X04 choices.

**Resolution package READY_FOR_INDEPENDENT_ACCEPTANCE; full Production Gate freeze/operation NOT APPROVED. STOP for independent ChatGPT review and owner decision.**
