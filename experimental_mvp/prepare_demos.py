"""Rebuild optional offline demonstration assets using a user-installed eSpeak NG and FFmpeg.

python -m experimental_mvp.prepare_demos --espeak /path/to/espeak-ng --data /path/containing/espeak-ng-data --font /path/to/font.ttf
No downloads, network services, copyrighted stock, or credentials are used by this command.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import uuid

from experimental_mvp.intelligence import apply_draft
from experimental_mvp.pipeline import DEMOS, duration, executable, intervals, save
from experimental_mvp.storyboard import suggest, fingerprint


def prepare(folder, espeak, data, font):
    folder=Path(folder).resolve();folder.mkdir(parents=True,exist_ok=True)
    for locale in ('ru','uk'):
        draft=json.loads((DEMOS/'media_hub'/f'editorial_{locale}.json').read_text(encoding='utf-8'))
        p=apply_draft({'locale':locale,'scenes':[],'topic':'Проверяем историю / Перевіряємо історію'}, {**draft,'locale':locale})
        for n,scene in enumerate(p['scenes']):
            scene['id']=uuid.uuid5(uuid.NAMESPACE_URL,f'story-studio-media-demo/{locale}/{n}').hex
        text=folder/f'narration_{locale}.txt';text.write_text(draft['script'],encoding='utf-8')
        speech=folder/f'{locale}_speech.wav';audio=folder/f'{locale}_speech.mp3'
        args=[str(espeak),'-v',locale,'-s','170','-f',str(text),'-w',str(speech)]
        if data:args.insert(1,'--path='+str(data))
        subprocess.run(args,check=True)
        subprocess.run([executable('ffmpeg'),'-y','-v','error','-i',str(speech),'-ar','24000','-ac','1','-b:a','64k',str(audio)],check=True)
        speech.unlink();text.unlink()
        total=duration(audio,executable('ffprobe'))
        spans=list(intervals([s['text'] for s in p['scenes']],total))
        for n,(scene,(start,end)) in enumerate(zip(p['scenes'],spans)):
            # Original local procedural illustration, no external photographs or model-generated assets.
            w,h=640,360; pixels=bytearray(bytes((18,36,57))*(w*h))
            for j in range(4):
                x0=20+j*155;y0=140
                for y in range(y0,270):
                    for x in range(x0,min(x0+140,w)):
                        pos=(y*w+x)*3;pixels[pos:pos+3]=bytes((45+20*j,125+10*n,155+15*j))
            ppm=folder/f'{locale}_{n}.ppm';ppm.write_bytes(f'P6\n{w} {h}\n255\n'.encode()+pixels)
            caption=folder/'title.txt';caption.write_text(f'{n+1}. '+scene['visual']+'\nLOCAL DIAGRAM / EXPERIMENTAL',encoding='utf-8')
            # Copy font to a simple local filename to avoid filtergraph path escaping.
            import shutil
            shutil.copyfile(font,folder/'demo-font.ttf')
            image=folder/f'{locale}_{n}.png'
            filters='drawtext=fontfile=demo-font.ttf:textfile=title.txt:fontsize=22:fontcolor=white:x=24:y=40'
            label_paths=[]
            for k,label in enumerate(draft['scenes'][n].get('visual_steps', [])):
                label_file=folder/f'label{k}.txt';label_file.write_text(label,encoding='utf-8');label_paths.append(label_file)
                filters += f',drawtext=fontfile=demo-font.ttf:textfile=label{k}.txt:fontsize=15:fontcolor=white:x={24+k*155}:y=190'
            subprocess.run([executable('ffmpeg'),'-y','-v','error','-i',str(ppm),'-vf',filters,
                            '-frames:v','1','-threads','1',str(image)],cwd=folder,check=True)
            ppm.unlink();caption.unlink();(folder/'demo-font.ttf').unlink()
            for label_file in label_paths:label_file.unlink()
            scene['anchors']=suggest(scene,end-start,7000)
            for j,a in enumerate(scene['anchors']):
                a['anchor_id']=uuid.uuid5(uuid.NAMESPACE_URL,f'story-studio-media-demo/{locale}/{n}/{j}').hex
                a.update(generation_mode='IMAGE_PAN_ZOOM',generation_status='IMPORTED',local_asset_path='./'+image.name,
                         license_status='ORIGINAL_LOCAL_DEMO',asset_sha256=sha256(image.read_bytes()).hexdigest())
                a['provenance']={'provider':'LOCAL_PROCEDURAL','original_name':image.name,
                                 'prompt_fingerprint':fingerprint(a),'sha256':a['asset_sha256']}
        p.update(audio='./'+audio.name,approved=False,mode='MANUAL_OFFLINE',output_profile={'width':640,'height':360,'fps':24},
                 demo_notes='Original instructional draft, local procedural cards and eSpeak NG narration. No production permission. Estimated scene boundaries require human listening review.')
        save(folder/f'{locale}.json',p)
        print(locale,total,'ms',sum(len(s['anchors']) for s in p['scenes']),'anchors')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DEMOS/'media_hub')
    parser.add_argument('--espeak',type=Path,required=True)
    parser.add_argument('--data',type=Path)
    parser.add_argument('--font',type=Path,required=True)
    a=parser.parse_args();prepare(a.output,a.espeak,a.data,a.font)


if __name__=='__main__':main()
