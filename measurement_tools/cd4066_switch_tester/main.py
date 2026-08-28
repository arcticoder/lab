"""
cd4066_switch_tester/main.py
------------------------------
Pico bring-up jig for one CD4066B analog switch: drives the switch's
control pin and probes its I/O B pin, then reports PASS/FAIL against the
same thresholds smoke_test.py checks against the SPICE model, and exits —
see README.md for the pass/fail criteria. Run once per switch (1-4) on
each CD4066BCN before trusting it in a downstream design.

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
SETTLE_S = 0.05  # let the switch settle before reading
CYCLES = 5  # closed+open pairs to average before judging pass/fail

# Same thresholds smoke_test.py checks against the SPICE model — a switch
# that wouldn't pass the sim doesn't pass on real hardware either.
CLOSED_MIN = 1.0  # I/O B should read clearly high when closed
OPEN_MAX = 0.1  # and clearly low when open
MIN_DELTA = 0.5  # closed vs. open must be unambiguously distinguishable


def raw_to_voltage(raw: int) -> float:
    return raw * VREF / ADC_MAX


def main() -> None:
    print("cd4066_switch_tester — toggling control (GP15), probing I/O B (GP26)")
    closed_readings = []
    open_readings = []
    closed = True
    for _ in range(CYCLES * 2):
        CONTROL.value(closed)
        time.sleep(SETTLE_S)
        v = raw_to_voltage(ADC_PROBE.read_u16())
        state = "CLOSED" if closed else "OPEN"
        print(f"control={state:>6}  v(I/O B)={v:.3f}V")
        (closed_readings if closed else open_readings).append(v)
        closed = not closed
        time.sleep(SAMPLE_INTERVAL_S)

    v_closed = sum(closed_readings) / len(closed_readings)
    v_open = sum(open_readings) / len(open_readings)
    delta = v_closed - v_open

    checks = [
        (
            "I/O B reads clearly HIGH when closed",
            v_closed > CLOSED_MIN,
            f"avg v(closed)={v_closed:.3f}V > {CLOSED_MIN}V",
        ),
        (
            "I/O B reads clearly LOW when open",
            v_open < OPEN_MAX,
            f"avg v(open)={v_open:.3f}V < {OPEN_MAX}V",
        ),
        (
            "closed vs. open unambiguously distinguishable",
            delta > MIN_DELTA,
            f"delta={delta:.3f}V > {MIN_DELTA}V",
        ),
    ]

    print()
    passed = True
    for label, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}: {detail}")
        if not ok:
            passed = False

    print()
    if passed:
        print("RESULT: PASS — switch passes signal when closed, blocks it when open")
    else:
        print("RESULT: FAIL — see README.md § Expected behaviour for what this switch did instead")


if __name__ == "__main__":
    main()
