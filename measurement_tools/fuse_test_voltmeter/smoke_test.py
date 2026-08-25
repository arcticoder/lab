"""
smoke_test.py — fuse_test_voltmeter

Safety: the 10 ohm test load resistor is a *physical* part of this bench
jig (unlike the PSU circuits' Rload, which is simulation-only), so its
power dissipation is a real overheating/smoke risk, not just a modeling
concern. Functional: cold vs. tripped readings must straddle main.py's
LOW_VOLTAGE=0.5V trip threshold, or the firmware's trip detection is wrong.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "fuse_test_voltmeter.spice")
RLOAD_OHM = 10.0
RLOAD_RATING_W = 1.0  # physical part is specified as >=1W, see breadboard.md
LOW_VOLTAGE = 0.5  # must match main.py's trip threshold

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)

for tier, cold_key, trip_key, vbatt in (("v1 (RXEF005)", "v(11)", "v(12)", 1.5), ("v2 (RXEF050)", "v(21)", "v(22)", 3.0)):
    v_cold = values[cold_key]
    v_trip = values[trip_key]

    p_cold = v_cold**2 / RLOAD_OHM
    check(
        f"{tier} smoke — load resistor power (cold)",
        p_cold < RLOAD_RATING_W,
        f"{p_cold:.3f}W dissipated in {RLOAD_OHM}ohm load, rated {RLOAD_RATING_W}W",
    )

    check(
        f"{tier} functional — cold reading above trip threshold",
        v_cold > LOW_VOLTAGE,
        f"{cold_key}={v_cold:.3f}V > {LOW_VOLTAGE}V (main.py would report this as NOT tripped)",
    )
    check(
        f"{tier} functional — tripped reading below trip threshold",
        v_trip < LOW_VOLTAGE,
        f"{trip_key}={v_trip:.3f}V < {LOW_VOLTAGE}V (main.py would report this as tripped)",
    )

    check(
        f"{tier} smoke — probe voltage within Pico ADC safe range",
        v_cold < 3.3 and v_trip < 3.3,
        f"cold={v_cold:.3f}V, tripped={v_trip:.3f}V, both < 3.3V ADC reference",
    )

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
