# Breadboard Wiring — transimpedance_amplifier

## Circuit overview

A PT334-6C photodiode (5mm, silicon PIN) in zero-bias/photovoltaic mode,
feeding one channel of an LM358 wired as a transimpedance amplifier: the
photodiode's cathode lands on the inverting input (virtual ground), a
feedback resistor sets the current-to-voltage gain, and the anode goes
straight to GND.

**Equivalent to:** `transimpedance_amplifier.spice`

Powered from [psu_low_v2](../../power_supplies/psu_low_v2/) — see
`README.md` for why this circuit's prerequisite is `psu_low_v2`, not
`psu_3xaa`.

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| LM358P | dual op-amp, DIP-8 | 1 |
| PT334-6C photodiode | 5mm, silicon PIN | 1 |
| Resistor | 100 kΩ (feedback, `Rf`) | 1 |
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

## PT334-6C pinout

Two leads, no polarity marking beyond lead length: the **longer lead is
the anode**, matching standard photodiode/LED convention (see
`lab/docs/parts_reference.md#pt334-6c-photodiode`) — confirm against the
physical part before wiring, since some photodiode packages reverse this
convention relative to LEDs.

---

## Wiring steps

### 1. Power the LM358

| From | To | Wire |
|------|----|------|
| [psu_low_v2](../../power_supplies/psu_low_v2/) output (+) | LM358 pin 8 (VCC) | Red Dupont jumper |
| psu_low_v2 output (−) | LM358 pin 4 (GND) | Black Dupont jumper |

### 2. Ground the non-inverting input

Wire LM358 pin 3 (non-inverting input) directly to the same GND rail as
pin 4. This sets the reference the feedback loop drives pin 2 toward.

### 3. Wire the photodiode

- PT334-6C **anode** (shorter lead) → GND rail (same rail as pin 4/pin 3).
- PT334-6C **cathode** (longer lead) → the row holding LM358 pin 2
  (inverting input).

### 4. Wire the feedback resistor

Insert `Rf` (100 kΩ) with one leg in the same row as LM358 pin 2 (and the
photodiode cathode) and the other leg in the row holding LM358 pin 1
(output).

### 5. Take the output

Output is LM358 pin 1 (same node as the `Rf` leg from step 4).

---

## Expected behavior

With the photodiode dark, the output should sit close to 0V (no
photocurrent, nothing for `Rf` to convert). Under ambient room light, the
output should read a positive voltage roughly proportional to incident
light — see [README.md](README.md) for the simulated 1.0V design point
and its illustrative-only photocurrent assumption. Covering the
photodiode with a finger should measurably drop the reading; pointing a
flashlight at it should raise it — that swing is the real-hardware
validation check (see `main.py`).
