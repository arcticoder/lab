"""
main.py — charge_amplifier

Streams the TL082 output (pin 1) voltage as fast as the Pico ADC allows —
a piezo tap is a fast transient (see breadboard.md's ~10ms settling
time), not a steady level, so this deliberately skips the multi-sample
averaging used elsewhere (raw_voltage_probe/transimpedance_amplifier)
that would smear a real tap out. There's no PASS/FAIL verdict to print
and exit on — this is a qualitative "watch it move when you tap the
piezo" check, same reasoning as electric_field_probe/main.py.

Wire a Pico ADC-capable GPIO (e.g. GP28) to TL082 pin 1 and a Pico GND
pin to the TL082's own GND (pin 4), then run with the Pico plugged in
over USB:

    mpremote run main.py

Tap or flex the piezo disc — the reading should show a brief transient
away from the ~1.65V rest point (see breadboard.md's "Expected
behavior"), settling back over roughly 10ms.
"""

import machine
import time

adc = machine.ADC(28)  # GPIO 28 = ADC2, wired to TL082 pin 1
VREF = 3.3
BIAS = VREF / 2


def read_voltage():
    raw = adc.read_u16()
    return (raw / 65535.0) * VREF


while True:
    v = read_voltage()
    print(f"CHGAMP output: {v:.3f} V  (deviation from rest: {v - BIAS:+.3f} V)")
    time.sleep(0.02)
