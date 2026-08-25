"""
smoke_test.py — switch_pin_identifier

No physical power source beyond the Pico's own 3.3V pull-ups (~50 kohm,
sub-mA), so there's no meaningful smoke/overheating risk to check here.
What matters is that the model actually reproduces valid digital logic
levels: a floating pin reads solidly HIGH, a grounded pin reads solidly
LOW, so main.py's plain `.value()` read (no analog thresholding) will
classify them correctly.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "switch_pin_identifier.spice")
VDD = 3.3
DIGITAL_HIGH_MIN = 2.0  # comfortably above typical ~1.65V CMOS input threshold
DIGITAL_LOW_MAX = 0.8  # comfortably below it

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)

for node in ("a", "b2"):
    v = values[f"v({node})"]
    check(
        f"functional — pin {node.upper()} reads solid digital HIGH when floating",
        v > DIGITAL_HIGH_MIN,
        f"v({node})={v:.3f}V > {DIGITAL_HIGH_MIN}V",
    )
    check(
        f"smoke — pin {node.upper()} never exceeds VDD",
        v <= VDD,
        f"v({node})={v:.3f}V <= {VDD}V",
    )

v_b1 = values["v(b1)"]
check(
    "functional — active pin reads solid digital LOW when switch closes it to GND",
    v_b1 < DIGITAL_LOW_MAX,
    f"v(b1)={v_b1:.3f}V < {DIGITAL_LOW_MAX}V",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
