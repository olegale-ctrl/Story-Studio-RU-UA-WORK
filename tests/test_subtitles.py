import unittest
from core.project_schema import Project, Track, Subtitle
from core.subtitles import export_srt

class SrtTests(unittest.TestCase):
    def test_export_unicode_and_order(self):
        p = Project('Київ', 'uk', (), tracks=(Track('captions', 'subtitle'),), subtitles=(
            Subtitle('b', 'captions', 65000, 1500, 'Другий', 'uk'),
            Subtitle('a', 'captions', 0, 500, 'Перший', 'uk'),
        ))
        self.assertEqual(export_srt(p, track_id='captions'),
                         '1\n00:00:00,000 --> 00:00:00,500\nПерший\n\n2\n00:01:05,000 --> 00:01:06,500\nДругий\n')

    def test_unknown_track(self):
        with self.assertRaises(ValueError): export_srt(Project('X', 'ru', ()), track_id='none')

    def test_empty_track(self):
        self.assertEqual(export_srt(Project('X', 'ru', (), tracks=(Track('s', 'subtitle'),)), track_id='s'), '')
