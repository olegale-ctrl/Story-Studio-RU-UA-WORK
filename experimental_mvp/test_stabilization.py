"""MVP-07.1 minimal reproducers and regression oracles, local fixtures only."""
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from experimental_mvp import pipeline as pipe, timeline as timeline
from experimental_mvp.test_timeline import project,audio


class DefectReproducers(unittest.TestCase):
    def test_confirmed_conflict_draft_never_keeps_approved_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=project();p['timeline']={'version':1};p['scenes'][0]['anchors'][1]['start_ms']=500
            e=timeline.Editor(p,timeline.timing_map(p,whole_ms=2000));path=Path(tmp)/'draft.json'
            e.save(path,allow_conflicts=True)
            self.assertFalse(pipe.load(path)['approved'])

    def test_close_failure_removes_temporary_file_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'project.json';pipe.save(path,{'topic':'old'});old=path.read_bytes()
            factory=tempfile.NamedTemporaryFile
            class CloseFailure:
                def __init__(self,*a,**k):self.stream=factory(*a,**k)
                def __enter__(self):return self.stream.__enter__()
                def __exit__(self,*a):
                    self.stream.__exit__(*a);raise OSError('injected close failure')
            with patch('experimental_mvp.pipeline.tempfile.NamedTemporaryFile',CloseFailure):
                with self.assertRaises(OSError):pipe.save(path,{'topic':'changed'})
            self.assertEqual(path.read_bytes(),old)
            self.assertEqual({f.name for f in root.iterdir()},{'project.json'})

    def test_readback_validation_rejects_silent_valid_json_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'project.json';pipe.save(path,{'topic':'old'});old=path.read_bytes();factory=tempfile.NamedTemporaryFile
            class CorruptWrite:
                def __init__(self,*a,**k):self.stream=factory(*a,**k)
                def __enter__(self):self.stream.__enter__();return self
                def __exit__(self,*a):return self.stream.__exit__(*a)
                def __getattr__(self,name):return getattr(self.stream,name)
                def write(self,value):return self.stream.write(value.replace('"changed"','"corrupt"'))
            with patch('experimental_mvp.pipeline.tempfile.NamedTemporaryFile',CorruptWrite):
                with self.assertRaises(ValueError):pipe.save(path,{'topic':'changed'})
            self.assertEqual(path.read_bytes(),old)
            self.assertEqual({f.name for f in root.iterdir()},{'project.json'})

    def test_cancel_after_scene_render_removes_only_this_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);audio(root/'a.wav');p=project();p.update(audio=str(root/'a.wav'),timeline={'version':1},output_profile={'width':320,'height':180,'fps':24})
            untouched=root/'timeline-preview-user-file';untouched.mkdir();(untouched/'keep').write_text('keep')
            stop=threading.Event();original=pipe.render_scene;snapshot=deepcopy(p)
            def stop_after(*args,**kwargs):
                value=original(*args,**kwargs);stop.set();return value
            with patch('experimental_mvp.pipeline.render_scene',side_effect=stop_after):
                with self.assertRaises(pipe.BuildStopped):timeline.preview(p,timeline.measure_audio(p,root),root,scene_id=p['scenes'][0]['id'],cancelled=stop.is_set)
            self.assertEqual(p,snapshot)
            self.assertEqual([f.name for f in root.glob('timeline-preview-*')],['timeline-preview-user-file'])


@unittest.skipUnless(os.name=='nt' or os.environ.get('DISPLAY'),'Tk display unavailable')
class CancelRaceReproducer(unittest.TestCase):
    def test_cancel_queued_success_before_poll_never_opens_or_retains_result(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        root=tk.Tk()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);audio(folder/'a.wav');p=project();p['audio']=str(folder/'a.wav');opened=[]
                panel=TimelinePanel(root,lambda:deepcopy(p),lambda _:None,lambda:folder,opened.append);panel.pack();root.update();panel.refresh()
                artifact=folder/('timeline-preview-'+'a'*12);artifact.mkdir();video=artifact/'preview.mp4';video.write_bytes(b'owned mock result')
                with patch('experimental_mvp.timeline.preview',return_value=video):
                    panel.make_preview('project');end=time.monotonic()+2
                    while panel.events.empty() and time.monotonic()<end:time.sleep(.005)
                panel.stop.set();panel.poll()
                self.assertFalse(opened);self.assertIsNone(panel.last_preview);self.assertFalse(artifact.exists());panel.destroy()
        finally:root.destroy()




