"""Build original local MVP-07 fixtures; requires separately installed eSpeak NG/FFmpeg and a font.
No downloads, AI media credits, external TTS calls or third-party imagery.
"""
import argparse
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import uuid
from experimental_mvp.pipeline import DEMOS, executable, duration, save
from experimental_mvp.storyboard import VideoAnchor
from experimental_mvp.timeline import Editor,timing_map,distribute


def run(args,folder=None):subprocess.run([str(x) for x in args],cwd=folder,check=True,capture_output=True)


def prepare(folder,espeak,data,font):
    folder=Path(folder).resolve();folder.mkdir(parents=True,exist_ok=True);ffmpeg=executable('ffmpeg');probe=executable('ffprobe')
    audit=[]
    for locale in ('ru','uk'):
        script=json.loads((DEMOS/'timeline'/(locale+'_script.json')).read_text(encoding='utf-8'))
        p={**script,'approved':False,'timeline':{'version':1,'scene_durations_ms':{}},
           'output_profile':{'width':1920,'height':1080,'fps':30},'captions_by_scene':{},
           'brief':'UNVERIFIED editorial-training draft; original diagrams are illustrative, not historical evidence.'}
        parts=[];lengths=[]
        for n,s in enumerate(p['scenes']):
            sid=uuid.uuid5(uuid.NAMESPACE_URL,f'mvp07/{locale}/{n}').hex;s['id']=sid
            text=folder/'speech.txt';text.write_text(s['text'],encoding='utf-8')
            raw=folder/f'{locale}{n}-raw.wav';out=folder/f'{locale}{n}.wav'
            args=[espeak,'-v',locale,'-s','180','-f',text,'-w',raw]
            if data:args.insert(1,'--path='+str(data))
            run(args);run([ffmpeg,'-y','-v','error','-i',raw,'-ar','24000','-ac','1',out]);raw.unlink()
            parts.append(out);lengths.append(duration(out,probe));text.unlink()
            # Original labelled process cards; no maps, archaeological photos or stock.
            pixels=bytearray(bytes((18,36,57))*640*360)
            for j in range(4):
                for y in range(145,270):
                    for x in range(20+j*155,160+j*155):
                        k=(y*640+x)*3;pixels[k:k+3]=bytes((50+20*j,100+10*n,150+15*j))
            ppm=folder/'card.ppm';ppm.write_bytes(b'P6\n640 360\n255\n'+pixels)
            caption=folder/'label.txt';caption.write_text(f'{n+1}. '+s['visual']+'\nILLUSTRATIVE LOCAL DIAGRAM\nNOT HISTORICAL EVIDENCE',encoding='utf-8')
            shutil.copyfile(font,folder/'font.ttf');image=folder/f'{locale}_{n}.png'
            run([ffmpeg,'-y','-v','error','-i',ppm,'-vf','drawtext=fontfile=font.ttf:textfile=label.txt:expansion=none:fontsize=21:fontcolor=white:x=20:y=28','-frames:v','1','-threads','1',image],folder)
            for file in (ppm,caption,folder/'font.ttf'):file.unlink()
        listing=folder/'audio.txt';listing.write_text(''.join("file '"+part.name+"'\n" for part in parts),encoding='ascii')
        output=folder/f'{locale}_narration.mp3'
        run([ffmpeg,'-y','-v','error','-f','concat','-safe','1','-i',listing,'-b:a','64k',output],folder)
        total=duration(output,probe);lengths[-1]+=total-sum(lengths)
        for part in parts:part.unlink()
        listing.unlink();p['audio']='./'+output.name
        clip=folder/f'{locale}_local_motion.mp4'
        run([ffmpeg,'-y','-v','error','-loop','1','-framerate','15' if locale=='ru' else '60','-i',folder/f'{locale}_0.png',
             '-vf',r'scale=640:360,zoompan=z=min(zoom+0.0004\,1.06):d=1:s=640x360:fps='+('15' if locale=='ru' else '60'),
             '-t','5','-c:v','libx264','-preset','ultrafast','-threads','2',clip])
        for n,(s,ms) in enumerate(zip(p['scenes'],lengths)):
            p['timeline']['scene_durations_ms'][s['id']]=ms;s['anchors']=[];start=0
            count=max(3,round(ms/7000));steps=distribute([1]*count,ms)
            for j,amount in enumerate(steps):
                a=asdict(VideoAnchor(uuid.uuid5(uuid.NAMESPACE_URL,f'mvp07/{locale}/{n}/{j}').hex,s['id'],start,amount,
                                     narration_excerpt=s['text'],visual_description=s['visual'],generation_mode='IMAGE_PAN_ZOOM',
                                     generation_status='IMPORTED',license_status='ORIGINAL_LOCAL_DEMO'))
                file=clip if j==0 and n==0 else folder/f'{locale}_{n}.png'
                a.update(local_asset_path='./'+file.name,asset_sha256=sha256(file.read_bytes()).hexdigest(),
                         fit_mode='FIT',provenance={'provider':'LOCAL_PROCEDURAL','original_name':file.name,'sha256':sha256(file.read_bytes()).hexdigest()})
                if file==clip:a.update(generation_mode='LOCAL_VIDEO',source_start_ms=0,source_end_ms=5000,source_duration_ms=5000,short_clip_policy='HOLD_LAST_FRAME')
                s['anchors'].append(a);start+=amount
            from experimental_mvp.captions import calculated
            rows=calculated(s['text'],ms)
            for row in rows:row['timing_kind']='ESTIMATED_CAPTION_TIMING'
            rows[0]['start_ms']=100;rows[0]['end_ms']-=100;rows[0]['timing_kind']='MANUAL_CAPTION_TIMING'
            p['captions_by_scene'][s['id']]=rows

        e=Editor(p,timing_map(p,whole_ms=total));s=p['scenes'][1];a,b=s['anchors'][:2]
        e.edit('set',a['anchor_id'],duration_ms=a['duration_ms']+400)
        e.edit('set',b['anchor_id'],start_ms=b['start_ms']+400,duration_ms=b['duration_ms']-400)
        # Explicit swap of the first two equal-length still anchors in a different scene.
        s=p['scenes'][2];a,b=s['anchors'][:2]
        ea=e.locate(e.project,a['anchor_id'])[1];eb=e.locate(e.project,b['anchor_id'])[1]
        old_a,old_b=ea['start_ms'],eb['start_ms'];len_a,len_b=ea['duration_ms'],eb['duration_ms']
        e.edit('set',a['anchor_id'],start_ms=old_b,duration_ms=len_b)
        e.edit('set',b['anchor_id'],start_ms=old_a,duration_ms=len_a)
        save(folder/(locale+'.json'),e.project)
        reopened=json.loads((folder/(locale+'.json')).read_text(encoding='utf-8'))
        assert reopened==e.project and not e.conflicts()
        audit.append(dict(locale=locale,topic=p['topic'],duration_ms=total,anchors=sum(len(s['anchors']) for s in p['scenes']),
                          demonstrated=['explicit duration edit + adjacent trim','two anchor position swap','manual captions','atomic save/reopen'],
                          audio_timing='manual boundaries from measured local segment durations; MP3 encoder tail assigned to last scene',
                          external_services=False))
    (folder/'editing-demonstration.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(audit,ensure_ascii=False,indent=2))


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--espeak',type=Path,required=True);a.add_argument('--data',type=Path);a.add_argument('--font',type=Path,required=True);a.add_argument('--output',type=Path,default=DEMOS/'timeline')
    v=a.parse_args();prepare(v.output,v.espeak,v.data,v.font)
