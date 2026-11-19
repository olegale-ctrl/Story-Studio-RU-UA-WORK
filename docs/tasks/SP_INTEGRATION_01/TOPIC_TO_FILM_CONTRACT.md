# Topic-to-Film contract

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

Implemented scope: offline request classification, deterministic detached intent, read-only intermediate observations and non-authorizing readiness/release diagnostics. Integration status PARTIAL_IMPLEMENTATION. No task is submitted. All proposed job types remain unsupported until an approved API and implementation are supplied.

`classify(topic=None,script=None,plan=None,materials=None)` requires exactly one nonempty primary input. Topic→A; script→B; plan→C; plan plus nonempty declared material map→D. Invalid or ambiguous input is rejected, never silently downgraded. A defaults to draft; production A adds CLASS_A_PRODUCTION_POLICY_REQUIRED. Other production routes also remain blocked on execution authority.

`prepare_intent(...)` copies inputs, validates plan/material declarations, records requested attestations and returns proposed stage names. Material declarations bind role, portable relative path, supplied raw SHA-256 and byte_length; they are unverified declarations, not fetched files, proof of ownership or typed PG references. CLI does not dereference the material map or resolve paths relative to an implicit current directory. A trusted future broker must define root, allowed inputs and exact byte snapshots before any use.

`intent_sha256 = canonical_si_sha256(body)` over schema/policy/route/mode/fallback/inputs/requested_attestations/proposed_job_types, before adding its own digest/status/blockers/accepted IDs. Reuses existing bounded SI canonical primitive; not RFC JCS, not PG-C14N-1, not a globally scoped identifier or idempotency receipt. Unchanged requests yield the same comparison hash. Changed content, policy, mode, declarations or fallback changes it. No JobStore duplicate suppression is claimed.

CLI examples (run at repository root):

```sh
python scripts/topic_to_film.py --topic 'Синтетическая тема'
python scripts/topic_to_film.py --script /absolute/path/script.txt --mode draft
python scripts/topic_to_film.py --plan /absolute/path/scene_plan.json
python scripts/topic_to_film.py --plan /absolute/path/scene_plan.json --materials /absolute/path/materials.json
python scripts/topic_to_film.py --topic 'Тема' --authorize-render --wait 5
```

Valid preparation prints JSON to stdout and exits **3** with BLOCKED_DISPATCHER_CONTRACT and accepted_job_ids `[]`. Invalid input/unsupported options exit **2**. No success exit, accepted IDs or completion is fabricated. `--wait 1..300` returns BLOCKED_JOBSTORE_CONTRACT immediately: absent observer API, it neither sleeps nor creates a poll/retry loop. No `--skip-gates`, output directory, overwrite, cleanup, queue/retry/resume or live-provider option exists. CLI cannot persist meta artifacts; future storage publication contract is blocked. Redirecting stdout is the user's shell action, not a protected publication protocol.

No direct `first_video.build`, `topic_to_video.run`, experimental pipeline build, subprocess render, provider, model, JobStore, Library mutation or network call occurs in this path. Input-read size/regular-file/link checks are diagnostics under a stable trusted local filesystem, not hostile-filesystem qualification. A plan can change between observations: no execution is authorized from these observations.

Attestation switches record intent only. A future verifier must establish actor/authority, evidence, exact identity/revision/hash scope, intended operation, policy, expiry, revocation and currentness under approved contracts. This task provides no trust registry, signature algorithm, permission issuer or validity override.
