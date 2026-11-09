# SI-E01.2a-RESUME / F1 — independent acceptance

**Date:** 2026-11-09
**Decision:** **ACCEPTED / PURE_LOCAL_TYPED_RECORDS_ONLY** (F1 correction reviewed)
**Review mode:** independent GitHub commit/diff and static source/test review, **not** independently executed tests or Windows qualification.
**Source acceptance:** original RESUME `f19fa33685f05df632222dbcd84abcaca8258547`, accepted together with F1 at `557c1fafac9a8bccd0421164436aa17886b82a77`.

## 1. Exact source and governance

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- F1 branch: `fix/story-intelligence-si-e01-2a-resume-f1-packet-capture`.
- Exact F1 base: `f752e9aa5745514677dd1fd9dcf82b915309c3b1`.
- F1 commit and remote head: `557c1fafac9a8bccd0421164436aa17886b82a77`.
- GitHub compare: one commit ahead / zero behind; **three allowlisted changed files: 166 additions, one deletion**:
  - `story_intelligence/records_v1.py` (3 additions / 1 deletion);
  - `tests/test_story_intelligence_records_v1.py` (34 additions);
  - `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_RESULT.md` (new, 129 additions).
- `main` observed at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`. No PR for this branch; GitHub commit-specific status checks and PR-triggered workflow runs not reported. CI PASS is **not** claimed.
- Prior independent finding and bounded task in documentation base remain unchanged. No PR/merge/release/main modification made by this review.

## 2. Finding F1 — reviewed against source and contracts

Prior blocker: nullable `BriefReviewState` value is valid before Brief creation, but Packet-specific capture must reference the actual Packet Brief and a CreativeAlternative; old `_packet` check skipped equality for captured `brief_ref=null` and allowed `creative_ref=null`.

The exact production diff replaces `if review['brief_ref'] is not None and review['brief_ref'] != p['brief_ref']` with `if review['brief_ref'] != p['brief_ref']`, and adds a Packet-only rejection for `review['creative_ref'] is None`. Both use approved `PROVENANCE_MISMATCH` with exact paths under `$.payload.review_state_at_capture`. There is no modification of the general `_REVIEW` schema, no assignment or mutation of client input and no external ref resolution claimed. The existing mismatch check is preserved.

Five new test methods cover captured null Brief, null Creative, wrong well-formed nonnull Brief, accepted valid Packet/detached copy, and a nullable general pre-Brief projection. The last uses the package's internal value schema because there is no separate public projection API; it is **not** evidence of end-to-end projection correctness.

Codex reports pre-fix five cases: **2 FAIL / 3 OK**, post-fix **5 OK**. Reported final targeted `66 OK`, full `908 OK`, Linux Python 3.12.14, exit0; **these commands were not independently rerun**. The original 18 complete record and 3 R1b FieldGrant/FieldView literal vectors were not modified by this F1 diff, nor were existing SI-E01.1 or storage test/source files.

**F1 decision:** **ACCEPTED**. The specific local contradiction is closed without changing the original/R1/R1a/R1b contracts or broadening the pure schema validator.

## 3. Resulting scope-limited SI-E01.2a acceptance

The prior SI-E01.2a-RESUME static review found all **18** typed payload schemas, three public record/ref validation APIs, closed R1b TEXT/STATE/REDACTED path mapping and uniqueness/order, canonical bytes/identity, local nested value constraints and independent literal vectors. F1 was the sole identified blocking finding in that review; the fix closes it.

Therefore **SI-E01.2a-RESUME (including F1) is ACCEPTED / PURE_LOCAL_TYPED_RECORDS_ONLY** as a structural foundation, **not** as a complete domain graph validator, operation engine, packet privacy authorization or production/workspace exporter.

Remaining mandatory subsequent checks are: exact SIRef/ERef resolution and hash verification, transitive Closure and DAG/cycle/history and Run-stage method/ancestry binding, semantic vs audit currentness, R1a creation/revision roots, Evaluation/Selection/Brief/Packet prerequisites, source actual field/index/text hash matching and privacy review. Their absence is **deferred according to the bounded scope**, not permission to silently skip them later. Synthetic single-record vectors do not form a verified graph. CI/Windows-native PASS and credential/rights/human-identity claims are not made.

Prior **SI-F01** worst-case 1 MB integer parsing performance remains a nonblocking hardening concern; do not change canonical byte policy or introduce an unapproved digit cap.

## 4. Stage gate

Next eligible step: **separate bounded SI-E01.2b.1 — pure read-only SIRef resolver, exact record hash and transitive DAG/Closure with provenance reference coverage**. Work must have its own exact source SHA, isolated branch, strict allowlist, literal independent graph vectors and negative tests, and independent acceptance. Do **not** grant SI-E01.2b.2 operations/currentness, SI-E02, persistence, provider, editorial authority, renderer, PR, merge, release or main modifications.

Original SI-D01–SI-D10 and exact original→R1→R1a→approved R1b precedence unchanged. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED. Context7 remains optional for external API documentation and irrelevant to this stdlib-only stage.

**STOP** after publishing this acceptance and bounded next-task documentation. No code is executed by this documentation publication.
