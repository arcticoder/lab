# KB: cross-repo docs conventions

Audience: future LLM sessions working in this repo (or the sibling `pico/`
repo). Process/structural notes about how the docs here are organized —
not useful to the end user, who already knows this stuff first-hand.

## Don't name a specific fringe/exotic-physics theory in current-state docs (established 2026-09-04)

`README.md` and `spacetime_circuits_dependency.md` used to name specific
candidate theories (electrogravitics, the Biefeld-Brown effect,
Woodward-effect propulsion) as the driving research goal. The user
corrected this explicitly: the actual goal is "a road to faster than
light travel," full stop — the user doesn't care which specific theory
gets tested, and doesn't want any of those specific terms appearing
anywhere in either repo's current-state docs (README, dependency graphs,
this kb file's own prose). Rewrote both to describe the goal generically
("spacetime research… experiments aimed at faster-than-light travel,
with no fixed commitment to any one specific theory or approach") instead
of naming a theory. The one exception is `docs/history.md` in both repos
— append-only per the entry below, so old references to those terms stay
there untouched as a historical record; this policy applies only to docs
that describe *current* framing. When adding new spacetime-tier circuits
or docs, describe them by circuit function (sensor interface, HV pulse,
calorimetric measurement) rather than by which specific theory they'd
support.

**Lifted 2026-09-21.** The user explicitly reversed this: naming a
specific theory, program, or institute in current-state docs (README,
dependency graphs, kb prose) is fine now — the restriction above was, in
their explanation, a holdover from earlier work in that area.
Nothing needs retroactively renaming; existing generic phrasing
("spacetime research," functional node labels) is still accurate and
doesn't need to change just because naming is now permitted. This entry
is kept for the historical reasoning, not as a live rule — don't strip a
name out of a new doc or kb entry on the strength of the paragraph above
anymore.

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

## Build/bench-test status doesn't belong in a dependency-graph node's displayed label — use a `%%` comment above the node instead (established 2026-09-09)

`general_purpose_circuit_dependency.md` used to embed dated build status
directly in node/subgraph label text, e.g. `PSUPICO["...
(power_supplies/psu_pico_rail/) — built & bench-tested 2026-08"]` or
`REF["... — built & bench-tested 2026-08-27"]`. The user flagged this as
clutter: that status is already tracked authoritatively in `README.md`'s
"Circuits — built & bench-tested" table and `docs/history.md`, so
repeating it (with its own copy of the date, subject to drifting out of
sync) inside the dependency graph's node labels was pure duplication with
no display benefit — the diagram exists to show dependency structure, not
status.

Fixed by stripping the status/date text out of every label and moving it
to a `%%` comment on its own line immediately above the node/subgraph
definition it describes (mermaid comments are not rendered, so the detail
stays in the source file for a reader of the raw `.md`/kb context without
cluttering the diagram itself). Example:

```
%% status: built & bench-tested 2026-08-27
REF["Precision Reference Voltage Generator (3.3V or 5V input) — see signal_conditioning/voltage_reference_lm358/"]
```

This is a narrow, additive exception to the "pure mermaid, no prose"
convention below (which is about full paragraphs, not single-line `%%`
status annotations) — don't read it as license to add prose elsewhere in
these files. Rule for future edits to either dependency-graph file: a
node's label describes *what the circuit is and where it lives*
(component values, folder path); *whether/when it was built* stays out of
the label and, if worth noting at all in the graph file, goes in a `%%`
comment above it — the durable source of truth for that status remains
`README.md`'s bench-tested table and `docs/history.md`, not this file.

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
explicitly framed around gravitation/field sensing and high-voltage
actuation work in their node labels; tiers 1–4/6/9 stayed general-purpose because
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

## `smoke_test.py` must also check that the netlist models the *whole* circuit, not just that its own numbers are internally consistent (found 2026-09-05, `psu_medlow_usbc`)

`psu_medlow_usbc`'s smoke/functional checks all passed green while the
physical build was incomplete: the "TYPE-C Female Test Board" breakout
(`pico/docs/inventory.md`) is passive (traces only, no PD controller IC),
and the netlist's `Vusb 1 0 DC 5.0` simply *assumes* VBUS is already
present rather than modeling USB-C CC1/CC2 sink termination or PD
negotiation — so the checks were only ever verifying "if VBUS shows up,
the fuse+bypass math is right," not "this circuit powers on from a real
USB-C source." A PD-only charger with no legacy 5V fallback may output
nothing at all without CC1/CC2 termination (5.1kΩ pull-downs), and
whether this specific breakout board has those wired was never confirmed
(`docs/parts_reference.md` § USB-C 16-pin test breakout board already
hedged this — "verify values with a meter" — but nothing downstream
propagated that hedge into a check that would actually fail).

Fix applied: added a static (non-simulated) `PD_SINK_TERMINATION_CONFIRMED
= False` check to `smoke_test.py` that fails until someone physically
confirms the termination — plus matching "Status: incomplete / unverified"
callouts in `README.md` and `breadboard.md`, and a `NOT MODELED:` comment
in the `.spice` file. Generalizes: when a circuit's physical BOM has a
component whose *presence* (not just its value) is unconfirmed and load-
bearing for the circuit to function at all — a breakout board that may or
may not carry termination/logic it's assumed to have, e.g. — encode that
as a static assertion in `smoke_test.py` that fails until verified,
rather than letting the simulated checks report green on an assumption
the netlist can't actually test. Don't wait for someone to notice the
prose caveat; make the test suite red.

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

## `mpremote run` cannot forward host keystrokes to a running script — never write `input()` into a script meant to be launched that way (found 2026-08-26)

Confirmed empirically (pexpect against a real Pico on `/dev/ttyACM0`,
`mpremote/1.27.0`) and traced in `mpremote`'s own source
(`transport_serial.py`'s `follow()` and `commands.py`'s `_do_execbuffer`):
`mpremote run script.py` executes the script over the raw-REPL protocol
and streams device *output* back by reading serial until it sees the
`\x04` (EOF) sentinel — it never reads the host's stdin or writes
anything back to the device while `follow()` is running. So a script
launched this way that calls `input()` blocks forever on the device side;
the user's local Enter keypress goes nowhere and the only way out is
Ctrl-C on the host, which kills the local `mpremote` process but leaves
the device still stuck mid-`input()` (confirmed — the device needs an
explicit `mpremote soft-reset` afterward, since it doesn't recover on its
own).

This bit `signal_conditioning/voltage_reference_lm358/main.py`, which
used two `input("...then press Enter...")` calls despite its own
docstring saying to run it with `mpremote run main.py` — the exact
"press Enter and nothing happens" symptom the user hit. Fixed by
replacing both `input()` calls with a fixed `time.sleep`-based countdown
(`COUNTDOWN_S = 10`) instead — confirmed working end-to-end (`mpremote
run` exits 0) since the script never touches stdin at all anymore.

Workarounds that looked plausible but were tested and ruled out, in case
this comes up again:
- **`mpremote repl` + Ctrl-K file injection** (`--inject-file` +
  in-REPL Ctrl-K): the injection helper calls `exit_raw_repl()`
  immediately after starting the script, and the raw-REPL-exit byte
  sequence it sends gets consumed by the script's still-pending
  `input()` as a stray empty line — so the *first* `input()` resolves
  instantly with `""` before the user can type anything. Looks like it
  works, silently doesn't.
- **MicroPython REPL paste mode** (Ctrl-E, paste source, Ctrl-D) inside
  `mpremote repl`: in principle this stays inside the same bidirectional
  `do_repl_main_loop` the whole time (unlike raw-REPL exec), so it should
  work, but scripting it reliably via a host-side automation harness
  (pexpect) proved flaky — timing-dependent, unclear if the flakiness is
  pexpect-specific or a real device-side issue. Not ruled fully in or out;
  don't assume it works without testing on the actual target script.
- The only mode `mpremote`'s own source confirms as truly bidirectional
  is interactive `mpremote repl` with a human actually typing at the
  keyboard (`repl.py`'s `do_repl_main_loop`, which forwards every
  keystroke to serial and every serial byte back to the console, in a
  single loop, with no protocol-exit sequence in between).

Rule for future lab scripts meant to run via `mpremote run`: never use
`input()`. If the script needs the user to pause and physically change
something, don't reach for a printed countdown either — see the entry
below (2026-08-27), which replaced `voltage_reference_lm358`'s countdown
with a push button. Checked the rest of the repo
(`grep -rl "input(" --include=main.py`) — `voltage_reference_lm358` was
the only offender; `fuse_test_voltmeter` and `cd4066_switch_tester`'s
`main.py` scripts stream output only and don't call `input()`.

## A push button (GPIO, `Pin.PULL_UP`, active-low) replaced the fixed countdown as the "wait for the user" mechanism in scripts needing a mid-run physical action (2026-08-27)

The `voltage_reference_lm358` countdown from the entry above
(`COUNTDOWN_S = 10`) was itself found to be too short on real hardware:
the user had to bump it to `13` after a too-fast unplug/replug of
`R_load` briefly touched leads together mid-reading. A fixed countdown
puts a hard time limit on a manual action (moving a resistor with bare
hands, on a breadboard) that has no natural fixed duration — too short
risks a mistimed/unsafe read, too long just wastes bench time, and either
way it has to be re-guessed and re-tuned per script/per user. A GPIO read
is not a keystroke: `mpremote run`'s raw-REPL streaming only blocks
*stdin*, not the device's own peripherals, so polling a push button
(`Pin(N, Pin.IN, Pin.PULL_UP)`, pressed = pin reads `0`) works fine and
gives an unbounded, no-guesswork "I'm ready" signal instead. Applied to
`voltage_reference_lm358/main.py`'s `wait_for_button()` (poll until
pressed, debounce, poll until released) in place of the `countdown()`
function; `breadboard.md`/`README.md` updated to describe wiring the
button (one leg to a spare GPIO, the other to GND) instead of the old
timing numbers. `pico/docs/inventory.md`'s Push Button row notes this use
case. Rule for future scripts in either repo that need the user to pause
mid-run for a physical action: wire a push button to a spare GPIO and
poll it, rather than reintroducing a `time.sleep`-based countdown.

## A bench-tested circuit's breadboard doesn't need to stay wired once its check passes — parts return to inventory unless a specific downstream circuit already needs them in place (2026-08-27)

