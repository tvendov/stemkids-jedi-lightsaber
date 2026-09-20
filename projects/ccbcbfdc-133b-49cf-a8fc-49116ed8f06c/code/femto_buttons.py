"""Два външни бутона на FEMTO; примерът отпечатва събития, без LED/звук."""

BUTTON_PINS = ("P015", "P100")


class DebouncedButton:
    def __init__(self, debounce_ms=25):
        if not isinstance(debounce_ms, int) or not 1 <= debounce_ms <= 1000:
            raise ValueError("debounce_ms must be 1..1000")
        self.debounce_ms = debounce_ms
        self.candidate = None
        self.stable = None
        self.elapsed = 0

    def update(self, pressed, dt_ms):
        if not isinstance(pressed, bool):
            raise ValueError("pressed must be bool")
        if not isinstance(dt_ms, int) or not 0 <= dt_ms <= 250:
            raise ValueError("dt_ms must be 0..250")
        if pressed != self.candidate:
            self.candidate, self.elapsed = pressed, 0
        else:
            self.elapsed = min(self.debounce_ms, self.elapsed + dt_ms)
        if self.elapsed < self.debounce_ms or self.stable == self.candidate:
            return False
        previous, self.stable = self.stable, self.candidate
        # Няма стартово включване при задържан бутон и няма auto-repeat.
        return previous is False and self.stable is True


def main():
    from machine import Pin
    from time import ticks_ms, ticks_diff, sleep_ms
    pins = [Pin(name, Pin.IN, Pin.PULL_UP) for name in BUTTON_PINS]
    buttons = [DebouncedButton(), DebouncedButton()]
    last = ticks_ms()
    print("S1 P015: включване/изключване; S2 P100: режим. Само събития.")
    while True:
        now = ticks_ms()
        dt, last = ticks_diff(now, last), now
        if not 0 <= dt <= 250:
            # След дълго блокиране изискваме отново стабилно отпускане.
            buttons = [DebouncedButton(), DebouncedButton()]
            dt = 0
        for index in range(2):
            if buttons[index].update(pins[index].value() == 0, dt):
                print("toggle" if index == 0 else "mode")
        sleep_ms(5)


if __name__ == "__main__":
    main()
