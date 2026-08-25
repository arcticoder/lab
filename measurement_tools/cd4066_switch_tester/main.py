"""
cd4066_switch_tester/main.py
------------------------------
Pico bring-up jig for one CD4066B analog switch: drives the switch's
control pin and probes its I/O B pin, printing whether the switch is
actually passing signal when told to close and blocking it when told to
open. Run once per switch (1-4) on each CD4066BCN before trusting it in a
downstream design — see README.md for the pass/fail criteria.

Hardware
--------
  GP15  — drives the switch's control pin (HIGH = closed, LOW = open)
  GP26 (ADC0) — probe lead, on the switch's I/O B pin (see breadboard.md)
  GND   — probe lead, shared reference

Run from MicroPico (or rshell / mpremote), Pico connected to the PC by USB:
  mpremote run main.py
"""

from machine import ADC, Pin
import time

CONTROL = Pin(15, Pin.OUT)
ADC_PROBE = ADC(Pin(26))

ADC_MAX = 65535
VREF = 3.3
SAMPLE_INTERVAL_S = 1.0


def raw_to_voltage(raw: int) -> float:
    return raw * VREF / ADC_MAX


def main() -> None:
    print("cd4066_switch_tester — toggling control (GP15), probing I/O B (GP26)")
    closed = True
    while True:
        CONTROL.value(closed)
        time.sleep(0.05)  # let the switch settle before reading
        v = raw_to_voltage(ADC_PROBE.read_u16())
        state = "CLOSED" if closed else "OPEN"
        print(f"control={state:>6}  v(I/O B)={v:.3f}V")
        closed = not closed
        time.sleep(SAMPLE_INTERVAL_S)


if __name__ == "__main__":
    main()
