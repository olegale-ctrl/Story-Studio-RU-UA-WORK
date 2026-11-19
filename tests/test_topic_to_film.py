import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import wave

from core.topic_to_film import (AXES, POLICY, assess_release, binding_matches,
    classify, hardware_preflight, initial_readiness, prepare_intent, validate_plan,
    validate_wav)
from core.topic_to_film_gates import read_json, read_local, run_gates
from scripts.topic_to_film import main


PLAN = {"locale": "ru", "scenes": [{"text": "Синтетический тест"}]}


class TopicToFilmTests(unittest.TestCase):
    def test_routes(self):
        self.assertEqual([classify(topic="тема"), classify(script="сценарий"),
                          classify(plan=PLAN), classify(plan=PLAN, materials={"voice": "declared"})], list("ABCD"))

    def test_ambiguous_input_rejected(self):
        with self.assertRaises(ValueError):
            classify(topic="x", script="y")

    def test_empty_materials_not_silently_class_c(self):
        with self.assertRaises(ValueError):
            classify(plan=PLAN, materials={})

    def test_a_defaults_draft(self):
        self.assertEqual(prepare_intent(topic="x")["mode"], "draft")

    def test_a_production_blocked(self):
        self.assertIn("CLASS_A_PRODUCTION_POLICY_REQUIRED", prepare_intent(topic="x", mode="production")["blockers"])

    def test_missing_plan_c(self):
        self.assertIn("PLAN_REQUIRED", run_gates("C")["blockers"])

    def test_bad_locale(self):
        with self.assertRaises(ValueError):
            validate_plan({**PLAN, "locale": "ua"})

    def test_bad_scene_count(self):
        with self.assertRaises(ValueError):
            validate_plan({**PLAN, "scenes": []})

    def test_unsafe_image_paths(self):
        for path in ("../secret.png", "C:\\secret.png", "\\\\host\\file.png", "sub/image.png", "x:secret.jpg", "a\\b.png"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_plan({"locale": "uk", "scenes": [{"text": "x", "image": path}]})

    def test_wav_corrupt(self):
        with self.assertRaises(ValueError):
            validate_wav(b"not wav")

    def test_wav_valid_and_truncated(self):
        output = io.BytesIO()
        with wave.open(output, "wb") as stream:
            stream.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
            stream.writeframes(bytes(1600))
        raw = output.getvalue()
        self.assertEqual(validate_wav(raw)["duration_ms"], 100)
        with self.assertRaises(ValueError):
            validate_wav(raw[:-1])

    def test_missing_wav(self):
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "plan.json"
            plan.write_text(json.dumps(PLAN), encoding="utf-8")
            result = run_gates("D", plan_path=plan, audio_dir=directory)
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("VOICE1_FAILED", result["blockers"])

    def test_placeholder_production(self):
        intent = prepare_intent(script="x", mode="production", fallback="placeholder")
        self.assertIn("PLACEHOLDER_NOT_AUTHORIZED", intent["blockers"])

    def test_degraded_without_policy(self):
        self.assertIn("DEGRADATION_POLICY_REQUIRED", prepare_intent(script="x", fallback="degraded")["blockers"])

    def test_equivalent_needs_evidence(self):
        self.assertIn("COMPATIBILITY_EVIDENCE_REQUIRED", prepare_intent(script="x", fallback="equivalent")["blockers"])

    def readiness(self):
        return {**{a: "true" for a in AXES}, "policy_version": POLICY,
                "fallback_class": "none", "blockers": []}

    def test_si_does_not_clear_facts(self):
        r = self.readiness()
        r.update(si_eligible="true", facts_reviewed="unknown")
        self.assertIn("AXIS_FACTS_REVIEWED", assess_release("production", r)["blockers"])

    def test_mp4_does_not_clear_rights(self):
        r = self.readiness()
        r.update(technical_pass="true", rights_cleared="unknown")
        self.assertIn("AXIS_RIGHTS_CLEARED", assess_release("production", r)["blockers"])

    def test_stale_sha_and_policy(self):
        self.assertFalse(binding_matches({"sha256": "a" * 64}, {"sha256": "b" * 64}))
        self.assertFalse(binding_matches({"policy": "1"}, {"policy": "2"}))

    def test_render_intent_never_grants(self):
        r = initial_readiness(prepare_intent(topic="x", authorize_render=True,
                         declare_facts_reviewed=True, declare_rights_cleared=True))
        self.assertTrue(all(r[a] == "unknown" for a in AXES))

    def test_repeat_intent_deterministic_not_submitted(self):
        first = prepare_intent(plan=PLAN)
        second = prepare_intent(plan=deepcopy(PLAN))
        self.assertEqual(first, second)
        self.assertEqual(first["accepted_job_ids"], [])

    def test_inputs_detached(self):
        plan = deepcopy(PLAN)
        result = prepare_intent(plan=plan)
        plan["scenes"][0]["text"] = "changed"
        self.assertEqual(result["inputs"]["plan"], PLAN)

    def test_material_declaration_shape(self):
        with self.assertRaises(ValueError):
            prepare_intent(plan=PLAN, materials={"voice": "not a binding"})
        materials = {"voice1": {"role": "voice1", "path": "voice1.wav",
                     "observation": {"sha256": "a" * 64, "byte_length": 100}}}
        self.assertEqual(prepare_intent(plan=PLAN, materials=materials)["route"], "D")

    def cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main(list(args))
        return code, json.loads(output.getvalue())

    def test_absent_dispatcher_never_direct_render(self):
        with patch("scripts.first_video.build", side_effect=AssertionError("direct render forbidden")), patch("subprocess.run", side_effect=AssertionError("no subprocess")):
            code, result = self.cli("--topic", "x")
        self.assertEqual(code, 3)
        self.assertEqual(result["intent"]["status"], "BLOCKED_DISPATCHER_CONTRACT")

    def test_wait_cannot_trust_local_mirror(self):
        code, result = self.cli("--topic", "x", "--wait", "1")
        self.assertEqual(code, 3)
        self.assertEqual(result["wait_status"], "BLOCKED_JOBSTORE_CONTRACT")
        # No JobStore/mirror exists: actual mismatch recovery is NOT_RUN.

    def test_publication_failure_not_simulated_as_success(self):
        result = run_gates("A", phase="final")
        self.assertIn("BLOCKED_RESULT_PUBLICATION_CONTRACT", result["blockers"])
        self.assertFalse(result["release_allowed"])
        # Actual crash between job commit/publication requires missing API.

    def test_insufficient_hardware(self):
        r = hardware_preflight({"schema_version": 1, "cpu_available": True, "ram_gib": 1}, available_disk_bytes=1)
        self.assertIn("RAM_UNKNOWN_OR_INSUFFICIENT", r["blockers"])
        self.assertIn("DISK_UNKNOWN_OR_INSUFFICIENT", r["blockers"])

    def test_installed_model_not_qualified(self):
        r = hardware_preflight({"schema_version": 1, "cpu_available": True, "ram_gib": 64, "wan_installed": True}, available_disk_bytes=10**12)
        self.assertFalse(r["provider_execution_allowed"])

    def test_final_incomplete(self):
        r = run_gates("C", phase="final")
        self.assertTrue({"PLAN_REQUIRED", "PROJECT_REQUIRED", "MP4_REQUIRED"}.issubset(r["blockers"]))
        self.assertEqual(r["technical_pass"], "unknown")

    def test_no_release_permission(self):
        r = self.readiness()
        r["authorized_for_release"] = "unknown"
        self.assertIn("AXIS_AUTHORIZED_FOR_RELEASE", assess_release("production", r)["blockers"])

    def test_draft_no_gates_bypass(self):
        r = assess_release("draft", self.readiness(), bindings_current="true", creative_review="true")
        self.assertFalse(r["necessary_conditions_satisfied"])
        self.assertFalse(r["release_allowed"])

    def test_even_all_assertions_are_not_authority(self):
        r = assess_release("production", self.readiness(), bindings_current="true", creative_review="true")
        self.assertTrue(r["necessary_conditions_satisfied"])
        self.assertFalse(r["release_allowed"])
        self.assertIn("BLOCKED_ATTESTATION_VERIFIER", r["blockers"])

    def test_boolean_axis_rejected(self):
        r = self.readiness()
        r["facts_reviewed"] = True
        with self.assertRaises(ValueError):
            assess_release("production", r)

    def test_duplicate_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "x.json"
            path.write_text('{"locale":"ru","locale":"uk"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                read_json(path)

    def test_read_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "x"
            path.write_bytes(b"123")
            with self.assertRaises(ValueError):
                read_local(path, 2)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target, link = Path(directory) / "x", Path(directory) / "link"
            target.write_text("x")
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("Symlink creation unavailable; not Windows qualification")
            with self.assertRaises(ValueError):
                read_local(link, 10)

    def test_intermediate_not_final_technical_pass(self):
        r = run_gates("A")
        self.assertEqual(r["status"], "INTERMEDIATE_CHECKS_PASS")
        self.assertEqual(r["technical_pass"], "unknown")

    def test_skip_gates_not_an_option(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(["--topic", "x", "--skip-gates"])
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
