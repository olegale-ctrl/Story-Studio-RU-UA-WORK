# Проверенные альтернативы неподтверждённым названиям

Дата: 2026-11-04. Пользователь отдельно разрешил исследование этих альтернатив; они не устанавливают тождество с исходными C03/C06/C11. Runtime/Windows и модели не запускались.

## Retention: YosukM

[yt-retention-analyzer, c615683](https://github.com/YosukM/yt-retention-analyzer/tree/c6156834d270b9deaf019370388a6fa1bd81f4db) — настоящий local pipeline: owner-authorized Analytics/Data APIs → JSON curve → местный видеофайл → FFmpeg16kHzmono → faster-whisper → Markdown/PNG с текстом возле изменений.

- [API](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/fetch_retention.py#L80-L105): channel==MINE, video filter, elapsedVideoTimeRatio, audienceWatchRatio, relativeRetentionPerformance.
- [Сохранение](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/fetch_retention.py#L158-L168) включает период, headers, rows, duration. Offline analysis читает этот JSON, не произвольный StudioCSV; CSV fallback в изученном tree не найден.
- [Temporal join](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/analyze.py#L65-L73) берёт сегменты, пересекающиеся с ±10s. [Позиция](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/analyze.py#L121-L123) умножается на YouTube duration.
- Channel pipeline имеет pagination uploads и metadata batches50; это реализованный код, не одна README-заявка.
- LLM/semantic diagnosis/prediction не найдено: анализ арифметический.

### Дефекты и границы

| Evidence | Вывод |
|---|---|
| [transcribe158–186](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/transcribe.py#L158-L186) | Жёсткий languageja, без languageCLI; готового RU/UA нет |
| [analyze125–143](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/analyze.py#L125-L143) | Top5 без positive-drop filter; растущая кривая тоже получает «отвалы» |
| [is_short48–67](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/fetch_channel.py#L48-L67) | Формат определяется duration/hashtags и awr>1. Для одинаковых 120s outcome.8/1.1 меняет группу; comparison bias |
| [analyze106–119](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/analyze.py#L106-L119) | Только duration mismatch warning>2s; identity/version опубликованного asset не подтверждается |
| [auth95–99](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/auth.py#L95-L99) | Token JSON plaintext, обычный open без explicit ACL/permissions/atomic replace |
| [requirements](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/requirements.txt) | Зависимости без pinned versions; LICENSE в tree отсутствует |
| [transcribe135–151](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/transcribe.py#L135-L151) | WhisperModel без model revision/local_files_only/checksum может скачать веса при первом запуске |
| [CLI defaults](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/transcribe.py#L195-L210) | Default large-v3/CUDA/float16; CPU/int8 selectable, не проверен |

Дельта относится к интервалу соседних samples, не к гарантированно точной секунде. Для длинного видео при редкой сетке окно±10s может пропустить часть соответствующего контента. Rewatch/seek и состав аудитории мешают причинной трактовке.

Потенциальный path risk: video_id не ограничен ожидаемым форматом перед использованием в local paths, FFmpeg работает с -y; эксплуатация не воспроизводилась. subprocess передаёт argument list, shell interpolation не найдено.

MIT upstream faster-whisper/Whisper не лицензирует код YosukM и не подтверждает provenance любого converted checkpoint. Коммерческое копирование BLOCKED до разрешения.

Рекомендация: самостоятельно связывать реальные кривые с собственным scene/script manifest Sprint26. Для уже созданных нами видео ASR не является необходимым первым шагом; для legacy-файлов он отдельный optional provider.

## Retention: darcydriscoll

[retention-clipper, 64ec3f4](https://github.com/darcydriscoll/retention-clipper/tree/64ec3f429634e8fe96ecc385b130b36364aabbf5) содержит один 5240byte script, README и demo images; LICENSE, tests, requirements и исходный CSV не обнаружены. [Script17–29](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L17-L29) требует ручного редактирования title/length и English CSV columns. OAuth/API/network calls, actual video cutting, audio/ASR/LLM отсутствуют.

Выход — graph.png и timestamps.txt. Top-level исполнение при import имеет side effects и overwrite. Это не reusable production module.

| Source-level находка | Evidence / собственная проверка |
|---|---|
| Regression slope по seconds сравнивается с gradient по процентной позиции | [48–82](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L48-L82); единицы несогласованы |
| Flat curve может стать red/worse | [79–87](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L79-L87): grad0 исключён из stable, b1=0 не делает better |
| Хороший хвост до EOF не сохраняется | [118–134](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L118-L134): нет final flush |
| Требуются 100samples и искусственная равномерная сетка | [28–42](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L28-L42), [90–98](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L90-L98) |
| Timestamp>=1h вызывает ValueError | dt.time(0,minute,second); собственный datetime.time(0,60,0) подтвердил ошибку |

Скрипт по конструкции CPU, но современная совместимость зависимостей/Windows не проверена. Рекомендация: REJECT IMPLEMENTATION, независимо реализовать CSV intake с реальными positions, единицами, missing statuses и interval annotations.

## Packaging: ericosiu skill

[packaging-youtube-thumbnails, d2237ec, v1.0.0](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/SKILL.md#L1-L15), MIT. Это другой пакет, не подтверждённый C06.

Реализованы:

1. Агентные инструкции для разных promise hypotheses/title-thumbnail вариантов.
2. [Rubric](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/references/packaging-rubric.md#L72-L91): fidelity20%, identity20%, specificity20%, complementarity15%, legibility15%, evidence10%, ручные thresholds. Это редакционный балл, не calibratedCTR.
3. [thumbnail_guard](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/scripts/thumbnail_guard.py#L100-L164): dimensions, вручную заданные boxes; edit-path pixel diff вне allowed region. Он не распознаёт факты/лица/логотипы/читаемость сам.
4. [Learning](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/scripts/thumbnail_learning.py#L270-L368): comparison-group medians и ручные ratio thresholds → triage labels; randomized allocation/exposure/pvalue отсутствуют.
5. Внешняя raster generation требует host imagegen; standalone model/API generator нет.

Документ [прямо говорит triage, not causality](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/references/performance-learning.md#L85-L106). Аналитические ограничения: APV называется retention; >100% отвергается; traffic scopes могут смешиваться; confidence зависит только от n; variant history теряется при upsert; historical as-of не ограничивает future snapshots. См. [метрики](METRICS_AND_EXPERIMENT_DESIGN.md).

Для Windows: locking предусматривает msvcrt, но [UTF8 write](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/scripts/thumbnail_learning.py#L55-L63) и [read_text без encoding](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/scripts/thumbnail_learning.py#L38-L46) создают conditional RU/UA risk при legacy locale. Pillow>=12.3,<13, exact lock нет. По AST44 test methods, исполнено 0 в этом исследовании.

Root workflow содержит version-check/telemetry preamble; оно не запускалось. MIT относится к предоставляемому коду/текстам; входные assets/fonts/brands и права output генератора отдельны.

Решение: REIMPLEMENT IDEA для review matrix, original promise variants и geometric/pixel guards; performance triage только после исправления contracts.

## Другие packaging-инструменты

### Gemini generator

[manuarora700/youtube-thumbnail-generator, c683960](https://github.com/manuarora700/youtube-thumbnail-generator/tree/c683960b7f947132005adbeb7dd1b8d387d3cbd4), MIT кода: React/Vite принимает prompt/reference/template и count, [вызывает gemini-2.5-flash-image](https://github.com/manuarora700/youtube-thumbnail-generator/blob/c683960b7f947132005adbeb7dd1b8d387d3cbd4/src/lib/gemini.ts#L155-L171) и возвращает несколько картинок. [A/B/Analytics](https://github.com/manuarora700/youtube-thumbnail-generator/blob/c683960b7f947132005adbeb7dd1b8d387d3cbd4/README.md#L219-L226) ещё roadmap.

Это генерация, не CTR/retention evaluation. Cloud inference не требует localNVIDIA, но не является offlineCPU. Model/API prices/ToS/regions/output rights не подтверждены; paid requests не было. Template images имеют отдельный неустановленный provenance.

[API key](https://github.com/manuarora700/youtube-thumbnail-generator/blob/c683960b7f947132005adbeb7dd1b8d387d3cbd4/src/lib/gemini.ts#L205-L228) хранится в localStorage; validateApiKey сама делает model request, поэтому не запускалась. Полезен provider contract с partial successes, version/model/cost metadata и artifact hashes, не adoption browser-secret storage.

### YouThumb

[popekim/YouThumb, 0d06ffd](https://github.com/popekim/YouThumb/tree/0d06ffd410305ba1fef414245395bc622ba278cd), MIT: [GDI+ composition](https://github.com/popekim/YouThumb/blob/0d06ffd410305ba1fef414245395bc622ba278cd/Main.cs#L116-L174) рисует исходную картинку, overlay и существующий title. Генерации смысла заголовка, trained scorer и A/B нет.

README говорит.NET2/тест Win7, projecttarget.NET4/AnyCPU. [Web parsing](https://github.com/popekim/YouThumb/blob/0d06ffd410305ba1fef414245395bc622ba278cd/Main.cs#L264-L281) по fixed<title>delimiters хрупок; на нынешнем YouTube не запускался. Полезна независимая CPU-компоновка оригинальных RU/UA шаблонов; устаревший C#GUI добавлять в Sprint26 нецелесообразно.

### Title generator

[dtcrout/yt-title-generator, 62e922b](https://github.com/dtcrout/yt-title-generator/tree/62e922b6fdf99f455e8c90c19ee1eba112d55efe), MIT: VGG16+LSTM image-captioning на внешнем KaggleUSVideos, старый TF1.13.1/Keras2.2.4. Не CTR predictor. [max_length](https://github.com/dtcrout/yt-title-generator/blob/62e922b6fdf99f455e8c90c19ee1eba112d55efe/app/src/train.py#L72-L77) берёт максимальное число букв слова, не token-sequence length. [Test](https://github.com/dtcrout/yt-title-generator/blob/62e922b6fdf99f455e8c90c19ee1eba112d55efe/app/src/train.py#L115-L156) используется как checkpoint validation; независимый итоговый holdout не показан. REJECT текущий product path; данные/веса не скачивались.

### GrowthBook

[e66eb5c](https://github.com/growthbook/growthbook/tree/e66eb5c50449d96e3a4e41c0a62ffd6339469d5a): JS SDK2.0.0 и statsMIT, Enterprise exceptions отдельны. Реальные salted assignment, tracking, continuous/sequential stats исследованы в [метриках](METRICS_AND_EXPERIMENT_DESIGN.md).

Это отдельная инфраструктура controlled site/player/panel; SDK callback не доказывает actual visibility. Не управляет organicYouTube hooks и не заменяет native platform experiments. JS/Python paths не требуют NVIDIA, но Windows/full self-hosted deployment не проверен. Вводить всю платформу в Sprint26 прямо сейчас не предлагается.

## Научные альтернативы C11

Подтверждены Beyond Views (ICWSM2018, aggregate watch percentage, MIT code) и D²Co (RecSys2023, debiased watch-time scalar, LICENSE не найден). vRetention source существует, но curve origin/paper не установлены. Dense/TTCC — курсовой curve project с исторической label leak и GPU requirement.

Публикации, методы, splits, права и независимые поправки подробно в [PREDICTION_VALIDATION](PREDICTION_VALIDATION.md). Ни одна работа не подтверждает готовое предсказание удержания современных RU/UA видео.
