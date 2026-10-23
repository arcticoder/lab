"""
diagnose_levels.py — lockin_amplifier (MicroPython, Raspberry Pi Pico)

A power walk: says what the GP28 jumper's row is, then reads the averagers A and B through their
switches. Put the GP28 jumper on one row, run

    mpremote run diagnose_levels.py

then move it to the next row. GP6, GP8 and GP9 stay high impedance; GP10 and GP11 are driven only
to close S1 and S2 one at a time.

Step 1 — the jumper row. The DC level is read, then GP28's own 50-80kΩ pull-up and pull-down are
switched on. A row that is really on a node reads ground, Vmid or the rail and keeps it, or (INN and
C2, whose virtual ground holds only against about 1µA) rests at Vmid and moves by volts under
the pulls. A pad that is not touching any row rests anywhere (0.76V was seen on 2026-10-19 and
2026-10-22) and moves by volts: the script says "floating", and that reading is the jumper not
seated, not a fault in the circuit.

Step 2 — averagers. With the demodulator switches open, A and B sit on their capacitors and drift
(0.39V to 1.84V between runs on 2026-10-22: meaningless). So S1 is closed alone and A is read, then
S2 alone and B: each reads OUT1's DC level through its switch, which is Vmid (about 1.115V) when
the gain stage's reference is right. Each gets a PASS or FAIL.

Expected (3.3V supply, Rm1 10kΩ over Rm2 5.1kΩ):
  + rail, U1/U2 pin 8, S1/S2 pin 14        3.3V
  - rail, U1/U2 pin 4, S1/S2 pin 7         0V
  VMR, VMO, OUT1 (no signal)               about 1.115V  (3.3V x 5.1k / 15.1k)
  INN, C2, SIG                             about 1.115V at rest; INN and C2 move by volts under the pulls
"""

import time
from machine import ADC, Pin, mem32

VMID = 3.3 * 5.1 / (10 + 5.1)
PAD28 = 0x4001C000 + 4 + 28 * 4
PUE, PDE = 1 << 3, 1 << 2
VMID_TOL = 0.12


def classify(rest, d_up, d_dn):
    """(label, on_a_node) from the rest level and its changes under the pad pull-up (d_up, positive)
    and pull-down (d_dn, negative), volts."""
    if rest < 0.15:
        return "ground (0V)", True
    if rest > 3.15:
        return "the 3.3V rail", True
    if abs(rest - VMID) < VMID_TOL:
        soft = d_up > 1.0 or -d_dn > 0.6
        return "Vmid (about 1.1V)" + (", soft under the pulls: INN or C2, or a node behind a large resistance" if soft else ", firm: VMR, VMO, OUT1, SIG"), True
    if d_up > 1.0 or -d_dn > 0.6:
        return "floating: the jumper is not touching a node (this is not a circuit fault)", False
    return "neither ground, Vmid nor the rail, and firm: a node with the wrong level", True


def read(adc, n=20000):
    s = 0
    for _ in range(n):
        s += adc.read_u16()
    return s / n * 3.3 / 65535


def run():
    mem32[0x40050000 + 0xA0 + 0x3000] = 0xFF  # PWM slices off
    for p in (6, 8, 9):
        Pin(p, Pin.IN)
    g10 = Pin(10, Pin.OUT, value=0)
    g11 = Pin(11, Pin.OUT, value=0)
    adc28 = ADC(28)
    orig = mem32[PAD28]
    try:
        time.sleep(0.3)
        rest = read(adc28)
        mem32[PAD28] = (orig & ~(PUE | PDE)) | PUE
        time.sleep(0.5)
        up = read(adc28)
        mem32[PAD28] = orig & ~(PUE | PDE)
        time.sleep(1.5)
        mem32[PAD28] = (orig & ~(PUE | PDE)) | PDE
        time.sleep(0.5)
        dn = read(adc28)
    finally:
        mem32[PAD28] = orig
    label, on_node = classify(rest, up - rest, dn - rest)
    print(f"GP28 jumper row: rest {rest:.3f}V, pull-up {up - rest:+.2f}V, pull-down {dn - rest:+.2f}V  -> {label}")
    time.sleep(1.5)
    adc_a, adc_b = ADC(26), ADC(27)
    g10.value(1)
    time.sleep(1.5)
    a = read(adc_a)
    g10.value(0)
    g11.value(1)
    time.sleep(1.5)
    b = read(adc_b)
    g11.value(0)
    for name, v, sw in (("A (GP26), S1 closed", a, "S1"), ("B (GP27), S2 closed", b, "S2")):
        ok = abs(v - VMID) < VMID_TOL
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {v:.3f}V, expected about {VMID:.2f}V (OUT1 at Vmid through {sw})")


try:
    run()
finally:
    Pin(10, Pin.IN)
    Pin(11, Pin.IN)
