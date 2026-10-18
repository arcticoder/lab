# KB: lockin_amplifier bench notes (2026-10-05)

For future LLM sessions. First wiring and run of `signal_conditioning/lockin_amplifier`,
done by the user with the rig left plugged in; the session ran probes over
`mpremote` afterwards.

## What the first run said

- `main.py` first run: `VB` low in every state (0.026V at `floor`, 0.14V low
  in phase); the next two runs were normal (floor 1.135V / 1.107V). Not
  explained; if it recurs, suspect `Cb` polarity or the `U2` pin 5/6 rows.
  Don't read a first-run `floor` failure as a design fault.
- Second run: structure right (sign flips, 90° near zero, 45° between),
  amplitude 4–5× the 0.26V design value (X +1.08V, anti-phase −1.39V),
  `VA`/`VB` swinging −0.77V/+0.34V and +0.60V/−0.78V. The asymmetry is the
  LM358 output stopping at about 1.8V and 0.02V (the sim's own model does
  the same), so a large X is clipped and the anti-phase/45° ratios fail with
  it. A fail list of ratio checks after an oversize in-phase X is one fault,
  not several.
- `main.py` now prints a pointer to `breadboard.md` § "Gain too high" when X
  is more than twice the upper limit.

## Duty sweep does not measure the gain

A narrow test pulse (2%–20% duty) was tried to get an unclipped slope. It
doesn't work: the LM358 at gain 91 has a closed-loop bandwidth near 10kHz
(about 35µs rise), so a 20µs pulse is attenuated by the amplifier before
anything clips, and a baseline that jumps by G·ΔV·d in the other direction
clips differently for in-phase and anti-phase pulses. Use a direct reading of
the node (`diagnose_gain.py`) instead.

## Suspects, in order

The measured factor is about 4.5–5×. Single-part errors that give it:
`Rbias` 5.1kΩ in place of 1kΩ (5.1×, and a 5.1kΩ `Rm2` is in the same build,
so the bin is in hand), `Rin` 2.2kΩ in place of 10kΩ (4.5×), a 220kΩ in place
of a 1MΩ source (4.5×). The kit's metal-film 1kΩ/10kΩ/100kΩ/1MΩ parts are all
`brown black black x brown`; the user's photos can't settle a band at
that angle. Clock pickup is ruled out as the main cause: the `floor` offset
was −28mV. Photos of this build: `breadboard-stage1..5.jpg`; stage 5 shows
the final wiring.

## Probe technique worth reusing

`diagnose_gain.py` samples one spare ADC pin (GP28) at MicroPython's
loop speed (about 30–40kSa/s), folds the samples modulo 1000µs (the PWM
clock and `ticks_us` share the crystal, so the fold is phase-stable) into 20
bins, and takes max−min of the bin means. On a floating GP28 it reads about
1mV p-p, so a 3.3mV signal and a 15mV signal are separable. `mpremote mount
. run script.py` lets a diagnostic `import main` from the circuit folder
without copying files to the Pico (and `main.py`'s `__main__` guard keeps it
from running on import). Tested on GP26, where the A average showed 0.5mV.

## Build-side answers from the user's report

- The 100nF across `S1`/`S2` can't span pins 14 and 7 (17.78mm); one leg goes
  in pin 14's row and the other in the nearest − rail hole. Now in
  `breadboard.md`.
- GP10/GP11 jumpers are about 100mm because the Pico shares the centre
  channel with the ICs; that length is acceptable (offset −28mV). Now in
  `breadboard.md`.

## The `GP28` row, and why the first probe read a "floating" node (2026-10-05 data, corrected 2026-10-17)

