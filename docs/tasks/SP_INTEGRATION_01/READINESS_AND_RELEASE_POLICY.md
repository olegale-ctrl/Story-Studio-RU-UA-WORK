# Readiness and release policy

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

Readiness values are exact strings `unknown|false|true`. `initial_readiness` sets all axes and SI eligibility unknown regardless of user flags. The following assignments are PROPOSED responsibilities, not newly granted roles.

|Axis|Source and proposed owner|Required evidence|Change/invalidation rule|
|---|---|---|---|
|script_ready|Editorial review; accountable editor|Exact script/plan identity+revision+hash, review disposition, actor and authority scope|Content/brief/policy change requires review; draft generation alone unknown|
|facts_reviewed|Scientific/fact review; qualified reviewer|Claim→source→verification mapping, unresolved claims, dates and provenance|Claim/source changes invalidate affected review; SI eligibility cannot assign true|
|rights_cleared|Rights review; rights authority|Intended use, source/voice/music/image licenses, territory/time/attribution/watermark constraints and proof|Any input/use/territory/expiry change recheck; technical PASS never clears rights|
|authorized_for_render|Approved execution authority verifier|Exact job/render plan, IDs/revisions/all input raw hashes, operation, policy, valid window, revocation state|Changed plan/input/policy/scope or revoked/expired grant invalidates applicability|
|technical_pass|Qualified technical worker|Bound output hashes, complete gates, tool/runtime versions and decode results|Any output or expected profile change requires revalidation; intermediate PASS insufficient|
|authorized_for_release|Independent release authority verifier|Exact finished film version/hash, permitted release destination/use, constraints, current grant|Render grant not release grant; changed film/use/expiry/revocation invalidates|

`si_eligible` is a separate SI policy observation, not truth. `fallback_class`, `evidence_refs`, `artifact_bindings`, `policy_version` and blockers travel independently. Unknown never equals true. A user CLI flag is only a request for attestation processing. Failed verification would produce false/denial; unavailable verification remains unknown/blocker. No current function promotes these axes from flags, MP4 presence or supplied evidence labels.

`assess_release(mode,readiness,bindings_current,creative_review)` checks necessary conditions deterministically, without I/O: production, all six axes true, matching diagnostic policy, no unresolved blockers, no prohibited fallback, confirmed bindings, human creative review. Booleans are rejected. `necessary_conditions_satisfied` is an assessment of supplied assertions only; it is NOT `release_allowed`. Even all-true supplied assertions produce `release_allowed=false`, BLOCKED_ATTESTATION_VERIFIER and BLOCKED_RELEASE_CONTRACT. Equivalent fallback also remains blocked without a qualified compatibility verifier. Degraded release qualification is open; current release diagnostic denies it conservatively.

Future permitted execution needs verified authoritative identities/revisions/raw hashes, approved attestation and grant applicability/revocation/clock semantics, qualified resource/storage/OS boundaries, exact worker job types, result evidence and independent owner approval. Final publication additionally needs approved destination/use, release authority, human creative suitability and final release contract. No current mode, including production, implies these conditions are met.

Creative suitability must answer why this topic merits a film, what evidence supports script claims, which claims need scientific review, mandatory visuals, remaining editorial risks, accountable editor and the exact production scope. Codecs/duration/SI score cannot answer those questions. A formal schema does not replace that decision.
