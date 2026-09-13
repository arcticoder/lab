# KB: AliExpress order-ingestion process notes

Audience: future LLM sessions working in this repo. Not linked from
README/docs — process/meta observations from ingesting AliExpress order
data into `docs/orders.md`, `docs/parts_reference.md`, `docs/manuals/`, and
`docs/inventory.md`. Not useful to the end user, who already knows this
stuff first-hand.

## gitignore behavior for manuals

`docs/manuals/*.pdf` and the bare pattern `*Zone.Identifier` are both
already in `.gitignore` (added in commit `daae9c3`). `*Zone.Identifier`
with no leading slash or path segment matches at any depth, so it covers
sidecar files under `docs/manuals/` too — no per-directory entry needed.
`Zone.Identifier` files are WSL/Windows browser-download zone-metadata
sidecars (`Foo.pdf:Zone.Identifier`); safe to `rm` on sight, never worth
tracking or fighting with.

Converted `.md` manuals in `docs/manuals/` are **not** ignored (only
`*.pdf` is) — that's deliberate, so the markitdown output is the durable,
git-tracked artifact and the source PDF stays a local/gitignored blob.

## markitdown gotcha: silent empty output on scanned PDFs

`markitdown <file>.pdf -o <file>.md` does not error on an image-only
(scanned) PDF with no text layer — it just writes an empty or near-empty
file. Confirmed on `schottky-rectifier-diodes-in5817-1a20v-do-41.pdf`
(15 pages, all scanned images, 5.1MB): both `markitdown` and
`pdftotext -layout` returned zero characters. Always check output file
size after conversion; don't assume success from exit code alone. When
extraction fails, fall back to whatever text description is already
available (e.g. the buyer-facing listing text) rather than leaving the
`.md` file empty and unexplained — note explicitly in the file that OCR
was not run and why.

## AliExpress listings bundle multiple part-number variants under one title

Common pattern: a listing title strings together many compatible/similar
part numbers (e.g. "RXEF003 RXEF010 RXEF025 ... RXEF500" or "1N5408 IN5408
... 5817 5819 5824") and the actual SKU is only fixed by the buyer's
selected variant/SKU string at order time (e.g. "RXEF050 0.5A 20pcs" or
"IN5817 1A20V DO-41"). When logging an order, always record the *selected
variant string*, not just the listing title — the title alone is
ambiguous and will misidentify the part in a future session.

## `inventory.md` lives in this repo now, not `pico/` (moved 2026-09-07)

Originally `pico/docs/inventory.md`, in the sibling `pico/` repo — a
separate git repo, so every edit needed its own add/commit there, distinct
from this repo's own commits. Moved to `docs/inventory.md` (this repo) per
explicit user request: most of the day-to-day ordering/inventory work
happens from `lab/`, and switching repos just to update quantities was
friction with no upside. `pico/docs/inventory.md` is now a one-line
pointer back to this file, kept so `pico/`'s own generic circuit BOMs
(`buttons/gpio_interrupt_button/bom.md` etc.) still resolve a path without
requiring `lab/` to be cloned alongside `pico/` — but note that pointer
file is *not* kept in sync automatically; if `inventory.md`'s path or
this repo's relationship to `pico/` changes again, check that stub too.
Still the shared master parts inventory across both projects, even though
most of its existing content (SunFounder Thales kit) predates and is
unrelated to the spacetime lab build — that hasn't changed, only which
repo owns the file.

## Photo-transcribed pinouts can contain OCR/transcription slips

The USB-C 16-pin test board's pad list, as transcribed from the AliExpress
product photo in the order notes, included a pad labeled `U+`. No standard
USB-C pinout has that label — it's almost certainly a mis-transcription of
`D+` (the board also has a `D-` pad, and `VBUS`/`GND`/`CC1`/`CC2`/`SBU1`/
`SBU2` round out a completely standard USB-C breakout pin set). Flagged in
`docs/parts_reference.md` with a caveat to verify against the physical
silkscreen on arrival. General lesson: treat photo-transcribed pin labels
as provisional until the physical part confirms them, especially single
characters that could be OCR confusions (D/U, O/0, B/8, etc.).

## Moving an item from "on order" to "received" touches 3 files, not 1

When a physical part arrives, it needs updating in all of: `lab/docs/inventory.md`
(delete from the "On Order" table, add to/create the appropriate received-parts
table), `lab/docs/orders.md` (delete the row from "On order", add a "Received"
subsection entry with the received date), and `lab/docs/parts_reference.md`
(the pinout/spec entry usually says "ordered" somewhere and should be updated
to say "received <date>" for accuracy — it's easy to migrate the other two
files and forget this one since it doesn't have an explicit on-order/received
table structure). Did this for the RXEF005/RXEF050/1N5817/AA-holder batch on
2026-08-21 — used as the template for future arrivals.

## AliExpress listing titles can misuse standard part-family terminology, not just bundle SKUs

The 3296W trimmer potentiometer batch (ordered 2026-08-25) is titled
"Multi-turn Trimming" but the 3296 package is the industry-standard
**single-turn** cermet trimmer designation (a genuinely multi-turn part
in a similar footprint is usually a different suffix, e.g. 3296X). This
is a different failure mode than the earlier "bundled part-number
variants" and "OCR/transcription slip" entries above — here the listing
text itself asserts an electrical property (turn count) that contradicts
the well-known meaning of the part's own package code. Don't take a
listing's adjectives (multi-turn, precision, etc.) at face value even
when the part number looks specific and legitimate; cross-check against
the package/family's established meaning and flag the discrepancy in
`parts_reference.md` rather than silently repeating the listing's claim.

## Two unrelated items can arrive in the same user message with the same URL

When ingesting the 2026-08-25 batch, the "18-in-1 wire stripper pliers"
item and the "2A glass tube fuses" item were given the identical
AliExpress URL — clearly a paste mistake on the user's part (a pliers
listing and a fuse listing are not the same product). Don't silently
"fix" this by guessing a plausible URL for the mismatched item; just log
the order from its title/spec text (which was distinct and complete for
both items) and flag the URL collision explicitly in `orders.md` so a
future session doesn't trust that link for the pliers.

