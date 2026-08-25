# switch_pin_identifier

A Raspberry Pi Pico, probing all pins of an unmarked switch at once over
USB, so you can identify which pin does what without a multimeter.
Generalizes the diagnostic process worked out in
[docs/history.md](../../docs/history.md) (2026-08-22 21:41 onward) for one
of the `pico/` repo's slide switches — reusable for any 2- or 3-pin switch
in inventory, not just that one.

Works for switches with no printed C/NO/NC markings (common on cheap
slide/tactile switches): wire every terminal to its own probe pin with the
Pico's internal pull-up doing the work, then watch which pin(s) read LOW
as you actuate the switch through each position.

---

## Files

| File | Purpose |
|------|---------|
| `switch_pin_identifier.spice` | ngspice netlist — pull-up voltage at each pin, both switch positions |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step probing/wiring guide |
| `main.py` | MicroPython — reads GP14/GP15/GP16, prints pin states over USB serial |

---

## Build

Follow **[breadboard.md](breadboard.md)**. Short version:

1. Plug the Pico into the PC over USB (power + serial, nothing else needed).
2. Wire each of the switch's pins to its own probe pin (GP14, GP15, GP16 —
   leave GP16 unconnected for a 2-pin switch).
3. Run `main.py` and slide/press the switch through every position,
   watching which pin(s) toggle.

---

## Simulate

```bash
# from the repo root
ngspice -b measurement_tools/switch_pin_identifier/switch_pin_identifier.spice
```

Prints the pull-up voltage at each probe pin, showing what a floating pin
vs. a grounded pin looks like:

```
--- Pins A and C: always floating (pulled high) regardless of switch position ---
v(a) = 3.300000e+00
v(c) = 3.300000e+00
--- Pin B (active pin): position 1 (closed to GND) vs position 2 (floating) ---
v(b1) = 6.599868e-05
v(b2) = 3.300000e+00
```

---

## Expected behaviour

A floating pin (pulled up, not connected by the switch in the current
position) reads ~3.3V — `main.py` reports it as `1`. A pin the switch
connects to GND in the current position reads ~0V — `main.py` reports it
as `0`.

For the specific 3-pin "1P2T" slide switch already characterized (see
`pico/docs/inventory.md`, "Slide Switch" row): one outer pin never toggles
in either position (always `1`), and the active pin reads `0` in one
position and `1` in the other. That's the pin to wire into a real circuit;
the never-toggling pin is unused.

---

## Interpreting the result on a new switch

1. Run `main.py` and note the resting state (before touching the switch).
2. Move the switch through each of its positions, one at a time, and
   record which pin(s) change and to what value.
3. A pin that changes between `0` and `1` as you move the switch is an
   **active** pin for that position. A pin that never changes across every
   position is unused for on/off purposes — leave it disconnected in the
   real circuit.
4. For a simple on/off switch, wire the active pin to your circuit's input
   (with the Pico's `PULL_UP` reading, `0` = the switch's "on" position)
   and leave the rest unconnected.
