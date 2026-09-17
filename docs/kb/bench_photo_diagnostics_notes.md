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
