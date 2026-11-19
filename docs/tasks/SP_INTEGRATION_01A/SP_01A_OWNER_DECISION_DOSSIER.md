# Minimal owner decision dossier

**SP-INTEGRATION-01a · 2026-11-19 · DOCS_ONLY · FREEZE_FOR_REVIEW, NOT OWNER_APPROVED.**

**Every recommendation below remains PROPOSAL — NO OWNER CHOICE RECORDED.** The task-supplied preliminary independent audit is not approval of these choices. No need to resolve production policy simply to review diagnostics.

|Priority|Original ID|Decision scope now|
|---|---|---|
|P0|SP-OD10|Whether to approve a limited, explicitly non-authorizing diagnostic contract with G01–G04 disclosed; never schema-only interchange|
|P1|SP-OD01|Implemented Dispatcher/JobStore API, exact version, registered stages, specialized bridge vs DAG decision|
|P1|SP-OD02|Identity/hash/typed-reference mapping, snapshot roots and binding applicability|
|P1|SP-OD03|Attestation authority/evidence/currentness/revocation for any actual execution|
|P2|SP-OD04|Class A production editorial/scientific policy and accountable editor|
|P1|SP-OD05|Fallback compatibility/loss/diagnostic permissions before any execution; production/degraded release extension stays P2|
|P1|SP-OD06|Qualified runtime/model/workload/resource profile before executing jobs; production platform scope stays P2|
|P1|SP-OD07|Worker technical validation before render-result claims; production result profile/qualification stays P2|
|P1|SP-OD08|Local publication/ingestion/save/recovery receipts before integration; S3/production durability remains P2|
|P2|SP-OD09|Independent finished-film release authority, destination/use scope and human creative approval|

## P0 — SP-OD10: bounded diagnostic semantics

Exact question: “Approve the observed SP/1-PROPOSAL behavior only as a local diagnostic interface, with false release, empty accepted jobs, required runtime semantic validation and G01–G04 limitations, or defer approval pending a separately scoped reconciliation?”

A: explicitly approve only that limited diagnostic reading, excluding strict interchange/JobStore/PG use. B: defer all contract approval and separately authorize a future schema/semantic reconciliation. C: leave this frozen snapshot as a proposal without approval or new work. Recommendation A if owner wants stable local diagnostics now; B if exact schema/runtime equivalence is a prerequisite. Rationale: useful preparation needs no execution authority. Risks: downstream readers may misread schema validity as acceptance, particularly terminal-LF hashes and route/digest inconsistencies. Dependencies: review this packet and explicitly acknowledge G01–G04. Still prohibited: code/schema changes without a new task, queue submission, trusting digest as identity, live APIs, production/release. Required post-decision tests: rerun exact vectors and source-hash checks; if B later authorizes changes, add cross-field/digest/terminal-LF/path/blank-text semantic tests and versioning compatibility tests. No option selected here.

## P1 — SP-OD01: one actual execution API

Exact question: “Which exact implemented/approved Dispatcher and JobStore revision is authoritative, and will SP use a constrained video-job bridge or separately approved generic DAG extension?” A: supply/qualify existing specialized video API and scope SP to supported operations. B: separately design/approve extension for the seven proposed stage types and dependencies. Recommendation A first where actual APIs suffice; no fictitious API exists today. Rationale: preserve one owner of durable effects. Risks: a general DAG expands scheduling/security/recovery guarantees; bridge may not support routes A/B. Dependencies: exact .2 artifacts, approval record, public API/errors/receipts, idempotency/observer tests. Prohibited: second queue/store/retry/locks, inferring supported types. Tests: duplicate submissions, immutable request scope, accepted≠completed, authoritative status sequence, bounded observer timeout and crash/publication receipts.

## P1 — SP-OD02: identity and hash mapping

Exact question: “Which existing typed identities/revisions, byte snapshots and hash domains bind SP inputs to authorized jobs?” A: explicit adapter to accepted identities and distinct SI/PG/raw/08B domains with a trusted snapshot/root broker. B: retain stdout-only diagnostics until authoritative mapping exists. Recommendation A only as separately approved design, B as current operational default. Rationale: local content equality is not scoped identity. Risks: accidental hash aliasing, mutable paths, stale policy, unqualified storage. Dependencies: OD01/03/08, G3 accepted pure rules and unresolved operational boundaries. Prohibited: relabeling SP digest as PG binding/job key, implicit latest asset. Tests: changed input/policy/revision, wrong type/namespace, mismatched byte length/hash, stale roots and malicious path substitutions.

## P1 — SP-OD03: attestation and execution authority

Exact question: “Who may attest facts/rights and authorize which exact render scope, with what evidence, validity window, revocation/currentness and trusted verification source?” A: separately approve scoped authority/verification contract with independent attestations. B: keep requested flags as unverified intentions and block effects. Recommendation A for future integration, B until qualified. Rationale: user flags cannot establish authority. Risks: forged, revoked, replayed or stale claims; role scope confused with cryptographic correctness. Dependencies: OD02 and qualified trust/clock/storage sources. Prohibited: new self-designed crypto, blanket grants, production implied by synthetic permission. Tests: wrong actor/scope, missing evidence, expiry/revocation, replay, changed materials and grant mix-up; render grant never release grant.

