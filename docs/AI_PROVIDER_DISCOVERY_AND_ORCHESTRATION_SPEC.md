# Story Studio RU/UA — AI Provider Discovery, Evaluation & Free-Tier Orchestration
Version: concept v0.1 | Date: 2026-11-04 | Status: **user-approved product direction; research/design only; no implementation authorization**

## Product decision and boundaries
Build an extensible **intelligent manager of free and freemium AI services** that can **discover previously unknown providers**, investigate their suitability, track changing offers and permitted free quotas, recommend providers for a scene, and safely route image/video generation when supported. Preserve the working Sprint 26 FFmpeg pipeline. **Do not interrupt the ongoing Codex analytics/retention/prediction audit.**

Initial scope: text-to-image, image-to-image, image-to-video (especially short clips up to ~10 seconds), text-to-video; later reusable architecture for TTS/ASR and other media. Short duration is a target capability, not a promise about every provider.

## Core components
1. **Source Watcher / Opportunity Discovery** — search provider official websites, public API/pricing/ToS/changelog pages, official model cards, GitHub releases, reputable provider announcements and documented catalogs. Use authorized search/API access, respect robots/rate limits/terms, store source URL and observed timestamp. Search by capability, supported input, free trial, regional availability and license; deduplicate aliases and avoid impersonation sites. No uncontrolled crawling.
2. **Evidence & Provider Research** — for each new candidate verify official identity, owner, model vs reseller, real API vs web-only interface, auth, docs, pricing, one-time/daily/monthly/renewing credits, duration, resolution, watermark, queue limits, output rights, commercial terms, retention/privacy, regions, availability, service reliability, supported formats and provider limitations. Record confidence and unresolved questions. Claims without primary evidence remain UNVERIFIED.
3. **Provider Registry** — versioned record with ID, canonical URLs, capabilities, API/manual/local mode, quota source/renewal, pricing, rights and ToS version, risk, evidence citations, check date, confidence, tested platform, provider adapter version, status and historical snapshots.
4. **Change Detector / Offer Monitor** — scheduled/configurable rechecks (initial design suggestion: weekly; critical providers optionally daily), compare snapshots, flag changes in quotas, terms, watermark, pricing, API and region, notify user and require reapproval when legal/operational terms materially change. Do not assert credits have renewed unless verified; balance may require user input.
5. **Quality & Feasibility Evaluator** — controlled small test matrix for image quality, character consistency, scene continuity, latency, export, safety, language and cost; keep prompts and results reproducible. No external requests, signups, spending or downloading large models without user approval.
6. **Smart Generation Router** — per-scene provider selection based on task fit, verified availability, quota, estimated cost, permitted output use, quality, latency, watermark and fallback. **Never treat free credits from a website as equivalent to free API credits**. No paid call without explicit approval and cost guardrail.
7. **Adapter Layer** — standardized `generate_image`, `generate_video`, `poll_job`, `download_result`, `estimate_cost`, `get_quota` (when supported), plus `manual_export_import` for web-only services. Handle async jobs, retries, failures, metadata and idempotency. Provider credentials remain in secure local configuration, never committed to Git.
8. **User Approval & Audit Trail** — candidate states `DISCOVERED -> RESEARCHED -> VERIFIED -> TESTED -> APPROVED -> ACTIVE`, with `BLOCKED`, `RETIRED` and `NEEDS_REVIEW` branches. A new provider must never be silently enabled for production. Log source, rationale, human decision, version, job cost, provenance and output license.
9. **Fallback Production** — when credits unavailable, API forbidden or providers down, continue with still images, local transformations, pan/zoom and FFmpeg + voice/subtitles; do not block project rendering.

