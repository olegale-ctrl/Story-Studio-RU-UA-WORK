# CODEX TASK — SI-E01.2a-RESUME-F1: Packet capture consistency regression

**Date:** 2026-11-09  
**Status:** **READY FOR OWNER HANDOFF — FIX ONLY; NOT STARTED**  
**Finding:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_INDEPENDENT_REVIEW_F1.md` @ `4c975fab264bd002232005915b01b794fbb06788`  
**Owner constraints:** no PR, merge, release, `main`, unrelated changes, or follow-on SI-E01.2b. **STOP after publication.**

## 1. Exact entrypoint

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.

**Source branch:** `docs/story-intelligence-si-e01-2a-independent-review`. The handoff supplies its **exact final remote HEAD SHA** after this task is published. Verify it equals the supplied SHA before creating the new feature branch; if not, STOP.

**New branch:** `fix/story-intelligence-si-e01-2a-resume-f1-packet-capture`.

Do not rewrite, amend, rebase, force-push or change the existing feature branch `feat/story-intelligence-si-e01-2a-resume-payload-schemas` at `f19fa33685f05df632222dbcd84abcaca8258547`. Do not edit the historical `BLOCKED_CONTRACT` branch. Do not start SI-E01.2b or SI-E02.

## 2. Read before editing

- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_INDEPENDENT_REVIEW_F1.md` (the exact defect and review limitations).
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_RESULT.md` and the complete `story_intelligence/records_v1.py` / existing record tests.
- `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md`, `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` §§4.3 and 5.1–5.3, approved `docs/tasks/STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md` P03 and its owner approval.
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_CODEX_TASK.md` (original limits continue to apply).

The approved original→R1→R1a→R1b precedence remains unchanged.

## 3. Fix precisely this local invariant

A **persisted ReviewPacket** always has `payload.brief_ref` (non-null SIRef). Its `payload.review_state_at_capture.brief_ref` must be **non-null and equal to the Packet brief_ref**. Because ProductionBrief has a required non-null `creative_ref`, the captured `review_state_at_capture.creative_ref` must also be **non-null** in a ReviewPacket. These are **Packet-specific** local invariants, not changes to the general `BriefReviewState` value schema, which remains nullable outside Packet.

Use existing approved `SIValidationError` codes, preferably `PROVENANCE_MISMATCH`, with precise `$.payload.review_state_at_capture.brief_ref` / `.creative_ref` paths. Preserve the existing mismatched non-null brief-ref rejection. No new code vocabulary or inferred refs. Do **not** resolve the actual Brief to assert creative-ref equality; that requires the future resolver. Do not recompute or modify any user-provided projection.

**Mandatory negative cases:** start from a valid `fixtures()['ReviewPacket']`, then independently set captured brief_ref=null, creative_ref=null, and captured brief_ref to another well-formed ProductionBrief SIRef. Each must reject with the documented path/code; no mutation. A valid Packet remains accepted. Verify a general pre-Brief `BriefReviewState` can still structurally carry nulls where its standalone schema permits; do not globally make nullable fields mandatory.

## 4. Exact allowlist

Modify **only**:
1. `story_intelligence/records_v1.py` — narrow local Packet-specific check.
2. `tests/test_story_intelligence_records_v1.py` — minimal regression cases.
3. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_RESULT.md` — **new**, evidence and limitations.
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_CONTRACT_GAPS.md` — **optional new** file only if an actual blocking contract ambiguity is found.

Do not edit vector tests or literal values, SI-E01.1 files, existing task/review/result docs, any contracts/approvals, editorial/storage, dependencies/CI/config, workspace, `main` or other files. If an additional code change seems necessary, STOP and ask for a separate scope.

## 5. Tests and evidence

Run the exact minimal reproducers **before** the fix and record their observed result, then after the fix show all three negatives rejected and the valid Packet accepted.

Execute and report actual commands, interpreter/OS, counts, exit status:
```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```
Use the equivalent project venv command if the environment is Windows. The previous Codex report was 61 targeted / 903 full, **not** a guarantee of new counts. Preserve all 18 literal record and 3 R1b value vectors byte-for-byte; verify exact SI-E01.1 and storage vectors remain unchanged. Run `git diff --check`; confirm only allowlisted files, clean worktree, remote HEAD, parent/base, no PR/main changes.

If the full suite cannot run, report BLOCKED_ENV rather than PASS. If a material contract conflict is found, STOP and publish only the new F1 gap/result documents, no guessed implementation.

## 6. Strict exclusions and STOP

No operation execution, Run stage dispatch, cross-record resolver, full Closure, currentness computation, privacy authorization/export, PII detection, external network/Context7 calls unless actually required for external APIs (not required for this stdlib-only fix), model/provider, UI, renderer, persistence, protected editorial writes, S1/S2/S3 storage changes, Windows VM or `PUBLISH_REVISION`.

Publish **only** the new isolated fix branch and result, **STOP** for independent review. SI-E01.2a-RESUME remains `CHANGES_REQUIRED` until the fix is reviewed; SI-E01.2b requires a new separately scoped task and owner handoff.
