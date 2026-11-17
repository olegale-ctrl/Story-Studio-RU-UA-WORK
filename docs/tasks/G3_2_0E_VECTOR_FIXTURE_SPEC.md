# E fixtures — exact byte and evidence specification

**DOCS_ONLY + OFFLINE_VECTOR_VERIFICATION — NO PRODUCTION AUTHORITY**

SI-INTEGRATION-G3.2.0e; 2026-11-17 (Europe/Kyiv). G3.2.0d ACCEPTED_DOCS_ONLY; only OP-01–06/26/27 approved pure-contract.

## Scope and source precedence

Exact base `667ee9fbfa7100c30a0ffd601fc4482182c22ab6`, tree `f00418a86270b39194a07be2173a36f79c4c45ca`, parent `86ae74058c2a90b563855eac15f46ff8b3be28e4`. Read-only main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

Precedence: direct owner X01–X04 and OP-01–06/26/27 → [D normative P1](G3_2_0D_P1_NORMATIVE_CONTRACT.md) → [B owner decisions](G3_2_0B_OWNER_DECISIONS_X01_X04.md) → compatible historical A/C proposals. No OP-07/08/09–25/28 approval. See [source blob registry](G3_2_0E_ACCEPTANCE_PACKET.md); all existing files and their87 vector IDs/58 oracle IDs remain unchanged.

Exactly28 main IDs E-V001…E-V028; subcase names are local labels, not additional main E IDs or PG result enums. E-V001–007 map seven boundary/precedence CM rows; E-V008–028 map21 safe-message CM rows. There are63 finite subcases. Sources, assumptions, exact recipe lengths, expectations and residual limitations are attached per main vector. This is not a PG serializer, validator, resolver, executor or trusted provider implementation.

## Byte language and published constants

`ASCII(text)` encodes exactly the displayed text as ASCII without newline; `UTF8(text)` encodes exactly shown Unicode scalars without BOM/newline. `hex...` decodes hex pairs. `||` is byte concatenation; `X^n` repeats n times; zero-based byte offsets and slices are half-open. `replace_once` requires exactly named first occurrence; absent substring is an error. Quotes inside ASCII(...) are data; outer parentheses are notation. A quoted hex string contains no hidden LF. `len` counts bytes, not codepoints. JSON fixtures below have no implicit leading/trailing whitespace.

From the **Byte language and fixture constants** section of pinned [A vectors](G3_2_0A_INDEPENDENT_VECTORS.md), blob `1035c8a50dbb3c943ba17a9eb8c9fd8781f3e427`:

