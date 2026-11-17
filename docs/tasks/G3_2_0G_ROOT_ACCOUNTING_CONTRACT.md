# Root accounting — approved units and finite offline convention

**DOCS_ONLY + OFFLINE_VECTORS. F-D02/A and F-D03/A: APPROVED_LIMITED_SCOPE.**

SI-INTEGRATION-G3.2.0g; 2026-11-17 (Europe/Kyiv). No implementation, PG API, production authority or G3.2.1.

## Sources and evidence labels

[Owner approval](G3_2_0G_OWNER_APPROVAL_FD02_FD03.md), direct task §1 F-D02/A, outranks historical F/C proposals only in the stated scope. [F pure options](G3_2_0F_PURE_CONTRACT_DECISION_OPTIONS.md) §2/§4 CM-022A provides the finite token/arithmetic vocabulary. [D P1](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-01–05 and [A canonicalization](G3_2_0A_CANONICALIZATION_SPEC.md) C01–C09 retain admissibility/Unicode distinctions. These documents are pinned in acceptance packet.

`APPROVED_LIMITED_SCOPE` marks owner-approved principles. `FIXTURE_LOCAL_PROPOSAL` marks the complete-input offline token convention, not production parser semantics. `OPEN_CONTRACT_DETAIL` marks unselected details; `VERIFIED_OFFLINE` marks actual finite counting/byte comparisons. None is a PG machine result, runtime implementation or new resource denial.

## G-AC-01 — approved root occurrence units

For a complete root JSON fixture count occurrences, not distinct decoded values or distinct names. Container roots are values. A key is an additional key node, not a string-value node. Do not deduplicate repeated decoded keys or depend on map insertion/iteration order.

| Counter | Conceptual definition | Status |
|---|---|---|
| N_value | Every JSON value occurrence, including root/nested containers and scalars | APPROVED_LIMITED_SCOPE F-D02/A |
| N_key | Every decoded object-key occurrence, additional to value nodes | APPROVED_LIMITED_SCOPE F-D02/A |
| N_total | N_value+N_key | Derived arithmetic, no cap selected |
| M_total | Every object-member occurrence, including duplicates | APPROVED_LIMITED_SCOPE F-D02/A |
| T | Separate lexical-token occurrences under finite convention below | Separation approved; exact offline vocabulary FIXTURE_LOCAL_PROPOSAL |
| D_key | Sum decoded UTF8 byte lengths of key occurrences | APPROVED_LIMITED_SCOPE F-D02/A |
| D_string | Sum decoded UTF8 byte lengths of string-value occurrences | APPROVED_LIMITED_SCOPE F-D02/A |
| D_total | D_key+D_string | Derived arithmetic, no cap selected |

## G-AC-02 — complete-input finite token convention

**FIXTURE_LOCAL_PROPOSAL**, task §6.2/F optionA: each scalar token1; each key string token1; each opening/closing brace/bracket1; each comma1; each colon1. Whitespace has no token but still contributes wire bytes. A string is one token regardless of raw escape expansion/decoded length. Number -0 is one token, not separate minus/zero. A quoted string key consumes T and N_key, not N_value/D_string.

Empty array/object T=2. Nonempty array of n scalar elements, n≥1: N_value=n+1,N_key=0,N_total=n+1,T=2n+1. Object with m scalar-valued members, m≥1: N_value=1+m,N_key=m,N_total=1+2m,M_total=m,T=4m+1. The empty object m=0 uses the explicit T=2 rule, not extrapolated T=1; these are piecewise complete-fixture rules, not a newly selected parser architecture.

## G-AC-03 — decoded bytes are not characters or raw input

JSON unescaping precedes decoded-byte accounting; paired surrogate escapes form one scalar, no lone-surrogate normalization/coercion. No NFC/NFD/trim/casefold. `é` is1 codepoint/2 UTF8 bytes; 😀1 codepoint/4 bytes, whether literal or paired escapes. Raw quoted escape spellings/whitespace count actual wire bytes, not decoded D. D_key/D_string include each occurrence; empty strings contribute0 decoded bytes but their tokens/nodes still count.

## G-AC-04 — rejection and full-fixture accounting are separate

Repeated keys remain separate N_key/M_total occurrences even when decoded names match. P1-05/C03 subsequently rejects duplicates with expected PG_FORMAT stage2; neither complete syntax nor counting implies PG acceptance. G vectors account the **entire supplied finite complete fixture** for review, not the actual counter value at a production early-reject point. Existing local-cap-exceeding examples similarly have complete-input counters, not a claim a real parser reads/processes all bytes after denial.

Rejected/malformed work must not become free under F-D02/A. Exact production rejection-time counter semantics, streaming increment timing, partial-token charge and cross-parser malformed-prefix token stream are **OPEN_CONTRACT_DETAIL**. No malformed-prefix G vectors are supplied; no uniform invalid-prefix tree or tokenizer semantics invented. This avoids claiming retrospective full-input arithmetic proves online early-stop/memory enforcement.

## G-AC-05 — preserved local guards and OPEN global scope

Approved P1 root wire cap8388608 inclusive before decode; container depth64; per key/string decodedUTF8 cap65536 inclusive; per-array10000 inclusive. See D P1-01-WIRE-LIMIT/P1-02-DEPTH/P1-03-STRING-BYTES/P1-04-ARRAY-CARDINALITY. They remain independent guards; none supplies a numerical N/T/M/D/global CPU/RAM cap. Scalars/arrays used as value probes are not full PG envelopes.

Depth measures active container nesting, not total nodes. Per-array cardinality does not bound a collection of nested/sibling arrays. Key occurrences differ from unique names; tokens differ from raw character/byte count. **Root-only** scope does not approve referenced-object parsing/dedup, graph closure, aggregate ByteRefs, per-invocation reset rules or OP-07/08/09. F-D01/F-D04–F-D12 remain unapproved.

## Actual two-method verification boundary

[Root vectors](G3_2_0G_ROOT_ACCOUNTING_OFFLINE_VECTORS.md) are authored exact bytes/tuples. Temporary MethodA scans only these complete finite fixtures with byte grammar/token roles and independent JSON string escape decoding. MethodB decodes complete JSON with a pairs-preserving object hook, then derives occurrence counts and punctuation counts from the tree independently. Normal dict decoding is never the sole duplicate-key oracle. A unique-key mapping equality control is used only for two known nonduplicate order-permutation examples, not duplicate counts.

These are explicitly authorised offline accounting tools outside repository, not PG parsers/validators, serializers or runtime resource enforcement. All differences in length/counter expectations require BLOCKED_VERIFICATION; expected tuples cannot be quietly fitted to outputs. No new numerical limit, hash preimage/domain or denial code is introduced. No runtime/application/provider/Windows/render test ran.

**STOP — units frozen only in limited scope; CM-022 remains PARTIAL, OP-07 remains OPEN.**
