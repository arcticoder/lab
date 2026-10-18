"""
main.py — signal_generator_ad9833 (MicroPython, Raspberry Pi Pico)

Bring-up check for an AD9833 DDS module (`TESTSIG`). The Pico programs the
chip over SPI0 (FSYNC=GP17, SCLK=GP18, SDATA=GP19) and reads the module's OUT
pin on its own ADC (GP26) through DMA at 100kSa/s, so the whole check needs
one wire from OUT to GP26 and no instrument.

    mpremote run main.py        (about 3 seconds)

What it checks: the output is quiet and at midscale while the chip is held in
reset; a 1kHz sine has the datasheet's 0.6V peak-to-peak swing above ground;
the module's clock is what the frequency words assume (25MHz) — the number
reported as the implied MCLK is what every later use of the module needs;
10kHz comes out ten times 1kHz; triangle and square wave have their own
shapes. SPI mode, control bits and register layout follow the AD9833 data
sheet (Rev. E): SCLK idles high and data is sampled on the falling edge
(SPI mode 2, CPOL=1 CPHA=0), 16-bit words MSB first, FSYNC low around each
word, B28=1 so a frequency takes two writes (14 LSBs then 14 MSBs).
"""

import array
import time

MCLK_NOM = 25_000_000
TWO28 = 1 << 28

# control register: D13 B28, D8 RESET, D5 OPBITEN, D3 DIV2, D1 MODE
CTRL_SINE = 0x2000
CTRL_TRIANGLE = 0x2002
CTRL_SQUARE = 0x2028  # OPBITEN + DIV2: the DAC's MSB at the full rate, VDD swing
CTRL_RESET = 0x2100
FREQ0 = 0x4000  # D15 D14 = 01
PHASE0 = 0xC000  # D15 D14 D13 = 110

# ADC with DMA (RP2040 datasheet register map; checked on a Pico 2026-10-17:
# DIV INT 479 -> 100kSa/s, INT 0 -> 499kSa/s)
ADC_BASE = 0x4004C000
ADC_CS, ADC_FCS, ADC_FIFO, ADC_DIV = 0x00, 0x08, 0x0C, 0x10
ADC_DREQ = 36
FS_HZ = 100_000
DIV_INT = 479  # 48MHz / 480
N_SAMPLES = 4000
SKIP = 64  # the first conversions after the ADC starts are not clean
VREF = 3.3
COUNTS = 4095  # the FIFO holds 12-bit counts

# check limits
FLAT_PP_MAX = 0.020  # volts, output held in reset
SINE_PP = (0.45, 0.75)  # datasheet: 38mV..650mV, 0.6V typical
SINE_MEAN = (0.25, 0.45)
MCLK_TOL = 0.03
RATIO_TOL = 0.01
CREST_SINE = 0.3536  # rms / peak-to-peak
CREST_TRI = 0.2887
CREST_SQUARE = 0.5
CREST_TOL = 0.04
SQUARE_PP_MIN = 2.5


def freq_word(f_hz, mclk=MCLK_NOM):
    word = round(f_hz * TWO28 / mclk)
    if not 0 <= word <= TWO28 // 2:  # above MCLK/2 the output aliases; the chip is specified to MCLK/2
        raise ValueError(f"{f_hz}Hz is outside 0..{mclk // 2}Hz")
    return word


def actual_freq(word, mclk=MCLK_NOM):
    return word * mclk / TWO28


def program_words(f_hz, ctrl=CTRL_SINE, mclk=MCLK_NOM):
    """The full write sequence: reset, frequency in two halves, phase 0, leave reset."""
    w = freq_word(f_hz, mclk)
    return [
        CTRL_RESET,
        FREQ0 | (w & 0x3FFF),
        FREQ0 | (w >> 14),
        PHASE0,
        ctrl,
    ]


class Ad9833:
    def __init__(self, spi, fsync):
        self.spi = spi
        self.fsync = fsync
        self.fsync.value(1)

    def write(self, word):
        self.fsync.value(0)
        self.spi.write(word.to_bytes(2, "big"))
        self.fsync.value(1)

    def start(self, f_hz, ctrl=CTRL_SINE, mclk=MCLK_NOM):
        for w in program_words(f_hz, ctrl, mclk):
            self.write(w)

    def hold(self):
        """Output at midscale and quiet."""
        self.write(CTRL_RESET)


def capture(pin=26):
    """N_SAMPLES (after SKIP start-up samples) of ADC counts from `pin` at
    FS_HZ by DMA, as an array('H'). Counts, not volts: a list of 4000 floats
    does not fit the Pico's heap twice."""
    import gc
    import rp2
    from machine import ADC, mem32

    gc.collect()
    ADC(pin)  # puts the pad in analog mode
    buf = array.array("H", bytes(2 * (N_SAMPLES + SKIP)))
    mem32[ADC_BASE + ADC_CS] = 0
    mem32[ADC_BASE + ADC_DIV] = DIV_INT << 8
    mem32[ADC_BASE + ADC_FCS] = 1 | (1 << 3) | (1 << 24)  # EN, DREQ_EN, THRESH 1
    dma = rp2.DMA()
    ctrl = dma.pack_ctrl(size=1, inc_read=False, inc_write=True, treq_sel=ADC_DREQ)
    dma.config(read=ADC_BASE + ADC_FIFO, write=buf, count=N_SAMPLES + SKIP, ctrl=ctrl, trigger=False)
    mem32[ADC_BASE + ADC_CS] = 1 | ((pin - 26) << 12) | (1 << 3)  # EN, AINSEL, START_MANY
    dma.active(1)
    while dma.active():
        pass
    mem32[ADC_BASE + ADC_CS] = 1
    dma.close()
    mem32[ADC_BASE + ADC_FCS] = 0
    return buf[SKIP:]


