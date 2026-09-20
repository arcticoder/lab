# KB: TODO-arcticoder.md conventions

Audience: future LLM sessions working in this repo. Process/meta notes
about how `TODO-arcticoder.md` itself is structured and maintained — the
user already knows this stuff first-hand, so none of it belongs in the
human-facing file itself. See also
[repo_docs_conventions.md](repo_docs_conventions.md) for the rest of this
repo's docs conventions.

## History and ordering authority

`TODO-arcticoder.md` was previously split across six separate
`*-arcticoder*.md` files (one active/BLOCKED/backlog trio per dependency
graph — general-purpose and spacetime). Consolidated back into one file
2026-09-06 per explicit user request. Don't re-split it.

**Claude has full control over the file's ordering as of 2026-09-07.**
The file is meant to be worked strictly top-to-bottom, one section at a
time — whichever section is first to still have an unchecked item is
next, and within that section the first bullet is the most important.
This replaces picking whatever feels like the next logical build on your
own initiative. Any re-ordering this implies (e.g. a "ready to build"
item turning out to be blocked on something elsewhere in the file, or a
section's contents needing to move because they never get reached in
practice) should happen by editing the file directly, not by
second-guessing the stated order while working from it.

## "Move to TODO-completed.md, don't delete" convention

For items on *this* list specifically (not circuit bench-test status,
which lives in `README.md`'s "built & bench-tested" table and
`docs/history.md`): when a TODO item is done, move it to
[TODO-completed.md](../TODO-completed.md) as a dated entry instead of
deleting it. This gives an audit trail that makes it easy to confirm
something was actually done and avoid re-proposing/duplicating it later —
mirrors the convention in the sibling `aqei-bridge` repo's
`docs/TODO-completed.md` / `docs/TODO-BLOCKED.md`.

## Sections with real lead-time consequences must sit near the top, not just wherever they logically fit (established 2026-09-09)

`TODO-arcticoder.md` originally had "Next parts to buy" and "Personal
action items" (ordering-related) positioned near the bottom of the file
(after "Blocked" and ahead of only "Backlog"). Because the file is worked
strictly top-to-bottom and there's almost always an unchecked item in an
earlier section, these two sections never actually got reached in
practice — the user flagged this explicitly (paraphrased: "lines
170–255 will never get actioned as long as it's further down the file, I
work the tasks starting from the top").

Fixed by merging both sections into one new top section, "Next
AliExpress order — action needed," placed immediately after the intro
(before "Ready to build now"). Rationale for putting ordering ahead of
bench-work sections specifically: AliExpress shipping from China runs a
few weeks, so an unplaced order is a compounding cost (every day it sits
unordered is a day added to the eventual arrival), whereas bench-work
items don't have that same clock running — they just wait for the
operator's bench time. The user's stated supply-chain objective (see
`docs/orders.md`'s intro) is to always have a few items en route, which
requires this section to actually get checked and actioned regularly
rather than accumulating stale entries at the bottom.

General lesson for future restructuring of this file: before adding a
new section, ask whether it has an external clock attached (shipping
transit, a decision blocking someone else, anything that keeps costing
time while unaddressed) — if so, it belongs near the top regardless of
how it fits thematically with neighboring sections, since bottom-of-file
placement in a top-to-bottom-worked list is equivalent to "will not be
looked at." "Backlog — undesigned, long-tail" was deliberately left at
the bottom in this same pass — genuinely no clock on it (nothing is
blocked waiting for a backlog item to be designed), so its bottom
position is correct, not an oversight to fix the same way.

## A single arrival report can unblock several "Blocked" bullets at once — check every remaining bullet's part name, not just the ones the arrival report seems to obviously match (2026-09-12)

When 6 items arrived in one report (the full 2026-09-03 batch: TL082,
MF52AT, IRLZ44N, piezo, SN74HC86N, KY-003 — see
[ordering_ingestion_notes.md](ordering_ingestion_notes.md)'s matching
entry, including the correction after an initial KY-003/GY-521 mixup), it
closed 6 of the 9 bullets then sitting in "Blocked — waiting on a
shipment" (`THERM`, `PHASED`, `ACTIVELIM`, `HVPULSE`, `EPFIELD`,
`CHGAMP` — `ACTIVELIM`/`HVPULSE` share one MOSFET so count as one
part-driven unblock; `HALLAMP` only *partially* unblocked, since KY-003
is digital-only and the tier5 op-amp design still needs a linear sensor).
`INDBRIDGE`, `SCOPELA`, and `ACCELIF` remained fully blocked, on the 3
items from the separate 2026-09-10 batch (GY-521, CY7C68013A, inductor
reorder) that didn't arrive. Each newly-unblocked bullet moved into
"Ready to build now" following the section's existing convention (name
the part, its quantity, arrival date, and "No folder exists yet") rather
than being deleted — none of these have a folder/netlist/breadboard
guide, so they're genuinely new build targets, not completions. Also had
to sweep the "Backlog — undesigned, long-tail" section for parenthetical
cross-references pointing at "Blocked" for `THERM`/`PHASED`/tier5 nodes
and repoint them at "Ready to build now" — those asides go stale
silently since nothing enforces they track the referenced section's
actual current contents. General lesson: when an arrival report resolves
more than one item, re-check the *entire* "Blocked" section against the
arrival list rather than hand-matching just the parts you already expect
to be there — and don't assume which specific part name goes with which
batch just because two candidate part codes (KY-003, GY-521) look
similarly formatted; re-verify the exact string per
[ordering_ingestion_notes.md](ordering_ingestion_notes.md)'s entry on
that mixup before writing status changes across four files.

