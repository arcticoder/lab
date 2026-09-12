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
