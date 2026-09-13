"""
main.py — transimpedance_amplifier

Streams the LM358 output (pin 1) voltage continuously — this is a light
sensor, not a fixed-target validation check, so there's no PASS/FAIL
verdict to print and exit on (see resistance_measurement/main.py for the
same reasoning applied to an unknown resistance instead of ambient
light).

Wire GP26 (ADC0) to LM358 pin 1 and a Pico GND pin to the LM358's own GND
(pin 4), then run with the Pico plugged in over USB:

    mpremote run main.py

Cover the photodiode with a finger (reading should drop toward 0V) or
point a flashlight at it (reading should rise) to confirm the circuit
responds to light — see breadboard.md's "Expected behavior".
"""

import machine
import time

adc = machine.ADC(26)  # GPIO 26 = ADC0, wired to LM358 pin 1
VREF = 3.3


def read_voltage(samples=50):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.001)
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * VREF


while True:
    v = read_voltage()
    print(f"TIA output: {v:.3f} V")
    time.sleep(0.5)
