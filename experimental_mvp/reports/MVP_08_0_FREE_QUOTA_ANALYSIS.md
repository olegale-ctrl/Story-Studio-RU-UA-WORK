**Status: PROPOSAL — OWNER REVIEW REQUIRED.** Проверено 2026-11-18 (Europe/Kyiv).

Scope: DOCS_ONLY; экспериментальный MVP. Нет production permissions, реализации, покупок, регистрации, платных запросов, CI, merge или release.

# MVP-08.0 — Free quota analysis

Evidence: [inventory](MVP_08_0_PROVIDER_INVENTORY.md) S01–S47 and [S48 trial policy](https://www.alibabacloud.com/help/en/model-studio/new-free-quota), all checked2026-11-18. H/M/U apply as defined there. Published quota is not account-observed balance; no login/generation performed.

| Channel | Refresh / requests / outputs per request | Download, quality, commercial | API, interactive / sequential / unattended | Conclusion and architectural effect |
|---|---|---|---|---|
| Qwen web | Daily refresh UNKNOWN; number requests/results U | Download-all, quality, commercial U | API-free U; interactive confirmation U; sequential UI use not unattended permission | D; guaranteed automatic seconds=0 |
| Wan eligible turbo trial |50s/model one-time,90day expiry; 5s output, example single video.10×5s arithmetic if unused, eligible and no other debits | API MP4 URL H,480/720p; watermark configurable; rights not fully cleared | Official API trial A; onboarding/account acceptance interactive; sequential submit/poll documented; no web scraping | Conditional pilot50s total, **not50s/day**. Enable provider Free Quota Only before any future trial |
| Arena Video |2generations/24h published; prompt shows2anonymous videos; wording doesn't establish4exportable clips/day |5–8s typical; resolution/watermark/download-all U; terms internal/personal plus commercial restrictions |Login/view/vote interactive; no video API shown; automated web access banned | D; no throughput or commercial supply promise |
| Kling web/direct |Start/day/month requests U; direct paid API does not prove free UI credits usable through API |Model/tier quality,download-all direct specs U; paid commercial clause M |Onboarding required; trial eligibility U; web permission U, API sequential NOT_RUN |B paid, free automatic baseline0 |
| PixVerse |Web free entitlement numeric U; API allowance not established; outputs/request model-specific U |API URL retrieval H; V6 resolution priced separately; commercial conditional/conflicting |Separate API balance; official async sequential supported by docs; live NOT_RUN |B; don't transpose consumer subscription |
| Hailuo/MiniMax |Consumer trial/day/month U; free API video quota U; one output URL documented |H3 4–15s,768P/2K; watermark U, rights gate open |API PAYG, sequential task workflow H; web quota not a freeAPI grant |B; planner cannot auto-refill U balance |
| Runway |Web125one-time, no daily free claim; API separate paidcredits |Web subset models; download watermark entitlement U; commercial terms conditional |API min$10, no free video API proven; async automatic path paid |B; initial webcredits not recurring capacity |
| Renderforest |Unlimited-free marketing conflicts with help Pro/Business-only zero-credit Fast |Fast4–10s vs whole-video12min distinction; free watermark; commercial tiers |API render requires subscription; explicit web automation permission absent |B template/D AIweb/F AIAPI; no infinite-free forecast |
| FusionBrain |Everything hosted quota-related U due502 |Kandinsky Lab open model specs ≠ FusionBrain downloads/rights |Hosted videoAPI/free/interactive/unattended U |F; RESEARCH_BLOCKED_SOURCE_ACCESS |
| BotHub |Free requests/credits/start/day/month U; exact outputs/request U |DocumentedMP4 unsigned_urls array, retrieve **all returned** artifacts if authorized; rights permodel U |Paid API H; webfree/API linkage U; sequentialpollH |B; no assumedfree throughput |
| Google Flow |50credits/day no rollover; first-generation reset; Lite10/generation non-Ultra.5×8s=40s/day **UI-only upper scenario**, capacity/eligibility not promised |720pLite, artistic reject U; rights/watermark/download-all U |Somefeatures create2videos/request, billed per generation; no freeAPI mapping or webpermission proven |D; exclude40s from unattended capacity |
| Google Omni API |Freevideo tier unavailable; requests perbudget, no Flowcredits mapping |Model-specificupscale/native distinction; quality/rejection not measured |Officialpaid programmaticMP4, no free quota claim |B, not freethroughput |
| Sora |No new generation after shutdown |Existing export window ≠ new supply |API closed |E; new capacity0 |

## Refill and accounting proposal

Future QuotaObservation should include provider/channel/account-reference/model/region/unit/balance/source/observed_at/expires_at/reset_rule/reset_timezone/credit_origin/eligibility/price_version. credit_origin enumerates ONE_TIME_TRIAL, DAILY, MONTHLY, PURCHASED. Do not refill from local calendar alone; don't sum non-fungible pools; count credits per output where provider charges that way. Balance UNKNOWN => WAITING_FOR_QUOTA. A fresh observed balance is still not a reservation.

No captcha/MFA automation, account rotation, exported cookies, hidden endpoints or unofficial API wrappers. Sequential API requests remain subject to provider rate and spend caps. Unattended *technical* availability does not approve unattended spending or release.

## Free conclusion

Guaranteed sustained automatic throughput supported by this research: **0 seconds/day** (no account-qualified recurring free video API established). Conditional Wan trial:50generated seconds once for the selected model, before expiry; at assumed70% acceptance35s; this alone cannot cover an8–12min film at25%AI share. Another model's trial must be evaluated separately, not multiplied from aliases. Local open weights incur hardware/time/licence costs; no Windows CPU-only video model benchmark, deployment or zero-cost claim made.
