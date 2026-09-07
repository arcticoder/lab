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
| Metal film resistor (for output validation, § 4) | 10 kΩ | 2 |
| Dupont M-M jumper | assorted | ~10 |

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

No resistor is needed between psu_4xaa's output and pin 8 — the NE555
draws only a few mA of quiescent supply current, and the 1kΩ Ra in the
timing network (§2) already limits the one current-carrying path that
actually needs limiting (the pin 7 discharge path, ~5.2mA at Vcc/(Ra+Ron)
— see `smoke_test.py`'s "discharge-pin sink current" check and the
netlist's header comment). Both are far under what psu_4xaa's 500mA
polyfuse or the Schottky can supply, so wiring VCC straight to psu_4xaa's
output (as in the table above) is correct as-is, if using [psu_4xaa's
optional power switch](../../power_supplies/psu_4xaa/breadboard.md) —
built here per its own breadboard.md — leave it ON before powering this
circuit up.

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

NE555 pin 3 (Output) is the square wave, swinging ~0V to ~VCC (~5.5V).
That's too high to wire straight onto any Pico pin — GP26/ADC0 (and every
other Pico GPIO) is limited to 0–3.3V (see `SCOPEPICO` in
`docs/general_purpose_circuit_dependency.md`). Bring it into range with
the same 2:1 resistor-divider approach used for
[psu_4xaa's own output validation](../../power_supplies/psu_4xaa/README.md#validation):

| From | To | Wire |
|------|----|------|
| NE555 pin 3 (Output) | 10 kΩ resistor #1 | Dupont M-M jumper |
| 10 kΩ resistor #1 / #2 junction | Pico GP26 (ADC0, Pin 31) | Dupont M-M jumper |
| 10 kΩ resistor #2 | GND rail | Dupont M-M jumper |
| psu_4xaa GND (−) / NE555 pin 1 | Pico GND (Pin 28) | Black Dupont jumper (shared ground reference — without this, GP26's reading is meaningless) |

**What this confirms today:** GP26 toggling between ~0V and ~2.75V (half
of pin 3's ~5.5V swing) proves this specific NE555 unit is actually
oscillating in astable mode — enough for this circuit's stated purpose
(first per-unit validation of the NE555 batch, see `README.md`).

**What this doesn't give you yet:** an actual frequency/duty-cycle
number. That needs either the tier2 `FREQC` frequency counter (not yet
designed/built — see `docs/TODO-arcticoder.md`)
or the `SCOPEPC` soundcard path, which itself still needs a
DC-blocking/attenuator buffer circuit that doesn't exist yet either (see
that node's own text in `docs/general_purpose_circuit_dependency.md`).
Turning the trimpot and watching GP26's toggling rate change qualitatively
is the only way to confirm the frequency *changes* until one of those two
gets built — treat a precise Hz reading as a real gap, not something this
divider quietly gives you.

### 5. Adjust the trimpot

Turning the 3296's adjustment screw sweeps Rb from ~0 to 10kΩ, sweeping
frequency and duty cycle together — see
[README.md § Expected behaviour](README.md#expected-behaviour) for the
usable range and what happens at the extremes.
