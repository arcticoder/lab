"""
main.py — lockin_amplifier (MicroPython, Raspberry Pi Pico)

Bench check for the lock-in: the Pico generates the reference clocks, a
1kHz test signal (in phase, anti-phase, or shifted by a chosen angle), and an
asynchronous 1.37kHz interferer, then reads the two averaged outputs on GP26
and GP27 and checks that the circuit behaves like a lock-in:

  - signal in phase with the reference  -> a positive output X = VB - VA
  - signal in anti-phase                -> the same size, negative
  - signal at 90 degrees                -> about zero
  - signal at 45 degrees                -> about half (a square-wave lock-in has
                                           a triangular phase response)
  - interferer alone                    -> about zero
  - signal + interferer                 -> the same X as the signal alone

    mpremote run main.py        (about 15 seconds)

The PWM slices are programmed through their registers instead of
machine.PWM so that three things hold: the reference and the test signal
share one counter clock and start on the same clock edge (so their phase is
fixed, and set exactly by the counter preset), the two outputs of one slice
are exact complements (REF and REFB), and a channel can be switched out to
high impedance without stopping its slice. The register map and the
1kHz/25%/inverted-B behaviour were checked on a Pico against the logic
analyzer (2026-10-02, see README.md).

Pins (Pico GPIO): GP10 REF, GP11 REFB (slice 5); GP8 signal, GP9 inverted
signal (slice 4); GP6 interferer (slice 3, 1.37kHz); GP26/GP27 ADC inputs.
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
SIG_A, SIG_B = 8, 9
INT_A = 6
ADC_A_PIN, ADC_B_PIN = 26, 27

DIV_INT = 2
PERIOD_REF = 62500  # counts: 125MHz / (2 * 62500) = 1000.0Hz
PERIOD_INT = 45620  # 125MHz / (2 * 45620) = 1370.0Hz
REF_DUTY = 0.48  # REF high 48%, REFB high the last 48%: 4% dead time
VREF = 3.3
SETTLE_S = 1.6  # the averagers settle with a ~0.21s time constant; 7.6 of them
N_READS = 1500

# Check limits (X in volts). Expected in-phase X is 0.26V from the simulation;
# resistor tolerance and op-amp offsets move it, so the limits are wide and the
# other checks are ratios to the measured in-phase value.
LEVEL_MIN, LEVEL_MAX = 0.90, 1.35
ZERO_MAX = 0.05
X_MIN, X_MAX = 0.12, 0.40
ANTI_RATIO = (-1.15, -0.85)
QUAD_MAX = 0.15
HALF_RATIO = (0.35, 0.65)
INTERFERER_MAX = 0.10
SIG_PLUS_INT = 0.10

# name, signal ('off' | 'in' | 'anti'), phase in degrees, interferer on
STATES = [
    ("floor", "off", 0, False),
    ("in_phase", "in", 0, False),
    ("anti_phase", "anti", 0, False),
    ("quadrature", "in", 90, False),
    ("half", "in", 45, False),
    ("interferer", "off", 0, True),
    ("signal_plus_interferer", "in", 0, True),
]


def _slice(pin):
    return (pin >> 1) & 7


def _w(sl, reg, val):
    mem32[PWM_BASE + 0x14 * sl + reg] = val


def _program(sl, period, cc_a, cc_b, b_inv):
    _w(sl, CSR, B_INV if b_inv else 0)  # slice disabled while it is programmed
    _w(sl, DIV, DIV_INT << 4)
    _w(sl, TOP, period - 1)
    _w(sl, CC, (cc_b << 16) | cc_a)


def pin_on(n):
    Pin(n, Pin.ALT, alt=ALT_PWM)


def pin_off(n):
    Pin(n, Pin.IN)


def stop():
    mem32[EN_REG + ATOMIC_CLR] = (1 << _slice(REF_A)) | (1 << _slice(SIG_A)) | (1 << _slice(INT_A))


def sync(phase_deg):
    """Stop all three slices, preset their counters, restart them in one
    write. The signal slice's counter starts phase_deg ahead of REF's."""
    stop()
    _w(_slice(REF_A), CTR, 0)
    _w(_slice(SIG_A), CTR, int(phase_deg / 360 * PERIOD_REF) % PERIOD_REF)
    _w(_slice(INT_A), CTR, 0)
    mem32[EN_REG + ATOMIC_SET] = (1 << _slice(REF_A)) | (1 << _slice(SIG_A)) | (1 << _slice(INT_A))


def start():
    _program(_slice(REF_A), PERIOD_REF, int(PERIOD_REF * REF_DUTY), int(PERIOD_REF * (1 - REF_DUTY)), True)
    _program(_slice(SIG_A), PERIOD_REF, PERIOD_REF // 2, PERIOD_REF // 2, True)
    _program(_slice(INT_A), PERIOD_INT, PERIOD_INT // 2, 0, False)
    pin_on(REF_A)
    pin_on(REF_B)
    for p in (SIG_A, SIG_B, INT_A):
        pin_off(p)
    sync(0)


def set_state(sig, phase_deg, interferer):
    for p in (SIG_A, SIG_B, INT_A):
        pin_off(p)
    sync(phase_deg)
    if sig == "in":
        pin_on(SIG_A)
    elif sig == "anti":
        pin_on(SIG_B)
    if interferer:
        pin_on(INT_A)


def read_ab(adc_a, adc_b, n=N_READS):
    sa = sb = 0
    for _ in range(n):
        sa += adc_a.read_u16()
        sb += adc_b.read_u16()
    return sa / n * VREF / 65535, sb / n * VREF / 65535


def evaluate(r):
    """r: {state name: (VA, VB)}. Returns [(label, ok, detail)]."""
    x0 = r["floor"][1] - r["floor"][0]
    x = {k: (v[1] - v[0]) - x0 for k, v in r.items()}
    x1 = x["in_phase"]
    out = []
    out.append(
        (
            "node levels near Vmid (op-amps and divider alive)",
            LEVEL_MIN <= r["floor"][0] <= LEVEL_MAX and LEVEL_MIN <= r["floor"][1] <= LEVEL_MAX,
            f"VA {r['floor'][0]:.3f}V, VB {r['floor'][1]:.3f}V, limits {LEVEL_MIN}-{LEVEL_MAX}V",
        )
    )
    out.append(("no-signal offset small", abs(x0) <= ZERO_MAX, f"X0 {x0*1e3:+.1f}mV, limit ±{ZERO_MAX*1e3:.0f}mV"))
    hint = " (too large: gain stage clips; see breadboard.md 'Gain too high')" if x1 > 2 * X_MAX else ""
    out.append(("in-phase signal gives a positive X", X_MIN <= x1 <= X_MAX, f"X {x1*1e3:+.0f}mV, limits {X_MIN*1e3:.0f}-{X_MAX*1e3:.0f}mV{hint}"))
    if x1 > 0:
        ratio = x["anti_phase"] / x1
        out.append(("anti-phase signal flips the sign", ANTI_RATIO[0] <= ratio <= ANTI_RATIO[1], f"X/X_inphase {ratio:+.2f}, limits {ANTI_RATIO}"))
        q = abs(x["quadrature"]) / x1
        out.append(("90 degrees gives about zero", q <= QUAD_MAX, f"|X|/X_inphase {q:.2f}, limit {QUAD_MAX}"))
        h = x["half"] / x1
        out.append(("45 degrees gives about half", HALF_RATIO[0] <= h <= HALF_RATIO[1], f"X/X_inphase {h:.2f}, limits {HALF_RATIO}"))
        i = abs(x["interferer"]) / x1
        out.append(("interferer alone gives about zero", i <= INTERFERER_MAX, f"|X|/X_inphase {i:.3f}, limit {INTERFERER_MAX}"))
        s = x["signal_plus_interferer"] / x1
        out.append(
            (
                "signal + interferer matches signal alone",
                abs(s - 1) <= SIG_PLUS_INT,
                f"X/X_inphase {s:.3f}, within ±{SIG_PLUS_INT}",
            )
        )
    else:
        out.append(("remaining checks need a positive in-phase X", False, "skipped"))
    return out


def run():
    adc_a, adc_b = ADC(ADC_A_PIN), ADC(ADC_B_PIN)
    start()
    readings = {}
    for name, sig, phase, interferer in STATES:
        set_state(sig, phase, interferer)
        time.sleep(SETTLE_S)
        readings[name] = read_ab(adc_a, adc_b)
        va, vb = readings[name]
        print(f"{name:24s} VA {va:.4f}V  VB {vb:.4f}V  VB-VA {(vb-va)*1e3:+7.1f}mV")
    ok = True
    for label, passed, detail in evaluate(readings):
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        ok = ok and passed
    return ok


def shutdown():
    stop()
    for p in (REF_A, REF_B, SIG_A, SIG_B, INT_A):
        pin_off(p)


if __name__ == "__main__":
    try:
        run()
    finally:
        shutdown()
