# KB: RP2040 throughput and timing — standing guidance for acquisition designs

Audience: future LLM sessions. The first part is the user's brief (2026-10-17)
for any design that needs a high sustained sample rate, deterministic
timing, or heavy processing on the Pico/RP2040; the second part is what was
measured on this bench. Use it when designing or reviewing a `main.py`
that samples, counts, times or filters.

Chip facts the brief assumes: 2× Cortex-M0+ (125MHz on this board at default,
133MHz is the datasheet figure), no FPU, no SIMD, a hardware integer
divider, 8 PIO state machines in 2 blocks, 12 DMA channels, 264KB SRAM.

## Levers, in order of expected impact

1. **Take timing and data movement off the CPU.** PIO state machines for
   precisely timed I/O (serial or parallel ADC readout, counters, pulse
   timing, bit-banged protocols); DMA to land samples in RAM with no CPU per
   sample (ring buffers, ping-pong, `chain_to` for double buffering); the
   on-chip ADC with DMA where its resolution and rate are enough.
2. **No software floating point in inner loops.** Fixed point (Q15, Q31,
   s1x14 or s15x16) — the Q-format multiply-accumulate is the largest measured
   speed-up over float on this chip; block floating point for FFT stages with
   varying dynamic range; ROM float routines where float can't be avoided (and
   confirm the toolchain really uses them: library choice alone moved one float
   benchmark about 5×).
3. **Hardware divider and interpolator** for division and for table lookups or
   address generation.
4. **Build settings (C/C++/Rust only).** `-O3`/`-Ofast` where results still match
   a reference; hot code and data in RAM rather than flash (XIP stalls); branch-light
   inner loops (no branch predictor).
5. **Two cores.** Core 0 for control, communication and slow logic; core 1 for
   acquisition or DSP; hand off with the inter-core FIFOs, not by polling shared
   state.

Don't: use float in an ISR or any time-critical path without measuring it first;
print (or write USB CDC) inside an acquisition path.

## Scenario map

| Need | Approach |
|------|----------|
| High-rate multi-channel ADC or SPI acquisition | PIO + DMA ring buffer |
| Counter, frequency meter, timestamp capture | PIO counter program or hardware timers, latched through DMA |
| Logic-analyzer-style capture | PIO sampling at a fixed clock, DMA to RAM, stream out afterwards |
| Pulse width / TDC-like event timing | PIO timing, interpolator where it fits |
| Large buffers | PIO-driven SPI PSRAM with DMA |
| FFT / spectra | fixed-point or block-floating-point FFT |
| FIR/IIR filtering | fixed-point biquad cascades |
| Statistics, Monte Carlo | integer or fixed-point accumulators; benchmark against float |
| Kalman / state estimation | Q31 with careful scaling |

Libraries and references named in the brief (all unverified in this repo;
check versions against a lock file before relying on an API): Rust
`embassy-rp` (`pio`, `dma`), `rp2040-hal` 0.12.0, `fixed`, `embedded-dsp` 0.5.0,
`libm`; C Pico SDK PIO/DMA/ADC/multicore APIs, Arduino-Pico, CMSIS-DSP, the
`rp2040-psram` driver; Cornell ECE4760's fixed-point pages for Q-format timing
data; a CTU thesis on a PIO-based universal counter and logic analyzer;
`hub75-pio`. Claims from two hobby repositories (MPTC, SaraNet) are
unverified. **Any speed-up number has to come from a benchmark built and run on
the RP2040 with the production clock and optimization settings.**

## How it applies in this repo

This repo's firmware is MicroPython, so the levers map to `rp2.PIO`,
`rp2.StateMachine`, `rp2.DMA`, direct register access through `machine.mem32`,
and `_thread` for the second core. Existing uses: `frequency_counter` counts with
the PWM slice hardware, and `lockin_amplifier` generates its clocks through PWM
registers. A script that samples in a Python loop (`diagnose_gain.py`'s fold,
the pin-probe scripts) is CPU-bound and about two orders of magnitude below
what the hardware can do; when a design needs a rate or a deterministic timestamp
the loop can't give, reach for DMA or PIO before reaching for C.

