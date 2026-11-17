"""Sprint 28 tests: typed provider contracts (ADR-0009) and SBOM generation."""
import json
import shutil
import tempfile
import unittest
import wave
from pathlib import Path

from core.providers import (
    APPROVED, BLOCKED, REVIEW_REQUIRED, CommercialUseBlocked, PreRecordedAudioProvider,
    ProviderSpec, SPECS, commercial_use_allowed, ensure_voice_provider, get_spec,
    require_commercial_use,
)
from scripts.first_video import build
from scripts.generate_sbom import (
    ASSETS_CSV, DEFAULT_OUTPUT, DEPENDENCY_CSV, MODELS_CSV, build_bom, check_sbom,
    render_bom, write_sbom,
)

ROOT = Path(__file__).resolve().parents[1]


def tone(path):
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(24000)
        f.writeframes(b"\x00\x00" * 24000)


class ProviderContractTests(unittest.TestCase):
    def test_spec_validation(self):
        spec = SPECS["silero_local"]
        self.assertEqual(spec.commercial_use, REVIEW_REQUIRED)
        self.assertEqual(spec.kind, "local")
        bad = ProviderSpec(provider_id="x", title="x", kind="cloud",
                           commercial_use=APPROVED, data_handling="d", status="s")
        with self.assertRaises(ValueError):
            bad.validate()
        with self.assertRaises(ValueError):
            ProviderSpec(provider_id="x", title="x", kind="local",
                         commercial_use="maybe", data_handling="d", status="s").validate()

    def test_registry_and_unknown_provider(self):
        self.assertEqual(set(SPECS), {"silero_local", "edge", "prerecorded"})
        with self.assertRaises(ValueError):
            get_spec("doubao")
        with self.assertRaises(ValueError):
            get_spec(None)

    def test_commercial_gate(self):
        self.assertFalse(commercial_use_allowed("edge"))
        self.assertFalse(commercial_use_allowed("silero_local"))
        self.assertFalse(commercial_use_allowed("prerecorded"))
        for provider_id in ("edge", "silero_local", "prerecorded"):
            with self.assertRaises(CommercialUseBlocked):
                require_commercial_use(provider_id)
        with self.assertRaises(ValueError):
            require_commercial_use("doubao")

    def test_edge_is_blocked_not_review(self):
        # Edge TTS must never drift from BLOCKED: a cloud grant was never confirmed.
        self.assertEqual(get_spec("edge").commercial_use, BLOCKED)


