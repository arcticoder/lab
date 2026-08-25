# Breadboard Wiring — voltage_reference_lm358

## Circuit overview

A 1kΩ/1kΩ divider off the [psu_pico_rail](../../power_supplies/psu_pico_rail/)
3.3V rail, buffered by one LM358 channel wired as a unity-gain follower.

**Equivalent to:** `voltage_reference_lm358.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| LM358P | dual op-amp, DIP-8 | 1 |
| Resistor | 1 kΩ | 2 |
| Dupont M-M jumper (red) | 12–20cm | 2 |
| Dupont M-M jumper (black) | 12–20cm | 2 |

---

## LM358 pinout (DIP-8, per `lab/docs/parts_reference.md`)

| Pin | Function | Pin | Function |
|-----|----------|-----|----------|
| 1 | Output 1 | 8 | VCC |
| 2 | Inverting input 1 (−) | 7 | Output 2 (unused) |
| 3 | Non-inverting input 1 (+) | 6 | Inverting input 2 (unused) |
| 4 | VEE / GND | 5 | Non-inverting input 2 (unused) |

Only channel 1 (pins 1–3) is used; leave channel 2 (pins 5–7) unconnected.

---

## Wiring steps

### 1. Power the LM358

| From | To | Wire |
|------|----|------|
| [psu_pico_rail](../../power_supplies/psu_pico_rail/) 3V3 | LM358 pin 8 (VCC) | Red Dupont jumper |
| psu_pico_rail GND | LM358 pin 4 (GND) | Black Dupont jumper |

### 2. Build the divider

- Insert R1 (1kΩ) from the VCC rail to a fresh breadboard row (the
  divider midpoint).
- Insert R2 (1kΩ) from that same row to the GND rail.

### 3. Feed the divider into the buffer

Wire the divider midpoint (between R1 and R2) to LM358 pin 3
(non-inverting input) — same breadboard row, no extra wire needed if
they're already in the same row.

### 4. Close the feedback loop

Wire LM358 pin 1 (output) to LM358 pin 2 (inverting input). This is what
makes it a unity-gain buffer instead of an open-loop comparator.

### 5. Take the output

Output is LM358 pin 1 (same node as the feedback wire).

---

## Expected behavior

~1.65V at pin 1, holding steady even with a 1kΩ load attached — see
[README.md](README.md) for the bare-divider-vs-buffered comparison numbers.