## Measured here, 2026-10-17 (Pico, MicroPython v1.27.0, 125MHz)

- `rp2.DMA`, `rp2.PIO` and `rp2.asm_pio` are all present in this build. Free
  RAM at the prompt was about 240KB, but a probe that appended 8000 samples and
  8000 timestamps to two Python lists raised `MemoryError` (16KB allocation),
  so record into preallocated `array` objects (an `array('H')` of 4000 samples
  is nothing).
- **ADC with DMA** (ADC FIFO at `0x4004C00C`, DREQ 36, `START_MANY`, `AINSEL` 2
  for GP28): `DIV` INT 479 gave 100.0kSa/s, INT 0 gave 499kSa/s (96 ADC clocks
  per conversion at the 48MHz ADC clock), and INT 95 gave 250kSa/s (192 clocks per
  sample), not the 500 the divider alone suggests; the conversion needs 96
  clocks, so use 0 or 96 and up. Setup: `CS = EN | AINSEL<<12 | START_MANY`, `FCS = EN |
  DREQ_EN | THRESH<<24`, `rp2.DMA().pack_ctrl(size=1, inc_read=False,
  inc_write=True, treq_sel=36)`, count = number of samples. Clear `START_MANY`
  afterwards.
- A `for` loop calling `ADC.read_u16()` ran at 77kSa/s with nothing else in the
  loop; with a `ticks_us()` call per sample (as `diagnose_gain.py` does) it is
  30–40kSa/s.
- Not measured: PIO programs, core 1, fixed-point filters.

## Measured here, 2026-10-19: PIO + DMA from MicroPython (`signal_generator_r2r`)

The user's brief said MicroPython isn't covered and PIO/DMA is hard to reach from it. It isn't:
`rp2.StateMachine`, `@rp2.asm_pio` and `rp2.DMA` did the whole job, and the result matched a
byte-exact check at every rate tried. What was measured and learned:

- **Endless table playback = two DMA channels chaining to each other.** RP2040 datasheet
  §2.5.2: "A channel can not chain to itself." Each channel reads one table period through a
  ring (`ring_size` = log2 of the table bytes, `ring_sel=0`) so its read pointer is back at the
  start when it finishes; `TRANS_COUNT` reloads on each trigger. `chain_to=other.channel`
  works in this MicroPython (the attribute exists).
- **The ring needs the table aligned to its own size.** A `bytearray` isn't; allocate twice
  the size and use the aligned half (`uctypes.addressof` gives the address).
- **PIO output at one byte per clock**: `out(pins, 8)` with autopull at 32 bits, shift right.
  DMA fed it at 62.5MS/s (15.6M words/s) with no mismatches over 2048-sample captures, with a
  hand-off between channels every 8 words (32-byte table at 62.5MS/s, 1.95MHz sine). The rate
  is set by the state machine's clock divider register (`0x50200C8` for SM0:
  INT in 31:16, FRAC in 15:8), a single write, glitch-free for a frequency change.
- **Byte-exact self-test without an instrument**: a second state machine on the same PIO
  (`in_(pins, 8)`, autopush at 32 bits, shift right) reads the output pins back at twice
  the output rate into RAM by DMA (`RXF1` at `0x50200024`, DREQ 5); the capture must repeat
  the table exactly. A table with one altered sample gives one mismatch per period, so the
  check can fail. Output rates above half the system clock can't be oversampled.
- **After `stop()` re-init the state machine.** Reconfiguring the pins as plain outputs
  (to park them) detaches them from the PIO; `sm.init(...)` on the next start gives them back.
- **MicroPython gaps that host tests hide**: `int.bit_length()` is missing; `bytes` and
  `bytearray` don't take stepped slices (`b[0::2]`); a quarter-wave table build (4096 bytes)
  takes 190ms, and 680ms through the nearest-level search.
- Float math on the Pico: a Goertzel distortion estimate over 4000 samples and 8
  harmonics takes 1.2s. Fine for a bench check, not for a loop.

