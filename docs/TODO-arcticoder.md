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

## Ready to build now — parts on hand, ranked by what it unlocks

Ranked top-to-bottom by real dependency-graph facts (does it unblock
another bullet here, is it a named prerequisite for the next design
target, is it a sunk-cost fix in hand, does it satisfy any other real
graph edge, ascending bench effort otherwise) — not by closeness to any
outside research goal. Full method:
[kb/todo_list_conventions.md](kb/todo_list_conventions.md).

1. [ ] **`protection/active_current_limiter` (`ACTIVELIM`) — physically
       assemble.** Uses the only IRLZ44N on hand (returns to inventory
       once its bench check passes, per this repo's ephemeral-circuit
       convention — see [kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)).
       Size the TL431A reference divider against the bench-measured
       cathode voltage — see that circuit's `breadboard.md` § Reference
       divider. **Known limitation, not a defect**: this is a hard-trip
       limiter with no hysteresis, so expect chatter right at the 2A trip
       boundary — see that circuit's README § Design notes.
2. [ ] **`measurement_tools/capacitance_bridge` (`CAPBRIDGE`) —
       physically assemble.** Targets the aluminum electrolytic capacitor
       kit (1µF–470µF). No PSU needed (runs off the Pico's own GPIO/3V3).

**No `OHMMETER` bullet on purpose** —
`measurement_tools/resistance_measurement` (already built, in active use)
already covers that node's present need with a 2-wire divider; a 4-wire
Kelvin design only matters once something specifically needs
lead/contact-resistance precision, which nothing on this bench does yet.

**Mechanical builds — no purchase needed:**

3. [ ] **`VIBISO`** (vibration isolation platform) — a weighted platform
       on soft-compliance feet (rubber pads, partially-inflated inner
       tubes/balloons). Check what's around the apartment first. Buildable
       now as a mechanical base for `FORCEBAL`/`LASERDRV`; can't be
       bench-*measured* for isolation quality until `ACCELIF` is
       designed and built (part received 2026-09-20 — design task now
       tracked in `TODO-agent.md`, not a purchase blocker anymore).
4. [ ] **`RIPPLETANK`** (2D ripple tank) — a shallow tray/baking dish,
       water, and a glass/acrylic sheet as the submerged depth-step
       insert. Wave driver: `pico/leds/gpio_pwm_led/` (already built in
       the sibling `pico/` repo) drives a small motor/speaker dipper
       directly — no `SIMPGEN` circuit needed. Buildable now for a first
       qualitative demo; an electronic phase-shift readout is a future
       step gated on tier6 `LOCKIN` (undesigned).

**Standalone validation tail — no real edge to anything else above,
ordered by which check informs the biggest decision first, then
ascending bench effort:**

5. [ ] **`power_supplies/psu_medlow_usbc` — clip
       [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/)
       onto the two CC pins.** Promoted to the top of this tail because
       the answer directly decides the SparkFun-kit purchase in
       "Deferred" below: if VBUS comes up with correct CC1/CC2
       termination, `psu_medlow` is done for free and that purchase is
       dropped for good; if not, move the kit from "Deferred" back into
       "Next order." `smoke_test.py` fails on purpose until this is
       resolved.
6. [ ] **`SCOPELA` — plug in the CY7C68013A board (received 2026-09-20)
       and confirm `sigrok`/PulseView detects it via `fx2lafw`.** No
       assembly needed — this board *is* the purchase, not a component
       (see `kb/ordering_ingestion_notes.md`). Zero-cost, lowest-effort
       check in this tail; check whether it included an 8-wire Dupont
       test-clip cable and whether it's USB-A dongle-style or needs its
       own Micro-USB cable.
7. [ ] **1N5817 Schottky diode — per-unit forward-drop check for
       whichever unit goes into `psu_3xaa`.** Two of 20 already confirmed
       (`psu_4xaa`, `psu_low_v2`); reuse the same Pico-divider technique
       (see `psu_4xaa/README.md` § Validation).
8. [ ] **`power_supplies/psu_3xaa` — confirm and assemble.** Blocked only
       on the diode check above. Honest note: nothing currently on this
       bench needs a 4.5V rail specifically — `oscillators/ne555_astable`
       tried it first and ruled it out (sags to ~4.02V under load, below
       the NE555's 4.5V minimum), and `psu_4xaa` (6.0V, already built)
       already covers what this tier would. This is a one-time hardware
       confirmation of an already-designed circuit against real
       parts, same category as item 9 below — not something anything
       else is waiting on, and not staged inventory for a future build.
9. [ ] **`power_supplies/psu_ultralow_v1`** — no assembled-circuit demo
        has been run, only component-level validation. One power-on check.
10. [ ] **CD4066BCN — switches 2–4 per chip still untested** (only switch
        1 of each of the 10 chips has been run through
        `measurement_tools/cd4066_switch_tester/`). Not blocking anything
        above — needed before trusting a chip in a future `MUX`/`DEMOD`
        build.
11. [ ] **Glass tube fuses (2A fast-blow, 10 on hand) — no test jig
        built.** Needs a jig from scratch. Not blocking anything above —
        needed before trusting one in the (backlog) `psu_medlow`
        protection path.
12. [ ] *(optional cleanup, not a blocker)* **`fuse_test_voltmeter` trip
        detection is non-functional** since bench wiring diverged from
        its original design — `ammeter_10ohm`/`ammeter_1ohm` already
        cover polyfuse sorting instead.

## Blocked — waiting on a shipment or a sourcing decision

- [ ] **`CHGAMP`** (tier5, charge amplifier). Blocked on: a leaded piezo
      disc, in cart but not yet checked out (see "Next order" above).
      Attempted 2026-09-16 with the bare-disc batch: no pre-attached
      leads, and a fluxless solder attempt destroyed one unit. Build
      paused — all its parts (TL082, piezo disc, resistors, capacitor)
      went back to inventory rather than sitting mid-assembly. Retry once
      the leaded piezo arrives.
- [ ] **`HALLAMP`** (tier5) — partially unlocked (KY-003/A3144 module
      received), but that part is digital switch-output only. Needs the
      linear/analog Hall sensor in cart in "Next order" above (not yet
      checked out) to build the op-amp amplifier circuit as scoped.

`INDBRIDGE`, `SCOPELA`, and `ACCELIF` all received their blocking part on
2026-09-20 and are no longer listed here — `SCOPELA` is a zero-cost
plug-in verification now in "Ready to build now" above (item 7);
`INDBRIDGE`/`ACCELIF` both still need a netlist designed against the new
part before there's anything to physically assemble, tracked as open
design items in `TODO-agent.md`, not here.

## Deferred — considered and declined, no action needed

- SparkFun Breadboard Power Supply Kit (5V/3.3V, LM317) for
  `power_supplies/psu_medlow_lm317` — **hold off.** This is one of two
  alternative paths to the same `psu_medlow` tier; the other,
  `psu_medlow_usbc`, is already built and sitting on the bench needing
  only a zero-cost continuity check ("Ready to build now" item 5 above)
  to know whether it already works. Buying this kit before that check
  risks paying for a part you don't need. Move it to "Next order" only
  if that check shows `psu_medlow_usbc` can't bring up VBUS.
- TL431A precision shunt reference (5 on hand, untested) — optional
  precision upgrade to the tier1 `REF` divider, not a purchase.
- LVDT transducer — the only tier5 node with zero hardware, instruments
  `FORCEBAL`'s displacement readout (see
  `spacetime_circuits_dependency.md`). Lowest-priority sensor on this
  bench: unlike the Hall sensor above, `CAPBRIDGE` (already
  designed) is a no-purchase alternative way to instrument `FORCEBAL`,
  so this only becomes relevant if that route proves insufficient.
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
  `CAPBRIDGE` route (see "Mechanical builds" above) needs no purchase.

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
      `ACTIVELIM` (their protection stage) is being built above, but
      that's not the PSU tier itself.
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
      — see "Ready to build now" item 6 above — but it's a plug-in tool,
      not a circuit; none of these dedicated designs exist yet.)
