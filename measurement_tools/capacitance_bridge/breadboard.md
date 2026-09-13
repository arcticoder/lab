# Breadboard Wiring — capacitance_bridge

## Circuit overview

A known reference resistor (`Rref`) in series with an unknown capacitor
(`Cx`), driven by a Pico GPIO output pin and read by a Pico ADC pin. The
GPIO drives the junction HIGH to charge `Cx` through `Rref`; timing how
long the ADC takes to cross 63.2% of the drive voltage (one RC time
constant) gives `Cx = t / Rref` directly.

**Equivalent to:** `capacitance_bridge.spice`

Powered from the Pico's own 3V3 rail / GPIO drive — no separate PSU
needed (same reasoning as
[resistance_measurement](../resistance_measurement/), which this circuit
is the capacitive counterpart to).

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| Resistor | 100 kΩ (`Rref`) | 1 |
| Capacitor under test (`Cx`) | any value from the aluminum electrolytic kit (1µF–470µF) — see "Range" in [README.md](README.md) | 1 |
| Dupont M-M jumper | 12–20cm | 3 |

---

## Wiring steps

### 1. Wire the divider

- Pico GP14 → one leg of `Rref` (100 kΩ).
- `Rref`'s other leg → a fresh breadboard row (call it the "junction"
  row).
- `Cx`'s **positive** lead → the same junction row.

  `Cx` from the aluminum electrolytic kit is **polarized** — long lead =
  positive, can body has a stripe on the negative side (see
  `docs/parts_reference.md#aluminum-electrolytic-capacitor-kit-1665025050v`).
  Getting this backwards doesn't just give a wrong reading; it can damage
  the part.

- `Cx`'s negative lead → GND rail.

### 2. Wire the ADC probe

Run a jumper from the junction row (where `Rref` and `Cx` meet) to Pico
GP26 (ADC0).

### 3. Power/ground

Wire a Pico GND pin to the GND rail `Cx`'s negative lead is already in.

---

## Expected behavior

With `Cx` fully discharged and GP14 driven HIGH, GP26's reading should
climb from 0V toward 3.3V along the standard RC charging curve, crossing
~2.09V (63.2% of 3.3V) at `t = Rref × Cx` seconds after GP14 goes high.
See [README.md](README.md) for the simulated numbers on a 10µF test
point, and `main.py` for how the real hardware measurement (including the
discharge step between readings) works.
