"""
analog_sims.py — runs the ngspice netlists in sim/ and reduces each to the numbers the smoke test judges (WP3).

The op-amp is a behavioral model built from the TLV9062 / OPA197 data sheets (sim/oa.inc): gain-bandwidth, phase margin,
output impedance and rails, with no noise or offset. TI's own SPICE macro models replace it before layout (WP5 task).
"""

import math
import os
import re
import subprocess
import tempfile

SIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim")


def _run(netlist, replace=None, params=None):
    text = open(os.path.join(SIM, netlist)).read()
    for k, v in (params or {}).items():
        text, n = re.subn(rf"\.param {k}=\S+", f".param {k}={v}", text)
        assert n == 1, k
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for old, new in (replace or {}).items():
            text = text.replace(old, os.path.join(tmp, new))
        path = os.path.join(tmp, "n.spice")
        # the netlists write their data next to themselves; run them from a copy of the sim directory's include file
        open(os.path.join(tmp, "oa.inc"), "w").write(open(os.path.join(SIM, "oa.inc")).read())
        open(path, "w").write(text)
        subprocess.run(["ngspice", "-b", "n.spice"], cwd=tmp, capture_output=True, text=True, timeout=120)
        for fn in os.listdir(tmp):
            if fn.endswith(".txt"):
                rows = []
                for line in open(os.path.join(tmp, fn)):
                    try:
                        rows.append([float(x) for x in line.split()])
                    except ValueError:
                        pass
                out[fn] = rows
    return out


def tia():
    d = _run("tia.spice")["tia_ac.txt"]
    f = [r[0] for r in d]
    db = [r[1] for r in d]
    g1k = db[min(range(len(f)), key=lambda i: abs(f[i] - 1000))]
    f3 = next(fr for fr, x in zip(f, db) if fr > 1000 and x < g1k - 3)
    return {"gain_1k_db": g1k, "peak_db": max(db) - g1k, "f3_hz": f3}


def led_sink():
    d = _run("led_sink.spice")["led_tran.txt"]
    t = [r[0] for r in d]
    v = [r[1] for r in d]
    dn = [r[3] for r in d]
    seg = lambda a, b: [(tt, vv, dd) for tt, vv, dd in zip(t, v, dn) if a <= tt <= b]
    hi = seg(740e-6, 768e-6)[-30:]
    lo = seg(980e-6, 1010e-6)[-30:]
    final = sum(x[1] for x in hi) / len(hi)
    settle = [tt for tt, vv, _ in seg(519e-6, 760e-6) if abs(vv - final) > 0.01 * final]
    return {
        "on_mA": final / 51 * 1e3,
        "off_uA": sum(x[1] for x in lo) / len(lo) / 51 * 1e6,
        "headroom_V": min(dd - vv for _, vv, dd in hi),
        "settle_us": (max(settle) - 520e-6) * 1e6 if settle else 0.0,
    }


def dut(kp=274, cgs="1.365n", rload=1.0, r1=1000, cc="1e-8"):
    d = _run("dut_source.spice", replace={"dut_tran.txt": "dut.txt"}, params={"kp": kp, "cgs": cgs, "rload": rload, "r1": r1, "cc": cc})["dut.txt"]
    t = [r[0] for r in d]
    v = [r[1] for r in d]
    seg = lambda a, b: [(tt, vv) for tt, vv in zip(t, v) if a <= tt <= b]
    tail = seg(3.5e-3, 3.99e-3)
    final = sum(x for _, x in tail) / len(tail)
    peak = max(x for _, x in seg(100e-6, 4e-3))
    settle = [tt for tt, vv in seg(100e-6, 4e-3) if abs(vv - final) > 0.02 * final]
    return {"final_A": final, "overshoot_pct": (peak - final) / final * 100, "settle_us": (max(settle) - 101e-6) * 1e6 if settle else 0.0}


def plate():
    d = _run("plate_driver.spice")
    tr = d["plate_tran.txt"]
    t = [r[0] for r in tr]
    v = [r[1] for r in tr]
    seg = lambda a, b: [(tt, vv) for tt, vv in zip(t, v) if a <= tt <= b]
    tail = seg(900e-6, 990e-6)
    final = sum(x for _, x in tail) / len(tail)
    settle = [tt for tt, vv in seg(50e-6, 900e-6) if abs(vv - final) > 0.01 * final]
    dc = d["plate_dc.txt"]
    worst = max(abs(y - 5.7 * x) / (5.7 * x) for x, y in dc if 0.5 <= x <= 4.0)
    return {"final_V": final, "overshoot_pct": (max(v) - final) / final * 100, "settle_us": (max(settle) - 50e-6) * 1e6, "gain_err_pct": worst * 100, "max_V": max(max(y for _, y in dc), max(v))}
