"""
smoke_test.py — active_current_limiter

Safety: confirms the normal-load case draws current well under both the
2A trip point and Rs's power rating, and that the sense node never
exceeds a safe level. Functional: the normal case's comparator must keep
the gate driven high (switch closed) below the trip point, and the
open-loop fault-level sense test must correctly read as a trip decision
(gate LOW) — see active_current_limiter.spice's header for why the fault
case is checked open-loop rather than as a closed-loop operating point
(a hard-trip comparator loop has no stable fixed point once tripped;
forcing one to converge in ngspice fails for the same electrical reason
real hardware would chatter at the boundary).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "active_current_limiter.spice")
I_LIMIT = 2.0  # A, trip point (Vref=0.2V / Rs=0.1ohm)
RS = 0.1  # ohms
RS_RATED_W = 0.25  # SunFounder Thales kit 1/4W resistors — Rs is a metal-film
# 1W part on hand (docs/parts_reference.md#metal-film-resistor-kit-1w-1), so this
# is a conservative bound, not the part's actual rating
VCC_LOGIC = 3.3

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
i_load = values["i_load"]
v_sense_normal = values["v(3)"]
v_gate_normal = values["v(4)"]
v_sense_fault = values["v(5)"]
v_gate_fault = values["v(6)"]

check(
    "smoke — normal-load current stays under the 2A trip point",
    i_load < I_LIMIT,
    f"i_load={i_load:.3f}A < {I_LIMIT}A",
)

check(
    "smoke — Rs dissipation in the normal case stays under a conservative 1/4W bound",
    i_load**2 * RS < RS_RATED_W,
    f"P={i_load**2 * RS * 1000:.2f}mW < {RS_RATED_W*1000:.0f}mW",
)

check(
    "functional — normal case: sense voltage stays below the 0.2V trip reference",
    v_sense_normal < 0.2,
    f"v(3)={v_sense_normal:.4f}V < 0.2V",
)

check(
    "functional — normal case: comparator holds the gate HIGH (switch closed)",
    abs(v_gate_normal - VCC_LOGIC) < 0.01,
    f"v(4)={v_gate_normal:.3f}V (expected ~{VCC_LOGIC}V)",
)

check(
    "functional — fault-level sense test (3A through Rs) reads above the 0.2V trip reference",
    v_sense_fault > 0.2,
    f"v(5)={v_sense_fault:.3f}V > 0.2V",
)

check(
    "functional — fault-level sense test correctly triggers a trip decision (gate LOW)",
    v_gate_fault < 0.1,
    f"v(6)={v_gate_fault:.3f}V (expected ~0V)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
