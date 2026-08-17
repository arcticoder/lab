# psu_ultralow_v1

Single AA alkaline cell behind a 50 mA slow-blow polyfuse. This is the
bootstrap power tier — the first PSU in the build order, with no regulation
and no adjustability, just a battery and a resettable fuse.

Spec: 1.5 V, ~100 mA, <0.15 W. See
[docs/spacetime_circuits_dependency.md](../../docs/spacetime_circuits_dependency.md)
(`psu_ultralow` node) and [docs/history.md](../../docs/history.md) for the
design conversation.

---

## Files

| File | Purpose |
|------|---------|
| `psu_ultralow_v1.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step breadboard wiring |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. AA battery holder, positive lead to the polyfuse.
2. Polyfuse (Littelfuse RXEF005 / 50 mA slow-blow) in series on the positive
   rail.
3. Battery negative ties directly to the ground rail.
4. Output taken from polyfuse output (+) and battery negative (−).

---

## Simulate

```bash
# from the repo root
ngspice -b psu_ultralow_v1/psu_ultralow_v1.spice
```

The first block prints the operating point at the nominal 15 Ω load
(~100 mA design point). The second block sweeps the load from 5 Ω to 100 Ω
to show how output voltage sags as current increases — this is the AA
cell's internal resistance at work, not the fuse (which is modeled at its
cold-state resistance only; this netlist doesn't simulate the PTC trip
transient).

---

## Expected behaviour

```
V_out ≈ 1.5V × Rload / (Rload + Rbatt + Rfuse)
```

At Rload = 15 Ω: **V_out ≈ 1.44 V, I ≈ 96 mA** — close to the 100 mA design
point. Below Rload = 15 Ω, current rises above the 50 mA polyfuse's steady
rating and it will eventually trip (not modeled here — see
`docs/history.md` for the LED-and-Pico trip demonstration).

---

## Validation without a multimeter

Probe across the polyfuse leads with a Pico ADC pin (GP26) referenced to
ground — voltage drop across the fuse should be small (~50 mV) under normal
load and climb sharply if you force a trip by shorting the load resistor.
See `docs/history.md` (2026-08-15) for the full fuse trip-test walkthrough.
