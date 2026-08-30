# resistance_measurement

A voltage-divider circuit that lets a Raspberry Pi Pico measure an unknown
resistance without a multimeter — built specifically to find the actual
resistance of a chain of jumper wires being pressed into service as a
low-value current-sense shunt for
[ammeter_1ohm](../ammeter_1ohm/), since no 0.1Ω resistor was on hand.

**Result: the jumper chain measures ~1.005Ω**, stable across repeated
readings. That value is what `ammeter_1ohm/main.py` uses as its
`SHUNT_OHMS`.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — reads GP26, averages ADC samples, computes and prints `R_x` |
| `breadboard.jpg` | Photo of the actual bench jig |

No `.spice`/`smoke_test.py` here — this is a one-off measurement jig for
characterizing a specific physical jumper chain, not a circuit with a
fixed design target to assert against.

---

## Circuit

A known reference resistor (`R_ref`, 10Ω from
[pico/docs/inventory.md](../../../pico/docs/inventory.md)) forms a voltage
divider with the unknown resistance (`R_x`, the jumper chain). The Pico's
3V3 rail drives the divider, and GP26/ADC0 reads the midpoint:

```
Pico 3V3 (Pin 36)
      │
  [R_ref] (10 Ohms)
      │
      ├──────► GPIO 26 / ADC0 (Pin 31)
      │
  [R_x Chain] (Unknown Resistance)
      │
Pico GND (Pin 28)
```

Solving the divider equation for the unknown leg:

```
R_x = R_ref × (V_out / (V_in − V_out))
```

where `V_in` is the Pico's 3V3 rail and `V_out` is what GP26 reads at the
R_ref/R_x junction. `main.py` averages 50 ADC samples per reading to cut
down noise before doing this division.

---

## Build

1. Wire the circuit above — see `breadboard.jpg` for the as-built layout.
   The jumper chain under test goes in the `R_x` position (GPIO26 junction
   down to GND); swap in whatever unknown resistance needs measuring.
2. `mpremote run main.py` and watch the serial output — it prints the
   measured voltage and the computed `R_x` continuously.
3. If it prints "Circuit Open," `R_x` isn't actually connected to GND. If
   it prints "Short to GND," `R_x` is reading as ~0Ω.

---

## Why this is safe near 0Ω

`R_ref` (10Ω) sits between the Pico's 3V3 rail and the divider midpoint, so
even if `R_x` is a dead short to GND, the current is still limited to
3.3V / 10Ω ≈ 330mA — well inside what a Pico GPIO can source without
damage, and small enough that a genuinely low `R_x` (like the ~1Ω jumper
chain this jig was built to measure) doesn't need any additional current
limiting of its own.
