# KB: bench-photo diagnostics and failure-signature notes (2026-09-16)

Process notes for future LLM sessions triaging a "built it, tested it,
got a weird reading" report. Not end-user content — see
`repo_docs_conventions.md` for the kb/ vs docs/ split.

---

## Failure signature: a stable, small, stimulus-independent reading usually means "no power," not "wrong wiring"

`transimpedance_amplifier` (LM358 TIA, `psu_low_v2` rail) read
~0.380–0.384V under both ambient room light and a phone flashlight
pointed straight at the photodiode — no measurable difference at all
(2026-09-16, see that circuit's README § Validation for the full
numbers). The three failure modes its own README/breadboard.md already
listed (missing `Rf` → high/noisy open-loop reading; reversed
photodiode; unpowered LM358) don't all fit equally well: a missing
`Rf` or a reversed photodiode still leaves the circuit *responsive* to
light, just wrong in sign or magnitude or noisy. A perfectly flat,
small, non-zero reading regardless of stimulus is the signature of the
op-amp not receiving VCC at all — an unpowered op-amp sitting between a
live GND rail and a live ADC-sensed output pin can settle to a small
"phantom" voltage through its own internal ESD/leakage paths,
independent of what's happening at its inputs. **General heuristic for
this repo:** when a bench test of any op-amp circuit here (TL082,
LM358, etc.) comes back completely flat and insensitive to the input
stimulus, check the supply rail before suspecting the signal-path
wiring — especially when that rail (like `psu_low_v2` here) was
assembled but never independently validated before being pressed into
service powering the next circuit in the chain. Don't let the
downstream circuit's own troubleshooting list anchor the diagnosis if
none of its listed causes actually predict the observed symptom.

**Confirmed 2026-09-17 — the diagnosis was correct.** `psu_low_v2`'s own
GP26 divider check found its Schottky diode installed backward (see
below), and fixing it made `TIA` respond to light normally (~0.505–0.51V
ambient, ~0.72–0.78V flashlight — see that circuit's own README
§ Validation). Worth remembering as a validated pattern, not just a
hypothesis, for the next "stable + stimulus-independent" report on this
bench.

## A moving-but-narrow reading over a short sampling window is a real pass, not a stuck value — for a *deliberately non-phase-locked* design specifically

`phase_detector` (`PHASED`, tier4) is designed so its two square-wave
inputs (`ne555_astable`'s own oscillator and an independent Pico PWM
reference, see that circuit's README § Design notes) are **not**
phase-locked on purpose — the pass criterion is that the filtered output
*moves* over time as their relative phase drifts, not that it settles at
a specific voltage. 2026-09-19 bench run: `main.py` (0.2s between
20-sample reads) captured 0.871V–1.546V across ~17 prints, roughly 3.5s
of wall-clock time — a real ~0.67V swing, clearly not pinned, but far
short of the full ~0–3.3V range `README.md`/`breadboard.md` describe.
**Don't misread a narrow-but-moving band as a partial failure.** Two
free-running oscillators nominally at the same frequency drift in and
out of phase at a rate set by how close their actual frequencies are —
arbitrarily slow if they happen to be very close. A few seconds of
capture is nowhere near enough to guarantee catching a full sweep; it
only needs to show *some* real movement to confirm the XOR gate is
genuinely responding to relative phase rather than one input in
isolation. The diagnostic question for this specific design is binary —
did it move at all, yes/no — not "how much of the full range did it
cover in this one run." Only a value that's truly flat across the whole
capture (matching `README.md`'s own "if the reading sits pinned"
failure case) should trigger the voltage-margin/gate-power
troubleshooting steps in that circuit's own docs. This is a distinct
failure-signature class from the "flat reading = no power" heuristic
above — that one's about a circuit meant to hold a stable value; this
one's about a circuit meant to never hold still, where the only real
failure is *not* moving.

## Worn/illegible polarity markings on a reused part are a standing risk, not a one-off

Root cause of the above: the specific 1N5817 Schottky in `psu_low_v2`
has no legible cathode band (the paint wore off), so its orientation was
installed by guesswork — and the guess was wrong. This is a real risk
specific to this repo's ephemeral-circuit convention
(`circuit_lifecycle_and_repo_scope.md`): parts get pulled from a shared
bin and reinstalled repeatedly, and a marking that degrades over one or
more assembly cycles can't be trusted the next time, even if it was
legible originally. **When triaging a future power/orientation-shaped
symptom, ask whether the relevant diode/LED/electrolytic-cap's polarity
mark is still actually legible in the photo/description before trusting
"installed per the marking" as ruled out.** This specific unit's fix
was verified electrically (a divider check reading the expected target
voltage), not visually — that's the general pattern to reach for when a
marking can't be trusted: confirm orientation by the same kind of
divider/continuity check already documented for that circuit, rather
than re-inspecting the part by eye. See
`docs/parts_reference.md#1n5817-schottky-diode` for how this specific
unit is now flagged so a future session doesn't re-trust its band either.

## Photo-based breadboard verification: crop before trusting a `breadboard.md` diff against reality

When a user reports a bench result and attaches a `breadboard.jpg`,
it's worth actually zooming into it rather than taking the written
`breadboard.md` steps on faith — the two can diverge. Technique used
here: `PIL.Image.open(...).crop(box).save(...)`, then `Read` the
cropped file (the `Read` tool displays images). The photos are large
(3072×4080 in this case but displayed scaled down, e.g. to 1506×2000 or
2000×1000 — the tool result states the actual scale factor to multiply
displayed coordinates by), so a naive full-image glance misses small
components; crop tightly around the area of interest (2–4x zoom) to
read resistor color bands, diode band orientation, IC pin-1 dots, and
switch positions.

Doing this on `transimpedance_amplifier/breadboard.jpg` and
`psu_low_v2/breadboard.jpg` (2026-09-16) found a slide switch and a
small diode-looking component on the shared breadboard that **neither
circuit's `breadboard.md` documents** — they're presumably part of
`psu_low_v2`'s own build (a switch isn't in that file's wiring steps
either) or a leftover from a previous ephemeral build sharing the same
physical board (see `circuit_lifecycle_and_repo_scope.md` on shared
parts reuse across ephemeral builds). Couldn't determine from the
photo alone whether the switch is actually in series in the power path
or merely present on the board unconnected, or confirm its slide
position (on/off) with confidence — flagged it back to the user as
something to physically check rather than guessing. **General
lesson:** when a photo shows a component absent from the documented
wiring, say so explicitly and ask/flag rather than silently trust
either the photo interpretation or the written guide — breadboards
reused across ephemeral builds can carry over undocumented parts.

## Bare piezo disc soldering: needs flux, or it depoles/cracks before the joint takes

`charge_amplifier`'s 12mm piezo disc has no pre-attached leads (unlike
a piezo buzzer module) — this wasn't spelled out in
`charge_amplifier/breadboard.md` before 2026-09-16, which just said
"piezo lead" as if leads already existed. A fluxless soldering attempt
destroyed a unit: the ceramic disc's poor thermal conductivity means
solder won't wet without flux, which forces more heat/dwell time onto
the joint — long enough to crack the ceramic or depole the
piezoelectric layer before the joint takes. Fixed now in
`breadboard.md` and `parts_reference.md#piezo-element-12mm-disc`. Worth
carrying forward to any *other* bare piezo-disc handling in this repo
(there are 19 left in the batch) — this is a property of the part, not
specific to `CHGAMP`.
