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
| Resistor | 1 kΩ | 2 (+1 optional, see step 6) |
| Push Button | momentary, 4-pin | 1 (optional, see step 6) |
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

Run a jumper wire from the divider midpoint row (where R1 and R2 meet)
to the row holding LM358 pin 3 (non-inverting input).

A breadboard row is one electrically-bonded node, so if you deliberately
land one of R1/R2's legs *in the same row as pin 3* back in step 2
(instead of a fresh, separate row), they're already the same node and
this jumper is unnecessary. That's a planning choice made *during* step
2, though — it won't happen by coincidence, since the LM358's DIP-8 body
straddles the breadboard's center gap and each of its pins sits in its
own row, physically separate from wherever you happened to plug R1/R2.
When in doubt, just run the jumper.

### 4. Close the feedback loop

Wire LM358 pin 1 (output) to LM358 pin 2 (inverting input). This is what
makes it a unity-gain buffer instead of an open-loop comparator.

### 5. Take the output

Output is LM358 pin 1 (same node as the feedback wire).

### 6. Optional: add `R_load` for `main.py`'s validation check

Only needed if you're running `main.py`'s "validation without a
multimeter" check (see [README.md](README.md)) — skip this for the
circuit itself.

`R_load` is a **third** 1kΩ resistor, separate from R1 and R2 — don't
reuse either divider resistor for this, since removing R1 or R2 breaks
the divider instead of just testing the buffer under load.

Insert `R_load` with one leg in the LM358 pin 1 row and the other leg in
a GND rail row. `main.py` walks you through disconnecting/reconnecting
it while it takes ADC readings, waiting on a push button rather than a
keypress or a fixed countdown (see the README section above for why).
Wire the button: one leg to Pico GP15, the other leg to a GND rail row —
`main.py` uses GP15's internal pull-up, so no external resistor is
needed. Press it once you've finished moving `R_load` for that phase.

---

## Expected behavior

~1.65V at pin 1, holding steady even with a 1kΩ load attached — see
[README.md](README.md) for the bare-divider-vs-buffered comparison numbers.
