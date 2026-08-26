# voltage_reference_lm358

A resistor-divider voltage reference (~1.65V off a 3.3V rail), buffered by
one channel of an LM358 dual op-amp so downstream circuits can draw current
from it without sagging the reference — the classic problem with a bare
resistor divider. This is the tier1 `REF` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md).

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) (the
Pico's onboard 3.3V rail) — well within its ~100mA budget, since this
circuit draws a few mA at most (LM358 quiescent current plus the divider's
own ~1.65mA).

---

## Files

| File | Purpose |
|------|---------|
| `voltage_reference_lm358.spice` | ngspice netlist — bare divider (sags under load) vs. buffered output (holds steady) |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R/V elements; the LM358 itself doesn't render (see netlist comments) |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — runs the "Validation without a multimeter" check below on real hardware |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Power the LM358 (VCC = pin 8, GND = pin 4) from
   [psu_pico_rail](../../power_supplies/psu_pico_rail/).
2. Build a 1kΩ/1kΩ divider from VCC to GND; tap the midpoint into the
   LM358's non-inverting input (pin 3).
3. Wire the LM358's output (pin 1) back to its own inverting input
   (pin 2) — this is what makes it a unity-gain buffer.
4. Take the reference output from pin 1.

---

## Simulate

```bash
# from the repo root
ngspice -b signal_conditioning/voltage_reference_lm358/voltage_reference_lm358.spice
```

```
--- A: bare divider, loaded directly (sags) ---
v(2a) = 1.100000e+00
--- B: buffered divider node (unloaded, ~1.65V) vs buffer output (loaded, should match) ---
v(2b) = 1.650000e+00
v(3b) = 1.649984e+00
```

---

## Expected behaviour

The bare divider (A), loaded with a 1kΩ resistor equal to its own bottom
leg, sags from 1.65V to **1.10V** — a 33% error, because the load resistor
forms a second divider leg the design didn't account for. The buffered
output (B) holds at **1.65V** under the identical 1kΩ load, because the
LM358's output impedance (a few ohms, not modeled in detail here) is small
enough relative to the load that it barely sags at all. This is the whole
point of the buffer: the reference stays accurate regardless of what's
downstream, as long as the load stays within the LM358's output current
capability (tens of mA).

**Headroom caveat**: standard LM358 parts can't swing their output
closer than ~1.5V below VCC (single-supply). At VCC=3.3V that's a ceiling
around 1.8V — the 1.65V reference here has margin, but don't push the
divider ratio much higher without checking the specific part's datasheet.

---

## Validation without a multimeter

Probe the output (pin 1) with a Pico ADC pin, with and without `RloadB`
(a 1kΩ resistor) connected — the reading should barely move. If it sags
noticeably, either the feedback wire (pin 1 → pin 2) is missing, or the
LM358 isn't getting power on pin 8/pin 4.

`main.py` runs this check on real hardware: wire GP26 to LM358 pin 1 and
a Pico GND pin to the LM358's own GND (pin 4), then run it with the Pico
plugged in over USB:

```bash
mpremote run main.py
```

It takes an averaged reading, then prompts you to disconnect/reconnect
`RloadB` between readings — waiting on your Enter keypress each time
instead of streaming continuously, since there's nothing useful to watch
scroll by while you're moving a resistor lead on the breadboard. It
finishes by printing `PASS`/`FAIL` against the same ±2% tolerance
`smoke_test.py` uses for the simulated buffered-vs-unloaded comparison.
