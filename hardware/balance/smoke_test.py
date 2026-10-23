"""
smoke_test.py — hardware/balance (the `FORCEBAL` torsion balance, gate G2/G3)

Model: the analytic model reproduces numbers published in two papers (stiffness, the 5 nm ->
12 nN conversion, drift, resonance, decay time, thermal-noise formula); the balance in
params.py has a resonance below the measurement frequency's neighbourhood and a strip stressed
far below yield; the eddy damper can supply the damping ratio the noise model assumes (by
partial engagement); the force-noise budget gives a go with margin, and the verdict flips
when the least certain assumption (air-speed fluctuation) is made four times worse.

CAD (needs cadquery; run with ~/.venvs/lab-hw/bin/python, otherwise these are SKIPPED, which
the repo-wide runner shows but does not fail): the moving assembly's mass and inertia agree
with params.py to 3%, its centre of mass is within 0.3 mm of the pivot axis, nothing collides
over +-1.5 degrees of swing, no moving parts overlap by accident, and every printed part fits the
printer.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import force_noise_budget as FB  # noqa: E402
import model as M  # noqa: E402
import params as P  # noqa: E402

failures = []


def check(label, condition, detail):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}: {detail}")
    if not condition:
        failures.append(label)


for label, ok, detail in FB.anchors():
    check(f"functional — model against the literature: {label}", ok, detail)

kappa, i, l = M.strip_stiffness(), M.inertia(), P.ARM_HALF_LENGTH
f0 = M.omega0(kappa, i) / (2 * math.pi)
check("functional — resonance is between 0.1 and 0.4 Hz (the measurement frequency sits below it)", 0.1 <= f0 <= 0.4 and P.F_MOD < f0, f"{f0:.3f} Hz, measured at {P.F_MOD} Hz")
stress = P.MOVING_MASS * P.G_ACC / (P.STRIP_WIDTH * P.STRIP_THICKNESS)
check("safety — the strip carries the balance at under a tenth of its yield stress", stress < P.STRIP_YIELD_PA / 10, f"{stress/1e6:.1f} MPa against {P.STRIP_YIELD_PA/1e6:.0f} MPa")
tilt_g = P.STRIP_WIDTH / P.STRIP_LENGTH
check("functional — the strip is wide enough to be a ribbon (width over 10x thickness) and and short", P.STRIP_WIDTH / P.STRIP_THICKNESS > 10 and P.STRIP_LENGTH < 60e-3, f"{P.STRIP_WIDTH/P.STRIP_THICKNESS:.0f}:1, {P.STRIP_LENGTH*1e3:.0f} mm")

c_vane, zeta_full, b_gap = M.eddy_damping_estimate()
check("functional — the N42 damper can supply the assumed damping (fully engaged it gives more, so it is tuned down)", zeta_full >= P.DAMPING_RATIO, f"estimated {zeta_full:.1f} fully engaged (B {b_gap:.2f} T between the discs, first-order estimate) against {P.DAMPING_RATIO} assumed")
check("safety — the damper magnets are fixed to the base: no permanent magnetic moment on the moving arm beyond the stray allowance", P.STRAY_MOMENT < 0.01 * P.n42_moment(), f"stray {P.STRAY_MOMENT:.0e} A*m^2 against one disc's {P.n42_moment():.3f} A*m^2")

f_max = P.plate_force(P.PLATE_BIAS_MAX)
g40 = P.plate_gain(P.PLATE_BIAS_MAX)
check("safety — the calibration plates reach micronewtons without exceeding the repo's 50 V DC line", P.PLATE_BIAS_MAX < 50 and f_max > 1e-6, f"{f_max*1e6:.1f} uN at {P.PLATE_BIAS_MAX:.0f} V ({P.PLATE_AREA*1e4:.0f} cm^2, {P.PLATE_GAP*1e3:.0f} mm gap)")
check("functional — a 1 mV step of the plate signal is under 1 nN (fine force control around the bias)", g40 * 1e-3 < 1e-9, f"{g40*1e9:.0f} nN/V at {P.PLATE_BIAS_MAX:.0f} V bias, 1 mV = {g40*1e-3*1e9:.2f} nN")
check("functional — the plates' force at the bias is within the strip's travel (displacement under 0.1 mm at 1 uN)", 1e-6 / M.k_eff(kappa, l) < 0.1e-3, f"1 uN moves the flag {1e-6/M.k_eff(kappa, l)*1e6:.0f} um, gap {P.PLATE_GAP*1e3:.0f} mm")

terms = M.force_terms()
sigma, need, ok = FB.verdict(terms)
check("functional — the budget's verdict is go with margin over the model-error allowance", ok and need / sigma > 2.0, f"predicted {sigma*1e9:.3f} nN per {P.INTEGRATION_S:.0f} s, need {need*1e9:.2f} nN ({need/sigma:.1f}x margin)")
dom = max(terms, key=terms.get)
check("functional — the dominant term is the least certain one (air currents), not the readout", dom == "air currents" and terms["readout (shot + electronics + LED)"] < 0.01 * terms[dom], f"{dom} {terms[dom]*1e9:.2f} nN/sqrt(Hz); readout {terms['readout (shot + electronics + LED)']*1e9:.4f}")
flips = [v for label, v, s_, ok_ in FB.sweeps() if label.startswith("air-speed") and not ok_]
check("functional — the verdict flips at about 4x worse air-speed fluctuation, so A5 must measure it", flips and min(flips) <= 4.01e-3, f"no-go from {min(flips)*1e3:.0f} mm/s" if flips else "never")
by_air = {v: s_ for label, v, s_, ok_ in FB.sweeps() if label.startswith("air-speed")}
check("functional — resolution worsens monotonically with air-speed fluctuation", all(by_air[a] < by_air[b] for a, b in zip(sorted(by_air), sorted(by_air)[1:])), "")

# ---- CAD -----------------------------------------------------------------------------------
try:
    import cadquery  # noqa: F401
    import balance as B
except ImportError:
    print("[SKIP] CAD checks: cadquery is not importable here; run with ~/.venvs/lab-hw/bin/python")
else:
    bl, cl = B.balance_solve()
    parts = B.build(bl, cl)
    m, com, izz, _ = B.moving_properties(parts)
    check("functional — CAD moving mass matches params.py to 3%", abs(m / 1e3 / P.MOVING_MASS - 1) < 0.03, f"{m:.1f} g against {P.MOVING_MASS*1e3:.1f} g")
    check("functional — CAD moment of inertia matches params.py to 3%", abs(izz / P.MOVING_INERTIA - 1) < 0.03, f"{izz:.3e} against {P.MOVING_INERTIA:.3e}")
    check("functional — the solved ballast puts the centre of mass within 0.3 mm of the pivot axis", math.hypot(com[0], com[1]) < 0.3, f"({com[0]:.2f}, {com[1]:.2f}) mm")
    check("functional — the ballast fits its pocket (under 24 mm)", bl < 24.0 and cl < 20.0, f"ballast {bl:.1f} mm, counter-mass {cl:.1f} mm")
    vol, who = B.interference(parts)
    check("functional — nothing collides with the fixed structure over +-1.5 degrees", vol < 0.01, f"{vol:.3f} mm^3 {who or ''}")
    over = B.moving_internal_overlaps(parts)
    check("functional — no moving parts overlap by accident", not over, f"{over}" if over else "none")
    bad = [n for n, d, fits in B.printability(parts) if not fits]
    check("functional — every printed part fits the printer's build volume", not bad, f"{bad}" if bad else f"{len(B.printability(parts))} parts")
    heavy = [n for n, d, _ in B.printability(parts) if min(d) < P.MIN_WALL * 1e3]
    check("smoke — no printed part is thinner than three perimeters", not heavy, f"{heavy}" if heavy else "all at least 1.2 mm")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
