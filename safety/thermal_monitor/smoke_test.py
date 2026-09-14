"""
smoke_test.py — thermal_monitor

Safety: checks the alarm-LED branch's current and power stay within safe
bounds for the 220ohm/quarter-watt resistor and a generic LED (the GPIO
pin itself sees a similarly small current — see README.md). Functional:
the Rref/Rntc divider must land at VCC/2 at the MF52AT's 25C reference
resistance (10k) — confirms the divider math this circuit's whole
temperature conversion depends on (see main.py).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "thermal_monitor.spice")
VCC = 3.3  # V, psu_pico_rail
RLED = 220  # ohms
RLED_RATED_W = 0.25  # SunFounder Thales kit 1/4W resistors
TOLERANCE = 0.02

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_mid = values["v(2)"]
v_led = values["v(4)"]
i_gpio = abs(values["i(vgpio)"])
p_rled = i_gpio**2 * RLED

check(
    "smoke — alarm-LED current stays well under a GPIO pin's safe drive current",
    i_gpio < 0.012,
    f"i={i_gpio*1000:.2f}mA < 12mA (RP2040 recommended continuous-drive ceiling)",
)

check(
    "smoke — Rled dissipation stays under its 1/4W rating",
    p_rled < RLED_RATED_W,
    f"P={p_rled*1000:.2f}mW < {RLED_RATED_W*1000:.0f}mW",
)

check(
    "smoke — LED forward voltage stays under VCC",
    v_led < VCC,
    f"v(4)={v_led:.3f}V < {VCC}V",
)

check(
    "functional — Rref/Rntc divider lands at VCC/2 at the 25C reference resistance",
    abs(v_mid - VCC / 2) / (VCC / 2) < TOLERANCE,
    f"v(2)={v_mid:.4f}V vs VCC/2={VCC/2:.4f}V (within {TOLERANCE*100:.0f}%)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
