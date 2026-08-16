# Breadboard Wiring — psu_low_v2

## Circuit overview

Two AA cells in series → Schottky (reverse-polarity protection) → 500 mA
polyfuse → output.

**Equivalent to:** `psu_low_v2.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| AA battery holder | single-cell, 5mm terminal | 2 |
| AA alkaline battery | 1.5V | 2 |
| Schottky diode | 1N5817 (1A, 20V) | 1 |
| Polyfuse | Littelfuse RXEF050 (500 mA slow-blow) | 1 |
| Dupont M-M jumper (red) | 16–20cm | 1 |
| Dupont M-M jumper (black) | 16–20cm | 1 |
| SYB170 breadboard | 170-pin, 300V, <5A | 1 |

---

## Wiring steps

### 1. Series the two AA holders

| From | To | Wire |
|------|----|------|
| Holder 1 (−) | Holder 2 (+) | Solder or short jumper |

### 2. Place the Schottky and polyfuse

Insert the Schottky (cathode stripe toward the fuse) and polyfuse in series
on the positive rail, downstream of holder 2.

### 3. Connect the battery pair

| From | To | Wire |
|------|----|------|
| Holder 1 (+) | Schottky anode | Red Dupont jumper |
| Holder 2 (−) | Ground rail | Black Dupont jumper |

### 4. Take the output

Output (+) is the polyfuse's far leg. Output (−) is the ground rail, tied
to holder 2 negative.

---

## Expected behavior

With a 10 Ω test load across the output: ~2.53 V, ~253 mA. See
[README.md](README.md) for the full simulate/validate workflow.