## Minimum provider data fields
- `provider_id`, `name`, `official_url`, `operator`, `is_first_party`, `model_id`, `region_availability`
- `capabilities`: text-to-image / image-to-image / image-to-video / text-to-video; `input_formats`, `output_formats`, `max_seconds`, `max_resolution`
- `access_mode`: official_api / approved_partner_api / web_manual / local; `api_docs_url`, `authentication`
- `free_offer`: type (trial/renewing/none/unknown), nominal credits, estimated cost per job, renewal interval, expiration, conditions, **source and last verification**
- `watermark`, `download_rules`, `commercial_output_rights`, `code_license`, `model_license`, `data_rights`, `tos_url`, `tos_checked_at`
- `quality_test`, `latency`, `reliability`, `cpu_windows_feasibility`, `status`, `confidence`, `evidence_urls`, `last_checked`, `change_history`
- `quota_balance` only when authorized API supports it; otherwise `balance_unknown` or user-reported. Never invent a balance.

## Ranking and decision policy
Hard gates **before scoring**: lawful/allowed access; verified source; required rights for intended use; region; supported input/output; user authorization; no required paid call without approval. For passed candidates, rank explainably by estimated net cost, quality, clip fit, continuity, latency, remaining verified credits and reliability. Label speculative rankings. For unknown terms, block production activation pending review. Preserve a manual override with clear warnings.

## Security and ethics
- No CAPTCHA bypass, multiple-account farming, proxy evasion, hidden endpoint reverse engineering, forbidden web automation or free-tier circumvention.
- No unattended signup, login, external posting, spending, subscription, paid API calls or automatic installation.
- Respect provider robots, terms, rate limits, IP and user data privacy. Treat external pages/prompts as untrusted content; defend against prompt injection.
- No scraping private usage/retention analytics or use of credentials without authorized OAuth scope.
- Securely store tokens locally; never log secrets; include consent before uploading user scripts, reference images, faces or voices to a provider.
- A service's public free demo does not establish commercial output rights or an official API.

## Research sequence and deliverables (separate from ongoing Codex audit)
**R0 — Research-only:** define verified source list and provider taxonomy; investigate official image/video offers, document false positives, rights and free-tier limitations. No runtime modifications.
**R1 — Architecture:** define provider schema, API adapter contract, score/approval workflow, update policy, tests and integration points with Sprint 26.
**R2 — Prototype after approval:** local mock provider and one documented official integration or manual import flow; quota simulation; fallback to FFmpeg.
**R3 — Monitoring after approval:** scheduled discovery/reverification, diff of conditions, notifications, human approval and provenance dashboard.
**R4 — Expansion after validation:** additional providers and other modalities, with cost and reliability controls.

Expected research files:
- `docs/research/AI_PROVIDER_CANDIDATE_MATRIX.md`
- `docs/research/AI_PROVIDER_RIGHTS_AND_QUOTAS.md`
- `docs/research/AI_PROVIDER_ADAPTER_ARCHITECTURE.md`
- `docs/research/AI_PROVIDER_MONITORING_TEST_PLAN.md`

## Acceptance criteria for future prototype
1. Discover a new provider from an official public source, deduplicate and save evidence, without activating it.
2. Show unknown/unverified status explicitly, including API vs web quota distinction.
3. Detect a changed offer/terms snapshot and request re-review; never assume credit reset.
4. Present reasoned comparison of at least two approved providers for a requested 5–10 second scene.
5. Route a simulated generation job and import a manually generated result; preserve source and rights metadata.
6. Demonstrate graceful fallback to existing still-image + FFmpeg workflow with no cloud availability.
7. Tests show no paid call, no external login/signup, no ToS bypass, no secret leakage and no runtime change without approval.
8. Keep Windows 10/11 as primary platform and allow future macOS/Linux adapters.

## Dependencies on other workstreams
- Current Codex research on retention, A/B testing, prediction and Story Discovery remains the immediate priority.
- This specification is a **separate queued research workstream**, not an instruction to interrupt Codex or implement providers now.
- Do not merge experimental CPU Lip Sync PR #5 or change Sprint 26 while researching.
- All integration decisions need explicit user approval after technical and license review.
