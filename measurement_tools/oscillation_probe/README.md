# oscillation_probe

A Pico ADC reader that confirms whether a node is actually **toggling**
(square wave, oscillator output) rather than sitting at a fixed DC level
— the fourth of the Pico-ADC instruments in `measurement_tools/`,
alongside [`raw_voltage_probe`](../raw_voltage_probe/),
[`resistance_measurement`](../resistance_measurement/), and
[`fuse_test_voltmeter`](../fuse_test_voltmeter/).

`raw_voltage_probe`'s averaging (50 samples, 1ms apart — a 50ms window)
is the wrong tool for this: any signal faster than a few Hz collapses
into a duty-weighted mid-voltage average that looks identical whether the
node is genuinely toggling or just stuck at that same mid-voltage (e.g.
a floating divider leg). This instead grabs 2000 raw ADC reads
back-to-back with no delay between them, then reports min/max/swing and a
zero-crossing count about the midpoint — direct evidence of toggling that
an averaged reading can't give.

Built for [oscillators/ne555_astable](../../oscillators/ne555_astable/)'s
first bench bring-up (2026-09-12) — see that circuit's `README.md` §
Validation for the worked result and what it uncovered about that
build's output divider.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — 2000 back-to-back raw ADC reads, then min/max/swing/avg and a zero-crossing count |

No `.spice`/`smoke_test.py`/`breadboard.md` here — like `raw_voltage_probe`,
this isn't a circuit with a fixed design of its own, it's a probe that
clips onto whatever circuit is under test. Wiring (which node goes to
GP26, which to GND, and what divider if any sits in front of GP26 to keep
it under 3.3V) is the calling circuit's responsibility.

---

## Usage

```bash
mpremote connect <port> run main.py
```

```
Samples: 2000 over 36873 us (~54240 sps)
GP26 min=0.000V max=3.300V avg=1.796V swing=3.300V
Zero-crossings (about mid=1.650V): 113
Rough toggle-rate estimate: ~1532 Hz (crude, aliasing-prone -- not a substitute for a real frequency counter)
```

**Reading the result:**

- **Toggling confirmed:** swing at least ~1V and crossings in the dozens
  or more over the burst window. The rough Hz estimate is aliasing-prone
  (2000 samples at ~54ksps is nowhere near a proper Nyquist-safe capture
  for a multi-kHz signal) — good enough to confirm "this is toggling in
  roughly the right ballpark," not a substitute for a real frequency
  counter (`FREQC`, not yet built — see `docs/TODO-arcticoder.md`) or the
  `SCOPEPC` soundcard path.
- **Stuck output:** swing under ~0.2V, with avg pinned near 0V or near
  the expected high level — check the fault signatures in the circuit
  under test's own `breadboard.md`/`README.md`.
- **Swing pinned at exactly 3.300V (this tool's own `V_IN`):** the ADC is
  saturating, not measuring — the true node voltage is at or above 3.3V,
  clipped. This almost always means a resistor-divider in front of GP26
  isn't actually dividing (a missing or open-circuit bottom leg is the
  usual cause) and the pin may be seeing more voltage than intended.
  **Disconnect and check the divider before probing further** — see
  `ne555_astable/README.md` § Validation for a worked example of this
  exact failure mode.
