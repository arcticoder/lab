# psu_low_v2

2× AA alkaline cells in series, a 1N5817 Schottky diode for reverse-polarity
protection, and a 500 mA slow-blow polyfuse. Upgrade path from
[psu_ultralow_v1](../psu_ultralow_v1/) — same battery chemistry, more
headroom.

Spec: 3.0 V, <300 mA, ~0.9 W. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_low` node).

---

## Files

| File | Purpose |
|------|---------|
| `psu_low_v2.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step breadboard wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Two single-cell AA holders wired in series (holder 1 negative → holder 2
   positive).
2. 1N5817 Schottky diode in series on the positive rail (cathode stripe
   toward the fuse), blocking reverse-polarity wiring.
3. 500 mA polyfuse (Littelfuse RXEF050) in series after the diode.
4. Output taken from polyfuse output (+) and holder 2 negative (−).

---

## Simulate

```bash
# from the repo root
ngspice -b psu_low_v2/psu_low_v2.spice
```

The first block prints the operating point at the nominal 10 Ω load
(~265 mA design point, after the Schottky drop). The second block sweeps
the load from 5 Ω to 30 Ω.

---

## Expected behaviour

```
V_out ≈ (3.0V − V_schottky) × Rload / (Rload + Rfuse)
```

At Rload = 10 Ω: **V_out ≈ 2.53 V, I ≈ 253 mA** — the Schottky costs about
0.35 V at this current.

---

## Validation without a multimeter

Probe across the Schottky with a Pico ADC pin. Forward bias should read
~0.35 V drop; reversing the battery leads should read ~0 V across the load
(diode blocking).
