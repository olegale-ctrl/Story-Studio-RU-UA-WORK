# MVP-08B.2a-FIX-01 — Active intent and admission

Status: **PROPOSAL / DOCS_ONLY — OWNER REVIEW REQUIRED**. Date: 2026-11-20.

Project status remains **BLOCKED_CONTRACT**. This document proposes resolution of accepted findings; it does not approve EC-01–EC-10, G1–G6, implementation, real APIs, spending, storage, CI, main, merge, release or production permissions.

Source precedence: owner instruction in this conversation accepting the limited audit and F01–F05; exact independent review `3744eb5584e72e338dc51fa3a6fe7aed4882651b`; original freeze `c5cd33023880fd6726b74f5631eb766cc0959892`; original B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`; B.2 `04ea194e4d57c8a0550d7412281da58d4ba252c5`; SP/1.1 `16d28ec0376c8c28f879c8aacb18d5378fea83a3`. Historical documents remain unchanged. New PURE records below are proposals, not replacements for approved external contracts.

## F02 — two different uniqueness constraints

The full immutable AdmissionKey is defined in CONTRACT_RECORDS_AND_PREIMAGES.md. Separately, the active slot key is exactly **(store_id, project_id, purpose_id)**. NamespaceBinding binds the store; scene, anchor, provider, request hash, batch ID/revision and permit are NOT dimensions of the slot. Changing any of them cannot bypass one-active-intent semantics. All nonterminal states hold the slot, including RESULT_AVAILABLE, paused, cancellation-requested and reconciliation states. Only COMPLETED, CANCELLED and FAILED are terminal; their terminal status must be proven, never inferred from a client timeout.

One atomic admission mutation acquires the slot and writes job, ADMITTED event and original acceptance receipt. Failure means none of these is authoritative. RELEASE is atomic with the proven terminal job transition/event and new RELEASED slot version. Historical full keys, requests, receipts, event chain and slot history are retained. RESULT_AVAILABLE cannot release the slot; first pure prefix therefore cannot automatically schedule a replacement for the same purpose. An uncertain terminal COMMIT keeps the namespace blocked and slot unavailable pending resolution; no cached terminal state may release it.

## Deterministic admission order

1. Parse bounded closed transport and typed reference closure; reject malformed input. Establish namespace read authority. For a recognized namespace, check store integrity and unresolved COMMIT barrier before logical admission decisions.
2. Compare supplied full key with recomputed request/manifest/namespace content. Same supplied key plus different request/content is IDEMPOTENCY_CONFLICT, regardless of permit expiry. Identical digest but different bytes is STORE_CORRUPT. A mutation_id reused for different intent is OPERATION_ID_CONFLICT.
3. Look up the historical full key **before looking at the active slot**. With exact original request, key and initial permit bytes, return original receipt, disposition REUSED, no writes, no new effect, no permission refresh. This is a read with required namespace read authority; old permit expiry/revocation does not erase historical acceptance. Changing the initial permit on the old key is IDEMPOTENCY_CONFLICT, not a grant refresh.
4. For a genuinely new key, verify the permitted profile, current fake authority, exact manifest/request scope, revocation and half-open validity under qualified fake clock. A correctly recomputed new key with the old request's permit is AUTHORIZATION_SCOPE_MISMATCH. It must not be mislabeled an idempotency conflict. No grant means AUTHORITY_MISSING.
5. Only a valid new request can attempt the active-slot acquisition. An existing HELD slot returns ACTIVE_INTENT_CONFLICT, no revision/event/receipt/outbox/effect writes. Concurrent candidates cannot both win; the FakeStore must expose an atomic transaction model, not a check-then-insert sequence.
6. Commit admission under one stable mutation_id. ACCEPTED requires COMMITTED proof. Unknown outcome returns HOLD, never ACCEPTED or permission to submit.

Historical terminal replay returns the old receipt even when a newer job holds the same active slot. It cannot reacquire the slot, reopen the old job or revive its authorization. Store restore/namespace substitution is not an idempotent replay; identity must match the original store and integrity context.

## Proposed acceptance oracles — NOT_RUN

| Case | Setup / action | Exact expected outcome |
|---|---|---|
| A01 | Two different valid keys, same store/project/purpose, first active | second ACTIVE_INTENT_CONFLICT; one slot and job |
| A02 | Same exact active key/request/initial permit | REUSED original receipt; zero writes/effects |
| A03 | Old terminal exact replay while newer job active | REUSED old receipt; newer slot unchanged |
| A04 | New key while earlier RESULT_AVAILABLE | ACTIVE_INTENT_CONFLICT; no replacement |
| A05 | Terminal mutation committed with valid proof | release atomically; next valid new key may acquire |
| A06 | Terminal mutation outcome unknown | HOLD UNKNOWN_COMMIT_OUTCOME; no release/admission |
| A07 | Supplied old key, changed request | IDEMPOTENCY_CONFLICT |
| A08 | Correct new key, old permit scope | AUTHORIZATION_SCOPE_MISMATCH before active-slot test |
| A09 | Exact historical replay with expired/revoked permit, authorized reader | REUSED only; submit/refresh forbidden |
| A10 | Two concurrent transactions with same projection | one winner; losing candidate no partial records |

No test above has been executed. Durable uniqueness on SQLite/NTFS and restoration qualification are future gates, not consequences of a FakeStore result.