def analyze(samples, fs=FS_HZ, scale=VREF / COUNTS):
    """Mean and peak-to-peak (times `scale`, volts for ADC counts), rms/peak-to-peak
    and frequency (Hz, 0 if under 3 cycles) of a sequence of samples."""
    n = len(samples)
    mean = sum(samples) / n
    pp = max(samples) - min(samples)
    rms = (sum((v - mean) ** 2 for v in samples) / n) ** 0.5
    crest = rms / pp if pp else 0.0
    # rising crossings of the mean, with a little hysteresis, interpolated
    hyst = max(pp * 0.1, 0.0016 / scale)  # about two ADC counts
    xs = []
    armed = False
    prev = samples[0]
    for i in range(1, n):
        v = samples[i]
        if v < mean - hyst:
            armed = True
        elif armed and prev < mean <= v:
            xs.append(i - 1 + (mean - prev) / (v - prev))
            armed = False
        prev = v
    freq = (len(xs) - 1) * fs / (xs[-1] - xs[0]) if len(xs) >= 3 else 0.0
    return mean * scale, pp * scale, crest, freq


def evaluate(r):
    """r: {'reset', 'sine1k', 'sine10k', 'tri', 'square'} -> analyze() tuples.
    Returns [(label, ok, detail)]."""
    out = []
    _, pp, _, _ = r["reset"]
    out.append(("output is quiet in reset", pp <= FLAT_PP_MAX, f"{pp*1e3:.1f}mV peak-to-peak, limit {FLAT_PP_MAX*1e3:.0f}mV"))
    mean, pp, crest, f1 = r["sine1k"]
    out.append(("1kHz sine swings about 0.6V", SINE_PP[0] <= pp <= SINE_PP[1], f"{pp:.3f}V peak-to-peak, limits {SINE_PP}"))
    out.append(("1kHz sine sits above ground (unipolar output)", SINE_MEAN[0] <= mean <= SINE_MEAN[1], f"mean {mean:.3f}V, limits {SINE_MEAN}"))
    out.append(("1kHz sine has a sine's shape", abs(crest - CREST_SINE) <= CREST_TOL, f"rms/pp {crest:.3f}, expected {CREST_SINE}"))
    implied = MCLK_NOM * f1 / actual_freq(freq_word(1000.0))
    out.append(("module clock is 25MHz", abs(implied / MCLK_NOM - 1) <= MCLK_TOL, f"implied MCLK {implied/1e6:.3f}MHz from {f1:.1f}Hz measured, limit ±{MCLK_TOL*100:.0f}%"))
    f10 = r["sine10k"][3]
    ratio = f10 / f1 if f1 else 0.0
    out.append(("10kHz is ten times 1kHz", abs(ratio / 10 - 1) <= RATIO_TOL, f"ratio {ratio:.3f}, limit ±{RATIO_TOL*100:.0f}%"))
    out.append(("triangle has a triangle's shape", abs(r["tri"][2] - CREST_TRI) <= CREST_TOL, f"rms/pp {r['tri'][2]:.3f}, expected {CREST_TRI}"))
    _, pp, crest, _ = r["square"]
    out.append(("square output swings the logic range", pp >= SQUARE_PP_MIN and abs(crest - CREST_SQUARE) <= CREST_TOL, f"{pp:.2f}V peak-to-peak, rms/pp {crest:.3f} (expected 0.5)"))
    return out


def run():
    from machine import Pin, SPI

    fsync = Pin(17, Pin.OUT, value=1)
    spi = SPI(0, baudrate=1_000_000, polarity=1, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(18), mosi=Pin(19))
    dds = Ad9833(spi, fsync)
    results = {}
    try:
        dds.hold()
        time.sleep(0.2)
        results["reset"] = analyze(capture())
        for name, f, ctrl in (("sine1k", 1000.0, CTRL_SINE), ("sine10k", 10000.0, CTRL_SINE), ("tri", 1000.0, CTRL_TRIANGLE), ("square", 1000.0, CTRL_SQUARE)):
            dds.start(f, ctrl)
            time.sleep(0.2)
            results[name] = analyze(capture())
            print(f"{name:8s} mean {results[name][0]:.3f}V  pp {results[name][1]:.3f}V  rms/pp {results[name][2]:.3f}  {results[name][3]:.1f}Hz")
    finally:
        dds.hold()
    ok_all = True
    for label, ok, detail in evaluate(results):
        print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    run()
