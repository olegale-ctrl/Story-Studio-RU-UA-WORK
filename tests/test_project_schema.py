import unittest
from dataclasses import replace
from core.project_schema import Project, Scene

class ProjectSchemaTests(unittest.TestCase):
    def setUp(self):
        self.project = Project("Історія / История", "uk", (Scene("s1", 0, 2500, "Привіт"),))

    def test_roundtrip_unicode(self):
        self.assertEqual(Project.from_json(self.project.to_json()), self.project)

    def test_ru_locale(self):
        replace(self.project, content_locale="ru").validate()

    def test_unsupported_locale(self):
        with self.assertRaises(ValueError): replace(self.project, content_locale="zh").validate()

    def test_negative_timing(self):
        with self.assertRaises(ValueError): replace(self.project, scenes=(Scene("x", -1, 10),)).validate()

    def test_duplicate_id(self):
        with self.assertRaises(ValueError): replace(self.project, scenes=(Scene("x", 0, 10), Scene("x", 10, 10))).validate()

    def test_unknown_field(self):
        payload = self.project.to_dict(); payload["unexpected"] = True
        with self.assertRaises(ValueError): Project.from_dict(payload)

    def test_float_timing_rejected(self):
        payload = self.project.to_dict(); payload["scenes"][0]["start_ms"] = 1.5
        with self.assertRaises(ValueError): Project.from_dict(payload)

if __name__ == "__main__": unittest.main()

from core.project_schema import Track, Subtitle

class TimelineV2Tests(unittest.TestCase):
    def setUp(self):
        self.p = Project('Київ', 'uk', (Scene('s1', 0, 1000, 'Текст'),),
                         tracks=(Track('t1', 'subtitle', 'Субтитри'),),
                         subtitles=(Subtitle('sub1', 't1', 0, 800, 'Привіт!', 'uk'),))

    def test_v2_roundtrip(self):
        self.assertEqual(Project.from_json(self.p.to_json()), self.p)

    def test_migrate_v1(self):
        payload = self.p.to_dict()
        payload.pop('tracks'); payload.pop('subtitles'); payload.pop('media'); payload.pop('clips'); payload['schema_version'] = 1; payload['scenes'] = list(payload['scenes'])
        migrated = Project.from_dict(payload)
        self.assertEqual(migrated.schema_version, 3)
        self.assertEqual(migrated.tracks, ())

    def test_migrate_v1_does_not_mutate_input(self):
        payload = self.p.to_dict()
        payload.pop('tracks'); payload.pop('subtitles'); payload.pop('media'); payload.pop('clips'); payload['schema_version'] = 1; payload['scenes'] = list(payload['scenes'])
        Project.from_dict(payload)
        self.assertEqual(payload['schema_version'], 1)

    def test_wrong_subtitle_track(self):
        with self.assertRaises(ValueError): replace(self.p, tracks=(Track('t1', 'audio'),)).validate()

    def test_missing_subtitle_track(self):
        with self.assertRaises(ValueError): replace(self.p, tracks=()).validate()

    def test_duplicate_track(self):
        with self.assertRaises(ValueError): replace(self.p, tracks=(Track('t1', 'subtitle'), Track('t1', 'subtitle'))).validate()

    def test_duplicate_subtitle(self):
        with self.assertRaises(ValueError): replace(self.p, subtitles=self.p.subtitles * 2).validate()

    def test_negative_subtitle_duration(self):
        with self.assertRaises(ValueError): replace(self.p, subtitles=(replace(self.p.subtitles[0], duration_ms=-1),)).validate()

    def test_invalid_subtitle_locale(self):
        with self.assertRaises(ValueError): replace(self.p, subtitles=(replace(self.p.subtitles[0], locale='zh'),)).validate()

    def test_bool_timing_rejected(self):
        with self.assertRaises(ValueError): replace(self.p, scenes=(Scene('s1', True, 100),)).validate()

    def test_unknown_v2_field_rejected(self):
        payload = self.p.to_dict(); payload['tracks'][0]['bad'] = 1
        with self.assertRaises(ValueError): Project.from_dict(payload)

    def test_v1_invalid_field_rejected(self):
        payload = self.p.to_dict(); payload.pop('tracks'); payload.pop('subtitles'); payload.pop('media'); payload.pop('clips'); payload['schema_version'] = 1; payload['scenes'] = list(payload['scenes'])
        payload['scenes'][0]['bad'] = 1
        with self.assertRaises(ValueError): Project.from_dict(payload)

    def test_nonfinite_fps_rejected(self):
        with self.assertRaises(ValueError): replace(self.p, fps=float('nan')).validate()

    def test_unicode_srt_ready_text(self):
        self.assertIn('Привіт!', self.p.to_json())
