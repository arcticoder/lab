"""
smoke_test.py — hall_amplifier

Safety: whatever the sensor does, the amplifier's output must stay inside the
Pico ADC's 0-3.3V (the LM358 can't exceed ~1.8V) at fields far beyond the
sensor's range; the amplifier's input nodes must stay inside the LM358's
input range (about 1.8V on 3.3V) for the working range of fields and for the
sensor's worst-case zero-field offset; and the supply draw (sensor plus
amplifier) must sit well inside the Pico rail's budget. The datasheet allows a
reversed supply to -5V, which is stated in the README, not asserted here.

Functional (static ngspice runs, sensor model from the Honeywell datasheet):
  - at zero field and a nominal sensor the output sits at the reference (0.94V)
  - the trimpot can null any sensor offset in the datasheet's +-0.25V (5V
    basis) range: after nulling, zero-field output is within 5mV of nominal
  - gain: output slope is 10 x the sensor's sensitivity (within the resistor
    loading) and symmetric for +-50 gauss to under 2%
  - sensitivity extremes (1.0 and 1.75 mV/G) change the slope proportionally
  - 5% resistor mismatch moves the zero level (the trimpot nulls it) but not
    the slope by more than 5%
Then main.py's decision functions are checked: nulling states, gauss
conversion, and its run against a mocked ADC that reproduces a healthy
sensor, an unplugged one, and one with excess noise.
"""

import os
import re
import subprocess
import sys
import tempfile
import math
import types

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values  # noqa: E402

SPICE = os.path.join(HERE, "hall_amplifier.spice")
LM358_CEILING = 1.8
VR_TARGET = 0.94
failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def run(**ov):
    text = open(SPICE).read()
    for k, v in ov.items():
        text, n = re.subn(rf"\.param {k}=\S+", f".param {k}={v}", text)
        assert n == 1, k
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
        tmp.write(text)
    try:
        r = subprocess.run(["ngspice", "-b", tmp.name], capture_output=True, text=True, timeout=60)
    finally:
        os.unlink(tmp.name)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return parse_op_values(r.stdout)


def pos_for(nullerr):
    """Trimpot position that makes Vn equal the sensor's zero-field output
    (Vn = 3.3V * (30k + pos*10k) / 70k)."""
    vh0 = 3.3 / 2 + nullerr * 3.3 / 5
    return (vh0 - 3.3 * 30 / 70) / (3.3 * 10 / 70)


# ---- safety ----
worst_out = 0.0
for b in (-5000, -800, -300, 300, 800, 5000):
    worst_out = max(worst_out, run(bgauss=b)["vout"], run(bgauss=b, nullerr=0.25)["vout"])
check("smoke — output stays under the LM358 ceiling at fields far beyond the sensor's range", worst_out <= LM358_CEILING + 1e-6, f"highest {worst_out:.3f}V (ADC limit 3.3V)")

worst_in = 0.0
positions = {n: pos_for(n) for n in (-0.25, 0.0, 0.2)}
for nullerr in (-0.25, 0.0, 0.2):
    for b in (-50, 0, 50):
        v = run(nullerr=nullerr, pos=positions[nullerr], bgauss=b)
        worst_in = max(worst_in, v["vplus"], v["vminus"], v["vnull"])
check(
    "smoke — amplifier input nodes stay inside the LM358's input range for ±50 gauss and the sensor's worst-case null",
    worst_in <= LM358_CEILING + 0.01,
    f"highest input node {worst_in:.3f}V vs ~{LM358_CEILING}V",
)
nom = run(pos=positions[0.0])
check("smoke — amplifier supply draw is small (the sensor adds 6-10mA at 5V per its datasheet)", nom["isup"] < 1e-3, f"{nom['isup']*1e3:.2f}mA from the netlist; sensor datasheet 10mA max at 25C")
check(
    "smoke — the trimpot's travel covers the datasheet's null spread up to +0.2V (5V basis)",
    all(0.0 < p < 1.0 for p in positions.values()) and positions[-0.25] < positions[0.0] < positions[0.2],
    f"wiper at {positions[-0.25]:.2f} / {positions[0.0]:.2f} / {positions[0.2]:.2f} of travel for -0.25V / 0 / +0.2V (5V basis)",
)

# ---- functional ----
check("functional — zero field, nominal sensor, nulled: output at the 0.94V reference", abs(nom["vout"] - VR_TARGET) < 0.01, f"{nom['vout']:.4f}V")
for nullerr in (-0.25, 0.2):
    v = run(nullerr=nullerr, pos=positions[nullerr])
    check(f"functional — trimpot nulls a {nullerr:+.2f}V sensor offset", abs(v["vout"] - v["vref"]) < 0.003, f"{v['vout']:.4f}V vs reference {v['vref']:.4f}V")
un = run(nullerr=0.2, pos=positions[0.0])
check("functional — an un-nulled sensor at +0.2V would rail the output (nulling is required)", un["vout"] >= LM358_CEILING - 0.01, f"{un['vout']:.3f}V without the trim")
edge = run(nullerr=0.25, pos=1.0)
check(
    "functional — documented limit: the datasheet's +0.25V extreme can't be nulled (buffer ceiling)",
    edge["vout"] - edge["vref"] > 0.05,
    f"{edge['vout']:.3f}V vs reference {edge['vref']:.3f}V with the trimpot at its end",
)

