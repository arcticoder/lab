# resistance_measurement

A Pico-ADC voltage-divider circuit that measures an unknown resistance
between two terminals, or confirms continuity between two nodes on
another circuit — the readout is a specific, digitally-loggable number
(console/serial output), not a momentary needle position, so it's the
measurement instrument for this bench rather than a stand-in for one.

Built specifically to find the actual resistance of a chain of jumper
wires being pressed into service as a low-value current-sense shunt for
[ammeter_1ohm](../ammeter_1ohm/), since no 0.1Ω resistor was on hand.
That original use case is a fixed two-terminal component with nothing
else attached — the general circuit below works the same way for any
unknown two-terminal resistance, which is why it's also reused as a
**continuity checker** on other circuits (clip `R_x`/GND onto a suspect
node pair instead of a dedicated unknown resistor — see
[psu_4xaa/README.md § Troubleshooting](../../power_supplies/psu_4xaa/README.md#troubleshooting)
and [cd4066_switch_tester/README.md § Troubleshooting a "fixed in-between value" fail](../cd4066_switch_tester/README.md#troubleshooting-a-fixed-in-between-value-fail)
for worked examples). In that mode, a near-0Ω reading (`main.py`'s "Short
to GND or 0 Ohms" message) means continuity is **confirmed** — it's a
pass, not a fault — while "Circuit Open" means the two nodes aren't
joined.

**Result on the original jumper-chain shunt: ~1.005Ω**, stable across
repeated readings. That value is what `ammeter_1ohm/main.py` uses as its
`SHUNT_OHMS`.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — reads GP26, averages ADC samples, computes and prints `R_x` |
| `breadboard.jpg` | Photo of the actual bench jig |

No `.spice`/`smoke_test.py` here — this is a one-off measurement jig for
characterizing a specific physical jumper chain, not a circuit with a
fixed design target to assert against.

---

## Circuit

A known reference resistor (`R_ref`, 10Ω from
[docs/inventory.md](../../docs/inventory.md)) forms a voltage
divider with the unknown resistance (`R_x`, the jumper chain). The Pico's
3V3 rail drives the divider, and GP26/ADC0 reads the midpoint:

```
Pico 3V3 (Pin 36)
      │
  [R_ref] (10 Ohms)
      │
      ├──────► GPIO 26 / ADC0 (Pin 31)
      │
  [R_x Chain] (Unknown Resistance)
      │
Pico GND (Pin 28)
```

Solving the divider equation for the unknown leg:

```
R_x = R_ref × (V_out / (V_in − V_out))
```

where `V_in` is the Pico's 3V3 rail and `V_out` is what GP26 reads at the
R_ref/R_x junction. `main.py` averages 50 ADC samples per reading to cut
down noise before doing this division.

**This diagram describes the hardware, not every use case.** When this
jig is clipped onto another circuit for a continuity check (§ "Reuse"
below) instead of measuring a discrete unknown resistor, there's no
physical component sitting in the `R_x` position — the "unknown
resistance" is just whatever's electrically between the two probed nodes
(a solid joint, an open break, or a forward/reverse-biased diode
junction). The same formula and the same two special-case messages in
`main.py` still apply without modification: "Short to GND or 0 Ohms"
means the two nodes are joined (continuity confirmed), "Circuit Open"
means they aren't. Only the printed `R_x` *number* is a true resistance
value in the direct-measurement case — see "Why this is safe near 0Ω" and
the diode caveat under "Reuse" below for what the reading means in each
mode.

---

## Build

1. Wire the circuit above — see `breadboard.jpg` for the as-built layout.
   The jumper chain under test goes in the `R_x` position (GPIO26 junction
   down to GND); swap in whatever unknown resistance needs measuring.
2. `mpremote run main.py` and watch the serial output — it prints the
   measured voltage and the computed `R_x` continuously.
3. If it prints "Circuit Open," `R_x` isn't actually connected to GND. If
   it prints "Short to GND," `R_x` is reading as ~0Ω.

---

## Why this is safe near 0Ω

`R_ref` (10Ω) sits between the Pico's 3V3 rail and the divider midpoint, so
even if `R_x` is a dead short to GND, the current is still limited to
3.3V / 10Ω ≈ 330mA — well inside what a Pico GPIO can source without
damage, and small enough that a genuinely low `R_x` (like the ~1Ω jumper
chain this jig was built to measure) doesn't need any additional current
limiting of its own.

---

## Reuse: continuity/troubleshooting checks on another circuit

This jig's `R_ref`/GP26/GND leads can clip onto any two-terminal node pair
on another circuit's own build instead of a dedicated unknown resistor —
that's what makes it a general-purpose continuity checker, not just a
one-off shunt-characterization tool.

**Before clipping onto a circuit that has its own power source**
(a battery pack, a PSU output): that circuit's own supply must be
disconnected first. This jig drives the node pair from the Pico's own
3V3 rail — if the node pair is still being driven by another live
source at the same time, the two supplies fight each other, the `R_x`
math is meaningless, and depending on the second source's voltage it can
also push current back into the Pico's 3V3 rail or exceed GP26's 3.3V
ceiling. Always break the other circuit's own power path (pull a
battery, unplug a PSU) before probing it this way — see
[psu_4xaa/README.md § Troubleshooting](../../power_supplies/psu_4xaa/README.md#troubleshooting)
for a worked example with a 4×AA pack.

**The `R_x` reading is only true ohmic resistance for a linear
(non-diode, non-junction) segment.** Across a genuinely resistive part
(a polyfuse, a wire, a switch contact) a low reading is a real resistance
value. Across a diode (e.g. the 1N5817 Schottky in several PSU builds
here), the Pico's 3.3V bias forward- or reverse-biases the junction
depending on which way you clip the leads — the computed "Ω" number isn't
a linear resistance in that case, but the reading still distinguishes
**conducting** (low reading, forward-biased) from **blocked** ("Circuit
Open", reverse-biased), which is exactly what a diode-orientation check
needs.
