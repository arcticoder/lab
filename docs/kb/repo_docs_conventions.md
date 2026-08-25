# KB: cross-repo docs conventions

Audience: future LLM sessions working in this repo (or the sibling `pico/`
repo). Process/structural notes about how the docs here are organized —
not useful to the end user, who already knows this stuff first-hand.

## `spacetime_circuits_dependency.md` / `general_purpose_circuit_dependency.md` are pure mermaid, no prose (one exception — see the 2026-08-24 split entry below)

Each file's body is a single mermaid `graph TD` block — no prose legend or
explanatory section within/around the diagram itself. Every node's
documentation *is* its bracketed label text (e.g. `PASSVM["..."]`), and
edges are explained only by inline `%%` comments grouped just above blocks
of edges. Since the 2026-08-24 split (below), each file does carry one
short prose paragraph *above* the ```mermaid fence pointing to the other
file — that's the one sanctioned exception, not a reopening of "add prose
wherever helpful." Everything else about a node or edge still belongs in
the label/comment, in-diagram.

Consequence: when a node's real-world implementation changes (e.g. it
turns out to be already satisfied by an existing circuit, or a planned
approach is dropped in favor of another), the fix is to edit the label
text in place — there's no separate paragraph elsewhere to update, and
none should be added (would duplicate/drift from the label). Example:
`PASSVM` was originally labeled "Passive Analog Voltmeter with
Galvanometer"; updated 2026-08-21 to reflect that the Pico-ADC-as-voltmeter
approach (already implemented in `measurement_tools/fuse_test_voltmeter/` and used in both
`psu_ultralow_v1`/`psu_low_v2` READMEs' "Validation without a multimeter"
sections) replaces the galvanometer build entirely — no separate circuit
needs to be designed for this bootstrap node.

## README cross-linking is one-directional: `lab/` → `pico/`, never back

`lab/README.md` is the workspace-home README (the `lab.code-workspace` file
opens both `../pico` and `.`, with `lab/` as the primary folder). Per
explicit user instruction, when `lab/` docs need to reference Pico
usage/setup that's already fully documented in `pico/README.md` (e.g. the
WSL `usbipd` device-attach dance, MicroPython firmware flashing,
`mpremote` install/usage), link out to the relevant `pico/README.md`
section instead of copying the steps. Do not add a reverse link from
`pico/README.md` back to `lab/README.md` — `pico/` is meant to stand alone
as the general-purpose Pico repo and shouldn't need to know about the
lab-specific consumer of its instructions. If `pico/README.md`'s section
headings change, re-check the anchor links from `lab/README.md` (currently
`../pico/README.md#running-on-real-hardware`).

## Moving a circuit into a category folder touches every cross-reference, not just the folder

`fuse_test_voltmeter/` moved to `measurement_tools/fuse_test_voltmeter/` on
2026-08-22 (mirroring how PSU circuits already sit under
`power_supplies/`, per the "measurement/test tools are grouped under
`measurement_tools/`" line in `lab/README.md`'s intro). Files touched
beyond the `git mv` itself: `lab/README.md` (ngspice command list, the
circuits table, the Notes bullets, the repo-structure tree — five separate
spots, not one), `lab/docs/orders.md`, `lab/docs/parts_reference.md`,
`lab/docs/spacetime_circuits_dependency.md` (the `PASSVM` mermaid node's
label text — see the entry above, same file), both files in this `kb/`
directory, and `pico/docs/inventory.md` in the sibling repo. Every
relative link *inside* the moved folder's own `README.md`/`breadboard.md`
also needed a `../` added (one more directory of nesting). `lab/docs/history.md`
was deliberately left with the old `fuse_test_voltmeter/` path in its
existing entries — it's an append-only log of past sessions, not
current-state documentation, so past entries describe the repo as it was
at the time and aren't corrected retroactively (see
[ordering_ingestion_notes.md](ordering_ingestion_notes.md) for the same
treatment of "received" dates). Grep the whole path string across both
repos before considering a move like this done; it's easy to migrate the
obvious doc and miss one of the KB files or the sibling-repo inventory.

## "Test" and "demo" are distinct, deliberately-not-merged concepts in the fuse_test_voltmeter docs

As of 2026-08-22, `measurement_tools/fuse_test_voltmeter/README.md` and
`breadboard.md` distinguish three stages, in order: **self-check** (prove
the voltmeter itself works, using a plain jumper wire instead of a fuse —
no fuse, no PSU), **test** (bench-check each raw polyfuse on a minimal
jig — battery + fuse + load resistor, *not* a full PSU build — to sort
good units from faulty ones), and **demo** (build a PSU with an
already-confirmed-good fuse installed and re-probe it, which proves the
PSU's wiring is correct, not the fuse's condition — that was already
established in the test stage). Before this, the docs conflated "test"
and "demo" into one "Validation" section that assumed the fuse was
already installed in a PSU circuit, which meant there was no way to
qualify a fuse before committing it to a build. If asked to add more
polyfuse-adjacent content (e.g. Schottky diode validation reuses the same
Pico-probe idea), keep the same three-stage split rather than collapsing
back to a single "validation" step — the user has explicitly called out
the test/demo conflation once already.

## Splitting `spacetime_circuits_dependency.md` (2026-08-24): cross-file mermaid edges get collapsed to one stub node per file, not preserved 1:1

