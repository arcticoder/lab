# psu_4xaa

4× AA alkaline cells in series, a 1N5817 Schottky diode for reverse-polarity
protection, and a 500 mA slow-blow polyfuse. Top of the plain-AA-series
progression — one cell up from [psu_3xaa](../psu_3xaa/), same battery
chemistry and protection stack as every AA tier below it.

Spec: 6.0 V, <300 mA, ~1.6 W. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_system` subgraph).

---

## Files

| File | Purpose |
|------|---------|
| `psu_4xaa.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step breadboard wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `validation_breadboard.jpg` | Photo of the 2×10 kΩ divider build used for § Validation |

Every check in § Validation and § Troubleshooting below reads GP26 with
[`measurement_tools/raw_voltage_probe`](../../measurement_tools/raw_voltage_probe/)'s
`main.py` — a plain averaged-voltage reader with no resistance math or
divider assumptions baked in, reused here rather than duplicated because
it's identical for any circuit that just needs "what does GP26 see."

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Four single-cell AA holders wired in series (holder 1 negative → holder
   2 positive → holder 3 positive → holder 4 positive, chained).
2. 1N5817 Schottky diode in series on the positive rail (cathode stripe
   toward the fuse), blocking reverse-polarity wiring.
3. 500 mA polyfuse (Littelfuse RXEF050) in series after the diode.
4. Output taken from polyfuse output (+) and holder 4 negative (−).

---

## Simulate

```bash
# from the repo root
ngspice -b power_supplies/psu_4xaa/psu_4xaa.spice
```

The first block prints the operating point at the nominal 20 Ω load
(~276 mA design point, after the Schottky drop). The second block sweeps
the load from 5 Ω to 50 Ω.

---

## Expected behaviour

```
V_out ≈ (6.0V − V_schottky) × Rload / (Rload + Rfuse)
```

At Rload = 20 Ω: **V_out ≈ 5.51 V, I ≈ 276 mA** — the Schottky costs about
0.35 V at this current, same as every other AA tier in this family.

---

## Validation

