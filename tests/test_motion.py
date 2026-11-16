"""Unit tests for core.motion Ken Burns camera animations."""
from __future__ import annotations

import unittest
from core.motion import (
    camera_at,
    ease_in_cubic,
    ease_out_cubic,
    resolve_shot_motion,
    smoothstep,
    MOTION_PRESETS,
)


class TestMotion(unittest.TestCase):
    def test_easing_functions(self):
        self.assertAlmostEqual(smoothstep(0.0), 0.0)
        self.assertAlmostEqual(smoothstep(1.0), 1.0)
        self.assertAlmostEqual(smoothstep(0.5), 0.5)

        self.assertAlmostEqual(ease_out_cubic(0.0), 0.0)
        self.assertAlmostEqual(ease_out_cubic(1.0), 1.0)

        self.assertAlmostEqual(ease_in_cubic(0.0), 0.0)
        self.assertAlmostEqual(ease_in_cubic(1.0), 1.0)

    def test_resolve_shot_motion_presets(self):
        shot = {"id": "s1", "duration_s": 5.0}
        resolve_shot_motion(shot, index=0, total_shots=3, preset_mode=True)
        self.assertEqual(shot["zoom"], [1.0, 1.12])
        self.assertTrue(shot["has_punch_in"])
        self.assertTrue(shot["has_punch_out"])

        # Intermediate time checks
        z, px, py = camera_at(shot, 2.5)
        self.assertTrue(1.0 <= z <= 1.25)
        self.assertAlmostEqual(px, 0.5, places=2)
        self.assertAlmostEqual(py, 0.5, places=2)

    def test_pan_motion(self):
        shot = {"id": "s2", "duration_s": 6.0}
        resolve_shot_motion(shot, index=1, total_shots=3, preset_mode=True)
        # Index 1 is pan_left: pivot_start x=0.58, pivot_end x=0.42
        z0, px0, py0 = camera_at(shot, 0.0)
        z_end, px_end, py_end = camera_at(shot, 6.0)

        self.assertAlmostEqual(px0, 0.58, places=2)
        self.assertAlmostEqual(px_end, 0.42, places=2)

    def test_clamp_and_safety(self):
        shot = {"id": "s3", "duration_s": 3.0}
        resolve_shot_motion(shot, index=2, total_shots=3)

        # t < 0 and t > duration must clamp without error
        z_neg, _, _ = camera_at(shot, -1.0)
        z_over, _, _ = camera_at(shot, 10.0)
        self.assertTrue(0.8 <= z_neg <= 2.0)
        self.assertTrue(0.8 <= z_over <= 2.0)


if __name__ == "__main__":
    unittest.main()
