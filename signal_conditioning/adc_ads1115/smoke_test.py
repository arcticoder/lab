"""
smoke_test.py — adc_ads1115

Safety: the ADS1115's analog input must never leave GND-0.3V .. VDD+0.3V
(3.6V at 3.3V VDD), including when a sensor on psu_4xaa's 6.4V rail drives
the channel or something drives it negative, with either a 5k or an
op-amp-low source impedance; the clamp must not push more than a
milliamp into the 3V3 rail; and the driver only ever writes the ADS1115's
own address and registers, with its comparator disabled.

Functional: the input network passes a divider midpoint with under 0.5%
error and has its low-pass corner near 159Hz (1/(2*pi*10k*100nF)); the
config word and LSB table match the datasheet values; two's-complement
counts convert correctly; read_volts() against a simulated ADS1115 returns
the input to within one LSB; and the bench check's pass/fail logic passes a
healthy pair of readings and fails an offset Pico ADC, a noisy ADS1115 and
a floating (0V) input.
"""

import math
import os
import random
import sys
import types

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values, run_ngspice  # noqa: E402

SPICE = os.path.join(HERE, "adc_ads1115.spice")
VDD = 3.3
ABS_MIN, ABS_MAX = -0.3, VDD + 0.3
RIN, C, RADC, RSRC = 10e3, 100e-9, 6e6, 5e3

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


vals = parse_op_values(run_ngspice(SPICE))
out = run_ngspice(SPICE)
fc = float(next(ln.split("=")[1].split()[0] for ln in out.splitlines() if ln.strip().startswith("fc_hz")))

for name, v in (("6.4V, 5k source", vals["v_fault_hi"]), ("6.4V, low-Z source", vals["v_fault_hi_lowz"]), ("-1V", vals["v_fault_lo"])):
    check(f"smoke — input stays inside the ADS1115 limits at {name}", ABS_MIN < v < ABS_MAX, f"{v:.3f}V vs {ABS_MIN}..{ABS_MAX:.1f}V")
check(
    "smoke — clamp injects under 1mA into the 3V3 rail",
    abs(vals["i_fault_hi"]) < 1e-3,
    f"{abs(vals['i_fault_hi'])*1e6:.0f}µA",
)

expected_nom = 1.65 * RADC / (RADC + RSRC + RIN)
check(
    "functional — divider midpoint passes with under 0.5% error",
    abs(vals["v_nom"] - 1.65) / 1.65 < 0.005 and abs(vals["v_nom"] - expected_nom) < 1e-4,
    f"{vals['v_nom']:.4f}V (Rin/6Meg loading predicts {expected_nom:.4f}V)",
)
fc_expected = 1 / (2 * math.pi * RIN * C)
check(
    "functional — low-pass corner near 1/(2*pi*Rin*C)",
    abs(fc - fc_expected) / fc_expected < 0.05,
    f"{fc:.0f}Hz vs {fc_expected:.0f}Hz",
)

# The driver, against a mocked machine module.
sys.modules["machine"] = types.SimpleNamespace()
sys.path.insert(0, HERE)
import main as drv  # noqa: E402

check("functional — AIN0, +/-4.096V, 128SPS config word is 0xC383", drv.config_word(0) == 0xC383, hex(drv.config_word(0)))
check("functional — AIN3 selects MUX=111", (drv.config_word(3) >> 12) & 0x7 == 0b111, hex(drv.config_word(3)))
check("smoke — comparator disabled (QUE=11) in every config", all(drv.config_word(c, p) & 3 == 3 for c in range(4) for p in range(6)), "all 24 combos")
lsb_us = {p: round(drv.lsb_volts(p) * 1e6, 3) for p in range(6)}
check(
    "functional — LSB table matches the datasheet",
    lsb_us == {0: 187.5, 1: 125.0, 2: 62.5, 3: 31.25, 4: 15.625, 5: 7.812},
    str(lsb_us),
)
check(
    "functional — two's-complement counts convert",
    drv.counts_to_volts(0x7FFF) > 4.095 and drv.counts_to_volts(0xFFFF) == -drv.lsb_volts() and drv.counts_to_volts(0x8000) == -4.096,
    f"+FS={drv.counts_to_volts(0x7FFF):.4f}V, -1={drv.counts_to_volts(0xFFFF)*1e6:.0f}µV",
)


class FakeADS:
    """Just enough of an ADS1115 on an I2C bus: single-shot reads of a fixed voltage."""

    def __init__(self, volts):
        self.volts = volts
        self.writes = []
        self.config = 0x8583

    def writeto_mem(self, addr, reg, data):
        self.writes.append((addr, reg, bytes(data)))
        self.config = int.from_bytes(data, "big")

    def readfrom_mem(self, addr, reg, n):
        if reg == drv.REG_CONFIG:
            return (self.config | 0x8000).to_bytes(2, "big")
        pga = (self.config >> 9) & 7
        counts = round(self.volts / drv.PGA_FSR[pga] * 32768)
        counts = max(-32768, min(32767, counts))
        return (counts & 0xFFFF).to_bytes(2, "big")


ads = FakeADS(1.650)
v = drv.read_volts(ads)
check("functional — read_volts returns the input to within one LSB", abs(v - 1.650) <= drv.lsb_volts(), f"{v:.5f}V")
check(
    "smoke — driver writes only 0x48's config register",
    all(a == 0x48 and r == drv.REG_CONFIG for a, r, _ in ads.writes) and len(ads.writes) == 1,
    f"{[(hex(a), r) for a, r, _ in ads.writes]}",
)

random.seed(1)
good_ads = [1.646 + random.gauss(0, 150e-6) for _ in range(64)]
good_pico = [1.652 + random.gauss(0, 400e-6) for _ in range(64)]
check("functional — healthy readings pass the bench check", all(ok for _, ok, _ in drv.evaluate(good_ads, good_pico)), "ADS 1.646V, Pico 1.652V")
check("functional — a 60mV-offset Pico ADC fails", not all(ok for _, ok, _ in drv.evaluate(good_ads, [x + 0.06 for x in good_pico])), "agreement check")
check("functional — a noisy ADS1115 fails", not all(ok for _, ok, _ in drv.evaluate([x + random.gauss(0, 3e-3) for x in good_ads], good_pico)), "steadiness check")
check("functional — a floating (0V) input fails", not all(ok for _, ok, _ in drv.evaluate([0.0] * 64, [0.0] * 64)), "expected-value check")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
