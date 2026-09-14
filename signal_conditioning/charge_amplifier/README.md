# charge_amplifier

A 12mm piezo disc feeding one channel of a TL082 wired as a classic
inverting charge amplifier: feedback capacitor `Cf` integrates the
piezo's charge output into a voltage, and a large parallel bias resistor
`Rf_bias` stabilizes the DC operating point without materially
attenuating fast (tap-speed) signals. This is the tier5 `CHGAMP` node in
[spacetime_circuits_dependency.md](../../docs/spacetime_circuits_dependency.md)
— a direct spacetime-research sensor front-end, not general-purpose
infrastructure.

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) (the
Pico's own onboard 3.3V rail) — same rationale as
[electric_field_probe](../electric_field_probe/): guarantees the output
can never exceed the Pico ADC's 0-3.3V input range.

---

## Files

| File | Purpose |
|------|---------|
| `charge_amplifier.spice` | ngspice netlist — bias divider + TL082 inverting charge-amp feedback network |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R/C elements; the TL082 itself doesn't render |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — streams the real-hardware output as fast as the ADC allows |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Power the TL082 (V+ = pin 8, V− = pin 4) from the Pico's own 3V3(OUT)
   and GND pins.
2. Bias divider: two 1MΩ resistors from V+ to GND; the midpoint goes to
   pin 3 (non-inverting input).
3. Piezo: one lead to pin 2 (inverting input), the other to GND.
4. Feedback: a 10nF ceramic cap (`Cf`) **and** a 1MΩ resistor
   (`Rf_bias`) in parallel, from pin 2 to pin 1 (output).
5. Output is pin 1.

---

## Simulate

```bash
# from the repo root
ngspice -b signal_conditioning/charge_amplifier/charge_amplifier.spice
```

```
--- CHGAMP: bias (VCC/2) vs virtual input (should match bias) vs output (bias + Iq*Rf_bias) ---
v(2) = 1.650000e+00
v(3) = 1.649983e+00
v(4) = 1.749983e+00
```

---

## Design notes

**Why a bias divider at all.** A piezo tap is bipolar — compressing the
disc and releasing it produce opposite-sign charge pulses. A
single-supply op-amp can't represent a negative output around 0V, so
(same as `electric_field_probe`) the non-inverting input is biased to
VCC/2 with a 1MΩ/1MΩ divider, giving the output room to swing both
directions around that midpoint instead of clipping every other tap.

**Why Cf and Rf_bias are both needed, not just Cf.** A pure capacitive
feedback path (just `Cf`, no resistor) has no DC path at all — the
op-amp's own tiny input bias current would integrate onto `Cf`
indefinitely with nothing to discharge it, drifting the output to a rail
over time. `Rf_bias` gives the loop a defined DC operating point. This is
standard charge-amp practice, not an approximation specific to this
build.

**Corner frequency — what "fast enough to matter" means here.** With
`Rf_bias` = 1MΩ and `Cf` = 10nF, the time constant τ = `Rf_bias`×`Cf` =
10ms, giving a corner frequency of 1/(2π·τ) ≈ **16Hz**. Above that
frequency, the circuit behaves as a true charge integrator (output
magnitude ≈ Q/Cf, largely independent of Rf_bias); below it, Rf_bias
increasingly dominates and the circuit behaves more like a simple
resistive current-to-voltage converter. A piezo tap's mechanical
transient is much faster than 16Hz (sub-millisecond to a few
milliseconds), so real taps should register as genuine charge-integrator
events, not get bled off by the bias resistor.

**Why this op-point doesn't simulate an actual tap.** This repo's smoke
tests only run ngspice `.op` (a static operating point), not `.tran`
(a time-domain transient) — see `ne555_astable.spice` for the one
exception, which needed `.tran` because an oscillator has no meaningful
DC operating point at all. A charge amp *does* have a meaningful DC
operating point (this is exactly what the simulation above checks: the
bias network and the virtual-short/feedback-loop math), so `.op` is
sufficient to validate the topology even though it can't show the
transient integrating behavior that's the whole point of the real
circuit. `Iq = 100nA` is a steady DC stand-in standing in for "some
charge is flowing," not a calibrated tap magnitude — real validation of
the transient behavior happens on hardware (see Validation below).

**Real-hardware caveat: TL082 below its typical minimum supply.** Same
caveat as `electric_field_probe` — 3.3V single-supply is below the
TL082's typical datasheet-recommended minimum. If the buffer doesn't
respond to piezo taps on the bench, this is the first thing to suspect,
along with checking that `Cf`/`Rf_bias` are genuinely in parallel (a
series-wiring mistake here would either block DC entirely through the
cap or bleed off every transient through the resistor, depending on
which one ends up in the direct signal path).

---

## Validation

`main.py` streams the TL082 output as fast as the Pico ADC allows (no
averaging — averaging would smear out a fast transient):

```bash
mpremote run main.py
```

At rest, expect a reading near ~1.65V. Tap or flex the piezo disc — the
reading should show a brief transient deflection (compress and release
producing opposite-sign deflections), settling back toward 1.65V over
roughly the 10ms time constant above. If nothing moves regardless of
tapping, see the Design notes caveats above.
