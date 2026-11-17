# P3 — formal resource model and candidate workload profiles

**DECISION_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0c; 2026-11-17 (Europe/Kyiv).
Base `0d6d9076ab535c1b258206beb4e4fe9c005e79e1`, tree `e55c00d0e7a95218e0978dd9677172608395ff5f`.

Primary OP-07/08 (PURE planning classification), both unresolved whole-parameter choices. P1 caps and P2 reference identity feed this model; CPU/RAM/native enforcement needs later evidence. **No benchmark results, parser implementation, validator or qualification were produced.** All profile figures below are unapproved policy caps on logical workload, not measured safe thresholds.

## 1. Counter definitions and accounting domains

| Counter | Exact proposed unit | Accounting rule |
|---|---|---|
| W | Root wire bytes actually read | Includes BOM/whitespace/binding field; before decode; limit+1 sentinel, no unbounded read |
| W_j | Bytes of each typed referenced JSON document | Count actual bytes once per distinct typed object; each document has its own wire/depth guard |
| D | Sum of decoded UTF8 key/string-value bytes | Count every occurrence, not unique strings; global across parsed root+typed dependencies |
| N | Total JSON nodes: each value node **plus each object-key node** | Containers count as value nodes; keys count separately; duplicates/invalid inputs still consume budget before rejection |
| T | Lexical tokens | Each string/key, integer/bool/null, opening/closing bracket/brace, comma, colon is one token; no count per character inside a string |
| A / O | Number of array/object containers | Subsets of N; root container included; count before growth |
| S | Number of string occurrences including keys | S≤N; per-string cap independent of D |
| d_json | Max active container nesting | Scalar0/root container1; reset per document, global N/D/T do not reset |
| U | Distinct typed reference nodes | Exact P2 identity; same exact object reused once for validation/cache work, conflicts deny |
| E | Declared reference edge occurrences | Repeated/shared-child edges still count; no hidden scanning of arbitrary opaque JSON |
| d_ref | Longest active reference dependency path | Separate from JSON nesting; bounded traversal stack/work queue; cycles follow X03 split |
| B_ref | Sum actual referenced bytes read/validated for distinct immutable identities | Not only descriptor length. Different IDs with same bytes counted separately unless a separately reviewed resolver proves safe identity equivalence |
| C | Canonical byte output for each document | Streaming hash possible; never assume full canonical buffer free. Own binding exclusion applies only where specified |
| CPU_cost / M_peak | Actual CPU/work and peak memory | Must be measured on selected runtime/algorithm/profile; no numeric safety ceiling claimed here |

Global N/T/D include all typed JSON payloads actually parsed during the bounded check, not a fresh unlimited allowance for every reference. Opaque binary/evidence blobs contribute B_ref even when not parsed; no automatic remote loading. Ref metadata that claims a small length does not authorize reading past actual budget. Counting policy is itself PROPOSED and must be frozen before guards/tests.

Output-file inspection/render output bytes need a distinct OP-18/19 budget. They are not silently free because B_ref was an input budget. Tool/model weights may exceed initial profiles; that is an explicit legitimate rejection, not grounds to hash only a prefix or trust a small descriptor instead of real content.

## 2. Deterministic bounds, not measured performance

For one valid JSON tree with C_cont containers, L scalar-value nodes and K key nodes: N=C_cont+L+K. Array child count and object members determine punctuation tokens. Exact token accounting:

```text
T = scalar/key lexical tokens
    + 2 * container_count
    + sum_arrays(max(element_count-1,0))
    + sum_objects(member_count + max(member_count-1,0))
```

For a valid tree this gives a loose `T ≤ 3*N` bound under these units. It is not character-processing work; a single long string can be one token. `[0,…,0]` with10,000 scalars: N=10,001 and T=20,001. An object with m scalar members has N=1+2m; a per-array cap does not bound object members. Independent object-member cap is needed or covered conservatively by N/W.

Strict UTF8 decoding/unescaping without normalization gives decoded-string bytes D≤wire bytes of that document; escapes may shrink, never justify an unbounded decoded buffer. Across root+typed refs, D≤W+sum(W_j), while B_ref also covers binary reads. Canonicalization removes outside whitespace and uses fixed escaping; it still allocates/copies unless implemented as a bounded stream. Hash input prefix/own-binding accounting is separate.

Reference traversal can be linear in U+E **if** exact identity caching and edge visiting rules are enforced; repeated parsing/hashing of the same object would invalidate that reasoning. Key sorting adds work roughly of the form sum over objects of `members * log(members) * key-comparison work`; long common prefixes make comparisons expensive. This is algorithmic reasoning, not a seconds estimate or proof that a particular map/parser cannot be attacked.

## 3. Three resource profiles — PROPOSED only

P1-derived caps are policy starting proposals; **unsupported new resource numbers remain OPEN**. Parenthesized values only define illustrative arithmetic scenarios for discussion, not selected recommendations or evidence-backed capacities. Choosing a row requires explicit owner approval and future profile-specific fixtures. No automatic retry with a larger row.

