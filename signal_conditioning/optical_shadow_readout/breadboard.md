# Breadboard Wiring — optical_shadow_readout

Build and bench-test `signal_conditioning/lockin_amplifier` first: this circuit
reuses its demodulator, and a working lock-in makes any problem here a
front-end problem.

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| LM358P, DIP-8 | 3 (`U1` TIA + gain stage, `U2` Vmid + follower A, `U3` follower B) | yes (10) |
| CD4066BCN, DIP-14 | 2 (`S1` for REF, `S2` for REFB); switch 1 of each | yes (10; switch 1 of every chip bench-tested) |
| PT334-6C photodiode | 1 | yes (10) |
| Red (or yellow, green) 5mm LED | 1 | yes |
| 10kΩ resistor | 5 (`Rm1`, `Rtb1`, `Rin`, `Rf`, `Rl1`) | yes (10) |
| 5.1kΩ resistor | 1 (`Rm2`) | yes (10) |
| 330Ω resistor | 1 (`Rtb2`) | yes (10) |
| 1kΩ resistor | 1 (LED) | yes (10) |
| 100kΩ resistor | 3 (`Rft`, `Ra`, `Rb`) | yes (10) |
| 100pF ceramic capacitor | 1 (`Cft`) | yes (assortment, 10pF–100nF) |
| 100nF ceramic capacitor | 6 (five supply decouplers, one on the TIA reference) | yes (10) |
| 1µF electrolytic capacitor | 4 (`Ca`, `Cb`, and two for `Cin`) | yes |
| Push button | 1 | yes (10) |
| Card or paper strip | 1 (the flag) | yes |
| Jumper wires | about 40 | yes |

Use the 830-point breadboard. Check each resistor's colour bands before it goes
in (`docs/inventory.md` records a 10kΩ bin that held a 220Ω part).

## Pinouts used

LM358P, notch up, pin 1 top-left: 1 `OUT A`, 2 `IN− A`, 3 `IN+ A`, 4 `GND`, 5 `IN+ B`, 6 `IN− B`, 7 `OUT B`, 8 `VCC`.

CD4066BCN, notch up, pin 1 top-left (datasheet pinout, corrected 2026-10-02): 1 switch 1 I/O A, 2 switch 1 I/O B, 5/6/12 controls of switches 2/3/4, **7 `VSS`**, 13 control 1, 14 `VDD`.

