# CODEX TASK — Story Intelligence V1 R1 contract reconciliation (docs only)

**Date:** 2026-11-09. **Status:** proposed specification repair only. No code or implementation permission.

## Source / branch

Repo `olegale-ctrl/Story-Studio-RU-UA-WORK`. Read this file and `STORY_INTELLIGENCE_V1_INDEPENDENT_REVIEW.md` from `docs/story-intelligence-v1-independent-review`. At execution, pin and report the exact remote HEAD as the base; if different from the handoff SHA, STOP for reconciliation. Never switch silently to `main`.

Create **new** branch `docs/story-intelligence-v1-r1-contract-clarifications` from that exact SHA (never force/reset an existing branch). Owner approval is still pending for SI-D01–SI-D10.

## Binding documents

1. `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` at `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
2. `docs/tasks/STORY_INTELLIGENCE_V1_INDEPENDENT_REVIEW.md` on pinned base (SI-R01–SI-R03).
3. `docs/architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md`.
4. `docs/tasks/STORY_INTELLIGENCE_COMPLETED_STAGES_REVIEW.md`.
5. Actual existing `editorial/model.py`, `editorial/current_package.py`, `editorial/versioned_codec.py`, `scripts/first_video.py`, and current rights/approval contracts, read-only.
6. Existing S3.2a acceptance and S3.2b hold. External register stays in separate branch; do not merge/adopt anything.

## Output — one complete erratum

**Only allowed file (NEW):**
`docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md`

Write a self-contained, normative **PROPOSAL / AWAITING OWNER APPROVAL** correction that has priority over the original proposal **only** for precisely identified clauses SI-R01–03 once accepted. The original source document remains unchanged.

- **R01 provenance:** provide full closed revised H.Origin/RunRecord stages and/or separate projection semantics for `ASSEMBLE_BRIEF` and `EXPORT_REVIEW_PACKET`. Map every §8 operation to: output type, recorded vs ephemeral, provenance mode, run/stage if needed, exact input closure, versioned method identifier, idempotency and stale/invalid behavior. Machine/template/derived must not become manual by selection. No circular refs/hashes.
- **R02 evaluation vs selection:** distinguish immutable per-evaluation diagnostics/eligibility from later explicit human selection and derived brief-review recommendation. Show actual records/projections, their exact refs and transition/re-evaluation rules, no implicit permissions. Include success before/after selection, blocker/unknown, withdrawal and input revision change.
- **R03 packet identity:** decide and specify persisted immutable packet or ephemeral read-only projection, not both. Define deterministic byte/layout semantics only to the extent required for coherency; export shape and `Response.output_refs` vs inline data, exact provenance/closure, status, privacy/redaction for locators and human labels, lifetime and invalidation. Keep `DISCUSSION_ONLY` and no editing/rights/render grants.

Provide a precise compatibility/override table quoting original section numbers and what is replaced vs retained, plus ≥8 table-driven acceptance cases (positive and negative) testing all three R issues. Explicitly identify any further needed owner decisions rather than silently selecting production policy. Validate that existing SI-T01–SI-T26 remain consistent or state necessary amendments within the erratum; no changes to other approved contracts. Keep RU/UK, Windows CPU-only, offline and commercial-license restrictions.

## Checks and STOP

Read-only inspection and documentation checks only. No CLI/engine/schema/codec/tests code, no dependencies, storage, Windows native, model calls, web crawling or paid API. Do not modify proposal, review, existing docs or main. No PR/merge/release. Run `git diff --check`, verify exact one-new-file allowlist, remote HEAD and clean working tree after publication. Do not claim unit tests as run.

Report source base SHA, output branch HEAD SHA, one-file diff, reconciliation summary, remaining owner decisions and any contract blockers. **STOP** for independent review and owner approval. This task does not imply acceptance of SI-D01–SI-D10.
