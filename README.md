# Electronics Lab — Circuits

Test and measurement circuits for a physics lab bench, built bottom-up from
a bootstrap PSU through the tiers laid out in
[docs/general_purpose_circuit_dependency.md](docs/general_purpose_circuit_dependency.md).
Spacetime research — experiments aimed at faster-than-light travel, with
no fixed commitment to any one specific theory or approach — is the
current driving objective and gets its own tier graph in
[docs/spacetime_circuits_dependency.md](docs/spacetime_circuits_dependency.md),
but the general-purpose foundation underneath it — PSU tiers, protection,
safety monitoring, signal conditioning, measurement tools — isn't specific
to that goal and is meant to be useful on its own.

Each circuit gets its own top-level folder with a SPICE netlist, a
generated schematic, and a breadboard wiring guide. Power supplies are
grouped under `power_supplies/`; measurement/test tools are grouped under
`measurement_tools/`; signal-conditioning building blocks (references,
amplifiers, sensor front-ends) are grouped under `signal_conditioning/`;
timing/waveform generators are grouped under `oscillators/`; safety
monitoring circuits are grouped under `safety/`; current/voltage
protection circuits are grouped under `protection/`; other circuit
categories get their own top-level folders as they're built.

---

## Schematics

Each project can render a `schematic.png` from its `.spice` netlist.
`schematic.png` is **not committed** (see `.gitignore`) — it's a build
artifact, regenerated on demand:

```bash
# from the repo root
python tools/spice_to_schematic.py oscillators/ne555_astable/ne555_astable.spice
```

Output is written as `schematic.png` in the same directory as the `.spice`
file. `tools/spice_to_schematic.py` uses **schemdraw** to parse SPICE `R`,
`C`, `V`, and `D` elements and render a schematic image.

---

## Running simulations

Every circuit folder has an ngspice `.spice` netlist. Run with `ngspice -b`
to predict voltages and currents before building.

```bash
# from the repo root
ngspice -b measurement_tools/fuse_test_voltmeter/fuse_test_voltmeter.spice
ngspice -b measurement_tools/cd4066_switch_tester/cd4066_switch_tester.spice
ngspice -b power_supplies/psu_pico_rail/psu_pico_rail.spice
ngspice -b power_supplies/psu_ultralow_v1/psu_ultralow_v1.spice
ngspice -b power_supplies/psu_low_v2/psu_low_v2.spice
ngspice -b power_supplies/psu_3xaa/psu_3xaa.spice
ngspice -b power_supplies/psu_4xaa/psu_4xaa.spice
ngspice -b power_supplies/psu_medlow_usbc/psu_medlow_usbc.spice
ngspice -b signal_conditioning/voltage_reference_lm358/voltage_reference_lm358.spice
ngspice -b signal_conditioning/transimpedance_amplifier/transimpedance_amplifier.spice
ngspice -b oscillators/ne555_astable/ne555_astable.spice
ngspice -b measurement_tools/capacitance_bridge/capacitance_bridge.spice
ngspice -b signal_conditioning/electric_field_probe/electric_field_probe.spice
ngspice -b signal_conditioning/charge_amplifier/charge_amplifier.spice
ngspice -b safety/thermal_monitor/thermal_monitor.spice
ngspice -b signal_conditioning/phase_detector/phase_detector.spice
ngspice -b protection/active_current_limiter/active_current_limiter.spice
ngspice -b measurement_tools/inductance_bridge/inductance_bridge.spice
ngspice -b signal_conditioning/accelerometer_interface/accelerometer_interface.spice
```

Run from the repo root. Each netlist prints an operating point at its
nominal load, then sweeps the load resistor to show the V/I curve.

`oscillators/ne555_astable/` (and any future circuit using a behavioral
macromodel rather than plain R/C/V/D elements) prints `gmin`/source-
stepping warnings during startup — expected for that kind of model, not a
sign the result is wrong; see that circuit's own README § Simulate for
why.

---

## Smoke-testing a circuit