## "Received" ≠ "validated" for bulk/consumable parts

For parts bought in bulk from AliExpress (polyfuses, diodes — anything where
a DOA rate across the batch is plausible), don't mark a part as simply
"received" without also tracking whether it's been individually tested yet.
The convention used here: the inventory.md/orders.md/parts_reference.md entry
gets an explicit "untested" or "not yet validated per-unit" note plus a
pointer to whatever tool does the validation (e.g.
`lab/measurement_tools/fuse_test_voltmeter/` for polyfuses and the Schottky diode), and that
caveat should be removed only once the user confirms the batch (or specific
units) have actually been tested — don't assume "received" implies "known
good" for these part classes. Single-item non-consumable parts (e.g. the AA
battery holder) don't need this caveat.

## A listing's own spec block can contradict its own description text — don't silently pick one (found 2026-08-30, ceramic capacitor assortment)

The "300pcs 10Value 50V ... Multilayer Ceramic Capacitor Assortment"
listing's structured "Specifications" field states operating temperature
−40 to 80°C, while its free-text product description states "Operating
temperature range: -25° C-185° C" for the same part. This is a different
failure mode than the previously-logged "bundled part numbers"/"OCR
slip"/"listing adjective contradicts package convention" cases — here
two *first-party* fields within the same listing disagree with each
other, so there's no obvious "trust the more authoritative source"
default (both are equally "the listing's own words"). Logged both
figures side by side in `parts_reference.md` and `orders.md` with an
explicit "unresolved" flag rather than guessing which one is real;
resolve only once a datasheet or the physical part's markings settle it.
General lesson: when transcribing a listing, diff the structured spec
table against the prose description for the same attribute before
writing either into the docs as fact — they're generated/written
independently on AliExpress and silently drift apart often enough to be
a recurring category, not a one-off.

## A user-supplied order URL can be a literal unfilled placeholder, not just a copy/paste mismatch (found 2026-08-30, electrolytic capacitor kit)

The earlier "two unrelated items, same URL" entry above covers a *wrong*
URL pasted for an item. This is a step further: for the "120pcs
Electrolytic Capacitor ... Kit" item, the message contained
`https://www.aliexpress.com/item/???.html` — the item-ID segment itself
was left as a literal `???`, meaning no real URL was ever supplied for
this item at all (not even a mismatched one). Handled the same way the
prior entry recommends: don't invent or guess a plausible-looking item
ID to fill the gap (this would produce a URL that looks legitimate but
points at an unrelated or nonexistent listing), and don't silently drop
the fact that it's missing either. Recorded the omission explicitly in
both `orders.md` and `parts_reference.md` so a future session doesn't
mistake the absence of a URL for an oversight in transcription and try
to "fix" it by guessing one.

## The user's order date wasn't stated in the order text itself, and a first guess at it can be wrong even when framed as a low-effort default (2026-08-30)

