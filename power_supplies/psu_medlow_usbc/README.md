# psu_medlow_usbc

5V USB-C wall adapter, a 500 mA polyfuse, and a 100 nF bypass cap to smooth
adapter ripple. No local regulation — the wall adapter already regulates to
5V, so this is fuse + bypass only.

Spec: 5V USB path of the medium-low tier. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_medlow` node) and [docs/history.md](../../docs/history.md) for the design
conversation.

---

## Files

| File | Purpose |
|------|---------|
| `psu_medlow_usbc.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image, gitignored — see repo `README.md` (note: the schematic tool only draws V/R/D elements, so the bypass cap isn't rendered — see the netlist for the full circuit) |
| `breadboard.md` | Step-by-step breadboard wiring |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. USB-C breakout board (breadboard-compatible pin breakout, passive — no PD
   negotiation) fed from any USB-C wall adapter.
2. 500 mA polyfuse (Littelfuse RXEF050) in series on VBUS.
3. 100 nF ceramic bypass cap from the fuse output to ground.
4. Output taken from the bypass cap node (+) and adapter GND (−).

---

## Simulate

```bash
# from the repo root
ngspice -b psu_medlow_usbc/psu_medlow_usbc.spice
```

The first block prints the operating point at the nominal 10 Ω load
(~500 mA — right at the polyfuse trip point by design). The second block
sweeps the load from 5 Ω to 50 Ω.

---

## Expected behaviour

```
V_out ≈ 5.0V × Rload / (Rload + Rfuse)
```

At Rload = 10 Ω: **V_out ≈ 4.76 V, I ≈ 476 mA** — close to the fuse's rated
threshold, which is intentional: this load point exercises the fuse near
its trip boundary. Use a higher Rload (lighter load) for normal operation.
