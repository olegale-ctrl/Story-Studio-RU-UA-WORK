import unittest
from core.project_schema import Project, Scene
from core.media_manifest import manifest_for_project, validate_media_path, manifest_json

class MediaManifestTests(unittest.TestCase):
    def test_ru_uk_manifest(self):
        for locale in ('ru', 'uk'):
            p = Project('История', locale, (Scene('s1', 0, 1000, 'Текст', 'images/кадр.png', 'audio/voice.wav'),))
            result = manifest_for_project(p)
            self.assertEqual(len(result['media']), 2)
            self.assertIn('кадр.png', manifest_json(p))
            self.assertEqual(result['content_locale'], locale)

    def test_windows_relative_normalization(self):
        self.assertEqual(validate_media_path(r'assets\scene\frame.png'), 'assets/scene/frame.png')

    def test_unsafe_paths(self):
        for path in ('../secret', 'assets/../secret', '/etc/passwd', r'C:\Windows\a', r'\\server\share',
                     '', '.', 'a//b', 'a/./b', 'a\\..\\b', 'a\x00b', 'https://x/y', 'a?b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_media_path(path)

    def test_invalid_scene_media_rejected(self):
        p = Project('Test', 'ru', (Scene('s1', 0, 1000, image_path='../secret'),))
        with self.assertRaises(ValueError): manifest_for_project(p)

    def test_empty_manifest(self):
        p = Project('Test', 'uk', ())
        self.assertEqual(manifest_for_project(p)['media'], [])

if __name__ == '__main__': unittest.main()
