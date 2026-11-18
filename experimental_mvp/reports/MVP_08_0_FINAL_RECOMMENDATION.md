# MVP-08.0 — Final recommendation and independent audit packet

**Status: READY_FOR_OWNER_MVP_08_0_DECISION.** Все архитектурные рекомендации — **PROPOSAL — NOT APPROVED**. Проверено2026-11-18. Это завершение исследования, не разрешение реализации.

## Exact scope and identity

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Branch: `docs/story-studio-experimental-mvp-08-0-provider-feasibility`.
- Base commit: `91d274c554433fbc2145d5fc6b6a591199c0243f`.
- Base tree: `38e2579cc3294fa5cf57b4d1bc267a37bfe078f8`.
- Final commit/tree: определяются Git commit, содержащим этот документ; точные значения в итоговом handoff и внешнем `ACCEPTANCE_PACKET.json`. Не встраиваются в собственный tree во избежание циклического SHA.
- Diff scope: только восемь новых Markdown ниже, mode100644. Implementation, providers.json, main, CI, G1/G2/G3.1/G3.2.1 и normative contracts не изменяются. Никакие отложенные implementation-файлы PR#11 не переносятся.

## Deliverables / independent evidence navigation

1. [Provider inventory + S01–S48 official source ledger](MVP_08_0_PROVIDER_INVENTORY.md): идентичность, параметры, квоты, цена, rights, region, API/download/rate/retry unknowns, access failures.
2. [Automation feasibility](MVP_08_0_AUTOMATION_FEASIBILITY.md): A–F по каналам; documentary availability отдельно от live testing; top3.
3. [Free quota analysis](MVP_08_0_FREE_QUOTA_ANALYSIS.md): Qwen/Arena/free web vs API, количество outputs, daily vs trial, manual fallback.
4. [Dispatcher architecture](MVP_08_0_DISPATCHER_ARCHITECTURE.md): шесть exact baseline blob IDs, реальные interfaces/gaps, adapter/queue/selection/validation/Library proposals, NOT_RUN fault oracles.
5. [Daily production model](MVP_08_0_DAILY_PRODUCTION_MODEL.md): $0/$10/$20/$50, generated/accepted/coverage, 8/10/12min, discrete calculations and assumptions.
6. [Security risks](MVP_08_0_SECURITY_RISKS.md): threat controls, остаточные OS/storage/rights risks, Windows NOT_RUN.
7. [Owner decisions](MVP_08_0_OWNER_DECISIONS.md): D01–D08, альтернативы, рекомендации, risks/consequences; ни одно не принято за владельца.
8. This final recommendation.

## Key findings and classification

| Channel | Classification | Decision impact |
|---|---|---|
| Qwen web | D | Free unattended video not evidenced |
| Wan eligible legacy trial / paid | A conditional one-time / B | 50s/model trial is not daily; provider Free Quota Only first |
| Arena Video | D | Web automation explicitly prohibited; text API not video API |
| Kling direct | B, medium evidence | Full direct specs blocked by JS shell; defer qualification |
| PixVerse API | B | Technical candidate, commercial clauses unresolved |
| MiniMax direct | B | Async H3 API; no durable free entitlement proven |
| Runway Dev | B | Paid API separate from125 one-time webcredits |
| Renderforest template / AI web / AI API | B / D / F | Template renderer is not proved AI-clip endpoint; free marketing conflict |
| FusionBrain hosted video | F | Official docs unavailable; model specs not free hosted API proof |
| BotHub video API | B | Official paid async workflow; processor/model rights review |
| Google Flow / Omni API | D / B | Daily webcredits separate from paid token API; old preview retired |
| Sora | E | Web/app26Apr, API24Sep2026 discontinued |

No C candidate qualifies. A is a published conditional trial, not successful account qualification. All live provider integration **NOT_RUN**; no purchases, key creation, registration or paid API calls. No browser automation.

