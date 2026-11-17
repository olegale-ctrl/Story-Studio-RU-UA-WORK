# Owner decision dossier — proposals only

**PROPOSED — NOT APPROVED. OWNER_AUTHORIZED_DOCS_ONLY.**

SI-INTEGRATION-G3.2.0f; 2026-11-17 (Europe/Kyiv). No implementation, merge or production authority.

## Package names and approval boundary

F review packages below are P1 independent pure contracts, P2 dependent pure contracts, P3 mixed contracts, P4 operational decisions. They are **local F review packages**, not a reassignment of the original C P1–P5 primary OP ownership. Original classifications/ownership and20 OPEN parameters remain unchanged. New F-D IDs are proposals, never renumbered OP IDs or approved decisions.

Source grounding for every proposal is the corresponding CM card and normative/source citations in [inventory](G3_2_0F_SEVEN_PARTIAL_GAPS_INVENTORY.md). Detailed alternatives/resource semantics: [pure options](G3_2_0F_PURE_CONTRACT_DECISION_OPTIONS.md); real trust boundaries: [dependencies](G3_2_0F_OPERATIONAL_AND_RESOURCE_DEPENDENCIES.md); completion oracles: [evidence plan](G3_2_0F_CONFORMANCE_AND_EVIDENCE_PLAN.md).

| Decision ID / package | Related CM | Related OP | Proposed choice | Alternatives | Recommendation | Hard decision dependencies | Consequences | Status |
|---|---|---|---|---|---|---|---|---|
| F-D01 / P1 | CM-006, CM-071 | OP-09 | Exact closed typed identity/ref/edge vocabulary with supplied bytes and no latest fallback; resolver authenticity separate | Versioned explicit adapter family after review; defer all closure admission | Prefer closed family; no live provider needed to decide vocabulary | None; approved P1 context only | Unblocks consistent dedup/conflict units; does not approve OP-09 as a whole or establish storage identity | PROPOSED — NOT APPROVED |
| F-D02 / P1 | CM-022 | OP-07 | Freeze root logical node/key/token/decoded/member occurrence units; no numerical global caps | Value-only nodes with separate keys budget; retain vocabulary open | Prefer value+key nodes and separate lexical tokens; root-only decision first | None; approved P1 context only | Makes arithmetic reproducible without capacity claims; whole OP-07 remains OPEN | PROPOSED — NOT APPROVED |
| F-D03 / P1 | CM-073 | OP-26, OP-27, OP-23 | Non-authoritative external result report retaining existing pure verdicts, safe public error and separate private observations; no grant fields | New closed versioned machine-report/API shape after explicit schema decision; defer output serialization | Prefer external report first; no new PG API or structural verdict | None; approved P1 context only | Enables byte-level reporting fixtures only; zero runtime effects remain unproved | PROPOSED — NOT APPROVED |
| F-D04 / P2 | CM-006, CM-022 | OP-07, OP-08, OP-09 | Whole-invocation symbolic global budgets plus distinct logical bytes and charged actual reads; select numeric profile separately | Charge every material occurrence/read without dedup; separately bounded streaming versus bounded DOM implementation later | Prefer logical distinct-object work plus physical-read counter; no unmeasured cap defaults | F-D01, F-D02 | Prevents alias/cache reset budget bypass only if later enforced; CPU/RAM qualification still needed | PROPOSED — NOT APPROVED |
| F-D05 / P2 | CM-071 | OP-08, OP-09, OP-07 | Closed typed edges, U distinct nodes/E edge occurrences/d_ref active path plus actual bytes; X03 separate abstract cycles from real closure | Versioned typed expansion profiles for opaque payloads; keep opaque bytes nonrecursive and reject unsupported expansion | Prefer explicit closed typed edges with no inferred links; finite limits chosen separately | F-D01, F-D02, F-D04 | Can document real acyclic hash-valid closures without claiming hash-valid cycles or head authenticity | PROPOSED — NOT APPROVED |
| F-D06 / P2 | CM-072 | OP-22, OP-09, OP-24 | New closed version/profile with mandatory X04 plan-bound toolchain/executor refs; legacy rejected for new-profile use | Explicit versioned adapter with before/after bytes and review invalidation; defer adoption | Prefer reject-legacy-for-new-use until adapter independently reviewed | F-D01 | New exact plan and SubjectKey on change; no migration grant or implicit compatibility | PROPOSED — NOT APPROVED |
| F-D07 / P3 | CM-072 | OP-22, OP-13, OP-14, OP-24 | Conservative change-class/reapproval matrix: uncertain impact requires affected re-review, technical continuity never implicit | Always full new reviews; separately approved continuity evidence for proven technical-only deltas | Prefer full affected re-review initially; reviewer identity/rights validity require separate qualification | F-D06 | Preserves X04 content/rights rules; actual reviewers and competence are not assigned | PROPOSED — NOT APPROVED |
| F-D08 / P3 | CM-070 | OP-10, OP-11, OP-12, OP-15, OP-16, OP-19, OP-23, OP-28 | Supplied-evidence claim model separates unavailable/unknown from authenticated negative, uses established stage/category order and explicit causality | Defer all grouped operational causes; selected protocol may later define ordered evidence without changing X02 | Prefer claim vocabulary only, leaving real chronology blocked | F-D01, F-D03 | Can compare provided claims, cannot authenticate them or invent provider errors | PROPOSED — NOT APPROVED |
| F-D09 / P4 | CM-073 | OP-17, OP-20, OP-23 | Separately scoped no-side-effect qualification with independent process/file/network/store observer on pinned host | Defer runtime evidence and keep CM partial; alternate explicitly selected OS with equivalent declared threat model | Prefer qualification plan only after pure/resource/reference decisions, no tests now | F-D03, F-D04, F-D05 | BLOCKED until actual separately authorised environment/evidence; no self-reported zero-call proof | PROPOSED — NOT APPROVED |
| F-D10 / P4 | CM-070 | OP-15, OP-16, OP-19, OP-20, OP-23, OP-28 | Separately selected authority/head/clock/admission/completion protocol and fault-qualified provenance chain | Separate qualified provider architecture; keep production blocked and preview-only if absent | Recommend explicit future design/qualification commission or defer, no provider selection by Codex | F-D08 | BLOCKED_OPERATIONAL_EVIDENCE until actual trusted evidence; no exactly-once physical execution claim | PROPOSED — NOT APPROVED |
| F-D11 / P3 | CM-095 | OP-21, OP-23, OP-27, OP-28 | Purpose-minimised private diagnostics/report field allowlist and separately labelled disclosure/retention policy references | Keep only safe fixed public summary plus private custodian evidence; separately authorised redacted export profile | Prefer private minimisation; contract not publication permission | F-D03 | No hash anonymity, export grant, retention duration or deletion authority inferred | PROPOSED — NOT APPROVED |
| F-D12 / P4 | CM-095 | OP-21, OP-23, OP-28, OP-14, OP-19, OP-20 | Separate real custody/readers/access/export/retention/erase/tombstone policy and selected-host enforcement qualification | Private custody with no export until qualified; independent qualified disclosure channel after explicit approval | Recommend policy owner/custodian decisions before any actual access/export test | F-D11, F-D10 | BLOCKED_OPERATIONAL_EVIDENCE; privacy/negative-history integrity need compatible real controls | PROPOSED — NOT APPROVED |

