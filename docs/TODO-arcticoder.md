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

- [ ] **AliExpress: add the PD trigger board and the power-resistor
      assortment to the cart, then check out the whole cart.** The cart
      is still under the $10 free-shipping threshold; both of these are
      real needs (`ACTIVELIM`'s ≥2A bench check, below), so they close
      the gap without padding. Already in the cart:
      [12× leaded 12mm piezo discs](https://www.aliexpress.com/item/1005003133740770.html)
      (retry `CHGAMP` without soldering to a bare disc),
      [10× 49E linear Hall sensors](https://www.aliexpress.com/item/32912682330.html)
      (the only way to build `HALLAMP`; the on-hand KY-003 is
      digital-only), and a Mini-USB cable (`SCOPELA`'s board takes
      Mini-USB; only Micro-USB/USB-C cables are on hand). To add:
      [USB-C PD/QC decoy trigger board, 100W/5A, 5V/9V/12V/15V/20V selectable](https://www.aliexpress.com/item/1005002483864283.html)
      and
      [10× 5W/10W ceramic wirewound resistor assortment, 0.1Ω–1kΩ](https://www.aliexpress.com/i/2251832677195042.html)
      — both found by search, not vetted beyond the listing text, so
      check price/stock first. For the `ACTIVELIM` test use the lowest
      tap that still gets 2A through a single 5W/10W resistor (5V →
      10W), never a tap above what the on-hand Lenovo 65W adapter
      outputs (20V/3.25A max). Pick the exact resistor once the
      board's real output is bench-measured.
- [ ] **RobotShop: order the
      [SparkFun Breadboard Power Supply Kit](https://ca.robotshop.com/products/sfe-breadboard-power-supply-kit)
      (5V/3.3V, LM317).** It's the adjustable-rail PSU that follows
      `psu_4xaa`'s fixed 6V (`power_supplies/psu_medlow_lm317`). It
      needs a 9–12V DC input and nothing on the bench makes one today:
      read the Lenovo adapter's label for a 9V or 12V output profile —
      if it has one, the PD trigger board above supplies that input
      and no further part is needed.

## Ready to build now — parts on hand

1. [ ] **`power_supplies/psu_medlow_usbc` — read both CC pins with
       [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/).**
       Closes the one deliberately-red `smoke_test.py` in the repo and
       would give a second, free 5V path if VBUS comes up (the SparkFun
       kit above is being bought either way). The jig you left set up
       (`breadboard3.jpg`) currently reads open, which only proves the
       probe leads aren't touching anything — it says nothing about the
       CC pins yet. The two SMD parts on the breakout are marked `512`
       and `215`; `215` is almost certainly `512` read upside-down, so
       both CC pins should read ~5.1kΩ to GND.
       1. Unplug the USB-C cable from the breakout — the jig drives the
          pins from the Pico's 3V3, nothing else may power the board.
       2. Probe lead A goes to the row where `R_REF` meets GP28; probe
          lead B goes to a Pico GND pin.
       3. `mpremote run main.py`, touch the two probe tips together:
          it must print "Short to GND or 0 Ohms." If it doesn't, fix
          the leads before going on.
       4. Lead A on the `CC1` pad, lead B on the `GND` pad (pad order
          on the silkscreen: `CC2, D+, D-, SBU1, SBU2, CC1, VBUS,
          GND`). Note the reading. Repeat with lead A on `CC2`.
       5. ~5.1kΩ on both (prints ~4.5k–5.7k, ~1.1V): the pull-downs are
          already there — plug the adapter in and read VBUS with
          [raw_voltage_probe](../measurement_tools/raw_voltage_probe/).
          "Circuit Open" on a CC pin (with step 3 passed): wire one of
          the 10 on-hand 5.1kΩ resistors from that pad to `GND`, then
          read VBUS.

Nothing else queued behind this one right now — see
[kb/todo_list_conventions.md](kb/todo_list_conventions.md) for the
ranking method this section uses whenever it has more than one item.

## Blocked — waiting on a shipment or a sourcing decision

- [ ] **`ACTIVELIM`** (`protection/active_current_limiter`) — needs a
      current-capable (≥2A) test source to find its real trip point;
      nothing on this bench can do that today. Unblocked by the PD
      trigger board + power resistor in "Next order" above — see
      `docs/kb/bench_photo_diagnostics_notes.md`'s `ACTIVELIM` entry for
      the full reasoning.
- [ ] **`CHGAMP`** (tier5, charge amplifier) — blocked on the leaded
      piezo disc in the AliExpress cart (see "Next order" above).
      A 2026-09-16 attempt with the bare-disc batch destroyed one unit
      (fluxless solder); all its parts went back to inventory. Retry once
      the leaded piezo arrives.
- [ ] **`HALLAMP`** (tier5) — the on-hand KY-003/A3144 module is digital
      switch-output only; needs the linear/analog Hall sensor in the
      AliExpress cart ("Next order" above) to build the op-amp
      amplifier circuit as scoped.
- [ ] **`SCOPELA` — needs a Mini-USB cable, in the AliExpress cart
      (see "Next order" above).** The board itself (received
      2026-09-20) needs no circuit design — plugging it in and
      confirming `sigrok`/PulseView detects it via `fx2lafw` is the
      whole check, once the cable is in hand.
- [ ] **`VIBISO`** (vibration isolation platform) — hold off on the
      mechanical build itself until `ACCELIF` (design task open in
      `TODO-agent.md`) exists to actually measure isolation quality; a
      platform with nothing to bench-test it against isn't worth
      building yet. For later: the on-hand Creality K1 (with PLA
      filament stock) can print feet/platform parts once this is
      actionable.
- [ ] **`RIPPLETANK`** (2D ripple tank) — needs an actual motor/speaker
      driver circuit that doesn't exist yet. `pico/leds/gpio_pwm_led/`
      only generates a GPIO-level PWM signal (tier1 `SIMPGEN`'s
      undesigned stand-in) — a Pico GPIO pin can't drive a motor's
      current directly without a transistor-switch + flyback-diode
      stage, which hasn't been designed. Design task open in
      `TODO-agent.md`; once done, the tray/water/depth-step-insert build
      itself needs no purchase. For later: the on-hand Creality K1 (PLA
      on hand) could print a precise stepped/sloped depth insert once
      this is actionable.

`INDBRIDGE` and `ACCELIF` both received their blocking part on
2026-09-20 and need a netlist designed against it before there's
anything to physically assemble — tracked as open design items in
`TODO-agent.md`, not here.

## Deferred — considered and declined, no action needed

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
      `ACTIVELIM` (their protection stage) is designed/simulated and
      waiting on a current-capable test source — see "Blocked" above —
      but that's not the PSU tier itself.
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
