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
[kb/todo_list_conventions.md](kb/todo_list_conventions.md) for the ranking
method if you want it. "Blocked" and "Backlog" are reference sections,
not action items, until something changes their status.

When an item is done, move it to [TODO-completed.md](TODO-completed.md)
(dated entry) instead of deleting it. Completed circuits' bench-test
status lives in `README.md`'s "built & bench-tested" table.

---

## Next order — action needed

- [ ] **Source soldering flux** (rosin paste or pen) from a Canadian
      retailer that isn't AliExpress and isn't RobotShop (RobotShop
      doesn't stock it) — your call which one. Needed before retrying
      `CHGAMP`'s piezo lead-soldering step (see "Blocked" below).
- [ ] **Add the SparkFun Breadboard Power Supply Kit (5V/3.3V) to your
      RobotShop cart.** Powers `power_supplies/psu_medlow_lm317`.
- [ ] **Linear/analog Hall-effect sensor (e.g. 49E), 5–10pk — add to next
      AliExpress order.** Needed for the `HALLAMP` op-amp circuit; the
      KY-003/A3144 module already on hand is digital switch-output only.

**Deferred — not on the shopping list, no action needed:**

- TL431A precision shunt reference (5 on hand, untested) — optional
  precision upgrade to the tier1 `REF` divider, not a purchase.
- LVDT transducer — the only tier5 node with zero hardware, instruments
  `FORCEBAL`'s displacement readout (see
  [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md)).
  Lowest-priority sensor still on this list.
- GΩ-range resistor — only becomes relevant if `CHGAMP` (once retried)
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
  `CAPBRIDGE` route (see "Mechanical builds" below) needs no purchase.

## Ready to build now — parts on hand, ranked by what it unlocks

Ranked top-to-bottom by real dependency-graph facts (does it unblock
another bullet here, is it a named prerequisite for the next design
target, is it a sunk-cost fix in hand, does it satisfy any other real
graph edge, ascending bench effort otherwise) — not by closeness to any
outside research goal. Full method:
[kb/todo_list_conventions.md](kb/todo_list_conventions.md).

1. [ ] **1N5817 Schottky diode — per-unit forward-drop check for
       whichever unit goes into `psu_3xaa`.** Two of 20 already confirmed
       (`psu_4xaa`, `psu_low_v2`); reuse the same Pico-divider technique
       (see `psu_4xaa/README.md` § Validation). The only bullet here with
       a literal, stated hard-blocker for another bullet on this list.
2. [ ] **`power_supplies/psu_3xaa` — confirm and assemble.** Blocked only
       on the diode check above; independent of `psu_low_v2`.
3. [ ] **`safety/thermal_monitor` (`THERM`) — physically assemble.**
       Folder/netlist/breadboard/smoke test exist. Powered from
       `psu_pico_rail`. Fills the safety gap flagged by the existing
       thermistor's "suspect faulty" status.
4. [ ] **`protection/active_current_limiter` (`ACTIVELIM`) — physically
       assemble.** Uses the only IRLZ44N on hand (returns to inventory
       once its bench check passes, per this repo's ephemeral-circuit
       convention — see [kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)).
       Size the TL431A reference divider against the bench-measured
       cathode voltage — see that circuit's `breadboard.md` § Reference
       divider. **Known limitation, not a defect**: this is a hard-trip
       limiter with no hysteresis, so expect chatter right at the 2A trip
       boundary — see that circuit's README § Design notes.
