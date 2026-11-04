# Метрики, API и корректный экспериментальный дизайн

Дата: 2026-11-04. Это проект контрактов, не реализованный analytics/experiment module.

## Разные измеряемые величины

| Величина | Значение | Недопустимая подмена |
|---|---|---|
| Views / engaged views | Счётчики по определению платформы/версии/периоду | Нельзя смешивать разные definitions и eras без metadata |
| CTR | Clicks/impressions в определённом traffic scope | CTR не измеряет удержание после открытия |
| Average percentage viewed | Среднее watch time / duration при определённых population и playback rules | Это не вероятность полного просмотра |
| Completion fraction | Доля подходящих независимых просмотров/зрителей, достигших заданного конца | Требует определения denominators/replays/censoring |
| Audience-retention curve | Показатель по позиции видео из указанного источника | Не обязательно монотонная survival; повторы могут дать рост и значения>1 |
| First-pass survival | Вероятность не завершить первый проход к t | Монотонность следует из определения; нельзя получить её простым переименованием другой curve |
| Relative retention | Сравнение с платформенным reference cohort | Отсутствие reference metric не равно плохому результату |
| Public replay heatmap | Локальная популярность участков по правилам платформы | Не число оставшихся зрителей; источник/нормализация обязательны |
| Editorial score | Объяснимые редакционные критерии | Не измеренная вероятность удержания или вирусности |
| Predicted outcome | Выход модели с target/cutoff/model version | Не фактическое наблюдение и не причинный эффект |

Собственный контрпример: все смотрят половину → APV50%, completion0%. Половина смотрит целиком, половина сразу уходит → APV50%, completion50%. Следовательно AVD/duration не определяет completion.

## Подтверждённые проблемы определения метрик

