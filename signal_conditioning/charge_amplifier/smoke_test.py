"""
smoke_test.py — charge_amplifier

Safety: draws nA-scale current off psu_pico_rail's 3.3V/~100mA budget —
no realistic overheating/overvoltage risk. What matters here is the
functional claim: the bias divider must land at VCC/2, the virtual input
must sit at that same bias (confirms the feedback loop is closed), and
the output must track bias + Iq*Rf_bias — or the feedback network (Cf/
Rf_bias) or bias divider is wired wrong.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "charge_amplifier.spice")
IQ = 100e-9  # A, illustrative DC stand-in — see .spice header
RFB = 1e6  # ohms
VCC = 3.3  # V, psu_pico_rail
TOLERANCE = 0.02  # ideal E-element op-amp model — should track tightly

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_bias = values["v(2)"]
v_virt = values["v(3)"]
v_out = values["v(4)"]
expected_out = v_bias + IQ * RFB

check(
    "smoke — bias node never exceeds VCC",
    v_bias <= VCC,
    f"v(2)={v_bias:.4f}V <= {VCC}V",
)

check(
    "smoke — output never exceeds VCC",
    v_out <= VCC,
    f"v(4)={v_out:.4f}V <= {VCC}V",
)

check(
    "functional — 1Meg/1Meg divider lands the bias at VCC/2",
    abs(v_bias - VCC / 2) / (VCC / 2) < TOLERANCE,
    f"v(2)={v_bias:.4f}V vs VCC/2={VCC/2:.4f}V (within {TOLERANCE*100:.0f}%)",
)

check(
    "functional — virtual input is held at the bias node (feedback loop closed)",
    abs(v_virt - v_bias) / v_bias < TOLERANCE,
    f"v(3)={v_virt:.4f}V vs v(2)={v_bias:.4f}V (within {TOLERANCE*100:.0f}%)",
)

check(
    "functional — output tracks bias + Iq*Rf_bias",
    abs(v_out - expected_out) / expected_out < TOLERANCE,
    f"v(4)={v_out:.4f}V vs bias+Iq*Rfb={expected_out:.4f}V (within {TOLERANCE*100:.0f}%)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
