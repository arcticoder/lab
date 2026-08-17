# Spacetime Research Lab — Circuits

Test and measurement circuits for a physics lab bench, built bottom-up from
a bootstrap PSU through the tiers laid out in
[docs/spacetime_circuits_dependency.md](docs/spacetime_circuits_dependency.md).
See [docs/history.md](docs/history.md) for the design conversation behind
each circuit — component choices, tradeoffs, and dead ends included.

Each circuit gets its own top-level folder with a SPICE netlist, a
generated schematic, and a breadboard wiring guide. Power supplies are
grouped under `power_supplies/`; other circuit categories (measurement
tools, safety monitoring, etc.) get their own top-level folders as they're
built.

---

## Schematics

Each project can render a `schematic.png` from its `.spice` netlist.
`schematic.png` is **not committed** (see `.gitignore`) — it's a build
artifact, regenerated on demand:

```bash
# from the repo root
python tools/spice_to_schematic.py power_supplies/psu_ultralow_v1/psu_ultralow_v1.spice
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
ngspice -b power_supplies/psu_ultralow_v1/psu_ultralow_v1.spice
ngspice -b power_supplies/psu_low_v2/psu_low_v2.spice
ngspice -b power_supplies/psu_medlow_usbc/psu_medlow_usbc.spice
ngspice -b fuse_test_voltmeter/fuse_test_voltmeter.spice
```

Run from the repo root. Each netlist prints an operating point at its
nominal load, then sweeps the load resistor to show the V/I curve.

---

## Circuits (designed, not yet built)

| Folder | Circuit | Tier |
|--------|---------|------|
| `power_supplies/psu_ultralow_v1/` | Single AA + 50 mA polyfuse | `psu_ultralow` (bootstrap) |
| `power_supplies/psu_low_v2/` | 2×AA + Schottky + 500 mA polyfuse | `psu_low` |
| `power_supplies/psu_medlow_usbc/` | 5V USB-C + 500 mA polyfuse + bypass cap | `psu_medlow` |
| `fuse_test_voltmeter/` | Pico ADC probe, streams voltage over USB to validate a polyfuse before it's trusted near an LED | bootstrap / concurrent measurement tool |

Each of these has a SPICE netlist, a generated schematic, and a breadboard
wiring guide, but none have been physically assembled yet. Everything else
in `docs/spacetime_circuits_dependency.md` (safety monitoring, tiers 1–9,
remaining bootstrap measurement tools) hasn't been worked out to netlist
stage at all — folders for those will show up here as they get one.

---

## Notes

- `fuse_test_voltmeter/` is the one circuit here with Pico firmware
  (`main.py`) checked in — everywhere else the Pico is used purely as an ad
  hoc probe, per the design conversation in `docs/history.md`. For more
  capable Pico ADC work (filtering, calibration curves, noise
  characterization), see the sibling `pico/` repo's
  `gpio_analog_sensing/` — that repo isn't limited to one project, so
  general-purpose Pico infrastructure lives there rather than being
  duplicated here.
- See `docs/history.md` for the reasoning behind part substitutions
  (e.g. why the fuse is 50 mA and not 500 mA, why the AA holder is two
  single-cell holders instead of one 2×AA holder).

---

## Repo structure

```
power_supplies/
    psu_ultralow_v1/         single AA + 50 mA polyfuse (designed, not built)
        psu_ultralow_v1.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        README.md

    psu_low_v2/               2xAA + Schottky + 500 mA polyfuse (designed, not built)
        psu_low_v2.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        README.md

    psu_medlow_usbc/          5V USB-C + 500 mA polyfuse + bypass cap (designed, not built)
        psu_medlow_usbc.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        README.md

fuse_test_voltmeter/         Pico ADC voltmeter, validates polyfuses via USB (designed, not built)
    fuse_test_voltmeter.spice
    schematic.png             (generated, gitignored)
    breadboard.md
    main.py
    README.md

docs/
    history.md                          design conversation log
    spacetime_circuits_dependency.md    full dependency diagram (mermaid)

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
```
