import json
import tempfile
import unittest
from pathlib import Path
from core.project_schema import Project, Scene, Track, MediaAsset, Clip
from core.timeline_audit import audit_timeline
from core.export_bundle import write_bundle
from core.bundle_integrity import verify_bundle

class Sprint08Tests(unittest.TestCase):
    def project(self):
        return Project('Тест','uk',(Scene('s',0,2000),), tracks=(Track('v','video'),), media=(MediaAsset('m','image','a.png'),), clips=(Clip('a','v','m',0,1200),Clip('b','v','m',1000,900,source_in_ms=100)))
    def test_overlap_warning(self):
        issues=audit_timeline(self.project())
        self.assertEqual(issues[0]['code'],'CLIP_OVERLAP')
        self.assertEqual(issues[1]['code'],'SOURCE_OFFSET_UNVERIFIED')
    def test_non_overlapping(self):
        p=Project('T','ru',(),tracks=(Track('v','video'),),media=(MediaAsset('m','image','a.png'),),clips=(Clip('a','v','m',0,100),Clip('b','v','m',100,100)))
        self.assertEqual(audit_timeline(p),[])
    def test_integrity_roundtrip_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); src=root/'src';src.mkdir();(src/'a.png').write_bytes(b'image')
            dst=root/'out';write_bundle(self.project(),src,dst,dry_run=False)
            self.assertEqual(verify_bundle(dst),[])
            (dst/'media/a.png').write_bytes(b'tampered')
            self.assertTrue(any('checksum mismatch' in x for x in verify_bundle(dst)))
    def test_unlisted_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/'src';src.mkdir();(src/'a.png').write_bytes(b'image')
            dst=root/'out';write_bundle(self.project(),src,dst,dry_run=False)
            (dst/'extra.txt').write_text('extra')
            self.assertIn('unlisted file: extra.txt',verify_bundle(dst))
    def test_migration_fixtures(self):
        for version in (1,2,3):
            data=json.loads((Path(__file__).parent/'fixtures'/f'project_v{version}.json').read_text(encoding='utf-8'))
            p=Project.from_dict(data)
            self.assertEqual(p.schema_version,3)
            self.assertEqual(Project.from_json(p.to_json()),p)
