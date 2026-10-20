# KB: RP2350 boards and this repo's RP2040-only code (2026-10-19)

Audience: future LLM sessions. The user found cheap candidate boards on
2026-10-19 (RP2350-Zero, STM32F411 Black Pill, ESP32-C3) and asked whether any
are worth adding. Facts below are from the RP2350 datasheet (read from
datasheets.raspberrypi.com, 1371 pages) unless marked.

## What changes from the RP2040

- **Peripheral base addresses move.** RP2350: `PWM_BASE` 0x400A8000, `ADC_BASE`
  0x400A0000, `DMA_BASE` 0x50000000, `PIO0_BASE` 0x50200000, `SIO_BASE`
  0xD0000000, `PADS_BANK0_BASE` 0x40038000. RP2040: PWM 0x40050000, ADC
  0x4004C000, pads 0x4001C000. **0x40050000 is `PLL_SYS` on the RP2350**, so this
  repo's raw-register scripts (`lockin_amplifier/main.py` and its diagnose
  scripts, `frequency_counter`, the ADC-DMA `capture()` in `signal_generator_r2r`,
  `trace_node.py`'s pad-pull writes) would write the system PLL's registers if run
  there. DMA, PIO and SIO addresses are the same. Before any RP2350 board runs
  one of them, add a chip check at the top of each (`'RP2350' in
  sys.implementation._machine` is the MicroPython form, unverified here) that
  aborts, or a per-chip address table.
- **Three PIO blocks, 12 state machines** (RP2040: two blocks, 8). The 4-SM-per-block
  numbering in MicroPython's `StateMachine(0..11)` is untested here.
- **Errata RP2350-E9** (affects stepping A2): a GPIO pad configured as an input with
  its voltage between VIL and VIH leaks about 120µA and sits near 2.2V; the pad
  pull-down is too weak to overcome it (a source of 8.2kΩ or less does); the
  pull-up still works. In this repo that bites anything that relies on `Pin.PULL_DOWN`
  on an input: the arm switch in `fuse_test_voltmeter`, `resistance_measurement`'s
  internal-pull-down step, and the pad-pull probe in `trace_node.py`. Check the
  stepping on arrival before trusting a pull-down.
- Datasheet claims the user's candidate listing repeats (150MHz, 520KB SRAM, FPU,
  DSP extensions) were not checked individually.

## Verdicts given to the user

- **RP2350-Zero**: worth one board if the cart has another need (capacity for a
  third parallel build; FPU and more PIO), but a port of the raw-register code
  comes first, and the E9 audit. Not needed for any current design.
- **STM32F411**: skipped. A different toolchain from the whole repo, and its
  advantage (a timer-triggered DMA to a GPIO port) is what the RP2040's PIO+DMA
  already does: `signal_generator_r2r`'s loopback ran error-free to 62.5MS/s.
- **ESP32-C3**: skipped; nothing here needs WiFi.
