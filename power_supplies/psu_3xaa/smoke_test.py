"""
smoke_test.py — psu_3xaa

Rload is a simulated representative downstream load (no physical resistor
in the parts list). Checks: output stays within the 3-cell source voltage,
Schottky forward drop is in its datasheet range (confirms the diode model
is oriented/conducting correctly, not reversed or shorted), and current
at the nominal load is plausible.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "psu_3xaa.spice")
VBATT = 4.5
EXPECTED_VOUT = 4.02  # V, at nominal Rload=15ohm per README "Expected behaviour"
TOLERANCE = 0.10
SCHOTTKY_DROP_MIN = 0.20
SCHOTTKY_DROP_MAX = 0.55  # 1N5817 datasheet range, ~0.35-0.45V typical at this current

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_out = values["v(5)"]
i_batt3 = abs(values["i(vbatt3)"])
schottky_drop = values["v(3)"] - values["v(4)"]

check(
    "smoke — output voltage within 3-cell source voltage",
    0 < v_out <= VBATT,
    f"v(5)={v_out:.3f}V, source={VBATT}V",
)

check(
    "functional — Schottky forward drop in datasheet range",
    SCHOTTKY_DROP_MIN < schottky_drop < SCHOTTKY_DROP_MAX,
    f"v(3)-v(4)={schottky_drop:.3f}V, expected {SCHOTTKY_DROP_MIN}-{SCHOTTKY_DROP_MAX}V (1N5817 forward drop)",
)

check(
    "functional — nominal output matches documented design point",
    abs(v_out - EXPECTED_VOUT) / EXPECTED_VOUT < TOLERANCE,
    f"v(5)={v_out:.3f}V vs expected {EXPECTED_VOUT}V (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "smoke — nominal-load current is plausible (not shorted)",
    0 < i_batt3 < 0.5,
    f"i(vbatt3)={i_batt3*1000:.1f}mA",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
