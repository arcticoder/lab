"""
trace_node.py — lockin_amplifier (MicroPython, Raspberry Pi Pico)

Says what the node on the GP28 jumper is connected to. Wire GP28 (pin 34) to
ONE row, run

    mpremote run trace_node.py

and read the four lines. Move the jumper to the next row and run it again.
No other wire moves, and nothing is written to the Pico's flash.

It uses only the Pico's own pins:
  - GP28's internal pull-up and pull-down (50-80kΩ) as a current injector:
    how far the node moves says how firmly something holds it.
  - GP8, GP9 and GP6 driven to constant 0 and 1: if one of the test-source
    resistors reaches this node, the node follows it.
  - GP8 toggled by software at about 1kHz: the same signal main.py uses.
GP10 and GP11 are set low so the demodulator switches stay off.

Expected on the row named SIG (design values, Rbias 1kΩ to Vmid, 1MΩ sources):
  rest 1.11-1.14V; pull-up +30..45mV, pull-down -16..-25mV;
  GP8/GP9 DC step 3.3mV, GP6 6.6mV; 1kHz step 3.3mV.
A node held by a much larger resistance moves by volts under the pulls. A node
no source reaches shows 0mV DC steps.
"""

import time
from machine import ADC, Pin, mem32

PAD = 0x4001C000 + 4 + 28 * 4
PWM_EN_CLR = 0x40050000 + 0xA0 + 0x3000
PUE, PDE = 1 << 3, 1 << 2
SOURCES = (8, 9, 6)

for p in (6, 8, 9):
    Pin(p, Pin.IN)
Pin(10, Pin.OUT, value=0)
Pin(11, Pin.OUT, value=0)
mem32[PWM_EN_CLR] = 0xFF
adc = ADC(28)
orig = mem32[PAD]


def mv(n=20000):
    s = 0
    for _ in range(n):
        s += adc.read_u16()
    return s / n * 3.3 / 65535 * 1e3


def pad(pu, pd):
    v = orig & ~(PUE | PDE)
    mem32[PAD] = v | (PUE if pu else 0) | (PDE if pd else 0)
    time.sleep(0.6)
    return mv()


def dc_step(pin):
    g = Pin(pin, Pin.OUT, value=0)
    time.sleep(1.0)
    a = mv()
    g.value(1)
    time.sleep(1.0)
    b = mv()
    g.value(0)
    time.sleep(1.0)
    c = mv()
    Pin(pin, Pin.IN)
    return b - (a + c) / 2


def ac_step(pin, n=30, reps=800):
    g = Pin(pin, Pin.OUT, value=0)
    hi = lo = 0.0
    for _ in range(reps):
        g.value(1)
        mv(2)
        hi += mv(n)
        g.value(0)
        mv(2)
        lo += mv(n)
    Pin(pin, Pin.IN)
    return (hi - lo) / reps


try:
    rest = pad(0, 0)
    up = pad(1, 0)
    pad(0, 0)
    time.sleep(1.5)
    pad(0, 0)
    dn = pad(0, 1)
    mem32[PAD] = orig
    time.sleep(1.5)
    print("rest %.3fV" % (rest / 1e3))
    print("pull-up %+.0fmV   pull-down %+.0fmV   (tens of mV: held firmly; over 1000mV: nearly floating)" % (up - rest, dn - rest))
    print("DC step   " + "   ".join("GP%d %+.2fmV" % (p, dc_step(p)) for p in SOURCES))
    print("1kHz step GP8 %+.2fmV" % ac_step(8))
finally:
    mem32[PAD] = orig
    for p in (6, 8, 9, 10, 11):
        Pin(p, Pin.IN)
