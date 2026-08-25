# Breadboard Wiring — switch_pin_identifier

## Circuit overview

No PSU needed — the Pico is powered by the PC's USB port. One switch
terminal is wired directly to a Pico GND pin (the reference point); the
remaining terminal(s) each get their own probe wire to a GPIO configured
with the Pico's internal pull-up, so no external resistors are required.

**This GND wire is required** — without it, no probe pin has any path to
ground, so closing the switch just shorts two already-pulled-up GPIOs
together and both keep reading HIGH regardless of switch position. See
[Troubleshooting](#troubleshooting) if you're seeing exactly that.

**Equivalent to:** `switch_pin_identifier.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| Raspberry Pi Pico | RP2040 | 1 |
| Micro USB cable | data-capable, to PC | 1 |
| Dupont M-M jumper | 22cm | 1 per switch terminal (2 or 3) |
| Switch under test | any 2- or 3-pin switch | 1 |

The Pico sits mounted directly on the breadboard (straddling the center
gap, per the Sunfounder kit / Wokwi convention), so its pins are already
in breadboard holes — an M-M jumper runs from that same column to
wherever else on the board it needs to go. There's no separate female
receptacle to plug into, so M-F jumpers aren't needed here; a bent solid-
core wire works just as well as an M-M jumper if that's what's on hand.

---

## Wiring steps

Wire everything first; plug the Pico into the PC last. Powering it up
mid-wiring risks a brief short between pins while a jumper is half-seated,
and there's no reason to have the rail live before the circuit is
complete.

### 1. Wire the switch terminals to GND and the probes

| Switch terminal | Pico pin | Wire |
|------------------|----------|------|
| Terminal 1 (reference) | GND — physical pin 18 (closest GND to GP14/GP15) | Dupont M-M |
| Terminal 2 | GP14 — physical pin 19 | Dupont M-M |
| Terminal 3 (if present) | GP15 — physical pin 20 | Dupont M-M |

Physical pins 18/19/20 sit next to each other on the same side of the
Pico, so this keeps every wire short. It doesn't matter *which* terminal
you pick as the GND reference — see
[Troubleshooting](#troubleshooting) if the one you picked turns out not
to be on the switch's current-carrying path.

For a 2-pin switch, wire only Terminal 1 (GND) and Terminal 2 (GP14);
there's no GP15 probe needed.

### 2. Plug the Pico into the PC

Micro USB cable, Pico to PC. This powers the Pico and gives you the
serial connection `main.py` prints to.

### 3. Run and actuate

Run `main.py` (`mpremote run main.py`). Move the switch through every
physical position, one at a time, and note which probe pin(s) print `0`
(connected to GND in that position) vs. `1` (floating).

---

## Expected behavior

See [README.md § Interpreting the result](README.md#interpreting-the-result-on-a-new-switch)
for how to turn the printed A/B states into "this is the active pin."

---

## Troubleshooting

**Every reading is `1`, on every switch position, and never changes:**
the terminal wired to Pico GND isn't part of this switch's
current-carrying path in either position — most likely because it isn't
wired to GND at all (double-check the wire actually lands on a GND pin,
not another GPIO), or because the terminal you picked as the reference
happens to be electrically isolated from the other two on this particular
switch. Confirm the GND wire first, then, if it's genuinely on a GND pin,
move it to a different terminal and re-run — one of the three pairings
will land on the switch's actual conduction path.