After `psu_pico_rail` and `voltage_reference_lm358` both passed their
real-hardware checks, the question came up of whether to keep
`voltage_reference_lm358` wired up for whatever gets built next.
Resolved by reading the actual dependency edges in
`general_purpose_circuit_dependency.md`: `REF --> tier2` points at tier2
nodes (`VM`, `AM`, `FREQC`, `TIA`) that don't have netlists yet — nothing
currently buildable consumes `REF`'s physical output today, so there's no
reason to keep it on the breadboard. The spice netlist, `breadboard.md`,
`smoke_test.py`, and the bench-test result recorded in `lab/README.md`
are the durable record; the physical build is disposable and gets
re-assembled from those whenever a real downstream circuit needs it as an
input. `lab/README.md`'s circuits section was split into "built &
bench-tested" (with a bench-tested date/result column) and "designed, not
yet built" to track this distinction going forward — check the tier's
outgoing edges in the dependency graph before deciding whether a
just-tested circuit needs to stay assembled.

## A script's docstring/README referencing a component isn't the same as `breadboard.md` telling you to wire it — check both when a script assumes hardware exists (found 2026-08-26)

`voltage_reference_lm358/main.py` and its `README.md` both referenced
"`RloadB`, a 1kΩ resistor" to be connected/disconnected from pin 1 during
the ADC validation check, but `breadboard.md`'s wiring steps (1 through
5) never once mentioned it — the divider's R1/R2 were the only resistors
described. A user following `breadboard.md` literally, then running
`main.py`, has nothing to disconnect when prompted and no way to know
"RloadB" isn't just an alias for R2 (guessing so and disconnecting R2
breaks the divider itself instead of testing the buffer under load).

Fixed by: renaming to `R_load` for clarity (avoids implying it's a
counterpart to some "RloadA"), adding an explicit "optional, test-only"
step 6 to `breadboard.md` describing it as a *third*, separate resistor,
and cross-linking README.md's mention of it to that step. General lesson:
when a `main.py`/README references a physical component or action by
name, grep `breadboard.md` for that same name before trusting the docs
are complete — a script can be internally consistent with its README
while `breadboard.md` still has a real gap, since nothing currently
checks the two against each other.

## `main.py` scripts must print a verdict and exit, not stream readings forever (found 2026-08-27, `cd4066_switch_tester`)

Before this date, `cd4066_switch_tester/main.py` toggled the control pin
and printed a reading every second in an unconditional `while True:` —
same shape as the pre-fix `switch_pin_identifier`/`voltage_reference_lm358`
scripts before those got their own fixes (see the `input()`/countdown/push-button
entries above). The user ran it, watched it flip-flop indefinitely, and
had to Ctrl-C out and ask "did it pass?" — the script never told them, and
the loop wouldn't have stopped on its own either way. This is the same
underlying defect class as the `input()` and fixed-countdown entries
above: a `mpremote run`-launched script that doesn't know how to end
itself pushes the "is this done, and did it work" judgment call onto the
user, every time. Fixed by sampling a fixed number of cycles (`CYCLES =
5`, closed+open pairs), averaging each state, checking the averages
against the *same* thresholds `smoke_test.py` already checks against the
SPICE model (`CLOSED_MIN = 1.0`, `OPEN_MAX = 0.1`, delta `> 0.5`), then
printing `RESULT: PASS`/`RESULT: FAIL` and returning. Rule for future
`main.py` scripts here: if the hardware check has a knowable finite
duration (N samples, N cycles), don't loop forever printing raw data and
leave the pass/fail call to whoever's reading the terminal — sample a
fixed count, apply the same numeric thresholds `smoke_test.py` uses
against the sim (duplicate the constants; the Pico can't import the host
`tools/ngspice_runner.py` machinery), and print an explicit verdict before
exiting.

## `cd4066_switch_tester` symptom pattern: both states near VDD/2, delta of tens of mV — chip likely unpowered or control pin not reaching it, not (necessarily) a dead switch (found 2026-08-27)

First real-hardware run against switch 1 of the first CD4066BCN read
~2.05–2.11V for *both* `CLOSED` and `OPEN` (expected ~1.63V closed, ~0V
open; delta needs to be `> 0.5V`, actual delta was only ~0.04–0.05V) —
`RESULT: FAIL`. This matches the "sits at some fixed in-between value
that doesn't move" failure mode already called out in this circuit's
README, but the *specific* voltage is a useful diagnostic detail worth
keeping: ~2.05–2.11V is close to VDD/2 (VDD=3.3V rail), not close to
either expected rail-referenced value, and it barely shifts with the
control pin. A CD4066B analog switch has body diodes to VDD/VSS on each
I/O pin regardless of whether the chip's control logic is actually
switching; with VDD unpowered or the control pin not actually reaching
pin 13, those diodes (plus the two 10kΩ bias resistors from VDD and to
GND on either side) can produce a fixed-ish mid-rail divider that has
nothing to do with the commanded state — which is consistent with what
was observed. This has **not** been confirmed as the root cause on this
specific bench setup (VDD/control continuity wasn't independently
probed before this was written) — treat "check VDD pin 14 and the GP15→
pin 13 control wire for actual continuity before condemning the switch
itself" as the first debugging step, not a settled diagnosis. If a future
session sees this same symptom (both states clustering near VDD/2, tiny
delta) on this or a similar bilateral-switch bring-up jig, check power/
control continuity first rather than assuming the part itself is bad.

Also worth noting for future wiring-step edits: the original step 3
("same breadboard row, no extra wire needed if they're already in the
same row") was true in principle (breadboard rows are single electrical
nodes) but unactionable as written — it reads like something that might
coincidentally happen, when actually it only happens if you deliberately
plan for it back in step 2, and won't by default since the LM358's DIP-8
body straddles the breadboard's center gap, putting every one of its
pins in its own row separate from wherever R1/R2 got plugged. Rewrote it
as an unconditional "run a jumper" instruction with the row-sharing
optimization noted as an aside, not the primary instruction.

## `cd4066_switch_tester` fail persists after swapping control wire, VDD wire, and the chip itself — narrows the fault to whatever wasn't touched (2026-08-27)

Following up on the entry above: the user swapped the GP15→pin 13
control wire, then the VDD (pin 14) wire, then the whole CD4066BCN, each
as a separate re-run. All three trials reproduced the same failure to
within a few mV (~2.08–2.10V closed, ~2.04–2.06V open, delta ~0.04V
every time) — none of the three swaps moved the reading at all. This
disproves the previous entry's leading hypothesis (VDD or control-pin
continuity, or a bad chip) as stated: if any of those three things were
the actual fault, replacing that specific thing should have changed the
symptom, and it didn't, across all three independent substitutions.

Elimination logic worth reusing on similar "swapped the obvious suspects,
symptom identical" reports: when N independent substitutions each
reproduce a symptom unchanged, the fault is almost certainly in whatever
was common to all N trials, not in any of the swapped parts. Here, what
stayed constant across all three trials: the VSS (pin 6) → GND wire (never
swapped), the two 10kΩ bias resistors and their breadboard rows (never
touched), the GP26 probe wire (never touched), and the physical
breadboard rows/rail segments themselves. Updated
`cd4066_switch_tester/README.md` with an explicit "Troubleshooting"
checklist covering exactly these four items, ordered by how cheap they
are to check, and flagged one candidate worth specifically calling out:
full-size breadboards commonly split their power rails into independent
left/right halves that look continuous but aren't bridged — if
`psu_pico_rail`'s GND jumper and the pull-down resistor's GND leg (or the
VDD jumper and the pull-up resistor's VDD leg) land on different
unbridged segments, every downstream reading floats regardless of how
correct each individual wire looks. None of this is confirmed yet — it's
the next set of things to check, same "not a settled diagnosis" caveat as
the previous entry. If a future session sees another report of "swapped
the suspect part, identical symptom" on any circuit here, apply the same
elimination logic before proposing a new hypothesis: list what was
actually held constant across the trials before guessing what's wrong.

## `cd4066_switch_tester` FAIL root cause was DIP pin misidentification, not power/control continuity — the two entries above chased the wrong hypothesis (resolved 2026-08-28)

The two kb entries above this one built up a careful elimination case for
VDD/control-pin continuity or split power rails as the fault, after
swapping the control wire, VDD wire, and the chip itself all reproduced
the identical ~2.05–2.11V/delta-~0.04V symptom. None of that was actually
wrong reasoning given what was known, but the real cause was upstream of
all of it: the user had misidentified the CD4066B's DIP-14 pins, so most
of the intended connections (I/O A, I/O B, control, VSS, the bias
resistors) weren't landing on the pins `breadboard.md` describes in the
first place. Swapping "the control wire" or "the chip" didn't change
anything because the swap preserved the same wrong pin mapping every
time — this is a case the elimination logic from the entry above
genuinely can't catch, since a systematic wiring-plan error is common
across every trial by construction, same as a real continuity fault
would be. Once wired to the pins `lab/docs/parts_reference.md` actually
specifies, all 10 CD4066BCN units passed switch 1 on the first run — see
`lab/README.md`'s bench-tested table and `cd4066_switch_tester/README.md`'s
"Resolved 2026-08-28" note.

Lesson for future DIP-package bring-up jigs here: before trusting any
continuity/power-rail hypothesis for a "swap didn't help" symptom, verify
pin identification itself first (pin 1 notch/dot, counting direction)
against `lab/docs/parts_reference.md` — a systematic pin-mapping error
produces exactly the same "every substitution reproduces the fault"
signature as a real constant-cause fault, and is cheaper to rule out.

## `psu_ultralow_v1`'s 15 Ω and `fuse_test_voltmeter`'s 10 Ω are two unrelated test loads, not a documentation contradiction (clarified 2026-08-28)

`psu_ultralow_v1/breadboard.md` and `README.md` state "15 Ω test load →
~1.44V, ~96mA" as the `.spice`-derived nominal design point (`Rload = 15`
in `psu_ultralow_v1.spice`, chosen for a ~100mA operating-point target).
`fuse_test_voltmeter/breadboard.md` and `.spice` use a 10 Ω load for its
own bench fuse-test jig instead. These look like the same "output load
resistor" restated with different values, but they aren't — the 15 Ω
figure is a purely descriptive characterization of the *finished PSU's*
output (no resistor is in `psu_ultralow_v1/breadboard.md`'s parts list or
wiring steps; `README.md` § "Validation without a multimeter" recommends
probing the fuse leads directly instead). The 10 Ω figure is an actual
physical component in `fuse_test_voltmeter`'s parts list, used to
bench-test a bare polyfuse *before* it's trusted in a PSU build at all —
see `breadboard.md`'s own build-order note ("voltmeter → test → PSU →
demo. Not PSU-first"). The 10 Ω value itself traces back to
`docs/history.md`'s 2026-08-15 10:41 entry: the user didn't have a 15 Ω
resistor in stock (only 10 Ω and 100 Ω), so 10 Ω was substituted and then
reused for both the RXEF005 and RXEF050 tiers rather than ordering a
dedicated value — it was never meant to match `psu_ultralow_v1`'s 15 Ω.
Both `breadboard.md` files now cross-reference each other on this point
(2026-08-28 edit) — if a future session sees a value mismatch between a
PSU's own characterization numbers and a measurement-tool jig's load
value, check whether they're actually describing the same test before
treating it as a bug.

