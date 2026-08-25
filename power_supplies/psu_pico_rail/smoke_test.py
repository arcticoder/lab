"""
smoke_test.py — psu_pico_rail

Rload is a simulated representative downstream load (no physical resistor
— circuits attach directly to the rail). Checks: output stays within the
3.3V source, and nominal-load current stays inside the ~100mA conservative
budget documented in README.md (this rail has no fuse of its own, so
"smoke" here means "don't quietly assume more current headroom than the
Pico's own regulator + logic draw can actually spare").
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "psu_pico_rail.spice")
VREG = 3.3
EXPECTED_VOUT = 3.11  # V, at nominal Rload=33ohm per README "Expected behaviour"
TOLERANCE = 0.10
BUDGET_A = 0.10  # conservative external current budget, see README.md

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_out = values["v(2)"]
i_reg = abs(values["i(vreg)"])

check(
    "smoke — output voltage within regulator source voltage",
    0 < v_out <= VREG,
    f"v(2)={v_out:.3f}V, source={VREG}V",
)

check(
    "functional — nominal output matches documented design point",
    abs(v_out - EXPECTED_VOUT) / EXPECTED_VOUT < TOLERANCE,
    f"v(2)={v_out:.3f}V vs expected {EXPECTED_VOUT}V (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "smoke — nominal-load current stays within the conservative external budget",
    i_reg < BUDGET_A,
    f"i(vreg)={i_reg*1000:.1f}mA < {BUDGET_A*1000:.0f}mA budget",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
