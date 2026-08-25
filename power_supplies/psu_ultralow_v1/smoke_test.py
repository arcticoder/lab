"""
smoke_test.py — psu_ultralow_v1

Rload in the netlist is a simulated representative downstream load, not a
physical part (see breadboard.md — nothing in the parts list), so there's
no physical-resistor wattage to check here. Checks instead: output stays
within a sane fraction of the 1.5V cell (no runaway/negative voltage from a
netlist typo), and the polyfuse's cold-state resistance approximation is
actually doing something (current isn't absurdly high, which would mean
the fuse model got dropped or shorted).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "psu_ultralow_v1.spice")
VBATT = 1.5
EXPECTED_VOUT = 1.44  # V, at nominal Rload=15ohm per README "Expected behaviour"
TOLERANCE = 0.10

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_out = values["v(3)"]
i_batt = abs(values["i(vbatt)"])

check(
    "smoke — output voltage within cell voltage",
    0 < v_out <= VBATT,
    f"v(3)={v_out:.3f}V, battery={VBATT}V (output can't exceed the unregulated source)",
)

check(
    "functional — nominal output matches documented design point",
    abs(v_out - EXPECTED_VOUT) / EXPECTED_VOUT < TOLERANCE,
    f"v(3)={v_out:.3f}V vs expected {EXPECTED_VOUT}V (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "smoke — nominal-load current is plausible (not shorted)",
    0 < i_batt < 0.5,
    f"i(vbatt)={i_batt*1000:.1f}mA — should be tens of mA at this load, not amps",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
