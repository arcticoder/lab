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

## "Ready to build now" is a no-urgency menu, not a mandatory queue, when nothing downstream needs its contents yet (established 2026-09-13)

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

## "Ready to build now" being a no-urgency menu is a snapshot, not a permanent verdict — re-check it whenever the downstream tiers actually get designed (established 2026-09-13, same day as the entry above)

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

## Don't frame "ready to build now" items by closeness to the spacetime-research objective, and don't assume a shared part needs duplicating (2026-09-14)

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
