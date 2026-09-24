# Breadboard Wiring — active_current_limiter

## Circuit overview

An IRLZ44N MOSFET in series with the protected load's return path, a
0.1Ω sense resistor to ground, and one channel of an LM358 wired as a
comparator that drives the gate: below the 2A trip point the MOSFET
stays fully on; above it, the comparator pulls the gate low and the
MOSFET turns off. This is the general-purpose `ACTIVELIM` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
— protects `psu_medhigh`/`psu_high` (both backlog, no folder yet), so
this circuit stands alone ahead of either PSU actually being built.

**Uses the only IRLZ44N MOSFET currently on hand** (1 unit — see
`docs/inventory.md`). `HVPULSE` (tier7/8, spacetime) was flagged in
`docs/TODO-agent.md` as sharing this same single part, but per this
repo's ephemeral-circuit convention it returns to inventory once this
build's bench check passes and nothing else needs it wired — a second
MOSFET is only actually needed if both circuits must be physically
assembled at once, which isn't the case today (see
`docs/kb/circuit_lifecycle_and_repo_scope.md`). See `README.md`'s Design
notes for why `HVPULSE` wasn't attempted in this same pass regardless.

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| IRLZ44N | logic-level N-channel MOSFET, TO-220 | 1 |
| LM358P | dual op-amp, DIP-8 (used as a comparator) | 1 |
| TL431A | precision shunt reference, TO-92 | 1 |
| Resistor | 0.1 Ω (sense, `Rs`, 1W metal-film) | 1 |
| Resistor | 100 Ω (reference divider, bottom leg) | 1 |
| Resistor | 1 kΩ (TL431A pull-up, and the divider's top leg for the 2A setting) | 2 |
| Resistor | 2 kΩ (divider top leg, added in series with a 1 kΩ, for the bench-check setting) | 1 |
| Dupont M-M jumper (red) | 12–20cm | 2 |
| Dupont M-M jumper (black) | 12–20cm | 2 |

---

## Reference divider (Vref)

The TL431A wired with its Ref pin tied to Cathode regulates Cathode to
its 2.495V internal reference (see `docs/parts_reference.md#tl431a-
precision-shunt-reference`). A two-resistor divider from Cathode to GND
brings that down to the comparator's reference, `Vref = 2.495V × R_bot /
(R_top + R_bot)`, and the trip current is `Vref / 0.1Ω`. `R_bot` is the
100 Ω resistor either way; the top leg is what changes:

| Setting | `R_top` | `Vref` | Trips at | Use |
|---------|---------|--------|----------|-----|
| Bench check | 2 kΩ + 1 kΩ in series | 0.080V | ~0.80A | The validation in `README.md` § Validation (5V source, 2A max) |
| 2A design point | 1 kΩ + 100 Ω in series | 0.208V | ~2.08A | Needs a source that can actually push more than 2A |

Both values come from ±5% kit resistors and the LM358's own input offset
(a few mV, which is several percent of 0.08V), so expect the real trip
point to land within roughly ±15% of the figure in the table — the bench
check's two dummy loads (0.625A and 1.0A) are far enough either side of
0.80A to tell that apart.

The TL431A needs at least ~1mA flowing into its Cathode to regulate.
From the 5V rail through a 1 kΩ pull-up that is (5V − 2.5V)/1kΩ = 2.5mA
total, of which the bench-check divider takes ~0.8mA, leaving ~1.7mA.
(A 10 kΩ pull-up, as an earlier version of this file specified, would
leave 0.25mA and the reference would sag.)

---

## Wiring steps

### 1. Wire the load path

- MOSFET Drain → the protected circuit's load return (whatever
  `psu_medhigh`/`psu_high` load this eventually protects; for the bench
  check, a 10W wirewound dummy load — 8Ω, then 5Ω — from the 5V rail).
- MOSFET Source → one leg of `Rs` (0.1Ω).
- Other leg of `Rs` → GND.

### 2. Wire the sense/comparator

- LM358 pin 2 (inverting input) → the MOSFET-Source/Rs junction (the
  sense node).
- LM358 pin 3 (non-inverting input) → the 0.2V reference divider output
  (§ Reference divider above).
- LM358 pin 1 (output) → MOSFET Gate, directly (no series resistor
  needed at Pico-logic drive levels, but a ~100Ω series resistor is
  harmless insurance against gate-drive ringing if one's on hand).
- Power LM358 (pin 8 VCC, pin 4 GND) from **5V**, not 3.3V. The LM358's
  output only pulls up to about Vcc − 1.5V, so on 3.3V the gate would
  reach ~1.8V — at the IRLZ44N's 1–2V threshold, not fully on — while on
  5V it reaches ~3.5V, which turns the MOSFET on properly. For the bench
  check, use the same 5V rail that feeds the load; on a bench without a
  separate 5V, the Pico's VBUS pin (physical pin 40) is a 5V source.

### 3. Wire the TL431A reference and divider

Per `docs/parts_reference.md#tl431a-precision-shunt-reference` for the
pinout:

- Cathode → a 1kΩ resistor → the 5V rail (the pull-up: the part only
  sinks current, never sources it).
- Ref → Cathode (tied together: the part then regulates Cathode to
  2.495V).
- Anode → GND.
- Cathode → `R_top` (per the table in § Reference divider) → the
  reference node → `R_bot` (100Ω) → GND. The reference node goes to LM358
  pin 3.

---

## Expected behavior

With the load drawing less than the trip current (2A at the design
setting, ~0.8A at the bench-check setting), the gate should read at the
drive level (~3.5V, fully on) and the sense node should read below the
reference (0.2V / 0.08V). Forcing a fault (a load drawing more than the
trip current) should trip the gate low and cut the
MOSFET off — but expect this to **chatter** (rapidly oscillate on/off)
right at the trip boundary rather than cleanly latch off, since this is
a simple comparator with no hysteresis or latch — see `README.md`'s
Design notes for why, and what a fix would require if that turns out to
be a real problem for whatever this ends up protecting.
