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

When 6 items arrived in one report (TL082, MF52AT, IRLZ44N, piezo,
SN74HC86N, GY-521 — see
[ordering_ingestion_notes.md](ordering_ingestion_notes.md)'s matching
entry), it closed 6 of the 9 bullets then sitting in "Blocked — waiting
on a shipment" (`THERM`, `PHASED`, `ACTIVELIM`, `HVPULSE`, `EPFIELD`,
`CHGAMP`, `ACCELIF` — `ACTIVELIM`/`HVPULSE` share one MOSFET so count as
one part-driven unblock). Only `INDBRIDGE`, `SCOPELA`, and `HALLAMP`
(partial) remained blocked, on the 3 items that didn't arrive. Each
newly-unblocked bullet moved into "Ready to build now" following the
section's existing convention (name the part, its quantity, arrival
date, and "No folder exists yet") rather than being deleted — none of
these six have a folder/netlist/breadboard guide, so they're genuinely
new build targets, not completions. Also had to sweep the "Backlog —
undesigned, long-tail" section for parenthetical cross-references
pointing at "Blocked" for `THERM`/`PHASED`/tier5 nodes and repoint them
at "Ready to build now" — those asides go stale silently since nothing
enforces they track the referenced section's actual current contents.
General lesson: when an arrival report resolves more than one item,
re-check the *entire* "Blocked" section against the arrival list rather
than hand-matching just the parts you already expect to be there — it's
easy to miss one (here, `ACCELIF`/GY-521 was the one most likely to be
overlooked, since GY-521 shipped in a different batch/order date than the
other five).

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
