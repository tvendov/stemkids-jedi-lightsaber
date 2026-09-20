import unittest
from femto_buttons import DebouncedButton, BUTTON_PINS


def settle(button, value):
    return [button.update(value, 5) for _ in range(8)]


class ButtonsTest(unittest.TestCase):
    def test_exact_pins(self):
        self.assertEqual(BUTTON_PINS, ("P015", "P100"))

    def test_held_at_start_needs_release(self):
        button = DebouncedButton()
        self.assertFalse(any(settle(button, True)))
        self.assertFalse(any(settle(button, False)))
        self.assertEqual(sum(settle(button, True)), 1)
        self.assertFalse(any(settle(button, True)))

    def test_bounce_and_release(self):
        button = DebouncedButton()
        settle(button, False)
        self.assertFalse(any(button.update(i % 2 == 0, 5) for i in range(10)))
        self.assertEqual(sum(settle(button, True)), 1)
        settle(button, False)
        self.assertEqual(sum(settle(button, True)), 1)

    def test_independent_simultaneous_buttons(self):
        buttons = [DebouncedButton(), DebouncedButton()]
        for b in buttons:
            settle(b, False)
        self.assertEqual([sum(settle(b, True)) for b in buttons], [1, 1])

    def test_bad_input(self):
        for value in (0, -1, 1001):
            with self.assertRaises(ValueError):
                DebouncedButton(value)
        with self.assertRaises(ValueError):
            DebouncedButton().update(True, 251)
        with self.assertRaises(ValueError):
            DebouncedButton().update(0, 5)


if __name__ == "__main__":
    unittest.main()
