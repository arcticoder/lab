# fuse_test_voltmeter

A Raspberry Pi Pico, probing across a polyfuse under test and streaming
voltage readings back over USB to this PC. Purpose-built to confirm a
polyfuse is genuinely good — and that it trips and resets the way it's
supposed to — *before* it's wired in series with an LED, so a defective or
stuck fuse doesn't take the LED out with it.

Not a powered circuit of its own: the Pico gets its power from the PC's USB
port, independent of whichever PSU tier is under test
([psu_ultralow_v1](../power_supplies/psu_ultralow_v1/) or
[psu_low_v2](../power_supplies/psu_low_v2/)). See
[docs/history.md](../docs/history.md) (2026-08-15 10:32 onward) for the
design conversation — this formalizes the ad hoc Pico-as-voltmeter probing
used throughout that session into its own reusable circuit.

For a more capable Pico ADC readout (filtering, noise characterization,
calibration curves), see
[pico/gpio_analog_sensing](../../pico/gpio_analog_sensing/) in the sibling
`pico/` repo (see `lab.code-workspace`, which opens both) — that's
general-purpose analog sensing
infrastructure, not lab-specific, so it lives over there rather than being
duplicated here. `main.py` in this folder borrows its
`raw_to_voltage`/constants layout but stays deliberately minimal: one ADC
channel, one job.

---

## Files

| File | Purpose |
|------|---------|
| `fuse_test_voltmeter.spice` | ngspice netlist — probe-point voltage, fuse cold vs. tripped, for both v1 and v2 |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step probing/wiring guide |
| `main.py` | MicroPython — reads GP26, prints voltage over USB serial, flags trip/reset |

---

## Build

Follow **[breadboard.md](breadboard.md)**. Short version:

1. Plug the Pico into the PC over USB (power + serial, nothing else needed).
2. Clip GP26 to the load resistor's fuse-side leg on the psu_ultralow_v1 or
   psu_low_v2 breadboard; clip a Pico GND pin to the resistor's ground-side
   leg.
3. Run `main.py` (`mpremote run main.py`) and watch the serial output.

---

## Simulate

```bash
# from the repo root
ngspice -b fuse_test_voltmeter/fuse_test_voltmeter.spice
```

Prints the probe-point voltage for both tiers, cold-fuse vs.
tripped-approximation:

```
--- v1 (1.5V, 50 mA fuse): cold vs. tripped ADC-probe voltage ---
v(11) = 1.428571e+00
v(12) = 1.363636e-01
--- v2 (3.0V, 500 mA fuse): cold vs. tripped ADC-probe voltage ---
v(21) = 2.857143e+00
v(22) = 2.727273e-01
```

---

## Expected behaviour

**v1** (psu_ultralow_v1, 10 Ω test load, 3x the 50 mA trip threshold): probe
reads ~1.43V cold, collapses to ~0.14V once the fuse trips.

**v2** (psu_low_v2, 10 Ω test load, right at the 500 mA trip threshold):
probe reads ~2.86V cold, collapses to ~0.27V once the fuse trips.

`main.py`'s `LOW_VOLTAGE = 0.5` threshold sits between the cold and
tripped readings for both tiers, so the same firmware flags a trip on
either PSU without changes.

---

## Validation

This *is* the validation instrument — there's no multimeter to check it
against. Confidence comes from:

1. The SPICE numbers above matching what the Pico reports cold (within
   ADC noise, a few mV).
2. Watching the printed voltage collapse and the onboard LED light up when
   you deliberately short the load resistor to force an over-threshold
   trip (see `breadboard.md`).
3. Watching it recover — reading and LED both reset — after ~2 minutes of
   cool-down. A fuse that doesn't reset is bad; discard it rather than
   wiring it in front of an LED.
