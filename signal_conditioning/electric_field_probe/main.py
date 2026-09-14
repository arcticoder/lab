"""
main.py — electric_field_probe

Streams the TL082 output (pin 1) voltage continuously — this is a
qualitative field sensor, not a fixed-target validation check, so there's
no PASS/FAIL verdict to print and exit on (same reasoning as
transimpedance_amplifier/main.py for ambient light instead of a nearby
field).

Wire a Pico ADC-capable GPIO (e.g. GP27) to TL082 pin 1 and a Pico GND
pin to the TL082's own GND (pin 4), then run with the Pico plugged in
over USB:

    mpremote run main.py

Bring a charged object (a balloon or comb rubbed on hair or fabric) near
the electrode — the reading should deflect away from the ~1.65V rest
point (see breadboard.md's "Expected behavior") — and move it away to
watch the reading drift back.
"""

import machine
import time

adc = machine.ADC(27)  # GPIO 27 = ADC1, wired to TL082 pin 1
VREF = 3.3
BIAS = VREF / 2


def read_voltage(samples=50):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.001)
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * VREF


while True:
    v = read_voltage()
    print(f"EPFIELD output: {v:.3f} V  (deviation from rest: {v - BIAS:+.3f} V)")
    time.sleep(0.5)
