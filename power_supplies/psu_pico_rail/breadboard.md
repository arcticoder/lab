# Breadboard Wiring — psu_pico_rail

## Circuit overview

The Pico's onboard 3.3V regulator output, tapped directly as a rail for a
separate circuit on the same breadboard. No additional components — this
is two jumper wires, not a build.

**Equivalent to:** `psu_pico_rail.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| Raspberry Pi Pico | RP2040 | 1 |
| Micro USB cable | to PC or USB power adapter | 1 |
| Dupont M-M jumper (red) | 12–20cm | 1 |
| Dupont M-M jumper (black) | 12–20cm | 1 |

---

## Pico pin reference

| Pin | Function |
|-----|----------|
| Physical pin 36 | 3V3(OUT) — regulated 3.3V rail |
| Physical pin 38 | GND |

---

## Wiring steps

### 1. Power the Pico

Plug the Pico into the PC (or a USB power adapter) over USB. This is what
powers the onboard regulator — no separate battery needed.

### 2. Tap the rail

| From | To | Wire |
|------|----|------|
| Pico pin 36 (3V3 OUT) | Target circuit's positive rail | Red Dupont jumper |
| Pico pin 38 (GND) | Target circuit's ground rail | Black Dupont jumper |

---

## Expected behavior

With a light load (tens of mA), the rail holds close to 3.3V. See
[README.md](README.md) for the full simulate/validate workflow and the
~100 mA conservative current budget.
