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

## Validation without a multimeter

Probe across the Schottky with a Pico ADC pin. Forward bias should read
~0.35 V drop; reversing the battery leads should read ~0 V across the load
(diode blocking).
