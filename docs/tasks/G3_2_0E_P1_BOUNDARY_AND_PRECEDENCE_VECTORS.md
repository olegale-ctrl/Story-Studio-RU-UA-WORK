# P1 — boundary and precedence E vectors

**DOCS_ONLY + OFFLINE_VECTOR_VERIFICATION — NO PRODUCTION AUTHORITY**

SI-INTEGRATION-G3.2.0e; 2026-11-17 (Europe/Kyiv). G3.2.0d ACCEPTED_DOCS_ONLY; only OP-01–06/26/27 approved pure-contract.

All byte notation/constants are defined in [fixture specification](G3_2_0E_VECTOR_FIXTURE_SPEC.md). Normative source for each row: [D pure P1](G3_2_0D_P1_NORMATIVE_CONTRACT.md), exact Rule ID; owner record [D P1 approval](G3_2_0D_OWNER_APPROVAL_P1.md), corresponding OP. Original target CM rows are in [D conformance](G3_2_0D_P1_CONFORMANCE_MATRIX.md). All expected results are layer-restricted; no validators/providers/native/render runs.

## E-V001 — CM-005, OP-01

Rule `P1-01-WIRE-LIMIT`; layer `PURE_BYTE_OBSERVATION`; status **VERIFIED_OFFLINE**.

Each stream is exactly E followed by spaces; EOF position and all delivered chunk lengths are defined below. Content-Length is deliberately untrusted metadata. Byte-limit result is not later JSON/schema validity. Offset8388608 (zero-based) is the first disallowed byte. All streams are finite fixtures; no production reader was executed.

| Case | Exact source recipe | Wire / EOF bytes | Chunk lengths | Cumulative delivered bytes | Claimed Content-Length | Layer expectation |
|---|---|---:|---|---|---:|---|
| at_eof | E &#124;&#124; hex20^8385318 | 8388608 | [8388607, 1] | [8388607, 8388608] | 8388608 | SIZE_GUARD_ONLY accepts W; subsequent JSON/schema/PG semantics not established |
| plus_one_new_chunk | E &#124;&#124; hex20^8385319 | 8388609 | [8388607, 1, 1] | [8388607, 8388608, 8388609] | 1 | PG_FORMAT at stage1 |
| cross_boundary_chunk | E &#124;&#124; hex20^8385319 | 8388609 | [8388607, 2] | [8388607, 8388609] | 8388608 | PG_FORMAT at stage1 |
| after_boundary_chunk | E &#124;&#124; hex20^8385319 | 8388609 | [8388608, 1] | [8388608, 8388609] | 8388708 | PG_FORMAT at stage1 |
| understated_length | E &#124;&#124; hex20^8385318 | 8388608 | [8388606, 1, 1] | [8388606, 8388607, 8388608] | 1 | SIZE_GUARD_ONLY accepts W; subsequent JSON/schema/PG semantics not established |
| overstated_length | E &#124;&#124; hex20^8385318 | 8388608 | [8388607, 1] | [8388607, 8388608] | 8388708 | SIZE_GUARD_ONLY accepts W; subsequent JSON/schema/PG semantics not established |

At a crossing chunk the source supplies the specified whole chunk; guard observation rejects at first excess byte, without a claim about actual reader allocation/consumption. EOF after overflow cannot reverse rejection. No Content-Length value can substitute for actual bytes. RAW/DOMAIN N/A for this size-only observation.

Limit: Finite actual-byte lengths/prefix sums checked, not a bounded-memory reader, throughput benchmark or full PG verdict. Canonical/hash digest N/A for size-guard observation.

## E-V002 — CM-009, OP-02

Rule `P1-02-DEPTH`; layer `FINITE_JSON_SHAPE`; status **VERIFIED_OFFLINE**.

| Case | Exact recipe | Wire bytes | Expected depth / decoded UTF8 bytes | Canonical bytes if accepted at this layer | Layer expectation |
|---|---|---:|---:|---:|---|
| scalar | hex30 | 1 | 0 | 1 | DEPTH_GUARD_ONLY accepts |
| root_array | hex5b5d | 2 | 1 | 2 | DEPTH_GUARD_ONLY accepts |
| scalar_leaf | hex5b305d | 3 | 1 | 3 | DEPTH_GUARD_ONLY accepts |
| nested_array | hex5b5b5d5d | 4 | 2 | 4 | DEPTH_GUARD_ONLY accepts |
| mixed64 | M(64) | 257 | 64 | 257 | DEPTH_GUARD_ONLY accepts |
| mixed65 | M(65) | 263 | 65 | N/A | PG_FORMAT stage2, no accepted output digest |

