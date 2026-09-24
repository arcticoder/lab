# active_current_limiter

An IRLZ44N MOSFET in series with a load's return path, a sense resistor,
and an LM358 comparator that cuts the MOSFET off above a 2A trip point.
This is the general-purpose `ACTIVELIM` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
— protection for `psu_medhigh`/`psu_high` (both backlog, no folder yet),
so this is designed and simulated ahead of either PSU actually existing.

---

## Files

| File | Purpose |
|------|---------|
| `active_current_limiter.spice` | ngspice netlist — closed-loop normal case + open-loop fault-detection case (see Design notes for why these are separate) |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`). Only draws the R elements; the switch/comparator model doesn't render |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

No `main.py` — like the PSU circuits, this is a passive protection stage
with no Pico-readable output of its own to stream.

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. MOSFET Drain → protected load; Source → sense resistor `Rs` (0.1Ω) →
   GND.
2. LM358 comparator, powered from 5V: inverting input on the sense node,
   non-inverting input on a reference from the TL431A divided down
   (0.2V for the 2A design point, 0.08V for the bench check), output to
   the MOSFET gate.

---

## Simulate

```bash
# from the repo root
ngspice -b protection/active_current_limiter/active_current_limiter.spice
```

```
--- ACTIVELIM Case 1 (normal, 12ohm load): load current, sense voltage, gate state ---
i_load = 9.876543e-01
v(3) = 9.876543e-02
v(4) = 3.500000e+00
--- ACTIVELIM Case 2 (fault-level 3A sense test): sense voltage, comparator decision ---
v(5) = 3.000000e-01
v(6) = 0.000000e+00
--- ACTIVELIM Case 3 (bench trip 0.08V): 0.625A no-trip sense/gate, 1.0A trip sense/gate ---
v(7) = 6.250000e-02
v(8) = 3.500000e+00
v(9) = 1.000000e-01
v(10) = 0.000000e+00
```

Case 3 is the bench-check reference setting described under Validation.

---

## Design notes

**Hard-trip (bang-bang), not linear foldback.** Two standard topologies
exist for an active current limiter: continuous linear foldback (the
MOSFET sits in its linear region, continuously throttled to hold current
right at the limit) and a hard trip (the MOSFET is either fully on or
fully off). This design is the simpler hard-trip version — deliberately,
for a first build: linear foldback requires the MOSFET to operate in a
continuously-variable resistance region, which needs either a real
transistor-level SPICE model or a proper analog control loop design;
this repo's existing convention models switching elements as ideal
two-state switches (see `ne555_astable.spice`'s discharge transistor),
which structurally can't represent a linear region at all.

**A real limitation the simulation itself surfaced: this design
chatters at the trip boundary.** Attempting to simulate a *sustained*
fault as a single closed-loop operating point (dropping `Rload` low
enough to force a trip, then re-running `.op` on the same closed
switch+comparator+sense-resistor loop) **fails to converge** in
ngspice — `Error: Transient op failed, timestep too small... trouble
with swmod-instance sfet`. This isn't a simulation bug to work around;
it reflects a genuine property of this topology: once the switch opens,
the sense voltage collapses toward 0V (no current flowing), which looks
like a perfectly safe condition to the comparator, so it immediately
tries to re-close — which immediately re-trips, and so on. A bang-bang
comparator with no hysteresis or memory has **no stable operating point
under a sustained fault** — in real hardware this manifests as rapid
oscillation (chattering) at the trip boundary, not a clean shutoff.
**This is why the fault case below is simulated open-loop instead**
(a fixed 3A test current through an isolated copy of the sense resistor,
checking only that the comparator's threshold decision is correct) —
asking the full closed loop to find a fixed point that doesn't exist
was the wrong thing to simulate, not a modeling gap to paper over.

**What would actually fix the chattering, if it matters for a real
build.** Either (a) add explicit hysteresis *and* a latch — some memory
element that keeps the gate off once tripped regardless of the
instantaneous sense reading, requiring a deliberate reset (power-cycle
or a manual button) to re-arm — or (b) switch to true linear foldback,
which has a genuine stable equilibrium under fault (the MOSFET
continuously regulates to hold exactly the limit current, rather than
snapping fully off). Neither is implemented here; this first build is a
hard trip with a known chattering failure mode at the boundary, useful
for protecting against a clean short or a load that draws well above the
limit (where chattering happens fast enough to still meaningfully limit
average current) but not a substitute for a proper latching/foldback
design if this ends up guarding something sensitive.

**Reference voltage.** The `.spice` model uses ideal constants for the
comparator reference (0.2V for the design point, 0.08V for Case 3). The
real circuit derives them from the on-hand TL431A tied as a 2.495V
reference and divided down with kit resistors — `breadboard.md`'s
§ Reference divider has the resistor values for each setting and the
TL431A's minimum-cathode-current sizing.

**The LM358 runs from 5V, not 3.3V (corrected 2026-09-23).** An LM358's
output only pulls up to about Vcc − 1.5V. The first version of this
design powered it from 3.3V "to match Pico logic levels" and modeled the
output as a clean 0V/3.3V swing; on real silicon the gate would have
reached ~1.8V, at the IRLZ44N's 1–2V threshold and nowhere near fully on
(the MOSFET would sit in its resistive region and drop far more than the
0.05Ω the model assumes). On 5V it reaches ~3.5V, so the model's high
level is now 3.5V.

**Why 2A, and why an illustrative 12V supply.** 2A is a working choice
that leaves margin under the Lenovo 65W adapter's rated currents at
various PD voltage tiers (`psu_medhigh`'s intended source, per
`general_purpose_circuit_dependency.md`) while still meaningfully
protecting a downstream circuit from a fault well above normal load.
12V is a representative `psu_medhigh`-tier voltage for the simulation —
`psu_medhigh` itself has no folder/build yet, so this is designed ahead
of its actual supply, same as `transimpedance_amplifier` was designed
ahead of `psu_low_v2` being physically assembled.

**Why `HVPULSE` wasn't attempted alongside this, despite sharing the
same MOSFET.** `docs/TODO-agent.md` flags `HVPULSE` (tier7/8, high-
voltage pulse generation) as needing "a real safety design pass
(isolation, discharge paths, and a target figure above this bench's 50V
DC/30V AC numeric high-voltage threshold) before any netlist" — and
critically, nothing on this bench currently defines a target peak
voltage or energy for it (no HV source of any kind is in inventory; the
highest voltage anywhere on this bench is the Lenovo adapter's 20V, and
no PSU folder is built around that adapter yet either). Building
`ACTIVELIM` doesn't resolve that — it answers a different, lower-risk
question (protecting a `psu_medhigh`-class rail from overcurrent) and
uses the only IRLZ44N on hand in the process. Per this repo's ephemeral-
circuit convention, that MOSFET returns to inventory once this build's
bench check passes, so it isn't actually gone — a second unit would only
be needed if `HVPULSE` had to be physically assembled *at the same time*
as `ACTIVELIM`, which isn't the case (see
`docs/kb/circuit_lifecycle_and_repo_scope.md`). Ordering a second one
ahead of that is optional — see `docs/TODO-arcticoder.md`'s "Next
AliExpress order" for it noted as a future (not urgent) candidate.

---

## Validation

No `main.py` — validate with the Pico's own ADC read directly across the
circuit's existing sense resistor `Rs` (the MOSFET-Source/`Rs` junction —
`breadboard.md`'s § 2 sense node), the same technique
[resistance_measurement](../../measurement_tools/resistance_measurement/)
and the `ammeter_10ohm`/`ammeter_1ohm` jigs use for a known shunt: load
current = `V(sense node) / 0.1Ω`. Confirm that voltage stays under 0.2V
(2A × 0.1Ω) in normal operation, and that a deliberately excessive load
(a low-resistance short, well below what the intended downstream circuit
would ever draw) drives it to the 0.2V trip threshold and the gate
collapses toward 0V as the MOSFET cuts off. Expect chattering at the
boundary itself — see Design notes above — not a clean single trip
event.

**What the on-hand source can and can't do.** The Lenovo 65W adapter's
profiles are 5V/2A, 9V/2A, 15V/3A and 20V/3.25A, and it only outputs
above USB default once a PD sink board negotiates one (the PD trigger
board in `docs/TODO-arcticoder.md`'s "Next order"). Its 5V profile is
rated 2A — the same number as this circuit's trip point — so a 2A trip
can't be shown *exceeded* at 5V. The 15V profile can exceed 2A, but 15V
into a load that draws 2.5A is ~37W, well past any single resistor in the
power-resistor assortment (5W/10W), and a chattering limiter doesn't
help enough to matter.

**Bench check: scale the trip instead of the load.** Set the reference
divider to the "Bench check" row in `breadboard.md` (~0.08V, ~0.8A trip)
and use the PD trigger board's **5V** tap:

1. 8Ω (10W wirewound) as the load: draws 0.625A, below the trip point.
   The Pico ADC on the sense node reads ~0.0625V and the gate stays high.
2. 5Ω as the load: draws 1.0A, above the trip point. The sense node
   reads ~0.1V at the moment of trip and the gate drops.

Same comparator, MOSFET and sense resistor as the 2A design; only the
reference divider differs. Case 3 in the netlist and smoke test covers
these two loads. Expect chattering at the boundary itself, as above.

This validates the switching logic, not the 2A number: confirming the
real 2A trip needs a source that can push more than 2A into a load,
which nothing on this bench does at a wattage one resistor can take.
