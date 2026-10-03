"""
smoke_test.py — lockin_amplifier

Safety: nothing may leave the range a part tolerates. The gain stage's
output must stay clear of the LM358's ~1.8V ceiling in every case (including
the signal plus the larger interferer), or the clipping would corrupt the
demodulated value; every node the Pico ADC reads must stay inside 0-3.3V;
the two CD4066B switches must never be closed together (REF and REFB are
complementary with dead time); and the Pico script must leave every pin it
used at high impedance with the PWM slices stopped.

Functional (seven transient runs of the netlist, one per bench state):
  - no signal: X = VB - VA is zero to a microvolt
  - in-phase signal: X matches a hand calculation within the finite-bandwidth
    loss, and is positive
  - anti-phase: exactly the negative; 90 degrees: about zero; 45 degrees: half
    (square-wave gating gives a triangular phase response, not a cosine)
  - a 1.37kHz interferer twice the signal's size changes X by under 0.1%
  - a DC offset at the input changes X by under 1%
Then main.py's register programming and decision logic are checked against a
mocked machine module: frequencies and duties from the register values, REF
and REFB complementary, phase set by the counter preset, pins released on
exit, and evaluate() passing the simulated bench and failing three broken
ones.
"""

import math
import os
import re
import sys
import tempfile
import types
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values  # noqa: E402
import subprocess  # noqa: E402

SPICE = os.path.join(HERE, "lockin_amplifier.spice")
LM358_CEILING = 1.8  # V at VCC = 3.3V (VCC - 1.5V)
ADC_MAX = 3.3

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


CASES = {
    "floor": dict(sigon=0),
    "in_phase": dict(),
    "anti_phase": dict(sigdir=-1),
    "quadrature": dict(sigphase="0.25m"),
    "half": dict(sigphase="0.125m"),
    "interferer": dict(sigon=0, inton=1),
    "signal_plus_interferer": dict(inton=1),
    "signal_plus_dc": dict(offv=1),
}


def run_case(item):
    name, overrides = item
    text = open(SPICE).read()
    for k, v in overrides.items():
        text, n = re.subn(rf"\.param {k}=\S+", f".param {k}={v}", text)
        assert n == 1, k
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
        tmp.write(text)
    try:
        # the shared runner's 30s timeout is too short for 2s transients run side by side
        r = subprocess.run(["ngspice", "-b", tmp.name], capture_output=True, text=True, timeout=180, env={**os.environ, "OMP_NUM_THREADS": "1"})
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        return name, parse_op_values(r.stdout)
    finally:
        os.unlink(tmp.name)


with ThreadPoolExecutor(max_workers=4) as pool:
    sim = dict(pool.map(run_case, CASES.items()))

x = {k: v["xavg"] for k, v in sim.items()}

# ---- safety ----
worst_out1 = max(v["o1max"] for v in sim.values())
check(
    "smoke — gain-stage output stays clear of the LM358 ceiling in every case",
    worst_out1 < LM358_CEILING - 0.1,
    f"highest out1 {worst_out1:.3f}V (signal + interferer) vs {LM358_CEILING}V",
)
worst_adc = max(max(v["amax"], v["bmax"]) for v in sim.values())
check("smoke — ADC-facing nodes stay inside 0-3.3V", 0 <= min(min(v["amin"], v["bmin"]) for v in sim.values()) and worst_adc < ADC_MAX, f"highest {worst_adc:.3f}V")
check(
    "smoke — switch inputs stay inside VSS..VDD (CD4066B signal range)",
    all(0 <= v["o1min"] and v["o1max"] <= 3.3 for v in sim.values()),
    f"out1 {min(v['o1min'] for v in sim.values()):.3f}-{worst_out1:.3f}V",
)

spice_text = open(SPICE).read()
ref = re.search(r"Vref\s+ref\s+0 PULSE\(0 3.3 (\S+) \S+ \S+ (\S+) (\S+)\)", spice_text)
refb = re.search(r"Vrefb\s+refb 0 PULSE\(0 3.3 (\S+) \S+ \S+ (\S+) (\S+)\)", spice_text)


def ms(s):
    return float(s.replace("m", "e-3"))


ref_on, ref_off = ms(ref.group(1)), ms(ref.group(1)) + ms(ref.group(2))
refb_on, refb_off = ms(refb.group(1)), ms(refb.group(1)) + ms(refb.group(2))
period = ms(ref.group(3))
check(
    "smoke — REF and REFB never overlap (switches never closed together)",
    ref_off < refb_on and refb_off <= period,
    f"REF high {ref_on*1e3:.2f}-{ref_off*1e3:.2f}ms, REFB high {refb_on*1e3:.2f}-{refb_off*1e3:.2f}ms of {period*1e3:.0f}ms",
)

