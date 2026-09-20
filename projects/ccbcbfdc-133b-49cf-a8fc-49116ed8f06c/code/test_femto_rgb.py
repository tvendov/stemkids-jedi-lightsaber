"""Host модел на RGB извикванията. Не изпълнява LED предаване."""
import sys
import types
import unittest
from unittest.mock import patch
from femto_rgb import demonstrate


class RGBTests(unittest.TestCase):
    def setup_hardware(self, failure=None):
        events = []

        class Pin:
            OUT = 1
            def __init__(self, name, mode, value):
                self.name = name
                events.append((name, value))
            def value(self, value):
                events.append((self.name, value))

        class WS2812:
            def __init__(self, pixel_count, pin, channels):
                self.pixels = [(0, 0, 0)] * pixel_count
                events.append(("init", pixel_count, pin.name, channels))
                if failure == "init":
                    raise OSError("simulated init failure")
            def __setitem__(self, index, color):
                self.pixels[index] = color
            def fill(self, color):
                self.pixels[:] = [color] * len(self.pixels)
            def write(self):
                events.append(("write", tuple(self.pixels)))
                if failure == "write":
                    raise OSError("simulated write failure")
            def deinit(self):
                events.append(("deinit",))
                if failure == "deinit":
                    raise OSError("simulated deinit failure")
        return types.SimpleNamespace(Pin=Pin, WS2812=WS2812), events

    def test_extra_onboard_pixel_and_cleanup(self):
        machine, events = self.setup_hardware()
        with patch.dict(sys.modules, machine=machine):
            demonstrate(sleep_ms=lambda ms: None)
        self.assertIn(("init", 6, "P112", 3), events)
        writes = [event[1] for event in events if event[0] == "write"]
        self.assertTrue(all(frame[0] == (0, 0, 0) for frame in writes))
        self.assertTrue(any(frame[5] != (0, 0, 0) for frame in writes))
        self.assertTrue(all(pixel == (0, 0, 0) for pixel in writes[-1]))
        self.assertEqual(events[-1], ("P500", 0))

    def test_power_off_even_on_driver_failure(self):
        for failure in ("init", "write", "deinit"):
            machine, events = self.setup_hardware(failure)
            with patch.dict(sys.modules, machine=machine):
                with self.assertRaises(OSError):
                    demonstrate(sleep_ms=lambda ms: None)
            self.assertEqual(events[-1], ("P500", 0))

    def test_reject_wrong_pixel_count(self):
        for count in (0, 6, True, 1.5):
            with self.assertRaises(ValueError):
                demonstrate(count)


if __name__ == "__main__":
    unittest.main()
