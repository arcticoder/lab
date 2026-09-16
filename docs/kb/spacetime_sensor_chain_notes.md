# KB: spacetime sensor-chain design notes (2026-09-13)

Audience: future LLM sessions working in this repo. Design-rationale
notes from building `EPFIELD`, `CHGAMP`, `THERM`, `PHASED`, and
`ACTIVELIM` in one pass (see `TODO-completed.md`'s 2026-09-13 second-pass
entry). None of this belongs in the human-facing docs — the user gets
the concise version in each circuit's own README.

## Why this pass happened: resolving "is this actually needed?" by designing the downstream tiers, not by arguing about it

`TODO-arcticoder.md`'s "Ready to build now" section had settled into a
framing (established in `todo_list_conventions.md`'s own dated entry) of
"nothing here blocks anything else, since tier4+ is itself undesigned" —
accurate as of 2026-09-13 morning, but the user pushed back explicitly:
if items in that section aren't contributing to the repo's actual stated
goal (`README.md`'s spacetime-research framing), they shouldn't be
presented as neutral "pick whenever" busywork — the fix isn't better
wording, it's actually designing the downstream tiers so the question
has a real answer. The user's framing: treat Claude as having "robot
arms" and just do the FTL-research design work directly, with the human
as the physical executor. This is a stronger mandate than
`TODO-agent.md`'s normal "pick an item, no urgency" workflow — it's a
one-time push to close out everything already flagged as ready-to-design
in that file, specifically because doing so would clarify (not just
restate) which "Ready to build now" items are real spacetime-research
prerequisites vs. generic infra of ambiguous present value.

**Result**: `EPFIELD` and `CHGAMP` are *directly* named tier5 nodes in
`spacetime_circuits_dependency.md` — building them isn't "generic infra
that might matter later," it's literally the sensor front-end work the
spacetime tier graph calls for. `PHASED` (tier4, general-purpose graph)
feeds tier6 `LOCKIN`, which is what would eventually do synchronous
detection on `EPFIELD`/`CHGAMP`'s weak output signals — so `PHASED` is a
real link in the spacetime sensing chain even though the dependency
graph doesn't draw a direct `PHASED --> SPACETIME` edge (the graph
represents this indirectly via `tier5 -.feeds.-> GENERAL`, i.e. tier5
sensor output feeds back into general-purpose tier6 processing — a
one-directional-looking edge that's really describing a consumption
relationship, not just a resource contribution). This is worth
re-deriving explicitly next time someone re-reads that graph and wonders
why `PHASED`/`LOCKIN` don't have a direct spacetime-tier edge — they
don't need one; the `-.feeds.->` edges already encode it, just not in
the most legible direction.

**What this pass did NOT resolve**: `HVPULSE` (tier7/8) remains blocked
on an actual human scope decision (a target peak voltage/energy, plus a
real safety design pass) — no amount of "just design it" instruction
should produce a fabricated HV spec. This was the one item in
`TODO-agent.md`'s queue correctly left alone rather than forced through;
see its own entry in `TODO-agent.md` for why.

## The psu_pico_rail-for-ADC-safety pattern (new, worth reusing)

Every op-amp sensor front-end built before this pass
(`voltage_reference_lm358`, `transimpedance_amplifier`) powers the op-amp
from a battery PSU tier (`psu_low_v2`, etc.) and documents a headroom
caveat against the Pico ADC's 0-3.3V ceiling — real hardware then
occasionally produces an out-of-range reading if that caveat's math is
ever wrong (see `ne555_astable/README.md`'s pinned-3.300V incident: an
output-divider fault that would have been structurally impossible to
create the same failure mode if the op-amp itself were on the same rail
as the ADC reference).

`EPFIELD`/`CHGAMP`/`THERM` all switch to powering their op-amp/logic
directly from `psu_pico_rail` (the Pico's own onboard 3.3V rail) instead.
This isn't just a supply-choice detail — it's a structural safety
improvement: the op-amp output is then *incapable* of exceeding the
ADC's safe input range, regardless of resistor values or op-amp
behavior, rather than merely unlikely to if the math is done right. The
tradeoff, documented honestly in each circuit's README: 3.3V is below
what a part like the TL082 is typically specified for (most dual JFET
op-amps in this class assume a wider split-supply range), so there's an
unconfirmed real-hardware risk that the buffer simply doesn't function
correctly at this supply voltage at all. **This hasn't been validated on
real hardware yet** — when one of these three circuits gets physically
assembled, that's the first thing to check, and if it turns out TL082
genuinely won't run at 3.3V, the fix path is documented in each README
(step up to `psu_low_v2`/`psu_4xaa` with an attenuator ahead of the ADC,
not a topology change).

**General lesson for future single-supply sensor front-ends**: default
to `psu_pico_rail` when the circuit's own current draw is trivial (µA-nA
range, well inside its ~100mA budget) and the failure mode of "output
exceeds ADC range" is worth designing out structurally rather than
managing with a caveat — reserve battery PSU tiers for circuits that
either need real current headroom or benefit from being independent of
the Pico's own rail for some other reason.

## Bias-network pattern for bipolar single-supply sensing

Both `EPFIELD` and `CHGAMP` needed to represent a signal that can swing
both positive and negative around some rest point on a single supply
rail (a floating electrode's induced signal; a piezo's compress/release
charge pulses). The pattern used in both: a 1MΩ/1MΩ divider from VCC to
GND, biasing the relevant op-amp input to VCC/2, so the output has equal
headroom to swing either direction from that midpoint rather than
clipping at 0V on every excursion in one direction. This is worth
reusing for any future single-supply sensor front-end with a genuinely
bipolar signal (e.g. a future AC-coupled sensor) — the two 1MΩ resistors
are cheap (10 on hand) and the pattern is now precedented twice.

## XOR phase detector validated via two independent, non-phase-locked oscillators — a legitimate technique, not a workaround

`PHASED`'s design note in `TODO-agent.md` flagged an unresolved question:
a classic XOR phase detector needs two same-frequency square waves at a
*variable* phase offset, and this bench only had one oscillator
(`ne555_astable`). The resolution — a Pico GPIO PWM output, tuned near
the NE555's frequency but **not** synchronized to it — works precisely
*because* it's unsynchronized: two free-running oscillators at nominally
the same frequency always drift in relative phase (their frequencies are
never exactly equal), continuously sweeping the XOR's duty cycle through
its full range. This is a legitimate, standard way to validate that an
XOR gate responds to *relative* phase between two independent signals
(watch the filtered output sweep 0V→3.3V→0V... on real hardware) without
needing a phase-locked or frequency-locked reference — building one of
those is real, separate future work for tier6 `LOCKIN`, not something
`PHASED` itself needs. Worth remembering if a similar "I only have one
of X but need two for this classic topology" situation comes up
elsewhere: check whether the topology's validation actually requires the
two sources to be *locked*, or just *independently present*.

## A hard-trip current limiter's chattering isn't a caveat to write around — it's a real electrical fact SPICE will refuse to converge on

Building `ACTIVELIM` as a simple comparator-driven hard trip (no
hysteresis, no latch) hit a genuine ngspice convergence failure when the
fault case was modeled as a single closed-loop operating point (forcing
`Rload` low enough to trip): `Error: Transient op failed, timestep too
small... trouble with swmod-instance sfet`. This is not a numerical
fluke to route around with different solver settings — it's ngspice
correctly reporting that **no stable DC operating point exists** for
this topology under sustained fault: open the switch → sense voltage
collapses toward 0V → comparator sees "safe" → recloses → retrips →
repeat. In real hardware this is chattering, not a clean shutoff — a
well-known limitation of bang-bang current limiters with no
hysteresis/latch, here rediscovered empirically via a simulation refusing
to solve rather than via prior EE knowledge being applied top-down.

**Fix used**: don't ask the closed loop to find a fixed point that
doesn't exist. Split the simulation into (a) a closed-loop *normal* case
(which does have a stable fixed point and converges fine) and (b) an
open-loop *fault-detection* case — a fixed test current forced through
an isolated copy of the sense resistor, checking only that the
comparator's threshold math correctly identifies the over-limit
condition, without needing the unstable feedback loop to settle.

**General lesson**: if a closed-loop `.op` fails to converge with a
"timestep too small" / gmin-stepping-failure message on a circuit
containing a bang-bang (hysteresis-free) switching element, check
whether the *specific operating condition being simulated* has a
genuinely stable equilibrium at all before assuming it's a modeling
mistake — a real bistable/oscillatory circuit will refuse to converge to
a single point for the same reason it would misbehave on the bench, and
that's worth documenting as a finding, not suppressing by decomposing
the simulation until it stops complaining without also writing up why.

## A resistive bias divider's own value sets a hard sensitivity ceiling — "the op-amp works" and "the sensor is sensitive enough" are two separate claims

`electric_field_probe` (`EPFIELD`) was physically assembled and
bench-tested 2026-09-15 (see `TODO-completed.md`'s 2026-09-15 entry and
that circuit's own README § Bench findings for the full writeup). Two
findings worth separating clearly, because it's easy to conflate them
into one "didn't work" verdict:

1. **The TL082 follower itself works fine** at 3.3V single-supply, below
   its datasheet-recommended minimum — rest output was ~1.693–1.701V
   against a simulated 1.650V ideal, a small stable offset, not pinned
   at either rail. This confirms the README's own "many parts in this
   class still function below spec, just with more offset" prediction.
2. **The sensor showed no measurable response to test charge sources**
   (piezo-igniter spark, triboelectrically-charged tape) — but this is
   *also* exactly what the design's own § Design notes predicted: the
   1MΩ/1MΩ bias divider presents only ~500kΩ at the sensing node (the
   two legs in parallel), vs. the GΩ range a dedicated electrometer
   front end needs. The reasoning worth internalizing: with a
   low-picofarad stray input capacitance, 500kΩ gives an RC decay time
   constant on the order of a microsecond — any charge the electrode
   couples in bleeds back to the bias point far faster than the
   circuit's own sampling can observe it (`main.py` samples the ADC at
   1ms intervals, prints every 0.5s). A GΩ resistor would push that time
   constant into an observable range; nothing about the op-amp changes.

**Why this matters generally**: a "no response" bench result on a
follower/buffer-based sensor doesn't by itself tell you whether the
active component or the passive network around it is the bottleneck —
check the passive network's own input impedance against the physics of
what's being sensed (here: electrostatic induction needs a
high-impedance path so charge doesn't bleed off before it can be read)
before concluding the amplifier needs replacing or re-testing in
isolation. In this case the follower's rest-voltage accuracy (within
~50mV of ideal, not railed) was itself sufficient evidence it was
working — isolating the TL082 for a separate test would not have added
information the rest-voltage reading didn't already give.

