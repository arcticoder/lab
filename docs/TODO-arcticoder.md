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
AliExpress order.** Not previously stocked or on order. Discovered as a
real blocker 2026-09-16: attempting to solder leads onto a bare piezo
disc (see `CHGAMP` bullet below) without flux destroyed that unit (see
[parts_reference.md#piezo-element-12mm-disc](parts_reference.md#piezo-element-12mm-disc)
and [inventory.md](inventory.md) for the updated count — 19 of 20
remain, only usable for a retry once flux is on hand). This is the one
item that should jump the "hold off on a top-up" stance below, since
it's a real dependency for a task already in progress, not a
speculative add. **2026-09-19: you'd rather wait out AliExpress transit
than make a store run, even for something this cheap/small** — batch it
into the same order as the tier5/7 shopping-list items below rather
than treating it as a special local-purchase case.

**Old backlog vs. new tier5/7 nodes — two different answers as of
2026-09-18.** The entire 2026-09-03 batch (TL082, MF52AT thermistor,
IRLZ44N MOSFET, piezo disc, SN74HC86N XOR gate, KY-003 Hall module)
arrived 2026-09-12. The NE555 batch validation (all 10 units) completed
2026-09-13, and the same day `EPFIELD`, `CHGAMP`, `THERM`, `PHASED`, and
`ACTIVELIM` all went from "parts on hand, no folder" to fully
designed/simulated/documented — see [TODO-completed.md](TODO-completed.md).
As of 2026-09-13, "Ready to build now" held 16 items against
parts/circuits already on hand; only the GY-521 module, CY7C68013A board,
and color-ring inductor reorder from the 2026-09-10 batch are still in
transit — see [orders.md](orders.md). **For that existing backlog,
build/validation rate, not part supply, is still the bottleneck** — no
reason to top up any of the items already covered above.

**That reasoning doesn't extend to the three tier5/7 nodes added
2026-09-18** (`FORCEBAL`, `SIPMFE`, `LASERDRV` — see
`spacetime_circuits_dependency.md`'s "Why these new tiers" section for the
literature grounding): each has **zero hardware sourced**, the same status
`LVDTAMP` was already flagged at below — this isn't a build/validation-rate
problem, it's a real ordering gap for a mechanical-dependency reason (a
zero-hardware tier-graph node), not a narrative one. `SIPMFE` in particular
needs a genuinely new part class nothing else on this bench uses.

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
      **Not the only option for `FORCEBAL`'s readout** (see the bullet
      below) — worth deciding both together.
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

**New for the 2026-09-18 tier5/7 additions — zero hardware sourced for
any of these three:**

- [ ] *(deferred by you 2026-09-19 — revisit later, not currently on the
      shopping list)* **SiPM (silicon photomultiplier) breakout module,
      small active area (1×1mm–3×3mm class), 1–2pcs — for tier5
      `SIPMFE`.** Needed for the new SiPM/scintillator particle-counting
      front-end node. Published hobbyist designs bias these around
      24–30V DC (some modules include an onboard boost from 5V) —
      comfortably under this bench's 50V DC threshold (see
      `kb/circuit_lifecycle_and_repo_scope.md`). A genuinely new part
      class — nothing already on hand substitutes. **Even the bare sensor
      is expensive enough that you've chosen to hold off on this node
      entirely for now** — not a rejection of `SIPMFE`, just not an
      active shopping-list item until you decide otherwise.
- [ ] *(deferred alongside the SiPM bullet above 2026-09-19 — it only
      pairs with that module, no reason to buy it alone)* **Small plastic
      scintillator tile/paddle (or equivalent scintillating block) — for
      tier5 `SIPMFE`, same node as above.** A GPS module for
      cross-station event timestamping would be a further enhancement on
      top of both, same reasoning.
- [ ] *(no urgency, and the laser-diode half is now off the table — see
      below)* **High-power LED — for tier7 `LASERDRV`.** The on-hand 5mm
      red/blue/green/white/yellow LEDs (10 each, `inventory.md`) can drive
      a first `LASERDRV` proof-of-concept for free right now, no purchase
      needed. **2026-09-19: you raised an eye-safety concern about the
      laser-diode option this bullet originally paired with LEDs as an
      alternative.** Fair concern, and an honest answer: a diffuse LED
      (even a bright one) carries no meaningful eye hazard the way a
      laser diode does — a laser (even a low-power Class 3R/3B module,
      which is the class typically sold as a "laser diode module") can
      cause retinal damage from a direct or *specular* reflection (the
      `FORCEBAL` mirror bullet below is exactly that kind of reflective
      surface), and doing that safely needs real engineering controls
      (an enclosure, a beam dump, wavelength-rated laser safety goggles,
      keeping the beam path below eye level) that aren't in place on this
      bench today. That's not something to wave through as "safe enough"
      without those controls. **Decision: stay on the free LED path for
      `LASERDRV`'s first proof-of-concept indefinitely; the laser-diode
      upgrade is off the shopping list until/unless you decide to invest
      in the enclosure/goggles/beam-dump controls that would make it
      genuinely safe** — a dedicated *higher-power LED* (still not a
      laser) remains the real eventual need for a measurable
      radiation-pressure force on `FORCEBAL`, and stays on the table
      without that safety question attached.
