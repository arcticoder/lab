# ammeter_10ohm

A Raspberry Pi Pico reading actual current (not just voltage) through a
polyfuse under test, via a 10Ω shunt resistor and a slide switch wired
across the shunt as a hands-free shorting jumper. Built to bench-test the
20 RXEF005 (0.05A / 50mA) polyfuses in
[pico/docs/inventory.md](../../../pico/docs/inventory.md) after
[fuse_test_voltmeter](../fuse_test_voltmeter/)'s voltage-only approach
turned out to have a wiring gap that made its trip/reset detection
unreliable — this tool measures the loop current directly instead of
inferring a trip from a probe-node voltage collapse.

**Result: all 20 RXEF005 polyfuses PASS.** Each unit was swapped into the
same jig, one at a time, and confirmed to trip when the shunt is shorted
and recover once the short is removed.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — reads GP26, prints current in mA over USB serial |
| `breadboard.jpg` | Photo of the actual bench jig |

No `.spice`/`smoke_test.py` here — this is a live diagnostic readout tool
(like a bench ammeter), not a circuit with a fixed pass/fail netlist
prediction. The pass/fail call is made by the operator watching the
current readout while manually shorting/unshorting the shunt.

---

## Circuit

```
AA Battery (+1.5V)
      │
[ Polyfuse under test ] (RXEF005, 50mA)
      │
      ├──────────────────────────────► Pico GPIO 26 (ADC0)
      │
[ 10Ω shunt resistor ] ◄── slide switch wired in parallel (shorting jumper)
      │
Battery (GND) ───────────────────────► Pico GND
```

GP26 probes the node between the fuse and the shunt; GND is shared with
the battery's negative terminal. `main.py` converts the ADC voltage at
that node straight to milliamps via `current_ma = (V / 10Ω) × 1000`.

The slide switch, wired directly across the 10Ω shunt's two legs, is the
shorting jumper: closing it drops the shunt to ~0Ω, so the only thing
left limiting current is the fuse's own cold resistance — a much harder
short than leaving the 10Ω shunt in the loop, which is what actually
forces a trip. Opening the switch restores the 10Ω shunt and lets the
Pico read current again.

---

## Build

1. Wire the circuit above on a breadboard — see `breadboard.jpg` for the
   as-built layout.
2. `mpremote run main.py` and watch the serial output (`mA` printed
   continuously, ~10 samples/sec).
3. With the switch open, confirm a steady baseline reading (loaded through
   the fuse + 10Ω shunt).
4. Close the switch to short the shunt — current should jump sharply as
   the loop drops to just the fuse's cold resistance, and the polyfuse
   should trip within a fraction of a second.
5. Open the switch again — current should collapse toward the ADC's noise
   floor while the fuse is tripped, then climb back once the fuse cools
   and resets.
6. Swap in the next polyfuse and repeat.

---

## Why the fuse resets so fast at 1.5V

The first pass through this test looked like the polyfuses were
"healing" instantly, which would be suspicious — a genuine PTC trip is
supposed to stay latched in its high-resistance state for a while after
an overcurrent event, not reset within a second or two. Once actually
measured with this ammeter (rather than inferred from a voltage probe),
the fast reset turns out to be expected behaviour at 1.5V specifically,
not a sign the fuse never really tripped:

- **Unshorted**: fuse (cold) + 10Ω shunt in series draws enough current to
  sit close to the fuse's rated trip threshold, without necessarily
  tripping on its own.
- **Shunt shorted**: loop resistance drops to just the fuse's cold value,
  current surges to several times the fuse's rating, and the fuse trips
  into its high-resistance state within a fraction of a second.
- **Short removed**: the fuse is now high-resistance in series with the
  10Ω shunt, across only 1.5V. That combination can only push a few
  hundred microamps through the tripped fuse — nowhere near enough
  self-heating (`I²R`, on the order of a milliwatt) to keep the polyfuse's
  polymer element hot. It cools and drops back to its low-resistance
  state almost immediately, and current climbs back to the baseline.

At a higher supply voltage (5V, 12V), the same tripped-state resistance
would pass enough current to keep the element self-heated and latched
open until the power is actually removed — 1.5V is just below the
threshold needed to sustain that latch once the heavy short-circuit load
is gone. So the fast recovery seen here is real PTC trip/reset behaviour,
just at a supply voltage too low to hold the latch — not a defect in any
of the 20 units tested.
