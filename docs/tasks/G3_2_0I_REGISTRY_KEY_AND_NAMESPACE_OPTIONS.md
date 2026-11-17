# H-D02 registry key and namespace — A/B/C proposals

**DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. H-D02: PROPOSED — NOT APPROVED.**

SI-INTEGRATION-G3.2.0i; 2026-11-17 (Europe/Kyiv). H-D01/A APPROVED_LIMITED_SCOPE for documentary direction only. F-D01 NOT APPROVED.

[APPROVED_LIMITED_SCOPE] H-D01/A only separates key, expected integrity metadata and observed bytes for research; [owner record](G3_2_0I_OWNER_APPROVAL_HD01_A.md). [PROPOSED] I-A/I-B/I-C below are separately unselected H-D02 alternatives, not inherited adoption from H-D01/A. Sources: [H owner dossier](G3_2_0H_OWNER_DECISION_DOSSIER.md) H-D02, [H identity analysis](G3_2_0H_IDENTITY_CONFLICT_AND_DEDUP_ANALYSIS.md) seven families, [C P2 proposals](G3_2_0C_P2_REFERENCE_AND_SCHEMA.md) §§1–4. No concrete tuple or namespace wire field is adopted.

| Dimension | I-A — explicit namespace + family + stable declared identity | I-B — globally scoped identity | I-C — defer concrete key |
|---|---|---|---|
| Proposed composition | Context, family and declared stable ID with only explicitly declared version/revision; expected hash/length not silent key slots | Global identity only if construction/uniqueness/authority/collision/immutable binding/type scope explicitly specified | Keep H-D01/A triad principle; concrete registry and admission OPEN |
| Identity ambiguity / collisions | Same local ID can be distinguished by chosen context; context substitution remains a threat | UUID-looking/global-looking string is no proof; actual duplicate issuance and issuer/type collision semantics needed | No new collision/lookup result claimed; unresolved scenarios explicit |
| Stable IDs / version | Use source-declared slots only; raw ByteRef has no invented revision | Global identity may encode/version content only under new explicit family semantics; no hash-as-automatic-version | Do not infer missing revision or latest; preserve historical proposals |
| Same-key conflicting metadata | Key remains separate so changed expected digest/length stays visible as a contradictory observation; disposition separately OPEN | Global key still needs associated immutable metadata/conflict policy; checksum alone cannot confer namespace legitimacy | Retain contradictory evidence without claiming a registry conflict result |
| Same bytes / different keys | Do not silently merge semantic subjects/roles; logical reuse question H-D07 separate | Global equal-content IDs need exact byte/domain/type/provenance semantics; content equality not rights/review equality | No alias/cache/dedup permission |
| Cross-family alias | Explicit proposed family context keeps toolchain/executor/raw/PG apart; family universe not adopted | Global ID must bind or be compared under family semantics; globally unique ID does not eliminate typed interpretation | No supported family set selected |
| PG canonical / raw identity | P1-05 fixed; registry wire-artifact policy waits H-D03, raw metadata/change policy H-D04 | Global identity cannot collapse domains or pretend every Hash field uses the same preimage | Preserve distinction only; exact equality/conflict policy OPEN |
| Namespace comparison vs authority | Can compare supplied context labels once equality chosen; actual context legitimacy/custody separate | Requires explicit issuer/provenance/uniqueness model and later actual evidence; none selected | Authority claims remain blocked; supplied equality alone not admission |
| Backward compatibility | No namespace field inserted into old wire data; context association is separately proposed, may require future version decision | Historical local IDs not auto-global; no auto-upgrade, qualifier stripping or implicit migration | Old docs/vectors unchanged; no new acceptance claimed |
| Resource implications | Define comparison units before future aggregate/dedup accounting; no free physical reads/allocations/retries | Global-key lookup/collision/provenance work not free; equality alone not cache authority | F-D04/05 budgets and dependency work remain OPEN |
| Migration / reapproval | Context/identity changes cannot silently transfer subject/rights/review; actual effect classes H-D08/F-D06/07 | Local→global remapping needs provenance/new subject/review policy when applicable, not string rewrite | No migration/continuity acceptance |
| Future independent evidence | Supplied namespace/key/metadata/header/byte case plans; real context binding/OS custody qualification separate | Above plus issuer collision/replay/uniqueness/provenance evidence and exact type/preimage model | Documentary gap inventory; no fake successful registry |
| Explicitly unapproved | Specific field tuple, context representation/equality/authority, schema/family/version/admission/error/dedup rules | Any global ID scheme, issuer/trust root/signing authority/hash-domain/ACL/resolver | Any concrete key or admission policy |

## Recommendation and exact narrow scope

**RECOMMENDATION — NOT APPROVED:** prefer I-A **as the next documentary comparison candidate** because it exposes local-ID collisions, wrong-family lookup and changed metadata without depending on claimed global uniqueness. It does not establish namespace authority; an unqualified namespace assertion can be forged. If a real global issuer/type/collision model is later available, I-B deserves separate review; I-C is appropriate until owner can pin missing representation/family boundaries. No choice occurs here.

[PROPOSED] Candidate stable-field compositions in [matrix](G3_2_0I_IDENTITY_METADATA_OBSERVATION_MATRIX.md) are analysis coordinates, not adopted registry tuples or new fields. The question is not whether a convenient hash string may redefine an allegedly immutable ID. Explicit content-addressed identity could be studied only as a separately selected family/preimage/version model, never smuggled into I-A by adding changed metadata to its key.

[OPEN_CONTRACT_DETAIL] Namespace equality: exact string/byte/codepoint comparison, validated global labels or explicit alias table are different future choices. No automatic NFC/casefold/trim/URI or UUID interpretation is selected. PG-C14N-1 scalar/key canonicalization remains fixed and does not itself define namespace authority/equivalence. Missing context must not be silently filled from caller cwd/path/current user/default tenant.

[OPEN_CONTRACT_DETAIL] Context association must eventually bind the namespace assertion to the exact requested reference/profile/location, not merely appear beside it in an unauthenticated file. Historical refs generally lack a namespace field; adding one would be a separate future wire/version decision with hash/subject consequences. No insertion into PG01–PG05 or new context JSON schema/API here. See I-Q02/03/10 and I-C029.

[APPROVED] X03/X04/P1-05/P1-06 remain fixed under all options. [PROPOSED] Concrete H-D03 PG artifact policy, H-D04 raw metadata/version policy and H-D05 role/head admission cannot be adopted through H-D02. **STOP.**
