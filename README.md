# Spacetime Research Lab — Circuits

Test and measurement circuits for a physics lab bench, built bottom-up from
a bootstrap PSU through the tiers laid out in
[docs/spacetime_circuits_dependency.md](docs/spacetime_circuits_dependency.md).
See [docs/history.md](docs/history.md) for the design conversation behind
each circuit — component choices, tradeoffs, and dead ends included.

Each circuit gets its own top-level folder with a SPICE netlist, a
generated schematic, and a breadboard wiring guide.

---

## Schematics

Each project has a `schematic.png` generated from its `.spice` netlist. To
regenerate any schematic after editing the netlist:

```bash
# from the repo root
python tools/spice_to_schematic.py psu_ultralow_v1/psu_ultralow_v1.spice
```

Output is written as `schematic.png` in the same directory as the `.spice`
file. `tools/spice_to_schematic.py` uses **schemdraw** to parse SPICE `R`,
`C`, `V`, and `D` elements and render a schematic image.

---

## Running simulations

Every circuit folder has an ngspice `.spice` netlist. Run with `ngspice -b`
to predict voltages and currents before building.

```bash
# from the repo root
ngspice -b psu_ultralow_v1/psu_ultralow_v1.spice
ngspice -b psu_low_v2/psu_low_v2.spice
ngspice -b psu_medlow_usbc/psu_medlow_usbc.spice
```

Run from the repo root. Each netlist prints an operating point at its
nominal load, then sweeps the load resistor to show the V/I curve.

---

## Circuits (built)

| Folder | Circuit | Tier |
|--------|---------|------|
| `psu_ultralow_v1/` | Single AA + 50 mA polyfuse | `psu_ultralow` (bootstrap) |
| `psu_low_v2/` | 2×AA + Schottky + 500 mA polyfuse | `psu_low` |
| `psu_medlow_usbc/` | 5V USB-C + 500 mA polyfuse + bypass cap | `psu_medlow` |

Everything else in `docs/spacetime_circuits_dependency.md` (safety
monitoring, tiers 1–9, bootstrap measurement tools) is designed but not yet
built — folders for those will show up here as they get a netlist to test.

---

## Notes

- No Raspberry Pi Pico firmware lives in this repo. Where a build uses the
  Pico as a validation instrument (ADC probing, fuse trip tests), that's
  called out in the circuit's `README.md` and covered in `docs/history.md`
  — code, if any, stays local to the test session rather than checked in.
- See `docs/history.md` for the reasoning behind part substitutions
  (e.g. why the fuse is 50 mA and not 500 mA, why the AA holder is two
  single-cell holders instead of one 2×AA holder).

---

## Repo structure

```
psu_ultralow_v1/            single AA + 50 mA polyfuse (built)
    psu_ultralow_v1.spice
    schematic.png
    breadboard.md
    README.md

psu_low_v2/                 2xAA + Schottky + 500 mA polyfuse (built)
    psu_low_v2.spice
    schematic.png
    breadboard.md
    README.md

psu_medlow_usbc/            5V USB-C + 500 mA polyfuse + bypass cap (built)
    psu_medlow_usbc.spice
    schematic.png
    breadboard.md
    README.md

docs/
    history.md                          design conversation log
    spacetime_circuits_dependency.md    full dependency diagram (mermaid)

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
```
