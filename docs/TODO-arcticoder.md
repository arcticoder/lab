# TODO — arcticoder

Single human-facing checklist for this repo: things that need your hands,
eyes, or a purchasing decision — ordering, physically assembling/wiring a
circuit, and bench validation. File-creation work (a netlist, a
breadboard guide, a smoke test, a folder for a new circuit) is **not**
on this list — that's Claude's job, tracked in
[TODO-agent.md](TODO-agent.md) and done proactively before a build ever
shows up here. See
[docs/kb/todo_list_conventions.md](kb/todo_list_conventions.md) for the
reasoning/history behind this file's structure — that's where it lives
now, not in this file itself.

Worked strictly top-to-bottom, one section at a time. A "Next order"
section goes first whenever a purchase has to happen before anything else
(AliExpress transit runs a few weeks); it is absent while nothing is
waiting on one, and it appears whenever nothing is en route. "Ready to build now" is a ranked queue, not a menu — item 1
is genuinely the most valuable thing to build next; see
[kb/todo_list_conventions.md](kb/todo_list_conventions.md) for the ranking
method if you want it. "En route" (when something is), "Blocked", "Deferred", and "Backlog" are
reference sections, not action items, until something changes their
status — they're placed *after* every actionable section on purpose, so
you never have to read past a "no action needed" note to reach the next
real task.

When an item is done, move it to [TODO-completed.md](TODO-completed.md)
(dated entry) instead of deleting it. Completed circuits' bench-test
status lives in `README.md`'s "built & bench-tested" table.

---

## Next order — AliExpress, nothing needed; one optional board

Nothing is en route and no build below waits on an order.

