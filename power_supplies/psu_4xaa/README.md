# psu_4xaa

4× AA alkaline cells in series, a 1N5817 Schottky diode for reverse-polarity
protection, and a 500 mA slow-blow polyfuse. Top of the plain-AA-series
progression — one cell up from [psu_3xaa](../psu_3xaa/), same battery
chemistry and protection stack as every AA tier below it.

Spec: 6.0 V, <300 mA, ~1.6 W. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_system` subgraph).

---

## Files

| File | Purpose |
|------|---------|
| `psu_4xaa.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step breadboard wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Four single-cell AA holders wired in series (holder 1 negative → holder
   2 positive → holder 3 positive → holder 4 positive, chained).
2. 1N5817 Schottky diode in series on the positive rail (cathode stripe
   toward the fuse), blocking reverse-polarity wiring.
3. 500 mA polyfuse (Littelfuse RXEF050) in series after the diode.
4. Output taken from polyfuse output (+) and holder 4 negative (−).

---

## Simulate

```bash
# from the repo root
ngspice -b power_supplies/psu_4xaa/psu_4xaa.spice
```

The first block prints the operating point at the nominal 20 Ω load
(~276 mA design point, after the Schottky drop). The second block sweeps
the load from 5 Ω to 50 Ω.

---

## Expected behaviour

```
V_out ≈ (6.0V − V_schottky) × Rload / (Rload + Rfuse)
```

At Rload = 20 Ω: **V_out ≈ 5.51 V, I ≈ 276 mA** — the Schottky costs about
0.35 V at this current, same as every other AA tier in this family.

---

## Validation

No multimeter, and no physical load resistor either (see
[breadboard.md § Expected behavior](breadboard.md#expected-behavior) for
why 20 Ω isn't something to build). The check instead uses a lightweight
2:1 resistor divider so a Pico ADC pin can safely read this PSU's ~5.5 V
output — GP26/ADC0 is limited to 0–3.3V (see
`docs/general_purpose_circuit_dependency.md`'s `SCOPEPICO` node), so it
can never be wired straight onto this rail.

**Build:** two 10 kΩ resistors (from `pico/docs/inventory.md`) in series
across the output, from output(+) to output(−)/ground rail, with the
midpoint tapped off to GP26.

```
psu_4xaa output (+)
      │
   [10 kΩ]
      │
      ├──────► Pico GPIO 26 / ADC0 (Pin 31)
      │
   [10 kΩ]
      │
psu_4xaa output (−) / ground rail ──────► Pico GND (Pin 28)
```

At ~275 µA, this divider draws negligible current — it doesn't meaningfully
load the PSU, and it's the *only* thing connected to the output for this
check (no other load).

**Expected readings** (read GP26 with the same ADC-averaging approach as
[measurement_tools/resistance_measurement](../../measurement_tools/resistance_measurement/)):

- Correct battery orientation: GP26 reads **~2.75 V** (half of the output
  voltage). Expect the output itself to sit a little *above* the
  documented ~5.51 V design figure — that number assumes the 276 mA drawn
  by a 20 Ω load, and this divider's ~275 µA draws far less, so the
  Schottky/fuse drops are smaller here.
- Reversed battery leads: GP26 reads **~0 V** — the Schottky blocks, no
  current reaches the divider.

Don't probe directly across the Schottky's own leads with the Pico —
doing that safely would mean moving Pico GND off the PSU's actual ground
rail (onto the diode's cathode) just for that one reading, which is easy
to get wrong and unnecessary here: the divider above already distinguishes
"diode conducting" from "diode blocking" without ever re-referencing
ground.
