"""
smoke_test.py — signal_generator_ad9833

Safety: the driver only touches GP17/GP18/GP19 (FSYNC, SCLK, SDATA) and
GP26 through the ADC, leaves FSYNC high between words, and ends with the
chip in reset (midscale, quiet). (That OUT can't exceed the ADC pin's 3.3V
rests on the module being powered from 3V3: the square-wave mode swings the
chip's own supply. That is a wiring rule, in breadboard.md, not testable here.)

Functional: the frequency word and control words match the AD9833 data
sheet's formulas (f = word * MCLK / 2^28, B28 two-write loading, reset
bit, OPBITEN/DIV2/MODE for square and triangle); a model of the chip's
registers, driven by the real write sequence, ends up at the requested
frequency to within one tuning step and in the requested waveform mode;
the waveform analysis measures amplitude, shape and frequency of synthetic
sine, triangle and square signals with noise and offset; and the bench
check's pass/fail logic passes a healthy module and fails a module with a
16MHz clock, a flat output and a bipolar-looking (mean 0V) output.
"""

import math
import os
import random
import sys
import types

HERE = os.path.dirname(__file__)
failures = []


def check(label, condition, detail):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}: {detail}")
    if not condition:
        failures.append(label)


sys.modules["machine"] = types.SimpleNamespace()
sys.path.insert(0, HERE)
import main as drv  # noqa: E402

# --- words, against the data sheet's formulas -------------------------------
w = drv.freq_word(1000.0)
check("functional — 1kHz at 25MHz is word 10737", w == 10737, f"{w}")
check("functional — the word is within one step of the request", abs(drv.actual_freq(w) - 1000.0) <= 25e6 / 2**28, f"{drv.actual_freq(w):.4f}Hz, step {25e6/2**28:.4f}Hz")
check("functional — 12.5MHz (MCLK/2) is the largest word and fits 28 bits", drv.freq_word(12.5e6) == 2**27, hex(drv.freq_word(12.5e6)))
try:
    drv.freq_word(13e6)
    rejected = False
except ValueError:
    rejected = True
check("functional — a frequency above MCLK/2 is refused", rejected, "ValueError")
check("functional — control words: sine 0x2000, triangle 0x2002, square 0x2028, reset 0x2100", (drv.CTRL_SINE, drv.CTRL_TRIANGLE, drv.CTRL_SQUARE, drv.CTRL_RESET) == (0x2000, 0x2002, 0x2028, 0x2100), "")
seq = drv.program_words(1000.0)
check("functional — sequence is reset, FREQ0 low 14, FREQ0 high 14, phase 0, wave", seq[0] == 0x2100 and seq[1] == 0x4000 | (10737 & 0x3FFF) and seq[2] == 0x4000 | (10737 >> 14) and seq[3] == 0xC000 and seq[4] == 0x2000, [hex(x) for x in seq])


# --- a model of the chip's registers ---------------------------------------
class Chip:
    def __init__(self):
        self.ctrl = 0
        self.freq0 = 0
        self.pending_low = None
        self.reset = True

    def word(self, w):
        top = w >> 14
        if top == 0b00:
            self.ctrl = w
            self.reset = bool(w & 0x100)
        elif top == 0b01:  # FREQ0, B28 mode: low half then high half
            assert self.ctrl & 0x2000, "B28 must be set for a two-write frequency load"
            if self.pending_low is None:
                self.pending_low = w & 0x3FFF
            else:
                self.freq0 = (w & 0x3FFF) << 14 | self.pending_low
                self.pending_low = None
        return

    def mode(self):
        if self.ctrl & 0x20:
            return "square"
        return "triangle" if self.ctrl & 0x2 else "sine"


class Pin:
    log = []

    def __init__(self, n):
        self.n, self.v = n, None

    def value(self, v):
        self.v = v
        Pin.log.append((self.n, v))


class Spi:
    def __init__(self, chip, fsync):
        self.chip, self.fsync, self.words = chip, fsync, 0

    def write(self, b):
        assert self.fsync.v == 0, "SPI write while FSYNC is high"
        assert len(b) == 2
        self.chip.word(int.from_bytes(b, "big"))
        self.words += 1


