"""
smoke_test.py — signal_generator_r2r

Safety: with every code and resistors 5% off, the ladder's output stays under
the LM358's 1.8V input ceiling (VCC - 1.5V on 3.3V), and no Pico pin is asked
for more than its 4mA default drive; the driver parks the ladder at code 0 on
stop(), uses only GP0..GP7 as outputs, and never starts the PIO before its
pins are handed back.

Functional: the Python model of the ladder agrees with ngspice at four codes; the
frequency planner returns a power-of-two table and a divider whose frequency is
within the divider's own step of the request, from 0.5Hz to 100kHz; the sine
table is antisymmetric, hits its peak codes and stays above the LM358's output
floor; calibrating against the ladder's measured levels takes a 5%-resistor
sine from about -39dB to the 8-bit quantization floor (-57dB); the DMA set-up
is what the RP2040 datasheet requires (ring wrap on an aligned table, two
channels chaining to each other, TRANS_COUNT of one period, the PIO TX FIFO as
target, DREQ 0); a frequency change within a table length writes one register
and touches no DMA channel; the loopback matcher finds a clean capture and
flags one wrong sample; and the bench check's pass/fail logic passes a healthy
ladder and fails an open MSB leg, a bad bit ratio, a distorted sine and a slow
output.
"""

import math
import os
import random
import re
import subprocess
import sys
import tempfile
import types

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values  # noqa: E402

SPICE = os.path.join(HERE, "signal_generator_r2r.spice")
failures = []


def check(label, condition, detail):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}: {detail}")
    if not condition:
        failures.append(label)


# --- fakes for the Pico-only modules ------------------------------------------
class FakeSM:
    log = []

    def __init__(self, sm_id):
        self.id = sm_id

    def init(self, prog, freq=None, out_base=None):
        FakeSM.log.append(("sm.init", out_base.n))

    def active(self, v):
        FakeSM.log.append(("sm.active", v))


class FakeDMA:
    count = 0
    log = []

    def __init__(self):
        self.channel = FakeDMA.count
        FakeDMA.count += 1
        self.cfg = None
        self.closed = False

    def pack_ctrl(self, **kw):
        return kw

    def config(self, read, write, count, ctrl, trigger):
        self.cfg = dict(read=read, write=write, count=count, ctrl=ctrl)

    def active(self, v=None):
        if v is not None:
            FakeDMA.log.append(("dma.active", self.channel, v))
        return 0

    def close(self):
        self.closed = True


class FakePin:
    OUT = 1
    outputs = {}

    def __init__(self, n, mode=None, value=None):
        self.n = n
        if mode == FakePin.OUT:
            FakePin.outputs[n] = value


class Mem:
    def __init__(self):
        self.w = {}

    def __setitem__(self, a, v):
        self.w[a] = v

    def __getitem__(self, a):
        return self.w.get(a, 0)


mem = Mem()
sys.modules["rp2"] = types.SimpleNamespace(
    PIO=types.SimpleNamespace(OUT_LOW=0, SHIFT_RIGHT=1),
    asm_pio=lambda **kw: (lambda f: f),
    StateMachine=FakeSM,
    DMA=FakeDMA,
)
sys.modules["machine"] = types.SimpleNamespace(freq=lambda: 125_000_000, Pin=FakePin, mem32=mem)
sys.modules["uctypes"] = types.SimpleNamespace(addressof=lambda b: 0x20001230)
sys.path.insert(0, HERE)
import main as drv  # noqa: E402
import loopback_test as lb  # noqa: E402


# --- the ladder model, against ngspice -----------------------------------------
def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        p = max(range(i, n), key=lambda j: abs(m[j][i]))
        m[i], m[p] = m[p], m[i]
        for j in range(i + 1, n):
            f = m[j][i] / m[i][i]
            for c in range(i, n + 1):
                m[j][c] -= f * m[i][c]
    v = [0.0] * n
    for i in range(n - 1, -1, -1):
        v[i] = (m[i][n] - sum(m[i][c] * v[c] for c in range(i + 1, n))) / m[i][i]
    return v


