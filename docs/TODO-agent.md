# TODO — agent (Claude-facing)

This is the mirror of [TODO-arcticoder.md](TODO-arcticoder.md) for work
that doesn't need the user's hands, eyes, or a purchasing decision — just
writing files. Design/simulate/document a circuit here (netlist,
`breadboard.md`, `smoke_test.py`, `README.md`, optionally `main.py`) as
its own PR-sized unit of work, *before* it ever gets a "physically
assemble" bullet added to `TODO-arcticoder.md`'s "Ready to build now"
section. See
[docs/kb/todo_list_conventions.md](kb/todo_list_conventions.md) for why
this split exists and the reasoning behind each entry's queue position.

Mirrors the sibling `aqei-bridge` repo's `docs/TODO.md` (a pure
agent-task list — see that repo for the pattern this one is modeled on).

**Workflow**: pick an item below (top-to-bottom isn't a strict ordering
requirement here the way it is in `TODO-arcticoder.md` — none of these
block each other), design and verify it (simulate with `ngspice -b`,
confirm the numbers, run `smoke_test.py` and get it green) the same way
`signal_conditioning/transimpedance_amplifier/` and
`measurement_tools/capacitance_bridge/` were built 2026-09-13, then:

1. Move the item from here to `TODO-completed.md` (dated entry, same
   convention as `TODO-arcticoder.md`'s completions).
2. Add a "physically assemble" bullet for it to `TODO-arcticoder.md`'s
   "Ready to build now" section, stating its real dependency (check
   `general_purpose_circuit_dependency.md`/`spacetime_circuits_dependency.md`
   first — don't infer one from list position, see
   `kb/todo_list_conventions.md`'s TIA correction) and whether anything
   downstream currently needs it built, or whether it's optional/no-rush
   like `TIA`/`CAPBRIDGE` turned out to be.
3. Update this file's own item count/status references elsewhere (this
   file's own intro doesn't currently carry one, but `TODO-arcticoder.md`'s
   "Next order" section does — check it).

---

## Next session plan (written 2026-10-22 by Opus 5.5, for Sonnet 5.5 to action)

The user switched models and asked for detailed action recommendations only;
nothing below has been started. Revised 2026-10-22 after the user's review:
Part A now starts with three gates (measurement goal, mechanics, force-noise
prediction) and uses only the fab's own SMT parts. Work top to bottom. Part A is
the new main direction; Part B finishes the lock-in diagnosis; Part C is the housekeeping the
user's 2026-10-22 report triggers. Follow the usual conventions (no quotes of the
user, TODO-arcticoder one-line style, datasheet-checked parts, real pass/fail
smoke tests). The 2026-10-22 chat about PCB fabs versus soldering was not to be
written to the kb; record only the decisions as stated here.

### Part A — a fabricated, fully assembled research instrument (JLCPCB)

**What changed.** The user stops hand soldering (header bridges again on the
ADS1115 on 2026-10-22; the braid stuck instead of wicking) and wants boards
designed in KiCad, analog blocks validated in ngspice (KiCad's simulator is
ngspice; LTspice is optional), and manufacturing files exported for a fully
assembled JLCPCB order. The result must be an instrument that can support a
publishable (arXiv-level) experimental study, not a set of one-circuit boards.

**Hard constraints:**
- **All electronic parts are SMT parts sourced and placed by JLCPCB** from its own
  library. The user does not mail parts to the fab, so the through-hole parts on
  hand (49E/SS49E, PT334-6C, MF52AT, 5mm LEDs, leaded piezo) are not part of the
  design; their roles go to JLC-stocked SMT equivalents (for example a SOT-23
  linear Hall sensor, an SMD photodiode, 0603 NTCs, an SMD LED or IR emitter, a
  MEMS accelerometer). Purely mechanical items that need no soldering (the N42
  discs as a calibration target, the coin motors' flying leads into a
  fab-assembled screw terminal) may still be used where they fit, but nothing
  depends on them.
- **No soldering by the user.** Sensor heads are separate small JLC-assembled SMT
  boards joined to the main board by cables (check what pre-crimped cable JLC or an
  AliExpress cart in the same order window can supply, so nothing needs crimping).
- **One consolidated order** (shipping paid once), USB-powered, everything under the
  repo's 50V DC / 30V AC line.
- **No schematic, parts table or layout before the three gates in A1 pass.**

#### A0. Record the scope change (first, small)

- [ ] Update `kb/circuit_lifecycle_and_repo_scope.md` and the memory
      `lab_circuit_ephemeral_and_repo_scope` (no quotes): the repo now aims at a
      fabricated research instrument for a publishable study; breadboard builds
      become validation steps; ranking for this work may use research value.
      Feedback memories: the user does no more hand soldering, and fab orders use
      only the fab's own SMT parts (no customer-supplied parts).

#### A1. Three gates before any electronics design

These define the scientific value; the electronics only implement them. Results go
in `docs/research_instrument_plan.md` (user-facing), with the calculations in a
script (`tools/force_noise_budget.py`, pass/fail smoke test like the circuits).

