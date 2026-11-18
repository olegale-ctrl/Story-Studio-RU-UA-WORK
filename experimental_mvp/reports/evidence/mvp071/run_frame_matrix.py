"""Local real-render frame budget qualification, no network/GPU/paid generators.
Run from repository root: PYTHONPATH=. python .../run_frame_matrix.py --output <dir>
"""
import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from experimental_mvp import pipeline as pipe, storyboard as sb, timeline as t
from experimental_mvp.test_timeline import audio


def run(args):subprocess.run([str(a) for a in args],capture_output=True,check=True)


def matrix(root):
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True);ffmpeg=pipe.executable('ffmpeg');probe=pipe.executable('ffprobe')
    image=root/'Локальная схема.png';clips=[root/'source15.mp4',root/'source60.mp4']
    run([ffmpeg,'-y','-v','error','-f','lavfi','-i','color=c=blue:s=192x108','-frames:v','1','-threads','1',image])
    for clip,fps,size in zip(clips,[15,60],['160x120','320x180']):
        run([ffmpeg,'-y','-v','error','-f','lavfi','-i',f'testsrc2=s={size}:r={fps}','-t','8','-c:v','libx264','-preset','ultrafast','-threads','2',clip])
    records=[]
    for label,count,fps in [('A',30,24),('B',60,25),('C',120,30),('D',180,30)]:
        lengths=[5000+(i%7)*17 for i in range(count)]
        expected=round(sum(lengths)*fps/1000);cursor=0;budget=[]
        for length in lengths:
            frames=round((cursor+length)*fps/1000)-round(cursor*fps/1000);assert frames>0
            budget.append(frames);cursor+=length
        assert sum(budget)==expected
        folder=root/label;folder.mkdir(exist_ok=True);speech=folder/'Инженерная тишина.wav';audio(speech,cursor/1000)
        project={'locale':'ru','approved':True,'timeline':{'version':1},'output_profile':{'width':160,'height':90,'fps':fps},
                 'audio':str(speech),'scenes':[{'text':'Инженерный тест, без утверждений о качестве речи.'}]}
        pipe.identify(project);scene=project['scenes'][0];scene['anchors']=[];start=0
        for i,length in enumerate(lengths):
            a=asdict(sb.VideoAnchor(f'matrix-{label}-{i}',scene['id'],start,length,generation_status='IMPORTED',license_status='ORIGINAL_LOCAL_FIXTURE'))
            if i%4==0:a.update(local_asset_path=str(image),generation_mode='IMAGE_PAN_ZOOM',fit_mode='FIT')
            elif i%4==1:a.update(local_asset_path=str(clips[0]),generation_mode='LOCAL_VIDEO',source_start_ms=100,source_end_ms=1100,short_clip_policy='HOLD_LAST_FRAME',fit_mode='FIT')
            elif i%4==2:a.update(local_asset_path=str(clips[1]),generation_mode='LOCAL_VIDEO',source_start_ms=200,source_end_ms=900,short_clip_policy='LOOP',fit_mode='CROP')
            else:a.update(local_asset_path=str(clips[0]),generation_mode='LOCAL_VIDEO',source_start_ms=500,source_end_ms=6500,short_clip_policy='ERROR',fit_mode='CROP')
            a['asset_sha256']=sha256(Path(a['local_asset_path']).read_bytes()).hexdigest();a['provenance']={'fixture':Path(a['local_asset_path']).name,'sha256':a['asset_sha256']}
            scene['anchors'].append(a);start+=length
        assert not t.coverage(scene,cursor)
        project_file=folder/'project.json';pipe.save(project_file,project)
        print('START',label,count,fps,cursor,flush=True)
        output=pipe.build(project,folder/'runs',lambda _:None)
        result=subprocess.run([probe,'-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,nb_frames,duration,r_frame_rate','-of','json',str(output)],capture_output=True,check=True)
        info=json.loads(result.stdout);actual=int(info['streams'][0]['nb_read_frames']);assert actual==expected
        packets=json.loads(subprocess.check_output([probe,'-v','error','-select_streams','v:0','-show_entries','packet=pts_time','-of','json',str(output)]))['packets']
        max_pts_error=max(abs(float(packet['pts_time'])-i/fps) for i,packet in enumerate(packets))
        assert len(packets)==expected and max_pts_error<=.000002
        decoded=subprocess.run([ffmpeg,'-v','error','-xerror','-i',str(output),'-f','null','-'],capture_output=True)
        assert decoded.returncode==0 and not decoded.stderr
        check=pipe.load(output.parent/'duration-check.json');assert check['passed']
        record=dict(configuration=label,anchors=count,fps=fps,resolution='160x90',duration_ms=cursor,pure_frame_budget=sum(budget),
                    actual_decoded_frames=actual,frame_counts=budget,max_packet_pts_error_seconds=max_pts_error,ffprobe_exit=0,full_decode_exit=decoded.returncode,decode_stderr_bytes=len(decoded.stderr),
                    duration_check=check,output=str(output),sha256=sha256(output.read_bytes()).hexdigest(),status='PASS',
                    output_1080p_stress='NOT_RUN',input_fps=[15,60],input_resolutions=['160x120','320x180','192x108'],policies=['ERROR/trim','HOLD_LAST_FRAME','LOOP','FIT','CROP'])
        records.append(record);(root/'matrix-results.json').write_text(json.dumps(records,indent=2)+'\n')
        (folder/'ffprobe.json').write_bytes(result.stdout)
        print('PASS',label,actual,'frames',flush=True)
    return records


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();matrix(args.output)