## Merge build/validation/correctness into one dependency-ordered list — don't split by category the way "Next AliExpress order" is split out (established 2026-09-13)

Until 2026-09-13, "Ready to build now," "Needs a validation step before
the part can be trusted," and "Open correctness issues to resolve" were
three separate sections/headers, in that order. The user flagged this
explicitly: a build in "Ready to build now" could depend on an item sitting
in "Needs a validation step" (e.g. `power_supplies/psu_low_v2`'s assembly
bullet said "nothing else is blocking this" while the 1N5817 Schottky
diode forward-drop check — which its own wiring needs — sat in the
*other* section, un-cross-referenced), and the file is worked strictly
top-to-bottom, so a reader doing the "Ready to build" bullet first could
build on an unvalidated part without realizing it. The user's framing:
this is *not* the same situation as "Next AliExpress order" sitting apart
from bench-work sections (see the entry above this one) — ordering has
its own external clock (shipping transit) that justifies a separate
top-of-file section, but build/validate/correctness are all bench work
with no such distinct clock, so splitting them by category just hides
real dependencies between bullets in different sections.

Fixed by merging all three into one section, keeping the "Ready to build
now — parts on hand" header, ordered so that whenever a build bullet
depends on a validation/correctness bullet, the dependency comes first
and says so explicitly (e.g. 1N5817 diode check → `psu_low_v2` assembly,
each bullet naming what it depends on). Items with no dependency on
anything above them follow in no particular order; items that don't
block anything currently in the list (e.g. CD4066BCN switches 2–4, which
only matter once `MUX`/`DEMOD` exist) say so explicitly rather than being
sorted purely by category.

General lesson for future restructuring: before splitting the file into
separate sections by *kind* of task (build vs. validate vs. fix vs.
order), check whether items across the proposed sections actually depend
on each other. If they can, a category split will silently hide that
dependency from someone working the file top-to-bottom one section at a
time — merge into a single ordered list instead, and only split out a
section when it has its own genuinely independent reason (like ordering's
shipping-transit clock, see the entry above).

