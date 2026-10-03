# adc_ads1115

A 16-bit ADS1115 ADC module on the Pico's I2C0 bus, with a protected input
network, as the first concrete `ADCDRV` (tier9 "ADC driver circuit", see
`docs/general_purpose_circuit_dependency.md`). Reason it exists: the Pico's
own ADC resolves 0.8mV per step (see `docs/spacetime_circuits_dependency.md`'s
"Bench-scale resolution budget"), and the sensor chain being built
(`TIA`, `CHGAMP`, `HALLAMP`) produces signals where that is the limit.
At ±4.096V full scale an ADS1115 step is 125µV, 6.4× finer; at ±2.048V it is
62.5µV.

**Status: designed and simulated 2026-10-01 (`smoke_test.py` green); not built.
One module is on order** (2026-10-02, `docs/orders.md` "On order"; a different
listing from the one first picked, same pin labels and I2C address range).
`main.py` was exercised against a host-side mock only.

---

## Files

| File | Purpose |
|------|---------|
| `adc_ads1115.spice` | ngspice netlist of the input network: nominal level, 6.4V and −1V faults, low-pass corner |
| `smoke_test.py` | Input-limit safety checks, config-word and LSB checks, `read_volts()` against a simulated ADS1115, and the bench check's pass/fail logic |
| `main.py` | MicroPython: scan for 0x48, read a divider midpoint with both ADCs, compare |
| `breadboard.md` | Wiring and failure table |

---

## Design

```
sensor ── Rin 10k ──┬── AIN0 ──► ADS1115 (VDD = 3V3, ADDR = GND → 0x48)
                    ├── 100nF ── GND
                    ├── 1N5817 ──► VDD   (anode on AIN0)
                    └── 1N5817 ◄── GND   (cathode on AIN0)
```

| Choice | Value | Why |
|--------|-------|-----|
| Supply | Pico `3V3(OUT)` | Single-ended inputs span 0 to VDD = 3.3V, so ±4.096V full scale gives 26 400 usable counts (14.7 bits), not 32 768 |
| `Rin` | 10kΩ | Limits clamp current to under 300µA in a 6.4V fault, and sets the low-pass corner |
| `Cin` | 100nF | Corner 159Hz with `Rin`: the sensors here (balance, vibration, light) are slow |
| Clamps | 2× 1N5817 | Keep the pin inside GND−0.3V…VDD+0.3V (recalled datasheet limit) if a sensor on `psu_4xaa`'s 6V rail drives it |

Simulated: input at 6.4V reaches the pin at 3.53–3.54V (about 70mV inside the 3.6V limit),
−1V reaches −0.20V; the clamp pushes 191µA into the 3V3 rail in that fault; low-pass corner 159Hz;
a divider midpoint passes with 0.25% loss.

## What this does not show

- The 70mV clamp margin depends on the diode's forward drop, which varies by unit and
  temperature. The clamp is a fault backstop; design sensors to stay at or below 3.3V.
- The ADS1115's input resistance (modeled 6MΩ), absolute-maximum input range and register map
  are recalled from its datasheet, not re-checked against the PDF in this session.
  The register values in `main.py` are pinned by `smoke_test.py` against that recollection, not
  against the part.
- `Rin`'s DC cost is `(Rsrc + Rin) / 6MΩ`: 0.17% for a low-impedance source, 0.25% for the
  5kΩ divider the bench check uses. That is a fixed gain error, not noise.
- The bench check compares against the Pico's ADC, which has its own tens-of-millivolts
  worst-case error. It confirms wiring and address and a sane reading; it is not a calibration.
- Source impedance above about 10kΩ needs a lower data rate or a buffer; not designed here.
