# Матрица внешних технологий

Дата проверки: 2026-11-04. Метод и ограничения — [README](README.md). Полные проверенные SHA доступны в закреплённых URL; HEAD означает наблюдавшуюся версию, а не обещание стабильного релиза. Runtime внешних проектов и Windows здесь не проверялись.

## Исходные 13 кандидатов

| ID | Проект / версия | Заявлено и фактически найдено | Данные и права | Решение |
|---|---|---|---|---|
| C01 | [Hwangbot/Shortform-Signals, d7e234d](https://github.com/Hwangbot/Shortform-Signals/tree/d7e234d24720910e97d2ffa92d3c451cc9d0bb6a) | pandas/sklearn/Tableau, корреляции, KMeans. Retention вычисляется full_views/views; не временная кривая и не prepublication predictor | 1000 CSV rows; origin UNKNOWN. MIT заявлен README, LICENSE в tree отсутствует | REIMPLEMENT IDEA для описательной аналитики; не доказательство удержания |
| C02 | [msertdev/keepwatching, 92e308c, v0.1.0](https://github.com/msertdev/keepwatching/tree/92e308cb44c9c687015c29f1d2752345c405f82b) | JSON formats → Playwright frames → FFmpeg; версии вариантов, CSV/manual observations. 24 formats, 0 measured | MIT кода. Четыре content samples не доказывают эффективность библиотеки; raw per-video curve exports не поставлены | REIMPLEMENT IDEA / EXPERIMENT для provenance; ошибки единиц/окон исправлять независимо |
| C03 | yt-retention, owner не указан | Точная идентичность не установлена | **UNVERIFIED SOURCE** | Не включать в интеграционные рекомендации; альтернативы ниже отдельны |
| C04 | [sxnnywu/reeled-in, 2905f67](https://github.com/sxnnywu/reeled-in/tree/2905f67c9473a0c119d6dfdcee492bdca467dde8) | TRIBE neural-response proxy + эвристическое сравнение вариантов; не randomized viewer A/B | LICENSE app отсутствует в tree; [TRIBE CC BY-NC 4.0](https://github.com/facebookresearch/tribev2/blob/af58661791a351a448a489042a28f6c37e1c14b7/LICENSE). Demo label записавшего клипы человека, не measured retention | REJECT как готовый коммерческий retention predictor/A-B; научная гипотеза отдельно |
| C05 | [cool-japan/oximedia, 5263510](https://github.com/cool-japan/oximedia/tree/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics); crate0.2.1 | События, session retention, assignment, статистика. WatchDuration ошибочно проходит proportion z-test | Apache-2.0; собственных приватных YouTube событий не добывает | REIMPLEMENT IDEA; статистический движок не переносить без проверки |
| C06 | content-thumbnail-package, owner не указан | Точный skill/repo не установлен | **UNVERIFIED SOURCE** | Не отождествлять с ericosiu skill; альтернативы ниже |
| C07 | [dav22-wa/youtube_shorts_tiktok_trends_2025, 1483e25](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/tree/1483e256e25460b65c4bb6672c95ea36b17ec45e) | Streamlit URL demo + RandomForest notebook; model отсутствует, входной вектор 65zeros; completion=.7 placeholder | CSV provenance неизвестен. README заявляет MIT, отдельного LICENSE нет | REJECT текущую реализацию |
| C08 | [darderrdur17/ViralIQ, 7ed2e85, v1.0.0](https://github.com/darderrdur17/ViralIQ/tree/7ed2e853ed6407ed59aba739cb3085ff16e76dc0) | Реальный metadata ML pipeline, temporal split, labels, registry, dashboard; не измеритель кривой удержания | All rights reserved; local evaluation разрешена, коммерция/redistribution по разрешению. Derived data заявлены CC BY-NC4.0; первичный HF source не проверен | REIMPLEMENT IDEA для контроля утечек; коммерческий перенос BLOCKED |
| C09 | [Hashi-AI/Video-retention-analysis, 79ff7e6](https://github.com/Hashi-AI/Video-retention-analysis/tree/79ff7e6456bb9fb078caa043cb8552d595b018f6) | Пять кривых ×6 точек; R²99.46% против той же средней кривой | Нет URL/аудиторий/даты/происхождения B–F; LICENSE отсутствует | REJECT как доказательство предсказания нового ролика |
| C10 | [RolyPo1y/TIML, 2245280](https://github.com/RolyPo1y/TIML/tree/2245280c2a833209f2670cac52918b1dae658522) | Multimodal PyTorch popularity network с short/long observed popularity sequences; не retention curve | MIT кода; права Bilibili Drive data и extraction pipeline не подтверждены. Paper DOI/venue не установлен | EXPERIMENT после rights/repro gates; текущий trainer имеет блокер |
| C11 | TARPA | Точная статья, авторы, DOI и официальный код не установлены | **UNVERIFIED RESEARCH REFERENCE** | Не приписывать алгоритмы/результаты; научные альтернативы ниже |
| C12 | [gomcpgo/youtube_analytics, 57d1822, v0.1.0](https://github.com/gomcpgo/youtube_analytics/tree/57d1822a9adb934f1b78643a346a7b0138cf23aa) | Реальные Go OAuth Data/Analytics/Reporting клиенты; own-channel retention. Missing relative metric может стать нулём и ложной оценкой | MIT, Go1.24. Fake-server tests и synthetic curves; не live API proof | REIMPLEMENT ADAPTER / EXPERIMENT, не ADOPT |
| C13 | [tarekmasryo/youtube-tiktok-trends-dataset-2025, 7d64808, citationv1.0.2](https://github.com/tarekmasryo/youtube-tiktok-trends-dataset-2025/tree/7d6480864623229554e1128cc8ad51b3ad2b0b79) | Explicit synthetic tables; validators структуры/checksums, не эмпирической достоверности | CC BY4.0. README заявляет 48079×58 raw/50000×32 ML; полностью строки не пересчитывались | EXPERIMENT для schema/fixtures; REJECT как доказательство реальных ML-закономерностей |

C05: опубликованный crate был проверен по SHA256 из index.crates.io: `4bd8cee724af5fb97c751a891a5633ac610cac5372ed5470df26b7e802ae41a1`. Packaged VCS — `a4086367931853a8191f6f7227ebc1e392328947`; изученный ab_testing.rs побайтово совпал с HEAD5263510.

## Независимо проверенный оригинал

[konlu/story-studio, 87c2bbf](https://github.com/konlu/story-studio/tree/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1): локальный corpus search + агентная Narrative/Evidence методика и реальные media tools. Каталог 57 записей, у всех source_url/published_at отсутствуют; есть engagement counts, нет retention. Полный разбор — [UPSTREAM_AUDIT](UPSTREAM_AUDIT.md).

Лицензия объявлена CC BY-NC-SA4.0, но текст сокращён/изменён. Коммерческий перенос покрытых материалов BLOCKED до разрешения/независимой замены; не следует автоматически распространять этот вывод на каждый самостоятельный файл RU/UA.

## Проверенные альтернативы — не переименование C03/C06/C11

| Альтернатива | Закреплённая версия | Назначение / права | Решение и CPU-граница |
|---|---|---|---|
| C03-A | [YosukM/yt-retention-analyzer, c615683](https://github.com/YosukM/yt-retention-analyzer/tree/c6156834d270b9deaf019370388a6fa1bd81f4db) | OAuth curve JSON → локальное видео/ASR → текстовый контекст; LICENSE нет | REIMPLEMENT IDEA. CPU/int8 selectable, default CUDA; язык ja, Windows/RU-UA не проверены |
| C03-B | [darcydriscoll/retention-clipper, 64ec3f4](https://github.com/darcydriscoll/retention-clipper/tree/64ec3f429634e8fe96ecc385b130b36364aabbf5) | Ручной CSV → graph/timestamps; LICENSE нет; реального clipping/API нет | REJECT IMPLEMENTATION. CPU по конструкции, ошибки slope/grid/EOF |
| C06-A | [ericosiu/packaging-youtube-thumbnails, d2237ec, v1.0.0](https://github.com/ericosiu/ai-marketing-skills/tree/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails) | Агентная rubric, raster guards, performance ledger; MIT кода/текстов | REIMPLEMENT IDEA. HelpersCPU; image generation внешняя; не A/B engine |
| C06-B | [manuarora700/youtube-thumbnail-generator, c683960, v1.0.0](https://github.com/manuarora700/youtube-thumbnail-generator/tree/c683960b7f947132005adbeb7dd1b8d387d3cbd4) | React/Vite + Gemini image variants; MIT кода, service/asset rights отдельно | EXPERIMENT UI/provider contract; cloud inference, не offlineCPU |
| C06-C | [popekim/YouThumb, 0d06ffd](https://github.com/popekim/YouThumb/tree/0d06ffd410305ba1fef414245395bc622ba278cd) | WinForms/GDI+ local text/image composition; MIT | REIMPLEMENT IDEA. Legacy.NET4, README testedWin7; Win10/11 не проверены |
| C06-D | [dtcrout/yt-title-generator, 62e922b](https://github.com/dtcrout/yt-title-generator/tree/62e922b6fdf99f455e8c90c19ee1eba112d55efe) | VGG16+LSTM title captioning; MIT; внешний Kaggle dataset/weights | REJECT product path: TF1.13.1/Keras2.2.4, max_length defect, не CTR model |
| Experiment infrastructure | [GrowthBook, e66eb5c; JS SDK2.0.0](https://github.com/growthbook/growthbook/tree/e66eb5c50449d96e3a4e41c0a62ffd6339469d5a) | Seeded assignment + callbacks + variance-aware stats; SDK/statsMIT, Enterprise exceptions | EXPERIMENT для своего player/site/panel; не nativeYouTube |
| C11-A | [Beyond Views / avalanchesiqi/youtube-engagement, 5f4a4bb](https://github.com/avalanchesiqi/youtube-engagement/tree/5f4a4bb62a10cfc4608a5163c44d059a69e81304) | Wu/Rizoiu/Xie, ICWSM2018. Aggregate average watch percentage; MIT кода, dataset rights отдельно | SCIENTIFIC BASELINE / REIMPLEMENT IDEA. CPU Ridge; старый Python3.6 stack |
| C11-B | [D²Co / hyz20/D2Co, 818116c](https://github.com/hyz20/D2Co/tree/818116c052e27a3e25cfc0849f9297eb50e50542) | Zhao etal., RecSys2023, DOI10.1145/3604915.3608797; watch-time label debiasing | Код LICENSE отсутствует; data access не подтверждён; CUDA вызовы блокируют готовый CPU путь |
| Curve research artifact | [flowtele/vRetention, 0be5174](https://github.com/flowtele/vRetention/tree/0be51742b414422f1d304546573c42768ed400cb) | SVG curve dataset/notebooks; GPLv3 кода, paper/capture/denominator не установлены | METRIC/PAPER UNVERIFIED. Не считать проверенным ground truth |
| Curve research project | [cliangyu/dense-retention-rl, a342c72](https://github.com/cliangyu/dense-retention-rl/tree/a342c723880f637eaa146a047eed1dcf59522ae2), [ttcc-rl, ca727ba](https://github.com/cliangyu/ttcc-rl/tree/ca727ba65b8303a4aed78ad8edb84630dbbdbf66) | Курсовой CS224R2026, temporal hazard curve; densecodeApache2.0, data/weights rights отдельно | EXPERIMENT идей, REJECT V7artifacts. GPU24GB+, не WindowsCPU-ready |

## Лицензии и воспроизводимость

Кодовая MIT/Apache лицензия не разрешает автоматически чужие изображения, шрифты, голоса, модели, платформенные данные или API output. Отсутствие LICENSE означает отсутствие подтверждённого grant, не доказательство незаконности проекта.

Ни один внешний Windows runtime в исследовании не запускался. C01/C02/C05/C09/C12 и локальные compositing/measurement helpers по конструкции CPU-выполнимы, но runtime и performance UNTESTED. C04 имеет A100-oriented deployment; TIML имеет CPU branch без доказанной производительности; D²Co содержит unconditional CUDA; Dense требует тяжёлую GPU-модель.

Подробные дефекты и evidence: [метрики](METRICS_AND_EXPERIMENT_DESIGN.md), [ML](PREDICTION_VALIDATION.md), [альтернативы](ALTERNATIVES_REVIEW.md), [независимое ревью](RED_TEAM_REVIEW.md). Ни одно решение не разрешает интеграцию до утверждения архитектуры.
