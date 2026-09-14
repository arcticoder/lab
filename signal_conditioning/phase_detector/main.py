"""
main.py — phase_detector

Drives the PWM reference (input 1B) and streams the filtered XOR output
(GP28) continuously. No PASS/FAIL verdict to print and exit on — the two
oscillators aren't phase-locked (see README.md's Design notes), so the
expected behavior is a slow, continuous sweep between ~0V and ~3.3V as
their relative phase drifts, not a fixed reading.

Wire per breadboard.md, then run with the Pico plugged in over USB:

    mpremote run main.py
"""

import machine
import time

PWM_FREQ_HZ = 1500  # near ne555_astable's own tuned frequency, see breadboard.md
pwm = machine.PWM(machine.Pin(16))  # any spare GPIO -> SN74HC86N pin 2 (1B)
pwm.freq(PWM_FREQ_HZ)
pwm.duty_u16(32768)  # 50% duty square wave

adc = machine.ADC(28)  # GPIO 28 = ADC2, wired to the Rf/Cf lowpass output
VREF = 3.3


def read_voltage(samples=20):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.0005)
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * VREF


while True:
    v = read_voltage()
    print(f"PHASED filtered output: {v:.3f} V")
    time.sleep(0.2)