When ingesting the inductor/ceramic-cap/electrolytic-cap batch, the
user's message gave full listing text for all three items but no order
date. Asking "today's date, or a different date?" got "Different date"
selected back with no date actually supplied in that same answer — the
option's label alone came back, not free text — so a second, more
specific question ("what is the actual date") was needed to get
2026-08-30 (matching the same-day resistor-kit/photodiode order already
in `orders.md`). Lesson: when a multiple-choice clarifying question
includes an option like "different value" that implies the user will
type something, don't assume the returned answer contains that
free-text value — check whether the answer is just the option's own
label before proceeding, and re-ask more narrowly (e.g. list plausible
concrete dates as the options) if so.

## An "assortment" listing can mean the buyer picked specific values, not that a random assortment shipped (found 2026-09-03, metal film resistor kit)

The "20pcs 1W Metal film resistor" listing had previously been logged
(2026-08-30) as "20 ordered, assorted values… notably including 0.1Ω" —
phrasing that implied a single 20-piece grab-bag across the listing's
value range. What actually happened: the listing lets the buyer select
specific values, and the user made **two separate 20-unit selections**
from it (0.1Ω ×20, 1Ω ×20 — 40 resistors total, no other values). This
is a distinct failure mode from the other listing-ambiguity entries in
this file (bundled part-number variants, OCR slips, contradicting spec
fields, placeholder URLs) — here the ingesting session correctly copied
the listing's value-range text but wrongly assumed "assortment" meant
"random assortment shipped" rather than "buyer selects from this menu."
Corrected in `orders.md`, `parts_reference.md`, and
`inventory.md` once the user clarified. General lesson: when a
listing's title/description offers a value range with no explicit random
assortment language ("random", "mixed", a fixed per-value count table),
don't assume the seller picks values — ask whether the buyer selected
specific values instead, especially before writing a specific per-value
quantity or "not previously stocked" claim into the docs.

## Items can sit "received" in prose while still filed under an "on order" heading

Found 2026-09-03: the 3296W trimpot and TL431A entries in `orders.md`
had gained a "Received: 2026-09-01" note (added in commit `de0a9d7`) but
were never physically moved out from under the `## On order (placed, not
yet received)` heading — so the file's own section header contradicted
its content for over two days across several more commits. Nothing
downstream broke because `inventory.md` (the actual
received-parts source of truth) had these correct the whole time, but a
future session skimming `orders.md` by heading alone would misreport
their status. Moved them into `## Received` while fixing an unrelated
batch of received items in the same file (2026-09-03) — worth a quick
`grep -n "^## \|^### "` sanity pass over `orders.md` any time an item's
received-status is being edited in place, not just appended to.

## A listing can be missing its selected-variant line entirely, not just be ambiguous about it (found 2026-09-03, KY-003 Hall sensor module)

All the earlier "bundled part-number variants" entries in this file cover
a listing whose title strings together options, resolved by a `>
selected variant` line the user includes. In the 2026-09-03 batch (TL082,
MF52AT thermistor, KY-003 Hall module, IRLZ44N, piezo, SN74HC86N), five
of six items had that line; the KY-003 listing simply didn't — no
quantity/variant text at all, not even an ambiguous one. Resolved by
asking the user directly (`AskUserQuestion`) rather than guessing a
plausible pack size; got "1 unit." General lesson: don't assume every
item in a batch message follows the same transcription pattern as its
neighbors — check each one individually for a selection line before
assuming a value can be read off the listing title/spec.

## Order date can require the same "returned answer is just the option's own label" re-ask as before (2026-09-03 batch, again)

Same failure mode as the 2026-08-30 entry above, recurring: asking "today,
or a different date?" as a multiple-choice question got "A different
date" back with no date value attached — the option's label alone, not
free text. A second, narrower question listing concrete candidate dates
(2026-09-02/03/04) got the actual answer (2026-09-03). This is evidently
a recurring interaction-pattern gotcha with this style of clarifying
question, not a one-off — default to listing concrete date options up
front rather than an "or a different date" escape hatch, when the
question is specifically about a date.

## A gap-analysis list from `docs/history.md` can get fully closed in one batch — cross-reference gap items by number when ingesting an order that fills them

