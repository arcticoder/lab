# vibration_driver

An S8050 low-side switch with a 1N5817 flyback diode that lets one Pico PWM
pin run a 3V vibration motor. It is the actuator stage the tier1 `SIMPGEN`
stand-in (`pico/leds/gpio_pwm_led/`) was missing: a GPIO pin can't source a
motor's current, and no motor or speaker is on hand (inventory checked
2026-09-23). It is also the driver `RIPPLETANK`'s wave dipper needs
(see `docs/TODO-arcticoder.md`).

**Status: designed and simulated 2026-10-01, revised 2026-10-02 for the motor
that was ordered (`smoke_test.py` green); not built. The motor is on order**
(2026-10-02, `docs/orders.md` "On order"). The `main.py` was exercised
against a host-side mock only.

---

## Files

| File | Purpose |
|------|---------|
| `vibration_driver.spice` | ngspice netlist: running and stalled operating points, GPIO-low leakage, and a 1kHz PWM transient (stalled) |
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
| Base resistor | 1kΩ | GPIO high 3.3V − Vbe ≈ 2.5mA of base current; the running motor needs 96mA (forced gain 38) and a stalled one 126mA (forced gain 50), so any S8050 with hFE ≥ 50 at 100mA saturates. The S8050's datasheet minimum at that current is higher than that, from memory, not re-checked |
| Base pull-down | 10kΩ | Keeps the transistor off while the GPIO is floating at boot |
| Flyback diode | 1N5817 | Clamps the turn-off spike of the motor's inductance |
| Supply | Pico `3V3(OUT)` (pin 36) | No extra hardware. Running, the motor sits at `psu_pico_rail`'s conservative ~100mA budget with nothing else drawing from that pin. **A stalled motor draws 126mA, over that budget** (still under half the regulator's documented ~300mA shared rating): don't hold the rotor, and don't leave PWM running into a jammed dipper. For anything that can stall (`RIPPLETANK`'s dipper in water), give the motor `psu_low_v2`'s 3.0V rail instead: connect its + in place of `3V3(OUT)`, share GND with the Pico, and the motor's noise stays off the Pico's ADC reference |

The motor's own figures, from the order listing (`docs/parts_reference.md`): rated 3V, working
range 2.7–3.3V, starts at 2.3V, 80–90mA rated, 120mA stall maximum. At 100% duty the
motor sees 3.3V − Vce ≈ 3.17V, inside that range.

Simulated numbers (running = 33Ω, 3V/90mA rated maximum; stalled = 25Ω, 3V/120mA stall maximum, no back-EMF):

| Quantity | Running | Stalled |
|----------|---------|---------|
| Motor current, GPIO high | 96mA | 126mA |
| Vce(sat) | 0.13V (12.6mW) | 0.15V (18.8mW) |
| GPIO current | 2.5mA (default pad drive is 4mA) | 2.5mA |
| Collector peak with the diode (1kHz PWM) | — | 3.71V |
| Collector peak without the diode | — | 342V in the model, against the S8050's 25V Vceo |
| Leakage, GPIO low | under 1pA | — |

## What this does not show

- The motor's inductance is an assumption, and its currents are the listing's rated and stall maximums, not measurements. Measure the real draw once (the Pico's `VSYS` read or a series 1Ω, `measurement_tools/ammeter_1ohm`'s approach) before trusting the 96mA.
- A coin or capsule motor spins at roughly 100–200Hz. Whether that makes useful ripples in a ripple tank (versus the 10–30Hz of a classic plunging dipper) has not been tested; the driver is the same either way.
- Motor brush noise on the Pico's `3V3(OUT)` rail can disturb the Pico's ADC, whose reference is that same rail. Don't read the ADC while the motor runs, or give the motor the `psu_low_v2` rail (see Supply above).
- The 100mA figure is `psu_pico_rail`'s own conservative budget, not a measurement of the Pico's regulator.
- Diode orientation matters: reversed, it ties the collector to 3V3 and the transistor sinks current through it instead of the motor. See `breadboard.md`.
