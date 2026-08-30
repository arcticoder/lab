# ammeter_1ohm

The 500mA counterpart to [ammeter_10ohm](../ammeter_10ohm/): a Raspberry
Pi Pico reading current through a polyfuse under test via a ~1Ω shunt (a
calibrated jumper-wire chain, since no 0.1Ω resistor was on hand — see
[resistance_measurement](../resistance_measurement/) for how the chain's
actual resistance was measured), plus a 1N5817 Schottky diode for
reverse-polarity protection. Built to bench-test the 20 RXEF050 (0.5A /
500mA) polyfuses in
[pico/docs/inventory.md](../../../pico/docs/inventory.md).

**Result: all 20 RXEF050 polyfuses PASS.** Each unit was swapped into the
same jig, one at a time, and confirmed to trip when shorted and recover
once the short is removed.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — reads GP26, averages ADC samples, prints current in mA |
| `breadboard.jpg` | Photo of the actual bench jig |

No `.spice`/`smoke_test.py` here — same reasoning as `ammeter_10ohm`: this
is a live diagnostic readout tool, and the pass/fail call is made by the
operator watching the current readout while manually shorting/unshorting
the load.

---

## Why ~1Ω instead of 10Ω

At 500mA, a 10Ω shunt would drop 5V — more than the whole battery pack
supplies. The shunt has to be small enough that its own voltage drop
doesn't starve the rest of the circuit. With no 0.1Ω resistor in stock
(on order from AliExpress — see
[pico/docs/inventory.md](../../../pico/docs/inventory.md) § On Order), a
short chain of jumper wires was measured instead
([resistance_measurement](../resistance_measurement/) found it to be
**~1.005Ω**) and used as the shunt. At ~1Ω, 1mV measured across the shunt
corresponds directly to 1mA — the same math `ammeter_10ohm/main.py` does,
just with `SHUNT_OHMS = 1.005` instead of `10.0`.

---

## Circuit

```
Batteries (+3V)
      │
  [ Anode ]
   1N5817 Diode
  [ Cathode (Silver Band) ]
      │
[ 500mA Polyfuse ]
      │
      ├──────────────────────────────────────────────► Pico GPIO 26 (ADC0)
      │
[ Jumper Chain shunt (~1.0Ω) ]
      │
Batteries (GND) ─────────────────────────────────────► Pico GND
```

The Schottky diode sits on the **high side**, between the battery's
positive terminal and the fuse — not in series with the shunt. This
matters: the shunt is on the low side (between the fuse and ground), so
GP26 only ever sees the voltage dropped across the ~1Ω shunt itself. The
diode's own forward drop (~0.32–0.45V at 500mA) happens earlier in the
loop and doesn't touch the shunt's voltage-to-current relationship at
all — if the diode were in series with the shunt instead, its drop would
have added a fixed offset to every reading that would need subtracting
out. Putting a low-side sense element anywhere except directly in the
sensed leg avoids that problem entirely.

At 500mA the shunt drops ~0.5V, leaving enough headroom from the 3V
battery pack (minus the diode's drop) to still drive the polyfuse into
its trip state under a dead short.

---

## Build

1. Wire the circuit above — see `breadboard.jpg` for the as-built layout.
2. `mpremote run main.py` and watch the serial output (`Current: N.N mA`).
3. With the load unshorted, confirm a steady baseline reading.
4. Short the polyfuse's downstream node to force a trip — current should
   spike well above 500mA momentarily, then the polyfuse should trip.
5. Remove the short — current should recover once the fuse cools (see
   [ammeter_10ohm](../ammeter_10ohm/)'s README for why this recovery is
   fast at low supply voltages, not a sign the fuse never really tripped).
6. Swap in the next polyfuse and repeat.