- [ ] **G1 — Measurement goal (one paragraph, then the user confirms it).** State
      the claim the instrument supports if it meets its predicted performance. A
      bare "build an instrument" goal is not enough; the question must be specific
      and answerable at the achievable sensitivity. Recommended default to propose:
      *quantify the spurious-force mechanisms that have produced false positives in
      the small-thrust literature (current in the device's power leads interacting
      with the ambient and geomagnetic field, ohmic heating and thermal expansion,
      convection) on an open, low-cost, fully SMT-assembled balance, with the
      power-feed geometry and current as the controlled variables*, alongside the
      instrument claim (for example: an open µN-scale force balance with
      characterized vibrational, thermal and magnetic couplings at a parts cost
      under $X). The cited literature in `spacetime_circuits_dependency.md` is where
      those mechanisms are documented; cite the specific papers. Fill in $X and the
      force scale from G3, not before.
- [ ] **G2 — First mechanical design, with a model.** The mechanics are the
      experiment, so this comes before the PCB. A concrete design (OpenSCAD or
      CadQuery source in the repo, printable on the K1): balance type (beam on a
      knife edge or flexure, or a torsion pendulum on a fibre or flexure pivot), arm
      lengths, pivot stiffness (flexure geometry and material), mass and moment of
      inertia, resonant frequency and Q, the displacement-to-force conversion, the
      calibration actuator's position and lever arm, sensor locations (optical
      readout at the arm's end, accelerometer on the base, field and temperature
      sensors near the device under test), and the isolation concept (a printed
      or bought passive stage; what `VIBISO` becomes). An analytic model at
      minimum (spring constant, resonance, thermal-expansion paths of PLA versus
      a stiffer material, the magnetic coupling geometry of the calibration
      coil); FEA where the analytic model is doubtful. The PCB's mounting holes,
      head-board sizes and connector positions are then set by this design.
- [ ] **G3 — End-to-end force-noise prediction and a go/no-go.** Chain every noise
      source to force: photodiode shot noise and LED intensity noise; TIA thermal
      and op-amp voltage/current noise; ADC noise; digital lock-in bandwidth; then
      displacement noise, through the mechanical transfer function of G2, to force
      noise in N/√Hz versus frequency. Add the environmental terms: floor
      vibration (seismic/building noise spectra from the literature, attenuated by
      the isolation concept), thermal drift (temperature spectrum × expansion
      coefficients), air currents, magnetic noise × the balance's magnetic moment.
      Compare against `tools/resolution_budget.py`'s table and against at least two
      published balances from the cited papers (take their reported noise floors
      from the papers, don't recall them). **Go/no-go:** if the predicted floor
      can't support G1's claim, change the mechanics, optics or environment (G2/A2)
      and repeat; don't proceed to parts or schematic until it does. Record the
      decision and the numbers.

#### A2. Environment control and absolute metrology (plan them; cost them)

- [ ] **Environment.** For each dominant term from G3, a control and its expected
      suppression: a closed enclosure against air currents (printed or acrylic box,
      draught shield), thermal mass and insulation with logged temperatures, a
      magnetic strategy (passive mu-metal is costly; active compensation with a
      Helmholtz pair driven by the board's coil driver, fed back from the field
      sensor, is the low-cost option; at minimum, measure and report the field),
      a heavy reference surface on soft feet, and vacuum flagged explicitly as out
      of scope for the first iteration with its expected effect stated (air damping
      and convection). Only the controls G3 shows to be necessary for G1 go into
      the first build.
- [ ] **Absolute calibration and uncertainty budget.** The coil-and-magnet actuator
      is a relative calibration; establish the absolute scale independently. Two
      candidates: (1) a known force from gravity, by tilting the balance a measured
      angle (measured with the board's accelerometer) or by placing small known
      masses; (2) the coil's force constant measured against (1), then used in-situ.
      Current measured on a precision shunt (0.1% or better, characterized against
      a reference), displacement scale from the optical readout calibrated with a
      known displacement (a micrometer stage or a printed step gauge). Write the
      uncertainty budget for the calibration constant, and for its drift over a
      measurement campaign (repeat calibration intervals, temperature dependence).

#### A3. Architecture (after the gates; verify every part before committing)

Main board, 4-layer (signal / GND / power / signal), size set by G2, plus small
SMT sensor-head boards in the same order:

- **MCU: RP2040 on the board** from Raspberry Pi's published minimal design (fetch
  their KiCad files from the "Hardware design with RP2040" document; check the
  licence): QSPI flash, 12MHz crystal, USB-C, BOOTSEL and RESET buttons, SWD pads.
  Keeps every RP2040 register address this repo's code uses (not RP2350: see
  `kb/rp2350_notes.md`). Fallback if layout risk looks too high: a Pico socket.
- **Power:** USB-C 5V in (ESD protection, polyfuse), separate 3.3V regulators for
  digital and analog (low-noise LDO for analog), ferrite split, one ground plane
  with a defined star point near the ADC. G3 sets how low the analog rail's noise
  must be.
