# electric_field_probe

A bare-electrode electrostatic-field sensor: a small conductor biased to
mid-rail through a high-impedance divider, buffered by a JFET-input
TL082 so the buffer itself doesn't load down (and thus erase) whatever
tiny signal the electrode couples in. This is the tier5 `EPFIELD` node in
[spacetime_circuits_dependency.md](../../docs/spacetime_circuits_dependency.md)
— one of the direct sensor front-ends the spacetime-research tier graph
calls for, not general-purpose infrastructure.

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) (the
Pico's own onboard 3.3V rail) rather than a battery PSU tier — see
§ Design notes below for why.

---

## Files

| File | Purpose |
|------|---------|
| `electric_field_probe.spice` | ngspice netlist — bias divider + TL082 follower |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R elements; the TL082 itself doesn't render, same as other op-amp circuits here |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — streams the real-hardware output continuously |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Power the TL082 (V+ = pin 8, V− = pin 4) from the Pico's own 3V3(OUT)
   and GND pins.
2. Bias divider: two 1MΩ resistors in series from V+ to GND; the
   midpoint (BIAS) goes to pin 3 (non-inverting input).
3. Electrode (any small bare conductor) also lands on the BIAS node.
4. Feedback: pin 2 (inverting input) tied directly to pin 1 (output) —
   unity-gain follower.
5. Output is pin 1.

---

## Simulate

```bash
# from the repo root
ngspice -b signal_conditioning/electric_field_probe/electric_field_probe.spice
```

```
--- EPFIELD: bias midpoint (should be VCC/2) vs buffered output (should track it) ---
v(2) = 1.650000e+00
v(3) = 1.649984e+00
```

---

## Design notes

**Why psu_pico_rail, not a battery PSU tier.** Every other op-amp
sensor front-end in this repo (`voltage_reference_lm358`,
`transimpedance_amplifier`) runs off a battery PSU tier and documents a
headroom caveat against the Pico ADC's 0-3.3V input ceiling. This circuit
sidesteps that risk entirely instead of documenting around it: powering
the TL082 directly from the same 3.3V rail the Pico's own ADC references
means the op-amp output is *structurally* incapable of exceeding 3.3V,
regardless of divider math or op-amp behavior. See
`oscillators/ne555_astable/README.md`'s § Validation for what happens on
real hardware when an op-amp/divider output referenced to a higher rail
gets fed into GP26 with the wrong resistor in place (pinned at exactly
3.300V, the ADC's own saturation point) — this design avoids that failure
mode by construction rather than by careful resistor selection.

**Real-hardware caveat: TL082 below its typical minimum supply.** 3.3V
single-supply is below what the TL082's datasheet typically recommends
for full-spec operation (JFET dual op-amps in this class are usually
specified from a much wider split-supply range). Many parts in this
class still function as a low-gain buffer well below their spec'd
minimum, just with reduced bandwidth/slew and more offset — but this
hasn't been confirmed for the specific TL082 units on hand. **If the
real buffer doesn't track the bias node on the bench** (output stuck at
0V, at VCC, or not responding to the electrode at all), this supply
choice is the first thing to suspect — the fix is trying `psu_low_v2`
(3V, same order of magnitude, unlikely to help) or `psu_4xaa` (6V, real
headroom) with an added attenuator/divider ahead of the Pico ADC, not a
new circuit topology.

**Why 1MΩ, not a "real" electrometer-grade bias resistor.** A dedicated
electrostatic-field electrometer front end conventionally uses GΩ-range
bias resistors to keep the input path as high-impedance as possible
(more sensitivity, longer time constant). 1MΩ is simply the largest
value on hand (`docs/inventory.md`'s Resistors table tops out there) —
this bounds real sensitivity accordingly. If a real build turns out too
insensitive to be useful, ordering a GΩ-range resistor (not currently
on hand or on order) is the concrete next step, not a topology change.

**No fixed sensitivity number is claimed.** Unlike
`transimpedance_amplifier`'s illustrative photocurrent, this circuit's
"input signal" isn't representable as a fixed SPICE current — a floating
electrode's real coupling depends entirely on its geometry and proximity
to whatever it's sensing. The simulation above only demonstrates the
bias-divider math and confirms the follower's feedback loop is closed;
real sensitivity is a qualitative, on-the-bench observation (see
Validation below), not a simulated or calculated figure.

---

## Validation

`main.py` streams the TL082 output continuously over USB serial:

```bash
mpremote run main.py
```

At rest, expect a reading near ~1.65V (VCC/2). Bring a charged object
(a balloon or comb rubbed on hair/fabric) near the electrode — the
reading should visibly deflect away from 1.65V — then move it away and
watch the reading drift back. If the reading never moves:

- Check TL082 power first (pin 8 should read ~3.3V against pin 4/GND).
- Check the pin 2-to-pin 1 feedback jumper is actually in place (without
  it, the "buffer" is running open-loop and will pin at a rail).
- Check the electrode is making real contact with the BIAS row, not
  just resting near it.
- If all of the above check out and it still doesn't respond, see the
  real-hardware supply-voltage caveat above.
