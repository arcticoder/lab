"""
main.py — capacitance_bridge

Streams a capacitance reading continuously (one discharge+charge+time
cycle per loop iteration) — this is a general-purpose instrument for
whatever unknown capacitor is currently wired into Cx, not a fixed-target
validation check, so there's no PASS/FAIL verdict to print and exit on
(same reasoning as measurement_tools/resistance_measurement/main.py,
which does the same thing for an unknown resistance).

Wire GP14 to Rref's input leg and GP26 (ADC0) to the Rref/Cx junction —
see breadboard.md. Run with the Pico plugged in over USB:

    mpremote run main.py
"""

import machine
import time

DRIVE_PIN = 14
ADC_PIN = 26
R_REF = 100_000.0  # ohms, known reference (SunFounder kit, see docs/inventory.md)
VIN = 3.3
THRESHOLD_V = VIN * (1 - 1 / 2.718281828)  # 63.2% of Vin = one RC time constant
DISCHARGE_THRESHOLD_V = VIN * 0.02  # "fully discharged" cutoff before timing a charge
TIMEOUT_S = 60.0  # covers the full electrolytic kit range up to 470uF
# (Rref*470uF = 47s, see README.md "Range") with margin, before giving up
# and reporting a fault rather than hanging forever. Applies to both the
# charge-timing loop and the discharge-wait loop below — a fixed sleep
# here would under-discharge the largest kit values (discharge follows
# the same RC time constant as charging).

drive = machine.Pin(DRIVE_PIN, machine.Pin.OUT)
adc = machine.ADC(ADC_PIN)


def read_voltage(samples=5):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * VIN


def measure_once():
    # Discharge Cx fully before timing a fresh charge — polled the same way
    # as the charge phase below, since discharge follows the same RC time
    # constant as charging and a fixed sleep would under-discharge a large Cx.
    drive.value(0)
    t_discharge_start = time.ticks_ms()
    while read_voltage() > DISCHARGE_THRESHOLD_V:
        if time.ticks_diff(time.ticks_ms(), t_discharge_start) / 1000.0 > TIMEOUT_S:
            return None
        time.sleep(0.001)

    t0 = time.ticks_ms()
    drive.value(1)
    while True:
        v = read_voltage()
        elapsed_s = time.ticks_diff(time.ticks_ms(), t0) / 1000.0
        if v >= THRESHOLD_V:
            return elapsed_s
        if elapsed_s > TIMEOUT_S:
            return None
        time.sleep(0.001)


while True:
    t63 = measure_once()
    if t63 is None:
        print(f"No 63.2% crossing within {TIMEOUT_S}s — Cx too large for Rref, or open/miswired")
    else:
        c_farads = t63 / R_REF
        print(f"t63={t63:.3f}s -> Cx={c_farads*1e6:.2f} uF")
