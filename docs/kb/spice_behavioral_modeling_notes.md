# KB: ngspice behavioral-modeling gotchas (from `oscillators/ne555_astable/`)

Audience: future LLM sessions writing `.spice` netlists in this repo, not
the end user. Every existing netlist before this one only used passive
R/C/V/D elements (op-point + load sweep); `ne555_astable.spice` was the
first to need a dynamic bistable element (an oscillator needs actual
memory, not just a resistor network), which surfaced several ngspice
footguns worth not rediscovering.

## The first line of a `.spice` file is ALWAYS the title, never parsed as an element

Classic SPICE convention, easy to forget: line 1 of any netlist is the
circuit title, silently consumed regardless of content. A netlist that
opens directly with a component line (no title comment) loses that first
element entirely — the node it defined floats, and everything downstream
mysteriously reads 0V with no error. Every `.spice` file in this repo
already led with a comment line by convention, which is exactly why this
never bit anything until a throwaway scratch test skipped it. Always
open a `.spice` file with a one-line description, not a component.

## Comparator-with-hysteresis (Schmitt trigger / SR-latch-equivalent) via a self-referencing B-source

`ne555_astable.spice`'s `NE555_ASTABLE` subckt models the 555's internal
flip-flop with one line:

```
Bout OUT 0 V = (V(OUT) > 2.5) ? (V(CT) > 3.333 ? 0 : 5) : (V(CT) < 1.667 ? 5 : 0)
```

This works *specifically* because in astable mode the 555's TRIG and
THRESH pins are tied together (both = `CT` here) — the internal SR latch
collapses to a single comparator with hysteresis on that one node, which
is exactly what a self-referencing B-source (referencing its own output
`V(OUT)` in the same expression) computes: ngspice resolves it via
per-timestep Newton iteration and it converges to the correct latched
state. Don't reuse this exact trick for monostable/bistable 555 configs
or anything where TRIG and THRESH differ — that needs an actual two-input
SR latch (two cross-coupled self-referencing B-sources), not this
collapsed one-node form.

Thresholds are hardcoded as absolute volts (`2.5`, `3.333`, `1.667`) for
a `VCC=5` design — `.param`-driven substitution into a `.model` line or a
`.subckt` body silently failed ("Undefined parameter") in this ngspice
build when the param was declared outside the subckt; if a variable-VCC
version is ever needed, pass VCC in as a subckt terminal/parameter
properly rather than fighting global `.param` scoping into `.model`.

## `SW` (voltage-controlled switch) default polarity: closes when control > Vt

`ngspice`'s `SW` model closes (Ron) when the control-pin differential
voltage exceeds `Vt`, not the other way around. The 555's discharge
transistor needed to be ON (DISCH shorted to GND) when `OUT` is LOW —
the opposite polarity — so the subckt derives an inverted control node
(`Boutn = 5 - V(OUT)`) and drives the switch from that, rather than
trying to find an "active-low" switch model flag. Getting this backwards
doesn't error — it just produces a circuit that charges once and then
sits latched forever (the failure mode actually hit while developing
this netlist: capacitor charged straight to VCC and stayed there, since
the discharge path silently activated on the wrong phase).

## `i(Rname)` doesn't work for a plain resistor in transient; `@Rname[i]` looked right but isn't reliable here either

Plain resistors aren't currrent-tracked components in ngspice the way
voltage sources/inductors are, so `i(Ra)` fails outright ("no such vector
as 'i(ra)'"). The documented workaround, `@Ra[i]`, parses without error
but — for this specific B-source/switch-driven topology — returned a
single frozen value (the pre-transient DC operating point's current)
across the *entire* transient trace instead of a real per-timestep
trace: `MIN` and `MAX` measured over it came back identical. Not worth
debugging further for a value this cheap to get analytically instead —
`ne555_astable/smoke_test.py` computes the discharge-phase current as
`Vcc/(Ra+Ron)` directly in Python rather than pulling it from the sim.
If a future netlist genuinely needs a real simulated transient current
through a plain resistor, verify `@R[i]` against a known-good hand
calculation before trusting it, rather than assuming the probe works.

## Bias-point stepping (`gmin`/source stepping) warnings on this netlist are expected, not a regression to chase

Running `ne555_astable.spice` prints, twice:

```
Note: Starting dynamic gmin stepping
Warning: Dynamic gmin stepping failed
Note: Starting true gmin stepping
Warning: True gmin stepping failed
Note: Starting source stepping
Warning: source stepping failed
Note: Transient op started
Note: Transient op finished successfully
```

Confirmed by comparison against `psu_ultralow_v1.spice` (plain R/D/V
elements only, no behavioral sources): that netlist shows *none* of these
stepping attempts or warnings at all. So the failures are specific to
this netlist's `NE555_ASTABLE` subckt — its self-referencing `Bout`
ternary comparator and the `SW` voltage-controlled switch are both
discontinuous around their trip points, which is exactly the shape of
circuit gmin-stepping/source-stepping (both DC-continuation strategies
for finding an initial bias point) handle poorly. That's fine here
because this netlist only ever runs `tran` (no `.op`/`.dc` on its own) —
ngspice has a fourth strategy, "Transient op" (solving the initial point
by time-domain relaxation instead of DC continuation), which is what
actually succeeds each time (`Transient op finished successfully`), and
the resulting `freq_lo`/`duty_lo`/`freq_hi`/`duty_hi` measurements match
the analytic 555 astable formulas in the netlist header. Treat these
three-stepping-methods-fail-then-transient-op-succeeds warnings as
diagnostic noise specific to behavioral B-source/switch topologies, not
a sign the result is wrong — but if a *future* behavioral netlist prints
the stepping warnings *without* the subsequent `Transient op finished
successfully` line, that's a real unconverged bias point and the result
should not be trusted.

The two repeated "Initial Transient Solution" blocks are likewise
expected: this netlist runs `tran` twice on purpose (Rb=10k, then
`alter Rb = 2k`, then `tran` again — see the netlist's `.control`
section), and each `tran` invocation gets its own bias-point/stepping
attempt and its own "Initial Transient Solution" printout. Not a
duplicated analysis, and not something to collapse into one run — the
whole point is bounding both ends of the recommended trim range.

`Note: No compatibility mode selected!` is unrelated to any of the above
— it's ngspice's standard startup banner (no `.options`
HSPICE/PSPICE-style compatibility mode requested) and appears on every
single ngspice invocation in this repo, `psu_ultralow_v1.spice` included.
Purely informational, never a fault signal.

## `.meas ... TRIG <vec>=<val> ... TARG <vec>=<val>` syntax needs `VAL=`, not `=`, once both TRIG and TARG are present

`meas tran thigh TRIG v(out)=2.5 RISE=3 TARG v(out)=2.5 FALL=3` fails
("no such vector as 'v(out)=2.5'"); the working form separates the
vector from its threshold: `TRIG v(out) VAL=2.5 RISE=3 TARG v(out)
VAL=2.5 FALL=3`. The simpler single-threshold form (`meas tran t1 WHEN
v(out)=2.5 RISE=3`) does accept the inline `=val` shorthand — the
`VAL=` requirement is specific to the two-sided `TRIG`/`TARG` form.
