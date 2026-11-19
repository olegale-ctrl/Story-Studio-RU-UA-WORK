# MVP08B compatibility matrix

**SP-INTEGRATION-01a · 2026-11-19 · DOCS_ONLY · FREEZE_FOR_REVIEW, NOT OWNER_APPROVED.**

Search time:2026-11-19. Evidence: complete advertised172-head listing, remote tags, local refs, local worktrees, tracked filenames, repository Python definition search and pinned MVP08B.1 reports, all saved externally. No MVP08B.2-named head/local ref/file or runtime Dispatcher/JobStore API found. Remote MVP08B.1 head is f0bce140451bf00a86f3939330e77ed63b2c98be. Candidate is its direct child. Search proves absence **in this inspected scope**, not absence of private/unadvertised artifacts or code under unknown names elsewhere.

`MVP_08B_1_ACCEPTANCE.md`, JOB_CONTRACT, STATE_MACHINE, RESULT_INGESTION and OPEN_DECISIONS explicitly say PROPOSAL/CONTRACT_PREPARATION_ONLY/NOT_IMPLEMENTED. Prior authorization or a planning sequence is not implementation evidence. All MVP08B.2 runtime conclusions remain NOT_VERIFIED until exact artifacts are supplied.

|SP requirement|MVP-08B contract|Implementation|Compatibility|Blocker|Required decision|
|---|---|---|---|---|---|
|Single Dispatcher|08B.1 proposes one fenced controller|None in inspected tree; .2 unavailable|MISSING_API|No submit owner/interface|SP-OD01 approve/supply exact API version|
|Persistent JobStore|Proposed CAS/events/outbox|No runtime store|MISSING_API|No authoritative request/state boundary|SP-OD01 implementation + store qualification|
|Accept/reuse/conflict receipt|Proposed immutable GenerationJob and idempotency key|No acceptance endpoint|MISSING_API|Local intent hash not job acceptance|SP-OD01/02 exact scope/key/receipt|
|Idempotent effects|Proposed project+purpose+request+batch scope|Not implemented|MISSING_API|Same intent replay only deterministic preparation|SP-OD01 preserve durable uniqueness/effect guarantees|
|Observation/status/wait|Proposed state revision and observer semantics|CLI --wait immediately blocks|MISSING_API|No authoritative observer; no mirror permitted|SP-OD01 bounded observer API|
|Completion receipts|Proposed saved JSON readback/asset receipt|No implemented authoritative end-to-end receipt|MISSING_API|COMPLETED label cannot replace saved result proof|SP-OD08 receipts/broker|
|Artifact publication/recovery|Proposed ingestion saga/reconciliation checkpoints|No Dispatcher publication/recovery; Library primitives are not this protocol|MISSING_API|Cross-resource outcomes unresolved|SP-OD08 qualify storage/receipts/recovery|
|Seven SP job types / general DAG|08B.1 GenerationJob is specialized video generation T2V/I2V, not generic dependency DAG|No registered type registry; .2 NOT_VERIFIED|NOT_VERIFIED|No evidence any SP type is supported|SP-OD01 choose explicit extension or constrained bridge; no automatic orchestration expansion|
|SP digest as direct 08B job key/payload|SP uses compact SI primitive; proposed08B JCS-LOCAL-1 uses base encoded default separators and broader scoped key|No mapping|CONTRACT_CONFLICT|Direct substitution would mix byte/hash/identity domains|SP-OD02 explicit typed/domain mapping; preserve originals|
|Rights/input pinning principle|08B.1 exact revisions/hash/use review; existing Library resolve validates local fields|Local primitives exist, not authenticated review|PARTIALLY_COMPATIBLE|Authority/revocation/native qualification incomplete|SP-OD03/07/08 qualified adapters|
|No auto paid/live/bypass|D01–D08 owner record, zero budget; unknown rights not clearance|Current SP never submits and never grants release|COMPATIBLE|Compatibility limited to prohibition, not execution support|No widening; future changes separately authorized|
|Actual MVP08B.2 results/permissions|No exact .2 source/result/acceptance artifact located|NOT_VERIFIED|NOT_VERIFIED|No evidence for any new implementation/grant|Supply exact commit/tree/API/tests/owner scope before reliance|

No job type is declared registered: script.draft,plan.from_script,plan.validate,assets.voice,assets.images,render.mp4,gates.technical are **proposed labels only**. A universal DAG engine would be a new architecture decision; neither existing video GenerationJob proposals nor this document authorize it.

Available approved material is narrow: unchanged D01–D08 constrain experimental direction/budget/rights/confirmations; MVP08A acceptance has limitations; G2 preview and G3.1 fixed D1 do not supply generic grants. G3 P1 approves specified pure rules, not trusted execution/identity/storage. S1 storage wire/MAC code does not persist or evaluate authority; Storage S3 remains unqualified for production. No normative contract changed.
