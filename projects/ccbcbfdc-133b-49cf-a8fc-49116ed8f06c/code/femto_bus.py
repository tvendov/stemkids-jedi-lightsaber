"""Начална FEMTO SoftI2C шина за SEN0250. Не е драйвер за измерване."""


def make_bus():
    from machine import Pin, SoftI2C
    # H1.3 = P001 (SCL); H1.4 = P002 (SDA). Pull-up само към 3.3 V.
    return SoftI2C(scl=Pin("P001"), sda=Pin("P002"), freq=100000)


if __name__ == "__main__":
    bus = make_bus()
    print("I2C адреси:", [hex(address) for address in bus.scan()])
    # SEN0250 фабрично е 0x69. ACK не доказва правилен chip ID или измерване.
