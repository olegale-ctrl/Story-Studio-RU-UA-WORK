# Owner decision dossier

**MVP-08B.2a · 2026-11-19 · DOCS_ONLY · PROPOSAL — NOT APPROVED FOR IMPLEMENTATION.**

## Approved boundaries — no reopening

The current owner explicitly accepts MVP08B.2 **as an audit with limitations** and approves DOCS_ONLY preparation of08B.2a. D01–D08 remain exactly OWNER_APPROVED atf0bce140451bf00a86f3939330e77ed63b2c98be/MVP_08_OWNER_APPROVAL.md;08Aacceptance/limitations remain unchanged. Initial$0,no live calls/payments/browser automation/production permissions;bounded confirmations,documented rights,quota pause andassumptions remain. No new real provider/model chosen. These are APPROVED source facts,not choices to reopen.

The following10questions are genuine futureimplementation blockers or scope-deferral decisions. **All remain OPEN;recommended alternatives are PROPOSAL.** An independent review plus a separate owner decision must name exact choices/source/base/allowlist before any code. Silence or approval ofthis document package is not automatic approval ofall technical rows. For documentation completion,no further owner decision is required.

## EC-01 — Result boundary and state profile

**Status: OPEN / PROPOSAL.**

Problem: B.1 COMPLETED requires SG05/SG10,not fake provider completion;core cannot truthfully finish handoff yet.

Source: [MVP_08B_1_STATE_MACHINE.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_STATE_MACHINE.md) / State registry,SM11–16;ASSET_HANDOFF SG05/10/11. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: prefix through RESULT_AVAILABLE with all later handoff disabled. B: defer core release until separately qualified full local saga permits COMPLETED.

Recommendation: A,with explicit nonterminal prefix result and no whole-pipeline claim.

Story Studio impact: Useful durable core without silently lowering completion proof.

Risks: Consumers may misread resultavailable as complete;reserved states/phase labels must stay explicit.

Verifiable acceptance: P008,A001,A007 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-02 — Immutable identity,idempotency and hash projections

**Status: OPEN / PROPOSAL.**

Problem: B.1 needs purpose ID/key scope,but draft/group projections do not resolve possible batch/request hash cycle or terminal-key lifetime.

Source: [MVP_08B_1_JOB_CONTRACT.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_JOB_CONTRACT.md) / GenerationJob object;Schema conventions;Identity/idempotency rules. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: explicit RequestIntent core→manifest→permit→acceptance graph,persistent full tuple keys,no edits/renewal in first profile. B: retain proposal-only until another exact compatible projection/lifecycle is supplied.

Recommendation: A as the narrow clarification;not automatic schema adoption.

Story Studio impact: Stable accepted/reused/conflict and no false duplicate/provenance equivalence.

Risks: A new field/profile and closed projections need explicit approval;do not hash grant/manifest back into core.

Verifiable acceptance: P001–P005,P012,P020,D001,D016 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-03 — Store and fault model

**Status: OPEN / PROPOSAL.**

Problem: RAM LAB/S2 is not persistent JobStore;Library SQLite is a different resource.

Source: [MVP_08B_1_IMPLEMENTATION_PLAN.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_IMPLEMENTATION_PLAN.md) / MVP08B.2 entry;JOB_CONTRACT execution/audit;OD07. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: separate managed SQLite single-writer JobStore with proposed DELETE/FULL/FK settings,identity/version,atomic W and no auto-repair. B: only pure fake-store tests until a different durable design/profile is frozen.

Recommendation: A after separate real local qualification;B for pure proof before qualification.

Story Studio impact: One durable authority instead of extra UI/store workarounds.

Risks: DBcommit is not universal power-loss/hostile OS protection;missing store must not reset dedup.

Verifiable acceptance: D001–D005,D007,D009–D011,D018 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-04 — Controller ownership,lease/fence and clock

**Status: OPEN / PROPOSAL.**

Problem: CAS/fencing requires exact owner/restart/time assumptions;expiry alone cannot stop uncontrolled workers.

