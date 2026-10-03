# hall_amplifier

An SS49E/49E linear Hall-effect sensor and an LM358 difference amplifier with
a trimpot null: it turns a magnetic field at the sensor into a voltage the
Pico's ADC can read, centred at 0.94V, at about 9.2mV per gauss. This is
tier5 `HALLAMP` in
[spacetime_circuits_dependency.md](../../docs/spacetime_circuits_dependency.md);
the on-hand KY-003 module is a digital switch and can't stand in for it
(`docs/parts_reference.md`). The 15 sensors arrive from the 2026-10-02
orders.

**Status: designed and simulated 2026-10-02 (`smoke_test.py` green, 20
checks); not built, sensors on order.** The sensor numbers come from the
Honeywell SS39ET/SS49E/SS59ET datasheet (read 2026-10-02), which describes the
original part; the AliExpress "49E"/"SS49E" parts are clones and may differ.
`main.py` was compiled under MicroPython on the Pico; its logic was run
against mocks only.

---

## Files

| File | Purpose |
|------|---------|
| `hall_amplifier.spice` | ngspice netlist (static): sensor model with null offset, field and sensitivity as parameters; trimpot null; difference amplifier |
| `smoke_test.py` | Output/input-range safety, nulling across the datasheet's null spread, gain and sensitivity-extreme checks, resistor mismatch, then `main.py`'s logic against a mocked ADC |
| `main.py` | MicroPython: null guide, zero-field noise check, live field readout in gauss |
| `breadboard.md` | Wiring and failure table |

---

## Design

```
3V3 ──┬── SS49E pin 1 (VCC)               3V3 ─10k─10k─10k─[10kΩ trimpot]─10k─10k─10k─ GND
      │   SS49E pin 2 (GND)                                  wiper ──► LM358 B follower ── Vn
      │   SS49E pin 3 (OUT) ──10k──┬──► U1A (+)                                            │
      │                            └──100k── Vr (0.93V: 3V3 ─5.1k─┬─2k─ GND)               10k
      │                                                                                     │
      │                                      Vn ──10k──┬──► U1A (−) ◄── 100k from OUT ◄─────┘
      └──────────────────────────────────────────────  OUT ──► Pico GP26
          Vout = 0.93V + 10 × (Vhall − Vn)
```

| Choice | Value | Why |
|--------|-------|-----|
| Supply | Pico `3V3(OUT)` | The sensor is ratiometric (null = VCC/2, sensitivity ∝ VCC) and so is `Vn`, so supply movement cancels in the subtraction; a 3.3V rail also guarantees the output can't leave the ADC's range |
| Sensor | SS49E at 3.3V | Datasheet: 2.7–6.5V supply; at 3.3V the sensitivity is 0.66–1.16mV/G (typ 0.92) and the output spans 1.05–2.25V (min), so ±0.6V about 1.65V |
| Null | trimpot between 3 × 10kΩ and 3 × 10kΩ, buffered | The sensor's zero-field output varies ±5% of VCC between units (datasheet, ±0.165V at 3.3V). Times a gain of 10 that's ±1.65V, far more than the output can swing, so the trim is required. The ladder spans 1.41V to 1.89V |
| Gain | 10 (100kΩ/10kΩ) | Full scale at about ±90 gauss before the LM358's 0.02V–1.8V limits, 0.087 gauss per Pico ADC count (0.014 per ADS1115 count). For ±9 gauss at 100× the gain, swap the two 100kΩ for 1MΩ |
| Difference stage | not a non-inverting amplifier | The 10k/100k divider at the inputs keeps both input nodes near 1.58V; a non-inverting stage would put the sensor's 1.65–2.25V straight on the LM358's input, which tops out near 1.8V |
| Zero-field output | 0.93V, from a 5.1k/2k divider | Puts the output where the LM358 has room both ways: +0.87V up, −0.92V down |

Simulated numbers (sensor model from the datasheet at 3.3V):

| Quantity | Value |
|----------|-------|
| Zero-field output, nominal sensor, nulled | 0.939V |
| Slope | 9.25mV/G (nominal 0.924mV/G × 10) |
| ±50 gauss | ±0.4625V, symmetric |
| Sensitivity 1.0 / 1.75 mV/G at 5V | +50G reads +330mV / +578mV |
| Output at fields far beyond range (±5000 G) | clamps at 0.02V / 1.8V, never above 1.8V |
| Highest amplifier input node, ±50G, nulls from −0.25V to +0.2V (5V basis) | 1.78V (the limit is about 1.8V) |
| Trimpot wiper for −0.25V / 0 / +0.2V nulls (5V basis) | 0.15 / 0.50 / 0.78 of travel |
| Amplifier supply draw | 0.5mA (the sensor adds up to 10mA at 5V per its datasheet; less at 3.3V) |
| 5% resistor mismatch | zero level moves −67mV (the trim removes it), slope +4% |

## What this does not show

- **A sensor whose null is above ~1.8V can't be nulled.** The LM358 can't output more than about 1.8V, so its buffer can't make a `Vn` above that. The datasheet allows a null up to 1.815V at 3.3V (+0.25V on a 5V basis); the simulation nulls everything up to +0.2V and pins the +0.25V case as a documented limit. With 15 sensors, the answer is another sensor, and `main.py` says so. Two other trims were tried and dropped (see the netlist header).
- **The sensors are clones.** The listings (49E, SS49E, "OH49E/AH49E") are generic. Sensitivity, null and pin order are the Honeywell datasheet's. The first zero-field reading and a magnet test are what confirm them.
- **Which pole raises the output** is not stated in the datasheet text read; find out with a magnet. The amplifier doesn't care.
- **Absolute field.** `main.py` converts at the typical sensitivity: the true field is 20% smaller to 40% larger than shown. Calibrating needs a known field; an N35 disc magnet at a measured distance gives roughly 35 G at 15mm (6×3mm, estimated from the axial-field formula, magnet grade assumed), good to tens of percent.
- **Earth's field** (about 0.25–0.65 G) is 2–6mV at the output. The noise check (limit 3mV) and an orientation flip show whether it is visible; the datasheet doesn't promise it.
- **Noise and drift** were not simulated. The sensor's null drifts up to ±0.1%/°C of VCC·(null) per the datasheet, which is 1.6mV/°C at the sensor, 16mV/°C at the output: warm hands or a nearby hot part show up as field. Let the circuit settle and keep heat sources away.
- **Reversed supply.** The datasheet's absolute maximum supply is −5V to 8V, so swapping `VCC` and `GND` on the sensor is survivable; other mis-wirings (output onto a rail) are not covered.
