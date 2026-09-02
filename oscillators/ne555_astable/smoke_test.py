"""
smoke_test.py — ne555_astable

Safety: the capacitor node (v(ct)) must never be asserted to exceed VCC by
the sim, and the discharge-pin current through Ra is bounded analytically
(the sim's own current probe on Ra isn't usable here - see the netlist's
header comment) at Vcc/(Ra+Ron), well under the NE555's discharge-sink
rating and Ra's 1/4W kit rating. Functional: the two simulated trimpot
settings (Rb=10k, Rb=2k) must each oscillate at a frequency and duty cycle
matching the standard 555 astable formulas within tolerance - confirming
the netlist models a real oscillator, not a stuck output.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from ngspice_runner import get_op_values

SPICE_FILE = os.path.join(os.path.dirname(__file__), "ne555_astable.spice")
VCC = 5.5  # psu_4xaa under this circuit's light load - see netlist header comment
RA = 1000.0
RON_DISCHARGE = 50.0  # typical saturated discharge-transistor on-resistance
C = 100e-9

TOLERANCE = 0.15  # generous: the behavioral model's idealized thresholds
# and Ron drift the simulated freq/duty a few % from the textbook formula

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def astable_formula(ra, rb, c):
    freq = 1.44 / ((ra + 2 * rb) * c)
    duty = (ra + rb) / (ra + 2 * rb)
    return freq, duty


values = get_op_values(SPICE_FILE)

# --- Safety ---
i_discharge = VCC / (RA + RON_DISCHARGE)
p_ra = i_discharge**2 * RA

check(
    "smoke — capacitor node never exceeds VCC",
    values["vct_max_lo"] <= VCC and values["vct_max_hi"] <= VCC,
    f"vct_max_lo={values['vct_max_lo']:.3f}V, vct_max_hi={values['vct_max_hi']:.3f}V, both <= {VCC}V",
)

check(
    "smoke — Ra (1/4W kit resistor) dissipation stays well under its rating",
    p_ra < 0.25 * 0.5,
    f"Ra dissipation ~{p_ra*1000:.1f}mW at Vcc/(Ra+Ron)~={i_discharge*1000:.2f}mA discharge current, "
    f"vs 250mW rated (checked at 50% margin)",
)

check(
    "smoke — discharge-pin sink current stays well under the NE555's rating",
    i_discharge < 0.02,
    f"~{i_discharge*1000:.2f}mA vs the NE555's ~200mA absolute max discharge-sink rating "
    "(checked against a conservative 20mA bound)",
)

# --- Functional: Rb=10k (lowest freq, most-square) ---
freq_lo_expected, duty_lo_expected = astable_formula(RA, 10_000.0, C)

check(
    "functional — Rb=10k frequency matches the 555 astable formula",
    abs(values["freq_lo"] - freq_lo_expected) / freq_lo_expected < TOLERANCE,
    f"freq_lo={values['freq_lo']:.1f}Hz vs formula {freq_lo_expected:.1f}Hz (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "functional — Rb=10k duty cycle matches the 555 astable formula",
    abs(values["duty_lo"] - duty_lo_expected) / duty_lo_expected < TOLERANCE,
    f"duty_lo={values['duty_lo']*100:.1f}% vs formula {duty_lo_expected*100:.1f}% (+/-{TOLERANCE*100:.0f}%)",
)

# --- Functional: Rb=2k (upper end of recommended trim range) ---
freq_hi_expected, duty_hi_expected = astable_formula(RA, 2_000.0, C)

check(
    "functional — Rb=2k frequency matches the 555 astable formula",
    abs(values["freq_hi"] - freq_hi_expected) / freq_hi_expected < TOLERANCE,
    f"freq_hi={values['freq_hi']:.1f}Hz vs formula {freq_hi_expected:.1f}Hz (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "functional — Rb=2k duty cycle matches the 555 astable formula",
    abs(values["duty_hi"] - duty_hi_expected) / duty_hi_expected < TOLERANCE,
    f"duty_hi={values['duty_hi']*100:.1f}% vs formula {duty_hi_expected*100:.1f}% (+/-{TOLERANCE*100:.0f}%)",
)

check(
    "functional — frequency actually changes with the trimpot (not stuck)",
    values["freq_hi"] > values["freq_lo"] * 1.5,
    f"freq_hi={values['freq_hi']:.1f}Hz vs freq_lo={values['freq_lo']:.1f}Hz "
    "(Rb=2k must run meaningfully faster than Rb=10k)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)

print("\nAll checks passed.")
