# P1 — Normative pure-contract rules

**P1_OWNER_DECISIONS_DOCUMENTED — DOCS_ONLY**

SI-INTEGRATION-G3.2.0d; 2026-11-17 (Europe/Kyiv). Только документация; не PRODUCTION_APPROVED и не полный PG freeze.

## Authority, labels and precedence

[Owner record](G3_2_0D_OWNER_APPROVAL_P1.md), sourced from task §1/§6, documents eight decisions. Exact technical proposal source: [G3.2.0c P1](G3_2_0C_P1_CANONICAL_FOUNDATION.md), blob `8905865ed0f41b363d39993408a78605d3a829df`. Existing [A canonical rules](G3_2_0A_CANONICALIZATION_SPEC.md) are read with [B X01–X04 decisions](G3_2_0B_OWNER_DECISIONS_X01_X04.md). Historical NOT APPROVED labels in A/C do not override this narrow owner record and are not rewritten.

- `OWNER_APPROVED_PURE_RULE`: the eight rule sections below, only within specified scope.
- `CONDITIONAL_VECTOR_EXPECTATION`: an existing expected result under its layer and remaining supplied/profile assumptions; not a passed executable test. P1 cap choice is now approved, other prerequisites are not thereby met.
- `OPEN_RESOURCE_DEPENDENCY`: OP-07/08 allocation/global budgets; not settled by local caps.
- `OPEN_OPERATIONAL_DEPENDENCY`: trust/provider/rights/native/qualification; `OPEN_OPERATIONAL_DETAIL` marks unresolved causal or execution-protocol distinctions.
- `NOT_RUN`: no serializer/PG validator/application/render/provider/native test was run. HASH_RECHECK only means digest arithmetic on published bytes.

Exactly **8 stable normative rule IDs**; the explanatory tables below refine those IDs, not additional approved OP or independent implementation authorization.

## P1-01-WIRE-LIMIT — OP-01

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-01; owner record OP-01; C P1 corresponding section.

- Normative statement: Full root input W MUST be measured in actual bytes before UTF-8 decode; W≤8388608 inclusive. Count surrounding JSON whitespace and own binding. Never substitute declared Content-Length or compacted/canonical size. Bounded streaming accounting must stop growth on first excess byte; no complete heap/CPU guarantee.
- Accounting domain: Root wire bytes, not canonical bytes, hash preimage or aggregate referenced bytes.
- Boundary: 8388608 passes size guard only;8388609 denies. Initial BOM independently forbidden.
- Validation stage: 1.
- Expected error: Overflow PG_FORMAT; no accepted canonical output on overflow.
- Existing vectors/oracles: V058, V059, V026, V002, COMMON-04.
- Exclusions/dependencies: ByteRef actual aggregate size, chunk/allocation/CPU/RAM limits OPEN OP-07/08; streamed enforcement NOT_RUN.

## P1-02-DEPTH — OP-02

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-02; owner record OP-02; C P1 corresponding section.

- Normative statement: Container depth MUST be ≤64. Scalar standalone0; root object/array1; nested object/array+1; scalar leaves+0. Array/object rules identical. Real PG root remains an object under existing contract, not permission to accept scalar envelopes.
- Accounting domain: Per JSON document container nesting, not reference depth.
- Boundary: 64 accepted by depth guard;65 rejected; [] depth1,[[]] depth2,[0] depth1.
- Validation stage: 2 (while bounded parsing; before local hash).
- Expected error: PG_FORMAT on depth excess.
- Existing vectors/oracles: V054, V055, COMMON-04.
- Exclusions/dependencies: Reference depth/budget OP-08 OPEN; native recursion/allocation NOT_RUN.

## P1-03-STRING-BYTES — OP-03

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-03; owner record OP-03; C P1 corresponding section.