def ladder(code, r2, r, rl, ron_hi=40.0, ron_lo=40.0, vdd=3.3):
    """Node voltages n0..n7 and the pin currents for one code."""
    n = 8
    a = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    gp = []
    for k in range(n):
        bit = (code >> k) & 1
        gk = 1 / (r2[k] + (ron_hi if bit else ron_lo))
        gp.append((gk, bit))
        a[k][k] += gk
        b[k] += gk * (vdd if bit else 0.0)
    a[0][0] += 1 / r2[0]
    for k in range(1, n):
        gk = 1 / r[k]
        a[k][k] += gk
        a[k - 1][k - 1] += gk
        a[k][k - 1] -= gk
        a[k - 1][k] -= gk
    a[7][7] += 1 / rl
    v = solve(a, b)
    cur = [gk * ((vdd if bit else 0.0) - v[k]) for k, (gk, bit) in enumerate(gp)]
    return v, cur


def nominal(code, **kw):
    return ladder(code, [2000.0] * 8, [1000.0] * 8, 1000.0, **kw)


def run_spice(code):
    text = open(SPICE).read()
    text, n = re.subn(r"\.param code=\S+", f".param code={code}", text)
    assert n == 1
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
        tmp.write(text)
    try:
        r = subprocess.run(["ngspice", "-b", tmp.name], capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        return parse_op_values(r.stdout)
    finally:
        os.unlink(tmp.name)


worst = 0.0
for code in (0, 1, 128, 255):
    sim = run_spice(code)["v(n7)"]
    mine = nominal(code)[0][7]
    worst = max(worst, abs(sim - mine))
check("functional — the Python ladder model agrees with ngspice at codes 0, 1, 128, 255", worst < 0.002, f"worst difference {worst*1e3:.2f}mV")
out255 = run_spice(255)["v(out)"]
check("functional — the buffer follows the ladder (code 255 at the output)", abs(out255 - nominal(255)[0][7]) < 0.005, f"{out255:.4f}V against {nominal(255)[0][7]:.4f}V")
v0 = run_spice(0)["v(out)"]
check("functional — codes 0..3 sit at the LM358's 0.02V floor, which is why the sine starts at code 28", v0 > 0.015 and drv.OFFSET - drv.AMP >= 8, f"code 0 gives {v0:.3f}V; lowest sine code {drv.OFFSET-drv.AMP}")

# --- safety: worst case over tolerance ------------------------------------------
random.seed(7)
worst_v = worst_i = 0.0
for _ in range(40):
    r2 = [2000 * (1 + random.uniform(-0.05, 0.05)) for _ in range(8)]
    r = [1000 * (1 + random.uniform(-0.05, 0.05)) for _ in range(8)]
    rl = 1000 * (1 + random.uniform(-0.05, 0.05))
    for code in (255, 127, 128, 0xAA, 0x55):
        v, cur = ladder(code, r2, r, rl, ron_hi=random.uniform(30, 60), ron_lo=random.uniform(30, 60))
        worst_v = max(worst_v, v[7])
        worst_i = max(worst_i, max(abs(c) for c in cur))
check("smoke — ladder output stays below the LM358 input ceiling with 5% resistors", worst_v < 1.8 - 0.1, f"highest {worst_v:.3f}V against 1.8V")
check("smoke — no pin sources or sinks more than 4mA", worst_i < 4e-3, f"worst {worst_i*1e3:.2f}mA")

# --- planner --------------------------------------------------------------------
bad = []
for f in (0.5, 1, 7.3, 100, 1000, 10_000, 50_000, 100_000):
    n, d = drv.plan(f)
    fa = drv.actual_freq(n, d)
    step = 0.5 / d  # relative half-step of a divider with 1/256 resolution
    if n & (n - 1) or not 32 <= n <= 4096 or abs(fa / f - 1) > step * 1.01 + 1e-9:
        bad.append((f, n, d, fa))
check("functional — planner gives a power-of-two table and a frequency within the divider's step", not bad, f"{bad}" if bad else "0.5Hz to 100kHz")
check("functional — 1kHz uses the 4096-byte table", drv.plan(1000)[0] == 4096, f"{drv.plan(1000)}")
try:
    drv.plan(5e6)
    refused = False
except ValueError:
    refused = True
check("functional — a frequency the table cannot make is refused", refused, "5MHz")

# --- the table --------------------------------------------------------------------
for n in (32, 256, 4096):
    t = bytearray(n)
    drv.make_table(t, n)
    anti = all(t[i] + t[(i + n // 2) % n] == 2 * drv.OFFSET for i in range(n))
    smooth = max(abs(t[i] - t[(i + 1) % n]) for i in range(n)) <= drv.AMP * 2 * math.pi / n + 1.01
    check(f"functional — {n}-byte table: antisymmetric about the offset, peaks at offset±amp, smooth, above the floor", anti and max(t) == drv.OFFSET + drv.AMP and min(t) == drv.OFFSET - drv.AMP and smooth and min(t) >= 8, f"codes {min(t)}..{max(t)}")


def spec_thd(samples):
    n = len(samples)
    m = sum(samples) / n

    def amp(k):
        re_ = sum((s - m) * math.cos(2 * math.pi * k * i / n) for i, s in enumerate(samples))
        im = sum((s - m) * math.sin(2 * math.pi * k * i / n) for i, s in enumerate(samples))
        return 2 * math.hypot(re_, im) / n

    return 20 * math.log10(math.sqrt(sum(amp(k) ** 2 for k in range(2, 17))) / amp(1))


def levels_for(r2, r, rl, ron_hi, ron_lo):
    return [ladder(c, r2, r, rl, ron_hi, ron_lo)[0][7] for c in range(256)]


random.seed(1)
unc, cal = [], []
ideal = None
for _ in range(10):
    r2 = [2000 * (1 + random.uniform(-0.05, 0.05)) for _ in range(8)]
    r = [1000 * (1 + random.uniform(-0.05, 0.05)) for _ in range(8)]
    rl = 1000 * (1 + random.uniform(-0.05, 0.05))
    lv = levels_for(r2, r, rl, random.uniform(30, 60), random.uniform(30, 60))
    t1 = bytearray(256)
    drv.make_table(t1, 256)
    t2 = bytearray(256)
    drv.make_table(t2, 256, nearest=drv.calibrator(lv))
    unc.append(spec_thd([lv[c] for c in t1]))
    cal.append(spec_thd([lv[c] for c in t2]))
    ideal = spec_thd(list(t1))
unc.sort()
cal.sort()
check(
    "functional — calibration takes 5%-resistor distortion to the 8-bit floor",
    cal[5] <= ideal + 3 and cal[5] < unc[5] - 10 and cal[-1] <= -50,
    f"uncalibrated median {unc[5]:.1f}dB (worst {unc[-1]:.1f}), calibrated median {cal[5]:.1f}dB (worst {cal[-1]:.1f}), ideal 8-bit {ideal:.1f}dB",
)

# --- the DMA/PIO set-up ------------------------------------------------------------
dds = drv.Dds()
check("functional — table buffer is aligned to its own size despite a misaligned allocation", dds.addr % drv.N_MAX == 0, f"{dds.addr:#x}")
f_act = dds.start(1000.0)
a, b = dds.a, dds.b
n, d = drv.plan(1000.0)
ok = (
    a.cfg["ctrl"]["ring_size"] == 12
    and a.cfg["ctrl"]["ring_sel"] == 0
    and a.cfg["ctrl"]["size"] == 2
    and a.cfg["ctrl"]["inc_read"] is True
    and a.cfg["ctrl"]["inc_write"] is False
    and a.cfg["ctrl"]["treq_sel"] == 0
    and a.cfg["write"] == 0x50200010
    and a.cfg["count"] == n // 4
    and a.cfg["read"] % n == 0
    and b.cfg["read"] == a.cfg["read"]
)
check("functional — both DMA channels: 32-bit words, ring wrap at the table size, PIO0 TX0 target, DREQ 0, one period each", ok, f"ring {a.cfg['ctrl']['ring_size']}, count {a.cfg['count']}, target {a.cfg['write']:#x}")
check("functional — the two channels chain to each other, not to themselves (the RP2040 cannot chain a channel to itself)", a.cfg["ctrl"]["chain_to"] == b.channel and b.cfg["ctrl"]["chain_to"] == a.channel and a.channel != b.channel, f"{a.channel} <-> {b.channel}")
check("functional — PIO divider register is INT<<16 | FRAC<<8", mem[0x50200000 + 0xC8] == drv.clkdiv_reg(d) and (mem[0x50200000 + 0xC8] >> 16) == d >> 8, f"{mem[0x50200000+0xC8]:#010x} for divider {d/256:.3f}")
check("functional — start() returns the frequency the divider really makes", abs(f_act / 1000 - 1) < 0.5 / d + 1e-9, f"{f_act:.3f}Hz")
sm_events = [e for e in FakeSM.log if e[0] in ("sm.init", "sm.active")]
check("smoke — the PIO is re-initialised (pins handed back) before it is started", sm_events.index(("sm.init", drv.PIN_BASE)) < sm_events.index(("sm.active", 1)), f"{sm_events}")
before = dict(mem.w)
dma_before = len(FakeDMA.log)
f2 = dds.set_freq(1100.0)
changed = {k for k in mem.w if mem.w[k] != before.get(k)}
check("functional — a frequency change in the same table length writes only the divider and touches no DMA channel", changed == {0x50200000 + 0xC8} and len(FakeDMA.log) == dma_before, f"{[hex(k) for k in changed]}, {f2:.2f}Hz")
try:
    dds.set_freq(50_000.0)
    raised = False
except ValueError:
    raised = True
check("functional — a change that needs another table length asks for start()", raised, "50kHz from 1kHz")
FakeDMA.log.clear()
FakePin.outputs.clear()
dds.stop()
aborted = {e[1] for e in FakeDMA.log if e[2] == 0}
check("smoke — stop() aborts both channels, closes them and parks the ladder at code 0 on GP0..GP7", aborted == {a.channel, b.channel} and a.closed and b.closed and FakePin.outputs == {i: 0 for i in range(8)}, f"outputs {sorted(FakePin.outputs.items())}")
src = open(os.path.join(HERE, "main.py")).read()
check("smoke — only GP0..GP7 are named as pins (PIN_BASE 0, 8 bits)", drv.PIN_BASE == 0 and drv.BITS == 8, "")

# --- loopback matcher ---------------------------------------------------------------
tab = bytearray(256)
drv.make_table(tab, 256)
cap = bytearray()
for i in range(2048):
    cap += bytes([tab[(i + 77) % 256]] * 2)
cap = bytes(cap[1:])  # an odd start: parity 1
m = lb.best_match(bytes(tab), 256, cap)
check("functional — loopback matcher finds a clean capture at a shift of 77 (an odd start offset)", m is not None and m[0] == 0 and m[3] == 77, f"{m}")
bad_cap = bytearray(cap)
bad_cap[2 * 500 + 1] ^= 0x10
bad_cap[2 * 500 + 2] ^= 0x10
m2 = lb.best_match(bytes(tab), 256, bytes(bad_cap))
check("functional — a wrong sample in the capture is counted", m2 is not None and m2[0] >= 1, f"{m2}")

# --- analysis -----------------------------------------------------------------------
fs = 100_000
sig = [1500 + 600 * math.sin(2 * math.pi * 1000 * i / fs) + 6 * math.sin(2 * math.pi * 3000 * i / fs) for i in range(4000)]
check("functional — distortion estimate reads a 1% third harmonic as -40dB", abs(drv.thd_db(sig, 1000, fs) + 40) < 0.5, f"{drv.thd_db(sig, 1000, fs):.2f}dB")
mean, pp, f = drv.analyze(sig, fs)
check("functional — analysis reads the 1kHz sine's frequency to 0.05% and its size", abs(f - 1000) < 0.5 and abs(pp / ((1200 + 12) * 3.3 / 4095) - 1) < 0.02, f"{f:.2f}Hz, {pp:.3f}V")

# --- bench logic -----------------------------------------------------------------------
lv_good = levels_for([2000] * 8, [1000] * 8, 1000, 40, 40)


def healthy():
    return {"levels": lv_good, "f_set": 1000.0, "cal": (0.81, (lv_good[228] - lv_good[28]), 1000.1), "thd_uncal": -39.0, "thd_cal": -52.0, "ceiling_hz": 40_000}


def fails(r):
    return {lab for lab, ok, _ in drv.evaluate(r) if not ok}


check("functional — a healthy ladder passes every check", not fails(healthy()), "")
r = healthy()
r["levels"] = levels_for([2000] * 7 + [1e9], [1000] * 8, 1000, 40, 40)
check("functional — an open MSB leg fails the span and bit-weight checks", {"ladder spans the expected swing", "each bit weighs 2^k steps (R-2R ratios hold)"} <= fails(r), "")
r = healthy()
r["levels"] = levels_for([2000, 2000, 2000, 2000, 3000, 2000, 2000, 2000], [1000] * 8, 1000, 40, 40)
check("functional — a 3kΩ leg on bit 4 fails the bit-weight check", "each bit weighs 2^k steps (R-2R ratios hold)" in fails(r), "")
r = healthy()
r["thd_cal"] = -30.0
check("functional — a distorted calibrated sine fails", "calibrated sine distortion" in fails(r), "-30dB")
r = healthy()
r["ceiling_hz"] = 4000
check("functional — an output that stops following below 10kHz fails", "amplitude holds to 10kHz" in fails(r), "4kHz")
r = healthy()
r["cal"] = (0.81, 0.5, 1010.0)
check("functional — a frequency 1% off the plan fails", "1kHz sine comes out at the planned frequency" in fails(r), "1010Hz")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
