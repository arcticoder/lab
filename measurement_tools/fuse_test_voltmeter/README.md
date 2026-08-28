# fuse_test_voltmeter

A Raspberry Pi Pico, probing across a polyfuse under test and streaming
voltage readings back over USB to this PC. Purpose-built to confirm a
polyfuse is genuinely good — and that it trips and resets the way it's
supposed to — *before* it's wired in series with an LED, so a defective or
stuck fuse doesn't take the LED out with it.

**Test vs. demo — these are different things.** *Testing* a polyfuse means
bench-checking the raw component on a minimal jig (battery, fuse, load
resistor — nothing else) to sort good units from faulty ones, before any
of them go near a real circuit. *Demonstrating* a polyfuse means showing a
fuse that has already passed that test working correctly once it's
installed in an actual PSU build
([psu_ultralow_v1](../../power_supplies/psu_ultralow_v1/) or
[psu_low_v2](../../power_supplies/psu_low_v2/)). The demo proves the PSU's
wiring around the fuse is correct; it does not re-establish that the fuse
itself is good — that's what the test is for. See
[breadboard.md](breadboard.md) for the full self-check → test → demo
sequence.

Not a powered circuit of its own: the Pico gets its power from the PC's USB
port, independent of whatever it's probing. This formalizes the ad hoc
Pico-as-voltmeter probing worked out early on into its own reusable
circuit.

For a more capable Pico ADC readout (filtering, noise characterization,
calibration curves), see
[pico/measurement_tools/gpio_analog_sensing](../../../pico/measurement_tools/gpio_analog_sensing/) in the
sibling `pico/` repo (see `lab.code-workspace`, which opens both) — that's
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
| `quickstart.md` | Just one fuse, one battery, in front of you right now — the direct build, no tiers/batch framing |
| `breadboard.md` | Full self-check → test → demo procedure (500 mA tier, batches of fuses, PSU demo) |
| `main.py` | MicroPython — reads GP26, prints voltage over USB serial, flags trip/reset |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Testing a single fuse right now? Follow
**[quickstart.md](quickstart.md)** — it skips the batch/tier framing
below. Otherwise, follow **[breadboard.md](breadboard.md)**. Short
version:

1. Plug the Pico into the PC over USB (power + serial, nothing else needed).
2. **Self-check first**: wire GP26/GND across a load resistor with a plain
   jumper wire standing in for a fuse, wire the GP15 arm switch (see
   `breadboard.md`), and confirm the reading and trip/reset logic behave
   sanely before trusting the instrument on any real fuse.
3. **Then test**: swap in one polyfuse at a time from the batch on the
   same minimal jig (no PSU needed yet) to sort good units from faulty
   ones.
4. **Then demo**: once a specific fuse has passed step 3, build
   psu_ultralow_v1 or psu_low_v2 with it installed, and re-probe the same
   way to confirm the PSU's wiring around the fuse.

Run `main.py` (`mpremote run main.py`) and watch the serial output at each
stage.

---

## Simulate

```bash
# from the repo root
ngspice -b measurement_tools/fuse_test_voltmeter/fuse_test_voltmeter.spice
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

**v1** (RXEF005, 1.5V, 10 Ω test load, 3x the 50 mA trip threshold): probe
reads ~1.43V cold, collapses to ~0.14V once the fuse trips.

**v2** (RXEF050, 3.0V, 10 Ω test load, right at the 500 mA trip threshold):
probe reads ~2.86V cold, collapses to ~0.27V once the fuse trips.

`main.py`'s `LOW_VOLTAGE = 0.5` threshold sits between the cold and
tripped readings for both tiers, so the same firmware flags a trip
whether it's probing the bench jig or a PSU during a demo, without
changes.

An SPDT slide switch on GP15 (wiring in `breadboard.md`/`quickstart.md`)
lets the operator flag ARMED/DISARMED before trip/reset detection is
trusted — see `main.py`'s docstring. This exists because the battery
itself has to be physically connected/disconnected by hand mid-test, and
without an explicit signal the expected zero-volt reading during that
action reads identically to a real trip.

---

## Validation

There's no multimeter in the loop, so validation happens in three stages
— each one has to pass before the next is meaningful.

### 1. Confirming the voltmeter itself

Before trusting a reading on any real fuse, wire the probe across a load
resistor with a plain jumper wire in place of a fuse (see
[breadboard.md](breadboard.md#1-self-check-the-voltmeter-no-fuse-yet)) and
confirm:

- The cold reading matches the SPICE numbers above (a wire adds ~0 Ω, so
  it should track the cold-state prediction within ADC noise).
- Deliberately shorting the load resistor collapses the reading and fires
  the trip indication (`*** FUSE TRIPPED ***`, onboard LED on).
- Removing the short recovers the reading and clears the indication
  (`*** fuse reset ***`, LED off).

If this doesn't hold, the fault is in the Pico wiring or firmware, not a
fuse — fix it before testing anything.

### 2. Testing raw polyfuses (sorting good from faulty)

With the self-check passing, swap in one polyfuse at a time from the batch
of 20 RXEF005 / 20 RXEF050 on the same minimal jig — no PSU involved.
Confidence per unit comes from:

1. The SPICE numbers above matching what the Pico reports cold (within
   ADC noise, a few mV).
2. Watching the printed voltage collapse and the onboard LED light up when
   you deliberately short the load resistor to force an over-threshold
   trip.
3. Watching it recover — reading and LED both reset — after ~2 minutes of
   cool-down.

A fuse that doesn't trip, doesn't reset, or reads far off the SPICE
prediction fails — discard it rather than wiring it in front of an LED.
This step is what produces the pool of confirmed-good fuses that PSU
builds draw from.

### 3. Demonstrating a confirmed-good fuse in the PSU

Only after a fuse has passed step 2: build psu_ultralow_v1 or psu_low_v2
with that specific unit installed, and re-run the same short/reset check,
probing the PSU's own load-resistor node instead of the bench jig's. This
confirms the PSU's wiring around the fuse is correct — it's a
demonstration of the already-proven-good fuse working in situ, not a
second test of the fuse component itself.
