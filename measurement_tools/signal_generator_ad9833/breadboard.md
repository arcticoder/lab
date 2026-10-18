# Breadboard Wiring — signal_generator_ad9833

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| AD9833 DDS module (25MHz clock, 7-pin header) | 1 | **no** — to order, see `docs/TODO-arcticoder.md` "Next order" |

Module pins, as most listings print them (read the silkscreen on the board;
labels vary): `VCC`, `DGND`, `SDATA` (or `DAT`), `SCLK` (or `CLK`), `FSYNC`
(or `FNC`/`CS`), `AGND`, `OUT`. Join `DGND` and `AGND` to the Pico's GND.

## Wiring steps

| From | To |
|------|----|
| Pico 3V3(OUT) (pin 36) | Module `VCC` |
| Pico GND (pin 38) | Module `DGND` and `AGND` |
| Pico GP17 (pin 22) | Module `FSYNC` |
| Pico GP18 (pin 24) | Module `SCLK` |
| Pico GP19 (pin 25) | Module `SDATA` |
| Module `OUT` | Pico GP26 (pin 31) |

Power the module from 3V3, not VBUS: the square-wave output swings the chip's
supply, and the ADC pin must not see more than 3.3V. If the module has an
output amplifier or an amplitude trimmer, the amplitude check can fail for
that reason; note the numbers instead of changing the limit.

## Run

```bash
mpremote run main.py
```

## Expected behavior

```
sine1k   mean 0.34xV  pp 0.6xxV  rms/pp 0.35x  1000.xHz
sine10k  mean 0.34xV  pp 0.6xxV  rms/pp 0.35x  10000.xHz
tri      mean 0.34xV  pp 0.6xxV  rms/pp 0.28x  1000.xHz
square   mean 1.6xV   pp 3.3xV   rms/pp 0.50x  1000.xHz
[PASS] output is quiet in reset: a few mV peak-to-peak
[PASS] 1kHz sine swings about 0.6V
[PASS] 1kHz sine sits above ground (unipolar output)
[PASS] 1kHz sine has a sine's shape
[PASS] module clock is 25MHz: implied MCLK 25.0xxMHz
[PASS] 10kHz is ten times 1kHz
[PASS] triangle has a triangle's shape
[PASS] square output swings the logic range
```

| Result | Meaning |
|--------|---------|
| every line fails, `pp` of a few mV | No SPI contact: `FSYNC`/`SCLK`/`SDATA` swapped or loose, or `VCC` missing |
| `output is quiet in reset` fails | `OUT` is not the chip's pin, or the chip never saw the reset word: check `FSYNC` |
| amplitude fails, shape is right | Module has an amplifier or trimmer, or a different `RSET`: report the numbers |
| `module clock` fails, `10kHz is ten times 1kHz` passes | The module's oscillator is not 25MHz; the implied MCLK is the number to record |
| square line fails, the rest pass | `OPBITEN` word not reaching the chip, or the module's `OUT` goes through a filter |
