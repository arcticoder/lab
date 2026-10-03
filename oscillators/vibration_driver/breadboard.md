# Breadboard Wiring — vibration_driver

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| Vibration motor, 3V coin type, 10mm (the 2026-10-02 order, `docs/orders.md`) | 1 | **on order**, not yet received |
| S8050 NPN transistor (TO-92) | 1 | yes (2) |
| 1N5817 Schottky diode | 1 | yes (18 untested) |
| 1kΩ resistor | 1 | yes |
| 10kΩ resistor | 1 | yes |
| Jumper wires | 4 | yes |

S8050 TO-92 pinout, flat face toward you, legs down: **E, B, C** left to right.

## Wiring steps

| From | To |
|------|----|
| Pico `3V3(OUT)` (pin 36) — or a `psu_low_v2` + rail, grounds shared | Motor lead 1, and the diode's cathode (stripe end) |
| Motor lead 2 | S8050 collector, and the diode's anode |
| S8050 emitter | Pico GND (pin 38) |
| Pico GP16 (pin 21) | 1kΩ → S8050 base |
| S8050 base | 10kΩ → GND |

Check the diode before powering. Its stripe marks the cathode and must sit on
the 3V3 side. A stripe worn off a reused 1N5817 can't be trusted (see
`docs/kb/bench_photo_diagnostics_notes.md`); confirm the orientation with the
forward-drop check in `power_supplies/psu_low_v2/README.md` § Validation.

## Run

```bash
mpremote run main.py
```

## Expected behavior

```
GP16: 0% duty
GP16: 10% duty
...
GP16: 100% duty
Holding 100%. Ctrl-C to stop.
```

The motor stays still at the low steps, starts to buzz around 40–60%, and is
steady at 100%. The S8050 stays barely warm (about 13mW). Two leads: red is the
plus side (to 3V3 / the diode's stripe side), blue or black the minus side
(to the collector); a motor wired backwards just spins the other way.

| Symptom | Likely cause |
|---------|--------------|
| Motor never moves, S8050 or Pico warm | Diode reversed. Unplug USB at once |
| Motor never moves, nothing warm | Motor leads not on the collector, or base wire not on GP16 |
| Motor buzzes at 0% duty or at power-up | Base pull-down missing (floating base), or base wire touching 3V3 |
| Pico resets when the motor starts | Motor start-up current dipping the 3V3 rail; add a 100µF capacitor across the motor and 3V3 (an electrolytic from the 16V/25V kit: the long lead on 3V3) |
| Pico or S8050 warms up, motor not turning | Rotor held or jammed: a stalled motor draws about 126mA. Stop the script |
