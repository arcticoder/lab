# signal_generator_r2r — software DDS sine generator on an R-2R ladder (`TESTSIG`)

A function generator built from parts on hand: the Pico (or RP2040-Zero) plays a
sine table out of RAM to an 8-bit R-2R resistor ladder on GP0..GP7, and an LM358P
buffers it. After `start()` the CPU does nothing per sample: one PIO state
machine clocks a byte to the ladder every cycle, and two DMA channels hand it
the table in an endless loop. The frequency is the PIO clock divided by the
table length, so changing it is one register write. It is the repo's `TESTSIG`
node (a verification source for tier 6, `lockin_amplifier`).

**Status: designed 2026-10-19. The digital half is verified on a Pico; the ladder
and buffer are not built.** On the Pico (MicroPython 1.27.0), `loopback_test.py`
plays the table and reads the eight pins back by a second PIO state machine and
DMA: every captured sample matched at 2.0, 7.8, 31.3 and 62.5 MS/s with a
256-byte table, at 31.3 and 62.5 MS/s with a 32-byte table (a DMA hand-off every
8 words, a 1.95MHz sine), and with the 4096-byte table a 1kHz sine uses; an
altered sample is caught (the negative control). `smoke_test.py` is green (ladder
model against ngspice, planner, tables, calibration, DMA set-up, bench logic).
Untested: the analog side, the calibration against a real ladder, the distortion
and the frequency ceiling `main.py` measures.

## What was found while building it

- **MicroPython reaches PIO and DMA.** This build has `rp2.StateMachine`,
  `rp2.asm_pio` and `rp2.DMA`, and the PIO+DMA path ran error-free at the rates
  above, so no C is needed for the upper frequency range. The ceiling is the
  buffer, not the code.
- **A DMA channel cannot chain to itself** (RP2040 datasheet §2.5.2). The endless
  loop is two channels chaining to each other, each reading one table period
  through a ring that wraps at the table size (so the table is aligned to its own
  size) and reloading its transfer count at every trigger.
- **Two MicroPython gaps** that the host tests couldn't see: `int` has no
  `bit_length()`, and `bytes` has no stepped slices.

## The ladder

| Part | Value | Count |
|------|-------|-------|
| `R` (between ladder nodes) | 1kΩ | 7 |
| `2R` (one per bit, and one termination) | 2kΩ | 9 |
| `RL` (output to ground; halves the swing to 0..1.65V so all 256 codes fit the LM358's 1.8V ceiling) | 1kΩ | 1 |
| LM358P buffer, 10kΩ to ground, 100nF supply | | 1 |

1kΩ and 2kΩ keep an exact 2:1 ratio and leave the 10kΩ and 5.1kΩ parts free for
the lock-in, which this source is meant to test. (The 5.1kΩ/10kΩ pair the
earlier plan named is a 2% mismatch, and with 20kΩ legs the build would use
nine 10kΩ against the ten on hand.)

- **Resistor tolerance doesn't matter much, because the Pico measures the ladder.**
  `main.py` reads all 256 codes at the buffer output with the ADC and builds the
  sine from the code whose measured level is closest to the ideal one. In
  simulation with 5% resistors and 30–60Ω pin output resistance the distortion of
  the played sine falls from −39dB (median; −32dB worst of 10 ladders) to −57dB,
  the same as an ideal 8-bit DAC (−56dB).
- **Range.** Code 255 gives 1.63V at the buffer. Codes 0 to 3 sit on the LM358's
  0.02V floor, so the default sine is codes 28..228 (1.28V p-p, 0.2V to 1.4V). A
  smaller `amp` gives a smaller sine.

## Frequency range

Frequency = system clock / (divider × table length): 125MHz / (divider × 4096) for
low frequencies, shorter tables above about 2kHz (a divider of at least 16 keeps
the steps under 0.03%).

| Limit | Value | Source |
|-------|-------|--------|
| Lowest | about 0.5Hz (divider under 65536, 4096-byte table) | arithmetic |
| Digital ceiling | 1.95MHz with a 32-byte table | `loopback_test.py` on a Pico |
| Frequency accuracy | the crystal's, about ±30ppm plus the 1/256 divider step | datasheet / arithmetic |
| LM358P slew rate | 0.3V/µs, gain-bandwidth 0.7MHz | TI LM358 datasheet, standard grade |
| Slew-limited frequency of a full 1.28V p-p sine | about 75kHz (`SR / (π × Vpp)`); 150kHz at 0.64V p-p | derived |

`main.py` measures the real analog ceiling: it steps 2, 5, 10, 20, 40 and 80kHz and
reports where the amplitude falls below 90% of its 1kHz size.

## On the user's lever list

1. PIO + DMA: used; the CPU is idle once running.
2. Chained DMA: two channels chaining to each other (see above).
3. Fixed-point phase accumulator: not needed, because the "accumulator" is the DMA
   read pointer and the PIO divider; the only CPU arithmetic is the table, built
   from a quarter wave of sines once (190ms for 4096 bytes, 680ms calibrated).
4. Hardware interpolator: not needed for the same reason.
5. RAM placement: the table is in RAM; `-O3` doesn't apply to MicroPython.
6. Second core: not needed; core 1 stays free. Frequency changes are one register
   write from core 0.

Limits kept out of the sample path: nothing prints or talks over USB while a table
is playing.

## Files

| File | Purpose |
|------|---------|
| `signal_generator_r2r.spice` | ladder, pin resistance and LM358 buffer at one code (`.param code`) |
| `main.py` | the `Dds` class (`start`, `set_freq`, `stop`), calibration, and the bring-up check |
| `loopback_test.py` | digital self-test through a second PIO state machine; needs no ladder |
| `smoke_test.py` | simulations and mocked checks |
| `breadboard.md` | wiring and expected output |

## Using it

```python
import main
dds = main.Dds()
dds.start(1000.0, amp=50)      # 1kHz, 0.64V p-p; returns the frequency actually made
dds.set_freq(1100.0)           # same table length: one register write, no glitch
dds.stop()                     # parks the ladder at code 0
```

`start(f, nearest=main.calibrator(levels))` plays the calibrated table. Changing to
a frequency that needs another table length needs `start()` again, which restarts
the output for a moment.