## Exact owner questions

### F-D01

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-006, CM-071: Exact closed typed identity/ref/edge vocabulary with supplied bytes and no latest fallback; resolver authenticity separate? Альтернатива: Versioned explicit adapter family after review; defer all closure admission. Это не утверждение всего набора OP-09, не разрешение implementation/qualification и не production grant. Dependencies: None.

### F-D02

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-022: Freeze root logical node/key/token/decoded/member occurrence units; no numerical global caps? Альтернатива: Value-only nodes with separate keys budget; retain vocabulary open. Это не утверждение всего набора OP-07, не разрешение implementation/qualification и не production grant. Dependencies: None.

### F-D03

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-073: Non-authoritative external result report retaining existing pure verdicts, safe public error and separate private observations; no grant fields? Альтернатива: New closed versioned machine-report/API shape after explicit schema decision; defer output serialization. Это не утверждение всего набора OP-26, OP-27, OP-23, не разрешение implementation/qualification и не production grant. Dependencies: None.

### F-D04

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-006, CM-022: Whole-invocation symbolic global budgets plus distinct logical bytes and charged actual reads; select numeric profile separately? Альтернатива: Charge every material occurrence/read without dedup; separately bounded streaming versus bounded DOM implementation later. Это не утверждение всего набора OP-07, OP-08, OP-09, не разрешение implementation/qualification и не production grant. Dependencies: F-D01, F-D02.

### F-D05

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-071: Closed typed edges, U distinct nodes/E edge occurrences/d_ref active path plus actual bytes; X03 separate abstract cycles from real closure? Альтернатива: Versioned typed expansion profiles for opaque payloads; keep opaque bytes nonrecursive and reject unsupported expansion. Это не утверждение всего набора OP-08, OP-09, OP-07, не разрешение implementation/qualification и не production grant. Dependencies: F-D01, F-D02, F-D04.

### F-D06

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-072: New closed version/profile with mandatory X04 plan-bound toolchain/executor refs; legacy rejected for new-profile use? Альтернатива: Explicit versioned adapter with before/after bytes and review invalidation; defer adoption. Это не утверждение всего набора OP-22, OP-09, OP-24, не разрешение implementation/qualification и не production grant. Dependencies: F-D01.

