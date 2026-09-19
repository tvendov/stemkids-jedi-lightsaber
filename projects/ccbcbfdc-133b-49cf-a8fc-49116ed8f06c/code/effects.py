"""Учебен автомат за светлина и звук. Не управлява пинове или говорител."""


class Effects:
    def __init__(self):
        self.state = "OFF"
        self.level = 0
        self.cooldown_ms = 0

    def tick(self, dt_ms, button=False, moving=False, impact=False,
             low_battery=False):
        # Подаваме изминало време, а не абсолютен ticks_ms с възможно превъртане.
        if not isinstance(dt_ms, int) or not 0 <= dt_ms <= 250:
            raise ValueError("dt_ms must be 0..250")
        self.cooldown_ms = max(0, self.cooldown_ms - dt_ms)
        sound = None
        if low_battery:
            self.state = "FAULT"
            self.level = 0
            return self.output("mute")
        if self.state == "FAULT":
            # Не възстановяваме светлината автоматично след временен спад.
            return self.output(None)
        if button:
            if self.state in ("OFF", "RETRACTING"):
                self.state, sound = "IGNITING", "ignite"
            else:
                self.state, sound = "RETRACTING", "retract"
        if self.state == "IGNITING":
            self.level = min(1000, self.level + dt_ms * 2)
            if self.level == 1000:
                self.state = "ACTIVE"
        elif self.state == "RETRACTING":
            self.level = max(0, self.level - dt_ms * 2)
            if self.level == 0:
                self.state = "OFF"
        elif self.state == "ACTIVE" and not self.cooldown_ms:
            # Това са виртуални събития, а не готови прагове за реален IMU.
            if impact:
                sound, self.cooldown_ms = "accent", 300
            elif moving:
                sound, self.cooldown_ms = "swing", 300
        return self.output(sound)

    def output(self, sound):
        # 64/255 е учебен лимит, не гаранция за допустим ток на лентата.
        return {"state": self.state, "length_permille": self.level,
                "brightness": 64 * self.level // 1000, "sound": sound}
