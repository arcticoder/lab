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

- [ ] **Piezo disc with pre-attached leads — in cart, not yet checked
      out.** [12× 12mm piezo elements with leads attached](https://www.aliexpress.com/item/1005003133740770.html),
      added to cart 2026-09-21 (replaces the flux-sourcing plan below).
      `CHGAMP` is tier5 in this bench's spacetime-research chain — the
      last unbuilt link before `LOCKIN`, the strongest-justified next
      *design* target on this whole bench (see
      `spacetime_circuits_dependency.md`'s "Why these tiers" section:
      synchronous/lock-in detection is the standard technique the cited
      literature uses to pull a small periodic force signal out of
      noise, and `PHASED`/`EPFIELD` are the other two prerequisites,
      both already bench-tested). The piezo disc is also the only
      charge-generating stimulus on hand to bench-test the
      charge-amplifier topology against at all — nothing else in
      inventory produces a charge signal. Buying leaded stock sidesteps
      soldering to the bare ceramic disc entirely, so the flux-sourcing
      problem (no acceptable Canadian retailer found; AliExpress/
      RobotShop both ruled out — see `docs/kb/todo_list_conventions.md`)
      goes away rather than getting solved. The 19 remaining bare discs
      and the rest of `CHGAMP`'s parts (1 TL082, resistors, capacitor)
      stay in inventory unused. **Action needed: check out the cart.**
- [ ] **Linear/analog Hall-effect sensor (49E) — in cart, not yet
      checked out.** [10× 49E TO-92 linear Hall-effect ICs](https://www.aliexpress.com/item/32912682330.html),
      added to cart 2026-09-21. Honest state of this one: nothing on this
      bench is currently *blocked* on it — the KY-003/A3144 module
      already on hand is digital switch-output only, so it doesn't
      unlock the `HALLAMP` op-amp circuit as scoped, and `HALLAMP`
      itself has no other bullet on this list waiting on it. It's here
      because it's cheap, it will definitely be needed eventually (there
      is no on-hand substitute), and bundling a low-urgency-but-certain
      item into the same cart as the piezo disc above costs nothing
      extra. That's a shipping-pipeline argument, not a build-priority
      one. **Action needed: check out the cart (same cart as the piezo
      disc above).**
- [ ] **USB-C PD trigger board + a low-ohm power-resistor assortment —
      not yet in any cart.** `ACTIVELIM`'s bench check (see "Blocked"
      below) needs a source that can push ≥2A into a dummy load; nothing
      on this bench can do that today — see
      `docs/kb/bench_photo_diagnostics_notes.md`'s `ACTIVELIM` entry for
      the full reasoning. **Voltage: use the lowest selectable tap that
      can still hit 2A within the resistor assortment's 5W/10W rating —
      not the trigger board's max.** A 2A fault at 5V only dissipates
      10W (R≈2.5Ω, in range of a single 5W/10W resistor); the same 2A at
      20V would dissipate 40W, above what one resistor in this
      assortment is rated for. Hard ceiling regardless: never pair the
      trigger board with anything but the on-hand Lenovo 65W adapter,
      and never select a tap above what that adapter itself actually
      outputs (20V/3.25A max, 65W total) — the trigger board's own
      100W/5A rating is a spec for a bigger supply than what's on this
      bench, not a target. Two candidates found by search, not vetted
      beyond the listing text — check current price/stock before adding
      to cart:
      [USB-C PD/QC decoy trigger board, 100W/5A, 5V/9V/12V/15V/20V selectable](https://www.aliexpress.com/item/1005002483864283.html)
      and
      [10× 5W/10W ceramic wirewound resistor assortment, 0.1Ω–1kΩ including several single-digit-ohm values](https://www.aliexpress.com/i/2251832677195042.html).
      Pick the exact resistor value once the trigger board's actual
      output voltage is bench-measured, not from the listing's range
      alone.
- [ ] **Mini-USB cable — not yet in any cart.** `SCOPELA`'s CY7C68013A
      board (received 2026-09-20) uses a Mini-USB port — the listing
      title said so all along ("...Module Mini USB"); an earlier note in
      `docs/parts_reference.md` guessed "Micro-USB" without checking that
      string and was wrong. Only Micro-USB and USB-C cables are on hand;
      neither fits. Bundle into the same not-yet-checked-out cart as the
      piezo disc/Hall sensor above to save on shipping.

## Ready to build now — parts on hand

1. [ ] **`power_supplies/psu_medlow_usbc` — clip
       [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/)
       onto the two CC pins.** Decides the SparkFun-kit purchase in
       "Deferred" below: if VBUS comes up with correct CC1/CC2
       termination, `psu_medlow` is done for free and that purchase is
       dropped for good; if not, move the kit from "Deferred" back into
       "Next order." `smoke_test.py` fails on purpose until this is
       resolved.

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
      piezo disc in cart, not yet checked out (see "Next order" above).
      A 2026-09-16 attempt with the bare-disc batch destroyed one unit
      (fluxless solder); all its parts went back to inventory. Retry once
      the leaded piezo arrives.
- [ ] **`HALLAMP`** (tier5) — the on-hand KY-003/A3144 module is digital
      switch-output only; needs the linear/analog Hall sensor in cart in
      "Next order" above (not yet checked out) to build the op-amp
      amplifier circuit as scoped.
- [ ] **`SCOPELA` — needs a Mini-USB cable, not yet on hand** (see "Next
      order" above). The board itself (received 2026-09-20) needs no
      circuit design — plugging it in and confirming `sigrok`/PulseView
      detects it via `fx2lafw` is the whole check, once the cable is in
      hand.
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

- SparkFun Breadboard Power Supply Kit (5V/3.3V, LM317) for
  `power_supplies/psu_medlow_lm317` — **hold off.** This is one of two
  alternative paths to the same `psu_medlow` tier; the other,
  `psu_medlow_usbc`, is already built and sitting on the bench needing
  only a zero-cost continuity check ("Ready to build now" item 1 above)
  to know whether it already works. Buying this kit before that check
  risks paying for a part you don't need. Move it to "Next order" only
  if that check shows `psu_medlow_usbc` can't bring up VBUS.
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
