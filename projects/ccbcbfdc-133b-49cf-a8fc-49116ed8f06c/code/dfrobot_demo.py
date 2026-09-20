"""Шестосна симулация на SEN0250; няма I2C, LED или аудио изход."""
from imu_model import SwingControl


def main():
    print("СИМУЛАЦИЯ: DFRobot BMI160, ос Z по острието")
    control = SwingControl(blade_axis=2, bias_dps=(0, 0, 0))
    # Коефициентът се променя плавно с жироскопа, не само при един праг.
    for speed in (0, 30, 100, 200, 300, 100, 0):
        print("Замах:", control.sample((0, 0, 9.80665), (speed, 0, 0), 5))
    # Чистото въртене по Z не се превръща в напречен замах.
    control = SwingControl()
    print("Въртене:", control.sample((0, 0, 9.80665), (0, 0, 180), 5))
    print("Няма прясна проба:", control.sample(None, None, 5, sensor_ok=False))


if __name__ == "__main__":
    main()
