# Sprint 10 — первое MP4 на Windows

**Предварительно:** установить FFmpeg и убедиться, что команда `ffmpeg -version` работает в PowerShell. FFmpeg — стороннее ПО; распространять его в нашем ZIP нельзя до проверки лицензий конкретной сборки. В Sprint10.zip FFmpeg не включён.

В PowerShell, из корня `Story-Studio-RU-UA`:

```powershell
python -m unittest discover -s tests -v
ffmpeg -version
python -m core.cli check .\examples\demo_project.json
python -m core.cli render-mp4 .\examples\demo_project.json --media-root .\examples\demo_media --output .\demo-first-video.mp4
```

Ожидаемые файлы: `demo-first-video.mp4` и `demo-first-video.sub01.srt` в корне проекта. Субтитры **не вшиты** в видео: импортируйте SRT в проигрыватель отдельно. Повторный запуск с тем же именем файла намеренно отклоняется (никакой перезаписи). Удалите тестовые выходные файлы или выберите другое имя перед повторным запуском.

Ограничения прототипа: только последовательные неподвижные изображения без пробелов/перекрытий, 1 необязательная аудиодорожка, выход H.264/AAC MP4, отдельный SRT; требуются FFmpeg с libx264 и AAC encoder. Размеры и длительности ограничены проектом; генерация AI, переходы, титры поверх видео, native editor export пока отсутствуют.

Демонстрационные изображения PPM и тестовый звук WAV созданы специально для этого проекта, не взяты из китайских корпусов.
