"""
smoke_test.py — transimpedance_amplifier

Safety: draws sub-mA (photocurrent + LM358 quiescent current) off
psu_low_v2's ~2.8V-at-light-load rail (see README.md) — no realistic
overheating or overvoltage risk from the current source itself. What
matters here is the functional claim: the inverting input must sit at
virtual ground (confirming the feedback loop is closed) and the output
must track Iph*Rf within the LM358's single-supply headroom, or the
photodiode/feedback wiring is wrong (missing feedback resistor, LM358
unpowered, photodiode reversed).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "transimpedance_amplifier.spice")
IPH = 10e-6  # A, illustrative bench-light value — see .spice header
RF = 100e3  # ohms
VCC = 2.8  # V, conservative psu_low_v2 rail estimate at this circuit's uA-scale
# load (see README.md — psu_low_v2's own 2.53V figure is measured at a much
# heavier 253mA design-point load; a near-zero-current load sags far less)
HEADROOM = 1.5  # V, typical LM358 single-supply output-swing ceiling below VCC
TOLERANCE = 0.02  # ideal E-element op-amp model — should track the formula tightly

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_virtual_gnd = values["v(2)"]
v_out = values["v(3)"]
expected_out = IPH * RF

check(
    "smoke — output stays within the LM358's single-supply swing ceiling",
    v_out < VCC - HEADROOM,
    f"v(3)={v_out:.3f}V vs ceiling {VCC - HEADROOM:.3f}V (VCC={VCC}V - {HEADROOM}V headroom)",
)

check(
    "smoke — output never exceeds VCC",
    v_out < VCC,
    f"v(3)={v_out:.3f}V < {VCC}V",
)

check(
    "functional — inverting input is held at virtual ground",
    abs(v_virtual_gnd) < 0.01,
    f"v(2)={v_virtual_gnd:.6f}V, within 10mV of 0V (confirms the feedback loop is closed)",
)

check(
    "functional — output tracks Iph * Rf",
    abs(v_out - expected_out) / expected_out < TOLERANCE,
    f"v(3)={v_out:.4f}V vs Iph*Rf={expected_out:.4f}V (within {TOLERANCE*100:.0f}%)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
