# I-Q02 and I-Q03 — independently answerable owner proposals

**OWNER_AUTHORIZED_DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. Implementation FORBIDDEN.**

SI-INTEGRATION-G3.2.0j; 2026-11-17 (Europe/Kyiv). I-Q02 and I-Q03: **PROPOSED — NOT APPROVED**. H-D02 and full F-D01: **NOT APPROVED**.

## I-Q02 — representation and equality

**PROPOSED — NOT APPROVED.** Existing prerequisite I-Q01 is preserved; its A alternative is now approved only as limited documentary separation direction. No concrete key is selected.

| Alternative | Representation principle | Comparison ambiguity | Required evidence | Dependencies | Security consequences | Migration consequences | Remains unapproved |
|---|---|---|---|---|---|---|---|
| J-R1 exact opaque | Explicit opaque identifier; exact equality independently specified | Bytes versus decoded scalar text; case, Unicode, controls and whitespace | Future J-C001–019/032–036 under chosen convention | I-Q01; H-D02; OP-09/22 | Exposes rather than silently normalizes differences; exact match still unauthenticated | No silent normalization/namespace retrofit; continuity separately decided | Encoding, equality, admissibility, tuple, binding implementation, family admission |
| J-R2 structured/versioned | Explicit descriptor principle only | Component equality, duplicates, unknown versions and defaults | Future duplicate/version/shape/comparison evidence after separate specification | I-Q01; H-D02; OP-07/09/22 | Structure can expose scope but create ambiguous comparison surface | Every future version/bridge separately reviewed | Actual fields, schema/version, parser, authority and implementation |
| J-R3 qualified global | Global identity only with qualified scope/issuance/uniqueness | URI/UUID spelling, collisions, issuer/type qualification | Future scheme comparison plus actual independent uniqueness/authority evidence | I-Q01; H-D02/10; future I-Q03 authority model separately | Global appearance can conceal issuer spoofing; equality is not legitimacy | Local IDs never auto-global; remapping needs provenance/review policy | Scheme, encoding, issuer/root, tuple and admission |
| J-R4 defer | Preserve approved separation only | All exact equality details OPEN | Documentary gap review; no conformance result | Existing constraints only | No authoritative/equality result invented | No compatibility capability claimed | All concrete namespace representation/comparison |

**RECOMMENDATION — NOT APPROVED:** J-R1 as a documentary principle only, with byte/text/equality/admissibility explicitly deferred. J-R4 is a separate valid defer answer. Neither recommendation selects a concrete encoding or comparison convention.

**Owner question I-Q02:** Approve only J-R1's documentary opaque-identifier study, choose J-R2 or J-R3 for separately bounded documentary investigation, reject, or defer via J-R4? Record the exact selected scope and unresolved byte/text/encoding/equality questions. This answer must not approve any registry tuple, schema, implementation, issuer or full H-D02.

## I-Q03 — authority boundary

**PROPOSED — NOT APPROVED.** Preserve existing I-Q03 ← I-Q02 edge as decision order. That edge does not force an owner to answer both together; I-Q03 may be explicitly deferred and no answer is inferred from I-Q02. Authority analysis can state missing evidence without pretending equality has been chosen.

| Alternative | Pure comparison scope | Trusted authority requirements | Required operational evidence | Failure/replay risks | Dependency on I-Q02 | Future owner decisions |
|---|---|---|---|---|---|---|
| J-A1 supplied assertion separate from authenticated authority | Compare supplied assertions/associations only once representation convention is separately pinned | Any authoritative claim requires independently qualified provenance, entitlement and applicable state | OPERATIONAL_EVIDENCE_REQUIRED; none obtained; genuine association/issuer/currentness/use evidence needed separately | Forgery, legitimate but unauthorized signer, detached scope, stale receipt | Equality identifies what is compared, never who owns it | Approve only documentary distinction if desired; later select provenance/currentness/qualification scope separately |
| J-A2 future issuer/provenance model, not selected | Supplied comparisons remain non-authoritative | Must later specify issuer scope/delegation/control, provenance and compromise model without appointing one now | OPERATIONAL_EVIDENCE_REQUIRED for actual trust/issuance/custody/revocation | Compromised issuer, excessive delegation, rollback, wrong signed context | Representation must bind the exact future claim; no equality answer selects issuer | Separately commission bounded model/qualification and decide actual infrastructure later |
| J-A3 defer all authoritative namespace claims | Only inherited separation and explicitly conditional supplied-data comparisons | No new authoritative claim | OPERATIONAL_EVIDENCE_REQUIRED before any actual authority finding | Avoid default trust; no fallback to digest/string/signature-shaped claims | I-Q02 can remain pending or be separately answered | Explicitly defer authority; later decisions remain required |

**RECOMMENDATION — NOT APPROVED:** J-A1 as the smallest documentary separation scope, retaining all actual authority claims unqualified. J-A3 is independently answerable deferral. J-A2 remains an unselected future research alternative; no issuer, signer, algorithm, root, ACL, identity/storage provider or registry service is chosen.

**Owner question I-Q03:** Approve only J-A1's assertion-versus-authority documentary distinction, commission a separately bounded J-A2 model study without selecting infrastructure, reject, or defer via J-A3? State explicitly that real namespace authority/currentness/use claims still require OPERATIONAL_EVIDENCE_REQUIRED.

An equality convention, even if later selected, does not authenticate namespace ownership. An I-Q03 documentary answer does not approve I-Q02 encoding/equality. Neither answer approves H-D02 as a whole, H-D03–H-D10, F-D01, resolver/cache/migration or production use.

## Preserved graphs and external gates

The [acceptance packet](G3_2_0J_ACCEPTANCE_PACKET.md) reproduces the unchanged H-D and I-Q adjacency lists from original dossiers and records their independent acyclicity checks. J-R1–4 and J-A1–3 are alternative labels, not new prerequisite nodes; no local J graph is introduced. Cross-references between alternatives describe evidence obligations, not new inherited graph edges.

H-D02 is still the unresolved complete key/context decision. H-D03 controls PG wire-artifact equivalence, H-D04 raw identity/metadata/change policy, and H-D05 policy-role/head boundaries; none is adopted here. OP-07/08 accounting/budgets, OP-09 admission, OP-22 exact tool/profile schemas and OP-24 roles remain OPEN. CM-006/071/072/095 remain PARTIAL, as do the other three retained CM. Real namespace/provider/storage/Windows qualification requires a separate authorized task and actual evidence. Documentary closure cannot satisfy an operational dependency.

Sources: [I owner dossier](G3_2_0I_HD02_OWNER_DECISION_DOSSIER.md) I-Q01–10 and exact graph; [H owner dossier](G3_2_0H_OWNER_DECISION_DOSSIER.md) H-D01–10; [I options](G3_2_0I_REGISTRY_KEY_AND_NAMESPACE_OPTIONS.md); original approved sources registered in packet.

**STOP. Await independent ChatGPT audit and separate owner approval. No merge, G3.2.1 or production permissions.**
