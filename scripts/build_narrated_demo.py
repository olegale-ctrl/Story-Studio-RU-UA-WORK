"""Build an original RU/UA narrated demo project from locally synthesized WAVs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import wave

LINES = {
 'uk': ['Вітаємо у Story Studio. Тут починається ваша історія.', 'Додавайте зображення, озвучення та субтитри.', 'Створюйте відео українською або російською мовою.'],
 'ru': ['Добро пожаловать в Story Studio. Здесь начинается ваша история.', 'Добавляйте изображения, озвучивание и субтитры.', 'Создавайте видео на русском или украинском языке.'],
}
COLORS = [(38, 78, 110), (40, 105, 92), (105, 65, 104)]

def duration_ms(path: Path) -> int:
    with wave.open(str(path), 'rb') as f:
        return (f.getnframes() * 1000 + f.getframerate() - 1) // f.getframerate()

def build(locale: str, out: Path, width: int = 640, height: int = 360) -> Path:
    if locale not in LINES: raise ValueError('locale must be ru or uk')
    if width < 2 or height < 2 or width % 2 or height % 2: raise ValueError('even dimensions required')
    out.mkdir(parents=True, exist_ok=True)
    media = out / 'media'; media.mkdir(exist_ok=True)
    project = dict(title='Story Studio — narrated demo', content_locale=locale, scenes=[], fps=25, width=width, height=height, schema_version=3, tracks=[dict(id='v',kind='video',label='Images'),dict(id='a',kind='audio',label='Voice'),dict(id='s',kind='subtitle',label='Captions')], subtitles=[], media=[], clips=[])
    cursor=0
    for i, (line, rgb) in enumerate(zip(LINES[locale], COLORS), 1):
        wav = media / f'voice{i}.wav'
        if not wav.is_file(): raise FileNotFoundError(f'Missing {wav}; run scripts/make_voice_demo.ps1 first')
        audio_ms = duration_ms(wav)
        # 25fps => 40ms per frame; allow half-second gap after speech.
        scene_ms = ((audio_ms + 500 + 39) // 40) * 40
        image = media / f'frame{i}.ppm'
        # Generated original gradient; no external assets or third-party libraries.
        with image.open('wb') as f:
            f.write(f'P6\n{width} {height}\n255\n'.encode('ascii'))
            for y in range(height):
                tint = y * 45 // height
                f.write(bytes(max(0, c - tint) for c in rgb) * width)
        project['media'] += [dict(id=f'i{i}',kind='image',path=f'frame{i}.ppm'),dict(id=f'a{i}',kind='audio',path=f'voice{i}.wav')]
        project['clips'] += [dict(id=f'v{i}',track_id='v',media_id=f'i{i}',start_ms=cursor,duration_ms=scene_ms,source_in_ms=0),dict(id=f'c{i}',track_id='a',media_id=f'a{i}',start_ms=cursor,duration_ms=audio_ms,source_in_ms=0)]
        project['subtitles'].append(dict(id=f's{i}',track_id='s',start_ms=cursor,duration_ms=audio_ms,text=line,locale=locale))
        cursor += scene_ms
    target=out / 'narrated_project.json'
    target.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return target

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--locale',choices=('ru','uk'),default='uk'); p.add_argument('--output-dir',type=Path,default=Path('examples/narrated_uk'))
    a=p.parse_args(); print('OK:',build(a.locale,a.output_dir))
