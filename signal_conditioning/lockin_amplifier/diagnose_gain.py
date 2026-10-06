"""
diagnose_gain.py — lockin_amplifier (MicroPython, Raspberry Pi Pico)

Reads the 1kHz ripple on ONE extra node, to find which stage is making the
in-phase reading too large. Wire a single jumper from the node to GP28 (pin
34), run

    mpremote mount . run diagnose_gain.py

(the mount lets this script import main.py's register code). Remove the
jumper when done. Start with SIG: it splits the circuit in two.

  SIG  -> GP28   expected swing about 3.3mV peak-to-peak. About 3mV means the
                 source side is right and the gain stage is the problem;
                 about 15mV means the source side (Rbias or a source 1MΩ) is.
  OUT1 -> GP28   expected swing about 0.30V peak-to-peak (a gain stage that
                 is too hot clips at about 0V and 1.8V, so a reading near
                 1.5V means clipped, not a measurement of the gain)

The Pico drives the same in-phase test signal as main.py, samples GP28 as
fast as MicroPython can, folds the samples onto the 1ms period, and reports
the peak-to-peak of the folded average, minus the same measurement with the
test signal off (clock pickup and ADC noise).
"""

import time
from machine import ADC

import main

PROBE_PIN = 28
N_SAMPLES = 6000
BINS = 20
PERIOD_US = 1000
VREF = 3.3


def fold_pp(adc):
    """Peak-to-peak (volts) of the 1kHz component, from folded samples."""
    sums = [0] * BINS
    counts = [0] * BINS
    t0 = time.ticks_us()
    for _ in range(N_SAMPLES):
        v = adc.read_u16()
        t = time.ticks_diff(time.ticks_us(), t0) % PERIOD_US
        b = t * BINS // PERIOD_US
        sums[b] += v
        counts[b] += 1
    means = [s / c for s, c in zip(sums, counts) if c]
    return (max(means) - min(means)) * VREF / 65535, len(means), sum(means) / len(means) * VREF / 65535


def run():
    adc = ADC(PROBE_PIN)
    main.start()
    out = {}
    for name, sig in (("signal off", "off"), ("in phase", "in")):
        main.set_state(sig, 0, False)
        time.sleep(main.SETTLE_S)
        pp, nbins, dc = fold_pp(adc)
        out[name] = pp
        print(f"{name:11s} pp {pp*1e3:7.1f}mV  mean {dc:.3f}V  ({nbins} of {BINS} phase bins filled)")
    net = out["in phase"] - out["signal off"]
    print(f"test-signal ripple on GP{PROBE_PIN}: {net*1e3:.1f}mV peak-to-peak")
    print("expected: SIG about 3.3mV, OUT1 about 300mV")


try:
    run()
finally:
    main.shutdown()
