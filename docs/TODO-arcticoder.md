# TODO — arcticoder

Single human-facing checklist for this repo, covering both the
general-purpose tier graph
([general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md))
and the spacetime-research tier graph
([spacetime_circuits_dependency.md](spacetime_circuits_dependency.md)), plus
personal action items only you can do (ordering, physical verification on
the bench, decisions). Previously split across six separate
`*-arcticoder*.md` files (one active/BLOCKED/backlog trio per graph) —
consolidated back into this one file 2026-09-06 per explicit request; see
[kb/repo_docs_conventions.md](kb/repo_docs_conventions.md) if a future
session is tempted to re-split it.

Completed circuits are tracked in `README.md`'s "built & bench-tested"
table and `docs/history.md` — there's no separate completed-TODO section
here; when an item below is done, delete it rather than checking the box
and leaving it.

> A future LLM chat's own working notes on this repo belong in `docs/kb/`,
> not here.

---

## Ready to build now — parts on hand

- [ ] **`oscillators/ne555_astable` (tier1 `OSC`) — bench-build it.**
      Design simulated, now mid-build (breadboard.md/README.md updated
      2026-09-06 with explicit Pico-probe wiring for output validation).
- [ ] **New `TIA` build (tier2, transimpedance amplifier).** PT334-6C
      photodiode (10 on hand) + LM358P (spares available beyond the one
      used in `voltage_reference_lm358`). No folder exists yet — create
      one under `signal_conditioning/` or `measurement_tools/` with the
      usual `.spice` + `breadboard.md` + `smoke_test.py` + `README.md`
      set.
- [ ] **New `OHMMETER` build (tier3, 4-wire Kelvin).** 0.1Ω and 1Ω metal
      film resistors (20 each on hand) are the reference legs. No folder
      exists yet.
- [ ] **`power_supplies/psu_low_v2` — physically assemble.** Wire-stripper
      blocker resolved 2026-09-03. RXEF050 polyfuse batch already
      validated (`measurement_tools/ammeter_1ohm/`). Nothing else is
      blocking this.
- [ ] **`power_supplies/psu_3xaa` — confirm and assemble.** Likely shares
      the same AA-holder lead-termination step as `psu_low_v2` above —
      verify that assumption once `psu_low_v2` is built.
- [ ] **`power_supplies/psu_4xaa` — bench-test the build in progress.**
      Physically assembled as of 2026-09-06 (including an optional power
      switch, now documented in its own `breadboard.md`); the 2×10kΩ
      divider + Pico-ADC validation in `README.md` § Validation still
      needs to actually be run and its result recorded here / in
      `README.md`'s bench-tested table.

## Needs a validation step before the part can be trusted

- [ ] **NE555 batch — no per-unit bring-up jig exists yet** (unlike
      CD4066B or the polyfuses). The `ne555_astable` build doubles as the
      first per-unit check for whichever unit goes in it, but doesn't
      cover the rest of the batch.
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
      (clip its `R_x`/GND leads onto the two CC pins — no multimeter used
      anywhere on this bench, see `kb/repo_docs_conventions.md`), or add a
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

- [ ] **`CAPBRIDGE`** (tier3, capacitance bridge). Blocked on: multilayer
      ceramic capacitor assortment (50V, 10 values) and aluminum
      electrolytic capacitor kit (16V/25V/50V, 12 values), both ordered
      2026-08-30, not yet received.
- [ ] **`INDBRIDGE`** (tier3, inductance bridge). Blocked on: color-ring
      inductor assortment (0307 1/4W, 12 values), ordered 2026-08-30, not
      yet received.
- [ ] **`ACTIVELIM`** (protection, required by `psu_medhigh`/`psu_high`;
      also feeds spacetime tier7 `HVPULSE`). Blocked on: IRLZ44N
      logic-level MOSFET, ordered 2026-09-03, not yet received. No
      switching MOSFET of any kind was previously on hand.
- [ ] **`THERM`** (safety monitoring) replacement sensor. Blocked on:
      MF52AT 10kΩ NTC thermistor batch, ordered 2026-09-03, not yet
      received. The existing thermistor in inventory is flagged "suspect
      faulty."
- [ ] **`PHASED`** (tier4) → feeds `LOCKIN` (tier6). Blocked on: SN74HC86N
      quad XOR gate, ordered 2026-09-03, not yet received. No logic gate
      IC suited to phase detection was previously on hand (only a 74HC595
      shift register).