**Correction, same day:** the first pass of this merge also wrote
`psu_3xaa` assembly as depending on `psu_low_v2` assembly ("Likely shares
the same AA-holder lead-termination step... verify that assumption once
`psu_low_v2` is built") — a dependency that was invented, not read off
anything. `psu_3xaa/README.md` and `breadboard.md` already existed in
full at the time and don't reference `psu_low_v2` for any open step; the
two are independent 2×AA/3×AA holder chains that both happen to use the
1N5817 batch, so both depend on the diode-check bullet directly, not on
each other. Separately, the `TIA` bullet was placed right after
`psu_3xaa` with no dependency stated, which read as "needs `psu_3xaa`"
simply from list position — but
[general_purpose_circuit_dependency.md](../general_purpose_circuit_dependency.md)
has `psu_low --> tier2` (not `psu_3aa --> tier2`), so `TIA`'s real
prerequisite is `psu_low_v2`, already satisfied by the bullet above
`psu_3xaa`. **Lesson: before writing "X depends on Y" (or ordering two
bullets so it reads that way) into this file, check it against
`general_purpose_circuit_dependency.md`/`spacetime_circuits_dependency.md`
and against the target circuit's own `README.md`/`breadboard.md` if one
exists — don't infer a dependency from "these two things seem similar" or
from where a new bullet happens to land in the list.** The user caught
this by literally asking "checking what this is needed for" at each step
and finding no source backing the implied chain — that check should
happen before the bullet is written, not after.

## `TODO-agent.md` split from `TODO-arcticoder.md`: file-creation work vs. bench/ordering work (established 2026-09-13)

Through 2026-09-13, "Ready to build now" mixed two genuinely different
kinds of task under one bullet style: physical bench work the user has to
do by hand (assemble a PSU, validate a diode batch), and file-creation
work that's entirely Claude's job (write a `.spice` netlist,
`breadboard.md`, `smoke_test.py`, `README.md` for a circuit that has
parts on hand but "no folder exists yet"). The user flagged this
explicitly and with some heat: creating those files is not something they
should ever be asked to do — "we live in a post-AI world now... systemize
a way to ensure the dependent tasks that can be completed by you are
performed before I attempt to complete the bench steps myself." They
pointed at `aqei-bridge/docs/TODO.md` (a sibling repo's pure agent-task
list) as the pattern to follow.

Fixed by creating [TODO-agent.md](../TODO-agent.md): every "no folder
exists yet" item moves there instead of sitting in
`TODO-arcticoder.md` as something that reads like an open task for the
user. `TODO-arcticoder.md` should only ever gain a bullet for a given
circuit once its folder/netlist/breadboard/smoke-test already exist — at
that point the bullet is purely "physically assemble," per how the `TIA`
and `CAPBRIDGE` bullets were rewritten the same day once
`signal_conditioning/transimpedance_amplifier/` and
`measurement_tools/capacitance_bridge/` were actually built. Both files
share the same `TODO-completed.md` audit-trail convention (one shared
log, not a second one per file) — a completed *design* task and a
completed *bench* task are still both just "this item is done," so
splitting the completion log by which file the item came from would add
bookkeeping with no reader benefit.

**Rule going forward: before adding "New `X` build... no folder exists
yet" to `TODO-arcticoder.md`, that's a signal the item belongs in
`TODO-agent.md` instead, not a valid `TODO-arcticoder.md` entry.** Design,
simulate, smoke-test, and document the circuit there (or immediately, if
asked to build something specific — see the `TIA`/`CAPBRIDGE` precedent),
then add the bench-assembly bullet to `TODO-arcticoder.md` once real
files back it.

## "Ready to build now" is a no-urgency menu, not a mandatory queue, when nothing downstream needs its contents yet (established 2026-09-13, **superseded 2026-09-17 — see the entry near the end of this file**)

Separately from the file-creation split above, the user also pushed back
on `TODO-arcticoder.md` reading like "a laundry list" even after the
file-creation items were accounted for — the remaining bench-work bullets
(validate a diode batch, assemble a PSU, etc.) were still presented with
the same top-to-bottom "do this next" framing as the ordering section,
despite most of them not actually blocking anything else on the bench.
Checking the dependency graphs confirmed this: as of 2026-09-13, every
downstream consumer of "Ready to build now"'s contents (tier4 and beyond)
is itself still undesigned, so nothing currently *requires* any of these
builds to happen — they're all genuinely optional right now, parts-on-
hand busywork, not a backlog the user is behind on.

Fixed by reframing the section's own intro (not by moving anything out of
it): explicit language that nothing in it blocks anything else, that it's
a menu to pick from rather than a queue to clear, and that skipping the
whole section costs nothing. This is a narrower, more specific version of
"Sections with real lead-time consequences must sit near the top" (below)
— that entry is about section *placement*; this one is about section
*framing* within an already-correctly-placed section. **Rule for future
edits: before presenting a section as an ordered queue, check whether its
items actually gate anything else currently on the list (via the
dependency graphs) — if none of them do, say so explicitly in the
section's own intro rather than leaving the reader to infer urgency from
list position alone.** Revisit this framing if/when tier4+ circuits start
getting designed and something in this section becomes a real
prerequisite again.

