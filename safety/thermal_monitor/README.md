# thermal_monitor

An MF52AT NTC thermistor divider read by the Pico ADC and converted to a
temperature via its beta equation, with a GPIO-driven LED that lights
once the reading crosses an alarm threshold. This is the safety `THERM`
node ("Thermal Monitoring with Alarm Threshold") in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
— the alarm output is what distinguishes this from a bare thermometer,
matching the node's own label.

Fills the gap flagged in `docs/inventory.md`: the thermistor already in
the SunFounder Thales kit is marked "suspect faulty"; this circuit uses
the MF52AT batch instead (10 on hand, received 2026-09-12).

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/).

---

## Files

| File | Purpose |
|------|---------|
| `thermal_monitor.spice` | ngspice netlist — Rref/Rntc divider at the 25°C reference point + alarm-LED branch |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R/D elements |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — reads temperature continuously, drives the alarm LED |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Divider: 10kΩ `Rref` from Pico 3V3(OUT) to a MID node; MF52AT
   thermistor from MID to GND (no polarity). MID also goes to a Pico ADC
   pin (e.g. GP26).
2. Alarm LED: LED anode through a 220Ω resistor to a Pico GPIO output
   (e.g. GP15); LED cathode to GND.

---

## Simulate

```bash
# from the repo root
ngspice -b safety/thermal_monitor/thermal_monitor.spice
```

```
--- THERM: divider midpoint at 25C (should be VCC/2) vs alarm-LED node/current ---
v(2) = 1.650000e+00
v(4) = 2.025628e+00
i(vgpio) = -5.79260e-03
```

---

## Design notes

**Why Rref = 10kΩ specifically.** It matches the MF52AT's own R25
(nominal resistance at 25°C), so the divider centers at VCC/2 right at
room temperature — equal ADC headroom whether the real reading ends up
above or below that point, rather than skewing the usable range toward
one end.

**Temperature conversion.** `main.py` inverts the divider equation to
recover the thermistor's resistance from the ADC voltage (same technique
as `measurement_tools/resistance_measurement`), then applies the MF52AT's
beta equation (B=3950K, per `docs/parts_reference.md`) to convert
resistance to temperature. This is a first-order approximation (true
NTC behavior is better fit by the full Steinhart-Hart equation with three
coefficients) — adequate for an alarm-threshold safety monitor, not
claimed as calibration-grade.

**Alarm threshold.** `main.py` defaults to 40°C — chosen as a
plausible "something on this bench is running warmer than it should"
trip point (well above normal room temperature, well below anything
that would itself be a burn/fire hazard), not tied to any specific
downstream circuit's rated maximum. Adjust `ALARM_THRESHOLD_C` in
`main.py` once this monitor is actually placed against a specific
component with its own rated thermal limit.

**LED forward-voltage model.** The `.spice` LED model (`IS=1e-19 N=2
RS=5`) is a generic red-LED-like approximation, not measured against the
specific LED colors on hand (`docs/inventory.md` lists them with no part
number) — it lands in the datasheet-typical ~1.8-2.2V range at a few mA,
which is all this smoke test needs to confirm the current/power stay
safe. The exact current will vary a little by which LED color is
actually used.

---

## Validation

`main.py` streams voltage, resistance, and computed temperature
continuously, lighting GP15's LED once the alarm threshold is crossed:

```bash
mpremote run main.py
```

At room temperature, expect a reading near 25°C and the LED off. Warm
the thermistor (finger pinch, or hold a soldering iron *near*, not
touching, it) — the reported temperature should rise, and the LED
should light once it crosses `ALARM_THRESHOLD_C`. Letting it cool back
down should turn the LED back off. If the reading doesn't move at all,
check the thermistor is actually in the MID-to-GND leg (not shorted or
open) and that `Rref` is actually 10kΩ, not a different value pulled
from the wrong inventory bin — see `docs/inventory.md`'s 2026-09-13
bin-mixup caution for why that's worth double-checking rather than
assuming.
