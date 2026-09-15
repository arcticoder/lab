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
   objective" — there is no in-repo objective to rank against; a
   dependency-graph grouping reason (e.g. "these are the spacetime-tier
   nodes") is fine to state, a priority claim on top of it is not.

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