5. [ ] **`measurement_tools/capacitance_bridge` (`CAPBRIDGE`) —
       physically assemble.** Targets the aluminum electrolytic capacitor
       kit (1µF–470µF). No PSU needed (runs off the Pico's own GPIO/3V3).

**No `OHMMETER` bullet on purpose** —
`measurement_tools/resistance_measurement` (already built, in active use)
already covers that node's present need with a 2-wire divider; a 4-wire
Kelvin design only matters once something specifically needs
lead/contact-resistance precision, which nothing on this bench does yet.

**Mechanical builds — no purchase needed:**

6. [ ] **`VIBISO`** (vibration isolation platform) — a weighted platform
       on soft-compliance feet (rubber pads, partially-inflated inner
       tubes/balloons). Check what's around the apartment first. Buildable
       now as a mechanical base for `FORCEBAL`/`LASERDRV`; can't be
       bench-*measured* for isolation quality until `ACCELIF` arrives
       (see "Blocked" below).
7. [ ] **`RIPPLETANK`** (2D ripple tank) — a shallow tray/baking dish,
       water, and a glass/acrylic sheet as the submerged depth-step
       insert. Wave driver: `pico/leds/gpio_pwm_led/` (already built in
       the sibling `pico/` repo) drives a small motor/speaker dipper
       directly — no `SIMPGEN` circuit needed. Buildable now for a first
       qualitative demo; an electronic phase-shift readout is a future
       step gated on tier6 `LOCKIN` (undesigned).

**Standalone validation tail — no real edge to anything else, ascending
bench effort:**

8. [ ] **`power_supplies/psu_ultralow_v1`** — no assembled-circuit demo
       has been run, only component-level validation. One power-on check.
9. [ ] **`power_supplies/psu_medlow_usbc`** — passive USB-C breakout, no
       PD controller; VBUS may never come up without confirmed CC1/CC2
       termination. Check with
       [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/)
       (clip its leads onto the two CC pins) before trusting this
       circuit. `smoke_test.py` fails on purpose until this is resolved.
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

- [ ] **`CHGAMP`** (tier5, charge amplifier). Blocked on: soldering flux,
      not yet sourced (see "Next order" above). Attempted 2026-09-16: the
      bare piezo disc has no pre-attached leads, and a fluxless solder
      attempt destroyed one unit before flux could be added to the plan.
      Build paused — all its parts (TL082, piezo disc, resistors,
      capacitor) went back to inventory rather than sitting
      mid-assembly. Retry once flux is on hand.
- [ ] **`INDBRIDGE`** (tier3, inductance bridge). Blocked on: color-ring
      inductor assortment, reordered 2026-09-10 (original order cancelled
      by AliExpress 2026-09-07), not yet received.
- [ ] **`SCOPELA`** (logic analyzer). Blocked on: CY7C68013A / EZ-USB
      FX2LP board, ordered 2026-09-10, not yet received. `sigrok`'s
      `fx2lafw` firmware supports it out of the box.
- [ ] **`ACCELIF`** (tier5). Blocked on: GY-521 (MPU6050) module, ordered
      2026-09-10, not yet received. Substitutes for the originally-scoped
      ADXL335.
- [ ] **`HALLAMP`** (tier5) — partially unlocked (KY-003/A3144 module
      received), but that part is digital switch-output only. Needs the
      linear/analog Hall sensor from "Next order" above to build the
      op-amp amplifier circuit as scoped.

## Backlog — undesigned, long-tail

Nothing below has a netlist, folder, or sourced part yet. Check
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) for
how each node connects before starting one.

- [ ] **Safety monitoring**: `LEAKDET`, `GFCI`, `ESDMON`, `INSMON`,
      `ARCDECT`, `OVERCUR`, `OVERVOLT`, `TEMPCOIL`, `EMSTOP`,
      `PSUHEALTH`, `FUSESTAT`, `RFRAD`, `VACPRES`, `SMOKDET`.
      (`THERM` is done — see "Ready to build now" above.)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` — no PSU tier built around
      the Lenovo 65W adapter (on hand) or any industrial supply.
      `ACTIVELIM` (their protection stage) is done, but that's not the
      PSU tier itself.
- [ ] **Bootstrap tier**: `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`,
      `CRTSC`. (`PASSVM` is already done via `fuse_test_voltmeter`.)
- [ ] **Tier 2**: `VM`, `AM`, `FREQC` — undesigned as dedicated circuits
      (distinct from the bootstrap ammeter jigs).
- [ ] **Tier 4**: `IA`, `DA`, `DEMOD`. (`PHASED` is done — see
      `README.md`'s bench-tested table.)
- [ ] **Tier 5** (spacetime): `LVDTAMP` — no transducer sourced (see
      "Next order" above). `FORCEBAL`/`SIPMFE` — zero hardware sourced;
      see `spacetime_circuits_dependency.md`'s "Why these new tiers"
      section for the justification. Not `TODO-agent.md` design tasks
      yet — that workflow needs a specific sourced part first.
- [ ] **Tier 6**: `LOCKIN`, `AAF`, `TIMEINT`, `JITTER` — undesigned.
      `LOCKIN` is this bench's strongest-justified next design target
      once `CHGAMP` is bench-tested (see
      `spacetime_circuits_dependency.md`'s "Why these tiers" section).
- [ ] **Tier 7** (spacetime): `RFPWR`, `MIXER`, `SWEEP` — unaddressed, no
      parts identified, lowest priority. `LASERDRV` — backlogged, though
      on-hand 5mm LEDs give a free first test (see "Next order" above).
- [ ] **Tier 8** (spacetime): `CALORIF`, `PWRFACT`, `ENGINT`, `NOISEFIG`
      — unaddressed, no parts identified.
- [ ] **Tier 9**: `SAMHOLD`, `ADCDRV`, `REFGEN2` — undesigned. `MUX` is
      partially covered by `cd4066_switch_tester` component validation,
      but the actual multiplexer circuit isn't built.
- [ ] **Concurrent measurement tools**: `SCOPEUSBSER`, `SCOPEDSO`,
      `SCOPEBENCH`, `PRECBOX`, `LOADBANK`, `NOISEGEN`, `TESTSIG`,
      `THERMOAMP` — undesigned/unsourced. (`SCOPELA` has a part on order
      — see "Blocked" above.)
