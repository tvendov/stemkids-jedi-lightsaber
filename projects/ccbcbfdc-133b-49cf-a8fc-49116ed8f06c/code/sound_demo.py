"""Кратък оригинален тестов тон, записан като WAV. Няма аудио възпроизвеждане."""
import math
import struct


def make_wav():
    rate, frequency, count = 16000, 180, 8000
    samples = bytearray(count)
    for i in range(count):
        # Плавната огъвка намалява щракването в началото и края.
        envelope = min(1.0, i / 400, (count - 1 - i) / 400)
        samples[i] = round(128 + 28 * envelope * math.sin(2 * math.pi * frequency * i / rate))
    header = struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + count,
                         b"WAVE", b"fmt ", 16, 1, 1, rate, rate, 1, 8,
                         b"data", count)
    return header + samples


if __name__ == "__main__":
    # Файлът е само материал за следващ тест с реалния аудио драйвер.
    with open("training_tone.wav", "wb") as file:
        file.write(make_wav())
    print("Записан е training_tone.wav; не е пускан към говорител.")
