# RC-01 · установка на Windows x64

Проверенная конфигурация: CPython **3.13.17 x64** с Tcl/Tk, **FFmpeg 9.0.2 Gyan essentials x64** и, для сетевого синтеза, **edge-tts 7.3.1** с закреплёнными зависимостями. Нужен checkout RC-01 и обычная пользовательская учётная запись Windows. Эти версии фиксируют окружение для ревью.

1. Установите [Python 3.13.17, Windows installer (64-bit)](https://www.python.org/downloads/release/python-31317/). В установщике оставьте компоненты **pip**, **tcl/tk and IDLE** и Python launcher. Выберите установку для текущего пользователя. После установки откройте новый PowerShell и проверьте `py -3.13 -VV`.
2. Скачайте [ffmpeg-9.0.2-essentials_build.zip](https://github.com/GyanD/codexffmpeg/releases/download/9.0.2/ffmpeg-9.0.2-essentials_build.zip). Проверьте SHA-256 по [реестру файлов релиза](https://github.com/GyanD/codexffmpeg/releases/expanded_assets/9.0.2), затем распакуйте архив. Разрешение на включение бинарников в поставку не используется: редактор устанавливает инструменты отдельно.

```powershell
$archive = "$env:USERPROFILE\Downloads\ffmpeg-9.0.2-essentials_build.zip"
$expected = '60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba'
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash -ne $expected) {
    throw 'Скачайте исходный ZIP точного выпуска 9.0.2 заново.'
}
$tools = "$env:LOCALAPPDATA\StoryStudioRC01\tools"
Expand-Archive -LiteralPath $archive -DestinationPath $tools
$bin = Join-Path $tools 'ffmpeg-9.0.2-essentials_build\bin'
$env:STORY_MVP_FFMPEG = Join-Path $bin 'ffmpeg.exe'
$env:STORY_MVP_FFPROBE = Join-Path $bin 'ffprobe.exe'
```

3. Из корня checkout создайте новое окружение и новый профиль приложения. Для локального импорта пропустите обе команды pip.

```powershell
if ((py -3.13 -c 'import platform; print(platform.python_version())') -ne '3.13.17') {
    throw 'Для RC-01 выберите Python 3.13.17 x64.'
}
$venv = "$env:LOCALAPPDATA\StoryStudioRC01\venv"
py -3.13 -m venv $venv
$python = Join-Path $venv 'Scripts\python.exe'
$env:STORY_MVP_HOME = "$env:LOCALAPPDATA\StoryStudioRC01\workspace"

# Только при намерении использовать онлайн-синтез:
& $python -m pip install --only-binary=:all: -r experimental_mvp/requirements-edge-win-amd64.txt
& $python -m pip check
```

4. Проверьте запуск окна Tk и локальную тестовую сборку. Проверка создаёт временный WAV, собирает MP4, проверяет H.264/AAC/mov_text через ffprobe и проверяет libass для предпросмотра сцены. Сетевых запросов она не выполняет. Для отдельной онлайн-проверки команда отправляет только короткую встроенную фразу на выбранном языке. Перед использованием Edge ознакомьтесь с [условиями и ограничениями](RC01_LICENSES.md).

```powershell
& $python -m experimental_mvp.pipeline --check
# Только для онлайн-режима:
& $python -m experimental_mvp.pipeline --check-edge ru
& $python -m experimental_mvp.pipeline --check-edge uk
# Запуск редактора:
& $python -m experimental_mvp.pipeline
```

Если Tk выдаёт ошибку, откройте установщик Python через **Modify**, включите **tcl/tk and IDLE** и повторите проверку в обычном пользовательском PowerShell. Если утилита не найдена, проверьте `Test-Path $env:STORY_MVP_FFMPEG` и `Test-Path $env:STORY_MVP_FFPROBE`. Если не проходит кодек или фильтр, сверьте хеш и пути к указанной сборке. Для Edge сначала проверьте `pip check` и сетевой доступ, затем запустите проверку выбранного голоса. При отказе сервиса можно продолжить с локальным MP3/WAV. Переменные окружения задаются заново в новом PowerShell.

## Первый ролик

- Для RU нажмите «Новый», введите тему, вручную заполните текст двух сцен и выберите локальные изображения. Для озвучки Edge оставьте общую и отдельные дорожки пустыми. Сохраните проект и подтвердите локальную сборку.
- Для UA откройте JSON сохранённого проекта или демо, укажите локальный MP3/WAV, откройте «Субтитры сцены» и сохраните правку. Постройте полный предпросмотр, затем экспортируйте MP4. В проигрывателе Windows выберите нужную дорожку субтитров.
- При использовании общей дорожки границы сцен оценочные. Итоговый `final.mp4` и `captions.srt` находятся в папке конкретного запуска под `runs` рядом с проектом.

Для повторения без Tk и сетевого клиента используйте тот же Python без установки pip-пакетов и передайте локальную озвучку.

```powershell
& $python -m experimental_mvp.pipeline --project experimental_mvp/demos/uk.json --audio 'C:\Media\narration.wav' --workspace 'C:\Media\rc01-runs' --approve
```
