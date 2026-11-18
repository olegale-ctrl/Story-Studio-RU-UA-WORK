"""MVP-07 pure transaction and real CPU FFmpeg oracles; no external services."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import wave
from experimental_mvp import timeline as t, storyboard as sb
from experimental_mvp.pipeline import save,load,identify,build,BuildStopped


def project(length=2000):
    p={'locale':'uk','approved':True,'scenes':[{'text':'Перевіряємо час та кадри.'}]}
    identify(p);s=p['scenes'][0];s['anchors']=sb.suggest(s,length,1000)
    for a in s['anchors']:a['fallback_mode']='PLACEHOLDER'
    return p


def audio(path,seconds=2):
    with wave.open(str(path),'wb') as f:
        f.setparams((1,2,24000,0,'NONE','not compressed'));f.writeframes(bytes(round(seconds*24000)*2))


class PureTests(unittest.TestCase):
    def editor(self):
        p=project();return t.Editor(p,t.timing_map(p,whole_ms=2000))

    def test_move_resize_ids_and_atomic_failure(self):
        e=self.editor();a=e.project['scenes'][0]['anchors'][0]['anchor_id'];before=deepcopy(e.project)
        with self.assertRaises(ValueError):e.edit('set',a,start_ms=-1)
        self.assertEqual(e.project,before);self.assertFalse(e.undo_stack)
        with self.assertRaises(ValueError):e.edit('set',a,duration_ms=3000)
        self.assertEqual(e.project,before)
        e.edit('set',a,start_ms=250,duration_ms=1200)
        self.assertEqual(e.locate(e.project,a)[1]['anchor_id'],a);self.assertFalse(e.project['approved']);self.assertTrue(e.dirty)
        e.undo();self.assertFalse(e.dirty);e.redo();self.assertTrue(e.dirty)

    def test_create_duplicate_split_merge_determinism(self):
        e=self.editor();original=e.project['scenes'][0]['anchors'][0]['anchor_id']
        a=e.edit('duplicate',original);self.assertNotEqual(a,original)
        e.undo();again=e.edit('duplicate',original);self.assertEqual(a,again)
        e.undo();b=e.edit('split',original,at_ms=400)
        self.assertEqual(e.locate(e.project,original)[1]['duration_ms'],400)
        e.edit('merge',original,other_id=b);self.assertEqual(e.locate(e.project,original)[1]['duration_ms'],1000)
        created=e.edit('create',scene_id=e.project['scenes'][0]['id'],start_ms=0,duration_ms=500)
        self.assertTrue(created);self.assertFalse(e.project['approved'])

    def test_merge_incompatible_atomic_and_delete_keeps_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/'user.mp4';file.write_bytes(b'original')
            e=self.editor();a,b=e.project['scenes'][0]['anchors'];a['local_asset_path']=str(file)
            snapshot=deepcopy(e.project)
            with self.assertRaises(ValueError):e.edit('merge',a['anchor_id'],other_id=b['anchor_id'])
            self.assertEqual(snapshot,e.project)
            with self.assertRaises(ValueError):e.edit('delete',a['anchor_id'])
            e.edit('delete',a['anchor_id'],confirmed=True);self.assertTrue(file.exists());e.undo();self.assertEqual(e.project['scenes'][0]['anchors'][0]['local_asset_path'],str(file))

    def test_video_split_preserves_source_intervals_and_provenance(self):
        e=self.editor();a=e.project['scenes'][0]['anchors'][0]
        a.update(local_asset_path='clip.mp4',source_start_ms=1000,source_end_ms=2000,provenance={'source':'original'})
        b=e.edit('split',a['anchor_id'],at_ms=400)
        left=e.locate(e.project,a['anchor_id'])[1];right=e.locate(e.project,b)[1]
        self.assertEqual((left['source_start_ms'],left['source_end_ms']),(1000,1400))
        self.assertEqual((right['source_start_ms'],right['source_end_ms']),(1400,2000))
        self.assertEqual(left['provenance'],right['provenance']);e.edit('merge',a['anchor_id'],other_id=b)
        self.assertEqual(e.locate(e.project,a['anchor_id'])[1]['source_end_ms'],2000)

    def test_manual_vs_estimated_audio_and_reorder(self):
        p=project();s2=deepcopy(p['scenes'][0]);s2['id']='b'*32;s2['anchors']=[];p['scenes'].append(s2)
        sid=p['scenes'][0]['id'];p['timeline']={'version':1,'scene_durations_ms':{sid:700}}
        m=t.timing_map(p,whole_ms=2000)
        self.assertEqual([s['duration_ms'] for s in m['scenes']],[700,1300]);self.assertEqual(m['scenes'][0]['boundary_kind'],t.MANUAL_SCENE_BOUNDARY)
        self.assertEqual(m['scenes'][1]['boundary_kind'],t.ESTIMATED_SCENE_BOUNDARY)
        p['scenes'][0]['anchors']=[];p['captions_by_scene']={sid:[dict(start_ms=0,end_ms=500,text='Київ')]}
        e=t.Editor(p,m);e.edit('scene_order',ids=[s2['id'],sid]);self.assertEqual(e.timing['scenes'][1]['start_ms'],1300)
        self.assertEqual(e.project['captions_by_scene'][sid][0]['text'],'Київ')
        self.assertEqual(t.timing_map(p,scene_ms={sid:700,s2['id']:1300})['scenes'][1]['boundary_kind'],t.MEASURED_AUDIO_DURATION)

    def test_duration_change_retains_intervals_and_caption_conflicts(self):
        p=project();other={'id':'b'*32,'text':'Інша сцена для перевірки','anchors':[]};p['scenes'].append(other)
        p['captions_by_scene']={p['scenes'][0]['id']:[dict(start_ms=0,end_ms=2000,text='Ручний')]}
        e=t.Editor(p,t.timing_map(p,whole_ms=4000))
        e.edit('scene_duration',scene_id=p['scenes'][0]['id'],duration_ms=1000,keep_intervals=True)
        self.assertEqual(e.project['scenes'][0]['anchors'][1]['duration_ms'],1000)
        self.assertTrue(any(c['kind']=='CAPTION_OUTSIDE_SCENE' for c in e.conflicts()))
        e.undo();self.assertEqual(e.timing['scenes'][0]['duration_ms'],2000)

    def test_reconcile_fallback_redistribute_and_bounds(self):
        e=self.editor();s=e.project['scenes'][0];aid=s['anchors'][1]['anchor_id'];sid=s['id']
        e.edit('delete',aid,confirmed=True);e.edit('fallback',scene_id=sid)
        self.assertFalse(e.conflicts());self.assertTrue(any(a['fallback_mode']=='PLACEHOLDER' for a in e.project['scenes'][0]['anchors']))
        e.edit('set',e.project['scenes'][0]['anchors'][0]['anchor_id'],duration_ms=500)
        self.assertTrue(e.conflicts());e.edit('redistribute',scene_id=sid);self.assertFalse(e.conflicts())
        self.assertEqual(sum(a['duration_ms'] for a in e.project['scenes'][0]['anchors']),2000)

    def test_repair_one_scene_does_not_require_atomic_repair_of_all_other_scenes(self):
        p=project();other=deepcopy(p['scenes'][0]);other['id']='b'*32
        for a in other['anchors']:a['anchor_id']+='b';a['scene_id']=other['id']
        p['scenes'].append(other)
        e=t.Editor(p,t.timing_map(p,whole_ms=3000))  # Each 2000-ms scene now has 1500 ms audio.
        e.edit('trim',scene_id=p['scenes'][0]['id'])
        self.assertTrue(e.conflicts());e.edit('trim',scene_id=other['id']);self.assertFalse(e.conflicts())
        e.edit('scene_duration',scene_id=p['scenes'][0]['id'],duration_ms=1400,keep_intervals=True)
        e.edit('reset_boundaries',keep_intervals=True)
        self.assertNotIn('scene_durations_ms',e.project['timeline']);self.assertEqual(e.timing['total_ms'],3000)

    def test_legacy_roundtrip_save_failure_and_dirty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'проект з пробілом.json';p=project();save(path,p);raw=path.read_bytes()
            e=t.Editor(load(path),t.timing_map(p,whole_ms=2000));self.assertFalse(e.dirty)
            aid=e.project['scenes'][0]['anchors'][0]['anchor_id'];e.edit('set',aid,visual_description='Нова схема')
            with patch('pathlib.Path.replace',side_effect=PermissionError('denied')):
                with self.assertRaises(PermissionError):e.save(path)
            self.assertEqual(path.read_bytes(),raw);self.assertTrue(e.dirty)
            e.save(path);self.assertFalse(e.dirty);self.assertEqual(load(path)['scenes'][0]['anchors'][0]['anchor_id'],aid)
            invalid=deepcopy(e.project);invalid['scenes'][0]['anchors'][0]['duration_ms']=0
            with self.assertRaises(ValueError):save(path,invalid)
            self.assertEqual(load(path),e.project)

    def test_captions_no_automatic_replacement_and_failed_edit(self):
        e=self.editor();sid=e.project['scenes'][0]['id'];cues=[dict(start_ms=100,end_ms=700,text='Українська / русский')]
        e.edit('caption',scene_id=sid,cues=cues);before=deepcopy(e.project)
        with self.assertRaises(ValueError):e.edit('caption',scene_id=sid,cues=[dict(start_ms=0,end_ms=9000,text='bad')])
        self.assertEqual(e.project,before);e.edit('redistribute',scene_id=sid);self.assertEqual(e.project['captions_by_scene'][sid],cues)


class RenderTests(unittest.TestCase):
    def test_many_mixed_anchors_fps_short_policy_duration_and_decode(self):
        with tempfile.TemporaryDirectory(prefix='Монтаж з пробілами-') as tmp:
            root=Path(tmp);audio(root/'a.wav',3.113);p=project();p['audio']=str(root/'a.wav')
            p['timeline']={'version':1};p['output_profile']={'width':320,'height':180,'fps':24}
            s=p['scenes'][0];s['anchors']=sb.suggest({'id':s['id'],'text':s['text']},3113,109)
            clip=root/'короткий.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=s=160x120:r=15','-t','0.3','-c:v','libx264','-threads','2',str(clip)],check=True,capture_output=True)
            a=s['anchors'][0];sb.import_asset(a,clip,root);a.update(duration_ms=400)
            # Explicitly redistribute all following intervals to avoid overlap.
            s['anchors']=s['anchors'][:1]+sb.suggest({'id':s['id'],'text':'Кадри'},2713,109)
            for b in s['anchors'][1:]:b['start_ms']+=400;b['fallback_mode']='PLACEHOLDER'
            before=deepcopy(p)
            with self.assertRaises(RuntimeError):build(p,root,lambda _:None)
            self.assertEqual(p,before)
            a['short_clip_policy']='HOLD_LAST_FRAME';p['scenes'][0]['anchors'][0]=a
            p['captions_by_scene']={s['id']:[dict(start_ms=0,end_ms=1000,text='Ручний титр')]}
            result=build(p,root,lambda _:None)
            data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(result)]))
            self.assertLess(abs(float(data['format']['duration'])-3.113),.1)
            self.assertEqual([v['codec_name'] for v in data['streams']],['h264','aac','mov_text'])
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(result),'-f','null','-'],check=True,capture_output=True)
            self.assertTrue(load(result.parent/'duration-check.json')['passed'])
            self.assertEqual(p['approved'],True)
            a['short_clip_policy']='LOOP';spec=sb.video_spec(a);self.assertEqual(spec['policy'],'LOOP')

    def test_probe_long_trim_corrupt_missing_and_explicit_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);clip=root/'long.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=s=320x180:r=60','-t','1','-c:v','libx264','-threads','2',str(clip)],check=True,capture_output=True)
            p=project(1000);s=p['scenes'][0];a=s['anchors'][0];sb.import_asset(a,clip,root)
            a.update(source_start_ms=200,source_end_ms=700,duration_ms=250,short_clip_policy='ERROR');self.assertEqual(sb.video_spec(a)['available_ms'],500)
            a['source_end_ms']=9000
            with self.assertRaises(ValueError):sb.video_spec(a)
            a['local_asset_path']=str(root/'missing.mp4')
            with self.assertRaises(FileNotFoundError):sb.video_spec(a)
            corrupt=root/'bad.mp4';corrupt.write_bytes(b'bad');a['local_asset_path']=str(corrupt)
            with self.assertRaises(subprocess.CalledProcessError):sb.video_spec(a)
            a.update(local_asset_path=str(clip),source_start_ms=0,source_end_ms=200,duration_ms=1000,short_clip_policy='LOOP');s['anchors']=[a]
            p.update(timeline={'version':1},audio=str(root/'a.wav'),output_profile={'width':320,'height':180,'fps':24});audio(root/'a.wav',1)
            result=build(p,root,lambda _:None);self.assertTrue(result.is_file())

    def test_png_jpeg_webp_crop_and_corrupt_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=project();audio(root/'a.wav',2);p.update(audio=str(root/'a.wav'),timeline={'version':1},output_profile={'width':320,'height':180,'fps':30})
            scene=p['scenes'][0];scene['anchors']=sb.suggest({'id':scene['id'],'text':'Зображення'},2000,500)
            for a,ext in zip(scene['anchors'],['png','jpg','webp','png']):
                source=root/('схема.'+ext)
                subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=blue:s=640x480','-frames:v','1','-threads','1',str(source)],check=True,capture_output=True)
                sb.import_asset(a,source,root);a.update(generation_mode='IMAGE_PAN_ZOOM',fit_mode='CROP')
            out=build(p,root,lambda _:None)
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True,capture_output=True)
            broken=root/'bad.png';broken.write_bytes(b'not an image');a=scene['anchors'][0];a['local_asset_path']=str(broken);a.pop('asset_sha256')
            with self.assertRaises(RuntimeError):build(p,root,lambda _:None)

    def test_subtitle_container_duration_cannot_hide_short_video(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);audio(root/'a.wav');p=project();p['scenes'][0].pop('anchors')
            p.update(timeline={'version':1},audio=str(root/'a.wav'),output_profile={'width':320,'height':180,'fps':24})
            from experimental_mvp.pipeline import render_scene
            def truncated(scene,index,length,folder,log,ffmpeg,profile=None,cancelled=lambda:False):
                return render_scene(scene,index,.5,folder,log,ffmpeg,{**profile,'frame_count':12},cancelled)
            with patch('experimental_mvp.pipeline.render_scene',side_effect=truncated):
                with self.assertRaisesRegex(RuntimeError,'Длительность/кадры'):
                    build(p,root,lambda _:None)
            run=next(root.glob('run-*'));check=load(run/'duration-check.json')
            self.assertFalse(check['passed']);self.assertFalse((run/'final.mp4').exists())
            self.assertEqual(load(run/'result.json')['status'],'error')

    def test_preview_cancel_nonmutating_and_measured_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);audio(root/'a.wav');p=project();p['audio']=str(root/'a.wav');p['timeline']={'version':1}
            p['output_profile']={'width':320,'height':180,'fps':24};m=t.measure_audio(p,root);snapshot=deepcopy(p)
            with self.assertRaises(BuildStopped):t.preview(p,m,root,cancelled=lambda:True)
            self.assertEqual(p,snapshot)
            out=t.preview(p,m,root,anchor_id=p['scenes'][0]['anchors'][0]['anchor_id'])
            self.assertTrue(out.is_file());self.assertEqual(p,snapshot)
            out=t.preview(p,m,root,seek_ms=500);self.assertTrue(out.is_file());self.assertEqual(p,snapshot)
            p.pop('audio');p['scenes'][0]['audio']=str(root/'a.wav')
            self.assertEqual(t.measure_audio(p,root)['scenes'][0]['boundary_kind'],t.MEASURED_AUDIO_DURATION)
            from experimental_mvp.pipeline import scene_audio,executable
            scene_audio(p,p['scenes'][0],root/'scene-audio',executable('ffmpeg'),executable('ffprobe'),lambda _:None)
            p['scenes'][0].pop('audio')
            # Cached synthesis key differs from imported-audio key, so use the resolved cache fixture explicitly.
            p['scenes'][0]['voice']='uk-UA-PolinaNeural'
            from experimental_mvp.pipeline import audio_key
            _,entry=audio_key(p,p['scenes'][0],root/'scene-audio');entry.mkdir(parents=True,exist_ok=True);audio(entry/'audio.wav')
            self.assertEqual(t.measure_audio(p,root)['total_ms'],2000)


if __name__=='__main__':unittest.main()
