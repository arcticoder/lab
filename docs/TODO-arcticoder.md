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
if it has an open item. **"Ready to build now" is a ranked queue, worked
top to bottom like the rest of this file** — item 1 there is genuinely
the most valuable thing to build next, not just grouped first for
dependency-graph tidiness. The ranking is a mechanical read of
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) —
which bullet unblocks another bullet on this list, which one is a real,
named prerequisite for the next design-ready node, which one is already
mid-attempt with a fix in hand — not a claim about which circuit matters
more to the research this equipment eventually supports (see
[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)
for why that second kind of claim stays out of scope here; see that
section's own intro below for the full rule, and
[kb/todo_list_conventions.md](kb/todo_list_conventions.md) for why this
replaced the previous "menu, pick whatever" framing on 2026-09-17).
Physically assembling anything below is for confirming its design
against real hardware once — per this repo's ephemeral-circuit
convention (see `README.md` § Circuits — built & bench-tested), it goes
back to inventory afterward rather than staying wired to feed anything
downstream. "Blocked" and "Backlog" are reference sections, not action
items, until something changes their status.

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

**Soldering flux (rosin flux paste or a flux pen) — add to the next
order, or pick up locally if that's faster.** Not previously stocked or
on order. Discovered as a real blocker 2026-09-16: attempting to solder
leads onto a bare piezo disc (see `CHGAMP` bullet below) without flux
destroyed that unit (see
[parts_reference.md#piezo-element-12mm-disc](parts_reference.md#piezo-element-12mm-disc)
and [inventory.md](inventory.md) for the updated count — 19 of 20
remain, only usable for a retry once flux is on hand). This is the one
new item that should jump the "hold off on a top-up" stance below, since
it's a real dependency for a task already in progress, not a
speculative add — but it's cheap/small enough that a local hardware or
craft store may beat AliExpress transit time; use judgment.

**No other order needed right now — hold off on a top-up otherwise.** The entire
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
      priority but the last unaddressed tier5 sensor. **Now has a
      concrete literature-backed justification** (2026-09-15 scan, see
      `spacetime_circuits_dependency.md`'s "Why these tiers" section):
      published small-force experimental apparatus consistently reads
      out a beam/pendulum's displacement via a capacitive or inductive
      sensor — an LVDT is a hobbyist-scale stand-in for that role, at
      far coarser resolution than the nN-scale published instruments.
- [ ] *(contingent — try `CHGAMP` and the free retest first, see that
      bullet above and `electric_field_probe/README.md` § Bench
      findings)* **GΩ-range resistor** — `EPFIELD`'s 1MΩ bias divider
      (the largest value on hand) showed no measurable response to test
      charge sources 2026-09-15; a GΩ-range unit replacing its R2 leg is
      the concrete fix if `CHGAMP` and a direct-touch retest both still
      come up empty. Not currently on hand or on order.
- [ ] *(optional, not a blocker — see*
      *[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md))*
      **Second IRLZ44N MOSFET (or a small pack)** — the only unit on
      hand is currently in `protection/active_current_limiter/`
      (`ACTIVELIM`, 2026-09-13), but per this repo's ephemeral-circuit
      convention it returns to inventory once that build's bench check
      passes and can then serve `HVPULSE` instead. A second unit is only
      actually needed if both circuits must stay physically assembled at
      the same time — not the case today. `HVPULSE` (tier7/8) also still
      needs an actual target voltage/energy figure (above this bench's
      50V DC/30V AC numeric high-voltage threshold) and a safety design
      pass before it has a scope at all — see
      [TODO-agent.md](TODO-agent.md)'s remaining open item. Ordering
      this now wouldn't unblock anything regardless.

## Ready to build now — parts on hand, ranked by what it unlocks

**This is a ranked queue, not a menu — build item 1 next unless a bullet
explicitly says it depends on another one below it.** Ranking rule,
applied in order until one criterion decides between two bullets:

1. Does finishing it unblock another bullet in *this same list* (a real,
   stated dependency, not an inferred one).
2. Is it a real, named prerequisite (per
   [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)/
   [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md))
   for the single most literature-backed next design target currently
   identified — tier6 `LOCKIN` (see
   [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md)'s
   "Why these tiers" section). `LOCKIN` needs `PHASED` + `EPFIELD`/`CHGAMP`
   + `OSC`; `EPFIELD` and `OSC` are already satisfied, so `PHASED` and
   `CHGAMP` are the two remaining physical-assembly steps standing between
   today and `LOCKIN` becoming a real, startable `TODO-agent.md` design
   task instead of a backlog placeholder.
3. Is it already mid-attempt with a documented fix ready to apply (sunk
   cost worth closing out).
4. Does it satisfy any other real graph edge, even one pointing at a tier
   that's itself still undesigned (e.g. `THERM --> tier2`,
   `ACTIVELIM -.required.-> psu_medhigh`) — ties within this tier broken
   by the order the two dependency-graph docs declare the subgraphs in
   (`safety` before `protection`, etc.), not by feel.
5. No real edge to anything currently on the graph — pure standalone
   validation, ordered last by ascending bench effort.

This is a mechanical read of the dependency graph, not a claim about
which circuit matters more to the research this equipment eventually
supports (see
[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md))
— criteria 1–2 just happen to put the two spacetime-tier bullets first
because they're the ones the graph actually shows gating the next open
design question, not because they're spacetime-tier. See
[kb/todo_list_conventions.md](kb/todo_list_conventions.md) for the fuller
reasoning and why this replaced the previous "menu, pick whatever"
framing (2026-09-17).

Only `HVPULSE` (tier7/8, high-voltage pulse generator) still has a part
on hand but no folder — and that's a real scope decision blocking it
(what peak voltage/energy, plus a safety design pass), not file-creation
work Claude can just do; see [TODO-agent.md](TODO-agent.md)'s remaining
open item.

- [ ] **`signal_conditioning/charge_amplifier` (tier5 `CHGAMP`) —
      physically assemble. Blocked on flux — see the shopping-list item
      at the top of this file.** Folder/netlist/breadboard guide/smoke
      test exist (2026-09-13). Powered from `psu_pico_rail`. **Ranked #1**:
      criteria 2+3 above both point here — it's one of the two remaining
      real prerequisites for `LOCKIN` (with `PHASED` below), and it's
      already mid-attempt with a known, cheap fix. **2026-09-16 attempt:**
      tried soldering leads onto the bare piezo disc without flux —
      destroyed that unit (see
      `parts_reference.md#piezo-element-12mm-disc`; 19 of 20 remain).
      The disc has no pre-attached leads, so this step was always
      needed, just under-documented — `breadboard.md` now spells out
      the flux requirement. **Worth trying next once flux is on hand**:
      `electric_field_probe` (`EPFIELD`, same tier) was physically
      assembled and bench-tested 2026-09-15 — TL082 confirmed working,
      but its resistive bias-divider approach showed no measurable
      response to a piezo-spark or triboelectric test charge (see that
      circuit's own README § Bench findings). `CHGAMP`'s
      charge-integrating (capacitor-feedback) topology is a
      fundamentally different, more sensitive approach to the same kind
      of signal — may succeed where `EPFIELD`'s did not.
- [ ] **`signal_conditioning/phase_detector` (tier4, `PHASED`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke
      test/`main.py` now exist (2026-09-13). **Requires
      `oscillators/ne555_astable` wired on a breadboard** — this circuit
      taps its existing output divider rather than building a fresh
      NE555 stage; if `ne555_astable` has already been broken back down
      to inventory since its own 2026-09-13 batch validation (see
      `README.md`'s "built & bench-tested" convention on returning parts
      once nothing else needs them wired), re-assemble it first.
      **Ranked #2, right behind `CHGAMP`**: this is the other real,
      named prerequisite `LOCKIN` needs (`PHASED --> LOCKIN` in
      `general_purpose_circuit_dependency.md`) — once this and `CHGAMP`
      are both bench-confirmed, designing `LOCKIN` stops being blocked
      on undesigned inputs and becomes a real `TODO-agent.md` task.
- [ ] **1N5817 Schottky diodes — still need a per-unit forward-drop check
      for whichever unit goes into `psu_3xaa` specifically.** Two of 20
      are now confirmed: `psu_4xaa`'s (2026-09-13, GP26 ≈ 1.990V,
      identifiable by curled legs/no tape) and `psu_low_v2`'s
      (2026-09-17, GP26 ≈ 1.007V — see that circuit's own README
      § Validation). **`psu_low_v2`'s unit has no legible cathode band**
      (paint worn off) and was actually installed backward on a guess at
      first; the divider check caught it and it was flipped. It can't be
      re-identified by eye if it's ever pulled for another build — see
      `docs/parts_reference.md#1n5817-schottky-diode`. **Ranked #3
      (criterion 1 — the only bullet on this list that's a literal, stated
      hard blocker for another bullet here, and it's quick: reuse the
      Pico-divider technique already proven twice).** **Still open:** the
      same divider check on whichever diode goes into `psu_3xaa` (bullet
      directly below — still gates it) — plan is to check each at
      assembly time rather than pre-validating the whole batch upfront;
      see `psu_4xaa/README.md` § Validation for the Pico-divider
      technique (same approach applies to any circuit using this diode).
- [ ] **`power_supplies/psu_3xaa` — confirm and assemble.** `README.md`
      and `breadboard.md` are already complete and don't reference
      `psu_low_v2` for anything — it's a separate 3×AA holder chain, not
      an extension of it. Only depends on the 1N5817 diode check above
      (same diode batch, same unvalidated-forward-drop status for the
      remaining 18 units); doesn't need `psu_low_v2` assembled first and
      can be done before, after, or in parallel with it.
- [ ] **`safety/thermal_monitor` (`THERM`) — physically assemble.**
      Folder/netlist/breadboard guide/smoke test/`main.py` now exist
      (2026-09-13). Powered from `psu_pico_rail`. Fills the safety
      `THERM` gap (the existing thermistor in `inventory.md` is flagged
      "suspect faulty"). **Ranked #5 (criterion 4)**: `THERM --> tier2` is
      a real edge in the dependency graph, even though tier2's remaining
      nodes (`VM`/`AM`/`FREQC`) are themselves still undesigned — ranks
      above `CAPBRIDGE` below, which has no forward edge at all; ranks
      above `ACTIVELIM` (next bullet) too, since
      `general_purpose_circuit_dependency.md` declares the `safety`
      subgraph before `protection` — the stated tiebreak for two bullets
      that both satisfy criterion 4.
- [ ] **`protection/active_current_limiter` (`ACTIVELIM`) — physically
      assemble.** Folder/netlist/breadboard guide/smoke test now exist
      (2026-09-13). **Uses the only IRLZ44N MOSFET on hand** — fine,
      since per this repo's ephemeral-circuit convention it returns to
      inventory once this build's bench check passes, and `HVPULSE`
      (the only other node wanting one) can't use it yet regardless
      (needs a scope decision first, see "Next AliExpress order" below);
      a second unit is only needed if both must be assembled at once,
      not the case today (see
      [kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)).
      **Ranked #6 (criterion 4)**: `ACTIVELIM -.required.-> psu_medhigh`/
      `psu_high` are real edges, but both PSU tiers are themselves
      backlog with no folder — same "real edge, nothing built against it
      yet" status as `THERM` above, which leads it under the
      subgraph-declaration-order tiebreak. Needs the TL431A reference
      divider sized against whatever Cathode voltage it ends up regulated
      to on the bench — a real-hardware sizing step, not something the
      netlist could pin down in advance; see that circuit's own
      `breadboard.md` § Reference divider. **Known limitation, not a
      build defect**: this is a simple hard-trip (bang-bang) limiter with
      no hysteresis/latch, so expect it to chatter (rapidly cycle on/off)
      right at the 2A trip boundary rather than cleanly shut off — see
      that circuit's own README § Design notes if that turns out to
      matter for whatever it ends up protecting.
- [ ] **`measurement_tools/capacitance_bridge` (tier3, `CAPBRIDGE`) —
      physically assemble.** Folder/netlist/breadboard guide/smoke test
      now exist (2026-09-13), targeting the aluminum electrolytic
      capacitor kit (1µF–470µF) — see its `README.md` § Range for why the
      pF/nF ceramic assortment isn't in scope for this design. No PSU
      needed (runs off the Pico's own GPIO/3V3). **Ranked #7 (criterion
      5)**: no edge to anything currently on the graph — the last "real
      circuit" bullet before the standalone validation tail below.

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

**Standalone validation tail — no real edge to anything else on this
graph, so criterion 5 (ascending bench effort) sets the order below,
lowest effort first:**

- [ ] **`power_supplies/psu_ultralow_v1` — no assembled-PSU demo has ever
      been run**, only component-level validation (battery holder +
      polyfuse individually confirmed). One power-on check of the
      already-validated pieces — the lowest-effort item left. Worth one
      real bench check of the assembled circuit.
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
      until this is resolved. A single measurement, one step up from the
      bullet above.
- [ ] **CD4066BCN — switches 2–4 per chip still untested** (only switch 1
      of each of the 10 chips has been run through
      `measurement_tools/cd4066_switch_tester/`). Mechanically simple but
      repetitive (3 more switches × 10 chips) — more bench time than the
      two single-measurement bullets above. Not blocking anything
      else above — needed before trusting a specific chip/switch in a
      `MUX` or `DEMOD` build (both still backlog, undesigned).
- [ ] **Glass tube fuses (2A fast-blow, 10 on hand) — no test jig built.**
      Highest-effort item in this tail — needs a jig built from scratch,
      not just a measurement with an existing tool. Not blocking anything
      else above — needed before trusting one in the `psu_medlow`
      protection path (pairs with the panel-mount fuse holder, also on
      hand; `psu_medlow` itself is backlog, undesigned).
- [ ] **`power_supplies/psu_medlow_lm317` — decide whether to order the
      SFE Breadboard Power Supply Kit.** Currently **not ordered** (see
      `power_supplies/psu_medlow_lm317/README.md`) — earlier docs
      incorrectly said "on order" in a couple of places; corrected
      2026-09-06. **Not bench work at all** — a purchase decision, tracked
      here only for cross-reference; see "Next AliExpress order" at the
      top of this file, where the same item is the actual action item.
- [ ] *(lowest priority — optional cleanup, not currently blocking
      anything)* **`fuse_test_voltmeter` trip detection is non-functional**
      since bench wiring diverged from its original design — the ammeter
      jigs (`ammeter_10ohm`/`ammeter_1ohm`) replaced its role for polyfuse
      sorting, so this is optional cleanup, not a blocker.

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
      transducer sourced yet (see "Next AliExpress order" above for its
      2026-09-15 literature-backed justification).
- [ ] **Possible missing tier5 node: precision force/displacement-balance
      readout.** A 2026-09-15 literature scan (see
      `spacetime_circuits_dependency.md`'s "Why these tiers" section)
      found that every published small-force experimental family centers
      on a mechanical beam/torsion balance read out by a capacitive or
      inductive displacement sensor — `LVDTAMP` covers the sensor half of
      that, but the balance structure itself has no node anywhere in
      this graph. Not added as a new node without your say — this is a
      structural graph change, not a design task Claude should decide
      alone. Worth a decision whenever you're ready: add a node (and
      what it should be named/scoped as), or decide `LVDTAMP` alone is
      close enough and skip it.
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
