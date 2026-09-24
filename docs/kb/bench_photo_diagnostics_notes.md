# KB: bench-photo diagnostics and failure-signature notes (2026-09-16, updated 2026-09-21)

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

## A single wildly-implausible sample surrounded by physically-sane readings is a handling glitch, not a wiring fault

`thermal_monitor` (`THERM`) bench run, 2026-09-21: during a sustained
finger-pinch warming test, 27 of 28 `main.py` prints traced a smooth,
monotonic divider response (10362Ω→8106Ω, 24.2°C→29.8°C as the MF52AT
warmed). One print mid-sequence read 3.253V/698639Ω/−47.4°C — a
physically nonsensical value (an NTC can't produce a negative absolute
resistance-derived temperature this way; 698kΩ implies the MID node sat
almost at VCC, i.e. `Rntc` momentarily looked close to open-circuit) —
then the very next sample snapped back to a value consistent with the
ongoing warming trend. **Read this pattern as a single momentary contact
glitch, not a real excursion or a wiring defect**: `main.py` takes a
20-sample average per print but does nothing across prints (no
outlier rejection, no debounce), so one bad print means the divider's
MID node briefly saw a bad connection — physically plausible here
specifically because the test protocol is fingers pinching a
through-hole leaded component seated in loose breadboard rows, which is
exactly the kind of handling that can momentarily lift a lead. The
general diagnostic question: does the surrounding data tell a coherent
physical story except for one (or a few) isolated samples? If yes, don't
chase the outlier as a wiring bug — note it and move on. This is a
distinct failure-signature class from both entries above: not "flat +
insensitive" (no power) and not "narrow but moving" (a real, if small,
signal) — this is "one sample breaks continuity with its neighbors,"
which reads as a transient mechanical/contact event.

**Real consequence worth flagging, not fixing reflexively:** `main.py`
sets the alarm LED directly off each print's own reading
(`temp_c >= ALARM_THRESHOLD_C`), with no debounce across prints. This
run's glitch happened to read *cold* (harmless), but a same-class glitch
that read *hot* instead would have driven a spurious momentary alarm
trip with no wiring fault behind it. Worth a debounce/consecutive-reads
guard before this circuit is trusted as an unattended safety monitor
(not needed just to confirm the sensor path works, which this run
already did) — noted as an open, non-urgent item in `TODO-agent.md`
rather than fixed reflexively here, since it's a design choice (how many
consecutive over-threshold reads should it take?) not obviously implied
by the one glitch observed.

## Photo-based verification can't always distinguish a thermistor bead from a resistor, or confirm a lead is seated