- C01 [analysis.py](https://github.com/Hwangbot/Shortform-Signals/blob/d7e234d24720910e97d2ffa92d3c451cc9d0bb6a/analysis.py#L22-L39): retention=full_views/views. Это возможный completion proxy только при согласованных единицах, окнах и знаменателях. В 1000 CSV rows найдено 427 full_views>views и 88 likes>views ([пример](https://github.com/Hwangbot/Shortform-Signals/blob/d7e234d24720910e97d2ffa92d3c451cc9d0bb6a/shortform_videos.csv#L1-L6)). Нужны определения; эти числа не доказывают synthetic origin. [Validation](https://github.com/Hwangbot/Shortform-Signals/blob/d7e234d24720910e97d2ffa92d3c451cc9d0bb6a/data_loader.py#L54-L86) не обеспечивает этот контракт, [runner](https://github.com/Hwangbot/Shortform-Signals/blob/d7e234d24720910e97d2ffa92d3c451cc9d0bb6a/run_analysis.py#L30-L41) продолжает после validation failures.
- C13 [dictionary](https://github.com/tarekmasryo/youtube-tiktok-trends-dataset-2025/blob/7d6480864623229554e1128cc8ad51b3ad2b0b79/docs/DATA_DICTIONARY.md#L90-L110) именует completion_rate отношением estimated watch time/duration. Dataset явно synthetic; [validator](https://github.com/tarekmasryo/youtube-tiktok-trends-dataset-2025/blob/7d6480864623229554e1128cc8ad51b3ad2b0b79/scripts/validate_dataset.py#L1-L8) прямо не является statistical audit.
- C02 [retention parser](https://github.com/msertdev/keepwatching/blob/92e308cb44c9c687015c29f1d2752345c405f82b/measure/src/ingest.ts#L129-L141) выбирает percent/fraction по value>1: значение 1 в percent column и ratio1.2 интерпретируются неправильно. [Report](https://github.com/msertdev/keepwatching/blob/92e308cb44c9c687015c29f1d2752345c405f82b/measure/src/report.ts#L154-L160) делит lifetime views на min(ageHours,24), что не восстанавливает first24h. [Seed](https://github.com/msertdev/keepwatching/blob/92e308cb44c9c687015c29f1d2752345c405f82b/measure/src/seed.ts#L121-L153) суммирует календарные дни, не точные интервалы от времени публикации.
- C02 при неизвестной duration [сохраняет fraction в t](https://github.com/msertdev/keepwatching/blob/92e308cb44c9c687015c29f1d2752345c405f82b/measure/src/ingest.ts#L205-L208), хотя t объявлен seconds. Требуется explicit axis unit.
- Packaging alternative [metric functions](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/scripts/thumbnail_learning.py#L195-L217) смешивают APV с retention и Browse/Suggested CTR с blended fallback; comparison populations могут различаться. [Confidence](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/scripts/thumbnail_learning.py#L355-L360) основан лишь на n, не CI/power.

## YouTube Analytics: установленное и неподтверждённое

C12 [Query](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/youtube/analytics.go#L35-L61) использует channel==MINE. [Retention](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/retention.go#L82-L136) запрашивает elapsedVideoTimeRatio, audienceWatchRatio, relativeRetentionPerformance и video filter. YosukM [запрашивает те же owner-authorized данные](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/fetch_retention.py#L80-L105).

Публичные metadata чужого канала не предоставляют его приватную retention curve. Live OAuth/Analytics requests здесь не выполнялись; существование клиента или fake-server tests не гарантирует текущую допустимость всех combinations.

Прямые developers.google.com pages вернули network403. Доступна [официальная discovery schema](https://github.com/googleapis/google-api-go-client/blob/c16ef96b4f993e8393df8e4ce9b8510d660275c7/youtubeanalytics/v2/youtubeanalytics-api.json#L342-L418), revision20230704, включая startIndex. В ней metrics являются строками; она не подтверждает все ограничения 2026 по Shorts/engagedViews/native title-thumbnail experiments/arm exports. Утверждения сторонних README об этих ограничениях не принимаются как актуальная официальная спецификация.

Перед интеграцией нужны current-doc/live gates: scope, metric definition/version, compatibility dimensions/filters, latency/withholding, quotas, pagination, period/timezone и privacy. Manual Studio CSV остаётся отдельным входом с явной схемой.

### C12: missing relative → ложное слабое удержание

Цепочка независимо проверена двумя исследователями:

1. [service.go84–102](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/service.go#L84-L102) после HTTP400 удаляет optional metric и повторяет запрос.
2. [Table.Num](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/youtube/analytics.go#L75-L80) для отсутствующей колонки возвращает 0.
3. [Retention construction](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/retention.go#L124-L131) сохраняет Relative=0.
4. [WeakSpans](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/retention.go#L238-L239) объявляет Relative<.35 below typical.

SOURCE-CONFIRMED path, не live Google reproduction. Требуется nullable value + availability/error/source, без оценки качества по missing. [Exit-query error](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/retention.go#L109) также подавляется: network/API error не следует выдавать за недостаток просмотров.

C12 smoothing5points при lifetime views<1000 — [эвристика](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/retention.go#L142-L164), не доверительный интервал. Трёхдневная задержка окна — политика app, не гарантированный latency Google. Generic per-video export ограничен 200 и не предоставляет полноценную pagination всех каналов ([videos](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/videos.go#L117-L155)); Reporting pagination отдельно существует.

## Варианты, наблюдения и причинный эксперимент

Генерация двух картинок, два organic uploads, sequential смена hooks или offline neural scores не обеспечивают randomized viewer experiment.

C04 [score path](https://github.com/sxnnywu/reeled-in/blob/2905f67c9473a0c119d6dfdcee492bdca467dde8/backend/scoring/score.py#L40-L65) получает TRIBE activations; [signals](https://github.com/sxnnywu/reeled-in/blob/2905f67c9473a0c119d6dfdcee492bdca467dde8/backend/scoring/signals.py#L1-L31) прямо сообщает PRIOR, not fit to outcome data. Winner строится из 60% neural/40% production signals, без реальных randomized exposures/outcomes. Demo labels boring/engaging даны записавшим видео человеком. Current batch normalization уже исправлена; старую per-clip minmax проблему нельзя объявлять current defect.

C02 [пререгистрация](https://github.com/msertdev/keepwatching/blob/92e308cb44c9c687015c29f1d2752345c405f82b/experiments/2026-09-counter-vs-hook.md#L37-L99) полезна как дисциплина, но ABCABC+n5/arm для органических uploads не является viewer randomization. Автор признаёт confounds. [Статус](https://github.com/msertdev/keepwatching/blob/92e308cb44c9c687015c29f1d2752345c405f82b/experiments/2026-09-counter-vs-hook.md#L110-L112) Not started; README running не доказывает результатов.

### C05: ошибки статистического движка

[WatchDuration](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L384-L390) возвращает миллисекунды; [winner](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L344-L360) подаёт их в [two-proportion z-test](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L226-L252).

Собственный контрпример: nA=nB=100, means1500/1000ms → pooled1250 → z0 → None. Continuous watch time требует variance/raw independent observations и отдельного метода. Деление на duration не превращает исход в Bernoulli.

[min_sample_size](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L21-L33) объявлен, но [winner](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L320-L365) фильтрует лишь impressions>0. n2/arm, rates1/0 дают z2 при alpha.05, даже если min100. Асимптотический z-test на столь малых counts сам ненадёжен. Единственный candidate возвращается без сравнения.

[Assignment](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L42-L95) использует FNV(user_id), Random является документированным alias; experiment namespace отсутствует. Stable hashing допустим, но correlated assignments между опытами требуют явной политики.

### Более сильный отдельный reference

GrowthBook [assignment](https://github.com/growthbook/growthbook/blob/e66eb5c50449d96e3a4e41c0a62ffd6339469d5a/packages/sdk-js/src/core.ts#L689-L713) использует experiment seed и hash; [tracking](https://github.com/growthbook/growthbook/blob/e66eb5c50449d96e3a4e41c0a62ffd6339469d5a/packages/sdk-js/src/core.ts#L797-L841) имеет callback/sticky mechanics. [Stats](https://github.com/growthbook/growthbook/blob/e66eb5c50449d96e3a4e41c0a62ffd6339469d5a/packages/stats/gbstats/frequentist/tests.py#L39-L72) различает continuous variance-aware outcomes; [sequential methods](https://github.com/growthbook/growthbook/blob/e66eb5c50449d96e3a4e41c0a62ffd6339469d5a/packages/stats/gbstats/frequentist/tests.py#L244-L265) существуют отдельно.

Это reference для управляемого player/site/panel, не способ назначать органических YouTube зрителей. Тесты и вся статистика engine нами не запускались/не сертифицированы. Callbacks должны соответствовать реальным показам. SDK/stats MIT, Enterprise exceptions проверять отдельно.

## Предлагаемый ExperimentSpec

- Immutable experiment_id, question, eligibility, treatment asset hashes, randomization unit, seed/namespace, allocation, start/endUTC.
- Assigned, actually exposed и outcome observed — разные события. event_id dedup, consent, pseudonymous subject/session, errors/censoring.
- Primary metric/denominator, MDE, alpha/power, minimum duration, fixed stopping либо валидный sequential protocol до начала.
- Repeated viewers, creator clustering, interference, sample-ratio mismatch, multiple tests и missingness проверять явно.
- Title/thumbnail packaging и содержательный hook — разные treatments. Эффект первого не доказывает второе.
- Недостаточно данных / эксперимент невалиден — разрешённые результаты; победитель не обязателен.

Иллюстрация мощности: independent binary outcome, baseline50%, MDE+5 п.п., alpha.05 two-sided, power80% → около 1570 наблюдений/arm по normal approximation. Это не универсальный порог; кластеры, потери и multiple hypotheses увеличивают требования.

## Предлагаемые проверки

1. 1% vs ratio1.2; missing vs0; APV>100 отдельно от bounded completion.
2. Все actual timestamps и nonuniform grid сохраняются; неизвестная duration не подменяет units.
3. Flat/rising curve → no detected drops; показывается разрешение интервала.
4. First24h требует реального временного окна, не lifetime/day buckets.
5. A/A, salted stable assignment, SRM, exposure dedup, stopping discipline и независимые исходы.
6. На synthetic fixtures проверяется механика; эффективность контента доказывается реальными данными.
