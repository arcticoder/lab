# Breadboard Wiring — lockin_amplifier

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| LM358P, DIP-8 | 2 (`U1` gain/Vmid, `U2` followers) | yes (10) |
| CD4066BCN, DIP-14 | 2 (`S1` for REF, `S2` for REFB); use switch 1 of each | yes (10; switch 1 of every chip bench-tested) |
| 10kΩ resistor | 3 (`Rm1`, `Rin`, `Rl1`) | yes (10) |
| 5.1kΩ resistor | 1 (`Rm2`) | yes (10) |
| 1kΩ resistor | 1 (`Rbias`) | yes (10) |
| 100kΩ resistor | 2 (`Ra`, `Rb`) | yes (10) |
| 1MΩ resistor | 5 (`Rf`, one from GP8, one from GP9, two in parallel from GP6) | yes (10) |
| 1µF electrolytic capacitor (from the 16V/25V/50V kit) | 3 (`Cin`, `Ca`, `Cb`) | yes |
| 100nF ceramic capacitor | 4 (one across the supply pins of each IC) | yes (10) |
| Jumper wires | about 30 | yes |

Use the 830-point breadboard. Check each resistor's colour bands before it
goes in (`docs/inventory.md` records a 10kΩ bin that held a 220Ω part);
`measurement_tools/resistance_measurement` reads one if a band is unclear.

## Pinouts used

LM358P, notch up, pin 1 top-left: 1 `OUT A`, 2 `IN− A`, 3 `IN+ A`, 4 `GND`, 5 `IN+ B`, 6 `IN− B`, 7 `OUT B`, 8 `VCC`.

CD4066BCN, notch up, pin 1 top-left (datasheet pinout, corrected 2026-10-02):
1 switch 1 I/O A, 2 switch 1 I/O B, 3 switch 2 I/O B, 4 switch 2 I/O A, 5 control 2, 6 control 3, **7 `VSS`**, 8 switch 3 I/O A, 9 switch 3 I/O B, 10 switch 4 I/O B, 11 switch 4 I/O A, 12 control 4, 13 control 1, 14 `VDD`.

Pico pins used: 3V3(OUT) pin 36, GND pin 38, GP6 pin 9, GP8 pin 11, GP9 pin 12,
GP10 pin 14, GP11 pin 15, GP26 pin 31, GP27 pin 32.

## Wiring steps

Name the rows as you go: `VMR`, `VMO`, `SIG`, `C2`, `INN`, `OUT1`, `XA`, `XB`, `A`, `B`.

### 1. Power

| From | To |
|------|----|
| Pico 3V3(OUT) (pin 36) | + rail |
| Pico GND (pin 38) | − rail |
| `U1` pin 8, `U2` pin 8 | + rail |
| `U1` pin 4, `U2` pin 4 | − rail |
| `S1` pin 14, `S2` pin 14 | + rail |
| `S1` pin 7, `S2` pin 7 | − rail |
| `S1` pins 5, 6, 12 and `S2` pins 5, 6, 12 (unused controls: never leave them floating) | − rail |
| 100nF across each of `U1`, `U2`, `S1`, `S2` | + rail to − rail, next to the chip |

For `S1` and `S2` the supply pins are 7 pins apart (17.78mm), too far for a
100nF capacitor to bridge them directly. Put one leg in pin 14's row and the
other in the − rail hole nearest pin 14; the rail is tied to pin 7 anyway.

### 2. Vmid and its buffer (`U1B`)

| From | To |
|------|----|
| 10kΩ (`Rm1`) | + rail to `VMR` |
| 5.1kΩ (`Rm2`) | `VMR` to − rail |
| `U1` pin 5 | `VMR` |
| `U1` pin 6 | `U1` pin 7 |
| `U1` pin 7 | row `VMO` (this is Vmid, about 1.11V) |

### 3. Gain stage (`U1A`)

| From | To |
|------|----|
| `U1` pin 3 | `VMO` |
| 1kΩ (`Rbias`) | `VMO` to `SIG` |
| 1µF (`Cin`), **+ lead on `SIG`** | `SIG` to `C2` |
| 10kΩ (`Rin`) | `C2` to `INN` |
| `U1` pin 2 | `INN` |
| 1MΩ (`Rf`) | `INN` to `OUT1` |
| `U1` pin 1 | `OUT1` |
| 10kΩ (`Rl1`) | `OUT1` to − rail |

### 4. Test sources (all three go to `SIG` through resistors, nothing else)

| From | To |
|------|----|
| Pico GP8 (pin 11) | 1MΩ to `SIG` |
| Pico GP9 (pin 12) | 1MΩ to `SIG` |
| Pico GP6 (pin 9) | two 1MΩ in parallel (500kΩ) to `SIG` |

### 5. Demodulator and averagers

| From | To |
|------|----|
| `OUT1` | `S1` pin 1 and `S2` pin 1 |
| Pico GP10 (pin 14) | `S1` pin 13 (REF) |
| Pico GP11 (pin 15) | `S2` pin 13 (REFB) |
| `S1` pin 2 | 100kΩ (`Ra`) to `A` |
| `S2` pin 2 | 100kΩ (`Rb`) to `B` |
| 1µF (`Ca`), **+ lead on `A`** | `A` to − rail |
| 1µF (`Cb`), **+ lead on `B`** | `B` to − rail |