plus, minus = run(bgauss=50, pos=positions[0.0])["vout"], run(bgauss=-50, pos=positions[0.0])["vout"]
slope = (plus - minus) / 100  # V per gauss
expected = 10 * 1.4e-3 * 3.3 / 5
check("functional — gain is 10 x the sensor sensitivity", abs(slope - expected) / expected < 0.03, f"{slope*1e3:.2f}mV/G vs {expected*1e3:.2f}mV/G")
check("functional — ±50 gauss deflections are symmetric", abs((plus - nom['vout']) + (minus - nom['vout'])) < 0.02 * (plus - minus) / 2, f"+{plus-nom['vout']:.4f}V / {minus-nom['vout']:.4f}V")
s_lo, s_hi = run(bgauss=50, sens=1.0, pos=positions[0.0])["vout"] - nom["vout"], run(bgauss=50, sens=1.75, pos=positions[0.0])["vout"] - nom["vout"]
check("functional — sensitivity extremes scale the deflection 1.0 : 1.75", abs(s_hi / s_lo - 1.75) < 0.05, f"{s_lo*1e3:.0f}mV and {s_hi*1e3:.0f}mV for +50G")
tol = run(bgauss=50, dRf=0.05, dRr=-0.05, pos=positions[0.0])["vout"] - run(bgauss=0, dRf=0.05, dRr=-0.05, pos=positions[0.0])["vout"]
check("functional — 5% resistor mismatch changes the slope by under 5%", abs(tol - (plus - nom['vout'])) / (plus - nom['vout']) < 0.05, f"{tol*1e3:.1f}mV vs {(plus-nom['vout'])*1e3:.1f}mV")
shift = run(dRf=0.05, dRr=-0.05, pos=positions[0.0])["vout"] - nom["vout"]
check("functional — the same mismatch shifts the zero level (the trim absorbs it)", abs(shift) > 0.02, f"{shift*1e3:+.0f}mV")

# ---- main.py ----
ADC_V = {"v": 0.94, "noise": 0.0}
counter = {"t": 0, "i": 0}


class FakeADC:
    def __init__(self, pin):
        assert pin == 26

    def read_u16(self):
        counter["i"] += 1
        n = ADC_V["noise"] * math.sin(counter["i"] / 1000)  # slow wander, visible through the 50-sample averages
        return int((ADC_V["v"] + n) / 3.3 * 65535)


class FakeTime:
    @staticmethod
    def ticks_ms():
        counter["t"] += 1
        return counter["t"]

    ticks_diff = staticmethod(lambda a, b: a - b)
    ticks_add = staticmethod(lambda a, b: a + b)
    sleep = staticmethod(lambda s: None)


sys.modules["machine"] = types.SimpleNamespace(ADC=FakeADC)
sys.path.insert(0, HERE)
import main as m  # noqa: E402

m.time = FakeTime
import contextlib  # noqa: E402
import io  # noqa: E402

check("functional — null_state classifies low / ok / high / rail", [m.null_state(v) for v in (0.8, 0.94, 1.1, 1.79, 0.02)] == ["low", "ok", "high", "rail", "rail"], str([m.null_state(v) for v in (0.8, 0.94, 1.1, 1.79, 0.02)]))
check("functional — 46mV above zero is +50 gauss at the typical sensitivity", abs(m.gauss(0.94 + 0.046, 0.94) - 50) < 0.1, f"{m.gauss(0.986, 0.94):.2f}G")
lo, hi = m.gauss_range(0.986, 0.94)
check("functional — the reported spread brackets the datasheet's sensitivity range (-20% / +40%)", lo < 50 < hi and abs(lo - 40) < 0.5 and abs(hi - 70) < 0.5, f"{lo:.0f} to {hi:.0f}G")

with contextlib.redirect_stdout(io.StringIO()):
    ADC_V.update(v=0.94, noise=0.0005)
    ok_null = m.null_stage(FakeADC(26), now=FakeTime.ticks_ms, sleep=FakeTime.sleep)
    v0, ok_base = m.baseline_stage(FakeADC(26), seconds=0.05)
check("functional — a healthy sensor nulls and passes the noise check", ok_null and ok_base, f"null {ok_null}, baseline noise ok {ok_base}, mean {v0:.4f}V")
with contextlib.redirect_stdout(io.StringIO()):
    ADC_V.update(v=0.02, noise=0.0)
    m.NULL_TIMEOUT_S = 0.01
    ok_unplugged = m.null_stage(FakeADC(26), now=FakeTime.ticks_ms, sleep=FakeTime.sleep)
check("functional — an unpowered amplifier (output at 0.02V) fails to null", not ok_unplugged, "timed out")
with contextlib.redirect_stdout(io.StringIO()):
    ADC_V.update(v=0.94, noise=0.02)
    _, ok_noisy = m.baseline_stage(FakeADC(26), seconds=0.05)
check("functional — a noisy output (±20mV) fails the baseline check", not ok_noisy, "flagged")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
