# Breadboard Wiring — phase_detector

## Circuit overview

One XOR gate of an SN74HC86N compares two square waves — the existing
`ne555_astable` oscillator's output-divider tap, and a Pico GPIO
configured as a PWM reference — and an RC lowpass filter turns the XOR's
duty-cycle-proportional-to-phase output into a slowly-varying DC voltage
the Pico ADC can read.

**Equivalent to:** `phase_detector.spice`

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) — same
rail that generates the PWM reference and reads the filtered output, so
everything shares one common ground and one logic-level standard.

**Requires `oscillators/ne555_astable` already built and wired** — this
circuit taps its existing output divider (see `ne555_astable/breadboard.md`
§ 4), it doesn't add a second NE555.

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| SN74HC86N | quad 2-input XOR gate, DIP-14 | 1 |
| Resistor | 10 kΩ (lowpass, `Rf`) | 1 |
| Ceramic capacitor | 100 nF (lowpass, `Cf`; EIA code `104`) | 1 |
| Dupont M-M jumper (red) | 12–20cm | 1 |
| Dupont M-M jumper (black) | 12–20cm | 2 |
| Dupont M-M jumper (any color) | 12–20cm | 2 |

---

## SN74HC86N pinout (DIP-14, per `lab/docs/parts_reference.md`)

Only gate 1 (pins 1, 2, 3) is used.

| Pin | Function | Pin | Function |
|-----|----------|-----|----------|
| 1 | 1A (input) | 14 | VCC |
| 2 | 1B (input) | 7 | GND |
| 3 | 1Y (output) | — | (gates 2-4 unused, leave unconnected) |

---

## Wiring steps

### 1. Power the gate

| From | To | Wire |
|------|----|------|
| Pico 3V3(OUT) pin | SN74HC86N pin 14 (VCC) | Red Dupont jumper |
| Pico GND pin | SN74HC86N pin 7 (GND) | Black Dupont jumper |

Also tie this same GND to `ne555_astable`'s own GND if it's on a separate
breadboard — the tapped signal in step 2 is only meaningful referenced to
a common ground.

### 2. Wire input 1A — the NE555 tap

Jumper `ne555_astable`'s existing output-divider tap (the node already
feeding its own GP26, per that circuit's `breadboard.md` § 4) to
SN74HC86N pin 1 (1A). This is a tap, not a new connection into the
NE555 circuit itself — don't disconnect `ne555_astable`'s own GP26
jumper to do this; the tap node can feed both.

**Voltage margin caveat:** this tap's "high" level is only ~2.2-2.9V
(the batch varies per unit — see `ne555_astable/README.md`'s Validation
table), not a full 3.3V. A 74HC-series gate at 3.3V VCC typically needs
≥~2.31V to reliably register a logic HIGH (roughly 0.7×VCC). Most units
in the batch clear this with some margin, but a unit reading close to
~2.2V is close enough to the threshold that it's worth confirming the
gate actually switches (see Validation below) rather than assuming it
does.

### 3. Wire input 1B — the Pico PWM reference

Configure a spare Pico GPIO as a PWM output (see `main.py`) at a
frequency near the NE555's own tuned frequency (~1.5kHz, per the
validated batch). Jumper that GPIO directly to SN74HC86N pin 2 (1B) — no
extra components needed, since this is already a clean 0-3.3V digital
signal.

### 4. Wire the output lowpass filter

- `Rf` (10 kΩ): one leg to SN74HC86N pin 3 (1Y), other leg to a fresh
  row — call this the OUT row.
- `Cf` (100 nF): one leg to the OUT row, other leg to GND.
- Jumper the OUT row to a Pico ADC-capable GPIO (e.g. GP28 — the Pico
  only has three ADC-capable pins total, GP26/27/28, already reused
  across several other circuits in this repo including
  `charge_amplifier`'s own default; fine since each circuit here is
  built and tested one at a time, not all wired simultaneously).

---

## Expected behavior

Because the NE555 and the Pico's PWM are two independent, non-phase-
locked oscillators, their relative phase continuously drifts — see
`README.md`'s Design notes for why this is the expected, useful
behavior, not a fault. The filtered output (GP28) should slowly sweep
between roughly 0V and 3.3V as the two clocks drift in and out of phase,
rather than settling at one fixed voltage. See `README.md`'s Validation
section for what to check if it doesn't.
