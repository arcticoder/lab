# phase_detector

One XOR gate of an SN74HC86N compares two square waves and an RC lowpass
filter turns the result into a duty-cycle-proportional DC voltage — the
standard XOR phase-detector primitive. This is the tier4 `PHASED` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md),
which feeds tier6 `LOCKIN` (still undesigned).

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/).

---

## Files

| File | Purpose |
|------|---------|
| `phase_detector.spice` | ngspice netlist — XOR truth table + RC lowpass, two static logic-level cases |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R/C elements; the XOR gate itself doesn't render |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — drives the PWM reference input, streams the filtered output |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring — it
requires `oscillators/ne555_astable` already built. Short version:

1. Power the SN74HC86N (VCC = pin 14, GND = pin 7) from the Pico's 3V3(OUT)
   and GND.
2. Input 1A (pin 1) ← tap from `ne555_astable`'s existing output divider.
3. Input 1B (pin 2) ← a Pico GPIO configured as PWM, ~1.5kHz.
4. Output 1Y (pin 3) → 10kΩ/100nF RC lowpass → a Pico ADC pin.

---

## Design notes

**The open design question this resolves.** `docs/TODO-agent.md` flagged
that a classic XOR phase detector needs two same-frequency square waves
at a variable phase offset, and this bench only had one square-wave
source (`ne555_astable`). Rather than building a second NE555 stage
(consuming a second unit from the batch for no functional gain — the
whole batch is already validated as interchangeable), the second input
is a **Pico GPIO PWM output**: independently generated, tuned near the
NE555's own frequency, but deliberately **not** phase-locked to it.

**Why not phase-locking them is fine, for what this node needs to
prove.** Two free-running oscillators at nominally the same frequency
will always drift in relative phase over time (their frequencies are
never exactly equal) — the XOR output's duty cycle will continuously
sweep through the full 0-100% range as that phase relationship drifts,
rather than settling at one value representing a fixed phase offset.
That's a real limitation for a *phase meter* (something that reports a
stable phase-difference number), but it's a perfectly good way to
validate the XOR primitive itself: watching the filtered output sweep
between ~0V and ~3.3V on real hardware is direct, visible confirmation
that the gate is genuinely responding to the *relative* phase of two
independent signals, not just to one input in isolation. Building an
actual phase-locked or frequency-locked reference (so the two inputs
hold a fixed, settable phase offset) is real future work for whatever
eventually implements tier6 `LOCKIN` — this node's job is the XOR
primitive, not the reference-clock design.

**Why a static two-case `.op` simulation, not a `.tran` sweep.** This
repo's smoke-test convention runs ngspice `.op` (see repo `README.md`);
`ne555_astable.spice` is the one exception, needed because an oscillator
has no meaningful DC operating point. A digital gate *does* have a
meaningful operating point at any fixed pair of input levels, so two
static cases — both inputs HIGH (in-phase) and one HIGH/one LOW
(out-of-phase) — are enough to confirm the XOR truth table and the
lowpass's DC pass-through behavior. The real continuously-sweeping
behavior described above is confirmed on hardware, not in this
simulation — see Validation below.

**Digital gate modeled behaviorally, not with a vendor macromodel.**
`Bxor` in the netlist is an ideal ngspice B-source implementing the XOR
truth table via `!=` on two thresholded comparisons — this repo's first
digital-logic element, following the same "ideal + documented caveats"
approach as the op-amp E-elements and the NE555 astable macromodel
elsewhere in this repo. It doesn't model propagation delay, input
capacitance, or the real 74HC86's actual switching thresholds.

**Voltage-margin caveat on input 1A.** See `breadboard.md`'s own
caveat — the NE555 tap's "high" level (~2.2-2.9V, varies per unit in the
validated batch) is close enough to a 74HC-series gate's ~2.31V typical
VIH threshold (at 3.3V VCC) that it's worth confirming the gate actually
switches cleanly on whichever specific NE555 unit is wired in, rather
than assuming it will.

---

## Simulate

```bash
# from the repo root
ngspice -b signal_conditioning/phase_detector/phase_detector.spice
```

```
--- Case 1: in-phase (A=HIGH, B=HIGH) ---
v_a_inphase = 3.300000e+00
v_b_inphase = 3.300000e+00
v_xor_inphase = 0.000000e+00
v_out_inphase = 0.000000e+00
--- Case 2: out-of-phase (A=HIGH, B=LOW) ---
v_a_outphase = 3.300000e+00
v_b_outphase = 0.000000e+00
v_xor_outphase = 3.300000e+00
v_out_outphase = 3.300000e+00
```

---

## Validation

`main.py` drives the PWM reference and streams the filtered output
continuously:

```bash
mpremote run main.py
```

Expect the reading to sweep slowly between roughly 0V and 3.3V as the
NE555 and the Pico's PWM drift in and out of phase — not a single fixed
value. If the reading sits pinned at one extreme and never moves,
either the two frequencies are drifting extremely slowly (try nudging
the NE555's trimpot slightly to force a bigger frequency mismatch and a
faster, more visible sweep) or the gate isn't switching — check the
voltage-margin caveat above first, then gate power (pins 14/7) and that
both inputs are actually landing on pins 1 and 2, not swapped or
floating.