Related, clarified the same day: `fuse_test_voltmeter.spice`'s header
comment states the RXEF005 tier's plain 10 Ω load (no short) already
draws ~150mA — 3x the fuse's 50mA rating — matching the ~1.43V "cold
reading" in `breadboard.md`'s Expected Behavior section. This isn't a
separate current level the deliberate short step produces; the fuse may
trip on its own within a few seconds of being loaded at all, and the
short step (near-dead-short current) exists to force a fast, unambiguous
trip regardless of unit-to-unit tolerance rather than to create the
overcurrent condition in the first place. Both `breadboard.md`'s
step-by-step procedure and its Expected Behavior section were reworded
2026-08-28 to say this explicitly, so a fuse tripping before it's ever
shorted should read as expected behavior, not a wiring problem.

## `fuse_test_voltmeter`'s "≥1W" load resistor spec was unsourceable — the kit has no such part; fixed with a 2x2 series-parallel bank of 1/4W resistors (2026-08-28)

The `smoke_test.py` convention entry above (2026-08-24) records that the
RXEF050 tier's ~0.82W dissipation was "fixed by specifying ≥1W in that
one part's row" in `breadboard.md`. That spec was never actually checked
against the real inventory — the user pointed out the SunFounder Thales
kit (`pico/docs/inventory.md`) only stocks 1/4W (0.25W) resistors at every
listed value; there's no ≥1W part to pull for this jig. `RLOAD_RATING_W =
1.0` in `smoke_test.py` was asserting a part that doesn't exist in this
lab's inventory — the smoke test was passing against a spec, not against
what could actually be built.

Fixed by building the RXEF050 jig's 10 Ω equivalent load as a 2-series x
2-parallel bank of four 10 Ω 1/4W resistors (two 20 Ω branches in
parallel) instead of a single part. In a symmetric 2s2p network the total
power divides evenly across all four resistors, so each one sees only
~0.204W (0.816W total / 4) — under its 0.25W rating with headroom, using
only kit-stock 10 Ω resistors (10 on hand, only 4 needed). The RXEF005
jig was never the problem: its single 10 Ω resistor dissipates ~0.204W
(1.5V cold), already under 1/4W, and the fuse self-trips within seconds
under that load anyway, further limiting exposure — no bank needed there.

`smoke_test.py` was rewritten to check *per-resistor* power
(`RLOAD_UNIT_RATING_W = 0.25`, `p_cold_total / n_resistors` where
`n_resistors` is 1 for the RXEF005 tier and 4 for RXEF050) instead of
comparing the network's total dissipation against a single part's rating
— this ties the smoke test to what `breadboard.md` actually specifies
building, catching exactly this class of mismatch in the future.
`pico/docs/inventory.md`'s Resistors section now states the 1/4W ceiling
explicitly so this doesn't need re-deriving from kit-listing silence
again. Lesson: a "use a ≥X-rated part" fix in a breadboard.md is only a
real fix if that part is confirmed to exist in `pico/docs/inventory.md`
(or a sourced replacement) — cross-check the actual inventory before
trusting a wattage/rating spec that was invented to satisfy a smoke-test
number, especially in a repo whose whole premise is "no part beyond what's
already on hand."

## `breadboard.md` files written as general/batch procedures are unusable as bench instructions for one physical unit — split off a `quickstart.md` (2026-08-28)

`measurement_tools/fuse_test_voltmeter/breadboard.md` was written to cover
the full scope at once: self-check, both fuse tiers (RXEF005 1.5V /
RXEF050 3.0V), a batch of 20 units per tier, the RXEF050 2s×2p resistor
bank, and the eventual PSU demo — every wiring table branched on "for
RXEF005 jig... for RXEF050 jig...". The user, holding one battery holder,
one 50 mA fuse, and a Pico already wired to USB, reported not being able
to make any sense of it and asked (with considerable profanity) for
explicit next steps for exactly the hardware in front of them. The fix
was not rewording the existing file — it was adding
[quickstart.md](../../measurement_tools/fuse_test_voltmeter/quickstart.md),
a separate doc with zero tier/batch branching, hardcoded to the single
1.5V/RXEF005/1-resistor case with concrete wire-by-wire steps, and no
"why" prose — plus a one-line pointer at the top of `breadboard.md`
sending the single-unit case there. `README.md`'s Files table and Build
section were updated to route to `quickstart.md` first. `breadboard.md`
itself was left otherwise intact — it's still the correct reference for
the 500 mA tier, batches, and the PSU demo, just not the first thing to
hand someone mid-build.

General lesson for any future circuit here with more than one
tier/variant/batch dimension: write the multi-dimensional reference doc
(good for planning, smoke tests, "why" context) *and* a separate,
tier-locked quickstart with no conditional branching at all, rather than
assuming a reader mid-build will filter a general doc down to their own
case themselves. Don't retrofit this everywhere preemptively — do it when
a circuit's `breadboard.md` actually has more than one branch a bench
user has to track (as fuse_test_voltmeter's did with 2 tiers × 3 stages),
not for single-path circuits that don't need it.

## `fuse_test_voltmeter`'s GP15 arm/disarm switch: one throw + internal pull-down, not both rails wired to the switch (2026-08-28)

Added a second, independent GPIO input (GP15) wired to an SPDT slide
switch, specifically so that deliberately disconnecting the battery to
stop a test doesn't print `*** FUSE TRIPPED ***` — a real trip and an
intentional power-down are otherwise indistinguishable to `main.py`
(both collapse GP26 to ~0V). Design choice worth preserving: the switch
is **not** wired into the battery's power path (not in series with the
fuse under test) — it's a separate signal-only circuit read by a second
GPIO, so its own contact resistance never confounds the fuse
current/voltage this jig exists to characterize. `main.py` gates
trip/reset detection and the onboard LED on this ARMED state; voltage
still streams every cycle regardless of ARMED/DISARMED. GP15 was picked
because it's unused elsewhere in the repo and sits next to a physical
GND pin (pin 18) for a short jumper run — there's no central
pin-allocation table for this repo, just per-circuit docstrings, so
check `main.py`/`breadboard.md` GPIO usage across the repo first if a
future circuit needs a spare digital input.

The first cut wired both switch outer pins live (pin 1 to GND, pin 3 to
3V3(OUT)) on the reasoning that neither pull resistor was then needed.
The user caught that this design permanently wires both power rails onto
the switch at once — the switch's own mechanism
never bridges both outer pins to each other (it only ever connects the
common pin to *one* outer pin at a time, per the `switch_pin_identifier`
entry above confirming it's a standard SPDT-style part), so GND and 3V3
are never directly shorted through it in steady state. But wiring GND to
one outer pin bought nothing: the only two states that ever mattered were
"common connected to 3V3" and "common connected to *not* 3V3," and a
second rail sitting one throw away serves no purpose except being one
mechanical fault (a bent contact, a worn/make-before-break slider bridging
both outer pins momentarily during the slide) away from a real rail-to-rail
short. There's also no benefit to burning a GND pin on a signal that
doesn't need it.

Fixed by dropping the GND wire entirely: pin 2 (common) → GP15, pin 1 →
3V3(OUT), pin 3 → left unconnected. `main.py` now configures
`Pin(15, Pin.IN, Pin.PULL_DOWN)` instead of the bare `Pin(15, Pin.IN)` from
the previous entry, so the unconnected throw still reads a defined LOW
(DISARMED) via the Pico's internal pull-down rather than floating — this
preserves the original goal (never let GP15 float, see the
`switch_pin_identifier` GND-reference entry above) without ever wiring a
second rail onto the switch. Updated `main.py`, `quickstart.md`,
`breadboard.md`, and `pico/docs/inventory.md`'s Slide Switch row to match;
jumper count for the arm switch dropped from 3 to 2 accordingly.

General lesson for any future switch-to-GPIO wiring in this repo: a single
SPDT throw + the target GPIO's internal pull resistor is sufficient to get
a defined level in both switch positions. Only wire a second rail onto a
switch's other throw if the pin's role genuinely needs an actively-driven
(not just pulled) level in both positions — e.g. driving a load that pulls
more current than an internal pull resistor can source/sink, not a plain
digital input like this one.

One footgun still worth flagging for this circuit: if the operator
forgets to flip to ARMED before shorting the resistor during an actual
fuse test, the voltage collapse still happens and still prints as a raw
number, but `*** FUSE TRIPPED ***` and the LED won't fire — easy to
misread as "it didn't trip" when actually the switch was just left in
the wrong position. `breadboard.md`/`quickstart.md` call out sliding to
ARMED before the short step, but there's no code-side safeguard against
forgetting it.

## `ne555_astable` output-divider fault survived a plausible visual re-wire — re-seating R1/R2 in series + bridging the two ground rails changed nothing (2026-09-12)

First bring-up of `oscillators/ne555_astable` found GP26 pinned at exactly
3.300V through the output divider (`breadboard.md` §4, two 10kΩ resistors)
instead of the expected ~2.75-2.9V half-swing — see the entry-worthy
detail in `ne555_astable/README.md` § Validation. The leading hypothesis
was R2 (tap→GND) missing/open, so the user re-wired R1/R2 into an actual
series pair and, on the theory that a full-size breadboard's two vertical
ground rails might be an unbridged split (a real failure mode already
documented in the `cd4066_switch_tester` entries above), also ran a jumper
bridging the two ground rails together. Re-running `oscillation_probe`
afterward produced a reading statistically indistinguishable from the
pre-fix one (swing still ~3.3V, still pinned at the ADC's saturation
point) — neither change moved the symptom at all.

Same elimination lesson as the `cd4066_switch_tester` pin-misidentification
case (see above): when a plausible-sounding visual re-wire doesn't move a
symptom, the fault likely isn't in what was changed. Don't propose a third
guess-and-rewire cycle here — the next step is a direct, instrumented
per-leg check with `measurement_tools/resistance_measurement` (power down
`psu_4xaa` first per that tool's own README, then check R1 and R2
individually and the tap→GP26 jumper's continuity) rather than another
round of eyeballing the breadboard. If a future session lands on this
build with the divider still unresolved, start with that measurement, not
another re-wire attempt.

## Windows/WSL photo saves can leave only a `*.jpg:Zone.Identifier`
stray file behind, with no actual image — check for the real file before
assuming a referenced photo exists (2026-09-12)

While documenting the `ne555_astable` bring-up, an `ls` of
`measurement_tools/oscillation_probe/` turned up
`PXL_20260912_193901707.jpg:Zone.Identifier` (a small, ~25-byte metadata
file Windows attaches to downloaded/copied files marking their security
zone) with no corresponding `PXL_20260912_193901707.jpg` actually present
— the photo transfer from the phone/Windows side hadn't completed yet, but
the Zone.Identifier companion file had already landed. A directory listing
that shows only the `:Zone.Identifier` file (rather than the real image
alongside it) means the referenced photo doesn't exist in the repo yet,
even if the user believes they already saved it — worth flagging rather
than assuming the file is just named something slightly different. In
this case the real `breadboard.jpg` followed shortly after in the same
session.

## `fuse_test_voltmeter`'s resistor-shorting instruction (hand-touching two bare leads) is unreliable — switched to a jumper seated in the breadboard rows instead (2026-08-28)

The original short-test instruction in `quickstart.md`/`breadboard.md`
said to "touch the resistor's two legs together" by hand, using two
Dupont wire tips. The user reported this connection as spotty and
inconsistent — consistent with hand-holding two thin wire tips against
each other being a poor, easily-fumbled contact compared to a wire seated
firmly in a breadboard's spring contacts. Since the whole jig is already
breadboard-mounted (`quickstart.md`'s parts list opens with "Parts to add
to what's already on the breadboard"), both ends of the resistor already
land in distinct breadboard rows — so a spare jumper wire (or a bent
solid-core one) plugged into those same two rows gives a firm, hands-free,
repeatable short instead. Both docs were updated to describe this
technique in place of hand-touching. If a future circuit here has a
similar "deliberately short two nodes by hand" step, prefer the
same jumper-in-breadboard-rows approach over hand contact from the start
rather than waiting for a reliability complaint.

## Don't offer "get a multimeter" as an alternative to restoring the sense resistor — it's a false dichotomy (2026-08-28)

`history.md:3498` and `:3508` phrased the fix as an either/or: "the resistor
goes back into the loop... or you check the fuse a different way
(multimeter/continuity check)." That framing is wrong and cost an entire
session's worth of goodwill. There is no "different way" that's actually
different — the resistor-divider *is* the Pico-based continuity/trip
check; suggesting an external multimeter implies the Pico jig can't do
this on its own, which is false. The only real fix was ever "put the
resistor back," full stop. Never present hardware the user doesn't have
(multimeter, continuity tester) as an option when the existing jig, once
correctly wired, already answers the question — that's asking them to buy
a tool to route around a bug in advice, not in the circuit.

**Also clarified this session**: bridging the resistor's two rows with a
spare jumper (the deliberate-short step `quickstart.md`/`breadboard.md`
already documented) already forces ~2A through just the fuse's cold
resistance — a harder short than the passive ~150mA load, and *more*
aggressive than what removing the resistor outright was ever trying to
achieve. So there was never a tradeoff between "sensitive" and
"aggressive" — bridging gives both, removal gives neither (it just reads
0V forever, tripped or not). `quickstart.md` and `breadboard.md` now carry
an explicit "resistor is the sensor, not a load — bridge it for a harder
short, never remove it" callout up top so this doesn't need rediscovering
a fourth time.

If a future session finds the resistor missing from this jig again: that
is the whole bug, restoring it is the whole fix, `main.py` needs no
changes, and no additional tool is needed to answer "is the fuse
tripping" — say so plainly instead of hedging toward external test
equipment.

## `fuse_test_voltmeter`'s open trip/reset question was bypassed, not resolved — the user built current-measuring `ammeter_10ohm`/`ammeter_1ohm` instead and validated both fuse batches that way (2026-08-30)

A long debugging thread on `fuse_test_voltmeter`'s voltage-probe approach
to detecting a polyfuse trip (chattering near threshold, battery-vs-switch
confounds, a mis-seated shorting jumper) never actually got closed out —
it ended with a real structural gap: with the sense resistor physically
removed from the loop, GP26's probe node and the GND probe node collapse
to the same physical node, so the reading pins at ~0V regardless of the
fuse's actual state, permanently reporting a trip. Instead, the user
built two new, separate jigs —
[measurement_tools/ammeter_10ohm/](../../measurement_tools/ammeter_10ohm/)
and
[measurement_tools/ammeter_1ohm/](../../measurement_tools/ammeter_1ohm/) —
that measure loop **current** directly through a shunt resistor, with a
slide switch wired in parallel with the shunt as a hands-free shorting
jumper, rather than inferring a trip from a probe-node voltage collapsing.
Both jigs were used to bench-test all 40 polyfuses in
[pico/docs/inventory.md](../../../pico/docs/inventory.md) (20× RXEF005 via
`ammeter_10ohm`, 20× RXEF050 via `ammeter_1ohm`) — all 40 units PASS
(confirmed trip on short, confirmed reset on short removal).

Consequence for future sessions: `fuse_test_voltmeter`'s own structural
bug (described above) is **still unfixed** and its own pass/fail criteria
from `quickstart.md` have still
never actually passed on that specific build. Don't treat the ammeter
jigs' PASS results as evidence that `fuse_test_voltmeter` itself got
fixed — they're a completely independent measurement approach on
different hardware. If a future session is asked to actually fix
`fuse_test_voltmeter`, that's still open work; it's just no longer
*blocking* anything, since polyfuse validation now has a working path
that doesn't depend on it. `lab/README.md`'s built-and-bench-tested table
was updated to say this explicitly on both rows.

## Working explanation for the "fuse self-heals instantly" symptom: thermal latch requires enough post-trip current to stay hot, and 1.5V doesn't supply it (2026-08-30)

Using `ammeter_10ohm` to actually watch current (not just a probe
voltage) through an RXEF005 during a deliberate short-then-release cycle
gave a physical explanation for a symptom that's been read as suspicious
throughout the `fuse_test_voltmeter` debugging thread above ("miracle
superfuse that heals itself instantly," sub-second/sub-~2-minute
recoveries): a polyfuse's high-resistance tripped state only *stays*
latched if enough current keeps flowing through it post-trip to sustain
self-heating (`I²R`) above the polymer's transition temperature. At the
lab's actual 1.5V single-cell supply, a tripped fuse in series with a
10Ω-class load can only pass on the order of hundreds of microamps to
low-single-digit milliamps — nowhere near enough `I²R` to hold the
element hot — so it cools and un-trips within roughly a second, not the
several-minutes figure usually associated with polyfuses. That figure
implicitly assumes a supply voltage (5V, 12V) high enough to keep pushing
enough leakage/holding current through the tripped device to sustain the
latch. This reframes every "impossibly fast reset" observation in the
`fuse_test_voltmeter` thread above as expected PTC behavior at this
specific (very low) supply voltage, not a sign the fuse never really
tripped — full writeup with the numeric reasoning is in
`measurement_tools/ammeter_10ohm/README.md` (end-user-facing, since it's
a real physics explanation worth keeping there, not just a process note).

One inconsistency worth flagging for a future session that needs the
exact numbers: the user's own reasoning behind this finding cited the
RXEF005's trip threshold as ~100mA, but every other doc in this repo
(`pico/docs/inventory.md`, `fuse_test_voltmeter`'s own SPICE/README) is
built around the RXEF005 being a **50mA**-rated device — that's also
literally what "005" encodes in Littelfuse's RXEF part-numbering scheme.
Not corrected in the end-user README (the qualitative conclusion — 1.5V
can't sustain the latch — holds regardless of which exact threshold
number is right, and the actual bench result, all 20 units passing, isn't
in question), but don't propagate "100mA" as this device's rated trip
current in future work without re-deriving it; treat 50mA as the
documented spec until someone explicitly re-measures the actual trip
point.

## `resistance_measurement`: measuring an unknown low resistance with only a Pico ADC and one known resistor (2026-08-30)

New pattern worth reusing whenever a future circuit here needs to
characterize an unknown low-value resistance (a shunt candidate, a cable,
a suspect component) without a multimeter on the bench: a simple
voltage-divider with a known reference resistor on the high side and the
unknown resistance on the low side, read by a single Pico ADC pin at the
midpoint. `R_x = R_ref * (V_out / (V_in - V_out))`, solved from the
standard divider equation. Built in
[measurement_tools/resistance_measurement/](../../measurement_tools/resistance_measurement/)
specifically because
[ammeter_1ohm](../../measurement_tools/ammeter_1ohm/) needed a ~1Ω-class
shunt and no 0.1Ω resistor was in stock yet (now on order — see
`pico/docs/inventory.md`'s "On Order" section, 2026-08-30 metal film
resistor kit); a chain of jumper wires was used as the improvised shunt,
and this jig measured it at ~1.005Ω. `R_ref = 10Ω` keeps worst-case
current (a dead short on `R_x`) to ~330mA through the Pico's 3V3 rail —
safe without any additional current limiting — which is a reusable
sizing rule: pick `R_ref` large enough that `V_in / R_ref` alone is a
safe short-circuit current for whatever's driving the divider, independent
of what `R_x` turns out to be.

## Low-side current sensing: keep any series protection element (diode, switch) off the sensed leg, not just off the ADC probe leg (2026-08-30)

`ammeter_1ohm`'s 1N5817 reverse-polarity diode is deliberately wired on
the **high side** (battery positive → diode → fuse), while the current
shunt sits on the **low side** (fuse → shunt → GND), with the ADC probe
at the fuse/shunt junction. This isn't arbitrary: any series element's
own voltage drop shows up in a low-side sensing circuit's ADC reading only
if that element sits between the probe node and the shunt itself. Putting
the diode in series with the shunt (either side of it) would have added a
fixed ~0.35–0.45V offset to every current reading that would then need to
be characterized and subtracted before the `V/R` math means anything;
putting it upstream of the entire fuse+shunt leg (as built) means the
diode's drop is invisible to the measurement — it just reduces the total
voltage available to the fuse+shunt loop, which the ammeter doesn't need
to know about to correctly report current through the shunt. General
rule for any future low-side-sensing circuit here: identify the exact two
nodes the ADC measures between, and keep every other series component
(protection diodes, switches, connectors) outside that specific span,
even if they're still logically "in series with the shunt" from a
whole-loop perspective.

## `psu_ultralow_v1` marked "built & bench-tested" in `lab/README.md` on component-level validation only — no assembled-PSU demo was performed (2026-08-30)

Per explicit user instruction, `psu_ultralow_v1`'s row moved from
"designed, not yet built" to "built & bench-tested" in `lab/README.md`
once its RXEF005 polyfuse passed validation via `ammeter_10ohm` (see the
entries above) and its AA battery holder was confirmed ready in
`pico/docs/inventory.md`. This is **not** the same thing as the
test-vs-demo distinction `fuse_test_voltmeter/README.md` establishes
elsewhere in this repo (bench-test the bare component, *then* build the
actual PSU and re-probe it as its own separate demo step) — no assembled
`psu_ultralow_v1` unit was built or re-probed as a finished PSU here. The
bench-tested table row's note says this explicitly ("component-level
validation... has not been separately re-probed as its own demo build")
so a future session doesn't read the table entry as claiming more than
what was actually done. If a future session is asked to actually build
and demo this PSU as an assembled unit, that's still open work, distinct
from what "built & bench-tested" records here.

## New AA-battery PSU tiers (`psu_3xaa`, `psu_4xaa`) inserted between `psu_low` and `psu_medlow` in the dependency graph (2026-08-30)

Added
[power_supplies/psu_3xaa/](../../power_supplies/psu_3xaa/) (4.5V) and
[power_supplies/psu_4xaa/](../../power_supplies/psu_4xaa/) (6.0V) as a
straightforward extension of the existing AA-series progression
(`psu_ultralow_v1` 1×AA → `psu_low_v2` 2×AA), reusing the exact same
protection stack (RXEF050 500mA polyfuse + 1N5817 Schottky) as
`psu_low_v2` rather than inventing a new one — both fit the "designed,
not yet built" category, same as `psu_low_v2`/`psu_medlow_usbc`. The
mermaid `graph TD` in
[general_purpose_circuit_dependency.md](../general_purpose_circuit_dependency.md)
got two new subgraphs (`psu_3aa`, `psu_4aa`) spliced into the existing
`psu_ultralow -->|upgrade to| psu_low` chain
(`psu_low --> psu_3aa --> psu_4aa --> psu_medlow`), plus matching
`POLYFUSE -.required.->` edges and `style` lines — per the "pure mermaid,
no prose" convention at the top of this file, no explanatory prose was
added outside the diagram itself.

Also added
[power_supplies/psu_medlow_lm317/](../../power_supplies/psu_medlow_lm317/)
as an alternative `psu_medlow`-tier implementation (the SFE Breadboard
Power Supply Kit — LM317 adjustable regulator, switch-selectable 3.3V/5V,
fed from a DC barrel jack) alongside the existing `psu_medlow_usbc`
(fuse+bypass only, since a USB-C adapter is already regulated). This one
is a kit that's only been ordered, not received or built — its
`breadboard.md` derives the standard LM317 feedback-resistor math
(`R1=240Ω` fixed, `R2` switched between 390Ω and 390Ω+330Ω for 3.3V/5V)
from the kit's own BOM rather than from a confirmed reading of the actual
PCB traces, and says so explicitly. If a future session gets the physical
kit in hand, verify that math against the real board before trusting it,
same treatment as the 3296 trimpot's "confirm once received" caveat
elsewhere in this repo. No `.spice`/`smoke_test.py` for this one — per
user instruction, no netlist was requested for the kit, only inclusion in
the dependency graph and matching README/breadboard.md docs. A new
`PSUMEDLOWLM317` node was added inside the existing `psu_medlow` subgraph
with a dotted `-.alternative.->` edge to `PSUMEDLOW`, matching the
existing `POLYSWITCH -.alternative.->` pattern used elsewhere in the same
file for other alternative-implementation edges.

## Scope/logic-analyzer tiers M0–M5 added to `concurrent_meas_tools` (2026-09-01), replacing the single `SCOPE` node

The old `SCOPE["Real-Time Oscilloscope or Equivalent"]` node (the one
`history.md` calls out as the long-standing gap forcing ADC-polling
scripts to stand in for a scope) was replaced with a nested `scope_tiers`
subgraph of six tier nodes (`SCOPEPICO`/M0 through `SCOPEBENCH`/M5),
mirroring the PSU tier-ladder pattern (`psu_ultralow -->|upgrade to|
psu_low --> ...`) via `SCOPEPC -->|upgrade to| SCOPEUSBSER -->|upgrade
to| SCOPELA -->|upgrade to| SCOPEDSO -->|upgrade to| SCOPEBENCH`. First
draft put the tier writeup in a prose section after the ```mermaid
fence — caught and reverted before being left in the repo, since that
directly violates the "pure mermaid, no prose" convention (top of this
file): all the tier detail (specs, what it unlocks, cost, purchased vs.
on-hand) now lives in each node's own bracketed label text instead, per
that convention's existing rule of "the fix is to edit the label text in
place, no separate paragraph."

