# lockin_amplifier

A single-phase lock-in amplifier (phase-sensitive detector): it pulls a
small signal at a known frequency out of larger interference at other
frequencies and out of any DC drift. It is the first concrete tier6
`LOCKIN` and tier4 `DEMOD` in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md),
built from parts on hand: two LM358 chips, two CD4066B chips, resistors,
capacitors and the Pico. The `PHASED` XOR detector
([phase_detector](../phase_detector/)) measured *phase*; this one measures
the *amplitude of a signal that is in phase with a reference*, which is what
the weak-signal sensor chains (`TIA`, `CHGAMP`, `HALLAMP`, an optical balance
readout) need.

**Status: built on the bench 2026-10-05; the demodulator works but the
in-phase reading is about 4–5× the design value (1.1V against 0.26V), so the
run does not pass yet.** Designed and simulated 2026-10-02 (`smoke_test.py`
green, 26 checks). The first run read `VB` low in every state (0.026V at `floor`, 0.14V under
the second run's value in phase); two runs after it read both nodes near
1.12V at `floor`, with `VA` repeating to within 16mV. The structure is right
on the bench: the sign flips with the signal phase (X +1.08V in phase,
−1.39V anti-phase), 90° reads near zero (+0.14V), 45° reads between, and the
interferer alone moves X by about 0.12V, a tenth of in-phase. What is wrong
is the size: at that amplitude the gain stage's output clips (the LM358 stops
at about 1.8V and 0.02V), which flattens the in-phase and anti-phase readings
and breaks the ratio checks. A duty sweep of the in-phase test pulse (2% to
50%) grew X from 68mV to 1.26V, so the signal path is live. `diagnose_gain.py` finds which stage is
responsible (below).

---

## Files

| File | Purpose |
|------|---------|
| `lockin_amplifier.spice` | ngspice transient netlist of the whole signal path, with case parameters the smoke test rewrites |
| `diagnose_gain.py` | One-jumper probe: reads the 1kHz ripple on SIG or OUT1 through GP28 to say whether the source side or the gain stage is too hot (`mpremote mount . run diagnose_gain.py`) |
| `smoke_test.py` | Seven simulated bench states plus a DC-offset case, then `main.py` against a mocked `machine` (register values, pin release, decision logic) |
| `main.py` | MicroPython: generates the clocks, test signal and interferer, reads both outputs, prints a table and PASS/FAIL lines (about 15s) |
| `breadboard.md` | Wiring tables and failure table |

---

## Design

```
                                   Vmid = 1.114V (10k/5.1k from 3V3, LM358 buffer U1B)
GP8  (signal)  ──1MΩ──┐                │
GP9  (inverted)──1MΩ──┤                │
GP6  (interferer)─500k┴── sig ──1kΩ────┘
                          │
                          └─1µF─10kΩ─►(−) U1A ─┬── out1 ──10kΩ── GND
                             Vmid ───►(+)      │   (Rf = 1MΩ from out1 to (−): gain −91)
                                               │
              GP10 REF ──► CD4066B #1 sw1 ◄────┤────► CD4066B #2 sw1 ◄── GP11 REFB
                                 │                              │
                              100kΩ                          100kΩ
                                 ├── A ─ 1µF ─ GND              ├── B ─ 1µF ─ GND
                                 └─► U2A follower ─► GP26       └─► U2B follower ─► GP27

            X = V(GP27) − V(GP26)  =  the lock-in output
```

How it works. The gain stage is AC-coupled (1µF into 10kΩ), so any DC at
the input is blocked and the stage's own DC gain is 1; the signal is
amplified by 1MΩ/(10kΩ+1kΩ) = −91. Switch 1 of one CD4066B passes the
amplified signal into an RC averager while REF is high, switch 1 of the other
passes it into a second averager while REFB is high. Each averager holds the
mean of the signal during its half-period. A signal in phase with REF has its
two halves land in different averagers, so `VB − VA` is large; interference
at another frequency lands in both halves equally and cancels in the
subtraction, as does anything slow. The 100kΩ and 1µF give an averaging time
constant of 0.21s (a switch is closed only 48% of the time), so a reading
needs about 1.6s to settle and then ignores anything faster than a few hertz.

