**Status: PROPOSAL — OWNER REVIEW REQUIRED.** Проверено 2026-11-18 (Europe/Kyiv).

Scope: DOCS_ONLY; экспериментальный MVP. Нет production permissions, реализации, покупок, регистрации, платных запросов, CI, merge или release.

# MVP-08.0 — Automated Video Generation Dispatcher

## Exact baseline, existing interfaces and missing pieces

Verified parent commit `91d274c554433fbc2145d5fc6b6a591199c0243f`, tree `38e2579cc3294fa5cf57b4d1bc267a37bfe078f8`; clean worktree before docs. Branch `docs/story-studio-experimental-mvp-08-0-provider-feasibility`. Later MVP-07.1 changes deliberately not imported: this task specifies exact MVP-07 base. No normative contract changed.

Every implementation fact below is from that exact Git object, read2026-11-18, confidence H (source inspection, not new test execution). Paths are relative to repository root.

| Component / source | Existing behavior / source locator | Integration boundary and gaps |
|---|---|---|
| `experimental_mvp/intelligence.py` blob `fb41052e2977a2d3dce115220f43043cf11a0d3b` | `generate` explicit confirmation, configurable OpenAI-compatible endpoint; `validate_draft`, `apply_draft`; output UNVERIFIED | Candidate topic/script input; not verified Evaluation, scientific review or production approval |
| `experimental_mvp/media_hub.py` blob `60d0c8e3d8f450350455aee89d6385f8051f3573` | `catalog`, `account_state`, `quota`, `plan`; manual login report, finite dated quota, no automatic refill; READY text explicitly manual | Future adapters separate from manual account state. No submit/poll/download, server reservation, persistent task queue or reliable charging ledger |
| `experimental_mvp/providers.json` blob `5fd003d639800b0499b1c410d63888c95e6df748` |13-service research catalog | Historical observations, not live capabilities; leave unchanged; future API channel catalog needs owner-approved versioned contract |
| `experimental_mvp/storyboard.py` blob `0cd9060b9650238a0c75a120d39a9a79dde0eed2` |VideoAnchor17fields; `fingerprint`, `import_asset`, `video_spec`, `render`; local content-hash cache/provenance |Bridge accepted Library asset→anchor; existing fingerprint hashes reference bytes but omits future provider policy/quote. Existing license_status is a label, not a grant. Not a managed Asset Library |
| `experimental_mvp/timeline.py` blob `86a98b2837e40bcabe9366d910f7b3a5f0fd6827` |`Editor`, `timing_map`, `measure_audio`, `coverage`, `preview`; IDs/interval edits, source trims, stale-apply checks |Attach to exact anchor revision; async result must not overwrite a newer edit. Timeline edits do not generate media. Whole-audio boundaries estimated/manual; no semantic alignment |
| `experimental_mvp/pipeline.py` blob `28aa1b7601be45a2d5dba713b04833270ac5041a` |`command`, `duration`, `build`, `render_preview`; local FFmpeg/FFprobe, audio cache, captions, hashes/evidence |Render validated local media; future remote ingest quarantine required. Cooperative cancel between commands at this base; no instant process kill. Not protected executor |
| `experimental_mvp/gui.py`, `media_ui.py`, `timeline_ui.py` |Existing manual form/Canvas editing, OS-player prerender flow |Future background dispatcher marshals events to Tk main thread; no UI-thread network polling. No implementation here |
| Existing reports |`MVP_05_06_ARCHITECTURE_AND_LIMITATIONS.md`, `MVP_07_LIMITATIONS.md`, `MVP_07_TEST_RESULTS.md` |Evidence of prior scope/limits; historical tests not rerun/relabelled. Existing `test_media_hub.py`, `test_pipeline.py`, `test_timeline.py`, UI tests are not provider adapter tests |

Missing: provider adapters, persistent remote-job ledger, quote/budget reservations, secure download/sandbox, provider-authorized free quota discovery, rights evidence records, Asset Library lifecycle, idempotency reconciliation, unattended quality oracle. Source code plus dated reports support these absence findings, not a proof of safe production.

## Proposed flow

Topic + target duration → editorial draft / evidence-needed claims → scene plan → VideoAnchor requirement snapshot → allowed provider selection → quote + consent + budget reserve → remote job → artifact quarantine → technical validation → editorial/rights acceptance → MVP-08A Library record → exact VideoAnchor revision → Timeline → local experimental export/evidence.

