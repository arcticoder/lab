"""
main.py — frequency_counter (MicroPython, Raspberry Pi Pico)

A hardware frequency counter on GP3: PWM slice 1 in rising-edge counting mode
(its B pin is the input), gated in software by the Pico's microsecond timer.
Auto-ranging: a 0.2ms probe (and, for slow inputs, a 20ms one) estimates the
frequency, then the gate is set so the 16-bit counter reaches about 60 000
counts: a 1s gate below 60kHz, shorter above, 1ms at the fastest. The probes
are short enough that the 16-bit counter can't wrap while estimating.

    mpremote run main.py

First it runs a loopback self-test: GP16 (a machine.PWM generator) must be
wired to the counter's input (breadboard.md). It checks 100Hz, 1kHz, 12.345kHz,
100kHz and 1MHz, and that an idle input reads as no signal, prints one
[PASS]/[FAIL] line each, then keeps measuring whatever is on the input, once a
second, until Ctrl-C. The self-test passing proves the counting and gating; it
can't prove the Pico's crystal, because the generator and counter share it.
Cross-check that against the logic analyzer (`measurement_tools/
logic_analyzer_check`).

The counter's input accepts 0-3.3V logic directly. Anything larger, or an
analog signal, goes through the input path in breadboard.md (10k + clamps, or
the LM358 Schmitt trigger).
"""

import time
from machine import PWM, Pin, mem32

PWM_BASE = 0x40050000
CSR, DIV, CTR, CC, TOP = 0x00, 0x04, 0x08, 0x0C, 0x10
EN = 1
DIVMODE_RISE = 2 << 4
ALT_PWM = 4

IN_PIN = 3  # slice 1, channel B
GEN_PIN = 16  # slice 0, channel A (self-test generator)
SLICE = (IN_PIN >> 1) & 7

PROBE_FAST_S = 0.0002  # counts at most 65 000 up to 325MHz: can't wrap
PROBE_SLOW_S = 0.02  # only used when the fast probe saw under FAST_MIN_COUNT edges
FAST_MIN_COUNT = 40
TARGET_COUNT = 60000
OVERFLOW_COUNT = 65000
GATE_MIN_S = 0.001
GATE_MAX_S = 1.0

SELFTEST_HZ = (100, 1000, 12345, 100000, 1000000)
TOL_FLOOR = 0.0005  # generator rounding and two independent timers, relative


def _w(reg, val):
    mem32[PWM_BASE + 0x14 * SLICE + reg] = val


def _r(reg):
    return mem32[PWM_BASE + 0x14 * SLICE + reg]


def setup():
    Pin(IN_PIN, Pin.ALT, alt=ALT_PWM, pull=Pin.PULL_DOWN)
    _w(CSR, DIVMODE_RISE)  # counting mode, not enabled
    _w(DIV, 1 << 4)
    _w(TOP, 0xFFFF)


def count(gate_s):
    """Count rising edges for gate_s seconds. Returns (counts, measured gate in
    seconds). The window is bounded by two register writes; the timer is read
    right after each, so the write latency cancels to first order."""
    _w(CTR, 0)
    gate_us = int(gate_s * 1e6)
    _w(CSR, DIVMODE_RISE | EN)
    t0 = time.ticks_us()
    if gate_us > 5000:
        time.sleep_us(gate_us - 3000)
    while time.ticks_diff(time.ticks_us(), t0) < gate_us:
        pass
    _w(CSR, DIVMODE_RISE)
    t1 = time.ticks_us()
    return _r(CTR), time.ticks_diff(t1, t0) / 1e6


def measure():
    """Returns (frequency in Hz or None, note)."""
    n1, e1 = count(PROBE_FAST_S)
    if n1 >= FAST_MIN_COUNT:
        f_est = n1 / e1
    else:
        n0, e0 = count(PROBE_SLOW_S)
        if n0 == 0:
            n, e = count(GATE_MAX_S)
            if n == 0:
                return None, "no signal"
            return n / e, f"{n} counts in {e:.3f}s (slow signal)"
        f_est = n0 / e0
    if f_est * GATE_MIN_S > OVERFLOW_COUNT:
        return None, f"counter overflow (about {f_est/1e6:.0f}MHz): input too fast for this method"
    gate = min(GATE_MAX_S, max(GATE_MIN_S, TARGET_COUNT / f_est))
    n, e = count(gate)
    if n >= OVERFLOW_COUNT:
        return None, f"counter overflow ({n} counts in {e*1e3:.1f}ms): input too fast for this method"
    return n / e, f"{n} counts in {e:.3f}s"


def evaluate(results, idle):
    """results: [(set Hz, measured Hz or None, counts note)], idle: (Hz or None)."""
    out = [("idle input reads no signal", idle is None, f"{idle}")]
    for f_set, f_meas, note in results:
        if f_meas is None:
            out.append((f"{f_set}Hz", False, note))
            continue
        # one count of quantization over the gate, plus the floor
        gate = min(GATE_MAX_S, max(GATE_MIN_S, TARGET_COUNT / f_set))
        tol = 1.5 / (f_set * gate) + TOL_FLOOR
        err = abs(f_meas - f_set) / f_set
        out.append((f"{f_set}Hz measured as {f_meas:.2f}Hz", err <= tol, f"error {err*100:.3f}% (limit {tol*100:.3f}%); {note}"))
    return out


def selftest():
    gen = PWM(Pin(GEN_PIN))
    results = []
    try:
        gen.duty_u16(0)
        gen.freq(1000)
        time.sleep(0.05)
        idle, _ = measure()  # duty 0: the generator pin sits low
        for f in SELFTEST_HZ:
            gen.freq(f)
            gen.duty_u16(32768)
            time.sleep(0.05)
            fm, note = measure()
            results.append((f, fm, note))
    finally:
        gen.deinit()
        Pin(GEN_PIN, Pin.IN)
    ok = True
    for label, passed, detail in evaluate(results, idle):
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        ok = ok and passed
    return ok


def shutdown():
    _w(CSR, 0)
    Pin(IN_PIN, Pin.IN)
    Pin(GEN_PIN, Pin.IN)


if __name__ == "__main__":
    try:
        setup()
        selftest()
        print("Measuring the input once a second. Ctrl-C to stop.")
        while True:
            f, note = measure()
            print("no signal" if f is None and note == "no signal" else f"{f:.2f} Hz  ({note})" if f else note)
            time.sleep(0.2)
    finally:
        shutdown()