Tier assignment logic, for a future session extending this ladder: **M0
(Pico MicroPython, $0, on hand)** and **M1 (desktop PC onboard sound
card, $0, on hand)** are already-owned capabilities getting formalized as
tiers, not purchases — M0 reuses the measured noise-floor figure from
`measurement_tools/gpio_analog_sensing/` (std-dev <5 counts/<0.25mV with
a 100nF filter) rather than a spec-sheet number, and M1 is scoped
strictly to AC/audio-band (20Hz-20kHz) since the sound card's AC coupling
can't read DC — it only supersedes the smartphone-based `AUDIOSC`
bootstrap node within that band, not generally. **M2 (USB-serial
bit-banged GPIO, ~$1-2)** is deliberately framed as a cross-check
channel, not a capture instrument — still software-timed like M0/M1, its
only advantage is being a second, PC-hosted, Pico-independent digital
line. **M3 (8ch 24MHz USB logic analyzer, ~$5-8)** is the first tier with
real hardware-timed sampling/triggering, which is the actual gap
`history.md`'s priority list flagged. **M4 (DSO138 kit, ~$15-25)** is the
first tier with true analog waveform capture (not just digital edges or
audio-band signal) — kept as a distinct tier from M3 rather than folded
together because digital timing (M3) and analog waveform shape (M4) are
different capabilities the existing tier1-9/safety graph needs
separately. **M5 (bench-grade mixed-signal, cost TBD)** is intentionally
left unpriced/unspecified — it's a placeholder for "revisit once tier7/8
RF/HV-pulse work outgrows M3/M4," not a purchase to plan around yet, per
the user's explicit instruction to postpone purchases until they're
definitely needed. `spacetime_circuits_dependency.md`'s `GENERAL` stub
node and intro paragraph were updated to mention "scope/logic-analyzer
tiers M0-M5" alongside the existing PSU/protection/tier callouts, since
`SCOPEBENCH -.required.-> SPACETIME` is the only cross-file edge this
addition introduced.

