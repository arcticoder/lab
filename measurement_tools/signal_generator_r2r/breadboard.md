# Breadboard Wiring — signal_generator_r2r

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico or RP2040-Zero (USB-connected) | 1 | yes (the Zero leaves the Pico on the lock-in) |
| 2kΩ resistor (`2R`) | 9 | yes (10) |
| 1kΩ resistor (`R` ×7 and `RL`) | 8 | yes (10; the lock-in's `Rbias` takes one) |
| 10kΩ resistor (buffer load) | 1 | yes (10) |
| LM358P | 1 | yes (10) |
| 100nF ceramic capacitor | 1 | yes (10) |

Check each resistor's colour bands as it goes in: 1kΩ is `brown black black brown
brown`, 2kΩ is `red black black brown brown`. `measurement_tools/resistance_measurement`
reads one if a band is unclear. The ladder tolerates 5% parts (the calibration
absorbs it) but not a 1kΩ where a 2kΩ belongs.

LM358P, notch up, pin 1 top-left: 1 `OUT`, 2 `IN−`, 3 `IN+`, 4 `GND`, 8 `VCC`.

## Wiring steps

Name the rows `N0` to `N7` (the ladder nodes), `OUT`.

| From | To |
|------|----|
| Pico GP0 (pin 1) | 2kΩ to `N0` |
| Pico GP1 (pin 2) | 2kΩ to `N1` |
| Pico GP2 (pin 4) | 2kΩ to `N2` |
| Pico GP3 (pin 5) | 2kΩ to `N3` |
| Pico GP4 (pin 6) | 2kΩ to `N4` |
| Pico GP5 (pin 7) | 2kΩ to `N5` |
| Pico GP6 (pin 9) | 2kΩ to `N6` |
| Pico GP7 (pin 10) | 2kΩ to `N7` |
| `N0` | 2kΩ to GND (the termination) |
| `N0` to `N1`, `N1` to `N2`, ... `N6` to `N7` | seven 1kΩ in series along the nodes |
| `N7` | 1kΩ (`RL`) to GND |
| `N7` | `U1` pin 3 |
| `U1` pin 2 | `U1` pin 1 (voltage follower); pin 1 is `OUT` |
| `OUT` | 10kΩ to GND |
| `U1` pin 8 | Pico 3V3(OUT) (pin 36) |
| `U1` pin 4 | GND |
| 100nF | `U1` pin 8 to pin 4, next to the chip |
| `OUT` | Pico GP26 (pin 31), for the bring-up check |

On the RP2040-Zero use the silkscreen names `GP0`..`GP7`, `GP26`, `3V3` and `GND`;
nothing else changes. With both boards attached, `mpremote devs` lists them, and
`mpremote connect id:<serial> ...` picks one.

## Run

First the digital check, which needs none of the above:

```bash
mpremote mount . run loopback_test.py
```

Seven `[PASS]` lines (2.0MS/s up to 62.5MS/s). Then, with the ladder wired:

```bash
mpremote mount . run main.py
```

It takes about 20 seconds.

## Expected behavior

```
levels: code 0 0.020V, 128 0.81xV, 255 1.63xV
uncal  mean 0.8xxV  pp 1.2xxV  1000.0xHz  distortion -3x dB
cal    mean 0.8xxV  pp 1.2xxV  1000.0xHz  distortion -5x dB
  2000Hz: pp 1.2xxV (100% of 1kHz), ...
  ...
[PASS] ladder spans the expected swing: about 1.63V
[PASS] each bit weighs 2^k steps (R-2R ratios hold)
[PASS] 1kHz sine comes out at the planned frequency
[PASS] amplitude matches the measured ladder levels
[PASS] uncalibrated sine distortion
[PASS] calibrated sine distortion
[PASS] calibration does not make it worse
[PASS] amplitude holds to 10kHz
```

The pass limits are provisional (set from the simulation and the data sheets); tighten
them after the first run.

| Symptom | Likely cause |
|---------|--------------|
| span under 1.3V | a bit's leg missing or open, or `RL` missing (then the swing is 3.3V and the buffer clips at 1.8V) |
| one bit's weight off by half or double | a 1kΩ and 2kΩ swapped on that bit |
| every level near 0.02V | `U1` unpowered, or `GP26` reading something other than `OUT` |
| distortion good calibrated, poor uncalibrated | normal for loose resistors; use the calibrated table |
| amplitude falls early in the sweep | the LM358P's slew limit; use a smaller `amp` |

## Driving the lock-in

Through 200kΩ (two 100kΩ) into the `SIG` row, with `dds.start(1000.0, amp=50)`:
0.64V p-p through 200kΩ into the 1kΩ `Rbias` is about 2.9mV at `SIG`, the design's
test amplitude. Share ground with the lock-in's board.
