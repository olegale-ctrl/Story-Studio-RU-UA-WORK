**Status: PROPOSAL — OWNER REVIEW REQUIRED.** Проверено 2026-11-18 (Europe/Kyiv).

Scope: DOCS_ONLY; экспериментальный MVP. Нет production permissions, реализации, покупок, регистрации, платных запросов, CI, merge или release.

# MVP-08.0 — Automation feasibility

## Ответ на главный вопрос

Автоматический цикл через официальный платный API документирован у нескольких платформ. Бесплатный автоматический ежедневный поток Qwen Chat / Arena **не доказан**. У Alibaba подтверждён ограниченный **разовый API trial** для отдельных legacy Wan моделей. Это другой канал, с eligibility, сроком и риском платного продолжения. В этой сессии нет разрешения активировать trial или расходовать его.

Все external facts и confidence: [Provider inventory](MVP_08_0_PROVIDER_INVENTORY.md), источники S01–S47, проверено2026-11-18. Классификация — вывод исследования, не успешный integration test.

| Channel | Class | Evidence / reason | Integration disposition |
|---|---|---|---|
| Qwen web | D MANUAL_ONLY | S01–02 M/U; UI есть в index, free video API не установлен | Manual fallback; no unattended path |
| Wan / Model Studio eligible 2.1 trial | A OFFICIAL_API_FREE, conditional one-time | S03–04, S48 trial policy | Только будущая проверка eligibility + Free Quota Only; не durable daily supply |
| Wan paid / ineligible or expired trial | B OFFICIAL_API_PAID | S03–04 H | Candidate; no automatic paid fallback |
| Arena Video | D MANUAL_ONLY | S07–09 H; explicit web automation ban, text API не video | Exclude unattended integration |
| Kling direct | B OFFICIAL_API_PAID | S10–12 M, paid packages; specs partially blocked | Hold until full docs / contract qualification |
| PixVerse API | B OFFICIAL_API_PAID | S13–22 H/M | Candidate technical; written rights clarification first |
| MiniMax API | B OFFICIAL_API_PAID | S19–20 H | Candidate; privacy/rights/eligibility gates |
| Runway Dev | B OFFICIAL_API_PAID | S23–25 H | Candidate; budget and model allowlist |
| Renderforest template API | B OFFICIAL_API_PAID | S32 H active subscription mandatory for rendering | Defer: different product function |
| Renderforest AI web / AI API | D / F UNKNOWN | S29–32: web exists, generative API scope U | Manual fallback; no unlimited API inference |
| FusionBrain hosted video | F UNKNOWN | S34 U | Research blocked; do not activate |
| BotHub API | B OFFICIAL_API_PAID | S36 H paid completion/caps, S37 API release | Reserve; underlying rights/processor chain unresolved |
| Google Flow web | D MANUAL_ONLY | S40 H quotas, no permitted unattended route proven | Manual fallback only |
| Google Omni1.2 API | B OFFICIAL_API_PAID | S41–43 H | Candidate reserve, token cost and model drift gates |
| Sora / ChatGPT video via Sora | E UNAVAILABLE | S44–45 H/M shutdown | Exclude new generation |

A classification proves published trial terms and API mechanism, **not this account's entitlement or an executed download**. No C PERMITTED_WEB_AUTOMATION candidate: no explicit permission plus technical verification found. D means only human UI use is evidenced; it does not certify commercial export rights. F means unknown, not unavailable.

Trial policy evidence: [Alibaba free quota for new users](https://www.alibabacloud.com/help/en/model-studio/new-free-quota), H, checked2026-11-18, updatedNov16: Singapore International only, account information required,90days, auto PAYG after expiry/exhaustion, Free Quota Only disabled by default. This evidence is **S48** in the inventory; it supplements S03.

## Top 3 — предложение, а не включение

1. **Wan / Alibaba Model Studio**: documented T2V trial plus async artifact flow; strongest low-cost qualification path. Qualify *one exact* model/region first. Trial-only mode must be demonstrated provider-side; don't rely solely on local counter.
2. **Runway Dev**: clear paid setup, model pricing and output workflow; broad capability with explicit output-commercial clause. Higher cost and input retention/training terms require owner review. Disable model router by default.
3. **MiniMax direct API**: direct H3 specs and task/download workflow; avoids aggregator hop. No confirmed durable free API quota, legal/account and model-specific limits remain gates.

PixVerse could replace a candidate only after resolving commercial clauses S17§1.4/§5.3 and applicable order. BotHub not first choice until processor/sublicensing/retention path qualified. Google Omni is a reserve with current API, but token accounting and recent model migration add integration complexity. Ranking is based on evidence completeness/integration fit, **not measured visual quality**.

## Что не проверено исполнением

No API key/account/registration, provider submission, quota debit, MP4 download, retry/refund/cancel, or model quality test was performed. Therefore network integration, cost correctness and unattended reliability are **NOT_RUN**. Windows acceptance remains WINDOWS_NOT_RUN. Source-access failures are scoped in inventory, not a global claim that research was impossible.

Next experimental implementation requires owner D01–D08 approval, exact provider/model terms, budget guards and independent mock/fault conformance before any allowed live experiment. This document does not start MVP-08B.
