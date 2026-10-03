"""
smoke_test.py — optical_shadow_readout

Safety: the GPIO that drives the LED must stay within the Pico's default 4mA
pad drive, whatever LED colour goes in; every node the ADC reads must stay in
0-3.3V; the TIA must not be driven into its ceiling at the design's ambient
and modulation, and the test pins where it does saturate (a documented
limit, not a hazard); the Pico script must leave all of its pins at high
impedance with the slices stopped.

Functional (transient runs of the netlist, one per bench state):
  - X scales linearly with the LED-driven photocurrent (2 : 1 : 0.5 uA
    gives 1 : 0.5 : 0.25 within 1%) and is zero with the beam blocked
  - a dark room (no ambient photocurrent) gives the same X as a lit one: the
    0.1V TIA bias keeps its output off the LM358's floor
  - ambient photocurrent from 0 to 13uA (TIA level 0.2V to 1.5V) changes X
    by under 0.5%, and 100Hz mains-lighting flicker 3uA peak (0.8V p-p at
    the TIA) by under 0.5%
  - above about 15uA of ambient the TIA saturates and X collapses: pinned as
    the documented limit
  - the 100k gain-stage option sees a 0.2uA signal at the same X as 2uA on the
    10k option
Then main.py's checks against a mocked bench (LED, ambient light, flag and
button): a healthy bench passes every stage, and a dead LED, a saturated
TIA, a leaky ambient path and a flag that doesn't block each fail the
right check.
"""

import contextlib
import io
import math
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

SPICE = os.path.join(HERE, "optical_shadow_readout.spice")
GPIO_DRIVE = 4e-3
failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def run_case(item):
    name, ov = item
    text = open(SPICE).read()
    for k, v in ov.items():
        text, n = re.subn(rf"\.param {k}=\S+", f".param {k}={v}", text)
        assert n == 1, k
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
        tmp.write(text)
    try:
        r = subprocess.run(["ngspice", "-b", tmp.name], capture_output=True, text=True, timeout=180, env={**os.environ, "OMP_NUM_THREADS": "1"})
    finally:
        os.unlink(tmp.name)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return name, parse_op_values(r.stdout)


CASES = {
    "open": dict(),
    "half": dict(imod="1u"),
    "quarter": dict(imod="0.5u"),
    "blocked": dict(imod=0),
    "dark_room": dict(iamb=0),
    "bright": dict(iamb="13u"),
    "flicker": dict(iflick="3u"),
    "saturated": dict(iamb="25u"),
    "gain100k": dict(rfs="100k", imod="0.2u"),
}
with ThreadPoolExecutor(max_workers=4) as pool:
    sim = dict(pool.map(run_case, CASES.items()))
x = {k: v["xavg"] for k, v in sim.items()}

# ---- safety ----
for vf, colour in ((1.8, "red"), (2.0, "yellow"), (2.2, "green")):
    i = (3.3 - vf) / 1000
    check(f"smoke — GPIO current into a {colour} LED (Vf {vf}V) through 1k is inside the default pad drive", 0.0003 < i < GPIO_DRIVE, f"{i*1e3:.2f}mA")
worst = max(max(v["amax"], v["bmax"], v["toutmax"], v["o1max"]) for v in sim.values())
check("smoke — every node the ADC or the switches see stays at or under the LM358's 1.8V", worst <= 1.8 + 1e-3, f"highest {worst:.3f}V")
check("smoke — the design point leaves the TIA clear of its ceiling", sim["open"]["toutmax"] < 1.6, f"TIA peak {sim['open']['toutmax']:.3f}V at 5uA ambient + 2uA LED")

# ---- functional ----
check("functional — the LED signal reads as X > 0", x["open"] > 0.05, f"X {x['open']*1e3:.1f}mV for 2uA p-p")
check("functional — half the light gives half X", abs(x["half"] / x["open"] - 0.5) < 0.01, f"{x['half']/x['open']:.4f}")
check("functional — a quarter of the light gives a quarter X", abs(x["quarter"] / x["open"] - 0.25) < 0.01, f"{x['quarter']/x['open']:.4f}")
check("functional — beam blocked gives X = 0", abs(x["blocked"]) < 1e-4, f"{x['blocked']*1e6:+.1f}uV")
check("functional — a dark room gives the same X as a lit one", abs(x["dark_room"] - x["open"]) / x["open"] < 0.005, f"{x['dark_room']*1e3:.2f}mV vs {x['open']*1e3:.2f}mV")
check(
    "functional — ambient from 0 to 13uA (TIA level 0.2V to 1.4V DC) leaves X unchanged",
    abs(x["bright"] - x["open"]) / x["open"] < 0.005,
    f"{x['bright']*1e3:.2f}mV vs {x['open']*1e3:.2f}mV while the TIA DC level went {sim['dark_room']['toutavg']:.2f}V -> {sim['bright']['toutavg']:.2f}V",
)
check(
    "functional — 100Hz mains flicker (0.8V p-p at the TIA) leaves X unchanged",
    abs(x["flicker"] - x["open"]) / x["open"] < 0.005 and sim["flicker"]["toutpp"] > 0.6,
    f"{x['flicker']*1e3:.2f}mV vs {x['open']*1e3:.2f}mV, TIA swing {sim['flicker']['toutpp']:.2f}V p-p",
)
check("functional — documented limit: 25uA of ambient saturates the TIA and X collapses", x["saturated"] < 0.1 * x["open"] and sim["saturated"]["toutmax"] > 1.79, f"X {x['saturated']*1e3:+.1f}mV, TIA at {sim['saturated']['toutmax']:.3f}V")
check("functional — the 100k gain option reads 0.2uA like the 10k option reads 2uA", abs(x["gain100k"] - x["open"]) / x["open"] < 0.02, f"{x['gain100k']*1e3:.1f}mV vs {x['open']*1e3:.1f}mV")