Source: [MVP_08B_1_STATE_MACHINE.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_STATE_MACHINE.md) / Global W;SM05/25/26;OPEN_DECISIONS OD05/OD07. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: one same-process serial logical worker,qualified exclusive owner lock,store-incarnation+lease tokens and failclosed clock. B: separately qualify multiprocess/external effect fencing before permitting that architecture.

Recommendation: A;no autonomous lease-steal/preemption of a live owner.

Story Studio impact: Simplifies initial offline fault boundary while retaining stale-token checks.

Risks: Check-to-effect and maliciousOS risk not removed;clock/reboot/lock behavior requiresplatform proof.

Verifiable acceptance: P009/P010,D005/D006/D012,W001–W004,W007 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-05 — Outbox,simulator acceptance and recovery

**Status: OPEN / PROPOSAL.**

Problem: Acceptance can commit in simulator while controller misses ACK;one DBtransaction cannot cover both.

Source: [MVP_08B_1_OFFLINE_SIMULATOR.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_OFFLINE_SIMULATOR.md) / durable fixture ledger,SIM08/09/18;STATE_MACHINE SM05–10. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: separate simulator ledger and immutable effect token/payload;W-before-effect;lookup-onlyunknown recovery;generation attemptcap1. B:restrict to pure fake-ledger tests and block durable dispatch until this protocol is qualified.

Recommendation: A as target;B until real commit/reopen evidence.

Story Studio impact: No regeneration after uncertain acceptance;preserves future external boundary.

Risks: SimulatorStore must not become second job scheduler;missing ledger not evidence no accept.

Verifiable acceptance: P013–P018,D002–D004,D008,D015 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-06 — Observer/cursor/wait semantics

**Status: OPEN / PROPOSAL.**

Problem: No authoritative JobStore observer currently exists;local report cannot decide completion.

Source: [MVP_08B_1_JOB_CONTRACT.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_JOB_CONTRACT.md) / execution/state_revision,polling;B.2 SP readiness #6–8. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`. Additional exact audit/SPsources:`04ea194e4d57c8a0550d7412281da58d4ba252c5`and`16d28ec0376c8c28f879c8aacb18d5378fea83a3`.

Alternatives: A: consistent store/job revision+receipt snapshot and bounded read-only wait with explicit predicate. B: single-shot observe only until qualified wait is supplied.

Recommendation: A if read deadline/cursor rules are frozen;B remains safe fallback.

Story Studio impact: Thin future CLI can wait without owning retry/queue.

Risks: Stale mirror/store-replacement/currentness confusion;timeout must not mutate job.

Verifiable acceptance: P019/P021,D014 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-07 — Synthetic fixture authority,resource andretention envelope

**Status: OPEN / PROPOSAL.**

Problem: Original OD05/07/08 unresolved;there are no pinned F01 bytes/hash in this proposal.

Source: [MVP_08B_1_OPEN_DECISIONS.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_OPEN_DECISIONS.md) / OD05,OD07,OD08;OFFLINE_SIMULATOR F01manifest. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: only self-authored nonsensitive pinned F01/project/prompt and trusted test-harness synthetic scope;proposed numeric caps;retainhistory,no automatic user-data deletion. B: specifications/pure placeholders only,with no positive durable fixture execution.

Recommendation: A only after exact source/bytes/rights/profile review;otherwiseB.

Story Studio impact: Real controlled offline success is testable without models/provider permissions.

Risks: Fake hashes/principals must never be called verified production evidence;caps need evidence.

Verifiable acceptance: P006/P007/P011/P017/P023/P024,D017,D018 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-08 — Typed errors anduncertainty vocabulary

**Status: OPEN / PROPOSAL.**

Problem: Unknown effects andknownfailed outcomes cannot share generic success/failure fallback.

Source: [MVP_08B_1_JOB_CONTRACT.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_JOB_CONTRACT.md) / Related contracts JobError;RECOVERY_MATRIX. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: closed local code mapping with preserved B.1retry/effect/billing classes andexplicitcheck order. B: freeze a different complete mapping before implementation.