- [ ] *(not currently on the shopping list — see the note below on why
      `FORCEBAL` doesn't need this to proceed)* **Thin torsion fiber
      (fine fishing line or wire) and a small front-surface mirror — for
      a torsion-pendulum build of tier5 `FORCEBAL`.** Not currently on
      hand or on order, and not added to the next AliExpress order.
      **2026-09-19: `FORCEBAL`'s own node name is "Torsion/**Beam-Balance**
      Displacement Readout" — a knife-edge beam balance (a rigid arm on a
      pivot, no suspension fiber at all) is the other mechanical form the
      node already allows**, and pairs with a capacitive-plate readout via
      `CAPBRIDGE` (tier3 — designed/simulated/smoke-tested, already queued
      as "Ready to build now" below) using foil/scrap-copper plates —
      the same "household materials, no purchase" precedent this file
      already uses for `VIBISO`/`RIPPLETANK` below. **That route needs
      nothing from AliExpress and nothing from a store — it's buildable
      once you're ready to try it.** The fiber+mirror bullet stays here
      only for the *torsion* variant specifically (a torsion pendulum is
      more sensitive than a beam balance, per the literature cited in
      `spacetime_circuits_dependency.md`) — worth adding to a future
      AliExpress order only if the beam-balance/capacitive route proves
      insufficient once tried.

**Two 2026-09-18 mechanical build objectives that likely need no order at
all** — `VIBISO` (vibration/seismic isolation platform: a weighted
platform on soft-compliance feet, e.g. rubber pads or partially-inflated
inner tubes/balloons — household materials) and `RIPPLETANK` (a shallow
tray/baking dish, water, and a glass or acrylic sheet as the submerged
depth-step insert). Its wave driver doesn't need tier1 `SIMPGEN` either —
that node is itself still backlog/undesigned (see Backlog section below) —
`pico/leds/gpio_pwm_led/` (already built in the sibling `pico/` repo) is
SIMPGEN's own documented "optional alternative" and can drive a small
motor/speaker dipper directly. Check what's already around the apartment
before adding either `VIBISO` or `RIPPLETANK` to a cart.

**2026-09-19: what else has to exist to actually run an experiment on
either, once built.** Neither needs anything *ordered* to physically
build (see above), but "build the platform/tank" and "run an experiment
with it" are different milestones:

- **`VIBISO`** is a mechanical prerequisite *for other nodes*
  (`FORCEBAL`, `LASERDRV` — see `spacetime_circuits_dependency.md`), not
  an experiment in its own right — there's nothing to read out from an
  isolation platform by itself. To actually *quantify* how well it
  isolates (rather than just judging it by eye/feel), the natural
  instrument is tier5 `ACCELIF` (an accelerometer interface, comparing
  vibration on vs. off the platform) — currently **blocked**, waiting on
  the GY-521 module already in transit (see "Blocked" below). Until that
  arrives, `VIBISO` can still be built and used qualitatively (as the
  mechanical base under a future `FORCEBAL`/`LASERDRV` build), just not
  bench-measured for its own isolation performance.
