"""
tools/force_noise_budget.py
----------------------------
End-to-end force-noise prediction for the torsion balance in hardware/balance
(`FORCEBAL`), the go/no-go gate (G3) before any schematic or layout work.

    python tools/force_noise_budget.py

It (1) checks the model against numbers published in two papers, (2) prints the
force-noise density of every term at the measurement frequency, the 1-sigma
resolution of one lock-in measurement, and a go/no-go against the claim in
hardware/balance/params.py, and (3) shows which assumed environmental values would
flip that verdict. Exits non-zero if an anchor check fails; the verdict itself is
printed, not an exit code, because it depends on assumptions the A5 prototype
check measures.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hardware", "balance"))
import model as M  # noqa: E402
import params as P  # noqa: E402

DAY = 86400.0


def anchors():
    """(label, ok, detail) for each published number the model is checked against."""
    out = []
    # [SR13] I = 0.0385 kg m^2, undamped omega_n = 2.240 rad/s -> kappa = I w^2, "around 0.0034 N m/deg"
    kappa = 0.0385 * 2.240**2
    out.append(("[SR13] kappa = I*w^2 gives their 0.0034 N*m/deg", abs(math.radians(1) * kappa - 0.0034) / 0.0034 < 0.03, f"{kappa*math.radians(1):.5f} N*m/deg"))
    # [SR13] arm radius 28.5 cm both for the force and the sensor; 5 nm -> 0.012 uN; 1.5 um -> 3.6 uN
    keff = 0.00345 / math.radians(1) / 0.285**2
    out.append(("[SR13] k_eff = kappa/l^2: 5 nm is their 0.012 uN", abs(keff * 5e-9 - 0.012e-6) / 0.012e-6 < 0.03, f"k_eff {keff:.3f} N/m, 5 nm = {keff*5e-9*1e6:.4f} uN"))
    out.append(("[SR13] 1.5 um of drift is their 3.6 uN", abs(keff * 1.5e-6 - 3.6e-6) / 3.6e-6 < 0.03, f"{keff*1.5e-6*1e6:.2f} uN"))
    # [CR22] kappa = 2.22e-8 N m/rad, I = 1.13e-5 kg m^2 -> 7.05 mHz; amplitude decay time 16.7-24.6 days for Q 3.2e4-4.7e4
    w0 = M.omega0(2.22e-8, 1.13e-5)
    out.append(("[CR22] resonance of kappa=2.22e-8, I=1.13e-5 is their 7.05 mHz", abs(w0 / (2 * math.pi) - 7.05e-3) / 7.05e-3 < 0.01, f"{w0/(2*math.pi)*1e3:.3f} mHz"))
    d1, d2 = 2 * 3.2e4 / w0 / DAY, 2 * 4.7e4 / w0 / DAY
    out.append(("[CR22] decay time 2Q/w is their 16.7 and 24.6 days", abs(d1 - 16.7) / 16.7 < 0.03 and abs(d2 - 24.6) / 24.6 < 0.03, f"{d1:.1f} and {d2:.1f} days"))
    # [CR22] Eq. 1 against an independent evaluation
    s = M.thermal_torque_density_structural(2.22e-8, 4.5e4, 2 * math.pi * 0.01, temp=5.0)
    ref = math.sqrt(4 * 1.380649e-23 * 5.0 * 2.22e-8 / (4.5e4 * 2 * math.pi * 0.01))
    out.append(("[CR22] Eq. 1 thermal torque noise at 5 K, 10 mHz", abs(s - ref) / ref < 1e-9, f"{s:.3g} N*m/sqrt(Hz)"))
    return out


def verdict(terms=None):
    terms = M.force_terms() if terms is None else terms
    sigma = M.resolution(M.total_density(terms))
    need = P.CLAIM_FORCE_N / (P.CLAIM_SIGMAS * P.MODEL_ERROR_FACTOR)
    return sigma, need, sigma <= need


def sweeps():
    """Resolution (1 sigma, one measurement) when one assumption changes."""
    rows = []
    base = P.AIR_SPEED_FLUCT, P.TEMP_NOISE, P.SPECTRAL_SLOPE, P.ARM_EXPANSION, P.DAMPING_RATIO
    try:
        for label, attr, vals in (
            ("air-speed fluctuation (m/s)", "AIR_SPEED_FLUCT", (1e-3, 2e-3, 4e-3, 1e-2)),
            ("temperature noise (K/sqrt(Hz))", "TEMP_NOISE", (1e-3, 3e-3, 1e-2)),
            ("spectral slope of the environment", "SPECTRAL_SLOPE", (1.0, 1.5, 2.0)),
            ("arm expansion coefficient (1/K)", "ARM_EXPANSION", (70e-6, 23e-6, 1e-6)),
            ("damping ratio", "DAMPING_RATIO", (0.2, 0.5, 1.0)),
        ):
            old = getattr(P, attr)
            for v in vals:
                setattr(P, attr, v)
                sigma, need, ok = verdict()
                rows.append((label, v, sigma, ok))
            setattr(P, attr, old)
    finally:
        P.AIR_SPEED_FLUCT, P.TEMP_NOISE, P.SPECTRAL_SLOPE, P.ARM_EXPANSION, P.DAMPING_RATIO = base
    return rows


def main() -> int:
    kappa, i, l = M.strip_stiffness(), M.inertia(), P.ARM_HALF_LENGTH
    k = M.k_eff(kappa, l)
    f0 = M.omega0(kappa, i) / (2 * math.pi)
    print("Balance (hardware/balance/params.py)")
    print(f"  torsion constant {kappa*1e6:.0f} uN*m/rad, inertia {i:.3e} kg*m^2, arm {l*1e3:.0f} mm")
    print(f"  resonance {f0:.3f} Hz (period {1/f0:.1f} s), k_eff {k:.4f} N/m: 1 uN moves the flag {1e-6/k*1e6:.1f} um")
    print(f"  measured at {P.F_MOD} Hz, {P.INTEGRATION_S:.0f} s per estimate (ENBW {1/(2*P.INTEGRATION_S)*1e3:.2f} mHz)")

    print("\nModel against published numbers")
    bad = 0
    for label, ok, detail in anchors():
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {detail}")
        bad += not ok

    terms = M.force_terms()
    dens = M.total_density(terms)
    xr, parts = M.displacement_noise_readout()
    print(f"\nForce-noise density at {P.F_MOD} Hz (readout {xr*1e12:.0f} pm/sqrt(Hz): shot {parts['shot']*1e12:.0f}, TIA {parts['tia']*1e12:.0f}, ADC {parts['adc']*1e12:.0f}, LED {parts['rin']*1e12:.0f} pm)")
    for name, v in sorted(terms.items(), key=lambda a: -a[1]):
        print(f"  {name:52s} {v*1e9:9.4f} nN/sqrt(Hz)")
    print(f"  {'total':52s} {dens*1e9:9.4f} nN/sqrt(Hz)")

    sigma, need, ok = verdict(terms)
    print(f"\nResolution of one {P.INTEGRATION_S:.0f} s measurement: {sigma*1e9:.3f} nN (1 sigma)")
    print(f"Claim: size a {P.CLAIM_FORCE_N*1e9:.0f} nN spurious-force term at {P.CLAIM_SIGMAS:.0f} sigma, with a {P.MODEL_ERROR_FACTOR:.0f}x allowance for the assumed terms")
    print(f"  needs sigma <= {need*1e9:.2f} nN; predicted {sigma*1e9:.3f} nN, margin {need/sigma:.1f}x over the allowance")
    print(f"  VERDICT: {'GO (conditional on A5 measuring the assumed environment)' if ok else 'NO-GO: change the mechanics, optics or environment and repeat'}")

    print("\nWhich assumption flips it (one change at a time)")
    for label, v, s, ok in sweeps():
        print(f"  {label:36s} {v:<9g} -> {s*1e9:7.3f} nN  {'go' if ok else 'NO-GO'}")

    print("\nLiterature (numbers as published; see docs/research_instrument_plan.md)")
    print("  [SR13] Soni & Roy: sensor noise 5 nm = 12 nN on a 2.4 N/m stand; 1.5 um drift over 8 h = 3.6 uN; 10 nN noise floor; lowest thrust measured 1.3 uN +/-20%")
    print(f"  this design: k_eff {k:.3f} N/m ({2.434/k:.0f}x softer), readout {xr*1e12:.0f} pm, predicted {sigma*1e9:.2f} nN per {P.INTEGRATION_S:.0f} s in air")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