chip = Chip()
fs = Pin(17)
spi = Spi(chip, fs)
dds = drv.Ad9833(spi, fs)
dds.start(1000.0, drv.CTRL_TRIANGLE)
check("functional — chip ends at the requested frequency, in triangle mode, out of reset", abs(drv.actual_freq(chip.freq0) - 1000.0) <= 25e6 / 2**28 and chip.mode() == "triangle" and not chip.reset, f"{drv.actual_freq(chip.freq0):.3f}Hz, {chip.mode()}, reset={chip.reset}")
check("smoke — FSYNC is high between words and every word had 16 bits", fs.v == 1 and spi.words == 5, f"FSYNC={fs.v}, {spi.words} words")
dds.start(12.5e6 / 2, drv.CTRL_SQUARE)
check("functional — square mode selected", chip.mode() == "square", f"ctrl {chip.ctrl:#06x}")
dds.hold()
check("smoke — hold() leaves the chip in reset", chip.reset and fs.v == 1, f"ctrl {chip.ctrl:#06x}")


# --- analysis on synthetic waveforms ----------------------------------------
random.seed(3)
FS = drv.FS_HZ


def synth(shape, f, pp, mean, noise_mv=1.5, n=4000, phase=0.37):
    out = []
    for i in range(n):
        t = i / FS * f + phase
        frac = t - math.floor(t)
        if shape == "sine":
            y = math.sin(2 * math.pi * frac)
        elif shape == "tri":
            y = 4 * abs(frac - 0.5) - 1
        elif shape == "square":
            y = 1.0 if frac < 0.5 else -1.0
        else:
            y = 0.0
        out.append(mean + pp / 2 * y + random.gauss(0, noise_mv * 1e-3))
    return out


def a(shape, f, pp, mean):
    return drv.analyze(synth(shape, f, pp, mean), scale=1.0)


f_nom = drv.actual_freq(drv.freq_word(1000.0))
healthy = {
    "reset": a("flat", 0, 0, 0.34),
    "sine1k": a("sine", f_nom, 0.61, 0.34),
    "sine10k": a("sine", 10 * f_nom, 0.61, 0.34),
    "tri": a("tri", f_nom, 0.61, 0.34),
    "square": a("square", f_nom, 3.3, 1.65),
}
m, pp, crest, f = healthy["sine1k"]
check("functional — analysis reads a 1kHz, 0.61V sine to 0.1% in frequency and 10mV in amplitude", abs(f - f_nom) / f_nom < 1e-3 and abs(pp - 0.61) < 0.01 and abs(crest - 0.3536) < 0.01, f"{f:.2f}Hz, {pp:.3f}Vpp, rms/pp {crest:.3f}")
check("functional — analysis reads a 10kHz sine to 0.5%", abs(healthy["sine10k"][3] / (10 * f_nom) - 1) < 5e-3, f"{healthy['sine10k'][3]:.1f}Hz")
check("functional — a triangle reads rms/pp 0.289 and a square 0.5", abs(healthy["tri"][2] - 0.2887) < 0.01 and abs(healthy["square"][2] - 0.5) < 0.01, f"tri {healthy['tri'][2]:.3f}, square {healthy['square'][2]:.3f}")
check("functional — a healthy module passes every check", all(ok for _, ok, _ in drv.evaluate(healthy)), "")

bad_clock = dict(healthy, sine1k=a("sine", f_nom * 16 / 25, 0.61, 0.34), sine10k=a("sine", 10 * f_nom * 16 / 25, 0.61, 0.34))
res = {lab: ok for lab, ok, _ in drv.evaluate(bad_clock)}
check("functional — a 16MHz module clock fails the clock check but passes the ratio check", not res["module clock is 25MHz"] and res["10kHz is ten times 1kHz"], f"{[k for k, v in res.items() if not v]}")
flat = dict(healthy, sine1k=a("flat", 0, 0, 0.34))
check("functional — a flat output fails the amplitude check", not all(ok for _, ok, _ in drv.evaluate(flat)), "no output")
bipolar = dict(healthy, sine1k=a("sine", f_nom, 0.61, 0.0))
check("functional — a mean-0V sine fails the unipolar check", not dict((l, ok) for l, ok, _ in drv.evaluate(bipolar))["1kHz sine sits above ground (unipolar output)"], "mean 0V")
noisy_reset = dict(healthy, reset=a("sine", 1000, 0.3, 0.34))
check("functional — output still swinging in reset fails the reset check", not dict((l, ok) for l, ok, _ in drv.evaluate(noisy_reset))["output is quiet in reset"], "0.3V swing")

# --- supply and pins ---------------------------------------------------------
src = open(os.path.join(HERE, "main.py")).read()
import re  # noqa: E402

pins = set(int(x) for x in re.findall(r"Pin\((\d+)", src))
check("smoke — driver names only GP17/18/19 as pins (GP26 only through ADC)", pins <= {17, 18, 19}, str(sorted(pins)))

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
