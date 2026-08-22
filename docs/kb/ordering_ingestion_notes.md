# KB: AliExpress order-ingestion process notes

Audience: future LLM sessions working in this repo. Not linked from
README/docs — process/meta observations from ingesting AliExpress order
data into `docs/orders.md`, `docs/parts_reference.md`, `docs/manuals/`, and
the sibling `pico/docs/inventory.md`. Not useful to the end user, who
already knows this stuff first-hand.

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

## pico/docs/inventory.md is a separate git repo

`../pico` is a sibling repo, not a subdirectory of this one — changes to
`pico/docs/inventory.md` need their own git add/commit in that repo, not
this one. It's treated as the shared master parts inventory across both
projects per explicit user instruction, even though most of its existing
content (SunFounder Thales kit) predates and is unrelated to the spacetime
lab build.

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

When a physical part arrives, it needs updating in all of: `pico/docs/inventory.md`
(delete from the "On Order" table, add to/create the appropriate received-parts
table), `lab/docs/orders.md` (delete the row from "On order", add a "Received"
subsection entry with the received date), and `lab/docs/parts_reference.md`
(the pinout/spec entry usually says "ordered" somewhere and should be updated
to say "received <date>" for accuracy — it's easy to migrate the other two
files and forget this one since it doesn't have an explicit on-order/received
table structure). Did this for the RXEF005/RXEF050/1N5817/AA-holder batch on
2026-08-21 — used as the template for future arrivals.

## "Received" ≠ "validated" for bulk/consumable parts

For parts bought in bulk from AliExpress (polyfuses, diodes — anything where
a DOA rate across the batch is plausible), don't mark a part as simply
"received" without also tracking whether it's been individually tested yet.
The convention used here: the inventory.md/orders.md/parts_reference.md entry
gets an explicit "untested" or "not yet validated per-unit" note plus a
pointer to whatever tool does the validation (e.g.
`lab/fuse_test_voltmeter/` for polyfuses and the Schottky diode), and that
caveat should be removed only once the user confirms the batch (or specific
units) have actually been tested — don't assume "received" implies "known
good" for these part classes. Single-item non-consumable parts (e.g. the AA
battery holder) don't need this caveat.
