# Proposed source correspondence and Git evidence contract

## Authorities and rows

Record authority per row family before extraction. Use the original decision or a later explicit scoped superseding decision for status. Preserve the older statement as historical provenance. Source packet indexes can locate originals. Where two applicable authorities conflict or ownership is unclear, report both with scope and stop the affected conclusion pending owner resolution. Missing, partial, truncated or undecodable retrieval leaves the relevant evidence incomplete.

Pin full commit, path and actual Git blob SHA-1. Check that the path resolves at that commit and that the object is a blob. Acquire complete bytes and preserve exact provenance. Git IDs identify Git objects. PG-C14N-1 and raw-byte integrity domains remain separate under P1-05. No new hash format is proposed.

An eventual documented Markdown subset would identify required sections and table schemas. Identify actual table blocks outside fenced code, verify separators and consistent column count, and handle escaped pipes according to the selected dialect. Unsupported multiline cells or ambiguous rendering require explicit treatment. Literal type names used as quoted historical evidence should be distinguishable from unresolved placeholders. Reject duplicate IDs before indexing. Review missing and extra IDs and compare every required cell by its documented identity. Preserve normative row order and explicit statuses. Where order is editorial, document that treatment and still compare exact row membership. Compare inherited adjacency maps without silently rewriting edges. Verify dependency target existence and acyclicity separately from approval.

## Git and publication

Verify the expected parent and tree against the candidate commit. Compare all base and candidate path, type, mode and blob IDs. An add-only allowlist requires the exact new paths in mode 100644 and preserved base entries. A repair requires the exact authorized changes. Record expected and observed values separately. Check fetched branches against the proposed Git object identities and repeat rendered-artifact verification on the fetched bytes or establish verified blob identity with the checked bytes. Working-tree success cannot prove remote publication. Recheck a moved ref before claiming the current branch points to the reviewed artifact.

For each check record the actual command or operation, scope, artifact identity, actual exit code when applicable and interpreted result. Keep self-reported statements separate from independently verified evidence. A planned check is NOT_RUN and has no exit code. A successful fetch does not prove a complete or meaningful artifact if output retrieval was truncated. Expected outcomes remain proposals where rules are open.

ACCEPTANCE-SHA-01 places the committed packet's own final Git blob SHA-1 in the external handoff. The packet may contain six verified sibling hashes and uses SELF_HASH_EXTERNAL_HANDOFF for itself. Preserve this arrangement without a new Git workflow.
