# KB: `INDBRIDGE`, `ACCELIF`, and `ACTIVELIM` design decisions (2026-09-23)

Audience: future LLM sessions. Not end-user content. Records why the
two circuits designed 2026-09-23 look the way they do, so a later session
doesn't redo the analysis, plus three corrections to `ACTIVELIM` found
while working out its validation.

## `INDBRIDGE` (`measurement_tools/inductance_bridge/`)

**Why not an RL time constant, the way `CAPBRIDGE` uses RC.** For the
1µH–1mH assortment, `L/R` at any resistance a GPIO can drive is
nanoseconds to microseconds. The Pico's polled ADC samples every ~10µs at
best. Same failure as the ceramic-capacitor range note in
`capacitance_bridge/README.md`. The inductors' own winding resistance
(0.1Ω up to ~15Ω, an estimate) also dominates a time-constant reading.

**Chosen: parallel-LC resonance sweep.** PWM square wave → 1kΩ → tank
(`Lx` ∥ 10nF) → 1N5817 peak detector → ADC. `Lx = 1/((2πf0)²C)`. The
PWM sets frequency; the diode + hold RC makes the amplitude a DC level a
slow ADC can read. Rejected alternatives, so they aren't reconsidered
from scratch:

- *Series-resonant tank:* Q multiplication puts several volts on the
  ADC-facing node at 1mH (Q~4.5 into a 316Ω characteristic impedance
  → ~10V). Parallel tank amplitude can't exceed the drive.
- *Colpitts/LC oscillator + PIO frequency counter:* the classic LC-meter
  topology, but start-up at 1µH (characteristic impedance ~10Ω) is
  doubtful with the two S8050s on hand, it needs a bias design that can't
  be verified without hardware, and the PIO counter is more moving parts
  than a sweep.
- *Flyback ramp / comparator timing:* 1mH at 3.3V and 10mA is 3µs, below
  the LM358's response and the Pico's polling.
- *Bridge with a known reference inductor:* none on hand, and the
  assortment's values are the thing being verified.

**One capacitor covers the whole assortment.** 10nF puts f0 at 50kHz
(1mH) to 1.59MHz (1µH); a second range capacitor was considered and not
needed. Drive resistor 1kΩ is deliberately large: it makes the loaded Q
follow the inductor's own Q instead of the GPIO's ~50Ω output
resistance, and caps drive current at 3.3mA with the tank shorted.

**Limits, stated in the README so they aren't rediscovered:**

- 1µH is the weak end: tank amplitude 0.35V simulated even at 5× the
  assumed winding resistance, and the PWM step near 1.6MHz is ~1.3%
  (125MHz sys clock, integer `top`).
- Accuracy is set by the 10nF capacitor's tolerance (f0 ∝ 1/√C, so
  ±10% C ≈ ±10% L). That resolves neighbours ≥1.4× apart but not 470µH
  vs 560µH (1.19×).
- The square wave's 3rd harmonic gives a secondary peak at f0/3 with
  ~34% of the main peak's detector level. `main.py` takes the global
  maximum, so it's harmless; the smoke test asserts the ratio stays
  under 50%.
- The winding-resistance table (`0.1Ω × (L/1µH)^0.7`) is an assumption.
  The smoke test repeats the peak check at 3× and 5× it.

**Unverified on hardware:** `main.py` relies on `machine.PWM.freq()`
returning the quantized frequency the divider really runs at. If this
MicroPython build returns the requested value, f0 error grows to the PWM
step (≤1.3% at 2MHz). Confirm on the first real run.

## `ACCELIF` (`signal_conditioning/accelerometer_interface/`)

- **No analog design exists** — the MPU-6050 digitizes on the module. The
  only electrical failure modes are I2C bus timing and the supply, and
  those are what the netlist/smoke test model. Placed under
  `signal_conditioning/` next to the other tier5 sensor nodes, though its
  shape is the Pico-driven digital-interface pattern of
  `cd4066_switch_tester`.
