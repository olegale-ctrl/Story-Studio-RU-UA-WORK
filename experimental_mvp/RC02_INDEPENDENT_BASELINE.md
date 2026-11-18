# RC-02 — независимая проверка, дополнение № 1

Дата: 18 ноября 2026. **Контрольный результат: `RC02_BASELINE_BLOCKED`.**

Windows 10/11 отсутствует в доступной среде: **`BLOCKED_ENVIRONMENT`**. Фактическое выполнение Windows-проверок: **`NOT_RUN`**. Ни Linux, ни Xvfb, ни успешные тесты не считаются Windows PASS. Проверка на слух и системный проигрыватель также `NOT_RUN`.

## Точная исходная версия и хронология

- Исходная ветка: `feat/story-studio-experimental-rc-02`.
- Проверенный исходный commit: `1f27a9bb024b4e2ad18121843f14fe57d0522f17`.
- Проверенный исходный tree: `2fd1e0f9f121016827f726606b821b510f6806e3`.
- Parent исходного commit: `0dc314311b1f6ae2d0a0ed51aaabe3406badcbec`.
- Исходный код проверялся из отдельного неизменённого detached checkout `/workspace/work/rc02-independent`; не из модифицированного MVP-05/06.
- Рабочая ветка отчёта: `feat/story-studio-experimental-mvp-05-06-media-hub`.
- Уже существовавший до получения дополнения implementation commit MVP-05/06: `6716ab3cd98252fb7b415de38d898c1035854ffe`, tree `6d491132fe858c5add076d26384d0b382b4304ff`.

Дополнение получено после предыдущей реализации и публикации MVP-05/06. Выполнить его задним числом «до реализации» невозможно. Этот отчёт не заявляет соблюдения такого порядка и не переписывает историю. Новая функциональность в рамках дополнения не реализуется; существующая реализация сохранена. Нормативные контракты, G3.2.1, CI, main и production storage не изменяются. Production permissions не выдаются.

## Конфигурация и установка

| Параметр | Фактически доступно | Windows 10/11 |
|---|---|---|
| ОС | Linux x86_64, ядро 6.18.57 | `BLOCKED_ENVIRONMENT`; версия/build Windows неизвестны |
| Python | CPython 3.12.14 | 3.13.17 x64: `NOT_RUN` |
| Tk | 9.0.4; реальный Tk через Xvfb :89 | Windows Tkinter: `NOT_RUN` |
| FFmpeg / FFprobe | 7.1.5-0+deb13u1 | Windows установка/кодеки: `NOT_RUN` |
| Edge TTS | Пакет не установлен | Windows без edge-tts: `NOT_RUN` |
| Пользователь | UID 1000; проверки без root | Отсутствие необходимости administrator на Windows: `NOT_RUN` |
| PowerShell / Wine | Не обнаружены | Запуск GUI из PowerShell: `NOT_RUN` |
| Профиль приложения | `STORY_MVP_HOME=/workspace/work/rc02-addendum-evidence/isolated-profile` | Чистое/изолированное Windows окружение: `NOT_RUN` |

Linux-профиль изолирует состояние приложения; это не заявление о чистой установке Windows или чистом системном Python. Внешние локальные test assets — собственная схема и eSpeak NG MP3 из существующего экспериментального пакета. Для исходного RC-02 из них подготовлены отдельные 6-секундные WAV/MP3. Новых внешних синтезов или заимствования чужих материалов не было.

Фактические команды, рабочая папка — точный detached RC-02:

```bash
python --version
ffmpeg -version
ffprobe -version
python -m unittest experimental_mvp.test_pipeline -v
DISPLAY=:89 python -m experimental_mvp.pipeline --check
python /workspace/work/rc02-addendum-evidence/verify_rc02.py
DISPLAY=:89 python /workspace/work/rc02-addendum-evidence/gui_baseline.py create
DISPLAY=:89 python /workspace/work/rc02-addendum-evidence/gui_baseline.py reopen
```

Для независимого Windows-исполнителя, **команды ещё не выполнялись**:

```powershell
$env:STORY_MVP_HOME = Join-Path $env:USERPROFILE 'StoryStudio-RC02-Independent'
python --version
python -c "import struct, tkinter; print(struct.calcsize('P') * 8, tkinter.TkVersion)"
ffmpeg -version
ffprobe -version
python -m experimental_mvp.pipeline --check
python -m experimental_mvp.pipeline
```

