# CM-069 / E-V007 — finite conformance evidence and additive resolution

**OWNER_AUTHORIZED_DOCS_ONLY — NO IMPLEMENTATION OR PRODUCTION AUTHORITY**

SI-INTEGRATION-G3.2.0e-RESOLVE-1; 2026-11-17 (Europe/Kyiv). P1-DIAG-01 APPROVED, narrow private-order decision only.

**READY_FOR_INDEPENDENT_REVIEW** — documentation only. Applicable owner rule: [P1-DIAG-01](G3_2_0E_RESOLVE_1_DIAGNOSTIC_ORDER_CONTRACT.md); unchanged [source E-V007](G3_2_0E_P1_BOUNDARY_AND_PRECEDENCE_VECTORS.md), blob `c15cc8d8e5f2e67bbf0e153a082f5c37b3bfdcce`. No existing E-vector or original CM row is modified or renumbered. R1–R4 are local finite evidence-case IDs, not new PG enums or a replacement vector namespace.

## Exact byte language and source constants

ASCII/UTF8 and concatenation have the same exact meaning as [E fixture specification](G3_2_0E_VECTOR_FIXTURE_SPEC.md): no implicit LF/BOM/space; replace_once replaces the first exact stated substring, absent match is an error; slices are zero-based half-open byte slices. BODY is the exact one-line UTF8 json fence after `BODY =` in pinned [A vectors](G3_2_0A_INDEPENDENT_VECTORS.md), blob `1035c8a50dbb3c943ba17a9eb8c9fd8781f3e427`. No JSON serialization is used to reconstruct these bytes.

H_ENV=ASCII(31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64).
SUFFIX=ASCII(,"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","mode":"PREVIEW_ONLY","revision":1}).
C_ENV=ASCII({"body":)||BODY||SUFFIX,3206 bytes.
E=ASCII({"binding_sha256":")||H_ENV||ASCII(",)||C_ENV[1:],3290 bytes; identical published E recipe. All source constants are pinned above and in acceptance registry.

## R1 — exact original E-V007

Unchanged recipe:

```text
replace_once(replace_once(E,own H_ENV,ASCII(0)^63),ASCII("revision":1}),ASCII("revision":true}))
```

Expected length3292 =3290−1+3. Actual3292. Wire order: binding_sha256,body,contract,id,mode,revision. Exact defects: revision bool true; own binding63 lowercasehex. Expected/actual finite ordinal order3,6: revision INVALID_DECLARED_TYPE → binding_sha256 INVALID_HASH_LENGTH. Primary abstract oracle DENY/PG_FORMAT/stage2. **VERIFIED_OFFLINE**, not a runtime PG verdict.

## R2 — explicit nonidentity wire permutation

Define complete top-level member byte fragments from R1, without outer braces/commas:

```text
F_contract = ASCII("contract":"pg-01/proposal-1")
F_id = ASCII("id":"00000000-0000-4000-8000-000000000001")
F_binding = ASCII("binding_sha256":") || ASCII(0)^63 || ASCII(")
F_revision = ASCII("revision":true)
F_mode = ASCII("mode":"PREVIEW_ONLY")
F_body = ASCII("body":) || BODY
```

R2=hex7b||F_contract||hex2c||F_id||hex2c||F_binding||hex2c||F_revision||hex2c||F_mode||hex2c||F_body||hex7d.

Expected/actual length3292; field order contract,id,binding_sha256,revision,mode,body. Both defects unchanged; decoded R2 equals decoded R1, exact wire bytes differ. Original R1 already placed binding before revision; R2 deliberately moves its ordinal **wire position**1→3 and revision6→4 while retaining the requested binding-before-revision relation. This is a genuine root-member byte permutation, not an identity transform or serializer normalization.

Expected/actual private order remains revision→binding, ordinals3→6, contrary to their encounter order in both cases. Primary DENY/PG_FORMAT/stage2. This finite control checks invariance for the specified permutation, not all possible JSON orders or runtime discovery behavior. **VERIFIED_OFFLINE**.

## R3 — revision-only stage2 defect

Recipe: replace_once(E,ASCII("revision":1}),ASCII("revision":true})). Length expected/actual3293. Original E wire order unchanged. revision bool true; binding is exact original H_ENV,64 lowercasehex. Expected/actual private sequence only revision INVALID_DECLARED_TYPE (ordinal3); primary DENY/PG_FORMAT/stage2. No digest equality claim: changed revision would change a later hash equation, but stage3 is not performed. **VERIFIED_OFFLINE**.

