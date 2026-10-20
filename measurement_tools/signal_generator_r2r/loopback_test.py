"""
loopback_test.py — signal_generator_r2r (MicroPython, Raspberry Pi Pico / RP2040-Zero)

The digital half of the check, with no ladder and no wiring needed: the DDS plays
a sine table on GP0..GP7 and a second PIO state machine on the same block reads
those pins back at twice the sample rate into RAM by DMA. The captured bytes
must repeat the table exactly, over several periods, so this proves the table,
the DMA ring, the hand-off between the two DMA channels and the PIO clock all
work at each rate, without any analog part. (If the ladder is wired, it is
driven too; that is harmless.)

    mpremote mount . run loopback_test.py       (about 5 seconds)

Pass means every captured sample equals the table's sample for that instant.
The highest passing rate is the digital ceiling; the analog ceiling is the
LM358's (main.py measures it).
"""

import array
import time

import main as g

try:
    import rp2

    @rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT, autopush=True, push_thresh=32)
    def _cap():
        in_(pins, 8)  # noqa: F821 — PIO assembler: sample the eight ladder pins every clock

except ImportError:
    _cap = None

DREQ_PIO0_RX1 = 5
RXF1 = 0x24
# (table length, output divider x256, captured output samples). The capture
# divider is half of the output's. A short table means a DMA hand-off every 8
# words; 4096 is the table a 1kHz sine uses.
TESTS = (
    (256, 64 * 256, 2048),
    (256, 16 * 256, 2048),
    (256, 4 * 256, 2048),
    (256, 2 * 256, 2048),
    (32, 4 * 256, 2048),
    (32, 2 * 256, 2048),
    (4096, 7812, 6144),
)
OVERSAMPLE = 2


def best_match(table, n, cap, over=OVERSAMPLE):
    """(mismatches, samples compared, parity, shift) of the best alignment of the
    captured bytes against the table played in a loop."""
    best = None
    for parity in range(over):
        seq = bytes(cap[i] for i in range(parity, len(cap), over))  # MicroPython has no stepped slices
        if len(seq) < 16:
            continue
        for s in range(n):
            if table[s] != seq[0] or table[(s + 1) % n] != seq[1] or table[(s + 2) % n] != seq[2]:
                continue
            bad = sum(1 for i in range(len(seq)) if seq[i] != table[(s + i) % n])
            if best is None or bad < best[0]:
                best = (bad, len(seq), parity, s)
    return best


def capture_pins(sysclk, div256, n_bytes):
    from machine import Pin, mem32

    sm = rp2.StateMachine(1)
    sm.init(_cap, freq=sysclk, in_base=Pin(g.PIN_BASE))
    mem32[g.PIO_BASES[0] + g.SM_CLKDIV + g.SM_STRIDE * 1] = g.clkdiv_reg(div256)
    buf = array.array("I", bytes(n_bytes))
    dma = rp2.DMA()
    ctrl = dma.pack_ctrl(size=2, inc_read=False, inc_write=True, treq_sel=DREQ_PIO0_RX1)
    dma.config(read=g.PIO_BASES[0] + RXF1, write=buf, count=n_bytes // 4, ctrl=ctrl, trigger=False)
    dma.active(1)
    sm.active(1)
    t0 = time.ticks_ms()
    while dma.active() and time.ticks_diff(time.ticks_ms(), t0) < 2000:
        pass
    done = not dma.active()
    dma.active(0)
    sm.active(0)
    dma.close()
    return bytes(buf), done


def run():
    dds = g.Dds()
    ok_all = True
    try:
        for n, div256, samples in TESTS:
            f = dds.start(0, n_div=(n, div256))
            time.sleep(0.01)
            cap, done = capture_pins(dds.sysclk, max(div256 // OVERSAMPLE, 256), samples * OVERSAMPLE)
            m = best_match(bytes(dds.table[:n]), n, cap) if done else None
            if m is None:
                ok, detail = False, "capture did not complete" if not done else "captured bytes do not match the table at any alignment"
            else:
                ok, detail = m[0] == 0, f"{m[0]} of {m[1]} samples differ (parity {m[2]}, shift {m[3]})"
            print(f"[{'PASS' if ok else 'FAIL'}] {f/1e3:9.2f}kHz, {n}-byte table ({dds.sysclk/(div256/256)/1e6:.1f}MS/s): {detail}")
            ok_all = ok_all and ok
    finally:
        dds.stop()
    return 0 if ok_all else 1


if __name__ == "__main__":
    run()
