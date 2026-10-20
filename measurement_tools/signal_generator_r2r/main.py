"""
main.py — signal_generator_r2r (MicroPython, Raspberry Pi Pico / RP2040-Zero)

A software DDS: one PIO state machine clocks bytes out to an 8-bit R-2R ladder
on GP0..GP7 (bit 0 = GP0), two DMA channels feed it a sine table from RAM in an
endless loop, and an LM358 buffers the ladder. After start() the CPU does
nothing per sample. The output frequency is the PIO clock divided by the table
length, so a frequency change is one register write (the PIO clock divider).

    mpremote run main.py         (about 20 seconds)

The bring-up check calibrates the ladder against the Pico's ADC (GP26 reads the
buffer's output), then plays 1kHz sine tables, uncalibrated and calibrated,
and reports amplitude, frequency, distortion and where the output stops
following as the frequency rises. SPI-free, no extra part beyond the ladder.

Facts used (RP2040 datasheet, read 2026-10-19): PIO0 TX FIFO 0 at 0x50200010,
SM clock divider at 0x50200C8 (INT in 31:16, FRAC in 15:8, f = sysclk /
(INT + FRAC/256)), DREQ_PIO0_TX0 = 0; a DMA channel cannot chain to itself, so
two channels chain to each other; DMA ring wrap needs the table aligned to its
own size; DMA TRANS_COUNT reloads on every trigger.
"""

import array
import math
import time

PIN_BASE = 0  # bit 0 on GP0 .. bit 7 on GP7 (GP0..GP7 are on the RP2040-Zero's header too)
BITS = 8
PIO_BASES = (0x50200000, 0x50300000)  # PIO0, PIO1
TXF0, SM_CLKDIV, SM_STRIDE = 0x10, 0xC8, 0x18
DREQ_PIO0_TX0 = 0
N_MIN, N_MAX = 32, 4096  # table length in bytes, powers of two
DIV_PREF256 = 16 * 256  # prefer a PIO divider of at least 16: finer frequency steps
DIV_MIN256 = 256  # divider 1.0: one sample per system clock
ADC_BASE = 0x4004C000
ADC_CS, ADC_FCS, ADC_FIFO, ADC_DIV = 0x00, 0x08, 0x0C, 0x10
ADC_DREQ = 36
ADC_PIN = 26
SKIP = 64
VREF, COUNTS = 3.3, 4095

# the bring-up check's expectations (provisional: set from the netlist and the
# data sheets, to be tightened after the first bench run)
SPAN_V = (1.30, 1.80)  # code 255 minus code 0 at the buffer output; ideal about 1.64V
WEIGHT_TOL = 0.15  # each bit's step against 2^k LSBs
FREQ_TOL = 0.002
PP_TOL = 0.12
THD_UNCAL_DB = -28.0
THD_CAL_DB = -40.0
CEILING_MIN_HZ = 10_000
AMP = 100  # peak, in codes; with offset 128 the sine spans codes 28..228 (0.2..1.4V)
OFFSET = 128


# --- planning -----------------------------------------------------------------


def plan(f_hz, sysclk=125_000_000):
    """(table length n, divider in 1/256 units). Largest n whose divider is at
    least 16, else the largest whose divider is at least 1."""
    for floor in (DIV_PREF256, DIV_MIN256):
        n = N_MAX
        while n >= N_MIN:
            div256 = round(sysclk * 256 / (f_hz * n))
            if floor <= div256 < 65536 * 256:
                return n, div256
            n //= 2
    raise ValueError(f"{f_hz}Hz is outside what the PIO clock and a {N_MIN}-byte table can make")


def actual_freq(n, div256, sysclk=125_000_000):
    return sysclk * 256 / (div256 * n)


def clkdiv_reg(div256):
    return ((div256 >> 8) << 16) | ((div256 & 0xFF) << 8)


def ilog2(n):
    k = 0  # MicroPython ints have no bit_length()
    while n > 1:
        n >>= 1
        k += 1
    return k


def unit_quarter(n):
    """sin(2*pi*i/n) for i = 0..n/4, as floats."""
    q = n // 4
    return array.array("f", [math.sin(math.pi / 2 * i / q) for i in range(q + 1)])