- BODY = exact UTF-8 of that section's first one-line json fence, without LF (published full literal, no omitted fields).
- REF = exact UTF-8 of its fence following `REF = UTF8`, without LF. I=`00000000-0000-4000-8000-000000000001`.
- SUFFIX=ASCII(,"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","mode":"PREVIEW_ONLY","revision":1}).
- C_ENV=ASCII({"body":)||BODY||SUFFIX, length3206.
- H_ENV=`31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64`.
- E=ASCII({"binding_sha256":")||ASCII(H_ENV)||ASCII(",)||C_ENV[1:], length3290. These reproduce exactly the published C_ENV/E bytes; H_ENV was recomputed here.
- P=hex53746f727953747564696f2f50472d4331344e2d3100, exact22-byte domain prefix including final00.
- RAW(X)=SHA256(X); DOMAIN(X)=SHA256(P||X). DOMAIN on a scalar/value probe or synthetic body is arithmetic only, not a valid PG identity/authority verdict.

For mixed containers define B(i)=ASCII({"k":) for odd i, hex5b for even i; Z(i)=hex7d for odd i, hex5d for even i. M(n)=B(1)||…||B(n)||hex30||Z(n)||…||Z(1). Thus M64 length257/depth64, M65 length263/depth65. This recipe defines the shape; depth checked separately on these finite JSON inputs, not a general PG parser.

For E-V003 define KEY(X)=hex7b22||X||hex223a307d and VALUE(X)=hex7b226b223a22||X||hex227d. Units ASCII=hex61, CONTROL=ASCII(\u0001), PAIR=ASCII(\ud83d\ude00). Canonical units: ASCII=hex61, CONTROL unchanged ASCII(\u0001), PAIR=hexf09f9880. Canonical KEY/VALUE construction uses the same wrapper and these units; no generic serializer is invoked. Lone-surrogate raw literals are separately stated and have no accepted canonical output.

For E-V004 N0=ASCII({"body":{"subject":{"snapshot":)||REF||ASCII(}})||SUFFIX. N1=replace_once(N0,ASCII(H_ENV),ASCII(0)^64). N0 has exactly one H_ENV occurrence, in nested REF; N1 preserves all other bytes. FULL(C,H)=ASCII({"binding_sha256":")||ASCII(H)||ASCII(",)||C[1:]. This is a finite fixture concatenation, not a production envelope builder. N0/N1 use V022-style wrapper body; they are NOT schema-admissible PG01 fixtures. Hash statements apply only to the named byte layer, conditional PG error labels only if earlier schema stages could succeed.

## Safe-message input/output grammar

Private diagnostics are wholly artificial; no real path, source, reviewer or exception was accessed. Common PRIVATE is exactly this ASCII line (no LF):

```json
{"path":"E_PRIVATE_PATH_7f91:/synthetic/private/input.bin","source_text":"E_PRIVATE_SOURCE_7f91:unpublished synthetic text","reviewer_identity":"E_PRIVATE_REVIEWER_7f91:fixture-person-not-real","exception_detail":"E_PRIVATE_EXCEPTION_7f91:RuntimeError(synthetic)"}
```

INPUT(CODE)=ASCII({"established_code":")||ASCII(CODE)||ASCII(","private_diagnostics":)||PRIVATE||hex7d.
PUBLIC(CODE,MESSAGE)=ASCII({"code":")||ASCII(CODE)||ASCII(","message":")||UTF8(MESSAGE)||ASCII("}). No message contains a quote/backslash requiring an unstated escape. This JSON wrapper is a fixture observation representation, not a newly approved PG error schema/transport.

All21 authored code/message literals are compared with D P1-27-SAFE-ERRORS, including exact Unicode, period and spaces; PRIVATE markers must be present in each input and absent in each expected public output. This finite expected projection check does not execute or qualify an application projection API. Established primary code is a premise; operational causes are never generated by a mock provider.

## Evidence status and digest policy

VERIFIED_OFFLINE means finite bytes/arithmetic/fixture predicates actually checked, not PG semantics. PARTIAL means a named expectation cannot be fully fixed under approved contracts. BLOCKED_CONTRACT flags an owner decision needed; NOT_RUN covers application/native/provider/runtime behaviors. These labels are report metadata, not new PG enums or permissions.

Hash ledger records every applicable accepted-layer canonical preimage:5 depth shapes,7 decoded string/key/scalar cases,3 own/nested preimages; each RAW+DOMAIN =30 comparisons. One additional RAW hash of supplied `abc` bytes supports abstract stage4 actual-byte mismatch, total31. Expected=hashlib; actual=sha256sum over the same exact bytes, all matched. Backend independence is not asserted. Safe-message/abstract-stage JSON has no PG canonical/domain hash; wire-only checks do not synthesize a successful canonical output. Rejected malformed/oversized cases have no accepted digest. No DIAGNOSTIC_RAW_ONLY malformed-input hashes are published.

Conformance matrix is an additive overlay: original95 rows remain60 COVERED/7 PARTIAL/28 MISSING. New documentary completion is not `95/95 TESTED`, a contract freeze, production permission or G3.2.1 authorization.

**STOP: CM-069 exact private ordering remains BLOCKED_CONTRACT. See closure and acceptance packet.**
