# TODO — arcticoder

Single human-facing checklist for this repo, covering both the
general-purpose tier graph
([general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md))
and the spacetime-research tier graph
([spacetime_circuits_dependency.md](spacetime_circuits_dependency.md)), plus
personal action items only you can do (ordering, physical verification on
the bench, decisions).

**Work this file top-to-bottom, one section at a time.** Whichever
section below is first to still have an unchecked item is what to do
next, and within that section the first bullet is the most important.

Completed circuits' bench-test status is tracked in `README.md`'s "built &
bench-tested" table and `docs/history.md`. For the TODO items on *this*
list specifically: when one is done, move it to
[TODO-completed.md](TODO-completed.md) (dated entry) instead of deleting
it.

---

## Next AliExpress order — action needed

Ordering is time-sensitive (transit from China runs a few weeks), so this
section stays at the top rather than after the bench-work sections —
finding it buried past several pages of build tasks meant it kept getting
skipped in practice.

**No order needed right now — hold off on a top-up.** The entire
2026-09-03 batch (TL082, MF52AT thermistor, IRLZ44N MOSFET, piezo disc,
SN74HC86N XOR gate, KY-003 Hall module) arrived 2026-09-12, unlocking 10
new-build items below ("Ready to build now"), on top of 4 existing
validation-pending items ("Needs a validation step"). That's ~14 backlog
items against parts already on hand, only the GY-521 module, CY7C68013A
board, and color-ring inductor reorder from the 2026-09-10 batch are
still in transit — see [orders.md](orders.md). **Build/validation rate,
not part supply, is the bottleneck right now**, so a top-up order would
just make the pipeline longer than the bench can work through. Revisit
once the 14-item backlog above has shrunk meaningfully (roughly half),
not on a fixed calendar schedule — the items below stay as the standing
candidates for whenever that top-up is actually warranted.

- [ ] **Linear/analog Hall-effect sensor (e.g. 49E), 5–10pk** — the
      KY-003/A3144 module already received only covers digital
      switch-output; this is still needed for the `HALLAMP` op-amp
      amplifier circuit as originally scoped.
- [ ] Decide whether to order the SFE Breadboard Power Supply Kit for
      `power_supplies/psu_medlow_lm317/` (see "Open correctness issues"
      below — currently not ordered).
- [ ] *(optional upgrade, not blocking)* **Tier 1 `REF`** — TL431A
      precision shunt reference (5 on hand, untested) could replace or
      supplement the resistor-divider + LM358 buffer for better precision.
- [ ] **LVDT transducer** — the only tier5 node with zero hardware behind
      it (`LVDTAMP`). Pricier/more niche than the items above; lower
      priority but the last unaddressed tier5 sensor.

## Ready to build now — parts on hand

- [ ] **New `TIA` build (tier2, transimpedance amplifier).** PT334-6C
      photodiode (10 on hand) + LM358P (spares available beyond the one
      used in `voltage_reference_lm358`). No folder exists yet — create
      one under `signal_conditioning/` or `measurement_tools/` with the
      usual `.spice` + `breadboard.md` + `smoke_test.py` + `README.md`
      set.
- [ ] **New `OHMMETER` build (tier3, 4-wire Kelvin).** 0.1Ω and 1Ω metal
      film resistors (20 each on hand) are the reference legs. No folder
      exists yet.
- [ ] **New `CAPBRIDGE` build (tier3, capacitance bridge).** Both the
      multilayer ceramic capacitor assortment (50V, 10 values) and the
      aluminum electrolytic capacitor kit (16V/25V/50V, 12 values)
      arrived 2026-09-10 — no longer blocked on a shipment. No folder
      exists yet.
- [ ] **`power_supplies/psu_low_v2` — physically assemble.** Wire-stripper
      blocker resolved 2026-09-03. RXEF050 polyfuse batch already
      validated (`measurement_tools/ammeter_1ohm/`). Nothing else is
      blocking this.
- [ ] **`power_supplies/psu_3xaa` — confirm and assemble.** Likely shares
      the same AA-holder lead-termination step as `psu_low_v2` above —
      verify that assumption once `psu_low_v2` is built.
