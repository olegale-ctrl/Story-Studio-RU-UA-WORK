# MVP-08B.2a-FIX-01 — COMMIT uncertainty, restart and fencing

Status: **PROPOSAL / DOCS_ONLY — OWNER REVIEW REQUIRED**. Date: 2026-11-20.

Project status remains **BLOCKED_CONTRACT**. This document proposes resolution of accepted findings; it does not approve EC-01–EC-10, G1–G6, implementation, real APIs, spending, storage, CI, main, merge, release or production permissions.

Source precedence: owner instruction in this conversation accepting the limited audit and F01–F05; exact independent review `3744eb5584e72e338dc51fa3a6fe7aed4882651b`; original freeze `c5cd33023880fd6726b74f5631eb766cc0959892`; original B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`; B.2 `04ea194e4d57c8a0550d7412281da58d4ba252c5`; SP/1.1 `16d28ec0376c8c28f879c8aacb18d5378fea83a3`. Historical documents remain unchanged. New PURE records below are proposals, not replacements for approved external contracts.

## F03 — mutation outcome is epistemic, not a lifecycle state

Keep three identities separate: immutable generation_operation_id/attempt_id/effect_token; stable StoreMutationIntent.mutation_id for one logical store mutation; current controller/worker fence for permission to perform that mutation. Neither lost ACK nor restart creates a new generation token. Retrying a different logical mutation with an old mutation_id is OPERATION_ID_CONFLICT.

| Observation of one mutation M | Store outcome | Required behavior |
|---|---|---|
| Explicit pre-COMMIT failure and complete intact consistent snapshot proves no M marker or linked members | NOT_COMMITTED | no authoritative change; bounded retry of same intent permitted after guards |
| Matching marker and entire valid atomic set in one consistent view | COMMITTED | return exact stored result, not a duplicate write |
| Exception during COMMIT; ACK lost; process dies before result known | UNKNOWN_COMMIT_OUTCOME | HOLD; do not infer rollback or success |
| After restart, complete same-store proof of all matching records | COMMITTED | resolve same M; continue only under current ownership |
| After restart, complete same-store proof of zero linked records | NOT_COMMITTED | resolve same M; revalidate before any retry |
| Missing marker but partial members, mismatched records or corrupt view | UNKNOWN_COMMIT_OUTCOME / STORE_CORRUPT | preserve barrier; no repair by guessing |
| Store unavailable or observation incomplete | UNKNOWN_COMMIT_OUTCOME / STORE_UNAVAILABLE | preserve barrier; never NOT_FOUND or NOT_COMMITTED |

UNKNOWN_COMMIT_OUTCOME is an operational namespace hold, not a new job state or proof record. A stable operation registry records immutable M and expected write-set bindings before a modelled commit attempt; the external fake test harness preserves the unresolved operation across simulated restart. This is a test precondition, not a claim that a real process can recover a volatile variable. Future durable implementation must qualify how unresolved M survives restart; if that record is unavailable, remain blocked rather than invent M or assume no acceptance.

During the hold, no namespace admission, state mutation, slot release, submit, cancel effect or retry is allowed. Read-only same-store resolution and transparent observation of the hold remain allowed. Malformed transport may be rejected but cannot clear the hold. A missing marker alone is insufficient; examine all M-linked records in one complete integrity-checked snapshot. A contradictory proof cannot downgrade unknown to no-write. No operator/manual repair API is in the proposed pure scope.

FakeStore must script failures before commit, during atomic boundary, after commit before ACK and after ACK. A simulated COMMITTED set must be all-or-nothing; a deliberately partial corrupt snapshot tests fail-closed resolution, not a valid transaction. These oracles do not qualify SQLite WAL, fsync, filesystem caches, power loss or NTFS.

## F04 — immutable evidence, current write authority

A provider acceptance/result receipt binds old immutable payload and generation IDs. It never carries current ownership. An old worker's callback is rejected, with zero job/event/error writes. After separately obtaining current controller ownership and a COMMITTED claim, the new controller may read-only look up the **same old effect token/payload**. It verifies namespace, ledger, provider job, cursor, profile, fixture and all association IDs. It then constructs a new APPLY_PROOF mutation under its current fence and current expected revision. The receipt remains unchanged; no identity is retokenized, and it cannot authorize its own application.

Proposed virtual ownership rules:

- One injected fake OwnerLock permits one controller. Incarnation monotonically increases in committed fake store state. TTL expiry alone never steals a HELD owner lock. Restart requires explicit test-harness evidence old owner is dead or released, then new acquisition and committed incarnation. No real OS lock is implemented or qualified.
- Worker claim is allowed only in QUEUED, SUBMITTING, SUBMISSION_UNCERTAIN, RUNNING, RETRY_WAIT, NEEDS_RECONCILIATION or CANCEL_REQUESTED. QUEUED initial claim requires no existing worker. Reclaim requires prior worker released/dead or proven expired under the same qualified clock, plus current controller ownership. No live owner/controller theft is allowed. All claims retain lifecycle state and cancel flag and increment lease_epoch and job revision atomically.
- Renewal requires exact current controller incarnation, worker ID, lease epoch, unexpired lease, current qualified clock epoch, expected revision and permitted source state above. It increments revision and extends lease under a bounded configured interval. It does not change generation IDs, lease epoch or cancellation intent. Expired or stale callers cannot renew themselves into authority.
- Each fixture defines positive lease interval L<=10000 virtual ticks before execution. New expiry=now+L, checked for overflow; renewal is allowed only if this strictly extends old expiry within the finite script horizon. Exact equality with expiry is expired. L is harness configuration, not native clock qualification.
- A clock epoch change or rollback gives CLOCK_UNQUALIFIED and hold. Do not compare ticks across epochs or convert unqualified clocks into forced expiry. A restart with incompatible epoch is blocked in the first scope; future reboot/native clock recovery is a separate decision.
- Applying recovered acceptance while cancel_requested=false follows guarded SM09 toward RUNNING. If cancel_requested=true, use SM31 toward CANCEL_REQUESTED, preserving cancellation; never use SM09 to clear it. No effect submission follows cancellation intent. Only verified settlement/nonacceptance proof permits guarded cancellation completion; a timeout is not settlement.

## Durable read reservations and retry meaning

Exactly **2 retries means 3 total calls** per checkpoint (initial call plus two). LOOKUP and POLL are independently typed checkpoint operations, not permission to generate again. Before each fake read, commit READ_RESERVED and increment calls_used. A crash after reservation consumes the slot conservatively even if no call happened. Unknown reservation COMMIT blocks the read until resolved.

No reset on restart, lease transfer, duplicate response, stale response, error or same cursor. A new checkpoint requires a verified, committed strictly newer provider cursor for the same generation operation and eligible current state; an initial checkpoint requires no prior checkpoint. Call indexes are 1,2,3, never zero or four. Three reservations without progress return READ_LIMIT_EXCEEDED/HOLD; no automatic override or second generation attempt. Cursor decrease or unrelated cursor is CURSOR_MISMATCH. Provider/result equality cannot be used to manufacture progress.

## Proposed recovery oracles — all NOT_RUN

R01 before commit/no members -> NOT_COMMITTED; R02 commit/ACK lost -> UNKNOWN then COMMITTED without duplicate; R03 genuine complete absence -> NOT_COMMITTED; R04 partial/corrupt -> unknown+STORE_CORRUPT; R05 unreadable -> unknown+STORE_UNAVAILABLE; R06 restart with missing unresolved identity -> hold; R07 stale callback -> no writes; R08 current reclaim + old receipt -> guarded new APPLY_PROOF; R09 cancellation preserved via SM31; R10 HELD owner cannot be stolen by TTL; R11 clock epoch change -> hold; R12 reserve/crash/restart -> consumed call; R13 duplicate cursor cannot reset; R14 known receipt with wrong payload -> RESULT_BINDING_MISMATCH; R15 claim mutation unknown -> no read/effect; R16 old generation token unchanged across all recovery paths.