Printing an operating point documents what a circuit *should* do; it
doesn't check it. Every circuit folder also has a `smoke_test.py` that
runs its netlist and asserts against real thresholds: no node exceeding a
part's safe voltage, no resistor dissipating more than its rated wattage
(where the resistor is an actual physical part — some netlists use `Rload`
purely as a simulated stand-in for whatever gets attached later, which
isn't a smoke risk on its own), and a functional check that the circuit
actually does what it claims (a divider ratio within tolerance, a
buffered reference holding steady under load, a switch reading
unambiguously different when open vs. closed). `tools/ngspice_runner.py`
holds the shared ngspice-invocation/parsing logic every `smoke_test.py`
reuses.

```bash
# from the repo root
python measurement_tools/cd4066_switch_tester/smoke_test.py
python measurement_tools/fuse_test_voltmeter/smoke_test.py
python power_supplies/psu_low_v2/smoke_test.py
python power_supplies/psu_3xaa/smoke_test.py
python power_supplies/psu_4xaa/smoke_test.py
python power_supplies/psu_medlow_usbc/smoke_test.py
python power_supplies/psu_pico_rail/smoke_test.py
python power_supplies/psu_ultralow_v1/smoke_test.py
python signal_conditioning/voltage_reference_lm358/smoke_test.py
python signal_conditioning/transimpedance_amplifier/smoke_test.py
python oscillators/ne555_astable/smoke_test.py
python measurement_tools/capacitance_bridge/smoke_test.py
python signal_conditioning/electric_field_probe/smoke_test.py
python signal_conditioning/charge_amplifier/smoke_test.py
python safety/thermal_monitor/smoke_test.py
python signal_conditioning/phase_detector/smoke_test.py
python protection/active_current_limiter/smoke_test.py
python measurement_tools/inductance_bridge/smoke_test.py
python signal_conditioning/accelerometer_interface/smoke_test.py
```

Or run all of them at once with `tools/run_all_smoke_tests.py`, which
finds every `smoke_test.py` in the repo so this list doesn't have to be
kept in sync by hand:

```bash
# from the repo root
python tools/run_all_smoke_tests.py
```

Exits non-zero on any failed check.

---

## Circuits — built & bench-tested

Each of these has been physically assembled and confirmed against its
`main.py`/`smoke_test.py` pass criteria on real hardware. Not committed
to a breadboard permanently — once a circuit's bench check passes and
nothing else currently under construction needs its wiring in place, its
parts go back to inventory; the netlist/breadboard.md/smoke_test.py stay
as the record for rebuilding it later, along with a `breadboard.jpg`
photo of the as-built jig where one was taken (see each circuit's own
`README.md` § Files).

| Folder | Circuit | Tier | Bench-tested |
|--------|---------|------|--------------|
| `power_supplies/psu_pico_rail/` | Pico's own onboard 3.3V rail, ~100mA budget | interim bootstrap PSU | 2026-08 |
| `signal_conditioning/voltage_reference_lm358/` | LM358 unity-gain buffer holds a resistor-divider reference steady under load | tier1 `REF` | 2026-08-27 — loaded reading within 0.23% of unloaded (±2% tolerance) |
| `measurement_tools/cd4066_switch_tester/` | Pico-driven bring-up jig for one CD4066B analog switch — confirms it passes/blocks before trusting it in a later design | component validation (ahead of tier9 `MUX`) | 2026-08-28 — switch 1 (I/O A pin 1 / I/O B pin 2 / control pin 13) PASS on all 10 CD4066BCN units; switches 2–4 per chip not yet individually tested |
| `measurement_tools/fuse_test_voltmeter/` | Pico ADC probe across a battery→fuse→resistor loop; arm switch (GP15) gates trip/reset detection so battery connect/disconnect isn't misread as a trip | bootstrap / concurrent measurement tool | 2026-08-28 — **bench wiring has since diverged and trip detection is currently non-functional** (no longer a blocker — polyfuses are now sorted via `ammeter_10ohm`/`ammeter_1ohm` below instead); see this circuit's own README § Current bench status for the full detail |
| `measurement_tools/ammeter_10ohm/` | Pico reads current (not just voltage) through a polyfuse under test, via a 10Ω shunt + slide-switch shorting jumper | polyfuse validation (bootstrap tier) | 2026-08-30 — all 20 RXEF005 (50mA) polyfuses PASS (trip + reset confirmed per unit) |
| `measurement_tools/ammeter_1ohm/` | Same approach as `ammeter_10ohm` scaled for 500mA: ~1Ω jumper-chain shunt (see `resistance_measurement/`) + 1N5817 reverse-polarity diode on the high side | polyfuse validation (`psu_low` tier) | 2026-08-30 — all 20 RXEF050 (500mA) polyfuses PASS (trip + reset confirmed per unit) |
| `measurement_tools/resistance_measurement/` | Voltage-divider jig (known 10Ω reference vs. unknown leg) for measuring a low-value resistance or checking continuity between two nodes | supporting tool for `ammeter_1ohm`; reused for continuity/troubleshooting checks (e.g. `psu_4xaa`) | 2026-08-30 — jumper-wire chain measured at ~1.005Ω, stable across repeated readings |
| `measurement_tools/raw_voltage_probe/` | Plain averaged-voltage reader at GP26 — no resistance math, no divider assumptions; the calling circuit's own README supplies the target | general-purpose probe, split out of `psu_4xaa` 2026-09-07 for reuse | 2026-09-11 — confirmed both the ~0V (divider unpowered) and non-zero (~1.9V, `psu_4xaa`'s divider) target readings against real hardware |
| `power_supplies/psu_ultralow_v1/` | Single AA + 50 mA polyfuse | `psu_ultralow` (bootstrap) | 2026-08-30 — component-level validation complete: RXEF005 polyfuse PASS via `ammeter_10ohm/` (all 20 units), AA battery holder ready per `docs/inventory.md`. The assembled PSU itself has not been separately re-probed as its own demo build (see `fuse_test_voltmeter/README.md`'s test-vs-demo distinction) |
| `power_supplies/psu_4xaa/` | 4×AA in series + 1N5817 Schottky + 500 mA polyfuse | `psu_system` (top of the plain-AA-series progression) | 2026-09-11 — GP26 read ~1.9V through the output's 10 kΩ/5.1 kΩ divider, matching the ~0.338 ratio's prediction. An earlier ~0.14V fault on a different breadboard was never pinned to one component — rebuilding the same circuit on a second breadboard fixed it immediately (see `README.md` § Troubleshooting) |
| `oscillators/ne555_astable/` | NE555 astable square-wave oscillator, 3296 trimpot timing | tier1 `OSC`, first per-unit NE555 batch validation | 2026-09-13 — oscillation confirmed (113/109 zero-crossings across two readings, ~1.5kHz, inside the expected 649Hz–2.9kHz trim range) via `measurement_tools/oscillation_probe/`. **Output divider fixed**: root cause was a mis-picked 220Ω resistor standing in for one of the two intended 10kΩ legs; swapped for a verified 10kΩ, GP26 now reads a real ~2.2V half-swing instead of pinning at 3.300V — see `README.md` § Validation |
| `measurement_tools/oscillation_probe/` | Burst-sampled GP26 reader that reports min/max/swing and a zero-crossing count — confirms genuine toggling where `raw_voltage_probe`'s averaging can't | general-purpose probe, built 2026-09-12 for `ne555_astable`'s bring-up | 2026-09-12 — used live against the `ne555_astable` bench build (see that row above) |
| `signal_conditioning/electric_field_probe/` | Bare-electrode electrostatic sensor: 1MΩ/1MΩ bias divider to VCC/2, TL082 unity-gain follower | tier5 `EPFIELD` — spacetime-research sensor node, see `docs/spacetime_circuits_dependency.md` | 2026-09-15 — TL082 follower confirmed live (rest ~1.693–1.701V vs. simulated 1.650V, a small stable offset, not railed — resolves the earlier "hasn't been confirmed below spec'd supply" caveat). A piezo-igniter spark and a triboelectric (rubbed tape) test charge both produced no deflection beyond that same offset — consistent with the design's own predicted sensitivity ceiling from the 1MΩ (not GΩ) bias divider, not a wiring fault; see that circuit's own README § Bench findings for the diagnosis and concrete next steps |
| `power_supplies/psu_low_v2/` | 2×AA + Schottky + 500 mA polyfuse | `psu_low` tier | 2026-09-17 — GP26 read 1.007V average (20 readings) through the output's 10 kΩ/5.1 kΩ divider, matching the ~1.0V correct-orientation target. Root cause of an earlier no-reading gap: the Schottky's cathode band paint had worn off and it was installed backward on a guess — flipped once this check caught it; see `README.md` § Validation |
| `signal_conditioning/transimpedance_amplifier/` | PT334-6C photodiode + LM358 current-to-voltage converter | tier2 `TIA` (fed from `psu_low_v2`) | 2026-09-17 — genuine light-dependent output confirmed: ~0.505–0.510V under ambient room light, ~0.72–0.78V under a phone flashlight (higher held close to the photodiode). Superseded a 2026-09-16 flat, light-independent ~0.38V reading that was traced to the `psu_low_v2` rail above, not this circuit's own wiring — see `README.md` § Validation |
| `signal_conditioning/phase_detector/` | SN74HC86N XOR gate compares `ne555_astable`'s output tap against an independent Pico PWM reference, RC-lowpassed | tier4 `PHASED`, feeds tier6 `LOCKIN` (undesigned) | 2026-09-19 — filtered output confirmed moving (0.871–1.546V over a ~3.5s window, not pinned at one extreme) as the two non-phase-locked oscillators drift, the real pass criterion per this circuit's own README § Validation. Required re-assembling `ne555_astable` first (broken back down to inventory since its own 2026-09-13 validation) |
| `safety/thermal_monitor/` | MF52AT NTC divider (centers at VCC/2 at 25°C) + GPIO-driven alarm LED | safety `THERM` ("Thermal Monitoring with Alarm Threshold") | 2026-09-21 — ambient baseline stable at 1.708–1.713V / 10723–10790Ω / 23.3–23.5°C (close to the simulated VCC/2 midpoint, matching room temp being a couple degrees under the MF52AT's 25°C reference point); a sustained finger pinch drove a monotonic, physically-consistent response — resistance fell 10362Ω→8106Ω and reported temperature rose 24.2°C→29.8°C. Alarm LED correctly stayed off throughout (`ALARM_THRESHOLD_C=40.0`, never reached) — a true alarm trip hasn't been bench-tested yet. One transient outlier mid-run (3.253V/698639Ω/−47.4°C, one sample, self-corrected next reading) attributed to a momentary contact disturbance from handling the thermistor rather than a wiring fault — see `kb/bench_photo_diagnostics_notes.md`'s matching 2026-09-21 entry |
| `measurement_tools/capacitance_bridge/` | RC charge-time capacitance meter (known `Rref`=100kΩ vs. unknown `Cx`, timed against a 63.2%-of-Vin threshold) | tier3 `CAPBRIDGE` | 2026-09-22 — a 47µF (25V) `Cx` from the electrolytic kit read 48.87µF/47.75µF/47.64µF across three consecutive runs, all within the kit's own ±20% tolerance of the 47µF nominal. A first attempt the same day (33µF `Cx`) read ~0.00–0.01µF on every run — traced to `Rref`'s far lead resting on the breadboard's center divider ridge rather than seated in the junction hole, leaving the ADC node floating; reseating the lead fixed it. See `kb/bench_photo_diagnostics_notes.md`'s matching entry |

---

## Circuits — designed, not yet built

Build order runs top to bottom: the voltmeter has to exist — and its own
fuse-free sanity check has to pass — before it's trustworthy for sorting
good polyfuses from bad, and a polyfuse has to be sorted good before it
belongs in a PSU. See
[measurement_tools/fuse_test_voltmeter/README.md](measurement_tools/fuse_test_voltmeter/README.md)
for the voltmeter self-check → bench-test-the-fuse-batch → demo-in-a-PSU
sequence this drives.

| Folder | Circuit | Tier |
|--------|---------|------|
| `power_supplies/psu_3xaa/` | 3×AA + Schottky + 500 mA polyfuse | `psu_system` (between `psu_low` and `psu_4xaa`) |
| `power_supplies/psu_medlow_usbc/` | 5V USB-C + 500 mA polyfuse + bypass cap | `psu_medlow` — **shelved 2026-09-23**: not being built; `psu_medlow_lm317` is the path forward. Kept as the record of the passive-breakout approach (see its README § Status) |
| `power_supplies/psu_medlow_lm317/` | SFE Breadboard Power Supply Kit — LM317 adjustable, 3.3V/5V-selectable | `psu_medlow` (the adopted implementation; kit decided 2026-09-23, ordering from RobotShop; not yet built — see `docs/TODO-arcticoder.md`) |
| `signal_conditioning/charge_amplifier/` | 12mm piezo disc + TL082 inverting charge amp (`Cf`/`Rf_bias` feedback), VCC/2-biased for bipolar swing | tier5 `CHGAMP` — a direct spacetime-research sensor node |
| `protection/active_current_limiter/` | IRLZ44N + 0.1Ω sense resistor + LM358 comparator, hard-trip at 2A | general-purpose `ACTIVELIM`, protects `psu_medhigh`/`psu_high` (both backlog) |
| `signal_conditioning/accelerometer_interface/` | GY-521 (MPU-6050) on I2C0 — bus-timing/supply simulation plus a bring-up script (ID, gravity, noise, vibration RMS) | tier5 `ACCELIF` (designed 2026-09-23); the measurement side of `VIBISO` |
| `measurement_tools/inductance_bridge/` | PWM-driven parallel LC resonance sweep: unknown inductor vs. a known 10nF, Schottky peak detector, Pico ADC | tier3 `INDBRIDGE` (designed 2026-09-23); targets the 1µH–1mH color-ring assortment |
Each of these (except `psu_medlow_lm317`, a kit with no netlist
of its own — see its own README) has a SPICE netlist, a generated
schematic, a breadboard wiring guide, and a `smoke_test.py` (all but
`active_current_limiter` also have a `main.py`, same reasoning as the
PSU rows above having none). `inductance_bridge`'s and
`accelerometer_interface`'s `main.py` files were exercised against
host-side mocks only, not the Pico. None of these have been physically
assembled with real components yet (`psu_low_v2`,
`transimpedance_amplifier`, and `phase_detector` were exceptions as of
2026-09-16/2026-09-19, and all three moved to the bench-tested table
above once their validation checks passed — see their rows there and
`docs/TODO-arcticoder.md`).
For the PSU rows, the polyfuses they depend on
are no longer the blocker — both batches passed validation via
`ammeter_10ohm`/`ammeter_1ohm` above — so what remains is just the
physical build; `charge_amplifier` runs off
`psu_pico_rail` and has no battery-PSU dependency. Everything else in
`docs/general_purpose_circuit_dependency.md` /
`docs/spacetime_circuits_dependency.md` (most safety monitoring, most of
tiers 1–9) hasn't been worked out to netlist stage at all — folders for
those will show up here as they get one. `docs/TODO-arcticoder.md`'s
"Ready to build now" section tracks the physical-assembly status of
every row above.

---

## Notes

- `measurement_tools/fuse_test_voltmeter/`, `cd4066_switch_tester/`,
  `measurement_tools/capacitance_bridge/`,
  `measurement_tools/inductance_bridge/`,
  `signal_conditioning/accelerometer_interface/`,
  `signal_conditioning/voltage_reference_lm358/`, and
  `signal_conditioning/transimpedance_amplifier/` are the circuits here
  with Pico firmware (`main.py`) checked in. For more
  capable Pico ADC work (filtering, calibration curves, noise
  characterization), see the sibling `pico/` repo's
  `measurement_tools/gpio_analog_sensing/` — that repo isn't limited to
  one project, so general-purpose Pico infrastructure lives there rather
  than being duplicated here.
- Getting the physical Pico talking to this PC (WSL + `usbipd` device
  attach, MicroPython firmware, installing/using `mpremote`) is documented
  once in the sibling `pico/` repo rather than duplicated here — see
  [pico/README.md § Running on real hardware](../pico/README.md#running-on-real-hardware).
  Needed any time you run one of this repo's `main.py` scripts against
  real hardware instead of just simulating.
- See `docs/orders.md` for what's actually been ordered/received from
  AliExpress, `docs/parts_reference.md` for pinouts/specs on those parts,
  and `docs/inventory.md` for the master parts/quantities list — shared
  with the sibling `pico/` repo, which keeps a one-line pointer back to
  this file at `pico/docs/inventory.md` rather than its own copy (see
  `docs/kb/repo_docs_conventions.md`).

---

## Repo structure

```
measurement_tools/
    fuse_test_voltmeter/     Pico ADC voltmeter, validates polyfuses via USB (built & bench-tested; trip/reset short test still pending)
        fuse_test_voltmeter.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

    cd4066_switch_tester/    CD4066B analog-switch bring-up jig (built & bench-tested)
        cd4066_switch_tester.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

    ammeter_10ohm/           10Ω-shunt current-based polyfuse tester (built & bench-tested)
        main.py
        breadboard.jpg
        README.md

    ammeter_1ohm/            ~1Ω-shunt version for 500mA polyfuses (built & bench-tested)
        main.py
        breadboard.jpg
        README.md

    resistance_measurement/  voltage-divider jig for measuring an unknown low resistance (built & bench-tested)
        main.py
        breadboard.jpg
        README.md

    raw_voltage_probe/       plain averaged-voltage reader at GP26, no divider math (built & bench-tested; reused by psu_4xaa)
        main.py
        README.md

    oscillation_probe/       burst-sampled GP26 reader, confirms genuine toggling vs. a stuck DC level (built & bench-tested; built for ne555_astable)
        main.py
        README.md

    capacitance_bridge/      RC charge-time capacitance meter, targets the 1uF-470uF electrolytic kit (built & bench-tested 2026-09-22)
        capacitance_bridge.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

    inductance_bridge/       PWM-driven parallel-LC resonance sweep for the 1uH-1mH color-ring inductor assortment (tier3 INDBRIDGE, designed 2026-09-23, not built)
        inductance_bridge.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

power_supplies/
    psu_pico_rail/            Pico onboard 3.3V rail, ~100mA (interim, built & bench-tested)
        psu_pico_rail.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_ultralow_v1/         single AA + 50 mA polyfuse (built & bench-tested — component-level)
        psu_ultralow_v1.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_low_v2/               2xAA + Schottky + 500 mA polyfuse (built & bench-tested 2026-09-17)
        psu_low_v2.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_3xaa/                 3xAA + Schottky + 500 mA polyfuse (designed, not built)
        psu_3xaa.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_4xaa/                 4xAA + Schottky + 500 mA polyfuse (built & bench-tested)
        psu_4xaa.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        validation_breadboard.jpg
        smoke_test.py
        README.md

    psu_medlow_usbc/          5V USB-C + 500 mA polyfuse + bypass cap (shelved 2026-09-23, not being built)
        psu_medlow_usbc.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

    psu_medlow_lm317/         SFE breadboard PSU kit, LM317 3.3V/5V-selectable (to be ordered from RobotShop, not built)
        breadboard.md
        README.md

signal_conditioning/
    voltage_reference_lm358/  LM358 buffered voltage reference (built & bench-tested)
        voltage_reference_lm358.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

    transimpedance_amplifier/ PT334-6C photodiode + LM358 current-to-voltage converter (built & bench-tested 2026-09-17, real light response confirmed)
        transimpedance_amplifier.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

    electric_field_probe/    bare-electrode electrostatic sensor, TL082 follower (tier5 EPFIELD, built & bench-tested 2026-09-15)
        electric_field_probe.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

    charge_amplifier/        12mm piezo disc + TL082 inverting charge amp (tier5 CHGAMP, designed, not built)
        charge_amplifier.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

    accelerometer_interface/ GY-521 (MPU-6050) I2C interface + bring-up script (tier5 ACCELIF, designed 2026-09-23, not built)
        accelerometer_interface.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        main.py
        smoke_test.py
        README.md

    phase_detector/          SN74HC86N XOR phase detector + RC lowpass (tier4 PHASED, built & bench-tested 2026-09-19)
        phase_detector.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

safety/
    thermal_monitor/         MF52AT NTC divider + GPIO alarm LED (safety THERM, built & bench-tested 2026-09-21)
        thermal_monitor.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        main.py
        smoke_test.py
        README.md

protection/
    active_current_limiter/  IRLZ44N + sense resistor + LM358 comparator (ACTIVELIM, designed, not built)
        active_current_limiter.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        smoke_test.py
        README.md

oscillators/
    ne555_astable/            NE555 astable oscillator, 3296 trimpot timing (built & bench-tested — oscillation confirmed, output divider fixed 2026-09-13)
        ne555_astable.spice
        schematic.png         (generated, gitignored)
        breadboard.md
        breadboard.jpg
        breadboard2.jpg
        smoke_test.py
        README.md

docs/
    history.md                                  design conversation log
    general_purpose_circuit_dependency.md       general-purpose tier graph (PSU, protection, tiers 1-4/6/9, scope/logic-analyzer tiers M0-M5)
    spacetime_circuits_dependency.md            spacetime-specific tier graph (tiers 5/7/8)
    TODO-arcticoder.md                          human TODO: single active/blocked/backlog checklist for both graphs above, plus personal action items
    TODO-agent.md                                Claude-facing TODO: file/folder-creation tasks (netlists, docs) queued for Claude, before a build gets a bench bullet in TODO-arcticoder.md
    TODO-completed.md                           dated audit trail of TODO-arcticoder.md/TODO-agent.md items once done — moved here, not deleted
    inventory.md                                master component inventory (moved from pico/docs/inventory.md 2026-09-07)
    orders.md                                   AliExpress order log (received / on order)
    parts_reference.md                          pinouts & specs for ordered parts without a datasheet on file
    manuals/                                    converted (markitdown) part manuals; source PDFs gitignored
    kb/                                         process notes for future LLM sessions, not end-user docs

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
    ngspice_runner.py       shared ngspice-invocation/parsing helper for smoke_test.py scripts
    run_all_smoke_tests.py  finds and runs every smoke_test.py in the repo
```
