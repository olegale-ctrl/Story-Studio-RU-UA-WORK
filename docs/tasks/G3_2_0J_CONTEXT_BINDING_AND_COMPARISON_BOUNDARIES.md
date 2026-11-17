# Context binding and comparison boundaries

**OWNER_AUTHORIZED_DOCS_ONLY — ANALYSIS / PROPOSALS ONLY. Implementation FORBIDDEN.**

SI-INTEGRATION-G3.2.0j; 2026-11-17 (Europe/Kyiv). I-Q02 and I-Q03: **PROPOSED — NOT APPROVED**. H-D02 and full F-D01: **NOT APPROVED**.

## Candidate documentary coordinates, not a registry key

The approved separation direction permits discussing namespace assertion, typed family, declared stable identity, expected integrity metadata and independently observed bytes/header as separate comparison coordinates. Their conjunction is a candidate documentary comparison tuple only. It is not a concrete approved registry key, accepted schema, hash preimage, namespace encoding or executable comparison algorithm. Metadata is not silently made a new stable identity when a digest changes.

| Association studied | Ambiguity / attack | Candidate documentary boundary; disposition still open |
|---|---|---|
| Exact request | Same ref copied between requests with distinct context | Preserve which request makes each assertion; no request-binding mechanism adopted |
| Reference location | Identical-looking refs occur in different slots/manifests | Preserve source position and semantic slot; source location is not namespace authority |
| Family | Structurally alike toolchain/executor/raw refs | Family assertion stays distinct; equal bytes do not select an accepted family |
| Stable identity | Local ID reused under another namespace | Retain both assertions and declared version only where present; no invented raw revision |
| Expected metadata | Same alleged identity has different expected digest/length | Expose inconsistency without silently re-keying; H-D03/04 conflict policy remains open |
| Observed bytes/header | Header/type differs despite familiar hash text | Compare supplied observation separately; digest equation is not authenticity |
| Detached manifest / copied reference | Context stripped and replaced by caller default | No inferred context; concrete transport/binding/admission outcome EXPECTED_RESULT_OPEN |
| Cache-key context | Cache omits namespace/family and returns equal digest | No cache reuse permission; logical equality, physical work and semantic authority separate |
| Cross-family aliases | Equal raw payload offered in another family | No automatic family conversion, byte-domain change or alias legitimacy |
| Policy role | Issuer/reviewer/rights policy confused with another slot | Role-sensitive comparison question stays H-D05/I-Q09/OP-24; no role grant |
| SubjectKey / X04 | Namespace relabeling masks changed bound tool/profile/plan | Actual render-affecting binding changes require changed exact plan/hash/subject/candidate under X04; namespace-only equivalence/review effects remain open |
| Historical namespace-free references | Old record copied into a new contextual profile | Historical bytes stay unchanged; no retrofit, default namespace, silent upgrade or inherited review |

Never infer namespace from current working directory, current OS user, file path, environment variable, default tenant, latest profile or caller-provided unverified alias. An explicit caller assertion can be recorded as an assertion; its alias mapping is not accepted as authoritative. No directory/environment/provider is probed to fill missing context.

## Fail-closed analysis without adopting runtime behavior

An unsupported or ambiguous comparison cannot justify a positive identity/authority/admission claim. This documentary withholding is not an implemented resolver denial, a new machine result or a prescribed new PG error. Preserve contradictions and missing evidence; do not select first/last/latest, replace unavailable evidence with authenticated negative findings, or claim an exception proves success. Concrete namespace failure classification remains EXPECTED_RESULT_OPEN until the relevant contracts are separately approved.

## Exact inherited byte and error boundaries

PG-C14N-1 is unchanged: strict scalar UTF-8/no initial BOM, duplicate decoded keys rejected, signed64 integers only, deterministic scalar key order, preserved arrays, no string normalization; remove only own top-level binding for SHA-256 over the existing PG domain prefix plus canonical bytes. Raw ByteRef SHA-256 binds complete actual raw bytes without PG prefix and with independent actual length. PG canonical-equivalent wire variants need not have equal raw bytes. Namespace rules cannot redefine these domains. Unpinned PolicyRef/HeadRef/use-scope preimages are not inferred from a Hash field.

P1-06 keeps the earliest failing stage: (1) bounded input/UTF-8 decode; (2) grammar/duplicates/closed schema/types/known enums; (3) local binding; (4) registry/reference/closure/dependency validation; (5) mode/subject consistency; (6) product/rights/trusted-state predicates; (7) execution/evidence. At stage4 established PG_FORMAT precedes PG_REFERENCE precedes PG_DIGEST; stage5 PG_MODE precedes PG_REFERENCE precedes PG_SCOPE. Stage6 established groups remain availability → identity/authority/history → revocation → expiry → evaluation/currentness → product → rights. Stage7 dependency/history loss precedes PG_EXECUTION, PG_INCOMPLETE, PG_DIGEST, PG_EVIDENCE. Unspecified operational causal distinctions stay open. A target issue discovered at stage4 is not retroactively a root-stage2 finding. Earlier-stage failures cannot be superseded by namespace authority assertions.

P1-DIAG-01 applies only to same-code/same-stage private diagnostics on the historical pg-01/proposal-1 root's declared fields in order contract, id, revision, mode, body, binding_sha256. It does not order new namespace descriptors, nested fields, graph traversal or provider observations. Existing public safe messages and verdict namespace remain unchanged; no new PG codes.

Sources: [B X01–X04](G3_2_0B_OWNER_DECISIONS_X01_X04.md), [D P1-05/06](G3_2_0D_P1_NORMATIVE_CONTRACT.md), [RESOLVE-1 scope](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md), [H edges](G3_2_0H_REFERENCE_EDGE_AND_CLOSURE_BOUNDARIES.md), [I matrix](G3_2_0I_IDENTITY_METADATA_OBSERVATION_MATRIX.md). H-D02/03/04/05/07/08/10, OP-07/08/09/22/24 and CM-006/071/072/095 remain separate gates. F-D02/A root units do not approve reference accounting; F-D03/A reports cannot prove zero effects.

**STOP. Await independent ChatGPT audit and separate owner approval. No merge, G3.2.1 or production permissions.**
