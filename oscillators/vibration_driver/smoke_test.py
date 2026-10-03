"""
smoke_test.py — vibration_driver

Safety: the transistor must never see more than its ratings. The motor is
modeled two ways, from the 2026-10-02 order's listing: running (3V / 90mA
rated maximum, 33 ohm) and stalled (3V / 120mA stall maximum, 25 ohm, no
back-EMF). In both the collector current must stay under the S8050's 500mA
and the switch must be saturated (Vce well under 0.5V). The running draw
must stay inside the Pico-rail budget; the stalled draw is known to exceed
that conservative budget (126mA vs 100mA), so the test pins it under half of
the Pico regulator's documented ~300mA instead, and asserts the overshoot
exists so the README's warning can't silently go stale. The GPIO must source
under its 4mA default drive, and the inductive turn-off spike must be
clamped by the flyback diode to just above the supply — without that diode
the same netlist spikes far past the S8050's 25V Vceo, which the test also
asserts so a "diode is optional" edit gets caught. The Pico script must
touch only GP16 and leave it low on exit.

Functional: GPIO high turns the motor on at about (VCC - Vce) / R_motor;
GPIO low turns it off (leakage under 1uA); the switch still saturates at a
pessimistic gain (hFE=50) with the running motor, so a low-gain S8050 from
the bin still works.
"""

import os
import re
import subprocess
import sys
import tempfile
import types

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values, run_ngspice  # noqa: E402

SPICE = os.path.join(HERE, "vibration_driver.spice")
VCC = 3.3
R_MOTOR = 33.0
IC_MAX = 0.5  # A, S8050 absolute maximum
VCEO = 25.0  # V, S8050 absolute maximum
GPIO_DRIVE = 4e-3  # A, Pico default pad drive strength
RAIL_BUDGET = 0.100  # A, power_supplies/psu_pico_rail's conservative external budget
R_STALL = 25.0  # ohm, 3V / 120mA stall maximum from the listing
STALL_LIMIT = 0.150  # A, half of the Pico regulator's documented ~300mA shared rating

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


vals = parse_op_values(run_ngspice(SPICE))
vce, ic, ib = vals["vce_on"], vals["ic_on"], vals["ib_on"]
expected_ic = (VCC - vce) / R_MOTOR

ic_st, vce_st = vals["ic_stall"], vals["vce_stall"]
check("smoke — collector current under the S8050's 500mA", max(ic, ic_st) < IC_MAX, f"running {ic*1e3:.1f}mA, stalled {ic_st*1e3:.1f}mA")
check("smoke — running draw within psu_pico_rail's ~100mA budget", ic <= RAIL_BUDGET, f"{ic*1e3:.1f}mA vs {RAIL_BUDGET*1e3:.0f}mA")
check("smoke — stalled draw under half the regulator's documented rating", ic_st < STALL_LIMIT, f"{ic_st*1e3:.1f}mA vs {STALL_LIMIT*1e3:.0f}mA")
check(
    "smoke — stalled draw does exceed the conservative budget (README warns about it)",
    ic_st > RAIL_BUDGET,
    f"{ic_st*1e3:.1f}mA vs {RAIL_BUDGET*1e3:.0f}mA",
)
check("smoke — switch stays saturated when the motor is stalled", vce_st < 0.5, f"Vce={vce_st:.3f}V, {vce_st*ic_st*1e3:.1f}mW")
check("smoke — switch is saturated (low dissipation)", vce < 0.5, f"Vce={vce:.3f}V, {vce*ic*1e3:.1f}mW")
check("smoke — GPIO sources less than its default drive", ib < GPIO_DRIVE, f"{ib*1e3:.2f}mA")
check(
    "smoke — flyback diode clamps the turn-off spike near the supply",
    vals["vpk"] < VCC + 0.8,
    f"collector peak {vals['vpk']:.2f}V vs VCC {VCC}V (+0.8V allowance for the diode drop)",
)

# Same netlist with the flyback diode removed.
with open(SPICE) as f:
    no_diode = "".join(ln for ln in f if not ln.startswith("Dfly"))
with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
    tmp.write(no_diode)
try:
    spike = parse_op_values(run_ngspice(tmp.name))["vpk"]
finally:
    os.unlink(tmp.name)
check("smoke — without the diode the spike would exceed Vceo", spike > VCEO, f"{spike:.0f}V vs {VCEO:.0f}V")

check(
    "functional — motor current is (VCC - Vce) / R_motor",
    abs(ic - expected_ic) / expected_ic < 0.02,
    f"{ic*1e3:.1f}mA vs {expected_ic*1e3:.1f}mA",
)
expected_st = (VCC - vce_st) / R_STALL
check(
    "functional — stalled current is (VCC - Vce) / R_stall",
    abs(ic_st - expected_st) / expected_st < 0.02,
    f"{ic_st*1e3:.1f}mA vs {expected_st*1e3:.1f}mA",
)
check("functional — GPIO low turns the motor off", vals["ic_off"] < 1e-6, f"{vals['ic_off']:.2e}A")

# Saturation margin at hFE=50: needs Ic/Ib_forced under 50.
hfe_forced = ic / ib
check("functional — saturates at hFE >= 50 (forced gain)", hfe_forced < 50, f"forced gain {hfe_forced:.0f}")

# main.py against a mocked machine module.
calls = {"duty": [], "pin": None, "freq": None, "out_value": None, "deinit": False}


class FakePWM:
    def __init__(self, pin):
        calls["pin"] = pin.num

    def freq(self, f):
        calls["freq"] = f

    def duty_u16(self, d):
        calls["duty"].append(d)

    def deinit(self):
        calls["deinit"] = True


class FakePin:
    OUT = 1

    def __init__(self, num, mode=None, value=None):
        self.num = num
        if mode == FakePin.OUT:
            calls["out_value"] = value


sys.modules["machine"] = types.SimpleNamespace(PWM=FakePWM, Pin=FakePin)
sys.path.insert(0, HERE)
import main as pico_main  # noqa: E402

pwm = pico_main.start()
pico_main.set_duty(pwm, 50)
pico_main.set_duty(pwm, 250)
pico_main.set_duty(pwm, -5)
check("smoke — Pico script drives only GP16", calls["pin"] == 16, f"pin {calls['pin']}")
check("functional — PWM at 1kHz", calls["freq"] == 1000, f"{calls['freq']}Hz")
check(
    "smoke — duty is clamped to 0..100%",
    calls["duty"][0] == 0 and calls["duty"][2] == 65535 and calls["duty"][3] == 0 and 32000 < calls["duty"][1] < 33500,
    f"{calls['duty']}",
)
src = open(os.path.join(HERE, "main.py")).read()
check(
    "smoke — script leaves the pin low on exit",
    re.search(r"finally:\s+pwm\.deinit\(\)\s+Pin\(PIN, Pin\.OUT, value=0\)", src) is not None,
    "finally: deinit + Pin(OUT, value=0)",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
