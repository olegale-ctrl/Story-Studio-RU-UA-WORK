# RC-02 · минимальная локальная поставка

Минимальный комплект для проверки: `pipeline.py`, `ui.py`, `captions.py`,
`diagnostics.py`, `demos/ru.json`, `demos/uk.json`, `INSTALL_RC01.md`,
`RC01_LICENSES.md` и этот документ, все под `experimental_mvp/`. Два JSON нужны штатным
кнопкам демо и примерам CLI. Для распространения необходимо подтверждение
прав на каждый из этих файлов, включая исходники, документацию и тексты демо.

Установите Python 3.13.17 x64 с Tk и FFmpeg/ffprobe Gyan 9.0.2 по закреплённой
инструкции. Оставьте `edge-tts` неустановленным. Из корня комплекта:

```powershell
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
python -m experimental_mvp.pipeline --help
python -m experimental_mvp.pipeline --check
python -m experimental_mvp.pipeline
python -m experimental_mvp.pipeline --project experimental_mvp/demos/uk.json --audio 'C:\Media\example.wav' --workspace 'C:\Media\rc02-runs' --approve
```

Готовые сегменты можно заново экспортировать без Edge. Откройте сохранённый
проект с теми же ID сцен и настройками звука, используйте прежнюю папку
`runs` или прежний `--workspace`. Если подходящего сегмента нет, добавьте
MP3/WAV сцены либо общую дорожку. Диагностика `--check` локальна.

Полный checkout добавляет синтез через `scripts/edge_voice_demo.py` и
`--check-edge ru` / `--check-edge uk` после установки закреплённых пакетов.
Существующие голоса, повторы и правила кэша сохраняются.
Анализ внешнего JSON через Editorial Preview тоже доступен из полного
checkout. В минимальном комплекте работает локальный шаблон темы,
редактор сцен, предпросмотр и локальный экспорт.

Медиа, бинарники, колёса и сетевой голос в этот комплект не входят.