| Choice | Value | Why |
|--------|-------|-----|
| Supply | Pico `3V3(OUT)`, about 2mA total | The LM358 can't swing above about 1.8V on 3.3V, so everything is centred on Vmid = 1.11V and kept small: the stage output reaches 1.53V at most. TL082s were rejected: their input range on 3.3V single supply is doubtful, the LM358's reaches ground |
| Gain | −91 | Puts a 3.3mV test signal at 0.3V p-p and a 2× larger interferer at 0.55V p-p, both inside the swing. Higher gain needs a smaller test signal |
| `Rl1` 10kΩ | to GND | Holds the LM358's output stage in the region where it conducts, avoiding its crossover kink around zero load current |
| Clocks | REF high 48%, REFB high the last 48% | 4% of the period with both switches open, so they are never closed together even with turn-on/turn-off skew |
| Two CD4066B chips, switch 1 of each | not switches 1 and 2 of one chip | Switch 1 of all ten chips passed the bring-up jig; switches 2–4 are untested |
| Frequencies | 1000Hz reference, 1370Hz interferer | From one 125MHz clock (`DIV` 2, 62 500 and 45 620 counts). The interferer is not a harmonic of 1kHz, so its mixing products fall well above the 0.2s averager |
| Slices | REF on slice 5, signal on slice 4, interferer on slice 3 | The reference and signal slices start on the same clock edge from preset counters, so their phase is exact and settable (0°, 45°, 90°, 180°), not random as with two `machine.PWM` objects started separately |

Simulated numbers (`ngspice`, LM358 as a 1MHz-GBW, 1.8V-ceiling behavioral model, CD4066B Ron = 1kΩ):

| Bench state | X = VB − VA |
|-------------|-------------|
| No signal | −0.35µV |
| Signal in phase with REF | +264.0mV (hand calculation 288mV; LM358 bandwidth smooths the edges) |
| Signal in anti-phase | −264.0mV |
| Signal at 45° | +128.6mV (0.49 of in-phase) |
| Signal at 90° | −13.5mV (5%: the op-amp's phase lag) |
| 1.37kHz interferer only, 0.55V p-p at the stage output | +0.87µV |
| Signal + interferer | 263.988mV against 263.985mV for the signal alone |
| Signal + 1V DC offset injected at the input | 264.04mV |
| Highest stage output (signal + interferer) | 1.53V |

The phase response is a triangle, not a cosine: gating a square wave with a
square clock gives X proportional to `1 − 2|φ|/180°`. That is why 45° reads
0.49 and not 0.71.

## Finding the gain error (2026-10-05)

Expected SIG swing is 3.3mV p-p (3.3V from GP8 through 1MΩ into the 1kΩ
`Rbias`). A SIG swing near 3mV puts the fault in the gain stage (`Rin`,
`Rf`, or `Cin` wrongly placed); a swing near 15mV puts it in the source
side. Metal-film resistors from the kit are all five-band `brown black black
x brown` for 1kΩ, 10kΩ, 100kΩ and 1MΩ, differing only in the fourth band, and
a 5.1kΩ part is the other likely stand-in for the 1kΩ `Rbias`. Wiring steps
and the decision table are in `breadboard.md` § "Gain too high".

## What this does not show

- **Real hardware numbers.** Op-amp input offsets (LM358: a few mV, times 1 at DC because the stage is AC-coupled), 5% resistor tolerance (the gain, and so X, moves by about ±10%), ADC channel offsets (the Pico's two channels can differ by a few mV) and the CD4066B's true on-resistance at 3.3V are not modeled or are assumed. `main.py` subtracts the no-signal reading and judges the rest as ratios to the in-phase reading, so it does not depend on the absolute gain; its limits on the absolute in-phase value (120–400mV) are wide for that reason.
- **Clock pickup.** The 3.3V clock edges can couple into the high-gain input through the breadboard. That pickup is at the reference frequency and in phase with it, which is exactly what a lock-in detects, so it shows up as a spurious signal. `main.py` measures it as the no-signal offset and subtracts it; it fails if it exceeds 50mV. Keep the jumpers from GP10/GP11 away from the `sig` and `inn` rows.
- **Fixed-phase operation only.** This is a single-phase detector. If the signal's phase relative to REF drifts, X drifts with it (triangularly). A two-phase (I/Q) version needs a second pair of switches and averagers.
- **No ripple bound on hardware.** The simulated ripple at the averagers is 0.4mV p-p; ripple at the ADC pins was not measured.
- **Averager settling.** Reading sooner than about 1.6s after any change gives a value still moving toward its final one.
- **CD4066B pinout.** The wiring uses the datasheet pinout (`VSS` on pin 7). The pinout this repo carried before 2026-10-02 had `VSS` on pin 6 and was wrong; see `docs/parts_reference.md`.
