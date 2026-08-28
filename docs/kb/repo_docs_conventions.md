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
