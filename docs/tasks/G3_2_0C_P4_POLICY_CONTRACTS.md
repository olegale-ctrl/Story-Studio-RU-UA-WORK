# P4 — Policy Contracts: pure projections versus trusted predicates

**DECISION_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0c; 2026-11-17 (Europe/Kyiv).
Base `0d6d9076ab535c1b258206beb4e4fe9c005e79e1`, tree `e55c00d0e7a95218e0978dd9677172608395ff5f`.

Primary OP-10/11/13/14/18/24/25, exactly seven MIXED parameters. Each has a pure data/comparison subset and separate trusted realization. All seven whole-parameter choices remain unresolved; partial schema review does not provide true clock/rights/reviewer/provider/output evidence. Exact source/alternatives/owner questions in [dossier](G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md).

## 1. OP-10 — timestamps are data, not clock authority

**Pure proposal:** exact integer Instant, domain0…253402300799 epoch seconds, no bool/float/timezone-string coercion. Comparisons deterministic on supplied values and exact profile/version. TimeWitness/observation reference includes chosen time policy/ref and uncertainty representation **only after its schema is separately selected**; a caller-provided timestamp/signature field is not verified time.

**Operational dependency:** trusted clock/source, rollback detection, uncertainty and authenticated freshness policy. No such source connected or qualified. Unknown/unavailable clock means operational deny, not assume zero uncertainty or machine-local wall clock trusted.

**Alternatives:** whole-second bounded domain versus explicit higher-precision version, never silent conversion. Domain/precision change affects canonical bytes/references and boundary fixtures. Related V060/V061/V062/V063/V069, P03-06. Owner can choose pure range without choosing time provider; whole OP remains OPEN.

## 2. OP-11 — interval algebra versus admission window

**Pure proposal:** all applicable windows explicit, `[from,until)`; require from<until and effective intersection nonempty. Effective start=max(starts), end=min(ends). now==end expired. No union of convenient approval/license windows, no auto extension, no timestamps as implicit grant.

If a separately approved uncertainty model supplies `[t-u,t+u]`, a conservative predicate requires the entire considered interval inside the authorized window, rather than picking the optimistic endpoint. This is a **formula proposal**, not approval of u, TTL, render estimate or actual clock. A planned completion margin/expected maximum duration must also fit; its number needs OP-18/20 evidence. Real expiry/revocation during run follows P5, not a pure comparison alone.

**Operational dependency:** actual trusted now, monitoring/cancellation/final-commit check and profile duration knowledge. **Alternatives:** narrow per-attempt lease versus explicit reviewed batch window; no auto renewal. Negative tombstone permanence OP-28 is not bounded by expiry of a prior positive grant. V063/P04-03/P04-06. Pure schema/algebra may be reviewed first, TTL/margins stay OPEN.

## 3. OP-13 — rights coverage versus actual legal permission

**Pure fields/invariants proposal:** exact material ByteRefs, asset kind/provenance/license-copy references, requested UseScope, required layers per selected policy, reviewer/policy/version/evidence refs, commercial/territory/channel/time/adaptation/attribution restrictions. Manifest closure must cover every actual use in every scene; no caller-chosen subset. Compare requested use against **intersection** of all required layers, exact bytes and revisions, no silent missing layer/default/worldwide permission.

**Operational dependency:** actual rights holder/source/license authenticity, competent reviewer/jurisdiction applicability, consent, current dispute/revocation state and authenticated policy. A formal layer record/CONFIRMED digest/VERIFIED_EXTERNALLY reported flag does not supply this. Public-domain/ownership/generated claims require basis, not automatic exemptions. Identity alone does not establish legal competence.

**Alternatives:** a narrow initial scope excluding external music/voices/stock versus explicitly reviewed real licensed assets. Narrow scope still needs actual lawful material set; synthetic permit does not license production. Any change to material/use/attribution can invalidate rights review and affected human review. Related P03-01/P03-03/P03-04/P03-05/P03-07 and PRODUCT-02. Policy applicability/roles/jurisdictions remain OPEN.

## 4. OP-14 — reviewer schema versus human competence/independence

**Pure proposal:** ActorRef, authority PolicyRef, review_kind, exact SubjectKey, decision/declarations/session/history links, reason, validity and evidence refs. Equality/coverage/ref validation deterministic. A1–A14/O1–O10 preserved: actor display name not identity; grants per gate/decision; HANDOFF editorial-only/no render/export permission. Unknown role/policy/session not accepted via fallback.

**Operational dependency:** actual OS-derived identity, valid authority, review session showing exact materials, explicit human action, competence/independence/conflict assessment. No implicit self-approval or current-user admin. LLM assessment does not become human approval. A person may hold multiple roles only if an explicitly reviewed policy permits it; this dossier assigns no person or powers.

**Alternatives:** distinct editor/scientific/rights roles versus controlled dual-role policy with disclosed conflicts and independent evidence requirements. Product consequence is small-team friction versus actual scrutiny. Technical identity authentication is necessary but not proof of scientific expertise or substantive review. P02-02/P02-03/P02-08/PRODUCT-06. Review policy/version changes require explicit scope/revalidation, not rewriting history.

## 5. OP-18 — output profiles versus actual media quality

**Pure proposal:** closed versioned expected-output profile: exact locale/output IDs/kinds/required flags, dimension/fps/codec/subtitle/attribution requirements, plan/toolchain/executor bindings, inspection evidence schema/version. No arbitrary command or caller executable/filename override. Exact required set, uniqueness and comparisons to supplied observed metadata are deterministic; no successful batch from RU-only result when UK required.

