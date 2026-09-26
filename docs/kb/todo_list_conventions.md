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
practice — the user works the file from the top, so anything placed
that far down would never get actioned.

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
build on an unvalidated part without realizing it. The user's point:
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
this by asking what each step was needed for and finding no source
backing the implied chain — that check should happen before the bullet is
written, not after.

## `TODO-agent.md` split from `TODO-arcticoder.md`: file-creation work vs. bench/ordering work (established 2026-09-13)

Through 2026-09-13, "Ready to build now" mixed two genuinely different
kinds of task under one bullet style: physical bench work the user has to
do by hand (assemble a PSU, validate a diode batch), and file-creation
work that's entirely Claude's job (write a `.spice` netlist,
`breadboard.md`, `smoke_test.py`, `README.md` for a circuit that has
parts on hand but "no folder exists yet"). The user flagged this
explicitly: creating those files is not something they should ever be
asked to do, and dependent tasks Claude can complete should be done
before the user attempts the bench steps. They pointed at `aqei-bridge/docs/TODO.md` (a sibling repo's pure agent-task
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

Separately from the file-creation split above, the user also objected
to `TODO-arcticoder.md` reading like a laundry list even after the
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
*present* need. The user's position: an ohmmeter is already built, and any
additional ones get built when they're actually required.

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
morning, but the user objected the same day: presenting items as
"no cost to skip" reads as settled when it was really just "true given
today's undesigned state of tier4+" — and if some of those items
*aren't* actually contributing to the repo's stated goal
(`README.md`'s spacetime-research framing), the fix isn't wording, it's
designing the downstream tiers so the question has a real answer instead
of an assumed one. The user's direction: Claude does the design work directly, with the
human as the physical executor, working through the FTL-research design work already queued in
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
indefinitely." The user objected to this exact framing for the second time
(first raised before this file's history captured it): presenting bench
work as an unranked menu means it doesn't get built, and the dependency
graphs exist to supply the ranking. The instruction was concrete:
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
qualifier. The user's feedback: no hardware-store suggestions, and the wait for
AliExpress shipping is acceptable. **Rule for future
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
implied. The user caught this by asking how `signal_conditioning/charge_amplifier`
could be "in progress" at all. **Lesson: a
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
and `TODO-completed.md`.** The user's preference: the backstory belongs in the knowledge base; the
checklist should say what to do and give a justification, and a
justification means what the item unlocks (which research it enables
alongside which circuit), not which session decided it. Separately: deferred/no-urgency shopping-list
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
- Deferred/no-urgency/reference-only material (things considered and
  declined, blocked items, backlog) goes in its own section placed
  **after every actionable section in the whole file — "Ready to build
  now" included, not just the handful of bullets under "Next order"**
  (corrected 2026-09-19, second pass same day: the first pass moved
  "Deferred" below "Next order"'s own 3 bullets but left it sitting
  *above* the much longer "Ready to build now" ranked list, so a
  top-to-bottom read still hit six settled non-actions before reaching
  the real build queue — exactly the complaint this rule exists to
  prevent, just at a different scale). Current file order:
  Next order → Ready to build now → Blocked → Deferred → Backlog.
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

The user asked whether a laser-diode option for `LASERDRV` could be done
safely, given they value their eyesight. **Rule for
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

## A real criterion-1 pair (X unblocks Y) doesn't earn priority if Y itself has no real downstream value (2026-09-19)

The five-criteria ranking (above) correctly flagged "1N5817 diode check
→ `psu_3xaa`" as a real, stated dependency pair (criterion 1) and
ranked the pair ahead of `THERM`/`ACTIVELIM` (criterion 4). That was a
mistake the user caught: `psu_3xaa` has **no real downstream
consumer** — nothing on this bench needs a 4.5V rail specifically
(`ne555_astable`'s own README already ruled `psu_3xaa` out for the one
thing it was tried against: it sags to ~4.02V under load, below the
NE555's 4.5V minimum, so `psu_4xaa` covers that need instead), and
`THERM`'s own bullet plainly states it runs off `psu_pico_rail`, not
`psu_3xaa` — so the pair's adjacency to `THERM` implied a relationship
that doesn't exist. **Lesson: criterion 1 (unblocks another bullet)
only earns a *high* rank if that other bullet itself clears criterion
2/3/4 — i.e., has a real edge to something else that matters. A pair
where both ends are criterion-5 (no real edge to anything, ascending
effort) stays a criterion-5 pair and belongs in the effort-ordered tail,
not ahead of criterion-4 items just because the internal pair-ordering
logic is real.** `psu_3xaa` (and the diode check that gates it) moved to
the standalone tail; framed there as a one-time hardware confirmation of
an already-designed circuit (per
[[circuit_lifecycle_and_repo_scope]]'s "don't stage inventory for a
future build" rule), not as unlocking anything.

## Criterion 4's "real graph edge" check needs a "does the destination's own hardware actually exist to test against" sub-check (2026-09-22)

The ranking that put `ACTIVELIM` at "Ready to build now" #1 (see the
2026-09-17 application above) used a real, stated criterion-4 edge
(`ACTIVELIM -.required.-> psu_medhigh`) — but never asked whether
`ACTIVELIM`'s own bench validation (its README's § Validation, which
needs a source that can push ≥2A into a load to find the real 2A trip
point) was actually *possible* with what's on this bench. It wasn't:
checking `inventory.md`/`orders.md` directly (2026-09-22) found nothing
here can source ≥2A at any voltage — the Lenovo 65W adapter needs a PD
sink controller to give anything above its 5V default (none on hand),
and there's no power resistor rated for the fault-test dissipation
either. **Lesson, same shape as the `psu_3xaa`/`THERM` correction above
but on the *source* side instead of the consumer side: a criterion-4
edge to an undesigned destination (`psu_medhigh`, no folder) can still
be real, but "Ready to build now" additionally means the build's own
validation step must be achievable with what's actually in inventory
today — not just that some dependency-graph edge exists.** Don't infer
"the PSU is backlog, so this is designed ahead of it and that's fine"
from a circuit's own README without independently checking whether its
*validation* method (as opposed to its wiring) has a real prerequisite
too. `ACTIVELIM` moved to "Blocked" pending a PD trigger board + a
power-resistor assortment (see `TODO-arcticoder.md`'s "Next order" and
"Blocked" sections); `CAPBRIDGE` (criterion 5, no purchase needed to
validate) took its place at #1.

## Before adding a paid alternative to cart, check whether its free/on-hand twin already works (2026-09-19)

`power_supplies/psu_medlow` has two alternative implementations:
`psu_medlow_usbc` (a passive USB-C breakout, already built, zero
additional cost, smoke-tests red only because CC1/CC2 termination is
unconfirmed) and `psu_medlow_lm317` (the SparkFun Breadboard Power
Supply Kit, not yet ordered, costs money). The kit had been sitting in
"Next order" as a bare "add to cart" bullet with no acknowledgment that
its own sibling implementation might make it unnecessary. **Lesson:
when two `-.alternative.->` edges in the dependency-graph docs point at
the same node and one side is free/already on hand while the other
costs money, the free side's outstanding validation step (here: clipping
`resistance_measurement`'s leads onto the two CC pins) gets promoted
ahead of its own normal ascending-effort tail position, specifically
because it gates a live purchase decision** — a real edge into the
purchasing section, distinct from (and not to be confused with) ranking
by closeness to the outside research goal.

## A criterion-5 item ("no real edge to anything") doesn't earn a standing spot in "Ready to build now" — it belongs in "Deferred" until something upstream needs it (2026-09-22)

Through 2026-09-22, the five-criteria ranking's fallback (criterion 5:
"no real edge to anything currently on the graph — order by ascending
bench effort") had accumulated a growing "standalone validation tail" of
bullets that all satisfied criterion 5 but never actually got any
closer to being needed: a 1N5817 diode-drop check for whichever unit
might someday go into `psu_3xaa`, `psu_3xaa` itself (no rail on this
bench needs 4.5V), a `psu_ultralow_v1` demo power-on check (superseded
by `psu_low_v2`), CD4066BCN switches 2–4 per chip (nothing downstream
needs a second/third/fourth switch yet), and a glass-tube-fuse test jig
(no circuit needs one built). None of these were *wrong* to rank last —
criterion 5 correctly said "no real edge" — but keeping them as
standing checklist bullets read as manufactured busywork, and the user
said so for several of them in one pass: if nothing needs an item yet, it
shouldn't be listed, and it gets built when it's needed.

**Rule going forward: criterion 5 is not itself sufficient to keep a
bullet in "Ready to build now."** A criterion-5 item stays in that
section only if there's a concrete reason to do it *now* despite having
no current consumer (e.g. it's free/zero-effort and directly gates a
live purchase decision, the way the `psu_medlow_usbc` CC-pin check gates
the SparkFun-kit purchase — that's actually a criterion-1-adjacent edge
into the ordering section, not a bare criterion-5 item, see the
"before adding a paid alternative to cart" entry below). A pure "nothing
needs this, but it's parts-on-hand busywork" item — batch-testing spares,
demoing an already-superseded PSU tier, building a jig for a circuit
that doesn't exist yet — moves to "Deferred" with a one-line "why not
now," worded the same way this section's existing purchase-decline
bullets already are. The validation itself still happens, just at the
point something real actually needs it (the diode gets checked when
pulled for a specific build, the CD4066 switch gets tested when a
`MUX`/`DEMOD` build needs it) — not staged ahead of that need. This is
the same "don't stage inventory for a future build" principle in
[[circuit_lifecycle_and_repo_scope]], applied to *validation* bullets
specifically rather than just physical-assembly ones.

## Check `parts_reference.md`/`inventory.md` before asking the user to re-supply a spec they already gave (2026-09-22)

The `psu_medlow_usbc` CC-pin-check bullet's own history had an open
question about the USB-C breakout board's exact pad layout — but
`parts_reference.md#usb-c-16-pin-test-breakout-board` already documented
the full pad list (`CC2, D+, D-, SBU1, SBU2, CC1, VBUS, GND`) and had
already flagged the one real ambiguity (a transcribed `U+` that's almost
certainly `D+`) back on 2026-08-24. Re-asking the user for the board's
specs instead of reading that entry first was an avoidable
question. **Rule for future sessions: before asking the user to
supply or re-confirm a physical part's spec/pinout, grep
`parts_reference.md` and `inventory.md` for that part first** — if an
entry already exists, use it (and resolve any flagged ambiguity from
whatever new information prompted the question) instead of asking from
scratch.

## Don't assume a reused circuit covers a new build's power/drive stage without checking its own documented scope (2026-09-22)

`TODO-arcticoder.md`'s `RIPPLETANK` bullet claimed
`pico/leds/gpio_pwm_led/` "drives a small motor/speaker dipper
directly" — checking that claim against
`general_purpose_circuit_dependency.md` shows `gpio_pwm_led` is only
ever documented as an alternative *signal source* for tier1 `SIMPGEN`
(a PWM waveform generator), not a load driver; `SIMPGEN` itself is
still backlog/undesigned, and nothing in this repo has ever put a motor
or speaker directly on a Pico GPIO pin. A GPIO pin can source on the
order of tens of mA at 3.3V logic level — nowhere near enough to
actually turn a small motor or drive a speaker cone without a
transistor-switch (or H-bridge) stage between the PWM pin and the load,
plus a flyback diode for an inductive load. **Rule: before writing that
an existing circuit/module "drives" or "powers" a component for a new
build, check what that circuit's own README/dependency-graph entry
actually documents it doing** — a signal generator is not a load driver,
an ADC probe is not a power source, etc. — rather than assuming a
superficially-relevant existing part covers a new requirement it was
never scoped for. See `TODO-agent.md`'s new open item for the actual
driver-stage design this exposed as missing.

## When a sourcing blocker can be eliminated instead of solved, prefer that (2026-09-19)

`CHGAMP` was blocked on flux (no acceptable non-AliExpress,
non-RobotShop retailer found — see the flux-exclusion entry above). The
user's own resolution: buy a piezo disc with pre-attached leads instead
of continuing to look for a flux source, since the flux was only ever
needed to solder leads onto the bare-disc batch. **Lesson: when a
blocker is "can't source consumable X for step Y," check whether a
different purchase removes step Y entirely before continuing to search
for X** — cheaper in both money and this bench's own multi-week
transit-time cost than solving the original sourcing problem. The 19
bare discs already on hand aren't wasted; they stay as reserve stock for
any future use that doesn't need pre-attached leads.

## A purchase the user has decided is not gated by a free alternative's pending check, and the pending check gets re-justified on its own (2026-09-23)

The 2026-09-19 rule ("before adding a paid alternative to cart, check
whether its free twin already works") put the SparkFun kit in "Deferred"
behind the `psu_medlow_usbc` CC-pin check. The user decided the kit is
being bought regardless — it's the adjustable-rail PSU that follows
`psu_4xaa` — so that gate is gone. The kit moved to "Next order"
(RobotShop, a separate channel from the AliExpress cart) and the decision
stays made; don't reintroduce a "check the free twin first" hold on it.

Consequences worked through in the file:

- The CC-pin check no longer gates any purchase, so it had to justify
  itself under the "Ready to build now" rule for criterion-5 items. It
  stays because it closes the repo's one deliberately-red
  `smoke_test.py` and could give a second free 5V path, and because the
  rig for it was already set up on the bench. It got literal steps (with
  a probe-tip positive control) rather than a description, per the
  concrete-troubleshooting preference.
- A new item can have a hidden input requirement: the kit takes 9–12V DC
  and nothing on the bench makes it. The candidate source (the PD trigger
  board's 9V/12V tap off the Lenovo adapter) is already on the AliExpress
  list for `ACTIVELIM`, so the TODO ties the two together with a
  one-line check of the adapter's label rather than adding a purchase
  nobody has vetted.

## Free-shipping thresholds decide what leads "Next order" (2026-09-23)

The AliExpress cart (piezo discs, 49E Hall sensors, Mini-USB cable) sat
under the $10 free-shipping threshold. The top "Next order" bullet is now
"add these real needs and check out," not three separate "check out"
bullets — a cart that can't be checked out yet needs one action at the
top, and the items that close the gap should be needs already on the
list (the PD trigger board and power-resistor assortment for
`ACTIVELIM`), not padding. RobotShop orders are a separate retailer, so
the AliExpress threshold doesn't apply to them; keep them as their own
bullet. Prices aren't visible from the session, so the TODO says "check
price/stock" instead of claiming the threshold will be crossed.

## A path the user has dropped is dropped — remove the item and its exclusive follow-ups, don't keep a "verification" stub (2026-09-23)

The `psu_medlow_usbc` CC-pin check had survived in "Ready to build now"
after the SparkFun-kit decision on the strength of two arguments (it
closes the repo's one red `smoke_test.py`; it might give a free 5V
path). The user's response was that the USB-C path isn't being used at
all, the kit is. Neither argument outweighs that: a check whose only
purpose is to rescue an approach the user has already dismissed is
busywork by the criterion-5 rule, regardless of how cheap it is.
**Rule:** when the user states which implementation they're using,
shelve the other one — keep its folder as the record, mark its README
"Status: shelved <date>", stop listing its outstanding checks, and make
its `smoke_test.py` report its unresolvable design check as `[SKIP]`
(not `[FAIL]`) so `run_all_smoke_tests.py` stays a useful signal. Don't
re-argue the abandoned path afterwards.

Also from the same exchange, for how bench steps get written:

- **Don't write steps that presuppose bench state you haven't seen.** The
  shelved item's step 1 said to unplug a USB-C cable from the breakout;
  the photo showed the Pico's Micro-USB as the only cable connected, and
  the user confirmed it. A photo tells you what's on the board, not what
  else might be plugged in somewhere; if a step is only needed under a
  condition you can't see, phrase it as "if X is connected, ..." or leave
  it out. Likewise a step that repeats what the photo already shows
  done (the probe leads were already in the divider row) is noise.
- **A block of sub-steps sitting under another bullet reads as a
  continuation of that bullet.** The CC-pin item's steps 4–5 read as a
  response to the whole "read both CC pins" heading, with a further
  branch ("plug the adapter in") that the user took to mean plugging a
  USB-C adapter into the breakout and the Pico. A branch that changes
  what is powered needs to say exactly what gets connected to what, or
  it shouldn't be there.
- **Justifications must survive a "what's this for?" read.** The 10W
  power-resistor bullet was read as belonging to the USB-C supply because
  the nearby text talked about USB-C adapters. Each purchase bullet names
  the circuit it serves (`ACTIVELIM`'s bench check) in its own line.

## Read a spare on-hand part's label *before* the order it gates goes out (2026-09-23)

*(The fallback purchase described here was removed 2026-09-25 — see the "Mains-connected parts never go on the AliExpress cart" entry at the end of this file.)*

The SparkFun kit needs a 9–12V DC barrel-jack input. The user reported an
unidentified wall adapter (on a drive enclosure). Nothing on the bench
lists it, and adapters from drive enclosures are often a different
connector (4-pin Molex/mini-DIN for 5V+12V dual outputs) or AC. Since an
AliExpress shipment takes weeks, the TODO makes the label read a step
*before* checking out the AliExpress cart, with a fallback line ("if it
fails any criterion, add a 12V, ≥1A, 5.5×2.1mm, centre-positive adapter
to this same cart") so a failed check doesn't cost a second shipment. The
pass/fail criteria live in `orders.md` (DC, 9–12V, 5.5×2.1mm barrel,
centre-positive, ≥0.5A; reverse polarity fails safe through the kit's
1N4004). Don't assume "any wall adapter" works and don't assume it
doesn't — list the criteria and let the label decide. The adapter and
the Lenovo 65W PD adapter are now rows in `inventory.md`.

## Ranking applied to the 2026-09-23 designs: `ACCELIF` is Ready, `INDBRIDGE` is Deferred (2026-09-23)

`TODO-agent.md`'s workflow says a finished design gets a "physically
assemble" bullet stating its real dependency. Applying the ranking rules:

- `ACCELIF` (`accelerometer_interface`): criterion 1 with a destination
  that itself has value — it's the measurement side of `VIBISO`, a
  mechanical build the user asked for, and `VIBISO` was explicitly held
  until this exists. Parts on hand, four jumpers, so it's the one item in
  "Ready to build now".
- `INDBRIDGE` (`inductance_bridge`): criterion 5. Nothing on this bench
  uses an inductor, and `parts_reference.md` only says to cross-check the
  color bands "once INDBRIDGE exists". Per the 2026-09-22 rule that isn't
  enough to hold a Ready slot, so it sits in "Deferred" with a one-line
  reason. The design work still counted as done in `TODO-agent.md`.

Consequence to expect: after `ACCELIF`, "Ready to build now" has
nothing left, and "Next order" plus the two orders it names are the
user's real critical path. That is correct, not a gap to fill with
busywork — see the "Free-shipping thresholds" and "criterion-5" entries
above.

## `ACTIVELIM` moves from "Blocked" to "Deferred" — a criterion-4 edge to an undesigned destination isn't enough on its own (2026-09-24)

The 2026-09-22 entry above ("Criterion 4's 'real graph edge' check needs
a 'does the destination's own hardware actually exist to test against'
sub-check") already found `ACTIVELIM`'s own validation step needs a
≥2A source this bench doesn't have, and moved it to "Blocked" pending
the PD trigger board + power resistors. The user pushed further
2026-09-24: even granting those parts arrive, *why* validate a
protection circuit at all when `psu_medhigh`/`psu_high` — the only thing
`ACTIVELIM` protects — is still Backlog with no folder, not even
started? "Blocked — waiting on a shipment" implies the build is wanted
now and only parts are missing; that's not this situation. Nothing on
this bench currently needs current-limiting protection, because nothing
on this bench currently sources the current that would need limiting.

This is the same failure shape as the 2026-09-19 `psu_3xaa`/`THERM`
correction ("a real criterion-1 pair doesn't earn priority if the
downstream end has no real value") but on criterion 4 instead of
criterion 1: a real graph edge (`ACTIVELIM -.required.-> psu_medhigh`)
to a destination that isn't just undesigned but has **zero current
activity or near-term plan** doesn't justify spending an order slot on
the edge's source node either. **Rule going forward: before ranking or
carting parts for a criterion-4 edge to an undesigned destination, check
whether that destination has *any* concrete next step already in motion
(a part sourced, a folder started) — if it's pure Backlog with nothing
moving, the edge is real but not yet load-bearing, and the dependent
item belongs in "Deferred" with a one-line "revisit once X becomes a
real build target," not "Blocked."**

Moved: `ACTIVELIM` out of "Blocked" into "Deferred"; the PD trigger
board and power-resistor assortment stay in `orders.md`'s "Candidates
found" (not carted) with a matching parked note, rather than being
proposed again as the fix for the AliExpress cart's free-shipping gap —
solder wick (a genuine, unrelated need — see
`ordering_ingestion_notes.md`) filled that gap instead.

## A tag missing from its own TODO bullet breaks grep for anyone chasing a cross-reference (2026-09-24)

`VIBISO`'s bullet referenced "`ACCELIF` (item 1 above)" but item 1 itself
(the `accelerometer_interface` bullet) never carried the `ACCELIF` tag —
every other tag in the file (`ACTIVELIM`, `CHGAMP`, `HALLAMP`, `SCOPELA`,
`VIBISO`, `RIPPLETANK`, …) appears on its own bullet, so `ACCELIF` was
the one exception, and the user caught it by noticing that a search for
the tag turned up only the one forward-reference, not the item it
pointed at. **Rule: whenever a circuit gets a dependency-graph tag
(`spacetime_circuits_dependency.md`/`general_purpose_circuit_dependency.md`),
make sure the tag itself appears on that circuit's own `TODO-arcticoder.md`
bullet, not just in prose referring to it — a future grep for the tag
should always resolve back to the item, not just its cross-references.**
Fixed by adding `(`ACCELIF`)` to item 1's own bullet.

## Mains-connected parts never go on the AliExpress cart, and a fallback purchase can't be bundled across retailers (2026-09-25)

The 2026-09-23 entry above ("Read a spare on-hand part's label before the
order it gates goes out") had the AliExpress bullet carry a fallback: if
the drive-enclosure adapter's label failed the SparkFun-kit criteria, add
a 12V DC adapter "to this same cart." Two things were wrong with it.
First, the user doesn't buy mains-connected supplies from AliExpress at
all (trust in the part's mains isolation/safety, same class of concern as
the flux exclusion) — so an adapter fallback there was never an option.
Second, the adapter's consumer is the RobotShop kit, a different seller
and cart from AliExpress; a fallback that lives in the other retailer's
bullet doesn't tie to anything that order does. **Rules: (1) any
mains-connected part (wall adapters, mains PSUs) is never proposed for
the AliExpress cart, including as a conditional; (2) a contingency
purchase belongs in the bullet for the retailer it would actually ship
from, and a checkout step in one retailer's bullet shouldn't be gated on
an unrelated retailer's part.**

Resolution: the user read both drive-enclosure adapter labels (12V/1A and
12V/1.2A, DC, centre-positive, universal 100–240V input). Both pass the
`orders.md` checklist on voltage, polarity and current, so no adapter is
bought and the fallback line was deleted. Plug size isn't printed on
either label, so that one criterion moved to a fit test at the kit's jack
on arrival (the kit's jack is 2.1mm; a snug seat passes). Both adapters
are universal-input switch-mode units, so their output shouldn't float
far above 12V at light load; at 12V into the LM317 kit, dissipation is
the real constraint (2.1W at 5V/300mA) — noted in
`psu_medlow_lm317/README.md`. RobotShop and AliExpress bullets stay
separate in "Next order"; AliExpress leads because it is the channel with
open blocked circuits behind it (`CHGAMP`, `HALLAMP`), the RobotShop item
is unconditional and independent.

## Inventory counts come from what was received, not from a later "confirmed on hand" (2026-09-25)

`inventory.md` had the 1×AA battery holder at 6 (5 received + "1 more
confirmed on hand, origin not tracked"). The user corrected it: there
were only ever 5 — four are in `psu_4xaa` and one is unused, which was
misread as an extra unit. **When a count can't be traced to an order line
and the user's statement was about a build's contents ("there's one left
over"), record the arithmetic (total = in-use + spare) instead of adding a
line to the received total.** Ask or state the reconciliation rather than
inventing an unrecorded second source.
