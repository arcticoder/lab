# signal_generator_ad9833 — programmable sine/triangle/square source (`TESTSIG`)

A cheap AD9833 DDS module driven by the Pico over SPI: a sine, triangle or
square wave from 0.1Hz to 12.5MHz in 0.1Hz steps (25MHz module clock), with
the frequency set in software. It is the repo's `TESTSIG` node
(`general_purpose_circuit_dependency.md`: "verification" input to tier 6), and
the first source on this bench that makes a clean sinusoid at a chosen
frequency. The Pico's own PWM gives only squares at integer divisions of
125MHz.

**Status: designed 2026-10-17 from the AD9833 data sheet (Rev. E, 2003–2019);
`smoke_test.py` green; not built — the module is not yet ordered.** The
driver's DMA capture and waveform analysis were run on a Pico against signals
that were not the module's (capture on the lock-in rig's nodes, analysis on a
synthetic sine: 1000.00Hz, 0.596V p-p in 241ms); the SPI side was run only
against a model of the chip's registers.

## What it is for

| Use | How |
|-----|-----|
| Verify `lockin_amplifier` with a sinusoid, not just the Pico's own square waves | OUT through 200kΩ (two 100kΩ) into the `SIG` row: about 3mV at `SIG`, the design's test amplitude. Sweeping 990–1010Hz and watching X shows the lock-in's selectivity (its averagers pass a difference frequency below roughly 0.75Hz) |
| Find the 12mm piezo discs' resonance (16.5kHz ±0.7kHz per the listing) | Sweep 10–25kHz into a disc and read `CHGAMP`'s output |
| Frequency-response sweeps of any filter or amplifier built here (`TIA`, `hall_amplifier`, the future `AAF`) | Step the frequency, read the output with the Pico's ADC or the `SCOPELA` board |

## Files

| File | Purpose |
|------|---------|
| `main.py` | Driver (`Ad9833` class, `program_words`, DMA `capture`, `analyze`) and a bring-up check with `[PASS]`/`[FAIL]` lines (about 3s) |
| `smoke_test.py` | Words and register behaviour against the data sheet's formulas, a model of the chip, analysis of synthetic waveforms, and the pass/fail logic |
| `breadboard.md` | Wiring and expected output |

## Design notes

- **SPI.** 16-bit words, MSB first, FSYNC low around each; SCLK idles high and
  data is taken on the falling edge, so `SPI(0, polarity=1, phase=0)`. The chip
  allows 40MHz SCLK; the driver uses 1MHz.
- **Frequency.** `f = word × MCLK / 2²⁸`, loaded as two 14-bit halves with
  B28=1 (low half first); 1kHz at 25MHz is word 10737, a 0.004% error. Above
  MCLK/2 the output aliases, so the driver refuses it.
- **Output.** About 0.6V p-p (data sheet: 38mV to 650mV) on a 0.34V pedestal,
  through an on-chip 200Ω: unipolar, so AC-couple it into anything that needs
  a centred signal, and use a high-impedance load. The 10-bit DAC limits
  distortion to −56 to −66dBc and spurs to about −60dBc: fine for response
  sweeps, not for a distortion measurement. Square mode outputs the DAC's
  most significant bit, which swings the chip's own supply (3.3V here).
- **The one unknown is the module's clock.** Modules are sold with a 25MHz
  oscillator; `main.py` measures the real frequency by DMA-sampling OUT on the
  Pico's ADC and reports the implied MCLK. A different clock changes every
  frequency by the same ratio and is not a fault, but the number must be
  recorded here.
- **Reading OUT with the Pico's ADC** needs a low source impedance: the chip's
  200Ω is fine. The same capture on the lock-in's `SIG` row (about 5kΩ with the
  wrong `Rbias`) showed 170mV of sampling noise, so don't use this capture on a
  high-impedance node.
