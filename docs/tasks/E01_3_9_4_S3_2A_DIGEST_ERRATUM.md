# E01.3.9.4 / S3.2a — Normative digest-byte erratum and restart instruction

**Date:** 2026-11-06.
**Scope:** Correct a transcription/escaping error in the **S3.2a Codex assignment only**. This is not a change to the owner-approved S3.1a protocol.
**Trigger:** `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core` at `210229308eb0293f4003c26d4c4e4e51ca18065d`, `docs/tasks/E01_3_9_4_S3_2A_RESULT.md` reports `BLOCKED_CONTRACT_CONFLICT`.

## Finding

S3.1a §3.3 at `cf70b8c0a93841f2bff272b584a2106374e3016f` is unambiguous:

```text
value_sha256 = SHA256(
    ASCII("story-studio-s3-2-lab-result-v1")
    || byte 00
    || R
)
R = exact canonical internal S1 Receipt bytes
```

**Normative separator:** exactly one NUL byte `0x00`. No literal backslash, x, 0, 0 sequence, no LF, no surrounding quotes, no trailing delimiter. `value_sha256` is a plain SHA-256, not an S1 MAC.

S3.2a task at `747ea3de5cb623df8fdfaa5dff6af58f893cc698`, §4 bullet describing terminal summary mistakenly rendered `b"\\x00"` (two backslash characters in its Markdown source) which evaluates to `5c783030` instead of `00`. This is a **task-author transcription/escape error**. It is not a substantive ambiguity in S3.1a. The latter remains unchanged.

**Correct reference Python (unambiguous and transport-safe):**

```python
import hashlib

def lab_summary_sha256(exact_canonical_internal_receipt_bytes: bytes) -> str:
    if type(exact_canonical_internal_receipt_bytes) is not bytes:
        raise TypeError("Receipt bytes required")
    return hashlib.sha256(
        b"story-studio-s3-2-lab-result-v1"
        + bytes([0])
        + exact_canonical_internal_receipt_bytes
    ).hexdigest()
```

`bytes([0])` intentionally avoids Markdown/JSON/backslash-escaping ambiguity. This reference code illustrates one separator byte; in production source S1 validation and internal receipt verification remain governed by the existing S1/S2 code and S3.1a requirements.

**Independent synthetic proof:** using `R=b"{}"` (not a valid Receipt, only an arbitrary shared byte suffix), the one-byte separator yields `66c044a3fa04b1baa95c05de618167622684843f04c4dde11e70add46870bcea`; the four-byte `5c783030` separator yields `8acda446a8aae48decc364502a3b476565fd8e9b3048a950ce6c5ec2e4854e25`. These are **synthetic discriminator vectors, not S1 golden values**.

## Resolution and precedence

1. The owner-approved S3.1a §3.3 `byte 00` is the **single authoritative definition** of the digest separator. The implementation must follow it.
2. This erratum **supersedes only the incorrect S3.2a assignment §4 separator example** at `747ea3de5cb623df8fdfaa5dff6af58f893cc698` and all inherited copies of that line. All other S3.2a instructions and previously approved L-01–L-04 / S3.2a split / hash sequencing remain unchanged.
3. Do not edit historic S3.1a or the historic Codex task, alter production S1/S2/golden, or bypass tests. Preserve the original `BLOCKED_CONTRACT_CONFLICT` report as an accurate historical STOP.
4. This narrowly fixes an assignment typo and **authorizes resuming the already owner-approved portable-only S3.2a** from the exact pinned erratum branch after successful verification of the byte rule. No new decisions are required for this typo; S3.2b and S3.3 remain STOP.
5. Add independent pure positive/negative tests proving `bytes([0])` and preventing a four-byte `5c783030` regression. Validate with an actual canonical internal S1 Receipt in addition to the arbitrary synthetic discriminator. Never send the raw receipt over LAB/1.
6. If any *other* semantic conflict emerges, STOP and submit a separate bounded report. Do not silently reinterpret contracts.

## Required Codex handoff

- **Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- **Base:** the final SHA of `docs/editorial-e01-3-9-4-s3-2a-digest-erratum` after publication. Pin the exact hash from the handoff.
- **New branch:** `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core-resume` (do not mutate the historical blocked branch).
- **Read:** this erratum first, then S3.2a owner decision, complete original Codex task, S3.1a contract and previous blocked result.
- **Allowed new files:** exactly the original S3.2a allowlist (`editorial/windows_lab/{__init__,protocol,fixtures,dispatcher}.py`, `tests/test_windows_lab_{protocol,dispatcher}_v1.py`, `docs/tasks/E01_3_9_4_S3_2A_RESULT.md`). The result file already exists on this base; **update it in full** to append/reconcile the new execution status while keeping the original BLOCKED report explicitly traceable in the retained Git commit history. Alternatively, STOP if the exact allowlist's existing-result constraint prevents a safe full replacement. Do not create any further files without an amendment.
- **Report:** new source SHA, changed files, all pure byte and policy tests, storage suite and full discovery, existing D-01, actual PASS/FAIL/BLOCKED, explicit no-native qualification, exact remote SHA.
- **STOP:** no PR/merge/release/main changes, no Windows VM, SCM, pipe implementation, native SID/ACL, protected writer, S3.2b or S3.3.

This erratum is purely a clarification of already-approved bytes. It does **not** substitute a successful LAB core test or native Windows qualification.
