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

- [ ] **AliExpress: check the cart subtotal and check out once it clears
      $10.** Mini-USB cable acquired directly 2026-09-24 — no longer in
      the cart. Currently in the cart:
      [12× leaded 12mm piezo discs](https://www.aliexpress.com/item/1005003133740770.html)
      (`CHGAMP` retry),
      [10× 49E linear Hall sensors](https://www.aliexpress.com/item/32912682330.html)
      (`HALLAMP`), and a roll of solder wick — added 2026-09-24 for the
      bridged header pins on the GY-521 module (see item 1 below).
      **Don't add the
      USB-C PD trigger board or the 5W/10W power-resistor assortment to
      close the gap** — those were for `ACTIVELIM`'s bench check, which
      is now in "Deferred" below: nothing on this bench needs that
      circuit's protection yet, so buying parts to validate it isn't a
      real need right now. If the cart is still under $10 with just the
      three items above, wait for a genuine need rather than padding it.
- [ ] **RobotShop: order the
      [SparkFun Breadboard Power Supply Kit](https://ca.robotshop.com/products/sfe-breadboard-power-supply-kit)
      (5V/3.3V, LM317).** Separate seller and cart from AliExpress, so
      place it independently of the item above. It's the adjustable-rail
      PSU that follows `psu_4xaa`'s fixed 6V
      (`power_supplies/psu_medlow_lm317`). Its input is a DC barrel jack;
      either drive-enclosure adapter (both 12V, DC, centre-positive, ≥1A —
      labels read 2026-09-25) covers it, so no adapter is being bought.
      The plug size isn't printed on the labels; when the kit arrives,
      the adapter's plug seating snugly in the jack is the check.

## Ready to build now — parts on hand

1. [ ] **`signal_conditioning/accelerometer_interface` (`ACCELIF`) —
       finish soldering the header, then wire the GY-521 to the Pico and
       run `main.py`.** It's the measurement side of `VIBISO` (see
       "Blocked") and the first power-up of the untested GY-521. A few
       header pins bridged during soldering (2026-09-24) — see
       [breadboard.md](../signal_conditioning/accelerometer_interface/breadboard.md)'s
       new "If pins bridge during header soldering" section for the
       drag-soldering fix (works with the iron/rosin solder already on
       hand; the solder wick in the AliExpress cart is the fallback if
       that doesn't fully clear it). Once the header's clean: four
       jumpers, `VCC`→3V3(OUT) (pin 36), `GND`→pin 38, `SDA`→GP4 (pin 6),
       `SCL`→GP5 (pin 7); module lying still on the bench;
       `mpremote run main.py`. All lines `[PASS]` is done; a `WHO_AM_I` of
       `0x70`–`0x72` is a clone that still passes. Full wiring table and
       failure meanings in `breadboard.md` above.
2. [ ] **`SCOPELA` — confirm `sigrok`/PulseView detects the CY7C68013A
       board via `fx2lafw`.** Mini-USB cable acquired 2026-09-24 (no
       longer in the AliExpress cart). `lsusb` already shows the board
       enumerating at Cypress's factory-default `04b4:8613` ID with
       jumper J4 removed — with J4 in (as it shipped), the board didn't
       enumerate at all. Best explanation (datasheet-backed, not
       confirmed on this board): J4 connects the onboard 24LC128 EEPROM,
       and with it in the chip boots whatever the EEPROM holds instead of
       its default USB identity. Leave J4 out — that's the state `sigrok`
       needs to load firmware over USB. The `lsusb` line above isn't
       the actual pass condition yet: install `sigrok-cli`/`pulseview` +
       `sigrok-firmware-fx2lafw` if not already present
       (`sudo apt install sigrok-cli pulseview sigrok-firmware-fx2lafw`),
       then run `sigrok-cli --driver fx2lafw --scan` (or open PulseView
       and pick the `fx2lafw` driver) — a device detected there is the
       real check. No circuit design needed either way; see
       `parts_reference.md`'s entry for the board's specs.

Ranked by the five-criteria method in
[kb/todo_list_conventions.md](kb/todo_list_conventions.md): item 1
unblocks `VIBISO`, a real downstream consumer; item 2 has no downstream
edge on this bench, just an already-purchased instrument to bring up.

## Blocked — waiting on a shipment or a sourcing decision

- [ ] **`CHGAMP`** (tier5, charge amplifier) — blocked on the leaded
      piezo disc in the AliExpress cart (see "Next order" above).
      A 2026-09-16 attempt with the bare-disc batch destroyed one unit
      (fluxless solder); all its parts went back to inventory. Retry once
      the leaded piezo arrives.
- [ ] **`HALLAMP`** (tier5) — the on-hand KY-003/A3144 module is digital
      switch-output only; needs the linear/analog Hall sensor in the
      AliExpress cart ("Next order" above) to build the op-amp
      amplifier circuit as scoped.
- [ ] **`VIBISO`** (vibration isolation platform) — hold off on the
      mechanical build itself until `ACCELIF` (item 1 above) is
      assembled and passing, so there is something to measure isolation
      quality with. For later: the on-hand Creality K1 (with PLA
      filament stock) can print feet/platform parts once this is
      actionable.
- [ ] **`RIPPLETANK`** (2D ripple tank) — needs a wave-dipper actuator
      and its driver stage, and neither exists yet: no motor or speaker
      is on hand (the only actuator is the 9G servo), and
      `pico/leds/gpio_pwm_led/` only generates a GPIO-level PWM signal,
      which can't drive a motor's current directly. What to build the
      driver around is open in `TODO-agent.md`. For later: the on-hand
      Creality K1 (PLA on hand) could print a precise stepped/sloped
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
- `power_supplies/psu_medlow_usbc` and the USB-C breakout's CC-pin check
  — shelved; the SparkFun kit is the `psu_medlow` implementation being
  built, and the breakout board stays in inventory unused.
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
  bench: unlike the Hall sensor above, `CAPBRIDGE` (already built &
  bench-tested) is a no-purchase alternative way to instrument
  `FORCEBAL`, so this only becomes relevant if that route proves
  insufficient.
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
- Torsion fiber + mirror (`FORCEBAL`) — not needed. A beam-balance +
  `CAPBRIDGE` route (see "Blocked" above) needs no purchase.

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
      `THERMOAMP` — undesigned/unsourced. (`SCOPELA`'s board is received
      — see "Blocked" above for its own remaining gap — but it's a
      plug-in tool, not a circuit; none of these dedicated designs exist
      yet.)