Also deleted `docs/spacetime_lab_budget.md` in the same session (explicit
user instruction — it was a one-off curiosity, not worth maintaining). It had three live referrers beyond `history.md` (which
was left alone, append-only-log treatment as usual): `lab/README.md`
(repo-structure tree + one prose mention), `docs/orders.md` (one
citation on the 3296 trimpot entry), `docs/parts_reference.md` (one
citation on the LM358 entry) — all three were edited to remove the
dangling reference rather than leaving a dead link. Before deleting a doc
like this, grep the whole repo for its filename, not just check whether
the user named specific referrers.

## Any signal from psu_4xaa/psu_3xaa's ~5.5–6V rail (or higher) must go through a divider before touching *any* Pico pin — GP26/ADC0 and every other GPIO cap out at 3.3V (found 2026-09-06)

`psu_4xaa/README.md`'s old "Validation without a multimeter" section said
to "probe across the Schottky with a Pico ADC pin," and
`oscillators/ne555_astable/breadboard.md` said to probe the NE555's pin 3
output (which swings ~0V to ~VCC, i.e. ~5.5V when powered from
`psu_4xaa`) with a Pico ADC pin, a multimeter, or the soundcard. Both are
unsafe as literally written: `general_purpose_circuit_dependency.md`'s
own `SCOPEPICO` node documents the RP2040 ADC as "0-3.3V only," and that
ceiling applies to every Pico GPIO, not just the ADC-capable ones — wiring
a ~5.5V node straight onto GP26 (or any other pin) risks exceeding the
pin's absolute maximum rating. This wasn't caught earlier because the
lower-voltage circuits this repo's GP26-probe convention was built around
(`resistance_measurement`, `ammeter_10ohm`/`ammeter_1ohm`,
`cd4066_switch_tester`) are all powered from the Pico's own 3.3V rail or
similarly low-voltage sources, so the convention never needed a divider
before now — `psu_4xaa`/`psu_3xaa` and anything powered from them (like
`ne555_astable`) are the first circuits in this repo's build-and-validate
sequence that actually exceed 3.3V.

