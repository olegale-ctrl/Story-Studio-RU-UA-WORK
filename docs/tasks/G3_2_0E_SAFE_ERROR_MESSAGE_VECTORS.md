# P1 —21 safe-message projection vectors

**DOCS_ONLY + OFFLINE_VECTOR_VERIFICATION — NO PRODUCTION AUTHORITY**

SI-INTEGRATION-G3.2.0e; 2026-11-17 (Europe/Kyiv). G3.2.0d ACCEPTED_DOCS_ONLY; only OP-01–06/26/27 approved pure-contract.

Source: [D P1-27-SAFE-ERRORS](G3_2_0D_P1_NORMATIVE_CONTRACT.md), exact21 code/message table. Underlying oracle COMMON-06; privacy/access boundary NATIVE-03 is not exercised. Common exact PRIVATE, INPUT and PUBLIC byte recipes are in [fixture spec](G3_2_0E_VECTOR_FIXTURE_SPEC.md). IDs here are exactly21 main E vectors, no provider simulations or new PG codes.

Input primary code is **already established**, not inferred from private data or a fake authority provider. Each vector checks the finite relation `established_code → fixed_safe_message`, exact code/message UTF8 comparison and absence of all four markers from its exact expected public output. This documents/checks an expected projection; no application projector was implemented or run. These checks do not prove actual runtime redaction/publication behavior. No new Error schema, fallback exception dump, result enum or grant.

PRIVATE markers (all ASCII; synthetic): E_PRIVATE_PATH_7f91, E_PRIVATE_SOURCE_7f91, E_PRIVATE_REVIEWER_7f91, E_PRIVATE_EXCEPTION_7f91. No raw paths/source/reviewer/exception from a real system are used. Output must contain only the exact code and message in the fixture wrapper; it carries no permit/production-authority field. Publication/access/retention policy OP-21/23 remains unapproved. RAW/DOMAIN N/A: neither plain public text nor this observation wrapper is an accepted PG envelope/hash preimage.

## E-V008 — CM-074

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_FORMAT)`, **319 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_FORMAT`.
- Exact safe message (60 UTF8 bytes): **Данные не соответствуют формату.**
- Exact expected public UTF8 output (93 bytes, no LF):

```json
{"code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V009 — CM-075

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_DIGEST)`, **319 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_DIGEST`.
- Exact safe message (54 UTF8 bytes): **Контрольная сумма не совпала.**
- Exact expected public UTF8 output (87 bytes, no LF):

```json
{"code":"PG_DIGEST","message":"Контрольная сумма не совпала."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V010 — CM-076

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_REFERENCE)`, **322 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_REFERENCE`.
- Exact safe message (62 UTF8 bytes): **Связанные данные не подтверждены.**
- Exact expected public UTF8 output (98 bytes, no LF):

```json
{"code":"PG_REFERENCE","message":"Связанные данные не подтверждены."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V011 — CM-077

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_EVALUATION)`, **323 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_EVALUATION`.
- Exact safe message (70 UTF8 bytes): **Оценка не подходит для этого перехода.**
- Exact expected public UTF8 output (107 bytes, no LF):

```json
{"code":"PG_EVALUATION","message":"Оценка не подходит для этого перехода."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V012 — CM-078

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_STALE)`, **318 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_STALE`.
- Exact safe message (68 UTF8 bytes): **Связанные данные требуют обновления.**
- Exact expected public UTF8 output (100 bytes, no LF):

```json
{"code":"PG_STALE","message":"Связанные данные требуют обновления."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V013 — CM-079

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_PRODUCT_GAP)`, **324 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_PRODUCT_GAP`.
- Exact safe message (70 UTF8 bytes): **Не закрыты содержательные требования.**
- Exact expected public UTF8 output (108 bytes, no LF):

```json
{"code":"PG_PRODUCT_GAP","message":"Не закрыты содержательные требования."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V014 — CM-080

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_IDENTITY)`, **321 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_IDENTITY`.
- Exact safe message (47 UTF8 bytes): **Личность не подтверждена.**
- Exact expected public UTF8 output (82 bytes, no LF):

```json
{"code":"PG_IDENTITY","message":"Личность не подтверждена."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V015 — CM-081

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_AUTHORITY)`, **322 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_AUTHORITY`.
- Exact safe message (51 UTF8 bytes): **Полномочия не подтверждены.**
- Exact expected public UTF8 output (87 bytes, no LF):

```json
{"code":"PG_AUTHORITY","message":"Полномочия не подтверждены."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V016 — CM-082

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_HISTORY)`, **320 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_HISTORY`.
- Exact safe message (60 UTF8 bytes): **История решений не подтверждена.**
- Exact expected public UTF8 output (94 bytes, no LF):

