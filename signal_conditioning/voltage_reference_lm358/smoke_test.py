"""
smoke_test.py — voltage_reference_lm358

Safety: draws a few mA off psu_pico_rail's 3.3V, well within any resistor's
rating (1kohm at 1.65V is ~2.7mW) — no realistic overheating risk. What
matters here is the functional claim the circuit exists to demonstrate:
the buffered output must hold steady under load while the bare divider
sags, or the LM358 buffer isn't doing its job (missing feedback wire,
no power to the part, etc.).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "voltage_reference_lm358.spice")
VCC = 3.3
UNLOADED_REF = 1.65  # V, 1k/1k divider off 3.3V
TOLERANCE = 0.02  # buffered output should track the unloaded divider closely

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_bare_loaded = values["v(2a)"]
v_divider_unloaded = values["v(2b)"]
v_buffered_loaded = values["v(3b)"]

check(
    "smoke — no node exceeds VCC",
    v_bare_loaded < VCC and v_divider_unloaded < VCC and v_buffered_loaded < VCC,
    f"v(2a)={v_bare_loaded:.3f}V, v(2b)={v_divider_unloaded:.3f}V, v(3b)={v_buffered_loaded:.3f}V, all < {VCC}V",
)

check(
    "functional — unbuffered divider sags noticeably under load",
    v_bare_loaded < UNLOADED_REF * 0.8,
    f"v(2a)={v_bare_loaded:.3f}V is well below the unloaded {UNLOADED_REF}V "
    "(demonstrates why a buffer is needed)",
)

check(
    "functional — buffered output holds close to the unloaded reference under the same load",
    abs(v_buffered_loaded - v_divider_unloaded) / v_divider_unloaded < TOLERANCE,
    f"v(3b)={v_buffered_loaded:.3f}V vs unloaded divider {v_divider_unloaded:.3f}V "
    f"(within {TOLERANCE*100:.0f}%)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