## P1 — SP-OD05: fallback before execution

Exact question: “What qualified evidence establishes equivalent media, and which explicit policy permits a recorded degradation or diagnostic placeholder?” A: retain all current blockers until measured compatibility/loss criteria and bounded authorizations are approved. B: separately approve a constrained synthetic-diagnostic-only fallback policy; no production or release expansion. Recommendation A for general flow, B only if specifically needed. Rationale: silent substitution can change scientific/visual meaning. Risks: materially false visuals, wrong duration/locale/rights, loss hidden by technical PASS. Dependencies: OD03/07; production use additionally OD04/09. Prohibited: automatic equivalent, production placeholder, degraded release without separate policy. Tests: missing compatibility evidence, loss record, unauthorized scope, changed replacement SHA, locale/timing/rights mismatch.

## P1 — SP-OD06: workload qualification

Exact question: “Which exact runtime/model/provider/platform profile and resource bounds qualify each supported job?” A: separately qualified CPU-first local profile with model/version/hash and RAM/disk/runtime checks. B: keep all execution blocked; installed models only inventory. Recommendation A when needed, B now. Rationale: installed or sufficiently large hardware is not qualified. Risks: exhaustion, unbounded runtime, optional provider silently enabled. Dependencies: OD01/03 and platform proof. Prohibited: heavy benchmark/model installation/pagefile changes/process killing/live provider activation from this decision. Tests: insufficient/unknown RAM/disk, wrong runtime/model hash, unqualified provider, deadline/resource enforcement; Windows requires real native runs later.

## P1 — SP-OD07: result validation

Exact question: “What approved worker profile proves exact declared inputs and complete required audio/image/clip/project/MP4 outputs?” A: reuse existing validators behind separately qualified bounded workers, full decode and exact result/tool/exit-code evidence. B: retain only current intermediate read-only observations and technical unknown. Recommendation A as future scope, B currently. Rationale: header/path/MP4 existence is insufficient. Risks: partial decode, wrong duration/codecs/subtitles, stale project, false artistic/scientific inference. Dependencies: OD01/02/06/08. Prohibited: technical true from intermediate status or release from codec success. Tests: missing/corrupt/truncated media, unsupported format, full decode error, wrong profile/output hash, incomplete evidence and interruption.

## P1 — SP-OD08: durable local outcomes

Exact question: “Which approved publication, Library import, saved-project CAS/readback and recovery receipts close cross-resource ambiguity?” A: separately qualified local protocol under the existing single Dispatcher, including idempotent import receipt and stable project identity. B: block autonomous completion and use explicitly scoped manual reconciliation until those APIs exist. Recommendation A for future automation, B as fail-closed default. Rationale: Library links/catalog status and in-memory success do not prove saved-film state. Risks: duplicate imports, stale overwrite, orphaned objects, publication after unknown commit. Dependencies: OD01/02/03/07 and MVP08B OD02/03/07/08. Prohibited: private CLI recovery, rmtree/user-file cleanup, claiming S3 qualification. Tests: lost ACK, duplicate import, crash between file/DB/editor/save/publication, current-vs-historical receipts and no stale overwrite. Production S3/OS qualification remains P2.

## P2 — SP-OD04: Class A production editorial policy

Exact question: “Who decides a topic warrants production, based on what claim/source/scientific review, mandatory visuals and explicit remaining risks?” A: approve a separately defined accountable human editorial policy and exact reviewed brief. B: leave topic route draft-only and production blocked. Recommendation B until real editorial policy/authority is qualified. Risks: syntactically valid but unsupported or misleading films. Dependencies: OD02/03/05/07/09. Prohibited: SI score as fact-check or default production authorization. Tests: unsupported claims, unresolved scientific review, missing required visuals/editor identity and stale brief; human suitability cannot be inferred from MP4.

## P2 — SP-OD09: independent release

Exact question: “Which independent verifier may authorize release of which finished film hash/version, to which destination/use, under current rights and human creative approval?” A: separately approve and implement that verifier and operational release contract after prerequisites. B: keep release_allowed false indefinitely. Recommendation B now; A requires a new explicit implementation/qualification task. Risks: publication of wrong version, expired rights, conflating render with release. Dependencies: every applicable P1 decision, OD04 where needed, qualified production OS/storage/clock/rights. Prohibited: current mode=production or all-true assertions issuing a grant, automatic publication, merge/release from this dossier. Tests: render-only grant, wrong output/destination/scope, revoked release, changed film, creative rejection, expired rights and incomplete evidence.

P0 approval would not choose P1/P2 alternatives. P1 approval would not authorize production/live requests/payments; unchanged D01–D08 and separate implementation/qualification gates still apply. No SP-INTEGRATION-02 is started automatically.