- Normative statement: Each decoded key/string value MUST contain ≤65536 UTF-8 bytes after unescaping into Unicode scalars. Pair high+low surrogate escapes into one scalar; reject lone surrogate. No normalization/trim/casefold. Raw escaped spelling is not decoded-byte length.
- Accounting domain: Decoded UTF-8 bytes per key/value; quotes excluded.
- Boundary: 65536 accepted by this guard;65537 rejected; 😀4 bytes,é2,e+combining accent3.
- Validation stage: 2; malformed raw UTF-8 already stage1.
- Expected error: PG_FORMAT for malformed scalar/oversized string.
- Existing vectors/oracles: V003, V004, V027, V028, V052, V053, V067, COMMON-03.
- Exclusions/dependencies: Global decoded memory OPEN OP-07; dedicated maximum-key and escaped-boundary literals missing.

## P1-04-ARRAY-CARDINALITY — OP-04

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-04; owner record OP-04; C P1 corresponding section.

- Normative statement: Each array MUST have ≤10000 elements, with any stricter field-specific cardinality still binding. Preserve order; no truncation, implicit deduplication or sort.
- Accounting domain: Elements of each array; not object members or whole graph nodes/tokens.
- Boundary: 10000 passes this guard;10001 rejects; empty array may still violate field minimum.
- Validation stage: 2 (generic cap and supplied schema cardinalities).
- Expected error: PG_FORMAT on generic excess; existing field-schema checks retained.
- Existing vectors/oracles: V056, V057, V009, V010, COMMON-04.
- Exclusions/dependencies: OP-07 total nodes/tokens/object members OPEN. This cap alone is not DoS qualification.

## P1-05-CANONICAL-BYTES — OP-05

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-05; owner record OP-05; C P1 corresponding section.

- Normative statement: Use exact PG-C14N-1 C01–C10 and B01 as detailed below. Canonical hash success MUST NOT replace schema/semantic/rights/authority checks.
- Accounting domain: Strict raw input, canonical C bytes, domain-prefixed preimage P||C, and ByteRef raw bytes are separate domains.
- Boundary: Signed64 [-9223372036854775808,9223372036854775807]; -0 canonical0; no floats/exponents; hash64 lowercasehex when supplied by existing schema.
- Validation stage: 1 strict decode;2 grammar/types/scalars;3 own binding;4 resolved ByteRef bytes.
- Expected error: PG_FORMAT before hash on malformed/type/range input; stage3 own mismatch PG_DIGEST; resolved raw length/hash mismatch stage4 PG_DIGEST; missing declared target PG_REFERENCE.
- Existing vectors/oracles: V001, V011, V017, V019, V022, V046, V047, V048, V049, V066, V067, COMMON-02, COMMON-05.
- Exclusions/dependencies: No new schema/ref/version migration approval; OP-09/22/24 OPEN; neither source authenticity nor protected storage follows.

## P1-06-ERROR-PRECEDENCE — OP-06

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-06; owner record OP-06; C P1 corresponding section.

- Normative statement: Use X01/X02 earliest failing stage and the exact residual category priority table below. A later-stage higher-priority code MUST NOT supersede an earlier failure. Primary code independent of arbitrary discovery order; bounded private diagnostics ordered by pinned declared schema/ref identity and original array index.
- Accounting domain: Established failures and validation stages, not inferred trust facts or wall-clock chronology.
- Boundary: Known stale-bound mode→PG_DIGEST stage3; corrected binding+forbidden known pair→PG_MODE stage5 after refs; unknown enum→PG_FORMAT stage2; empty required Text→PG_FORMAT stage2.
- Validation stage: All7 stages.
- Expected error: Only already-defined codes; unknown exceptions never success. Missing trust availability is not authenticated not-found/revocation.
- Existing vectors/oracles: V039, V051, V071, V072, V073, COMMON-06, P01-07, P04-01.
- Exclusions/dependencies: OPEN_OPERATIONAL_DETAIL for unresolved provider causal distinctions/within-category priorities/causal logs; no invented runtime protocol.

## P1-26-STATUS-BOUNDARY — OP-26

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-26; owner record OP-26; C P1 corresponding section.