```json
{"code":"PG_HISTORY","message":"История решений не подтверждена."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V017 — CM-083

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_REVOKED)`, **320 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_REVOKED`.
- Exact safe message (53 UTF8 bytes): **Решение нельзя использовать.**
- Exact expected public UTF8 output (87 bytes, no LF):

```json
{"code":"PG_REVOKED","message":"Решение нельзя использовать."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V018 — CM-084

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_EXPIRED)`, **320 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_EXPIRED`.
- Exact safe message (47 UTF8 bytes): **Период действия завершён.**
- Exact expected public UTF8 output (81 bytes, no LF):

```json
{"code":"PG_EXPIRED","message":"Период действия завершён."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V019 — CM-085

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_RIGHTS)`, **319 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_RIGHTS`.
- Exact safe message (94 UTF8 bytes): **Права для заданного использования не подтверждены.**
- Exact expected public UTF8 output (127 bytes, no LF):

```json
{"code":"PG_RIGHTS","message":"Права для заданного использования не подтверждены."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V020 — CM-086

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_SCOPE)`, **318 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_SCOPE`.
- Exact safe message (69 UTF8 bytes): **Действие выходит за заданные границы.**
- Exact expected public UTF8 output (101 bytes, no LF):

```json
{"code":"PG_SCOPE","message":"Действие выходит за заданные границы."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V021 — CM-087

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_MODE)`, **317 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_MODE`.
- Exact safe message (70 UTF8 bytes): **Режим не подходит для этого контракта.**
- Exact expected public UTF8 output (101 bytes, no LF):

```json
{"code":"PG_MODE","message":"Режим не подходит для этого контракта."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V022 — CM-088

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_REPLAY)`, **319 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_REPLAY`.
- Exact safe message (73 UTF8 bytes): **Попытку нельзя повторить этим запросом.**
- Exact expected public UTF8 output (106 bytes, no LF):

```json
{"code":"PG_REPLAY","message":"Попытку нельзя повторить этим запросом."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V023 — CM-089

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_PATH)`, **317 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_PATH`.
- Exact safe message (67 UTF8 bytes): **Место выполнения не прошло проверку.**
- Exact expected public UTF8 output (98 bytes, no LF):

```json
{"code":"PG_PATH","message":"Место выполнения не прошло проверку."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V024 — CM-090

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_TOOLCHAIN)`, **322 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_TOOLCHAIN`.
- Exact safe message (64 UTF8 bytes): **Набор инструментов не подтверждён.**
- Exact expected public UTF8 output (100 bytes, no LF):

```json
{"code":"PG_TOOLCHAIN","message":"Набор инструментов не подтверждён."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V025 — CM-091

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_EXECUTION)`, **322 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_EXECUTION`.
- Exact safe message (64 UTF8 bytes): **Выполнение не завершилось успешно.**
- Exact expected public UTF8 output (100 bytes, no LF):

```json
{"code":"PG_EXECUTION","message":"Выполнение не завершилось успешно."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V026 — CM-092

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_INCOMPLETE)`, **323 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_INCOMPLETE`.
- Exact safe message (34 UTF8 bytes): **Результат неполон.**
- Exact expected public UTF8 output (71 bytes, no LF):

```json
{"code":"PG_INCOMPLETE","message":"Результат неполон."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V027 — CM-093

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_EVIDENCE)`, **321 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_EVIDENCE`.
- Exact safe message (78 UTF8 bytes): **Свидетельства выполнения не подтверждены.**
- Exact expected public UTF8 output (113 bytes, no LF):

```json
{"code":"PG_EVIDENCE","message":"Свидетельства выполнения не подтверждены."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## E-V028 — CM-094

Rule `P1-27-SAFE-ERRORS`; OP-27. Layer SAFE_MESSAGE_PROJECTION_ORACLE. Status **VERIFIED_OFFLINE** (finite fixture checks only).

- Exact input: `INPUT(PG_DEPENDENCY_UNAVAILABLE)`, **335 ASCII bytes**; exact PRIVATE shared recipe unchanged.
- Established primary code: `PG_DEPENDENCY_UNAVAILABLE`.
- Exact safe message (69 UTF8 bytes): **Обязательная зависимость недоступна.**
- Exact expected public UTF8 output (118 bytes, no LF):

```json
{"code":"PG_DEPENDENCY_UNAVAILABLE","message":"Обязательная зависимость недоступна."}
```

Actual finite verification: authored code/message equals pinned table exactly (including punctuation/spaces/Unicode); public wrapper contains exactly code/message; all four PRIVATE markers are present in input and absent from expected output. No cause/provider behavior or real public export was tested. Runtime projector, protected diagnostic storage, rights/authority and native leakage enforcement: **NOT_RUN**.

## Non-claims and negative extensions

Exactly21 principal vectors; unknown-code handling and actual interpolation vulnerabilities are not newly specified. No fallback public code/message is invented for unknown codes. A future unknown-code or malicious runtime interpolation test requires separate contract/implementation scope. Here every expected output is fixed independently of PRIVATE; arithmetic/input/output byte equality was checked, not behavior of unimplemented runtime software.

**STOP — no production authority or G3.2.1. Whole package remains BLOCKED_CONTRACT for E-V007/CM-069, independently of these21 completed documentary fixtures.**