# ---- functional ----
check("functional — no signal gives X = 0", abs(x["floor"]) < 1e-5, f"{x['floor']*1e6:+.2f}uV")

v_in_pp = 3.3 * 1e3 / (1e6 + 1e3)  # 1Meg from the PWM, 1k to Vmid
rsrc = 1e3 * 1e6 / (1e3 + 1e6)
gain = 1e6 / (10e3 + rsrc)
ideal_x = v_in_pp * gain * 0.96  # square wave gated 48%/48%: both gates sit inside the flat parts
check(
    "functional — in-phase X is positive and within the finite-bandwidth loss of the hand calculation",
    0.75 * ideal_x <= x["in_phase"] <= ideal_x,
    f"{x['in_phase']*1e3:.1f}mV vs ideal {ideal_x*1e3:.1f}mV (gain {gain:.1f}, LM358 edge smoothing costs ~10%)",
)
check(
    "functional — anti-phase gives the negative",
    abs(x["anti_phase"] + x["in_phase"]) < 0.005 * x["in_phase"],
    f"{x['anti_phase']*1e3:+.1f}mV",
)
check(
    "functional — 90 degrees gives about zero (op-amp lag leaves a few percent)",
    abs(x["quadrature"]) < 0.08 * x["in_phase"],
    f"{x['quadrature']*1e3:+.1f}mV = {x['quadrature']/x['in_phase']*100:+.1f}% of in-phase",
)
check(
    "functional — 45 degrees gives about half (triangular phase response)",
    abs(x["half"] / x["in_phase"] - 0.5) < 0.05,
    f"{x['half']/x['in_phase']:.3f} of in-phase",
)
check(
    "functional — interferer alone gives zero",
    abs(x["interferer"]) < 0.001 * x["in_phase"],
    f"{x['interferer']*1e6:+.2f}uV against a {sim['interferer']['o1pp']*1e3:.0f}mV p-p interferer at the stage output",
)
check(
    "functional — signal + interferer equals the signal alone (interferer is 2x larger)",
    abs(x["signal_plus_interferer"] - x["in_phase"]) < 0.001 * x["in_phase"],
    f"{x['signal_plus_interferer']*1e3:.3f}mV vs {x['in_phase']*1e3:.3f}mV",
)
check(
    "functional — a DC offset at the input is rejected",
    abs(x["signal_plus_dc"] - x["in_phase"]) < 0.01 * x["in_phase"],
    f"{x['signal_plus_dc']*1e3:.2f}mV vs {x['in_phase']*1e3:.2f}mV",
)

# ---- main.py against a mocked machine module ----


class FakeMem:
    def __init__(self):
        self.regs = {}

    def __getitem__(self, addr):
        return self.regs.get(addr, 0)

    def __setitem__(self, addr, val):
        base = 0x40050000 + 0xA0
        if addr == base + 0x2000:
            self.regs[base] = self.regs.get(base, 0) | val
        elif addr == base + 0x3000:
            self.regs[base] = self.regs.get(base, 0) & ~val
        else:
            self.regs[addr] = val


mem = FakeMem()
funcsel = {}


class FakePin:
    IN = 0
    OUT = 1
    ALT = 2

    def __init__(self, num, mode=None, value=None, alt=None):
        funcsel[num] = "pwm" if (mode == FakePin.ALT and alt == 4) else "hiz" if mode == FakePin.IN else "other"


class FakeADC:
    def __init__(self, pin):
        self.pin = pin

    def read_u16(self):
        return int(bench_voltage(self.pin) / 3.3 * 65535)


def bench_state():
    sig = "anti" if funcsel.get(9) == "pwm" else "in" if funcsel.get(8) == "pwm" else "off"
    ctr4 = mem[0x40050000 + 0x14 * 4 + 0x08]
    phase = ctr4 / 62500 * 360
    return sig, phase, funcsel.get(6) == "pwm"


def triangle(phase):
    p = (phase + 180) % 360 - 180
    return 1 - 2 * abs(p) / 180


X_IN = x["in_phase"]
defect = {"interferer_leak": 0.0, "dead": False, "stuck": False}


def bench_voltage(pin):
    sig, phase, intf = bench_state()
    if defect["stuck"]:
        return 0.0
    xv = 0.0 if sig == "off" else (1 if sig == "in" else -1) * X_IN * triangle(phase)
    if defect["dead"]:
        xv = 0.0
    if intf:
        xv += defect["interferer_leak"] * X_IN
    xv += 0.008  # ADC channel offset difference + pickup, removed by the zero reading
    return 1.114 + (xv / 2 if pin == 27 else -xv / 2)


