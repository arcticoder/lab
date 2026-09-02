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

## AA battery holder leads: twisted bare jump wire + electrical tape is an accepted temporary termination, not a wiring defect (2026-08-28)

Ahead of the wire-stripper order (`pico/docs/inventory.md`) arriving, the
user terminated one AA battery holder's bare leads by twisting a
non-covered 0.25cm jump wire around each lead and wrapping the joint in
electrical tape — no soldering, no crimp, no Dupont connector. This was
confirmed electrically sound in an actual `psu_ultralow_v1`-shaped build
(battery + RXEF005 fuse + slide switch). Treat this construction as a
valid, intentional stand-in when reviewing this or similar breadboard
photos/wiring going forward — not as something to flag or suggest
re-wiring — until the leads get properly stripped and terminated to
Dupont connectors once the stripper/crimper tool arrives.

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

## `fuse_test_voltmeter` RXEF005 real-hardware run: sub-second self-clearing trips + below-predicted resting voltage read as PTC chattering near the trip threshold, not a fault (2026-08-28)

First real `mpremote run main.py` log on an actual RXEF005 (no deliberate
short applied) showed two `*** FUSE TRIPPED ***` events that each cleared
within 1–2 samples of the 0.2s `SAMPLE_INTERVAL_S` (first: 0.467V→0.210V
then reset, ~0.4s tripped; second: 0.476V then reset, ~0.2s tripped) —
nothing like the ~2 minute cool-down `breadboard.md`/`quickstart.md`
document. The resting (non-tripped) voltage also sat at ~1.04V for most of
the run, not the ~1.4V `quickstart.md`/SPICE predicts for a fresh 1.5V
cell across a cold fuse.

Working diagnosis (not independently instrumented/confirmed — no way to
separately measure fuse temperature or exact battery voltage on this
bench): both symptoms are consistent with the fuse chattering right at its
trip threshold rather than doing a single clean trip-and-latch. This jig's
own docs already establish that a plain 10 Ω load draws ~150mA on a 50mA
fuse (3x rated, see the "cold reading" entry above) — enough for a good
unit to self-trip from the resting load alone, with no short needed. If
the post-trip holding current is only marginally below what's needed to
keep the PTC element hot, it can partially cool, drop back into
conduction, reheat, and re-trip on a ~sub-second-to-second thermal time
constant — a real, documented PTC failure/near-threshold mode, distinct
from the full-latch case where remaining current is negligible and actual
room-temperature cooldown (the ~2 minute figure) is what's needed to
reset. The below-1.4V resting reading fits the same story: a fuse that
never truly returns to a cold baseline (still slightly warm/elevated in
resistance between chatter cycles) would read low exactly like this
without requiring the battery itself to be weak.

Consequence for interpreting future logs against this jig: a trip that
clears in under ~1s (a few samples at `SAMPLE_INTERVAL_S = 0.2`) without
the user having deliberately shorted and then released the load resistor
is *not* the same event as the documented short→trip→2min-cooldown→reset
cycle in `breadboard.md`/`README.md`'s "Expected behaviour" sections —
don't map log timestamps against the ~2 minute figure unless a deliberate
short was actually applied and removed. The deliberate-short test remains
the actual pass/fail signal (`breadboard.md` step 2 / `quickstart.md`
"Pass / fail"): a fuse that won't hold a trip for the full ~2 minutes
*after a genuine short* is a real fail; self-clearing chatter under the
plain resting 3x-rated load is a separate, expected-per-docs phenomenon
and shouldn't be read as a defect on its own. `quickstart.md` was updated
2026-08-28 with a short paragraph covering this, since it only had the
"may self-trip" half of the story (from `breadboard.md`) and nothing about
the fast self-clearing case.

## `fuse_test_voltmeter` second real-hardware run (different fuse, same day) weakens the "still-warm PTC" explanation for the sub-1.4V resting reading — battery chemistry is a better first hypothesis (2026-08-28)

