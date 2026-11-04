# Независимая критическая проверка

Дата: 2026-11-04. Пять исследовательских агентов проверяли данные/Analytics, A/B, ML, права/Windows и оригинал. Отдельный агент F независимо читал ключевые исходники и пересчитывал формулы. Во второй волне проверены семантика кривых и дополнительные альтернативы. Внешний код, модели и тесты не запускались.

CONFIRMED ниже означает доказательство указанного масштаба, а не runtime-сертификацию.

## Основные выводы

| Тезис | Вердикт и основание |
|---|---|
| C09: R²=99,46% воспроизводится | CONFIRMED собственным расчётом: 0.9945884946320797 |
| C09: это точность нового Video A | Не подтверждается: [fit и копирование целей](https://github.com/Hashi-AI/Video-retention-analysis/blob/79ff7e6456bb9fb078caa043cb8552d595b018f6/ML%20Analysis.ipynb#L59-L97), затем [оценка на той же Average](https://github.com/Hashi-AI/Video-retention-analysis/blob/79ff7e6456bb9fb078caa043cb8552d595b018f6/ML%20Analysis.ipynb#L121-L131). Фактической кривой A нет |
| C05: WatchDuration проходит неверный тест | CONFIRMED: [score в миллисекундах](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L384-L390) передаётся в [proportion z-test](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L226-L252) |
| C05: победитель никогда не выбирается | Формулировка слишком широкая: [единственный кандидат](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L320-L333) возвращается без сравнения |
| Любой stable hash делает A/B недействительным | Неверно. Допустима стабильная разбивка; здесь проблема в [игнорируемом режиме и отсутствии experiment namespace](https://github.com/cool-japan/oximedia/blob/5263510374761ec8ef02dace5d26d62fb20e405b/crates/oximedia-analytics/src/ab_testing.rs#L65-L95) |
| C12: missing relative становится below typical | CONFIRMED source path: [fallback](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/service.go#L84-L102) → [missing=0](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/youtube/analytics.go#L75-L80) → [WeakSpan](https://github.com/gomcpgo/youtube_analytics/blob/57d1822a9adb934f1b78643a346a7b0138cf23aa/pkg/analytics/retention.go#L238-L239) |
| C07: любой разобранный URL даёт 65 нулей | CONFIRMED независимым AST/opcode анализом: [input](https://github.com/dav22-wa/youtube_shorts_tiktok_trends_2025/blob/1483e256e25460b65c4bb6672c95ea36b17ec45e/virality-predictor/app.py#L62-L66). Пересечение 8 metadata keys и 65 training names пустое; отсутствующая модель может остановить запуск раньше |
| TIML: первая итерация даёт KeyError:1 | CONFIRMED при достижении [fold_seeds](https://github.com/RolyPo1y/TIML/blob/2245280c2a833209f2670cac52918b1dae658522/train.py#L235-L243). Прежние imports/data могут упасть раньше |
| C08: test выбирает модель | CONFIRMED: [select_champion](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/models/train.py#L637-L656). Временной split в проекте действительно есть |
| C08: доказан перенос test-labels в train | NOT ESTABLISHED. [Sound stats](https://github.com/darderrdur17/ViralIQ/blob/7ed2e853ed6407ed59aba739cb3085ff16e76dc0/src/feature_engineering/features.py#L151-L162) ограничены train; подтверждено включение собственного outcome в обучающий признак |
| Upstream rank — прогноз удержания | Не соответствует [локальному поиску по релевантности и разнообразию](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/scripts/history_tool.py#L24-L87) |
| vRetention точно private retention либо точно Most Replayed | Оба варианта UNVERIFIED: [SVG description](https://github.com/flowtele/vRetention/blob/0be51742b414422f1d304546573c42768ed400cb/README.md#L12-L20) и [converter](https://github.com/flowtele/vRetention/blob/0be51742b414422f1d304546573c42768ed400cb/analysis/mmsys24-vRetention.ipynb#L619-L629) не раскрывают capture и denominator |
| Dense V7 пригоден на основании малого IBS | REJECT историческое качество: [авторское расследование](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/INFERENCE.md#L3-L15) отзывает checkpoints |
| Нынешний Dense eval сохраняет старую утечку по default | Неверно: [strip_assistant=True и очистка](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/eval_ibs.py#L202-L241) уже реализованы |
| Dense сохраняет raw curve | Неверно: [нормирование и монотонизация](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/tools/build_v8_from_hf.py#L66-L78) меняют target |
| YosukM готов для RU/UA | Не соответствует [hardcoded ja](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/transcribe.py#L158-L186). CPU flags при этом существуют |
| Packaging variants означают controlled A/B | Неверно: [triage, not causality](https://github.com/ericosiu/ai-marketing-skills/blob/d2237ec431608c9ab0551d03a69479b000603f11/packaging-youtube-thumbnails/references/performance-learning.md#L85-L106); собственного assignment/exposure engine нет |

## Арифметическая репродукция C09

Это собственный расчёт стандартной библиотекой; внешний notebook и sklearn не нужны.

```python
from statistics import mean

actual = [104.426, 88.478, 84.822, 82.728, 81.804, 80.816]
x = list(range(1, 6))
y = actual[1:]
slope = sum((a - mean(x)) * (b - mean(y)) for a, b in zip(x, y))
slope /= sum((a - mean(x)) ** 2 for a in x)
intercept = mean(y) - slope * mean(x)
predicted = actual[:2] + [intercept + slope * i for i in range(2, 6)]
sse = sum((a - p) ** 2 for a, p in zip(actual, predicted))
sst = sum((a - mean(actual)) ** 2 for a in actual)
print(1 - sse / sst)  # approximately 0.9945884946320797
```

Это training fit. Истинные первые две точки копируются, а не предсказываются.

## Контрпримеры второй волны

- YosukM: одинаковые 120 секунд без hashtags при awr=.8/1.1 попадают в разные группы из-за [is_short](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/fetch_channel.py#L48-L67). Это обусловленная outcome классификация, а не утечка ML training.
- YosukM: [нет positive-drop filter](https://github.com/YosukM/yt-retention-analyzer/blob/c6156834d270b9deaf019370388a6fa1bd81f4db/src/analyze.py#L125-L143), поэтому плоская и растущая кривые тоже дают «падения».
- Darcy: [regression по секундам](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L48-L55) и [gradient по процентной позиции](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L69-L82) несопоставимы без приведения единиц. Flat gradient исключён из stable; хороший хвост до EOF не сохраняется.
- Darcy использует [локальный CSV](https://github.com/darcydriscoll/retention-clipper/blob/64ec3f429634e8fe96ecc385b130b36364aabbf5/retention_clipper.py#L17-L29); API quota и настоящий clipping не реализованы.
- vRetention нормирует x; нормирование y по максимуму видео в converter не найдено. Нельзя приписывать ему преобразование Dense.
- Dense: [средняя baseline по val](https://github.com/cliangyu/dense-retention-rl/blob/a342c723880f637eaa146a047eed1dcf59522ae2/examples/custom/qwen2_5_omni_retention/eval_ibs.py#L243-L251) не является чистой train baseline. Обычно она становится оптимистичнее; автоматический рост model win-rate не следует.

## Ограничения критики

1. Retention выше 100% сама по себе не доказывает fake data: повторы допустимы. C01 origin UNKNOWN; C13 явно synthetic.
2. Неустановленная идентичность C03/C06/C11 не доказывает несуществование проекта.
3. Upstream имеет реальные media/evidence инструменты. Отсутствие crawler не исключает web-действия самого агента.
4. Старые per-clip normalization замечания C04 не относятся к нынешнему batch path с общим 95-м перцентилем.
5. Root MIT не лицензирует все assets; declared NC не устанавливает автоматически ограничения на каждый самостоятельно написанный RU/UA файл.
6. Pickle/joblib, plaintext tokens и недоверенный comment text — границы доверия. Malicious artifact, утечка токенов или remote exploit здесь не обнаружены.
7. Наличие serializer/UI tests не доказывает реальный CapCut/Windows playback и не означает исполнение тестов.

## Оставшиеся gates

Актуальный Google metric contract, live OAuth, права/происхождение данных, независимые holdouts, Windows CPU/RU-UA performance и editor compatibility требуют отдельных проверок после разрешения. Архитектура остаётся PROPOSED. Публикация Markdown не закрывает эти gates.
