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

Worked strictly top-to-bottom, one section at a time. "Next order" comes
first because it's the only section with a real clock (AliExpress
transit runs a few weeks). "Ready to build now" is a ranked queue, not a
menu — item 1 is genuinely the most valuable thing to build next; see
[kb/todo_list_conventions.md](kb/todo_list_conventions.md) for the
ranking method if you want it. "Blocked", "Deferred", and "Backlog" are
reference sections, not action items, until something changes their
status — they're placed *after* every actionable section on purpose, so
you never have to read past a "no action needed" note to reach the next
real task.

When an item is done, move it to [TODO-completed.md](TODO-completed.md)
(dated entry) instead of deleting it. Completed circuits' bench-test
status lives in `README.md`'s "built & bench-tested" table.

---

## Next order — action needed

- [ ] **AliExpress: add the solder wick and disc magnets to the cart, then
      check the total before paying.** Nothing in "Ready to build now" waits
      on this; it is first only because transit takes weeks. Add: solder wick,
      any basic roll (`ACCELIF`'s first power-up; also clears a bridge if the
      ADS1115's header pins arrive loose and need soldering), and small
      neodymium disc magnets, about 6×3mm, 10–20 pcs (`hall_amplifier`'s
      field source). If checkout shows no shipping fee, pay. If it still
      shows one, don't: the next design pass adds the top-up. Prices weren't
      verifiable from here.

Already en route (ordered 2026-10-02): 10 leaded 12mm piezo discs, 15 linear
Hall sensors (10 × 49E, 5 × SS49E), 1 ADS1115 module, 10 coin vibration
motors. Details and listing numbers in [orders.md](orders.md).

## Ready to build now — parts on hand

1. [ ] **`signal_conditioning/lockin_amplifier` (`LOCKIN`/`DEMOD`) — wire it
       and run it.** Strongest-justified tier6 node, and item 2 builds on it.
       Two LM358, two CD4066B (switch 1 of each; **ground on pin 7**, the
       old pinout was wrong), about 25 resistors and capacitors; wiring
       tables in its [breadboard.md](../signal_conditioning/lockin_amplifier/breadboard.md),
       then `mpremote run main.py` (15s). Eight `[PASS]` lines is done; the
       in-phase reading should be near 260mV. Leave it assembled.
2. [ ] **`signal_conditioning/optical_shadow_readout` (`FORCEBAL`'s optical
       readout) — change the lock-in's front end.** Needs item 1 wired; no
       other parts to find. Swap the test-signal resistors for a TIA, a
       photodiode and a red LED, add a third LM358, a push button and a card
       flag ([breadboard.md](../signal_conditioning/optical_shadow_readout/breadboard.md)),
       then `mpremote run main.py`; it asks for a phone flashlight and the
       flag. All `[PASS]` lines is done; it also reports how much light the
       LED really puts on the photodiode, the one number the design assumes.
3. [ ] **`safety/overvoltage_monitor` (`OVERVOLT`) — wire it with its input
       on the Pico's 3V3 pin.** First run of a TL431A from the batch; the 3V3
       rail is the known voltage that proves it trips and clears. TL431A,
       LM358, S8050, trimpot, LED
       ([breadboard.md](../safety/overvoltage_monitor/breadboard.md)); `mpremote
       run main.py`, trimpot to each end when asked. All `[PASS]` lines and
       the LED flipping is done.
4. [ ] **`measurement_tools/frequency_counter` (`FREQC`/`SIMPLECNT`) — wire
       the digital path and run the loopback self-test.** First counting of
       a real signal by the Pico's PWM hardware; also the tool that reads
       `ne555_astable`'s frequency. GP16 → 10kΩ → GP3 with two 1N5817 clamps
       ([breadboard.md](../measurement_tools/frequency_counter/breadboard.md)),
       `mpremote run main.py` (6s). Six `[PASS]` lines is done; the analog
       (Schmitt) path is added later, only when a sensor needs counting.

Nothing else is startable right now: everything else on the list is waiting
on the 2026-10-02 shipment, the wick, or is Deferred or undesigned.

## Blocked — waiting on a shipment

- [ ] **`ACCELIF`** (`signal_conditioning/accelerometer_interface`) —
      blocked on the solder wick, **not** in the 2026-10-02 order (see "Next
      order"). A few GY-521 header pins bridged during soldering
      (2026-09-24); wick clears them. When it arrives: lay the braid over
      the bridge, press the iron on the braid for 2–3 seconds, lift both
      together, and check the row by eye (steps in that circuit's
      [breadboard.md](../signal_conditioning/accelerometer_interface/breadboard.md)).
      Then four jumpers: `VCC`→3V3(OUT) (pin 36), `GND`→pin 38,
      `SDA`→GP4 (pin 6), `SCL`→GP5 (pin 7); module lying still;
      `mpremote run main.py`. All lines `[PASS]` is done; a `WHO_AM_I` of
      `0x70`–`0x72` is a clone that still passes. It's the measurement
      side of `VIBISO` and the first power-up of the untested GY-521.
- [ ] **`CHGAMP`** (tier5, charge amplifier) — blocked on the leaded
      piezo discs (ordered 2026-10-02, 12mm, 5000pF). A 2026-09-16
      attempt with the bare-disc batch destroyed one unit (fluxless
      solder); all its parts went back to inventory. Retry once the leaded
      piezo arrives.
- [ ] **`hall_amplifier`** (`signal_conditioning/hall_amplifier`, tier5
      `HALLAMP`) — designed and simulated; blocked on the 49E/SS49E sensors
      (15 ordered 2026-10-02). Parts otherwise on hand (LM358, trimpot, eight
      10kΩ, two 100kΩ, 5.1kΩ, 2kΩ). Wire it per its
      [breadboard.md](../signal_conditioning/hall_amplifier/breadboard.md),
      `mpremote run main.py`, turn the trimpot until the reading holds at
      0.94V, `[PASS]` for the noise line is done; the magnet test waits on the
      magnets in "Next order". Try a second sensor if the first can't be nulled.
- [ ] **`adc_ads1115`** (`signal_conditioning/adc_ads1115`, tier9
      `ADCDRV`) — designed and simulated; blocked on the ADS1115 module
      (1 ordered 2026-10-02). Parts otherwise on hand (10kΩ ×3, 100nF,
      1N5817 ×2). Wire it per its
      [breadboard.md](../signal_conditioning/adc_ads1115/breadboard.md) and
      `mpremote run main.py`; four `[PASS]` lines is done, and it doubles as
      the genuineness check on the module.
- [ ] **`vibration_driver`** (`oscillators/vibration_driver`, `SIMPGEN`'s
      actuator stage) — designed and simulated; blocked on the coin motors
      (10 ordered 2026-10-02, 80–90mA rated, 120mA stall). Parts otherwise on
      hand (S8050, 1N5817, 1kΩ, 10kΩ). It is the driver `RIPPLETANK` needs.
- [ ] **`VIBISO`** (vibration isolation platform) — hold off on the
      mechanical build itself until `ACCELIF` (first bullet above) is
      assembled and passing, so there is something to measure isolation
      quality with. For later: the on-hand Creality K1 (with PLA
      filament stock) can print feet/platform parts once this is
      actionable.
- [ ] **`RIPPLETANK`** (2D ripple tank) — blocked on the coin motors (see
      `vibration_driver` above): it becomes the wave dipper, driven by that
      circuit. Whether a ~150Hz coin motor makes useful ripples is
      untested; the mechanical side (a dipper arm and tank) is still to be
      worked out. For later: the on-hand Creality K1 (PLA on hand) could
      print a precise stepped/sloped depth insert once this is actionable.

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
