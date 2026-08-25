# Breadboard Wiring — switch_pin_identifier

## Circuit overview

No PSU needed — the Pico is powered by the PC's USB port. Each of the
switch's pins gets its own probe wire straight to a GPIO configured with
the Pico's internal pull-up, so no external resistors are required.

**Equivalent to:** `switch_pin_identifier.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| Raspberry Pi Pico | RP2040 | 1 |
| Micro USB cable | data-capable, to PC | 1 |
| Dupont M-F jumper | 22cm | 1 per switch pin (2 or 3) |
| Switch under test | any 2- or 3-pin switch | 1 |

---

## Wiring steps

### 1. Plug the Pico into the PC

Micro USB cable, Pico to PC. This powers the Pico and gives you the serial
connection `main.py` prints to.

### 2. Wire the switch pins to the probes

| Switch pin | Pico pin | Wire |
|------------|----------|------|
| Terminal 1 | GP14 | Dupont M-F, female end on breadboard |
| Terminal 2 | GP15 | Dupont M-F, female end on breadboard |
| Terminal 3 (if present) | GP16 | Dupont M-F, female end on breadboard |

Order doesn't matter — the point is that every physical terminal lands on
its own probe pin. For a 2-pin switch, wire only GP14 and GP15 and ignore
GP16 in the output.

### 3. Run and actuate

Run `main.py` (`mpremote run main.py`). Move the switch through every
physical position, one at a time, and note which pin(s) print `0`
(connected to GND in that position) vs. `1` (floating).

---

## Expected behavior

See [README.md § Interpreting the result](README.md#interpreting-the-result-on-a-new-switch)
for how to turn the printed A/B/C states into "this is the active pin."
