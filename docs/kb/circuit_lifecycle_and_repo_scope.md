# KB: circuit lifecycle and repo scope boundary

Audience: future LLM sessions in this repo. Established 2026-09-14 from
explicit user correction after several docs (`TODO-agent.md`,
`TODO-arcticoder.md`, `inventory.md`, `parts_reference.md`,
`protection/active_current_limiter/README.md`/`breadboard.md`) drifted
from these three points. See also
[repo_docs_conventions.md](repo_docs_conventions.md) and
[todo_list_conventions.md](todo_list_conventions.md).

## Three distinct scope layers — don't conflate them

1. **Design / simulate / document** (`.spice`, `breadboard.md`,
   `smoke_test.py`, `README.md`, optionally `main.py`). Claude's job,
   tracked in `TODO-agent.md`, always in scope, no purchasing or hazard
   decision needed.
2. **Physical assembly + bench validation** — confirming a build matches
   its own README's expected behavior / smoke-test predictions on real
   hardware. The human's job, tracked in `TODO-arcticoder.md`. In scope
   for this repo, but see the ephemeral convention below — it's a
   one-time confirmation, not a standing installation.
3. **Actual research experiments** (the spacetime/FTL-travel work this
   bench ultimately supports) — **out of scope for this repo entirely**.
   They belong to a separate future repo. Never write text implying this
   repo "exists to build toward" or "is working on" the experiments
   themselves — it exists to build and validate the *equipment* the
   experiments will eventually use. Don't add urgency/prioritization
   language to a bench-work item because it's "closer to the real
   objective" — there is no in-repo objective to rank against that way.

   **Narrower than it first reads (revised 2026-09-17):** this only bars
   ranking by *narrative closeness to the outside research goal*.
   Ranking `TODO-arcticoder.md`'s "Ready to build now" bullets by
   mechanical dependency-graph facts — does finishing bullet A unblock
   bullet B on the same list, is A a real named prerequisite for the next
   design-ready node, is A already mid-attempt with a fix in hand — is
   fine and is now the standing convention for that section (see
   [todo_list_conventions.md](todo_list_conventions.md)'s 2026-09-17
   entry). The test: would the same ranking argument hold if this repo's
   downstream consumer were swapped for an unrelated one? If yes (it's
   about which node the graph shows gating which other node), it's a
   mechanical claim and it's fine to state and act on. If the argument
   only works by naming the FTL-research goal itself ("do this first
   because it's closer to solving X"), it's a narrative claim and stays
   out.

## Every circuit is ephemeral — parts are shared inventory, not permanent installs

Nothing gets left wired on a breadboard once its own bench check passes
and nothing else currently under construction needs it — see
`README.md` § Circuits — built & bench-tested. This means:

- **A part "consumed" by one circuit isn't gone** — it returns to
  `docs/inventory.md` once that circuit's own validation is done, and
  can be reused by the next circuit that needs one, unless two circuits
  genuinely need to be assembled *simultaneously* (e.g. two active loads
  running at once in a real experiment — which, per the scope boundary
  above, isn't something this repo does). Concrete resolved case
  (2026-09-14): `ACTIVELIM` and `HVPULSE` both want the single on-hand
  IRLZ44N MOSFET; docs previously said a second unit "would need
  ordering" before `HVPULSE` could proceed — wrong, since nothing
  requires both assembled at once. A second unit is optional, only
  worth ordering if the human wants both physically available
  concurrently.
- Don't write "no current downstream consumer, but build it anyway to
  have it ready for X" — that implies leaving it installed to feed a
  future stage, which contradicts the ephemeral convention. Bench-
  building something with no current consumer is for confirming the
  design against real hardware once; state it that way, not as staging
  inventory for later.
- A netlist/BOM for build-order and dependency-graph clarity does **not**
  imply a physical-assembly commitment or timeline — see the `HVPULSE`
  entry in `TODO-agent.md` for the precedent (numerically scoped and
  documented once a target figure exists, but not queued for physical
  assembly until the hazard-level decision below is made).

## This bench's numeric "high voltage" threshold

Established 2026-09-14: **above 50V DC / 30V AC RMS** counts as high
voltage on this bench — matches IEC 61140's SELV (safety extra-low
voltage) limit. Derivation: dry-skin resistance is commonly cited as
~100kΩ–600kΩ, but broken/damp-skin contact resistance can drop to
~1,000Ω; at 1,000Ω, 50V drives 50mA — inside the 30–50mA range that can
paralyze respiratory muscles, bordering the 50–100mA range that can
induce ventricular fibrillation. Standard household mains (120–240V AC)
is far past this threshold, hence "mains-adjacent" work is out of scope
without a real isolation/discharge-path design.

**Nothing on this bench currently exceeds 50V/30V.** The highest voltage
anywhere in inventory is the Lenovo 65W USB-C PD adapter's 20V rail
(`PSUMEDHIGH` node in `general_purpose_circuit_dependency.md`) — **no
PSU circuit folder is built around it yet**; `psu_medhigh`/`psu_high` are
both still backlog with no folder (see `TODO-arcticoder.md`'s Backlog
section). Don't imply an existing PSU uses the Lenovo adapter — none of
`psu_pico_rail`/`psu_ultralow_v1`/`psu_low_v2`/`psu_3xaa`/`psu_4xaa`/
`psu_medlow_usbc`/`psu_medlow_lm317` do; it's the adapter physically on
hand, reserved for whichever future PSU tier needs it.

**Practical consequence:** the human isn't prepared to increase the
hazard level of assembled circuits past this threshold until regularly
building/validating circuits that push the Lenovo adapter (or equivalent
amperage). Until then, don't queue physical assembly of anything above
50V/30V (`HVPULSE` included) in `TODO-arcticoder.md`, even once it has a
netlist — see the scope-layer distinction above.

## Resolved 2026-09-15: circuit selection now traces to literature, repo-scope boundary itself unchanged

The question below was raised and resolved same-day. **Resolution**: the
user chose to have Claude read the actual experimental-methodology
literature behind this kind of small-force/anomalous-thrust sensor kit
for real design justification (not just the tier graph's generic
labels), while keeping every current-state doc — README, dependency
graphs, **and kb prose** — free of any specific theory/program/researcher
name, per [[no_fringe_science_terms]] (which explicitly covers kb prose,
not just user-facing docs — don't relax that just because a kb file is
LLM-only). See `spacetime_circuits_dependency.md`'s "Why these tiers"
section for the sourced-but-unnamed rationale this produced, and
`spacetime_sensor_chain_notes.md`'s matching session-notes entry for the
literature-scan process to repeat on future passes.

**What did NOT change**: the three-layer scope split below (design/
bench-validate/actual-experiments-elsewhere) stands as originally
established 2026-09-14 — this only added a sourced justification layer
on *why* a tier5/7/8 node exists, not a change to what's in-scope to
build here. The friction that started this was partly a documentation-
clarity bug ("no current downstream consumer" reading as "no purpose" —
see `todo_list_conventions.md`'s entry) and partly a genuine desire for
deeper grounding, which this literature pass addresses without touching
the scope boundary itself.

<details>
<summary>Original open-question entry (2026-09-15, kept for context)</summary>

## Open question as of 2026-09-15: does this scope boundary still hold?

The three-layer split above was established 2026-09-14 at the user's own
explicit, heated request — quoted directly in this file's own history.
One day later (2026-09-15), the user pushed back hard on the *result* of
that same decision: seeing "no current downstream consumer" attached to
`EPFIELD`/`CHGAMP` in `TODO-arcticoder.md` (layer 2 items, per this
file), they asked "why am I building them then? Are we doing spacetime
research or not?" and floated requiring a literature/preprint-backed
research question to justify a circuit before it gets designed at all —
which would mean layer 3 (the actual research question) starting to
reach back into what layers 1-2 are allowed to do, the opposite
direction from how this file currently draws the boundary.

**Don't read this as the boundary being wrong or already reversed.**
Two things are true at once: (a) part of the 2026-09-15 friction was a
documentation-clarity bug, not a scope problem — see
[todo_list_conventions.md](todo_list_conventions.md)'s new entry on "no
current downstream consumer" reading as "no purpose" out of context,
when `EPFIELD`/`CHGAMP` already have a stated purpose (named tier5 nodes
in `spacetime_circuits_dependency.md`) independent of whether tier6
exists yet; (b) the deeper question — should circuit *selection/design*
require an explicit research-question trace before it happens, rather
than working forward from the general tier graph — is a real, open
question about how this repo should run, not something Claude should
resolve unilaterally in either direction. As of this writing the session
that surfaced this asked the user to clarify rather than assuming an
answer; check `docs/history.md` and this file's own future entries for
which way it was actually resolved before assuming the 2026-09-14 scope
still holds unmodified, or that it's been replaced.

**If the answer turns out to be "yes, trace forward from research
questions"**: that likely means revisiting how `spacetime_circuits_
dependency.md` frames tier5/7/8 nodes (currently theory-agnostic by
design, see [[no_fringe_science_terms]]-equivalent constraint already in
that file's own header) — probably by naming the *class* of experimental
validation each node serves (e.g. "detecting a small quasi-static
electric field near a test article") without naming a specific theory,
rather than a wholesale reversal of the design/bench-only repo-scope
line itself. **If the answer is "no, the 2026-09-14 boundary stands"**:
the fix is just the documentation-wording one in
`todo_list_conventions.md` — no scope change needed at all.

</details>

## No multimeter — ever (recurring correction, see also [[instrument_not_absence_framing]])

The user does not own or use a handheld multimeter; every measurement on
this bench goes through a Pico circuit with loggable output. This
extends beyond the previously-recorded "don't frame a circuit as
'without a multimeter'" preference: **never suggest reaching for a
multimeter as a validation method at all**, even as an "or" alternative
next to a Pico-based technique (caught 2026-09-14 in
`protection/active_current_limiter/README.md`'s "validate by placing a
multimeter or [resistance_measurement]..." — the "multimeter or" framed
it as an available option, which it isn't). Always name the actual
Pico-based instrument and technique: which GPIO/ADC pin, which node,
what value confirms pass/fail. If the circuit already has its own sense
node (e.g. `ACTIVELIM`'s `Rs` sense resistor), read that node directly
with the Pico ADC rather than reaching for a separate measurement jig.
