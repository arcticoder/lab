# overvoltage_monitor

A hardware overvoltage trip: it compares a monitored voltage (0 to about
9V, trimpot-set threshold from 1.5V to 8.8V) with a TL431 reference through an
LM358 comparator, lights an LED through a transistor, and drives a `TRIP`
line the Pico (or a later shutdown stage) can read. It works without the
Pico's software: the comparator, reference and LED need only 3V3. This is
safety `OVERVOLT` ("Overvoltage Monitor & Shutdown Signal") in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md),
built from parts on hand, and the first use of the TL431A batch.

**Status: designed and simulated 2026-10-02 (`smoke_test.py` green, 22
checks); not built.** `main.py` was compiled under MicroPython on the Pico;
its logic was run against mocks only.

**It is a monitor, not a protector, and it is not fail-safe**: see "What this
does not show". It disconnects nothing.

---

## Files

| File | Purpose |
|------|---------|
| `overvoltage_monitor.spice` | ngspice netlist: reference, trip ladder, divider, comparator with hysteresis, LED stage. Case parameters: trimpot position, TL431 error, monitored voltage, rail, transistor gain |
| `smoke_test.py` | Bias, logic-level and LED checks; swept trip/release thresholds; TL431 tolerance; the 3V3-rail positive control; then `main.py`'s checks against healthy and broken readings |
| `main.py` | MicroPython: end-to-end check of the trimpot's two ends against `TRIP`, then a live read |
| `breadboard.md` | Wiring, the positive-control procedure and failure table |

---

## Design

```
3V3 ─330Ω─┬── TL431A cathode (pin 1), REF (pin 3) tied to it, anode (pin 2) to GND   = 2.495V, 2.4mA
          └─ 5.1k ─┬─[ 10kΩ trimpot, wiper = Vt ]─┬─ 2k ─ GND     Vt = 0.29V to 1.75V ──► LM358 (−)  and GP27
                   └──────────────────────────────┘
Vin ─10k─10k─10k─10k─┬── SENSE = 0.2 × Vin ──► LM358 (+) and GP26
                     └─ 10k ─ GND                  │ 1MΩ from OUT to (+) = hysteresis
                                                   │
        3V3 ─ 10k ─┬── OUT (LM358 pin 1, sinks to ground when clear) ──► GP2 (TRIP: high = over)
                   └─ 100k ─ S8050 base ; collector ─ LED ─ 330Ω ─ 3V3
```

Trip voltage = `Vt / 0.2`: **1.46V to 8.75V**, set by turning the trimpot (toward the 5.1kΩ end raises
it). The comparator releases about 126mV below the trip point.

| Choice | Value | Why |
|--------|-------|-----|
| Reference | TL431A on 3V3 through 330Ω | 2.44mA is above its 1mA minimum with margin: it still regulates down to a 2.83V rail. 2.495V ±1% (A grade, per TI's datasheet). Nothing else on the cathode: a capacitor can make it oscillate |
| Trip reference | divided down to 0.29–1.75V | The LM358's input range ends near 1.8V on 3.3V, so the 2.495V reference can't go to the comparator directly |
| Input divider | 4 × 10kΩ over 10kΩ (0.2) | A 9V input puts 1.8V on the comparator, the top of its range; the divider draws 0.18mA from the monitored rail at 9V |
| Hysteresis | 1MΩ feedback, 126mV at the input | Keeps a rail that hovers at the threshold from chattering the LED and `TRIP` |
| Output | open-collector style: LM358 sinks, 10kΩ pulls up | The LM358 alone can't output above 1.8V on 3.3V, which is not a logic high; the pull-up makes `TRIP` a real 3.05V |
| LED stage | S8050, 100kΩ base, 330Ω + LED | A 1kΩ base resistor was tried first and held the tripped `TRIP` line at 0.92V (below a logic high); at 100kΩ it sits at 3.05V and the LED still gets 4.0mA (1.4mA with a low-gain transistor) |

Simulated numbers:

| Quantity | Value |
|----------|-------|
| Trip voltage at the trimpot's ends / middle | 1.47V / 5.15V / 8.83V (formula `2.495 × (2k + pos × 10k) / 17.1k / 0.2` within 1%) |
| Release at the middle setting | 5.02V (126mV hysteresis) |
| TL431A at ±1% | moves the trip by ±1% |
| TRIP line | 3.05V tripped, 16mV clear |
| LED | 4.0mA tripped (1.4mA at hFE 60), 5pA clear |
| TL431 current | 2.44mA at 3.3V, 1.53mA at 3.0V, 1.02mA at 2.83V |
| Set for 3.0V | trips on the 3.3V rail; clear at 2.8V |

## What this does not show

- **Not fail-safe.** It is powered from 3V3. If that rail drops out, the LED is off and `TRIP` reads low, which looks like "voltage OK". A shutdown that must act on loss of the monitor needs the opposite polarity (a healthy-line that has to be held high), which this design doesn't provide. Below a 2.83V rail the reference stops regulating and the trip point drifts.
- **Absolute accuracy.** The trip voltage is `Vt / 0.2`, where 0.2 comes from five 10kΩ resistors of unknown tolerance (±5% if they are 5% parts) and `Vt` from the TL431A's ±1% (`docs/inventory.md`'s resistor kit does not state a grade). The numbers `main.py` prints use the nominal 0.2. To set a real threshold, trip it on a voltage you trust and adjust the trimpot to that.
- **Speed.** An LM358 comparator with 1MΩ of hysteresis responds in tens of microseconds to milliseconds. It is a rail monitor, not a spike detector.
- **It disconnects nothing.** No crowbar, relay or series switch. The `TRIP` line is a signal; what acts on it is a later design (`ACTIVELIM`'s MOSFET is the nearest part, and is itself deferred).
- **Input range.** Valid from 0V to about 9V. Above that the comparator's input leaves its range and, for the LM358, keeps reading "over", which is the safe side. The LM358's own input limit is far higher, so a 20V rail won't damage it, but nothing here has been tested above 9V.
- **TL431 parts untested.** None of the five on hand has been run; this circuit is the first. If its cathode doesn't read about 2.49V, check the pin order (`docs/parts_reference.md`) before blaming the part.
