# Breadboard Wiring — overvoltage_monitor

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| TL431A shunt reference, TO-92 | 1 | yes (5, untested) |
| LM358P, DIP-8 | 1 | yes (10) |
| S8050 NPN transistor, TO-92 | 1 | yes (2) |
| 3296 trimpot, 10kΩ | 1 | yes (10) |
| Red LED, 5mm | 1 | yes |
| 10kΩ resistor | 6 (four divider resistors, one to ground, `Rpu`) | yes (10) |
| 330Ω resistor | 2 (TL431 pull-up, LED) | yes (10) |
| 5.1kΩ resistor | 1 | yes (10) |
| 2kΩ resistor | 1 | yes (10) |
| 100kΩ resistor | 1 (transistor base) | yes (10) |
| 1MΩ resistor | 1 (hysteresis) | yes (10) |
| 100nF ceramic capacitor | 1 (LM358 supply only; **none** on the TL431) | yes (10) |
| Push button | 1 | yes (10) |
| Jumper wires | about 20 | yes |

Check each resistor's colour bands before it goes in; `docs/inventory.md`
records a 10kΩ bin that held a 220Ω part.

## Pinouts used

TL431A, TO-92, flat face toward you, leads down, left to right: **1 `CATHODE`,
2 `ANODE`, 3 `REF`** (TI datasheet; see `docs/parts_reference.md`).

LM358P, notch up, pin 1 top-left: 1 `OUT A`, 2 `IN− A`, 3 `IN+ A`, 4 `GND`, 5 `IN+ B`, 6 `IN− B`, 7 `OUT B`, 8 `VCC`.

S8050, flat face toward you, legs down: `E`, `B`, `C` left to right.

3296 trimpot: outer pins are the ends of the 10kΩ track, middle pin is the wiper.

Pico pins: 3V3(OUT) pin 36, GND pin 38, GP2 pin 4, GP14 pin 19, GP26 pin 31, GP27 pin 32.

## Wiring steps

Name the rows: `KA`, `T1`, `T2`, `VT`, `SENSE`, `OUT`, `BASE`, `COL`, `LED`.

### 1. Power

| From | To |
|------|----|
| Pico 3V3(OUT) (pin 36) | + rail |
| Pico GND (pin 38) | − rail |
| LM358 pin 8 | + rail; 100nF from pin 8 to pin 4 |
| LM358 pin 4 | − rail |
| LM358 pin 5 | − rail (unused half) |
| LM358 pin 6 | LM358 pin 7 (unused half) |

### 2. Reference

| From | To |
|------|----|
| 330Ω | + rail to row `KA` |
| TL431A pin 1 (`CATHODE`) | `KA` |
| TL431A pin 3 (`REF`) | `KA` (tie it to the cathode) |
| TL431A pin 2 (`ANODE`) | − rail |

The cathode (`KA`) should sit at about 2.49V (2.47–2.52V for an A-grade part).
It can't be read by `main.py` (GP27 reads `VT`, which follows it): if the
trip reference is wrong, the troubleshooting table below says what to check.

### 3. Trip reference

| From | To |
|------|----|
| 5.1kΩ | `KA` to `T1` |
| Trimpot end A | `T1` |
| Trimpot end B | `T2` |
| 2kΩ | `T2` to − rail |
| Trimpot wiper | row `VT` |
| LM358 pin 2 | `VT` |
| Pico GP27 (pin 32) | `VT` |

Turning the wiper toward end A (the 5.1kΩ end) raises `VT` and so the trip voltage.

### 4. Input divider and comparator

| From | To |
|------|----|
| The voltage to monitor (the "input") | 10kΩ → 10kΩ → 10kΩ → 10kΩ in series → row `SENSE` |
| 10kΩ | `SENSE` to − rail |
| Ground of the monitored supply | − rail (they must share it) |
| LM358 pin 3 | `SENSE` |
| Pico GP26 (pin 31) | `SENSE` |
| LM358 pin 1 | row `OUT` |
| 1MΩ | `OUT` to `SENSE` (hysteresis) |
| 10kΩ (`Rpu`) | + rail to `OUT` |
| Pico GP2 (pin 4) | `OUT` |

### 5. LED and button

| From | To |
|------|----|
| 100kΩ | `OUT` to `BASE` |
| S8050 base | `BASE` |
| S8050 emitter | − rail |
| S8050 collector | row `COL` |
| LED cathode (shorter lead) | `COL` |
| LED anode | row `LED` |
| 330Ω | `LED` to + rail |
| Push button, one leg | Pico GP14 (pin 19) |
| Push button, other leg | − rail |

## Check

```bash
mpremote run main.py
```

For the first run wire the **input** to the Pico's 3V3 pin (pin 36) — the
positive control: the 3V3 rail is a known 3.3V that any threshold above or
below it should trip or clear.

1. Turn the trimpot fully toward the 2kΩ end (lowest trip, about 1.5V) and
   press the button: `TRIP` must read OVER and the LED must be lit.
2. Turn it fully the other way (highest trip, about 8.8V) and press the button:
   `TRIP` must read clear and the LED must be dark.
3. `[PASS]` lines follow; then a live read of the monitored and trip voltages
   until Ctrl-C. Turn the trimpot until the printed trip voltage is where you
   want it; set it just under 3.3V and the LED should flip as you cross.

| Symptom | Likely cause |
|---------|--------------|
| `VT` doesn't move with the trimpot | Wiper not on the middle pin, or `T1`/`T2` ends swapped to the wrong rows |
| `VT` reads near 0V or near 3.3V | TL431A pin order wrong (check `KA` is about 2.49V: if it reads 0.7V the cathode/anode are swapped; if it reads 3.3V the TL431 isn't conducting) |
| `TRIP` never goes high | LM358 pins 2/3 swapped, or `Rpu` missing |
| `TRIP` stuck high | `OUT` shorted to the 3V3 rail, or the input divider's bottom 10kΩ missing (`SENSE` floats up) |
| LED lit when `TRIP` is clear | LED stage wired to `SENSE` or a base-to-emitter short: check `BASE` is only on the 100kΩ and the S8050 base |
| LED never lights but `TRIP` goes high | LED reversed, or S8050 pin order wrong |
| `TRIP` high level reads under 2.3V | Base resistor below 100kΩ loading `OUT` |
