# Breadboard Wiring — ne555_astable

## Circuit overview

VCC --Ra(1kΩ)--> pin 7 (discharge) --Rb(3296 trimpot, 0-10kΩ)--> pins 2+6
(trigger+threshold, tied together) --C(100nF)--> GND. Pin 3 is the square-
wave output.

**Equivalent to:** `ne555_astable.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| NE555 timer IC | DIP-8 | 1 |
| Resistor | 1 kΩ | 1 |
| 3296 trimming potentiometer | 10 kΩ | 1 |
| Ceramic capacitor | 100 nF | 1 |
| Ceramic capacitor | 10 nF | 1 |
| 4x AA battery holders + cells (from [psu_4xaa](../../power_supplies/psu_4xaa/)) | 6.0V raw | 1 |
| Dupont M-M jumper | assorted | ~8 |

---

## NE555 pinout (DIP-8, per `lab/docs/parts_reference.md`)

| Pin | Function | Pin | Function |
|---|---|---|---|
| 1 | GND | 8 | VCC |
| 2 | Trigger | 7 | Discharge |
| 3 | Output | 6 | Threshold |
| 4 | Reset | 5 | Control Voltage |

Pin 1 is the corner nearest the notch/dot at the end of the DIP-8 package.

---

## Wiring steps

### 1. Power the chip

Build [psu_4xaa](../../power_supplies/psu_4xaa/) first if you haven't
already (4x AA in series + 1N5817 Schottky + 500mA polyfuse, 6.0V raw).
This is the AA-battery tier — the NE555 needs ≥4.5V, and psu_3xaa's 4.5V
sags to ~4.02V under load (below that minimum, per its own smoke test),
so psu_4xaa is the first AA tier that actually clears it, with margin.
If it ever proves insufficient on the real bench, the next step up is a
12V supply (not yet its own folder — see `docs/parts_reference.md`
`psu_medlow` node), not another AA tier.

| From | To | Wire |
|------|----|------|
| psu_4xaa output (+) | NE555 pin 8 (VCC) | Red Dupont jumper |
| psu_4xaa output (+) | NE555 pin 4 (Reset) | Red Dupont jumper (keeps the chip enabled) |
| psu_4xaa GND (−) | NE555 pin 1 (GND) | Black Dupont jumper |

### 2. Wire the timing network

- 1kΩ resistor from NE555 pin 8 (VCC) to pin 7 (Discharge) — this is Ra.
- 3296 trimpot as Rb, wired as a glitch-safe 2-terminal rheostat: one
  outer pin to NE555 pin 7 (Discharge), and the wiper (middle pin) *and*
  the other outer pin both tied together to a shared breadboard row —
  that row then goes to pins 2+6 below. Tying the wiper to the unused
  outer pin means a momentary loss of wiper contact (common on cermet
  trimmers) can't open-circuit Rb — current still has a path through the
  full resistive track.
- Jumper from that shared Rb row to NE555 pin 2 (Trigger) *and* pin 6
  (Threshold) — both pins land in the same breadboard row.
- 100nF capacitor from that pin 2/6 row to GND rail. This is the timing
  capacitor C.

### 3. Wire the control-voltage decoupling cap

- 10nF capacitor from NE555 pin 5 (Control Voltage) to GND rail. Purely a
  noise-decoupling cap on the unused CV pin — does not affect timing.

### 4. Take the output

- NE555 pin 3 (Output) is the square wave. Probe it with a multimeter (DC
  average will read roughly `duty% x Vcc`), a Pico ADC pin, or — since the
  design targets the audio band — the desktop PC's onboard soundcard
  line-in via a DC-blocking/attenuator buffer (see `SCOPEPC` in
  `docs/general_purpose_circuit_dependency.md`) for an actual waveform and
  frequency reading.

### 5. Adjust the trimpot

Turning the 3296's adjustment screw sweeps Rb from ~0 to 10kΩ, sweeping
frequency and duty cycle together — see
[README.md § Expected behaviour](README.md#expected-behaviour) for the
usable range and what happens at the extremes.