The approved target is automation with manual import as fallback. Automatic execution of a previously approved job/budget does not itself make editorial assertions true or grant commercial/production rights. PG normative contracts remain untouched; all records below are **experimental proposals**, not PG replacements.

## ProviderAdapter proposal v0

Interface returns typed, versioned records rather than provider-specific JSON in project files.

| Operation | Required result / invariant | Unsupported/error |
|---|---|---|
| `availability(context)` |channel,exactmodel,region,capability version,observed_at,expiry,eligibility evidence |UNKNOWN/BLOCKED_AUTH/BLOCKED_REGION; no login inference |
| `quota(context)` |balance/unit/origin/expiry/source, account_ref; separate API vsweb |UNSUPPORTED_QUOTA_OBSERVATION => explicit manual observation, never refill |
| `quote(plan)` |immutable plan hash, currency, conservative max charge, unit rules, input/output costs, quote expiry |UNKNOWN_PRICE/UNSUPPORTED_MODE => no submit |
| `submit(plan, consent_ref, attempt_key)` |providerjobid, traceid, resolvedmodel, accepted_time, charge status |UNSUPPORTED_IDEMPOTENCY advertised; ambiguous response => RECONCILE, not blind retry |
| `status(job_ref)` |normalized pending/running/succeeded/failed, rawstatus, updated_at, artifacts list |RATE_LIMIT with retry_after; timeout not terminal failure |
| `retrieve(artifact_ref)` |bounded bytes or vetted URL metadata, expiry,MIME,size; no auto-open |URL_POLICY/EXPIRED_ARTIFACT/INTEGRITY_FAILURE |
| `cancel(job_ref)` |acknowledged request and final charge reconciliation |UNSUPPORTED_CANCEL; user cancel doesn't prove provider stopped or refunded |
| `reconcile(attempt)` |known providerjob/ledger charge/refund/final balance |UNKNOWN_REMOTE_STATE => hold reservation; human resolution |

Common Error record: code, retry_class, provider/channel/model, internal_job_id, sanitized trace_id, occurred_at, safe_message, charge_state, next_action. Never rawheaders/body/tokens/URLqueries in logs. Classes AUTH, POLICY, ELIGIBILITY, QUOTA, BUDGET, INVALID_INPUT, MODERATION, RATE_LIMIT, TRANSIENT_GET, AMBIGUOUS_SUBMIT, REMOTE_FAILED, DOWNLOAD, VALIDATION, RIGHTS, STALE_TARGET, UNSUPPORTED. Retry only allowlisted operations; no model fallback without approved new quote/scope.

Provider facts backing adapter variation: inventory S04,S19,S21,S25,S36 async URL flows; S41 also MP4 bytes. Numeric limits are not invented. No requirement that every provider expose cancel, quota API, idempotency key or refund API.

## Queue, persistence, spending

JobRecord required: schema_version, job_id, project_ref, scene_id, anchor_id, anchor_revision/hash, script/claims-review refs, priority, created_at, updated_at, requestedmode(T2V/I2V), duration_ms, native_min_resolution, outputprofile, watermarkpolicy, promptref/hash, inputasset refs/hashes, providerchannel/model/region, policy_version, quote_ref, consent_ref, max_job_charge, monthly_budget_ref, reservedcost, attempts, provider_job_ref, state, resultassetrefs, failure.

State machine:

`DRAFT → BLOCKED_POLICY | WAITING_APPROVAL | WAITING_QUOTA | QUEUED → RESERVED → SUBMITTING → REMOTE_PENDING → REMOTE_RUNNING → RETRIEVING → VALIDATING → REVIEW_REQUIRED → ACCEPTED → ATTACHED`.

`SUBMITTING` crash/timeout → `RECONCILIATION_REQUIRED`; terminal failures retain charge state, artifacts and history. `CANCEL_REQUESTED` separate from confirmed `CANCELLED`; completed-after-cancel result quarantined, not attached. `RIGHTS_HOLD`, `STALE_TARGET`, `VALIDATION_FAILED` cannot become ACCEPTED merely by retrying download. STOPPED_BUDGET resumes only on explicit revised approval. Local states aren't written into normative G3 contracts.

Proposal: local transactional journal (e.g. SQLite, **owner-review choice**, no code now), durable atomic commits/fsync at transitions; never store secrets. Persist attempt fingerprint, reservation and SUBMITTING before network call. Deduplicate `(project,anchorrevision,planhash,providerchannel,attemptpurpose)`; unique active submission constraint across workers. No exactly-once promise: without provider idempotency/status lookup after lost response, doublecharge cannot be eliminated by local hashing. Hold and reconcile rather than resubmit.

