# SI-PRODUCT-02.2 — карта интеграции

План первого сквозного задания. Текущие API проверены на `da1d3dd2ad6a55943e88503f5231f4c34a1e4e5f`.

| Шаг | Фактический интерфейс | Работа для 02.2 |
|---|---|---|
| Выбранная тема | Формат интеграционного `topic.json` пока отсутствует. Два примера `first_video_plan_{ru,uk}.json` — уже готовые планы сцен | Добавить адаптер для одной синтетической темы и двух локалей. Зафиксировать проверяемые входы и ожидаемые результаты |
| Evaluation | `story_intelligence.evaluate_v1.evaluate_si(records, semantic_input_refs, observed_context, ratings, expected_context, human_findings, required_current_premise=None, *, ui_locale=None)`. Возвращает plain dict: OK с eligibility, баллом и диагностикой или INVALID/STALE без принятой eligibility. Использует exact SI/1 refs и полные снимки контекста | Подготовить по существующим схемам связанный набор данных и контекст для каждой оцениваемой локали. `ui_locale` должен совпасть с локалью Audience/Idea Intake. Поддержать явный отказ при отсутствующих или устаревших входах |
| Editorial card | `story_intelligence.decision_projection_v1.project_evaluation(evaluation_inputs, evaluation_result, display_locale)`. Повторно вызывает evaluator и возвращает приватную карточку либо UNAVAILABLE. Язык отображения независим от локали оценки | Вызвать с тем же набором аргументов. Сохранить диагностический результат. Отдельно потребовать редакционное разрешение перед сборкой производственных файлов |
| Production plan | `scripts.first_video.read_plan` принимает UTF-8 JSON с `locale` (`ru`/`uk`), опциональным `title`, 1–20 `scenes` с непустым `text` до 2000 символов и необязательным именем `image` | Преобразовать одобренные тексты и материалы в два scene plan, с WAV по порядковому номеру сцены. Карточка сама по себе не создаёт сценарий |
| RU/UK MP4 | `python scripts/first_video.py --plan <json> --audio-dir <dir> --output-dir <new-dir>` или `scripts.first_video.build`. На входе `voice1.wav` и далее. На выходе `project.json`, `media/` и `first-video.mp4` для каждого языка. Длительность и субтитры рассчитываются по WAV на уровне сцены. `--no-render` создаёт только проект | Выполнить два вызова из одного запуска. Проверить H.264/AAC, сценовые тексты и интервалы в `project.json`, наличие прожжённых субтитров и повторяемость структуры и длительности при одинаковых входах |

Редактор задаёт тему и аудиторию, предоставляет или подтверждает источники, даты получения и проверяемые фрагменты, привязку утверждений к доказательствам, ratings/findings и требования к свежести. Для реального материала проверка источников предшествует оценке. Решение о съёмке, утверждённые RU/UK тексты и проверка прав на изображения, WAV и голоса предшествуют сборке. Синтетическая тема помечается как тестовая. Eligibility и AI-обоснование сами по себе не подтверждают факты, права или разрешение на производство.

Локальная оценка, проекция, сборка из WAV и FFmpeg работают без сети при подготовленных входах и инструментах. Поиск источников, LLM-оценка и независимая критика ведутся в 02.3. Испытания Silero остаются отложенными. Новый обработчик темы, преобразование в два плана и единая команда ещё не реализованы.

## Воспроизводимый тест видеочасти сегодня

Из корня создать три WAV mono PCM16 24 кГц с одной секундой тишины. Оба существующих плана содержат по три сцены. Использовать новый суффикс выходных каталогов при повторе.

```text
python -c "from pathlib import Path; import wave; p=Path('output/synthetic-wav'); p.mkdir(parents=True, exist_ok=True); exec('for i in range(1, 4):\n with wave.open(str(p / f\'voice{i}.wav\'), \'wb\') as w:\n  w.setparams((1, 2, 24000, 0, \'NONE\', \'not compressed\')); w.writeframes(bytes(48000))')"
python scripts/first_video.py --plan examples/first_video_plan_ru.json --audio-dir output/synthetic-wav --output-dir output/smoke-ru
python scripts/first_video.py --plan examples/first_video_plan_uk.json --audio-dir output/synthetic-wav --output-dir output/smoke-uk
ffprobe -v error -show_entries stream=codec_name,codec_type -show_entries format=duration -of json output/smoke-ru/first-video.mp4
ffprobe -v error -show_entries stream=codec_name,codec_type -show_entries format=duration -of json output/smoke-uk/first-video.mp4
```

Проверить `project.json` на три субтитра и правильную локаль. Прожжённые субтитры проверять на кадрах. Отдельного subtitle stream у этого режима рендера нет. Повторять с новыми директориями и сопоставлять структуру, тайминг и потоки. Битовая идентичность MP4 между версиями FFmpeg не является критерием.

Первое задание 02.2 — один синтетический сценарий с двумя локалями и заранее выбранными сценами, один адаптер и один сквозной тест. Test input не должен зависеть от моделей речи, сети или лицензируемых голосов. Прогон должен фиксировать карточку, планы и результаты ffprobe, а также проверять, что отклонённый вход не переходит к рендеру.
