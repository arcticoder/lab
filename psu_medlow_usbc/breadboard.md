# Breadboard Wiring — psu_medlow_usbc

## Circuit overview

USB-C VBUS (5V, adapter-regulated) → 500 mA polyfuse → 100 nF bypass cap →
output.

**Equivalent to:** `psu_medlow_usbc.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| USB-C breadboard breakout board | passive VBUS/GND breakout | 1 |
| USB-C wall adapter | 5V, 2–3A | 1 |
| Polyfuse | Littelfuse RXEF050 (500 mA slow-blow) | 1 |
| Ceramic capacitor | 100nF | 1 |
| Dupont M-M jumper (red) | 16–20cm | 1 |
| Dupont M-M jumper (black) | 16–20cm | 1 |
| SYB170 breadboard | 170-pin, 300V, <5A | 1 |

---

## Wiring steps

### 1. Seat the USB-C breakout

Plug the breakout board into the breadboard so VBUS and GND land on
separate rows.

### 2. Place the polyfuse

Insert the polyfuse in series on the VBUS row, downstream of the breakout.

### 3. Place the bypass cap

| From | To |
|------|----|
| Polyfuse output | 100nF cap (+) |
| 100nF cap (−) | Ground rail |

### 4. Take the output

Output (+) is the polyfuse output / cap (+) node. Output (−) is the ground
rail, tied to USB GND.

---

## Expected behavior

With a 10 Ω test load across the output: ~4.76 V, ~476 mA — near the
polyfuse's 500 mA rating by design. See [README.md](README.md) for the full
simulate workflow.