- **RP2350-Zero ×1** (the listing you found, [orders.md](orders.md) "Candidates
  found") — a third controller for parallel builds. Add it only to a cart that has
  another need, so shipping isn't paid alone; check the total first. Before it runs
  any raw-register `main.py` here, those scripts need a chip check
  ([kb/rp2350_notes.md](kb/rp2350_notes.md)); that is an agent task, done when one is in hand.

## Ready to build now — parts on hand

Two controllers are free to use: the Pico stays on the lock-in (items 1–2), the
RP2040-Zero takes one other build at a time (items 3–5 and on), by silkscreen name
and with `mpremote connect id:<serial>` when both are attached. Builds that need `GP16`
(items 9 and 11) run on the Pico or remap that pin.

1. [ ] **`signal_conditioning/lockin_amplifier` (`LOCKIN`/`DEMOD`) — find
       why the mid-rail reference is at 0V after the board fell.** `Rbias`
       is fixed (the 10kΩ is out, `trace_node.py` reads the design values), but
       `main.py` reads both averagers near 0.03V, and a live check on 2026-10-19
       showed `OUT1` sitting at 0.024V with either switch closed. Put the `GP28`
       jumper (it was off the board; row 49, column j is `SIG`) on each row in turn
       (`+` rail, `VMR`, `VMO`, `INN`, `OUT1`, the chips' supply pins),
       `mpremote run diagnose_levels.py`; the table in
       [breadboard.md](../signal_conditioning/lockin_amplifier/breadboard.md)
       § "After the fix" says what each row should read and which leg to
       re-seat. Then pull the jumper and `mpremote run main.py`; eight `[PASS]`
       lines is done. Leave it assembled; item 2 builds on it.
2. [ ] **`signal_conditioning/optical_shadow_readout` (`FORCEBAL`'s optical
       readout) — change the lock-in's front end.** Needs item 1 wired; no
       other parts to find. Swap the test-signal resistors for a TIA, a
       photodiode and a red LED, add a third LM358, a push button and a card
       flag ([breadboard.md](../signal_conditioning/optical_shadow_readout/breadboard.md)),
       then `mpremote run main.py`; it asks for a phone flashlight and the
       flag. All `[PASS]` lines is done; it also reports how much light the
       LED really puts on the photodiode, the one number the design assumes.
3. [ ] **Solder the headers on the ADS1115 module and the RP2040-Zero, then
       flash and self-test the Zero.** Both need their pins before anything else
       uses them. Steps and the firmware file are in
       [parts_reference.md](parts_reference.md#rp2040-zero) "First power-up". Done
       when `mpremote connect id:<serial> mount . run loopback_test.py` (in
       [signal_generator_r2r](../measurement_tools/signal_generator_r2r/)) prints
       seven `[PASS]` lines on the Zero: no wiring, and it exercises its PIO and DMA.
4. [ ] **`signal_conditioning/adc_ads1115` (`ADCDRV`) — first power-up of the
       module, on the Zero.** It doubles as the genuineness check, and a dud is a
       refund claim; the buyer-protection end date is on the order page (not visible
       to me). 10kΩ ×3, 100nF, 1N5817 ×2
       ([breadboard.md](../signal_conditioning/adc_ads1115/breadboard.md), with the Zero's
       pin names); `mpremote run main.py`. Four `[PASS]` lines is done.
5. [ ] **`measurement_tools/signal_generator_r2r` (`TESTSIG`) — wire the ladder and
       run the bring-up.** Nine 2kΩ, eight 1kΩ, one 10kΩ, an LM358P and 100nF
       ([breadboard.md](../measurement_tools/signal_generator_r2r/breadboard.md)); on the Zero
       after item 4 is torn down. `mpremote mount . run main.py`: eight `[PASS]` lines
       is done, and the run prints the real frequency ceiling. It then drives the lock-in's
       `SIG` row through 200kΩ for a sinusoid test once item 1 passes.
6. [ ] **`signal_conditioning/charge_amplifier` (`CHGAMP`) — retry with a
       leaded piezo disc.** Retry of the 2026-09-16 attempt; the leaded discs
       need no soldering to the disc. TL082, 1MΩ ×3, 10nF
       ([breadboard.md](../signal_conditioning/charge_amplifier/breadboard.md));
       `mpremote run main.py`. All `[PASS]` lines is done.
7. [ ] **`signal_conditioning/accelerometer_interface` (`ACCELIF`) — clear the
       bridged GY-521 pins, then wire four jumpers.** Wick arrived. Lay the
       braid over the bridge, press the iron on it 2–3 seconds, lift both
       together, check the row by eye (steps in
       [breadboard.md](../signal_conditioning/accelerometer_interface/breadboard.md)).
       `VCC`→3V3(OUT) (pin 36), `GND`→pin 38, `SDA`→GP4 (pin 6), `SCL`→GP5
       (pin 7); module lying still; `mpremote run main.py`. All `[PASS]` lines
       is done (a `WHO_AM_I` of `0x70`–`0x72` is a clone that still passes).
       It's the measurement side of `VIBISO`.
8. [ ] **`signal_conditioning/hall_amplifier` (`HALLAMP`) — first run of a
       49E/SS49E, then the magnet test.** Read each sensor's top mark first
       (the SS49E listing also sold latching types), then wire it per
       [breadboard.md](../signal_conditioning/hall_amplifier/breadboard.md),
       `mpremote run main.py`, and turn the trimpot until the reading holds at
       0.94V. `[PASS]` for the noise line, then the magnet test: hold a disc
       with its curved side toward the sensor, not a flat face. Try a second
       sensor if the first can't be nulled.
9. [ ] **`oscillators/vibration_driver` (`SIMPGEN`'s actuator stage) — wire it
       and run it.** The driver `RIPPLETANK` needs; coin motors arrived. S8050,
       1N5817, 1kΩ, 10kΩ ([breadboard.md](../oscillators/vibration_driver/breadboard.md));
       `mpremote run main.py`. All `[PASS]` lines is done.
10. [ ] **`safety/overvoltage_monitor` (`OVERVOLT`) — wire it with its input
       on the Pico's 3V3 pin.** First run of a TL431A from the batch; the 3V3
       rail is the known voltage that proves it trips and clears. TL431A,
       LM358, S8050, trimpot, LED
       ([breadboard.md](../safety/overvoltage_monitor/breadboard.md)); `mpremote
       run main.py`, trimpot to each end when asked. All `[PASS]` lines and
       the LED flipping is done.
11. [ ] **`measurement_tools/frequency_counter` (`FREQC`/`SIMPLECNT`) — wire
       the digital path and run the loopback self-test.** First counting of
       a real signal by the Pico's PWM hardware; also the tool that reads
       `ne555_astable`'s frequency. GP16 → 10kΩ → GP3 with two 1N5817 clamps
       ([breadboard.md](../measurement_tools/frequency_counter/breadboard.md)),
       `mpremote run main.py` (6s). Six `[PASS]` lines is done; the analog
       (Schmitt) path is added later, only when a sensor needs counting.
## Blocked — waiting on another item

- [ ] **`VIBISO`** (vibration isolation platform) — hold off on the
      mechanical build itself until `ACCELIF` (item 7) is assembled and
      passing, so there is something to measure isolation quality with. For
      later: the on-hand Creality K1 (with PLA filament stock) can print
      feet/platform parts once this is actionable.
- [ ] **`RIPPLETANK`** (2D ripple tank) — waits on `vibration_driver` (item
      9): it becomes the wave dipper, driven by that circuit. Whether a
      ~150Hz coin motor makes useful ripples is untested; the mechanical side
      (a dipper arm and tank) is still to be worked out. For later: the
      on-hand Creality K1 (PLA on hand) could print a precise stepped/sloped
      depth insert once this is actionable.

## Deferred — considered and declined, no action needed

- `protection/active_current_limiter` (`ACTIVELIM`) — designed and
  simulated, one IRLZ44N on hand, but nothing on this bench needs its
  protection yet: it exists to guard `psu_medhigh`/`psu_high`, and that
  PSU tier is still Backlog with no folder (see below) — no PSU circuit
  it would protect is even being built right now. Its own bench check
  also needs a ≥2A source this bench doesn't have (the PD trigger board's
  5V tap + 5Ω/8Ω power resistors, still just candidates in `orders.md`,
  not carted); buying those now would be validating a protection circuit
  for a supply that doesn't exist, not a real need. An extra AA battery
  holder doesn't change this — the gap is current capacity and PD
  negotiation, not cell count; AA cells can't safely source the current
  this check needs regardless of how many are wired in series. Revisit
  once `psu_medhigh`/`psu_high` becomes an actual build target.
- `measurement_tools/inductance_bridge` (`INDBRIDGE`) — designed and
  simulated, parts on hand, but nothing on this bench uses an inductor
  yet. Build it when a design needs a verified inductance, or when you
  want the assortment's color bands cross-checked (good to about the
  10nF reference capacitor's tolerance, ±10% or so).
- `power_supplies/psu_medlow_lm317` (SparkFun/RobotShop kit) and
  `psu_medlow_usbc` with the USB-C breakout's CC-pin check — shelved
  2026-10-01 / 2026-09-23. No designed circuit needs a regulated rail above
  what `psu_4xaa` (6V, <300mA) or the Pico's 3V3 pin gives; every circuit
  designed so far fits one of them. A single-item RobotShop order would
  also pay shipping alone. Revisit when a design needs 3.3V/5V above about
  300mA from wall power; the adapter notes are kept in `orders.md`.
- `power_supplies/psu_3xaa` + the remaining 1N5817 diode-drop checks —
  no current rail need (nothing on this bench needs 4.5V specifically;
  `psu_4xaa` at 6.0V already covers what this tier would). A diode gets
  checked at pull-time for whichever build actually uses it, same as
  every other build here — not a standing to-do.
- `power_supplies/psu_ultralow_v1` demo power-on check — no current
  consumer beyond the component-level validation already passed; skip
  until something specifically needs a 1.5V rail.
- CD4066BCN switches 2–4 per chip (only switch 1 of each of the 10
  chips has been run, and that pass used a pinout with `VSS` on the wrong
  pin; corrected 2026-10-02) — nothing needs them yet; `lockin_amplifier`
  uses switch 1 of two chips, so its first run is also the first
  correctly-wired CD4066B check. Validate whichever other switch a future
  build pulls.
- Glass tube fuses (2A fast-blow, 10 on hand) — no test jig; build one
  only once the (backlog) `psu_medlow` protection path is actually being
  assembled.
- TL431A precision shunt reference (5 on hand, untested) — optional
  precision upgrade to the tier1 `REF` divider, not a purchase.
- LVDT transducer — the only tier5 node with zero hardware, instruments
  `FORCEBAL`'s displacement readout (see
  `spacetime_circuits_dependency.md`). Lowest-priority sensor on this
  bench: an optical shadow readout (on-hand LED + PT334-6C photodiode into
  the bench-tested `TIA`) is a no-purchase alternative way to instrument
  `FORCEBAL`, so this only becomes relevant if that route proves
  insufficient. (`CAPBRIDGE` can't do it: a plate pair is pF-range, far
  below its µF-range design.)
- GΩ-range resistor — only becomes relevant if `CHGAMP` (once built)
  and a direct-touch retest of `EPFIELD` both come up empty; not on hand
  or on order.
- Second IRLZ44N MOSFET — not needed. The one unit on hand returns to
  inventory after `ACTIVELIM`'s bench check and can then serve `HVPULSE`.
- SiPM module + scintillator tile (`SIPMFE`) — deferred, the sensor
  alone is pricier than the rest of this bench; revisit later.
- Higher-power LED (`LASERDRV`) — no rush; on-hand 5mm LEDs already give
  a free first test. The laser-diode option is off the table over a real
  eye-safety gap (no enclosure/beam-dump/goggles on this bench) — see
  [kb/todo_list_conventions.md](kb/todo_list_conventions.md).
- Torsion fiber + mirror (`FORCEBAL`) — not needed. A beam balance with an
  optical shadow readout needs no purchase; the readout is designed
  (`optical_shadow_readout`, in "Ready to build now"), the balance's
  mechanics are not.

## Backlog — undesigned, long-tail

Nothing below has a netlist, folder, or sourced part yet. Check
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) for
how each node connects before starting one.

- [ ] **Safety monitoring**: `LEAKDET`, `GFCI`, `ESDMON`, `INSMON`,
      `ARCDECT`, `OVERCUR`, `TEMPCOIL`, `EMSTOP`, `PSUHEALTH`, `FUSESTAT`,
      `RFRAD`, `VACPRES`, `SMOKDET`. (`THERM` is built & bench-tested — see
      `README.md`'s "built & bench-tested" table; `OVERVOLT` is designed, in
      "Ready to build now".)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` — no PSU tier built around
      the Lenovo 65W adapter (on hand) or any industrial supply.
      `ACTIVELIM` (their protection stage) is designed/simulated but has
      nothing to protect yet and isn't a real need until this tier starts
      — see "Deferred" above — and that's not the PSU tier itself anyway.
- [ ] **Bootstrap tier**: `LEDIND`, `TUNINGFK`, `AUDIOSC`, `CRTSC`.
      (`PASSVM` is already done via `fuse_test_voltmeter`; `SIMPLECNT` is
      `frequency_counter`, designed.)
- [ ] **Tier 2**: `VM`, `AM` — undesigned as dedicated circuits (distinct
      from the bootstrap ammeter jigs). `FREQC` is `frequency_counter`,
      designed.
- [ ] **Tier 4**: `IA`, `DA` — undesigned as dedicated circuits (`hall_amplifier`'s
      stage is a difference amplifier built for 3.3V). `DEMOD` is
      `lockin_amplifier`, designed. (`PHASED` is done — see `README.md`'s
      bench-tested table.)
- [ ] **Tier 5** (spacetime): `LVDTAMP` — no transducer sourced (see
      "Deferred" above). `SIPMFE` — zero hardware sourced; see
      `spacetime_circuits_dependency.md`'s "Why these new tiers"
      section for the justification. Not `TODO-agent.md` design tasks
      yet — that workflow needs a specific sourced part first.
      (`FORCEBAL`'s optical readout is `optical_shadow_readout`, designed;
      `HALLAMP` is `hall_amplifier`, designed.)
- [ ] **Tier 6**: `AAF`, `TIMEINT`, `JITTER` — undesigned. `LOCKIN` is
      `lockin_amplifier`, designed.
- [ ] **Tier 7** (spacetime): `RFPWR`, `MIXER`, `SWEEP` — unaddressed, no
      parts identified, lowest priority. `LASERDRV` — backlogged, though
      on-hand 5mm LEDs give a free first test (see "Deferred" above).
- [ ] **Tier 8** (spacetime): `CALORIF`, `PWRFACT`, `ENGINT`, `NOISEFIG`
      — unaddressed, no parts identified.
- [ ] **Tier 9**: `SAMHOLD`, `ADCDRV`, `REFGEN2` — undesigned. `MUX` is
      partially covered by `cd4066_switch_tester` component validation,
      but the actual multiplexer circuit isn't built.
- [ ] **Concurrent measurement tools**: `SCOPEUSBSER`, `SCOPEDSO`,
      `SCOPEBENCH`, `PRECBOX`, `LOADBANK`, `NOISEGEN`, `TESTSIG`,
      `THERMOAMP` — undesigned/unsourced. (`SCOPELA` is bench-validated
      2026-10-02 and is a plug-in tool, not a circuit; none of these
      dedicated designs exist yet.)
