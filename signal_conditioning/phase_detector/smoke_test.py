"""
smoke_test.py — phase_detector

Safety: purely logic-level (0-3.3V) — no realistic overvoltage/current
risk. What matters here is the functional claim: the XOR truth table
(in-phase -> LOW, out-of-phase -> HIGH) must hold for both simulated
static cases, and the RC lowpass must pass a static (DC) level through
unattenuated — a real, continuously-toggling input would have this
filter average the duty cycle instead, but that behavior can only be
confirmed on real hardware (see README.md), not in a static op-point.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "phase_detector.spice")
VCC = 3.3
TOLERANCE = 0.02

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)

XOR_OUT_KEYS = ["v_xor_inphase", "v_out_inphase", "v_xor_outphase", "v_out_outphase"]

check(
    "smoke — no node exceeds VCC in either case",
    all(values[k] <= VCC for k in XOR_OUT_KEYS),
    f"xor/filtered-output nodes: {[f'{k}={values[k]:.3f}' for k in XOR_OUT_KEYS]}",
)

check(
    "functional — in-phase case (A=B=HIGH) reads XOR LOW",
    values["v_xor_inphase"] < 0.1,
    f"v_xor_inphase={values['v_xor_inphase']:.3f}V (expected ~0V)",
)

check(
    "functional — in-phase case's filtered output matches the XOR node (DC passes unattenuated)",
    abs(values["v_out_inphase"] - values["v_xor_inphase"]) < 0.01,
    f"v_out_inphase={values['v_out_inphase']:.3f}V vs v_xor_inphase={values['v_xor_inphase']:.3f}V",
)

check(
    "functional — out-of-phase case (A=HIGH, B=LOW) reads XOR HIGH",
    abs(values["v_xor_outphase"] - VCC) / VCC < TOLERANCE,
    f"v_xor_outphase={values['v_xor_outphase']:.3f}V (expected ~{VCC}V)",
)

check(
    "functional — out-of-phase case's filtered output matches the XOR node (DC passes unattenuated)",
    abs(values["v_out_outphase"] - values["v_xor_outphase"]) < 0.01,
    f"v_out_outphase={values['v_out_outphase']:.3f}V vs v_xor_outphase={values['v_xor_outphase']:.3f}V",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
