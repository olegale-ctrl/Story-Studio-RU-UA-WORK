# Research brief — external analytics / A-B / prediction technologies for Story Studio RU/UA
Date: 2026-11-04. Status: **candidate list / research assignment, NOT validated integration recommendations**.

## Mission
Independently inspect projects proposed by the user and determine which technologies, ideas, data contracts or algorithms can improve the **Story Discovery -> Evidence -> Editorial Scoring -> Human Selection -> Narrative RU/UA -> Video -> Outcome Feedback** pipeline. Work **read-only** first. Do not merge external code or execute unknown install scripts. Main Sprint 26 and experimental PR #5 remain untouched.

## Candidate register
| ID | Candidate | Claimed focus | First verification |
|---|---|---|---|
| C01 | https://github.com/Hwangbot/Shortform-Signals | Short-video engagement / retention, 1000-video dataset, Tableau | Repository observed; check dataset provenance, synthetic-vs-real, licenses, metric definitions |
| C02 | https://github.com/msertdev/keepwatching | Retention measurement | Verify exact repo URL, code, license and dataset |
| C03 | `yt-retention` (owner not supplied) | CSV retention-curve analysis | Resolve canonical repository, avoid name collision |
| C04 | https://github.com/sxnnywu/reeled-in | Neural A/B testing | Verify repo and meaning of A/B; actual randomized exposure vs offline comparison |
| C05 | `oximedia-analytics` (owner not supplied) | Experiment assignment / significance | Resolve canonical repository and API |
| C06 | `content-thumbnail-package` Agent Skill (owner not supplied) | Title/thumbnail variants | Resolve repository, terms, copyright, experimental validity |
| C07 | https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025 | Trend prediction | Verify existence, model files, training provenance and leakage |
| C08 | https://github.com/darderrdur17/ViralIQ | Top-1% virality prediction | Verify repository; distinguish unrelated proprietary apps named ViralIQ |
| C09 | https://github.com/Hashi-AI/Video-retention-analysis | Retention-curve regression, claimed R² 99.46% | Verify dataset, split, target leakage, generalization and baseline |
| C10 | `TIML` (research project, no canonical link) | Bilibili multimodal popularity | Identify paper, DOI, official code, license, datasets |
| C11 | `TARPA` (research project, no canonical link) | YouTube retention | Identify paper, DOI, official code, license, datasets |
| C12 | https://github.com/gomcpgo/youtube_analytics | Own-channel YouTube Analytics OAuth, retention | Independently inspect API limitations, credentials, license and deployment security |
| C13 | https://github.com/tarekmasryo/youtube-tiktok-trends-dataset-2025 | Synthetic cross-platform trends dataset | Dataset explicitly synthetic; useful for schemas/tests, **not** evidence of real predictive performance |

The list is not proof all names resolve. C01 was visible publicly on 2026-11-04; C12/C13 also surfaced publicly in initial discovery. All others require verification. Do not infer nonexistence solely from a failed search. User-supplied descriptions are hypotheses to test.

## Mandatory evaluation for each candidate
1. Repository existence, canonical URL, latest stable commit SHA, maintenance status, real entry points, tests, runnable demo.
2. Features: advertised vs implemented vs agent/manual vs nonfunctional; reproduce minimal behavior or mark UNTESTED.
3. Data provenance: real vs synthetic, source/rights, temporal span, sample selection, collection bias, platform access and privacy.
4. Retention metrics: actual audience-retention curve vs completion-rate proxy; first 3/30 seconds, audience cohorts, censoring, denominator and confidence interval.
5. A/B tests: randomization unit, allocation, exposure, sample size, peeking/multiple tests, interference, platform support; generating two variants alone is NOT a controlled A/B experiment.
6. Prediction: pre-publication feature availability, train/test chronological and creator-level isolation, target leakage, baseline, calibration, class imbalance, uncertainty, independent test set, robustness RU/UA, and cross-platform validity. Treat R² 99.46% as unverified until reproduced with leakage controls.
7. Integration: interfaces, Python versions, CPU-only Windows compatibility, dependencies, maintenance, API credentials/costs, ToS, licensing of code, models, data and outputs.
8. Security: prompt injection in fetched content, untrusted media/CSV, unsafe deserialization, shell execution, OAuth token handling and secret leakage.
9. Verdict: ADOPT (with evidence and rights), REIMPLEMENT IDEA, EXPERIMENT, REJECT or BLOCKED. Never use ADOPT until verified.

## Expected deliverables
- `docs/research/EXTERNAL_TECHNOLOGY_MATRIX.md`: per-candidate evidence, exact file:line, reproducibility and verdict.
- `docs/research/METRICS_AND_EXPERIMENT_DESIGN.md`: metric definitions, ethical data collection and realistic randomized tests.
- `docs/research/PREDICTION_VALIDATION.md`: leakage review, holdout scheme, honest baselines, model cards and uncertainty.
- `docs/research/INTEGRATION_ARCHITECTURE.md`: minimal independent RU/UA architecture, interfaces, staged build plan, tests, license gates, CPU cost.
- `docs/research/RED_TEAM_REVIEW.md`: independently challenged claims, counterexamples, unresolved risks and response.

First pass must **not modify runtime code**. Report findings in Russian, with status FACT / INFERENCE / UNVERIFIED. A second reviewer should be tasked separately; do not claim one was consulted unless it actually ran.

## Research sequencing
1. Validate exact identity and rights of all 13 candidates.
2. Inspect metric/data acquisition and privacy (C01, C12, C13), then A/B and prediction candidates.
3. Produce integration decisions and architecture only after evidence is assembled.
4. Seek user approval before any code, installs, external API use, dataset ingestion or Sprint ZIP.

## Critical design distinction
Public metadata on another channel does not grant its private audience-retention curves. OAuth access to **one's own** analytics is different from internet discovery. An editorial score before publishing is not a measured retention probability. Model outputs trained on synthetic datasets are not proof of performance on real RU/UA videos.