**Also worth noting**: `main.py`'s printed "deviation from rest" is
`v - 1.65` (a hardcoded constant recomputed every call), not a captured
baseline sample from an earlier reading. Multiple printed lines showing
similar deviation values means the output is sitting in a tight band
around a fixed offset from ideal — not "three repeated measurements
against an earlier baseline." Worth double-checking this distinction
before reading a run of near-identical "deviation" values as either
confirming or ruling out a response to an external stimulus.

**Secondary, compounding factor**: the as-built electrode was a long
(~30–40cm) Dupont jumper trailing off the desk edge — the opposite of
`breadboard.md`'s own explicit "keep this row's wiring short" guidance
for high-impedance nodes. Didn't cause the null result by itself (the
500kΩ-impedance argument above is sufficient on its own), but adds noise
susceptibility for free with no sensitivity benefit — worth fixing on
any rebuild regardless of whether the GΩ-resistor fix happens.

## Literature scan session, 2026-09-15 — instrumentation requirements for tier5–8, sourced but theory-agnostic

Session context: the user questioned why tier5/7/8 circuits were being
designed with "no current downstream consumer" and asked for a
literature-backed pass on what experimental validations these nodes
actually need to serve, working backwards from real published
small-force/anomalous-thrust research rather than the tier graph's own
generic labels. Explicitly approved reading the actual methodology
papers behind this kind of hobbyist sensor kit for real design
justification, on the condition that **no specific theory, program, or
researcher name appears in any current-state doc — including this kb
file** (re-confirmed 2026-09-15: [[no_fringe_science_terms]]'s ban
explicitly covers "kb prose," not just README/dependency-graph text — do
not relax that here just because this file is LLM-only). Everything
below is written to that constraint: functional description only, bare
URLs for citation, never a quoted paper title if the title itself
contains a banned/adjacent name.