- **Precision ADC:** compare ADS131M04 (24-bit, 4 simultaneous channels, up to
  32kSa/s, SPI: fits the digital lock-in and vibration channels; read by PIO+DMA per
  `kb/rp2040_performance_notes.md`), ADS1220 (24-bit, slower) and ADS1115 (too slow
  for a kHz lock-in). G3 decides whether its noise matters. Slow housekeeping on
  the RP2040's own ADC.
- **Op-amps:** rail-to-rail CMOS parts JLC stocks (candidates: OPA2376, OPA2333,
  TLV9062, MCP6022), chosen on G3's noise numbers; simulate with the vendor's model.
- **Front ends**, all SMT, on the main board or the heads per G2's sensor
  locations:
  1. Optical readout (number of channels from G2): modulated SMD LED or IR emitter
     with a DAC-set current sink (PIO-gated), SMD photodiode, TIA and anti-alias
     filter into the ADC; demodulated in firmware (digital lock-in).
  2. Magnetic field: SMD linear Hall sensors (or a 3-axis magnetometer chip if G3
     needs better resolution) near the device under test; ratiometric amplifier with
     a DAC-set null where an analog sensor is used.
  3. Vibration: MEMS accelerometer on the base (noise density chosen from G3;
     ADXL355-class if needed) and optionally one on the beam.
  4. Temperature: 0603 NTCs or digital temperature sensors at the points G2/G3 name.
- **Actuators and stimulus:**
  1. Calibration-coil driver: a linear current source (op-amp + MOSFET + precision
     shunt, DAC-set), bipolar if possible; the same driver can feed the Helmholtz
     compensation if A2 adopts it. The coil itself (wound bobbin or ready-made) is a
     sourcing decision for the user.
  2. Disturbance injection: drivers for vibration actuators (the coin motors via a
     screw terminal, or a JLC-stocked SMD motor/buzzer if preferred) and a
     controllable heater (SMD resistor) for thermal-coupling tests.
  3. Test currents for G1's spurious-force study: a driver that passes a known
     current through a dummy load and leads of chosen geometry.
  4. Stimulus DAC: a DC-capable DAC chip is required (LED current, coil current,
     Hall null); the PIO+DMA R-2R (`signal_generator_r2r`) is optional and costs 8
     GPIOs.
- **Bring-up aids:** labelled test pads on every analog node, SWD header, status
  LEDs, spare-GPIO header, mounting holes from G2.
- **Pin budget** early: 30 GPIOs for ADC SPI, DAC, LED modulation, actuator PWMs,
  I2C, housekeeping ADC pins.

#### A4. Toolchain in WSL (verify each step and record versions)

- [ ] KiCad 8 or 9 with `kicad-cli` (`sch erc`, `pcb drc`, export of
      Gerbers/drill/positions/BOM/PDF, `pcb render` to PNG for in-session visual
      review).
- [ ] Parts data: `easyeda2kicad` (symbols/footprints/3D by LCSC number) and the
      `jlcparts` database (stock, basic versus extended; extended parts carry a
      per-part setup fee, so count them).
- [ ] Design entry: script-generated netlist (SKiDL) imported into pcbnew, or KiCad
      schematics written through a file library such as `kiutils`. Criteria: ERC
      runs, a readable PDF schematic comes out, edits are diffable.
- [ ] Routing: critical nets (USB pair, crystal, ADC inputs, reference, TIA inputs)
      placed and routed deliberately; the rest may go through Freerouting. Design
      rules from JLC's current published capabilities (fetched, not recalled).
- [ ] Simulation: ngspice with vendor op-amp models (`set ngbehavior=ps` for
      PSpice-format models); every analog block gets a netlist and a pass/fail
      `smoke_test.py`.
- [ ] Mechanics: OpenSCAD or CadQuery in the repo, with a script that exports STLs
      and computes the G2 model numbers from the same parameters.

#### A5. Prototype check before the order (de-risks iteration)

- [ ] Before committing to layout, test G2's mechanics and the optical readout's
      displacement sensitivity with what is already on the bench: a printed beam,
      the breadboard optical readout and lock-in (`optical_shadow_readout`, no
      soldering), the Pico. Compare the measured resonance, Q and displacement noise
      with the G2/G3 predictions. A disagreement over a factor of a few sends the
      design back to G2/G3, not to the fab.

#### A6. Work packages (after A1–A5, each PR-sized, in order)

- [ ] WP1 — Requirements, block diagram, pin budget, power budget (USB 500mA versus
      coil, heater and actuators), all traced to G1–G3.
- [ ] WP2 — Part selection table (`hardware/<board>/parts.md`): LCSC number,
      basic/extended, stock, price, datasheet limits at 3.3V, noise figures used in
      G3, vendor SPICE model location.
- [ ] WP3 — Simulations of each analog block with the chosen parts; check each
      against its G3 noise allocation.
- [ ] WP4 — Schematic, hierarchical by block; ERC clean; PDF committed.
- [ ] WP5 — Layout: RP2040 per the reference layout, ADC per its datasheet, analog
      and digital partition, decoupling, USB pair, mounting holes and connector
      positions from G2, silkscreen pin names; DRC clean against JLC's rules.