## R4 — binding-only stage2 defect

Recipe: replace_once(E,own H_ENV,ASCII(0)^63). Length expected/actual3289. Original E wire order unchanged. revision exact integer1, binding63 lowercasehex. Expected/actual private sequence only binding_sha256 INVALID_HASH_LENGTH (ordinal6); primary DENY/PG_FORMAT/stage2. No accepted canonical digest. **VERIFIED_OFFLINE**.

## Actual/expected table

| Case | Expected bytes | Actual bytes | Expected private sequence | Actual ordinal sequence | Expected primary / layer | Actual offline status |
|---|---:|---:|---|---|---|---|
| R1 | 3292 | 3292 | revision:INVALID_DECLARED_TYPE → binding_sha256:INVALID_HASH_LENGTH | [3, 6] | DENY / PG_FORMAT / stage2 abstract oracle | VERIFIED_OFFLINE; observed finite cause order equals expected |
| R2 | 3292 | 3292 | revision:INVALID_DECLARED_TYPE → binding_sha256:INVALID_HASH_LENGTH | [3, 6] | DENY / PG_FORMAT / stage2 abstract oracle | VERIFIED_OFFLINE; observed finite cause order equals expected |
| R3 | 3293 | 3293 | revision:INVALID_DECLARED_TYPE | [3] | DENY / PG_FORMAT / stage2 abstract oracle | VERIFIED_OFFLINE; observed finite cause order equals expected |
| R4 | 3289 | 3289 | binding_sha256:INVALID_HASH_LENGTH | [6] | DENY / PG_FORMAT / stage2 abstract oracle | VERIFIED_OFFLINE; observed finite cause order equals expected |

All four fixed public observations equal UTF8 of the following exact93-byte line, without LF:

```json
{"code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

Actual fixture-byte checks: exact code/message matches pinned D PG_FORMAT message, object has only code/message; revision/binding_sha256 field names, INVALID_DECLARED_TYPE/INVALID_HASH_LENGTH labels, raw true,63 zeros and H_ENV are absent. This checks **expected-output fixture bytes**, not a running projection/redaction API or permission to publish private content. Labels are documentary only; actual PG Error.code catalogue remains21 codes.

## Verification method, commands and limits

Actual temporary helper outside repository:

```text
python /workspace/work/g320e-resolve1-scratch/verify_fixtures.py
```

Exit0, CPython3.12.14. It reads pinned published bytes, extracts the exact historical Envelope order, reproduces R1 without altering its recipe, concatenates explicitly named R2 member fragments, decodes only these four fixed JSON fixtures for observation, and compares cause tuples sorted by owner ordinals with separately authored expected tuples. It checks lengths/strict UTF8/no BOM/within8MiB, JSON bool vs exact integer, hex lengths, R1/R2 model equality and byte inequality, fixed public bytes/no private labels or values. No generic PG schema validator, serializer or runtime module is created/imported; no cryptographic accepted-output digest is computed for malformed input. Stage1 checks are finite fixture observations; stage2 result is an abstract expected oracle. Stages3–7 NOT_RUN.

The expected tuples are explicit above; the ordinal registry is contract1,id2,revision3,mode4,body5,binding6, independently read from pinned source and compared against the direct owner decision. Reproduction requires only the published recipes, finite observations and tuple ordering, not helper-generated hidden fixture bytes. A consistency checker separately re-reads document tables, links, statuses/source blobs and source vector/oracle IDs; commands/exit codes appear in acceptance packet. This is offline arithmetic/document evidence, not independent human acceptance or runtime PG validation.

## Additive resolution only

| CM | Before decision | After decision | Evidence |
|---|---|---|---|
| CM-069 | PARTIAL_CONTRACT_DEPENDENCY | DOCUMENTARY_FIXTURE_COMPLETE | P1-DIAG-01 + R1–R4 VERIFIED_OFFLINE |

- Original D matrix stays60 COVERED/7 PARTIAL/28 MISSING,95 rows, unchanged bytes.
- Original E overlay stays27 complete/1 partial, unchanged bytes; original28 E IDs/63 subcases remain historically intact.
- This RESOLVE-1 adds1 resolved target row and4 local finite controls, without rewriting the historical count63 or claiming old cases rerun.
- Cumulative **28/28 target documentary fixtures complete**;7 original PARTIAL remain,20 OP remain OPEN.
- No95/95 TESTED, full contract freeze or production-ready claim. This resolution is ready for independent documentation review only.

**STOP — no main change, merge, PG implementation, G3.2.1, providers or production permissions.**
