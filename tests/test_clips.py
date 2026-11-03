import unittest
import json
from dataclasses import replace
from core.project_schema import Project, Scene, Track, Clip, MediaAsset

class ClipTests(unittest.TestCase):
    def setUp(self):
        self.p = Project('Тест', 'ru', (Scene('s',0,1000),), tracks=(Track('v','video'),Track('a','audio')),
            media=(MediaAsset('img','image','media/frame.png'),MediaAsset('snd','audio','media/voice.wav')),
            clips=(Clip('c','v','img',0,1000),Clip('d','a','snd',0,1000,100)))
    def test_roundtrip(self): self.assertEqual(Project.from_json(self.p.to_json()),self.p)
    def test_missing_media(self):
        with self.assertRaises(ValueError): replace(self.p, media=()).validate()
    def test_wrong_track(self):
        with self.assertRaises(ValueError): replace(self.p,clips=(Clip('x','a','img',0,100),)).validate()
    def test_bad_path(self):
        with self.assertRaises(ValueError): replace(self.p,media=(MediaAsset('x','image','../x'),)).validate()
    def test_duplicate_clips(self):
        with self.assertRaises(ValueError): replace(self.p,clips=(self.p.clips[0],self.p.clips[0])).validate()
    def test_v2_migration(self):
        d=json.loads(self.p.to_json()); d['schema_version']=2; d.pop('media'); d.pop('clips')
        migrated=Project.from_dict(d)
        self.assertEqual(migrated.schema_version,3); self.assertEqual(migrated.clips,())
    def test_v1_migration(self):
        d=json.loads(self.p.to_json()); d['schema_version']=1
        for k in ('tracks','subtitles','media','clips'): d.pop(k)
        self.assertEqual(Project.from_dict(d).schema_version,3)
    def test_source_offset_negative(self):
        with self.assertRaises(ValueError): replace(self.p,clips=(Clip('x','v','img',0,100,-1),)).validate()