## Don't propose rebuilding something that already exists — check `README.md`'s bench-tested table and existing folders before writing "New `X` build" (established 2026-09-13)

`TODO-arcticoder.md` briefly carried a "New `OHMMETER` build (tier3,
4-wire Kelvin)" bullet listing the 0.1Ω/1Ω metal film resistors as
reference legs, with "No folder exists yet." This was wrong on the
premise, not just the wording: `measurement_tools/resistance_measurement/`
already exists, is already built and bench-tested, and is in active
reuse (it isolated the `ne555_astable` output-divider fault — see
`repo_docs_conventions.md`'s `cd4066_switch_tester`/`ne555_astable`
entries). It's a 2-wire divider, not a literal 4-wire Kelvin bridge, so it
doesn't perfectly match the dependency graph's `OHMMETER` node label — but
per the same substitution logic as `PASSVM` (see
`repo_docs_conventions.md`), that's close enough to satisfy the node's
*present* need. The user's own words: "I've already built an ohmmeter. If
more are needed I'll build them when they're required."

Fixed by removing the bullet entirely (not just editing it) and replacing
it with a short prose note explaining why no `OHMMETER` bullet exists —
the precedent set by `capacitance_bridge`'s own README, which documents
the identical reasoning for why it substitutes a timing comparison for a
literal AC bridge (see the entry above). **Rule for future TODO edits:
before writing "New `X` build" for any dependency-graph node, check
`README.md`'s "built & bench-tested" table and this repo's existing
folders for something that already functionally satisfies the node — a
node's literal label (e.g. "4-Wire Kelvin Ohmmeter") doesn't require a
literal from-scratch rebuild if a simpler existing circuit already covers
its current use, and proposing one anyway reads as not having checked
first.** Only propose the more precise/literal version once something
concrete actually needs the improvement the simpler version can't
provide.

## "Ready to build now" being a no-urgency menu is a snapshot, not a permanent verdict — re-check it whenever the downstream tiers actually get designed (established 2026-09-13, same day as the entry above; **superseded 2026-09-17 — see the entry near the end of this file**)