- **Pull-up value on the GY-521 is an assumption** (4.7kΩ typical; not
  measured). The netlist sweeps 2.2k/4.7k/10k × 50/100/200pF instead of
  trusting one value. Standard mode (100kHz, `main.py`'s default) passes
  everywhere except 10k with 200pF of wiring; fast mode passes only the
  low-capacitance cells. Default is 100kHz for that reason.
- **The listing variant was "1pcs Compatible"** — plausibly a clone die
  reporting `WHO_AM_I` 0x70–0x72 instead of 0x68. `main.py` accepts those
  IDs with a note (accelerometer registers match) rather than failing.
- Pins: I2C0, SDA=GP4 (pin 6), SCL=GP5 (pin 7), VCC=3V3(OUT) (pin 36),
  GND=pin 38. `AD0` left unconnected (0x68); `main.py` also accepts 0x69.
- `main.py` is a verdict-and-exit bring-up check (project convention for
  validation scripts) that also prints the vibration RMS over its
  window, which is the figure `VIBISO` will compare. It polls, so the
  sample rate is I2C-limited (a few hundred Hz to ~1kHz) and jittery:
  fine for RMS, not for a spectrum.

## `ACTIVELIM` corrections (2026-09-23)

Found while working out how to validate it with the parts being ordered;
the circuit stays a 2A hard-trip design.

1. **The Lenovo adapter's 5V profile is rated 2A** (profiles: 5V/2A,
   9V/2A, 15V/3A, 20V/3.25A, from the `PSUMEDHIGH` node label). The
   earlier plan, "5V tap, 10W resistor at 2A", could never *exceed* a 2A
   trip. The first tap that can is 15V, and 15V into a 2.5A load is ~37W,
   past any single resistor in the assortment. **Fix: scale the trip for
   the bench check, not the load.** Reference divider set to ~0.08V
   (trip ~0.8A) via R_top = 2kΩ+1kΩ, R_bot = 100Ω, then 5V into 8Ω
   (0.625A, no trip) and 5Ω (1.0A, trip). Netlist Case 3 and the smoke
   test cover it. This validates the switching logic, not the 2A number.
2. **The LM358 is not rail-to-rail on the high side** (output ≈ Vcc −
   1.5V). Powered from 3.3V the gate reaches ~1.8V, at the IRLZ44N's
   1–2V threshold, so the MOSFET wouldn't be fully on. The original
   netlist modeled an ideal 0/3.3V swing and hid this. Now the LM358 runs
   from 5V and the model's high level is 3.5V. `parts_reference.md`'s
   LM358 entry carries the warning.
3. **The TL431A needs ≥~1mA into its cathode.** The original 10kΩ
   pull-up from 3.3V gave ~0.08mA; from 5V it would give 0.25mA. Changed
   to 1kΩ from 5V (2.5mA total, ~1.7mA left after the bench-check
   divider). The divider values, previously "a real-hardware sizing
   step", are now concrete resistors from the SunFounder kit.

Lesson (same family as the "check what the reused circuit actually
documents" entry in `todo_list_conventions.md`): validating a design
against the real source's *rated current at the chosen tap* is part of
"is the validation achievable", not just "does a source exist".

## Verifying `main.py` without the Pico

No Pico was attached this session (`mpremote devs` listed only `ttyS*`).
The two new `main.py` files were run on the host with a mocked `machine`
(`PWM`/`ADC`/`I2C`/`Pin`) and `time.sleep_ms`/`ticks_us` patched in, the
device modeled from the same physics as the netlist (tank impedance for
`inductance_bridge`; register reads for the MPU-6050). That catches logic
bugs — peak finding, unit conversion, verdict strings, the
open/shorted/no-device messages — and the READMEs say so in their
Validation sections. It cannot show that the real peripheral behaves the
same (PWM quantization readback, I2C ACKs, real component values), and
nothing should be marked "bench-tested" from it. The mock scripts lived
in the session scratchpad, not the repo; a future session can rebuild one
in ~40 lines.
