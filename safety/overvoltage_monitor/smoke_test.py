"""
smoke_test.py — overvoltage_monitor

Safety (the circuit is a safety monitor, so these are about it being a sound
monitor, not about hazards in it): the TL431 must be fed above its 1mA
minimum including with a sagging 3V3 rail (it fails below 2.83V, stated in
the README); the TRIP line must reach a real logic high when tripped and a
real low otherwise and never exceed 3.3V; the LED stage must light with a
low-gain transistor and draw nothing when not tripped; the comparator's input
stays inside the LM358's input range at the highest trip setting.

Functional (static ngspice runs and swept thresholds):
  - the trip voltage follows 2.495V x (2k + pos x 10k)/17.1k / 0.2 across the
    trimpot's travel, from 1.47V to 8.83V
  - release is below trip by 100-160mV (the hysteresis)
  - a TL431A at either end of its +-1% tolerance moves the trip by the same
  - set for 3.0V, it is tripped by the 3.3V rail and clear at 2.8V; set
    for 5.15V (mid-travel), the 3.3V rail does not trip it
Then main.py's checks: a healthy monitor passes, and a stuck-low TRIP, a stuck-
high TRIP, a trimpot that does nothing, and an input beyond range each fail.
"""

import os
import re
import subprocess
import sys
import tempfile
import types

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from ngspice_runner import parse_op_values  # noqa: E402

SPICE = os.path.join(HERE, "overvoltage_monitor.spice")
VIH_MIN = 0.7 * 3.3
VIL_MAX = 0.3
failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def run(control=None, **ov):
    text = open(SPICE).read()
    for k, v in ov.items():
        text, n = re.subn(rf"\.param {k}=\S+", f".param {k}={v}", text)
        assert n == 1, k
    if control:
        text = text[: text.index(".control")] + control + ".end\n"
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as tmp:
        tmp.write(text)
    try:
        r = subprocess.run(["ngspice", "-b", tmp.name], capture_output=True, text=True, timeout=60)
    finally:
        os.unlink(tmp.name)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return r.stdout


def op(**ov):
    return parse_op_values(run(**ov))


def threshold(edge, **ov):
    sweep = "0 9.5 0.002" if edge == "RISE" else "9.5 0 -0.002"
    out = run(f".control\ndc vmon {sweep}\nmeas dc vx WHEN v(out)=1.65 {edge}=1\nprint vx\nquit\n.endc\n", **ov)
    m = re.search(r"^vx\s*=\s*([-+0-9.e]+)", out, re.M)
    assert m, out[-300:]
    return float(m.group(1))


def trip_expected(pos, tol=0.0):
    return 2.495 * (1 + tol) * (2000 + pos * 10000) / 17100 / 0.2


# ---- safety ----
for rail in (3.3, 3.0):
    v = op(vs=rail)
    check(f"smoke — TL431 bias current is above its 1mA minimum with the 3V3 rail at {rail}V", 0.001 <= v["ik"] < 0.1, f"{v['ik']*1e3:.2f}mA")
low = op(vs=2.83)
check("smoke — the README's 2.83V rail floor is where the TL431 current reaches 1mA", abs(low["ik"] - 0.001) < 0.0001, f"{low['ik']*1e3:.2f}mA at 2.83V")
on, off = op(vin=7.0), op(vin=3.0)
check("smoke — tripped TRIP line is a real logic high and within the GPIO's range", VIH_MIN < on["vout"] <= 3.3, f"{on['vout']:.3f}V (needs above {VIH_MIN:.2f}V)")
check("smoke — clear TRIP line is a real logic low", off["vout"] < VIL_MAX, f"{off['vout']*1e3:.0f}mV")
for gain in (200, 60):
    v = parse_op_values(run(vin=7.0, bf=gain))
    check(f"smoke — LED lights with the S8050 at hFE {gain}", 0.001 < v["iled"] < 0.02, f"{v['iled']*1e3:.2f}mA")
