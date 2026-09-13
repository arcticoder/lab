# TODO — arcticoder

Single human-facing checklist for this repo: things that need your hands,
eyes, or a purchasing decision — ordering, physically assembling/wiring a
circuit, and bench validation. Anything that's just creating a file
(a netlist, a breadboard guide, a smoke test, a folder for a new circuit)
is **not** on this list — that's Claude's job, tracked separately in
[TODO-agent.md](TODO-agent.md) and done proactively, before a build ever
shows up here as something for you to physically assemble. See
[docs/kb/todo_list_conventions.md](kb/todo_list_conventions.md) for why
this split exists.

**"Next AliExpress order" comes first because it's the one section with
a real clock** (shipping transit runs a few weeks) — work that one first
if it has an open item. **"Ready to build now" is a menu, not a queue**:
as of 2026-09-13, nothing in it is currently blocking any other buildable
work (everything downstream — tier4 and beyond — is itself still
undesigned), so pick whatever you feel like out of it, or ignore the
whole section, with no cost to anything else on this list. "Blocked" and
"Backlog" are reference sections, not action items, until something
changes their status.

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
SN74HC86N XOR gate, KY-003 Hall module) arrived 2026-09-12. The NE555
batch validation (all 10 units) completed 2026-09-13 — see
[TODO-completed.md](TODO-completed.md). As of 2026-09-13, "Ready to build
now" holds 11 items against parts/circuits already on hand (down from 17
— 6 moved to [TODO-agent.md](TODO-agent.md) pending a folder/design, or
were dropped as already satisfied; see that section's own note and
[docs/kb/todo_list_conventions.md](kb/todo_list_conventions.md)); only the
GY-521 module, CY7C68013A board, and color-ring inductor reorder from the
2026-09-10 batch are still in transit — see [orders.md](orders.md).
**Build/validation rate, not part supply, is the bottleneck right now**,
so a top-up order would just make the pipeline longer than the bench can
work through. Revisit once that backlog has shrunk meaningfully (roughly
half), not on a fixed calendar schedule — the items below stay as the
standing candidates for whenever that top-up is actually warranted.

- [ ] **Linear/analog Hall-effect sensor (e.g. 49E), 5–10pk** — the
      KY-003/A3144 module already received only covers digital
      switch-output; this is still needed for the `HALLAMP` op-amp
      amplifier circuit as originally scoped.
- [ ] Decide whether to order the SFE Breadboard Power Supply Kit for
      `power_supplies/psu_medlow_lm317/` (see "Ready to build now"
      below — currently not ordered).
- [ ] *(optional upgrade, not blocking)* **Tier 1 `REF`** — TL431A
      precision shunt reference (5 on hand, untested) could replace or
      supplement the resistor-divider + LM358 buffer for better precision.
- [ ] **LVDT transducer** — the only tier5 node with zero hardware behind
      it (`LVDTAMP`). Pricier/more niche than the items above; lower
      priority but the last unaddressed tier5 sensor.

## Ready to build now — parts on hand, none of this is urgent

**Nothing below is blocking anything else currently on this list** — every
downstream consumer (tier4 and beyond) is itself still undesigned, so
there's no cost to skipping this entire section indefinitely. Treat it as
a menu of what you *could* spend bench time on, not a backlog you're
behind on. Builds, validation steps, and correctness fixes are one
dependency-ordered list here, not three separate lists — when a build
needs a validation or correctness step done first, that step is the
bullet directly above it. Everything past the dependency-linked pair at
the top has no such dependency and can be done in any order.

Five other circuits have parts on hand but no folder/netlist/breadboard
guide yet (`PHASED`, a `THERM` replacement, `ACTIVELIM`/`HVPULSE`,
`EPFIELD`, `CHGAMP`) — that design/file-creation work is tracked in
[TODO-agent.md](TODO-agent.md), not here, since it's not something you do.
They'll appear below, as bench-assembly bullets, once that's done.

- [ ] **1N5817 Schottky diodes — not validated per-unit.** Check forward
      drop (~0.35–0.45V) on each before wiring into `psu_low_v2` or
      `psu_3xaa` (both bullets directly below — this gates both, not just
      the first one); see `psu_4xaa/README.md` § Validation for the
      Pico-divider technique (same approach applies to any circuit using
      this diode). `psu_4xaa` uses the same diode type and is already
      trusted, but only by continuity/orientation check, not a measured
      forward drop — do the real measurement before either build below,
      not after.
