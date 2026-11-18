"""Offline integration oracles for the experimental workbench; no real accounts are used."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
import wave

from experimental_mvp import intelligence as llm, media_hub as hub, storyboard as sb
from experimental_mvp.pipeline import (build, check_project, load, save, identify,
                                       preview_signature, render_preview, preview_audio)


def draft():
    return dict(editorial_assessment='Нужны проверяемые источники', audience='Зрители', hooks=['Вопрос?'],
                structure=['Вопрос', 'Вывод'], script='Непроверенный черновик',
                scenes=[dict(text='Текст', visual='Карта', prompt='Схема')],
                claims_to_verify=['Проверить число'], visual_recommendations=['Схема'], risks=['Нет источника'])


def project():
    p = {'locale': 'ru', 'topic': 'Проверка', 'scenes': [{'text': 'Ручной сценарий'}]}
    identify(p)
    p['scenes'][0]['anchors'] = sb.suggest(p['scenes'][0], 2000, 1000)
    return p


def wav(path, seconds=2):
    with wave.open(str(path), 'wb') as stream:
        stream.setparams((1, 2, 24000, 0, 'NONE', 'not compressed'))
        stream.writeframes(bytes(round(seconds*24000)*2))


class StoryboardTests(unittest.TestCase):
    def test_roundtrip_script_edit_reorder_preserve_ids_and_assets(self):
        with tempfile.TemporaryDirectory(prefix='якоря-') as tmp:
            root = Path(tmp)
            p = project(); scene = p['scenes'][0]
            asset = root/'материал.bmp'
            asset.write_bytes(bytes.fromhex('424d3a000000000000003600000028000000010000000100000001001800000000000004000000000000000000000000000000000000000000ff00'))
            original = sb.import_asset(scene['anchors'][0], asset, root)
            a = deepcopy(scene['anchors'][0]); other_id=scene['anchors'][1]['anchor_id']
            sb.reorder(scene, a['anchor_id'], 1)
            scene['text'] = 'Текст изменён; материал сохранён'
            p['scenes'].append({'id':'b'*32,'text':'Вторая'})
            p['scenes'].reverse()
            save(root/'проект.json', p)
            again=load(root/'проект.json')['scenes'][1]
            self.assertEqual(again['anchors'][1]['anchor_id'],a['anchor_id'])
            self.assertEqual(again['anchors'][0]['anchor_id'],other_id)
            self.assertEqual(again['anchors'][1]['local_asset_path'],str(original))
            self.assertEqual(sha256(original.read_bytes()).hexdigest(),a['asset_sha256'])
            with self.assertRaises(ValueError): sb.suggest(again,2000)

    def test_explicit_coverage_fallback_modes_and_invalid_times(self):
        p=project(); scene=p['scenes'][0]
        self.assertTrue(any('fallback' in e for e in sb.validate(scene,2000)))
        for a in scene['anchors']:a['fallback_mode']='PLACEHOLDER'
        self.assertEqual(sb.validate(scene,2000),[])
        scene['anchors'][1]['start_ms']=1500
        self.assertTrue(any('пробел' in e for e in sb.validate(scene,2000)))
        scene['anchors'][1]['start_ms']=500
        self.assertTrue(sb.validate(scene,2000))
        scene['anchors'][1]['duration_ms']=True
        self.assertTrue(sb.validate(scene,2000))
        scene['anchors'][0]['scene_id']='other'
        self.assertTrue(any('чужая' in e for e in sb.validate(scene,2000)))
        with self.assertRaises(ValueError):sb.output_profile({'width':321})

    def test_material_reuse_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'clip.mp4';source.write_bytes(b'fixture-not-decoded-here')
            p=project();a,b=p['scenes'][0]['anchors']
            first=sb.import_asset(a,source,root)
            self.assertEqual(sb.import_asset(b,source,root),first)
            self.assertEqual(len(list((root/'assets').iterdir())),1)
            self.assertEqual(hub.plan(p)['reused_assets'],2)
            a['video_prompt']='Изменённый промпт'
            self.assertIn('промпт изменён',hub.plan(p)['jobs'][0]['reason'])
            before=preview_signature(p)
            first.write_bytes(b'tampered-longer')
            self.assertNotEqual(before,preview_signature(p))
            self.assertTrue(any('изменился' in e for e in sb.validate(p['scenes'][0],2000)))
            self.assertEqual(hub.plan(p)['jobs'][0]['status'],'FAILED')
            with self.assertRaises(FileNotFoundError):sb.import_asset(a,root/'missing.mp4',root)

    def test_explicit_split_preserves_asset_and_offsets(self):
        p=project();scene=p['scenes'][0];a=scene['anchors'][0]
        a.update(duration_ms=2500, local_asset_path='/manual/original.mp4')
        key=a['anchor_id'];parts=sb.split(scene,key,1000)
        self.assertEqual([x['duration_ms'] for x in parts],[1000,1000,500])
        self.assertEqual([x['source_start_ms'] for x in parts],[0,1000,2000])
        self.assertEqual(parts[0]['anchor_id'],key)
        self.assertEqual(len({x['anchor_id'] for x in parts}),3)
        self.assertTrue(all(x['local_asset_path']=='/manual/original.mp4' for x in parts))

    def test_anchor_counts_are_guidance_not_provider_limits(self):
        scene={'id':'a','text':'x'}
        self.assertEqual(len(sb.suggest(scene,180000,7000)),26)
        self.assertEqual(len(sb.suggest(scene,300000,7000)),43)
        self.assertEqual(len(sb.suggest(scene,300000,300000)),1)


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.p=project()
        for a in self.p['scenes'][0]['anchors']:
            a.update(generation_mode='AI_VIDEO',preferred_provider='sample')
        self.providers=[dict(id='sample',kinds=['video'],video_durations_seconds=[1])]
        self.now=datetime(2026,11,18,tzinfo=timezone.utc)

    def test_offline_no_account_login_refusal_unknown_and_exhausted(self):
        self.assertEqual(hub.plan(self.p,self.providers,self.now)['jobs'][0]['status'],'WAITING_FOR_USER')
        self.p['media_accounts']={'sample':{'login_reported':False}}
        self.assertEqual(hub.plan(self.p,self.providers,self.now)['ready_clips'],0)
        account=self.p['media_accounts']['sample'];account['login_reported']=True
        self.assertEqual(hub.plan(self.p,self.providers,self.now)['jobs'][0]['status'],'WAITING_FOR_QUOTA')
        account.update(balance=1,cost_per_clip=1,unit='credits',source='User account observation',
                       confirmed_at=self.now.isoformat(),valid_until=(self.now+timedelta(days=7)).isoformat())
        result=hub.plan(self.p,self.providers,self.now)
        self.assertEqual([j['status'] for j in result['jobs']],['READY','WAITING_FOR_QUOTA'])
        self.assertEqual(account['balance'],1)  # Planning is not spending.
        self.assertEqual(hub.plan(self.p,self.providers,self.now),result)
        account['reset_at']=(self.now+timedelta(days=2)).isoformat()
        self.assertEqual(hub.plan(self.p,self.providers,self.now+timedelta(days=3))['ready_clips'],0)
        account['balance']=float('nan')
        self.assertIsNone(hub.quota(account,self.now))

    def test_duration_provider_unavailable_and_no_catalog_balance(self):
        self.assertEqual(hub.plan(self.p,[],self.now)['ready_clips'],0)
        self.p['media_accounts']={'sample':dict(login_reported=True,durations_seconds=[5])}
        self.assertIn('Длительность',hub.plan(self.p,self.providers,self.now)['jobs'][0]['reason'])
        for p in hub.catalog():
            self.assertFalse(p['quota_is_account_balance'])
            self.assertEqual(p['app_integration'],'MANUAL_BROWSER_IMPORT_ONLY')
        self.assertEqual(len(hub.catalog()),13)


class IntelligenceTests(unittest.TestCase):
    def test_manual_edit_apply_and_no_asset_loss(self):
        value=llm.validate_draft(draft(),'uk')
        self.assertFalse(value['approved']);self.assertEqual(value['fact_status'],'UNVERIFIED')
        p=llm.apply_draft({'locale':'uk','scenes':[]},value)
        self.assertEqual(p['locale'],'uk');self.assertTrue(p['scenes'][0]['id'])
        with self.assertRaises(ValueError):llm.apply_draft(project(),value)
        with self.assertRaises(ValueError):llm.validate_draft({},'ru')
        with self.assertRaises(ValueError):llm.generate('topic','ru','https://example.invalid/v1','model')
        with self.assertRaises(ValueError):llm.generate('topic','ru','http://example.invalid/v1','m',confirmed=True)
        with self.assertRaises(ValueError):llm.generate('topic','ru','https://user:secret@example.invalid','m',confirmed=True)

    def test_real_http_compatible_mock_and_invalid_provider_response(self):
        class Handler(BaseHTTPRequestHandler):
            payload=draft()
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                self.server.received=(self.path,body)
                result={'choices':[{'message':{'content':json.dumps(self.payload)}}]}
                self.send_response(200);self.end_headers();self.wfile.write(json.dumps(result).encode())
            def log_message(self,*_):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        endpoint=f'http://127.0.0.1:{server.server_port}/v1'
        try:
            value=llm.generate('Почему проверять источники?','ru',endpoint,'mock',confirmed=True)
            self.assertEqual(value['fact_status'],'UNVERIFIED')
            applied=llm.apply_draft({'locale':'ru','scenes':[]},value)
            self.assertEqual(applied['editorial_draft']['provenance']['model'],'mock')
            self.assertEqual(applied['editorial_draft']['provenance']['topic_sha256'],sha256('Почему проверять источники?'.encode()).hexdigest())
            self.assertEqual(server.received[0],'/v1/chat/completions')
            self.assertEqual(server.received[1]['model'],'mock')
            Handler.payload={'wrong':True}
            with self.assertRaises(ValueError):llm.generate('topic','ru',endpoint,'mock',confirmed=True)
        finally:server.shutdown();server.server_close();worker.join()
        with self.assertRaises(ValueError):llm.generate('topic','ru',endpoint,'mock',confirmed=True,timeout=1)


class MediaIntegrationTests(unittest.TestCase):
    def test_different_fps_resolution_short_clips_cyrillic_mp3_and_full_decode(self):
        with tempfile.TemporaryDirectory(prefix='Студія-') as tmp:
            root=Path(tmp);p=project();p['approved']=True
            p['output_profile']={'width':320,'height':180,'fps':24}
            wav(root/'голос.wav')
            subprocess.run(['ffmpeg','-v','error','-i',str(root/'голос.wav'),str(root/'голос.mp3')],check=True)
            p['audio']=str(root/'голос.mp3')
            for i,(a,fps,size,seconds) in enumerate(zip(p['scenes'][0]['anchors'],[15,60],['160x120','640x360'],[0.3,1.5])):
                source=root/f'Кадр {i}.mp4'
                subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'testsrc2=s={size}:r={fps}',
                                '-t',str(seconds),'-c:v','libx264','-threads','2',str(source)],check=True)
                sb.import_asset(a,source,root)
                a['generation_mode']='LOCAL_VIDEO'
            # MP3 duration includes encoder delay: match the actual measured audio span.
            from experimental_mvp.pipeline import duration, executable
            total=duration(root/'голос.mp3',executable('ffprobe'))
            p['scenes'][0]['anchors'][-1]['duration_ms']=total-1000
            self.assertFalse(check_project(p,root))
            p['captions_by_scene']={p['scenes'][0]['id']:[dict(start_ms=0,end_ms=1000,text='Ручний підпис')]}
            output=build(p,root,lambda _:None)
            probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)],capture_output=True,check=True)
            data=json.loads(probe.stdout)
            self.assertEqual([s['codec_name'] for s in data['streams']],['h264','aac','mov_text'])
            self.assertEqual(data['streams'][0]['width'],320)
            self.assertEqual(data['streams'][0]['r_frame_rate'],'24/1')
            self.assertAlmostEqual(float(data['format']['duration']),total/1000,delta=.15)
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,capture_output=True)
            evidence=load(output.parent/'execution-evidence.json')
            self.assertEqual(evidence['output_sha256'],sha256(output.read_bytes()).hexdigest())
            self.assertFalse(evidence['production_permissions'])
            preview,_=render_preview(p,0,root,preview_audio(p,0,root))
            self.assertTrue(preview.is_file())

    def test_native_text_animation_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=project();wav(root/'a.wav');p['audio']=str(root/'a.wav');p['approved']=True
            p['output_profile']={'width':320,'height':180,'fps':24}
            for a in p['scenes'][0]['anchors']:
                a.update(generation_mode='TEXT_ANIMATION',visual_description='Источник → контекст → решение')
            self.assertFalse(check_project(p,root))
            self.assertTrue(build(p,root,lambda _:None).is_file())

    def test_gap_rejected_and_explicit_fallback_can_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=project();wav(root/'a.wav');p['audio']=str(root/'a.wav');p['approved']=True
            p['output_profile']={'width':320,'height':180,'fps':24}
            self.assertTrue(any(i[1]=='anchors' for i in check_project(p,root)))
            with self.assertRaises(RuntimeError):build(p,root,lambda _:None)
            for a in p['scenes'][0]['anchors']:a['fallback_mode']='PLACEHOLDER'
            self.assertTrue(build(p,root,lambda _:None).is_file())
            p['scenes'][0]['anchors'][1]['start_ms']=1100
            with self.assertRaises(RuntimeError):build(p,root,lambda _:None)


if __name__=='__main__':unittest.main()