Fixed by adding an explicit 2:1 resistor divider (two 10kΩ, on-hand kit
parts) in front of GP26 in both `psu_4xaa/README.md` § Validation and
`ne555_astable/breadboard.md` § 4 — halves the ~5.5V swing down to a safe
~2.75V max, drawing only ~275µA (negligible load on either the PSU or the
NE555's output stage). General rule for any future circuit here powered
above 3.3V (the whole AA-series `psu_system` family from `psu_3xaa` up,
`psu_medlow`, anything mains- or wall-adapter-derived): never route a
node from that circuit straight to a Pico pin for validation — always
check the expected voltage against 3.3V first, and insert a divider
(matching this 2:1 pattern, or scaled further for higher rails) if it's
anywhere close. This is a distinct hazard from the "no multimeter" rule
below (which is about *how* to measure, not what's safe *to* measure) —
both need checking independently for any new PSU-adjacent circuit.

## `psu_4xaa.spice`'s `Rload = 20` (and the matching "20 Ω test load" language in `breadboard.md`) describes a simulated design point, not a physical part to build — same convention as `psu_ultralow_v1`, but stated ambiguously enough to cause real confusion (found 2026-09-06)

The user had physically built `psu_4xaa` per its `breadboard.md` and got
stuck on "wire the 20Ω test load" — a real problem, since
`pico/docs/inventory.md` has no 20Ω resistor, and `psu_4xaa/smoke_test.py`
already carries the comment "Rload is a simulated representative
downstream load (no physical resistor in the parts list)," directly
contradicting the breadboard.md prose that reads like a build instruction.
The user's own guess (two 10Ω in series) would have been actively unsafe
if followed: at the ~276mA nominal design current, two 10Ω 1/4W resistors
in series each dissipate ~0.76W — three times their 0.25W rating.

Fixed by rewording `breadboard.md`'s "Expected behavior" section to state
explicitly that 20Ω is `Rload`'s simulated value, cross-referencing
`psu_ultralow_v1/README.md`'s validation section as the established
precedent for this exact pattern (a PSU's `.spice`/`smoke_test.py` models
a representative load; nothing in the breadboard parts list builds one).
`psu_4xaa`'s actual validation now uses the lightweight divider from the
entry above instead, which draws only ~275µA — nowhere near the 276mA
nominal design point, so it doesn't confirm the PSU can *deliver* that
current, only that the Schottky is oriented correctly and the rail is
live. If a future session needs to confirm the full-current operating
point for real, that still needs an actual physical load sized correctly
for its wattage (see the "2s2p bank" technique in the `fuse_test_voltmeter`
entry above) — not yet done for any AA-tier PSU in this repo.

**General lesson**: when a PSU's `.spice` netlist and `smoke_test.py`
already flag `Rload` as simulated-only, grep every sibling `breadboard.md`/
`README.md` for that same numeric value before trusting its prose is
consistent — a "with an N Ω load..." sentence in an "Expected behavior"
section reads as a build instruction to someone mid-build even when the
author meant it purely descriptively, unless it's flagged as explicitly
as `psu_ultralow_v1`'s already is.

## `psu_4xaa` gained an optional power switch, wired directly in the battery return leg — a genuine power-path break, unlike `fuse_test_voltmeter`'s signal-only arm switch (2026-09-06)

The user added a slide switch to their physical `psu_4xaa` build (visible
in `breadboard.jpg`) that wasn't in the original `breadboard.md`; they like having a power switch
on their PSUs. Documented as an optional § 5 in
`power_supplies/psu_4xaa/breadboard.md`: switch common (pin 2) in series
between holder 4 (−) and the ground rail, pin 1 to the ground rail, pin 3
left unconnected. Unlike the `fuse_test_voltmeter` arm switch (GP15,
signal-only, deliberately *not* in the power path — see that entry
above), this switch's whole purpose *is* to interrupt the power path, so
the "don't put a switch in the sense loop" caution from that entry doesn't
apply here — there's no sense loop, just an on/off break. If the user adds
the same switch to other AA-tier PSUs (`psu_low_v2`, `psu_3xaa`) later,
replicate this same placement (return leg, not the positive rail) rather
than re-deriving it.

## The user doesn't own or use a multimeter — every "confirm with a multimeter" doc instruction needs a Pico-circuit substitute, not a caveat (found 2026-09-05)

`cd4066_switch_tester/README.md`'s troubleshooting checklist (items 1 and
4, added 2026-08-28) told the reader to "confirm with a multimeter" for
two continuity checks (VSS pin 6 → GND, and power-rail continuity across a
possibly-split breadboard). The user pointed out they don't use a
multimeter at all — every voltage/current/resistance measurement on this
bench already goes through a Pico circuit with output routed to console/
log (same "Pico-as-instrument" philosophy as `fuse_test_voltmeter`'s own
"There's no multimeter in the loop" validation section). Fixed by naming
[resistance_measurement](../../measurement_tools/resistance_measurement/)
specifically in both checklist items instead of the word "multimeter":
its `R_x` leg and GND return get clipped directly onto the same two nodes
a multimeter's continuity probe would touch (pin 6 + Pico GND for item 1;
the two suspect rail segments for item 4), non-invasively and in parallel
with whatever's already wired — a near-0Ω reading is continuity, "Circuit
Open" is a break. This works because `resistance_measurement` already
exists in the repo for exactly this "measure an unknown resistance
without a multimeter" purpose (it was originally built to characterize a
jumper-wire chain for `ammeter_1ohm`'s shunt) — no new circuit was needed.

General rule for any future doc edit here: when text says "check/confirm
with a multimeter," don't just soften the wording — replace it with a
specific existing circuit in `measurement_tools/` (or say what a new one
would need to measure) that produces the same console-loggable result.
The three circuits available for this today: `fuse_test_voltmeter`
(voltage across two points), `ammeter_1ohm`/`ammeter_10ohm` (current
through a shunt), `resistance_measurement` (resistance/continuity of an
unknown two-terminal element via a known-resistor divider). If a future
check needs something none of these three actually measure (e.g. AC
frequency, capacitance), that's a gap to name explicitly rather than
reflexively pointing at `resistance_measurement` because it's the closest
existing fit.

## `psu_4xaa` real-hardware validation run (2026-09-06): wrong script run, and the raw voltage doesn't validate either — still "designed, not built"

The user built `psu_4xaa`'s validation divider (two 10 kΩ resistors,
midpoint to GP26) and ran `measurement_tools/resistance_measurement/main.py`
against it (`mpremote run main.py` from inside that folder), reading
~0.017 V / ~0.051 Ω with the pack disconnected and ~0.143 V / ~0.454 Ω
powered. Two separate problems, not one:

1. **Wrong tool, ambiguous doc pointer.** `psu_4xaa/README.md`'s
   Validation section said to read GP26 "with the same ADC-averaging
   approach as `measurement_tools/resistance_measurement`" — meant as
   "reuse the oversample-and-average *technique*," but read (reasonably)
   as "run that script." `resistance_measurement/main.py` assumes a
   completely different circuit: an *unknown* resistor forming a divider
   against a *known* 10 Ω reference, fed from the Pico's own 3V3 rail (see
   the "measuring an unknown low resistance" entry above). `psu_4xaa`'s
   divider has two *known* 10 kΩ resistors and is fed by the PSU's own
   output, not 3V3 — nothing for that script's `R_x = R_REF * (V_out /
   (V_in - V_out))` formula to solve for, so its printed "Resistance"
   column is meaningless here. Its "Measured Voltage" column is still a
   real, correctly-computed GP26 voltage regardless of circuit (`main.py`
   does a plain `avg_raw/65535*3.3` ADC conversion, independent of the
   R_x math printed alongside it) — that part of the output is trustworthy.
   Fixed `psu_4xaa/README.md`'s Validation section (2026-09-06) to say
   this explicitly and to stop pointing at the script itself.

2. **The trustworthy number still doesn't validate.** Expected GP26 ≈
   2.75 V for correct polarity (half of the PSU's ~5.5 V output through a
   1:1 divider) or ≈ 0 V for reversed polarity (Schottky blocks). The
   actual powered reading, ~0.143 V, matches neither — it's much closer to
   the "reversed/blocked" ~0 V case than to ~2.75 V, but isn't a clean
   match for that either. This is not just the wrong-script confusion;
   even the correct raw-voltage number says something in the physical
   build isn't delivering the expected output. Don't mark `psu_4xaa` built
   (`lab/README.md`'s circuits table already has it correctly as "designed,
   not built") on the strength of this run — the divider circuit itself
   was confirmed present (something changes between power-off and
   power-on), but the PSU's actual output voltage has not been confirmed
   in range.
   Untested next steps for whoever picks this back up: verify the two
   "10 kΩ" resistors are actually 10 kΩ and verify continuity along the
   4-cell series chain + Schottky + polyfuse, using `resistance_measurement`
   in its *actual* intended mode this time (clip its own R_x leg + GND
   return across each suspect node pair) rather than repeating the
   mismatched-circuit run above; also worth open-circuit-probing the
   battery pack directly (bypassing Schottky/fuse) — a fresh alkaline
   pack should rest noticeably above its nominal per-cell voltage with
   nothing loading it, while a NiMH-chemistry or weak/miswired pack reads
   low — in case the cells themselves are weak/miswired.

3. **Ground wire.** The user also reported the circuit "didn't start
   working at all" until they added a wire from the PSU's ground rail to
   Pico GND. That connection *was* already in `README.md`'s Validation
   ASCII diagram (last line, "Pico GND (Pin 28)") — it just wasn't
   restated as an explicit step anywhere `breadboard.md` itself covers,
   and the diagram alone was easy to miss mid-build. Same class of gap as
   the `RloadB`/`voltage_reference_lm358` entry above (a doc references a
   connection in one place but not in the step-by-step a bench user
   actually follows). Added an explicit "this wire is required, not
   optional" callout directly under the diagram in `README.md`
   (2026-09-06) rather than moving the diagram itself — general lesson
   still holds: when a circuit's physical build steps live in
   `breadboard.md` but a follow-on check (validation, demo) lives in
   `README.md` instead, don't assume a diagram in the second file is
   enough on its own; call out anything load-bearing in prose too.

## Never write `vscode-webview://` links into any doc, including `history.md` (found 2026-09-07)

A prior session's `history.md` entries (around 2026-09-06,
~line 3799-3818 as of this writing) linked to files using
`vscode-webview://<session-id>/...` URIs — these only resolve inside that
specific IDE webview instance at the time they were generated; the user
confirmed they show "Unable to open/resolve resource" every time, in any
later session. Per the append-only-log convention elsewhere in this file,
those specific already-committed `history.md` entries were **not**
rewritten (same treatment as other stale-but-historical content there) —
but no future entry, in `history.md` or anywhere else, should ever use
this URI scheme. When linking to a file for a human reader, use a plain
relative path (`power_supplies/psu_4xaa/README.md#validation`) exactly
like every other cross-reference in this repo already does — never
anything IDE-session-specific.

## `resistance_measurement` generalized from a one-off shunt-characterization jig to a reusable continuity/troubleshooting probe (2026-09-07)

Originally framed narrowly ("measure the jumper-chain shunt for
`ammeter_1ohm`"), and worded as "measure an unknown resistance without a
multimeter" — a framing the user explicitly rejected (see the "doesn't
own or use a multimeter" entry above): the circuit *is* the measurement
instrument here, not a workaround for lacking one, and describing it by
what's absent undersold what it actually does (a specific, digitally
loggable number, better suited to this bench than a handheld meter's
momentary display). Reworded `README.md`'s intro to describe it
positively, and added an explicit "Reuse: continuity/troubleshooting
checks on another circuit" section generalizing the existing
`R_ref`-known/`R_x`-unknown divider technique to *any* two-terminal node
pair, not just the original jumper chain — this is not a new circuit,
just documentation catching up to what the topology already supported.