User's `diagnose_gain.py` reading on 2026-10-05: signal off 5.2mV p-p, in
phase 24.8mV, net 19.7mV on the `GP28` node (design 3.3mV); `Rbias` read as
1kΩ, `GP8`/`GP9` resistors 1MΩ. Session probes with the Pico's own pins
(`trace_node.py` is the reusable form) found: a clean 1kHz square of about
±8.5mV; 0.0–0.3mV DC steps from `GP8`/`GP9`/`GP6`; a step that decayed over
about 20ms; and a node that moved +2.0V/−1.1V under `GP28`'s internal pull-up
and pull-down and relaxed back in about 0.25s. The session read that as "`SIG`
is nearly floating, the wiring is wrong" and said so in chat and in the docs.
**That was wrong.** The user then gave the row numbers: the jumper was on row
50, and `SIG` is row 49 (left and right halves joined by a jumper), so the
probed node was the next row, `C2`:

- `C2` is `Cin`'s other lead; at 1kHz `Cin` is 159Ω against `Rin` = 10kΩ, so
  `C2` carries 98% of `SIG`'s ripple (17.3mV measured there, 16.4mV on `SIG`).
- DC is held at Vmid through `Rin` and the op-amp's virtual ground, so the
  sources' DC steps vanish; a slow step decays with `Rin`·`Cin` ≈ 10ms.
- The virtual ground only holds against about 1µA (`Rf` can supply
  (1.8V−1.1V)/1MΩ). A 50–80kΩ pad pull injects 20–35µA, so `C2` and `INN`
  look "soft" under that test. **Don't read a pull-test result on `C2`/`INN` as
  a floating node, and don't read "tens of mV" there as proof of a firm hold.**

On `SIG` itself (user, 2026-10-17): DC steps 31.7/32.1/63.5mV from `GP8`/`GP9`/
`GP6`, 1kHz step 16.4mV, `diagnose_gain.py` ripple 15.5mV. The DC step is
3.3V × R_hold / R_source, so R_hold is 9.7kΩ: the `Rbias` slot holds a 10kΩ.
With 10kΩ the netlist gives X = +1.057V (1kΩ gives 0.264V), against 1.08V
measured on 2026-10-05, and the 1kHz step is 10kΩ ∥ (Rin + Cin) = 5.0kΩ →
16.5mV, as measured. The part had been reported as 1kΩ; the kit's 1kΩ and 10kΩ differ only
in the fourth band, so a visual read can't separate them.

Lessons for future sessions:

- **Ask for the row number of a probe jumper before interpreting a probe**, or
  make the script say what the node should look like on each candidate row.
  The wrong-row reading was self-consistent and produced a plausible, wrong
  fault.
- **A measurement whose design value is far from the reading, with all named
  parts "right", points at a mis-read part before it points at wiring.** The DC
  step on the correct row read the resistance directly.
- A part reported as "1kΩ" without a meter reading is not a measurement.
  Keep `measurement_tools/resistance_measurement` as the arbiter for the 1k/10k
  pair; a bag holding both (`10K / 1K`) is a hazard (`inventory.md` § Storage).

## `VB` stuck, 2026-10-17

`main.py` on 2026-10-17 (rig idle for twelve days, `Rbias` still 10kΩ): `VB`
1.1715V in all seven states (±0.3mV), `VA` wandering 0.27–1.69V and drifting
down state to state. `demodprobe`-style test (S1 only, then S2 only, no
signal): with `S1` closed `A` settled to 1.131V and held it after `S1` opened;
with `S2` closed `B` stayed at 1.172V, the same as with `S2` open. So the
`S2`/`B` path was not connected (or `S2` never closed) and `A` was fine in DC.
On 2026-10-05 `VB` did move (+0.34V/−0.78V), except in the first run after
plugging in, when it read 0.026V: that early run was probably the same fault
appearing intermittently, a loose contact on the `B` side (suspects:
`GP11`→`S2` pin 13, `S2` pin 2→`Rb`, `Rb`→`B`, `Cb`, `U2` pins 5/6/7). The
S1/S2 chip swap in `breadboard.md` separates a bad chip switch from wiring.
`diagnose_demod.py` is the check; a test that compared A and B DC levels
instead was tried and dropped, because a dead `B` sitting at 1.172V and a
healthy one at 1.135V differ by less than the offsets the two channels have
(the 2026-10-05 floor read −28mV).