class SaveAndDraftRegressionTests(unittest.TestCase):
    def test_save_failures_at_write_flush_fsync_and_replace_are_atomic(self):
        with tempfile.TemporaryDirectory(prefix='Збереження з пробілом-') as tmp:
            root=Path(tmp);target=root/'проект.json';pipe.save(target,{'topic':'old'});old=target.read_bytes()
            for point in ('write','flush','fsync','replace'):
                with self.subTest(point=point):
                    if point in ('fsync','replace'):
                        context=patch('experimental_mvp.pipeline.os.fsync' if point=='fsync' else 'pathlib.Path.replace',side_effect=PermissionError('injected '+point))
                    else:
                        factory=tempfile.NamedTemporaryFile
                        class BrokenStream:
                            def __init__(self,*a,**k):self.stream=factory(*a,**k)
                            def __enter__(self):self.stream.__enter__();return self
                            def __exit__(self,*a):return self.stream.__exit__(*a)
                            def __getattr__(self,name):return getattr(self.stream,name)
                            def write(self,value):
                                if point=='write':raise OSError('injected write')
                                return self.stream.write(value)
                            def flush(self):raise OSError('injected flush')
                        context=patch('experimental_mvp.pipeline.tempfile.NamedTemporaryFile',BrokenStream)
                    with context:
                        with self.assertRaises(OSError):pipe.save(target,{'topic':'changed'})
                    self.assertEqual(target.read_bytes(),old);self.assertEqual(pipe.load(target),{'topic':'old'})
                    self.assertEqual({p.name for p in root.iterdir()},{'проект.json'})

    def test_explicit_newline_policy_survives_windows_translation_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'Unicode проєкт.json';factory=tempfile.NamedTemporaryFile
            class WindowsTextTranslation:
                def __init__(self,*a,**k):
                    self.translate=k.get('newline')!='';self.stream=factory(*a,**k)
                def __enter__(self):self.stream.__enter__();return self
                def __exit__(self,*a):return self.stream.__exit__(*a)
                def __getattr__(self,name):return getattr(self.stream,name)
                def write(self,value):
                    return self.stream.write(value.replace('\n','\r\n') if self.translate else value)
            with patch('experimental_mvp.pipeline.tempfile.NamedTemporaryFile',WindowsTextTranslation):
                pipe.save(target,{'topic':'Київ / русский'})
            self.assertEqual(pipe.load(target),{'topic':'Київ / русский'})
            self.assertNotIn(b'\r\n',target.read_bytes())

    @unittest.skipIf(os.name=='nt' or getattr(os,'geteuid',lambda:0)()==0,'POSIX non-root permission oracle only')
    def test_actual_unwritable_directory_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'old.json';pipe.save(path,{'a':1});old=path.read_bytes();root.chmod(0o500)
            try:
                with self.assertRaises(PermissionError):pipe.save(path,{'a':2})
                self.assertEqual(path.read_bytes(),old)
            finally:root.chmod(0o700)

    def test_semantic_drafts_reopen_but_export_fails_before_final(self):
        from experimental_mvp import storyboard as sb
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);audio(root/'a.wav');clip=root/'clip.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=blue:s=160x90:r=30','-t','1','-c:v','libx264','-threads','2',str(clip)],check=True,capture_output=True)
            for kind in ('GAP','OVERLAP','OUTSIDE_SCENE','MANUAL_MAP','MISSING','CHANGED_HASH','SOURCE_INTERVAL'):
                with self.subTest(kind=kind):
                    p=project();p.update(audio=str(root/'a.wav'),timeline={'version':1},output_profile={'width':320,'height':180,'fps':24})
                    s=p['scenes'][0];a,b=s['anchors']
                    if kind=='GAP':a['duration_ms']=500
                    elif kind=='OVERLAP':b['start_ms']=500
                    elif kind=='OUTSIDE_SCENE':b['duration_ms']=1500;b['allow_outside_scene']=True
                    elif kind=='MANUAL_MAP':p['timeline']['scene_durations_ms']={s['id']:3000}
                    elif kind=='MISSING':a['local_asset_path']=str(root/'missing.png')
                    elif kind=='CHANGED_HASH':sb.import_asset(a,clip,root);a['asset_sha256']='0'*64
                    elif kind=='SOURCE_INTERVAL':sb.import_asset(a,clip,root);a.update(source_start_ms=0,source_end_ms=9000)
                    e=timeline.Editor(p,timeline.timing_map(p if kind!='MANUAL_MAP' else {**p,'timeline':{'version':1}},whole_ms=2000))
                    file=root/(kind+'.json');e.save(file,allow_conflicts=True);reopened=pipe.load(file)
                    self.assertFalse(reopened['approved']);self.assertEqual(reopened['scenes'],p['scenes'])
                    self.assertTrue(any(not row[3] for row in pipe.check_project(reopened,root)))
                    with self.assertRaises(ValueError):pipe.build(reopened,root/(kind+'-unapproved'),lambda _:None)
                    reopened['approved']=True
                    with self.assertRaises(RuntimeError):pipe.build(reopened,root/(kind+'-forced'),lambda _:None)
                    self.assertFalse(list((root/(kind+'-forced')).glob('run-*/final.mp4')))
            bad=root/'broken.json';bad.write_text('{ malformed',encoding='utf-8')
            with self.assertRaises(json.JSONDecodeError):pipe.load(bad)

    def test_all_history_operations_preserve_ids_provenance_and_rights(self):
        from experimental_mvp.timeline_ui import content
        for operation in ('move','resize','split','merge','duplicate','delete','scene_order','caption'):
            with self.subTest(operation=operation):
                p=project();other=deepcopy(p['scenes'][0]);other['id']='b'*32
                for a in other['anchors']:a['scene_id']=other['id'];a['anchor_id']+='b'
                p['scenes'].append(other)
                for s in p['scenes']:
                    for a in s['anchors']:a.update(provenance={'fixture':'original'},license_status='UNKNOWN')
                e=timeline.Editor(p,timeline.timing_map(p,whole_ms=4000));sid=p['scenes'][0]['id'];aid=p['scenes'][0]['anchors'][0]['anchor_id']
                before=content(e.project)
                if operation=='move':e.edit('set',aid,start_ms=100)
                elif operation=='resize':e.edit('set',aid,duration_ms=900)
                elif operation=='split':e.edit('split',aid,at_ms=400)
                elif operation=='merge':e.edit('merge',aid,other_id=p['scenes'][0]['anchors'][1]['anchor_id'])
                elif operation=='duplicate':e.edit('duplicate',aid)
                elif operation=='delete':e.edit('delete',aid,confirmed=True)
                elif operation=='scene_order':e.edit('scene_order',ids=[other['id'],sid])
                else:e.edit('caption',scene_id=sid,cues=[dict(start_ms=0,end_ms=500,text='Ручные / ручні')])
                after=content(e.project);e.undo();self.assertEqual(content(e.project),before);e.redo();self.assertEqual(content(e.project),after)
                for s in e.project['scenes']:
                    for a in s['anchors']:self.assertEqual(a['provenance'],{'fixture':'original'});self.assertEqual(a['license_status'],'UNKNOWN')

    def test_audio_measurements_refresh_after_file_change_without_relabelling_estimates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'a.wav';audio(source,2);p=project();other={'id':'b'*32,'text':p['scenes'][0]['text'],'anchors':[]};p['scenes'].append(other);p['audio']=str(source)
            m=timeline.measure_audio(p,root);self.assertEqual(m['total_ms'],2000)
            self.assertTrue(all(s['boundary_kind']==timeline.ESTIMATED_SCENE_BOUNDARY for s in m['scenes']))
            audio(source,3);updated=timeline.measure_audio(p,root);self.assertEqual(updated['total_ms'],3000)
            p['timeline']={'version':1,'scene_durations_ms':{p['scenes'][0]['id']:5000}}
            snapshot=deepcopy(p)
            with self.assertRaises(ValueError):timeline.measure_audio(p,root)
            self.assertEqual(p,snapshot)


