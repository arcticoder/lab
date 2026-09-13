# TODO — agent (Claude-facing)

This is the mirror of [TODO-arcticoder.md](TODO-arcticoder.md) for work
that doesn't need the user's hands, eyes, or a purchasing decision — just
writing files. Design/simulate/document a circuit here (netlist,
`breadboard.md`, `smoke_test.py`, `README.md`, optionally `main.py`) as
its own PR-sized unit of work, *before* it ever gets a "physically
assemble" bullet added to `TODO-arcticoder.md`'s "Ready to build now"
section. See
[docs/kb/todo_list_conventions.md](kb/todo_list_conventions.md) for why
this split exists and the reasoning behind each entry's queue position.

Mirrors the sibling `aqei-bridge` repo's `docs/TODO.md` (a pure
agent-task list — see that repo for the pattern this one is modeled on).

**Workflow**: pick an item below (top-to-bottom isn't a strict ordering
requirement here the way it is in `TODO-arcticoder.md` — none of these
block each other), design and verify it (simulate with `ngspice -b`,
confirm the numbers, run `smoke_test.py` and get it green) the same way
`signal_conditioning/transimpedance_amplifier/` and
`measurement_tools/capacitance_bridge/` were built 2026-09-13, then:

1. Move the item from here to `TODO-completed.md` (dated entry, same
   convention as `TODO-arcticoder.md`'s completions).
2. Add a "physically assemble" bullet for it to `TODO-arcticoder.md`'s
   "Ready to build now" section, stating its real dependency (check
   `general_purpose_circuit_dependency.md`/`spacetime_circuits_dependency.md`
   first — don't infer one from list position, see
   `kb/todo_list_conventions.md`'s TIA correction) and whether anything
   downstream currently needs it built, or whether it's optional/no-rush
   like `TIA`/`CAPBRIDGE` turned out to be.
3. Update this file's own item count/status references elsewhere (this
   file's own intro doesn't currently carry one, but `TODO-arcticoder.md`'s
   "Next AliExpress order" section does — check it).

---

## Open items

### `PHASED` — tier4 phase detector

Part on hand: SN74HC86N quad 2-input XOR gate (1 unit, arrived
2026-09-12; DIP-14 per the listing's own truncated variant string,
**unconfirmed against the physical part** — see
[parts_reference.md](parts_reference.md#sn74hc86n-quad-2-input-xor-gate)
for the caveat, check this before designing pin assignments). Feeds tier6
`LOCKIN`.

Design note not yet resolved: a classic XOR phase detector needs two
square waves of the same frequency at a variable phase offset — this
bench has one square-wave source (`oscillators/ne555_astable`), not two
phase-related ones. Before writing a netlist, work out what the second
input actually is on this bench (a second NE555 stage, a GPIO-driven
reference square wave from the Pico, or something else) — don't assume a
second oscillator exists without checking.

### `THERM` replacement — general-purpose temperature sensing

Part on hand: MF52AT 10kΩ NTC thermistor (10 units, arrived 2026-09-12).
Replaces the "suspect faulty" thermistor currently in `inventory.md`; no
folder/circuit exists yet. No dependency-graph tier node currently named
for this — check whether it maps to an existing undesigned node
(`TEMPCOMP`, tier3) or stands alone before creating the folder.

Likely most tractable design here: a resistor-divider + Pico ADC
temperature readout (thermistor value → ADC voltage → resistance via the
same divider math as `measurement_tools/resistance_measurement`, then
resistance → temperature via the MF52AT's beta/Steinhart-Hart
coefficients from its datasheet) — similar complexity class to
`capacitance_bridge`, not a novel topology.

### `ACTIVELIM`/`HVPULSE` — protection current limiter + tier7/8 HV pulse

Part on hand: IRLZ44N logic-level MOSFET (1 unit only, arrived
2026-09-12) — serves both nodes until/unless more are ordered, so whoever
picks this up first should design with that scarcity in mind (e.g. don't
consume the only unit on a throwaway test if both nodes need it).
`ACTIVELIM` feeds `psu_medhigh`/`psu_high` (both backlog, undesigned —
see `general_purpose_circuit_dependency.md`'s `ACTIVELIM -.required.->`
edges). `HVPULSE` is tier8 spacetime work
(`spacetime_circuits_dependency.md`).

**Flag before starting**: `HVPULSE` implies actual high-voltage pulse
generation — this needs a real safety design pass (isolation, discharge
paths, what "high" actually means here numerically) before any netlist,
not just a topology copy-paste. Don't treat this the same way as the
low-voltage sensor builds above.

### `EPFIELD` — tier5 electric field probe

Part on hand: TL082 JFET-input dual op-amp (10 units, arrived
2026-09-12) — picked specifically for input impedance a bipolar-input
LM358 can't provide. No electrode/probe hardware identified yet in
`inventory.md`/`orders.md` — check whether a physical sensing electrode
needs to be ordered before this can be fully designed, or whether a
simple exposed-wire/foil electrode is the intended approach for a first
build.

### `CHGAMP` — tier5 charge amplifier

Parts on hand: TL082 (shared with `EPFIELD` above) + 12mm piezo disc (20
units, arrived 2026-09-12) as the charge-output transducer. Standard
charge-amp topology: piezo modeled as a capacitive charge source, op-amp
in an integrator-like configuration with a feedback **capacitor** (not a
resistor — contrast with `transimpedance_amplifier`'s feedback resistor)
plus a large parallel bias resistor to prevent output drift. Check the
electrolytic/ceramic capacitor kits in `inventory.md` for a suitable
feedback capacitor value before assuming one needs to be ordered.

---

## Completed (moved out)

- **2026-09-13**: `signal_conditioning/transimpedance_amplifier/` (`TIA`)
  and `measurement_tools/capacitance_bridge/` (`CAPBRIDGE`) — both
  designed, simulated (`ngspice -b`, confirmed against hand-derived
  expected values), smoke-tested (green), and documented
  (`README.md`/`breadboard.md`/`main.py`). See
  [TODO-completed.md](TODO-completed.md) for the full entry and
  `TODO-arcticoder.md`'s "Ready to build now" for their new
  physically-assemble bullets.
