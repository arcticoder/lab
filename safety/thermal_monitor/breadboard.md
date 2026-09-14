# Breadboard Wiring — thermal_monitor

## Circuit overview

An MF52AT NTC thermistor in a resistor divider against a fixed 10kΩ
reference, read by the Pico ADC and converted to a temperature via the
thermistor's beta equation. A separate GPIO pin drives an LED when the
computed temperature crosses an alarm threshold — this is what makes the
circuit "Thermal Monitoring **with Alarm Threshold**," the safety `THERM`
node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md),
not just a bare thermometer.

**Equivalent to:** `thermal_monitor.spice`

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/).

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| MF52AT NTC thermistor | 10kΩ @ 25°C | 1 |
| Resistor | 10 kΩ (reference leg, `Rref`) | 1 |
| Resistor | 220 Ω (LED current limit) | 1 |
| LED | any color on hand | 1 |
| Dupont M-M jumper (red) | 12–20cm | 1 |
| Dupont M-M jumper (black) | 12–20cm | 1 |

---

## Wiring steps

### 1. Wire the divider

- `Rref` (10 kΩ): one leg to a Pico 3V3(OUT) pin, other leg to a fresh
  row — call this the MID row.
- MF52AT thermistor (no polarity — either lead either way): one leg to
  the MID row, other leg to GND.
- Jumper the MID row to a Pico ADC-capable GPIO (e.g. GP26).

### 2. Wire the alarm LED

- LED anode (longer lead) → a row.
- 220Ω resistor from that row to a GPIO pin used as a digital output
  (e.g. GP15).
- LED cathode (shorter lead, flat side of the case) → GND.

Keep the thermistor away from the LED and from anything else that gives
off heat on the same breadboard (a nearby lit LED, a warm regulator) —
it will happily read *that* heat source instead of ambient/whatever
you're actually trying to monitor.

---

## Expected behavior

At room temperature (~25°C), GP26 should read close to VCC/2 (~1.65V) —
see `README.md`'s simulated divider math, since the MF52AT's resistance
is nominally 10kΩ (matching `Rref`) right at 25°C. Warming the
thermistor (finger pinch, or briefly holding a soldering iron *near*,
not touching, it) should lower its resistance and shift the reading;
`main.py`'s beta-equation conversion turns that shift into an actual °C
figure. Crossing the alarm threshold in `main.py` should light the LED;
letting it cool back down should turn the LED back off.
