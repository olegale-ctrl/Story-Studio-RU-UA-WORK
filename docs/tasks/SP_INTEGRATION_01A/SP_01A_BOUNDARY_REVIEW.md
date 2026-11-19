# Architecture boundary review

**SP-INTEGRATION-01a · 2026-11-19 · DOCS_ONLY · FREEZE_FOR_REVIEW, NOT OWNER_APPROVED.**

|Boundary|Source/test evidence|Verdict|Qualification limit|
|---|---|---|---|
|Execution|CLI main→prepare_intent/initial_readiness/run_gates; no build/submit/retry/queue owner; target tests patch forbidden direct build|VERIFIED|Actual submission/idempotency/status/recovery NOT_TESTED; missing API BLOCKED_CONTRACT|
|Authority|requested_attestations only; initial_readiness unknown; render vs release axes independent|VERIFIED|No attestation actor/authority/expiry/revocation checker; input assertions untrusted|
|Storage|observe_bytes raw digest, prepare_intent local SI digest, binding_matches equality only; no writes/publication|VERIFIED_WITH_LIMITATIONS|No PG binding/typed authority mapping; no immutable read snapshot, S3 or native OS qualification|
|Editorial|si_eligible separate; facts_reviewed independently checked; creative_review required as supplied assertion|VERIFIED_WITH_LIMITATIONS|No scientific review/editor identity or artistic-quality measurement is performed|
|Release|assess_release always false and adds authority/release blockers; final run_gates unknown/blocked|VERIFIED|No release executor/permission verifier; MP4 bytes do not establish decodability or publication rights|

|Adversarial condition|Current actual behavior / evidence|Status|Still needed|
|---|---|---|---|
|Stale permission after SHA/policy change|binding_matches detects unequal supplied snapshots; no real permission is accepted or used|VERIFIED_WITH_LIMITATIONS|Trusted currentness, expiry/revocation, exact authority scope are BLOCKED_CONTRACT|
|Input replacement/TOCTOU|read_local rejects visible symlink/reparse ancestors, caps bytes; plan/WAV rechecks are separate reads|VERIFIED_WITH_LIMITATIONS|No atomic check-to-use guarantee; hostile rename/hardlink/mount/FIFO races and Windows native behavior NOT_TESTED; trusted broker required|
|Incomplete results|FV23 final missing plan/project/MP4 →BLOCKED; technical_pass unknown|VERIFIED|Real interrupted-render/publication crash tests NOT_TESTED, missing runtime|
|Repeated intent acceptance|test_repeat_intent_deterministic_not_submitted repeats local digest, IDs remain empty|VERIFIED_WITH_LIMITATIONS|Actual duplicate acceptance/effect suppression NOT_TESTED, no JobStore|
|JobStore vs local report divergence|--wait returns BLOCKED_JOBSTORE_CONTRACT; jobs schema empty observations, no local authoritative mirror|BLOCKED_CONTRACT|No mismatch injected into nonexistent store; qualified observer/versioned receipts needed|
|Implicit media replacement|Fallback blocker for equivalent/degraded/placeholder; D/final no generated background fallback|VERIFIED_WITH_LIMITATIONS|Actual approved equivalence/loss/rights validation NOT_TESTED; no substitution executed|
|Missing/corrupted/unavailable artifact|Existing target tests cover missing WAV, corrupt/truncated WAV, unsafe paths and missing plan; exceptions fail closed for these cases|VERIFIED_WITH_LIMITATIONS|Image/video decode, hostile filesystems, source-to-project-to-render correspondence NOT_TESTED|
|All asserted axes true|FV24 returns necessary=true but release=false/BLOCKED_CONTRACT|VERIFIED|G04 is a diagnostic API-scope gap, not evidence authentication|

No time-of-check/time-of-use claim is upgraded by successful Linux unit tests. Repeated reads can observe different bytes, and checking paths before open is not a qualified OS containment boundary. File existence, sample header checks and supplied SHA values cannot prove rights, intended scientific visuals, originality, attribution or source integrity throughout execution.

The topic-to-film product still needs accountable answers to topic value, script/source evidence, scientific claims, required visuals, editorial risks, decision maker and exact authorized plan. This review cannot substitute schemas or technical codecs for those answers. SyntheticRenderPermitV1 stays confined to the original registered D1 scenario; no use by this CLI or docs freeze.

Rejected inferences: schema-valid→semantic-valid; digest-equal→permission-current; SI eligible→facts reviewed; MP4 exists→rights cleared; job state completed→artifact published; draft→execution permitted; necessary conditions→release authorization. No protected storage/user-file deletion or replacement occurs in current SP diagnostics.
