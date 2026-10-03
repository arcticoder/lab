"""
main.py — hall_amplifier (MicroPython, Raspberry Pi Pico)

Nulls and reads the SS49E/49E Hall-sensor amplifier on GP26.

    mpremote run main.py

Three stages, printed as it goes:
 1. NULL: no magnet anywhere near the sensor. Turn the trimpot until the
    reading sits at the zero-field target (0.94V) and holds for 3 seconds.
    The sensor's own zero-field output differs from unit to unit by up to
    +-0.165V at 3.3V; times the amplifier's gain of 10 that is +-1.65V, far more
    than the output can swing, so this step is not optional.
 2. BASELINE: two seconds of readings at zero field. Reports the mean and the
    noise (standard deviation). PASS needs the noise under 3mV (0.3 gauss).
 3. LIVE: field in gauss, estimated from the *typical* sensitivity of
    0.92mV/gauss at 3.3V times the gain of 10. The datasheet's sensitivity
    spread (1.0 to 1.75mV/G at 5V) makes the true field 20% smaller to 40%
    larger than the number shown; the sign and relative changes are exact.
    Which pole raises the reading is whatever the sensor's orientation says;
    try both.

Wire only GP26 (pin 31) to the amplifier's output; 3V3 and GND as in
breadboard.md.
"""

import time
from machine import ADC

PIN = 26
VREF = 3.3
V_ZERO_TARGET = 0.94  # output at zero field, from Vr (simulated 0.939V)
NULL_TOL = 0.015
NULL_HOLD_S = 3.0
NULL_TIMEOUT_S = 120
GAIN = 10.0
SENS_V_PER_GAUSS = 0.00092  # typical 1.4mV/G at 5V, scaled to 3.3V
NOISE_MAX = 0.003
RAIL_HI, RAIL_LO = 1.75, 0.05  # the LM358 output limits near 1.8V and 0.02V
SENS_SPREAD = (1.0 / 1.4, 1.75 / 1.4)  # datasheet min/typ and max/typ sensitivity at 5V


def read_v(adc, n=200):
    total = 0
    for _ in range(n):
        total += adc.read_u16()
    return total / n * VREF / 65535


def null_state(v):
    """'ok' within tolerance of the target, 'low'/'high' otherwise, 'rail' when
    the output is pinned at an LM358 limit (no useful reading)."""
    if v >= RAIL_HI or v <= RAIL_LO:
        return "rail"
    if abs(v - V_ZERO_TARGET) <= NULL_TOL:
        return "ok"
    return "low" if v < V_ZERO_TARGET else "high"


def gauss(v, v0):
    return (v - v0) / SENS_V_PER_GAUSS


def gauss_range(v, v0):
    """Field range for the datasheet's sensitivity spread: a more sensitive
    sensor means a smaller field for the same deflection."""
    g = gauss(v, v0)
    return g / SENS_SPREAD[1], g / SENS_SPREAD[0]


def mean_std(xs):
    m = sum(xs) / len(xs)
    return m, (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5


def null_stage(adc, now=None, sleep=None):
    now = now or time.ticks_ms
    sleep = sleep or time.sleep
    held_since = None
    t0 = now()
    while time.ticks_diff(now(), t0) < NULL_TIMEOUT_S * 1000:
        v = read_v(adc)
        s = null_state(v)
        hint = {"ok": "on target", "low": "below target", "high": "above target", "rail": "pinned at a limit: sensor unpowered/unwired, or magnet near"}[s]
        print(f"NULL  {v:.3f}V (target {V_ZERO_TARGET}V ±{NULL_TOL*1e3:.0f}mV): {hint}")
        if s == "ok":
            held_since = held_since if held_since is not None else now()
            if time.ticks_diff(now(), held_since) >= NULL_HOLD_S * 1000:
                return True
        else:
            held_since = None
        sleep(0.1)
    return False


def baseline_stage(adc, seconds=2.0):
    vals = []
    t_end = time.ticks_add(time.ticks_ms(), int(seconds * 1000))
    while time.ticks_diff(t_end, time.ticks_ms()) > 0:
        vals.append(read_v(adc, 50))
    m, sd = mean_std(vals)
    ok = sd <= NOISE_MAX
    print(f"[{'PASS' if ok else 'FAIL'}] zero-field noise: mean {m:.4f}V, std {sd*1e3:.2f}mV ({sd/SENS_V_PER_GAUSS:.2f} gauss), limit {NOISE_MAX*1e3:.0f}mV")
    return m, ok


def live_stage(adc, v0):
    while True:
        v = read_v(adc)
        if v >= RAIL_HI or v <= RAIL_LO:
            print(f"{v:.3f}V  OUT OF RANGE (amplifier at its limit: field beyond about ±90 gauss)")
        else:
            lo, hi = gauss_range(v, v0)
            print(f"{v:.3f}V  {gauss(v, v0):+7.1f} gauss (sensitivity spread: {lo:+.0f} to {hi:+.0f})")
        time.sleep(0.2)


if __name__ == "__main__":
    adc = ADC(PIN)
    if not null_stage(adc):
        print("[FAIL] never reached the zero-field target within the timeout.")
        print("  Pinned near 0.02V or 1.8V at every trimpot position: check the sensor's pin order and the")
        print("  amplifier's wiring (breadboard.md). Stuck high only at one end of the trimpot: this sensor's")
        print("  zero-field output is above about 1.8V, beyond what the LM358 reference can follow; use another")
        print("  of the sensors.")
    else:
        print("[PASS] nulled")
        v0, ok = baseline_stage(adc)
        print("Live reading. Bring a magnet near; Ctrl-C to stop.")
        live_stage(adc, v0)