Recommendation: A;no untyped swallowed exception or newlifecycleenum.

Story Studio impact: Recoverable diagnostics preserve exact required action andscope.

Risks: Leaking prompts/secrets or collapsingUNKNOWN intoNO_EFFECT could duplicate effects.

Verifiable acceptance: P015/P018/P021,D007–D009 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-09 — Asset Library/project save boundary

**Status: OPEN / PROPOSAL.**

Problem: No unique import receipt/stable project saveCAS;P1-01/02/03 remain open.

Source: [MVP_08B_1_ASSET_HANDOFF.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_ASSET_HANDOFF.md) / SG04–SG11;OPEN_DECISIONS OD02/03/04/06. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`.

Alternatives: A: no import/attach/save in initial core;retainresultandhold beforeSM12. B: separately approve required Library/save/validation/lifecycle extensions first.

Recommendation: A for initial core;B as a later separate qualificationstage,not current widening.

Story Studio impact: Existing accepted interfaces unchanged,missingguarantees visible.

Risks: Library links/cached status/sameSHA may falselylookcomplete;no swallowed ambiguous import.

Verifiable acceptance: A001–A010 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## EC-10 — Minimum Route D compatibility

**Status: OPEN / PROPOSAL.**

Problem: SP Dwhole-film render/gates differs from B.1anchor clipT2V/I2V;sevenSPtypes are unregistered.

Source: [MVP_08B_1_JOB_CONTRACT.md](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/f0bce140451bf00a86f3939330e77ed63b2c98be/experimental_mvp/reports/MVP_08B_1_JOB_CONTRACT.md) / request.mode;B.2 SP readiness;SP1.1diagnostic contract. Exact source SHA`f0bce140451bf00a86f3939330e77ed63b2c98be`. Additional exact audit/SPsources:`04ea194e4d57c8a0550d7412281da58d4ba252c5`and`16d28ec0376c8c28f879c8aacb18d5378fea83a3`.

Alternatives: A:freeze only accept/observe/receipt boundary anddefer Dexecutionmapping. B: separately specify one bounded syntheticrender-plan handler/schema before integrating D;no genericDAG.

Recommendation: A now;assessB only underseparately approved interface scope.

Story Studio impact: Core remains minimal;RouteDstayshonestlyBLOCKED ratherthan direct rendererbypass.

Risks: Changing modes/IDs or treating SPdigestasjob payload would expandarchitecture/authority.

Verifiable acceptance: P020/P022,A001,L006 in ACCEPTANCE_ORACLES.md;allNOT_RUN. Rejection/missing choice keeps its dependent operationblocked. No choice authorizes implementation,merge,live/production orotherSP-OD01–09.

## Original OD01–OD08 disposition

|Originaldecision|Status preserved|Effect on minimal proposal|
|---|---|---|
|OD01exactliveWanprofile|OPEN/deferred|No liveprofile selected;does not block writing thisofflineproposal|
|OD02Libraryuniqueimportreceipt|OPEN|Blocks future import/SM14;EC-09defers|
|OD03stableproject/saveCAS|OPEN|Only explicit fixtureprojectIDs now;realprojects/save blocked|
|OD04decodedcount/media policy|OPEN|No new decoder/evidence claim;futurevalidation qualification required|
|OD05authority/revocation/expiry|OPEN|EC-04/07must freeze exact synthetic scope before effect-capable code|
|OD06Tk isolation/lifecycle|OPEN|NoGUI/Tk in initial scope;cannot claimclosed|
|OD07store/resources/platform|OPEN|EC-03/04/07 +durable/Windowsseparate qualification|
|OD08retention/deletion|OPEN|Nonsensitive authored fixtures only;no automaticuser-data deletion|

No D01–D08 contradiction was found that warrants reopening an approved decision. Newhash/identity/completion choices clarify unresolved B.1 proposals,not override approved production authority. Futureowner response should identify EC-ID,chosen/modification,scope,authority/date,source/base andrequired evidence.
