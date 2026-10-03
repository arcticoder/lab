"""
main.py — optical_shadow_readout (MicroPython, Raspberry Pi Pico)

Bench check and live readout for the modulated-LED / photodiode shadow sensor.
The Pico drives the LED with a 1kHz square wave, generates the lock-in's
reference clocks from the same counter, and reads both averagers (GP26, GP27)
and the TIA's DC level (GP28).

    mpremote run main.py

Stages (a push button on GP14 to GND advances the manual ones):
 1. LED check, automatic: X = VB - VA with the LED off, then on. The LED
    must raise X, the averagers must be away from the rails, and the TIA
    must not be saturated.
 2. Ambient rejection, manual: shine a bright light (a phone flashlight)
    at the photodiode and press the button. The TIA's DC level must rise
    while X stays within 5%: that is the lock-in doing its job.
 3. Flag, manual: with the flag out of the beam press the button, then
    with the flag fully blocking the beam press it again. The flag must
    remove at least 80% of the LED signal.
 4. Live: percent of the beam that gets through, 100 * (X - X_blocked) /
    (X_open - X_blocked), four times a second. Ctrl-C stops.

The PWM slices are programmed through their registers (see
signal_conditioning/lockin_amplifier/main.py for why: REF/REFB and the LED
start from one counter on one clock edge, so the LED is exactly in phase with
the demodulator). Pins: GP10 REF, GP11 REFB (slice 5); GP8 LED (slice 4,
channel A); GP26/GP27 averagers; GP28 TIA level; GP14 button.
"""

import time
from machine import ADC, Pin, mem32

PWM_BASE = 0x40050000
EN_REG = PWM_BASE + 0xA0
ATOMIC_SET = 0x2000
ATOMIC_CLR = 0x3000
CSR, DIV, CTR, CC, TOP = 0x00, 0x04, 0x08, 0x0C, 0x10
B_INV = 1 << 3
ALT_PWM = 4

REF_A, REF_B = 10, 11
LED = 8
BUTTON = 14
ADC_A_PIN, ADC_B_PIN, ADC_TIA_PIN = 26, 27, 28

DIV_INT = 2
PERIOD = 62500  # 125MHz / (2 * 62500) = 1000.0Hz
REF_DUTY = 0.48
VREF = 3.3
SETTLE_S = 1.6
N_READS = 1000

LED_MIN_RISE = 0.010  # V of X the LED must add
LEVEL_MIN, LEVEL_MAX = 0.20, 1.70  # averager nodes
TIA_MAX = 1.60  # above this the TIA is close to its 1.8V ceiling
AMBIENT_MIN_RISE = 0.05  # TIA DC rise that counts as a real ambient step
AMBIENT_X_TOL = 0.05
FLAG_BLOCK_MIN = 0.80


def _slice(pin):
    return (pin >> 1) & 7


def _w(sl, reg, val):
    mem32[PWM_BASE + 0x14 * sl + reg] = val


def _program(sl, cc_a, cc_b, b_inv):
    _w(sl, CSR, B_INV if b_inv else 0)
    _w(sl, DIV, DIV_INT << 4)
    _w(sl, TOP, PERIOD - 1)
    _w(sl, CC, (cc_b << 16) | cc_a)


def pin_on(n):
    Pin(n, Pin.ALT, alt=ALT_PWM)


def pin_off(n):
    Pin(n, Pin.IN)


def stop():
    mem32[EN_REG + ATOMIC_CLR] = (1 << _slice(REF_A)) | (1 << _slice(LED))


def sync():
    stop()
    _w(_slice(REF_A), CTR, 0)
    _w(_slice(LED), CTR, 0)
    mem32[EN_REG + ATOMIC_SET] = (1 << _slice(REF_A)) | (1 << _slice(LED))


