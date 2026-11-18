# MVP-07 — Windows independent checklist

**WINDOWS_NOT_RUN.** Linux/Xvfb результаты не закрывают пункты ниже. Требуется точный commit из финального handoff manifest, Windows 10/11, Python/Tkinter x64 и CPU-only FFmpeg. Для legacy RC-02 Windows gate см. ../RC02_INDEPENDENT_BASELINE.md: он остаётся RC02_BASELINE_BLOCKED.

Сохранить Windows edition/build, Python architecture/version, Tcl/Tk patchlevel, FFmpeg/FFprobe версии/кодеки, профиль без administrator, масштаб 100%/150% и действительные exit codes. Не использовать старые отчёты Python 3.13.17 как доказательство этого запуска.

```powershell
$env:STORY_MVP_HOME = Join-Path $env:USERPROFILE 'StoryStudio-MVP07-Independent'
python --version
python -c "import struct,tkinter; r=tkinter.Tk(); print(struct.calcsize('P')*8,r.tk.eval('info patchlevel')); r.destroy()"
ffmpeg -version
ffprobe -version
python -m experimental_mvp.pipeline --check
python -m experimental_mvp.pipeline
python -m unittest experimental_mvp.test_pipeline experimental_mvp.test_media_hub experimental_mvp.test_media_ui experimental_mvp.test_timeline experimental_mvp.test_timeline_ui -v
```

1. Открыть старый RU/UA JSON без timeline-полей. Проверить сохранность IDs/assets/captions, save/reopen и прежний export. Edge TTS не обязателен для локального MP3/WAV.
2. Демо RU «Почему исчезли древние цивилизации?» / UA «Як виникли перші міста?»: 8 сцен; новый Canvas tab; прочитать текстовые статусы при разных цветах/масштабах. Проверить scroll, zoom, SCENE/AUDIO/ANCHOR/CAPTION и общую длину.
3. Выбрать якорь; drag body внутри сцены, правый край, numeric edit; Shift/arrow keys, Ctrl+Z/Y/D, Delete с подтверждением. Попробовать отрицательную/нулевую длину и непреднамеренный выход за сцену: исходный проект не должен измениться частично.
4. Split обычного импортированного clip: соседние source intervals одного файла; export обоих. Incompatible merge должен отказать без изменений. Duplicate получает новый ID; deletion не удаляет файл; Undo восстанавливает ссылки.
5. Импортировать собственные PNG/JPEG/WebP и MP4 с разными FPS/resolution через старую «Раскадровку», применить и reload timeline. Не использовать чужие материалы без прав. Проверить missing/tampered/corrupt asset, кириллический путь и пробелы.
6. Выбрать source in/out, FIT/CROP и явно ERROR/HOLD_LAST_FRAME/LOOP. Short clip без решения не должен незаметно растягиваться; скорость не меняется. Проверить смешанную последовательность нескольких 5–10 s клипов.
7. Импортировать whole audio и отдельные scene files; подготовить cache. Переставить сцены, сверить ID и доступную карту. Различить измеренное audio, оценочные границы, ручные длительности и неподготовленную плановую оценку. Изменить audio duration: увидеть конфликты, затем явно redistribute/fallback/trim/keep manual.
8. Ручной subtitle cue: текст, start/end; overrun/overlap должен отказать. Остальные manual cues не заменяются calculated без решения. Сцены меняют порядок без потери caption binding. Проверить RU/UA Unicode.
9. Preview anchor/scene/project/position, progress и cancellation. Проверить, что source project unchanged; Windows shell открывает правильный временный файл. При правках во время render preview должен помечаться stale. Не ожидать синхронного player cursor; seek-preview заканчивается текущей сценой.
10. Создать unsaved untitled project, закрыть: Save/Discard/Cancel. Повторить для timeline edits, New/Open, stale apply и отказа записи (readonly/locked file). Существующий файл не должен повредиться; окно не должно закрыться при ошибке сохранения.
11. Подтвердить только локальный экспериментальный render, экспортировать оба проекта и проверить FFprobe/full decode. Посмотреть весь MP4 **и прослушать**: произношение, синхронизация, субтитры, порядок кадров, held/loop решения. Decoder success не заменяет такую приёмку.

```powershell
ffprobe -v error -show_streams -show_format -of json <final.mp4>
ffmpeg -v error -xerror -i <final.mp4> -f null -
```

Ожидаемые output streams: 1920×1080 H.264, AAC, mov_text. Сверить duration-check.json, реальные frame/audio durations, SHA-256, copied-input intervals и result.json. Не заявлять PASS для NOT_RUN. На этом этапе нельзя запускать CI, merge/release, менять main, нормативные PG/G3.2.1 contracts, production storage или permissions.