- [ ] **New `PHASED` build (tier4, phase detector).** SN74HC86N quad XOR
      gate (1 on hand, arrived 2026-09-12; DIP-14 per the listing's own
      truncated variant string, unconfirmed against the physical part —
      see [parts_reference.md](parts_reference.md#sn74hc86n-quad-2-input-xor-gate)).
      Feeds tier6 `LOCKIN`. No folder exists yet.
- [ ] **`THERM` replacement — design + build.** MF52AT 10kΩ NTC thermistor
      (10 on hand, arrived 2026-09-12) replaces the "suspect faulty"
      thermistor currently in `inventory.md`. No circuit exists yet.
- [ ] **New `ACTIVELIM`/`HVPULSE` build (protection + tier7).** IRLZ44N
      logic-level MOSFET (only 1 on hand, arrived 2026-09-12) serves both
      nodes until/unless more units are ordered. No folder exists yet.
- [ ] **New `EPFIELD` build (tier5, electric field probe).** TL082
      JFET-input dual op-amp (10 on hand, arrived 2026-09-12) — the
      high-impedance front end LM358 couldn't provide. No folder exists
      yet.
- [ ] **New `CHGAMP` build (tier5, charge amplifier).** TL082 (shared with
      `EPFIELD` above) + 12mm piezo disc (20 on hand, arrived 2026-09-12)
      as the charge-output transducer. No folder exists yet.

## Needs a validation step before the part can be trusted

- [ ] **NE555 batch — 9 of 10 units still unchecked.** The
      `ne555_astable` build doubles as the per-unit check (unlike CD4066B
      or the polyfuses, which have dedicated jigs) — the unit currently
      installed passed (oscillation confirmed 2026-09-12, see
      `ne555_astable/README.md` § Validation), and the build's output
      divider fault that blocked reusing this wiring across the rest of
      the batch is now **fixed** (2026-09-13 — bad 220Ω resistor in the
      R2 leg, swapped for a verified 10kΩ; see that README's § Validation
      resolution entry). **Now unblocked to test the rest of the batch:**
      for each remaining unit, swap it into the `ne555_astable` socket,
      power up from `psu_4xaa`, run `oscillation_probe`, and expect swing
      ~2.2V (no longer pinned at 3.300V) with a crossing count in the
      dozens+ over the burst window — see `ne555_astable/README.md` §
      Expected behaviour for the fault signatures if a unit fails this
      check.
- [ ] **1N5817 Schottky diodes — not validated per-unit.** Check forward
      drop (~0.35–0.45V) on each before wiring into `psu_low_v2`; see
      `psu_4xaa/README.md` § Validation for the Pico-divider technique
      (same approach applies to any circuit using this diode).
- [ ] **CD4066BCN — switches 2–4 per chip still untested** (only switch 1
      of each of the 10 chips has been run through
      `measurement_tools/cd4066_switch_tester/`). Needed before trusting a
      specific chip/switch in a `MUX` or `DEMOD` build.
- [ ] **Glass tube fuses (2A fast-blow, 10 on hand) — no test jig built.**
      Needed before trusting one in the `psu_medlow` protection path
      (pairs with the panel-mount fuse holder, also on hand).

## Open correctness issues to resolve

- [ ] **`power_supplies/psu_medlow_usbc` — status is "incomplete /
      unverified."** The USB-C breakout is passive with no PD controller;
      VBUS may never come up without confirmed CC1/CC2 termination. Check
      termination using
      [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/)
      (clip its `R_x`/GND leads onto the two CC pins — every measurement
      on this bench goes through a Pico circuit, see
      `kb/repo_docs_conventions.md`), or add a
      PD sink controller IC + buck converter, before trusting this
      circuit. `smoke_test.py` has a static
      `PD_SINK_TERMINATION_CONFIRMED = False` check that fails on purpose
      until this is resolved.
- [ ] **`power_supplies/psu_medlow_lm317` — decide whether to order the
      SFE Breadboard Power Supply Kit.** Currently **not ordered** (see
      `power_supplies/psu_medlow_lm317/README.md`) — earlier docs
      incorrectly said "on order" in a couple of places; corrected
      2026-09-06.
- [ ] **`power_supplies/psu_ultralow_v1` — no assembled-PSU demo has ever
      been run**, only component-level validation (battery holder +
      polyfuse individually confirmed). Worth one real bench check of the
      assembled circuit.
- [ ] *(low priority, not currently blocking anything)* **`fuse_test_voltmeter`
      trip detection is non-functional** since bench wiring diverged from
      its original design — the ammeter jigs (`ammeter_10ohm`/`ammeter_1ohm`)
      replaced its role for polyfuse sorting, so this is optional cleanup,
      not a blocker.

## Blocked — waiting on a shipment

- [ ] **`INDBRIDGE`** (tier3, inductance bridge). Blocked on: color-ring
      inductor assortment (0307 1/4W, 12 values) — **original order
      cancelled by AliExpress 2026-09-07** (shipping issue), refund
      processed. **Reordered 2026-09-10** (same listing/variant), not yet
      received.
- [ ] **`SCOPELA`** (concurrent measurement tools, hardware-timed logic
      analyzer). Blocked on: CY7C68013A / EZ-USB FX2LP USB logic analyzer
      board, ordered 2026-09-10, not yet received. `sigrok`'s `fx2lafw`
      firmware supports it out of the box — no vendor software needed.
- [ ] **`ACCELIF`** (tier5). Blocked on: GY-521 (MPU6050) module, ordered
      2026-09-10, not yet received. Substitutes for the originally-scoped
      ADXL335.
- [ ] **`HALLAMP`** (tier5) — partially unlocked now that KY-003/A3144
      has arrived (2026-09-12), but not fully. It's digital switch-output
      (a presence/proximity read), not the linear-analog Hall element the
      original op-amp-amplifier design needs — a genuinely linear part
      (e.g. a 49E, see "Next AliExpress order" at the top of this file,
      not yet even ordered) is still needed to actually build the
      `HALLAMP` op-amp circuit as scoped.

## Backlog — undesigned, long-tail

Nothing below has a netlist, folder, or sourced part yet. Check
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) for
how each node connects before starting one.

- [ ] **Safety monitoring** (general-purpose): `LEAKDET`, `GFCI`,
      `ESDMON`, `INSMON`, `ARCDECT`, `OVERCUR`, `OVERVOLT`, `TEMPCOIL`,
      `EMSTOP`, `PSUHEALTH`, `FUSESTAT`, `RFRAD`, `VACPRES`, `SMOKDET` all
      undesigned. (`THERM` now has a part on hand — see "Ready to build
      now" above.)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` — no fuse/limiter circuit
      built around the Lenovo 65W adapter (on hand) or any industrial
      supply.
- [ ] **Bootstrap tier**: `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`,
      `CRTSC` all undesigned (`PASSVM` is already done via
      `fuse_test_voltmeter`).
- [ ] **Tier 2**: `VM`, `AM`, `FREQC` undesigned as dedicated circuits
      (distinct from the bootstrap ammeter jigs).
- [ ] **Tier 4**: `IA`, `DA`, `DEMOD` undesigned. (`PHASED` now has a part
      on hand — see "Ready to build now" above.)
- [ ] **Tier 5** (spacetime): `EPFIELD` and `CHGAMP` now have parts on
      hand (see "Ready to build now" above) but no folder, netlist, or
      breadboard guide yet — two net-new builds. `ACCELIF` is still
      blocked on the GY-521 module, not yet received (see "Blocked"
      above). `HALLAMP` is partially unlocked (KY-003 arrived, but a
      linear/analog sensor like the 49E is still needed for the op-amp
      circuit as scoped — see "Blocked" above). `LVDTAMP` remains fully
      backlogged — no transducer sourced yet.
- [ ] **Tier 6**: `LOCKIN`, `AAF`, `TIMEINT`, `JITTER` undesigned.
- [ ] **Tier 7** (spacetime): `RFPWR`, `MIXER`, `SWEEP` completely
      unaddressed; no parts identified. Lowest priority of the spacetime
      tiers — nothing currently depends on this starting.
- [ ] **Tier 8** (spacetime): `CALORIF`, `PWRFACT`, `ENGINT`, `NOISEFIG`
      completely unaddressed; no parts identified. Same low-priority
      status as tier 7.
- [ ] **Tier 9**: `SAMHOLD`, `ADCDRV`, `REFGEN2` undesigned. `MUX` is
      partially covered by `cd4066_switch_tester` component validation,
      but the actual multiplexer circuit isn't built.
- [ ] **Concurrent measurement tools**: `SCOPEUSBSER`, `SCOPEDSO`,
      `SCOPEBENCH`, `PRECBOX`, `LOADBANK`, `NOISEGEN`, `TESTSIG`,
      `THERMOAMP` all undesigned/unsourced. (`SCOPELA` has a part on
      order — see "Blocked — waiting on a shipment" above.)
