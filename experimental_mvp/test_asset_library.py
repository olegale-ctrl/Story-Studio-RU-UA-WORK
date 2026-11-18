"""Local synthetic fixtures, fault injection, revision and recovery acceptance oracles."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import fields
import errno
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from experimental_mvp.asset_library import AssetLibrary, LibraryError, anchor_token, encoded, resolve_anchor
from experimental_mvp import storyboard, timeline


def cleared():
    return dict(rights_status='CLEARED_FOR_EXPERIMENT', license_reference='self-authored synthetic fixture',
                commercial_use=False, attribution_required=False, territory='LOCAL_EXPERIMENT_ONLY',
                expiration='NOT_APPLICABLE', watermark_status='NONE', review_reference='fixture-review')


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(); cls.fixtures=Path(cls.fixture.name)
        cls.png=cls.fixtures/'схема с пробелами.png'
        cls.mp4=cls.fixtures/'клип с пробелами.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=80x60','-frames:v','1','-threads','1',str(cls.png)],check=True)
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=red:s=160x90:r=24','-f','lavfi','-i','sine=frequency=220:sample_rate=24000',
                        '-t','1','-c:v','libx264','-threads','1','-pix_fmt','yuv420p','-c:a','aac',str(cls.mp4)],check=True)

    @classmethod
    def tearDownClass(cls):cls.fixture.cleanup()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.lib=AssetLibrary(self.root/'lib')

    def imported(self,source=None,**kw):return self.lib.import_file(source or self.png,rights=kw.pop('rights',cleared()),**kw)

    def project(self):
        a=dict(anchor_id='a'*32,scene_id='b'*32,start_ms=0,duration_ms=1000,generation_mode='LOCAL_VIDEO',
               generation_status='PLANNED',fallback_mode='PLACEHOLDER',local_asset_path='',license_status='UNKNOWN')
        return dict(topic='Synthetic test',locale='ru',approved=False,scenes=[dict(id='b'*32,text='test',anchors=[a])])

    def attached(self,source=None):
        r=self.imported(source);p=self.project();a=p['scenes'][0]['anchors'][0]
        self.lib.attach(p,'project-local',a['anchor_id'],r['asset_id'],1,expected_anchor=anchor_token(a))
        return r,p,a

    def assert_code(self,code,fn):
        with self.assertRaises(LibraryError) as cm:fn()
        self.assertEqual(cm.exception.code,code)

    def test_interrupted_schema_initialization_rolls_back_all_tables(self):
        factory=sqlite3.connect;folder=self.root/'init-failure'
        class InitFailure:
            def __init__(self,*args,**kwargs):object.__setattr__(self,'db',factory(*args,**kwargs))
            def __setattr__(self,k,v):setattr(self.db,k,v)
            def __getattr__(self,k):return getattr(self.db,k)
            def executescript(self,script):
                self.db.executescript('BEGIN IMMEDIATE;CREATE TABLE assets(id TEXT PRIMARY KEY);')
                raise sqlite3.OperationalError('injected initialization failure')
        with patch('experimental_mvp.asset_library.sqlite3.connect',InitFailure):
            with self.assertRaises(sqlite3.OperationalError):AssetLibrary(folder)
        with sqlite3.connect(folder/'catalog.sqlite3') as db:
            self.assertEqual(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),[])
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],0)
        self.assertEqual(AssetLibrary(folder).search(),[])

    def test_unknown_schema_version_never_downgraded(self):
        with self.lib.connection(write=True) as db:db.execute('PRAGMA user_version=2')
        self.assert_code('SCHEMA_VERSION',lambda:AssetLibrary(self.lib.root))
        with self.lib.connection() as db:self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],2)

    def test_image_unicode_spaces_bytes_metadata(self):
        r=self.imported();p=self.lib.managed(r['storage_reference'])
        self.assertEqual(p.read_bytes(),self.png.read_bytes());self.assertEqual(r['sha256'],sha256(self.png.read_bytes()).hexdigest())
        self.assertEqual((r['technical']['width'],r['technical']['height']),(80,60));self.assertEqual(r['technical']['duration'],'UNKNOWN')
        self.assertEqual(r['provenance']['source_sha256'],r['sha256']);self.assertEqual(r['original_filename'],self.png.name);self.assertEqual(r['lifecycle_status'],'ACTIVE')

    def test_video_probe_decode_and_audio(self):
        r=self.imported(self.mp4);t=r['technical']
        self.assertEqual(t['video_codec'],'h264');self.assertEqual(t['duration'],1)
        self.assertEqual(t['frame_rate'],'24');self.assertEqual(t['audio_streams'][0]['codec_name'],'aac')

    def test_invalid_image_and_video_leave_no_active_or_staging(self):
        for suffix in ('.png','.mp4'):
            with self.subTest(suffix=suffix):
                f=self.root/('bad'+suffix);f.write_bytes(b'not media')
                with self.assertRaises(LibraryError):self.lib.import_file(f)
                self.assertEqual(self.lib.search(),[]);self.assertEqual(list((self.lib.root/'staging').iterdir()),[])

    def test_empty_oversized_unsupported(self):
        for suffix,data,limit,code in [('.png',b'',100,'SIZE_LIMIT'),('.png',b'x'*20,10,'SIZE_LIMIT'),('.svg',b'<svg/>',100,'UNSUPPORTED_FORMAT')]:
            with self.subTest(code=code):
                f=self.root/('input'+suffix);f.write_bytes(data);lib=AssetLibrary(self.lib.root,max_bytes=limit)
                self.assert_code(code,lambda:lib.import_file(f))

    def test_dedupe_content_independent_provenance_rights(self):
        a=self.imported(provenance={'source_type':'MANUAL','provider':'one'})
        b=self.imported(provenance={'source_type':'AI_GENERATED','provider':'two'},rights={'rights_status':'REJECTED'})
        self.assertNotEqual(a['asset_id'],b['asset_id']);self.assertEqual(a['storage_reference'],b['storage_reference'])
        self.assertEqual(len(list((self.lib.root/'objects').iterdir())),1)
        self.assertEqual(a['rights']['rights_status'],'CLEARED_FOR_EXPERIMENT');self.assertEqual(b['rights']['rights_status'],'REJECTED')
        self.lib.retire(a['asset_id']);self.assertTrue(self.lib.managed(b['storage_reference']).is_file())

    def test_missing_original_persists_after_restart(self):
        r=self.imported();self.lib.managed(r['storage_reference']).unlink()
        result=AssetLibrary(self.lib.root).verify_asset(r['asset_id'])
        self.assertEqual(result['lifecycle_status'],'MISSING');self.assertEqual(len(self.lib.list_missing_assets()),1)
        self.assertEqual(self.lib.list_corrupted_assets(),[])

    def test_corrupted_same_size_original(self):
        r=self.imported();p=self.lib.managed(r['storage_reference']);data=p.read_bytes();p.write_bytes(b'x'+data[1:])
        self.assertEqual(self.lib.verify_asset(r['asset_id'])['lifecycle_status'],'CORRUPTED')
        self.assertEqual(len(self.lib.list_corrupted_assets()),1)
        self.assert_code('OBJECT_CORRUPTED',lambda:self.imported())
        self.assertEqual(p.read_bytes(),b'x'+data[1:])

    def test_metadata_revisions_pin_and_compare(self):
        r=self.imported();new=self.lib.update_metadata(r['asset_id'],expected_revision=1,tags=['new'])
        self.assertEqual(new['revision'],2);self.assertEqual(self.lib.get(r['asset_id'],1)['tags'],[])
        self.assert_code('SOURCE_HASH_MISMATCH',lambda:self.lib.update_metadata(r['asset_id'],expected_revision=2,provenance={'source_sha256':'0'*64}))
        self.assertEqual(self.lib.get(r['asset_id'])['revision'],2)
        self.assert_code('STALE_REVISION',lambda:self.lib.update_metadata(r['asset_id'],expected_revision=1,tags=[]))
        self.assert_code('ASSET_REVISION_CHANGED',lambda:self.lib.resolve(r['asset_id'],1))

    def test_unknown_rights_not_clearance(self):
        r=self.lib.import_file(self.png)
        self.assertEqual(r['rights']['rights_status'],'UNKNOWN')
        self.assert_code('RIGHTS_NOT_CLEARED',lambda:self.lib.resolve(r['asset_id'],1))
        self.assert_code('PRODUCTION_NOT_AUTHORIZED',lambda:self.lib.resolve(r['asset_id'],1,action='PRODUCTION'))

    def test_rights_requires_evidence_and_applicability(self):
        for missing in ('license_reference','review_reference','commercial_use','attribution_required','expiration'):
            with self.subTest(missing=missing):
                law=cleared();law[missing]='UNKNOWN';r=self.imported(rights=law)
                self.assert_code('RIGHTS_NOT_CLEARED',lambda:self.lib.resolve(r['asset_id'],1))

    def test_expired_rights(self):
        law=cleared();law['expiration']='2000-01-01T00:00:00Z';r=self.imported(rights=law)
        self.assert_code('RIGHTS_EXPIRED',lambda:self.lib.resolve(r['asset_id'],1))

    def test_invalid_metadata_rejected_before_import(self):
        cases=[dict(provenance={'source_type':'FAKE'}),dict(provenance={'source_sha256':'bad'}),dict(rights={'rights_status':'PRODUCTION_READY'}),
               dict(rights={'commercial_use':1}),dict(rights={'expiration':'tomorrow'}),dict(provenance={'api_key':'secret'}),dict(tags=[None]),dict(rights=[]),dict(provenance=[]),dict(tags=''),dict(rights={'rights_status':[]}),dict(provenance={'source_type':{}})]
        for kw in cases:
            with self.subTest(kw=kw):self.assert_code('INVALID_METADATA',lambda:self.lib.import_file(self.png,**kw))
        self.assertEqual(self.lib.search(),[])

    def test_path_traversal_relative_and_storage(self):
        for path in (Path('relative.png'),self.root/'..'/'foo.png'):
            with self.subTest(path=path):self.assert_code('UNSAFE_PATH',lambda:self.lib.import_file(path))
        self.assert_code('UNSAFE_STORAGE_REFERENCE',lambda:self.lib.managed('../outside.png'))
        self.assert_code('UNSAFE_STORAGE_REFERENCE',lambda:self.lib.managed('/tmp/file'))

    @unittest.skipUnless(hasattr(os,'symlink'),'symlink unavailable')
    def test_symlink_source_parent_and_library(self):
        p=self.root/'link.png';p.symlink_to(self.png)
        self.assert_code('UNSAFE_PATH',lambda:self.lib.import_file(p))
        parent=self.root/'dir';parent.symlink_to(self.fixtures,target_is_directory=True)
        self.assert_code('UNSAFE_PATH',lambda:self.lib.import_file(parent/self.png.name))
        self.assert_code('UNSAFE_PATH',lambda:AssetLibrary(parent/'lib'))

    @unittest.skipUnless(os.name=='nt','WINDOWS_NOT_RUN: junction/reparse requires Windows/NTFS')
    def test_windows_junction(self):
        p=self.root/'junction'
        subprocess.run(['cmd','/c','mklink','/J',str(p),str(self.fixtures)],check=True,capture_output=True)
        self.addCleanup(lambda:os.rmdir(p))
        self.assert_code('UNSAFE_PATH',lambda:self.lib.import_file(p/self.png.name))

    def test_toctou_source_replaced_after_stat(self):
        p=self.root/'source.png';p.write_bytes(self.png.read_bytes());old=p.read_bytes()
        def swap(phase):
            if phase=='source_checked':p.unlink();p.write_bytes(old)
        self.lib.fault=swap
        self.assert_code('SOURCE_CHANGED',lambda:self.imported(p));self.assertEqual(self.lib.search(),[])

    def test_toctou_source_modified_during_copy(self):
        p=self.root/'source.png';p.write_bytes(self.png.read_bytes())
        def swap(phase):
            if phase=='copy_chunk':p.write_bytes(b'corruption')
        self.lib.fault=swap
        self.assert_code('SOURCE_CHANGED',lambda:self.imported(p));self.assertEqual(self.lib.search(),[])

    def test_staging_corruption_detected(self):
        def corrupt(phase):
            if phase=='before_validation':
                next((self.lib.root/'staging').iterdir()).write_bytes(b'corrupt')
        self.lib.fault=corrupt
        with self.assertRaises(LibraryError):self.imported()
        self.assertEqual(self.lib.search(),[])

    def test_failure_matrix_source_bytes_preserved_and_retry(self):
        phases=['copy_chunk','staging_written','before_validation','before_publication','after_publication','before_db_commit']
        for phase in phases:
            with self.subTest(phase=phase):
                lib=AssetLibrary(self.root/phase);original=self.png.read_bytes()
                def fault(p):
                    if p==phase:raise OSError(errno.ENOSPC,'injected disk/write/validation failure')
                lib.fault=fault
                with self.assertRaises(OSError):lib.import_file(self.png)
                self.assertEqual(lib.search(),[]);self.assertEqual(list((lib.root/'staging').iterdir()),[])
                self.assertEqual(self.png.read_bytes(),original)
                lib.fault=None;lib.recover_incomplete_imports();r=lib.import_file(self.png)
                self.assertEqual(lib.verify_asset(r['asset_id'])['integrity_status'],'VALID')
                self.assertEqual(len(list((lib.root/'objects').iterdir())),1)

    def test_failed_sqlite_commit_keeps_original_no_active(self):
        def fail(phase):
            if phase=='before_db_commit':raise sqlite3.OperationalError('injected transaction failure')
        self.lib.fault=fail
        with self.assertRaises(sqlite3.OperationalError):self.imported()
        self.assertEqual(self.lib.search(),[]);self.assertTrue(self.png.is_file())
        self.lib.fault=None;self.lib.recover_incomplete_imports()
        self.assertEqual(len(self.imported()['sha256']),64)

    def test_real_connection_commit_failure_rolls_back_catalog(self):
        factory=sqlite3.connect;count=[0]
        class CommitFailure:
            def __init__(self,*args,**kwargs):object.__setattr__(self,'db',factory(*args,**kwargs))
            def __setattr__(self,k,v):setattr(self.db,k,v)
            def __getattr__(self,k):return getattr(self.db,k)
            def commit(self):
                count[0]+=1
                if count[0]==2:raise sqlite3.OperationalError('injected commit failure')
                return self.db.commit()
        with patch('experimental_mvp.asset_library.sqlite3.connect',CommitFailure):
            with self.assertRaises(sqlite3.OperationalError):self.imported()
        self.assertEqual(self.lib.search(),[]);self.assertTrue(self.png.is_file())
        self.lib.recover_incomplete_imports();self.assertEqual(self.imported()['integrity_status'],'VALID')

    def test_actual_child_timeout_and_source_hash_mismatch(self):
        lib=AssetLibrary(self.lib.root,timeout=.05)
        self.assert_code('PROCESS_TIMEOUT',lambda:lib._run([sys.executable,'-c','import time;time.sleep(10)']))
        self.assert_code('SOURCE_HASH_MISMATCH',lambda:self.imported(provenance={'source_sha256':'0'*64}))
        self.assertEqual(self.lib.search(),[])

    def test_read_failure_open_source(self):
        original=os.open
        def fail(path,*a,**k):
            if Path(path)==self.png:raise PermissionError('injected read failure')
            return original(path,*a,**k)
        with patch('experimental_mvp.asset_library.os.open',side_effect=fail):
            with self.assertRaises(PermissionError):self.imported()
        self.assertEqual(self.lib.search(),[])

    def test_real_process_crash_after_publication_recovery_idempotent(self):
        code='''import os,sys
from experimental_mvp.asset_library import AssetLibrary
from pathlib import Path
lib=AssetLibrary(Path(sys.argv[1]),fault=lambda phase:os._exit(73) if phase==sys.argv[3] else None)
lib.import_file(Path(sys.argv[2]))
'''
        cp=subprocess.run([sys.executable,'-c',code,str(self.lib.root),str(self.png),'after_publication'])
        self.assertEqual(cp.returncode,73);lib=AssetLibrary(self.lib.root)
        self.assertEqual(lib.search(),[])
        first=lib.recover_incomplete_imports();second=lib.recover_incomplete_imports()
        self.assertEqual(len(first['aborted_imports']),1);self.assertEqual(second['aborted_imports'],[])
        r=lib.import_file(self.png);self.assertEqual(r['integrity_status'],'VALID')
        self.assertEqual(len(list((lib.root/'objects').iterdir())),1)

    def test_actual_process_crash_during_copy_recovers_staging(self):
        code="from experimental_mvp.asset_library import AssetLibrary;from pathlib import Path;import os,sys;AssetLibrary(Path(sys.argv[1]),fault=lambda p:os._exit(74) if p=='copy_chunk' else None).import_file(Path(sys.argv[2]))"
        cp=subprocess.run([sys.executable,'-c',code,str(self.lib.root),str(self.png)])
        self.assertEqual(cp.returncode,74);self.assertEqual(self.lib.search(),[])
        stage=list((self.lib.root/'staging').iterdir());self.assertEqual(len(stage),1);stage[0].write_bytes(b'corrupt staging')
        recovered=AssetLibrary(self.lib.root).recover_incomplete_imports()
        self.assertEqual(len(recovered['aborted_imports']),1);self.assertEqual(list((self.lib.root/'staging').iterdir()),[])
        self.assertEqual(self.lib.recover_incomplete_imports()['aborted_imports'],[])
        self.assertEqual(self.imported()['integrity_status'],'VALID')

    def test_recovery_only_managed_staging_keeps_user_file(self):
        d=self.lib.root/'staging';(d/'user-notes.txt').write_text('keep');(d/('f'*32+'.png')).write_bytes(b'corrupt')
        self.lib.recover_incomplete_imports();self.assertEqual([x.name for x in d.iterdir()],['user-notes.txt'])

    def test_concurrent_imports_share_object_independent_assets(self):
        def job(i):return AssetLibrary(self.lib.root).import_file(self.png,provenance={'provider':str(i)})
        with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(job,range(4)))
        self.assertEqual(len({r['asset_id'] for r in rows}),4)
        self.assertEqual(len({r['storage_reference'] for r in rows}),1);self.assertEqual(len(self.lib.search()),4)

    def test_tool_timeout_and_invalid_json(self):
        with patch('experimental_mvp.asset_library.subprocess.run',side_effect=subprocess.TimeoutExpired('probe',.1)):
            self.assert_code('PROCESS_TIMEOUT',lambda:self.imported())
        with patch.object(self.lib,'_run',return_value=b'{not-json'):
            self.assert_code('INVALID_TOOL_OUTPUT',lambda:self.imported())
        self.assertEqual(self.lib.search(),[])

    def test_media_dimensions_duration_and_unsafe_name(self):
        small=AssetLibrary(self.lib.root,max_pixels=10)
        self.assert_code('MEDIA_LIMIT',lambda:small.import_file(self.png))
        short=AssetLibrary(self.lib.root,max_duration=.1)
        self.assert_code('MEDIA_LIMIT',lambda:short.import_file(self.mp4))
        p=self.root/'bad\nname.png';p.write_bytes(self.png.read_bytes())
        self.assert_code('UNSAFE_FILENAME',lambda:self.lib.import_file(p))

    def test_search_all_filters_and_stable_pagination(self):
        a=self.imported(provenance={'provider':'local','model':'manual'},tags=['demo'])
        b=self.imported(rights={'rights_status':'REJECTED'})
        _,p,anchor=self.attached();binding=anchor['asset_library_binding']
        filters=[dict(asset_id=a['asset_id']),dict(media_type='image'),dict(provider='local'),dict(model='manual'),
                 dict(rights_status='CLEARED_FOR_EXPERIMENT'),dict(technical_status='VALID'),dict(sha256=a['sha256']),
                 dict(date_from='2000'),dict(date_to='9999'),dict(project_id='project-local'),dict(anchor_id=anchor['anchor_id']),dict(tag='demo')]
        for kw in filters:
            with self.subTest(kw=kw):self.assertTrue(self.lib.search(**kw))
        allids=[r['asset_id'] for r in self.lib.search()]
        self.assertEqual(allids,sorted(allids));self.assertEqual([self.lib.search(offset=i,limit=1)[0]['asset_id'] for i in range(3)],allids)
        self.assertEqual(self.lib.search(provider="' OR 1=1 --"),[])
        self.assert_code('INVALID_SEARCH',lambda:self.lib.search(limit=10000))

    def test_attach_detach_preserves_previous_and_original(self):
        r=self.imported();p=self.project();a=p['scenes'][0]['anchors'][0];old=deepcopy(a)
        self.lib.attach(p,'project',a['anchor_id'],r['asset_id'],1,expected_anchor=anchor_token(a))
        self.assertEqual(resolve_anchor(a),self.lib.managed(r['storage_reference']))
        self.lib.detach(p,a['anchor_id'],expected_anchor=anchor_token(a));self.assertEqual(a,old)
        self.assertEqual(self.lib.managed(r['storage_reference']).read_bytes(),self.png.read_bytes())

    def test_attach_duplicate_requires_explicit_replacement(self):
        r,p,a=self.attached()
        self.assert_code('EXPLICIT_REPLACE_REQUIRED',lambda:self.lib.attach(p,'p',a['anchor_id'],r['asset_id'],1,expected_anchor=anchor_token(a)))

    def test_stale_deleted_and_edited_target(self):
        r=self.imported();p=self.project();a=p['scenes'][0]['anchors'][0];old=anchor_token(a);a['duration_ms']=900
        self.assert_code('STALE_TARGET',lambda:self.lib.attach(p,'p',a['anchor_id'],r['asset_id'],1,expected_anchor=old))
        p['scenes'][0]['anchors']=[]
        self.assert_code('STALE_TARGET',lambda:self.lib.attach(p,'p','a'*32,r['asset_id'],1,expected_anchor=old))

    def test_target_edit_during_attach_no_overwrite(self):
        r=self.imported();p=self.project();a=p['scenes'][0]['anchors'][0];old=anchor_token(a)
        self.lib.fault=lambda phase:a.update(visual_description='edited') if phase=='before_attach' else None
        self.assert_code('STALE_TARGET',lambda:self.lib.attach(p,'p',a['anchor_id'],r['asset_id'],1,expected_anchor=old))
        self.assertNotIn('asset_library_binding',a);self.assertEqual(a['visual_description'],'edited')

    def test_explicit_replace_then_detach_restores_exact_previous_binding(self):
        r,p,a=self.attached();previous=deepcopy(a);other=self.imported(self.mp4)
        self.lib.attach(p,'p',a['anchor_id'],other['asset_id'],1,expected_anchor=anchor_token(a),replace=True)
        self.lib.detach(p,a['anchor_id'],expected_anchor=anchor_token(a))
        self.assertEqual(a,previous);self.assertEqual(resolve_anchor(a),self.lib.managed(r['storage_reference']))

    def test_retired_during_attach_rejected(self):
        r=self.imported();p=self.project();a=p['scenes'][0]['anchors'][0]
        self.lib.fault=lambda phase:self.lib.retire(r['asset_id']) if phase=='before_attach' else None
        self.assert_code('ASSET_UNAVAILABLE',lambda:self.lib.attach(p,'p',a['anchor_id'],r['asset_id'],1,expected_anchor=anchor_token(a)))
        self.assertNotIn('asset_library_binding',a)

    def test_unsafe_object_marks_corrupted_without_following_link(self):
        r=self.imported();p=self.lib.managed(r['storage_reference']);p.unlink();p.symlink_to(self.png)
        self.assertEqual(self.lib.verify_asset(r['asset_id'])['lifecycle_status'],'CORRUPTED')
        self.assert_code('ASSET_UNAVAILABLE',lambda:self.lib.resolve(r['asset_id'],1))

    def test_invalid_technical_state_cannot_attach(self):
        r=self.imported()
        with self.lib.connection(write=True) as db:
            value=json.loads(db.execute('SELECT data FROM revisions WHERE id=?',(r['asset_id'],)).fetchone()[0]);value['technical']['technical_status']='INVALID'
            db.execute('UPDATE revisions SET data=? WHERE id=?',(encoded(value),r['asset_id']))
        with self.assertRaises(LibraryError):self.lib.resolve(r['asset_id'],1)
        self.assertEqual(self.lib.get(r['asset_id'])['lifecycle_status'],'QUARANTINED')

    def test_binding_mismatch_no_silent_replacement(self):
        r,p,a=self.attached();a['local_asset_path']=str(self.mp4)
        self.assert_code('BINDING_MISMATCH',lambda:resolve_anchor(a))

    def test_retire_and_revoked_rights_block_existing_binding(self):
        r,p,a=self.attached()
        self.lib.update_metadata(r['asset_id'],expected_revision=1,rights={'rights_status':'REJECTED'})
        self.assert_code('ASSET_REVISION_CHANGED',lambda:resolve_anchor(a))
        self.lib.retire(r['asset_id']);self.assert_code('ASSET_UNAVAILABLE',lambda:resolve_anchor(a))

    def test_missing_and_corrupt_binding_fail_storyboard_validation(self):
        for missing in (True,False):
            with self.subTest(missing=missing):
                lib=AssetLibrary(self.root/str(missing));r=lib.import_file(self.png,rights=cleared());p=self.project();a=p['scenes'][0]['anchors'][0]
                lib.attach(p,'p',a['anchor_id'],r['asset_id'],1,expected_anchor=anchor_token(a));path=lib.managed(r['storage_reference'])
                if missing:path.unlink()
                else:path.write_bytes(b'bad')
                self.assertTrue(storyboard.validate(p['scenes'][0],1000))

    def test_17_fields_unchanged(self):self.assertEqual(len(fields(storyboard.VideoAnchor)),17)

    def test_undo_redo_and_stale_project_commit(self):
        p=self.project();e=timeline.Editor(p,timeline.timing_map(p,whole_ms=1000));before=encoded(e.project)
        candidate=deepcopy(e.project);r=self.imported();a=candidate['scenes'][0]['anchors'][0]
        self.lib.attach(candidate,'p',a['anchor_id'],r['asset_id'],1,expected_anchor=anchor_token(a))
        e.asset_change(candidate,expected_project=before);self.assertIn('asset_library_binding',e.project['scenes'][0]['anchors'][0])
        e.undo();self.assertNotIn('asset_library_binding',e.project['scenes'][0]['anchors'][0]);e.redo()
        self.assertEqual(resolve_anchor(e.project['scenes'][0]['anchors'][0]),self.lib.managed(r['storage_reference']))
        self.assert_code('STALE_TARGET',lambda:e.asset_change(p,expected_project=before))

    def test_thumbnail_regenerate_deterministic_corruption_isolated(self):
        r=self.imported();original=self.lib.managed(r['storage_reference']).read_bytes();a=self.lib.thumbnail(r['asset_id'],1,size=64)
        path=self.lib.managed(a['storage_reference']);old=path.read_bytes();path.write_bytes(b'broken')
        b=self.lib.thumbnail(r['asset_id'],1,size=64);self.assertEqual(b['sha256'],sha256(old).hexdigest())
        self.assertEqual(self.lib.managed(r['storage_reference']).read_bytes(),original)
        self.assertEqual(self.lib.get(r['asset_id'])['revision'],1);self.assertEqual(self.lib.get(r['asset_id'])['integrity_status'],'VALID')

    def test_video_poster_bounded_and_original_unchanged(self):
        r=self.imported(self.mp4);old=self.lib.managed(r['storage_reference']).read_bytes();thumb=self.lib.thumbnail(r['asset_id'],1,size=64)
        t=self.lib.technical(self.lib.managed(thumb['storage_reference']),'image');self.assertLessEqual(max(t['width'],t['height']),64)
        self.assertEqual(self.lib.managed(r['storage_reference']).read_bytes(),old)

    def test_thumbnail_corrupt_original_refused(self):
        r=self.imported(self.mp4);self.lib.managed(r['storage_reference']).write_bytes(b'bad')
        self.assert_code('ASSET_UNAVAILABLE',lambda:self.lib.thumbnail(r['asset_id'],1))

    def test_preview_renders_bound_video_without_mutating_project_or_original(self):
        from experimental_mvp.test_timeline import audio
        r,p,a=self.attached(self.mp4);wav=self.root/'audio.wav';audio(wav,1)
        p.update(audio=str(wav),timeline={'version':1},output_profile={'width':320,'height':180,'fps':24})
        before=deepcopy(p);binary=self.lib.managed(r['storage_reference']).read_bytes()
        result=timeline.preview(p,timeline.measure_audio(p,self.root),self.root,scene_id='b'*32)
        self.assertTrue(result.is_file());self.assertEqual(p,before)
        self.assertEqual(self.lib.managed(r['storage_reference']).read_bytes(),binary)


if __name__=='__main__':unittest.main()
