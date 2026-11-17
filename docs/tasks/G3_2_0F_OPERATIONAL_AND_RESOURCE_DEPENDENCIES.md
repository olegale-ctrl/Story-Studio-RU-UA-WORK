# Operational and resource dependencies — no simulated trust

**PROPOSED — NOT APPROVED. OWNER_AUTHORIZED_DOCS_ONLY.**

SI-INTEGRATION-G3.2.0f; 2026-11-17 (Europe/Kyiv). No implementation, merge or production authority.

Primary trust-sensitive scope is CM-070 and CM-095; CM-073 has a separate real no-effect boundary. Other rows require resource/resolver evidence before runtime claims. Source: [C operational governance](G3_2_0C_P5_OPERATIONAL_GOVERNANCE.md) OP-12/15/16/17/19/20/21/23/28; [C policy projections](G3_2_0C_P4_POLICY_CONTRACTS.md) OP-10/11/14/24; [A/B oracle matrix](G3_2_0A_ERROR_AND_ORACLE_MATRIX.md) COMMON-06/P04-04/P04-05/P05-03/P05-05/P05-07/NATIVE-01/02/03; [D normative](G3_2_0D_P1_NORMATIVE_CONTRACT.md) P1-06/26/27. These source OP protocols are proposals and qualifications absent; they are not upgraded here.

`BLOCKED_OPERATIONAL_EVIDENCE` is an evidence-plan label for claims lacking actual qualified trust, not an added PG error/machine verdict or the final dossier status. Preparing a reviewable decision dossier can be ready while the underlying execution/disclosure claims remain blocked.

## Requirement → trusted dependency matrix

| Requirement | Trusted dependency | Missing evidence | Possible failure | Qualification environment | Owner decision / current evidence status |
|---|---|---|---|---|---|
| CM-070 authenticated negative vs outage | Real selected issuer/provider and authenticated current head/policy | Real error taxonomy/provenance, absence proof vs unavailable, rollback anchor | Outage falsely treated as revoked/not-found, stale negative/positive accepted | Separately authorised isolated provider/OS/runtime with independent observer | F-D08 supplied claim model; F-D10 trust design. BLOCKED_OPERATIONAL_EVIDENCE |
| CM-070 chronology/time/revocation | Qualified clock/uncertainty, history/lease state and actual issuer | Trusted timestamps/currentness and causal ordering across events | Wall-clock rollback, forged ordering, revoked approval reused | Pinned host/provider/clock boundaries, outages/replay and restart observations | OP-10/11/12/15/23/28 still OPEN; no source/time authority chosen |
| CM-070 lost ACK/admission/completion | Durable admission ledger, executor and completion witness | Reserve-before-spawn/concurrent consume/reconcile/disk durability evidence | Duplicate physical execution, unobserved attempt claimed never started, fabricated terminal success | Selected real store/service/host, bounded fault/restart tests; process crash distinct from power loss | F-D10 protocol qualification or defer. BLOCKED_OPERATIONAL_EVIDENCE; not exactly-once physical execution |
| CM-095 reader/author/custodian authority | Actual approved identity/role/purpose and authenticated access channel | Real policy decisions and least-privilege enforcement observations | Display name/fake role becomes access; unintended upload/log disclosure | Separately approved private host/store/channel and actual authorised principals | F-D11/12 proposals only; no reviewer/custodian or publication permission assigned |
| CM-095 retention/erase/tombstones | Protected history/completion custody, authorised privacy/legal policy | Retention purpose/intervals/legal hold, erase/backup/copy semantics, no-resurrection proof | Deletion revives old approve; hidden backup copy or over-retention | Qualified store/backups/channel/audit, failure/restart/deletion observations | OP-21/23/28 OPEN, no duration/erase grant selected. BLOCKED_OPERATIONAL_EVIDENCE |
| CM-073 zero side effects | Actual runtime sandbox/capabilities and independent effect observer | Child process/files/network/store/ACL observations including denied cases | Correct DENY/report after forbidden effect; cleanup hides transient effect | Selected isolated OS/runtime plus external observer; Windows evidence required for Windows claim | F-D09 only future qualification scope; RUNTIME_TEST_REQUIRED |
| CM-006/022/071 actual resource/identity containment | Chosen parser/cache/resolver and qualified OS handles | Actual byte/read/allocation/time measurements, held identity/reparse containment | Alias/cache/budget reset/TOCTOU causes excess work or wrong input | Pinned platform/runtime/input corpus; Windows10/11 native path cases where claimed | F-D04/05 design then separate runtime/OS tests; not evidence from numeric schema |
| CM-072 actual tool/profile use | Immutable resolved tools/profiles, competent review and output inspection | Opened binary/config/asset identity and actual run/effect evidence | PATH override, wrong tool/profile, technical label masks content/rights change | Separately authorised runtime/OS/media qualification with review provenance | F-D06/07 pure/mixed decisions do not qualify real render or rights |

## CM-070 pure versus operational

Pure F-D08 may define supplied cause/provenance/subject/policy/event links and deterministic comparison, using only established facts and fixed seven-stage/category rules. It can distinguish a missing supplied ref from an explicitly unavailable dependency **as described evidence**, not verify that a real provider was unavailable. No generic exception is automatically mapped to PG_DEPENDENCY_UNAVAILABLE. Existing fixed categories do not supply the remaining provider-specific same-group distinctions or observed causal chronology. Avoid a circular rule that requires actual provider selection to discuss pure P1/report vocabulary.

Real authenticity, currentness/revocation, clock authority, actual reviewer competence/grants, event durability and observed execution order cannot be obtained from JSON flags, signatures with unqualified keys, local timestamps, array order or mock-provider success. Evidence remains BLOCKED_OPERATIONAL_EVIDENCE. A new schema cannot retrospectively certify a failed/unknown run. Lost ACK recovery must not imply zero execution or automatic rerender.

## CM-095 pure versus operational

Pure F-D11 may propose data minimisation, fixed safe-message projection and exact declared allowlist/policy refs. Selecting content fields is not selecting lawful purpose, actual readers, public release, retention duration, erase permission or logging implementation. No default public export or CI upload; even hashes/opaque identities can disclose membership and are not proven anonymous. No public diagnostics from private reason ordering. Public message safety does not prove real log/temp/backup/process traces are clean.

F-D12 requires actual policy owner/custodian, channel/store identity, access and retention/erase/legal-hold decisions plus qualification. No person/service is assigned here. Negative decision semantics cannot vanish and resurrect old approvals because a retention timer expired; exact minimised retained evidence/tombstone policy is an unresolved tradeoff for owner/legal/authority review, not an instruction to keep/delete real data now.

## Shared safety and qualification boundary

Storage S3 is the internal protected-storage track, not an assumed Amazon service; it is **not production-qualified**. Choosing a provider project does not qualify its trust roots/durability or lift disabled publication/reconstruction boundaries. Private-looking paths, repeated string checks or symlink tests on Linux do not prove Windows NTFS/reparse/ACL/handle behavior. CPU-only native Windows10/11 qualification was not performed, and actual media rights/scientific/editorial quality still require their independent reviews. No service, key, credential, real state, host/admin authority, rights licence or production grant was accessed/created by this dossier.

Future qualification needs exact owner-authorised platform/build/runtime/source/profile, threat model, allowed operations/observers/custody and explicit stop/rollback boundaries. Absent those, retain blocked claims; do not simulate trust or broaden privileges. **STOP — no implementation, provider operations, native tests, render or G3.2.1.**
