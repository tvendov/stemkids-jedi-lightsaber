"""RGB кадър за адресируеми LED. Само числа, без GPIO и без LED драйвер."""


def frame(state, count=24, color=(0, 180, 255)):
    if not isinstance(count, int) or not 1 <= count <= 300:
        raise ValueError("LED count")
    if len(color) != 3 or any(not isinstance(c, int) or not 0 <= c <= 255 for c in color):
        raise ValueError("RGB color")
    level, brightness = state["length_permille"], state["brightness"]
    if not 0 <= level <= 1000 or not 0 <= brightness <= 64:
        raise ValueError("effect state")
    result = []
    for index in range(count):
        # Всеки LED има собствена стойност. Граничният пиксел се запалва плавно.
        coverage = max(0, min(1000, level * count - index * 1000))
        result.append(tuple(c * brightness * coverage // (255 * 1000) for c in color))
    # Реалният драйвер трябва да превърне RGB в реда на конкретния модел LED.
    return result
