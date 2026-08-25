"""
smoke_test.py — cd4066_switch_tester

Safety: sub-mA draw through two 10kohm bias resistors off a 3.3V rail —
no realistic overheating risk. Functional: the whole point of this jig is
telling closed from open, so the two states must be clearly distinguishable
at the probe point (I/O B), not just "different by some tiny amount."
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "cd4066_switch_tester.spice")
VDD = 3.3
CLOSED_MIN = 1.0  # I/O B should read clearly high when the switch is closed
OPEN_MAX = 0.1  # and clearly low when open

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_closed = values["v(bc)"]
v_open = values["v(bo)"]

check(
    "smoke — no node exceeds VDD",
    values["v(ac)"] <= VDD and v_closed <= VDD and values["v(ao)"] <= VDD,
    f"v(ac)={values['v(ac)']:.3f}V, v(bc)={v_closed:.3f}V, v(ao)={values['v(ao)']:.3f}V, all <= {VDD}V",
)

check(
    "functional — I/O B reads clearly HIGH when switch is closed",
    v_closed > CLOSED_MIN,
    f"v(bc)={v_closed:.3f}V > {CLOSED_MIN}V",
)

check(
    "functional — I/O B reads clearly LOW when switch is open",
    v_open < OPEN_MAX,
    f"v(bo)={v_open:.6f}V < {OPEN_MAX}V",
)

check(
    "functional — closed vs. open states are unambiguously distinguishable",
    (v_closed - v_open) > 0.5,
    f"delta={v_closed - v_open:.3f}V (need > 0.5V so main.py's reading can't be misread)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