Cropped `safety/thermal_monitor/breadboard.jpg` (2026-09-21, same
technique as the entry below) looking for the MF52AT thermistor
specifically. Found: the LED, its 220Ω current-limit resistor, and what
is presumably the second in-circuit resistor (`Rref`, 10kΩ) — both of
the latter are ordinary axial color-band resistors, visually
indistinguishable from each other in the photo. **No component
distinctly identifiable as the thermistor bead was found** — the MF52AT
is a small epoxy-dipped axial part that can look like a third resistor
at this photo's resolution, and one candidate lead (following the wire
that continues past the second resistor) appears in the crop to curl
off the edge of the breadboard into open air over the cutting mat,
rather than terminating in a populated hole. Given the electrical data
from the same session shows a clearly-intact, physically-responsive
divider (see the entry above), **the data is stronger evidence of correct
wiring at test time than this photo is evidence of a problem** — most
likely explanation is the photo was taken at a slightly different moment
than the `mpremote run main.py` capture (e.g. thermistor lead
momentarily freed for the finger-pinch handling described in that
session's own log). Flagged rather than resolved, per this file's
existing "say so explicitly" convention — don't silently assume the
photo is stale, but don't treat it as contradicting a data-backed PASS
either. Worth a fresh, deliberately-framed close-up photo next time this
circuit is reassembled, if a canonical wiring-reference image matters
more than it did for this pass.

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

## Failure signature: a near-zero, near-instant reading on an RC-timing circuit usually means a floating ADC node, not a code bug — and zooming into the photo can prove it

`capacitance_bridge` (2026-09-22 bench run, 33µF `Cx`) printed
`t63≈0.000–0.001s -> Cx≈0.00–0.01uF` on essentially every loop — three
orders of magnitude off the ~3.3s a 100kΩ×33µF RC should take. `main.py`
itself is correct (re-read line by line to confirm: discharge and charge
both poll correctly, threshold math is right). A reading that's wrong by
*that* much in the "too fast" direction, on a circuit whose whole design
is measuring elapsed time, points at a much smaller effective time
constant than intended — either the wrong `Rref` value, or (as here) the
ADC node not actually being driven through `Rref` at all, only picking up
whatever a floating high-impedance node happens to see (stray coupling
from the adjacent drive-pin lead, ADC leakage), which crosses either
threshold in far less than 1ms.

**The breadboard photo confirmed it, but only after cropping/zooming —
not from the full-frame image.** `Read`ing `breadboard.jpg` at full
frame shows a resistor and a capacitor near the Pico's pins with wires
converging on a plausible junction; at that resolution the wiring looks
right. Cropping progressively tighter with PIL (`Image.crop` + a 5–8×
resize, saved to the scratchpad dir, then `Read` again) on the resistor's
far lead specifically showed it terminating on the breadboard's plastic
center divider ridge — the raised strip between the two 5-hole blocks —
rather than in the metal-lined hole a few mm away where the ADC probe
wire and `Cx`'s positive lead were actually (correctly) seated. A lead
resting on that ridge looks, at a glance and especially compressed in a
full-frame photo, like it's "near" the junction; it makes zero electrical
contact. **General technique for this repo going forward**: when a
bench-photo diagnosis needs to confirm a *specific* lead-to-hole
connection (not just "is a component present"), don't rely on the
full-frame read — crop to just that lead's endpoint and resize up
several times before judging seated-vs-not. The full frame is enough to
identify parts and rough topology; it is not reliably enough resolution
to tell "seated in the hole" from "resting beside it."

**Don't conflate this with a `psu_medhigh`/`ACTIVELIM`-style sourcing
gap.** This is a one-off assembly mistake on an otherwise-correct design
(reseating the lead is the whole fix, no BOM/design change) — different
in kind from `ACTIVELIM`'s entry below, which is a genuine missing-part
blocker.

**Confirmed 2026-09-22 — the diagnosis was correct.** Reseating `Rref`'s
lead and swapping `Cx` for a 47µF (25V) unit gave three consecutive
readings (48.87µF/47.75µF/47.64µF) within the kit's ±20% tolerance of the
47µF nominal. `CAPBRIDGE` moved to `README.md`'s "built & bench-tested"
table. Same lesson as the `psu_low_v2`/`TIA` entry above: a floating-node
diagnosis reached from a photo crop is worth trusting and re-testing
against, not just a hypothesis to note and move past.

## `ACTIVELIM`'s real blocker is a missing current-capable *test source*, not `psu_medhigh` itself — don't conflate the two

`ACTIVELIM`'s own docs (`README.md`/`breadboard.md`) describe it as
protection for `psu_medhigh`/`psu_high`, "both backlog, no folder yet" —
worded in a way that reads like the build is blocked on those PSU tiers
existing. It isn't, and the distinction matters: `psu_medhigh` doesn't
need a `lab/power_supplies/` folder to exist as a source, because it's
just the Lenovo 65W USB-C PD adapter (already on hand, per
`docs/general_purpose_circuit_dependency.md`'s `PSUMEDHIGH` node) used
directly — no regulation circuit needed, only the *wall adapter itself*.

The real gap, confirmed 2026-09-22 by checking `docs/inventory.md` and
`docs/orders.md` for anything current-capable: **nothing on this bench
can currently push ≥2A into a load at any voltage**, which is what
`ACTIVELIM`'s bench validation (its README's own § Validation) actually
needs to find the real 2A trip point. The Lenovo adapter only outputs
above its 5V/1.5A-ish USB default once a PD sink controller IC (e.g.
CH224K, STUSB4500) negotiates a higher-power profile — none is on hand,
and the only USB-C breakout on the bench (`psu_medlow_usbc`'s `TYPE-C
Female Test Board`) is a passive pinout breakout with no PD silicon at
all. Even the bare 5V/default path isn't confirmed working yet
(`psu_medlow_usbc`'s own VBUS-comes-up check is still an open,
unactioned item). And separately, no power resistor rated for the
resulting wattage (tens of watts, depending on test voltage) is in
inventory — the resistors on hand are small-signal kit parts, not power
resistors.

**Don't rank `ACTIVELIM` as "ready to build now" again until a PD
trigger board and a suitable power resistor are actually received** —
see `docs/TODO-arcticoder.md`'s "Next order"/"Blocked" sections for the
two candidate parts identified for this. *Updated 2026-09-23:* the check
was re-planned around what those parts can actually do (5V tap, ~0.8A
scaled trip, 5Ω/8Ω loads) and the comparator stage itself changed (LM358
on 5V, TL431A pull-up 1kΩ) — see
`kb/inductance_accelerometer_actlim_design_notes.md`. The wiring in
`breadboard.md` is no longer unchanged from the first design.

## Resistance jig: a drifting several-hundred-kΩ reading is an open input, and it can't be told apart from a real ~800kΩ path (2026-09-23)

`resistance_measurement` (GP28, `R_REF` = 10kΩ) printed 706kΩ–848kΩ,
V = 3.254–3.262V, with the probe leads on the USB-C breakout. Read-only
ADC probing over `mpremote` (400 samples per run, three runs):

- Floating mean raw ~64750/65535 (98.8% of full scale), individual
  samples from ~62300 up to a clipped 65535. That's the ADC's noisy top
  end, not a divider working at 780kΩ: at `R_REF` = 10kΩ, 780kΩ and a
  true open differ by ~1.3% of the rail, which is inside the ADC's own
  error there.
- Enabling the internal pull-down on GP28 dropped the mean to ~54000
  (ratio 0.834). Solving `Rpd / (Rpd + R_REF)` for the RP2040's 50–80kΩ
  pull-down gives `R_REF` of 10–16kΩ, consistent with the 10kΩ the config
  says is fitted (a 220Ω or 1kΩ part would barely move). It does **not**
  separate "open" from "~800kΩ" — both give the same ratio.
- VSYS/3 on GP29 read 5.016V, so the USB supply is fine.

The same ~3.25V open-input value showed up as `THERM`'s one-sample
outlier on 2026-09-21 (3.253V, 698639Ω, −47.4°C, above): that reading
was an open thermistor leg for one sample, which supports the
contact-glitch explanation logged there. On this Pico's ADC, ~3.25V on a
pulled-up divider node reads as "the lower leg is open," whichever
circuit it turns up in.

Two takeaways for future sessions:

1. Above ~30×`R_REF` this jig cannot report a resistance. Treat any
   drifting, run-to-run-inconsistent value up there as "open." `main.py`
   now does (`OPEN_FRACTION` = 0.97, ~320kΩ at 10kΩ).
2. "Open" from a probe setup only means something after a positive
   control (probe tips touched together → "Short to GND or 0 Ohms").
   `breadboard3.jpg` shows a ribbon of Dupont leads whose breadboard-end
   pins look like they lie on the board rather than sit in holes; from a
   photo alone that can't be settled, so the check was handed back as a
   step with a positive control rather than declared a CC-pin result.

Trap hit while probing: `machine.ADC(n)` reconfigures the pin to its
analog function, so a `Pin(n, Pin.OUT, value=1)` followed by
`ADC(n)` reads the pin *undriven*. There's no way in stock MicroPython to
drive a GPIO and read it through the ADC in the same pin; a
"driven-high vs floating" comparison isn't available. Don't build a test
on it.

`parts_reference.md`'s USB-C breakout entry carries the related
inference that the two SMD parts marked `512` and `215` are both 5.1kΩ
(`215` is `512` upside-down; a real 2.1MΩ isn't a plausible CC
termination). Unmeasured as of this entry. **Superseded 2026-09-23:**
the USB-C path was shelved (the SparkFun kit is the `psu_medlow`
implementation), so the CC readings are no longer planned; the jig and
the open-input findings above still stand for any future use of
`resistance_measurement`.
