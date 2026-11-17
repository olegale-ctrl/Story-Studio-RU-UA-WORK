# SI-E02.2.1d — Bounded evaluator readiness audit

Дата: 2026-11-12 (Europe/Kyiv). **DOCS ONLY / OWNER REVIEW PREPARATION.**
Base: `1fa37fa03b0dfb0a6ed754ddf70e9665c5a91eb0`.
**RC-P01–P06 NOT APPROVED. IMPLEMENTATION NOT AUTHORIZED.**

## 1. Verdict

**Required-current/frozen findings logic can be implemented as local pure values on
existing SI/1 after exact contract approval and a separate bounded task. No SI/1
schema/API change has been demonstrated necessary.**

**Approval RC-P01–P06 alone is NOT sufficient to declare the complete bounded EVALUATE
classifier ready. BC01/BC02, non-freshness BC03 and BC05/T25 still need a small exact
base-condition applicability/decision/mapping specification.** This is retained
material under-specification, not permission to invent scientific policy. Current
package prepares those decisions; no automatic approval or implementation handoff.

[Final RC proposal](STORY_INTELLIGENCE_SI_E02_2_1D_REQUIRED_CURRENT_FINAL_PROPOSAL.md),
[final oracles](STORY_INTELLIGENCE_SI_E02_2_1D_TEST_ORACLES.md),
[previous BC audit](STORY_INTELLIGENCE_SI_E02_2_1_RESUME_CONTRACT_GAPS.md) and
[implementation boundary](STORY_INTELLIGENCE_SI_E02_2_1B_IMPLEMENTATION_BOUNDARY.md)
remain separate from normative owner approvals.

## 2. Read-only interface and compatibility findings

| Existing interface / fields | What it establishes | What it does not establish |
| --- | --- | --- |
| records_v1.validate_si_record / si_record_ref / validate_si_record_ref | Closed shapes/local invariants and exact bytes/ref binding | Review applicability, science/rights/freshness truth or evaluation execution |
| resolver_v1.resolve_si_closure / resolve_si_record | Exact graph/hash/types/cycles, complete audit ancestry/Run snapshots | Current semantic selection or factual adequacy |
| provenance_v1.verify_si_provenance | Actual method/stage/version, revision ancestry, E1↔Run Rubric binding | Actual execution, human identity or scientific review |
| currentness_v1.check_si_currentness | CURRENT/STALE/INVALID relative to explicit active/head sets, G01/G02/F1-D1 | Data freshness, requiredness, score, scientific validity; public result has no dependency manifest/error paths |
| Risk.blocking/resolution/category/basis_refs | Explicit recorded blocker assertion and linked grounds | Natural-language inference of new blocker or generic reason-code mapping |
| ClaimCheck.claim_ref/state/evidence_refs/qualification | Recorded review for exact claim, known states/metadata | Automatic choice among several independent checks or literal factual wording adequacy |

Source-set proposal mirrors accepted typed currentness traversal without editing it;
proof-only graph checking avoids recursive freshness review while preserving ERef
boundary. One local projection/helper may be needed in a future new module; absence
of public S output is an implementation detail, not justification to change accepted
currentness or add schema fields. Differential tests must check equivalence of roles.

## 3. BC01–BC06 focused review

| BC | Existing normative basis / deterministic part | Remaining exact detail / independent oracle | Readiness |
| --- | --- | --- | --- |
| BC01 essential claim/review coverage | [original §3/5.2](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md), [R1 §3.2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md): unsupported/disputed central factual claim BLOCKED; missing ref INVALID | Which explicit claim set is evaluated; which exact checks are applicable for each claim; multiple checks and removed/qualified wording handling without parsing arbitrary Text. Oracle must pin exact graph/check set and expected reasons | Explicit cases implementable; full coverage needs Q1 below |
| BC02 risk/rights/capability | Open blocking Risk outranks score; essential rights/capability gaps retain existing blockers. Severity alone not new automatic policy | Category-to-existing-code/path mapping for arbitrary applicable Risk; exact human-verified fallback/mitigation prerequisites and treatment of non-essential Visual/source. No new risk inferred from prose | Needs Q2 for complete deterministic mapping |
| BC03 framing/current input | Missing exact refs/schema INVALID; expected context changed STALE; EVAL-F01–F03 close required-current conceptual choice | RC approval supplies detailed current-data predicate. Remaining framing/audience/channel adequacy cannot be inferred merely from nonempty Text or every UNKNOWN field being essential | Required-current branch after RC; other framing needs Q3 |
| BC04 research | EVAL-P02/P03 UNKNOWN/confidence/portfolio/exhaustive pair rules frozen. RC proposes ordinary/required freshness evidence | General noncentral evidence/locator adequacy must use declared applicability from Q1, not every source in audit bundle | RC + Q1 coverage; no new provider required |
| BC05 complete diagnostics | Findings codes/order frozen; RC D01–D16 precise. Existing R1 precedence/all reasons binding | Base claim/risk/framing code/path/message matrix and full literal T25 fixture; RC diagnostics do not define generic ethical/legal Risk mapping | Q1–Q3 mapping then independent fixture |
| BC06 pure API | No writer/Run/Report/Selection fabrication, request_id, clock, network, mutation; same exact inputs deterministic | Exact local signature/result and supported root roles are routine task specifications; no operation/wire change needed | No new material blocker found |

