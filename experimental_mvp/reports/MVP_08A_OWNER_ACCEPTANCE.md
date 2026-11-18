**Status: OWNER_ACCEPTED_WITH_LIMITATIONS — recorded owner decision. New work: CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. All future behavior below is NOT_IMPLEMENTED / NOT_RUN.

**Evidence labels used throughout:** EXISTING = inspected at base `1ff403e47d35adb34139278de1d056fbbc563e6d`, not re-executed here; APPROVED = owner task plus unchanged D01–D08 in [owner record](MVP_08_OWNER_APPROVAL.md); PROPOSED = this new contract, not implementation authority; OPEN = unresolved gates in [decision register](MVP_08B_1_OPEN_DECISIONS.md). Windows qualification remains WINDOWS_NOT_RUN. No runtime, live adapter, downloader, executable tests, API calls, payments or production permissions are introduced.

# Owner acceptance of MVP-08A and authorization of MVP-08B.1

## APPROVED — new owner decision

Authority: Project Owner, task supplied in this conversation, dated2026-11-18. Accepted repository `olegale-ctrl/Story-Studio-RU-UA-WORK`; accepted commit `1ff403e47d35adb34139278de1d056fbbc563e6d`; accepted tree `2fecb71e711861431a775f4aa3764d771f35ecb5`. MVP-08A status **OWNER_ACCEPTED_WITH_LIMITATIONS** (ACCEPTED_WITH_LIMITATIONS following independent ChatGPT review, as asserted by the owner). This document records that owner decision; it does not claim this author performed the independent review. The independent review text itself was not supplied; no extra findings are invented.

MVP-08.0 remains ACCEPTED_WITH_LIMITATIONS. Exact D01–D08 wording in MVP_08_OWNER_APPROVAL.md is retained byte-for-byte; the earlier research recommendation table is not substituted. The old MVP-08A candidate report and old authorization record remain historical documents, not silently rewritten. This new decision supersedes only their pending-acceptance status.

## EXISTING accepted limitations and carried P1 issues

Trusted-user local SQLite/filesystem only; cached catalog status requires verification before use; residual TOCTOU/hardlink/reparse and power-loss risks; no decoder OS sandbox or authenticated legal evidence; incomplete imports abort and may need metadata re-entry; retained orphan binaries; historical links aren't current project truth; optional bindings need explicit portability decisions; minimal UI; bounded rather than instant cancellation. Windows/NTFS/ACL/native Tk acceptance is NOT_RUN. Rights revocation cannot atomically cancel an already-running native render.

P1-01: FFprobe nb_frames may differ from decoded frames. P1-02: preliminary Tcl/SIGILL lifecycle failure is not closed by later Linux passes. P1-03: no atomic transaction spans catalog link history, editor state and project JSON. All remain explicit future qualification gates.

## Authorization boundary

**MVP-08B.1: CONTRACT_PREPARATION_ONLY.** Read interfaces; write architecture/contracts/oracles and implementation sequence; all repository changes under experimental_mvp/reports/. No Dispatcher runtime, executable Wan adapter, executable tests or Python changes. No approval for MVP-08B.2–.5 implementation is implied. Initial budget remains$0. Real API/account creation/credits/payments/browser automation remain STOP, including advertised free trials. Main, CI, G3.2.1/normative PG contracts, production storage/permissions, merge/release remain STOP.

## PROPOSED / OPEN / NOT_IMPLEMENTED

The remaining fourteen documents are new proposals for independent review. Open decisions do not reopen D01–D08; they resolve concrete integration gaps. No future implementation or production action is authorized by acceptance of a prior stage.