class PreRecordedProviderTests(unittest.TestCase):
    def test_satisfies_contract(self):
        ensure_voice_provider(PreRecordedAudioProvider("."))

    def test_missing_directory(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                PreRecordedAudioProvider(Path(td) / "nope")

    def test_voices_empty(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(PreRecordedAudioProvider(td).voices("ru"), ())

    def test_synthesize_copies_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tone(root / "voice1.wav")
            provider = PreRecordedAudioProvider(root)
            target = root / "out" / "media" / "voice1.wav"
            result = provider.synthesize(text="Текст", locale="uk",
                                         voice="voice1.wav", output=target)
            self.assertEqual(result, target)
            self.assertTrue(target.is_file())
            self.assertEqual(target.stat().st_size, (root / "voice1.wav").stat().st_size)

    def test_missing_file_message(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(FileNotFoundError) as caught:
                PreRecordedAudioProvider(root).synthesize(
                    text="t", locale="ru", voice="voice2.wav", output=root / "o.wav")
            self.assertIn("Missing audio: " + str(root / "voice2.wav"), str(caught.exception))

    def test_traversal_and_extension_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tone(root / "voice1.wav")
            provider = PreRecordedAudioProvider(root)
            with self.assertRaises(ValueError):
                provider.synthesize(text="t", locale="ru", voice="../voice1.wav",
                                    output=root / "o.wav")
            with self.assertRaises(ValueError):
                provider.synthesize(text="t", locale="ru", voice="C:\\x.wav",
                                    output=root / "o.wav")
            with self.assertRaises(ValueError):
                provider.synthesize(text="t", locale="ru", voice="voice1.mp3",
                                    output=root / "o.wav")

    def test_fake_object_rejected_by_contract(self):
        class NotAProvider:
            pass

        with self.assertRaises(TypeError):
            ensure_voice_provider(NotAProvider())


class FirstVideoIntegrationTests(unittest.TestCase):
    def test_audio_route_builds_through_provider(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav")
            plan = root / "plan.json"
            plan.write_text('{"locale":"ru","scenes":[{"text":"Сцена"}]}',
                            encoding="utf-8")
            project_path, video = build(plan, root / "out", audio_dir=audio, render=False)
            self.assertIsNone(video)
            self.assertTrue((root / "out" / "media" / "voice1.wav").is_file())
            self.assertTrue(project_path.is_file())

    def test_missing_audio_still_fails_loudly(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            plan = root / "plan.json"
            plan.write_text('{"locale":"ru","scenes":[{"text":"Сцена"}]}',
                            encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                build(plan, root / "out", audio_dir=audio, render=False)


class SbomTests(unittest.TestCase):
    def test_build_is_deterministic(self):
        first = build_bom()
        second = build_bom()
        self.assertEqual(first, second)
        self.assertTrue(first["serialNumber"].startswith("urn:uuid:"))

    def test_bom_structure(self):
        bom = build_bom()
        self.assertEqual(bom["bomFormat"], "CycloneDX")
        self.assertEqual(bom["specVersion"], "1.5")
        self.assertEqual(bom["version"], 1)
        refs = [c["bom-ref"] for c in bom["components"]]
        self.assertEqual(len(refs), len(set(refs)), "bom-refs must be unique")
        types = {c["type"] for c in bom["components"]}
        self.assertEqual(types, {"library", "machine-learning-model", "file"})
        torch = next(c for c in bom["components"] if c["name"] == "torch")
        self.assertEqual(torch["type"], "library")
        self.assertEqual(torch["licenses"][0]["license"]["name"], "BSD-3-Clause")
        silero = next(c for c in bom["components"] if "Silero" in c["name"])
        props = {p["name"]: p["value"] for p in silero["properties"]}
        self.assertEqual(props["storystudio:register"], "AI_MODELS_AND_SERVICES")
        self.assertIn("noncommercial", props["storystudio:commercial-use"])

    def test_write_and_check_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "SBOM.cdx.json"
            write_sbom(target)
            self.assertTrue(check_sbom(target))
            tampered = json.loads(target.read_text(encoding="utf-8"))
            tampered["components"][0]["name"] += "!"
            target.write_text(render_bom(tampered), encoding="utf-8", newline="\n")
            self.assertFalse(check_sbom(target))
            self.assertFalse(check_sbom(Path(td) / "absent.json"))

    def test_real_repository_sbom_is_current(self):
        # The committed SBOM must match the audited CSVs (CI drift gate).
        self.assertTrue(check_sbom(DEFAULT_OUTPUT), "Run python scripts/generate_sbom.py")

    def test_empty_rows_are_skipped(self):
        with tempfile.TemporaryDirectory() as td:
            dep = Path(td) / "dep.csv"
            dep.write_text(
                "package,version,source,license,commercial_use,status,notes\n"
                "\n"
                "demo-pkg,1.0,pip,MIT,Yes,OK,\n", encoding="utf-8")
            models = Path(td) / "models.csv"
            shutil.copyfile(MODELS_CSV, models)
            assets = Path(td) / "assets.csv"
            shutil.copyfile(ASSETS_CSV, assets)
            bom = build_bom(dep, models, assets)
            names = [c["name"] for c in bom["components"]]
            self.assertIn("demo-pkg", names)
            self.assertNotIn("", names)


if __name__ == "__main__":
    unittest.main()
