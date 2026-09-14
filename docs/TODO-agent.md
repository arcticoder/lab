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

### `HVPULSE` — tier7/8 high-voltage pulse generator

**Still blocked on a scope decision, not a part.** The only IRLZ44N on
hand was consumed designing [ACTIVELIM](../protection/active_current_limiter/)
instead (see that circuit's README § Design notes for why it was
prioritized) — a second unit would need ordering before this could use
its own MOSFET regardless. More fundamentally: nothing on this bench
currently defines what "high voltage" means here numerically. There's no
HV source of any kind in inventory (the highest voltage anywhere on the
bench is the Lenovo adapter's 20V) and no isolation/discharge-path safety
design has been done. **Don't start a netlist for this without first
getting an actual target peak voltage/energy figure and a real safety
design pass (isolation, discharge paths)** — this is a judgment call
that needs the human, not something to infer from the tier graph's
generic label.

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
- **2026-09-13** (second pass, same day): `signal_conditioning/
  electric_field_probe/` (`EPFIELD`, tier5), `signal_conditioning/
  charge_amplifier/` (`CHGAMP`, tier5), `safety/thermal_monitor/`
  (`THERM`), `signal_conditioning/phase_detector/` (`PHASED`, tier4),
  and `protection/active_current_limiter/` (`ACTIVELIM`) — all five
  designed, simulated, smoke-tested (green), and documented. This was
  the direct spacetime-research sensor chain (`EPFIELD`/`CHGAMP` are
  named tier5 nodes in `spacetime_circuits_dependency.md`, not general
  infrastructure) plus the `PHASED` node that unlocks tier6 `LOCKIN`
  processing of their output — see
  [kb/spacetime_sensor_chain_notes.md](kb/spacetime_sensor_chain_notes.md)
  for the design decisions made along the way (single-supply ADC-safety
  bias pattern, the resolved "second oscillator" question for `PHASED`,
  and a real hard-trip chattering limitation `ACTIVELIM`'s own
  simulation surfaced). `HVPULSE` (shares `ACTIVELIM`'s MOSFET) remains
  open above — it needs a scope decision, not more design time. See
  [TODO-completed.md](TODO-completed.md) for the full entry and
  `TODO-arcticoder.md`'s "Ready to build now" for the new
  physically-assemble bullets.