**Operational dependency:** actual binary/config/font/runtime identity, actual produced bytes/stream/subtitle/frame checks and trustworthy completion evidence. Real RU/UK readability, scientific/visual meaning, language alignment and playback require appropriate human/host observations. D1 brightness/JSON reproducibility is not full production quality/rights qualification.

**Alternatives:** one exact two-locale batch versus independently scoped per-locale authorizations; never silently treat partial batch as complete. Numeric thresholds, permitted codec/font/runtime versions, duration estimates/output-byte budgets remain OPEN. P04-02/P04-08/P05-01/P05-02/P05-06. New output profile changes plan/candidate binding under X04 and relevant reapproval policy.

## 6. OP-24 — policy-role typing versus policy registry authority

**Pure recommendation:** role-aware exact PolicyRef interpretation. Root content/use, actor authority, asset rights, render issuer, executor and output profile are distinct slots. Within each slot compare exact id/version/hash and allowed schema/profile; no caller-supplied default/latest policy. A single policy object is not automatically valid in all roles.

Two encoding alternatives:

1. **Slot-derived role** from closed contract field/profile; preserves current proposed PolicyRef shape but requires explicit role-to-profile mapping.
2. Explicit role-tagged reference type in a new version, with no automatic migration of old refs.

Either needs a selected compatibility/namespace rule. Current ambiguously named policy fields must be clarified **before future implementation**, not renamed silently here. SubjectKey root policy need not equal rights/authority policy bytes; what must match is the role-specific declared binding, complete selected policy map and cross-subject scope. Unexpected interchange is a reference/scope failure under chosen profile, not permission.

**Operational dependency:** authenticated current registry, valid actual grants, policy revocation/time/history and anti-rollback. A role label inside untrusted JSON does not prove it. P02-01/P03-08/P04-03. Primary P4 OP-24 depends on P2 identity/binding, not vice versa; P2 secondary pure coverage does not duplicate primary ownership or create P1/provider dependency.

## 7. OP-25 — full snapshot contract versus actual recomputation

**Pure proposal:** bind exact original raw editor input, parsed-value hash under unchanged G2 wire rules, source/code/runtime identity, supplied context, full evaluator result and full Projection association, exact plans/assets/dossier/limitations and redacted-view refs. No substitution of one hash namespace for another, no detached result blessed by `verified=true`.

G2 export evaluation diagnostics are code-only. Missing field_path/input_ref/message cannot be reconstructed from guesses or manufactured from a previous card. Proposed future collector must recompute full result on exact pinned original inputs and preserve PD-01 Projection re-verification; if changed context/result means a different snapshot, old approval is not silently repaired/replaced.

**Operational dependency:** actual original bytes/pinned runtime availability, deterministic full evaluator execution, trusted current-context observation and private immutable collection. None is executed in this docs task. Supplied full result can be checked for structure/binding in future pure tests, but a JSON CURRENT label is not trusted latest state.

**Alternatives:** new collector preserving G2 interfaces versus diagnostics-only deny when original/runtime/context absent. No fallback to redacted-export-as-authoritative-full-result. P01-02/P01-04/P01-08. New collector/snapshot identity and migration policy explicit; G1/G2/G3.1 implementations untouched.

## 8. Product quality is not a security or legal shortcut

| Product question | Proposed evidence/review responsibility | What is not a substitute |
|---|---|---|
| Стоит ли снимать тему и почему? | Editor evaluates audience need, why_film, angle, novelty grounds and actual constraints | High score, long rationale or completed JSON form |
| Какие источники поддерживают тезисы? | Exact claim→fragment→source/locator/date mapping, contrary evidence, uncertainty | Citation count or URL list without relation |
| Какие научные/редакционные риски? | Identify central factual/hypothesis claims, competent scientific review where required, unresolved blocking risks/disclosures | LLM confidence, identity role string or fake research conclusion |
| Какие варианты подачи? | Human comparison of angle/hooks/scene meaning with evidence/factual limits | Gate fabricates story/translation or changes claims to pass |
| Какие визуальные доказательства нужны? | Required VisualNeed→scene→actual asset/feasibility/rights mapping, meaning reviewed | Random gradient, synthetic footage or licensed-but-irrelevant image |
| Кто принял решение? | Exact bound human decision/role/session/history, actual authority checked separately | actor display name, auto checkbox or synthetic permit |
| Что отправляется в производство? | Exact plan/assets/use/tools/profile with applicable reviews and later separate authorization | Formally valid schema, CONTENT_COMPLETE or preview permission=false turned true |

Product findings are substantive criteria; they do **not** waive rights, identity, immutable inputs or operational gates. A scientifically sound idea may still lack image/music/voice rights. A licensed asset may illustrate a false central claim. Fiction may honestly omit scientific support for fictional content but not hide real assertions or missing disclosures. Unresolved actual human/product policies remain OPEN, not pure automatic truth functions.

## 9. Approval separation and STOP

Owner may separately review pure field/enum/version/comparison projections without connecting clock/registry/reviewer/renderer. Whole MIXED parameters remain unresolved until their policy/trust/real-evidence choices are defined. All proposed questions/dependencies/statuses remain in dossier, no actual authority exercised. No validators/recomputation/render/license/identity/integration tests run here. **STOP for independent review and owner decision.**