sys.modules["machine"] = types.SimpleNamespace(ADC=FakeADC, Pin=FakePin, mem32=mem)
sys.path.insert(0, HERE)
import main as m  # noqa: E402

m.time = types.SimpleNamespace(sleep=lambda s: None)  # no real waiting in the mocked runs

m.start()
B = 0x40050000


def reg(sl, off):
    return mem[B + 0x14 * sl + off]


def freq(sl):
    div = (reg(sl, 4) >> 4) + (reg(sl, 4) & 0xF) / 16
    return 125e6 / (div * (reg(sl, 0x10) + 1))


top5 = reg(5, 0x10) + 1
check("functional — reference frequency is 1000Hz from the registers", abs(freq(5) - 1000) < 0.01, f"{freq(5):.3f}Hz")
check("functional — signal slice runs at the same frequency and counter length as the reference", freq(4) == freq(5) and reg(4, 0x10) == reg(5, 0x10), f"{freq(4):.3f}Hz")
check("functional — interferer is 1370Hz and not a harmonic of 1kHz", abs(freq(3) - 1370) < 0.05, f"{freq(3):.3f}Hz")
cc5 = reg(5, 0x0C)
a_hi, b_lo = cc5 & 0xFFFF, cc5 >> 16
check(
    "smoke — REF high for 48%, REFB (inverted B) high for the last 48%, dead gap between",
    abs(a_hi / top5 - 0.48) < 1e-3 and (reg(5, 0) & m.B_INV) and a_hi < b_lo and abs((top5 - b_lo) / top5 - 0.48) < 1e-3,
    f"REF high counts 0-{a_hi}, REFB high counts {b_lo}-{top5} of {top5}",
)
check(
    "functional — signal and its complement are exact opposites (50%, B inverted)",
    reg(4, 0x0C) & 0xFFFF == reg(4, 0x0C) >> 16 == top5 // 2 and (reg(4, 0) & m.B_INV),
    f"CC {reg(4, 0x0C) & 0xFFFF}/{reg(4, 0x0C) >> 16}",
)
check("smoke — only the reference pins drive at start (signal/interferer high-Z)", funcsel[10] == funcsel[11] == "pwm" and funcsel[8] == funcsel[9] == funcsel[6] == "hiz", str({k: funcsel[k] for k in (6, 8, 9, 10, 11)}))
check("smoke — all three slices start in one write", mem[B + 0xA0] == (1 << 5) | (1 << 4) | (1 << 3), f"EN {mem[B + 0xA0]:#x}")

m.set_state("in", 90, False)
check("functional — 90 degrees is a counter preset of a quarter period", reg(4, 8) == top5 // 4 and reg(5, 8) == 0, f"CTR4 {reg(4, 8)}, CTR5 {reg(5, 8)}")
m.set_state("anti", 0, True)
check("functional — anti-phase uses GP9 and the interferer GP6, not GP8", funcsel[9] == funcsel[6] == "pwm" and funcsel[8] == "hiz", str({k: funcsel[k] for k in (6, 8, 9)}))
m.shutdown()
check(
    "smoke — shutdown stops the slices and releases every pin to high impedance",
    mem[B + 0xA0] == 0 and all(funcsel[p] == "hiz" for p in (6, 8, 9, 10, 11)),
    f"EN {mem[B + 0xA0]:#x}, pins {[funcsel[p] for p in (6, 8, 9, 10, 11)]}",
)

# decision logic: simulated healthy bench, then three broken ones
import io, contextlib  # noqa: E402


def run_quiet():
    with contextlib.redirect_stdout(io.StringIO()):
        readings = {}
        adc_a, adc_b = FakeADC(26), FakeADC(27)
        m.start()
        for name, sig, phase, intf in m.STATES:
            m.set_state(sig, phase, intf)
            readings[name] = m.read_ab(adc_a, adc_b, n=4)
        m.shutdown()
    return m.evaluate(readings)


res = run_quiet()
check("functional — evaluate() passes the simulated bench", all(ok for _, ok, _ in res), f"{sum(ok for _, ok, _ in res)}/{len(res)} checks")
defect["interferer_leak"] = 0.3
res = run_quiet()
check("functional — evaluate() fails when the interferer leaks through (30%)", not all(ok for _, ok, _ in res), "interferer check flagged" if any("interferer" in l and not ok for l, ok, _ in res) else "NOT flagged")
defect["interferer_leak"] = 0.0
defect["dead"] = True
res = run_quiet()
check("functional — evaluate() fails when the signal never arrives", not all(ok for _, ok, _ in res), "flagged")
defect["dead"] = False
defect["stuck"] = True
res = run_quiet()
check("functional — evaluate() fails when the nodes sit at 0V (unpowered or unwired)", not all(ok for _, ok, _ in res), "flagged")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