- [ ] WP6 — Visual review from `kicad-cli pcb render` images and a written checklist.
- [ ] WP7 — Fabrication outputs in `hardware/<board>/fab/`: Gerbers + drill, BOM and
      CPL in JLC's format (rotations checked against JLC's placement preview), and an
      order-settings README (layers, thickness, finish, assembly sides, quantity
      minimums checked at the time).
- [ ] WP8 — Firmware and host software: bring-up scripts per block with
      `[PASS]`/`[FAIL]` lines; fixed-point digital lock-in; ADC by PIO+DMA; USB
      streaming to a host-side Python logger (timestamped CSV or HDF5); analysis
      scripts that produce the G1 numbers (noise spectra, calibration, coupling
      coefficients with uncertainties).
- [ ] WP9 — Bring-up and experiment procedures for the user, including the
      calibration sequence from A2 and the measurement campaign (durations,
      repeats, conditions logged).
- [ ] WP10 — The order: a "Next order" entry in `TODO-arcticoder.md` with the JLC
      upload steps and settings (the user gets the quote), plus off-board items
      (coil, cables, enclosure materials, calibration masses) for an AliExpress cart
      in the same window.
- [ ] WP11 — The paper: a LaTeX skeleton (`docs/paper/`) started at G1 and filled as
      results come in: apparatus (from G2/A3), noise model (G3) against measurement,
      calibration and its uncertainty (A2), systematics, the G1 result, and
      open-source availability.

#### A7. Decisions to put to the user (one line each in TODO-arcticoder, when reached)

The G1 measurement goal; the G3 go/no-go outcome; which environment controls the
first build includes (A2); a budget ceiling for the order; RP2040 on the board
versus a Pico socket; the coil's source; whether the on-hand coin motors and N42
discs are used as off-board mechanical parts.

### Part B — lock-in amplifier: reading of the 2026-10-22 level walk

User readings with `diagnose_levels.py`: + rail 3.300V, `VMR` 1.142V, `VMO`
1.143V, `OUT1` 1.134V, `U2` pin 8 and `S1`/`S2` pin 14 at 3.300V, `U2` pin 4 and
`S1`/`S2` pin 7 at 0.017V: all correct. `INN` read 0.758V, which is exactly what
`GP28` read on 2026-10-19 with its jumper touching nothing (`trace_node.py` rest
0.758V), and a truly floating `INN` could not leave `OUT1` at Vmid: so that reading
was almost certainly a jumper without contact. The `A`/`B` numbers it printed are
meaningless: the script opens both switches, so `A` and `B` sit on their 1µF
capacitors and drift (0.39V to 1.84V between runs). Conclusion: the DC chain is
healthy now; the 2026-10-19 state (`OUT1` at 0.024V) is gone, most likely re-seated
during the walk. This rig has now had intermittent contacts three times.

- [ ] B1 — Fix `diagnose_levels.py` (my flaw): (a) after the rest reading, apply
      `GP28`'s pad pull-up and pull-down (as `trace_node.py` does) and print "the
      jumper is not on a driven node" when the rest is not ground/Vmid/rail and the
      pulls move it by volts (note: `INN`/`C2` are also soft under the pulls but rest
      at Vmid); (b) read `A` and `B` with `S1` and `S2` closed, so each reads `OUT1`
      through its switch (a real check of both switch paths), and stop printing the
      switches-open values; (c) host-side test of the classification.
- [ ] B2 — `breadboard.md` § "After the fix": add the readings that are not 0V (the
      0.75–0.76V floating-pad value; `A`/`B` drift with the switches open), so the
      table covers what the user actually saw.
- [ ] B3 — `TODO-arcticoder.md` item 1: the walk passed; next is `mpremote run
      main.py`; if `VA`/`VB` are not near Vmid at `floor`, `mpremote mount . run
      diagnose_demod.py`; re-probe `INN` only with the jumper pushed firmly into the
      `INN` strip.
- [ ] B4 — If the user leaves the rig plugged in, run `main.py` and the
      switch-closed probe from the session before asking anything.
- [ ] B5 — Keep items 1–2 (lock-in, optical readout) in the queue: the optical
      readout's measured light level is the one number the PCB's optical channel
      needs, and the working breadboard lock-in is the reference for the digital
      lock-in firmware.

### Part C — housekeeping from the same report

- [ ] C1 — ADS1115 module: headers soldered with bridges. Tell the user not to power
      it until a photo shows which pins are bridged (a `VDD`–`GND` bridge shorts the
      3V3 rail). Move `TODO-arcticoder.md` items 3 (headers + Zero flash) and 4
      (`adc_ads1115` on the Zero) to "Deferred" with one line each: the PCB carries
      its own ADC, and no more hand soldering. Same for `ACCELIF` (the GY-521 has
      bridged pins since 2026-09-24): Deferred, superseded by the board's
      accelerometer.
- [ ] C2 — RP2040-Zero (headers loose, not soldered): stays in inventory; usable
      later on a fab board with a socket, or press-fit for a temporary test only.
      Remove the soldering wording from `parts_reference.md#rp2040-zero` "First
      power-up" (step 1).
