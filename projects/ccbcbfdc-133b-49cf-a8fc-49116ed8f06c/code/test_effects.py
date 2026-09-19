"""Логически проверки на компютър, не тестове на светодиоди или звук."""
import unittest
from effects import Effects
from sound_demo import make_wav
from rgb_pixels import frame
from acceleration import Motion


class EffectsTests(unittest.TestCase):
    def test_switch_on_off(self):
        e = Effects()
        self.assertEqual(e.tick(0, button=True)["sound"], "ignite")
        e.tick(250)
        self.assertEqual(e.tick(250)["state"], "ACTIVE")
        self.assertEqual(e.tick(0, button=True)["sound"], "retract")
        e.tick(250)
        self.assertEqual(e.tick(250)["state"], "OFF")

    def test_fault_is_latched(self):
        e = Effects()
        e.tick(200, button=True)
        self.assertEqual(e.tick(1, low_battery=True)["brightness"], 0)
        self.assertEqual(e.tick(20, button=True)["state"], "FAULT")

    def test_event_spacing(self):
        e = Effects()
        e.tick(250, button=True)
        e.tick(250)
        self.assertEqual(e.tick(1, moving=True)["sound"], "swing")
        self.assertIsNone(e.tick(1, impact=True)["sound"])

    def test_wav(self):
        data = make_wav()
        self.assertEqual(len(data), 8044)
        self.assertEqual(data[:4], b"RIFF")
        self.assertLessEqual(max(data[44:]), 156)

    def test_addressable_rgb(self):
        pixels = frame({"length_permille": 500, "brightness": 64}, 5, (255, 0, 0))
        self.assertEqual(pixels, [(64, 0, 0), (64, 0, 0), (32, 0, 0), (0, 0, 0), (0, 0, 0)])
        self.assertEqual(frame({"length_permille": 0, "brightness": 0}, 3), [(0, 0, 0)] * 3)
        with self.assertRaises(ValueError):
            frame({"length_permille": 0, "brightness": 0}, color=(0, 0, 0, 0))

    def test_acceleration(self):
        motion = Motion()
        self.assertFalse(motion.sample(0, 0, 9.80665, 20)["moving"])
        self.assertTrue(motion.sample(3, 0, 9.80665, 20)["moving"])
        for _ in range(150):
            quiet = motion.sample(0, 0, 9.80665, 20)
        self.assertFalse(quiet["moving"])
        with self.assertRaises(ValueError):
            motion.sample(float("nan"), 0, 0, 20)


if __name__ == "__main__":
    unittest.main()
