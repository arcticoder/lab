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

**No urgent order needed right now, but the pipeline is thinning** — 6 of
the last 9 in-transit items (TL082, MF52AT thermistor, IRLZ44N MOSFET,
piezo disc, SN74HC86N XOR gate, GY-521 accelerometer module) arrived
2026-09-12, unlocking several new builds below (see "Ready to build now").
Only 3 items are still in transit: KY-003 Hall module (ordered
2026-09-03), and the CY7C68013A logic analyzer board + color-ring
inductor reorder (both ordered 2026-09-10) — see [orders.md](orders.md).
That's thinner than the prior 9-item pipeline, so a top-up order is worth
placing soon (transit runs a few weeks) rather than waiting for these 3
to also land before shopping again — the items below are the standing
candidates for that top-up.

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
- [ ] **New `ACCELIF` build (tier5, accelerometer interface).** GY-521
      (MPU6050) module (1 on hand, arrived 2026-09-12) — I2C only, no
      analog frontend needed. No folder exists yet.
- [ ] **New `EPFIELD` build (tier5, electric field probe).** TL082
      JFET-input dual op-amp (10 on hand, arrived 2026-09-12) — the
      high-impedance front end LM358 couldn't provide. No folder exists
      yet.
- [ ] **New `CHGAMP` build (tier5, charge amplifier).** TL082 (shared with
      `EPFIELD` above) + 12mm piezo disc (20 on hand, arrived 2026-09-12)
      as the charge-output transducer. No folder exists yet.

## Needs a validation step before the part can be trusted

- [ ] **NE555 batch — only 1 of the batch has been through a per-unit
      check** (unlike CD4066B or the polyfuses, which have dedicated
      jigs). The `ne555_astable` build doubles as that check for
      whichever unit goes in it — the unit currently installed passed
      (oscillation confirmed 2026-09-12, see `ne555_astable/README.md`
      § Validation) — but the rest of the batch is still unchecked.
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

- [ ] **`oscillators/ne555_astable` — fix the output divider (still open
      after one attempted fix).** Bench-built and oscillation confirmed
      2026-09-12 (113 zero-crossings, ~1.5kHz, inside the expected trim
      range — see `README.md` § Validation) using
      `measurement_tools/oscillation_probe/`. This chip/build **passes**
      its per-unit validation as an oscillator — that part is done. The
      output divider (two 10kΩ resistors, `breadboard.md` §4) is a
      **separate, still-unresolved** issue: it isn't actually halving
      pin 3's swing, so GP26 reads a full 0–3.3V swing pinned at the
      ADC's own saturation point instead of the expected ~2.75-2.9V.
      **First attempted fix (2026-09-12, same day) did not resolve it:**
      re-wired R1/R2 into an actual series pair and bridged the
      breadboard's two vertical ground rails together, then re-ran
      `oscillation_probe` — result was statistically the same as before
      the fix (swing still ~3.3V pinned). See `ne555_astable/README.md`
      § Validation for both readings side by side. **Next step:** stop
      re-wiring by eye and isolate it with
      `measurement_tools/resistance_measurement` instead — power down
      `psu_4xaa` first, then check R1 (pin 3→tap) reads ~10kΩ, R2
      (tap→GND) reads ~10kΩ, and the tap→GP26 jumper shows continuity.
      Current through the existing wiring is small enough this almost
      certainly hasn't damaged the Pico pin, but don't leave it wired
      this way, and don't reuse this same GP26 wiring across the rest of
      the NE555 batch (next bullet) until it's actually fixed — every
      additional chip swap on a still-broken divider repeats the same
      over-voltage exposure to GP26.
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
- [ ] **`HALLAMP`** (tier5) — partially unlocked once KY-003/A3144
      arrives (not yet received), but not fully even then. It's digital
      switch-output (a presence/proximity read), not the linear-analog
      Hall element the original op-amp-amplifier design needs — a
      genuinely linear part (e.g. a 49E, see "Next AliExpress order" at
      the top of this file) is still needed.

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
- [ ] **Tier 5** (spacetime): `EPFIELD`, `ACCELIF`, `CHGAMP` now have
      parts on hand (see "Ready to build now" above) but no folder,
      netlist, or breadboard guide yet — three net-new builds. `HALLAMP`
      is still only partially unlocked (KY-003 digital module still in
      transit, and a linear/analog sensor like the 49E is still needed
      regardless — see "Blocked" above). `LVDTAMP` remains fully
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
