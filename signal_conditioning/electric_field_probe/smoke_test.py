"""
smoke_test.py — electric_field_probe

Safety: draws pA-to-nA-scale current off psu_pico_rail's 3.3V/~100mA
budget — no realistic overheating/overvoltage risk. What matters here is
the functional claim: the 1Meg/1Meg divider must land the electrode bias
at VCC/2, and the TL082 follower must actually track that bias (confirms
the feedback loop is closed) — if either check fails, the divider is
wired wrong or the follower's feedback path (pin 2 to pin 1) is open.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "electric_field_probe.spice")
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
v_out = values["v(3)"]

check(
    "smoke — bias node never exceeds VCC",
    v_bias <= VCC,
    f"v(2)={v_bias:.4f}V <= {VCC}V",
)

check(
    "smoke — buffered output never exceeds VCC",
    v_out <= VCC,
    f"v(3)={v_out:.4f}V <= {VCC}V",
)

check(
    "functional — 1Meg/1Meg divider lands the electrode bias at VCC/2",
    abs(v_bias - VCC / 2) / (VCC / 2) < TOLERANCE,
    f"v(2)={v_bias:.4f}V vs VCC/2={VCC/2:.4f}V (within {TOLERANCE*100:.0f}%)",
)

check(
    "functional — TL082 follower tracks the bias node",
    abs(v_out - v_bias) / v_bias < TOLERANCE,
    f"v(3)={v_out:.4f}V vs v(2)={v_bias:.4f}V (within {TOLERANCE*100:.0f}%)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