def start():
    _program(_slice(REF_A), int(PERIOD * REF_DUTY), int(PERIOD * (1 - REF_DUTY)), True)
    _program(_slice(LED), PERIOD // 2, 0, False)
    pin_on(REF_A)
    pin_on(REF_B)
    pin_off(LED)
    sync()


def led(on):
    """LED drive on or off; the reference clocks keep running either way."""
    if on:
        pin_on(LED)
    else:
        pin_off(LED)


def read_all(adcs, n=N_READS):
    sa = sb = st = 0
    for _ in range(n):
        sa += adcs[0].read_u16()
        sb += adcs[1].read_u16()
        st += adcs[2].read_u16()
    k = VREF / 65535 / n
    return sa * k, sb * k, st * k


def x_of(reading):
    return reading[1] - reading[0]


def check_led(dark, on):
    out = []
    rise = x_of(on) - x_of(dark)
    out.append(("the LED raises X", rise >= LED_MIN_RISE, f"X {x_of(dark)*1e3:+.1f}mV dark, {x_of(on)*1e3:+.1f}mV on: +{rise*1e3:.1f}mV (need {LED_MIN_RISE*1e3:.0f}mV)"))
    levels_ok = all(LEVEL_MIN <= v <= LEVEL_MAX for v in (on[0], on[1]))
    out.append(("averager nodes away from the rails", levels_ok, f"VA {on[0]:.3f}V, VB {on[1]:.3f}V, limits {LEVEL_MIN}-{LEVEL_MAX}V"))
    out.append(("TIA not saturated", on[2] <= TIA_MAX, f"TIA DC {on[2]:.3f}V (limit {TIA_MAX}V; ceiling 1.8V)"))
    return out


def check_ambient(on, bright):
    out = []
    rise = bright[2] - on[2]
    out.append(("ambient light raises the TIA level", rise >= AMBIENT_MIN_RISE, f"TIA {on[2]:.3f}V -> {bright[2]:.3f}V (+{rise*1e3:.0f}mV; need {AMBIENT_MIN_RISE*1e3:.0f}mV)"))
    if bright[2] > TIA_MAX:
        out.append(("TIA stayed below saturation", False, f"{bright[2]:.3f}V: too bright, the TIA is near its ceiling and X is no longer valid"))
        return out
    x0, x1 = x_of(on), x_of(bright)
    change = abs(x1 - x0) / max(abs(x0), 1e-9)
    out.append(("X unchanged by the ambient light", change <= AMBIENT_X_TOL, f"X {x0*1e3:+.1f}mV -> {x1*1e3:+.1f}mV ({change*100:.1f}% change; limit {AMBIENT_X_TOL*100:.0f}%)"))
    return out


def check_flag(dark, open_, blocked):
    span = x_of(open_) - x_of(dark)
    removed = (x_of(open_) - x_of(blocked)) / span if span > 0 else 0
    return [("the flag removes most of the LED signal", removed >= FLAG_BLOCK_MIN, f"open {x_of(open_)*1e3:+.1f}mV, blocked {x_of(blocked)*1e3:+.1f}mV: {removed*100:.0f}% removed (need {FLAG_BLOCK_MIN*100:.0f}%)")]


def percent_open(x, x_open, x_blocked):
    span = x_open - x_blocked
    return 100.0 * (x - x_blocked) / span if span != 0 else 0.0


def wait_for_button(btn):
    while btn.value():
        time.sleep(0.02)
    while not btn.value():
        time.sleep(0.02)


def report(results):
    ok = True
    for label, passed, detail in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        ok = ok and passed
    return ok


def measure(adcs):
    time.sleep(SETTLE_S)
    return read_all(adcs)


def run():
    adcs = [ADC(ADC_A_PIN), ADC(ADC_B_PIN), ADC(ADC_TIA_PIN)]
    btn = Pin(BUTTON, Pin.IN, Pin.PULL_UP)
    start()
    led(False)
    dark = measure(adcs)
    led(True)
    on = measure(adcs)
    print(f"LED off: VA {dark[0]:.3f} VB {dark[1]:.3f} TIA {dark[2]:.3f}V;  LED on: VA {on[0]:.3f} VB {on[1]:.3f} TIA {on[2]:.3f}V")
    ok = report(check_led(dark, on))
    print("Shine a bright light at the photodiode, then press the button.")
    wait_for_button(btn)
    bright = measure(adcs)
    ok = report(check_ambient(on, bright)) and ok
    print("Put the flag fully OUT of the beam and press the button.")
    wait_for_button(btn)
    open_ = measure(adcs)
    print("Put the flag fully IN the beam (blocking it) and press the button.")
    wait_for_button(btn)
    blocked = measure(adcs)
    ok = report(check_flag(dark, open_, blocked)) and ok
    print("Live: percent of the beam getting through. Ctrl-C to stop.")
    x_open, x_blocked = x_of(open_), x_of(blocked)
    while True:
        r = read_all(adcs, 300)
        print(f"{percent_open(x_of(r), x_open, x_blocked):6.1f}% open   X {x_of(r)*1e3:+7.1f}mV   TIA {r[2]:.3f}V")
        time.sleep(0.15)


def shutdown():
    stop()
    for p in (REF_A, REF_B, LED):
        pin_off(p)


if __name__ == "__main__":
    try:
        run()
    finally:
        shutdown()