The 2026-09-03 batch (TL082, MF52AT thermistor, KY-003 Hall module,
IRLZ44N, piezo, SN74HC86N) closes 6 of the 7 gap items from the
~2026-09-01 gap-analysis table in `docs/history.md` (lines ~3684–3697) —
only item 2 (ADXL335 accelerometer) remains, and the user is substituting
a GY-521 (MPU6050 breakout) for it instead of the originally-suggested
part. When an order this clearly maps to a known gap list, cite the gap
item number in `orders.md`/`parts_reference.md` rather than just
describing the tier node — makes it easy for a future session to check
whether the whole known-gaps list has been closed without re-deriving the
mapping from scratch. One substitution is not a straight swap: the
ordered KY-003/A3144 Hall module is a **digital switch-output** sensor,
while the gap explicitly asked for **linear analog output** — it doesn't
actually unlock the tier5 `HALLAMP` op-amp-amplifier circuit as
originally scoped, just a simpler presence/switch use case. Don't assume
an order that name-matches a gap's suggested part number, or even its
general sensor family, actually satisfies that gap's specific circuit
requirement — check the electrical characteristics against what the tier
node needs.

## "CY7C68013A board" is not a component you'd add to the SCOPELA logic analyzer — it IS the SCOPELA logic analyzer (2026-09-04)

The cheap "8ch 24MHz USB logic analyzer" clones (~$5-8) referenced
throughout `docs/history.md` and `general_purpose_circuit_dependency.md`
(the `SCOPELA` tier) are, near-universally, boards built around the
Cypress **CY7C68013A** (EZ-USB FX2LP) microcontroller — that chip's USB
interface plus the `fx2lafw` open-source firmware (bundled with
`sigrok`/`PulseView`, package `sigrok-firmware-fx2lafw` on
Debian/Ubuntu) is exactly what makes these boards work as
hardware-timed logic analyzers, and is why they're supported
out-of-the-box by PulseView with zero vendor software. So a listing
titled "CY7C68013A 24MHz 8-channel logic analyzer" or similar *is* the
`SCOPELA` purchase, not a sub-part needed to build one. Most listings
ship with an 8-wire Dupont test-clip cable included; if not, the
existing M-M/M-F Dupont jumper stock in `inventory.md`
covers it. Check whether the board is USB-A dongle-style (plugs
straight into a port, no cable needed) or has its own Micro-USB port
(would need a second Micro-USB cable, since the one already in
inventory is earmarked for the Pico) before assuming no cable is
needed.

## `orders.md` gained a fourth lifecycle stage, "In cart (not yet checked out)" — distinct from "On order" (found 2026-09-09)

Until now `orders.md` only tracked three states: Received, Cancelled, and
On order (placed, not yet received) — nothing between "not yet in any
cart" and "actually placed." The user reported items sitting in an
AliExpress cart (CY7C68013A logic analyzer, GY-521 accelerometer) that
hadn't been checked out yet, plus a concrete blocker (checkout is $0.31
short of the $10 free-shipping minimum) — genuinely different from "On
order," which by this file's own convention means the order has already
been placed with a real order date. Added a new `## In cart (not yet
checked out)` section, positioned first (before "Received"), matching
cart's position as the earliest lifecycle stage. Entries in this section
use "Added to cart: <date>" instead of "Ordered: <date>," and move to "On
order" once checkout actually happens (same pattern as the existing
"On order" → "Received" migration described in the entry below — update
`orders.md`, `TODO-arcticoder.md`, and eventually `parts_reference.md`/
`inventory.md` together at each stage transition, not just at checkout).
Don't add a `parts_reference.md` entry for a cart-stage item — that file's
convention (per the entry below) is populated once a part is actually
ordered/received, and a cart isn't a commitment (items can silently drop
out of a cart, quantities can change at checkout).

## Physical part markings can be used to positively confirm a received batch against its ordered value list — worked example: ceramic capacitor EIA codes (2026-09-10)