- [ ] C3 — `signal_generator_r2r`: its ladder build needs no soldering (breadboard),
      so it can run on the Pico once items 1–2 are done; reword item 5 accordingly.
      Its PIO+DMA code carries over to the board whichever stimulus option WP2
      picks.
- [ ] C4 — `inventory.md`: note the ADS1115 module and GY-521 as "headers bridged,
      not usable as is".

---

## Open items

### `THERM` — main.py has no debounce on the alarm decision, non-urgent

Surfaced 2026-09-21 during `THERM`'s bench-test run (see
`kb/bench_photo_diagnostics_notes.md`'s matching entry): a momentary
contact glitch during finger-pinch handling produced one wildly-off
sample (698639Ω/−47.4°C) sandwiched between physically-sane readings.
Harmless this time (the glitch read cold, not hot), but `main.py`'s
alarm LED currently fires off a single print's reading with no
consecutive-reads guard, so a same-class glitch reading *hot* would
trigger a spurious momentary trip with no real over-temperature behind
it. Not blocking `THERM`'s own PASS (the sensor/divider path is
confirmed working) and not urgent — this bench doesn't yet run `THERM`
unattended against a real hazard. Worth a small debounce (e.g. N
consecutive over-threshold reads before lighting the LED) before this
circuit is ever trusted as an unattended monitor; pick N against how
often this kind of breadboard contact glitch actually recurs rather than
guessing a number now.

### `lockin_amplifier` — `Rbias` fixed; mid-rail reference at 0V after a fall (2026-10-19)

`Rbias` was a 10kΩ (read 10.15kΩ on `resistance_measurement`); replaced with a 1kΩ,
and `trace_node.py` on row 49-j reads the design values. Then the board fell,
`S2`'s pins were dislodged, and after re-seating them both averagers read about
0.03V; a live check showed `OUT1` at 0.024V with either switch closed, so the
`VMO` reference is at ground. The user finds the leg with `diagnose_levels.py` and
the table in `breadboard.md`. Not probed further: the `GP28` jumper was off the
board. When the user reports back: README status, `TODO-completed.md`, the kb;
then `optical_shadow_readout` is startable, and `signal_generator_r2r` can drive
the lock-in's `SIG` row.

### `RP2040-Zero` — per-circuit pass done for `adc_ads1115` and `charge_amplifier` (2026-10-19)

Both circuits only use pins the Zero has (`GP4`, `GP5`, `GP26`, `GP28`, `3V3`, `GND`),
so `main.py` is unchanged; their `breadboard.md` files gained an "On the RP2040-Zero"
section by silkscreen name. First power-up steps (headers, firmware UF2, usbipd, picking a
board with `mpremote connect id:`) are in `parts_reference.md#rp2040-zero`. Other
circuits get the same pass only when the user says one moves to the Zero; the ones that
use `GP16` (`frequency_counter`, `vibration_driver`) need a pin remap, not just names.

### `RP2350` chip guard — when an RP2350 board is in hand

Not started: no RP2350 board is on hand or ordered. Raw-register scripts write RP2040
peripheral addresses (`0x40050000` is `PLL_SYS` on the RP2350). Before such a board runs
any of them, add a chip check to each (`lockin_amplifier`, `frequency_counter`,
`signal_generator_r2r`, `trace_node.py`) and audit `Pin.PULL_DOWN` uses against erratum E9.
Facts in `kb/rp2350_notes.md`.

### Next design pass — what to pick and why (2026-10-19)

Queue state 2026-10-19: eleven on-hand builds, nothing en route, no purchase pending.
The user rejects buying cheap AliExpress modules whose shipping makes them cost more than
their listing (they want builds from parts on hand where a software route exists), so the
2026-10-17 `TESTSIG` plan around an AD9833 module became `signal_generator_r2r`, a software
DDS on an R-2R ladder. A purchase therefore comes only from a design that cannot be made
from stock; none of the candidates below needs one. Two bought-part ideas looked at and
left:

- **`THERMOAMP`** (a K-thermocouple interface; MAX6675 module plus probe): graph node, cheap,
  Pico SPI. Held back because its data sheet could not be fetched on 2026-10-17 (a part isn't
  listed from recall), and because a module of that price carries the same shipping problem.
  Resolution is 0.25°C and the range 0–1024°C, so it suits hot parts, not calorimetry
  (`MF52AT` thermistors are finer near room temperature).
- **A load-cell front end (HX711 + load cell)**: not on the dependency graph, so it needs a
  graph decision before a design.

Candidates already on this file, none blocked on a decision:

- **`AAF`** (tier6 anti-alias filter) — an LM358 Sallen-Key low-pass
  ahead of `adc_ads1115`, corner chosen against the ADS1115's data rate
  (128 SPS → Nyquist 64Hz, so a corner near 25Hz). Design and simulation can
  start now; its bench check waits on the module. On-hand parts (100kΩ, ceramic
  capacitors up to 100nF; check the corner is reachable with them).
