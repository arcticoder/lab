# TODO — completed (arcticoder)

Entries move here from
[TODO-arcticoder.md](TODO-arcticoder.md) once done, instead of being
deleted — this is the audit trail of what was on the active checklist and
when it was closed out, so finished work stays visible and isn't
accidentally re-proposed or duplicated later. Mirrors the format used in
the sibling `aqei-bridge` repo's `docs/TODO-completed.md`: one `##
YYYY-MM-DD` heading per closure batch, with a short bullet per item under
it.

This is a different record from `README.md`'s "built & bench-tested"
table and `docs/history.md`: those track a *circuit's* real-world status
(has it been physically assembled and validated), while this file tracks
the *TODO item's* lifecycle (was it on the list, and when did it come
off). A circuit can be bench-tested without its TODO wording exactly
matching, so don't assume one file makes the other redundant.

---

## 2026-09-10

- Checked out the AliExpress cart: CY7C68013A / EZ-USB FX2LP USB logic
  analyzer board (`SCOPELA`) and GY-521 (MPU6050) accelerometer module,
  plus a color-ring inductor assortment reorder added to clear the $10
  free-shipping minimum. All three now "on order" in
  [orders.md](orders.md) — see [TODO-arcticoder.md](TODO-arcticoder.md)
  § "Blocked — waiting on a shipment."
- Sourced a replacement for the cancelled color-ring inductor assortment
  (0307 1/4W, 12 values) — reordered the same listing/variant, still
  cheapest available.

## 2026-09-11

- **`power_supplies/psu_4xaa` § Validation check — passed.** GP26 read
  ~1.9V through the output's divider, confirming the PSU's 4-cell chain,
  Schottky, and polyfuse are all wired and working. An earlier attempt on
  a different breadboard read ~0.14V even with the battery pack confirmed
  installed/powered and the Schottky reseated/correctly oriented; the
  fault was never pinned to one component — rebuilding the identical
  circuit on a second breadboard fixed it immediately. The divider ended
  up as 10 kΩ + 5.1 kΩ (not the originally-documented two 10 kΩ), kept as
  the standard going forward. See `power_supplies/psu_4xaa/README.md`
  § Validation/§ Troubleshooting and `README.md`'s bench-tested table.
- Unblocked `oscillators/ne555_astable`, which was waiting specifically
  on this PSU's bench-test — moved from "Blocked" to the top of "Ready to
  build now" in `TODO-arcticoder.md`.

## 2026-09-13

- **`oscillators/ne555_astable` — output divider fault fixed.** Isolated
  with `measurement_tools/resistance_measurement` (reconfigured to
  10kΩ reference / GP28, on its own breadboard, per instruction from the
  user to keep it off GP26 so `oscillation_probe`'s wiring doesn't need
  to move): R1 read ~10kΩ as expected, but R2 read ~273Ω — a mis-picked
  220Ω resistor (confirmed by color bands), not the intended 10kΩ.
  Swapped in a verified 10kΩ; `oscillation_probe` re-run shows swing no
  longer pinned at 3.300V (now ~2.2V) with the same crossing
  count/toggle-rate as both earlier readings. Removed from
  `TODO-arcticoder.md`'s "Open correctness issues" — see
  `oscillators/ne555_astable/README.md` § Validation for the full
  resolution.
- Also found and fixed a stale `R_REF` in
  `measurement_tools/resistance_measurement/main.py` — the working tree
  had `R_REF = 0.1` (an old ammeter-shunt value), which would have
  produced meaningless "Measured Resistance" numbers for anyone running
  it going forward. Corrected to `R_REF = 10000.0` to match the currently
  wired 10kΩ reference resistor.
- **NE555 batch — remaining 9 of 10 units validated PASS.** With the
  output-divider fault fixed (same day, above), swapped IC 2 through IC
  10 through the same `ne555_astable` socket/wiring and ran
  `oscillation_probe` on each (`breadboard3.jpg`): all 9 show swing
  ~2.2-2.25V and crossings in the low hundreds, matching IC 1's already-
  passed reading. **All 10 units in the batch are now validated** — see
  `oscillators/ne555_astable/README.md` § Validation for the per-unit
  table and `docs/inventory.md`'s NE555 row. Removed from
  `TODO-arcticoder.md`'s "Needs a validation step" section.
- **`signal_conditioning/transimpedance_amplifier/` (tier2 `TIA`) —
  designed, simulated, smoke-tested.** PT334-6C photodiode in zero-bias
  mode into an LM358 transimpedance stage (photodiode modeled as an ideal
  10µA current source, `Rf`=100kΩ from the on-hand kit, giving a 1.0V
  design-point output — confirmed by `ngspice -b`, current-source node
  order specifically verified by simulation to give the documented
  positive polarity). `smoke_test.py` checks virtual-ground behavior,
  headroom against `psu_low_v2`'s rail, and the Iph×Rf functional
  relationship — all green. `breadboard.md`, `README.md`, and a streaming
  `main.py` (mirrors `voltage_reference_lm358`'s style) also written. Not
  yet physically assembled — see `TODO-arcticoder.md`'s "Ready to build
  now" for that bullet (no current downstream urgency).
- **`measurement_tools/capacitance_bridge/` (tier3 `CAPBRIDGE`) —
  designed, simulated, smoke-tested.** RC charge-time capacitance meter
  (known `Rref`=100kΩ + unknown `Cx`, timed crossing of 63.2% of Vin)
  substituting for a classical 4-arm AC bridge, the same kind of
  substitution `resistance_measurement` already made for `OHMMETER`.
  Confirmed by `ngspice -b` (10µF nominal test point recovers ~9.997µF).
  `smoke_test.py` checks `Rref` dissipation and the derived-capacitance
  functional relationship — both green. `README.md` documents a "Range"
  table showing this technique targets the 1µF–470µF electrolytic kit,
  not the pF/nF ceramic assortment; `main.py` polls both a discharge and
  a charge phase (not a fixed sleep, so the largest kit values discharge
  fully before timing). Not yet physically assembled — see
  `TODO-arcticoder.md`'s "Ready to build now" for that bullet.
- **`OHMMETER` (tier3) — resolved as already satisfied, removed from the
  active list.** The user pointed out an ohmmeter (`resistance_measurement`)
  already exists and is in active use; re-checked
  `general_purpose_circuit_dependency.md` and found `OHMMETER`'s only
  consumer (tier4) is itself undesigned, so there's no concrete need for
  the originally-scoped 4-wire Kelvin precision upgrade right now. Removed
  the "New `OHMMETER` build" bullet from `TODO-arcticoder.md`'s "Ready to
  build now" (was previously listed there with no folder, which read as
  an open task) and replaced it with a short prose note explaining why
  it's intentionally absent, instead of silently deleting it.
- **`TODO-agent.md` created** — a new Claude-facing counterpart to
  `TODO-arcticoder.md`, tracking file/folder/netlist-creation work (not
  physical bench work) so it gets done proactively instead of surfacing
  as a "no folder exists yet" line item on the user's own list. Moved the
  5 remaining "parts on hand, no folder yet" items (`PHASED`, a `THERM`
  replacement, `ACTIVELIM`/`HVPULSE`, `EPFIELD`, `CHGAMP`) there from
  `TODO-arcticoder.md`'s "Ready to build now", each with enough of its
  current design/sourcing state written down for a future session to pick
  up without re-deriving it. See `docs/kb/todo_list_conventions.md` for
  the reasoning this split is based on.