- Normative statement: STRUCTURALLY_VALID MUST remain descriptive only. No new machine result enum. Pure result namespace remains CONSISTENT_NO_AUTHORITY/DENY; a value probe or field-shaped fixture alone MUST NOT claim whole-PG consistency or any grant.
- Accounting domain: Report annotations versus pure API result and Body05 outcome.
- Boundary: Even canonical/hash-correct synthetic E grants no execution permission.
- Validation stage: Result interpretation after applicable checks; never an added validation stage.
- Expected error: No new PG error code; insufficient whole-contract evidence cannot be promoted to success.
- Existing vectors/oracles: V019, V058, P01-01, COMMON-05.
- Exclusions/dependencies: Full semantic result/operational approval NOT_RUN; all production gates remain blocked.

## P1-27-SAFE-ERRORS — OP-27

**OWNER_APPROVED_PURE_RULE**. Source: owner task §6 OP-27; owner record OP-27; C P1 corresponding section.

- Normative statement: Retain exactly21 code/message pairs below. Separate one public primary error from private bounded diagnostics. No interpolation of raw paths/secrets/private source/reviewer identity/exception dumps. Public access/export is not granted.
- Accounting domain: Fixed public message text versus separate protected diagnostic content.
- Boundary: All21 pairs must match pinned P1 exactly; no PG_VERSION/ALLOW_RENDER/new status.
- Validation stage: Presentation after OP-06 primary selection; private causality remains separate.
- Expected error: No new code; classify only established causes. Unknown internal errors cannot become success or fabricated provider failures.
- Existing vectors/oracles: COMMON-06, NATIVE-03.
- Exclusions/dependencies: OP-21/23 publication/privacy/retention and provider behavior remain OPEN; runtime leakage tests NOT_RUN.

## Exact canonical-byte elaboration — P1-05-CANONICAL-BYTES

1. Strict scalar UTF-8, no initial BOM; exactly one JSON value with only20/09/0a/0d outer whitespace. Actual PG envelope root remains object. Literal controls must be JSON-escaped.
2. Reject duplicate keys after unescaping; no last-key-wins. Validate scalars before comparing keys. Lexicographic Unicode scalar-codepoint sequence sorting, shorter prefix first; not locale or UTF-16 ordering. Preserve every array element and its order.
3. Integer grammar `-?(0|[1-9][0-9]*)`, exact signed64. Bool is not Int. No float/exponent/NaN/Infinity. Minimal decimal, `-0`→`0`. Do not use arbitrary-precision coercion as acceptance; CPU/allocation implementation remains unqualified.
4. Canonical JSON has no outside spaces/newline/BOM; lowercase true/false/null. Missing and explicit null remain distinct; allowed null depends on existing supplied schema, not a newly approved schema.
5. Double-quote strings. Escape quote as backslash+quote, backslash as two backslashes; U+0008/000C/000A/000D/0009 as `\b/\f/\n/\r/\t`; other U+0000…001F as lowercase `\u00xx`. Other scalar values literal UTF-8; slash unescaped. No normalization.
6. After structural checks, remove **only own top-level binding_sha256** for canonical own preimage, not nested occurrences and not replacement by zeros. Hash `P || C` with SHA-256, `P=hex:53746f727953747564696f2f50472d4331344e2d3100`. Own binding stays mandatory in actual full envelope. Raw ByteRef is `SHA256(actual whole raw bytes)` with actual byte_length; no prefix hash, no automatic network/path resolver. Git SHA-1/G2/SI hashes are not substitutes.

## Residual deterministic selection — P1-06-ERROR-PRECEDENCE

The following is the adopted fixed-category option from C P1 §6, not its alternative canonical-walk-first option. For equal public codes use canonical declared schema-field/ref-identity order for bounded diagnostics, array indices in original order; exact future schema/provider diagnostic vocabulary is not introduced here.