The entry above ("'Ready to build now' is a no-urgency menu... when
nothing downstream needs its contents yet") was correct as of that
morning, but the user pushed back the same day: presenting items as
"no cost to skip" reads as settled when it was really just "true given
today's undesigned state of tier4+" — and if some of those items
*aren't* actually contributing to the repo's stated goal
(`README.md`'s spacetime-research framing), the fix isn't wording, it's
designing the downstream tiers so the question has a real answer instead
of an assumed one. The user's framing: treat Claude as having "robot
arms" and directly do the FTL-research design work already queued in
`TODO-agent.md`, rather than waiting for it to be picked up at whatever
pace felt natural.

This produced the second 2026-09-13 pass: `EPFIELD`, `CHGAMP` (both
directly-named tier5 spacetime nodes), `THERM`, `PHASED` (feeds tier6
`LOCKIN`, which will process the tier5 sensors' output), and `ACTIVELIM`
all designed/simulated/smoke-tested/documented in one sitting — see
[spacetime_sensor_chain_notes.md](spacetime_sensor_chain_notes.md) for
the design decisions and
`TODO-completed.md`'s matching dated entry for the summary. `HVPULSE`
was deliberately left alone (needs an actual scope decision from the
user, not more design effort — see `TODO-agent.md`'s remaining open
item).

**Rule for future sessions**: "nothing downstream needs this yet" is a
true statement about the *current* state of the dependency graph, not a
permanent property of the item. When enough of `TODO-agent.md`'s open
items get designed in one pass that the graph's actual shape changes
(a "Ready to build now" item's downstream consumer stops being
undesigned), re-check whether that item's own framing/urgency in
`TODO-arcticoder.md` needs to change too — don't let it keep reading as
"generic, skippable busywork" once it's actually become a real
prerequisite for something.

## Don't frame "ready to build now" items by closeness to the spacetime-research objective, and don't assume a shared part needs duplicating (2026-09-14; **narrowed 2026-09-17 — see the entry near the end of this file: ranking by mechanical dependency-graph facts is fine, only ranking by narrative closeness to the outside research goal is barred**)

User correction, 2026-09-14: this file's own intro (and several bullets)
had drifted into saying the `EPFIELD`/`CHGAMP`/`PHASED` bullets were
placed first because they're "the actual spacetime-research sensor chain
this whole repo exists to build toward" / "the closest thing on this
list to the real objective." That overstates this repo's scope — it
designs/simulates/documents/bench-validates equipment only; the actual
research experiments run in a separate future repo and are never started
here. Grouping those bullets first for dependency-graph clarity is fine;
ranking them as more important than the rest of the "menu, not queue"
section is not, since there's no in-repo objective to rank against.
Separately, the IRLZ44N MOSFET shared between `ACTIVELIM` and `HVPULSE`
was documented as requiring a second unit before `HVPULSE` could
proceed — wrong, since every circuit here is ephemeral (see
[[lab_pico_repo_structure]]'s build → bench-test → return-to-inventory
convention): the single unit returns to inventory once `ACTIVELIM`'s own
bench check passes, and a duplicate is only actually needed if both
circuits must be assembled at the same time. Full writeup, plus the new
50V DC/30V AC numeric "high voltage" threshold established the same day,
is in
[circuit_lifecycle_and_repo_scope.md](circuit_lifecycle_and_repo_scope.md) —
read that before writing "no current downstream consumer, but build it
anyway" language into either TODO file again.

## Don't write future-session working notes into TODO-arcticoder.md itself

A future LLM chat's own working notes on this repo belong in `docs/kb/`
(this directory), not in `TODO-arcticoder.md` — that file is strictly the
human-facing checklist. This used to be stated as a blockquote reminder
inside `TODO-arcticoder.md` itself; removed 2026-09-09 per user feedback
(it was a repeated reminder of something already established by every
kb file's own "Audience: future LLM sessions... not the end user" header,
and reading it in the TODO list itself was pointless friction for the
user). The rule still applies — it just doesn't need restating inside the
human-facing file anymore.

## "No current downstream consumer" reads as "no purpose" on a re-read a day later — it means something narrower

`TODO-arcticoder.md` used "No current downstream consumer (tier6
`LOCKIN` is undesigned)" for `EPFIELD`/`CHGAMP`, and similar phrasing for
`THERM`/`CAPBRIDGE`/`TIA`. Caught 2026-09-15 (the day after this phrasing
was written 2026-09-13): re-encountering that line without the same
context fresh caused the user to read it as "these circuits have no
purpose at all — why build them?" and to question whether this repo is
actually in service of the spacetime-research goal at all. The phrase's
*intended* meaning is narrower and still accurate: no other **in-repo**
node currently consumes this one's output (the next tier6 processing
stage isn't designed yet) — it says nothing about whether the circuit
itself serves the dependency graph's stated purpose. `EPFIELD`/`CHGAMP`
specifically ARE named tier5 sensor-interface nodes in
`spacetime_circuits_dependency.md`, whose own header states they exist
to serve as sensing building blocks for whatever FTL-research experiment
eventually needs them (see [[circuit_lifecycle_and_repo_scope]] for why
running that experiment itself is out of this repo's scope) — that's a
real purpose, just not one satisfied by another *in-repo* node yet.

**How to apply**: when writing "no current downstream consumer" (or
similar) about a tier5/7/8 (spacetime) node, make the distinction
explicit inline rather than assuming the reader will re-derive it from
the file's intro paragraph — e.g. "no further in-repo processing stage
built yet (tier6 `LOCKIN` is undesigned) — this doesn't mean the sensor
itself lacks a purpose; it's one of the tier5 nodes `spacetime_circuits_
dependency.md` scopes as an FTL-research sensor front-end." For
general-purpose nodes (`THERM`, `CAPBRIDGE`, `TIA`) the plain "no current
downstream consumer, build whenever you feel like it" reading is fine
as-is — the ambiguity specifically bites on spacetime-tier nodes because
those carry an extra "why does this exist at all" question the
general-purpose ones don't.

## "Ready to build now" is a ranked queue, not a menu — the "no urgency" framing is repealed (2026-09-17)

The two "no-urgency menu" entries above (2026-09-13) and the "don't frame
by closeness to the research objective" entry (2026-09-14) together
produced a section whose own intro told the reader to "pick whatever you
feel like... with no scheduling cost to skipping this entire section
indefinitely." The user pushed back hard and explicitly, for the second
time, on this exact framing (first flagged, evidently, before this file's
history captured it — they referenced having asked before): presenting
bench work as an unranked menu means it doesn't get built. Their own
words: "If you just give me a 'menu of what you *could* spend bench time
on, not a backlog you're behind on' then I won't build the circuits...
This is why the dependency graphs exist." The instruction was concrete:
prioritize, put the most important item at the top, and if a genuine tie
can't be broken, say so explicitly and make resolving *that* the top
task — not fall back to "no priority" as a default.

**The actual problem with the old framing wasn't that ranking is
impossible — it's that the only kind of ranking argument this repo's
scope allows (see [[circuit_lifecycle_and_repo_scope]]) is "closeness to
the outside FTL-research objective," and that one really is out of
scope.** But that's not the only kind of ranking available. The
dependency graphs (`general_purpose_circuit_dependency.md`/
`spacetime_circuits_dependency.md`) encode real, checkable edges between
nodes, independent of any claim about the outside research goal's
priorities — which node gates which other node is a fact about this
repo's own graph, not a value judgment about physics. Five criteria,
applied in order, produce a total order without inventing anything:

1. A bullet unblocks another bullet already in the same list (a stated,
   not inferred, dependency — see the TIA-correction entry above on the
   inferred-dependency failure mode to avoid).
2. A bullet is a real, named prerequisite (per the dependency-graph docs)
   for the single most literature-backed next *design* target currently
   identified. As of 2026-09-17 that's tier6 `LOCKIN` —
   `spacetime_circuits_dependency.md`'s "Why these tiers" section names it
   as the strongest-justified next node, gated on `PHASED` +
   `EPFIELD`/`CHGAMP` + `OSC`. `EPFIELD`/`OSC` are already satisfied, so
   whichever of `PHASED`/`CHGAMP` isn't yet bench-confirmed ranks at the
   top. This criterion is graph-mechanical, not narrative: it names a
   node in *this repo's own* dependency graph, not the outside research
   goal — see [[circuit_lifecycle_and_repo_scope]]'s revised point 3 for
   the exact test that distinguishes the two.
3. A bullet is already mid-attempt with a documented, ready-to-apply fix
   (sunk cost) — e.g. `CHGAMP`'s destroyed piezo disc, root-caused to a
   missing-flux step that's now fixed in `breadboard.md`.
4. A bullet satisfies any other real graph edge, even to a tier that's
   itself still undesigned (e.g. `THERM --> tier2`, `ACTIVELIM
   -.required.-> psu_medhigh`) — both edges are real, neither destination
   is buildable yet, so this criterion alone can't break a tie between
   them. When it can't, fall back to the order the two dependency-graph
   docs themselves declare their subgraphs in (e.g. `safety` before
   `protection`) — a real, checkable, arbitrary-free tiebreak, not "pick
   whichever."
5. No real edge to anything currently on the graph — order by ascending
   bench effort (a single measurement before a repetitive batch check
   before building a test jig from scratch).

Applied 2026-09-17 to `TODO-arcticoder.md`'s "Ready to build now": new
order is `CHGAMP` (criteria 2+3) → `PHASED` (criterion 2) → 1N5817 diode
check (criterion 1, the list's only literal stated hard-blocker pair) →
`psu_3xaa` → `THERM` (criterion 4, `safety` subgraph declared first) →
`ACTIVELIM` (criterion 4, `protection` subgraph declared second) →
`CAPBRIDGE` (criterion 5) → the standalone-validation tail
(`psu_ultralow_v1` demo → `psu_medlow_usbc` CC-pin check → CD4066
switches 2–4 → glass-fuse jig → `psu_medlow_lm317` order decision →
`fuse_test_voltmeter` cleanup, ascending effort). The file's intro and
the section's own intro were both rewritten to state the ranking rule
inline rather than pointing here for it, since the user reads
`TODO-arcticoder.md` directly and shouldn't have to trust an unstated
rule.

**Rule for future sessions: don't reintroduce "menu, not a queue" /
"no urgency" framing into this section.** If a future pass finds the
five criteria above producing a genuine unbreakable tie (not just
"several items all seem fine, whatever"), the correct move per the
user's own instruction is to say so explicitly *and add resolving that
tie as the actual top task* — never to default back to "pick whatever
you feel like."

## Don't suggest a local hardware/craft-store run as an alternative to AliExpress, even for cheap items (2026-09-19)

Two "Next AliExpress order" bullets (soldering flux; torsion fiber +
mirror) had been written with a "cheap/small enough that a local
hardware or craft store may beat AliExpress transit time; use judgment"
qualifier. The user's own feedback, given directly: "No hardware store
talk. I don't mind waiting for aliexpress." **Rule for future
sessions: never propose or hedge toward a local-store purchase in this
file, regardless of item cost or how much transit time it would save.**
The user has an explicit preference for consolidating everything into
AliExpress orders and is fine with the multi-week transit tradeoff —
don't reintroduce the "or pick up locally" framing on some future cheap
item on the theory that it's obviously convenient; it isn't a live
option here. If an item is genuinely time-sensitive in a way transit
time can't accommodate, say so and let the user decide, but the
recommendation itself should stop at "add to the next AliExpress
order," not extend to where else it could be bought.

## Don't let a "why" ever go stale into a false "in progress" — and keep analysis out of the checklist itself (2026-09-19)

Two separate but related corrections, both from the same session.

**1. `CHGAMP` had drifted into reading as an in-progress build with a
"cheap fix ready to apply," when the real state was: attempted once
2026-09-16 without flux, failed (destroyed a piezo disc), and the user
**stopped working on it and returned every part to inventory** — not
"paused mid-fix, will finish once flux arrives" the way the file's own
"Ranked #1... already mid-attempt with a known, cheap fix" language
implied. The user caught this by asking directly: "How is
`signal_conditioning/charge_amplifier` 'in progress'?" **Lesson: a
"sunk-cost, mid-attempt" framing (criterion 3 in the ranking rule below)
is only accurate while the human is actually still attempting the build.
Once they've explicitly stopped and put parts back, the bullet moves to
"Blocked" like any other real-world-dependency item — don't keep it in
"Ready to build now" on the strength of a fix that exists on paper but
hasn't been tried again.** Resolution (confirmed via direct question):
retry later once flux is sourced — this is a *paused*, not *abandoned*,
node; `TODO-arcticoder.md`'s "Blocked" section now carries it, and
`inventory.md`/`parts_reference.md` were corrected to describe the parts
as returned rather than "for the retry" mid-build.

**2. The file itself had accumulated multi-paragraph ranking-rationale,
arrival-date narrative, and session-history asides that duplicate this
kb file, `spacetime_circuits_dependency.md`'s "Why these tiers" sections,
and `TODO-completed.md`.** The user's own words: "I appreciate the
exhaustive backstory but this is really what your knowledgebase is for.
I just need you to tell me what to do, and provide justification.
Justification doesn't mean 'we had a conversation on september 18',
justification means 'this will allow you to do X type of research
alongside Y circuit'." Separately: deferred/no-urgency shopping-list
items (SiPM+scintillator, the laser-diode-adjacent LED note, the torsion
fiber+mirror) had been interleaved into "Next AliExpress order" ahead of
genuinely actionable items — the user reads top-to-bottom and objected to
scrolling past settled non-actions to find the real one.

**Rule for future sessions:**
- Every checklist bullet gets a checklist item plus **one line of
  justification** in the "this unlocks X" / "this is needed for Y" shape
  — never a re-narration of which session decided what on which date.
  That narration belongs in `TODO-completed.md` (what got decided/done)
  or this kb file (why the file is structured the way it is), not in the
  live checklist.
- Within any section, actionable items go first; deferred/no-urgency
  items get their own clearly-labeled subsection below them (e.g. "Next
  order"'s "Deferred — not on the shopping list, no action needed") so a
  top-to-bottom read never has to step over a settled non-action to reach
  the next real one.
- Before restating the ranking method, the literature justification, or
  a past decision's reasoning inline in `TODO-arcticoder.md`, check
  whether it already lives in this file or
  `spacetime_circuits_dependency.md`/`general_purpose_circuit_dependency.md`
  — if so, a one-line pointer replaces the restatement, it doesn't sit
  alongside it.

## Flux is excluded from AliExpress for a different reason than the general "no hardware store talk" rule — don't conflate the two (2026-09-19)

The existing "no hardware store talk" convention (below) is about not
proposing a *local* purchase to save transit time — the user is fine
waiting out AliExpress shipping. **Flux is a separate, narrower
exclusion**: the user doesn't want AliExpress-sourced flux specifically,
for a toxicity/quality concern ("it's poisonous enough already just
buying from canadian sellers"), not a transit-time tradeoff. RobotShop
(an online Canadian retailer, not a local store — the SparkFun
Breadboard Power Supply Kit is going there) was proposed as an
alternative but doesn't carry flux. **Don't write flux into an
AliExpress shopping list, and don't assume RobotShop is the fallback for
it** — it's tracked in `TODO-arcticoder.md`'s "Next order" section as its
own open sourcing decision (which non-AliExpress, non-RobotShop retailer)
rather than folded into either existing order channel.

## Laser-diode/eye-safety questions get an honest capability-gap answer, not a reassurance (2026-09-19)

The user asked, about a laser-diode option for `LASERDRV`: "I value my
vision. Unless you can assure me this can be done safely?" **Rule for
future sessions on this bench: don't answer a direct safety question
about a real hazard (laser eye exposure, high voltage, etc.) with a
blanket reassurance just because the underlying circuit is
well-understood or low-power on paper.** The honest answer here was
specific: a diffuse LED carries no meaningful eye hazard, but even a
low-power laser diode module (the class actually sold under that name)
introduces a real specular-reflection hazard — worsened here since
`FORCEBAL`'s own mirror bullet is exactly the kind of reflective surface
that turns a contained beam into a stray one — and doing it safely needs
engineering controls (enclosure, beam dump, wavelength-rated goggles)
that don't exist on this bench. The resolution wasn't "yes it's safe" or
a refusal to engage — it was naming the specific gap and defaulting to
the already-adequate LED-only path (already documented as sufficient for
a first `LASERDRV` proof-of-concept) until the user decides the
controls are worth building. See `TODO-arcticoder.md`'s `LASERDRV`
bullet and `TODO-completed.md`'s 2026-09-19 entry for the resulting
decision. General pattern: this bench's own 50V/30V high-voltage
threshold (`kb/circuit_lifecycle_and_repo_scope.md`) and `HVPULSE`'s
"needs a real safety design pass from the human" gate in
`TODO-agent.md` are the same discipline applied elsewhere — a
capability/hazard gap gets named and left as the user's call, not
smoothed over.