- **`OVERCUR` / `AM`** (current monitor) — a 0.1Ω low-side shunt (1W, on hand)
  into the difference-stage topology of `hall_amplifier`, referenced at 0.93V.
  Reason for that topology: a plain non-inverting amplifier on a few millivolts
  loses its low end to the LM358's input offset and its 0.02V output floor
  (an offset of −2mV at gain 50 pins the output at the floor for the first
  20mA); a referenced difference stage doesn't. Calibrate against a known
  load (100Ω resistors in parallel from the 3V3 pin: 33mA, 66mA, 132mA).
- **`TIMEINT` / `JITTER`** — pulse width and edge-to-edge time from the same
  PWM-slice machinery as `frequency_counter` (level-gated mode counts system
  clocks while the pin is high: 8ns resolution, 0.5ms span at no divider);
  Pico-only, so no purchase; verify with the logic analyzer.
- **`REFGEN2` / `VM`** — TL431A on the Pico's `ADC_VREF` pin (Pico datasheet
  §4.3: the board feeds `ADC_VREF` from 3V3 through 201Ω with a 2.2µF
  capacitor and a 1Ω series resistor, and says an external shunt reference
  may be connected there; with 2.495V the ADC range becomes 0–2.495V). Open
  risk: a TL431 can oscillate with a few µF on its cathode, and that
  capacitor is on the board; the design must include a stability check (ADC
  noise with and without it) and name the fallback (an LM4040-3.0, which the
  Pico datasheet recommends). Wait for `overvoltage_monitor`'s first run: it
  is the first use of the TL431A batch.
- **`SAMHOLD`** — CD4066B switch, hold capacitor, LM358 follower, Pico-timed;
  droop measured by the ADC.
- **`IA`** — **not with an INA126.** Checked 2026-10-02 against TI's datasheet:
  its input common-mode range stays about 1.5V inside each supply rail
  (Figure 5-7), which leaves a 0.3V window on 3.3V. At 3.3V the difference
  stage in `hall_amplifier` is the usable instrumentation-amplifier building
  block; a real IA needs a 5V supply (the Pico's VBUS pin) and an output
  divider for the ADC. Don't put an INA126 on the AliExpress list for 3.3V use.

### AA-battery power budget

Tally recorded 2026-10-01 in `kb/power_rail_budget_notes.md`. The earlier
claim that this bench can't run off AA cells was over-broad: it was true
only of `ACTIVELIM`'s 2A check. Keep that file current as designs are added;
the SparkFun kit (shelved 2026-10-01) is revived by a design that breaks the
budget, not by the tier label `psu_medlow`.

### `FORCEBAL` / `SIPMFE` / `LASERDRV` — new tier5/7 nodes (2026-09-18); `SIPMFE`/`LASERDRV` blocked on part sourcing; `FORCEBAL`'s optical readout designed 2026-10-02 as `optical_shadow_readout` (the balance's mechanics are still open)

Added to `spacetime_circuits_dependency.md` 2026-09-18 (see that file's
"Why these new tiers" section) at the user's explicit direction, alongside
two non-circuit mechanical build objectives (`VIBISO`, `RIPPLETANK`, no
`TODO-agent.md` item — nothing to design/simulate for those). Same
situation as `HVPULSE` below in one respect (not startable yet) but for a
different reason: this isn't a scope judgment call, it's that **none of
the three have a specific part sourced yet**, and this file's own workflow
(design/simulate against a real component's real values, the same way
every completed entry below was built) needs one to mean anything —
`FORCEBAL`'s design depends on which displacement-sensing approach gets
picked, and `SIPMFE`/`LASERDRV` both need an actual SiPM/laser-diode part
number before bias/drive values can be simulated. **Don't start a netlist
for any of the three from the tier-graph label alone** — check
`TODO-arcticoder.md`'s "Next order" and "Blocked" sections
first; move this entry to a real open item once a part from any of them
is confirmed received.

**Corrected 2026-10-01: `CAPBRIDGE` is not a displacement readout route.**
An earlier pass listed "a capacitive plate read by `CAPBRIDGE`" as the
no-purchase way to instrument `FORCEBAL`. `CAPBRIDGE` times an RC charge
through 100kΩ with ~1ms ADC polling and its README rates anything near
10pF "No"; a foil plate pair is 3–90pF (see `spacetime_circuits_dependency.md`'s
"Bench-scale resolution budget", reproduced by `tools/resolution_budget.py`),
a charge time of microseconds. So the no-purchase capacitive route needs a
different transduction (a 555 astable with the plate as timing capacitance,
frequency read in hardware), which is a new circuit, not a reuse. The
purchase-free route that *does* reuse built circuits is an optical
readout: on-hand LED + a flag/shadow on the balance beam + on-hand PT334-6C
photodiode into the bench-tested `TIA`. That is a startable design item
(netlist, `breadboard.md`, `smoke_test.py`) independent of the mechanical
balance, and its output range maps directly onto the budget's `R` and `k`
table. Recommendation when it's picked up: the optical shadow readout
first, since every part is on hand and `TIA` is already validated; the 555
C-to-f route second, and only if the optical one proves insufficient.

### `HVPULSE` — tier7/8 high-voltage pulse generator

**Still blocked on a scope decision, not a part.** The only IRLZ44N
currently *wired* is in [ACTIVELIM](../protection/active_current_limiter/)
(see that circuit's README § Design notes for why it was designed
first) — but per this repo's ephemeral-circuit convention (nothing stays
assembled once its own bench check passes and nothing else currently
needs it wired — see `README.md` § Circuits — built & bench-tested),
that single on-hand IRLZ44N returns to inventory once `ACTIVELIM` is
bench-validated, and can then be reused here. **A second unit is only
actually required if `ACTIVELIM` and `HVPULSE` need to be physically
assembled at the same time** — not the case today: both protect/generate
for PSU tiers (`psu_medhigh`/`psu_high`) that are themselves still
backlog with no folder, and this repo doesn't run the experiments that
would ever need two such circuits live simultaneously (see
[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)).
Ordering a second IRLZ44N ahead of that is optional, not a blocker.

