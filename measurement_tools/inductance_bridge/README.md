# inductance_bridge

A Pico-driven resonance sweep for measuring an unknown inductor: a PWM
square wave drives a parallel tank made of the inductor (`Lx`) and a
known 10nF capacitor (`Cref`) through a 1kΩ resistor, a diode peak
detector turns the tank's amplitude into a DC level, and the Pico sweeps
the drive frequency to find where that level peaks. At resonance
`Lx = 1 / ((2π·f0)² · Cref)`. This is the tier3 `INDBRIDGE` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md).

Like [capacitance_bridge](../capacitance_bridge/) and
[resistance_measurement](../resistance_measurement/), this swaps a
known-reference-vs-unknown comparison for a literal 4-arm AC bridge and
its phase-sensitive null detector. Here the reference is a known
capacitor and the comparison is at resonance instead of at balance.

Powered from the Pico's own GPIO — `psu_pico_rail` is enough, and the
PWM pin is the AC excitation source, so nothing needs buying.

---

## Files

| File | Purpose |
|------|---------|
| `inductance_bridge.spice` | ngspice netlist — resonance sweep of all 12 assortment values (`.ac`) plus a time-domain run of the real square drive and detector at the 100µH design point |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — streams real-hardware inductance readings, one sweep per line |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Pico GP14 → `Rs` (1kΩ) → tank row.
2. `Cref` (10nF) and `Lx` from the tank row to GND.
3. 1N5817 anode on the tank row, cathode (banded end) to a detector row;
   `Cd` (10nF) and `Rd` (100kΩ) from the detector row to GND.
4. Pico GP26 (ADC0) → detector row.

---

## Simulate

```bash
# from the repo root
ngspice -b measurement_tools/inductance_bridge/inductance_bridge.spice
```

The output is `ACPEAK` lines (inductance, assumed winding resistance,
peak frequency, peak tank amplitude) for each assortment value, then
`TDPOINT` lines (drive frequency, detector DC level, tank amplitude) for
the time-domain run. At the 100µH design point the resonance peak is at
159.3kHz and the detector reads 1.49V there.

---

## Range

Why resonance and not a time constant like `capacitance_bridge`: an RL
circuit's time constant `L/R` for this assortment (1µH–1mH) is
nanoseconds to microseconds at any resistance a GPIO can drive, and the
Pico's polled ADC samples every ~10µs. The resonant frequency does not
need a fast ADC, because the PWM sets the frequency and the detector
holds the amplitude as a DC level.

With `Cref` = 10nF every value in the assortment resonates inside
`main.py`'s 40kHz–2MHz sweep:

| `Lx` | f0 |
|------|----|
| 1µH | 1.59MHz |
| 10µH | 503kHz |
| 22µH | 339kHz |
| 47µH | 232kHz |
| 100µH | 159kHz |
| 220µH | 108kHz |
| 470µH | 73kHz |
| 1mH | 50kHz |

(All 12 are in the smoke test.) The 1µH end is the weak one: a small
inductor has low impedance at resonance, so the tank amplitude is
smallest there (0.35V simulated even at five times the assumed winding
resistance) and the PWM step near 1.6MHz is ~1.3%, so its f0 is only
resolved to a couple of percent.

## Accuracy

Two things set it, neither of them the code:

- **`Cref`'s tolerance.** f0 scales as 1/√C, so a ±10% capacitor is
  about ±10% on `Lx`. That is enough to tell apart neighbours in the
  assortment that differ by ≥1.4× (22 vs 33µH, 150 vs 220µH, 330 vs
  470µH) but not 470µH from 560µH (1.19×) — treat those two as one
  group.
- **The inductor's own tolerance**, which the listing doesn't state.

So this confirms a color-band reading; it doesn't calibrate it.

---

## Expected behaviour

The tank is parallel, not series, on purpose. A series tank's Q
multiplication would put several volts on the ADC-facing node; the
parallel tank cannot exceed the drive, and the simulated detector never
passes 1.5V.

The square wave's odd harmonics excite the tank too: driving at f0/3
gives a secondary peak of about a third the size (34% simulated). The
real resonance is always the tallest peak, so `main.py` takes the
sweep's global maximum, and the smoke test asserts the ratio stays under
half.

---

## Validation

```bash
mpremote run main.py
```

Start with no inductor in the tank row: it must print the "level highest
at the sweep edge" message (see `breadboard.md` for what each message
means). Then seat inductors one at a time and compare the printed value
with the color bands, which `docs/parts_reference.md` flags as
unverified for this batch.

**Not yet bench-tested.** `main.py`'s sweep and peak-finding logic was
run against a host-side model of the tank with a mocked `machine`
module (all 12 assortment values recovered to within ~1%, and the
open/shorted-tank messages appear), but that is not the Pico. Two
things only hardware will settle: whether this MicroPython build's
`PWM.freq()` reads back the quantized frequency the divider actually
runs at (`main.py` relies on it; if it returns the requested value the
error grows to the PWM step, ≤1.3% at 2MHz), and the real inductors'
winding resistance and stray capacitance, which the netlist estimates.
