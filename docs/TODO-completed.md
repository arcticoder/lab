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
