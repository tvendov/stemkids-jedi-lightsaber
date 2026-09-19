"""Симулация без LED лента, батерия, усилвател или сензор."""
from effects import Effects
from rgb_pixels import frame
from acceleration import Motion


def main():
    effect = Effects()
    print("СИМУЛАЦИЯ: бутонът и движението са предварително зададени.")
    print(effect.tick(0, button=True))
    for _ in range(5):
        state = effect.tick(100)
        print(state, "RGB:", frame(state, count=5))
    sensor = Motion()
    sensor.sample(0, 0, 9.80665, 20)  # Симулация: покой, земно ускорение по Z.
    motion = sensor.sample(3.0, 0, 9.80665, 20)  # Симулация: промяна по X.
    print("Ускорение:", motion)
    print(effect.tick(20, moving=motion["moving"]))
    print(effect.tick(100, button=True))
    for _ in range(4):
        print(effect.tick(100))
    # Ниският заряд има приоритет пред всички светлинни ефекти.
    print(effect.tick(100, low_battery=True))
    print(effect.tick(100, button=True))


if __name__ == "__main__":
    main()