**Search scope**: six web searches across three independent published
families of small-force/thrust claims — (a) a high-voltage
capacitor/sharp-electrode family, historically attributed by mainstream
analysis to an aerodynamic ion/corona-wind effect; (b) a closed-cavity
RF-power family tested by multiple independent groups with null results;
(c) a resonant piezoelectric-stack family requiring a precisely
phase-controlled dual drive. This was a first-pass scan (a double
handful of sources), not an exhaustive dozens-of-papers review — treat
the findings below as a starting rationale to build on, not a closed
literature review.

**Findings, condensed** (full writeup with citations is in
`spacetime_circuits_dependency.md`'s own "Why these tiers" section —
that's the current-state doc; this entry is the session's working notes
behind it):

- Every family's published apparatus centers on a **precision
  force/displacement balance** (knife-edge beam balance, torsion
  pendulum, capacitive displacement sensor), resolving tens of nN to
  ~1µN. Nothing in this bench's tier graph names that mechanical
  structure directly — `LVDTAMP` is the closest existing fit (an LVDT is
  one real way to read a beam/pendulum's displacement) but a dedicated
  torsion-/beam-balance node doesn't exist. Flagged as a real gap in
  `spacetime_circuits_dependency.md` and `TODO-arcticoder.md`'s Backlog,
  not added as a new node without the human's say — that's a structural
  graph change, a bigger decision than a rationale addition.
- **Thermal drift is the single most-repeated false-positive source**
  across every family's published methodology — one group built a
  specific mechanical arrangement (an inverted, counterbalanced pendulum
  design) purely to cancel it, and explicitly warns that thermal/
  mechanical load plus high current creates false-positive force
  readings. This reframes tier8 `CALORIF` (and the already-built safety
  `THERM`) as artifact-rejection instruments specifically, not generic
  "energy measurement" — worth keeping that framing in mind if `CALORIF`
  ever gets designed.
- **RF power + frequency sweep** is central to the closed-cavity family
  (sweep to find cavity resonance, compute thrust-per-watt against a
  classical radiation-pressure floor) — direct tier7 `RFPWR`/`SWEEP`
  justification.
- **Precisely phase-controlled dual drive signals + frequency sweep to
  find peak response** is central to the resonant piezoelectric-stack
  family. This is the strongest justification found for tier6 `LOCKIN`
  specifically (not just "generically useful DSP") — synchronous
  detection at a known drive frequency is the standard technique for
  pulling a small periodic force signal out of noise here, and it's the
  direct next stage downstream of `PHASED` (built) and `EPFIELD`/`CHGAMP`
  (bench-tested).
- **Ion/corona-wind characterization** (particle-image velocimetry,
  electrostatic probes) is the standard technique for isolating that
  specific confound in the high-voltage capacitor/electrode family —
  functionally identical to what `EPFIELD` already does (sense a local
  field/charge). Gives `EPFIELD` a second concrete role beyond detecting
  a target field: ruling out this specific confound in any high-voltage
  setup a future experiment repo runs.

**How to apply if asked to go deeper**: the six searches used generic
functional query terms (e.g. "asymmetric capacitor high voltage
electrostatic thrust experiment methodology," "closed RF cavity thrust
measurement torsion balance," "resonant piezoelectric thruster phase
measurement instrumentation," "torsion balance nanonewton force sensor
design") rather than the theories' own names — this kept search results
usable without needing the banned names in the query either, and is the
pattern to repeat for follow-up scans (e.g. going deeper on `LVDTAMP`'s
displacement-sensor requirements, or on the still-unaddressed
force/displacement-balance gap noted above).
