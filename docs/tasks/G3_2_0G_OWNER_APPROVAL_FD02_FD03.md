# G3.2.0g — exact limited owner approval record

**DOCS_ONLY + OFFLINE_VECTORS. F-D02/A and F-D03/A: APPROVED_LIMITED_SCOPE.**

SI-INTEGRATION-G3.2.0g; 2026-11-17 (Europe/Kyiv). No implementation, PG API, production authority or G3.2.1.

## Exact authority text and provenance

The direct task SI-INTEGRATION-G3.2.0g §1 is reproduced below verbatim as the documentary authority. Uploaded task `Вставленный текст.txt`, SHA-256 `199e9887c14734c91a7730998df2fbb768ef0a592f70211932954b7424847cae`. This identifies task bytes; it is not an operational identity receipt, rights grant or qualified signature/provider action.

> The owner explicitly approved:
>
> **G3.2.0f — ACCEPTED_DOCS_ONLY.**
>
> **F-D02/A — APPROVED_LIMITED_SCOPE**
>
> Approve only the accounting-unit direction for root JSON resource measurements:
>
> - Each JSON value occurrence is one logical value node.
> - Each decoded object-key occurrence is an additional logical key node.
> - Object-member occurrences are counted separately.
> - Lexical tokens are counted separately.
> - Decoded UTF-8 bytes of keys and string values are accounted separately.
> - Rejected or malformed input must not receive free unmetered work merely because it is rejected.
> - Accounting must not depend on object insertion order, map iteration order, or deduplication of repeated keys.
>
> This approval does **not** select numerical global limits, parser architecture, operational resource enforcement, referenced-document accounting, whole-invocation budgets, or the complete OP-07 contract.
>
> **F-D03/A — APPROVED_LIMITED_SCOPE**
>
> Approve only a non-authoritative external result-report direction:
>
> - Retain existing pure verdict namespace: `CONSISTENT_NO_AUTHORITY` and `DENY`.
> - Preserve approved safe public error code/message behavior.
> - Keep private observations separate from public output.
> - Do not introduce a new PG API, machine verdict, grant, permission or execution authorization.
> - A report cannot prove zero runtime side effects.
> - `STRUCTURALLY_VALID` remains descriptive only.
>
> No actual report serializer, API endpoint, consumer, provider or permission is authorized.
>
> **All other decisions remain unchanged:**
>
> - F-D01 and F-D04–F-D12: `PROPOSED — NOT APPROVED`.
> - All 20 OP-07–25 and OP-28: `OPEN — NOT APPROVED`.
> - All seven CM-006/022/070/071/072/073/095: `PARTIAL`.
> - X01–X04, OP-01–06, OP-26/27 and P1-DIAG-01 remain unchanged.
>
> Do not infer broader authority from this task.

## Pinned accepted F provenance

G3.2.0f ACCEPTED_DOCS_ONLY, exact task base `85952f8b55965da5b9bb4fc3c23144b6f35fa1f8`, tree `fe818fe6df653566b87047d0d0daf603ecd3ee3f`, parent `ceb561109f8f18cd9e585a9b950bdf88034498a3`. Read-only main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.

- [F pure options](G3_2_0F_PURE_CONTRACT_DECISION_OPTIONS.md), blob `e371a41b6ebb45f3fff990c24e67b574e804e72e`: §4 CM-022 optionA / CM-073 optionA. Only the directions explicitly stated above are selected.
- [F owner dossier](G3_2_0F_OWNER_DECISION_DOSSIER.md), blob `a71e03f527ec907257966e9b6b9110d20724ce42`: F-D02/F-D03; entire F-D02/03 proposals are not expanded beyond this task's limited text.
- [D approved P1](G3_2_0D_P1_NORMATIVE_CONTRACT.md), blob `e082c93e25ceb9fbed415becb3b47fe867ff0d1d`: P1-01–06/26/27 remain unchanged; X01–X04 and P1-DIAG-01 retain exact prior scope.

## Approved principle versus finite fixture convention

F-D02/A approves **root occurrence accounting direction**, not numerical global caps, parser architecture/rejection-time semantics, referenced-document/global invocation accounting or complete OP-07. Detailed token vocabulary below is explicitly a finite F optionA `FIXTURE_LOCAL_PROPOSAL`; it is not a global runtime tokenizer decision.

F-D03/A approves **non-authoritative external reporting direction**, not a JSON schema/API/report serializer/consumer, new verdict or access/publication/retention policy. Illustrative wrappers and exact field order/empty projection are **FIXTURE_LOCAL_NON_NORMATIVE**; they are not production fields or new PG01–PG05 records. No report canonicalization/hash domain is created.

All7 CM-006/022/070/071/072/073/095 remain PARTIAL; OP-07–25 and OP-28 remain OPEN — NOT APPROVED; F-D01/F-D04–F-D12 remain PROPOSED — NOT APPROVED. No implicit typed-reference closure, provider, host/rights qualification, production permission or merge.

**STOP after publication — independent ChatGPT audit and separate owner decision.**
