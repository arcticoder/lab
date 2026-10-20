"""
diagnose_levels.py — lockin_amplifier (MicroPython, Raspberry Pi Pico)

A power walk: reads the DC level on the GP28 jumper's row (and on A and B, GP26
and GP27) and says what kind of level it is. Put the GP28 jumper on one row,
run

    mpremote run diagnose_levels.py

then move it to the next row. The test pins GP6, GP8, GP9 and the demodulator
controls GP10, GP11 are all left high impedance or low, so nothing drives the
circuit.

Expected (3.3V supply, Rm1 10kΩ over Rm2 5.1kΩ):
  + rail, U1/U2 pin 8, S1/S2 pin 14        3.3V
  - rail, U1/U2 pin 4, S1/S2 pin 7         0V
  VMR, VMO, INN, C2, SIG (no signal)       about 1.115V  (3.3V x 5.1k / 15.1k)
  OUT1 (no signal)                         about 1.115V  (the stage's DC gain is 1)
A reading of 0V on VMR means Rm1 (10kΩ from the + rail) is open or its rows are
not the ones in the table; 0V on VMO with a good VMR means U1 pin 5, 6 or 7.
"""

import time
from machine import ADC, Pin, mem32

VMID = 3.3 * 5.1 / (10 + 5.1)


def classify(v):
    if v < 0.15:
        return "ground (0V)"
    if abs(v - VMID) < 0.12:
        return "Vmid (about 1.1V)"
    if v > 3.15:
        return "the 3.3V rail"
    return "neither ground, Vmid nor the rail"


def read(adc, n=20000):
    s = 0
    for _ in range(n):
        s += adc.read_u16()
    return s / n * 3.3 / 65535


def run():
    mem32[0x40050000 + 0xA0 + 0x3000] = 0xFF  # PWM slices off
    for p in (6, 8, 9):
        Pin(p, Pin.IN)
    Pin(10, Pin.OUT, value=0)  # demodulator switches open
    Pin(11, Pin.OUT, value=0)
    time.sleep(0.2)
    for name, pin in (("GP28 jumper row", 28), ("A (GP26)", 26), ("B (GP27)", 27)):
        v = read(ADC(pin))
        print(f"{name:16s} {v:.3f}V  {classify(v)}")


try:
    run()
finally:
    Pin(10, Pin.IN)
    Pin(11, Pin.IN)