# ---- main.py against a mocked bench ----


class FakeMem:
    def __init__(self):
        self.regs = {}

    def __getitem__(self, a):
        return self.regs.get(a, 0)

    def __setitem__(self, a, v):
        base = 0x40050000 + 0xA0
        if a == base + 0x2000:
            self.regs[base] = self.regs.get(base, 0) | v
        elif a == base + 0x3000:
            self.regs[base] = self.regs.get(base, 0) & ~v
        else:
            self.regs[a] = v


mem = FakeMem()
funcsel = {}
bench = {"led_ok": True, "ambient_dc": 0.0, "ambient_leak": 0.0, "flag": 0.0, "tia_sat": False}  # flag: 0 out, 1 blocking
X_OPEN = x["open"]


def led_on():
    return funcsel.get(8) == "pwm" and bench["led_ok"]


def x_value():
    if not led_on():
        return 0.002
    light = X_OPEN * (1 - bench["flag"]) + 0.002
    return light * (1 + bench["ambient_leak"] * bench["ambient_dc"])


def tia_dc():
    return 0.105 + 5e-6 * 1e5 + bench["ambient_dc"] + (0.15 if led_on() else 0)


class FakePin:
    IN = 0
    ALT = 2
    PULL_UP = 1
    presses = []

    def __init__(self, n, mode=None, pull=None, alt=None):
        self.n = n
        funcsel[n] = "pwm" if (mode == FakePin.ALT and alt == 4) else "hiz"

    def value(self):
        # a press: the script waits for the button to read 0 then 1
        if self.n == 14:
            FakePin.presses.append(1)
            if FakePin.presses and (len(FakePin.presses) % 2 == 1):
                return 1
            return 0
        return 1


class FakeADC:
    def __init__(self, pin):
        self.pin = pin

    def read_u16(self):
        xv = x_value()
        tia = min(tia_dc(), 1.8) if not bench["tia_sat"] else 1.8
        v = {26: 1.114 - xv / 2, 27: 1.114 + xv / 2, 28: tia}[self.pin]
        return int(v / 3.3 * 65535)


class FakeTime:
    sleep = staticmethod(lambda s: None)


sys.modules["machine"] = types.SimpleNamespace(ADC=FakeADC, Pin=FakePin, mem32=mem)
sys.path.insert(0, HERE)
import main as m  # noqa: E402

m.time = FakeTime
adcs = [FakeADC(26), FakeADC(27), FakeADC(28)]


def stages(**setup):
    bench.update(led_ok=True, ambient_dc=0.0, ambient_leak=0.0, flag=0.0, tia_sat=False)
    bench.update(setup)
    m.start()
    m.led(False)
    dark = m.read_all(adcs, 4)
    m.led(True)
    on = m.read_all(adcs, 4)
    bench["ambient_dc"] = setup.get("bright_dc", 0.5)
    bright = m.read_all(adcs, 4)
    bench["ambient_dc"] = 0.0
    bench["flag"] = 0.0
    open_ = m.read_all(adcs, 4)
    bench["flag"] = setup.get("flag_block", 1.0)
    blocked = m.read_all(adcs, 4)
    res = m.check_led(dark, on) + m.check_ambient(on, bright) + m.check_flag(dark, open_, blocked)
    return res, (dark, on, bright, open_, blocked)


def failed(res):
    return [label for label, ok, _ in res if not ok]


res, readings = stages()
check("functional — a healthy mocked bench passes every stage", not failed(res), f"{len(res)} checks, failed: {failed(res)}")
res, _ = stages(led_ok=False)
check("functional — a dead LED fails 'the LED raises X'", "the LED raises X" in failed(res), str(failed(res)))
res, _ = stages(bright_dc=1.6)
check("functional — an ambient step that saturates the TIA is reported", "TIA stayed below saturation" in failed(res), str(failed(res)))
res, _ = stages(ambient_leak=0.5)
check("functional — an ambient path that leaks into X fails 'X unchanged by the ambient light'", "X unchanged by the ambient light" in failed(res), str(failed(res)))
res, _ = stages(flag_block=0.5)
check("functional — a flag that blocks only half the beam fails the flag check", "the flag removes most of the LED signal" in failed(res), str(failed(res)))
dark, on, bright, open_, blocked = readings
pc = m.percent_open(m.x_of(on), m.x_of(open_), m.x_of(blocked))
check("functional — percent_open reads 100% open and 0% blocked", abs(pc - 100) < 1e-6 and abs(m.percent_open(m.x_of(blocked), m.x_of(open_), m.x_of(blocked))) < 1e-9, f"{pc:.2f}%")

m.shutdown()
B = 0x40050000
check("smoke — shutdown stops the slices and releases the pins", mem[B + 0xA0] == 0 and all(funcsel[p] == "hiz" for p in (8, 10, 11)), f"EN {mem[B + 0xA0]:#x}, pins {[funcsel[p] for p in (8, 10, 11)]}")
period = mem[B + 0x14 * 5 + 0x10] + 1
check(
    "functional — the LED slice shares the reference's period and starts with it",
    mem[B + 0x14 * 4 + 0x10] + 1 == period and mem[B + 0x14 * 4 + 0x08] == mem[B + 0x14 * 5 + 0x08] == 0,
    f"period {period} counts",
)

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