The entry above hypothesized that the ~1.04V resting reading (vs. ~1.4V
predicted) was the fuse never fully returning to a cold baseline between
chatter cycles — plausible, but explicitly flagged there as unconfirmed
and only explaining *post-trip* low readings. A second run the same day,
with a fresh/different 50 mA fuse, showed the same ~1.0–1.08V resting
value from the *very first* sample — before any trip had occurred at all,
so there'd been no chance yet for the fuse to be pre-warmed by a prior
chatter cycle. The user also independently noted they'd now seen this on
two different physical fuses and didn't think it was fuse-specific. Two
independent units producing the identical below-prediction baseline from
a cold start points away from a fuse-specific PTC-memory effect and
toward something common to both trials instead — the battery, or the
loop's total series resistance.

Working hypothesis, not yet confirmed on this bench (no multimeter
available — see README.md "Validation" intro): 1.4V assumes a fresh 1.5V
alkaline cell with near-zero internal resistance. If the AA in the holder
is actually a 1.2V-nominal NiMH rechargeable, the same 10 Ω/cold-fuse
divider math predicts ~1.14V — already most of the ~1.0–1.08V observed gap
— with the remainder plausibly ordinary sag under the ~150 mA this load
draws (3x the fuse's rating; see the entries above). `quickstart.md`'s
troubleshooting section now suggests a cheap way to check this without a
meter: with ARMED off, move the GP26/GND probe jumpers directly onto the
battery holder's leads (bypassing fuse and resistor) to read open-circuit
voltage — ~1.5V is alkaline, ~1.2–1.3V is NiMH or a partly-discharged
cell. If a future session gets this diagnostic run, record the result
here and update/retire whichever hypothesis (still-warm PTC vs. battery
chemistry) it points away from — right now neither is confirmed, they're
just the two live candidates.

## `fuse_test_voltmeter` gained a GP15 arm/disarm switch (SPDT slide switch) to stop battery insertion/removal from reading as a false trip (2026-08-28)

The user's real-hardware runs kept ending with `*** FUSE TRIPPED ***`
printed at the very end of the log, from deliberately disconnecting the
battery to stop the test — a real trip and an intentional power-down are
indistinguishable to `main.py` purely from the voltage collapsing to
~0V, since both look identical on GP26. Fixed by adding a second,
independent GPIO input (GP15) wired to an SPDT slide switch: common (pin
2) to GP15, one throw (pin 1) to GND, the other throw (pin 3) to 3V3(OUT).
Because both throws are driven (never floating), no pull resistor is
needed and the pin always reads a definite HIGH (armed) or LOW (disarmed)
— this sidesteps the exact floating-input bug the deleted
`switch_pin_identifier` circuit hit (see the GND-reference entry above).

Design choice worth preserving: the switch is **not** wired into the
battery's power path (i.e., not in series with the fuse under test) —
it's a separate signal-only circuit read by a second GPIO. Putting it in
the power path would have added the switch's own contact resistance to
the very loop whose current/voltage this jig exists to characterize,
which would confound the fuse test it's supposed to validate. `main.py`
now gates trip/reset detection and the onboard LED on this ARMED state
(`armed` variable in `main()`); voltage still streams every cycle
regardless of ARMED/DISARMED, only the trip/reset print and LED are
suspended while disarmed. GP15 was picked because it's unused elsewhere
in this repo (GP14–16 were freed when `switch_pin_identifier` was deleted)
and sits next to a physical GND pin (pin 18, per the entry above) for a
short GND jumper run. If a future circuit here also needs a spare digital
input, check `main.py`/`breadboard.md` GPIO usage across the repo first —
there's no central pin-allocation table, just per-circuit docstrings.

One footgun worth flagging to a future session touching this circuit: if
the operator forgets to flip to ARMED before shorting the resistor during
an actual fuse test, the voltage collapse still happens and still prints
as a raw number, but `*** FUSE TRIPPED ***` and the LED won't fire —
easy to misread as "it didn't trip" when actually the switch was just
left in the wrong position. Both `breadboard.md` and `quickstart.md` now
call out sliding to ARMED once the circuit has settled, before the short
step, but there's no code-side safeguard against forgetting it.

## `fuse_test_voltmeter`'s arm switch: wiring both outer pins to GND *and* 3V3 was an unnecessary design — corrected to one throw + internal pull-down (2026-08-28)

**Supersedes the wiring rationale in the entry above** ("common (pin 2) to
GP15, one throw (pin 1) to GND, the other throw (pin 3) to 3V3(OUT)... no
pull resistor needed"). The user caught that this design permanently wires
both power rails onto the switch at once — the switch's own mechanism
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

## `fuse_test_voltmeter` bench setup grew a second slide switch *in the battery power path itself* — a new candidate confound distinct from the still-open battery-chemistry hypothesis (2026-08-28)

Neither `quickstart.md`/`breadboard.md` nor the two "sub-1.4V resting
voltage" kb entries above account for this: the user's physical bench now
has **two** slide switches, not one. GP15's arm/disarm switch is still
signal-only as designed (confirmed live via `mpremote connect /dev/ttyACM0
exec` — reads 0 with battery out, matches the physical position). The
second switch is the user's own addition, wired in series in the actual
battery → fuse → resistor loop, added deliberately so power doesn't reach
the circuit the instant the battery is seated (fine-grained control over
when the test starts). This is exactly the kind of thing the arm-switch
design rationale two entries above warned against doing *to that switch*
("putting it in the power path would have added the switch's own contact
resistance to the very loop whose current/voltage this jig exists to
characterize") — except here it's a second, separate switch the user
added on their own initiative, so that warning never reached them.

A run with both switches "on" and current flowing showed a steady,
non-chattering ~1.09V→1.085V resting reading, no trip/reset events at all
over ~26s. That's notably *more* stable/lower-current-looking than the
two prior logged runs (which at least self-tripped and chattered near
threshold) — consistent with additional series resistance (this switch's
contacts, on top of whatever the battery-chemistry hypothesis already
predicts) pushing the loop current further below the fuse's trip
threshold, not just closer to it.

Not yet confirmed which factor dominates (recommended next step, given to
the user: with ARMED off, move the GP26/GND probe jumpers directly onto
the battery holder's leads — bypassing fuse, resistor, *and* this power
switch — and read open-circuit voltage; this isolates battery chemistry
from switch/wiring resistance, and was already the standing diagnostic
from the entry above, still applicable here). If a future session gets
that result: record it here, and if the power switch turns out to be a
meaningful contributor, consider whether `quickstart.md`/`breadboard.md`
should explicitly warn against putting any user-added manual power switch
in-loop (same rationale as the existing arm-switch design note) rather
than only implicitly relying on the reader to generalize it themselves.

## `fuse_test_voltmeter` open-circuit diagnostic result: battery chemistry hypothesis ruled out, user's own power switch is the remaining suspect (resolved 2026-08-28)

The entry above's recommended diagnostic was run: GP26/GND jumpers moved
straight onto the AA battery holder's leads (fuse, resistor, and the
user's own in-loop power switch all bypassed), fresh battery, both
DISARMED and ARMED. Result: a steady **~1.605–1.608V**, settling from an
initial ~1.72V transient (contact-bounce as the jumpers were seated —
expected, not a fault; it's the same "unsteady reading during DISARMED
settling is expected" behavior the README already documents for the
normal fuse-loop case, just observed here in the open-circuit variant
instead).

This confirms alkaline, decisively — not NiMH (which would read
1.2–1.3V). ~1.6V is *higher* than the 1.5V nominal `quickstart.md`'s
troubleshooting section originally described as the alkaline-confirming
value, but that's expected: a fresh cell with literally nothing loading it
(the Pico's ADC input draws negligible current) commonly rests somewhat
above its 1.5V nominal — the 1.4V figure elsewhere in the docs already
assumes the 10Ω *loaded* case, not open-circuit. `quickstart.md` was
updated same-day to say "1.5–1.65V confirms alkaline" instead of "close to
1.5V", so a future >1.5V open-circuit reading isn't misread as suspicious.

Consequence: the battery-chemistry hypothesis from the two entries above
is now ruled out as the explanation for the earlier ~1.09V *in-loop*
reading (full battery → fuse → resistor → user's power switch path). With
a ~1.6V source and only cold-fuse + 10Ω-load resistance, the loaded
reading should track proportionally *above* the ~1.43V SPICE figure, not
land at ~1.09V — so the gap is real series resistance somewhere in the
loop that isn't accounted for in the netlist. The user's own
manually-added power switch (see the entry above — wired in series in the
actual power path, not signal-only like the GP15 arm switch) is the
leading remaining suspect, stacked on top of the fuse's own cold
resistance. Not yet isolated on its own (e.g. by comparing the loop
reading with that switch jumpered/bypassed vs. in-circuit) — if a future
session gets that comparison, record the result here. This is also a
concrete data point for the still-open question the entry above raised:
whether `quickstart.md`/`breadboard.md` should explicitly warn against
adding any manual power switch into the battery loop.

Also confirmed live via `mpremote connect /dev/ttyACM0 exec` while the
battery was physically removed (holder leads open, GP26/GND jumpers still
seated on them, both slide switches left "on"): the ADC read a **stable
~0.017V** across 10 samples (raw ~320–352/65535), not noisy/floating
garbage. Worth knowing for future sessions debugging a similarly
"disconnected" node on this bench: a GP26-class input wired only to a
short breadboard jumper stub, with no battery or other source attached,
apparently settles to a low, repeatable value here rather than picking up
ambient EMI — don't assume a small nonzero-but-stable reading on a
nominally floating pin proves an unintended connection exists; on this
bench it doesn't.

## `fuse_test_voltmeter` in-loop reading recovered to ~1.497V — the ~1.09V mystery from the entries above looks resolved (2026-08-28)

A later run (`mpremote run main.py`, full loop: battery → fuse → 10Ω
resistor, GP15 arm switch) showed a steady **~1.496–1.499V** in both the
`-- DISARMED --` and `-- ARMED --` phases, with the arm switch toggling
cleanly (both banner lines printed, unlike some earlier sessions where
`-- ARMED --` never appeared at all). No short was applied in this run,
so this is the cold/unloaded-by-short baseline only — the deliberate-short
trip/reset check from `quickstart.md` was not exercised.

This number lines up with the open-circuit finding two entries above: that
same battery rests at ~1.6V open-circuit (not the 1.5V nominal the SPICE
model assumes), so the loaded prediction scales up from ~1.43V to roughly
1.6/1.5 × 1.43 ≈ **1.53V** — ~1.497V observed is a close match, well
within plausible cold-fuse/contact-resistance variance. That closes the
gap that the "user's own power switch" entry above left open as the
leading unresolved suspect for the earlier ~1.09V reading.

The photo (`breadboard.jpg`) taken alongside this run shows only one
switch in the whole build — a small slide switch on the main breadboard
consistent with the 2-wire GP15 arm switch — with no second switch
visible in series with the fuse/resistor loop on the small red
breadboard. So the earlier "extra, undocumented power switch wired in
series with the fuse" (see the entry several above this one, describing
the breadboard photo where it was first spotted) appears to have been
removed from the physical build at some point between that session and
this one; nothing in the conversation log narrates the removal
explicitly, so treat this as inferred from the photo, not confirmed by
the user's own words. If a future session sees the ~1.09V-class low
reading recur, re-check for a stray switch or connector in the power
path before re-opening the battery-chemistry line of investigation, since
that one is now fairly well exhausted (open-circuit ~1.6V confirmed
alkaline twice).

Also re-confirmed live (`mpremote exec`, battery physically unplugged,
slide switch left "on"/armed): GP26 read a steady ~0.014–0.017V across 10
samples — the same low, repeatable floor documented in the entry above,
not new information, just reproduced on a later date with a different
mpremote invocation style (inline `exec` script vs. the connect+exec form
used previously).

**Still open:** the deliberate-short trip/reset test from `quickstart.md`
(bridge the resistor's two rows, expect `*** FUSE TRIPPED ***`, wait ~2
min, expect `*** fuse reset ***`) has not been run since the reading
recovered to ~1.497V. Until that passes, `fuse_test_voltmeter` should be
described as "wiring/voltage confirmed" rather than "fully passes its own
pass/fail criteria" — see `lab/README.md`'s built-&-bench-tested table,
which was updated 2026-08-28 to say exactly that rather than claiming a
full pass.

## `fuse_test_voltmeter` deliberate-short attempt (2026-08-28, later same day): resistor physically removed + jumper installed, but the loop never showed a short at all

User removed the 10Ω resistor entirely and seated a jumper across the same
two breadboard rows it had occupied (the intended equivalent of shorting
it — see the "hand-touching two bare leads" kb entry above, which is why a
seated jumper was used instead of hand contact). Sequence: DISARMED +
battery out → battery in → `mpremote run main.py` → switch to ARMED.
Logged output (`mpremote run main.py`, ~107 samples over ~21s): a smooth
monotonic climb from 1.360V → 1.386V during `-- DISARMED --`, continuing
to climb after `-- ARMED --` up to a 1.401–1.404V plateau. **No trip
message ever printed, and the reading never dropped below ~1.36V.**

This is diagnostic, not just "short didn't trip yet": a genuine 0Ω bridge
across the probe/ground nodes forces the ADC-probe voltage toward 0V
*immediately* via Ohm's law, before the fuse's PTC element has any time to
heat up and go high-Z — the collapse is supposed to be near-instant and is
independent of whether the fuse has tripped yet. The logged values instead
sit squarely in the normal *unshorted* cold-reading range this same
`quickstart.md` documents (~1.4V, see the entry above), with a shape (slow
climb then plateau) that looks like ordinary battery-settling after
insertion, not a shorted node. Conclusion: **the shorting jumper was not
actually completing a low-resistance bridge between the two rows during
this run** — most likely seated in the wrong rows (off by one from where
the resistor's legs actually landed) or making poor/partial contact,
rather than any deliberate-short logic problem in `main.py` or a fuse
fault. This is a *different* failure mode from the resistance-based
"~1.0–1.1V" confound investigated in the entries above (that was about a
loaded-but-real path with extra series resistance; this is about a
shorting path that doesn't appear to exist electrically at all).

Also re-confirmed live during this session, after the user removed the
battery again and left the arm switch "on" (`mpremote connect /dev/ttyACM0
exec`, 10 samples): steady **~0.017V**, matching the established
no-source floor from the entries above exactly. This isolates the fault
to the shorting jumper specifically — the Pico-side GP26/GND/GP15 wiring
and firmware are behaving exactly as previously validated, both before and
after the anomalous run.

**Recommended next step for a future session or the user**: reseat the
shorting jumper, double-checking it lands in the *exact* two rows the
resistor's legs occupied (not an adjacent row), with battery in and
switch ARMED; expect a near-instant collapse toward 0V and `*** FUSE
TRIPPED ***` within a second or two of seating it, not a gradual change.
If it still doesn't collapse, suspect the jumper wire itself (bad crimp/
broken conductor) over the breadboard rows. Until this passes,
`fuse_test_voltmeter`'s pass/fail criteria per its own `quickstart.md`
remain unmet — don't upgrade the `lab/README.md` bench-tested note past
"wiring/voltage confirmed" on the basis of this run.

## `fuse_test_voltmeter` rewire (fuse moved straight onto the power rail, extra jumper/power wire removed) — baseline re-confirmed, short test still not attempted (2026-08-28, later same day)

User removed the jumper and the additional power wire that had been
routing to the fuse and instead seated the fuse's leg directly in the
power rail (`breadboard.jpg` updated to match). This is a wiring
simplification, not the shorting-jumper fix recommended in the entry
immediately above — no short was applied in this run either; the
resistor was still in circuit, untouched.

Sequence: DISARMED + battery out → battery in → `mpremote run main.py` →
switch to ARMED partway through. Logged output: `-- DISARMED --` settled
around 1.33–1.34V, dipped to ~0.95–1.2V for a handful of samples right at
the switch-flip transition (consistent with physical handling/contact
noise from flipping the slide switch, not a new symptom), then
`-- ARMED --` began at 0.954V and climbed smoothly over ~150 samples
(~30s at the 0.2s sample interval) to a **~1.384–1.386V plateau**, still
inching upward at the last logged samples. No `TRIPPED`/`reset` message
printed anywhere in the log.

This is the same slow-climb-then-plateau shape documented in the
deliberate-short-attempt entry above (there it topped out ~1.401–1.404V)
and is consistent with ordinary battery-settling behavior after
insertion/handling, not a short and not a fault — see that entry's
reasoning for why a real short would collapse the reading near-instantly
instead. The ~1.384–1.386V plateau itself sits a bit below both the
~1.497V "resolved" baseline and the ~1.401–1.404V unshorted-attempt
plateau from the entries above; the spread across all three runs
(1.36–1.50V) is within the contact-resistance/battery-settling variance
already established for this jig, not evidence the rewire changed
anything electrically.

Also re-confirmed live (`mpremote exec` against `/dev/ttyACM0`, battery
physically unplugged, arm switch left "on"): GP26 steady at
**~0.016–0.018V** across 5 samples, matching the established no-source
floor exactly — the Pico-side wiring/firmware is unaffected by the fuse
rewire.

**Still open, unchanged from the entry above**: the deliberate-short
trip/reset test has still not been exercised on this build — this run
didn't touch the resistor or attempt a bridge at all, it only confirmed
the cold baseline survived the fuse-to-rail simplification. Moving the
fuse directly onto the rail does remove one jumper's worth of contact
resistance from the loop, which may make a subsequent short attempt more
likely to succeed if the earlier inconclusive attempt really was a
seating/contact issue as suspected — worth trying the short again now
that this simplification is in place, per the "reseat the shorting
jumper" guidance above.

## `fuse_test_voltmeter` resistor removal breaks trip detection, not just adds load — and the "still in circuit" claim about `breadboard.jpg` in the entry above was never actually re-verified against the image (2026-08-28, later same day; kb entry written 2026-08-28 after being promised in `history.md:3500` and dropped for one session)

The user physically removed the 10Ω resistor entirely and wired the fuse's
far leg straight onto the battery-minus rail (a jumper across where the
resistor used to sit). Per [main.py](../../measurement_tools/fuse_test_voltmeter/main.py#L8-L11),
GP26 probes the fuse's far leg and GND probes the resistor's far leg — the
resistor is what makes those two distinct nodes. With it gone, they're the
same physical node, wired straight to battery-. That node reads ~0V by
definition regardless of whether the fuse is intact or tripped: there's no
longer a divider for the ADC to see across. `LOW_VOLTAGE = 0.5` in main.py
then reports permanent-trip unconditionally. **This is a structural
measurement gap, not a load/current issue** — no amount of re-running the
short test, reseating jumpers, or unplug/replug live-checks (which only
verify the Pico-side ADC/firmware floor, not the fuse) can produce a valid
trip/reset result on this wiring. The resistor needs to go back in
*somewhere*, or trip status needs to be read a different way (multimeter/
continuity check directly across the fuse), before this jig's pass/fail
criteria from `quickstart.md` mean anything again.

**Process failure worth flagging for future sessions**: the entry
immediately above this one (and `history.md:3487`) asserted the
`breadboard.jpg` committed at `a8de156` "explicitly left the 10Ω resistor
in place," and that assertion was carried forward as settled fact rather
than re-checked against the actual image each time it was cited. On
inspection (cropped/zoomed the actual file), the small red breadboard in
that photo shows only the polyfuse and jumper wires — no resistor is
visible in it at all. Whether the original claim was a misread of a blurry
photo or the resistor was already gone by that commit, the lesson is the
same: a claim about *what an image shows* is not safe to reuse
session-to-session without re-opening and re-looking at the file — it
should be re-verified every time it's load-bearing for a diagnosis, the
same way a code claim gets re-grepped rather than trusted from memory.

Also: the kb entry documenting this resistor-removal finding was promised
in `history.md:3500` ("I'll log this... unless you tell me otherwise") and
then not written — `git log -1 -- docs/history.md` showed the commit that
added that promise (`446ed0f`) touched only `docs/history.md`, not this
file. If a turn's summary says something was logged to this file, verify
it actually landed (`git diff`/`git log -1 -- <this file>`) before telling
the user it's done, rather than trusting the stated intent.

## Don't offer "get a multimeter" as an alternative to restoring the sense resistor — it's a false dichotomy that made the user (rightly) furious (2026-08-28)

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

## `fuse_test_voltmeter` first real TRIPPED→reset cycles with the resistor genuinely restored: recovery is fast (~15–25s) and plateaus below the confirmed baseline, not instant and not necessarily a fail yet (2026-08-28, later same day)

With the resistor back in place per the entry above and a shorting jumper
seated alongside it (bridging its two rows, per `quickstart.md`), the user
got two genuine `*** FUSE TRIPPED ***` → `*** fuse reset ***` cycles in one
`mpremote run main.py` log — the first time this jig has logged an actual
short-then-recover sequence rather than a false negative (wrong rows, see
two entries above) or a structural gap (resistor missing, see entry
above). Both cycles: reading held at ~0.016–0.02V while the jumper was
seated (indistinguishable from this jig's established no-source floor,
~0.014–0.018V — expected, since bridging the resistor pulls GP26 toward
GND directly regardless of the fuse's own state, per the "resistor is the
sensor" callout in `quickstart.md`), then on jumper removal `*** fuse
reset ***` printed immediately followed by a real, sample-by-sample climb
— 0.927V→1.096V over ~100 samples and 1.053V→~1.098V over ~90 samples
(both ~0.2s/sample) — not an instant square jump. The user's framing
("miracle superfuse that heals itself instantly") is the second time a
fast recovery has read as suspicious on this bench; the entries above
already cover cases where no short actually landed at all, this is the
first case with a real short and a real (if fast) recovery.

Two things distinguish this from a full documented trip-and-latch: the
recovery took ~15–25s, not the ~2 minute figure `quickstart.md`/`README.md`
give for a genuine latch-and-cool; and both plateaus (~1.096V, ~1.098V)
sit noticeably below this jig's own confirmed-good baseline with the same
alkaline battery (~1.497V, see the "resolved" entry above; ~1.4–1.5V
observed across three separate cold-baseline runs that same day). Working
read: the fuse warmed under the ~2A short enough to cross `LOW_VOLTAGE =
0.5` but didn't fully latch into a high-Z open state — a partial/marginal
trip, not the clean full trip the ~2 minute recovery figure assumes.
Not yet isolated whether the sub-baseline plateau is the fuse still
partway through cooling (would keep climbing given more idle time) or a
separate marginal-contact issue independent of the fuse (this bench has
hit stray series resistance before — see the "user's own power switch"
entry above, later resolved as unrelated). Recommended next step: after
the next reset, leave the circuit untouched for the full ~2 minutes and
see whether the reading keeps climbing toward ~1.4–1.5V (fuse still
recovering, consistent with a genuine-if-slow trip) or flatlines near
~1.09V (points to wiring/contact resistance, not the fuse). If a future
session gets that result, record it here — this determines whether
`quickstart.md`'s "if a fuse won't hold a trip for the full ~2 minutes,
that's a fail" criterion actually applies to this unit yet, or whether the
fast-recovery pattern needs to be re-tested with a wiring confound ruled
out first.

## `fuse_test_voltmeter`'s open trip/reset question was bypassed, not resolved — the user built current-measuring `ammeter_10ohm`/`ammeter_1ohm` instead and validated both fuse batches that way (2026-08-30)

Every entry above this one traces one long debugging thread on
`fuse_test_voltmeter`'s voltage-probe approach to detecting a polyfuse
trip, ending with the resistor-removal structural gap (still unfixed) and
an open question about whether a fast-but-real trip/reset cycle should
count as a pass. None of that thread was actually closed out. Instead, the
user built two new, separate jigs —
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
bug (resistor removed, probe/GND nodes collapsed to one node — see the
"resistor removal breaks trip detection" entry above) is **still
unfixed** and its own pass/fail criteria from `quickstart.md` have still
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
user instruction — "no point in keeping that updated, I was just curious
at one point"). It had three live referrers beyond `history.md` (which
was left alone, append-only-log treatment as usual): `lab/README.md`
(repo-structure tree + one prose mention), `docs/orders.md` (one
citation on the 3296 trimpot entry), `docs/parts_reference.md` (one
citation on the LM358 entry) — all three were edited to remove the
dangling reference rather than leaving a dead link. Before deleting a doc
like this, grep the whole repo for its filename, not just check whether
the user named specific referrers.
