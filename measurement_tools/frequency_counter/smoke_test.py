"""
smoke_test.py — frequency_counter

Safety: the GP3 pin must never leave its rated range whatever the input
does. A 1kHz square from -1V to 6V (an NE555 on psu_4xaa, plus a negative
excursion) through the 10k + 1N5817 clamps must stay between -0.5V and 3.8V
(the RP2040's absolute maximum, IOVDD+0.5V), and the LM358 Schmitt path's
output, which is pulled up to 3.3V, must reach a true logic level (above
2.3V = 0.7 x IOVDD) and a true low (under 0.3V). The Pico script must
release both pins it used.

Functional (transient runs of the netlist, edges counted in Python):
  - the Schmitt trigger reproduces a 1kHz, 50mV-peak sine as exactly 1kHz
    (18 rising edges in an 18ms window), with 8mV of 100kHz interference on top
  - it does not toggle when the input stays inside its hysteresis window
    (12mV peak sine), and ignores noise smaller than the window (15mV peak,
    30mV peak-to-peak), but does chatter once noise exceeds it (20mV peak)
  - the switching level follows the trimpot at both ends of its range
Then main.py is run against a mocked machine/time pair whose counter
increments at a chosen input frequency (with 16-bit wraparound): the
self-test must pass for the generator frequencies it uses, fail when the
counter is stuck, fail on a wrong gate, and report overflow rather than a
wrapped number.
"""

import os
import re
import subprocess
import sys
import tempfile
import types
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values  # noqa: E402

