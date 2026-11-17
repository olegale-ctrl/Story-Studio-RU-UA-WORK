# Typed reference families — A/B/C alternatives

**DOCS_ONLY. F-D01 and every H-D decision: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0h; 2026-11-17 (Europe/Kyiv). Analysis only; no adoption, implementation, merge or production authority.

[PROPOSED] F-D01 is not approved; historical preference for closed families in C/F is not adoption. Sources: [C P2 reference/schema](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§1–4; [F pure choices](G3_2_0F_PURE_CONTRACT_DECISION_OPTIONS.md) CM-071; [F dossier](G3_2_0F_OWNER_DECISION_DOSSIER.md) F-D01/04–08; [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X03/X04. Every option below inherits the fixed approved constraints but remains a new unselected research alternative.

| Dimension | Option A — closed exact typed family | Option B — explicit versioned adapters | Option C — deferred admission |
|---|---|---|---|
| Proposed rule | Closed version/family/namespace vocabulary; exact key, metadata, observed byte interpretation separately; no inferred edges/latest | Explicit input/output family/version adapters, their own provenance/failure/work policies; no implicit migration | Keep all reference family and closure admission OPEN; record only existing approved constraints |
| Security/correctness | Small explicit surface, but wrong key/equivalence choice still permits conflict bugs | Transformation may hide role/identity/scope changes; must prove exact before/after correspondence | Avoids adopting unsafe assumptions; no full closure capability claimed |
| Implementation complexity | Future medium registry/header/domain matrix; no implementation now | Future high adapter/compatibility/lineage/resource matrix; none authorised | Lowest adoption risk, document maintenance only; future work deferred |
| Schema evolution | New explicit family/version decision, unsupported versions not auto accepted | Every adapter version separately reviewed, no heuristic unknown-version recovery | Historical schemas remain proposals, no new supported-version set |
| Historical compatibility | Source declarations are starting evidence, not an approved wire list; PG canonical vs raw artifact question must be settled | Must name source/target compatibility exactly, preserve raw provenance; old refs/approvals not automatically accepted | Does not rewrite or retroactively invalidate old documentary/synthetic evidence |
| Aliasing/conflicts | Registry key must not include mutable expected hash so same-ID changes vanish as new versions | Adapter could remap IDs/namespaces and conceal conflict; reverse/provenance mapping needed | Conflict detection not newly claimed; unresolved examples retain EXPECTED_RESULT_OPEN |
| Cache/dedup | Candidate integrity reuse only after type/namespace/header/equivalence decisions; physical cost not free | Input/output caches distinct; transformed outputs do not inherit original authority | No new cache or resolver policy; repeated-work implications stay OPEN |
| Graph traversal | Closed declared typed edges; opaque bytes do not self-declare links; exact order still separate | Only explicit versioned expansion profiles may add edges; input+output work must later be accounted | No new graph traversal/admission authorised |
| Migration/reapproval | New identity/version does not transfer human review/rights; X04 change propagation fixed | Deterministic transformation not review continuity; new subject/affected review policy separately needed | No migration or old-subject equivalence; approved X04 direction still required for any future gate |
| Future evidence | Same key/metadata/bytes triad, PG wire equivalence, raw conflict, missing/header/revision/version/role cases | Above plus adapter before/after provenance, unsupported transform, scope widening, work amplification | Evidence inventory and unresolved-decision checklist; no fictional successful closure |
| Owner decisions | H-D01/02/03/04/05 and later edge/dedup/closure scope; no automatic full OP-09 | Same base questions plus H-D08 adapter/compatibility/reapproval scope | Explicitly retain F-D01/OP-09 admission OPEN; identify what evidence would reopen it |
| Trusted infrastructure | Pure tuple/byte rules can be discussed without providers; actual object custody/currentness remains OPERATIONAL_EVIDENCE_REQUIRED | Same plus actual adapter execution/custody/version integrity; no signing-key-as-trust shortcut | Real production claims remain blocked; no infrastructure is qualified by deferral |
| Explicitly unapproved | Concrete key schema/namespace bindings, PG wire policy, family target preimages, edge/limit/admission/migration, resolver/cache | All concrete adapters, schemas, continuity and operational trust | Any new identity/registry/edge/admission policy; existing approved rules unchanged |

## Recommendation, independently justified

**RECOMMENDATION — NOT APPROVED:** use Option A only as a staged documentary candidate, starting with separation of registry key/integrity metadata/observed bytes. Reason: closed explicit type/namespace boundaries expose hash-as-version and cross-role alias errors with fewer transformation paths than B. This recommendation does not adopt a family/key/version or change F-D01's status. PG canonical equivalence and unpinned policy/head target recipes remain real unresolved questions, not solved by selecting the letter A.

[PROPOSED] Option B is rational only when a concrete legacy/evolution need outweighs its larger provenance/review/work surface and owner explicitly commissions that separate design. Never silently choose B as fallback on an unsupported schema. Option C is the safe alternative if owner cannot yet decide even the narrow candidate direction or pin namespace/preimage boundaries; lack of admission is honest, not a failing test to work around.

## Minimum safe adoption boundary that could be considered later

[PROPOSED] Ask H-D01 alone: may A's **principle of explicit typed separation** be developed into later owner-reviewable key/preimage questions, without adopting any reference family, OP-09 admission, resolver, edge profile, resource cap or migration? Accept/reject/defer should be explicit. H-D02 onward make concrete independent questions; no approval in this dossier and no next-stage execution implied.

[APPROVED] X03 separation, X04 mandatory exact plan binding, P1 byte/error/result rules and P1-DIAG-01's narrow root private ordering are not selectable alternatives. Any option contradicting those is outside scope. [APPROVED_LIMITED_SCOPE] G root/report directions do not widen reference or runtime authority. **STOP for independent review and owner decision.**
