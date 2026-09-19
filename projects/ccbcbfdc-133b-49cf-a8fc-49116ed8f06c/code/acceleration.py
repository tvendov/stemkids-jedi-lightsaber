"""Учебна обработка на ускорение X/Y/Z в m/s^2, без сензорен драйвер."""
import math


class Motion:
    def __init__(self, trigger=1.5, time_constant_ms=400):
        # Праговете са начални учебни стойности. Калибрират се на реалния корпус.
        if not math.isfinite(trigger) or trigger <= 0 or time_constant_ms <= 0:
            raise ValueError("motion settings")
        self.trigger = trigger
        self.time_constant_ms = time_constant_ms
        self.baseline = None
        self.moving = False

    def sample(self, x, y, z, dt_ms):
        values = (x, y, z)
        if not 0 < dt_ms <= 250 or not all(math.isfinite(v) for v in values):
            raise ValueError("acceleration sample")
        if self.baseline is None:
            self.baseline = list(values)
        # Бавният филтър следи постоянната съставка, включително гравитацията.
        dynamic = [values[i] - self.baseline[i] for i in range(3)]
        magnitude = math.sqrt(sum(v * v for v in dynamic))
        alpha = dt_ms / (self.time_constant_ms + dt_ms)
        for i in range(3):
            self.baseline[i] += alpha * dynamic[i]
        # Хистерезисът предотвратява бързо включване/изключване около прага.
        threshold = self.trigger * (0.65 if self.moving else 1.0)
        self.moving = magnitude >= threshold
        return {"xyz_m_s2": values, "dynamic_m_s2": magnitude,
                "moving": self.moving}


# Това не е пълно сливане на данни от акселерометър и жироскоп.
# При въртене се променя и гравитационният вектор; не изчисляваме ъгъл или скорост.
