# P1-DIAG-01 — narrow diagnostic-order contract

**OWNER_AUTHORIZED_DOCS_ONLY — NO IMPLEMENTATION OR PRODUCTION AUTHORITY**

SI-INTEGRATION-G3.2.0e-RESOLVE-1; 2026-11-17 (Europe/Kyiv). P1-DIAG-01 APPROVED, narrow private-order decision only.

## Source and precedence

[Owner record](G3_2_0E_RESOLVE_1_OWNER_APPROVAL_P1_DIAG_01.md) reproduces the direct approved decision. Priority: P1-DIAG-01 → already-approved OP-06 → compatible A–E documents. [D normative P1](G3_2_0D_P1_NORMATIVE_CONTRACT.md) retains earliest-stage/code priority and safe public handling. The [E blocked overlay](G3_2_0E_CONFORMANCE_CLOSURE_MATRIX.md) remains an unchanged historical record; only the new additive resolution applies to CM-069.

## Scope predicate

This registry applies only to private diagnostics for multiple errors **of the same code in the same stage** on the specified historical `pg-01/proposal-1` root Envelope's declared fields. It is not wire-schema approval or an operational policy. Nested fields, other record types, future versions and cases needing another tie-breaker receive no automatic ordinal.

## P1-DIAG-01-ORDER — OWNER_APPROVED narrow rule

Use the following ordinal registry from the published historical Envelope:

| Ordinal | Declared field |
|---|---|
| 1 | contract |
| 2 | id |
| 3 | revision |
| 4 | mode |
| 5 | body |
| 6 | binding_sha256 |

For established same-stage/same-code causes on different listed fields, sort private field observations by ascending ordinal. Do not sort by input encounter order, lexicographic field name, runtime hash-map order or a serializer's key ordering. An unchanged array's diagnostic indices retain already-approved OP-06 index order; this document adds no further tie-breaker. Cases not determined by these approved rules stay OPEN instead of receiving an invented order.

## CM-069 application and public/private boundary

R1/E-V007 has two established stage2 format observations: JSON bool true at revision (not Int) and63 lowercasehex characters at binding_sha256 (not Hash64). Resulting private order:

1. revision — INVALID_DECLARED_TYPE, ordinal3.
2. binding_sha256 — INVALID_HASH_LENGTH, ordinal6.

These two labels are human-readable fixture notation, **not new PG error codes, normative machine enums, logging fields or API types**. Other stage2 failures are not inferred. The primary remains **DENY / PG_FORMAT / stage2**. Stage1 succeeds only for the finite byte/decode fixture checks; stage3 and later are not executed in this abstract oracle. In particular R3's Hash64 format does not establish correct digest equality.

Expected public observation (93 UTF-8 bytes, no LF/BOM):

```json
{"code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

No new public API fields. The fixture wrapper exactly preserves the pre-existing code/message observation; no private field names, bool/hash values or reason labels enter it. Public export/access/privacy/retention remain OPEN OP-21/23; checking fixed expected output is not runtime redaction qualification.

## Preserved boundaries and explicit OPEN

The seven-stage error precedence remains:1 bounded input/decode;2 grammar/schema/types/known enum;3 local binding;4 refs/closure;5 mode/subject;6 product/rights/trusted-state;7 execution/evidence. P1-DIAG-01 only orders the applicable same-code private causes; no later-stage error supersedes an earlier one. X01/X02 distinctions are preserved, X03 crypto/abstract split and X04 exact-plan scope are not changed.

OPEN: nested diagnostics; different/new record registries or versions; further equal-ordinal tie policy not already determined by OP-06; operational provider cause/chronology; full schema/reference admission OP-09/22; global resources OP-07/08. None prevents this exact two-distinct-field fixture from being documented, and none is silently approved.

No actual authenticated findings, rights grants, render permit, production logging, PG validator/serializer/executor or provider implementation follows. Storage S3 and native Windows qualification remain unqualified/NOT_RUN. **STOP — no G3.2.1 or production permissions.**
