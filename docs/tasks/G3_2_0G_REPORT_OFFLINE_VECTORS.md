# External report —12 finite G-R examples

**DOCS_ONLY + OFFLINE_VECTORS. F-D02/A and F-D03/A: APPROVED_LIMITED_SCOPE.**

SI-INTEGRATION-G3.2.0g; 2026-11-17 (Europe/Kyiv). No implementation, PG API, production authority or G3.2.1.

Source: [report direction/conventions](G3_2_0G_NON_AUTHORITY_REPORT_CONTRACT.md), G-RP-01/02/03/04 and local G-RP-L01; [owner approval](G3_2_0G_OWNER_APPROVAL_FD02_FD03.md) F-D03/A. Every shown object/order/empty summary is **FIXTURE_LOCAL_NON_NORMATIVE**, not a new PG API/schema/serializer or report hash domain. Normative derivation is limited to existing verdict namespace and approved message text where applicable; scenario meanings and transport syntax are illustrative.

Input scenario uses only synthetic privately held observations or stipulated verdict/code. No real provider/rights/identity evidence is created. Empty public summary means no verdict reported in that local example, not an additional machine result or PG rejection code. Code/message pairs are exact D P1-27 values. No message for CONSISTENT_NO_AUTHORITY is supplied.

| ID | Exact public UTF8 bytes | Independent scalar-width length | Supplied verdict | Supplied code |
|---|---:|---:|---|---|
| G-R001 | 37 | 37 | CONSISTENT_NO_AUTHORITY | N/A; not invented |
| G-R002 | 104 | 104 | DENY | PG_DIGEST |
| G-R003 | 110 | 110 | DENY | PG_FORMAT |
| G-R004 | 110 | 110 | DENY | PG_FORMAT |
| G-R005 | 110 | 110 | DENY | PG_FORMAT |
| G-R006 | 2 | 2 | Not established/not reported | N/A; not invented |
| G-R007 | 2 | 2 | Not established/not reported | N/A; not invented |
| G-R008 | 110 | 110 | DENY | PG_FORMAT |
| G-R009 | 110 | 110 | DENY | PG_FORMAT |
| G-R010 | 110 | 110 | DENY | PG_FORMAT |
| G-R011 | 110 | 110 | DENY | PG_FORMAT |
| G-R012 | 2 | 2 | Not established/not reported | N/A; not invented |

## Exact finite examples

### G-R001

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: An existing full pure verdict is stipulated CONSISTENT_NO_AUTHORITY, not established by a shape-only fixture.

Exact existing verdict/code/message where applicable: CONSISTENT_NO_AUTHORITY / no code / no message invented.

Exact public UTF8 line, no LF/BOM (37 bytes):

```json
{"verdict":"CONSISTENT_NO_AUTHORITY"}
```

Exact hex: `7b2276657264696374223a22434f4e53495354454e545f4e4f5f415554484f52495459227d`.

Separately held synthetic private tokens/field names: None supplied; no private API/evidence schema inferred.

Expected separation: Pure verdict premise only; no code/message approved for this verdict is invented.

Forbidden interpretation: Using pure consistency as execution/render/rights permission.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R002

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Established DENY/PG_DIGEST is a premise, independently of report projection.

Exact existing verdict/code/message where applicable: DENY / PG_DIGEST / Контрольная сумма не совпала..

Exact public UTF8 line, no LF/BOM (104 bytes):

```json
{"verdict":"DENY","code":"PG_DIGEST","message":"Контрольная сумма не совпала."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f444947455354222c226d657373616765223a22d09ad0bed0bdd182d180d0bed0bbd18cd0bdd0b0d18f20d181d183d0bcd0bcd0b020d0bdd0b520d181d0bed0b2d0bfd0b0d0bbd0b02e227d`.

Separately held synthetic private tokens/field names: None supplied; no private API/evidence schema inferred.

Expected separation: Exact approved PG_DIGEST safe RU message; verdict not produced by a validator.

Forbidden interpretation: Treating integrity failure summary as an authenticated operational finding or permission.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R003

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Established DENY/PG_FORMAT premise; finite stage2 format summary.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: None supplied; no private API/evidence schema inferred.

Expected separation: Exact approved PG_FORMAT text; not an implementation test result.

Forbidden interpretation: Claiming a real PG validator ran.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R004

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: A private observation describes revision bool type; primary PG_FORMAT supplied.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: `revision`, `G_PRIVATE_TYPE_4f20`.

Expected separation: Private observation stays outside public fixture.

Forbidden interpretation: Private observation presence as publication permission.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R005

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Two private observations (revision and binding length), same established primary PG_FORMAT.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: `revision`, `binding_sha256`, `G_PRIVATE_HASH_4f20`, `INVALID_DECLARED_TYPE`, `INVALID_HASH_LENGTH`.

Expected separation: Multiplicity does not change fixed safe public message; no new private ordinal registry.

Forbidden interpretation: Publicly listing private reason labels or inventing new diagnostic enums.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R006

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Required evidence is unknown/unavailable; no pure verdict or operational cause has been established.

Exact existing verdict/code/message where applicable: No pure verdict/code established; no PG result invented.

Exact public UTF8 line, no LF/BOM (2 bytes):

