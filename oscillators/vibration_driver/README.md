# vibration_driver

An S8050 low-side switch with a 1N5817 flyback diode that lets one Pico PWM
pin run a 3V vibration motor. It is the actuator stage the tier1 `SIMPGEN`
stand-in (`pico/leds/gpio_pwm_led/`) was missing: a GPIO pin can't source a
motor's current, and no motor or speaker is on hand (inventory checked
2026-09-23). It is also the driver `RIPPLETANK`'s wave dipper needs
(see `docs/TODO-arcticoder.md`).

**Status: designed and simulated 2026-10-01 (`smoke_test.py` green); not built.
The motor is not on hand** — it is one of the parts in `docs/orders.md`'s
"Decided, not yet ordered". The `main.py` was exercised against a host-side
mock only.

---

## Files

| File | Purpose |
|------|---------|
| `vibration_driver.spice` | ngspice netlist: switch on/off operating points and a 1kHz PWM transient |
| `smoke_test.py` | Safety and functional assertions on the netlist, plus `main.py` against a mocked `machine` |
| `main.py` | MicroPython: 1kHz PWM on GP16, duty stepped 0→100% in 10% steps |
| `breadboard.md` | Wiring, run steps, failure table |

---

## Design

```
3V3(OUT) ──┬──────────┐
           │          │ motor (R≈33Ω, L≈1mH, stalled-winding model)
           │ 1N5817 ▲ │
           │ (cathode │
           │  at 3V3) │
           └──────────┴── collector
GP16 ─ 1kΩ ─┬─ base   S8050
            └─ 10kΩ ─ GND        emitter ── GND
```

| Part | Value | Why |
|------|-------|-----|
| Base resistor | 1kΩ | GPIO high 3.3V − Vbe ≈ 2.5mA of base current; the motor needs 96mA, a forced gain of 38, so any S8050 with hFE ≥ 40 at 100mA saturates |
| Base pull-down | 10kΩ | Keeps the transistor off while the GPIO is floating at boot |
| Flyback diode | 1N5817 | Clamps the turn-off spike of the motor's inductance |
| Supply | Pico `3V3(OUT)` (pin 36) | No extra hardware. The 96mA worst case sits at `psu_pico_rail`'s conservative ~100mA budget with nothing else drawing from that pin; a real motor draws less than the stalled model, and a motor rated at tens of mA leaves margin. The alternative is a `psu_low_v2` 3.0V rail (2×AA, ~250mA design point): connect its + in place of `3V3(OUT)`, share GND with the Pico, and the motor's noise stays off the Pico's ADC reference |

Simulated numbers (stalled-winding motor, so conservative: a spinning motor draws less):

| Quantity | Value |
|----------|-------|
| Motor current, GPIO high | 96mA |
| Vce(sat) | 0.13V (12.6mW in the transistor) |
| GPIO current | 2.5mA (default pad drive is 4mA) |
| Collector peak with the diode | 3.70V |
| Collector peak without the diode | 287V in the model, against the S8050's 25V Vceo |
| Leakage, GPIO low | under 1pA |

## What this does not show

- The motor's inductance and current are assumptions from a listing's rated maximum, not measurements.
- A coin or capsule motor spins at roughly 100–200Hz. Whether that makes useful ripples in a ripple tank (versus the 10–30Hz of a classic plunging dipper) has not been tested; the driver is the same either way.
- Motor brush noise on the Pico's `3V3(OUT)` rail can disturb the Pico's ADC, whose reference is that same rail. Don't read the ADC while the motor runs, or give the motor the `psu_low_v2` rail (see Supply above).
- The 100mA figure is `psu_pico_rail`'s own conservative budget, not a measurement of the Pico's regulator.
- Diode orientation matters: reversed, it ties the collector to 3V3 and the transistor sinks current through it instead of the motor. See `breadboard.md`.