PT334-6C: the longer lead is the anode (as for the TIA, confirm against the part: a reversed photodiode reads 0V instead of a light-dependent level; swap and retry, it isn't damaged by 0.1V).

Pico pins: 3V3(OUT) pin 36, GND pin 38, GP8 pin 11, GP10 pin 14, GP11 pin 15, GP14 pin 19, GP26 pin 31, GP27 pin 32, GP28 pin 34.

## Wiring steps

Name the rows: `TB`, `TIN`, `TOUT`, `C2`, `INN`, `OUT1`, `VMR`, `VMO`, `XA`, `XB`, `A`, `B`.

### 1. Power

| From | To |
|------|----|
| Pico 3V3(OUT) (pin 36) | + rail |
| Pico GND (pin 38) | − rail |
| `U1`, `U2`, `U3` pin 8 | + rail |
| `U1`, `U2`, `U3` pin 4 | − rail |
| `S1`, `S2` pin 14 | + rail |
| `S1`, `S2` pin 7 | − rail |
| `S1` and `S2` pins 5, 6, 12 (unused controls) | − rail |
| 100nF across the supply pins of each of the five ICs | + rail to − rail |

### 2. TIA (`U1A`)

| From | To |
|------|----|
| 10kΩ (`Rtb1`) | + rail to `TB` |
| 330Ω (`Rtb2`) | `TB` to − rail |
| 100nF | `TB` to − rail |
| `U1` pin 3 | `TB` |
| `U1` pin 2 | `TIN` |
| 100kΩ (`Rft`) | `TIN` to `TOUT` |
| 100pF (`Cft`) | `TIN` to `TOUT` |
| `U1` pin 1 | `TOUT` |
| Photodiode cathode | `TIN` |
| Photodiode anode | − rail |
| `TOUT` | Pico GP28 (pin 34) |

### 3. Vmid and its buffer (`U2A`)

| From | To |
|------|----|
| 10kΩ (`Rm1`) | + rail to `VMR` |
| 5.1kΩ (`Rm2`) | `VMR` to − rail |
| `U2` pin 3 | `VMR` |
| `U2` pin 2 | `U2` pin 1 |
| `U2` pin 1 | row `VMO` (about 1.11V) |

### 4. Gain stage (`U1B`)

| From | To |
|------|----|
| 1µF + 1µF electrolytics, anti-series (the two **+** leads joined, a non-polar 0.5µF) | `TOUT` to `C2` |
| 10kΩ (`Rin`) | `C2` to `INN` |
| `U1` pin 6 | `INN` |
| 10kΩ (`Rf`) | `INN` to `OUT1` |
| `U1` pin 7 | `OUT1` |
| `U1` pin 5 | `VMO` |
| 10kΩ (`Rl1`) | `OUT1` to − rail |

### 5. Demodulator and averagers (as in `lockin_amplifier`)

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
| `U2` pin 5 | `A` |
| `U2` pin 6 | `U2` pin 7 |
| `U2` pin 7 | Pico GP26 (pin 31) |
| `U3` pin 3 | `B` |
| `U3` pin 2 | `U3` pin 1 |
| `U3` pin 1 | Pico GP27 (pin 32) |
| `U3` pin 5 | − rail |
| `U3` pin 6 | `U3` pin 7 (the unused half, parked as a follower of 0V) |

### 7. LED, flag and button

| From | To |
|------|----|
| Pico GP8 (pin 11) | 1kΩ → LED anode (the longer lead) |
| LED cathode | − rail |
| Push button, one leg | Pico GP14 (pin 19) |
| Push button, other leg | − rail |

Stand the LED and the photodiode on the breadboard about 15mm (six holes)
apart, leads bent so the two lenses face each other. The flag is a strip of
card that slides between them. Keep the TIA's input row (`TIN`), the 100kΩ
and the photodiode away from the GP8, GP10 and GP11 wires.

## Run

```bash
mpremote run main.py
```

1. The LED check runs by itself (about 4 seconds).
2. When asked, shine a phone flashlight at the photodiode and press the button.
3. Put the flag out of the beam and press the button; put it in and press again.
4. Live percentages follow until Ctrl-C.

## Expected behavior

```
LED off: VA 1.1xx VB 1.1xx TIA 0.xxxV;  LED on: VA 1.0xx VB 1.2xx TIA 0.xxxV
[PASS] the LED raises X: ... (need 10mV)
[PASS] averager nodes away from the rails: ...
[PASS] TIA not saturated: ...
[PASS] ambient light raises the TIA level: ...
[PASS] X unchanged by the ambient light: ... (limit 5%)
[PASS] the flag removes most of the LED signal: ...
 100.0% open ...
```

| Symptom | Likely cause |
|---------|--------------|
| `the LED raises X` fails with X unchanged | LED not lit (reversed, or GP8 wire off), photodiode not facing it, or the TIA row wiring: check `TOUT` on GP28 moves when the LED is covered |
| X is negative | REF/REFB swapped, or the LED's phase wrong: check GP10 on `S1` pin 13 |
| `TIA not saturated` fails | Ambient light on the photodiode is too bright (the TIA is near 1.8V): shade it, or move the LED closer and shade the photodiode |
| X rises but only a few mV | Little light reaches the photodiode: move the two closer, or use the larger gain option (README) |
| X is large (over 600mV) or the averagers sit at a rail | Too much signal for the gain: use `Rf` 10kΩ / `Rin` 10kΩ as built, or increase the LED distance |
| `X unchanged by the ambient light` fails | The TIA is saturated by the flashlight (see the line above it), or `A`/`B` electrolytics reversed |
| `flag removes` fails | Flag doesn't fully block the beam, or electrical pickup into the TIA row (move the wires), or light leaks around the flag |
