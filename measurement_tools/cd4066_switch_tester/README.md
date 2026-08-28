# cd4066_switch_tester

A Raspberry Pi Pico, driving one CD4066B analog switch's control pin and
probing its output over USB, to confirm the switch actually passes signal
when closed and blocks it when open — before it's trusted in a later
design (tier9 `MUX`, tier4 `DEMOD` in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)).
Same "validate the part before trusting it downstream" philosophy as
[fuse_test_voltmeter](../fuse_test_voltmeter/), applied to an IC instead
of a passive component — 10 CD4066BCN chips were received 2026-08-24
(`pico/docs/inventory.md`), each with 4 independent switches, so there are
40 individual switches worth spot-checking, not just "the part."

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) — this
draws well under 1mA (just the two 10kΩ bias resistors), comfortably
within its ~100mA budget.

---

## Files

| File | Purpose |
|------|---------|
| `cd4066_switch_tester.spice` | ngspice netlist — I/O B voltage, switch closed vs. open |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step wiring guide |
| `main.py` | MicroPython — toggles the control pin, reads GP26, prints a PASS/FAIL verdict, and exits |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)**. Short version:

1. Power the CD4066B (VDD pin 14, VSS pin 6) from
   [psu_pico_rail](../../power_supplies/psu_pico_rail/).
2. Wire one switch's I/O A (pin 1) through a 10kΩ resistor to VDD, and its
   I/O B (pin 2) through a 10kΩ resistor to GND.
3. Wire that switch's control pin (pin 13) to Pico GP15.
4. Probe I/O B (pin 2) with Pico GP26 (ADC0).
5. Run `main.py` — it toggles the control pin for 5 closed/open cycles,
   prints each reading, then averages each state and prints a PASS/FAIL
   verdict before exiting.

---

## Simulate

```bash
# from the repo root
ngspice -b measurement_tools/cd4066_switch_tester/cd4066_switch_tester.spice
```

```
--- Switch CLOSED: I/O A vs I/O B (Pico ADC probe on I/O B) ---
v(ac) = 1.666337e+00
v(bc) = 1.633663e+00
--- Switch OPEN: I/O A vs I/O B (should read near 0, isolated) ---
v(ao) = 3.299967e+00
v(bo) = 3.299934e-05
```

---

## Expected behaviour

**Closed** (control HIGH): I/O B reads ~1.63V — signal passes through the
switch's on-resistance to the pull-down. **Open** (control LOW): I/O B
reads ~0V — the switch blocks, and the pull-down holds the node at ground.
`main.py` toggles the control pin for 5 closed/open cycles, printing each
reading, then averages each state and checks it against three thresholds
(mirroring `smoke_test.py`'s checks against the SPICE model):

- closed average > 1.0V
- open average < 0.1V
- (closed average − open average) > 0.5V

**Pass**: all three hold — reading clearly tracks the commanded state
(high when closed, near-zero when open). **Fail**: reading stays near 0V
regardless of control state (switch stuck open, or dead), stays high
regardless (stuck closed, or control pin not actually reaching the part),
or sits at some fixed in-between value that doesn't move much either way
(e.g. both averages a couple volts above ground with a delta of a few
tens of mV). `main.py` prints `RESULT: PASS` or `RESULT: FAIL` and exits
either way. Repeat for each of the 4 switches per chip by moving the I/O A
/ I/O B / control wires to that switch's pins (see
`lab/docs/parts_reference.md` for the full CD4066B pinout) — a chip can
have some switches good and others bad.

### Troubleshooting a "fixed in-between value" fail

If both states read close together (small delta) instead of near the
rails, check these in order — swapping the control wire, the VDD wire, or
the chip itself does **not** rule out any of the items below, since none
of those swaps touch them:

1. **VSS (pin 6) → GND continuity.** Confirm with a multimeter that pin 6
   is actually at the same potential as the Pico's own GND, not just that
   a wire is present.
2. **The two 10kΩ bias resistors and their breadboard rows.** Confirm
   each resistor leg is in the row `breadboard.md` says it should be, not
   an adjacent row.
3. **The GP26 probe wire.** Confirm it lands in I/O B's row (pin 2 for
   switch 1) and not a neighboring one.
4. **Power-rail continuity across the whole board.** Many breadboards
   split their power rails into independent left/right halves that look
   like one continuous rail but aren't electrically joined. If the VDD or
   GND jumper from `psu_pico_rail` lands on a different rail segment than
   the bias resistors or the VSS jumper, everything downstream floats
   regardless of how correct each individual wire looks in isolation.
   Check with a multimeter across the rail, not just by eye.
