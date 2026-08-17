# Breadboard Wiring — psu_ultralow_v1

## Circuit overview

Single AA cell → 50 mA polyfuse → output. No regulation, no adjustability —
a battery interface with resettable overcurrent protection.

**Equivalent to:** `psu_ultralow_v1.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| AA battery holder | single-cell, 5mm terminal | 1 |
| AA alkaline battery | 1.5V | 1 |
| Polyfuse | Littelfuse RXEF005 (50 mA slow-blow) | 1 |
| Dupont M-M jumper (red) | 16–20cm | 1 |
| Dupont M-M jumper (black) | 16–20cm | 1 |
| SYB170 breadboard | 170-pin, 300V, <5A | 1 |

---

## Wiring steps

### 1. Place the polyfuse

Insert the polyfuse across two breadboard columns so each leg sits in its
own node — one leg becomes the battery-side node, the other becomes the
output node.

### 2. Connect the battery

| From | To | Wire |
|------|----|------|
| Battery holder (+) | Polyfuse leg 1 | Red Dupont jumper |
| Battery holder (−) | Ground rail | Black Dupont jumper |

### 3. Take the output

Output (+) is the polyfuse's far leg (leg 2). Output (−) is the ground
rail, tied to the battery negative.

---

## Expected behavior

With a 15 Ω test load across the output: ~1.44 V, ~96 mA. See
[README.md](README.md) for the full simulate/validate workflow.
