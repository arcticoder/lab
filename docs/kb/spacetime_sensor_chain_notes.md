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