Existing ClaimCheck local validation intentionally does not decide cross-record
truth. Example of a remaining specification question: current Angle lists exact
CENTRAL factual q; supplied roots contain two independent checks of q with different
review states. There is no declared check-selection field in Angle; do not choose
latest/reviewer label or silently ignore one. A conservative combination rule can
be proposed, but must be explicitly selected if not entailed by the agreed input
role contract. This is not a claim that every contradictory check is ignorable:
known disputed central evidence must still block under the approved policy.

Another concrete gap is complete diagnostics for explicit ETHICAL blocking OPEN Risk
whose grounds are not a central unsupported claim, rights gap or capability failure.
There is no ETHICAL_BLOCKED in closed Code. TYPE would misrepresent a valid graph.
Choosing an existing generic code/class mapping is possible without wire changes,
but no exact matrix is approved here. Do not invent a new code or omit the blocker.

## 4. Smallest additional owner decision package (NOT APPROVED)

| Question | Exact decision requested | Narrow implementation impact |
| --- | --- | --- |
| Q1 Applicable claim/check/evidence set | Define authoritative supplied roots/typed roles for main claims vs freshness-proof-only claims; select a combination rule for all applicable independent checks of one exact claim. Give central/supporting, factual/interpretation/fictional, unreviewed/supported/disputed/unverified/qualified/removed table, including missing evidence/locator outcomes. No latest or prose truth inference | Claim/research base branches and BC01/BC04; not new SI record or Scientific Review automation |
| Q2 Explicit Risk/rights/capability matrix | Which supplied risks/visuals are applicable and which `blocking/resolution/category` combinations block; map each applicable condition to an existing code/path. Identify exact recorded human basis used for usable fallback/mitigation; no automatic source-license inference | BC02 and base diagnostics; no new authority or clearance service |
| Q3 Non-freshness framing predicates and full output matrix | Which present-but-UNKNOWN audience/channel/framing values mean NEEDS_INPUT versus research/allowed hypothesis; distinguish missing ref INVALID. Pin existing codes/paths and fixture messages for these cases | BC03/BC05 and complete T25; not UI/Topic Intent/persistence |

These are exact additional decisions/questions, not implementation decisions already
made by this audit. Existing unambiguous behavior should be reused without repeated
approval. String phrasing alone is routine, not material architecture. Proposed
answers must remain narrow: no generic policy record, hidden JSON flags, speculative
roles/credentials, new source fetching or imported scientific model.

If owner instead wants only the score/findings/required-current kernel, a **separate
explicit narrower task** can avoid unestablished base-classifier branches. Do not
silently call that a complete EVALUATE engine or claim T25 completed.

## 5. T25 exact scope and independence

Approved T25 is a requirement for priority plus preservation of all applicable
base reasons, not a ready literal classifier oracle. RC F02/F03 gives a real
NEEDS_INPUT premise; it does not establish all other base conditions.

One composed future fixture can independently stipulate: explicit essential-rights
blocker, UNDETERMINED required-current premise, UNKNOWN rating, UNRESOLVED duplicate
pair. Then logical primary BLOCKED and union of existing codes
[DUPLICATE_REVIEW_NEEDED,EVIDENCE_NEEDED,RIGHTS_BLOCKED] follow **provided** base
applicability/rights mapping is established. At least four distinct diagnostics must
survive (blocker,input,research,duplicate), despite shared EVIDENCE_NEEDED.

This demonstrates composition, not arbitrary-data classification. A complete T25
test still needs genuine content-addressed graph, frozen source/check/risk membership,
exact local inputs, independently authored canonical digests and complete expected
code/path/message tuples. BX in final oracle C14/C44 is explicitly proposed until Q2.
No assertion that a max score or a positive human premise makes claims true/licensed.
T27 remains future Request integration, non-executable for this pure scope.

## 6. RC review and later handoff gates

1. Owner reviews RC-P01–P06 as exact final proposal, including Q⊇R/E⊇Q, no stitching,
   source-set/proof boundary and private diagnostic messages; statuses remain NOT APPROVED now.
2. Close Q1–Q3 or explicitly bound a narrower component scope. Independently review
   final fixtures/oracles including updated C01–C34 and C35–C48 additions.
3. Only then a separate exact-base implementation task/allowlist. Keep accepted
   modules/schemas/vectors/contracts intact. Run focused and full suites with actual
   counts/exits; no test output exists for the new engine in this task.

**SI-PRODUCT-01** is preserved as a future projection requirement: editor-facing
explanations without hashes/SIRef/codes. Internal diagnostic IDs/refs are not product
content and must not be leaked via exception strings or copied into a ReviewPacket.
Presentation/privacy mapping is future scoped work, not a pure kernel prerequisite.

No SI-D03 persistence, Topic Intent, Scientific Review automation, ERef adapter for
ERef-free inputs, production handoff or Windows writer prerequisite added. Do not
strip relevant ERefs. Exact SI/1 field order/refs/hash/provenance, nine weights/formula,
R1 precedence, G01/G02/F1-D1, RU/UA wire `ru/uk`, CPU-only/licensing remain unchanged.

No new contradiction between approved requirements was established; retained
material **under-specification** Q1–Q3 prevents full-readiness claim after RC alone.
**Unit tests: NOT RUN — DOCS ONLY.** EVAL-P05 OPEN; PUBLISH_REVISION DISABLED;
partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
STOP; no code/tests/PR/merge/release/main changes or evaluator RESUME.
