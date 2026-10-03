"""
main.py — overvoltage_monitor (MicroPython, Raspberry Pi Pico)

Reads the monitor's three signals and checks that its hardware trip agrees
with its own reference:
    GP2   TRIP   (high when the monitored voltage is over the threshold)
    GP26  SENSE  (the monitored voltage after its 0.2 divider)
    GP27  VT     (the trip reference; trip voltage = VT / 0.2)

    mpremote run main.py

Two stages (the push button on GP14 to GND advances them):
 1. With the input wired to the Pico's 3V3 pin, turn the trimpot to one end
    and press the button, then to the other end and press it again. The
    two ends must give different TRIP states, trip voltages that differ by
    more than 2V, and at both ends TRIP must agree with SENSE vs VT (inside a
    ±30mV band around the comparison, where the 26mV hysteresis on SENSE
    makes either state valid).
 2. Live: monitored voltage, trip voltage, state, and the margin, until Ctrl-C.
Setting a real threshold: turn the trimpot until the printed trip voltage
is where you want it. The monitored input is valid from 0V to about 9V.
"""

import time
from machine import ADC, Pin

TRIP_PIN = 2
SENSE_PIN, VT_PIN = 26, 27
BUTTON = 14
VREF = 3.3
DIV = 0.2
AGREE_BAND = 0.030  # V at SENSE; the comparator's hysteresis is 26mV
RANGE_MAX_SENSE = 1.75  # the LM358 input range ends near 1.8V on 3.3V
MIN_TRIP_SPREAD = 2.0  # V between the trimpot's two ends
N = 200


def read_v(adc, n=N):
    total = 0
    for _ in range(n):
        total += adc.read_u16()
    return total / n * VREF / 65535


def sample(trip, sense, vt):
    return trip.value(), read_v(sense), read_v(vt)


def agrees(trip_state, sense_v, vt_v):
    """TRIP should be high when SENSE > VT and low when below; inside the
    hysteresis band either is valid."""
    if sense_v > vt_v + AGREE_BAND:
        return trip_state == 1
    if sense_v < vt_v - AGREE_BAND:
        return trip_state == 0
    return True


def evaluate(a, b):
    """a, b: (trip, sense, vt) at the two ends of the trimpot."""
    out = []
    for name, (t, s, v) in (("end A", a), ("end B", b)):
        out.append((f"{name}: TRIP agrees with SENSE vs VT", agrees(t, s, v), f"TRIP {t}, monitored {s/DIV:.2f}V, trip at {v/DIV:.2f}V"))
    out.append(("the two ends give different TRIP states", a[0] != b[0], f"{a[0]} / {b[0]}"))
    spread = abs(a[2] - b[2]) / DIV
    out.append(("the trimpot moves the trip voltage over a wide range", spread >= MIN_TRIP_SPREAD, f"{a[2]/DIV:.2f}V to {b[2]/DIV:.2f}V ({spread:.2f}V apart, need {MIN_TRIP_SPREAD}V)"))
    out.append(("monitored input inside the comparator's range", a[1] <= RANGE_MAX_SENSE and b[1] <= RANGE_MAX_SENSE, f"SENSE {a[1]:.3f}V / {b[1]:.3f}V, limit {RANGE_MAX_SENSE}V"))
    return out


def wait_for_button(btn):
    while btn.value():
        time.sleep(0.02)
    while not btn.value():
        time.sleep(0.02)


if __name__ == "__main__":
    trip = Pin(TRIP_PIN, Pin.IN, Pin.PULL_DOWN)
    sense, vt = ADC(SENSE_PIN), ADC(VT_PIN)
    btn = Pin(BUTTON, Pin.IN, Pin.PULL_UP)
    print("Turn the trimpot fully to one end, then press the button.")
    wait_for_button(btn)
    a = sample(trip, sense, vt)
    print("Turn the trimpot fully to the other end, then press the button.")
    wait_for_button(btn)
    b = sample(trip, sense, vt)
    ok = True
    for label, passed, detail in evaluate(a, b):
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        ok = ok and passed
    print("Live: monitored voltage / trip voltage. Ctrl-C to stop.")
    while True:
        t, s, v = sample(trip, sense, vt)
        print(f"monitored {s/DIV:5.2f}V  trip at {v/DIV:5.2f}V  margin {(v-s)/DIV:+5.2f}V  TRIP={'OVER' if t else 'ok'}")
        time.sleep(0.3)
