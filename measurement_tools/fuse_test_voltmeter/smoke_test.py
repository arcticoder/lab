"""
smoke_test.py — fuse_test_voltmeter

Safety: the 10 ohm test load resistor is a *physical* part of this bench
jig (unlike the PSU circuits' Rload, which is simulation-only), so its
power dissipation is a real overheating/smoke risk, not just a modeling
concern. The kit (SunFounder Thales) only stocks 1/4W resistors — there's
no >=1W part to reach for — so the RXEF050 jig's 10 ohm equivalent load is
built as a 2-series x 2-parallel bank of four 10 ohm 1/4W resistors
instead of one part; see breadboard.md. Functional: cold vs. tripped
readings must straddle main.py's LOW_VOLTAGE=0.5V trip threshold, or the
firmware's trip detection is wrong.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "fuse_test_voltmeter.spice")
RLOAD_OHM = 10.0
RLOAD_UNIT_RATING_W = 0.25  # actual kit resistor rating (1/4W), see pico/docs/inventory.md
LOW_VOLTAGE = 0.5  # must match main.py's trip threshold

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


values = get_op_values(SPICE_FILE)

# n_resistors: how many physical 10 ohm 1/4W resistors realize the 10 ohm
# equivalent load per breadboard.md — 1 for the RXEF005 jig, 4 for the
# RXEF050 jig's 2-series x 2-parallel bank (power splits evenly across all
# four in that symmetric network).
for tier, cold_key, trip_key, vbatt, n_resistors in (
    ("v1 (RXEF005)", "v(11)", "v(12)", 1.5, 1),
    ("v2 (RXEF050)", "v(21)", "v(22)", 3.0, 4),
):
    v_cold = values[cold_key]
    v_trip = values[trip_key]

    p_cold_total = v_cold**2 / RLOAD_OHM
    p_cold_per_resistor = p_cold_total / n_resistors
    check(
        f"{tier} smoke — load resistor power per unit (cold)",
        p_cold_per_resistor < RLOAD_UNIT_RATING_W,
        f"{p_cold_per_resistor:.3f}W per resistor ({n_resistors}x 10ohm 1/4W, "
        f"{p_cold_total:.3f}W total across the {RLOAD_OHM}ohm equivalent load), "
        f"rated {RLOAD_UNIT_RATING_W}W each",
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
