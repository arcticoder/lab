# psu_medlow_lm317

The SFE Breadboard Power Supply Kit
(https://ca.robotshop.com/products/sfe-breadboard-power-supply-kit) — an
LM317-based adjustable regulator, switch-selectable between 3.3V and 5V
output, fed from an unregulated DC barrel-jack wall adapter. An alternative
implementation of the `psu_medlow` tier alongside
[psu_medlow_usbc](../psu_medlow_usbc/) — that one is fuse+bypass only
because a USB-C adapter already regulates to 5V; this one does its own
regulation from a raw DC input, at the cost of extra parts to solder.

**Status: on order, not yet built.** No physical unit has been assembled or
tested — see [breadboard.md](breadboard.md) for the caveat on the exact
voltage-select switch wiring.

Spec: 3.3V or 5V (switch-selected), up to 1.5A (LM317 TO-220 max, though the
kit's own trace width/heatsinking may limit sustained current well below
that). See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_medlow` node, `PSUMEDLOWLM317`).

---

## Kit contents

| Component | Qty | Role |
|-----------|-----|------|
| DC barrel jack (2.1mm, center-positive) | 1 | Unregulated DC input from a wall adapter |
| LM317 (TO-220, 1.5A max) | 1 | Adjustable linear regulator |
| 1N4004 diode | 1 | Reverse-polarity protection on the input |
| 100µF 25V capacitor | 1 | Input bulk/smoothing cap |
| 10µF 25V capacitor | 1 | Output cap (LM317 datasheet recommendation) |
| 0.1µF 50V capacitor | 1 | ADJ-pin bypass cap (ripple rejection) |
| Red power LED | 1 | Lit whenever the output rail is powered |
| SPDT slide switch | 2 | One selects 3.3V/5V, one is the main power switch |
| 0.1" header pins | 4 | Output breakout — plugs into the breadboard's power rails |
| 330Ω resistor (1/6W) | 2 | One sets the 5V feedback step, one limits LED current |
| 390Ω resistor (1/6W) | 1 | Base feedback resistor (R2), sets the 3.3V step |
| 240Ω resistor (1/6W) | 1 | Fixed feedback resistor (R1), LM317 datasheet-standard value |
| Bare PCB | 1 | Silkscreen-labeled solder board |

---

## Files

| File | Purpose |
|------|---------|
| `breadboard.md` | Wiring/assembly plan, with the LM317 feedback-resistor math |

No `.spice` netlist or `smoke_test.py` for this circuit — it's a
switch-selectable regulator kit rather than a from-scratch design, and the
exact PCB routing needs confirming against the physical board once it
arrives (see `breadboard.md`).

---

## Design: LM317 feedback network

The LM317 holds 1.25V between OUT and ADJ, so:

```
V_out = 1.25V × (1 + R2/R1)
```

With **R1 = 240Ω** fixed (the LM317 datasheet's standard value, since it
also sets the ~5mA minimum load current the LM317 needs to regulate):

- **R2 = 390Ω** → V_out = 1.25 × (1 + 390/240) = **3.28V** (labeled 3.3V)
- **R2 = 390Ω + 330Ω = 720Ω** → V_out = 1.25 × (1 + 720/240) = **5.00V**

So the voltage-select switch adds the second 330Ω resistor in series with
the 390Ω to jump from 3.3V to 5V. The kit's second 330Ω is the LED's
current-limiting resistor, unrelated to the feedback network — see
`breadboard.md` for how each of the four resistors maps onto the circuit.

---

## Expected behaviour

- 3.3V setting: ~3.28V at the output header, ±5% resistor tolerance.
- 5V setting: ~5.00V at the output header, ±5% resistor tolerance.
- LED lights whenever the output rail is powered; it runs dimmer in 3.3V
  mode than 5V mode since it's wired off the regulated output — expected,
  not a fault.
- Input needs enough headroom above the selected output for the LM317's
  ~2–3V dropout — a 9V or 12V wall adapter works for either setting; a 5V
  adapter would not leave enough headroom for the 5V output setting.