| Stage | Fixed selection within earliest failed stage | Unresolved boundary |
|---|---|---|
| 1 bounded input/decode | PG_FORMAT; guard before unbounded growth; private bounded-input reason before decode reason | Chunk sizes and memory proof OPEN_RESOURCE_DEPENDENCY |
| 2 grammar/duplicates/schema/types/known enum | PG_FORMAT; deterministic declared-field diagnostics, no raw key echo | This does not freeze new schemas/field registries |
| 3 local binding | PG_DIGEST only after successful structure; malformed Hash is earlier stage2 PG_FORMAT | No hashing malformed input as accepted result |
| 4 reference/dependency validation | PG_FORMAT(target/resource shape) before PG_REFERENCE(registry/typed link) before PG_DIGEST(resolved bytes), for established same-stage failures | OP-07/08 supply future resource limits; supplied missing ref differs from unavailable provider |
| 5 mode/subject | PG_MODE before PG_REFERENCE before PG_SCOPE | Only after successful earlier stages |
| 6 product/rights/trusted state | Established categories: verified-context availability → identity/authority/history → revocation → expiry → evaluation/currentness → product → rights | Group order frozen; unresolved provider-specific causal distinction or order within grouped categories is OPEN_OPERATIONAL_DETAIL. Do not invent authenticated findings to fill a group |
| 7 execution/evidence | Established dependency/history loss before PG_EXECUTION before PG_INCOMPLETE before PG_DIGEST(actual-byte tamper) before PG_EVIDENCE(unsupported commit claim) | Ordering between dependency/history causes and observed chronology is OPEN_OPERATIONAL_DETAIL; no invented causal log or trusted executor |

X01 empty required why_film→PG_FORMAT(stage2); nonempty insufficient rationale→PG_PRODUCT_GAP(stage6) only with established unmet predicate and earlier stages satisfied. X02 known forbidden mode+stale binding→PG_DIGEST(stage3), known forbidden mode+correct binding→PG_MODE(stage5), unknown enum→PG_FORMAT(stage2). An actual missing supplied dependency maps to PG_REFERENCE; a genuinely unavailable required trusted dependency may map PG_DEPENDENCY_UNAVAILABLE at its applicable stage. Unknown exception must deny without raw public details; precise provider/exception classification remains OPEN_OPERATIONAL_DETAIL where unspecified. No fabricated success, code or authority is allowed.

X03 abstract DAG/cycle cases do not prove crypto closure; X04 exact raw plan hash binds mandatory toolchain/executor refs with no caller override. P1 does not implement/migrate those contracts or approve OP-08/09/22/24.

## Fixed safe public-message mapping — P1-27-SAFE-ERRORS

Copied byte-for-byte as code/message values from C P1 §8, not public export permission. The21 codes are compared against the explicit pinned A catalogue sentence, not PG-like token counting.

| Code | Fixed public message |
|---|---|
| PG_FORMAT | Данные не соответствуют формату. |
| PG_DIGEST | Контрольная сумма не совпала. |
| PG_REFERENCE | Связанные данные не подтверждены. |
| PG_EVALUATION | Оценка не подходит для этого перехода. |
| PG_STALE | Связанные данные требуют обновления. |
| PG_PRODUCT_GAP | Не закрыты содержательные требования. |
| PG_IDENTITY | Личность не подтверждена. |
| PG_AUTHORITY | Полномочия не подтверждены. |
| PG_HISTORY | История решений не подтверждена. |
| PG_REVOKED | Решение нельзя использовать. |
| PG_EXPIRED | Период действия завершён. |
| PG_RIGHTS | Права для заданного использования не подтверждены. |
| PG_SCOPE | Действие выходит за заданные границы. |
| PG_MODE | Режим не подходит для этого контракта. |
| PG_REPLAY | Попытку нельзя повторить этим запросом. |
| PG_PATH | Место выполнения не прошло проверку. |
| PG_TOOLCHAIN | Набор инструментов не подтверждён. |
| PG_EXECUTION | Выполнение не завершилось успешно. |
| PG_INCOMPLETE | Результат неполон. |
| PG_EVIDENCE | Свидетельства выполнения не подтверждены. |
| PG_DEPENDENCY_UNAVAILABLE | Обязательная зависимость недоступна. |

Private diagnostics may carry bounded reason identifiers/stage/opaque references only under a separately decided protected policy. No actual limits, retention, reviewer disclosure or public transport policy are invented. No raw exception/private text fallback. Operational tests NOT_RUN.

**STOP — docs-only; implementation, production permissions and final PG freeze remain unauthorized.**
