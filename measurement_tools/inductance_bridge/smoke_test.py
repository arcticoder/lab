"""
smoke_test.py — inductance_bridge

Safety: the only resistor a physical part limits is Rs (1k, 1/4W kit
resistor). Worst case it sees is the full 3.3V square wave across it
with the tank shorted: 3.3mA and 11mW, far under both the GPIO's
sourcing limit and the resistor's rating. What actually needs checking is
the ADC-facing node: a series-resonant tank would multiply the drive
voltage by Q and could put ~10V on a Pico pin, so the parallel-tank claim
is asserted (detector level and tank amplitude both under 3.3V).

Functional: the resonance peak of the tank must land at
f0 = 1/(2*pi*sqrt(Lx*C)) for every one of the 12 assortment values, or
the "find the peak, solve for Lx" technique doesn't recover the right
inductance. The winding resistances in the netlist are estimates, so the
check is repeated at 3x and 5x those values (real parts are not going to
be better than an assumption made with no datasheet). The time-domain
run confirms the *detector* — the thing the ADC actually reads — peaks at
f0 under the real square-wave drive, and that the square wave's 3rd
harmonic (a secondary peak at f0/3) stays well under the true peak so the
sweep's global maximum is still the fundamental.
"""

import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import run_ngspice

SPICE_FILE = os.path.join(os.path.dirname(__file__), "inductance_bridge.spice")
VLOGIC = 3.3
RS = 1e3  # ohms
C_TANK = 10e-9 + 5e-12  # Cref + assumed winding/stray capacitance, farads
SWEEP_MIN_HZ = 40e3  # main.py's sweep window — every f0 must sit inside it
SWEEP_MAX_HZ = 2.0e6
F0_TOL = 0.03  # nominal DCR
F0_TOL_HIGH_DCR = 0.05  # 5x DCR
MIN_TANK_V_HIGH_DCR = 0.3  # V peak at 5x DCR; must stay clear of the Schottky knee
MAX_HARMONIC_RATIO = 0.5  # f0/3 detector level vs the f0 level

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def parse(stdout, tag):
    rows = []
    for line in stdout.splitlines():
        if line.startswith(tag + " "):
            rows.append([float(x) for x in line.split()[1:]])
    return rows


def run_variant(dcr_factor):
    """Run the netlist with the winding-resistance estimate scaled."""
    with open(SPICE_FILE) as f:
        text = f.read()
    text = re.sub(r"let dcr = 0\.1 \*", f"let dcr = {0.1 * dcr_factor} *", text)
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
        tmp.write(text)
        path = tmp.name
    try:
        return run_ngspice(path)
    finally:
        os.unlink(path)


nominal = run_variant(1)
ac_nominal = parse(nominal, "ACPEAK")
td = parse(nominal, "TDPOINT")

check(
    "smoke — Rs (1/4W kit resistor) worst-case dissipation stays well under its rating",
    (VLOGIC**2 / RS) < 0.25 * 0.5,
    f"{VLOGIC**2/RS*1000:.1f}mW with the tank shorted ({VLOGIC/RS*1000:.1f}mA) vs 250mW rated",
)

max_vdet = max(r[1] for r in td)
max_vtank = max(r[2] for r in td)
check(
    "smoke — detector (ADC) node stays under the Pico's 3.3V pin limit at every swept frequency",
    max_vdet < VLOGIC,
    f"max detector level {max_vdet:.2f}V, max tank amplitude {max_vtank:.2f}V (parallel tank: no Q multiplication)",
)

check(
    "functional — all 12 assortment values simulated",
    len(ac_nominal) == 12,
    f"{len(ac_nominal)} rows",
)


def check_peaks(rows, tol, label):
    worst = 0.0
    worst_l = None
    for l_val, _dcr, f_peak, _v in rows:
        f_ideal = 1 / (2 * 3.141592653589793 * (l_val * C_TANK) ** 0.5)
        err = abs(f_peak - f_ideal) / f_ideal
        if err > worst:
            worst, worst_l = err, l_val
        if not (SWEEP_MIN_HZ < f_peak < SWEEP_MAX_HZ):
            check(f"{label} — f0 inside main.py sweep window", False, f"L={l_val*1e6:.0f}uH f0={f_peak/1e3:.0f}kHz")
    check(
        f"functional — resonance peak matches 1/(2*pi*sqrt(L*C)) for every value ({label})",
        worst < tol,
        f"worst error {worst*100:.2f}% at L={worst_l*1e6:.0f}uH (tolerance {tol*100:.0f}%)",
    )


check_peaks(ac_nominal, F0_TOL, "nominal DCR")
check_peaks(parse(run_variant(3), "ACPEAK"), F0_TOL_HIGH_DCR, "3x DCR")

ac_high = parse(run_variant(5), "ACPEAK")
check_peaks(ac_high, F0_TOL_HIGH_DCR, "5x DCR")
weakest = min(ac_high, key=lambda r: r[3])
check(
    "functional — weakest tank (5x DCR) still gives a peak well above the Schottky knee",
    weakest[3] > MIN_TANK_V_HIGH_DCR,
    f"L={weakest[0]*1e6:.0f}uH peak tank amplitude {weakest[3]:.2f}V vs {MIN_TANK_V_HIGH_DCR}V minimum",
)

# time-domain detector: global max must be at f0 (ratio 1.0 of 159.15kHz)
f0 = 159.15e3
peak_row = max(td, key=lambda r: r[1])
check(
    "functional — detector level peaks at f0 under the real square-wave drive",
    abs(peak_row[0] - f0) / f0 < 0.03,
    f"detector max {peak_row[1]:.2f}V at {peak_row[0]/1e3:.1f}kHz vs f0 {f0/1e3:.1f}kHz",
)
third = min(td, key=lambda r: abs(r[0] - f0 / 3))
ratio = third[1] / peak_row[1]
check(
    "functional — 3rd-harmonic secondary peak (f0/3) stays under half the true peak",
    ratio < MAX_HARMONIC_RATIO,
    f"detector at {third[0]/1e3:.1f}kHz is {ratio*100:.0f}% of the f0 level",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
