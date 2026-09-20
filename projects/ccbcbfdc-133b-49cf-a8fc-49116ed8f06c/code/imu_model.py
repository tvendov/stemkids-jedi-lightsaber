"""BMI160 управляващ модел, не драйвер и не готов SmoothSwing audio mix."""
import math
from acceleration import Motion


def _vector(values):
    return (isinstance(values, (tuple, list)) and len(values) == 3
            and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                    and math.isfinite(v) for v in values))


class SwingControl:
    def __init__(self, blade_axis=2, bias_dps=(0, 0, 0)):
        if type(blade_axis) is not int or blade_axis not in (0, 1, 2) or not _vector(bias_dps):
            raise ValueError("IMU model configuration")
        # В демонстрацията Z е по дължината на острието. Монтажът се проверява.
        self.blade_axis = blade_axis
        self.bias = tuple(bias_dps)
        self.level = 0.0
        self.motion = Motion()

    def sample(self, acceleration_m_s2, gyro_dps, dt_ms, sensor_ok=True):
        if (isinstance(dt_ms, bool) or not isinstance(dt_ms, (int, float))
                or not math.isfinite(dt_ms) or not 0 < dt_ms <= 250):
            raise ValueError("sample interval")
        # sensor_ok включва прясна проба, успешен прочит и липса на насищане.
        if (sensor_ok is not True or not _vector(acceleration_m_s2) or not _vector(gyro_dps)
                or any(abs(v) > 8 * 9.80665 for v in acceleration_m_s2)
                or any(abs(v) > 2000 for v in gyro_dps)):
            self.level = 0.0
            self.motion = Motion()
            return {"valid": False, "swing_level": 0.0, "hum_level": 0.0,
                    "twist_dps": 0.0, "transverse_dps": 0.0,
                    "dynamic_m_s2": None}
        gyro = [gyro_dps[i] - self.bias[i] for i in range(3)]
        speed = math.sqrt(sum(gyro[i] ** 2 for i in range(3) if i != self.blade_axis))
        # Учебна крива: 15 dps мъртва зона, 300 dps достига пълен коефициент.
        # Тези стойности не са измерени настройки на бъдещия корпус.
        target = max(0.0, min(1.0, (speed - 15.0) / 285.0))
        self.level += dt_ms / (50.0 + dt_ms) * (target - self.level)
        motion = self.motion.sample(*acceleration_m_s2, dt_ms)
        return {"valid": True, "swing_level": self.level,
                "hum_level": 1.0 - 0.4 * self.level,
                "twist_dps": gyro[self.blade_axis], "transverse_dps": speed,
                "dynamic_m_s2": motion["dynamic_m_s2"]}


# Не се изчислява ориентация, абсолютна скорост, ударна сила или звук.
# Реалният драйвер преобразува raw counts според записания range и подава SI/dps.
