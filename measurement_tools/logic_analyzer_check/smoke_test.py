"""
smoke_test.py — logic_analyzer_check

No analog circuit here; the checks are that the host-side analysis is
right (it is the pass/fail authority for the bench run) and that the Pico
script drives what the analysis expects.

Safety: the Pico script drives one GPIO output at 3.3V logic into the
analyzer's input, which is a high-impedance logic input — nothing here
sources current into a load. The test asserts the script touches only the
one documented pin.

Functional: the analysis passes an ideal 1kHz/25% capture, and fails a
wrong frequency, an inverted signal, a stuck line, and a capture too short
to mean anything. sigrok-cli's csv output is parsed from the real tool
(demo driver), so a format change in sigrok is caught here. If the board is
plugged in, the live capture runs too; otherwise that check reports SKIP.
"""

import os
import shutil
import subprocess
import sys
import types

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import check_capture as cc  # noqa: E402

failures = []


def check(label, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not condition:
        failures.append(label)


def square(freq, duty, rate, n, invert=False, phase=0):
    period = rate / freq
    out = []
    for i in range(n):
        v = 1 if ((i + phase) % period) < duty * period else 0
        out.append(1 - v if invert else v)
    return out


RATE = 1_000_000
N = 25_000


def passes(samples):
    return all(ok for _, ok, _ in cc.verdict(cc.analyze(samples, RATE)))


check("functional — ideal 1kHz/25% capture passes", passes(square(1000, 0.25, RATE, N)), "ideal wave")
check("functional — phase offset doesn't matter", passes(square(1000, 0.25, RATE, N, phase=137)), "137-sample shift")
check("functional — wrong frequency fails", not passes(square(2000, 0.25, RATE, N)), "2kHz")
check("functional — inverted signal fails", not passes(square(1000, 0.25, RATE, N, invert=True)), "75% duty")
check("functional — stuck-low line fails", not passes([0] * N), "no edges")
check("functional — stuck-high line fails", not passes([1] * N), "no edges")
check("functional — too-short capture fails", not passes(square(1000, 0.25, RATE, 5000)), "5 periods")

# main.py against a mocked machine module.
calls = {}


class FakePWM:
    def __init__(self, pin):
        calls["pin"] = pin.num

    def freq(self, f):
        calls["freq"] = f

    def duty_u16(self, d):
        calls["duty"] = d / 65535

    def deinit(self):
        pass


class FakePin:
    def __init__(self, num, *a, **k):
        self.num = num


sys.modules["machine"] = types.SimpleNamespace(PWM=FakePWM, Pin=FakePin)
sys.path.insert(0, HERE)
import main as pico_main  # noqa: E402

pico_main.start()
check("smoke — Pico script drives only one pin, GP15", calls.get("pin") == 15, f"pin {calls.get('pin')}")
check(
    "functional — Pico frequency matches the analysis's expectation",
    calls.get("freq") == cc.EXPECTED_FREQ_HZ,
    f"{calls.get('freq')}Hz",
)
check(
    "functional — Pico duty matches the analysis's expectation",
    abs(calls.get("duty", 0) - cc.EXPECTED_DUTY) < 0.001,
    f"{calls.get('duty', 0)*100:.1f}%",
)

# Parser against real sigrok-cli output.
if shutil.which("sigrok-cli"):
    out = subprocess.run(
        ["sigrok-cli", "--driver", "demo", "--config", "samplerate=1m", "--channels", "D0",
         "--samples", "50", "-O", "csv"],
        capture_output=True, text=True,
    ).stdout
    parsed = cc.parse_csv(out)
    check(
        "functional — csv parser reads real sigrok-cli output",
        len(parsed) == 50 and set(parsed) <= {0, 1},
        f"{len(parsed)} samples from the demo driver",
    )
else:
    print("[SKIP] csv parser against real sigrok-cli output: sigrok-cli not installed")

# Live capture, only if the board is plugged in.
if shutil.which("sigrok-cli") and cc.board_present():
    print("[INFO] fx2lafw board found; live capture needs the Pico running main.py wired to D0")
    rc = subprocess.run([sys.executable, os.path.join(HERE, "check_capture.py")]).returncode
    check("functional — live capture of the Pico's 1kHz/25% wave", rc == 0, f"check_capture exit {rc}")
else:
    print("[SKIP] live capture: no fx2lafw board on USB")

print()
if failures:
    print(f"{len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("All checks passed.")
