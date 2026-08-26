# psu_pico_rail

The Raspberry Pi Pico's own onboard 3.3V regulator (3V3(OUT), pin 36),
used directly as a bench PSU for low-current circuits. No battery holder,
no polyfuse, no wiring beyond a couple of jumpers — the Pico is already on
the bench for every measurement tool in this repo, so this is the fastest
path to a working rail while [psu_ultralow_v1](../psu_ultralow_v1/) and
[psu_low_v2](../psu_low_v2/) wait on wire strippers to arrive for their AA
battery holder leads.

Spec: 3.3V, treat **~100mA as the safe external budget**. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_pico_rail` node) for where this sits relative to the other PSU tiers.

---

## Files

| File | Purpose |
|------|---------|
| `psu_pico_rail.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Plug the Pico into the PC over USB (this is what powers the onboard
   regulator).
2. Jumper from **3V3(OUT)** (physical pin 36) to your circuit's positive
   rail.
3. Jumper from any **GND** pin (e.g. physical pin 38) to your circuit's
   ground rail.

---

## Simulate

```bash
# from the repo root
ngspice -b power_supplies/psu_pico_rail/psu_pico_rail.spice
```

The first block prints the operating point at the nominal 33 Ω load
(~94 mA design point). The second block sweeps the load from 15 Ω to 100 Ω.

---

## Expected behaviour

```
V_out ≈ 3.3V × Rload / (Rload + Rint)
```

At Rload = 33 Ω: **V_out ≈ 3.11 V, I ≈ 94 mA**. `Rint` (2 Ω) is an
illustrative approximation, not a datasheet figure — the RP2040/Pico
datasheet documents the onboard RT6150 regulator as capable of ~300 mA
total, but that's shared with the Pico's own ~20–30 mA logic draw and
hasn't been independently measured here. Treat 100mA as a conservative
external budget, not a hard verified limit.

---

## Validation without a multimeter

Probe the 3V3(OUT) pin directly with a second Pico's ADC (or a similar
single-Pico probe setup) to confirm the rail holds close to 3.3V under
your circuit's actual load before trusting it — same philosophy as the
other PSU tiers' "validation without a multimeter" sections.

---

## When to move on

This rail is for **low-current circuits only** (tens of mA, not the
~250–500 mA the AA/USB-C tiers target). Once wire strippers are on hand
and `psu_ultralow_v1`/`psu_low_v2` are buildable, switch any circuit that
needs more than ~100 mA — or that should be electrically independent of
the PC/Pico's own USB power — over to one of those instead.