Нужно сохранить точный checkout исходного RC-02, реальные Windows build, Python 3.13.17 x64, версии бинарников и stdout/stderr. Команды `--check-edge ru/uk` требуют отдельного разрешённого онлайн-прогона, установленного клиента и доступного сервиса. Их возможный успех не означает разрешение на использование голосов в production.

## Матрица фактических проверок

Все PASS ниже относятся **только к Linux**. Для всех строк Windows выполнение `NOT_RUN` по причине `BLOCKED_ENVIRONMENT`.

| Проверка | Linux статус / доказательство | Реальный exit code |
|---|---|---:|
| Исходный unittest | `PASS`: 9 tests, 0 skips, 3.272 s | 0 |
| `--check` | `PASS`: Tk, ffmpeg/ffprobe, 1080p H.264/AAC/mov_text, preview с libass; edge-tts не установлен | 0 |
| GUI: открыть RU-демо; новый проект; добавить/удалить сцену | `PASS`: реальные Tk widgets/commands исходного GUI, процесс create | 0 |
| GUI: текст/изображение; перестановка сцен | `PASS`: widget-driven редактирование и изменение порядка | 0 |
| GUI: ручные титры, пересчёт, отказ сохранить overrun | `PASS`: действительный диалог субтитров; ошибочная строка помечена invalid и не сохранена | 0 |
| GUI: сохранить, закрыть процесс, заново открыть/сохранить | `PASS`: отдельные процессы create/reopen; сравнены ID, тексты, image path, captions_by_scene и UTF-8 | 0 / 0 |
| Локальный WAV, без edge-tts | `PASS`: реальный CLI export | 0 |
| Локальный MP3, без edge-tts | `PASS`: независимый реальный CLI export | 0 |
| Предпросмотр сцены / всего ролика | `PASS`: реальные вызовы исходных render_preview / build(preview=True), файлы созданы; это API, не нажатие GUI playback | N/A: API вернул путь, без исключения |
| FFprobe | `PASS`: 1920×1080, H.264/AAC/mov_text, 6.000000 s | 0 |
| Полное декодирование MP4 | `PASS`: ffmpeg -xerror, stderr без ошибок | 0 |
| Визуальная проверка | `PASS` только одного извлечённого кадра: схема/кириллица читаемы; весь ролик человеком не просмотрен | N/A |
| Прослушивание и субъективная синхронизация | `NOT_RUN`; наличие аудиопотока/декодирование это не подтверждает | N/A |
| Системный проигрыватель | `NOT_RUN`; ни Windows Shell playback, ни desktop player здесь не квалифицированы | N/A |
| Ошибка отсутствующего аудиофайла | `PASS`: ожидаемый отказ CLI | 1, ожидается 1 |
| Повреждённый MP3 / WAV | `PASS`: ожидаемые отказы CLI | 1 / 1, ожидается 1 |
| Отсутствующий FFmpeg | `PASS`: задан несуществующий STORY_MVP_FFMPEG, ожидаемый отказ | 1, ожидается 1 |
| Повреждённый project JSON | `PASS`: ожидаемый отказ загрузки CLI | 1, ожидается 1 |
| Реплика за длительностью сцены | `PASS`: отказ CLI и invalid-строка GUI | 1 CLI; GUI процесс 0 |
| Восстановление после ошибок | `PASS`: исправлены входы; проект повторно прочитан/экспортирован CLI | 0 |
| Кириллица и пробелы в путях | `PASS`: реальные WAV/MP3, image и project под `Кириллица и пробелы/` | 0 у экспортов |
| Отсутствие сети | `PASS` для Linux CLI: strace запрещает socket/connect в Python и FFmpeg children; 0 сетевых вызовов | 0 |
| Остановить после аудио / повторить / reuse | `PASS` в исходных автоматизированных тестах; настоящий cache и FFmpeg, аудиосинтез — детерминированный mock | 0 test suite |
| Ошибка Edge/синтеза и повтор | `PASS` только обработчик смоделированного сбоя в исходных тестах; не реальный Edge outage | 0 test suite |
| Реальный Edge TTS RU/UA | `NOT_RUN`; клиент отсутствует, онлайн-синтез не выполнялся; доступность сервиса не установлена | N/A |
| GUI repair missing-file links / GUI stop button | `NOT_RUN`; есть автоматизированные file-repair/cancel oracles, они не равны ручному GUI-прохождению этих действий | N/A |
| Ложный успешный export | `PASS`: для failed result.json нет завершённого final.mp4; corrupt JSON не создаёт успешный run | N/A: assertion |

