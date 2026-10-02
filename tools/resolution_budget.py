"""
tools/resolution_budget.py
---------------------------
Reproduces the numbers in spacetime_circuits_dependency.md's "Bench-scale
resolution budget" section, and checks the two conclusions that section
leans on. Pure arithmetic — no hardware, no ngspice.

    python tools/resolution_budget.py

Exits non-zero if either check fails.
"""

import math
import sys

VREF = 3.3
ADC_BITS = 12
EPS0 = 8.854e-12  # F/m

# measurement_tools/capacitance_bridge/main.py polls the ADC about every
# 1ms and its README's Range table sets the Rref it assumes.
CAPBRIDGE_RREF = 100e3
CAPBRIDGE_SAMPLE_S = 1e-3


def adc_lsb_v() -> float:
    return VREF / 2**ADC_BITS


def quantization_rms_v() -> float:
    """RMS error of an ideal quantizer: LSB / sqrt(12)."""
    return adc_lsb_v() / math.sqrt(12)


def u16_count_v() -> float:
    """One MicroPython read_u16() count (the 12-bit result left-shifted)."""
    return VREF / 65535


def force_per_lsb_n(k_n_per_m: float, range_m: float, bits: float = ADC_BITS) -> float:
    """Force that moves a linear displacement sensor by one ADC step.

    The sensor's full range is assumed to span the ADC's 0-3.3V.
    """
    return k_n_per_m * range_m / 2**bits


def plate_capacitance_f(area_m2: float, gap_m: float) -> float:
    return EPS0 * area_m2 / gap_m


def main() -> int:
    print(f"ADC LSB: {adc_lsb_v()*1e3:.4f} mV  (one read_u16 count = {u16_count_v()*1e6:.2f} uV, 16 per LSB)")
    q = quantization_rms_v()
    print(f"ideal quantization noise: {q*1e3:.4f} mV rms = {q/u16_count_v():.2f} u16 counts")

    print("\nForce per ADC step, F = k * range / 2^bits (sensor range spans 0-3.3V)")
    print(f"{'range':>8} {'k (N/m)':>8} {'12 bit':>12} {'9 bit':>12}")
    for range_m in (1e-3, 10e-3):
        for k in (0.1, 1.0, 10.0):
            f12 = force_per_lsb_n(k, range_m)
            f9 = force_per_lsb_n(k, range_m, bits=9)
            print(f"{range_m*1e3:6.0f}mm {k:8.1f} {f12*1e9:9.1f} nN {f9*1e9:9.1f} nN")

    print("\nParallel-plate sensor, C = eps0 * A / d")
    for area_cm2, gap_mm in ((4, 1.0), (25, 1.0), (100, 1.0)):
        c = plate_capacitance_f(area_cm2 * 1e-4, gap_mm * 1e-3)
        t63 = CAPBRIDGE_RREF * c
        print(
            f"A={area_cm2:3d}cm2 d={gap_mm}mm: C={c*1e12:5.1f}pF, "
            f"CAPBRIDGE t63={t63*1e6:5.1f}us vs {CAPBRIDGE_SAMPLE_S*1e6:.0f}us sample interval"
        )

    failures = []

    # u16-count std-dev figures near 5 counts / 0.25mV are the ideal quantizer's
    # own noise, i.e. a floor on how quiet a reading can look, not a resolution.
    if not (4.0 < q / u16_count_v() < 5.0):
        failures.append("quantization noise is no longer ~4.6 u16 counts")

    # A plate pair of any size a bench sensor would use charges through
    # CAPBRIDGE's Rref in well under one sample interval, which that
    # circuit's own README lists as unusable.
    biggest_plate_t63 = CAPBRIDGE_RREF * plate_capacitance_f(100e-4, 1e-3)
    if not biggest_plate_t63 < 0.05 * CAPBRIDGE_SAMPLE_S:
        failures.append("a 100cm2/1mm plate no longer charges faster than the sample interval")

    print()
    if failures:
        for msg in failures:
            print(f"[FAIL] {msg}")
        return 1
    print("[PASS] quantization noise ~4.6 u16 counts (the <5 counts / <0.25mV figure)")
    print("[PASS] plate-pair capacitance is far below CAPBRIDGE's usable range")
    return 0


if __name__ == "__main__":
    sys.exit(main())
