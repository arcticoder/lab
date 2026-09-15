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
| Resistor | see § Reference divider below | 2 |
| Resistor | 10 kΩ (TL431A pull-up) | 1 |
| Dupont M-M jumper (red) | 12–20cm | 2 |
| Dupont M-M jumper (black) | 12–20cm | 2 |

---

## Reference divider (Vref = 0.2V)

The TL431A's internal bandgap reference is fixed at 2.495V between its
Ref and Anode pins — see `docs/parts_reference.md#tl431a-precision-shunt-
reference`. To get a 0.2V comparator reference, divide the TL431A's
regulated Cathode output (set to some convenient value, e.g. 2.5V, by its
own feedback divider per that part's own reference circuit) down further
with a second divider feeding the LM358's non-inverting input. Work out
the exact two resistor values against whichever Cathode voltage the
TL431A ends up regulated to on the bench — this is a real hardware
sizing step the `.spice` model deliberately skips (see `README.md`'s
Design notes for why).

---

## Wiring steps

### 1. Wire the load path

- MOSFET Drain → the protected circuit's load return (whatever
  `psu_medhigh`/`psu_high` load this eventually protects).
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
- Power LM358 (pin 8 VCC, pin 4 GND) from a rail matching the gate-drive
  logic level intended (3.3V for direct Pico-GPIO-equivalent levels).

### 3. Wire the TL431A reference

Per `docs/parts_reference.md#tl431a-precision-shunt-reference`: Cathode
needs a pull-up resistor/current source (it only sinks, never sources)
— a 10kΩ resistor from VCC to Cathode works. Ref and Anode set the
regulated Cathode voltage via their own feedback divider — see that
part's own reference-circuit configuration before wiring specific
values.

---

## Expected behavior

With the load drawing under 2A, the gate should read at the drive rail
(fully on) and the sense node should read below 0.2V. Forcing a fault
(a load drawing more than 2A) should trip the gate low and cut the
MOSFET off — but expect this to **chatter** (rapidly oscillate on/off)
right at the trip boundary rather than cleanly latch off, since this is
a simple comparator with no hysteresis or latch — see `README.md`'s
Design notes for why, and what a fix would require if that turns out to
be a real problem for whatever this ends up protecting.