class ProcessCancellationTests(unittest.TestCase):
    def test_owned_real_ffmpeg_is_reaped_and_cancel_latency_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);stop=threading.Event();requested=[]
            def cancel():requested.append(time.monotonic());stop.set()
            timer=threading.Timer(.3,cancel);start=time.monotonic();timer.start();session=None
            try:
                with self.assertRaises(pipe.BuildStopped):
                    with pipe.preview_session(stop.is_set) as session:
                        folder=root/'owned';folder.mkdir();pipe.register_preview_folder(folder)
                        pipe.command(['ffmpeg','-nostdin','-v','error','-re','-f','lavfi','-i','color=blue:s=160x90:r=30','-t','30','-c:v','libx264','-threads','2','partial.mp4'],folder,folder/'render.log')
            finally:timer.cancel()
            elapsed=time.monotonic()-start;self.assertLess(elapsed,3)
            self.assertTrue(session['processes']);self.assertTrue(all(p['returncode'] is not None for p in session['processes']))
            self.assertFalse((root/'owned').exists());print('CANCEL_TOTAL_SECONDS',round(elapsed,4),'CANCEL_REQUEST_TO_EXIT_SECONDS',round(time.monotonic()-requested[0],4),'REAPED',len(session['processes']))

    def test_all_four_preview_scopes_cancel_during_ffmpeg_then_retry(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);audio(root/'a.wav');p=project();p.update(audio=str(root/'a.wav'),timeline={'version':1},output_profile={'width':320,'height':180,'fps':24});m=timeline.measure_audio(p,root);snapshot=deepcopy(p)
            kwargs=[{'anchor_id':p['scenes'][0]['anchors'][0]['anchor_id']},{'scene_id':p['scenes'][0]['id']},{},{'seek_ms':200}]
            original=subprocess.Popen
            for kw in kwargs:
                stop=threading.Event();timer=[];observed=[]
                def throttled(args,*a,**k):
                    args=list(args)
                    if Path(str(args[0])).name.startswith('ffmpeg') and str(args[-1]).endswith('.mp4') and '-i' in args and not timer:
                        args.insert(args.index('-i'),'-re');timer.append(threading.Timer(.2,stop.set));timer[0].start()
                    process=original(args,*a,**k);observed.append(process);return process
                with self.subTest(scope=kw):
                    with patch('experimental_mvp.pipeline.subprocess.Popen',side_effect=throttled):
                        with self.assertRaises(pipe.BuildStopped):timeline.preview(p,m,root,cancelled=stop.is_set,**kw)
                    for t in timer:t.cancel()
                    self.assertTrue(all(proc.poll() is not None for proc in observed))
                    self.assertFalse(list(root.glob('timeline-preview-*')));self.assertFalse(list(root.glob('movie-preview-*')))
                    self.assertEqual(p,snapshot)
                    result=timeline.preview(p,m,root,**kw);self.assertTrue(result.is_file())
                    pipe.discard_preview_result(result,root)

    def test_cancel_before_start_has_no_outputs_or_processes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=project();m=timeline.timing_map(p,whole_ms=2000)
            for kw in ({},{'scene_id':p['scenes'][0]['id']},{'anchor_id':p['scenes'][0]['anchors'][0]['anchor_id']},{'seek_ms':200}):
                with self.assertRaises(pipe.BuildStopped):timeline.preview(p,m,root,cancelled=lambda:True,**kw)
            self.assertFalse(list(root.iterdir()))

    def test_unrelated_files_are_never_removed_by_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);foreign=root/'user-project';foreign.mkdir();file=foreign/'preview.mp4';file.write_bytes(b'keep')
            with self.assertRaises(ValueError):pipe.discard_preview_result(file,root)
            self.assertTrue(file.exists())


