"""Supplemental exact-RC02 Linux functional checks; not Windows acceptance."""
import json,os,subprocess,sys,shutil
from pathlib import Path
from hashlib import sha256
BASE=Path('/workspace/work/rc02-independent')
ROOT=Path('/workspace/work/rc02-addendum-evidence')
sys.path.insert(0,str(BASE))
from experimental_mvp.pipeline import save,load,build,preview_audio,render_preview
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()=='1f27a9bb024b4e2ad18121843f14fe57d0522f17'
media=ROOT/'Кириллица и пробелы';media.mkdir(exist_ok=True)
audio_source=Path('/workspace/work/experimental-media-hub/experimental_mvp/demos/media_hub/ru_speech.mp3')
image=media/'Моя схема.png';shutil.copyfile('/workspace/work/experimental-media-hub/experimental_mvp/demos/media_hub/ru_0.png',image)
results=[]
def run(name,args,expected=0,env=None):
 r=subprocess.run(args,cwd=BASE,env=env,capture_output=True,text=True,timeout=180)
 (ROOT/(name+'.txt')).write_text(r.stdout+'\nSTDERR\n'+r.stderr)
 results.append(dict(check=name,command=[str(x) for x in args],exit_code=r.returncode,expected_exit_code=expected,status='PASS' if r.returncode==expected else 'FAIL'))
 assert r.returncode==expected,(name,r.returncode,r.stderr[-500:])
 return r
for ext in ('wav','mp3'):
 run('prepare-'+ext,['ffmpeg','-y','-v','error','-i',str(audio_source),'-t','6','-ar','24000',str(media/('Озвучка сцены.'+ext))])
p=dict(locale='ru',approved=True,audio=str(media/'Озвучка сцены.wav'),scenes=[dict(text='Красивое видео ещё не объяснение.',image=str(image)),dict(text='Начните с вопроса зрителя.',image=str(image))])
file=media/'Проект проверки.json';save(file,p)
p['captions_by_scene']={p['scenes'][0]['id']:[dict(start_ms=100,end_ms=1200,text='Ручной титр — Київ')]};save(file,p)
cli=[sys.executable,'-m','experimental_mvp.pipeline','--project',str(file),'--workspace',str(ROOT/'runs'),'--approve']
run('local-wav-export',cli)
video=Path((ROOT/'local-wav-export.txt').read_text().split('STDERR')[0].strip().splitlines()[-1]);assert video.is_file()
r=run('ffprobe',['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)])
probe=json.loads(r.stdout);streams=probe['streams'];assert (streams[0]['width'],streams[0]['height'])==(1920,1080)
assert [s['codec_name'] for s in streams]==['h264','aac','mov_text'];assert abs(float(probe['format']['duration'])-6)<.2
run('full-decode',['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'])
run('frame',['ffmpeg','-y','-v','error','-ss','1','-i',str(video),'-frames:v','1','-threads','1',str(ROOT/'checked-frame.png')])
scene_preview,approx=render_preview(p,0,ROOT/'previews',preview_audio(p,0,ROOT/'runs'))
results.append(dict(check='scene-preview',status='PASS',exit_code=None,api_return=str(scene_preview),approximate_audio_boundaries=approx))
movie=build(p,ROOT/'movie',lambda _:None,preview=True)
results.append(dict(check='movie-preview',status='PASS',exit_code=None,api_return=str(movie)))
p['audio']=str(media/'Озвучка сцены.mp3');save(file,p);run('local-mp3-export',cli)
for ext in ('mp3','wav'):(media/('Испорчен.'+ext)).write_bytes(b'not audio')
for name,path in [('missing-audio',media/'Отсутствует.wav'),('corrupt-mp3',media/'Испорчен.mp3'),('corrupt-wav',media/'Испорчен.wav')]:
 p['audio']=str(path);save(file,p);run(name,cli,1)
 # Invalid exports cannot appear complete.
p['audio']=str(media/'Озвучка сцены.wav');save(file,p)
env={**os.environ,'STORY_MVP_FFMPEG':str(ROOT/'not-installed-ffmpeg')};run('missing-ffmpeg',cli,1,env)
p['captions_by_scene'][p['scenes'][0]['id']][0]['end_ms']=20000;save(file,p);run('caption-overrun',cli,1)
file.write_text('{ broken JSON',encoding='utf-8');run('corrupt-project-json',cli,1)
save(file,p);p['captions_by_scene'].clear();save(file,p)
run('reopen-after-errors',cli)
run('offline-export',['strace','-f','-e','trace=network','-e','inject=socket:error=ENETDOWN','-e','inject=connect:error=ENETUNREACH','-o',str(ROOT/'offline.trace'),*cli])
# No invalid run reports successful completion or exposes a completed output.
for f in (ROOT/'runs').glob('run-*/result.json'):
 status=load(f)['status']
 if status!='complete':assert not (f.parent/'final.mp4').exists()
results.append(dict(check='no-false-success',status='PASS',exit_code=None))
(ROOT/'results.json').write_text(json.dumps({'source_commit':'1f27a9bb024b4e2ad18121843f14fe57d0522f17','platform':'Linux','python':sys.version,'results':results,'output':str(video),'output_sha256':sha256(video.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
print('SUPPLEMENTAL_CHECKS',len(results),'PASS')
