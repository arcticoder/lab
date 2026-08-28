# Breadboard Wiring — psu_ultralow_v1

## Circuit overview

Single AA cell → 50 mA polyfuse → output. No regulation, no adjustability —
a battery interface with resettable overcurrent protection.

**Equivalent to:** `psu_ultralow_v1.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| AA battery holder | single-cell, 5mm terminal | 1 |
| AA alkaline battery | 1.5V | 1 |
| Polyfuse | Littelfuse RXEF005 (50 mA slow-blow) | 1 |
| Dupont M-M jumper (red) | 16–20cm | 1 |
| Dupont M-M jumper (black) | 16–20cm | 1 |
| SYB170 breadboard | 170-pin, 300V, <5A | 1 |

---

## Wiring steps

### 1. Place the polyfuse

Insert the polyfuse across two breadboard columns so each leg sits in its
own node — one leg becomes the battery-side node, the other becomes the
output node.

### 2. Connect the battery

| From | To | Wire |
|------|----|------|
| Battery holder (+) | Polyfuse leg 1 | Red Dupont jumper |
| Battery holder (−) | Ground rail | Black Dupont jumper |

### 3. Take the output

Output (+) is the polyfuse's far leg (leg 2). Output (−) is the ground
rail, tied to the battery negative.

---

## Expected behavior

With a 15 Ω test load across the output: ~1.44 V, ~96 mA. This is the
`.spice` nominal design-point characterization of the *finished PSU's*
output, not a component in this breadboard's own parts list or a step
above — no 15 Ω resistor needs to be wired in to build or validate this
circuit. It is also unrelated to the 10 Ω load resistor used in
[fuse_test_voltmeter](../../measurement_tools/fuse_test_voltmeter/)'s
bench fuse-test jig (different circuit, different purpose — that jig
validates the bare polyfuse *before* it goes into this PSU). See
[README.md](README.md) § Validation without a multimeter for how to
actually check this circuit once built (probe across the fuse leads with
a Pico ADC pin — no load resistor needed).