### 6. Followers and ADC wires

| From | To |
|------|----|
| `U2` pin 3 | `A` |
| `U2` pin 2 | `U2` pin 1 |
| `U2` pin 1 | Pico GP26 (pin 31) |
| `U2` pin 5 | `B` |
| `U2` pin 6 | `U2` pin 7 |
| `U2` pin 7 | Pico GP27 (pin 32) |

Keep the GP10/GP11 jumpers short and away from the `SIG`, `C2` and `INN` rows.
With the Pico on the same centre channel as the ICs, about 100mm is as short
as these two jumpers get; what matters is the route, so lay them over the
power rails, not over the `SIG`, `C2` and `INN` rows. The 2026-10-05 build
used about 100mm and read a no-signal offset of −28mV, inside the 50mV limit.

## Run

```bash
mpremote run main.py
```

It takes about 15 seconds.

## Expected behavior

```
floor                    VA 1.1xxxV  VB 1.1xxxV  VB-VA   +x.x mV
in_phase                 VA 0.9xxxV  VB 1.2xxxV  VB-VA +2xx.x mV
anti_phase               ...                     VB-VA -2xx.x mV
quadrature               ...                     VB-VA  about 0
half                     ...                     VB-VA +1xx.x mV
interferer               ...                     VB-VA  about floor
signal_plus_interferer   ...                     VB-VA  same as in_phase
[PASS] node levels near Vmid (op-amps and divider alive): ...
... eight [PASS] lines
```

The in-phase `VB-VA` should land near 260mV (anywhere from 120mV to 400mV
passes). The other lines are judged against it.

| Symptom | Likely cause |
|---------|--------------|
| `node levels` fails, both near 0V | `U2` or `U1B` unpowered, or `U2` pins 1/2 or 7/6 not tied; `U1` pin 4 or 8 not on the rails |
| `node levels` fails, both near 1.8V | `Rl1` missing or `U1A` saturated: check `Rf` is on `INN`, not `VMO` |
| `no-signal offset` fails | Clock pickup into `INN`/`SIG` (move the GP10/GP11 jumpers away), or `A`/`B` electrolytics reversed (leaky) |
| in-phase X near zero, other checks fail | GP8's 1MΩ not on `SIG`, `Cin` open, or `S1`/`S2` control wires not on pins 13 |
| in-phase X negative | REF and REFB swapped (GP10 on `S2`, GP11 on `S1`), or `U1`'s `IN+`/`IN−` swapped |
| in-phase X small (under 120mV) but other ratios right | A resistor in the gain path is the wrong value: check `Rf` (1MΩ), `Rin` (10kΩ), `Rbias` (1kΩ) |
| anti-phase doesn't flip | GP9's 1MΩ missing (the signal is only on GP8) |
| interferer alone is not near zero | `A` and `B` averagers unequal (a 100kΩ or 1µF wrong), or `S1`/`S2` skew: check both chips are CD4066B with `VDD` on pin 14 |
| `floor` row has `VB` near 0V on the first run after plugging in, then fine on the next run | The `B` averager read low in every state of that first run (0.026V at `floor`); the next two runs were normal. Seen once, 2026-10-05; if it recurs, check `Cb`'s polarity and that `U2` pins 5/6 are on the right rows |
| Sign, 90° and interferer behave, but the in-phase X is 4–5× the 260mV expected (X above 1V) and the ratio checks fail | The gain stage clips (output stops at about 1.8V and 0.02V). See "Gain too high" below |
| Everything fails at the first run on one chip pair | Swap in another CD4066B; switch 1 of every chip tested good, but `VSS` must be on pin 7 |

## Gain too high (in-phase X above about 0.6V)

Seen 2026-10-05: in-phase X +1.08V, anti-phase −1.39V, and the other states
sensible. A part in the signal path is the wrong value, or the signal is too
big going in. One jumper, then one reading.

1. Wire a jumper from row `SIG` to Pico GP28 (pin 34). Nothing else moves.
2. From this folder: `mpremote mount . run diagnose_gain.py`
3. Read the last line, `test-signal ripple on GP28`:

| Reading | Means | Next |
|---------|-------|------|
| about 3mV (2–5mV) | Source side is right; the gain stage is 4–5× too hot | Pull `Rin` and `Rf` one at a time and read each with `measurement_tools/resistance_measurement` (10kΩ and 1MΩ expected). A 2.2kΩ in `Rin`'s place gives about 4.5× |
| about 15mV (10–20mV) | The signal arriving at `SIG` is 4–5× too big | Pull `Rbias`; read it. A 5.1kΩ in place of 1kΩ gives about 5×. If `Rbias` is 1kΩ, read the `GP8` and `GP9` 1MΩ resistors (a 220kΩ in either gives about 4.5×) |
| anything else | Report the number | |

4. Fix the part, move the jumper off GP28, and run `mpremote run main.py`.
   The in-phase `VB-VA` should come to about 260mV.