Top3 PROPOSAL: **Wan direct → Runway Dev → MiniMax direct**, for evidence clarity and integration fit; not a quality leaderboard. Start future scope with one exact approved model, not all adapters at once. PixVerse cost used for arithmetic only, subject to unresolved rights; Google Omni and BotHub reserve candidates.

## Throughput conclusion

Guaranteed recurring free automatic supply not established: planning0s/day. Conditional unused eligible Wan trial50generated seconds **once**, not perday. In a conditional $0.04/s output-only scenario with5s clips,30-daymonth,30%reject,80%usabletrim,25%AI-share: $10/$20/$50 give8.333/16.667/41.667generatedseconds/day;5.833/11.667/29.167accepted;4.667/9.333/23.333distinctAIcoverageseconds/day. Expected8/10/12min days26/33/39,13/17/20,6/7/8 respectively. Every quality/operational input is ASSUMPTION; other75% content must exist; taxes/FX/extra charges and queue/rights failures may reduce supply tozero. These values are not purchase authorization or guarantees.

## Source-access blockers and unresolved gates

Scoped `RESEARCH_BLOCKED_SOURCE_ACCESS`: FusionBrain home/API(502/inaccessible); Qwen SPA/terms empty extraction; Kling direct fullspec/legal JS shell; MiniMax fullterms emptytext; BotHub fullcatalog timeout; requested Runway outputs URL inaccessible. Official searchable excerpts markedM; missing legal/spec/entitlement fieldsU. Other open questions are **UNVERIFIED**, not falsely called source-access failures: region/account eligibility, full commercial chain, permodel rate/cancel/refund/idempotency, real download/quality and actualfreebalances. Research can be ready for owner decision while live qualification remains blocked.

Important conflicts: current Alibaba price table differs from older indexed snapshots; use current model-specific rows (newer models nofreequota). Renderforest marketing free/unlimited differs from subscriber-only help; template API requires subscription. PixVerse API§1.4 writtencommercialauthorization vs§5.3 outputcommercialuse requires clarification/order. Sora closure and Google preview retirement invalidate older catalog assumptions. Runtime catalog remains untouched; unsafe adapter selection must not rely on it in a future implementation.

Windows acceptance WINDOWS_NOT_RUN; no local Windows host available. Existing Linux implementation tests are historical baseline reports, **not rerun or claimed PASS in this DOCS_ONLY audit**. No FFmpeg render, human listening, provider-generated MP4 or visual-quality evaluation was performed. No claims that synthetic permit or technical schema grants production permission.

## Verification and reproduction

Documentation validation for this packet: exact parent/tree, eight-file allowlist/new100644 modes, UTF-8, relative Markdown links, required D01–D08, price/model arithmetic and `git diff --check`. These are documentation checks only. Command exit codes and final blob/SHA256 manifest are in external `validation.json`, `ACCEPTANCE_PACKET.json`, and exact `MVP_08_0_EXACT.diff`; no runtime test result invented. External evidence stays outside repository so changed scope remains eight documents.

Reproduce identity with `git show -s --format='%H %T %P' HEAD`; diff with `git diff 91d274c554433fbc2145d5fc6b6a591199c0243f HEAD -- experimental_mvp/reports/`; file modes/blobs with `git ls-tree -r HEAD`; compute SHA-256 from `git show HEAD:path` bytes. Validate links offline; recheck official source dates/terms online. Commit publication does not require a PR; no PR/CI requested or triggered intentionally in this task.

## Recommendation and STOP

Owner must choose D01 providers, D02 budget, D03 permitted web automation policy, D04 quota exhaustion behavior, D05 rights minimum, D06 rejection planning, D07 confirmations, D08 MVP-08B minimum. Asset Library08A/secure ingestion and Windows qualification remain dependencies; automatic editorial/scientific acceptance is not proven. Keep recommendations PROPOSAL until explicit owner decision after independent ChatGPT audit. **STOP: do not implement dispatcher, modify CI/main, merge, release, use production storage or issue production permissions.**
