# Electronics Lab — Circuits

Test and measurement circuits for a physics lab bench, built bottom-up from
a bootstrap PSU through the tiers laid out in
[docs/general_purpose_circuit_dependency.md](docs/general_purpose_circuit_dependency.md).
Spacetime research (electrogravitics, the Biefeld-Brown effect) is the
current driving objective and gets its own tier graph in
[docs/spacetime_circuits_dependency.md](docs/spacetime_circuits_dependency.md),
but the general-purpose foundation underneath it — PSU tiers, protection,
safety monitoring, signal conditioning, measurement tools — isn't specific
to that goal and is meant to be useful on its own.

Each circuit gets its own top-level folder with a SPICE netlist, a
generated schematic, and a breadboard wiring guide. Power supplies are
grouped under `power_supplies/`; measurement/test tools are grouped under
`measurement_tools/`; signal-conditioning building blocks (references,
amplifiers) are grouped under `signal_conditioning/`; other circuit
categories (safety monitoring, etc.) get their own top-level folders as
they're built.

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
ngspice -b measurement_tools/fuse_test_voltmeter/fuse_test_voltmeter.spice
ngspice -b measurement_tools/cd4066_switch_tester/cd4066_switch_tester.spice
ngspice -b power_supplies/psu_pico_rail/psu_pico_rail.spice
ngspice -b power_supplies/psu_ultralow_v1/psu_ultralow_v1.spice
ngspice -b power_supplies/psu_low_v2/psu_low_v2.spice
ngspice -b power_supplies/psu_3xaa/psu_3xaa.spice
ngspice -b power_supplies/psu_4xaa/psu_4xaa.spice
ngspice -b power_supplies/psu_medlow_usbc/psu_medlow_usbc.spice
ngspice -b signal_conditioning/voltage_reference_lm358/voltage_reference_lm358.spice
```

Run from the repo root. Each netlist prints an operating point at its
nominal load, then sweeps the load resistor to show the V/I curve.

---

## Smoke-testing a circuit

Printing an operating point documents what a circuit *should* do; it
doesn't check it. Every circuit folder also has a `smoke_test.py` that
runs its netlist and asserts against real thresholds: no node exceeding a
part's safe voltage, no resistor dissipating more than its rated wattage
(where the resistor is an actual physical part — some netlists use `Rload`
purely as a simulated stand-in for whatever gets attached later, which
isn't a smoke risk on its own), and a functional check that the circuit
actually does what it claims (a divider ratio within tolerance, a
buffered reference holding steady under load, a switch reading
unambiguously different when open vs. closed). `tools/ngspice_runner.py`
holds the shared ngspice-invocation/parsing logic every `smoke_test.py`
reuses.

```bash
# from the repo root
python measurement_tools/cd4066_switch_tester/smoke_test.py
python measurement_tools/fuse_test_voltmeter/smoke_test.py
python power_supplies/psu_low_v2/smoke_test.py
python power_supplies/psu_3xaa/smoke_test.py
python power_supplies/psu_4xaa/smoke_test.py
python power_supplies/psu_medlow_usbc/smoke_test.py
python power_supplies/psu_pico_rail/smoke_test.py
python power_supplies/psu_ultralow_v1/smoke_test.py
python signal_conditioning/voltage_reference_lm358/smoke_test.py
```

Or run all of them at once with `tools/run_all_smoke_tests.py`, which
finds every `smoke_test.py` in the repo so this list doesn't have to be
kept in sync by hand:

```bash
# from the repo root
python tools/run_all_smoke_tests.py
```

Exits non-zero on any failed check.

---

## Circuits — built & bench-tested

Each of these has been physically assembled and confirmed against its
`main.py`/`smoke_test.py` pass criteria on real hardware. Not committed
to a breadboard permanently — once a circuit's bench check passes and
nothing else currently under construction needs its wiring in place, its
parts go back to inventory; the netlist/breadboard.md/smoke_test.py stay
as the record for rebuilding it later.

| Folder | Circuit | Tier | Bench-tested |
|--------|---------|------|--------------|
| `power_supplies/psu_pico_rail/` | Pico's own onboard 3.3V rail, ~100mA budget | interim bootstrap PSU | 2026-08 |
| `signal_conditioning/voltage_reference_lm358/` | LM358 unity-gain buffer holds a resistor-divider reference steady under load | tier1 `REF` | 2026-08-27 — loaded reading within 0.23% of unloaded (±2% tolerance) |
| `measurement_tools/cd4066_switch_tester/` | Pico-driven bring-up jig for one CD4066B analog switch — confirms it passes/blocks before trusting it in a later design | component validation (ahead of tier9 `MUX`) | 2026-08-28 — switch 1 (I/O A pin 1 / I/O B pin 2 / control pin 13) PASS on all 10 CD4066BCN units; switches 2–4 per chip not yet individually tested |
| `measurement_tools/fuse_test_voltmeter/` | Pico ADC probe across a battery→fuse→resistor loop; arm switch (GP15) gates trip/reset detection so battery connect/disconnect isn't misread as a trip | bootstrap / concurrent measurement tool | 2026-08-28 — **bench wiring has since diverged from this design and trip detection is currently non-functional**: the 10Ω resistor was physically removed and the fuse wired straight onto the power rail, which collapses the probe (GP26) and GND nodes into one — the jig now reads ~0V regardless of whether the fuse is tripped, since there's no longer a divider to read across (see `docs/kb/repo_docs_conventions.md` "resistor removal breaks trip detection"). Prior to the removal: arm switch toggled ARMED/DISARMED correctly, loaded reading was steady ~1.36–1.50V across runs (matches SPICE prediction scaled to this cell's ~1.6V open-circuit voltage). The deliberate-short trip/reset pass/fail check from `quickstart.md` has never actually passed on this build. **This no longer blocks polyfuse validation**: both fuse batches have since been sorted good/bad by the `ammeter_10ohm`/`ammeter_1ohm` jigs below instead, which measure current directly rather than inferring a trip from a voltage probe. Fixing this jig's own wiring gap is optional going forward, not a prerequisite for anything currently planned |
| `measurement_tools/ammeter_10ohm/` | Pico reads current (not just voltage) through a polyfuse under test, via a 10Ω shunt + slide-switch shorting jumper | polyfuse validation (bootstrap tier) | 2026-08-30 — all 20 RXEF005 (50mA) polyfuses PASS (trip + reset confirmed per unit) |
| `measurement_tools/ammeter_1ohm/` | Same approach as `ammeter_10ohm` scaled for 500mA: ~1Ω jumper-chain shunt (see `resistance_measurement/`) + 1N5817 reverse-polarity diode on the high side | polyfuse validation (`psu_low` tier) | 2026-08-30 — all 20 RXEF050 (500mA) polyfuses PASS (trip + reset confirmed per unit) |
| `measurement_tools/resistance_measurement/` | Voltage-divider jig (known 10Ω reference vs. unknown leg) for measuring a low-value resistance without a multimeter | supporting tool for `ammeter_1ohm` | 2026-08-30 — jumper-wire chain measured at ~1.005Ω, stable across repeated readings |
| `power_supplies/psu_ultralow_v1/` | Single AA + 50 mA polyfuse | `psu_ultralow` (bootstrap) | 2026-08-30 — component-level validation complete: RXEF005 polyfuse PASS via `ammeter_10ohm/` (all 20 units), AA battery holder ready per `pico/docs/inventory.md`. The assembled PSU itself has not been separately re-probed as its own demo build (see `fuse_test_voltmeter/README.md`'s test-vs-demo distinction) |

---

## Circuits — designed, not yet built

Build order runs top to bottom: the voltmeter has to exist — and its own
fuse-free sanity check has to pass — before it's trustworthy for sorting
good polyfuses from bad, and a polyfuse has to be sorted good before it
belongs in a PSU. See
[measurement_tools/fuse_test_voltmeter/README.md](measurement_tools/fuse_test_voltmeter/README.md)
for the voltmeter self-check → bench-test-the-fuse-batch → demo-in-a-PSU
sequence this drives.

| Folder | Circuit | Tier |
|--------|---------|------|
| `power_supplies/psu_low_v2/` | 2×AA + Schottky + 500 mA polyfuse | `psu_low` (waiting on wire strippers; RXEF050 polyfuse itself is validated — see `ammeter_1ohm/` above) |
| `power_supplies/psu_3xaa/` | 3×AA + Schottky + 500 mA polyfuse | `psu_system` (between `psu_low` and `psu_4xaa`) |
| `power_supplies/psu_4xaa/` | 4×AA + Schottky + 500 mA polyfuse | `psu_system` (top of the plain-AA-series progression) |
| `power_supplies/psu_medlow_usbc/` | 5V USB-C + 500 mA polyfuse + bypass cap | `psu_medlow` |
| `power_supplies/psu_medlow_lm317/` | SFE Breadboard Power Supply Kit — LM317 adjustable, 3.3V/5V-selectable | `psu_medlow` (alternative to `psu_medlow_usbc`; kit on order, not yet built) |

Each of these (except `psu_medlow_lm317`, an on-order kit with no netlist
of its own — see its own README) has a SPICE netlist, a generated
schematic, a breadboard wiring guide, and a `smoke_test.py`, but none have
been physically assembled with real components yet. The polyfuses they
depend on are no longer the blocker — both batches passed validation via
`ammeter_10ohm`/`ammeter_1ohm` above — so what remains is just the
physical build. Everything else in
`docs/general_purpose_circuit_dependency.md` /
`docs/spacetime_circuits_dependency.md` (safety monitoring, most of tiers
1–9) hasn't been worked out to netlist stage at all — folders for those
will show up here as they get one.

---

## Notes

- `measurement_tools/fuse_test_voltmeter/`, `cd4066_switch_tester/`, and
  `signal_conditioning/voltage_reference_lm358/` are the circuits here with
  Pico firmware (`main.py`) checked in. For more
  capable Pico ADC work (filtering, calibration curves, noise
  characterization), see the sibling `pico/` repo's
  `measurement_tools/gpio_analog_sensing/` — that repo isn't limited to
  one project, so general-purpose Pico infrastructure lives there rather
  than being duplicated here.
- Getting the physical Pico talking to this PC (WSL + `usbipd` device
  attach, MicroPython firmware, installing/using `mpremote`) is documented
  once in the sibling `pico/` repo rather than duplicated here — see
  [pico/README.md § Running on real hardware](../pico/README.md#running-on-real-hardware).
  Needed any time you run one of this repo's `main.py` scripts against
  real hardware instead of just simulating.
- See `docs/orders.md` for what's actually been ordered/received from
  AliExpress, and `docs/parts_reference.md` for pinouts/specs on those
  parts. Physical part counts are also mirrored into the sibling `pico/`
  repo's `pico/docs/inventory.md`, the shared master inventory across both
  repos.

---

## Repo structure

```
measurement_tools/
    fuse_test_voltmeter/     Pico ADC voltmeter, validates polyfuses via USB (built & bench-tested; trip/reset short test still pending)
        fuse_test_voltmeter.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

    cd4066_switch_tester/    CD4066B analog-switch bring-up jig (built & bench-tested)
        cd4066_switch_tester.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

    ammeter_10ohm/           10Ω-shunt current-based polyfuse tester (built & bench-tested)
        main.py
        breadboard.jpg
        README.md

    ammeter_1ohm/            ~1Ω-shunt version for 500mA polyfuses (built & bench-tested)
        main.py
        breadboard.jpg
        README.md

    resistance_measurement/  voltage-divider jig for measuring an unknown low resistance (built & bench-tested)
        main.py
        breadboard.jpg
        README.md