The 300pcs multilayer ceramic capacitor assortment (10 values, ordered
2026-08-30) arrived with each cap printed with a standard 3-digit EIA
code (two significant digits + a ×10^n multiplier in picofarads, or a
bare 2-digit value under 100pF with no multiplier). The user reported 10
distinct printed codes — `200`, `560`, `300`, `104`, `100`, `102`, `101`,
`680`, `47`, `103` — with "about 30 of them" each. Decoding each against
the EIA convention and cross-checking against the 10 originally-ordered
values (10pF, 20pF, 30pF, 47pF, 56pF, 68pF, 100pF, 1nF, 10nF, 100nF) gave
a clean 1:1 match with no leftover/unexplained codes and no ordered value
missing a code — see the decode table in
[parts_reference.md](parts_reference.md#multilayer-ceramic-capacitor-assortment-50v).
This is a stronger confirmation than the earlier "received, untested"
entries in this file get (which just log a count) — it independently
verifies the *value* of what shipped, not just the quantity, from data
the user could read directly off the parts without a meter. General
lesson: when a received batch's individual units carry a standard,
decodable marking (EIA capacitor codes, resistor color bands, symbol/date
codes on ICs), ask for or transcribe those markings and cross-check them
against the ordered value list rather than just trusting the order
quantity matched — it's a free correctness check that a bulk assortment
listing (prone to the value-substitution/mislabeling issues logged
elsewhere in this file) actually shipped what it claimed.

## The "In cart" → "On order" transition observed end-to-end: a third item added specifically to clear the free-shipping minimum (2026-09-10)

The 2026-09-09 entry below introduced `orders.md`'s "In cart (not yet
checked out)" stage, noting the cart (CY7C68013A logic analyzer +
GY-521 accelerometer) was $0.31 short of the $10 free-shipping minimum
and suggesting a 49E Hall sensor or a replacement color-ring inductor
listing as candidates to close the gap. What actually happened: the user
found a replacement inductor listing (same as the cancelled 2026-08-30
order, still cheapest available) and added *that* to the same cart,
clearing the threshold, then checked out all three together on
2026-09-10. Confirms the predicted mechanism worked as designed — when a
future session sees a cart-stage entry with a documented shipping-minimum
shortfall, expect the eventual checkout batch to include whatever small
item closed the gap, and treat all items checked out in the same
message/session as one order batch (same order date, moved into
`orders.md`'s "On order" section together) unless the user says
otherwise. Also resolved the GY-521 entry's outstanding "quantity not yet
confirmed" caveat from the cart stage: the checkout variant string was
"1pcs Compatible," settling it at 1 unit.

## A batch arrival report can name only some items from an in-transit set — check each order line individually, don't assume "arrived today" covers everything still on order (2026-09-12)

The user reported 6 items arrived on the same day (2026-09-12): TL082,
MF52AT thermistor, IRLZ44N MOSFET, 12mm piezo disc, SN74HC86N XOR gate
(all from the 2026-09-03 batch of 6), plus GY-521 (from the 2026-09-10
batch of 3). **Two items from those same two batches were *not* in the
arrival report**: KY-003 Hall module (2026-09-03 batch — odd that it
shipped separately from its 5 batch-mates, but nothing in the message
explained why) and the CY7C68013A logic analyzer board + color-ring
inductor reorder (2026-09-10 batch). Moved only the 6 named items through
the on-order → received pipeline (`orders.md`, `inventory.md`,
`parts_reference.md`, `TODO-arcticoder.md`'s Blocked/Ready-to-build
sections) and left the other 3 exactly where they were. General lesson:
match the arrival report against the full current "On order" list item
by item rather than assuming a same-batch/same-order-date grouping arrives
atomically — AliExpress sellers routinely split one order into multiple
shipments/tracking numbers, so partial-batch arrival is the expected case,
not an anomaly to double-check before acting on.

## Moving 6 items to "received" at once surfaced an unrelated copy-paste bug in `parts_reference.md` — worth a skim of neighboring content when editing a section, not just the lines being changed

While updating the SN74HC86N XOR gate entry in `parts_reference.md` for
its 2026-09-12 arrival, its trailing paragraph ("Long lead = positive...
solder at 350–380°C... prolonged heat can damage the electrolyte...
candidate use: bulk output filtering for `psu_medlow_lm317`... higher-
capacitance tier3 `CAPBRIDGE`") turned out to describe the **aluminum
electrolytic capacitor kit**, not a XOR gate IC — a digital logic chip has
no lead polarity or electrolyte to damage. The electrolytic capacitor
kit's own section, just above it in the same file, was missing exactly
this content (it only had a bare "Polarized — orientation matters."
sentence). Moved the paragraph to the correct section and left the XOR
gate entry ending at its citation link. Root cause unclear (likely a
stray paste during a past edit of adjacent sections) but nothing else in
the file appeared to reference the misplaced text, so this was a pure
copy-paste orphan rather than an intentional cross-reference. General
lesson: when editing one entry in `parts_reference.md`, a quick skim of
the surrounding 1-2 entries for content that doesn't match their own
heading is worth doing — this file has no automated consistency check,
and the failure mode (real solder-handling advice attached to the wrong
part) could mislead a bench session if never caught.

## `psu_medlow_lm317/README.md` claims "on order" for the SFE Breadboard Power Supply Kit, but no matching entry exists in `orders.md` or either inventory

Found 2026-09-03, not resolved. The kit is a RobotShop item (not
AliExpress, unlike everything actually tracked in `orders.md`), which may
be why it was never logged there — but that means its claimed "on order"
status is unverifiable from the docs alone. Flagged to the user rather
than silently trusting or silently correcting the README's claim; if a
future session needs to know whether `psu_medlow_lm317` is actually
buildable soon, ask the user rather than trusting that status line.