| Guard / unit | Conservative | Balanced (starting proposal) | Large dossier |
|---|---:|---:|---:|
| Root W and each typed JSON W_j | 4MiB | 8MiB | 16MiB |
| d_json | 32 | 64 | 64 |
| Per decoded key/value string | 32KiB | 64KiB | 128KiB |
| Per array elements | 2,000 | 10,000 | 20,000 |
| Per object members | OPEN (illustrative2,000) | OPEN (illustrative10,000) | OPEN (illustrative20,000) |
| Global N root+parsed dependencies | OPEN (illustrative100,000) | OPEN (illustrative250,000) | OPEN (illustrative500,000) |
| Global T root+parsed dependencies | OPEN (3*N scenario300,000) | OPEN (3*N scenario750,000) | OPEN (3*N scenario1,500,000) |
| Global decoded D | OPEN (conditional20MiB) | OPEN (conditional72MiB) | OPEN (conditional272MiB) |
| U distinct reference identities | OPEN (illustrative1,024) | OPEN (illustrative4,096) | OPEN (illustrative16,384) |
| E edge occurrences | OPEN (illustrative4,096) | OPEN (illustrative16,384) | OPEN (illustrative65,536) |
| d_ref | OPEN (illustrative32) | OPEN (illustrative64) | OPEN (illustrative128) |
| Aggregate B_ref actual referenced bytes | OPEN (illustrative16MiB) | OPEN (illustrative64MiB) | OPEN (illustrative256MiB) |
| CPU deadline / cancellation granularity | OPEN | OPEN | OPEN |
| Process RAM cap / allocator headroom | OPEN | OPEN | OPEN |
| Render/output byte budget | OPEN via OP-18/19 | OPEN via OP-18/19 | OPEN via OP-18/19 |

D caps20/72/272MiB are conservative arithmetic accounting ceilings W_root+B_ref (4+16,8+64,16+256), **not predicted decoded allocations**. T=3*N caps avoid internally contradictory N/T maxima; tighter token guard could be separately selected. U/E/d_ref values are deliberate finite design options, not evidence-backed machine limits. B fixture V043-S6's2-node cap does not approve any row.

### Conditional maximum workload and tradeoffs

No fully selected/accepted resource profile exists while cells remain OPEN. Conditional acceptance, **if** separately selected and qualified, is the **intersection** of all counters and field-specific schema/semantic constraints; maxima need not be simultaneously attainable. A root at wire boundary can still fail N/d_json/schema. Referenced bytes can remain huge relative to metadata; counting only the descriptor would defeat B_ref. Shared child validates once by exact identity, edge occurrences still spend E.

| Profile | Likely legitimate rejection | DoS/security consideration | Product interpretation |
|---|---|---|---|
| Conservative | Long legal excerpts/large manifests/deep history, assets above16MiB aggregate | Lowest logical allowance; actual heap/CPU still not proved | Useful trial profile only, never substitute missing evidence with truncation |
| Balanced | Many nested arrays/keys, high-fidelity material/model assets above64MiB, long linked histories | Larger aggregate reads; sort/hash/decoder behavior needs qualification | Starting dossier proposal, not all real-video workload support |
| Large | Very large weights/footage or history still exceeds256MiB/input budgets | Largest exposure and caching/sorting headroom; needs strongest platform evidence | Only explicit profile choice; not automatic escalation to make a candidate pass |

Counter limits are not scientific/legal suitability tests. Small valid data can be wrong; large data can be legitimate but rejected. Error must remain explicit, original bytes preserved, no partial-hash claim, no silent dropped source/claim/asset.

## 4. Memory and CPU remain OPEN

An illustrative peak-memory model is:

```text
M_peak <= M_fixed + qW*live_wire + qD*live_decoded + qC*live_canonical
          + cN*live_nodes + cU*reference_registry + cE*edge_storage
```

Coefficients include actual runtime object/string representation, allocator overhead, duplicate buffers, caches and implementation strategy. They are **unknown**, not assigned guessed byte values. A DOM parser may retain raw+decoded+canonical copies; a streaming parser may reduce some terms but still needs duplicate-key/reference state. Python/other runtimes, UTF8/Unicode representation, OS allocator and 32/64-bit architecture matter. Numeric process-RAM/CPU/time caps cannot be claimed safe without future measurement and enforcement evidence.

Likewise no measured parse MB/s or timeout is asserted. Required later methodology, only after separate authorization: exact runtime/tool/source profile, adversarial common-prefix keys/escapes/depth/large arrays, many small documents/shared refs/conflicts, actual bytes/nodes/token counts, peak RSS/allocator observations, cancellation/limit-before-growth evidence, failed as well as successful runs. Deterministic logical counts are not benchmarks. A privileged OS memory/clock/provider configuration is not part of this docs task.

## 5. Guard ordering, testing and ownership

Root wire sentinel before decode/unbounded buffering; decoded byte/node/token/container increments before growing corresponding state; typed ref/edge/aggregate-byte counters before recursive resolution/reads. Exact internal resource-denial code/tie policy follows proposed OP-06/27, while approved X02 stage ordering is preserved. Guards discovered while resolving external closure occur at that dependency stage; they are not pretended known from root metadata.

Pinned V052–V059 and COMMON-04 inform byte/list/depth boundaries; V041/V042/V043-S4/V043-S6 inform identity/shared-child/budget models. They are not modified/re-executed here, and profile-specific new vectors/benchmark runs are **not created**. Pinned64/8MiB cases remain conditional for that profile; Conservative/Large alternatives do not rewrite old expectations.

OP-07 hard dependencies OP-01/02/03/04/09; OP-08 hard dependencies OP-07/09. Thus P1 can be reviewed independently, then P2 identity units, then P3 accounting/caps. No dependency on live provider to discuss logical budgets; actual CPU/memory/OS qualification is later and OPEN. **STOP — no implementation, benchmarks, native operations or production authority.**
