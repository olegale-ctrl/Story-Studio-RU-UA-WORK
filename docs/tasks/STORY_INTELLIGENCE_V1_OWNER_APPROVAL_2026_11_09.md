# Story Intelligence V1 — owner approval of composite specification

**Date:** 2026-11-09
**Decision status:** **APPROVED — SI-D01 through SI-D10, composite specification**
**Implementation status:** **STAGED / EACH TASK SEPARATELY BOUNDED**
**Owner instruction (verbatim):** «Утверждаю SI-D01–SI-D10 в рекомендованной редакции, включая исходную спецификацию, R1 и R1a. Подготовь отдельное ограниченное задание Codex для SI-E01. Без merge/main.»

## 1. Exact approved contract

This approval refers to the exact composite set, with precedence as described in the errata:

1. `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` — `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
2. `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` — `978fbed45513a00e851201a9018d17c7da4752be`. R1 overrides only the original clauses it explicitly identifies.
3. `docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md` — `b3f16984edc8daad364f356aa51aeddc2ac0b5b8`. R1a overrides only its identified R1 operation/RecordSet clauses.
4. `docs/tasks/STORY_INTELLIGENCE_V1_COMPOSITE_INDEPENDENT_REVIEW_AND_OWNER_DECISIONS.md` — `c38f6fed74c04a60f7d6446fd3153e87112cd3f6`, including its ten recommended SI-D01–SI-D10 decisions and bounded implementation sequence.

The independent review's earlier `READY_FOR_OWNER_DECISION — SPEC_ONLY` status is superseded **only as to owner approval** by the explicit owner instruction above. This record is not evidence that executable implementation has been tested or approved for release.

## 2. Approved decisions and preserved limits

- **SI-D01:** offline/manual, CLI-first, separate Discovery → Evaluation → Creative → pre-script Production Brief → private discussion packet; no automatic trends/search/renderer.
- **SI-D02:** SI/1 draft namespace, exact typed SIRef/ERef, immutable revisions, Known/UNKNOWN, provenance and method stages, strict canonical bytes/hash and closed operation sets per R1/R1a; no editorial schema2 modification.
- **SI-D03:** user-owned local private draft workspace outside Git and protected storage **as a principle**. Exact path, persistence format, atomicity, concurrency, integrity, backup, retention and cleanup **remain a separate pre-implementation contract**.
- **SI-D04:** nine heuristic criteria, 0–5 ratings, proposed weights `15/10/10/20/15/10/10/5/5`, UNKNOWN not zero, blockers outrank scores; no viral-probability claims.
- **SI-D05:** explicit human research/review, selection/withdrawal and provenance; labels are not trusted identity, rights grants or editorial approval. EvaluationEligibility remains independent of later selection.
- **SI-D06:** three distinct safe RU/UK creative strategies where feasible, natural language, qualitative 0–30s hooks, evidence/qualifier preservation.
- **SI-D07:** separate pre-script Brief and immutable, private, redacted, discussion-only ReviewPacket; no automatic network/file export or editorial write; detailed privacy/lifecycle requires later contract.
- **SI-D08:** Windows 10/11 target, CPU-only Intel-integrated-graphics viable; local WAV/stills/FFmpeg planning and honest capability limits.
- **SI-D09:** no network, paid, GPU, LLM, external code/model/Chinese corpora or provider adoption in V1 without separate approval/licence/privacy/cost review; commercial-release licence checkpoint unchanged.
- **SI-D10:** composite specification and future acceptance cases `SI-T01–26 + R1-T01–20 + R04-T01–10` approved as **requirements**, not as tests already passed; independently reviewed bounded implementation steps.

## 3. First bounded implementation assignment

The owner requested a **separate limited Codex task for SI-E01**. The first unit is **SI-E01.1 — pure types, strict canonical codec and independent literal vectors**. Its precise source/test allowlist, entrypoint and stop conditions are in `docs/tasks/STORY_INTELLIGENCE_SI_E01_1_CODEX_TASK.md` on this documentation branch.

**Only that limited assignment may be handed to Codex.** SI-E01.2 (full record schemas, run/operation semantics), SI-E02 onward, persistence, editorial adapter, renderer, VM/native storage, provider integration, PR/merge/release and `main` changes are **not** authorized by this approval or by the SI-E01.1 handoff. The implementation task may be executed only when the owner forwards the exact task; publishing this record does not execute code.

## 4. Storage and governance

- S3.2a: `ACCEPTED / PURE_ONLY`; S3.2b: `BLOCKED_HOST_NOT_PROVIDED`, still on hold.
- `PUBLISH_REVISION` remains disabled; partial COMMIT reconstruction OFF; S1/S2/D-01/golden, A/E/O/D contracts and editorial rights/approval boundaries unchanged.
- Do not commit media, personal research inputs, secrets, host identifiers, generated workspaces, downloaded models or test outputs containing private data.
- No PR/merge/release, no `main` changes; independent verification and explicit owner gate before each next stage.

**Next action:** hand off SI-E01.1 task on its pinned documentation branch, execute on a new feature branch, publish evidence and STOP for independent review.
