# Breadboard Wiring — electric_field_probe

## Circuit overview

A bare-wire/foil electrode biased to VCC/2 through a 1MΩ/1MΩ divider,
buffered by one channel of a TL082 (JFET-input, so its own input current
doesn't swamp the tiny signal the electrode couples in). Output rides
around ~1.65V and deviates when a charged/grounded object comes near the
electrode.

**Equivalent to:** `electric_field_probe.spice`

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) — the
Pico's own onboard 3.3V rail, not a battery PSU tier. See README.md for
why: it guarantees the op-amp output can never exceed the Pico ADC's own
0-3.3V safe input range.

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| TL082 | JFET-input dual op-amp, DIP-8 | 1 |
| Resistor | 1 MΩ | 2 |
| Electrode | any small bare conductor — a stripped jump-wire end or foil scrap | 1 |
| Dupont M-M jumper (red) | 12–20cm | 1 |
| Dupont M-M jumper (black) | 12–20cm | 2 |

No dedicated probe/electrode part has been ordered — none is needed for
a first build. Any small exposed conductor works; a bigger/flatter one
(foil) couples more strongly to a nearby field than a thin wire tip, but
either demonstrates the circuit.

---

## TL082 pinout (DIP-8, per `lab/docs/parts_reference.md`)

| Pin | Function | Pin | Function |
|-----|----------|-----|----------|
| 1 | Output 1 | 8 | V+ |
| 2 | Inverting input 1 (−) | 7 | Output 2 (unused) |
| 3 | Non-inverting input 1 (+) | 6 | Inverting input 2 (unused) |
| 4 | V− | 5 | Non-inverting input 2 (unused) |

Only channel 1 (pins 1–3) is used; leave channel 2 (pins 5–7)
unconnected. V− (pin 4) goes to GND, not a negative supply — this is a
single-supply build.

---

## Wiring steps

### 1. Power the TL082

| From | To | Wire |
|------|----|------|
| Pico 3V3(OUT) pin | TL082 pin 8 (V+) | Red Dupont jumper |
| Pico GND pin | TL082 pin 4 (V−/GND) | Black Dupont jumper |

### 2. Wire the bias divider

- R1 (1 MΩ): one leg to the same row as TL082 pin 8 (V+/3.3V), other leg
  to a fresh row — call this the BIAS row.
- R2 (1 MΩ): one leg to the BIAS row, other leg to GND.
- Jumper the BIAS row to TL082 pin 3 (non-inverting input).

### 3. Wire the electrode

Connect the electrode (stripped wire end or foil) to the same BIAS row as
R1/R2's junction and TL082 pin 3. Keep this row's wiring short — it's a
high-impedance node, more susceptible to picking up unrelated noise the
longer the lead run is.

### 4. Close the follower feedback loop

Jumper TL082 pin 2 (inverting input) directly to pin 1 (output). This is
the unity-gain follower connection — pin 1 will track whatever pin 3
sees.

### 5. Take the output

Output is TL082 pin 1. Wire it to a Pico ADC-capable GPIO (e.g. GP27 —
GP26 is already used by `ne555_astable`'s output divider if that circuit
is on the same breadboard).

---

## Expected behavior

At rest (no nearby charged object), the output should read close to
~1.65V (VCC/2) — see `README.md`'s simulated bias-divider math. Bringing
a charged object near the electrode (a balloon or comb rubbed on hair or
fabric) should visibly deflect the reading away from 1.65V; moving it
away should let the reading drift back. If the reading never moves
regardless of what's brought near the electrode, check TL082 power
(pins 8/4), the pin 2-to-pin 1 feedback jumper, and that the electrode is
actually making contact with the BIAS row — see `README.md`'s Validation
section for the full troubleshooting list.
