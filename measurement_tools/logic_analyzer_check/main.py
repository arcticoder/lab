"""
main.py — logic_analyzer_check (MicroPython, Raspberry Pi Pico)

Drives a known square wave on GP15 for the CY7C68013A logic analyzer to
capture: 1kHz, 25% duty. The duty is deliberately not 50% so the capture
check can tell a true signal from an inverted one and a real duty cycle
from a stuck-at-half-level artifact.

Run:  mpremote run main.py     (Ctrl-C to stop; the pin goes quiet)
"""

from machine import PWM, Pin
import time

PIN = 15
FREQ_HZ = 1000
DUTY_PCT = 25


def start():
    pwm = PWM(Pin(PIN))
    pwm.freq(FREQ_HZ)
    pwm.duty_u16(DUTY_PCT * 65535 // 100)
    return pwm


if __name__ == "__main__":
    pwm = start()
    print(f"GP{PIN}: {FREQ_HZ}Hz, {DUTY_PCT}% duty. Capture it now; Ctrl-C to stop.")
    try:
        while True:
            time.sleep(1)
    finally:
        pwm.deinit()