def make_table(buf, n, amp=AMP, offset=OFFSET, nearest=None):
    """Fill buf[0:n] with one sine period. `nearest(target)` maps a target in
    code units about `offset` to a code (the calibrated path); default is
    rounding. Uses the quarter-wave symmetry, so only n/4 sines are computed."""
    q = n // 4
    s = unit_quarter(n)
    for i in range(q + 1):
        t = amp * s[i]
        up = nearest(t) if nearest else offset + round(t)
        dn = nearest(-t) if nearest else offset - round(t)
        buf[i] = up
        buf[n // 2 - i] = up
        buf[n // 2 + i] = dn
        buf[(n - i) % n] = dn
    return buf


# --- the PIO program and the generator ----------------------------------------


try:
    import rp2

    @rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * BITS, out_shiftdir=rp2.PIO.SHIFT_RIGHT, autopull=True, pull_thresh=32)
    def _dac():
        out(pins, 8)  # noqa: F821 — PIO assembler: one byte to the ladder per state-machine clock

except ImportError:  # host-side tests without the rp2 module
    _dac = None


def aligned_buffer(size):
    """A bytearray's memory view, aligned to `size` (the DMA ring needs it)."""
    import uctypes

    raw = bytearray(2 * size)
    off = (-uctypes.addressof(raw)) % size
    return raw, memoryview(raw)[off : off + size], uctypes.addressof(raw) + off


class Dds:
    def __init__(self, sm_id=0, pin_base=PIN_BASE):
        import machine
        import rp2

        self.sysclk = machine.freq()
        self.sm_id = sm_id
        self.pio_base = PIO_BASES[sm_id // 4]
        self.sm = rp2.StateMachine(sm_id)
        self.pin_base = pin_base
        self.raw, self.table, self.addr = aligned_buffer(N_MAX)
        self.a = self.b = None
        self.n = 0
        self.div256 = 0

    def _set_div(self, div256):
        from machine import mem32

        mem32[self.pio_base + SM_CLKDIV + SM_STRIDE * (self.sm_id % 4)] = clkdiv_reg(div256)
        self.div256 = div256

    def start(self, f_hz, amp=AMP, offset=OFFSET, nearest=None, n_div=None):
        """Play a sine at f_hz; returns the frequency actually produced.
        n_div=(table length, divider*256) overrides the planner (loopback_test.py)."""
        import rp2

        import machine

        self.stop()
        # stop() left the pins as plain outputs: init() hands them back to the PIO
        self.sm.init(_dac, freq=self.sysclk, out_base=machine.Pin(self.pin_base))
        n, div256 = n_div or plan(f_hz, self.sysclk)
        make_table(self.table, n, amp, offset, nearest)
        self.n = n
        self.a, self.b = rp2.DMA(), rp2.DMA()
        txf = self.pio_base + TXF0 + 4 * (self.sm_id % 4)
        dreq = DREQ_PIO0_TX0 + (8 if self.sm_id >= 4 else 0) + (self.sm_id % 4)
        for me, other in ((self.a, self.b), (self.b, self.a)):
            ctrl = me.pack_ctrl(size=2, inc_read=True, inc_write=False, ring_size=ilog2(n), ring_sel=0, treq_sel=dreq, chain_to=other.channel)
            me.config(read=self.addr, write=txf, count=n // 4, ctrl=ctrl, trigger=False)
        self._set_div(div256)
        self.sm.active(1)
        self.a.active(1)
        return actual_freq(n, div256, self.sysclk)

    def set_freq(self, f_hz):
        """Change frequency. Same table length: one register write, no glitch."""
        n, div256 = plan(f_hz, self.sysclk)
        if n == self.n and self.a is not None:
            self._set_div(div256)
            return actual_freq(n, div256, self.sysclk)
        raise ValueError("table length changes at this frequency: call start() again")

    def stop(self):
        """Stop and park the ladder at code 0."""
        from machine import Pin

        if self.a is not None:
            for _ in range(4):
                self.a.active(0)
                self.b.active(0)
            self.a.close()
            self.b.close()
            self.a = self.b = None
        self.sm.active(0)
        for i in range(BITS):
            Pin(self.pin_base + i, Pin.OUT, value=0)
        self.n = 0


# --- measurement ---------------------------------------------------------------


def capture(pin=ADC_PIN, n_samples=4000, div_int=479):
    """n_samples of ADC counts from `pin` by DMA (div_int 479: 100kSa/s, 0: 499kSa/s)."""
    import gc
    import rp2
    from machine import ADC, mem32

    gc.collect()
    ADC(pin)
    buf = array.array("H", bytes(2 * (n_samples + SKIP)))
    mem32[ADC_BASE + ADC_CS] = 0
    mem32[ADC_BASE + ADC_DIV] = div_int << 8
    mem32[ADC_BASE + ADC_FCS] = 1 | (1 << 3) | (1 << 24)
    dma = rp2.DMA()
    ctrl = dma.pack_ctrl(size=1, inc_read=False, inc_write=True, treq_sel=ADC_DREQ)
    dma.config(read=ADC_BASE + ADC_FIFO, write=buf, count=n_samples + SKIP, ctrl=ctrl, trigger=False)
    mem32[ADC_BASE + ADC_CS] = 1 | ((pin - 26) << 12) | (1 << 3)
    dma.active(1)
    while dma.active():
        pass
    mem32[ADC_BASE + ADC_CS] = 1
    dma.close()
    mem32[ADC_BASE + ADC_FCS] = 0
    return buf[SKIP:]


def analyze(samples, fs, scale=VREF / COUNTS):
    """(mean, peak-to-peak, frequency) of a sine; mean and pp times `scale`."""
    n = len(samples)
    mean = sum(samples) / n
    pp = max(samples) - min(samples)
    hyst = max(pp * 0.1, 0.0016 / scale)
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
    return mean * scale, pp * scale, freq


def goertzel(samples, mean, f, fs):
    """Amplitude of the component at f (same units as samples)."""
    w = 2 * math.pi * f / fs
    c = 2 * math.cos(w)
    s1 = s2 = 0.0
    for v in samples:
        s0 = (v - mean) + c * s1 - s2
        s2 = s1
        s1 = s0
    return math.sqrt(max(s1 * s1 + s2 * s2 - c * s1 * s2, 0.0)) * 2 / len(samples)


def thd_db(samples, f, fs, harmonics=range(2, 10)):
    """Distortion below the fundamental, in dB, from harmonics 2..9 below Nyquist."""
    mean = sum(samples) / len(samples)
    a1 = goertzel(samples, mean, f, fs)
    sq = 0.0
    for k in harmonics:
        if k * f < fs / 2 * 0.95:
            sq += goertzel(samples, mean, k * f, fs) ** 2
    return 20 * math.log10(max(math.sqrt(sq), 1e-12) / max(a1, 1e-12))


def levels_from(adc_read, set_code, settle_s=0.002):
    """Volts at the buffer output for each of the 256 codes."""
    lv = array.array("f", bytes(4 * 256))
    for code in range(256):
        set_code(code)
        time.sleep(settle_s)
        lv[code] = adc_read()
    return lv


def calibrator(levels, amp=AMP, offset=OFFSET):
    """`nearest(target)` for make_table: the code whose measured level is closest
    to the level a perfect DAC would give at offset + target."""
    order = sorted(range(256), key=lambda c: levels[c])
    sl = [levels[c] for c in order]
    lo, hi = levels[offset - amp], levels[offset + amp]
    mid, half = (lo + hi) / 2, (hi - lo) / 2

    def nearest(t):
        x = mid + half * t / amp
        a, b = 0, 255
        while a < b:  # first sorted level >= x
            m = (a + b) // 2
            if sl[m] < x:
                a = m + 1
            else:
                b = m
        if a > 0 and abs(sl[a - 1] - x) <= abs(sl[a] - x):
            a -= 1
        return order[a]

    return nearest


def evaluate(r):
    """r: dict from the bring-up run. Returns [(label, ok, detail)]."""
    out = []
    lv = r["levels"]
    span = lv[255] - lv[0]
    out.append(("ladder spans the expected swing", SPAN_V[0] <= span <= SPAN_V[1], f"{span:.3f}V between code 0 and code 255, limits {SPAN_V}"))
    lsb = span / 255
    bad = []
    for k in range(BITS):
        w = lv[1 << k] - lv[0]
        ratio = w / (lsb * (1 << k))
        if abs(ratio - 1) > WEIGHT_TOL and (1 << k) * lsb > 0.02:
            bad.append(f"bit {k} {ratio:.2f}")
    out.append(("each bit weighs 2^k steps (R-2R ratios hold)", not bad, "all within ±%d%%" % (WEIGHT_TOL * 100) if not bad else "off: " + ", ".join(bad)))
    f_set = r["f_set"]
    f_meas = r["cal"][2]
    out.append(("1kHz sine comes out at the planned frequency", abs(f_meas / f_set - 1) <= FREQ_TOL, f"{f_meas:.2f}Hz measured, {f_set:.2f}Hz planned, limit ±{FREQ_TOL*100:.1f}%"))
    expect_pp = (lv[OFFSET + AMP] - lv[OFFSET - AMP])
    out.append(("amplitude matches the measured ladder levels", abs(r["cal"][1] / expect_pp - 1) <= PP_TOL, f"{r['cal'][1]:.3f}V p-p against {expect_pp:.3f}V from the levels"))
    out.append(("uncalibrated sine distortion", r["thd_uncal"] <= THD_UNCAL_DB, f"{r['thd_uncal']:.1f}dB, limit {THD_UNCAL_DB}dB"))
    out.append(("calibrated sine distortion", r["thd_cal"] <= THD_CAL_DB, f"{r['thd_cal']:.1f}dB, limit {THD_CAL_DB}dB"))
    out.append(("calibration does not make it worse", r["thd_cal"] <= r["thd_uncal"] + 1.0, f"{r['thd_uncal']:.1f}dB -> {r['thd_cal']:.1f}dB"))
    out.append(("amplitude holds to 10kHz", r["ceiling_hz"] >= CEILING_MIN_HZ, f"output within 10% of its 1kHz size up to {r['ceiling_hz']/1e3:.0f}kHz, limit {CEILING_MIN_HZ/1e3:.0f}kHz"))
    return out


def run():
    from machine import ADC, Pin

    dds = Dds()
    adc = ADC(ADC_PIN)
    pins = [Pin(PIN_BASE + i, Pin.OUT, value=0) for i in range(BITS)]

    def set_code(c):
        for i in range(BITS):
            pins[i].value((c >> i) & 1)

    def read():
        s = 0
        for _ in range(256):
            s += adc.read_u16()
        return s / 256 / 65535 * VREF

    r = {}
    try:
        r["levels"] = lv = levels_from(read, set_code)
        print(f"levels: code 0 {lv[0]:.3f}V, 128 {lv[128]:.3f}V, 255 {lv[255]:.3f}V")
        nearest = calibrator(lv)
        for name, nr in (("uncal", None), ("cal", nearest)):
            r["f_set"] = dds.start(1000.0, nearest=nr)
            time.sleep(0.05)
            s = capture()
            m, pp, f = analyze(s, 100_000)
            r[name] = (m, pp, f)
            r["thd_" + name] = thd_db(s, f, 100_000)
            print(f"{name:6s} mean {m:.3f}V  pp {pp:.3f}V  {f:.2f}Hz  distortion {r['thd_' + name]:.1f}dB")
        # frequency sweep with the calibrated table: where does the amplitude fall?
        ceiling = 1000
        base_pp = r["cal"][1]
        for f in (2000, 5000, 10_000, 20_000, 40_000, 80_000):
            dds.start(f, nearest=nearest)
            time.sleep(0.05)
            s = capture(div_int=0)
            m, pp, fm = analyze(s, 499_000)
            print(f"{f:6d}Hz: pp {pp:.3f}V ({pp / base_pp * 100:.0f}% of 1kHz), measured {fm:.0f}Hz")
            if pp >= 0.9 * base_pp and abs(fm / f - 1) < 0.05:
                ceiling = f
            else:
                break
        r["ceiling_hz"] = ceiling
    finally:
        dds.stop()
    ok_all = True
    for label, ok, detail in evaluate(r):
        print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    run()