- [ ] **`HALLAMP`** (tier5) — partially unlocked once KY-003/A3144
      arrives, but not fully. It's digital switch-output (a
      presence/proximity read), not the linear-analog Hall element the
      original op-amp-amplifier design needs — a genuinely linear part
      (e.g. a 49E, see "Next parts to buy" below) is still needed.
- [ ] **`EPFIELD`** (tier5). Blocked on: TL082 JFET-input dual op-amp,
      ordered 2026-09-03, not yet received. LM358 (on hand) is
      bipolar-input — wrong device class for a high-impedance
      electrometer front end.
- [ ] **`CHGAMP`** (tier5). Blocked on: TL082 (same order as above) *and*
      the 12mm piezo disc batch, both ordered 2026-09-03, not yet
      received.
- [ ] **`HVPULSE`** (tier7). Blocked on: IRLZ44N logic-level MOSFET,
      ordered 2026-09-03, not yet received (same part as `ACTIVELIM`
      above).

## Next parts to buy

- [ ] **8ch 24MHz USB logic analyzer** (`SCOPELA` tier, ~$5–8, built
      around the CY7C68013A / EZ-USB FX2LP chip — `sigrok`'s `fx2lafw`
      firmware supports it out of the box, no vendor software needed).
      First tier with real hardware-timed sampling/triggering; needed to
      properly validate tier2/tier3 circuits and the CD4066 `MUX` beyond
      what the Pico's software-timed ADC can confirm. Check whether the
      listing bundles an 8-wire test-clip cable and a USB cable (dongle
      vs. separate port) before assuming nothing else is needed.
- [ ] *(optional upgrade, not blocking)* **Tier 1 `REF`** — TL431A
      precision shunt reference (5 on hand, untested) could replace or
      supplement the resistor-divider + LM358 buffer for better precision.
- [ ] **Linear/analog Hall-effect sensor (e.g. 49E), 5–10pk** — the
      KY-003/A3144 module on order only covers digital switch-output; this
      is still needed for the `HALLAMP` op-amp amplifier circuit as
      originally scoped.
- [ ] **ADXL335 analog 3-axis accelerometer breakout (or equivalent, e.g.
      GY-521) — confirm/place the order.** This was identified as the
      `ACCELIF` gap and was last known to be sitting in a shopping cart,
      not a confirmed placed order — check whether it actually went
      through, and place it if not.
- [ ] **LVDT transducer** — the only tier5 node with zero hardware behind
      it (`LVDTAMP`). Pricier/more niche than the items above; lower
      priority but the last unaddressed tier5 sensor.

## Backlog — undesigned, long-tail

Nothing below has a netlist, folder, or sourced part yet. Check
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) for
how each node connects before starting one.

- [ ] **Safety monitoring** (general-purpose): `LEAKDET`, `GFCI`,
      `ESDMON`, `INSMON`, `ARCDECT`, `OVERCUR`, `OVERVOLT`, `TEMPCOIL`,
      `EMSTOP`, `PSUHEALTH`, `FUSESTAT`, `RFRAD`, `VACPRES`, `SMOKDET` all
      undesigned. (`THERM` has a part on order — see "Blocked" above.)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` — no fuse/limiter circuit
      built around the Lenovo 65W adapter (on hand) or any industrial
      supply.
- [ ] **Bootstrap tier**: `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`,
      `CRTSC` all undesigned (`PASSVM` is already done via
      `fuse_test_voltmeter`).
- [ ] **Tier 2**: `VM`, `AM`, `FREQC` undesigned as dedicated circuits
      (distinct from the bootstrap ammeter jigs).
- [ ] **Tier 4**: `IA`, `DA`, `DEMOD` undesigned. (`PHASED` has a part on
      order — see "Blocked" above.)
- [ ] **Tier 5** (spacetime): once the blocked parts arrive, none of
      `HALLAMP`, `EPFIELD`, `LVDTAMP`, `ACCELIF`, `CHGAMP` have a folder,
      netlist, or breadboard guide yet — all five are net-new builds.
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
      `THERMOAMP` all undesigned/unsourced. (`SCOPELA` is the active-queue
      next buy, above.)

## Personal action items

Things only you can do (ordering, physical verification, decisions) —
not for Claude to work from unprompted.

- [ ] Decide whether to order the SFE Breadboard Power Supply Kit for
      `power_supplies/psu_medlow_lm317/` (see "Open correctness issues"
      above — currently not ordered).
