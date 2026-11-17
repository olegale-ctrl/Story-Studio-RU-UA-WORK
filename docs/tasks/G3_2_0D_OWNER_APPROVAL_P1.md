# P1 — Owner approval record

**P1_OWNER_DECISIONS_DOCUMENTED — DOCS_ONLY**

SI-INTEGRATION-G3.2.0d; 2026-11-17 (Europe/Kyiv). Только документация; не PRODUCTION_APPROVED и не полный PG freeze.

## Authority and exact scope

Основание записи: прямое задание владельца **SI-INTEGRATION-G3.2.0d, §1 и §6** (получено в этом сеансе). Это документирование сообщённого решения, а не создание operational approval/grant, установление реальной личности reviewer или проверка подписи. G3.2.0c принят `ACCEPTED_DOCS_ONLY`; восемь ниже — `OWNER_APPROVED`, строго pure-contract. X01–X04 ранее approved и сохранены. Historical OPEN/PROPOSED формулировки старых файлов остаются неизменными; этот новый dated record задаёт только явно разрешённое уточнение.

Base `86ae74058c2a90b563855eac15f46ff8b3be28e4`, tree `f0f3aaf1c95a1d6400a9e65d12beff04d0159895`, parent `0d6d9076ab535c1b258206beb4e4fe9c005e79e1`. Main read-only `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

## OP-01 — OWNER_APPROVED pure wire cap

Maximum full root wire input **8,388,608 actual bytes inclusive**, before UTF-8 decoding. Whitespace and own binding field count. ByteRef descriptor is part of root; actual referenced content is accounted separately, not granted an8MiB aggregate cap. Canonical output and domain-prefixed hash preimage are distinct accounting domains. Initial BOM remains forbidden under OP-05. No complete CPU/RAM safety claim.

## OP-02 — OWNER_APPROVED pure container depth

Maximum64. Standalone scalar0; root array/object1; nested array/object increments1; scalar leaves do not increment. JSON depth is distinct from reference traversal depth.

## OP-03 — OWNER_APPROVED decoded strings

Maximum65,536 decoded UTF-8 bytes for each key/string value, after JSON unescaping. Validate scalar sequence; combine paired surrogate escapes; reject lone surrogates. No NFC/NFD, trim or casefold. Raw escaped bytes remain under OP-01.

## OP-04 — OWNER_APPROVED per-array cap

Maximum10,000 elements per array; stricter field cardinalities remain. Preserve order, no truncation/deduplication. Global nodes/tokens/object-member budgets remain OPEN OP-07.

## OP-05 — OWNER_APPROVED PG-C14N-1 bytes

Pinned [C01–C10/B01 canonical specification](G3_2_0A_CANONICALIZATION_SPEC.md) and [G3.2.0c P1](G3_2_0C_P1_CANONICAL_FOUNDATION.md) §5: strict UTF-8/no initial BOM; exact signed64; no float/exponent syntax; -0→0; Unicode codepoint key ordering; duplicates after unescaping rejected; no normalization; exact escapes; original array order; explicit null distinct from missing. SHA-256 domain prefix is UTF8("StoryStudio/PG-C14N-1") followed by byte00. Own hash excludes only own top-level binding_sha256; nested bindings retained. ByteRef uses raw SHA-256 without domain prefix. No interchangeability with Git SHA-1, G2 or SI digests. This does not approve complete schemas, RenderPlanV2 implementation or migration.

## OP-06 — OWNER_APPROVED pure error selection

Preserve X01/X02 and seven-stage order; earliest failing stage wins. Apply fixed within-stage category priority from G3.2.0c P1 §6, then canonical schema-field/ref-identity ordering for safe bounded diagnostics, not arbitrary parser discovery order. Unknown exceptions cannot produce success. Actual dependency unavailability cannot become an authenticated negative finding.

[Normative contract](G3_2_0D_P1_NORMATIVE_CONTRACT.md) separates the frozen deterministic selections from `OPEN_OPERATIONAL_DETAIL`: provider-specific causal distinctions, unresolved within-category operational ordering and execution chronology must not be invented. No new error code or catch-all fake classification is approved.

## OP-26 — OWNER_APPROVED status boundary

STRUCTURALLY_VALID is descriptive only; no new machine enum. Pure result remains CONSISTENT_NO_AUTHORITY or DENY. No render, release or production authority can be inferred. Canonical/hash correctness alone is not a whole-PG consistency result.

## OP-27 — OWNER_APPROVED safe errors

Retain exactly21 existing PG codes and the fixed safe public-message mapping in G3.2.0c P1 §8, copied exactly into the normative contract. Separate public primary error from private bounded diagnostics. Public output contains no raw paths, secrets, private source text, reviewer identity or exception dumps. Publication/access policy stays under OPEN OP-21/23; approval does not authorize export or establish provider behavior.

## Explicit exclusions

OP-07/08, OP-09–25 and OP-28 —20 parameters — remain **OPEN — NOT APPROVED**, including previously decision-ready OP-09/22. No final schemas/migrations beyond P1, production qualification/permissions, G3.2.1, actual providers, rights grants, render or release is approved. Existing source files, vectors and CI remain unchanged. Conformance evidence below is documentary/hash arithmetic, not validator execution.

**STOP: independent ChatGPT audit and separate owner decision required before any further stage.**
