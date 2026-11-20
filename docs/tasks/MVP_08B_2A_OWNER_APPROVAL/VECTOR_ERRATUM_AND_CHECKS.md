# Derived vector erratum and static checks

Mode: **DOCS_ONLY / OWNER_APPROVAL**. Recorded date: 2026-11-20 (Europe/Kiev). This records a decision supplied by the project owner in the current conversation; no identity/signature infrastructure is claimed. **Implementation is NOT authorized.** No code, models, SQLite, provider API, CI, main, merge, release, production storage or production permissions.

## Concrete discrepancy found: V030

At exact FIX-01 base, CONTRACT_RECORDS_AND_PREIMAGES.md, section V030, the canonical PURE.JobError contains `required_action: "INSPECT"`. The same document's Additional closure rules close ErrorAction to FIX_INPUT|REAUTHORIZE|RELOAD|RECONCILE|STOP. ERROR_AND_ORACLE_MATRIX.md additionally maps STALE_WORKER_FENCE to RELOAD. INSPECT is invalid under both approved constraints. The old SHA `4f029054d2ddcfab31ce93c4f428fcd198cc9eb1fd20f71136cf6fd0f30c8374` correctly hashes the old bytes; hashing correctness never implied schema validity. Prior arithmetic checks did not check this enum.

## Mechanical correction, without changing the contract or historical file

The normative enum and existing code-to-action mapping already determine the sole conforming value **RELOAD**. This addendum changes no schema, enum, error rule, gate or approved profile. It supplies the derived positive value below; retain old V030 as a negative test input expecting FORMAT. Do not change the historical V030 bytes/hash or silently substitute its digest.

New vector identifier: **OA-V030-CORRECTED-1**. All fields are unchanged except required_action INSPECT -> RELOAD. No other record references old V030 in the fixed vector set, so this correction has no transitive digest updates.

Canonical UTF-8, no final newline, 529 bytes. SHA-256 `1ee3123931b2fdac839858cc79d20bd05342c778c2855fb2cef3a26c7bf4fe58`.

```json
{"attempt": null, "billing": "ZERO", "code": "STALE_WORKER_FENCE", "domain": "PURE_LOCAL", "error_id": "00000000-0000-0000-0000-000000000031", "evidence_ref": null, "external_effect": "NONE", "kind": "PURE.JobError", "occurred_at": {"clock_epoch_id": "00000000-0000-0000-0000-000000000009", "tick": 2}, "operation": "INCIDENT", "provider_status": null, "required_action": "RELOAD", "retry_class": "NONE", "safe_message": "Worker fence is stale.", "scope": "PURE_FAKE_ONLY", "state": "DRAFT", "trace_redacted": null, "version": 1}
```

Future conformance test: old V030 is rejected as FORMAT; corrected record validates and has the digest above; ResponseError for STALE_WORKER_FENCE has required_action RELOAD. This tests the already-approved closed mapping. No stale caller is allowed to persist JobError; positive record encoding is not write authority. Independent byte/shape review of this derived correction is still required at implementation entry. If the reviewer rejects this derivation, status becomes BLOCKED_CONTRACT; never add INSPECT as a new accepted action.

## Checks actually executed

- Exact docs base/tree and exact SP/1.1 base/tree match the pinned values.
- 13/13 proposed paths are absent from SP/1.1, have no case-fold collision or file ancestor, and are members of the historical 22-path proposal. They are additive paths, not overwrites. This is Git-tree compatibility, not runtime/import/Windows qualification.
- All 36 historical canonical blocks have matching byte counts and SHA-256. One invalid positive schema example is identified above and superseded for positive use by the derived vector, with old bytes retained for negative use.
- Corrected vector digest independently calculated by Python hashlib and Node crypto: agreement, exit 0. This verifies digest arithmetic; it does not execute product schema/state-machine logic.
- Static review covers exact FIX-01 registry, admission, restart, error rules and G1–G6. No additional blocking logical contradiction identified in the bounded PURE profile after applying the derived example erratum. This is not an exhaustive formal proof or new independent acceptance.
- Runtime tests: **0**. Future A/R/E and SP regressions: NOT_RUN. SQLite/media/provider/model execution: NOT_RUN. Windows: WINDOWS_NOT_RUN.

External evidence contains machine-readable per-path checks, source blob/SHA-256 manifest, corrected canonical bytes and final diff/tree reproduction. All helper activity is documentation/Git inspection, not implementation of the proposed execution core.
