# accelerometer_interface

An I2C connection from the Pico to a GY-521 module (MPU-6050 3-axis
gyro/accelerometer), with a bring-up script that confirms the module
answers and reads gravity correctly. This is the tier5 `ACCELIF` node in
[spacetime_circuits_dependency.md](../../docs/spacetime_circuits_dependency.md).

The module digitizes on board (16 bits per axis, ±2/4/8/16g), so unlike
the other tier5 front-ends (`electric_field_probe`, `charge_amplifier`)
there is no analog circuit to design — the electrical design questions
are the I2C bus timing and the supply, and those are what the netlist
and smoke test cover. It is closer in shape to
[cd4066_switch_tester](../../measurement_tools/cd4066_switch_tester/)
(Pico-driven digital interface) than to the op-amp circuits.

Powered from the Pico's 3V3(OUT) pin via `psu_pico_rail` — no purchase
needed.

Its reason for existing is `VIBISO`: measuring how much a vibration-
isolation platform attenuates bench vibration needs an accelerometer on
the platform and one on the bench (or the same one moved between them).
See `docs/TODO-arcticoder.md`'s "Blocked" section.

---

## Files

| File | Purpose |
|------|---------|
| `accelerometer_interface.spice` | ngspice netlist — I2C bus rise time across pull-up/wiring-capacitance cases, and the supply operating point |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — bring-up check with a PASS/FAIL verdict, plus the vibration RMS over its sampling window |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version: VCC → 3V3(OUT) (pin 36), GND → GND (pin 38), SDA → GP4 (pin 6),
SCL → GP5 (pin 7). Nothing else.

---

## Simulate

```bash
# from the repo root
ngspice -b signal_conditioning/accelerometer_interface/accelerometer_interface.spice
```

Prints `RISE` lines (pull-up, bus capacitance, 30%→70% rise time, low
level) for nine cases and one `RAIL` line (module voltage, current).

---

## Bus timing

I2C is open-drain: the pull-up resistors charge the wiring capacitance,
and that RC sets how fast the lines rise. The GY-521 carries its own
pull-ups; a typical layout uses 4.7kΩ, **but the value on this board
hasn't been measured**, so the simulation sweeps 2.2k/4.7k/10k against
50/100/200pF of wiring instead of assuming one.

| Pull-up | 50pF | 100pF | 200pF |
|---------|------|-------|-------|
| 2.2k | 93ns | 186ns | 373ns |
| 4.7k | 199ns | 398ns | 796ns |
| 10k | 424ns | 847ns | 1695ns |

Standard mode (100kHz, what `main.py` runs at) allows 1000ns; fast mode
(400kHz) allows 300ns. Everything passes standard mode except 10k with
200pF of wiring, and only the low-capacitance cells of the 2.2k/4.7k
rows pass fast mode. If a longer jumper or a different pull-up ever
makes `main.py` flaky, this table is the first thing to check;
`I2C_FREQ` is one line at the top of `main.py`.

---

## Range and accuracy

`main.py` sets ±2g: 16384 LSB/g, the most sensitive setting, and enough
for bench vibration. The datasheet's sensitivity tolerance is ±3% and
its zero-g offset ±50mg per axis, which is why the gravity check allows
±0.1g rather than something tighter. The accelerometer bandwidth is set
to its 260Hz maximum (digital low-pass off). `main.py` polls rather than
using the chip's FIFO or a timer, so the sample rate is whatever the I2C
transaction time allows (a few hundred Hz to ~1kHz) and jitters — fine
for an RMS figure, not for a spectrum.

---

## Validation

**Not yet bench-tested.** The netlist and smoke test cover bus timing and
supply. `main.py`'s logic (address scan, ID check, unit conversion,
mean/noise/RMS math, verdicts) was exercised against a host-side mock of
the I2C device, not the Pico or the module. Things only the real module
settles:

- Whether `WHO_AM_I` reads `0x68` — the AliExpress variant was "1pcs
  Compatible", which is sometimes a different die.
- Whether the header pins are soldered on and make contact.
- The actual pull-up value on the board (not needed for the check to
  pass, but it decides whether 400kHz is available).
