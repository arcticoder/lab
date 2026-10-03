# frequency_counter

A frequency counter built on the Pico's own PWM hardware: slice 1 counts
rising edges on GP3 with no CPU involvement, a software gate opens and closes
it, and `main.py` auto-ranges from about 1Hz to tens of MHz. It is tier2
`FREQC` and the bootstrap `SIMPLECNT` in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md).
Two input paths cover what this bench produces:

- a **digital path** (10kΩ + two 1N5817 clamps) for logic signals, including
  the `ne555_astable` output (about 5V swing on `psu_4xaa`), the phase
  detector's XOR output, or anything else that is a clean 0-to-a-few-volts
  square wave;
- an **analog path** (an LM358 Schmitt trigger with a trimpot-set switching
  level) for sensor outputs that sit at a DC level, such as `TIA`, `CHGAMP`,
  `EPFIELD` and `HALLAMP`, so their vibration or modulation frequency can be
  counted.

It also closes a loop on the logic analyzer: both are crystal-referenced, so
they should agree to within the two crystals' tolerances.

**Status: designed and simulated 2026-10-02 (`smoke_test.py` green, 15
checks); not built.** Parts on hand: Pico, LM358, trimpot, 1N5817s, resistors.
`main.py` was compiled under MicroPython on the Pico and its register
accesses (counting-mode bits, pull-down, no false counts on an unconnected
pin) were checked there; the counting of a real signal has not been tried.

---

## Files

| File | Purpose |
|------|---------|
| `frequency_counter.spice` | ngspice transient netlist of both input paths: clamp levels, Schmitt switching, hysteresis, noise, trimpot range |
| `smoke_test.py` | Clamp safety, Schmitt behavior (edges counted from the simulated waveform), then `main.py` against a mocked counter with 16-bit wraparound |
| `main.py` | MicroPython: loopback self-test at 100Hz to 1MHz, then a live reading once a second |
| `breadboard.md` | Wiring for the loopback test and both input paths |

---

## Design

```
                digital path                          analog path
                                                3V3 ─10k─┐
IN_D ──10kΩ──┬──────────────► GP3                    [3296 10k pot]── wiper = Vref ──► LM358 (−)
             ├─ 1N5817 ─► 3V3 (stripe on 3V3)       GND ─5.1k─┘
             └─ 1N5817 ◄─ GND (stripe on GP3)
                                         IN_A ──10k──┬──► LM358 (+) ── out ──10k pull-up to 3V3
                                                     └─ 1MΩ feedback from out to (+)   │
                                                                            out ──10k──► the GP3 node
```

| Choice | Value | Why |
|--------|-------|-----|
| Counter | PWM slice 1, B pin (GP3), `DIVMODE` = rising edge | Counts in hardware up to the sysclock/2 range; a 16-bit counter, so the gate is chosen to reach about 60 000 counts |
| Gate | software, 1ms to 1s, measured with the microsecond timer | The count is divided by the *measured* gate, so jitter in when `main.py` stops it doesn't matter, only the timer read around each register write does (a few µs) |
| Accuracy | ±1 count over the gate | 1Hz in 1s; 0.05% at 1.5kHz; 0.0017% at 60kHz. At the fastest range (1ms gate, 60MHz) the timer's few µs matter: about 0.3% |
| Digital input | 10kΩ + 1N5817 pair | Limits clamp current to 0.25mA at 6V and keeps the pin under 3.54V |
| Pull-down | the Pico's internal one | An unconnected input reads 0Hz instead of counting noise |
| Schmitt trigger | LM358, `Rin` 10kΩ, `Rf` 1MΩ, 10kΩ pull-up | Hysteresis window of 33mV (−22mV to +11mV about the trimpot level): noise below that can't chatter it. The pull-up lifts the output from the LM358's ~1.8V ceiling to a real logic high |
| Switching level | 10kΩ + 3296 trimpot + 5.1kΩ divider, 0.67V to 1.98V | Set it to the DC level the signal sits at; keep the wiper under 1.8V, the LM358's input limit on 3.3V |

Simulated numbers:

| Quantity | Value |
|----------|-------|
| Pin voltage on a −1V to 6V, 1kHz square, through the digital path | −0.21V to 3.54V (RP2040 limits: −0.5V to 3.8V) |
| Schmitt output levels | 0.016V / 3.28V |
| 50mV-peak 1kHz sine + 8mV 100kHz noise | 18 edges in 18ms: exactly 1kHz |
| Smallest sine that toggles it (sine centred in the window) | about 19mV peak; 12mV does not |
| Noise alone | 15mV peak (30mV p-p): no chatter. 20mV peak (40mV p-p): chatters (653 edges in 18ms) |
| Trimpot range | 0.671V to 1.985V; the Schmitt toggles at both ends |

## What this does not show

- **Counting a real signal.** Rising-edge counting on a PWM B pin is documented behavior (RP2040 datasheet), and the register bits and pin setup were exercised, but no edge has been counted on this bench. The loopback test in `main.py` is the first real counting.
- **Crystal accuracy.** The loopback generator and the counter both run from the Pico's crystal, so the self-test checks counting and gating, not the absolute frequency. For that, compare with the logic analyzer (a second crystal): feed the same signal to `PB0` and run `check_capture.py`'s method, or capture it with `sigrok-cli` and read the period.
- **Speed.** The auto-range reaches the 16-bit counter's 60 000 counts down to a 1ms gate. How fast the PWM edge detector itself follows an input (the RP2040 samples it with the system clock) hasn't been measured here; treat anything above about 30MHz as untested. The 1MHz self-test point is the highest one exercised.
- **Schmitt trigger timing.** The LM358 is slow as a comparator (propagation of microseconds, slew limited): fine for kHz sensor signals, not for MHz. The model is a pure sink, so the delay isn't simulated.
- **A source impedance** adds to `Rin` (10kΩ) and widens the hysteresis window by the same ratio: a 1kΩ source adds 10%.
- **AC-coupled signals.** There is deliberately no capacitor in the analog path; see the netlist header for why a first AC-coupled version was rejected. A signal with no DC level (a bare piezo, a coil) needs a bias stage in front, such as `charge_amplifier`.
