# switch_pin_identifier

A Raspberry Pi Pico, probing an unmarked switch's terminals over USB, so
you can identify which terminal does what without a multimeter. Reusable
for any 2- or 3-pin switch in inventory.

Works for switches with no printed C/NO/NC markings (common on cheap
slide/tactile switches): one terminal is wired directly to the Pico's own
GND pin (the reference point), the remaining 1–2 terminals each get their
own probe pin with the Pico's internal pull-up doing the work, and you
watch which probe pin(s) read LOW as you actuate the switch through each
position — LOW means that terminal is connected to the grounded terminal
in the current position.

A probe pin can only ever read LOW if the switch's path actually includes
the terminal wired to GND. If none of the probe pins ever read LOW across
every position, the terminal picked as "GND" isn't in the switch's
current-carrying path for this arrangement — move the GND wire to a
different terminal and try again (see
[breadboard.md § Troubleshooting](breadboard.md#troubleshooting)).

---

## Files

| File | Purpose |
|------|---------|
| `switch_pin_identifier.spice` | ngspice netlist — pull-up voltage at each probe pin, both switch positions |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step probing/wiring guide |
| `main.py` | MicroPython — reads GP14/GP15, prints pin states over USB serial |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)**. Short version:

1. Wire one switch terminal to the Pico's GND pin, and the remaining 1–2
   terminals to their own probe pin (GP14, and GP15 for a 3-pin switch).
2. Plug the Pico into the PC over USB (power + serial) once the wiring is
   in place.
3. Run `main.py` and slide/press the switch through every position,
   watching which probe pin(s) read LOW.

---

## Simulate

```bash
# from the repo root
ngspice -b measurement_tools/switch_pin_identifier/switch_pin_identifier.spice
```

Prints the pull-up voltage at each probe pin, showing what a floating pin
vs. a grounded pin looks like:

```
--- Pin A: floating (pulled high) in this switch's positions ---
v(a) = 3.300000e+00
--- Pin B (active pin): position 1 (closed to grounded terminal) vs position 2 (floating) ---
v(b1) = 6.599868e-05
v(b2) = 3.300000e+00
```

---

## Expected behaviour

A floating probe pin (not connected by the switch, in the current
position, to the terminal wired to GND) reads ~3.3V — `main.py` reports it
as `1`. A probe pin the switch connects to the grounded terminal in the
current position reads ~0V — `main.py` reports it as `0`.

`pico/docs/inventory.md`'s "Slide Switch" row describes the specific 3-pin
"1P2T" slide switch in inventory as having one floating outer pin and one
active pin — but that characterization came from an earlier ad hoc probe
that, like this circuit's first draft, may not have had a solid GND
reference wired in. Treat it as a hypothesis to reconfirm with this
corrected circuit (GND wire actually in place) rather than a given, and
update that inventory row if re-testing turns up different pin roles.

---

## Interpreting the result on a new switch

1. Wire one terminal to GND and run `main.py`; note the resting state
   (before touching the switch).
2. Move the switch through each of its positions, one at a time, and
   record which probe pin(s) change and to what value.
3. A pin that changes between `0` and `1` as you move the switch is an
   **active** pin for that position, and its `0` reading confirms
   continuity to the terminal wired to GND. A pin that never changes
   across every position never connects to that grounded terminal on this
   switch — either it's unused, or it's the switch's true common/other
   throw, only distinguishable by re-wiring GND to a different terminal
   and re-running (see the troubleshooting note in `breadboard.md` if
   *no* pin ever reads `0`).
4. For a simple on/off switch, wire the active pin to your circuit's input
   (with the Pico's `PULL_UP` reading, `0` = the switch's "on" position)
   and leave the rest unconnected.
