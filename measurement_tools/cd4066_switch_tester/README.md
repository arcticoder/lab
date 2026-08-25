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
| `main.py` | MicroPython — toggles the control pin, reads GP26, prints pass/block state |
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
5. Run `main.py` and watch it toggle the control pin and print the
   resulting voltage.

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
`main.py` toggles the control pin every second and prints both states, so
a working switch shows the reading alternate between roughly 1.6V and 0V
in step with the printed `control=` state.

**Pass**: reading clearly tracks the commanded state (high when closed,
near-zero when open). **Fail**: reading stays near 0V regardless of
control state (switch stuck open, or dead), stays high regardless (stuck
closed, or control pin not actually reaching the part), or sits at some
fixed in-between value that doesn't move (control pin not connected).
Repeat for each of the 4 switches per chip by moving the I/O A / I/O B /
control wires to that switch's pins (see `lab/docs/parts_reference.md`
for the full CD4066B pinout) — a chip can have some switches good and
others bad.
