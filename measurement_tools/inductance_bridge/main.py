"""
main.py — inductance_bridge

Streams an inductance reading continuously (one PWM frequency sweep per
loop iteration) — like measurement_tools/capacitance_bridge/main.py and
resistance_measurement/main.py, this is a general-purpose instrument for
whatever inductor is currently wired into the tank, so there is no
PASS/FAIL verdict to print and exit on.

A GPIO PWM square wave drives Rs (1k) into a parallel tank made of the
unknown inductor and Cref (10nF). A Schottky diode + hold RC turns the
tank's amplitude into a DC level the ADC can read. The sweep finds the
frequency where that level peaks (the tank's resonance f0) and solves
Lx = 1 / ((2*pi*f0)^2 * C_TOTAL). See README.md "Range" for why this
uses resonance instead of the RL time constant.

Wire GP14 to Rs, and GP26 (ADC0) to the detector node — see breadboard.md.
Run with the Pico plugged in over USB:

    mpremote run main.py
"""

import machine
import math
import time

DRIVE_PIN = 14
ADC_PIN = 26
VREF = 3.3
C_REF = 10e-9  # farads, 10nF ceramic. Its tolerance (kit parts are +/-10-20%)
# sets the floor on Lx accuracy: f0 scales with 1/sqrt(C), so +/-10% on
# C is roughly +/-10% on the printed Lx. See README.md "Accuracy".
C_STRAY = 20e-12  # farads: diode junction + breadboard + ADC pin, an estimate
C_TOTAL = C_REF + C_STRAY

SWEEP_MIN_HZ = 40_000
SWEEP_MAX_HZ = 2_000_000
COARSE_STEP = 1.015  # 1.5% per step
FINE_SPAN = 1.05  # +/-5% around the coarse peak
FINE_STEP = 1.0025
SETTLE_MS = 8  # detector hold RC is 100k x 10nF = 1ms; 8 time constants
ADC_SAMPLES = 16
MIN_PEAK_V = 0.03  # below this the sweep found no tank amplitude at all
PEAK_TO_MEDIAN = 3.0  # a real resonance stands well above the sweep's median

# The 12 values in the on-hand color-ring assortment (docs/inventory.md)
ASSORTMENT_UH = (1, 10, 22, 33, 47, 100, 150, 220, 330, 470, 560, 1000)

pwm = machine.PWM(machine.Pin(DRIVE_PIN))
pwm.duty_u16(32768)  # 50% square wave
adc = machine.ADC(ADC_PIN)


def level_at(freq_hz):
    """Set the drive frequency, let the detector settle, return (actual_hz, volts)."""
    pwm.freq(int(freq_hz))
    actual = pwm.freq()  # the PWM divider quantizes; use the frequency it really runs at
    time.sleep_ms(SETTLE_MS)
    total = 0
    for _ in range(ADC_SAMPLES):
        total += adc.read_u16()
    return actual, (total / ADC_SAMPLES / 65535.0) * VREF


def sweep(start_hz, stop_hz, step):
    points = []
    f = start_hz
    last_actual = None
    while f <= stop_hz:
        actual, v = level_at(f)
        if actual != last_actual:  # skip duplicates where the PWM can't resolve two requests
            points.append((actual, v))
            last_actual = actual
        f *= step
    return points


def parabolic_peak(points, i):
    """Refine the peak using the log-frequency parabola through points i-1..i+1."""
    if i == 0 or i == len(points) - 1:
        return points[i][0]
    x0, x1, x2 = (math.log(points[j][0]) for j in (i - 1, i, i + 1))
    y0, y1, y2 = (points[j][1] for j in (i - 1, i, i + 1))
    denom = (x0 - x1) * (x0 - x2) * (x1 - x2)
    if denom == 0:
        return points[i][0]
    a = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / denom
    b = (x2 * x2 * (y0 - y1) + x1 * x1 * (y2 - y0) + x0 * x0 * (y1 - y2)) / denom
    if a >= 0:  # not a maximum — fall back to the raw peak
        return points[i][0]
    return math.exp(-b / (2 * a))


def measure_once():
    coarse = sweep(SWEEP_MIN_HZ, SWEEP_MAX_HZ, COARSE_STEP)
    levels = sorted(v for _, v in coarse)
    median = levels[len(levels) // 2]
    i_peak = max(range(len(coarse)), key=lambda k: coarse[k][1])
    f_peak, v_peak = coarse[i_peak]

    if v_peak < MIN_PEAK_V:
        return None, "no tank signal at all — Rs/tank/detector not wired, or the inductor is shorted"
    if i_peak == 0 or i_peak == len(coarse) - 1:
        return None, "level highest at the sweep edge — no resonance inside 40kHz-2MHz (inductor missing/open, or a value outside the assortment range)"
    if v_peak < PEAK_TO_MEDIAN * median:
        return None, "no distinct resonance peak — sweep is nearly flat"

    fine = sweep(f_peak / FINE_SPAN, f_peak * FINE_SPAN, FINE_STEP)
    j = max(range(len(fine)), key=lambda k: fine[k][1])
    f0 = parabolic_peak(fine, j)
    return (f0, fine[j][1]), None


while True:
    result, problem = measure_once()
    if result is None:
        print(f"No reading: {problem}")
    else:
        f0, v_peak = result
        l_uh = 1e6 / ((2 * math.pi * f0) ** 2 * C_TOTAL)
        nearest = min(ASSORTMENT_UH, key=lambda x: abs(math.log(x / l_uh)))
        off_pct = (l_uh / nearest - 1) * 100
        print(
            f"f0={f0/1e3:.1f}kHz peak={v_peak:.2f}V -> Lx={l_uh:.1f} uH "
            f"(nearest assortment value {nearest}uH, {off_pct:+.0f}%)"
        )
