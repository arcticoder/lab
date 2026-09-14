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
if it has an open item. **"Ready to build now" is a menu, not a queue**
in the narrow sense that nothing in it is currently a hard blocker for
anything else on this list — pick whatever you feel like out of it, or
skip the whole section, with no scheduling cost to anything else here.
That's a different claim than it was as of yesterday, though: tier4
(`PHASED`) and tier5 (`EPFIELD`/`CHGAMP`, the electric-field-probe and
charge-amp sensor front-ends) got designed 2026-09-13 specifically
because they're the actual spacetime-research sensor chain this whole
repo exists to build toward — see `README.md`'s "Circuits — designed,
not yet built" table and
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) for
why those two nodes aren't generic infrastructure the way most of this
section's other items are. Nothing downstream of them (tier6 `LOCKIN`)
exists yet either, so there's still no scheduling deadline forcing them
ahead of anything else — but if you're choosing what to spend bench time
on based on what actually matters to the goal rather than just picking
whatever's easiest, those two are the closest thing on this list to the
real objective right now, which is why they're placed first below rather
than sorted alphabetically or by part-arrival date. "Blocked" and
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
batch validation (all 10 units) completed 2026-09-13, and the same day
`EPFIELD`, `CHGAMP`, `THERM`, `PHASED`, and `ACTIVELIM` all went from
"parts on hand, no folder" to fully designed/simulated/documented — see
[TODO-completed.md](TODO-completed.md). As of 2026-09-13, "Ready to build
now" holds 16 items against parts/circuits already on hand (up from 11
that morning — the 5 items above just finished design, not new parts
arriving; only `HVPULSE` remains in [TODO-agent.md](TODO-agent.md), and
that's blocked on a scope decision, not file-creation work — see that
file's remaining open item and
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
- [ ] *(no rush — `HVPULSE` has no defined scope yet either)* **Second
      IRLZ44N MOSFET (or a small pack)** — the only unit on hand went
      into `protection/active_current_limiter/` (`ACTIVELIM`,
      2026-09-13); `HVPULSE` (tier7/8) would need its own unit once it
      actually has a target voltage/energy and a safety design behind
      it, neither of which exist yet — see
      [TODO-agent.md](TODO-agent.md)'s remaining open item. Ordering
      this now wouldn't unblock anything; only worth doing once
      `HVPULSE`'s scope is actually decided.

## Ready to build now — parts on hand, none of this is urgent