Two things worth preserving if this gets reused again: (1) a circuit
being probed this way must have its own power source disconnected first
(battery pulled, PSU unplugged) — `resistance_measurement` drives the
node pair from the Pico's own 3V3 rail, and a second live source at the
same nodes fights it, producing meaningless readings and a possible
back-feed into the Pico's rail; (2) the computed "Ω" reading is only a
true linear resistance across an actual resistive part (wire, fuse,
switch contact) — across a diode (e.g. the 1N5817 Schottky used
throughout this repo's PSU tiers), the reading still usefully
distinguishes forward-biased/conducting from reverse-biased/blocked, but
isn't a real ohmic value, and documentation reusing this technique on a
diode should say so rather than imply a resistance measurement.

First concrete reuse: `psu_4xaa/README.md`'s new "Troubleshooting"
section (below) uses this to continuity-check the 4-cell AA chain,
Schottky, and polyfuse with the battery pack disconnected.

## `psu_4xaa` troubleshooting made concrete: a new `gp26_raw_voltage.py` script, plus a `README.md` § Troubleshooting with per-segment wiring/expected values (2026-09-07)

The prior session's `history.md` entry (2026-09-06, the "no --- don't
mark it built yet" one referenced above) left three follow-up
instructions vague enough to be unactionable on their own: "confirm the
two 10 kΩ resistors are actually 10 kΩ," "check continuity... using
`resistance_measurement` in its actual intended mode," and "re-read GP26
with a script that prints raw voltage only." The user correctly pushed
back that they'd followed the *existing* README instruction (adapt
`resistance_measurement`'s averaging technique) and then been told that
was the wrong script — the fault was in the instruction's ambiguity, not
the user's execution, and per explicit standing instruction ("if a new
script needs to be created, then create it") the fix is to actually build
the missing pieces, not just describe them more carefully in prose.

Created `power_supplies/psu_4xaa/gp26_raw_voltage.py` — the "print raw
voltage only, no `R_x` math" script the old README text gestured at but
never produced; it's now what `README.md`'s own § Validation points to
instead of the old "adapt `resistance_measurement`, but don't run it
unmodified" hedge. Added a `README.md` § Troubleshooting with an explicit
per-segment table (each AA-holder joint, the Schottky both directions,
the polyfuse) giving exactly what to clip `resistance_measurement`'s
leads to and what reading counts as pass/fail, plus a battery
open-circuit-voltage check that reuses the *same* 2×10 kΩ divider
hardware already built for § Validation (just re-clipped from the
polyfuse output to Holder 1(+) directly) rather than reaching for
`fuse_test_voltmeter` — that circuit's jig is scoped to its own
single-cell voltage range and has no divider in front of GP26, so it
isn't safe to wire across this pack's ~6 V. General lesson: when a
troubleshooting instruction says "use circuit X in its intended mode" or
"write a script that does Y," a future session should treat that as a
to-do, not a description already discharged by mentioning it — the user
has flagged this exact gap (vague-instead-of-actionable troubleshooting
steps) more than once now.

## `pico/docs/inventory.md` moved to `lab/docs/inventory.md` (2026-09-07) — `pico/` keeps a one-line pointer, doesn't lose the file

Per explicit user request (repo-switching friction from referencing
inventory items while working in `lab/`). This crosses the "README
cross-linking is one-directional: `lab/` → `pico/`, never back"
convention documented above — `pico/`'s own generic circuit BOMs
(`buttons/gpio_interrupt_button/bom.md`,
`displays/gpio_i2c_lcd/bom.md`, `leds/gpio_pwm_led/bom.md`) and its own
`README.md` reference the inventory too, unrelated to any `lab/`-specific
work. Resolved (user's explicit choice, offered as options): move the
real file to `lab/docs/inventory.md`, and leave `pico/docs/inventory.md`
as a one-line pointer back to it — `pico/`'s own links still resolve to
*a* file without requiring `lab/` to be cloned alongside it, they just
land on a stub instead of the full content if `lab/` genuinely isn't
present. Every other cross-reference to the old path, in both repos,
across READMEs/breadboard.md/smoke_test.py/orders.md/parts_reference.md/
this KB directory, was updated to the new relative path (see
`git log` around this date for the full file list — same "grep the whole
path string before considering a move done" discipline as the earlier
`fuse_test_voltmeter` folder-move entry above). `docs/history.md` in both
repos was deliberately left with old-path mentions in already-committed
entries, per the append-only-log convention.

The stub at `pico/docs/inventory.md` is **not** kept in sync
automatically — if `lab/docs/inventory.md` moves again, or the
relationship between the two repos changes, that stub needs a matching
update, and it's easy to forget precisely because it's rarely opened
once `lab/` is actually cloned alongside `pico/`.

## `gp26_raw_voltage.py` moved out of `psu_4xaa/` into its own `measurement_tools/raw_voltage_probe/` (2026-09-07)

The script created earlier the same day (see the "psu_4xaa troubleshooting
made concrete" entry above) had no `psu_4xaa`-specific logic at all — it's
a plain averaged-ADC-voltage-at-GP26 reader with no resistance math and no
divider assumptions, identical to what any future circuit would need for
a "what does GP26 actually see" check. The user pointed this out directly
and asked for it to live in its own reusable directory rather than being
fused to one circuit, same instinct as the general-purpose-repo-framing
preference recorded elsewhere. Moved to
`measurement_tools/raw_voltage_probe/main.py` (renamed to `main.py` to
match every other tool folder's convention — `resistance_measurement`,
`fuse_test_voltmeter`, `ammeter_10ohm`/`ammeter_1ohm` all use that
filename, not a circuit-specific one) with its own `README.md` explaining
how it differs from `resistance_measurement` (adds known-`R_ref` math) and
`fuse_test_voltmeter` (adds trip/reset logic).

Per the "moving a circuit into a category folder touches every
cross-reference" entry above, this touched: `psu_4xaa/README.md` (file
table, § Validation's script link + new power-source prerequisite note, §
Troubleshooting's link and new step 0), `lab/README.md` (built &
bench-tested table, repo-structure tree). `docs/history.md` was correctly
left alone (append-only, describes the repo as it was that session).
`docs/kb/repo_docs_conventions.md`'s own prior entry about the script's
creation was also left alone rather than edited in place — this entry
documents the subsequent move instead, so the chronological record shows
both steps rather than rewriting history.

## A ~0V divider reading is usually "no power reaching the divider," not a wiring fault — check this before deeper troubleshooting (established 2026-09-07)

The user ran `psu_4xaa`'s § Validation check (2×10kΩ divider off the PSU
output, expecting ~2.75V at GP26) and got ~0.017V — but had pulled the
battery pack out of its holders first, on the assumption that was part of
safely building the divider. With no power reaching the output, ~0V is
exactly what the divider *should* read; it isn't evidence of a wiring
fault, and sent the user down the § Troubleshooting continuity-check path
(steps 1–3) for a problem that doesn't exist. Fixed by adding a step 0 to
`psu_4xaa/README.md` § Troubleshooting ("confirm the battery pack is
actually installed and powered") ahead of the existing per-segment
continuity checks, plus an explicit prerequisite note in § Validation
itself. General lesson for any future circuit's own Troubleshooting
section that starts from a Pico-ADC divider reading: a reading pinned at
or near the Pico's own noise floor (well under a volt, not just "lower
than expected") is cheap to misdiagnose as a wiring fault when the far
more common cause is simply that the circuit under test isn't powered —
lead with a "confirm power is actually present" check before any
continuity/component-level debugging.

## `resistance_measurement`'s "unknown `R_x`" framing intentionally covers both real-resistance measurement and continuity-checking — not split into two tools (established 2026-09-07)

The user asked, while troubleshooting `psu_4xaa`, whether
`resistance_measurement/README.md`'s § Circuit (which frames `R_x` as "an
unknown resistance" being solved for) needed to be split into two
separate circuits/directories, since a continuity check (clipping onto
two nodes on another circuit, expecting "near-0Ω" or "Circuit Open," not
an actual ohms value to record) doesn't obviously fit that framing.
Decided against splitting: `main.py`'s two special-case branches ("Short
to GND or 0 Ohms" / "Circuit Open") already handle continuity-checking
using the exact same hardware, wiring, and formula as real-resistance
measurement — splitting would duplicate an identical circuit for zero
functional gain, working against the general-purpose/reuse framing
preference recorded elsewhere. Fixed instead by adding a clarifying
paragraph directly under § Circuit's divider-equation block, making
explicit that the diagram/equation describe the hardware, not every use
case, and that continuity-checking has no discrete component in the
`R_x` position at all — just two probed nodes. If a future session is
tempted to split this tool again, re-read that paragraph and the existing
§ "Reuse" section first; the "two use cases, one tool" framing is
deliberate, not an oversight.

## `psu_4xaa`'s ~0.14V fault (2026-09-11) was never traced to a component — it was the breadboard itself; rebuilding on a fresh board is a legitimate diagnostic step, not giving up

The user worked through `README.md` § Troubleshooting step 0's full
checklist on the original breadboard — all 4 cells reseated, power switch
confirmed ON, dupont jumpers reseated, Schottky reseated, Schottky
orientation independently re-confirmed correct (stripe/cathode away from
the battery pack) — and GP26 still read ~0.14V, essentially unchanged.
The polyfuse and both divider resistors were queued to reseat next but
never got to it: instead, the user built the identical circuit from
scratch on a second breadboard and it worked immediately (~1.9V, matching
the divider math). Root cause was never identified more precisely than
"something about the first breadboard" — no single swapped/reseated
component on it ever restored the reading.

Generalizes: for this repo's simple series-DC PSU circuits (battery
chain + diode + fuse + divider), if the § Troubleshooting-style
component-level checklist (cells, switch, diode reseat+orientation) is
exhausted and the fault persists, a full rebuild on a different physical
breadboard is a cheap, legitimate next diagnostic step — not a
"something else must be wrong" admission of defeat, and not something to
talk the user out of in favor of continuing to reseat individual parts.
Full-size and mini (SYB170) breadboards can have a bad row or a broken
mid-strip contact that silently kills continuity for an entire branch
while every individually-checked component still looks fine in isolation
— see also the existing "split power rails" caveat later in this file
(`cd4066_switch_tester` entries above) for the same underlying class of
breadboard-level (not component-level) fault. If a future session hits an
unresolved near-0V/near-open fault on any breadboard-built circuit here
after exhausting the obvious component checks, suggest trying a second
breadboard before escalating to more exotic hypotheses.

A cheap intermediate check worth reusing before a full rebuild: the user
also independently wired just 2 of the 4 battery holders in series,
probed directly (no divider) on yet another breadboard, and got ~2.98V —
matching 2×1.5V almost exactly. Testing a subset of a series battery
chain directly (raw, undivided) on a spare breadboard is a fast way to
confirm the cells/holders themselves are fine before concluding the fault
is elsewhere; it doesn't test the Schottky/fuse/divider, but it rules out
the battery pack cheaply.

## `psu_4xaa`'s § Validation divider is 10 kΩ + 5.1 kΩ, not the originally-designed two 10 kΩ — a deliberate, non-default choice, don't "fix" it back

As of 2026-09-11, `power_supplies/psu_4xaa/README.md` and `breadboard.md`
document a 10 kΩ (top leg, output side) + 5.1 kΩ (bottom leg, GND side)
divider for § Validation, giving a ≈0.338 ratio (not the clean 0.5 a
matched pair would give). This traces back to a suggestion from a
*different* chat session the user was running in parallel while
troubleshooting the ~0.14V fault above; when asked here whether to revert
to a matched 10 kΩ pair (matching every other divider-based validation
convention in this repo) or keep the asymmetric pair, the user explicitly
chose to keep it as-is — reasoning given was "less work." Both resistor
values are already in inventory (10 on hand each, see
`docs/inventory.md`), so this isn't a parts-availability constraint,
purely a preference to not re-touch a working build. Treat the 10 kΩ/5.1
kΩ pair as the current correct spec for this circuit's validation divider
going forward — don't propose reverting to two 10 kΩ for consistency's
sake alone; that would just be re-litigating a decision already made.

## `raw_voltage_probe`'s averaged reading can't confirm toggling — built `oscillation_probe` instead, and it caught a real divider fault on `ne555_astable`'s first bring-up (2026-09-12)

`raw_voltage_probe/main.py` averages 50 ADC samples spaced 1ms apart (a
50ms window) and prints one number. For any node oscillating faster than
a few Hz — like `ne555_astable`'s ~650Hz–2.9kHz output — that averaging
window spans many full periods, so the result collapses to a
duty-weighted mid-voltage that looks *identical* whether the node is
genuinely toggling or just stuck at that same fixed DC level (e.g. a
floating divider leg settling at some in-between voltage). `raw_voltage_probe`
alone cannot distinguish these two cases for any circuit whose output
swings faster than its own sampling cadence — this will recur for any
future oscillator/PWM/logic-toggle bring-up, not just this one.

Built [`measurement_tools/oscillation_probe`](../../measurement_tools/oscillation_probe/)
to fix this class of gap: it grabs `BURST_SAMPLES = 2000` raw ADC reads
back-to-back with no `sleep()` between them (~54ksps on real hardware),
then reports min/max/swing/avg plus a zero-crossing count about the
burst's own midpoint. A real toggling signal produces a large swing and
many crossings; a stuck DC level (even a "wrong" one) produces near-zero
swing and ~0 crossings. This is a direct instrument-vs-averaging
distinction, not a refinement of `raw_voltage_probe` — keep both tools
rather than merging them; `raw_voltage_probe` stays correct and simpler
for genuinely slow/DC signals (its actual use in `psu_4xaa`), and
`oscillation_probe` is the one to reach for whenever the question is
specifically "is this node actually toggling."

First real run, against `ne555_astable`'s bench build (`breadboard2.jpg`,
GP26 through the circuit's own 2:1 output divider per `breadboard.md`
§4): `min=0.000V max=3.300V avg=1.796V swing=3.300V`, 113 zero-crossings,
crude estimate ~1532 Hz. The zero-crossing count alone is unambiguous
proof of real oscillation (and the rough frequency lands inside this
build's documented 649Hz–2.9kHz trim range) — so the NE555 chip itself
passes its per-unit validation. But the *swing* value is a second,
independent finding: it's pinned at exactly 3.300V, this tool's own
`V_IN` constant and the Pico ADC's actual saturation voltage — not the
~2.75V the two-10kΩ divider should produce from a ~5.5V pin-3 swing. A
reading landing exactly on the ADC's own rail like this is a strong
signal the ADC is clipping, not measuring: the real node voltage is at or
above 3.3V. Most likely explanation for *this* circuit: the divider's
bottom leg (R2, from the R1/GP26 tap to GND) is missing, not seated, or
otherwise open, leaving GP26 fed through R1 alone with no path to ground
— see `oscillation_probe/README.md`'s "Reading the result" section,
which documents this exact `swing == V_IN` signature generically so a
future circuit hitting the same pattern doesn't need this specific
diagnosis re-derived. Not yet physically re-checked/fixed as of this
writing — `docs/TODO-arcticoder.md`'s `ne555_astable` entry has the
concrete next physical step (disconnect GP26, verify both divider
resistors are actually in series, re-probe expecting ~2.75-2.9V).

General lesson for any future circuit whose validation reads GP26 through
a resistor divider: a swing (or a single `raw_voltage_probe` reading)
landing at exactly `V_IN` (3.3V) or exactly 0V, rather than somewhere
inside the divider's predicted range, means the ADC saturated — treat
that as evidence the divider itself is broken (open leg, wrong
resistor, bad connection), not as "the source is at a rail" unless the
circuit's own design actually expects a rail-to-rail reading at that
specific probe point.

**Resolution, 2026-09-13:** the `ne555_astable` divider fault above was
finally isolated with `resistance_measurement`, per-leg, as the "Next
diagnostic step" suggested — and the actual cause was neither wiring nor
an open leg, but a **wrong-value resistor pulled from the wrong bin**:
R2 measured ~273Ω, and its color bands confirmed it was a 220Ω part, not
the intended 10kΩ. Two prior visual re-wires (series-pairing R1/R2,
bridging ground rails) didn't find this because both assumed the parts
themselves were correct and only the wiring topology was suspect — a
component-value check with an actual measurement tool caught what visual
inspection during the original build missed. **General lesson: when a
divider/reading fault survives a topology re-check, verify the actual
component *values* next with `resistance_measurement`, not just their
placement** — a resistor drawer mix-up looks identical to a wiring fault
in a divider-swing symptom, and band-reading by eye is exactly the kind
of check that's easy to get wrong under bench lighting/fatigue. This also
means quantities in `docs/inventory.md`'s Resistors table shouldn't be
treated as a guarantee that a given pulled part is the value its bin
says it is — see that file's 2026-09-13 caution note.

## `resistance_measurement` reconfigured to GP28/10kΩ for a second, concurrent role (2026-09-13)

Historically documented as a fixed 10Ω-reference/GP26 jig (built
2026-08-30 to characterize the `ammeter_1ohm` jumper-chain shunt, see the
entry above). On 2026-09-13 the user repurposed it to isolate the
`ne555_astable` divider fault above, and explicitly chose **GP28 instead
of GP26** and moved it onto its own, separate breadboard — reasoning
given directly: they didn't want to disturb the GP26 wiring
`oscillation_probe` already uses on the `ne555_astable`/`psu_4xaa` board,
so adding this jig on a different ADC pin and a different breadboard
means both tools can be used back-to-back without re-wiring either one.
`R_REF` was changed from `10.0` to `10000.0` to match a 10kΩ reference
resistor (matching the divider's own 10kΩ legs, since the immediate job
was measuring those same-value resistors).

**Bug caught in the same session:** at the point this conversation
picked up, the live `main.py` on disk had `R_REF = 0.1` — neither the
original 10.0 (10Ω) nor the intended 10000.0 (10kΩ) — apparently drifted
back to a stale value after the actual bench measurements (which produced
sane ~10kΩ and ~273Ω readings, only explainable if `R_REF` was actually
10000.0 *at the time those specific `mpremote run` invocations
happened*). Corrected back to `10000.0`. **General lesson: `main.py`'s
`adc`/`R_REF` constants for this jig are mutable bench state, not a fixed
spec** — before trusting or reasoning about a `resistance_measurement`
reading (past or future), check what the file's constants actually say
*now* rather than assuming they match either the tool's original design
or a value mentioned earlier in the same conversation. This tool is
reused across jobs (shunt characterization, continuity checks, divider
diagnosis) more than any other jig in this repo, so its config is the
most likely of any file here to be silently out of sync with the last
bench session's narrative.

## Wide/far-away breadboard photos are not enough to catch real wiring bugs by eye — expect closer-up photos going forward (2026-09-13)

`psu_4xaa`'s divider re-check (§ Validation in that circuit's README) was
reviewed here from `validation_breadboard.jpg`-style wide shots, which
didn't resolve individual leads/jumper endpoints clearly enough to catch
actual wiring issues that were present on the board. arcticoder found and
fixed those issues themselves, purely by inspecting the physical board,
and reported explicitly that the photos being too far away is the likely
reason a review here didn't catch them first. Going forward, expect
closer-up photos (see `psu_4xaa/validation_breadboard2.jpg` for the new
style) — but even those can still be too cluttered with tape/jumpers to
fully verify topology by eye alone (confirmed on that same photo: dense
tape wrapping and overlapping jumpers made it impossible to trace every
connection with confidence even at close range). Don't assert a wiring
fix is visually confirmed from a photo unless individual leads/terminals
are actually traceable in it — when in doubt, say the photo doesn't
resolve enough to confirm, rather than guessing. The measured
electrical result (a real `raw_voltage_probe` reading matching the
documented target) remains the actual source of truth for whether a
build is correct, not a visual read of any photo, close-up or not.

## 1N5817 diodes get individually tracked by a physical marker (curled legs + no tape = already used), not by count alone (2026-09-13)

The `psu_4xaa` bullet in `TODO-arcticoder.md`'s "1N5817 Schottky diodes"
item requires a per-unit forward-drop check (via the Pico-divider
technique in `psu_4xaa/README.md` § Validation) before a given physical
diode goes into `psu_low_v2` or `psu_3xaa` — but the batch has no printed
serial numbers, so "which diode was already checked" isn't otherwise
distinguishable. arcticoder's convention: the diode already installed and
measured in `psu_4xaa` has curled legs and its tape wrapping removed,
while every other 1N5817 in the batch is still straight-legged and taped.
When reasoning about which diode is validated vs. still-unchecked-spare in
future sessions, use this physical marker rather than assuming order/count
in the bin — and don't suggest re-taping or straightening the used one, since
that would erase the marker.