SPICE = os.path.join(HERE, "frequency_counter.spice")
RP2040_ABS_MAX_HIGH = 3.8
RP2040_ABS_MAX_LOW = -0.5
VIH_MIN = 0.7 * 3.3
VIL_MAX = 0.3

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def run_case(overrides):
    text = open(SPICE).read()
    for k, v in overrides.items():
        text, n = re.subn(rf"\.param {k}=\S+", f".param {k}={v}", text)
        assert n == 1, k
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "out.txt")
        text = text.replace("frequency_counter_out.txt", out)
        path = os.path.join(d, "c.spice")
        open(path, "w").write(text)
        r = subprocess.run(["ngspice", "-b", path], capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        vals = parse_op_values(r.stdout)
        rows = []
        for ln in open(out):
            p = ln.split()
            if len(p) == 3 and p[0].isdigit():
                rows.append((float(p[1]), float(p[2])))
    edges = sum(1 for i in range(1, len(rows)) if rows[i - 1][1] < 1.65 <= rows[i][1] and rows[i][0] >= 2e-3)
    return vals, edges


CASES = {
    "nominal": dict(),
    "sine_12mV": dict(amp=0.012, noise=0),
    "sine_25mV": dict(amp=0.025, noise=0),
    "noise_15mV": dict(amp=0, noise=0.015),
    "noise_20mV": dict(amp=0, noise=0.02),
    "pos_low": dict(pos=0.0),
    "pos_high": dict(pos=1.0),
}
with ThreadPoolExecutor(max_workers=4) as pool:
    res = dict(zip(CASES, pool.map(run_case, CASES.values())))
v_nom, e_nom = res["nominal"]

# ---- safety ----
check(
    "smoke — GP3 stays inside the RP2040's absolute maximum on a -1V..6V square",
    RP2040_ABS_MAX_LOW <= v_nom["dmin"] and v_nom["dmax"] <= RP2040_ABS_MAX_HIGH,
    f"{v_nom['dmin']:.3f}V to {v_nom['dmax']:.3f}V (limits {RP2040_ABS_MAX_LOW}V to {RP2040_ABS_MAX_HIGH}V)",
)
check(
    "smoke — Schmitt output reaches a real logic high and low at the pin",
    v_nom["omax"] > VIH_MIN and v_nom["omin"] < VIL_MAX and v_nom["gmax"] <= RP2040_ABS_MAX_HIGH,
    f"out {v_nom['omin']:.3f}V to {v_nom['omax']:.3f}V, pin high {v_nom['gmax']:.3f}V",
)

# ---- functional ----
check("functional — Schmitt reproduces a 50mV sine (+8mV 100kHz noise) as 1kHz", e_nom == 18, f"{e_nom} rising edges in 18ms (expect 18)")
check("functional — 25mV sine toggles it cleanly", res["sine_25mV"][1] == 18, f"{res['sine_25mV'][1]} edges")
check("functional — a 12mV sine (inside the hysteresis window) does not toggle it", res["sine_12mV"][1] == 0, f"{res['sine_12mV'][1]} edges")
check("functional — 15mV-peak (30mV p-p) noise alone does not chatter it", res["noise_15mV"][1] == 0, f"{res['noise_15mV'][1]} edges")
check("functional — 20mV-peak (40mV p-p) noise does chatter it (the stated limit)", res["noise_20mV"][1] > 100, f"{res['noise_20mV'][1]} edges")
vr_lo, vr_hi = res["pos_low"][0]["vr"], res["pos_high"][0]["vr"]
check(
    "functional — trimpot moves the switching level from 0.67V to about 1.98V",
    abs(vr_lo - 0.671) < 0.01 and abs(vr_hi - 1.985) < 0.01,
    f"{vr_lo:.3f}V to {vr_hi:.3f}V",
)
check(
    "functional — the Schmitt still toggles at both ends of the trimpot range",
    res["pos_low"][1] == 18 and res["pos_high"][1] == 18,
    f"{res['pos_low'][1]} / {res['pos_high'][1]} edges",
)

# ---- main.py against mocks ----


class FakeTime:
    def __init__(self):
        self.t = 0

    def ticks_us(self):
        self.t += 2  # every call costs time, so busy-wait loops advance
        return self.t

    @staticmethod
    def ticks_diff(a, b):
        return a - b

    def sleep_us(self, us):
        self.t += us

    def sleep_ms(self, ms):
        self.t += ms * 1000

    def sleep(self, s):
        self.t += int(s * 1e6)


ft = FakeTime()
state = {"f_in": 0.0, "t_en": None, "freq_gen": 0, "duty": 0, "stuck": False, "gate_err": 1.0}


class FakeMem:
    def __init__(self):
        self.regs = {}

    def __getitem__(self, a):
        return self.regs.get(a, 0)

    def __setitem__(self, a, v):
        csr = 0x40050000 + 0x14 * 1
        if a == csr:
            was, now = self.regs.get(csr, 0) & 1, v & 1
            if not was and now:
                state["t_en"] = ft.t
            if was and not now:
                if not state["stuck"]:
                    n = int(state["f_in"] * (ft.t - state["t_en"]) / 1e6 * state["gate_err"]) % 65536
                    self.regs[csr + 8] = n
        self.regs[a] = v


class FakePin:
    IN = 0
    ALT = 2
    PULL_DOWN = 1
    log = {}

    def __init__(self, n, mode=None, pull=None, alt=None, value=None):
        FakePin.log[n] = ("in" if mode == FakePin.IN else "alt" if mode == FakePin.ALT else "other")


class FakePWM:
    def __init__(self, pin):
        pass

    def freq(self, f):
        state["freq_gen"] = f
        state["f_in"] = f if state["duty"] else 0.0

    def duty_u16(self, d):
        state["duty"] = d
        state["f_in"] = state["freq_gen"] if d else 0.0

    def deinit(self):
        state["f_in"] = 0.0
        state["duty"] = 0


mem = FakeMem()
sys.modules["machine"] = types.SimpleNamespace(PWM=FakePWM, Pin=FakePin, mem32=mem)
sys.path.insert(0, HERE)
import main as m  # noqa: E402

m.time = ft
import contextlib  # noqa: E402
import io  # noqa: E402


def quiet_selftest():
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        m.setup()
        ok = m.selftest()
    return ok, buf.getvalue()


ok, out = quiet_selftest()
check("functional — self-test passes with a healthy counter at 100Hz to 1MHz", ok, f"{out.count('[PASS]')} PASS lines, {out.count('[FAIL]')} FAIL")

state["stuck"] = True
ok, out = quiet_selftest()
check("functional — self-test fails when the counter never counts", not ok and out.count("[FAIL]") >= 5, f"{out.count('[FAIL]')} FAIL lines")
state["stuck"] = False

state["gate_err"] = 1.01
ok, out = quiet_selftest()
check("functional — self-test fails when the count is 1% off (wrong gate)", not ok, f"{out.count('[FAIL]')} FAIL lines")
state["gate_err"] = 1.0

# overflow: an input faster than the counter can follow in the shortest gate
state["f_in"] = 80e6
fm, note = m.measure()
check("functional — an input above the counter's range is reported, not a wrapped number", fm is None and "overflow" in note, note)
state["f_in"] = 0.0

# fixed-frequency accuracy through the auto-range, including 16-bit wraparound paths
worst = 0.0
for f in (7.0, 50.0, 440.0, 1370.0, 59999.0, 250e3, 4.7e6, 20e6):
    state["f_in"] = f
    fm, note = m.measure()
    worst = max(worst, abs(fm - f) / f)
state["f_in"] = 0.0
check("functional — auto-range reads 7Hz to 20MHz within the quantization limit", worst < 0.2, f"worst error {worst*100:.2f}% (7Hz is ±1 count in 1s: 14%)")

m.shutdown()
check("smoke — shutdown stops the slice and releases both pins", mem[0x40050000 + 0x14] == 0 and FakePin.log[3] == "in" and FakePin.log[16] == "in", f"CSR {mem[0x40050000 + 0x14]:#x}, pins {FakePin.log}")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
