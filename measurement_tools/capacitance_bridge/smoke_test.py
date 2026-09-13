"""
smoke_test.py — capacitance_bridge

Safety: Rref (100k) limits any charge/discharge current to well under
3.3V/100k = 33uA regardless of Cx's value — far below any Pico GPIO's
sourcing limit and nowhere near enough to stress a 1/4W kit resistor.
What matters here is the functional claim: charging a known-nominal
Cx through Rref must cross 63.2% of Vin at t = Rref*Cx, or the timing
technique this circuit is built around doesn't actually recover the
right capacitance (wrong Rref value, Cx miswired, wrong threshold
voltage).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "capacitance_bridge.spice")
VIN = 3.3
RREF = 100e3  # ohms
CX_NOMINAL = 10e-6  # F, the netlist's design/test point
TOLERANCE = 0.02  # ideal RC model — should track the formula tightly

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
t63 = values["t63"]
c_measured = values["c_measured"]

i_peak = VIN / RREF
p_rref = i_peak**2 * RREF

check(
    "smoke — Rref (1/4W kit resistor) dissipation stays well under its rating",
    p_rref < 0.25 * 0.5,
    f"Rref dissipation ~{p_rref*1000:.3f}mW at peak charge current "
    f"{i_peak*1000:.3f}mA, vs 250mW rated (checked at 50% margin)",
)

expected_t63 = RREF * CX_NOMINAL

check(
    "functional — time to 63.2% of Vin matches Rref * Cx",
    abs(t63 - expected_t63) / expected_t63 < TOLERANCE,
    f"t63={t63:.4f}s vs Rref*Cx={expected_t63:.4f}s (within {TOLERANCE*100:.0f}%)",
)

check(
    "functional — derived capacitance matches the nominal design point",
    abs(c_measured - CX_NOMINAL) / CX_NOMINAL < TOLERANCE,
    f"c_measured={c_measured*1e6:.3f}uF vs nominal {CX_NOMINAL*1e6:.1f}uF "
    f"(within {TOLERANCE*100:.0f}%)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