```json
{}
```

Exact hex: `7b7d`.

Separately held synthetic private tokens/field names: `G_PRIVATE_UNKNOWN_4f20`.

Expected separation: Withheld fixture-local public summary; no new UNKNOWN machine verdict, no revoked/not-found finding.

Forbidden interpretation: Turning unknown/unavailable into an authenticated negative or a supplied DENY/PG_* result.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R007

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: A descriptive STRUCTURALLY_VALID annotation exists; full pure verdict unestablished.

Exact existing verdict/code/message where applicable: No pure verdict/code established; no PG result invented.

Exact public UTF8 line, no LF/BOM (2 bytes):

```json
{}
```

Exact hex: `7b7d`.

Separately held synthetic private tokens/field names: `STRUCTURALLY_VALID`.

Expected separation: Description remains separately held; no structural machine verdict.

Forbidden interpretation: Promoting description to CONSISTENT_NO_AUTHORITY or operation permission.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R008

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Established DENY/PG_FORMAT supplied; actual runtime-effect observation is NOT_RUN.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: `G_PRIVATE_EFFECT_UNOBSERVED_4f20`.

Expected separation: No runtime-effect field in public fixture; absence proves nothing about real effects.

Forbidden interpretation: Claiming zero effects from a missing field or correct DENY.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R009

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Established PG_FORMAT with separately held synthetic private field names.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: `reviewer_identity`, `source_text`, `diagnostic_path`.

Expected separation: Private names do not appear as public keys/text.

Forbidden interpretation: Treating safe public bytes as proof real logs, ACLs or retention are safe.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R010

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Established PG_FORMAT with four artificial path/source/reviewer/exception markers.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: `G_PRIVATE_PATH_4f20:/synthetic/input`, `G_PRIVATE_SOURCE_4f20:synthetic unpublished`, `G_PRIVATE_REVIEWER_4f20:fixture-only`, `G_PRIVATE_EXCEPTION_4f20:synthetic error`.

Expected separation: Each marker absent in exact public UTF8 fixture.

Forbidden interpretation: Claiming actual runtime redaction or real reviewer/provider qualification.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R011

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Different private format cause than G-R004: malformed nonempty field value, same established PG_FORMAT.

Exact existing verdict/code/message where applicable: DENY / PG_FORMAT / Данные не соответствуют формату..

Exact public UTF8 line, no LF/BOM (110 bytes):

```json
{"verdict":"DENY","code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Exact hex: `7b2276657264696374223a2244454e59222c22636f6465223a2250475f464f524d4154222c226d657373616765223a22d094d0b0d0bdd0bdd18bd0b520d0bdd0b520d181d0bed0bed182d0b2d0b5d182d181d182d0b2d183d18ed18220d184d0bed180d0bcd0b0d182d1832e227d`.

Separately held synthetic private tokens/field names: `G_PRIVATE_VALUE_4f20`.

Expected separation: Public bytes exactly equal G-R003/004/005 despite different supplied causes.

Forbidden interpretation: Inferring private cause or authenticated identity from fixed public message.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

### G-R012

**FIXTURE_LOCAL_NON_NORMATIVE; VERIFIED_OFFLINE for expected fixture bytes only.**

Input scenario: Unrecognised fixture-local input convention g-example/99 with an extra synthetic field; no PG verdict established.

Exact existing verdict/code/message where applicable: No pure verdict/code established; no PG result invented.

Exact public UTF8 line, no LF/BOM (2 bytes):

```json
{}
```

Exact hex: `7b7d`.

Separately held synthetic private tokens/field names: `g-example/99`, `G_PRIVATE_EXTRA_4f20`.

Expected separation: Withheld fixture-local public summary; no global schema/version rule, no new PG error.

Forbidden interpretation: Treating unsupported local fields/version as adopted PG API or authority.

Derivation/limit: Existing verdict namespace and exact code/message only when supplied; all wrapper fields/serialization FIXTURE_LOCAL_NON_NORMATIVE. Any actual execution, provider qualification, rights grant, public access permission or zero-effects claim is **NOT_RUN/not established**.

## Actual independent byte checks

```text
python /workspace/work/g320g-scratch/verify_reports.py
```

CPython3.12.14, exit0. Authored exact public literals are decoded only as finite JSON observations for allowed key/verdict/code checks. They are compared to an independently assembled byte recipe using pinned source-message table and literal wrappers; UTF8 length is independently checked by Unicode scalar byte-width arithmetic. Every private token above is absent in its public bytes; authority-bearing fields and extra keys absent. G-R003/004/005/011 have byte-identical public output despite different private scenarios. Only2 of21 messages are exercised; all21 remain preserved. No runtime projection function/API or complete PG validator ran.

G-R001 existing pure consistency is a stipulated premise, not proved by a report fixture. G-R006 unknown evidence does not become negative; G-R007 descriptive validity supplies no verdict; G-R008 absent runtime observations cannot claim zero effects; G-R012 unsupported local field/version convention has no adopted PG semantics. Runtime logging/privacy/access/no-effect/rights/provider behavior remains NOT_RUN.

**STOP — CM-073 remains PARTIAL; no implementation or production authority.**
