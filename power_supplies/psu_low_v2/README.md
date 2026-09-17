# psu_low_v2

2× AA alkaline cells in series, a 1N5817 Schottky diode for reverse-polarity
protection, and a 500 mA slow-blow polyfuse. Upgrade path from
[psu_ultralow_v1](../psu_ultralow_v1/) — same battery chemistry, more
headroom.

Spec: 3.0 V, <300 mA, ~0.9 W. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_low` node).

---

## Files

| File | Purpose |
|------|---------|
| `psu_low_v2.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step breadboard wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

§ Validation below reads GP26 with
[`measurement_tools/raw_voltage_probe`](../../measurement_tools/raw_voltage_probe/)'s
`main.py` — the same plain averaged-voltage reader `psu_4xaa` uses for its
own divider check, reused here rather than duplicated.

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Two single-cell AA holders wired in series (holder 1 negative → holder 2
   positive).
2. 1N5817 Schottky diode in series on the positive rail (cathode stripe
   toward the fuse), blocking reverse-polarity wiring.
3. 500 mA polyfuse (Littelfuse RXEF050) in series after the diode.
4. Output taken from polyfuse output (+) and holder 2 negative (−).

---

## Simulate

```bash
# from the repo root
ngspice -b psu_low_v2/psu_low_v2.spice
```

The first block prints the operating point at the nominal 10 Ω load
(~265 mA design point, after the Schottky drop). The second block sweeps
the load from 5 Ω to 30 Ω.

---

## Expected behaviour

```
V_out ≈ (3.0V − V_schottky) × Rload / (Rload + Rfuse)
```

At Rload = 10 Ω: **V_out ≈ 2.53 V, I ≈ 253 mA** — the Schottky costs about
0.35 V at this current.

---

## Validation

Same divider-based technique as
[psu_4xaa](../psu_4xaa/README.md#validation) — same battery chemistry and
protection stack, just two cells instead of four. GP26/ADC0 is limited to
0–3.3 V, and two fresh AA cells in series can sit close to that limit
open-circuit, so this rail also gets divided down rather than probed
directly; full rationale and troubleshooting for this technique (including
why the Schottky's own leads aren't probed directly) live in that README.

**Build:** the same 10 kΩ + 5.1 kΩ resistor pair (from
`../../docs/inventory.md`) in series across the output, from output(+) to
output(−)/ground rail, with the midpoint tapped off to GP26 — and Pico GND
tied to the ground rail, required for a meaningful reading:

```
psu_low_v2 output (+)
      │
   [10 kΩ]
      │
      ├──────► Pico GPIO 26 / ADC0 (Pin 31)
      │
   [5.1 kΩ]
      │
psu_low_v2 output (−) / ground rail ──────► Pico GND (Pin 28)
```

**Run:**

```bash
cd measurement_tools/raw_voltage_probe
mpremote run main.py
```

**Expected readings** (5.1 kΩ ⁄ (10 kΩ + 5.1 kΩ) ≈ 0.338 of the output
voltage):

- Correct battery orientation: GP26 reads **~1.0 V**. The loaded design
  figure of ~2.53 V (§ Expected behaviour above) assumes 253 mA at a 10 Ω
  load; the divider only draws ~200 µA, so the Schottky/fuse drops are
  much smaller here and the actual output sits closer to its unloaded
  ~2.8–3.0 V.
- Reversed battery leads: GP26 reads **~0 V** — the Schottky blocks, no
  current reaches the divider.

**Status, 2026-09-16:** physically assembled (`breadboard.jpg`), but
this divider check itself hasn't been run yet — assembly moved straight
to powering `transimpedance_amplifier` instead. That circuit's own
bench test came back with a symptom (output completely unresponsive to
light, stable at ~0.38V) that's consistent with this rail not actually
reaching the LM358 — see
[transimpedance_amplifier/README.md](../../signal_conditioning/transimpedance_amplifier/README.md#validation).
**Run the GP26 divider check above next**, standalone (LM358
disconnected or not), before assuming anything about the TIA circuit's
own wiring — it'll confirm or rule out this rail as the cause. Also
worth a look: the breadboard photo shows a slide switch and a diode
whose state/role isn't obvious from this file's wiring steps alone —
confirm the switch (if it's in series in the power path) is ON.
