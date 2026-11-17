# Root accounting —27 finite G-N vectors

**DOCS_ONLY + OFFLINE_VECTORS. F-D02/A and F-D03/A: APPROVED_LIMITED_SCOPE.**

SI-INTEGRATION-G3.2.0g; 2026-11-17 (Europe/Kyiv). No implementation, PG API, production authority or G3.2.1.

Source: [root accounting contract](G3_2_0G_ROOT_ACCOUNTING_CONTRACT.md), G-AC-01–05; [owner approval](G3_2_0G_OWNER_APPROVAL_FD02_FD03.md), F-D02/A. Token detail is **FIXTURE_LOCAL_PROPOSAL**, not global runtime tokenization. Input recipes are exact raw bytes, no implicit BOM/LF; explicit hex0a in G-N019 is data. `hex:` decodes pairs, `||` concatenates bytes, `X^n` repeats exactly n times. A10000 in G-N022 is exactly G-N020 input. No megabyte literal or hidden files.

Counter tuple order is **(N_value,N_key,N_total,M_total,T,D_key,D_string,D_total)**. Every expected tuple below was authored separately from both counting algorithms. MethodsA/B are the actual independently implemented offline counting routes described in contract. Each row is VERIFIED_OFFLINE for bytes/counts only. All27 inputs have complete valid JSON syntax; G-N012/013 have prohibited duplicate decoded keys; G-N021/024 exceed an existing local guard. There are no malformed-prefix vectors and no selected global budget/novel resource rejection.

| ID | Expected wire bytes | Actual wire bytes | Expected tuple | MethodA actual | MethodB actual |
|---|---:|---:|---|---|---|
| G-N001 | 4 | 4 | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) |
| G-N002 | 4 | 4 | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) |
| G-N003 | 1 | 1 | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) |
| G-N004 | 2 | 2 | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) | (1, 0, 1, 0, 1, 0, 0, 0) |
| G-N005 | 2 | 2 | (1, 0, 1, 0, 2, 0, 0, 0) | (1, 0, 1, 0, 2, 0, 0, 0) | (1, 0, 1, 0, 2, 0, 0, 0) |
| G-N006 | 2 | 2 | (1, 0, 1, 0, 2, 0, 0, 0) | (1, 0, 1, 0, 2, 0, 0, 0) | (1, 0, 1, 0, 2, 0, 0, 0) |
| G-N007 | 3 | 3 | (2, 0, 2, 0, 3, 0, 0, 0) | (2, 0, 2, 0, 3, 0, 0, 0) | (2, 0, 2, 0, 3, 0, 0, 0) |
| G-N008 | 13 | 13 | (4, 0, 4, 0, 7, 0, 0, 0) | (4, 0, 4, 0, 7, 0, 0, 0) | (4, 0, 4, 0, 7, 0, 0, 0) |
| G-N009 | 4 | 4 | (2, 0, 2, 0, 4, 0, 0, 0) | (2, 0, 2, 0, 4, 0, 0, 0) | (2, 0, 2, 0, 4, 0, 0, 0) |
| G-N010 | 7 | 7 | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) |
| G-N011 | 17 | 17 | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) |
| G-N012 | 13 | 13 | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) |
| G-N013 | 18 | 18 | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) |
| G-N014 | 8 | 8 | (2, 1, 3, 1, 5, 2, 0, 2) | (2, 1, 3, 1, 5, 2, 0, 2) | (2, 1, 3, 1, 5, 2, 0, 2) |
| G-N015 | 10 | 10 | (2, 1, 3, 1, 5, 1, 2, 3) | (2, 1, 3, 1, 5, 1, 2, 3) | (2, 1, 3, 1, 5, 1, 2, 3) |
| G-N016 | 14 | 14 | (1, 0, 1, 0, 1, 0, 4, 4) | (1, 0, 1, 0, 1, 0, 4, 4) | (1, 0, 1, 0, 1, 0, 4, 4) |
| G-N017 | 10 | 10 | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) |
| G-N018 | 19 | 19 | (5, 2, 7, 2, 13, 2, 1, 3) | (5, 2, 7, 2, 13, 2, 1, 3) | (5, 2, 7, 2, 13, 2, 1, 3) |
| G-N019 | 14 | 14 | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) |
| G-N020 | 20001 | 20001 | (10001, 0, 10001, 0, 20001, 0, 0, 0) | (10001, 0, 10001, 0, 20001, 0, 0, 0) | (10001, 0, 10001, 0, 20001, 0, 0, 0) |
| G-N021 | 20003 | 20003 | (10002, 0, 10002, 0, 20003, 0, 0, 0) | (10002, 0, 10002, 0, 20003, 0, 0, 0) | (10002, 0, 10002, 0, 20003, 0, 0, 0) |
| G-N022 | 40005 | 40005 | (20003, 0, 20003, 0, 40005, 0, 0, 0) | (20003, 0, 20003, 0, 40005, 0, 0, 0) | (20003, 0, 20003, 0, 40005, 0, 0, 0) |
| G-N023 | 65538 | 65538 | (1, 0, 1, 0, 1, 0, 65536, 65536) | (1, 0, 1, 0, 1, 0, 65536, 65536) | (1, 0, 1, 0, 1, 0, 65536, 65536) |
| G-N024 | 65539 | 65539 | (1, 0, 1, 0, 1, 0, 65537, 65537) | (1, 0, 1, 0, 1, 0, 65537, 65537) | (1, 0, 1, 0, 1, 0, 65537, 65537) |
| G-N025 | 17 | 17 | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) | (3, 2, 5, 2, 9, 2, 0, 2) |
| G-N026 | 6 | 6 | (1, 0, 1, 0, 1, 0, 4, 4) | (1, 0, 1, 0, 1, 0, 4, 4) | (1, 0, 1, 0, 1, 0, 4, 4) |
| G-N027 | 12 | 12 | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) | (2, 1, 3, 1, 5, 1, 0, 1) |

