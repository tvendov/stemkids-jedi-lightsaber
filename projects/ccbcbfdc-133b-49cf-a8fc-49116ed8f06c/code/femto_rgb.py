"""FEMTO LEDOUT: 1 бордов + N външни RGB пиксела. Хардуерно непроверен пример."""


def demonstrate(external_count=5, sleep_ms=None):
    # Началният опит е само с кратък сегмент. Това не е номинален токов лимит.
    if type(external_count) is not int or not 1 <= external_count <= 5:
        raise ValueError("Use 1..5 external pixels for this bench example")
    from machine import Pin, WS2812
    if sleep_ms is None:
        from time import sleep_ms

    power = Pin("P500", Pin.OUT, value=0)
    data = Pin("P112", Pin.OUT, value=0)
    strip = None
    try:
        power.value(1)
        sleep_ms(100)
        # LEDOUT е след бордовия пиксел: той заема индекс 0.
        strip = WS2812(pixel_count=external_count + 1, pin=data, channels=3)
        strip.fill((0, 0, 0))
        strip.write()
        for color in ((20, 0, 0), (0, 20, 0), (0, 0, 20)):
            for index in range(1, external_count + 1):
                strip[index] = color
                strip.write()
                sleep_ms(150)
            sleep_ms(500)
    finally:
        # Изключваме захранването дори ако записът или deinit дадат грешка.
        try:
            if strip is not None:
                strip.fill((0, 0, 0))
                strip.write()
        finally:
            try:
                if strip is not None:
                    strip.deinit()
            finally:
                power.value(0)


# Не използвай UART(2)/SPI(2) едновременно: machine.WS2812 заема SCI2.
# VLED -> захранване на краткия сегмент, LEDOUT -> 330 ohm -> DIN, обща GND.
# Преди изпълнение: проверени монтаж, ток и подходящ MicroPython build.
if __name__ == "__main__":
    demonstrate()