- **`RIPPLETANK`** needs a wave driver to do anything at all — tier1
  `SIMPGEN` is itself undesigned, but `pico/leds/gpio_pwm_led/` (already
  built in the sibling `pico/` repo) is its documented stand-in and can
  drive a small motor/speaker dipper directly, no new build required.
  Reading wavefront phase shift *electronically* instead of by eye would
  use tier4 `PHASED` — **now bench-tested as of today (2026-09-19, see
  "Ready to build now" section)** — feeding tier6 `LOCKIN` for a clean
  synchronous readout, but `LOCKIN` itself is still undesigned. Net: a
  first qualitative `RIPPLETANK` demo (visual wave refraction, driven by
  the sibling repo's PWM dipper) needs no further build at all; an
  electronic phase-shift readout is a real future step gated on `LOCKIN`,
  not a blocker for trying the tank itself.

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
   + `OSC`; `EPFIELD`, `OSC`, and now `PHASED` (bench-tested 2026-09-19,
   see `README.md`'s "built & bench-tested" table) are all satisfied, so
   `CHGAMP` is the one remaining physical-assembly step standing between
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
— criteria 1–2 just happen to put `CHGAMP` first because it's the one
bullet the graph actually shows still gating the next open design
question (`LOCKIN`) now that `PHASED` is bench-tested, not because it's
spacetime-tier. See
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
      criteria 2+3 above both point here — with `PHASED` now bench-tested
      (2026-09-19, see below and `README.md`), this is the *one* remaining
      real prerequisite for `LOCKIN`, and it's already mid-attempt with a
      known, cheap fix. **2026-09-16 attempt:** tried soldering leads onto
      the bare piezo disc without flux — destroyed that unit (see
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
- [ ] **1N5817 Schottky diodes — still need a per-unit forward-drop check
      for whichever unit goes into `psu_3xaa` specifically.** Two of 20
      are now confirmed: `psu_4xaa`'s (2026-09-13, GP26 ≈ 1.990V,
      identifiable by curled legs/no tape) and `psu_low_v2`'s
      (2026-09-17, GP26 ≈ 1.007V — see that circuit's own README
      § Validation). **`psu_low_v2`'s unit has no legible cathode band**
      (paint worn off) and was actually installed backward on a guess at
      first; the divider check caught it and it was flipped. It can't be
      re-identified by eye if it's ever pulled for another build — see
      `docs/parts_reference.md#1n5817-schottky-diode`. **Ranked #2
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
      "suspect faulty"). **Ranked #4 (criterion 4)**: `THERM --> tier2` is
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
      **Ranked #5 (criterion 4)**: `ACTIVELIM -.required.-> psu_medhigh`/
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
      needed (runs off the Pico's own GPIO/3V3). **Ranked #6 (criterion
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
      done — bench-tested 2026-09-19, see `README.md`'s "built &
      bench-tested" table.)
- [ ] **Tier 5** (spacetime): `EPFIELD` and `CHGAMP` are done — see
      "Ready to build now" above. `ACCELIF` is still blocked on the
      GY-521 module, not yet received (see "Blocked" above). `HALLAMP` is
      partially unlocked (KY-003 arrived, but a linear/analog sensor like
      the 49E is still needed for the op-amp circuit as scoped — see
      "Blocked" above). `LVDTAMP` remains fully backlogged — no
      transducer sourced yet (see "Next AliExpress order" above for its
      2026-09-15 literature-backed justification). **New 2026-09-18:**
      `FORCEBAL` and `SIPMFE` are also fully backlogged — zero hardware
      sourced for either, see "Next AliExpress order" above and
      `spacetime_circuits_dependency.md`'s "Why these new tiers" section
      for the justification. Neither is a `TODO-agent.md` design task yet
      — that file's own workflow expects a specific sourced part (a
      specific SiPM model's bias/pulse spec, a chosen displacement-sensing
      approach for `FORCEBAL`) before a netlist can mean anything, same
      precedent as every other backlog tier5 node above.
- [x] ~~Possible missing tier5 node: precision force/displacement-balance
      readout.~~ **Resolved 2026-09-18**: added as `FORCEBAL`, at your own
      explicit direction this session (not a unilateral Claude call — see
      `spacetime_circuits_dependency.md`'s "Why these new tiers" section).
      `LVDTAMP` remains one real way to instrument it; a capacitive-plate
      approach read by `CAPBRIDGE` (designed/simulated, not yet physically
      assembled — see "Ready to build now," ranked #6) is the other, and
      doesn't require ordering anything new (see "Next AliExpress order"
      above).
- [ ] **Tier 6**: `LOCKIN`, `AAF`, `TIMEINT`, `JITTER` undesigned. **New
      as of 2026-09-18**: `TIMEINT`/`JITTER` now have a concrete near-term
      consumer once `SIPMFE` above is sourced (coincidence timing between
      two scintillator paddles, and jitter in that timing) — still
      undesigned, but no longer just a generic DAQ placeholder; see
      `spacetime_circuits_dependency.md`'s "Why these new tiers" section.
- [ ] **Tier 7** (spacetime): `RFPWR`, `MIXER`, `SWEEP` completely
      unaddressed; no parts identified — still lowest priority of the
      original spacetime tiers, nothing currently depends on these
      starting. **New 2026-09-18**: `LASERDRV` also backlogged, zero
      hardware sourced (though on-hand 5mm LEDs give a free first test —
      see "Next AliExpress order" above) — this one does have a real
      near-term consumer (`FORCEBAL`'s radiation-pressure-driven variant,
      and the optical-lever/interferometer/fiber-loop chain built from
      general-purpose `TIA`/`DA`), unlike `RFPWR`/`MIXER`/`SWEEP`.
- [ ] **Tier 8** (spacetime): `CALORIF`, `PWRFACT`, `ENGINT`, `NOISEFIG`
      completely unaddressed; no parts identified. Same low-priority
      status as tier 7's original three nodes.
- [ ] **Mechanical/optical build objectives (new 2026-09-18,
      `spacetime_circuits_dependency.md`'s `mech` subgraph)**: `VIBISO`
      and `RIPPLETANK` — neither is a circuit (no netlist/smoke_test
      applies), and neither likely needs an AliExpress order at all, see
      "Next AliExpress order" above. Not a `TODO-agent.md` item either —
      there's no file-creation step analogous to a netlist for a
      mechanical build; whether either gets its own `README.md`/build
      notes once attempted is a call to make when you actually build one,
      not before.
- [ ] **Tier 9**: `SAMHOLD`, `ADCDRV`, `REFGEN2` undesigned. `MUX` is
      partially covered by `cd4066_switch_tester` component validation,
      but the actual multiplexer circuit isn't built.
- [ ] **Concurrent measurement tools**: `SCOPEUSBSER`, `SCOPEDSO`,
      `SCOPEBENCH`, `PRECBOX`, `LOADBANK`, `NOISEGEN`, `TESTSIG`,
      `THERMOAMP` all undesigned/unsourced. (`SCOPELA` has a part on
      order — see "Blocked — waiting on a shipment" above.)