Дополнительный CLI/API runner выполнил **18 checks**, процесс exit **0**. Его отдельные отрицательные команды действительно вернули **1**; такой ожидаемый отказ — PASS проверки, а не успешный export. Для прямых Python API не выдумывается subprocess exit code. Полные результаты/команды: [results.json](reports/evidence/rc02_addendum/results.json).

## A / B / C и субтитры

**A — локальный режим:** `PASS` Linux для двух независимых CLI экспортов WAV и MP3 без установленного Edge TTS. Windows: `BLOCKED_ENVIRONMENT` / `NOT_RUN`.

**B — сетевой Edge RU/UA:** `NOT_RUN`. Не заявляется ни успешный вызов, ни `BLOCKED_EXTERNAL_SERVICE`: сервис фактически не опрашивался. Вызов не нужен для локальной сборки.

**C — восстановление:** `PASS` Linux automated oracle `test_interruption_after_audio_retains_cache_and_never_exposes_export`: остановка после подготовки аудио, interrupted result, повторный build, повторное использование cache без дополнительного синтеза. Сценарий `test_resume_failure_edit_and_reorder` проверяет повтор после mock-TTS ошибки и пересборку изменённой сцены. Ручной GUI stop/resume и Windows остаются `NOT_RUN`.

Привязка captions_by_scene к ID при перестановке, UTF-8 и пересчёт проверены исходным тестовым набором; реальный GUI дополнительно отредактировал, пересчитал, сохранил и восстановил ручные титры в новом процессе. Границы общей аудиодорожки оценочные; валидные таймкоды не доказывают синхронизацию на слух.

## MP4 и результаты

Контрольный WAV-export: **6.000000 s**, 1920×1080, H.264, AAC, mov_text. SHA-256:

`79c7ca4065b4a4f58bdd433991a359a770e608f9549590cd93f59f9a39ae35ac`

```bash
ffprobe -v error -show_streams -show_format -of json <final.mp4>
ffmpeg -v error -xerror -i <final.mp4> -f null -
```

Обе команды exit 0. FFprobe и decode logs приложены. Извлечённый кадр просмотрен визуально; это не заменяет полный просмотр, прослушивание, проверку pacing и синхронизации человеком.

## Дефекты, исправления и их SHA

1. В исходном RC-02 системное открытие файла вызывает `os.startfile` без Linux/macOS ветвления. Это ограничение Linux, не доказанный Windows-дефект. Ранее существовавший commit `6716ab3cd98252fb7b415de38d898c1035854ffe` добавил платформенный launcher и выбор доступного шрифта. Git blob `experimental_mvp/ui.py` в нём: `8ccf78dfd548e8a3e6befb0d4ce23f813209d683`. Реальное OS playback этим дополнением не квалифицировано.
2. Критические Windows-дефекты запуска, сохранения, аудио или экспорта **не оценены**: среды нет. Нельзя заявлять их отсутствие. Доступные Linux проверки не выявили новых критических отказов сохранения/экспорта при пригодных локальных входах.
3. Новых исправлений implementation в этом дополнении нет. Исходный checkout остался неизменным. Предыдущие development-сбои и прежние прогоны не выдаются за новые Windows результаты.

## Блокировки, продолжение и STOP

`RC02_BASELINE_BLOCKED` сохраняется до фактического Windows 10/11 прогона. Не закрыты Python 3.13.17 x64/PowerShell, Windows GUI и non-admin install, системный player, проверка на слух/синхронизация, реальный Edge RU/UA и ручные GUI repair/stop действия. Для закрытия нужен независимый Windows исполнитель и протокол реальных результатов.

Переход к MVP-05/06, Media Hub и интеграции уже произошёл до получения этого дополнения; соответствующая реализация имеется в commit `6716ab3…`. Она не выполняется повторно и не получает Windows PASS из этого отчёта. Дополнение добавляет только отчёт и воспроизводимые тестовые свидетельства. **STOP перед production-внедрением; независимый аудит и решение владельца.**

Нормативные контракты, main, CI, merge/release, production storage и production permissions не затронуты.