No physical load resistor either (see
[breadboard.md § Expected behavior](breadboard.md#expected-behavior) for
why 20 Ω isn't something to build). The check instead uses a lightweight
2:1 resistor divider so a Pico ADC pin can safely read this PSU's ~5.5 V
output — GP26/ADC0 is limited to 0–3.3V (see
`docs/general_purpose_circuit_dependency.md`'s `SCOPEPICO` node), so it
can never be wired straight onto this rail.

**Build:** two 10 kΩ resistors (from `../../docs/inventory.md`) in series
across the output, from output(+) to output(−)/ground rail, with the
midpoint tapped off to GP26.

```
psu_4xaa output (+)
      │
   [10 kΩ]
      │
      ├──────► Pico GPIO 26 / ADC0 (Pin 31)
      │
   [10 kΩ]
      │
psu_4xaa output (−) / ground rail ──────► Pico GND (Pin 28)
```

The Pico GND wire on the last line is **required**, not optional — GP26's
ADC reading is only meaningful relative to the Pico's own ground. Without
it the Pico and the PSU don't share a reference and GP26 reads garbage
regardless of how correctly the two 10 kΩ resistors are wired.

At ~275 µA, this divider draws negligible current — it doesn't meaningfully
load the PSU, and it's the *only* thing connected to the output for this
check (no other load).

**Before reading GP26, confirm the battery pack is actually installed and
powering the circuit**: all 4 cells seated in their holders, and the
power switch (if built per `breadboard.md` § 5) slid to the closed/ON
position. With the divider wired correctly but no power reaching it, GP26
reads ~0 V — which looks identical to a real fault but isn't one; see
§ Troubleshooting's first step below if that happens.

**Expected readings** — read GP26 with
[`raw_voltage_probe`](../../measurement_tools/raw_voltage_probe/)'s
`main.py`, which prints the averaged raw voltage directly
(`avg_raw / 65535 * 3.3`), nothing else. Don't use
[measurement_tools/resistance_measurement](../../measurement_tools/resistance_measurement/)'s
`main.py` for this specific check even though it reads GP26 the same
oversampled-average way: that script's printed "Resistance (R_x)" assumes
a *different* circuit — an unknown resistor forming a divider against a
known 10 kΩ reference, fed from the Pico's own 3V3 rail. This divider is
fed by the PSU's own output through two *known* 10 kΩ resistors, with
nothing unknown to solve for, so that script's resistance formula would
be meaningless here (`resistance_measurement` gets reused below, in
§ Troubleshooting, but for a different job — continuity-checking the
PSU's internal wiring with the battery disconnected, which is exactly the
divider-against-an-unknown-resistance case it's built for):

- Correct battery orientation: GP26 reads **~2.75 V** (half of the output
  voltage). Expect the output itself to sit a little *above* the
  documented ~5.51 V design figure — that number assumes the 276 mA drawn
  by a 20 Ω load, and this divider's ~275 µA draws far less, so the
  Schottky/fuse drops are smaller here.
- Reversed battery leads: GP26 reads **~0 V** — the Schottky blocks, no
  current reaches the divider.

Don't probe directly across the Schottky's own leads with the Pico —
doing that safely would mean moving Pico GND off the PSU's actual ground
rail (onto the diode's cathode) just for that one reading, which is easy
to get wrong and unnecessary here: the divider above already distinguishes
"diode conducting" from "diode blocking" without ever re-referencing
ground.

---

## Troubleshooting

If § Validation's divider reading doesn't land near the ~2.75 V target,
work through these in order — each rules out one segment of the chain
before moving to the next.

### 0. Confirm the battery pack is actually installed and powered

A ~0 V reading (not just "low," but at or near the Pico's own noise
floor, well under a volt) with the divider otherwise wired as described
in § Validation is most often simply **no power reaching the divider** —
a cell missing from a holder, a holder lead not seated, or the power
switch (if built) left open — not a wiring fault downstream. Reinsert all
4 cells, confirm the switch (if present) is closed/ON, and re-run
§ Validation before working through steps 1–3 below; they assume power
*is* reaching the divider and something else is wrong.

### 1. Confirm the two 10 kΩ divider resistors are actually 10 kΩ

Already visually confirmed from the color bands in `breadboard.jpg` —
no further action needed unless the physical parts in the build have
since changed. If it's ever genuinely in doubt, pull one resistor out of
circuit (out-of-circuit, so no parallel path through the rest of the
divider skews the reading) and check it with
[measurement_tools/resistance_measurement](../../measurement_tools/resistance_measurement/):
clip its `R_x` leg to one leg of the pulled resistor and GND to the
other, `mpremote run main.py`, expect a reading near 10,000 Ω.

### 2. Continuity-check the 4-cell chain + Schottky + polyfuse

Uses [resistance_measurement](../../measurement_tools/resistance_measurement/)
in its actual designed mode (known `R_ref` vs. unknown `R_x`) — see that
circuit's own README § "Reuse: continuity/troubleshooting checks on
another circuit" for the general rule this follows.

**Disconnect the battery pack first** — pull at least one AA cell out of
its holder, or unclip the red jumper from Holder 1(+) to the Schottky
anode (step 3 of `breadboard.md`'s wiring). This is required, not
optional: `resistance_measurement` drives whatever it's clipped to from
the Pico's own 3V3 rail, and leaving the ~6 V battery pack connected at
the same nodes means two power sources fighting each other — the
reading becomes meaningless and can push current back into the Pico's
3V3 rail.

With the pack disconnected, clip `resistance_measurement`'s `R_x`/GND
leads across each segment in turn and run `main.py`:

| Segment | Clip `R_x` to | Clip GND to | Expect |
|---|---|---|---|
| Holder 1→2 joint | Holder 1 (−) | Holder 2 (+) | Near-0 Ω ("Short to GND") = good continuity |
| Holder 2→3 joint | Holder 2 (−) | Holder 3 (+) | Same |
| Holder 3→4 joint | Holder 3 (−) | Holder 4 (+) | Same |
| Schottky, forward direction | Schottky anode | Schottky cathode | Low reading (diode conducting) — this is **not** a true ohmic value, see the caveat below |
| Schottky, reversed | Schottky cathode | Schottky anode | "Circuit Open" (diode blocking) |
| Polyfuse | Polyfuse leg 1 | Polyfuse leg 2 | A few ohms (cold-fuse resistance) — genuinely resistive, this one *is* a true reading |

A "Circuit Open" on any of the three holder-to-holder joints means that
specific solder/twisted-wire termination isn't actually making contact —
re-terminate that joint. A "Circuit Open" on the Schottky forward
direction, or a non-collapsing reading reversed, points at the diode
itself or its orientation. Once every segment above checks out, reconnect
the battery pack and re-run § Validation.

### 3. Battery pack open-circuit voltage (bypassing the Schottky/fuse)

Reuses the *same* 2×10 kΩ divider hardware already built for §
Validation — just re-clip the divider's top leg from the polyfuse output
over to **Holder 1 (+)** directly (the battery pack's raw positive
terminal), keeping the divider's bottom leg on the ground rail / Holder 4
(−) as before. This still safely halves the pack's ~6 V down to GP26-safe
territory, same reasoning as § Validation.

Run [`raw_voltage_probe/main.py`](../../measurement_tools/raw_voltage_probe/)
and compare the printed average against:

- **~3.0 V** — fresh 4×AA alkaline pack (4 × 1.5 V / 2).
- **~2.4 V** — 4×AA NiMH, or a partly-discharged alkaline pack (4 × 1.2 V
  / 2).
- Meaningfully below ~2.4 V — weak/dead cell(s) or a miswired holder;
  check individual cells.

This is the correct circuit for this specific check — not
[fuse_test_voltmeter](../../measurement_tools/fuse_test_voltmeter/),
whose jig is built around its own much lower single-cell voltage range
and has no divider in front of GP26, so it isn't safe to wire directly
across this pack's ~6 V.

When done, move the divider's top leg back to the polyfuse output before
resuming § Validation.