@unittest.skipUnless(os.name=='nt' or os.environ.get('DISPLAY'),'Tk display unavailable')
class GuiLifecycleRegressionTests(unittest.TestCase):
    def test_overlap_save_reopen_force_refusal_repair_apply_save_export(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        root=tk.Tk()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);audio(folder/'a.wav');p=project();p.update(audio=str(folder/'a.wav'),timeline={'version':1},output_profile={'width':320,'height':180,'fps':24});state={'p':p}
                panel=TimelinePanel(root,lambda:deepcopy(state['p']),lambda p:state.update(p=p),lambda:folder,lambda _:None);panel.pack();root.update();panel.refresh()
                sid=p['scenes'][0]['id'];second=p['scenes'][0]['anchors'][1]['anchor_id'];panel.aid=second;panel.sid=sid
                panel.edit('set',start_ms=500);file=folder/'конфликтный черновик.json'
                with patch('tkinter.filedialog.asksaveasfilename',return_value=str(file)),patch('tkinter.messagebox.askyesno',return_value=True):panel.save()
                panel.destroy();state['p']=pipe.load(file)
                self.assertFalse(state['p']['approved']);self.assertTrue(timeline.coverage(state['p']['scenes'][0],2000))
                panel=TimelinePanel(root,lambda:deepcopy(state['p']),lambda p:state.update(p=p),lambda:folder,lambda _:None);panel.pack();root.update();panel.refresh();panel.sid=sid;panel.aid=second
                forced=deepcopy(state['p']);forced['approved']=True
                with self.assertRaises(RuntimeError):pipe.build(forced,folder/'blocked',lambda _:None)
                self.assertFalse(list((folder/'blocked').glob('run-*/final.mp4')))
                panel.edit('set',start_ms=1000);self.assertFalse(panel.editor.conflicts());panel.apply()
                with patch('tkinter.filedialog.asksaveasfilename',return_value=str(file)):panel.save()
                ready=pipe.load(file);self.assertFalse(ready['approved']);self.assertFalse(pipe.check_project(ready,folder))
                ready['approved']=True;output=pipe.build(ready,folder/'approved',lambda _:None);self.assertTrue(output.is_file());panel.destroy()
        finally:root.destroy()

    def test_destroy_while_preview_worker_returns_cleans_result_without_opening(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        root=tk.Tk()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);audio(folder/'a.wav');p=project();p['audio']=str(folder/'a.wav');opened=[]
                panel=TimelinePanel(root,lambda:deepcopy(p),lambda _:None,lambda:folder,opened.append);panel.pack();root.update();panel.refresh()
                artifact=folder/('timeline-preview-'+'b'*12);artifact.mkdir();video=artifact/'preview.mp4';video.write_bytes(b'owned mock')
                gate=threading.Event();returned=threading.Event()
                def waiting(*a,**k):gate.wait(2);returned.set();return video
                with patch('experimental_mvp.timeline.preview',side_effect=waiting):
                    panel.make_preview('project');panel.destroy();gate.set();end=time.monotonic()+3
                    while artifact.exists() and time.monotonic()<end:time.sleep(.01)
                self.assertTrue(returned.is_set());self.assertFalse(artifact.exists());self.assertFalse(opened);self.assertEqual(p['approved'],True)
        finally:root.destroy()


