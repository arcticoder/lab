# Breadboard Wiring — psu_4xaa

## Circuit overview

Four AA cells in series → Schottky (reverse-polarity protection) → 500 mA
polyfuse → output.

**Equivalent to:** `psu_4xaa.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| AA battery holder | single-cell, 5mm terminal | 4 |
| AA alkaline battery | 1.5V | 4 |
| Schottky diode | 1N5817 (1A, 20V) | 1 |
| Polyfuse | Littelfuse RXEF050 (500 mA slow-blow) | 1 |
| Dupont M-M jumper (red) | 16–20cm | 1 |
| Dupont M-M jumper (black) | 16–20cm | 1 |
| Dupont M-M jumper (any) | 12–16cm | 3 |
| SYB170 breadboard | 170-pin, 300V, <5A | 1 |
| Slide Switch (optional) | 3-pin SPDT, SunFounder Thales kit | 1 |
| Metal film resistor (optional, validation only) | 10 kΩ | 2 |

The slide switch and 10 kΩ resistors are not part of the base PSU circuit
— see § 5 (power switch) and [README.md § Validation](README.md#validation)
for what each is for. Skip both if you just want the bare PSU.

---

## Wiring steps

### 1. Series the four AA holders

| From | To | Wire |
|------|----|------|
| Holder 1 (−) | Holder 2 (+) | Solder or short jumper |
| Holder 2 (−) | Holder 3 (+) | Solder or short jumper |
| Holder 3 (−) | Holder 4 (+) | Solder or short jumper |

### 2. Place the Schottky and polyfuse

Insert the Schottky (cathode stripe toward the fuse) and polyfuse in series
on the positive rail, downstream of holder 4.

### 3. Connect the battery pack

| From | To | Wire |
|------|----|------|
| Holder 1 (+) | Schottky anode | Red Dupont jumper |
| Holder 4 (−) | Ground rail | Black Dupont jumper |

### 4. Take the output

Output (+) is the polyfuse's far leg. Output (−) is the ground rail, tied
to holder 4 negative.

### 5. Power switch (optional)

Not part of the original design, but a reasonable addition to any PSU
you want to switch off without unplugging jumpers — insert the slide
switch in series in the return leg from step 3, between holder 4 (−) and
the ground rail:

| From | To | Wire |
|------|----|------|
| Holder 4 (−) | Switch pin 2 (common) | Black Dupont jumper |
| Switch pin 1 | Ground rail | Black Dupont jumper |

Switch pin 3 is left unconnected (per the slide-switch pinout note in
`../../docs/inventory.md` — pin 2 always connects to whichever outer pin
the slider is pushed toward). Sliding toward pin 1 closes the loop
(PSU on); sliding toward the unconnected pin 3 opens it (PSU off). This
switch is in the power path itself (unlike the signal-only arm switch in
`measurement_tools/fuse_test_voltmeter/`), so treat it as a simple
mechanical break, not a probe point.

---

## Expected behavior

**6.0 V raw, ~5.51 V / ~276 mA at the netlist's nominal 20 Ω design
point.** That 20 Ω is `psu_4xaa.spice`'s `Rload` — a simulated
stand-in used to pick a representative operating point for the sweep,
**not a physical resistor to build** (nothing in the parts list above is
a load resistor, matching every other AA-tier PSU in this repo — see
[psu_ultralow_v1/README.md](../psu_ultralow_v1/README.md)'s "Validation"
section for the same convention). Building an actual 20 Ω/276 mA load
from kit-stock 10 Ω 1/4 W resistors isn't a simple two-resistor swap
either: two 10 Ω in series dissipate ~0.76 W *each* at that current —
three times their 0.25 W rating. See
[README.md § Validation](README.md#validation) for how this PSU is
actually checked on the bench, which needs no load resistor at all.
