**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. All future behavior below is NOT_IMPLEMENTED / NOT_RUN.

**Evidence labels used throughout:** EXISTING = inspected at base `1ff403e47d35adb34139278de1d056fbbc563e6d`, not re-executed here; APPROVED = owner task plus unchanged D01–D08 in [owner record](MVP_08_OWNER_APPROVAL.md); PROPOSED = this new contract, not implementation authority; OPEN = unresolved gates in [decision register](MVP_08B_1_OPEN_DECISIONS.md). Windows qualification remains WINDOWS_NOT_RUN. No runtime, live adapter, downloader, executable tests, API calls, payments or production permissions are introduced.

# Budget, quota and batch authorization contract

APPROVED D02: initial budget$0, future$10/month needs explicit separate approval. D04: quota exhaustion pauses, no automatic paid fallback. D07: bounded batch approval with reapproval for material changes. This is contract only; no ledger/reservation/API is implemented.

## Guard order

Before queue admission and again immediately before submit: verify current implementation authorization → execution mode/channel gate → exact capability/entitlement/availability → request/target/input hashes → batch scope/expiry/revocation → input/intended-use/data-transfer rights → price/maximum liability → atomic budget/quota reservation. For future offline core mode only locally authorized simulator with documented charge0 and LOCAL_ONLY data is eligible. A “free” live channel still fails the independent live-execution authorization gate, regardless of estimate0. No live free trial or credit activation is approved. A future independently qualified zero-cost live channel would still require a new explicit live-execution authorization/profile and proof of zero maximum liability; it is not enabled by this contract or by D02 alone.

All amounts integer minor units with explicit currency. ceiling0 means exactly0, not missing/unlimited. Unknown price/liability/FX/tax/charge rounding → PAUSED_BUDGET. CostEstimate stores base/input/output/reference/audio/rounding/tax/attempt upper bounds, immutable price version and expiry; never equate websitecredits to APIcredits. Estimated cost ≠ max liability or actual debit. Budgets cover account/channel/batch/job/attempt and overlapping concurrent reservations; no double counting across scopes.

## Durable ledger proposal

Reservation R keyed by job+attempt+batch revision; one transaction verifies sum(settleddebits + active/uncertainreservations) + max_new_liability ≤ every applicable cap, inserts reserve and submit-intent/outbox marker. Idempotent replay returns same R, not an additional reserve. Append-only entries RESERVE,DEBIT,VERIFIED_REFUND,RELEASE; unknown outcome keeps reservation held. Observed debit supersedes covered reserve without charging twice; provider rebate/refund only on verified ledger evidence. In offline simulator ledger all monetary entries0, but event/uniqueness/state assertions still exercised. This doesn't authorize spend when nonzero values appear in a fixture.

QuotaObservation separate from money: provider/account/model/region/channel,unit,balance,origin(one-time/daily/monthly/purchased),observed_at,expires_at,reset_rule/timezone,source_ref. No local-calendar refill. Reservation of quota and actual consumption distinct; stale/UNKNOWN observation pauses. Simulator quotas from fixture ledger only. Another provider requires existing authorization or new job/reapproval, never an implicit model switch.

## Retry/cancel/unknown accounting

Safe read/download/validation retries don't create new generation charge assumptions; any metered retrieval has its own liability cap or is blocked. New generation attempt reserves full maximum additional charge even for a failed previous output; reject-rate30% is planning only, not permission for “retry until good.” Sensitivity10–50% remains an assumption until separately approved measurements.

SUBMITTING crash/response lost → SUBMISSION_UNCERTAIN → NEEDS_RECONCILIATION; no release/new attempt on timeout alone. CANCEL_REQUESTED retains liability until actual outcome/ledger settlement. Cancel unsupported or late completion can be charged; neither user close nor local cancel implies refund. Reservation release requires known no-acceptance, verified settlement/refund or qualified simulator proof. Human “try again” without a new explicit uncertainty/liability decision does not waive caps or settle an unknown provider outcome.

## BatchPermit and expiry

Permit identifies exact job request hashes/purpose IDs, provider/model/version/region, data recipients/categories, cost/attempt caps, validity, reviewer authority and allowed local ingest/handoff actions. Revocation is an event consulted before every side effect. New provider/model/region, changed prompt/input/resolution/duration, increased budget/attempts, changed rights/data sensitivity or expired terms requires renewed approval; immutable old job is retained, replacement job explicitly linked. Expiry prevents new submissions; safe status/retrieval of an already-created result is allowed only if a separately explicit post-expiry containment/retrieval scope remains valid. Otherwise pause/reconcile, never silently extend consent (OD05).

OPEN: future authenticated permit authority and post-expiry containment policy, schema of provider-side hard caps, actual zero-cost eligibility. Default blocked; simulator fixture authority is not production authority. No actual reservation or billing reconciliation performed here.