class LegacyPreviewCancellationTests(unittest.TestCase):
    def test_legacy_scene_preview_uses_same_owned_process_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);audio(root/'a.wav');p=project();p.update(audio=str(root/'a.wav'),output_profile={'width':320,'height':180,'fps':24})
            stop=threading.Event();timer=threading.Timer(.2,stop.set)
            original=pipe.subprocess.Popen;started=[]
            def slow(args,*a,**k):
                args=list(args)
                if str(args[-1]).endswith('.mp4') and not started:
                    args.insert(args.index('-i'),'-re');started.append(True);timer.start()
                return original(args,*a,**k)
            data=pipe.preview_audio(p,0,root)
            try:
                with patch('experimental_mvp.pipeline.subprocess.Popen',side_effect=slow):
                    with self.assertRaises(pipe.BuildStopped):pipe.render_preview(p,0,root,data,cancelled=stop.is_set)
            finally:timer.cancel()
            self.assertFalse(list(root.glob('preview-*')))
            output,_=pipe.render_preview(p,0,root,data);self.assertTrue(output.is_file())




class LoopTimestampRegressionTests(unittest.TestCase):
    def test_loop_stream_duration_equals_its_frame_budget_at_24fps(self):
        import subprocess
        from experimental_mvp import storyboard as sb
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);clip=root/'loop.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=s=320x180:r=60','-t','8','-c:v','libx264','-preset','ultrafast','-threads','2',str(clip)],capture_output=True,check=True)
            audio(root/'a.wav',10.034);p=project();s=p['scenes'][0];a=s['anchors'][0]
            s['anchors'][1].update(start_ms=5034,duration_ms=5000)
            sb.import_asset(a,clip,root);a.update(duration_ms=5034,source_start_ms=200,source_end_ms=900,short_clip_policy='LOOP',fit_mode='CROP')
            p.update(timeline={'version':1},audio=str(root/'a.wav'),output_profile={'width':160,'height':90,'fps':24})
            out=pipe.build(p,root,lambda _:None)
            value=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration,nb_frames','-of','json',str(out)]))['streams'][0]
            self.assertAlmostEqual(float(value['duration']),int(value['nb_frames'])/24,places=5)


@unittest.skipUnless(os.name=='nt' or os.environ.get('DISPLAY'),'Tk display unavailable')
class TimerCleanupRegressionTests(unittest.TestCase):
    def test_manual_poll_then_destroy_leaves_no_tk_after_callback(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        root=tk.Tk()
        try:
            before=set(root.tk.call('after','info'))
            panel=TimelinePanel(root,lambda:project(),lambda _:None,lambda:Path('/no-cache'),lambda _:None)
            panel.poll();panel.destroy()
            self.assertEqual(set(root.tk.call('after','info'))-before,set())
        finally:root.destroy()


if __name__=='__main__':unittest.main()