- [ ] **`power_supplies/psu_low_v2` — physically assemble.** Wire-stripper
      blocker resolved 2026-09-03. RXEF050 polyfuse batch already
      validated (`measurement_tools/ammeter_1ohm/`). Depends on the
      1N5817 diode check directly above — nothing else is blocking this.
- [ ] **`power_supplies/psu_3xaa` — confirm and assemble.** `README.md`
      and `breadboard.md` are already complete and don't reference
      `psu_low_v2` for anything — it's a separate 3×AA holder chain, not
      an extension of it. Only depends on the 1N5817 diode check two
      bullets above (same diode batch, same unvalidated-forward-drop
      status); doesn't need `psu_low_v2` assembled first and can be done
      before, after, or in parallel with it.
- [ ] **`signal_conditioning/transimpedance_amplifier` (tier2, `TIA`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke test
      now exist (2026-09-13). Per
      [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)
      (`psu_low --> tier2` edge), its supply-rail prerequisite is
      `psu_low_v2` (two bullets above), not `psu_3xaa`. No current
      downstream consumer (tier4/spacetime are still undesigned) — build
      whenever you feel like it.
- [ ] **`measurement_tools/capacitance_bridge` (tier3, `CAPBRIDGE`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke test
      now exist (2026-09-13), targeting the aluminum electrolytic
      capacitor kit (1µF–470µF) — see its `README.md` § Range for why the
      pF/nF ceramic assortment isn't in scope for this design. No PSU
      needed (runs off the Pico's own GPIO/3V3). No current downstream
      consumer — build whenever you feel like it.

**No `OHMMETER` bullet here on purpose.**
`measurement_tools/resistance_measurement` (already built and in active
use — see its own README) already covers the tier3 `OHMMETER` node's
present need with a 2-wire divider, the same kind of substitution
`capacitance_bridge` above makes for a literal 4-arm bridge. A dedicated
4-wire Kelvin design would only matter for measuring resistances small
enough that lead/contact resistance corrupts a 2-wire reading — nothing
on this bench currently needs that precision (its only consumer, tier4,
is undesigned). Not queued anywhere; revisit only if a specific
low-resistance measurement actually needs it.

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
- [ ] **`power_supplies/psu_ultralow_v1` — no assembled-PSU demo has ever
      been run**, only component-level validation (battery holder +
      polyfuse individually confirmed). Worth one real bench check of the
      assembled circuit.
- [ ] **CD4066BCN — switches 2–4 per chip still untested** (only switch 1
      of each of the 10 chips has been run through
      `measurement_tools/cd4066_switch_tester/`). Not blocking anything
      else above — needed before trusting a specific chip/switch in a
      `MUX` or `DEMOD` build (both still backlog, undesigned).
- [ ] **Glass tube fuses (2A fast-blow, 10 on hand) — no test jig built.**
      Not blocking anything else above — needed before trusting one in
      the `psu_medlow` protection path (pairs with the panel-mount fuse
      holder, also on hand; `psu_medlow` itself is backlog, undesigned).
- [ ] **`power_supplies/psu_medlow_lm317` — decide whether to order the
      SFE Breadboard Power Supply Kit.** Currently **not ordered** (see
      `power_supplies/psu_medlow_lm317/README.md`) — earlier docs
      incorrectly said "on order" in a couple of places; corrected
      2026-09-06. This is an ordering decision, not bench work — see
      "Next AliExpress order" at the top of this file, where the same
      item is tracked as a purchase candidate.
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
      undesigned. (`THERM` now has a part on hand — folder/design pending
      in [TODO-agent.md](TODO-agent.md).)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` — no fuse/limiter circuit
      built around the Lenovo 65W adapter (on hand) or any industrial
      supply.
- [ ] **Bootstrap tier**: `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`,
      `CRTSC` all undesigned (`PASSVM` is already done via
      `fuse_test_voltmeter`).
- [ ] **Tier 2**: `VM`, `AM`, `FREQC` undesigned as dedicated circuits
      (distinct from the bootstrap ammeter jigs).
- [ ] **Tier 4**: `IA`, `DA`, `DEMOD` undesigned. (`PHASED` now has a part
      on hand — folder/design pending in [TODO-agent.md](TODO-agent.md).)
- [ ] **Tier 5** (spacetime): `EPFIELD` and `CHGAMP` now have parts on
      hand but no folder, netlist, or breadboard guide yet — two net-new
      builds pending in [TODO-agent.md](TODO-agent.md). `ACCELIF` is still
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
