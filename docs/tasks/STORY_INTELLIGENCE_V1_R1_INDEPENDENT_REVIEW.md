# Story Intelligence V1 R1 — independent review and final narrow correction gate

**Date:** 2026-11-09. **Status:** **SI-R01–03 RESOLVED IN PROPOSAL; COMPOSITE CHANGES_REQUIRED (NARROW SI-R04)**. This is independent technical review, **not** owner approval of SI-D01–SI-D10.

## Provenance / verification

- Repo `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Original proposal `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` @ `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
- Earlier independent review `docs/tasks/STORY_INTELLIGENCE_V1_INDEPENDENT_REVIEW.md` @ `9ce417c81c532255185c200aebcff6cf628983a6`.
- R1 `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` @ `978fbed45513a00e851201a9018d17c7da4752be`.
- GitHub verified R1 branch remote HEAD matches; R1 base exact previous review HEAD; compare shows one commit / one new Markdown file / **691 lines added**, zero behind. No PR found. `main` observed unchanged at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`.
- Examined complete R1 and original §3/§8 operation model. No runtime tests executed independently; publication diff verified remotely.

## Resolved defects from first review

**SI-R01: RESOLVED** — R1 explicitly defines `BRIEF_ASSEMBLY`, `PACKET_EXPORT`, `REVISION` RunRecord stages and HUMAN_EDIT mode. It separates run input closure from output refs and defines exact replay boundaries. Automatic output cannot silently become MANUAL_INPUT merely because a user clicked/selects it.

**SI-R02: RESOLVED** — EvaluationReport retains immutable eligibility `ELIGIBLE_FOR_CREATIVE` independent of future creative/brief choices. `BriefReviewState` is separate, calculated, nonpersisted projection from explicit Selection heads. Withdrawal and changed input revisions do not modify historic evaluation bytes or confer authority.

**SI-R03: RESOLVED** — persisted immutable ReviewPacket selected consistently (not ephemeral). R1 has exact closure/ref-only output, privacy grant/redaction, capture vs current-state, retention dependence, no direct editorial/renderer export, and negative cases. This is **a proposed privacy design, not security certification**; SI-D03/SI-D07 owner decisions remain necessary.

R1 supplies 20 new proposed acceptance cases and explicit mapping to SI-T01–26. This resolves the requested reconciliation at the level of the three specific earlier findings.

## SI-R04 — record creation / revision coverage (new, narrow contract gap)

### R04-A — StoryIdea cannot be revised through declared API

Original proposal §3 declares `StoryIdea` with immutable versioned revision, and V1 workflow allows user edits/creative correction. R1 §2 `DISCOVER_LOCAL` outputs StoryIdea, but `REVISE_INPUT` accepts only the same `RecordSet` listed for `RECORD_INPUT`. This set does **not** include StoryIdea. Thus after Discovery there is no declared way to create `StoryIdea` next revision with `previous`, while preserving derivation. The only path would recreate a new idea with a new id, breaking intended identity/edition history.

**Recommended correction:** define distinct *createable* and *revisable* closed sets. Add StoryIdea to `REVISE_INPUT` only, with HUMAN_EDIT/REVISION run, exact previous/input/provenance retention; keep initial StoryIdea creation only under `DISCOVER_LOCAL`, unless owner explicitly chooses a separate manual-create interface. No schema2 change.

### R04-B — manual CreativeAlternative has a mandatory run but RECORD_INPUT has no run

Original proposal §3 requires `CreativeAlternative.run_ref:SIRef`. R1 §2 allows `RECORD_INPUT(CreativeAlternative)` with `MANUAL_INPUT` or USER_IMPORT, and states no RunRecord is created for RECORD_INPUT. Yet successful CreativeAlternative under `PROPOSE_CREATIVE` references the exact creative RunRecord. A purely manual alternative has no run that can correctly satisfy this required payload field without invented provenance or misleading reference to someone else's run.

**Recommended correction for minimal V1:** remove CreativeAlternative from `RECORD_INPUT` creatable set; keep template-based `PROPOSE_CREATIVE` (CPU-only, no LLM) and let user modify that output through `REVISE_INPUT` with HUMAN_EDIT/REVISION run. Clarify semantic difference between `CreativeAlternative.payload.run_ref` (original creating CREATIVE run, retained as ancestry in edited revisions) and `H.origin.run_ref` (the exact REVISION run on HUMAN_EDIT). For initial template output those point to the same CREATIVE run. Do not introduce false manual provenance or loosen mandatory run check. If genuinely standalone hand-authored CreativeAlternatives are a V1 product requirement, document a **different** explicit create path with truthful provenance and make it an owner choice; do not invent a generating run.

### Required regression examples

- DISOVER_LOCAL creates StoryIdea revision1; user changes viewer question by REVISE_INPUT -> same id/revision2, previous exact ref, HUMAN_EDIT origin and no source/provenance loss.
- Template CREATIVE run produces CreativeAlternative; human edit -> next revision with preserved original CREATIVE run and HUMAN_EDIT REVISION run; cannot mark manually reworked template as original MANUAL_INPUT.
- RECORD_INPUT attempts to fabricate CreativeAlternative or StoryIdea must fail with typed closed-set error; old declared / accepted operations retain other behavior.
- Repeating an exact revise request must return same refs, not generate another revision or rewind heads.

## Owner gate recommendation

Preserve SI-D01–SI-D10 as **PROPOSED**, and present recommended bounded defaults after **SI-R04** correction, rather than silently approving choices. The owner should explicitly approve overall SI V1 shape, scoring weights/UNKNOWN/blockers, persistence privacy/retention, selection and claims-review semantics, redacted private packet export, provider opt-ins, implementation stages.

**Next step:** one small docs-only R1a erratum covering only R04-A/B and acceptance examples. Then perform final independent check and present composite proposal for owner's explicit decision. No implementation until then.

Keep storage S3.2b `BLOCKED_HOST_NOT_PROVIDED`; SI V1 is CPU-only Windows 10/11 offline/manual and neither modifies protected S1/S2/approval/rights nor creates renderer permission. No PR/merge/release/`main` changes.
