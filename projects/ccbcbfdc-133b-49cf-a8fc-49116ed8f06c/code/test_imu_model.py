"""Host проверки, без BMI160, истински звук или измерване на латентност."""
import unittest
from imu_model import SwingControl


class IMUModelTests(unittest.TestCase):
    def test_rest_and_twist_are_not_swing(self):
        model = SwingControl()
        rest = model.sample((0, 0, 9.80665), (0, 0, 0), 5)
        self.assertEqual(rest["swing_level"], 0)
        twist = model.sample((0, 0, 9.80665), (0, 0, 180), 5)
        self.assertEqual(twist["swing_level"], 0)
        self.assertEqual(twist["twist_dps"], 180)

    def test_smooth_rise_and_fall(self):
        model = SwingControl()
        levels = [model.sample((0, 0, 9.80665), (300, 0, 0), 5)["swing_level"]
                  for _ in range(30)]
        self.assertGreater(levels[0], 0)
        self.assertLess(levels[-1], 1)
        self.assertEqual(levels, sorted(levels))
        lower = model.sample((0, 0, 9.80665), (0, 0, 0), 5)
        self.assertLess(lower["swing_level"], levels[-1])

    def test_bias_and_mounting_axis(self):
        model = SwingControl(blade_axis=0, bias_dps=(1, 2, 3))
        sample = model.sample((0, 0, 9.80665), (101, 2, 3), 5)
        self.assertEqual(sample["swing_level"], 0)
        self.assertEqual(sample["twist_dps"], 100)

    def test_invalid_sample_mutes_coefficients(self):
        model = SwingControl()
        model.sample((0, 0, 9.80665), (300, 0, 0), 5)
        for acceleration, gyro, ok in ((None, None, False),
                                       ((0, 0, 9.8), (float("nan"), 0, 0), True),
                                       ((0, 0), (0, 0, 0), True),
                                       ((0, 0, 9.8), (1e300, 0, 0), True)):
            value = model.sample(acceleration, gyro, 5, ok)
            self.assertFalse(value["valid"])
            self.assertEqual(value["swing_level"], 0)
            self.assertEqual(value["hum_level"], 0)

    def test_invalid_configuration(self):
        for axis in (-1, 3, True):
            with self.assertRaises(ValueError):
                SwingControl(blade_axis=axis)
        for dt in (0, 251, float("nan"), True):
            with self.assertRaises(ValueError):
                SwingControl().sample((0, 0, 9.8), (0, 0, 0), dt)


if __name__ == "__main__":
    unittest.main()
