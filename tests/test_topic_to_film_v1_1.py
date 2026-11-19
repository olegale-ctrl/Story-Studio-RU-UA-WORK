import contextlib
from copy import deepcopy
import io
import json
import unittest
from unittest.mock import patch

from core import topic_to_film as old
from core import topic_to_film_v1_1 as new
from story_intelligence.codec_v1 import canonical_si_sha256, canonical_si_json
from scripts.topic_to_film import main

PLAN = {"locale": "ru", "scenes": [{"text": "Тест", "image": "frame1.png"}]}
MATERIALS = {role: {"role": role, "path": path,
             "observation": {"sha256": "a" * 64, "byte_length": 44}}
             for role, path in [("voice1", "voice1.wav"), ("image1", "frame1.png")]}


class DiagnosticRevisionTests(unittest.TestCase):
    def intent(self):
        return new.prepare_intent(topic="Тема")

    def ready(self):
        value = new.initial_readiness(self.intent())
        value.update({a: "true" for a in new.AXES})
        value["blockers"] = []
        return value

    def rejected(self, intent):
        with self.assertRaises(ValueError):
            new.validate_diagnostic("job_intent", intent)

    def test_routes(self):
        for route, kwargs in [("A", {"topic": "x"}), ("B", {"script": "x"}),
                              ("C", {"plan": PLAN}), ("D", {"plan": PLAN, "materials": MATERIALS})]:
            with self.subTest(route=route):
                value = new.prepare_intent(**kwargs)
                self.assertEqual(value["route"], route)
                self.assertEqual(value["proposed_job_types"], new.ROUTES[route])

    def test_wrong_route(self):
        value = self.intent(); value["route"] = "D"; self.rejected(value)

    def test_stage_order(self):
        value = self.intent(); value["proposed_job_types"].reverse(); self.rejected(value)

    def test_unknown_duplicate_and_missing_stage(self):
        for stages in [["unknown"], new.ROUTES["A"] + ["render.mp4"], new.ROUTES["A"][:-1]]:
            with self.subTest(stages=stages):
                value = self.intent(); value["proposed_job_types"] = stages; self.rejected(value)

    def test_digest_mutation(self):
        value = self.intent(); value["intent_sha256"] = "0" * 64; self.rejected(value)

    def test_conflicting_inputs(self):
        value = self.intent(); value["inputs"]["script"] = "y"; self.rejected(value)

    def test_no_inputs(self):
        value = self.intent(); value["inputs"] = {}; self.rejected(value)

    def test_unknown_input_field(self):
        value = self.intent(); value["inputs"]["dag"] = {}; self.rejected(value)

    def test_mode_fallback_status_and_accepted_ids(self):
        for key, data in [("mode", "live"), ("fallback_class", "auto"), ("status", "ACCEPTED"), ("accepted_job_ids", ["job"]), ("blockers", [])]:
            with self.subTest(key=key):
                value = self.intent(); value[key] = data; self.rejected(value)

    def test_sha_lexical_cases(self):
        for digest in ["a" * 63, "a" * 65, "A" * 64, "a" * 64 + "\n", "a" * 64 + "\r\n", " " + "a" * 64, "a" * 64 + " ", "а" * 64, "a" * 63 + "g"]:
            with self.subTest(digest=repr(digest)):
                value = self.intent(); value["intent_sha256"] = digest
                with self.assertRaises(ValueError): new.validate_structure("job_intent", value)
        new.validate_structure("job_intent", self.intent())

    def test_byte_observation_sha_exact(self):
        value = new.prepare_intent(plan=PLAN, materials=MATERIALS)
        value["inputs"]["materials"]["voice1"]["observation"]["sha256"] += "\n"
        self.rejected(value)

    def test_related_uuid_and_ref_hash_endings(self):
        value = self.ready()
        ref = {"type": "Intake", "id": "00000000-0000-0000-0000-000000000001", "revision": 1, "sha256": "a" * 64}
        value["evidence_refs"] = [ref]
        new.validate_diagnostic("readiness", value)
        for key in ("id", "sha256"):
            bad = deepcopy(value); bad["evidence_refs"][0][key] += "\n"
            with self.subTest(key=key), self.assertRaises(ValueError): new.validate_diagnostic("readiness", bad)

    def test_blank_topic_script_scene_title(self):
        for kwargs in [{"topic": " \n"}, {"script": "\t"}, {"plan": {"locale": "ru", "scenes": [{"text": " "}]}}, {"plan": {**PLAN, "title": " "}}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError): new.prepare_intent(**kwargs)

    def test_bad_locale_and_plan_fields(self):
        for plan in [{**PLAN, "locale": "ua"}, {"locale": "ru", "scenes": []}, {"locale": "ru"}, {**PLAN, "extra": True}]:
            with self.subTest(plan=plan), self.assertRaises(ValueError): new.prepare_intent(plan=plan)

    def test_path_traversal_in_plan(self):
        for path in ["../x.png", "/x.png", "C:\\x.png", "a\\b.png", "a/b.png"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                new.prepare_intent(plan={"locale": "ru", "scenes": [{"text": "x", "image": path}]})

    def test_plan_material_mismatch(self):
        for change in ["wrong_path", "missing", "extra", "no_plan_image"]:
            material = deepcopy(MATERIALS); plan = deepcopy(PLAN)
            if change == "wrong_path": material["image1"]["path"] = "other.png"
            if change == "missing": del material["image1"]
            if change == "extra": material["image2"] = {**material["image1"], "role": "image2"}
            if change == "no_plan_image": del plan["scenes"][0]["image"]
            with self.subTest(change=change), self.assertRaises(ValueError): new.prepare_intent(plan=plan, materials=material)

    def test_unsupported_material_type(self):
        material = deepcopy(MATERIALS); material["clip1"] = material.pop("image1"); material["clip1"]["role"] = "clip1"
        with self.assertRaises(ValueError): new.prepare_intent(plan=PLAN, materials=material)

    def test_bad_audio_format(self):
        material = deepcopy(MATERIALS); material["voice1"]["path"] = "voice1.mp3"
        with self.assertRaises(ValueError): new.prepare_intent(plan=PLAN, materials=material)

    def test_structural_pass_is_not_semantic_pass(self):
        value = self.intent(); value["route"] = "D"
        new.validate_structure("job_intent", value)
        self.rejected(value)

    def test_incomplete_readiness_never_necessary(self):
        for key in self.ready():
            value = self.ready(); del value[key]
            with self.subTest(key=key):
                self.assertFalse(new.assess_release("production", value, bindings_current="true", creative_review="true")["necessary_conditions_satisfied"])

    def test_wrong_axis_types_and_states(self):
        for axis in new.AXES:
            for state in [True, False, None, 1, "TRUE", "unknown", "false"]:
                value = self.ready(); value[axis] = state
                with self.subTest(axis=axis, state=state):
                    result = new.assess_release("production", value, bindings_current="true", creative_review="true")
                    self.assertFalse(result["necessary_conditions_satisfied"])
                    self.assertFalse(result["release_allowed"])

    def test_all_axes_true_is_diagnostic_only(self):
        value = self.ready()
        result = new.assess_release("production", value, bindings_current="true", creative_review="true")
        self.assertTrue(result["necessary_conditions_satisfied"])
        self.assertFalse(result["release_allowed"])
        self.assertEqual(result["status"], "BLOCKED_CONTRACT")

    def test_unverified_attestation_not_promoted(self):
        intent = new.prepare_intent(topic="x", authorize_render=True, declare_facts_reviewed=True, declare_rights_cleared=True)
        value = new.initial_readiness(intent)
        self.assertTrue(all(value[a] == "unknown" for a in new.AXES))
        value["attestations"] = {"trusted": True}
        self.assertFalse(new.assess_release("production", value)["necessary_conditions_satisfied"])

    def test_readiness_semantic_bad_binding(self):
        value = self.ready(); value["artifact_bindings"] = [{"role": "render", "path": "../film.mp4", "observation": {"sha256": "a" * 64, "byte_length": 1}}]
        self.assertFalse(new.assess_release("production", value, bindings_current="true", creative_review="true")["necessary_conditions_satisfied"])

    def test_fallback_and_draft_never_qualify(self):
        for fallback in ["equivalent", "degraded", "placeholder"]:
            value = self.ready(); value["fallback_class"] = fallback
            with self.subTest(fallback=fallback):
                self.assertFalse(new.assess_release("production", value, bindings_current="true", creative_review="true")["necessary_conditions_satisfied"])
        self.assertFalse(new.assess_release("draft", self.ready(), bindings_current="true", creative_review="true")["necessary_conditions_satisfied"])

    def test_old_objects_not_new(self):
        with self.assertRaises(ValueError): new.validate_diagnostic("job_intent", old.prepare_intent(topic="x"))
        with self.assertRaises(ValueError): new.validate_diagnostic("readiness", old.initial_readiness(old.prepare_intent(topic="x")))
        self.assertFalse(new.assess_release("production", old.initial_readiness(old.prepare_intent(topic="x")))["necessary_conditions_satisfied"])

    def test_version_and_digest_differ(self):
        self.assertEqual(old.VERSION, "SP/1-PROPOSAL")
        self.assertNotEqual(old.prepare_intent(topic="x")["intent_sha256"], new.prepare_intent(topic="x")["intent_sha256"])

    def test_determinism_and_body_scope(self):
        one = new.prepare_intent(plan=PLAN)
        two = new.prepare_intent(plan={"scenes": PLAN["scenes"], "locale": "ru"})
        self.assertEqual(one, two)
        body = {k: one[k] for k in new.BODY_FIELDS}
        self.assertEqual(one["intent_sha256"], canonical_si_sha256(body))
        self.assertEqual(canonical_si_json(body), canonical_si_json({k: body[k] for k in reversed(body)}))

    def test_cli_explicit_new_and_legacy_default(self):
        for argv, version in [([], old.VERSION), (["--contract-version", new.VERSION], new.VERSION)]:
            with self.subTest(version=version), contextlib.redirect_stdout(io.StringIO()) as output, patch("scripts.first_video.build", side_effect=AssertionError("forbidden")), patch("subprocess.run", side_effect=AssertionError("forbidden")):
                code = main(["--topic", "Тема", "--wait", "1", *argv])
            result = json.loads(output.getvalue())
            self.assertEqual(code, 3)
            self.assertEqual(result["intent"]["schema_version"], version)
            self.assertEqual(result["intent"]["accepted_job_ids"], [])

    def test_no_diagnostic_grant(self):
        for kind, value in [("readiness", self.ready()), ("production_readiness_report", new.assess_release("production", self.ready())), ("technical_gate_report", new.run_gates("A"))]:
            value["release_allowed"] = True
            with self.subTest(kind=kind), self.assertRaises(ValueError): new.validate_diagnostic(kind, value)

    def test_fixed_schema_profile_rejects_unknown_kind(self):
        with self.assertRaises(ValueError): new.validate_diagnostic("dag", {})

    def test_readiness_duplicate_artifact_role(self):
        value = self.ready(); binding = {"role": "render", "path": "film.mp4", "observation": {"sha256": "a" * 64, "byte_length": 1}}
        value["artifact_bindings"] = [binding, deepcopy(binding)]
        with self.assertRaises(ValueError): new.validate_diagnostic("readiness", value)


if __name__ == "__main__":
    unittest.main()
