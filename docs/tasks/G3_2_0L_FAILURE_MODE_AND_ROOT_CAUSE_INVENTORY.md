# Failure modes and root cause

At original K commit c038809, four required tables ended after their separators. Lines 41, 49, 55 and 59 held one string-array and three object-array type names. The recorded PowerShell assembly nested row arrays inside an outer array. Its shallow join converted the nested arrays to their type names. Source checks and Git checks passed while the artifact omitted 57 rows. FIX-1 restored the rows and documented the cause. The defect combines generation, incomplete rendering, validation gap and false-positive check. K's original proposal status and authoritative inputs survived.

The historical inspection compared original K with corrected K and scanned the A–J acceptance packets at the L base for a specific structural symptom: a pipe-table separator followed by a non-row. The scan flagged none in A–J. This narrow read-only check leaves dialect, row meaning, source correspondence and unstructured tables unevaluated. It changes no historical disposition.

| Class | Symptom and potential cause | Minimum evidence | Misclassification risk | Response | Inference boundary |
|---|---|---|---|---|---|
| GENERATION_DEFECT | Emitted rows differ after serialization | Same pinned input reproduces discrepant bytes | Blaming rendering for incomplete input | Repair the emission and recheck | Source correctness needs separate proof |
| SOURCE_DATA_DEFECT | Pinned source is missing or internally inconsistent | Exact source passages and expected record set | Using an informal summary as authority | Investigate source ownership | Output failure alone proves little about source |
| CONTRACT_AMBIGUITY | Two plausible rules resolve one row differently | Competing scoped readings | Treating a merely missing artifact as ambiguous | Defer and seek owner decision | No automatic precedence |
| VALIDATION_GAP | Required assertion absent from evidence | Check coverage compared with artifact defect | Confusing missing check with failed check | Add review evidence | No new code authorized |
| IDENTITY_MISMATCH | Observed Git ID differs | Exact expected and observed object IDs | Comparing names or different object types | STOP | Does not identify actor or motive |
| EVIDENCE_GAP | Claimed result lacks complete trace | Verification boundary and retrieval status | Equating absence with failure | Investigate or record NOT_RUN | No inferred test result |
| STALE_ARTIFACT | Material belongs to earlier revision | Two pinned identities and reference history | Treating historical evidence as invalid in its own scope | Re-fetch current target | No source corruption implied |
| UNAUTHORIZED_SCOPE_CHANGE | Extra path, changed approval or mode | Pinned scope and actual diff | Using a mutable summary as authorization | STOP | Does not establish malicious intent |
| INCOMPLETE_RENDERING | Missing table, cells or rows | Complete emitted bytes and expected inventory | Mistaking truncation during retrieval for emitted omission | Verify retrieval then repair | Source arrays may be intact |
| FALSE_POSITIVE_CHECK | Success reported despite unmet predicate | Success trace plus artifact-level counterevidence | Applying a check outside its stated scope | Withdraw affected claim and recheck | Other checks may remain valid |
| SELF_HASH_CYCLE | Packet asked to include its own final blob ID | Field requirement and Git byte dependency | Confusing sibling IDs with self-reference | Apply ACCEPTANCE-SHA-01 | No new hash scheme |
| NOT_REPRODUCED | Reported discrepancy cannot be confirmed | Read-only attempts and limitations | Declaring the artifact sound | Investigate or defer | No proven cause or absence of defect |
