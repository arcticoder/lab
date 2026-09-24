"""
smoke_test.py — accelerometer_interface

Nothing analog is conditioned here — the GY-521's MPU-6050 digitizes on
the module — so the checks are the two electrical things that can break
the link: the I2C bus timing (open-drain lines charged by pull-ups) and
the supply (psu_pico_rail, ~100mA budget).

Safety: the pull-up's worst-case sink current (2.2k, a lower value than
a typical GY-521 carries) must stay inside the I2C 3mA limit, the low
level must stay under the 0.4V logic-low limit, and the module's draw
must sit well inside the Pico rail's budget.

Functional: the bus's 30%->70% rise time must meet I2C standard mode
(1000ns, what main.py runs at) across the pull-up values a GY-521 could
plausibly carry and up to 100pF of wiring, and fast mode (300ns) at the
design point (4.7k, 50pF) so 400kHz is available if the wiring stays
short. The pull-up value on this specific board is an assumption (see the
netlist) — the sweep exists so the result doesn't hinge on it.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import run_ngspice

SPICE_FILE = os.path.join(os.path.dirname(__file__), "accelerometer_interface.spice")
VDD = 3.3
SINK_LIMIT_A = 3e-3  # I2C spec, 3mA sink
VOL_LIMIT_V = 0.4
STD_MODE_TR_S = 1000e-9
FAST_MODE_TR_S = 300e-9
RAIL_BUDGET_A = 0.100
MPU_VDD_MIN_V = 2.375  # MPU-6050 datasheet minimum VDD

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


out = run_ngspice(SPICE_FILE)
rises = {}
rail = None
for line in out.splitlines():
    parts = line.split()
    if parts and parts[0] == "RISE":
        rpu, cbus, tr, vlow = (float(x) for x in parts[1:5])
        rises[(rpu, cbus)] = (tr, vlow)
    elif parts and parts[0] == "RAIL":
        rail = (float(parts[1]), float(parts[2]))

check("functional — all 9 pull-up/capacitance cases simulated", len(rises) == 9, f"{len(rises)} cases")

min_rpu = min(k[0] for k in rises)
check(
    "smoke — worst-case pull-up sink current inside the I2C 3mA limit",
    VDD / min_rpu < SINK_LIMIT_A,
    f"{VDD/min_rpu*1000:.2f}mA at {min_rpu/1000:.1f}k",
)
worst_vlow = max(v for _, v in rises.values())
check(
    "smoke — bus logic-low level under 0.4V",
    worst_vlow < VOL_LIMIT_V,
    f"worst {worst_vlow*1000:.0f}mV (Pico pad ~50 ohm into the lowest pull-up)",
)

if rail is None:
    check("smoke — supply operating point simulated", False, "no RAIL line")
else:
    v_mod, i_mod = rail
    check(
        "smoke — module current well inside psu_pico_rail's ~100mA budget",
        i_mod < RAIL_BUDGET_A * 0.5,
        f"{i_mod*1000:.1f}mA modeled (MPU-6050 ~3.9mA + board LED/regulator) vs {RAIL_BUDGET_A*1000:.0f}mA budget",
    )
    check(
        "smoke — supply at the module stays above the MPU-6050's minimum VDD",
        v_mod > MPU_VDD_MIN_V + 0.5,
        f"{v_mod:.2f}V at the module vs {MPU_VDD_MIN_V}V minimum",
    )

design = rises[(4700.0, 50e-12)][0]
check(
    "functional — design point (4.7k, 50pF) meets fast-mode rise time (400kHz available)",
    design < FAST_MODE_TR_S,
    f"{design*1e9:.0f}ns vs {FAST_MODE_TR_S*1e9:.0f}ns",
)

std_ok = [
    (k, tr)
    for k, (tr, _) in rises.items()
    if k[1] <= 100e-12 or k[0] <= 4700.0
]
bad = [(k, tr) for k, tr in std_ok if tr >= STD_MODE_TR_S]
check(
    "functional — standard-mode (100kHz) rise time met for every pull-up up to 100pF, and for <=4.7k up to 200pF",
    not bad,
    f"{len(std_ok)} cases, slowest {max(tr for _, tr in std_ok)*1e9:.0f}ns vs {STD_MODE_TR_S*1e9:.0f}ns"
    if not bad
    else f"failing: {bad}",
)

corner = rises[(10000.0, 200e-12)][0]
print(f"[INFO] limit: 10k pull-up with 200pF of wiring rises in {corner*1e9:.0f}ns — over the standard-mode limit; keep jumpers short")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