## Exact fixtures and scoped expectations

### G-N001

- Exact byte recipe: `hex:6e756c6c`.
- Expected/actual wire length: **4/4 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Root null; JSON scalar is not PG envelope.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N002

- Exact byte recipe: `hex:74727565`.
- Expected/actual wire length: **4/4 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Root boolean.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N003

- Exact byte recipe: `hex:30`.
- Expected/actual wire length: **1/1 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Root integer.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N004

- Exact byte recipe: `hex:2d30`.
- Expected/actual wire length: **2/2 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Negative-zero lexical representation; existing C14N rule remains0.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N005

- Exact byte recipe: `hex:5b5d`.
- Expected/actual wire length: **2/2 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 2, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Empty array has2 tokens.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N006

- Exact byte recipe: `hex:7b7d`.
- Expected/actual wire length: **2/2 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 2, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Empty object; absence control for G-N017.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N007

- Exact byte recipe: `hex:5b305d`.
- Expected/actual wire length: **3/3 bytes**.
- Exact expected tuple: `(2, 0, 2, 0, 3, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: One scalar array.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N008

- Exact byte recipe: `hex:5b302c747275652c6e756c6c5d`.
- Expected/actual wire length: **13/13 bytes**.
- Exact expected tuple: `(4, 0, 4, 0, 7, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Three scalar array.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N009

- Exact byte recipe: `hex:5b5b5d5d`.
- Expected/actual wire length: **4/4 bytes**.
- Exact expected tuple: `(2, 0, 2, 0, 4, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Nested arrays; depth2 vs nodes2.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N010

- Exact byte recipe: `hex:7b2261223a307d`.
- Expected/actual wire length: **7/7 bytes**.
- Exact expected tuple: `(2, 1, 3, 1, 5, 1, 0, 1)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: One-member object.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N011

- Exact byte recipe: `hex:7b2261223a302c2262223a66616c73657d`.
- Expected/actual wire length: **17/17 bytes**.
- Exact expected tuple: `(3, 2, 5, 2, 9, 2, 0, 2)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Two-member object.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N012

- Exact byte recipe: `hex:7b2261223a302c2261223a317d`.
- Expected/actual wire length: **13/13 bytes**.
- Exact expected tuple: `(3, 2, 5, 2, 9, 2, 0, 2)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON with prohibited duplicate decoded keys**.
- Applicable rule/status: PG_FORMAT stage2 expected for duplicate keys; accounting does not imply admission. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Duplicate decoded keys both counted.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N013

- Exact byte recipe: `hex:7b2261223a302c225c7530303631223a317d`.
- Expected/actual wire length: **18/18 bytes**.
- Exact expected tuple: `(3, 2, 5, 2, 9, 2, 0, 2)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON with prohibited duplicate decoded keys**.
- Applicable rule/status: PG_FORMAT stage2 expected for duplicate keys; accounting does not imply admission. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Escaped duplicate a still adds a key/member.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N014

- Exact byte recipe: `hex:7b22c3a9223a307d`.
- Expected/actual wire length: **8/8 bytes**.
- Exact expected tuple: `(2, 1, 3, 1, 5, 2, 0, 2)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: One codepoint key has2 UTF8 bytes.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N015

- Exact byte recipe: `hex:7b2261223a22c3a9227d`.
- Expected/actual wire length: **10/10 bytes**.
- Exact expected tuple: `(2, 1, 3, 1, 5, 1, 2, 3)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Multibyte string value separately counted.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N016

- Exact byte recipe: `hex:225c75643833645c756465303022`.
- Expected/actual wire length: **14/14 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 4, 4)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Paired escapes decode1 scalar/4 UTF8 bytes.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N017

- Exact byte recipe: `hex:7b2261223a6e756c6c7d`.
- Expected/actual wire length: **10/10 bytes**.
- Exact expected tuple: `(2, 1, 3, 1, 5, 1, 0, 1)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Explicit null adds value,key,member vs G-N006.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N018

- Exact byte recipe: `hex:7b2261223a5b302c7b2262223a2278227d5d7d`.
- Expected/actual wire length: **19/19 bytes**.
- Exact expected tuple: `(5, 2, 7, 2, 13, 2, 1, 3)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Mixed nested object/array.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N019

- Exact byte recipe: `hex207b20226122203a2030207d200a`.
- Expected/actual wire length: **14/14 bytes**.
- Exact expected tuple: `(2, 1, 3, 1, 5, 1, 0, 1)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Same decoded value as G-N010; whitespace counts wire only.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N020

- Exact byte recipe: `hex5b30 || (hex2c30)^9999 || hex5d`.
- Expected/actual wire length: **20001/20001 bytes**.
- Exact expected tuple: `(10001, 0, 10001, 0, 20001, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Array10000 boundary; cardinality guard only.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N021

- Exact byte recipe: `hex5b30 || (hex2c30)^10000 || hex5d`.
- Expected/actual wire length: **20003/20003 bytes**.
- Exact expected tuple: `(10002, 0, 10002, 0, 20003, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: PG_FORMAT stage2 expected for existing local array cap only. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Array10001; existing local cardinality PG_FORMAT expected.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N022

- Exact byte recipe: `hex5b || A10000 || hex2c || A10000 || hex5d, A10000=G-N020 input`.
- Expected/actual wire length: **40005/40005 bytes**.
- Exact expected tuple: `(20003, 0, 20003, 0, 40005, 0, 0, 0)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Each array≤10000 but20003 total nodes; no selected global cap.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N023

- Exact byte recipe: `hex22 || hex(c3a9)^32768 || hex22`.
- Expected/actual wire length: **65538/65538 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 65536, 65536)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Decoded string65536 byte boundary.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N024

- Exact byte recipe: `hex22 || hex(c3a9)^32768 || hex78 || hex22`.
- Expected/actual wire length: **65539/65539 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 65537, 65537)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: PG_FORMAT stage2 expected for existing local decoded-string cap only. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Decoded string65537; existing local byte cap PG_FORMAT expected.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N025

- Exact byte recipe: `hex:7b2262223a66616c73652c2261223a307d`.
- Expected/actual wire length: **17/17 bytes**.
- Exact expected tuple: `(3, 2, 5, 2, 9, 2, 0, 2)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Object order permutation G-N011 leaves counts unchanged.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N026

- Exact byte recipe: `hex:22f09f988022`.
- Expected/actual wire length: **6/6 bytes**.
- Exact expected tuple: `(1, 0, 1, 0, 1, 0, 4, 4)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Same scalar value as G-N016; literal vs escape wire length.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

### G-N027

- Exact byte recipe: `hex:7b225c7530303631223a307d`.
- Expected/actual wire length: **12/12 bytes**.
- Exact expected tuple: `(2, 1, 3, 1, 5, 1, 0, 1)`; A/B actual tuples equal expected in table.
- Classification: **Complete valid JSON**.
- Applicable rule/status: Accounting fact only; no full PG verdict or new global-limit denial. Existing-code outcomes are expected isolated-rule oracles, **not PG validator results**.
- Property isolated: Escaped key equals G-N010 without duplicate.
- Actual verification: **VERIFIED_OFFLINE**; reproduce recipe and apply both methods; no accepted canonical digest computed.

## Required relationships and independent reproduction

- G-N010/G-N019/G-N027 decode the same unique-key JSON value with wire lengths7/14/12. Counts agree; whitespace and escape spelling are not decoded D.
- G-N011/G-N025 have the same unique-key member mapping, different member encounter order, identical counts. Their pairs-preserving tree sequences intentionally differ in order; counting does not.
- G-N012/G-N013 count2 keys/2 members despite equal decoded key name a; accounting does not grant admission. Neither method collapses duplicate occurrences before counting.
- G-N014 key é:1 codepoint/2 decodedUTF8 bytes. G-N016/G-N026:1 scalar/4 decoded bytes, wire14/6 respectively. No Unicode normalization/hash change.
- G-N017 explicit null versus G-N006 absence changes members/keys/value nodes. Missing and null are not coercible.
- G-N020/G-N021 local cardinality10000/10001 uses existing P1-04 expectation only. G-N022 has root cardinality2 and each child cardinality10000 yet N_total20003, demonstrating absence of a global work bound from per-array cardinality.
- G-N023/G-N024 decoded string65536/65537 uses existing P1-03 expectation only. Full-fixture totals do not define production early-reject counters.

Actual command:

```text
python /workspace/work/g320g-scratch/verify_accounting.py
```

CPython3.12.14, final exit0. MethodA: byte-token grammar traversal counts values/key roles/members, lexical tokens and decoded byte lengths with separately implemented escape/pair decoding. MethodB: stdlib complete JSON parsing with object_pairs_hook preserving every pair; a separate tree walk counts nodes/member/key occurrences and derives braces/brackets/comma/colon totals arithmetically. Neither uses expected tuples to obtain actual counts; normal dictionary parsing is not used for duplicate occurrence counts. Shared Python execution is not independent human acceptance; counting logic is separate, not a claim of two production parsers.

Harness note: an initial extra semantic check incorrectly compared pair-list sequence equality for G-N011/G-N025 (exit1), although all27 declared lengths/tuples had already matched A/B. That control was corrected to mapping equality for these unique-key objects only. No fixture input, expected length or expected tuple was changed. No actual counting disagreement was observed or hidden. Future genuine counting disagreement requires BLOCKED_VERIFICATION, no automatic expected-value adjustment.

All runtime PG/parser/allocator/provider/Windows/production behavior **NOT_RUN**. These27 fixtures do not close CM-022, complete OP-07 or select new caps. **STOP.**