**Nothing below is a hard blocker for anything else on this list** — the
two spacetime-sensor bullets placed first are genuinely part of the
research goal (see this file's intro), but nothing *downstream of them*
(tier6 `LOCKIN`) is designed yet, so there's still no scheduling cost to
skipping this entire section indefinitely if you'd rather not. Treat it
as a menu of what you *could* spend bench time on, not a backlog you're
behind on. Builds, validation steps, and correctness fixes are one
dependency-ordered list here, not three separate lists — when a build
needs a validation or correctness step done first, that step is the
bullet directly above it. Everything past the dependency-linked pair at
the top has no such dependency and can be done in any order. The first
two bullets are placed first deliberately (see this file's intro above),
not because anything technically requires them before the rest.

Only `HVPULSE` (tier7/8, high-voltage pulse generator) still has a part
on hand but no folder — and that's a real scope decision blocking it
(what peak voltage/energy, plus a safety design pass), not file-creation
work Claude can just do; see [TODO-agent.md](TODO-agent.md)'s remaining
open item. Everything else that was in that state as of yesterday
(`PHASED`, a `THERM` replacement, `ACTIVELIM`, `EPFIELD`, `CHGAMP`) got
designed, simulated, smoke-tested, and documented 2026-09-13 — see
[TODO-completed.md](TODO-completed.md) for the full entry — and now has
its bench-assembly bullet below.

- [ ] **`signal_conditioning/electric_field_probe` (tier5 `EPFIELD`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke test
      now exist (2026-09-13). Powered from `psu_pico_rail` (already
      built) — no PSU assembly needed first. No electrode has been
      ordered; any small bare conductor (a stripped jump-wire end or
      foil scrap) works for a first build, per that circuit's own
      README. No current downstream consumer (tier6 `LOCKIN` is
      undesigned) — but this is a direct spacetime-research sensor
      build, not generic infra; see this file's intro for why it's
      placed here rather than sorted by part-arrival date.
- [ ] **`signal_conditioning/charge_amplifier` (tier5 `CHGAMP`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke test
      now exist (2026-09-13). Powered from `psu_pico_rail`. Same
      no-current-downstream-consumer situation as `EPFIELD` above, same
      reason it's prioritized here anyway.
- [ ] **1N5817 Schottky diodes — still need a per-unit forward-drop check
      for whichever units go into `psu_low_v2`/`psu_3xaa` specifically.**
      The diode already installed in `psu_4xaa` is now past
      continuity/orientation-only trust: re-ran the divider check
      2026-09-13 after finding and fixing wiring issues on a rebuild
      (`psu_4xaa/validation_breadboard2.jpg`) and got GP26 ≈ 1.990 V,
      matching the ~1.9 V target — that specific diode's forward-conduction
      behavior is confirmed. It's identifiable in the batch by curled legs
      and no tape (every other 1N5817 is still straight-legged and taped).
      **Still open:** the same check, on whichever diode(s) actually go
      into `psu_low_v2` and `psu_3xaa` (both bullets directly below — this
      still gates both) — plan is to check each at assembly time rather
      than pre-validating the whole batch upfront; see
      `psu_4xaa/README.md` § Validation for the Pico-divider technique
      (same approach applies to any circuit using this diode).
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
      downstream consumer specifically calling for a `TIA` (tier4/tier5
      now have some designed nodes — `PHASED`, `EPFIELD`, `CHGAMP` — but
      none of them actually use a transimpedance amplifier) — build
      whenever you feel like it.
- [ ] **`measurement_tools/capacitance_bridge` (tier3, `CAPBRIDGE`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke test
      now exist (2026-09-13), targeting the aluminum electrolytic
      capacitor kit (1µF–470µF) — see its `README.md` § Range for why the
      pF/nF ceramic assortment isn't in scope for this design. No PSU
      needed (runs off the Pico's own GPIO/3V3). No current downstream
      consumer — build whenever you feel like it.
- [ ] **`safety/thermal_monitor` (`THERM`) — physically assemble.**
      Folder/netlist/breadboard guide/smoke test/`main.py` now exist
      (2026-09-13). Powered from `psu_pico_rail`. Fills the safety
      `THERM` gap (the existing thermistor in `inventory.md` is flagged
      "suspect faulty") — no current downstream consumer, build whenever
      you feel like it.
- [ ] **`signal_conditioning/phase_detector` (tier4, `PHASED`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke
      test/`main.py` now exist (2026-09-13). **Requires
      `oscillators/ne555_astable` wired on a breadboard** — this circuit
      taps its existing output divider rather than building a fresh
      NE555 stage; if `ne555_astable` has already been broken back down
      to inventory since its own 2026-09-13 batch validation (see
      `README.md`'s "built & bench-tested" convention on returning parts
      once nothing else needs them wired), re-assemble it first. Feeds
      tier6 `LOCKIN` (still undesigned) — no current downstream consumer,
      but see this file's intro for why this and the two spacetime
      sensor bullets above it are worth prioritizing over pure
      busywork regardless.
- [ ] **`protection/active_current_limiter` (`ACTIVELIM`) — physically
      assemble.** Folder/netlist/breadboard guide/smoke test now exist
      (2026-09-13). **Consumes the only IRLZ44N MOSFET on hand** — fine,
      since `HVPULSE` (the only other node wanting one) can't use it yet
      regardless of availability (needs a scope decision first, see
      "Next AliExpress order" below). Needs the TL431A reference divider
      sized against whatever Cathode voltage it ends up regulated to on
      the bench — a real-hardware sizing step, not something the netlist
      could pin down in advance; see that circuit's own `breadboard.md`
      § Reference divider. **Known limitation, not a build defect**: this
      is a simple hard-trip (bang-bang) limiter with no hysteresis/latch,
      so expect it to chatter (rapidly cycle on/off) right at the 2A trip
      boundary rather than cleanly shut off — see that circuit's own
      README § Design notes if that turns out to matter for whatever it
      ends up protecting.

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
      still undesigned. (`THERM` is done — see "Ready to build now" above.)
- [ ] **PSU system**: `psu_medhigh`/`psu_high` themselves — no complete
      PSU tier built around the Lenovo 65W adapter (on hand) or any
      industrial supply. The limiter piece those tiers need
      (`ACTIVELIM`) is done — see "Ready to build now" above — but that's
      a protection stage, not the PSU tier itself.
- [ ] **Bootstrap tier**: `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`,
      `CRTSC` all undesigned (`PASSVM` is already done via
      `fuse_test_voltmeter`).
- [ ] **Tier 2**: `VM`, `AM`, `FREQC` undesigned as dedicated circuits
      (distinct from the bootstrap ammeter jigs).
- [ ] **Tier 4**: `IA`, `DA`, `DEMOD` still undesigned. (`PHASED` is
      done — see "Ready to build now" above.)
- [ ] **Tier 5** (spacetime): `EPFIELD` and `CHGAMP` are done — see
      "Ready to build now" above. `ACCELIF` is still blocked on the
      GY-521 module, not yet received (see "Blocked" above). `HALLAMP` is
      partially unlocked (KY-003 arrived, but a linear/analog sensor like
      the 49E is still needed for the op-amp circuit as scoped — see
      "Blocked" above). `LVDTAMP` remains fully backlogged — no
      transducer sourced yet.
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
