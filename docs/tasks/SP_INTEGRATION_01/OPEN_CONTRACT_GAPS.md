# Open contract gaps and owner decisions

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

No additional confirmation is needed to prepare this safe partial scope. The following decisions are required before corresponding future integration, not permission to continue implementation automatically.

|ID|Exact missing decision/API|Recommendation (PROPOSAL)|Current fail-closed behavior|
|---|---|---|---|
|SP-OD01|Approve and supply implemented Dispatcher/JobStore API, exact commit/version, supported types, idempotency/observation/publication receipts; decide general DAG extension vs existing video jobs|Reuse single authoritative controller; qualify seven types separately; preserve MVP08B guarantees|BLOCKED_DISPATCHER_CONTRACT / BLOCKED_JOBSTORE_CONTRACT|
|SP-OD02|Approve authoritative identities and PG binding mapping for script/plan/project/materials/policy; native storage broker and stale-snapshot semantics|Reuse accepted typed refs/PG hash domains; local digest remains diagnostic|BLOCKED_AUTHORITY_CONTRACT / no grant applicability verifier|
|SP-OD03|Attestation actors, evidence, authority/trust source, scope, expiry, revocation and clock checks for facts/rights/render/release|Independent attestations with exact snapshots, no CLI booleans as grants|All readiness axes initially unknown|
|SP-OD04|Class A production editorial/scientific selection policy and accountable human editor|Draft-first; require claim/source review and declared visual requirements|CLASS_A_PRODUCTION_POLICY_REQUIRED|
|SP-OD05|Qualified equivalent/degraded/placeholder policies and measurable compatibility/loss; degraded final-release admissibility|No automatic substitution; placeholder only explicitly permitted diagnostics|Fallback-specific blockers; no release|
|SP-OD06|Approved workload/runtime/model/provider/RAM/disk/OS qualification profile and bounded worker resource policy|CPU-first; optional providers never enabled by installation alone|BLOCKED_WORKLOAD_QUALIFICATION|
|SP-OD07|Final technical gate profile: image/clip decode, expected dimensions/codecs/subtitles/durations, artifact completeness, immutable input/result binding|Existing validators plus separately qualified decoder worker and evidence|Final technical_pass unknown; asset/render validation blocked|
|SP-OD08|Storage publication/recovery receipts; Library import idempotency; stable project identity/CAS/readback; S3 qualification if later needed|Reuse approved storage/Dispatcher; no CLI recovery or mirror authority|BLOCKED_STORAGE_CONTRACT / BLOCKED_RESULT_PUBLICATION_CONTRACT|
|SP-OD09|Final release contract/destination authority and independent human creative suitability|Exact finished-film version/use scope plus approved release verifier; separate from render grant|release_allowed always false; no publication implementation|
|SP-OD10|Approve SP/1 transport proposal or supply authoritative replacement, including plan dialect/schema version and declared-root mapping|Review seven schemas and semantic rules before persistent interchange|Prepared stdout diagnostics only|

MVP08B.1 OD01–OD08 and Asset Library P1 issues remain open; none resolved implicitly here. Existing D01–D08 owner record unchanged: zero budget, no live requests/payments/subscriptions, no browser automation, no unqualified provider/model/region changes, unknown rights not clearance. G3.2.1, production permissions/storage, main/merge/release/CI remain outside scope. No reinterpretation of SyntheticRenderPermitV1.

Recommended sequence: independent audit of this partial packet → owner decisions/SP schema mapping → explicitly authorized single Dispatcher implementation/qualification → worker technical/storage/hardware qualification → synthetic integration/failure injection → platform qualification → separately authorized bounded usage. No next stage is started automatically.
