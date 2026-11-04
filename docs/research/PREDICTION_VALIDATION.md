# Прогнозирование: данные, утечки и воспроизводимость

Дата: 2026-11-04. Полный training/inference внешних проектов не выполнялся. Сохранённые авторские metrics не являются нашими повторными измерениями.

## C09: точный смысл R²=99,46%

[ML Analysis.ipynb](https://github.com/Hashi-AI/Video-retention-analysis/blob/79ff7e6456bb9fb078caa043cb8552d595b018f6/ML%20Analysis.ipynb#L59-L97) содержит 30 чисел: пять анонимных видео B–F ×6 позиций. Их среднее образует одну кривую. OLS обучается на её точках 1–5; prediction0 копирует Average0, prediction1 алгебраически воспроизводит Average1; оставшиеся точки вычисляет модель, обученная на них же. [R²](https://github.com/Hashi-AI/Video-retention-analysis/blob/79ff7e6456bb9fb078caa043cb8552d595b018f6/ML%20Analysis.ipynb#L121-L131) снова сравнивается с той же Average.

Два независимых расчёта собственной stdlib OLS:

| Величина | Результат |
|---|---|
| Average | [104.426, 88.478, 84.822, 82.728, 81.804, 80.816] |
| intercept / slope | 89.2322 / -1.8342 |
| predictions | [104.426, 88.478, 85.5638, 83.7296, 81.8954, 80.0612] |
| SSE / SST | 2.1315468 / 393.891654 |
| R² | 0.9945884946320797 =99.4588494632% |

Число подтверждено как **in-sample fit**, с подстановкой двух целевых точек. У отдельного VideoA нет исходных измерений и содержательных признаков. Это не 99.46% accuracy нового видео и не способность выбрать хороший сюжет. Обычная OLS на точках 1–5 имеет trainingR²≈.91072; копирование начальных точек и initial drop усиливают общий показатель.

Dataset provenance, аудитории, URL и даты не установлены. Значения>100% сами по себе допустимы при replay и не доказывают synthetic origin. В tree README+два notebooks, LICENSE нет.

## C07: дефект признаков и ограничения notebook

[App metadata](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/blob/1483e256e25460b65c4bb6672c95ea36b17ec45e/virality-predictor/app.py#L17-L42) содержит views, likes, comments, shares, saves, completion_rate, category, engagement_rate. Completion=.7 — placeholder обеих платформ.

[Input construction](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/blob/1483e256e25460b65c4bb6672c95ea36b17ec45e/virality-predictor/app.py#L62-L66) вызывает metadata.get(col,0) для [training_columns.pkl](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/blob/1483e256e25460b65c4bb6672c95ea36b17ec45e/virality-predictor/training_columns.pkl). Безопасный pickletools opcode parse, без load/joblib/deserialization, показал 65 имён (title_len, text_richness, like_rate, platform_youtube, language_ru и другие), пересечение с восемью metadata keys пусто. Отдельный критик подтвердил AST/opcode проверкой: при достижении predict любой успешно разобранный URL даёт одинаковые 65zeros.

[Строка 8](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/blob/1483e256e25460b65c4bb6672c95ea36b17ec45e/virality-predictor/app.py#L7-L9) требует virality_model.pkl, отсутствующий в tree. Это более ранний blocker обычного запуска.

[Notebook](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/blob/1483e256e25460b65c4bb6672c95ea36b17ec45e/virality-predictor/youtube_shorts_tiktok_trends_2025.ipynb), cells2–11/14 (minified одной строкой): manual CSV upload, сохранённая shape50000×32, get_dummies до random stratified80/20 split, X=все поля кроме trend_label, RandomForest200trees/max_depth15, saved accuracy.813. Это авторский output, не повторный прогон. Time/creator holdout и hash/provenance CSV не показаны.

Имена/shape похожи на C13, но байтовое происхождение не доказано. Нельзя писать «точно обучен на C13». Views/likes/rates/traffic_source текущего ролика не являются prepublication features.

## C08 ViralIQ: сильные guards и реальные недостатки

Подтверждённые сильные стороны: [temporal split](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/models/train.py#L95-L132), [train-only thresholds и missing24h/7d labels](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/labeling/labels.py#L97-L191), [feature allowlists](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/feature_engineering/features.py#L33-L74), [PR-AUC/ranking и clustered bootstrap](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/evaluation/metrics.py#L117-L189). Это не случайный split и не полностью фиктивный pipeline.

Подтверждённые ограничения:

1. [select_champion](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/models/train.py#L609-L656) выбирает модель по test PR-AUC и testPrecision@K. Этот test участвует в selection и не является нетронутым итоговым набором победителя.
2. [fit_sound_stats](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/feature_engineering/features.py#L151-L165) агрегирует median views по всему train и [присоединяет stats к тем же train rows](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/models/train.py#L377-L405). Для singleton sound собственные views видео входят в его признак; OOF/as-of construction не показана. Это self-target encoding/риск временной недоступности, а не доказанный перенос test-labels в train.
3. [not_recommended_for_fyp](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/feature_engineering/features.py#L112-L126) включён в prepublication features; момент появления snapshot-флага не доказан. Пока это риск postpublication feature, не универсально доказанная утечка.

[Data sources](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/docs/data_sources.md#L1-L37) ссылаются на datasocial/tiktok-5.6B-videos. Первичная HF карточка не проверена. [Benchmark](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/reports/evaluation/model_benchmark.md#L8-L40) содержит PR-AUC.0318, ROC-AUC.7419, test prevalence1.399%; это сохранённые результаты авторов. Независимый recent set в описанном запуске не заполнен. Это metadata popularity, не measured retention.

[LICENSE](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/LICENSE#L1-L27): all rights reserved, commercial/redistribution по письменному разрешению; derived datasets обозначены CC BY-NC4.0. Joblib model loading — trust boundary, не найденный malicious artifact. Коммерческий перенос BLOCKED.

## C10 TIML

MIT [model](https://github.com/RolyPo1y/TIML/blob/2245280c2a833209f2670cac52918b1dae658522/model.py#L165-L210): visual4096/acoustic2688/text1538 embeddings, metadata/social, short72×4 и long6×3 popularity sequences, LSTM/attention/fusion. [Dataloader](https://github.com/RolyPo1y/TIML/blob/2245280c2a833209f2670cac52918b1dae658522/dataloader.py#L61-L92) использует наблюдавшиеся временные признаки популярности. Это не готовый prepublication retention predictor.

[train.py235–243](https://github.com/RolyPo1y/TIML/blob/2245280c2a833209f2670cac52918b1dae658522/train.py#L235-L243): fold_seeds={} затем fold_seeds[1] без заполнения. При достижении строки гарантирован KeyError1; прежние imports/data/path failures могут произойти раньше. [Random80/10/10](https://github.com/RolyPo1y/TIML/blob/2245280c2a833209f2670cac52918b1dae658522/train.py#L245-L252) не обеспечивает creator/time isolation. Внешние npy загружаются [allow_pickle=True](https://github.com/RolyPo1y/TIML/blob/2245280c2a833209f2670cac52918b1dae658522/dataloader.py#L15-L17).

README требует external Bilibili Drive dataset и сообщает GPU/CUDA; CPU branch существует, но performance/Windows не проверены. Data rights, raw extraction provenance и paper DOI/venue не подтверждены. Реальный multimodal code не равен воспроизведённой научной точности.

## Подтверждённые научные альтернативы

### Beyond Views — Wu, Rizoiu, Xie, ICWSM2018

[Авторский publication index](https://github.com/avalanchesiqi/avalanchesiqi.github.io/blob/925819adf569372fbd08e2cbdbd401a4011524fe/pub.html#L165-L174), [прочитанная авторская статья](https://github.com/avalanchesiqi/avalanchesiqi.github.io/blob/925819adf569372fbd08e2cbdbd401a4011524fe/files/icwsm2018_youtube_engagement.pdf), [код 5f4a4bb](https://github.com/avalanchesiqi/youtube-engagement/tree/5f4a4bb62a10cfc4608a5163c44d059a69e81304). Это ICWSM, не WWW. DOI10.7910/DVN/L3UWZT относится к **датасету**, не к статье.

Описание сбора:5,331,204 YouTube videos/1,257,412channels2016, daily views/watch minutes; [selection](https://github.com/avalanchesiqi/youtube-engagement/blob/5f4a4bb62a10cfc4608a5163c44d059a69e81304/README.md#L76-L81) требует упоминания в Twitter, доступных Insight stats и 100views за 30 дней. Raw данные не скачивались/не пересчитывались.

[Target](https://github.com/avalanchesiqi/youtube-engagement/blob/5f4a4bb62a10cfc4608a5163c44d059a69e81304/wrangling/construct_formatted_dataset.py#L70-L84): wp30=watch minutes30d×60/views30d/duration. Relative engagement — duration-calibrated rank. Ось temporal analysis — дни после публикации, не секунды внутри видео. [Ridge](https://github.com/avalanchesiqi/youtube-engagement/blob/5f4a4bb62a10cfc4608a5163c44d059a69e81304/utils/ridge_regressor.py#L25-L68) использует контекст, темы и репутацию канала. Авторский R²≈.77 не перепроверен и не сопоставим напрямую с C09.

[Split](https://github.com/avalanchesiqi/youtube-engagement/blob/5f4a4bb62a10cfc4608a5163c44d059a69e81304/wrangling/split_dataset_and_append_relative_engagement.py#L34-L47): trainJul1–Aug20, testAug21–31. Paper сообщает 66% test channels seen in train. [Channel reputation](https://github.com/avalanchesiqi/youtube-engagement/blob/5f4a4bb62a10cfc4608a5163c44d059a69e81304/engagement_prediction/extract_channel_reputation.py#L48-L62) использует train30day outcomes: для train-публикаций 20Aug labels созревают после test-публикаций 21–31Aug. Для строгого prospective backtest нужен maturity embargo/as-of join. Это не опровержение всей работы, а ограничение протокола для нашего deployment.

[MIT code](https://github.com/avalanchesiqi/youtube-engagement/blob/5f4a4bb62a10cfc4608a5163c44d059a69e81304/LICENSE), старый Python3.6/NumPy1.13/SciPy.19 CPU stack и Bash wrappers. Data rights Dataverse независимо не прочитаны из-за 403;4.6GBcompressed/26GBraw не скачивались. Наличие ru/uk в vocabulary не является современной RU/UA валидацией.

Решение: научный baseline duration-normalized outcomes, не готовый story-quality/fullcurve predictor.

### D²Co — Zhao etal., RecSys2023

Работа: Uncovering User Interest from Biased and Noised Watch Time in Video Recommendation, DOI10.1145/3604915.3608797. Авторы/venue подтверждены [primary supplement](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/D2Co_supp_materials.pdf); publisher fulltext403, numerical superiority не воспроизведено.

[Gaussian mixture](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/src/preprocessing/cal_gmm_label.py#L9-L45) по duration превращает watch time в clipped interest label; далее recommendation models. Это scalar label/objective, не внутривидеокривая и не narrative scoring.

Есть chronological split, но [label transformation](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/src/prepare_data.py#L46-L81) fit на полной processed таблице до [split](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/src/train_model.py#L49-L64). Нужен train-only fit; размер оптимизма неизвестен. [Ground truth](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/src/preprocessing/cal_ground_truth.py#L8-L27) — operational long_view2 с 18s/completion threshold, не прямое наблюдение внутреннего интереса.

[Dataset wrapper](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/src/utils/data_wrapper.py#L7-L13) default CUDA, [evaluation](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/src/train_model.py#L189-L197) unconditional.cuda: готовый WindowsCPU путь отсутствует. LICENSE кода не найден. [README](https://github.com/hyz20/D2Co/blob/818116c052e27a3e25cfc0849f9297eb50e50542/README.md#L1-L9) требует обращаться за KuaiRand к держателю. Права/доступность benchmarks не подтверждены. Метод duration bias полезен, прямое внедрение BLOCKED.

## Кривые: research artifacts с ограничениями

### vRetention

[README](https://github.com/flowtele/vRetention/blob/0be51742b414422f1d304546573c42768ed400cb/README.md#L9-L27) определяет retentionCurve как SVG path. [Conversion](https://github.com/flowtele/vRetention/blob/0be51742b414422f1d304546573c42768ed400cb/analysis/mmsys24-vRetention.ipynb#L619-L629): y=100−SVGy, x=SVGx/maxSVGx×duration, interpolation. Это нормализация x; нормализация y по максимуму в этой функции **не найдена**.

Capture pipeline, OAuth, denominator и точная paper identity отсутствуют. Нельзя утверждать ни privateAnalytics, ни publicMostReplayed. Notebook name mmsys24 и слова thispaper не заменяют библиографию. GPLv3 кода не устанавливает права/метрологию данных. Descriptive analysis не является predictor. Статус: source confirmed, metric/paper UNVERIFIED; не ground truth для интеграции.

### Dense Retention / TTCC

[Liangyu Chen, CS224R Spring2026, Per-Second Retention Curve Prediction with SFT+GRPO](https://github.com/cliangyu/ttcc-rl/blob/ca727ba65b8303a4aed78ad8edb84630dbbdbf66/docs/10_milestone_report.md#L1-L10) — авторский курсовой отчёт, peer-reviewed venue/DOI не установлены.

[Hazard head](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/register.py#L259-L275): softplus hazards → exp(−cumsum) → monotone0..1 curve. [Data normalizer](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/tools/build_v8_from_hf.py#L66-L78) peak-normalizes, forcesR0=1, clamps и убирает подъёмы. Выход — преобразованный target, не rawYouTube curve.

[Incident disclosure](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/INFERENCE.md#L3-L15) отзывает V7 checkpoints: target попадал во вход; авторские video-swap/randomization audits не выявили полезного использования видео. Это авторская проверка, не наш model runtime. Старое IBS.000092 ниже в guide не принимается как качество.

Текущий [eval default](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/eval_ibs.py#L202-L241) уже очищает assistant content; старую утечку нельзя приписывать исправленному default. Без train-jsonl [baseline](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/eval_ibs.py#L243-L251) строится по val; для честного сравнения заморозить по train. [per_ad_ibs](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/eval_ibs.py#L72-L76) — curveMSE, не автоматически индивидуальный censoring-aware survival Brier score.

Отдельный более ранний [TTCC experiment](https://github.com/cliangyu/ttcc-rl/blob/ca727ba65b8303a4aed78ad8edb84630dbbdbf66/README.md#L119-L130) на 87test сообщает IBS.0083 для meanbaseline и GRPO без ясного общего выигрыша. Нельзя смешивать его split717/87 с поздними hazard-checkpoints.

Dense codebaseApache2.0; права TTCC data/weights и исходные denominators не проверены; ttcc-rl отдельный LICENSE не найден. Guide требует GPU24GB+. V7 REJECT, чистый V8/WindowsCPU/RU-UA UNVERIFIED. Полезны методы фальсификации и baseline, не скачивание checkpoints.

## Протокол будущей модели Story Studio

1. Определить target: fixed-age popularity, APV, completion или конкретная curve; не объединять несовместимые величины.
2. Feature snapshot имеет value, source, available_at, cutoff_at, definition_version. История автора допустима только если тогда была доступна; текущие outcomes предсказываемого видео исключаются.
3. Labels получают outcome horizon и maturity timestamp. Train не видит labels, не созревшие к simulated prediction time.
4. Split по времени и creators/groups; близкие сценарии/варианты одного материала не расходятся между train/test.
5. Train → selection-validation → calibration → untouched outer test. Все thresholds/transforms/encoders fit только train. History/sound stats — as-of/OOF.
6. Baselines: training mean, duration/genre/history-only; для rare class PR-AUC и precision/lift@k с prevalence, для curve — явно определённый error. Calibration и uncertainty отдельно.
7. Content-swap, shuffled-labels, metadata-only, no-video ablations; все failures counted, generated outputs без target во входе.
8. RU/UA, platform, genre и creator generalization проверяются отдельно. Synthetic fixtures проверяют кодовую механику, не аудиторию.

До реальных разрешённых данных, прав и независимого holdout использовать объяснимый редакционный score; вероятность вирусности не обещать.
