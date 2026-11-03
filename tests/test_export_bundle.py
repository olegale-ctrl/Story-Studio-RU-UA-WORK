import tempfile
import unittest
from pathlib import Path
from core.project_schema import Project, Scene, Track, Subtitle, MediaAsset, Clip
from core.export_bundle import build_bundle_manifest, write_bundle


def sample():
    return Project('Тест', 'uk', (Scene('s',0,1000,image_path='imgs/a.png'),),
        tracks=(Track('v','video'),Track('sub','subtitle')),
        subtitles=(Subtitle('st','sub',0,900,'Привіт','uk'),),
        media=(MediaAsset('m','image','imgs/a.png'),),
        clips=(Clip('c','v','m',0,1000),))

class BundleTests(unittest.TestCase):
    def test_dry_run_no_io(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'bundle'
            manifest=write_bundle(sample(),Path(tmp)/'missing',dest)
            self.assertFalse(dest.exists())
            self.assertEqual(manifest['timeline_duration_ms'],1000)
            self.assertEqual(len(manifest['media']),1)
    def test_real_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'src'; (src/'imgs').mkdir(parents=True)
            (src/'imgs/a.png').write_bytes(b'png')
            dst=Path(tmp)/'out'
            write_bundle(sample(),src,dst,dry_run=False)
            self.assertEqual((dst/'media/imgs/a.png').read_bytes(),b'png')
            self.assertIn('Привіт',(dst/'subtitles/001.srt').read_text(encoding='utf-8'))
            self.assertIn('"bundle_version": 1',(dst/'bundle-manifest.json').read_text())
    def test_missing_input_does_not_create_dest(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'src';src.mkdir();dst=Path(tmp)/'out'
            with self.assertRaises(FileNotFoundError):write_bundle(sample(),src,dst,dry_run=False)
            self.assertFalse(dst.exists())
    def test_reject_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'src';src.mkdir();(src/'imgs').mkdir();(src/'imgs/a.png').write_bytes(b'x')
            with self.assertRaises(FileExistsError):write_bundle(sample(),src,src/'existing',dry_run=False) if False else write_bundle(sample(),src,Path(tmp),dry_run=False)
    def test_conflicting_kinds(self):
        p=Project('x','ru',(Scene('s',0,1000,audio_path='a.mp3'),),media=(MediaAsset('a','image','a.mp3'),))
        with self.assertRaises(ValueError):build_bundle_manifest(p)
    def test_unicode_and_order(self):
        m=build_bundle_manifest(sample())
        self.assertEqual(m['locale'],'uk')
        self.assertEqual(m['subtitle_tracks'][0]['path'],'subtitles/001.srt')