The dependency graph was split into
[general_purpose_circuit_dependency.md](../general_purpose_circuit_dependency.md)
(safety, psu_system, protection, bootstrap, tiers 1–4/6/9, concurrent
measurement tools) and the trimmed `spacetime_circuits_dependency.md`
(tiers 5/7/8 — sensor interfaces, HV pulse, calorimetric/energy work).
Mermaid diagrams can't span files — an edge needs both endpoints defined
in the same `graph` block — so every edge that used to cross what's now a
file boundary (e.g. `OVERCUR --> tier7`, `IA --> tier5`, `TIMEINT -->
tier7`) was redirected to a single stub node in the *source* file
(`SPACETIME[...]` in the general-purpose file, `GENERAL[...]` in the
spacetime file) rather than trying to preserve the original fine-grained
edge across files. This loses some precision (you can no longer tell from
the graph alone that, say, `ARCDECT` specifically feeds `tier7` and not
`tier8`) in exchange for two diagrams that are each independently valid
and self-contained. If a future session needs the original fully precise
edge list, it's in git history (the single-file version, pre-2026-08-24
split) — don't try to reconstruct exact cross-tier edges from the stub
nodes alone. Deciding which tier goes in which file: tier5 (sensor
interfaces: Hall/field-probe/LVDT/accelerometer/charge amps) and tier7/8
(HV pulse, calorimetric/energy) went to the spacetime file because they're
explicitly framed around gravitation/field sensing and Woodward/lifter
work in their node labels; tiers 1–4/6/9 stayed general-purpose because
nothing in their labels is spacetime-specific (voltmeters, ammeters,
bridges, lock-in amps, DAQ — useful for literally any lab bench). This
also means the "pure mermaid, no prose" convention (above) now has one
sanctioned exception: each split file gets a short prose paragraph at the
top pointing to the other file, since a bare stub node's label isn't
enough context on its own for someone landing on one file without having
read the other first.

## `smoke_test.py` convention (introduced 2026-08-24)

Every circuit folder has a `smoke_test.py` alongside its `.spice` netlist,
using the shared `tools/ngspice_runner.py` (confirmed against real
`ngspice -b` output format: `op` + `print` produces `name = value` lines,
lowercase node/element names regardless of netlist capitalization — e.g.
`Vbatt` in the netlist prints as `i(vbatt)`). Two check categories, always
both where applicable: **smoke** (no node exceeds a part's safe voltage,
no *physical* resistor exceeds its rated wattage) and **functional** (the
circuit does what its README's "Expected behaviour" section claims,
within a documented tolerance — usually ±10%). Important distinction that
tripped up the first pass: in the PSU circuits (`psu_ultralow_v1`,
`psu_low_v2`, `psu_medlow_usbc`, `psu_pico_rail`), `Rload` in the netlist
is a *simulated representative downstream load* — nothing in the
`breadboard.md` parts list says to physically build it — so its power
dissipation isn't a real smoke risk and doesn't need a wattage check.
`fuse_test_voltmeter`'s 10Ω test-load resistor is different: it's an
actual physical part in the bench jig (see its `breadboard.md` parts
table), so running its power dissipation through the RXEF050 tier's 3.0V
test point for real surfaced a genuine finding — ~0.82W in a resistor
whose wattage wasn't specified, which would run hot/could smoke a
standard 1/4W or 1/2W part. Fixed by specifying ≥1W in that one part's
row rather than leaving it unstated. When adding a new circuit, check
its own `breadboard.md` parts list the same way before deciding whether a
resistor power-dissipation check belongs in its `smoke_test.py`.

## `psu_pico_rail` is an interim/low-current PSU tier, not a replacement for the AA/USB-C tiers

Added 2026-08-24 alongside `power_supplies/psu_pico_rail/` (the Pico's own
onboard 3.3V rail, ~100mA conservative budget). It exists specifically
because `psu_ultralow_v1`/`psu_low_v2` need wire strippers (in transit as
of this date) to terminate the AA battery holder leads, and the Pico is
already on the bench for every measurement tool here anyway. Two new
circuits (`signal_conditioning/voltage_reference_lm358/`,
`measurement_tools/cd4066_switch_tester/`) were built against it rather
than waiting, since both draw single-digit mA — comfortably inside the
budget. Don't reflexively route every new low-current circuit through
`psu_pico_rail` once the AA/USB-C tiers become buildable again; it's the
fastest path to power right now, not the long-term intended PSU for
circuits that should be electrically independent of the PC/Pico's own USB
supply.

## Fixing bad commit authorship in `pico/` (2026-08-24)

Three tip commits on `pico`'s `main` were authored as `Your Name
<you@example.com>` (a stale/default git identity) instead of Arcticoder.
Since `origin/main` already pointed at those commits, fixing this needed
`git rebase HEAD~3 --exec 'git commit --amend --no-edit
--author="Arcticoder <...>"'` (rewrites author only, keeps messages/dates)
followed by `git push --force-with-lease origin main` (not plain
`--force` — `--force-with-lease` refuses if origin moved since last
fetched, which is the safer default for rewriting already-pushed history).
This only works cleanly when the bad commits are contiguous at the tip;
if bad-author commits are interleaved with good ones further back,
`git rebase -i` with per-commit `exec` lines (or `git filter-branch`/
`git filter-repo` for a bulk rewrite) would be needed instead.
