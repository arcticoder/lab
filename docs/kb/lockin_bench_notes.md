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

## Source side diagnosed: the `GP28` node is not SIG (2026-10-05, later)

User's `diagnose_gain.py` reading: signal off 5.2mV p-p, in phase 24.8mV,
net 19.7mV on the `GP28` node (design 3.3mV, so the "about 15mV" row);
`Rbias` read 1kΩ, `GP8`/`GP9` resistors 1MΩ. Session re-ran it with the rig
left plugged in (18.1mV) and probed further. All with the Pico's own pins:

- **Shape.** A 40-bin fold shows a clean square wave, about ±8.5mV, that flips
  with `GP9` against `GP8`. So the ripple is real, not an ADC artifact.
- **DC step** (pin held 0 then 1 for 1s each, 40000-sample means): 0.0–0.3mV
  for `GP8`, `GP9`, `GP6`; design 3.3, 3.3, 6.6mV. A connected 1MΩ would give
  more than 1V here, so no source reaches the node through a resistor.
- **Software-toggled step vs half-period:** 17mV from 217µs to 18ms, 10mV at
  74ms, about 0 at DC. Step response: 18–25mV decaying over about 20ms.
- **`GP28` pad pull as a current injector** (pad register
  `0x4001C000 + 4 + 28*4`, bit 3 pull-up, bit 2 pull-down; `ADC(28)` leaves
  the pad with pulls off, so writing the bits works and the original value
  is restored): rest 1.131V, pull-up +1998mV, pull-down −1062mV, relaxing back
  with about 0.25s time constant. With a 50–80kΩ pull, that is a node held by
  roughly 0.5–1MΩ. Design: 1kΩ, under 50mV. Reusable for any ADC pin: it
  turns an ADC pin into a "how firmly is this node held" probe without
  moving a lead.
- **Controls:** toggling `GP10`, `GP11` and the unwired `GP12` moves the node
  by 0mV, so it is not clock pickup or on-chip crosstalk. `GP6`'s 1kHz
  step (47mV) is 2.7× `GP8`'s, which tracks the number of resistors on it,
  not a clean resistance ratio.
- **What this rules out and what is open.** Resistor values are out (right
  parts, and a resistor path would pass DC). Not established: which row
  `GP28` is on. The photo's pencil labels show a `SIG` row on each side of the
  centre channel; the photo can't say which, or whether they are joined. A
  single consistent topology for the AC-only coupling was not found by
  reasoning; don't write one into the docs until the row-by-row check
  (`trace_node.py`, `breadboard.md`) says which strip differs.
- The gain stage itself is unverified: 18–20mV × 100 is about 2V, which would
  clip, matching X 1.1V, so nothing so far says it is wrong.
- Rejected on the way: capacitive pickup from stray coupling (a pF-scale
  stray gives well under 1mV here), and `Rbias` = 5.1kΩ (would still give a DC
  step).