On restart: acquire single-writer lease; recover reservations, poll knownjobids; unknown submit outcomes hold; resume downloads only when object identity/version verified. Account-month budget uses exact decimal/minor units and transactionally reserves maximum cost across concurrent jobs, including input charges, retries and tax allowance. Actual ledger debits settle; only observed refunds release money. Currency mismatch/price drift/insufficient cap blocks. No auto top-up or paid transition from trial. Provider-side hard caps required when available; local guard is not an absolute bound on external billing.

Scheduling: strict eligibility/mode/duration/rights/data-region/quality/budget filters first; then estimated accepted-second cost and measured success/latency. Priority with aging prevents starvation; per-account concurrency cap and jittered poll schedule. History initially UNKNOWN, never fictional ranking. Batch number and total reserved amount displayed before consent. Expired policy/quote requires revalidation. A pause does not erase outstanding provider liability.

## Result validation and Library handoff

Download to private perjob quarantine; vetted HTTPS, bounded size/time/redirects, no credentials forwarded to CDN; safe filename generated internally. Probe JSON with strict numeric finite bounds; media-only protocols; sandboxed full decode, process/memory/time limits; expected MIME/container/codecs, duration tolerance, resolution and stream counts. Compute SHA-256 after completed write, verify stable identity, close/reopen safe handle as qualified OS permits. Preserve original bytes separately from normalized derivative; record parent hash and FFmpeg arguments/tool versions. Technical PASS is not artistic PASS.

Editorial check: relevant visual content, prompt fidelity, temporal artifacts, continuity, factual/scientific accuracy, sensitive identity, speech sync/pronunciation and required evidence. Automated scorers can flag; initial acceptance REVIEW_REQUIRED, not auto-approved. No verified benchmark supports fully unattended artistic acceptance here. Rights missing => RIGHTS_HOLD. Mark generated reconstructions explicitly. No false documentary evidence.

**MVP-08A Asset Library record proposal** (no implementation): asset_id/revision;provider/channel/requested_model/resolved_model; provider_job_id;generated_at/received_at;prompt or protected promptref/hash/version;input_asset_ids/revisions/SHA; original_outputSHA256/path/bytecount/MIME; derived_asset refs/SHA; cost/currency/credits/quote/ledger; source_url redacted + expiry; rights_evidence refs/termsversion/territory/expiry/alloweduses/attribution/consent;watermark visible/invisible/UNKNOWN;technicalvalidation report/toolversions/status;artisticreview status/reviewer;linked project/scene/VideoAnchor IDs+revision;retention/deletion/tombstone state.

Required fields cannot be replaced by free-form provider name or UNKNOWN rights at final acceptance. Library commit and evidence publication must be atomic/recoverable, then anchor attachment via compare-and-swap on exact revision. Edited/deleted target: keep reusable asset unlinked, ask explicit reattach; no late result overwrites. Attach doesn't duplicate or delete originals. Fingerprint includes actual input bytes, exact model/settings and policy version; prompt change yields new job plan, not silent regeneration.

## Future conformance oracles — NOT_RUN

1. Expired quote/quota, NaN/negative cost, unsupportedmode, forbiddenregion, unknownrights: zero submissions.
2. Concurrent jobs exceed monthlycap: at most budget-reserved jobs submit; no floating-point drift.
3. POST succeeds but response lost; crash before savedID; repeatedclick/restart: hold ambiguous attempt; no automatic second POST.
4.429 GET respectsretry_after; terminal moderation not blindly retried; retry spending separately reserved.
5. Cancel running/restart/result late: no success attachment; external charge remains reconciled.
6. Malicious redirect/loop/private-IP/oversized/truncated/invalid media: quarantine, no project mutation.
7. Input substitution, stale anchor, changed prompt/model, corrupt libraryjournal: no ATTACHED.
8. Multiple output artifacts: all permitted outputs recorded individually, partial results explicit; charged unusable outputs remain cost.
9. ValidMP4 wrong scene/false scientific visual/unknownlicence: technicalPASS, editorial/rights hold.
10. Price/model retirement between quote and submit: blocked or new owner-approved quote, not automatic substitution.

These tests plus a separate Windows qualification and an explicitly authorized live experiment precede any implementation acceptance. Main/CI/production/storage remain STOP.