check("smoke — LED draws nothing when clear", abs(off["iled"]) < 1e-6, f"{off['iled']:.2e}A")
top = op(pos=1.0, vin=8.83)
check("smoke — the comparator's sense node stays inside the LM358's ~1.8V input range at the highest trip setting", top["vsense"] <= 1.8, f"{top['vsense']:.3f}V at 8.83V in")

# ---- functional ----
worst = 0.0
for pos in (0.0, 0.25, 0.5, 0.75, 1.0):
    t = threshold("RISE", pos=pos)
    worst = max(worst, abs(t - trip_expected(pos)) / trip_expected(pos))
check("functional — trip voltage follows the formula across the trimpot's travel", worst < 0.015, f"worst error {worst*100:.2f}% (1.47V to 8.83V)")
trip, release = threshold("RISE", pos=0.5), threshold("FALL", pos=0.5)
check("functional — release is below trip by 100-160mV (hysteresis)", 0.10 <= trip - release <= 0.16, f"trip {trip:.3f}V, release {release:.3f}V, hysteresis {(trip-release)*1e3:.0f}mV")
for tol in (-0.01, 0.01):
    t = threshold("RISE", pos=0.5, vtol=tol)
    check(f"functional — a TL431A at {tol*100:+.0f}% moves the trip by {tol*100:+.0f}%", abs(t / trip - (1 + tol)) < 0.003, f"{t:.3f}V vs {trip:.3f}V")
pos3 = (3.0 * 0.2 / 2.495 * 17100 - 2000) / 10000
check("functional — set for 3.0V, the 3.3V rail trips it", op(pos=pos3, vin=3.3)["vout"] > VIH_MIN, f"pos {pos3:.3f}: out {op(pos=pos3, vin=3.3)['vout']:.2f}V")
check("functional — set for 3.0V, 2.8V does not", op(pos=pos3, vin=2.8)["vout"] < VIL_MAX, f"out {op(pos=pos3, vin=2.8)['vout']*1e3:.0f}mV")
check("functional — mid-travel (5.15V), the 3.3V rail does not trip it", op(pos=0.5, vin=3.3)["vout"] < VIL_MAX, "clear")

# ---- main.py ----
sys.modules["machine"] = types.SimpleNamespace(ADC=object, Pin=object)
sys.path.insert(0, HERE)
import main as m  # noqa: E402

D = m.DIV
sense = 3.3 * D  # monitoring the 3V3 rail
a_ok = (1, sense, 3.0 * D)  # trip set at 3.0V: over
b_ok = (0, sense, 8.0 * D)  # trip set at 8.0V: clear


def failed(res):
    return [label for label, ok, _ in res if not ok]


res = m.evaluate(a_ok, b_ok)
check("functional — a healthy monitor passes every main.py check", not failed(res), f"{len(res)} checks, failed: {failed(res)}")
res = m.evaluate((0, sense, 3.0 * D), b_ok)
check("functional — TRIP stuck low while SENSE is over VT is caught", "end A: TRIP agrees with SENSE vs VT" in failed(res), str(failed(res)))
res = m.evaluate(a_ok, (1, sense, 8.0 * D))
check("functional — TRIP stuck high is caught", "end B: TRIP agrees with SENSE vs VT" in failed(res) and "the two ends give different TRIP states" in failed(res), str(failed(res)))
res = m.evaluate((1, sense, 3.0 * D), (1, sense, 3.05 * D))
check("functional — a trimpot that does not move the trip voltage is caught", "the trimpot moves the trip voltage over a wide range" in failed(res), str(failed(res)))
res = m.evaluate(a_ok, (0, 1.9, 8.0 * D))
check("functional — an input beyond the comparator's range is caught", "monitored input inside the comparator's range" in failed(res), str(failed(res)))
check("functional — inside the hysteresis band either TRIP state is accepted", m.agrees(0, 0.62, 0.60) and m.agrees(1, 0.62, 0.60) and not m.agrees(0, 0.70, 0.60), "0.62V vs 0.60V")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
