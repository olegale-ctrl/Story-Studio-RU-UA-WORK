# OWNER DECISION RECORD — MVP-08.0 / D01–D08

Project: Story Studio RU/UA
Decision date: 2026-11-18
Authority: Project Owner
Decision status: OWNER_APPROVED
Scope: Experimental MVP-08A and subsequent planning of MVP-08B
Research reference commit: f4661c86103bbcedf304201202203f20f3bb2747
Research reference path: experimental_mvp/reports/MVP_08_0_OWNER_DECISIONS.md
Important: The research document contains proposals, not the approved decisions. The authoritative owner-approved wording is reproduced below from the conversation.

## Approved decisions

D01 — Provider selection
Design the future dispatcher for Wan, Runway and MiniMax.
Begin implementation with one Wan adapter and one exact model version.
This does not authorize live API calls.

D02 — Budget
Initial budget: $0.
A possible future experimental budget of $10/month requires separate explicit owner approval.
No purchases, subscriptions, paid requests or automatic top-ups are authorized.

D03 — Browser automation
Browser automation is permitted only when the provider explicitly authorizes the relevant automation in writing and the exact integration has passed separate qualification.
No browser automation is authorized for MVP-08A.

D04 — Quota exhaustion
When the available quota is exhausted, pause the job.
An alternative already-approved API or fallback material may be offered within its existing authorization.
Never transition automatically to paid generation.

D05 — Usage rights
Require documented permission for the intended use, including rights to source materials, voices, music, and applicable attribution, territorial, duration and watermark requirements.
Unknown rights do not constitute clearance.

D06 — Rejection rate
Use 30% as the initial planning assumption.
Calculate sensitivity scenarios covering 10–50% rejection.
Replace assumptions with measured provider/model-specific data after separately authorized testing.

D07 — User confirmations
The user may approve a bounded batch of jobs and its budget once.
Require renewed confirmation when material conditions change, including provider, model, region, spending limits or sensitive data transfer.
No unlimited unattended spending is authorized.

D08 — Minimum MVP-08B scope
The future dispatcher must include:
- One provider adapter.
- A persistent, recoverable job queue.
- Spending controls.
- Secure MP4 retrieval and validation.
- Asset Library integration.
- Failure-injection and recovery tests.
MVP-08B implementation and live API qualification require their respective authorization gates.

## Approved acceptance and execution boundaries

MVP-08.0: ACCEPTED_WITH_LIMITATIONS.
MVP-08A: AUTHORIZED_EXPERIMENTAL.
MVP-08B.1: architecture/planning only until separately authorized for implementation.
Real API requests: STOP.
Payments and subscriptions: STOP.
Windows qualification: WINDOWS_NOT_RUN.
Main / merge / release / CI: STOP.
G3.2.1 and production permissions: STOP.
Production storage changes: STOP.

## Required Codex action

1. Use this exact decision record as the source for experimental_mvp/reports/MVP_08_OWNER_APPROVAL.md.
2. Preserve the distinction between the original Codex proposals and subsequent owner approval.
3. Record the research commit and source path.
4. Do not replace the approved wording with the earlier recommendation table.
5. Do not interpret these decisions as authorization for real provider requests, payments, production integration or release.
6. Continue MVP-08A within the previously authorized experimental boundaries.
No additional owner decision is required solely to resolve this missing wording.

## Source and implementation scope note

Authoritative source: owner reply in this conversation, 2026-11-18, to the missing exact D01–D08 wording question. The approved wording above is reproduced verbatim with Markdown headings/spacing only. The earlier Codex recommendation table is not substituted for it. Research files are read directly from the exact research commit, not merged. Implementation base: `96fcbe7e48bf5d5a6ba0c50dd6ba9eb21712e520`, tree `5dfe9e27b2c9617c6ee6bf8b841c7498d2aa1098`. This authorizes only local experimental Asset Library implementation/tests/evidence; no provider adapter or MVP-08B implementation is started. Windows actual execution remains NOT_RUN / WINDOWS_NOT_RUN.
