# Namespace comparison, authority and conflicting observations

**DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. H-D02: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0i; 2026-11-17 (Europe/Kyiv). H-D01/A APPROVED_LIMITED_SCOPE for documentary direction only. F-D01 NOT APPROVED.

Sources: [H identity analysis](G3_2_0H_IDENTITY_CONFLICT_AND_DEDUP_ANALYSIS.md) key/metadata/bytes triad and seven families; [H owner dossier](G3_2_0H_OWNER_DECISION_DOSSIER.md) H-D02/03/04/05/07/10; [D P1 normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-05/P1-06; [B owner X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md) X03/X04; [C operational dependencies](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md) OP-15/17/20/21/23/28.


## Independent questions — no issuer or resolver chosen

| Question | Supplied/offline comparison that could be studied | What remains OPEN or needs actual evidence |
|---|---|---|
| Who declares a namespace? | Identify the document/profile/caller that makes a namespace assertion, without accepting its truth | Declaration is not authority. Actual entitled issuer/custodian/uniqueness model not selected; no signing root/ACL/provider appointed |
| How is context bound to requested ref? | Candidate explicit association between namespace assertion, request/reference location, family and expected identity | Binding representation, provenance and tamper/replay properties unresolved. No new wire field/schema/hash domain |
| Same ID in two namespaces? | Distinguish two supplied contexts under I-A or examine explicit global-ID claim under I-B | Actual equality/alias/collision policy and namespace authority require separate decision; do not silently strip qualifiers |
| One object in multiple roles? | Compare bytes independently from declared semantic roles/subjects | Equal content does not transfer rights, reviewer authority, issuer power or old approval. Concrete H-D05 role admission OPEN |
| Same stable ID, conflicting hash/length? | Preserve both metadata assertions and independently compare actual header/bytes | No first/last/latest resolution; PG canonical equivalence versus raw artifact policy depends H-D03/04. Exact registry/error disposition OPEN |
| Different IDs, identical bytes? | Recognise supplied content coincidence without collapsing semantic identities | Actual byte reuse/caching/dedup policy H-D07 and real cost/custody evidence separate |
| Observed header contradicts request? | Compare declared/observed type, ID and revision as supplied data | Supported schema/family rules not adopted; digest match alone does not prove requested object identity or authority |
| Provider unavailable? | Record that no authenticated observation is supplied; compare any cached/supplied data only as such | Not a confirmed missing/revoked/current finding. P1-06 no fabricated negative; no new public code assigned |
| Which claims can be pure? | Equality/inequality of explicitly supplied contexts, stable fields, metadata and declared headers under a chosen comparison convention | Not actual namespace ownership, trusted uniqueness, latest state, durable immutability or authorisation |
| Which need real infrastructure? | Documentary list of missing trust assumptions/evidence | Actual registry/namespace authority, access, stable OS handles/storage, authenticated time/history/revocation/custody require future authorised qualification |

## Conflict analysis sequence — PROPOSAL, not an algorithm implementation

[PROPOSED] First keep context/family/stable fields, expected metadata and actual observation conceptually separate; do not rewrite contradictory claims or re-key them by changed digest merely to make them fit. Then ask which family equivalence rule is applicable. PG binding corresponds to canonical preimage, raw ByteRef to raw bytes; actual header consistency is another comparison. Record unresolved comparisons as OPEN_CONTRACT_DETAIL, not accepted/denied registry results with new codes. I-Q07 proposes visibility and questions only; H-D03/04/05 still control concrete policy.

[OPEN_CONTRACT_DETAIL] A stable raw key is proposed for an allegedly immutable object. A global content-addressed model would be a different explicitly selected family/ID contract with pinned type/domain/collision/version semantics; it cannot be introduced by treating changed metadata as an automatic valid version under an unchanged opaque object_id. PG equivalent wire artifacts need a separate H-D03 decision, not blanket raw-byte conflict or a changed canonical hash.

[OPEN_CONTRACT_DETAIL] Namespace comparison can be deterministic without authenticated authority. A profile/manifest could **eventually** specify context association, or a globally scoped ID contract could include namespace semantics. Neither transport/encoding/provenance mechanism is adopted here. Historical refs without namespace fields remain unchanged; no guessed cwd/current-user/path/default tenant supplies missing context. Copying a reference without its context can change interpretation even if the target digest string is unchanged; I-C029 captures this gap.

## Failure modes and Story Studio consequences

[PROPOSED] Cross-namespace/family cache aliases could substitute another RU/UK plan, evaluator/source fragment, toolchain or executor profile while showing a familiar ID/hash. Role confusion could reuse asset/licence/policy content under a different intended-use or issuer context. Stable-key metadata conflicts could be hidden by constructing cache keys from expected hash/length. Namespace normalisation/global-ID claims could collapse distinct contexts or split one context unpredictably. These are future attack analyses, not actual vulnerabilities tested in running Story Studio.

[APPROVED] X04 exact plan/subject binding and no inherited review for changed render-affecting subjects remain fixed. [OPEN_CONTRACT_DETAIL] Namespace-only migration/equivalence and role-policy selection still need separate review; no rule automatically transfers rights or approves every namespace change as technically harmless. Human/editorial/scientific quality and actual licences cannot be inferred from content/key equality.

## Operational boundary — not selectable infrastructure

[OPERATIONAL_EVIDENCE_REQUIRED] Actual namespace authority/uniqueness, authenticated registry response/currentness, trusted history/time/revocation, immutable storage/opened object identity, TOCTOU/reparse/access containment and durable cache/ledger behaviour require independently qualified actual infrastructure under future explicit owner scope. No issuer, trust root, signer, ACL, storage provider or resolver is chosen. Storage S3 is not production-qualified; Windows10/11 CPU-only/native/NTFS tests NOT_RUN. Synthetic assertions, signatures-as-text and matching digests are not substitutes.

[APPROVED_LIMITED_SCOPE] H-D01/A authorises this documentary investigation only. [PROPOSED] I-A recommendation is not adoption; all concrete namespace comparison/admission/cache/migration rules remain pending. **STOP.**