RAW/DOMAIN of accepted canonical value preimages appear in ledger below; rejected cases have no accepted output hash. Wire and decoded units are deliberately separate.

Limit: Object/array depth checked on six finite shapes only; scalar is not valid PG envelope. No reference depth/native-stack proof.

## E-V003 — CM-017, OP-03

Rule `P1-03-STRING-BYTES`; layer `FINITE_DECODED_BYTE_BOUNDARY`; status **VERIFIED_OFFLINE**.

| Case | Exact recipe | Wire bytes | Expected depth / decoded UTF8 bytes | Canonical bytes if accepted at this layer | Layer expectation |
|---|---|---:|---:|---:|---|
| key_ascii_65536 | KEY(ASCII^65536) | 65542 | 65536 | 65542 | STRING_GUARD_ONLY accepts |
| key_ascii_65537 | KEY(ASCII^65536 &#124;&#124; hex78) | 65543 | 65537 | N/A | PG_FORMAT stage2; no accepted canonical digest |
| key_control_65536 | KEY(CONTROL^65536) | 393222 | 65536 | 393222 | STRING_GUARD_ONLY accepts |
| key_control_65537 | KEY(CONTROL^65536 &#124;&#124; hex78) | 393223 | 65537 | N/A | PG_FORMAT stage2; no accepted canonical digest |
| key_pair_65536 | KEY(PAIR^16384) | 196614 | 65536 | 65542 | STRING_GUARD_ONLY accepts |
| key_pair_65537 | KEY(PAIR^16384 &#124;&#124; hex78) | 196615 | 65537 | N/A | PG_FORMAT stage2; no accepted canonical digest |
| value_ascii_65536 | VALUE(ASCII^65536) | 65544 | 65536 | 65544 | STRING_GUARD_ONLY accepts |
| value_ascii_65537 | VALUE(ASCII^65536 &#124;&#124; hex78) | 65545 | 65537 | N/A | PG_FORMAT stage2; no accepted canonical digest |
| value_control_65536 | VALUE(CONTROL^65536) | 393224 | 65536 | 393224 | STRING_GUARD_ONLY accepts |
| value_control_65537 | VALUE(CONTROL^65536 &#124;&#124; hex78) | 393225 | 65537 | N/A | PG_FORMAT stage2; no accepted canonical digest |
| value_pair_65536 | VALUE(PAIR^16384) | 196616 | 65536 | 65544 | STRING_GUARD_ONLY accepts |
| value_pair_65537 | VALUE(PAIR^16384 &#124;&#124; hex78) | 196617 | 65537 | N/A | PG_FORMAT stage2; no accepted canonical digest |
| standalone_pair | hex225c75643833645c756465303022 | 14 | 4 | 6 | Scalar decoding only: paired escapes → U+1F600, no PG verdict |
| lone_high_value | ASCII({"k":"\ud83d"}) | 14 | N/A | N/A | PG_FORMAT stage2: lone surrogate; no scalar UTF8 length/output digest |
| lone_low_key | ASCII({"\ude00":0}) | 12 | N/A | N/A | PG_FORMAT stage2: lone surrogate; no scalar UTF8 length/output digest |

RAW/DOMAIN of accepted canonical value preimages appear in ledger below; rejected cases have no accepted output hash. Wire and decoded units are deliberately separate.

Limit: Finite expected scalar/byte checks, not a production parser. stdlib accepts lone surrogate codepoints in memory; explicit finite probe notes they are not Unicode scalars. Max keys are below wire cap; no closed PG schema claim.

## E-V004 — CM-061, OP-05

Rule `P1-05-CANONICAL-BYTES`; layer `OWN_VS_NESTED_BYTE_HASH_ORACLE`; status **VERIFIED_OFFLINE**.

Premises: exact published constants and finite synthetic wrapper as specified; no authority, schema admissibility or reference closure assumption is smuggled into hash equality.

| Case | Exact full-input recipe | Wire bytes | Own excluded preimage | Supplied own binding | Layer expectation |
|---|---|---:|---|---|---|
| E_original | published E | 3290 | C_ENV | 31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64 | Own local byte hash equality only; E is not full semantic success |
| E_own_changed | replace first own H_ENV in E with ASCII(0)^64 | 3290 | C_ENV unchanged | 0000000000000000000000000000000000000000000000000000000000000000 | PG_DIGEST stage3 if earlier structure succeeds; own field excluded but supplied wrong digest still denied |
| nested_baseline | FULL(N0,DOMAIN(N0)) | 399 | N0 | 92a1306ff4f1e1ffd545900df15ac78947711832a599f23128ca39faa1bfb5f9 | Local hash equality only; synthetic body not full schema/closure |
| nested_mutation_stale | FULL(N1,DOMAIN(N0)) | 399 | N1 changed | 92a1306ff4f1e1ffd545900df15ac78947711832a599f23128ca39faa1bfb5f9 | Local byte-hash oracle mismatch; conditional stage3 PG_DIGEST only if earlier schema succeeds |
| nested_mutation_rebound | FULL(N1,DOMAIN(N1)) | 399 | N1 | 672f3a51abf1b2abdc4971bc580d59274038f9b0f129f0c08e6a8e5d8cf4f921 | New local byte-hash equality only; no target/closure/approval claim |

Only own top-level field is excluded. E→E_own_changed gives identical C_ENV but supplied own digest is wrong. N0→N1 changes only nested REF binding, hence new preimage/digest. Old nested digest denies only the local hash equation, not proof of successful stage2/full closure. The rebound full bytes satisfy that equation and still grant nothing.

Limit: N0/N1 body is a synthetic V022-style reference wrapper, not a schema-admissible PG01 body. Conditional local error labels do not bypass stage2. No crypto-valid reference closure, target origin or production grant is claimed.

## E-V005 — CM-067, OP-06

Rule `P1-06-ERROR-PRECEDENCE`; layer `ABSTRACT_STAGE_ORACLE`; status **VERIFIED_OFFLINE**.

Prior-stage premises1–3: bounded root decode, grammar/schema and root local binding are stipulated successful **in this abstract model**, not actual executions. The records below are explicit supplied reference observations with the same typed identity. Their differing content/claimed binding establishes identity conflict for the model; the separate raw check compares actual bytes with SHA256({}). These are not PG targets with valid self hashes. No unavailable provider is modelled as missing.

### both

Exact ASCII input (554 bytes, no LF):

```json
{"prior_stage_assumptions":[1,2,3],"records":[{"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1,"claimed_binding":"1111111111111111111111111111111111111111111111111111111111111111","raw_hex":"7b7d"},{"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1,"claimed_binding":"2222222222222222222222222222222222222222222222222222222222222222","raw_hex":"5b5d"}],"raw_check":{"expected_sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a","actual_raw_hex":"616263"}}
```

Established observations: identity conflict, actual raw digest mismatch. Expected: ABSTRACT_STAGE_ORACLE primary PG_REFERENCE at stage4.

### identity_only

Exact ASCII input (552 bytes, no LF):

```json
{"prior_stage_assumptions":[1,2,3],"records":[{"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1,"claimed_binding":"1111111111111111111111111111111111111111111111111111111111111111","raw_hex":"7b7d"},{"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1,"claimed_binding":"2222222222222222222222222222222222222222222222222222222222222222","raw_hex":"5b5d"}],"raw_check":{"expected_sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a","actual_raw_hex":"7b7d"}}
```

Established observations: identity conflict, matching raw bytes. Expected: ABSTRACT_STAGE_ORACLE primary PG_REFERENCE at stage4.

### digest_only

Exact ASCII input (554 bytes, no LF):

```json
{"prior_stage_assumptions":[1,2,3],"records":[{"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1,"claimed_binding":"1111111111111111111111111111111111111111111111111111111111111111","raw_hex":"7b7d"},{"contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1,"claimed_binding":"1111111111111111111111111111111111111111111111111111111111111111","raw_hex":"7b7d"}],"raw_check":{"expected_sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a","actual_raw_hex":"616263"}}
```

Established observations: identical duplicate record, no conflict, actual raw digest mismatch. Expected: ABSTRACT_STAGE_ORACLE primary PG_DIGEST at stage4.

Limit: Prior stages1–3 assumed successful as supplied model premises, not run. claimed_binding values and records are observation fixtures, not hash-valid PG targets. OP-08/09 remain open. No providers or authenticated not-found. Input JSON hashes N/A; raw abc check is arithmetic only.

## E-V006 — CM-068, OP-06

Rule `P1-06-ERROR-PRECEDENCE`; layer `ABSTRACT_STAGE_ORACLE`; status **VERIFIED_OFFLINE**.

Context: PG01 contract-mode rule admits PREVIEW_ONLY, recognises but forbids PRODUCTION_CANDIDATE; UNRECOGNIZED_MODE is an unknown enum probe, not a new enum. For stage5 cases stages1–4 are stipulated satisfied: bounded decode; grammar/schema/known enum; local binding; supplied reference closure. Wrong subject reference here is the stage5 contract relation, not a missing stage4 target. For earlier-failure controls only prior stages are stipulated successful. Outcomes are authored expectations checked against finite fact/priority tables, not PG implementation results.

### all_stage5

Exact ASCII input (166 bytes):

```json
{"mode":"PRODUCTION_CANDIDATE","local_binding_matches":true,"stage4_references_pass":true,"forbidden_pair":true,"wrong_subject_reference":true,"scope_violation":true}
```

Prior-stage assumptions: [1, 2, 3, 4]; expected primary `PG_MODE`, stage5.

### ref_and_scope

Exact ASCII input (159 bytes):

```json
{"mode":"PREVIEW_ONLY","local_binding_matches":true,"stage4_references_pass":true,"forbidden_pair":false,"wrong_subject_reference":true,"scope_violation":true}
```

Prior-stage assumptions: [1, 2, 3, 4]; expected primary `PG_REFERENCE`, stage5.

### scope_only

Exact ASCII input (160 bytes):

```json
{"mode":"PREVIEW_ONLY","local_binding_matches":true,"stage4_references_pass":true,"forbidden_pair":false,"wrong_subject_reference":false,"scope_violation":true}
```

Prior-stage assumptions: [1, 2, 3, 4]; expected primary `PG_SCOPE`, stage5.

### unknown_mode

Exact ASCII input (167 bytes):

```json
{"mode":"UNRECOGNIZED_MODE","local_binding_matches":false,"stage4_references_pass":true,"forbidden_pair":false,"wrong_subject_reference":false,"scope_violation":false}
```

Prior-stage assumptions: [1]; expected primary `PG_FORMAT`, stage2.

### known_stale_binding

Exact ASCII input (169 bytes):

```json
{"mode":"PRODUCTION_CANDIDATE","local_binding_matches":false,"stage4_references_pass":true,"forbidden_pair":true,"wrong_subject_reference":false,"scope_violation":false}
```

Prior-stage assumptions: [1, 2]; expected primary `PG_DIGEST`, stage3.

### known_correct_binding

Exact ASCII input (168 bytes):

```json
{"mode":"PRODUCTION_CANDIDATE","local_binding_matches":true,"stage4_references_pass":true,"forbidden_pair":true,"wrong_subject_reference":false,"scope_violation":false}
```

Prior-stage assumptions: [1, 2, 3, 4]; expected primary `PG_MODE`, stage5.

Reference source X02: V039 stale-known-binding→PG_DIGEST, V071 corrected-known-binding→PG_MODE, V073 unknown-enum→PG_FORMAT. They remain unchanged; these abstract controls do not reapprove X02. RAW/DOMAIN N/A for boolean observation models.

Limit: For stage5,1 boundeddecode,2 grammar/types/known enum,3 local hash,4 closure are stipulated successful; wrong subject relation is contract-specific stage5, not missing stage4 target. Single earlier failure controls match X02/V039/V071/V073, not full PG executions. No new enum. Hashes N/A for abstract predicate fixture.

## E-V007 — CM-069, OP-06

Rule `P1-06-ERROR-PRECEDENCE`; layer `FINITE_STAGE2_PRIMARY_ORACLE`; status **PARTIAL**.

Exact recipe: `replace_once(replace_once(E,own H_ENV,ASCII(0)^63),ASCII("revision":1}),ASCII("revision":true}))`. Length **3292 bytes**. Original E3290; own hash64→63 reduces1, revision1→true adds3. Resulting revision is JSON bool true, not Int; binding is63 lowercasehex, not Hash64. Both are declared-field format defects; no local digest is computed as accepted output. Earlier stage1 finite byte/decode conditions hold.

Expected primary: **DENY / PG_FORMAT stage2**. Expected public code/message observation is exactly UTF8 of:

```json
{"code":"PG_FORMAT","message":"Данные не соответствуют формату."}
```

The historical A schema `Envelope` record lists contract,id,revision,mode,body,binding_sha256, whereas actual wire E begins with binding and ends revision. Neither enumeration is an owner-approved private diagnostic ordinal registry: OP-09/22 are OPEN. Do not choose lexical/wire/inventory order silently. **Exact private diagnostic ordering: PARTIAL / BLOCKED_CONTRACT.** No field names, input or exception text in public output.

Limit: revision bool is not Int; own binding63hex is malformed. Both independently established by finite JSON/field observation. A schema inventory lists fields but is historical proposal, not approved diagnostic ordinal registry (OP-09/22 OPEN). No private order invented; BLOCKED_CONTRACT for completing CM-069 private-order expectation. No malformed-input accepted digest.

## Literal hash ledger — actual independent recalculation

CPython3.12.14 hashlib expected values compared with external sha256sum actual values,31 comparisons, all equal, exit0. These tools may share a crypto backend; no backend independence is claimed. Bytes come from fixed recipes, no production/generic canonicalizer. RAW length excludes P; DOMAIN preimage length adds22. Names below are local case labels under existing E IDs. RAW/D arithmetic for scalar/synthetic wrappers is not a PG binding/semantic grant except the narrowly defined own-envelope equation.

| Case | Kind / role | Raw canonical or raw-data bytes | Hashed preimage bytes | Expected (hashlib) | Actual (sha256sum) |
|---|---|---:|---:|---|---|
| E-V002/scalar | RAW / C14N_VALUE_ARITHMETIC | 1 | 1 | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| E-V002/scalar | DOMAIN / C14N_VALUE_ARITHMETIC | 1 | 23 | `bb73b0a9ea7841431b16caa5efe39a17af87b7632f9964c1b733b6516e47923f` | `bb73b0a9ea7841431b16caa5efe39a17af87b7632f9964c1b733b6516e47923f` |
| E-V002/root_array | RAW / C14N_VALUE_ARITHMETIC | 2 | 2 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| E-V002/root_array | DOMAIN / C14N_VALUE_ARITHMETIC | 2 | 24 | `ffaf100393752ec3527e80da5ca96bf3a22536180c0a7c82ec2effc59c98ab13` | `ffaf100393752ec3527e80da5ca96bf3a22536180c0a7c82ec2effc59c98ab13` |
| E-V002/scalar_leaf | RAW / C14N_VALUE_ARITHMETIC | 3 | 3 | `d0bca111f8628137adc4c16f123496dcdd1d590d06cb5d9acd68b39fe656fb97` | `d0bca111f8628137adc4c16f123496dcdd1d590d06cb5d9acd68b39fe656fb97` |
| E-V002/scalar_leaf | DOMAIN / C14N_VALUE_ARITHMETIC | 3 | 25 | `92c124a1d7af1aa0fd2b61e6792122b989b261b3c8ec7323856912c23450991e` | `92c124a1d7af1aa0fd2b61e6792122b989b261b3c8ec7323856912c23450991e` |
| E-V002/nested_array | RAW / C14N_VALUE_ARITHMETIC | 4 | 4 | `cf1cbb66a638b4860a516671fb74850e6ccf787fe6c4c8d29e9c04efe880bd05` | `cf1cbb66a638b4860a516671fb74850e6ccf787fe6c4c8d29e9c04efe880bd05` |
| E-V002/nested_array | DOMAIN / C14N_VALUE_ARITHMETIC | 4 | 26 | `8ec2c49d845a82e9d7f903a10b701d657f48988c944b725f0fcd8674022d08af` | `8ec2c49d845a82e9d7f903a10b701d657f48988c944b725f0fcd8674022d08af` |
| E-V002/mixed64 | RAW / C14N_VALUE_ARITHMETIC | 257 | 257 | `eed3cdb0fe440b97e4d70802f46593571f1b33eaedb52c54b090337e41f6a143` | `eed3cdb0fe440b97e4d70802f46593571f1b33eaedb52c54b090337e41f6a143` |
| E-V002/mixed64 | DOMAIN / C14N_VALUE_ARITHMETIC | 257 | 279 | `cc9743b9c0de6e95ec72ce04f8a2632603f174bc4a10bde1df8e0e9ecab8d2f4` | `cc9743b9c0de6e95ec72ce04f8a2632603f174bc4a10bde1df8e0e9ecab8d2f4` |
| E-V003/key_ascii_65536 | RAW / C14N_VALUE_ARITHMETIC | 65542 | 65542 | `308a4b09d5fc3db0a5be22158b5d0fa0b4735e2b7c7a2d2ae329b4e9b2beb45f` | `308a4b09d5fc3db0a5be22158b5d0fa0b4735e2b7c7a2d2ae329b4e9b2beb45f` |
| E-V003/key_ascii_65536 | DOMAIN / C14N_VALUE_ARITHMETIC | 65542 | 65564 | `28b83375cb073eaf7627b10bf3fe58321ff4e074184f94dd60c38fa30469dff6` | `28b83375cb073eaf7627b10bf3fe58321ff4e074184f94dd60c38fa30469dff6` |
| E-V003/key_control_65536 | RAW / C14N_VALUE_ARITHMETIC | 393222 | 393222 | `bfc85fa2f00989110948872884aae4b97b8bcae576087388b48e5ed76d6f93e3` | `bfc85fa2f00989110948872884aae4b97b8bcae576087388b48e5ed76d6f93e3` |
| E-V003/key_control_65536 | DOMAIN / C14N_VALUE_ARITHMETIC | 393222 | 393244 | `8f5a254037ad331442623ca603ed2f9d3fcaa8c47a6b30104935bd79681ff3c3` | `8f5a254037ad331442623ca603ed2f9d3fcaa8c47a6b30104935bd79681ff3c3` |
| E-V003/key_pair_65536 | RAW / C14N_VALUE_ARITHMETIC | 65542 | 65542 | `8a1104742ef697bdc66bcf6f69e913f4cf8ee792c6480809e1097f8563d2cab8` | `8a1104742ef697bdc66bcf6f69e913f4cf8ee792c6480809e1097f8563d2cab8` |
| E-V003/key_pair_65536 | DOMAIN / C14N_VALUE_ARITHMETIC | 65542 | 65564 | `a3bb4bc33f0a0a1eb0c403b31110ac544fd8537b886c473d5f967734be488e4a` | `a3bb4bc33f0a0a1eb0c403b31110ac544fd8537b886c473d5f967734be488e4a` |
| E-V003/value_ascii_65536 | RAW / C14N_VALUE_ARITHMETIC | 65544 | 65544 | `409834cf4ec0a19f532a1eebaee1eb093466217c376ee5cf5e67260852328cf8` | `409834cf4ec0a19f532a1eebaee1eb093466217c376ee5cf5e67260852328cf8` |
| E-V003/value_ascii_65536 | DOMAIN / C14N_VALUE_ARITHMETIC | 65544 | 65566 | `0fa52a3be1d51af7c257ea4c448e4ee84efa34ffa51008e04872e46c1ef68388` | `0fa52a3be1d51af7c257ea4c448e4ee84efa34ffa51008e04872e46c1ef68388` |
| E-V003/value_control_65536 | RAW / C14N_VALUE_ARITHMETIC | 393224 | 393224 | `a0be5695cfb09c8e278de5706ff88e76500e79dfc877c6bc48f6e1235fbc93bb` | `a0be5695cfb09c8e278de5706ff88e76500e79dfc877c6bc48f6e1235fbc93bb` |
| E-V003/value_control_65536 | DOMAIN / C14N_VALUE_ARITHMETIC | 393224 | 393246 | `db979c030fef3758ca0db62cd56236c22a1c21c43f26e70dd6b9da0837e5d9e4` | `db979c030fef3758ca0db62cd56236c22a1c21c43f26e70dd6b9da0837e5d9e4` |
| E-V003/value_pair_65536 | RAW / C14N_VALUE_ARITHMETIC | 65544 | 65544 | `cb4bb4290382d1e7f711758a1ad856ab95487d3de58311426fe3fd953293702e` | `cb4bb4290382d1e7f711758a1ad856ab95487d3de58311426fe3fd953293702e` |
| E-V003/value_pair_65536 | DOMAIN / C14N_VALUE_ARITHMETIC | 65544 | 65566 | `08fdceb194e7b7a222a44339bd072523dab8fe193e61954d6f5d72efc44b4787` | `08fdceb194e7b7a222a44339bd072523dab8fe193e61954d6f5d72efc44b4787` |
| E-V003/standalone_pair | RAW / C14N_VALUE_ARITHMETIC | 6 | 6 | `7a0c50b92434b015545fe93ab723db2d4b2cdd14a441405624a9ce8be29f1d5a` | `7a0c50b92434b015545fe93ab723db2d4b2cdd14a441405624a9ce8be29f1d5a` |
| E-V003/standalone_pair | DOMAIN / C14N_VALUE_ARITHMETIC | 6 | 28 | `b39e0a2b71bf4499567a0e5ccaf0259092ed3c8e604510d39cd8aa99388e8b7f` | `b39e0a2b71bf4499567a0e5ccaf0259092ed3c8e604510d39cd8aa99388e8b7f` |
| E-V004/C_ENV | RAW / ENVELOPE_PREIMAGE_NOT_SEMANTIC_VERDICT | 3206 | 3206 | `35383fc2952dde8f386f7653eae6793aa43c443c59048d574ec276006e4cdd0c` | `35383fc2952dde8f386f7653eae6793aa43c443c59048d574ec276006e4cdd0c` |
| E-V004/C_ENV | DOMAIN / ENVELOPE_PREIMAGE_NOT_SEMANTIC_VERDICT | 3206 | 3228 | `31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64` | `31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64` |
| E-V004/N0 | RAW / SYNTHETIC_ENVELOPE_BYTE_PREIMAGE_ONLY | 315 | 315 | `48afc7dc6f952270de62d6c2ea4532f929dfa0dc3e18e2c87bf5e205f8071dde` | `48afc7dc6f952270de62d6c2ea4532f929dfa0dc3e18e2c87bf5e205f8071dde` |
| E-V004/N0 | DOMAIN / SYNTHETIC_ENVELOPE_BYTE_PREIMAGE_ONLY | 315 | 337 | `92a1306ff4f1e1ffd545900df15ac78947711832a599f23128ca39faa1bfb5f9` | `92a1306ff4f1e1ffd545900df15ac78947711832a599f23128ca39faa1bfb5f9` |
| E-V004/N1 | RAW / SYNTHETIC_ENVELOPE_BYTE_PREIMAGE_ONLY | 315 | 315 | `c6f8aef79dd244b71d88e3a681865a10faf971605fd977f866e43349a5fae748` | `c6f8aef79dd244b71d88e3a681865a10faf971605fd977f866e43349a5fae748` |
| E-V004/N1 | DOMAIN / SYNTHETIC_ENVELOPE_BYTE_PREIMAGE_ONLY | 315 | 337 | `672f3a51abf1b2abdc4971bc580d59274038f9b0f129f0c08e6a8e5d8cf4f921` | `672f3a51abf1b2abdc4971bc580d59274038f9b0f129f0c08e6a8e5d8cf4f921` |
| E-V005/raw_abc | RAW / SUPPLIED_RAW_BYTE_HASH_ARITHMETIC | 3 | 3 | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |

No mismatch observed. Hash agreement proves only the specified byte computation. Scope: VERIFIED_OFFLINE for E-V001–006, PARTIAL for E-V007; all PG behavior/native/provider/production checks NOT_RUN. **STOP BLOCKED_CONTRACT: missing CM-069 private-order contract.**
