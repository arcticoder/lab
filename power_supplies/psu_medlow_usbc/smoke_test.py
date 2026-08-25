"""
smoke_test.py — psu_medlow_usbc

Rload is a simulated representative downstream load (no physical resistor
in the parts list — see README: "use a higher Rload for normal operation",
the 10ohm nominal point deliberately sits at the polyfuse's trip boundary).
Checks: output stays within the 5V USB rail, and current at the documented
nominal load sits near — not wildly past — the 500mA polyfuse rating (if
it were e.g. 5A, the cold-state fuse-resistance approximation in the
netlist would be wrong, not just "near the trip point").
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "psu_medlow_usbc.spice")
VUSB = 5.0
EXPECTED_VOUT = 4.76  # V, at nominal Rload=10ohm per README "Expected behaviour"
TOLERANCE = 0.10
FUSE_RATING_A = 0.5

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)
v_out = values["v(2)"]
i_usb = abs(values["i(vusb)"])

check(
    "smoke — output voltage within USB 5V rail",
    0 < v_out <= VUSB,
    f"v(2)={v_out:.3f}V, source={VUSB}V",
)

check(
    "functional — nominal output matches documented design point",
    abs(v_out - EXPECTED_VOUT) / EXPECTED_VOUT < TOLERANCE,
    f"v(2)={v_out:.3f}V vs expected {EXPECTED_VOUT}V (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "functional — nominal-load current is near the fuse's rated threshold, not far past it",
    FUSE_RATING_A * 0.7 < i_usb < FUSE_RATING_A * 1.5,
    f"i(vusb)={i_usb*1000:.1f}mA vs {FUSE_RATING_A*1000:.0f}mA fuse rating "
    "(this point is deliberately near the trip boundary by design)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
