# 36 adversarial future cases and evidence plan

**OWNER_AUTHORIZED_DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. Implementation FORBIDDEN.**

SI-INTEGRATION-G3.2.0j; 2026-11-17 (Europe/Kyiv). I-Q02 and I-Q03: **PROPOSED — NOT APPROVED**. H-D02 and full F-D01: **NOT APPROVED**.

## Evidence and interpretation rules

All J-C cases below are **PROPOSED documentary plans**, not executable fixtures, vectors or performed tests. Synthetic setup is conceptual prose; no cryptographic digest/proof or actual provider receipt is fabricated. For each case the concrete equality/admission/resolver/error result is EXPECTED_RESULT_OPEN. The cited inherited constraint is the only fixed conclusion where applicable. Future pure comparison evidence proves supplied-data correspondence only; actual trusted facts always require OPERATIONAL_EVIDENCE_REQUIRED.

Source anchors: [I prior cases](G3_2_0I_ADVERSARIAL_CASES_AND_EVIDENCE_PLAN.md) I-C001–030; [I matrix](G3_2_0I_IDENTITY_METADATA_OBSERVATION_MATRIX.md) seven families; [B X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md); [D normative P1](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-05/06/26/27; [G root accounting](G3_2_0G_ROOT_ACCOUNTING_CONTRACT.md) G-AC-04/05. No historical expected result is rewritten.

## J-C001 — Exact same assertion

- **Synthetic setup:** Two requests supply the same opaque namespace spelling and same declared ref.
- **Ambiguity / attack and competing interpretations:** Deterministic supplied equality versus legitimate common ownership.
- **Inherited approved constraint:** I-Q01/A separation only; equality convention remains unapproved.
- **OPEN decision:** I-Q02/03; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin comparison domain, then independently prove provenance for any ownership claim.
- **Execution:** NOT_RUN.

## J-C002 — Distinct assertions

- **Synthetic setup:** Two requests supply distinct namespace spellings and the same remaining declarations.
- **Ambiguity / attack and competing interpretations:** Distinct identities versus an unqualified alias relationship.
- **Inherited approved constraint:** I-Q01/A separates explicit context; no alias model approved.
- **OPEN decision:** I-Q02/03/08; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Specify exact equality and any future separately qualified alias provenance.
- **Execution:** NOT_RUN.

## J-C003 — Same local ID across namespaces

- **Synthetic setup:** Same local object ID appears under two asserted namespaces.
- **Ambiguity / attack and competing interpretations:** Separate local identities versus global uniqueness assumed from ID.
- **Inherited approved constraint:** I-Q01/A does not approve a concrete registry key.
- **OPEN decision:** I-Q02/03; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Prove namespace-scoped comparison after selection; authority separately.
- **Execution:** NOT_RUN.

## J-C004 — Same digest across namespaces

- **Synthetic setup:** Distinct namespaces carry equal expected digest assertions.
- **Ambiguity / attack and competing interpretations:** Byte coincidence versus cross-namespace identity/rights transfer.
- **Inherited approved constraint:** I-Q05/A separates expected integrity from identity and observation.
- **OPEN decision:** I-Q02/03/08; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Independent whole-byte correspondence under selected family; no identity transfer inferred.
- **Execution:** NOT_RUN.

## J-C005 — Different digest under same asserted key

- **Synthetic setup:** Same asserted context/family/stable declaration accompanies different digest metadata.
- **Ambiguity / attack and competing interpretations:** Visible inconsistency versus silently treating digest as a new stable version.
- **Inherited approved constraint:** I-Q05/A preserves metadata separation; H-D03/04 disposition unapproved.
- **OPEN decision:** I-Q05/07; H-D03/04; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin family conflict/equivalence policy before any registry outcome.
- **Execution:** NOT_RUN.

## J-C006 — Same bytes with different family

- **Synthetic setup:** Same supplied payload is labeled toolchain in one location and executor in another.
- **Ambiguity / attack and competing interpretations:** Physical byte coincidence versus family/role interchange.
- **Inherited approved constraint:** H-D01/A typed-family research; X04 exact bound roles preserved.
- **OPEN decision:** I-Q06; H-D04/05; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin family/header interpretation and independently qualify actual runtime use.
- **Execution:** NOT_RUN.

## J-C007 — Case variation

- **Synthetic setup:** Namespace spellings differ only in letter case.
- **Ambiguity / attack and competing interpretations:** Case-sensitive equality versus case-insensitive alias collapse.
- **Inherited approved constraint:** No namespace casefold rule approved; P1-05 unchanged.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Specify case semantics without relying on filesystem or locale defaults.
- **Execution:** NOT_RUN.

## J-C008 — NFC versus decomposed Unicode

- **Synthetic setup:** One supplied label uses composed accented scalar; another uses base plus combining mark.
- **Ambiguity / attack and competing interpretations:** Visual sameness versus distinct scalar/byte sequences.
- **Inherited approved constraint:** P1-05 performs no string normalization; external namespace equality still open.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin byte/text comparison and normalization decision separately; no default NFC.
- **Execution:** NOT_RUN.

## J-C009 — NFKC compatibility characters

- **Synthetic setup:** Compatibility-form label and visually related ordinary form are supplied.
- **Ambiguity / attack and competing interpretations:** Compatibility folding versus distinct opaque identifiers.
- **Inherited approved constraint:** P1-05 unchanged; no default NFKC.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Independent compatibility-character and confusable comparisons under chosen convention.
- **Execution:** NOT_RUN.

## J-C010 — Invalid UTF-8 namespace bytes

- **Synthetic setup:** External namespace material is described as containing invalid UTF-8 bytes.
- **Ambiguity / attack and competing interpretations:** Opaque byte identity versus invalid decoded-text representation.
- **Inherited approved constraint:** P1-05 rejects malformed raw UTF-8 within applicable PG input; external encoding not selected.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Separate PG input validity from external namespace admissibility; pin decoder/domain.
- **Execution:** NOT_RUN.

## J-C011 — Embedded NUL

- **Synthetic setup:** Namespace candidate contains an embedded NUL scalar or byte.
- **Ambiguity / attack and competing interpretations:** Exact complete value versus truncated C-string/display interpretation.
- **Inherited approved constraint:** P1-05 escapes JSON controls; does not approve namespace NUL admissibility.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Compare complete length-aware value and pin admissibility; no parser implemented.
- **Execution:** NOT_RUN.

## J-C012 — Control characters

- **Synthetic setup:** Namespace assertion contains escaped control characters in otherwise valid textual material.
- **Ambiguity / attack and competing interpretations:** Literal identifier content versus display/log splitting.
- **Inherited approved constraint:** P1-27 safe public messages cannot interpolate raw private text.
- **OPEN decision:** I-Q02/03; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Separate comparison/admissibility from bounded private presentation and operational leakage evidence.
- **Execution:** NOT_RUN.

## J-C013 — Prefix or suffix whitespace

- **Synthetic setup:** Assertions differ by leading or trailing whitespace.
- **Ambiguity / attack and competing interpretations:** Significant content versus silent trim.
- **Inherited approved constraint:** X01/P1-05 no trim; namespace policy unselected.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin exact comparison and display treatment; no implicit trim.
- **Execution:** NOT_RUN.

## J-C014 — URI-equivalent-looking values

- **Synthetic setup:** Namespace spellings look related by URI case, escaping or path-segment rules.
- **Ambiguity / attack and competing interpretations:** Opaque identifiers versus parsed/normalized URI identity.
- **Inherited approved constraint:** I-A limited direction selects no URI scheme or resolver.
- **OPEN decision:** I-Q02/03; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Explicit scheme, interpretation, comparison and authority evidence before URI equivalence claims.
- **Execution:** NOT_RUN.

## J-C015 — UUID-equivalent-looking values

- **Synthetic setup:** Namespace strings look like differently cased or formatted UUIDs.
- **Ambiguity / attack and competing interpretations:** Opaque strings versus parsed UUID values/global legitimacy.
- **Inherited approved constraint:** No globally qualified namespace scheme approved.
- **OPEN decision:** I-Q02/03; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin UUID interpretation if ever selected; formatting never proves issuer authority.
- **Execution:** NOT_RUN.

## J-C016 — Alias mapping

- **Synthetic setup:** An unverified caller table claims two namespace assertions are aliases.
- **Ambiguity / attack and competing interpretations:** Caller convenience versus legitimate scoped equivalence.
- **Inherited approved constraint:** I-Q01/A does not authenticate alias mappings.
- **OPEN decision:** I-Q02/03/08; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Separately specify alias provenance, scope, conflict and migration evidence.
- **Execution:** NOT_RUN.

## J-C017 — Missing namespace

- **Synthetic setup:** Historical reference is supplied with no namespace assertion.
- **Ambiguity / attack and competing interpretations:** Explicit unresolved context versus inferred convenience default.
- **Inherited approved constraint:** Present task forbids silent namespace inference.
- **OPEN decision:** I-Q02/10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Define future historical compatibility/admission without inventing fields or error codes.
- **Execution:** NOT_RUN.

## J-C018 — Cwd or path supplies namespace

- **Synthetic setup:** Same reference is copied to a different directory and caller infers a namespace.
- **Ambiguity / attack and competing interpretations:** Filesystem location versus explicit contextual assertion.
- **Inherited approved constraint:** Present task forbids cwd/path/current-user namespace inference.
- **OPEN decision:** I-Q02/03/10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Show explicit context provenance separately from path; real containment qualification later.
- **Execution:** NOT_RUN.

## J-C019 — Environment or default tenant supplies namespace

- **Synthetic setup:** Namespace is absent while environment/default tenant/latest profile changes.
- **Ambiguity / attack and competing interpretations:** Convenient default versus detached/unverified context.
- **Inherited approved constraint:** Present task forbids environment/default-tenant/latest-profile inference.
- **OPEN decision:** I-Q02/10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Future explicit binding/compatibility evidence; no environment values read.
- **Execution:** NOT_RUN.

## J-C020 — Detached context binding

- **Synthetic setup:** Reference copied without the manifest that asserted its request/location association.
- **Ambiguity / attack and competing interpretations:** Preserved reference bytes versus lost association.
- **Inherited approved constraint:** I-Q01/A approves separation, not transport or binding implementation.
- **OPEN decision:** I-Q02/03/10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin exact request/location association and independent tamper/provenance evidence.
- **Execution:** NOT_RUN.

## J-C021 — Namespace swapped between requests

- **Synthetic setup:** Two supplied requests have their external namespace assertions exchanged.
- **Ambiguity / attack and competing interpretations:** Locally plausible labels versus original request association.
- **Inherited approved constraint:** No namespace binding mechanism approved; X04 still exact.
- **OPEN decision:** I-Q02/03; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Future negative request-association evidence and actual custody proof.
- **Execution:** NOT_RUN.

## J-C022 — Namespace swapped between families

- **Synthetic setup:** Namespace context from a raw-ref location is attached to executor-family reference.
- **Ambiguity / attack and competing interpretations:** Same-looking label versus family-bound meaning.
- **Inherited approved constraint:** H-D01/A separates typed family; no new family admission.
- **OPEN decision:** I-Q02/03/06; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin family/context associations and negative copied-context cases.
- **Execution:** NOT_RUN.

## J-C023 — Forged issuer assertion

- **Synthetic setup:** Supplied text claims a prestigious namespace issuer without independent evidence.
- **Ambiguity / attack and competing interpretations:** Issuer naming versus entitled authenticated provenance.
- **Inherited approved constraint:** P1-26 no authority from pure consistency.
- **OPEN decision:** I-Q03; H-D10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Actual authorized issuer/control/provenance evidence; no issuer selected.
- **Execution:** NOT_RUN.

## J-C024 — Signature-shaped text

- **Synthetic setup:** A supplied manifest includes signature-like text and matching digest text.
- **Ambiguity / attack and competing interpretations:** Presence of cryptographic-looking material versus genuine authenticated scoped association.
- **Inherited approved constraint:** P1-05 digest correspondence is not authority.
- **OPEN decision:** I-Q03; H-D10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Actual verification/trust/entitlement/compromise evidence under later selected model.
- **Execution:** NOT_RUN.

## J-C025 — Provider unavailable

- **Synthetic setup:** Namespace authority observation is unavailable while cached assertions remain.
- **Ambiguity / attack and competing interpretations:** Unknown trusted state versus authenticated absent/revoked/current.
- **Inherited approved constraint:** P1-06 forbids fabricated authenticated negatives.
- **OPEN decision:** I-Q03; H-D10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Real availability/cause evidence and separately specified failure semantics.
- **Execution:** NOT_RUN.

## J-C026 — Stale or replayed registry observation

- **Synthetic setup:** Old supplied receipt is reused as if current.
- **Ambiguity / attack and competing interpretations:** Authentic past fact versus current namespace authority/use permission.
- **Inherited approved constraint:** P1-06 distinguishes established state from unavailable or unknown facts.
- **OPEN decision:** I-Q03/04; H-D05/10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Actual freshness/history/revocation/anti-replay evidence; sequence alone insufficient.
- **Execution:** NOT_RUN.

## J-C027 — Cross-namespace cache alias

- **Synthetic setup:** Cached payload from one namespace is offered in another based on digest only.
- **Ambiguity / attack and competing interpretations:** Physical sharing versus semantic identity/authority reuse.
- **Inherited approved constraint:** F-D02/A is root-only; no cache or free dependency-work approval.
- **OPEN decision:** I-Q02/03/08; H-D07; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Future identity/metadata isolation and actual read/allocation/retry/custody evidence.
- **Execution:** NOT_RUN.

## J-C028 — Role / PolicyRef confusion

- **Synthetic setup:** Policy bytes supplied in one role are offered in another namespace/role slot.
- **Ambiguity / attack and competing interpretations:** Same policy digest versus authority/right equivalence.
- **Inherited approved constraint:** X04 and P1-26 do not transfer review/permission by equality.
- **OPEN decision:** I-Q03/09; H-D05; OP-24; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin role/preimage contracts; actual actor/rights/currentness evidence separately.
- **Execution:** NOT_RUN.

## J-C029 — SubjectKey / X04 context change

- **Synthetic setup:** Namespace relabeling accompanies changed bound executor/toolchain while old subject approval is reused.
- **Ambiguity / attack and competing interpretations:** Cosmetic context change versus actual changed render-affecting binding.
- **Inherited approved constraint:** X04 changed target/ref/plan/hash/subject requires new candidate, no automatic old approval.
- **OPEN decision:** I-Q02/03; H-D08; OP-22; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Future before/after exact binding evidence; actual affected review and technical reapproval separately.
- **Execution:** NOT_RUN.

## J-C030 — Historical namespace-free migration

- **Synthetic setup:** Old namespace-free ref is proposed for a new contextual profile.
- **Ambiguity / attack and competing interpretations:** Silent retrofit and inherited approval versus separately decided compatibility.
- **Inherited approved constraint:** X04 concrete versions/migration/reapproval remain unapproved.
- **OPEN decision:** I-Q02/03/10; H-D08; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin source/target compatibility/provenance and review effects without rewriting old bytes.
- **Execution:** NOT_RUN.

## J-C031 — Windows path / reparse / TOCTOU

- **Synthetic setup:** An earlier hash assertion precedes changed ancestor/reparse/opened target.
- **Ambiguity / attack and competing interpretations:** Prior byte coincidence versus actual held object/custody identity.
- **Inherited approved constraint:** No OS/storage qualification follows from P1-05.
- **OPEN decision:** I-Q03; H-D10; OP-17/20; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Actual Windows/NTFS/handle/custody evidence in a later authorized scope.
- **Execution:** NOT_RUN.

## J-C032 — Malformed prefix

- **Synthetic setup:** A descriptor prefix is truncated or syntactically malformed.
- **Ambiguity / attack and competing interpretations:** Early rejection versus invented complete parse/accounting tree.
- **Inherited approved constraint:** F-D02/A malformed work not free; rejection-time semantics remain open.
- **OPEN decision:** I-Q02/10; OP-07/08; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin future syntax and prefix accounting; no runtime resource claim.
- **Execution:** NOT_RUN.

## J-C033 — Duplicate descriptors

- **Synthetic setup:** Two conflicting namespace descriptors occur at one proposed association.
- **Ambiguity / attack and competing interpretations:** First/last wins versus unresolved conflict.
- **Inherited approved constraint:** P1-05 rejects decoded duplicate JSON keys where applicable; descriptor-list conflicts are separate.
- **OPEN decision:** I-Q02/03/07; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Pin duplicate descriptor semantics; preserve both supplied claims in analysis.
- **Execution:** NOT_RUN.

## J-C034 — Ambiguous comparison domain

- **Synthetic setup:** One assertion has different raw escape spelling but the same decoded scalars.
- **Ambiguity / attack and competing interpretations:** Raw transport equality versus decoded-text equality.
- **Inherited approved constraint:** P1-05 PG canonical bytes do not choose namespace identity domain.
- **OPEN decision:** I-Q02; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Owner selects byte/text principle separately; independent comparison evidence then.
- **Execution:** NOT_RUN.

## J-C035 — Unsupported descriptor version

- **Synthetic setup:** A namespace descriptor claims an unselected version.
- **Ambiguity / attack and competing interpretations:** Fallback/guess versus explicit unsupported contract gap.
- **Inherited approved constraint:** No new schema/wire version or adapter approved.
- **OPEN decision:** I-Q02/10; H-D08; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Separate version and compatibility decisions; no new PG_VERSION code.
- **Execution:** NOT_RUN.

## J-C036 — Current user substitution

- **Synthetic setup:** Copied reference is assigned a namespace from the executing OS user.
- **Ambiguity / attack and competing interpretations:** Local execution identity versus explicit namespace assertion/authority.
- **Inherited approved constraint:** Present task forbids current-OS-user namespace inference.
- **OPEN decision:** I-Q02/03/10; full H-D02/F-D01 remain NOT APPROVED.
- **Expected result:** EXPECTED_RESULT_OPEN for concrete namespace equality/admission/error. Only the cited inherited constraint is already justified; no exact new PG code.
- **Pure versus operational evidence:** Future PURE supplied-data comparison only under separately selected rules. Actual authority, storage, currentness or permission: OPERATIONAL_EVIDENCE_REQUIRED.
- **Future proof requirements:** Explicit assertion and provenance requirements; actual identity/entitlement evidence later.
- **Execution:** NOT_RUN.


**STOP. Await independent ChatGPT audit and separate owner approval. No merge, G3.2.1 or production permissions.**