More fundamentally: nothing on this bench currently defines what "high
voltage" means here numerically. **This bench's numeric threshold: above
50V DC / 30V AC RMS counts as high voltage** — the same limit IEC 61140's
SELV (safety extra-low voltage) classification uses. Reasoning: dry-skin
resistance runs roughly 100kΩ–600kΩ, but broken/damp-skin contact
resistance can fall to ~1,000Ω — at 1,000Ω, 50V drives 50mA, inside the
30–50mA range that can paralyze respiratory muscles and bordering the
50–100mA range that can induce ventricular fibrillation. Nothing on the
bench today exceeds this threshold (the Lenovo 65W adapter tops out at
20V; no PSU circuit is built around it yet — see
`docs/general_purpose_circuit_dependency.md`'s `PSUMEDHIGH` node) and no
HV source of any kind is in inventory; no isolation/discharge-path safety
design has been done either. **Don't start a netlist for this without
first getting an actual target peak voltage/energy figure and a real
safety design pass (isolation, discharge paths) from the human** — this
is a judgment call, not something to infer from the tier graph's generic
label.

**Once scoped, a netlist/BOM here is fine even with no near-term
physical-assembly plans** — the point is dependency-graph/build-order
clarity, not an assembly commitment (see
[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)
for the repo-scope reasoning). Physical assembly of anything exceeding
the 50V/30V threshold above stays out of scope until the human decides
to raise the hazard level of assembled circuits on this bench — don't
add a "physically assemble" bullet for it to `TODO-arcticoder.md` on the
strength of a netlist alone.

---

## Completed (moved out)

- **2026-10-19**: `measurement_tools/signal_generator_r2r/` (`TESTSIG`): a software DDS,
  PIO + two chained DMA channels playing a sine table to an 8-bit R-2R ladder (1kΩ/2kΩ)
  and an LM358P buffer, calibrated against the Pico's ADC. Built after the user rejected
  the AD9833-module plan (cost with shipping); every part is on hand. Checked on a Pico:
  `loopback_test.py` reads the output pins back through a second PIO state machine and DMA
  and matched the table exactly at 2.0 to 62.5MS/s (256-byte table), 31.3 and 62.5MS/s
  (32-byte table, a DMA hand-off every 8 words, a 1.95MHz sine) and with the 4096-byte
  table a 1kHz sine uses; an altered sample is caught (negative control). The RP2040
  datasheet corrected my first design: a DMA channel can't chain to itself, so two channels
  chain to each other. Real hardware also found what the host tests couldn't: MicroPython
  `int` has no `bit_length()` and `bytes` no stepped slices. Simulation: with 5% resistors the
  sine's distortion falls from −39dB to −57dB (the 8-bit floor) once calibrated; the Python
  ladder model agrees with ngspice to under 0.01mV. Not run: the analog side. Also written
  this pass: `diagnose_levels.py` and `diagnose_demod.py` for the lock-in, `kb/rp2350_notes.md`,
  `kb/inventory_storage_notes.md` and `kb/rp2040_performance_notes.md`.

- **2026-10-02**: five circuits designed, simulated, smoke-tested and
  documented, all `main.py` files compiled under MicroPython on the Pico and
  exercised against mocks (not run against the circuits):
  `signal_conditioning/lockin_amplifier/` (`LOCKIN`/`DEMOD`),
  `signal_conditioning/optical_shadow_readout/` (`FORCEBAL`'s optical
  readout, resolving the open item from 2026-10-01),
  `signal_conditioning/hall_amplifier/` (`HALLAMP`, for the SS49E now on
  order), `measurement_tools/frequency_counter/` (`FREQC`/`SIMPLECNT`) and
  `safety/overvoltage_monitor/` (`OVERVOLT`). Also revised
  `oscillators/vibration_driver/` for the ordered motor's 120mA stall current.
  The checks caught faults that would otherwise have reached the bench:
  `lockin_amplifier`'s averagers settle with a 0.21s time constant (not the
  0.1s of RC), so readings need 1.6s; `frequency_counter`'s first auto-range
  wrapped its 16-bit counter on any input above 3MHz, and an AC-coupled
  Schmitt trigger chattered on 8mV of noise or latched high, so the analog
  path is DC-coupled with a trimpot level; `hall_amplifier`'s first
  null scheme couldn't null a sensor at the datasheet's +0.25V extreme (the
  LM358 can't output 1.8V+), a second one unbalanced the amplifier's legs
  (+10% gain, a common-mode gain of 1), so the first came back with its limit
  documented; `optical_shadow_readout`'s TIA lost 20% of the signal in a dark
  room until its reference moved off ground (0.1V reverse bias), and a polarized
  coupling capacitor would have been reverse-biased (two electrolytics
  anti-series); `overvoltage_monitor`'s 1kΩ LED base resistor held its TRIP
  line at 0.92V, below a logic high (100kΩ fixes it). Datasheet checks (TI,
  Honeywell, Raspberry Pi) replaced recalled pinouts: the CD4066B `VSS` is
  pin 7 (the repo had pin 6), the TL431A's TO-92 pinout was added, the
  SS49E's null/sensitivity/span at 3.3V were taken from its datasheet.
  See `kb/lm358_single_supply_design_notes.md` and
  `kb/datasheet_and_live_probe_notes.md` for the method and findings.

- **2026-10-01** (second pass): `oscillators/vibration_driver/`
  (`SIMPGEN`'s actuator stage, the `RIPPLETANK` dipper driver) and
  `signal_conditioning/adc_ads1115/` (`ADCDRV`, a 16-bit external ADC with a
  protected input) — both designed, simulated (`ngspice -b`, numbers
  confirmed against hand calculation), smoke-tested (green) and documented;
  `main.py` files exercised against host mocks only. The motor was chosen
  (a 3V coin vibration motor, the open question in the former `SIMPGEN`
  entry): the servo option was dropped because it needs a supply this bench
  doesn't have, and the motor needs only the 3V3 pin. Their parts are added
  to `TODO-arcticoder.md`'s "Next order". Also fixed the `logic_analyzer_check`
  host script so it prints sigrok's own error (the first run's traceback
  hid a usbipd re-enumeration failure) and added `--find-channel`.

- **2026-10-01**: `measurement_tools/logic_analyzer_check/` (`SCOPELA`'s
  first capture) — not a circuit, so no netlist: a Pico 1kHz/25% PWM
  script, a host-side `sigrok-cli` capture/analysis script, and a
  smoke test (analysis checks, mocked-`machine` check of `main.py`, csv
  parser against real `sigrok-cli` demo output; the live-capture check
  SKIPs without the board). Added to `TODO-arcticoder.md`'s "Ready to
  build now"; nothing downstream needs it — it's an instrument bring-up.
- **2026-09-23**: `measurement_tools/inductance_bridge/` (`INDBRIDGE`)
  and `signal_conditioning/accelerometer_interface/` (`ACCELIF`) —
  designed, simulated, smoke-tested (green) and documented. Both
  `main.py` files were exercised against host-side mocks only. See
  [TODO-completed.md](TODO-completed.md) for the design decisions and
  `TODO-arcticoder.md`'s "Ready to build now" / "Deferred" for their
  assembly status. The same pass corrected `protection/active_current_
  limiter/` (LM358 supply, TL431A pull-up, and a validation plan that
  fits a 2A-rated source).
- **2026-09-13**: `signal_conditioning/transimpedance_amplifier/` (`TIA`)
  and `measurement_tools/capacitance_bridge/` (`CAPBRIDGE`) — both
  designed, simulated (`ngspice -b`, confirmed against hand-derived
  expected values), smoke-tested (green), and documented
  (`README.md`/`breadboard.md`/`main.py`). See
  [TODO-completed.md](TODO-completed.md) for the full entry and
  `TODO-arcticoder.md`'s "Ready to build now" for their new
  physically-assemble bullets.
- **2026-09-13** (second pass, same day): `signal_conditioning/
  electric_field_probe/` (`EPFIELD`, tier5), `signal_conditioning/
  charge_amplifier/` (`CHGAMP`, tier5), `safety/thermal_monitor/`
  (`THERM`), `signal_conditioning/phase_detector/` (`PHASED`, tier4),
  and `protection/active_current_limiter/` (`ACTIVELIM`) — all five
  designed, simulated, smoke-tested (green), and documented. This was
  the direct spacetime-research sensor chain (`EPFIELD`/`CHGAMP` are
  named tier5 nodes in `spacetime_circuits_dependency.md`, not general
  infrastructure) plus the `PHASED` node that unlocks tier6 `LOCKIN`
  processing of their output — see
  [kb/spacetime_sensor_chain_notes.md](kb/spacetime_sensor_chain_notes.md)
  for the design decisions made along the way (single-supply ADC-safety
  bias pattern, the resolved "second oscillator" question for `PHASED`,
  and a real hard-trip chattering limitation `ACTIVELIM`'s own
  simulation surfaced). `HVPULSE` (shares `ACTIVELIM`'s MOSFET) remains
  open above — it needs a scope decision, not more design time. See
  [TODO-completed.md](TODO-completed.md) for the full entry and
  `TODO-arcticoder.md`'s "Ready to build now" for the new
  physically-assemble bullets.
