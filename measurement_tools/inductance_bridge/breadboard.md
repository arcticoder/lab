# Breadboard Wiring — inductance_bridge

## Circuit overview

The unknown inductor (`Lx`) and a known 10nF capacitor (`Cref`) sit in
parallel from one breadboard row (the "tank" row) to GND. A Pico PWM pin
drives a 50% square wave into that row through `Rs` (1kΩ). A 1N5817
diode and a small hold circuit (`Cd` + `Rd`) turn the tank row's
amplitude into a DC level on a second row (the "detector" row), which a
Pico ADC pin reads. `main.py` sweeps the PWM frequency and reports where
that level peaks — the tank's resonance — then solves for `Lx`.

**Equivalent to:** `inductance_bridge.spice`

Powered from the Pico's own GPIO drive — no separate PSU needed (`Rs`
limits the drive to 3.3mA into a shorted tank).

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| Resistor | 1 kΩ (`Rs`) | 1 |
| Resistor | 100 kΩ (`Rd`) | 1 |
| Capacitor | 10 nF (`Cref`) — kit ceramic, marked `103` | 1 |
| Capacitor | 10 nF (`Cd`) — kit ceramic, marked `103` | 1 |
| Diode | 1N5817 Schottky | 1 |
| Inductor under test (`Lx`) | any value from the color-ring assortment (1µH–1mH) | 1 |
| Dupont M-M jumper | 12–20cm | 3 |

Two 10nF capacitors are needed and they play different roles: `Cref`
sets the resonant frequency (its tolerance sets the accuracy of the
result), `Cd` only holds the detector level (any 10nF, tolerance
irrelevant). If either turns out to be the 100nF kit part (marked `104`)
by mistake, swap it before running — a 100nF `Cref` puts every
resonance below the sweep window.

---

## Wiring steps

### 1. Drive

- Pico GP14 (physical pin 19) → one leg of `Rs` (1kΩ).
- `Rs`'s other leg → a fresh breadboard row (call it the "tank" row).

### 2. Tank

All three of these share the tank row on one end and the GND rail on the
other:

- `Cref` (10nF): one lead in the tank row, other lead in the GND rail.
- `Lx` (color-ring inductor): one lead in the tank row, other lead in
  the GND rail. Either way round — it has no polarity.
- (nothing else goes on the tank row except the diode, next step)

### 3. Detector

- 1N5817 **anode** (the end *without* the band) → the tank row.
- 1N5817 **cathode** (the banded end) → a second fresh row (call it the
  "detector" row).
- `Cd` (10nF): one lead in the detector row, other lead in the GND rail.
- `Rd` (100kΩ): one lead in the detector row, other lead in the GND rail.

### 4. ADC probe and ground

- Jumper from the detector row to Pico GP26 (ADC0, physical pin 31).
- Jumper from a Pico GND pin to the GND rail the tank and detector
  parts share.

### 5. Run

```bash
mpremote run main.py
```

Each sweep takes a few seconds and prints one line. Swap `Lx` between
sweeps; there is nothing to reset.

---

## Expected behavior

With `Lx` seated, each sweep prints a resonance frequency, the detector
level at the peak (0.3V to 1.7V depending on the inductor), and the
resulting inductance with the nearest assortment value beside it. At the
100µH design point the peak lands near 159kHz.

| Printed | Meaning |
|---------|---------|
| `Lx≈` a value within ~±20% of an assortment value | Inductor matches its color bands |
| `No reading: level highest at the sweep edge` | No resonance in 40kHz–2MHz: `Lx` missing, open, or one lead not in the tank row |
| `No reading: no tank signal at all` | Level ~0V everywhere: `Lx` leads shorted together, the diode is in backwards, or GP14/GP26 not wired |
| `No reading: no distinct resonance peak` | Nearly flat sweep: `Rs` or the detector `Rd`/`Cd` value is wrong, or the tank row isn't connected to the diode |

Run it once with **no inductor** in the tank row first. That should print
the "sweep edge" message; if it prints a value instead, something other
than `Lx` is creating a resonance (a stray part in the tank row).
