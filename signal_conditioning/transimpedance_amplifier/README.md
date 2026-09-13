# transimpedance_amplifier

A PT334-6C silicon PIN photodiode in zero-bias (photovoltaic) mode,
converted to a voltage by one channel of an LM358 wired as a
transimpedance amplifier (current-to-voltage converter). This is the
tier2 `TIA` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md).

Powered from [psu_low_v2](../../power_supplies/psu_low_v2/) — per the
`psu_low --> tier2` edge in the dependency graph, **not**
`psu_3xaa` (a separate, unrelated 3×AA holder chain; see
[docs/kb/todo_list_conventions.md](../../docs/kb/todo_list_conventions.md)
for the correction that established this).

---

## Files

| File | Purpose |
|------|---------|
| `transimpedance_amplifier.spice` | ngspice netlist — photodiode modeled as an ideal current source into the LM358's inverting input |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R/I elements; the LM358 itself doesn't render, same as `voltage_reference_lm358` |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — streams the real-hardware output continuously |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Power the LM358 (VCC = pin 8, GND = pin 4) from
   [psu_low_v2](../../power_supplies/psu_low_v2/).
2. Ground the non-inverting input (pin 3).
3. Photodiode anode → GND; photodiode cathode → LM358 pin 2 (inverting
   input).
4. Feedback resistor `Rf` (100kΩ) from pin 2 to pin 1 (output).
5. Take the output from pin 1.

---

## Simulate

```bash
# from the repo root
ngspice -b signal_conditioning/transimpedance_amplifier/transimpedance_amplifier.spice
```

```
--- TIA: virtual-ground node (should be ~0V) vs output (Iph * Rf) ---
v(2) = -9.99990e-06
v(3) = 9.999900e-01
```

---

## Expected behaviour

The inverting input (node 2) stays pinned at virtual ground (~0V)
regardless of the photocurrent — that's what the feedback loop is for.
The output (node 1 / node 3 in the sim) is `Iph × Rf`: at the simulated
10µA illustrative photocurrent and the 100kΩ feedback resistor on hand,
that's **1.0V**. `Iph = 10µA` is **not** a calibrated responsivity/lux
measurement for this specific PT334-6C — no such measurement has been
taken on this bench — it's a representative bench-light value chosen to
land safely inside the LM358's single-supply output headroom; the real
part's output will scale with whatever light actually reaches it.

**Headroom caveat**: standard LM358 parts can't swing their output
closer than ~1.5V below VCC (single-supply). `psu_low_v2`'s output under
this circuit's sub-mA load is conservatively estimated at ~2.8V (its own
documented 2.53V figure is measured at a much heavier 253mA design-point
load — a near-zero-current load sags far less), giving a ceiling around
1.3V — the 1.0V design point has margin, but don't push `Rf` much higher
without re-checking against the real rail voltage.

---

## Validation

`main.py` streams the LM358 output (pin 1) continuously over USB serial:

```bash
mpremote run main.py
```

Cover the photodiode with a finger — the reading should drop toward 0V.
Point a flashlight at it — the reading should rise, possibly toward the
headroom ceiling above if the light is bright enough. If the reading
never moves regardless of light level, either the feedback resistor is
missing (check for a very high/noisy reading, effectively open-loop), the
photodiode is wired backwards (anode/cathode swapped), or the LM358 isn't
getting power on pin 8/pin 4.