### F-D07

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-072: Conservative change-class/reapproval matrix: uncertain impact requires affected re-review, technical continuity never implicit? Альтернатива: Always full new reviews; separately approved continuity evidence for proven technical-only deltas. Это не утверждение всего набора OP-22, OP-13, OP-14, OP-24, не разрешение implementation/qualification и не production grant. Dependencies: F-D06.

### F-D08

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-070: Supplied-evidence claim model separates unavailable/unknown from authenticated negative, uses established stage/category order and explicit causality? Альтернатива: Defer all grouped operational causes; selected protocol may later define ordered evidence without changing X02. Это не утверждение всего набора OP-10, OP-11, OP-12, OP-15, OP-16, OP-19, OP-23, OP-28, не разрешение implementation/qualification и не production grant. Dependencies: F-D01, F-D03.

### F-D09

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-073: Separately scoped no-side-effect qualification with independent process/file/network/store observer on pinned host? Альтернатива: Defer runtime evidence and keep CM partial; alternate explicitly selected OS with equivalent declared threat model. Это не утверждение всего набора OP-17, OP-20, OP-23, не разрешение implementation/qualification и не production grant. Dependencies: F-D03, F-D04, F-D05.

### F-D10

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-070: Separately selected authority/head/clock/admission/completion protocol and fault-qualified provenance chain? Альтернатива: Separate qualified provider architecture; keep production blocked and preview-only if absent. Это не утверждение всего набора OP-15, OP-16, OP-19, OP-20, OP-23, OP-28, не разрешение implementation/qualification и не production grant. Dependencies: F-D08.

### F-D11

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-095: Purpose-minimised private diagnostics/report field allowlist and separately labelled disclosure/retention policy references? Альтернатива: Keep only safe fixed public summary plus private custodian evidence; separately authorised redacted export profile. Это не утверждение всего набора OP-21, OP-23, OP-27, OP-28, не разрешение implementation/qualification и не production grant. Dependencies: F-D03.

### F-D12

**PROPOSED — NOT APPROVED.** Утвердить только следующее направление для CM-095: Separate real custody/readers/access/export/retention/erase/tombstone policy and selected-host enforcement qualification? Альтернатива: Private custody with no export until qualified; independent qualified disclosure channel after explicit approval. Это не утверждение всего набора OP-21, OP-23, OP-28, OP-14, OP-19, OP-20, не разрешение implementation/qualification и не production grant. Dependencies: F-D11, F-D10.

## Minimal first owner package

Recommend **F-D02 + F-D03**, each separately answered, not blanket approval: root-only accounting vocabulary without new numbers; external non-authoritative report contract without new PG API. Both use approved P1 constraints and can progress independently of providers and closure schema. They support low-risk future document-only counter and result-output fixtures, but do not close CM-022/073 or OP-07/23 automatically.

Next consider **F-D01** independently to unblock identity-dependent resource/closure decisions; including it in the first meeting is optional, never implicit adoption. F-D04/05 require explicit OP-07/08/09 subdecisions and numeric/profile choices before real resource/closure implementation. F-D06 precedes F-D07; no migration or continuity acceptance until separately decided. Provider/OS/custody choices remain blocked evidence gates, not prerequisites for the first pure decisions.

## Dependency-aware roadmap — future PROPOSAL, not execution

1. Independently audit these6 docs and original scopes; owner decides F-D02/F-D03 (and optionally F-D01) separately.
2. After separate docs/vector authorization, author finite root-counter/result-report fixtures for those selected rules. Symbolic limits may illustrate arithmetic only; no invented accepted numeric profile or new tests run now.
3. Decide F-D01 then F-D04, F-D05: exact reference units→global accounting→finite graph limits. No closure/resource implementation, full acceptance claims or benchmarks before OP-07/08/09 decisions and separate task authorization. Provider-less abstract fixtures remain explicitly abstract.
4. Decide F-D06 version/type/legacy boundary; then F-D07 reapproval policy. Prepare future raw-plan/hash/subject mutation and compatibility negatives without rendering after authorisation. Do not inherit old approvals or accept caller overrides.
5. Decide F-D08 causal data model and F-D11 private minimisation. Supplied-fact vectors may verify shape/equality only. Actual state/time/revocation/chronology and publication remain blocked.
6. Separately commission F-D09/10/12 qualification designs, select authorised hosts/trust roots/custodians and bounded operations. Only later separately authorised runtime/provider/Windows work can supply the required evidence. Storage S3 is not qualified by selection; no exactly-once physical execution claim.
7. Return evidence per CM to independent audit and owner acceptance. A row changes only in a future additive accepted record when its whole scope is satisfied; no formal target-count closure substitutes for runtime security, actual rights, science/editorial suitability or legal permission.

No next stage is started by this roadmap; G3.2.1 remains NOT AUTHORIZED. **STOP after publication.**
