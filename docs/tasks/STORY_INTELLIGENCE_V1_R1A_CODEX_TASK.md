# CODEX TASK — Story Intelligence V1 R1a, SI-R04 narrow contract correction

**Date:** 2026-11-09. **Scope:** docs-only, exact SI-R04. **No implementation or owner approval implied.**

## Starting point

Repository `olegale-ctrl/Story-Studio-RU-UA-WORK`. Exact source branch:
`docs/story-intelligence-v1-r1-independent-acceptance`.
Read `docs/tasks/STORY_INTELLIGENCE_V1_R1_INDEPENDENT_REVIEW.md` and this task.
Confirm the source branch remote HEAD equals the SHA in handoff, or STOP for reconciliation.
Create `docs/story-intelligence-v1-r1a-record-operations` from that exact commit.
Do not modify, merge or rebase onto `main`.

## Exact normative context (read-only)

- Original `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` @ `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
- R1 `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` @ `978fbed45513a00e851201a9018d17c7da4752be`.
- Current independent review: `docs/tasks/STORY_INTELLIGENCE_V1_R1_INDEPENDENT_REVIEW.md`.
- Story Intelligence concept and completed-stage review, existing `editorial/model.py` and rights/approval boundaries. Source only; no edits.
- S3.2a PURE_ONLY / S3.2b BLOCKED_HOST_NOT_PROVIDED unchanged. External ideas candidate status unchanged.

## Only deliverable

Create exactly one new file:
`docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md`

Status **PROPOSAL / AWAITING OWNER APPROVAL**. This is a small additive erratum to original+R1, overriding only R1's specified operation/type rules.

**R04-A:** define complete closed `CreateableRecordSet` and `RevisableRecordSet`; allow StoryIdea to be revised via `REVISE_INPUT` after `DISCOVER_LOCAL`, with exact previous revision, HUMAN_EDIT + REVISION run and full preserved ancestry. Explicitly forbid creating StoryIdea through `RECORD_INPUT` unless separately owner-approved. Maintain strict unknown fields/ref validation.

**R04-B:** for the minimal V1, disallow manual `RECORD_INPUT(CreativeAlternative)`; create via `PROPOSE_CREATIVE` template run, then human edit via `REVISE_INPUT`. Explicitly distinguish the required original creative provenance run in CreativeAlternative payload from human Revision run in H.origin, and whether/how the former is retained through successive edits. Do not fabricate a Creative Run, label derived content MANUAL_INPUT, relax mandatory run fields or change source/editorial schemas. Note standalone hand-authored alternatives as deferred optional design requiring separate owner approval if needed.

Include exact replacement operation rows, affected RecordSet/types, method/stage constraints and idempotent result behavior; at least four positive/negative future acceptance cases for R04, including exact retry, alternate input revision and previous lineage. Check all earlier R1-T01–20 and SI-T01–26 for impacted cases and document amendments without rewriting those artifacts.

No new API operation, no new schema2 authority or provider. Keep RU/UK offline CPU-only, user/local privacy, no direct handoff or renderer. No code, tests, dependencies, Windows service, models, API calls or protected writes. No changing existing files and no PR/merge/release/main.

Run `git diff --check`; verify one-file allowlist, exact base, remote HEAD, clean worktree after publish. Unit tests are not necessary and must not be claimed PASS unless actually executed.

Publish docs-only feature branch and hand off full exact base/commit SHA plus a short decision summary. **STOP** for independent review and explicit owner SI-D01–SI-D10 approval. 
