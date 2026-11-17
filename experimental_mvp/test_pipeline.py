import tempfile
import json
import unittest
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch
import wave

from experimental_mvp.pipeline import (DEMOS, BuildStopped, brief, build, check_project,
                                       audio_key, executable, export_history, intervals, load,
                                       preview_signature, render_scene, save, subtitles)
from experimental_mvp.captions import CueError, render_srt


class PipelineTests(unittest.TestCase):
    def test_legacy_project_defaults_to_photo_and_keeps_scene_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "legacy.json"
            path.write_text('{"locale":"ru","scenes":[{"text":"Legacy"}]}', encoding="utf-8")
            project = load(path)
            scene = project["scenes"][0]
            self.assertNotIn("visual_mode", scene)
            with patch("experimental_mvp.pipeline.command") as run:
                render_scene(scene, 1, 1, root, root / "log", "ffmpeg")
            self.assertIn("color=c=0x17365a:s=1920x1080:r=30", run.call_args.args[0])
            cache = audio_key(project, scene, root)
            old_preview = preview_signature(project)
            scene.update(visual_mode="camera", camera_preset="pan")
            save(path, project)
            reopened = load(path)
            self.assertEqual(reopened["scenes"][0], scene)
            self.assertEqual(audio_key(reopened, reopened["scenes"][0], root), cache)
            self.assertNotEqual(preview_signature(reopened), old_preview)

    def test_video_drops_audio_and_holds_last_frame_or_trims(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ffmpeg, ffprobe = executable("ffmpeg"), executable("ffprobe")
            source = root / "клип.mp4"
            subprocess.run([ffmpeg, "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x240:r=20",
                            "-f", "lavfi", "-i", "sine=frequency=900", "-t", "0.4", "-c:v", "libx264",
                            "-c:a", "aac", str(source)], check=True, timeout=30)
            scene = {"visual_mode": "video", "video": str(source), "image": "unused.png"}
            for index, seconds in enumerate((1, 0.2), 1):
                with self.subTest(seconds=seconds):
                    clip = render_scene(scene, index, seconds, root, root / "log", ffmpeg)
                    probe = subprocess.check_output([ffprobe, "-v", "error", "-show_streams",
                                                     "-of", "json", str(root / clip)], timeout=30)
                    [video] = json.loads(probe)["streams"]
                    self.assertEqual((video["codec_type"], video["width"], video["height"],
                                      video["pix_fmt"], video["r_frame_rate"]),
                                     ("video", 1920, 1080, "yuv420p", "30/1"))
                    self.assertAlmostEqual(float(video["duration"]), seconds, places=3)
                    if seconds == 1:
                        raw = subprocess.check_output(
                            [ffmpeg, "-v", "error", "-i", str(root / clip), "-vf", "scale=96:54",
                             "-pix_fmt", "gray", "-f", "rawvideo", "-"], timeout=30)
                        size = 96 * 54
                        frames = [raw[i:i + size] for i in range(0, len(raw), size)]
                        self.assertEqual(len(frames), 30)
                        reference = frames[-1]
                        for frame in frames[-12:]:
                            # Lossy H.264 may reconstruct identical source frames slightly differently.
                            self.assertLess(sum(abs(a - b) for a, b in zip(frame, reference)) / size, 0.5)
                        self.assertGreater(sum(abs(a - b) for a, b in zip(frames[0], reference)) / size, 1)

    def test_missing_and_corrupt_video_identify_scene_for_repair(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "broken.mp4"
            project = {"locale": "ru", "scenes": [
                {"text": "Сцена", "visual_mode": "video", "video": str(source)}]}
            save(root / "project.json", project)
            for exists in (False, True):
                if exists:
                    source.write_bytes(b"broken")
                issues = check_project(project, root)
                field, message = [(field, msg) for _, field, msg, pending in issues if not pending][0]
                self.assertEqual(field, "video")
                self.assertIn("выберите фото", message)
                self.assertEqual(issues[0][0], project["scenes"][0]["id"])

    def test_offline_cli_starts_without_edge_adapter(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            package = root / "experimental_mvp"
            package.mkdir()
            for name in ("pipeline.py", "captions.py", "diagnostics.py", "ui.py"):
                shutil.copyfile(Path(__file__).with_name(name), package / name)
            result = subprocess.run(
                [sys.executable, "-E", "-s", "-m", "experimental_mvp.pipeline", "--help"],
                cwd=root, capture_output=True, timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b"--check-edge", result.stdout)
            result = subprocess.run(
                [sys.executable, "-E", "-s", "-c",
                 "from experimental_mvp.pipeline import synthesize; synthesize()"],
                cwd=root, capture_output=True, timeout=20,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"MP3/WAV", result.stderr)
    def test_missing_media_repair_preserves_scene_identity_and_captions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = root / "frame.bmp"
            # A minimal 1x1 local RGB image.
            image.write_bytes(bytes.fromhex(
                "424d3a00000000000000360000002800000001000000010000000100180000000000"
                "04000000000000000000000000000000000000000000ff00"))
            project_path = root / "project.json"
            project = {"locale": "ru", "scenes": [{"text": "Первый", "image": str(image)}]}
            save(project_path, project)
            scene_id = project["scenes"][0]["id"]
            captions = {scene_id: [{"start_ms": 0, "end_ms": 250, "text": "Правка"}]}
            project["captions_by_scene"] = captions
            before = preview_signature(project)
            moved = image.rename(root / "moved.bmp")
            self.assertNotEqual(preview_signature(project), before)
            issues = check_project(project, root)
            self.assertTrue(any(row[:2] == (scene_id, "image") and not row[3] for row in issues))
            project["scenes"][0]["image"] = str(moved)
            save(project_path, project)
            reopened = load(project_path)
            self.assertEqual(reopened["scenes"][0]["id"], scene_id)
            self.assertEqual(reopened["captions_by_scene"], captions)
            issues = check_project(reopened, root)
            self.assertEqual([(row[1], row[3]) for row in issues], [("captions", True)])

    def test_interruption_after_audio_retains_cache_and_never_exposes_export(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            audio = root / "fixture.wav"
            with wave.open(str(audio), "wb") as stream:
                stream.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
                stream.writeframes(bytes(24000))
            project = {"locale": "ru", "approved": True, "scenes": [{"text": "Работа"}]}
            project_file = root / "project.json"
            save(project_file, project)
            workspace = root / "runs"
            stopped = False

            def notify(message):
                nonlocal stopped
                if message == "Озвучка подготовлена":
                    stopped = True

            def fake_synthesis(voice, text, output, **_):
                shutil.copyfile(audio, output)

            with patch("experimental_mvp.pipeline.synthesize", side_effect=fake_synthesis) as synth:
                with self.assertRaises(BuildStopped):
                    build(project, workspace, notify, cancelled=lambda: stopped)
                self.assertEqual(synth.call_count, 1)
                [(folder, status)] = export_history(workspace)
                self.assertEqual(status, "interrupted")
                self.assertFalse((folder / "final.mp4").exists())
                build(load(project_file), workspace)
                self.assertEqual(synth.call_count, 1)
            journal = next((workspace / "scene-audio").rglob("audio.log"))
            self.assertIn("reuse", journal.read_text(encoding="utf-8"))
            crashed = workspace / "run-crashed"
            crashed.mkdir()
            save(crashed / "result.json", {"status": "running"})
            (crashed / "final.mp4").touch()
            self.assertIn((crashed, "interrupted"), export_history(workspace))
    def test_manual_cues_round_trip_and_follow_scene_after_reorder(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "project.json"
            project = {"scenes": [{"text": "Первый"}, {"text": "Другий"}]}
            save(file, project)
            scene = project["scenes"][0]
            overrides = {scene["id"]: [{"start_ms": 125, "end_ms": 826, "text": "Правка"}]}
            project["captions_by_scene"] = overrides
            save(file, project)
            reopened = load(file)
            self.assertEqual(reopened["captions_by_scene"], overrides)
            reopened["scenes"].reverse()
            srt = render_srt(reopened["scenes"], [(0, 1500), (1500, 2500)], overrides)
            self.assertIn("00:00:01,625 --> 00:00:02,326\nПравка", srt)
            self.assertLess(srt.index("Другий"), srt.index("Правка"))

    def test_shortened_audio_rejects_manual_interval_and_reset_recovers(self):
        scenes = [{"id": "one", "text": "Первый"}, {"id": "two", "text": "Другий"}]
        overrides = {"two": [{"start_ms": 150, "end_ms": 900, "text": "Правка"}]}
        with self.assertRaisesRegex(CueError, "Сцена 2, реплика 1.*500 мс"):
            render_srt(scenes, [(0, 1200), (1200, 1700)], overrides)
        overrides.clear()
        self.assertIn("00:00:01,200 --> 00:00:01,700\nДругий",
                      render_srt(scenes, [(0, 1200), (1200, 1700)], overrides))
    def test_projects_round_trip_and_default_to_unapproved(self):
        for locale in ("ru", "uk"):
            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as temp:
                project = load(DEMOS / f"{locale}.json")
                file = Path(temp) / "local" / "project.json"
                save(file, project)
                self.assertEqual(load(file), project)
                with self.assertRaisesRegex(ValueError, "подтвердите"):
                    build(project, Path(temp) / "runs")
                self.assertFalse((Path(temp) / "runs").exists())
                self.assertIn(project["topic"], brief(project["topic"], locale))

    def test_imported_audio_intervals_are_contiguous(self):
        spans = list(intervals(["коротко", "друга сцена довша"], 2011))
        self.assertEqual(spans[0][0], 0)
        self.assertEqual(spans[0][1], spans[1][0])
        self.assertGreater(spans[1][1] - spans[1][0], spans[0][1])
        self.assertEqual(spans[1][1], 2011)

    def test_srt_preserves_cyrillic_and_does_not_emit_user_markup(self):
        output = subtitles(["<b>Історія</b>"], [(0, 1500)])
        self.assertIn("00:00:00,000 --> 00:00:01,500", output)
        self.assertIn("Історія", output)
        self.assertNotIn("<b>", output)

    def test_resume_failure_edit_and_reorder(self):
        try:
            executable("ffmpeg")
            executable("ffprobe")
        except RuntimeError as exc:
            self.skipTest(str(exc))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            audio = root / "fixture.wav"
            with wave.open(str(audio), "wb") as stream:
                stream.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
                stream.writeframes(bytes(24000))
            calls = []

            def synthesis(voice, text, output, **_):
                calls.append(text)
                if text == "middle" and calls.count(text) == 1:
                    raise RuntimeError("Deterministic simulated TTS failure")
                shutil.copyfile(audio, output)

            project_file = root / "project.json"
            project = {"locale": "ru", "approved": True,
                       "scenes": [{"text": s} for s in ("first", "middle", "last")]}
            save(project_file, project)
            ids = [s["id"] for s in project["scenes"]]
            runs = root / "runs"
            with patch("experimental_mvp.pipeline.synthesize", side_effect=synthesis):
                with self.assertRaisesRegex(RuntimeError, "simulated TTS failure"):
                    build(project, runs)
                self.assertEqual(calls, ["first", "middle", "last"])
                self.assertIn("simulated TTS failure",
                              (runs / "scene-audio" / ids[1] / "audio.log").read_text())
                project = load(project_file)
                self.assertEqual([s["id"] for s in project["scenes"]], ids)
                build(project, runs)
                self.assertEqual(calls, ["first", "middle", "last", "middle"])
                project["scenes"][0]["text"] = "updated"
                project["scenes"].reverse()
                final = build(project, runs)
                self.assertEqual(calls, ["first", "middle", "last", "middle", "updated"])
                srt = (final.parent / "captions.srt").read_text(encoding="utf-8")
                self.assertLess(srt.index("last"), srt.index("middle"))
                self.assertLess(srt.index("middle"), srt.index("updated"))
                print(f"Deterministic synthesis calls: {calls}")
