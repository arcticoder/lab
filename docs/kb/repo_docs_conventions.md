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

## `measurement_tools/switch_pin_identifier/` deleted (2026-08-25) — premise was wrong, not just the first draft

The whole circuit existed to identify which pin of an unmarked "1P2T"
slide switch was active, because the inventory row hypothesized one
floating outer pin and one active pin (see the README's own "treat it as
a hypothesis to reconfirm" caveat, written before this deletion). The
actual switch received turned out to be a standard SunFounder Thales-kit
slide switch: pin 2 (middle) is the fixed/common contact, and it connects
to pin 1 or pin 3 depending on slide direction — a completely standard,
already-documented-by-the-manufacturer SPDT-style part, not something
that needs per-unit reverse-engineering. Per user instruction the folder
was deleted outright rather than kept as a generic "identify any unmarked
switch" tool. The two entries below (GND-reference bug, wiring-order fix)
describe bugs found while building this now-gone circuit; the folder,
`main.py`, `smoke_test.py`, and every README/spice/inventory.md reference
to it are gone, but the two entries are left in place because the
technical lessons — no probe pin can read LOW without an explicit GND
path in the circuit, and wire fully before powering on — generalize to
any future digital-probe circuit design here, not just this one. Don't
treat either entry as describing a file that currently exists.

## `switch_pin_identifier`'s original 3-GPIO design had no GND reference — always read all-1s on real hardware (found 2026-08-24)

The first cut of this circuit wired all 2–3 switch terminals straight to
GPIO probe pins (GP14/GP15/GP16), each with the Pico's internal pull-up,
and expected one to read LOW when the switch closed. That's physically
wrong: with nothing in the circuit tied to GND, closing the switch just
shorts two already-pulled-up-high GPIOs together — both stay HIGH. The
user built this exact circuit and confirmed it: `A:1 B:1 C:1`, unchanging
across every switch position. They also independently noticed the wiring
table never mentioned a GND pin at all, which is what tipped it off.

The `docs/history.md` session this circuit generalizes from (2026-08-22
21:41 onward) is ambiguous about whether the original ad hoc test that
"worked" (user reported `B` going `1`→`0`) had a real GND wire in place —
an earlier step in that same session did instruct "wire the switch: one
terminal to GND, the other to GP15," but the later 3-pin test's
instructions ("wire all three switch pins to GP14/15/16") don't
explicitly say to keep that GND wire, and there's no way to tell from the
transcript alone whether the user left it physically connected or not.
Don't take that transcript as confirmed evidence either way for a given
pin's role — what's certain is only the physics (no GND reference means
no pin can read LOW) and the current user's confirmed hardware result
against *this* repo's actual (GND-less) breadboard.md, both of which
independently point to the same fix. Fixed (2026-08-24) by making the GND
wire explicit and mandatory: one terminal always
wires directly to a Pico GND pin (physical pin 18, adjacent to
GP14/GP15 — physical pin 19/20), and only the *remaining* 1–2 terminals
get GPIO+pull-up probes. This also simplified the design from 3 GPIO
probes down to 2 (GP14, GP15) — a 3rd probe pin was never actually needed
once one terminal is dedicated to GND, since 2 probes plus a grounded
reference fully characterizes a 2-position (or ON-OFF-ON 3-position)
switch. `main.py`, `switch_pin_identifier.spice`, and `smoke_test.py` were
all updated to drop the `C`/`GP16` pin accordingly. If a similar
"probe every terminal, none tied to a reference" pattern shows up in a
future circuit design here, it has the same bug — internal pull-ups alone
never establish a LOW without an explicit path to GND somewhere in the
circuit.

## `Dupont M-F` jumper wording was wrong throughout the repo — should be `M-M` (fixed 2026-08-24)

Every `breadboard.md`'s parts list and wiring tables originally called for
"Dupont M-F jumper" (or "M-F, female end on breadboard") wherever a wire
ran from a Pico pin to elsewhere on the breadboard. That's backwards for
how these builds actually work: the Pico sits mounted directly on the
breadboard (straddling the center gap, per the Sunfounder Thales kit
instructions / Wokwi convention), so its pins are already seated in
breadboard holes — there's no separate female receptacle on the Pico side
to plug an M-F's male end into. The correct wire is M-M (both ends plug
into breadboard holes — one in the Pico's pin column, one wherever else
the connection needs to land), or a bent solid-core wire. Fixed across
`fuse_test_voltmeter/breadboard.md`, `cd4066_switch_tester/breadboard.md`,
and `switch_pin_identifier/breadboard.md`. `docs/history.md` still has the
old (wrong) M-F reasoning at 2026-08-15 13:03 — left alone per the
append-only-log convention (see the "moving a circuit" entry above); don't
resurrect that reasoning if referencing that history.md session.

## Wiring order: build the circuit fully before powering the Pico on

`switch_pin_identifier/breadboard.md` originally listed "plug the Pico
into the PC" as its first step, before any of the switch wiring. Per user
feedback, this is backwards in general — power should go on only after
the circuit is fully wired, not before, to avoid a transient short while a
jumper is half-seated. Fixed there (wiring is now step 1, power is step
2). Deliberately did *not* apply the same reorder to
`fuse_test_voltmeter/breadboard.md` or `psu_pico_rail/breadboard.md`:
both need the Pico powered throughout for reasons beyond just this one
circuit's wiring (serial console needed to watch readings as the jig is
adjusted; `psu_pico_rail` literally *is* the Pico's own onboard rail being
tapped, so there's nothing to wire before powering it). If asked to make
this consistent repo-wide, that's the distinction to preserve rather than
mechanically moving "plug in USB" to last everywhere.

## `docs/history.md` is not a doc readers should be pointed to — strip "see history.md" pointers on sight

As of 2026-08-24, per explicit user feedback, no README/breadboard/main.py
should tell a reader to consult `docs/history.md` for design rationale —
it's a raw chat-session log (see the append-only-log note above), not
polished documentation, and the user doesn't want it surfaced as if it
were. Removed a first round of these pointers from `README.md`,
`fuse_test_voltmeter/README.md` + `main.py`, `switch_pin_identifier/README.md`
+ `main.py`, `psu_low_v2/README.md`, `psu_ultralow_v1/README.md`,
`psu_medlow_usbc/README.md`, `docs/orders.md`, `docs/parts_reference.md`,
and `docs/manuals/schottky-rectifier-diodes-in5817-1a20v-do-41.md`. When
adding new docs, don't add a fresh "see history.md" pointer even though
older docs in git history do this — just state the relevant fact directly
instead of citing the log. The repo-structure tree listing in
`README.md` still names `history.md` as a file that exists (factual
inventory, not a "go read this" pointer) — that one line is fine to leave.

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
