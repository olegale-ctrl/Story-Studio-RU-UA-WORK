# Scoped source authority evidence model

| Concept | Evidence question |
|---|---|
| Source object identity | Which exact commit, path and blob supplied the bytes? |
| Source provenance | Who presented the claim, through which channel and in which project? |
| Claim identity | Which precise assertion and source occurrence is being assessed? |
| Row family and decision identity | Which register and decision does it purport to address? |
| Owner authority | What separate evidence supports the claimant's authority for that decision? |
| Approval status and effective scope | Which status applies to which field, action or research boundary? |
| Historical status | What was stated at the pinned source, including proposals? |
| Partial supersession | Which field changes and which original fields retain their status? |
| Revocation claim | What explicit evidence identifies the affected scope and effective boundary? |
| Conflicting claims | Which applicable statements disagree and on what field? |
| Missing authority | Which evidence is absent even though the source bytes are available? |
| Evidence completeness | Can an auditor retrieve every cited source and scope statement? |

| Model | Benefit | Unresolved risks and evidence |
|---|---|---|
| N-AUTH-A scoped mapping | Records a rationale for each family, decision and scope | Require pinned original approval, provenance and clear field boundaries. Avoid treating index rows as approval. |
| N-AUTH-B owner-maintained versioned manifest | Offers a reproducible view of scoped claims at a revision | Require provenance for each manifest version, linkage to original decisions and handling of partial amendments and stale manifests. |
| N-AUTH-C qualified chain | Preserves historical decisions and explicit partial supersession evidence | Require justified links and evidence for conflicting, missing or revoked claims. Newer commits supply chronology without deciding authority. |
| Defer | Preserves complete assertions and uncertainty | Keep affected claims open while owner authority or precedence remains unclear. |

A Git blob SHA-1 identifies retrieved bytes. Owner authority requires separate evidence. An acceptance packet can record a decision without creating one through its title or presence in Git.

The pinned M dossier at dde9c05 records M-D01 and M-D05 as proposals. The subsequent owner instruction for N approves only M-D01/A and M-D05/A for the specified closed-subset and scoped-authority documentary research. Retain the M proposal statements as historical. No adjacent alternative becomes approved. The exact source objects are in the acceptance packet; the later instruction is the scoped owner authority, not a Git blob inference.

The original K packet at c038809 and FIX-1 at 8c7468d differ in table rendering and the assessment. Compare the corrected rows with the unchanged dossier and source registers. FIX-1 is evidence of repair without a normative grant. No model, precedence or revocation policy is selected.
