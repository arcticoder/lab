"""
main.py — vibration_driver (MicroPython, Raspberry Pi Pico)

Drives the S8050 switch's base (through the 1k resistor) from GP16 with
1kHz PWM and steps the duty from 0% to 100% in 10% steps, two seconds each,
printing every step. A coin/capsule vibration motor starts to buzz around
40-60% duty (it needs roughly 1.5-2V average to overcome static friction)
and is steady at 100%. Ctrl-C stops it and leaves the pin low, so the
transistor is off and the motor stops.

    mpremote run main.py
"""

from machine import PWM, Pin
import time

PIN = 16
FREQ_HZ = 1000
STEP_PCT = 10
STEP_S = 2


def start():
    pwm = PWM(Pin(PIN))
    pwm.freq(FREQ_HZ)
    pwm.duty_u16(0)
    return pwm


def set_duty(pwm, pct):
    pwm.duty_u16(min(max(pct, 0), 100) * 65535 // 100)


if __name__ == "__main__":
    pwm = start()
    try:
        for pct in range(0, 101, STEP_PCT):
            set_duty(pwm, pct)
            print(f"GP{PIN}: {pct}% duty")
            time.sleep(STEP_S)
        print("Holding 100%. Ctrl-C to stop.")
        while True:
            time.sleep(1)
    finally:
        pwm.deinit()
        Pin(PIN, Pin.OUT, value=0)
