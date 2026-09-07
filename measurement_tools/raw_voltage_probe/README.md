# raw_voltage_probe

A Pico ADC reader that prints the averaged raw voltage at GP26 — no
resistance math, no divider assumptions, no trip/reset logic. Whatever
external divider or node is clipped to GP26/GND at the time, this just
reports what the Pico's ADC0 actually sees, oversampled and averaged to
cut down noise. It has no PASS/FAIL of its own: the calling circuit's own
README supplies the target voltage for whichever probe point is currently
wired.

This is deliberately the simplest of the three Pico-ADC instruments in
`measurement_tools/`:

- **`raw_voltage_probe`** (this folder) — prints voltage only, no divider
  math. Use it when you just need to know what a node reads, and you (or
  the calling circuit's README) already know what to compare it against.
- [`resistance_measurement`](../resistance_measurement/) — same
  oversampled-average technique, but drives a known `R_ref` divider and
  solves for an unknown `R_x` (a component's resistance, or continuity
  between two nodes).
- [`fuse_test_voltmeter`](../fuse_test_voltmeter/) — adds trip/reset
  detection logic on top of a voltage read, specific to polyfuse testing.

Split out 2026-09-07 from `power_supplies/psu_4xaa/gp26_raw_voltage.py`,
where it originated — that circuit's Validation and Troubleshooting
sections both just needed a plain voltage readout at GP26 with nothing
circuit-specific baked into the script, so it's reusable by any future
circuit that needs the same thing rather than every circuit growing its
own copy.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — averages 50 ADC samples per reading, 20 readings, prints each and the overall average |

No `.spice`/`smoke_test.py`/`breadboard.md` here — this isn't a circuit
with a fixed design of its own, it's a probe that clips onto whatever
circuit is under test. Wiring (which node goes to GP26, which to GND, and
what divider if any sits in front of GP26 to keep it under 3.3V) is the
calling circuit's responsibility and lives in that circuit's own
`README.md`/`breadboard.md`.

---

## Usage

```bash
mpremote run main.py
```

Prints 20 readings (200 ms apart) and their average:

```
[1/20] GP26 raw voltage: 2.751 V
...
[20/20] GP26 raw voltage: 2.749 V
Average over 20 readings: 2.750 V
```

**Before wiring anything to GP26**, make sure the node being probed is
already safely under 3.3V — through a resistor divider sized for the
source rail if it isn't. GP26, like every RP2040 GPIO, is not tolerant of
more than 3.3V.

---

## Current users

- [`power_supplies/psu_4xaa`](../../power_supplies/psu_4xaa/) — §
  Validation (PSU output divider) and § Troubleshooting (battery-direct
  divider, reversed-polarity check).
