# Version compatibility

**SP-INTEGRATION-01b · 2026-11-19 · LIMITED_DIAGNOSTIC_IMPLEMENTATION_CANDIDATE · no execution/release authority.**

Base: b4d787701295aa9d7c088e5116db9bd9de9a5f6e/tree c93da4e81be97edeb68883b7fe63938e43ffc14e. Exact historical SP implementation and37 tests unchanged; SP_INTEGRATION_01A documents/46vectors unchanged. External old execution evidence copied byte-for-byte and separately replayed;117assertions/46vectors match prior expected results exactly.

|Producer/object|Consumer|Result|
|---|---|---|
|SP/1-PROPOSAL object|Existing SP/1 schema/helpers|Historical behavior/limitations retained, not retrospectively repaired|
|SP/1-PROPOSAL object|1.1 validate_diagnostic|Reject version/policy, no automatic migration|
|SP/1.1-DIAGNOSTIC object|1.1 both-stage validation|Accept only if all current shape+semantic rules hold|
|SP/1.1-DIAGNOSTIC object|Old schemas|Reject schema_version constant; old helpers are not a comprehensive record validator|
|Fresh same source inputs|Explicit1.1 prepare_intent|New object/version/policy/body digest; no old grant,job ID or receipt carried over|

CLI defaults to legacy SP/1 to preserve its existing interface/tests. Explicit command:

```sh
python scripts/topic_to_film.py --contract-version SP/1.1-DIAGNOSTIC --topic 'Тема'
```

Both valid preparation paths return exit3 BLOCKED_DISPATCHER_CONTRACT and [] accepted IDs; invalid inputs/options exit2. --wait still blocks immediately, no polling. Flag selection is not authorization, conversion or schema inference. The caller must explicitly choose1.1 and create/validate a fresh object; there is no disk updater or migration of user projects. Changing a version string on an old object is insufficient because policy and digest differ and1.1 semantic/material rules also apply.

No central version constraint required BLOCKED_VERSION_CONTRACT: constants/schema consts already support independent diagnostic transports, and owner explicitly proposed1.1. All other identity/hash protocols stay separate: PG prefix bindings, raw byte SHA,SI record refs and proposed08B JCS-LOCAL-1 are not renamed. Historical APPROVED_WITH_LIMITATIONS for local SP/1 is distinct from independent acceptance of this implementation candidate.
