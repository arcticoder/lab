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

- [ ] **AliExpress: add two items to the cart, then check the total
      before paying.** Cart now: 12× leaded piezo discs (`CHGAMP`), 10×
      49E Hall sensors (`HALLAMP`), solder wick (`ACCELIF`). Add:
      [2× ADS1115 16-bit ADC module](https://www.aliexpress.com/item/1pcs-16-Bit-I2C-ADS1115-Module-ADC-4-channel-with-Pro-Gain-Amplifier-for-Arduino-RPi/32648046830.html)
      (`adc_ads1115`; one spare in case of a dud) and a multi-piece lot of
      [3V coin vibration motors](https://www.aliexpress.com/item/1005007703166995.html)
      (`vibration_driver`; stay at or under 90mA rated current). Prices
      weren't verifiable from here (about $1.65 per ADS1115, under $1 per
      motor when listed). If checkout shows no shipping fee, pay. If it still
      shows one, don't — the next design pass adds the top-up.

## Ready to build now — parts on hand

1. [ ] **`measurement_tools/logic_analyzer_check` (`SCOPELA`'s first
       capture) — attach the board, move one wire, run two commands.** The
       first attempt failed before it reached the signal: sigrok loads its
       firmware, the board re-enumerates, and usbipd drops it. In an
       administrator PowerShell: `usbipd bind --busid 3-3`, then
       `usbipd attach --wsl --busid 3-3 --auto-attach` (leave it open; use
       the busid `usbipd list` shows for "fx2lafw"). Wiring: Pico `GP15`
       (pin 20) → the board's **`PB0`** pad (J2, row "PB0 PB1"; the board has
       no pad called `D0`), Pico GND (pin 18) → J2's `GND` in its bottom row.
       Then, with `mpremote run main.py` running in terminal 1:
       `python3 check_capture.py --find-channel` (expect `toggling: D0`),
       then `python3 check_capture.py` — three `[PASS]` lines is done. Full
       steps and failure table in its
       [breadboard.md](../measurement_tools/logic_analyzer_check/breadboard.md).

Nothing else is startable right now: `ACCELIF`'s soldering fix waits on
the wick shipment (see "Next order" and "Blocked"), and the rest of the
list is Blocked, Deferred or undesigned.

## Blocked — waiting on a shipment or a sourcing decision

- [ ] **`ACCELIF`** (`signal_conditioning/accelerometer_interface`) —
      blocked on the solder wick in the AliExpress cart (see "Next order"
      above). A few GY-521 header pins bridged during soldering
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
      piezo disc in the AliExpress cart (see "Next order" above).
      A 2026-09-16 attempt with the bare-disc batch destroyed one unit
      (fluxless solder); all its parts went back to inventory. Retry once
      the leaded piezo arrives.
- [ ] **`HALLAMP`** (tier5) — the on-hand KY-003/A3144 module is digital
      switch-output only; needs the linear/analog Hall sensor in the
      AliExpress cart ("Next order" above) to build the op-amp
      amplifier circuit as scoped.
- [ ] **`adc_ads1115`** (`signal_conditioning/adc_ads1115`, tier9
      `ADCDRV`) — designed and simulated; blocked on the ADS1115 modules in
      the AliExpress list (see "Next order"). Parts otherwise on hand
      (10kΩ ×3, 100nF, 1N5817 ×2). Wire it per its
      [breadboard.md](../signal_conditioning/adc_ads1115/breadboard.md) and
      `mpremote run main.py`; four `[PASS]` lines is done, and it doubles as
      the genuineness check on the module.
- [ ] **`vibration_driver`** (`oscillators/vibration_driver`, `SIMPGEN`'s
      actuator stage) — designed and simulated; blocked on the coin motor
      in the AliExpress list (see "Next order"). Parts otherwise on hand
      (S8050, 1N5817, 1kΩ, 10kΩ). It is the driver `RIPPLETANK` needs.
- [ ] **`VIBISO`** (vibration isolation platform) — hold off on the
      mechanical build itself until `ACCELIF` (first bullet above) is
      assembled and passing, so there is something to measure isolation
      quality with. For later: the on-hand Creality K1 (with PLA
      filament stock) can print feet/platform parts once this is
      actionable.
- [ ] **`RIPPLETANK`** (2D ripple tank) — blocked on the coin motor (see
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
  chips has been run) — untested, but nothing needs them yet; validate
  whichever switch a future `MUX`/`DEMOD` build actually pulls.
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
  optical shadow readout (LED + photodiode + `TIA`, all on hand) needs no
  purchase; its design is an open item in `TODO-agent.md`.

## Backlog — undesigned, long-tail

Nothing below has a netlist, folder, or sourced part yet. Check
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) for
how each node connects before starting one.

- [ ] **Safety monitoring**: `LEAKDET`, `GFCI`, `ESDMON`, `INSMON`,
      `ARCDECT`, `OVERCUR`, `OVERVOLT`, `TEMPCOIL`, `EMSTOP`,
      `PSUHEALTH`, `FUSESTAT`, `RFRAD`, `VACPRES`, `SMOKDET`.
      (`THERM` is built & bench-tested — see `README.md`'s "built &
      bench-tested" table.)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` — no PSU tier built around
      the Lenovo 65W adapter (on hand) or any industrial supply.
      `ACTIVELIM` (their protection stage) is designed/simulated but has
      nothing to protect yet and isn't a real need until this tier starts
      — see "Deferred" above — and that's not the PSU tier itself anyway.
- [ ] **Bootstrap tier**: `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`,
      `CRTSC`. (`PASSVM` is already done via `fuse_test_voltmeter`.)
- [ ] **Tier 2**: `VM`, `AM`, `FREQC` — undesigned as dedicated circuits
      (distinct from the bootstrap ammeter jigs).
- [ ] **Tier 4**: `IA`, `DA`, `DEMOD`. (`PHASED` is done — see
      `README.md`'s bench-tested table.)
- [ ] **Tier 5** (spacetime): `LVDTAMP` — no transducer sourced (see
      "Deferred" above). `FORCEBAL`/`SIPMFE` — zero hardware sourced;
      see `spacetime_circuits_dependency.md`'s "Why these new tiers"
      section for the justification. Not `TODO-agent.md` design tasks
      yet — that workflow needs a specific sourced part first.
- [ ] **Tier 6**: `LOCKIN`, `AAF`, `TIMEINT`, `JITTER` — undesigned.
      `LOCKIN` is this bench's strongest-justified next design target
      once `CHGAMP` is bench-tested (see
      `spacetime_circuits_dependency.md`'s "Why these tiers" section).
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
      `THERMOAMP` — undesigned/unsourced. (`SCOPELA`'s board is received and
      detected by `sigrok`, with its first capture in "Ready to build
      now" — but it's a plug-in tool, not a circuit; none of these
      dedicated designs exist yet.)
