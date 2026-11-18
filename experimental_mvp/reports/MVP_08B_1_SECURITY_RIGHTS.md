**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. All future behavior below is NOT_IMPLEMENTED / NOT_RUN.

**Evidence labels used throughout:** EXISTING = inspected at base `1ff403e47d35adb34139278de1d056fbbc563e6d`, not re-executed here; APPROVED = owner task plus unchanged D01–D08 in [owner record](MVP_08_OWNER_APPROVAL.md); PROPOSED = this new contract, not implementation authority; OPEN = unresolved gates in [decision register](MVP_08B_1_OPEN_DECISIONS.md). Windows qualification remains WINDOWS_NOT_RUN. No runtime, live adapter, downloader, executable tests, API calls, payments or production permissions are introduced.

# Security, rights, Tk lifecycle and trust boundaries

APPROVED D03/D05/D07: no browser automation/live requests here; documented intended-use/input/voice/music/territory/duration/attribution/watermark permission; renewed approval on material transfer/provider/model/region/spend changes. Locally entered rights metadata is not authenticated legal evidence. Simulator fixtures may carry explicit self-authored local experimental evidence, never live-provider or production permission.

## Proposed gates and residual risk

|Threat / boundary|Proposed control|Existing limit / remaining qualification|
|---|---|---|
|Prompt/source leakage|Immutable approved byte manifest; classified inputs; exact provider/region/recipient/retention consent before submit; no sensitive data in fixtures/logs|Live data-transfer approval and provider retention/terms unqualified; BLOCK live |
|Rights / commercial use|Input rights before submit; output/provider licence evidence and intended-use review before attach/save; expiry/revocation current at boundaries|Asset metadata text/ownership/paid plan not legal authentication; don't auto-promote UNKNOWN to CLEARED |
|Credentials|Opaque ephemeral handle only in worker transport context; no credentials in jobs/projectJSON/SQLite/evidence/URL/logs; redact headers/query/exception bodies|No production credential storage designed or activated; simulator rejects credential fields |
|SSRF / untrusted download|Exact host/peer/redirect policy and limits from ingestion contract; quarantine+sandbox-qualified decoder proposal|String URL checks cannot close DNS/OS attacks; current Library is not downloader/sandbox |
|Budget double charge|Durable submit intent/reserve,qualified idempotency,uncertain outcome hold|Local CAS cannot undo remote side effects or prove non-acceptance; no automatic paid fallback |
|Job DB corruption / simultaneous workers|Schema/integrity checks,append-only events,lease epochs/CAS,outbox tokens,qualified durability|Hashchain alone not authenticated; quarantine corrupt DB, no regenerate-from-project guess |
|File/SQLite/JSON TOCTOU|Managed paths,hash+identity,explicit receipts/readback; preserve committed originals|Windows reparse,hostile writers,network shares,power-loss remain unqualified; no production storage guarantee |
|Late result/cancel/revocation|Known identity,quarantine/no attach after cancel; no refund assumptions; preserve liabilities|Current render cannot atomically enforce in-flight revocation; gate future executor separately |
|Editorial quality|Keep topic rationale,sources,scientific claims/required visuals,residual risk/reviewer separate from technical validation|Codec/schema/count PASS not relevance,truth,sync or production approval; no new artificial “approved” checkbox |

## P1-02 — lifecycle protocol (proposal, not closed)

Worker boundary: persistent controller/simulator/ingestion workers own plain immutable messages and local service handles only, **no Tk widgets,Variables,PhotoImages,bound widget methods or Tk-containing closures**. GUI bridge owns queue polling,session epochs and all Tk creation/access/destruction. Request/reply IDs include job,state revision,session epoch andtarget token. Code inspection must include indirect references/finalizers, not just explicit Tk calls.

Cleanup ownership: GUI thread invalidates session epoch and cancels only its after handlers, releases images/variables/registered commands in creating thread, drains/discards stale replies. Controller job lifetime is separate from panel lifetime: close is not remote cancel, not proof import stopped, not save confirmation. Reopen creates new session epoch, queries durable state, reapplies nothing until explicit valid target/CAS. A result for closed/older session may update durable job/artifact ledger under fence but cannot call Tk or mutate a newly edited scene. Crash/lost GUI acknowledgement handled by saga, not blindly repeating apply.

Base has daemon workers,queue+80ms poll,GUI-thread collection of prior Tcl garbage and resource release. These mitigations and later Linux passes do **not** prove the prior native Tcl/SIGILL risk closed. Proposed future dispatcher workers should be isolated from Tk ownership; OD06 considers process isolation vs strictly controlled threads. No process/thread runtime introduced here. Cross-thread finalizer bugs can exist without explicit off-thread widget calls; gc.collect alone isn't a security or qualification boundary.

Future stress protocol: deterministic delayed messages,100 close/reopen cycles and1000queued/reordered/duplicate replies per test seed, cancellation at every phase, thumbnails/imports during repeated panel destruction, worker exceptions/timeouts, GC pressure, app exit with pending workers, stale/new project sessions; record OS/Python/Tk/FFmpeg builds,thread/process ownership traces,callback exceptions,exit signals,leaked processes/after handles and bytes/project hashes. Numbers are proposed minimum qualification fixtures (OD06), not executed measurements. Any native crash,off-thread Tcl finalizer,late mutation or unowned callback is failure, not flaky-test retry-to-pass.

Windows10/11/NTFS/PowerShell/Tk/HiDPI and OS cancellation/handle cleanup require separate actual hosts; Linux/Xvfb does not substitute. WINDOWS_NOT_RUN persists. Resource/process/sandbox/network qualification belongs to MVP-08B.4 and a future separately authorized live pilot; no claim production credential management or protected storage is solved.

## Retention and secrecy

Preserve immutable originals/derivatives/provenance/evidence separately; no physical delete of a shared object while references may exist. Quarantine isn't permission to retain sensitive/licence-revoked data indefinitely; OD08 must specify reviewer,hold period,lawful deletion/retention exceptions and audit-safe redaction. Default pause/no new transfer/attachment; controller must not silently delete user originals or invent permissions. Secret redaction must be tested on nested metadata,headers,URLqueries,tracebacks and simulator fixtures. Any real secret/data incident follows separately approved handling, not automated publication of raw evidence.