power_supplies/
    psu_pico_rail/            Pico onboard 3.3V rail, ~100mA (interim, built & bench-tested)
        psu_pico_rail.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_ultralow_v1/         single AA + 50 mA polyfuse (built & bench-tested — component-level)
        psu_ultralow_v1.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_low_v2/               2xAA + Schottky + 500 mA polyfuse (designed, not built)
        psu_low_v2.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_3xaa/                 3xAA + Schottky + 500 mA polyfuse (designed, not built)
        psu_3xaa.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_4xaa/                 4xAA + Schottky + 500 mA polyfuse (designed, not built)
        psu_4xaa.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_medlow_usbc/          5V USB-C + 500 mA polyfuse + bypass cap (designed, not built)
        psu_medlow_usbc.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_medlow_lm317/         SFE breadboard PSU kit, LM317 3.3V/5V-selectable (on order, not built)
        breadboard.md
        README.md

signal_conditioning/
    voltage_reference_lm358/  LM358 buffered voltage reference (built & bench-tested)
        voltage_reference_lm358.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

docs/
    history.md                                  design conversation log
    general_purpose_circuit_dependency.md       general-purpose tier graph (PSU, protection, tiers 1-4/6/9, scope/logic-analyzer tiers M0-M5)
    spacetime_circuits_dependency.md            spacetime-specific tier graph (tiers 5/7/8)
    orders.md                                   AliExpress order log (received / on order)
    parts_reference.md                          pinouts & specs for ordered parts without a datasheet on file
    manuals/                                    converted (markitdown) part manuals; source PDFs gitignored
    kb/                                         process notes for future LLM sessions, not end-user docs

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
    ngspice_runner.py       shared ngspice-invocation/parsing helper for smoke_test.py scripts
    run_all_smoke_tests.py  finds and runs every smoke_test.py in the repo
```
