# Breadboard Wiring — frequency_counter

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| 10kΩ resistor | 2 for the digital path and the self-test; 2 more (`Rpu`, `Rin`) for the analog path | yes (10) |
| 1N5817 Schottky diode | 2 | yes (18 untested) |
| LM358P (analog path only) | 1 | yes (10) |
| 1MΩ resistor (analog path only) | 1 | yes (10) |
| 3296 trimpot, 10kΩ (analog path only) | 1 | yes (10) |
| 5.1kΩ resistor (analog path only) | 1 | yes (10) |
| 100nF ceramic capacitor (LM358 supply) | 1 | yes (10) |
| Jumper wires | about 10 | yes |

Build the digital path and run the self-test first; add the analog path only
when there is a sensor to count.

## 1. Digital path and loopback self-test

Both 1N5817s sit on the GP3 side of the 10kΩ resistor. A stripe marks the
cathode.

| From | To |
|------|----|
| Pico GP16 (pin 21) | 10kΩ `Rd` → row `IN` |
| Row `IN` | Pico GP3 (pin 5) |
| 1N5817 #1 anode | row `IN` |
| 1N5817 #1 cathode (stripe) | Pico 3V3(OUT) (pin 36) |
| 1N5817 #2 cathode (stripe) | row `IN` |
| 1N5817 #2 anode | Pico GND (pin 38) |

Hold off on trusting a diode whose stripe has worn off: a reversed clamp sinks
current into the pin. `power_supplies/psu_low_v2/README.md` § Validation
describes the forward-drop check.

To count an external logic signal later, take the wire from GP16 off the 10kΩ
and put the signal there instead, with its ground tied to the Pico's GND.

```bash
mpremote run main.py
```

Expected (about 6 seconds, then a live reading until Ctrl-C):

```
[PASS] idle input reads no signal: None
[PASS] 100Hz measured as 100.00Hz: error 0.000% (limit 1.500%); 100 counts in 1.000s
[PASS] 1000Hz measured as 1000.00Hz: ...
[PASS] 12345Hz measured as 12345.xxHz: ...
[PASS] 100000Hz measured as 100000.xxHz: ...
[PASS] 1000000Hz measured as 1000000.xxHz: ...
Measuring the input once a second. Ctrl-C to stop.
```

| Result | Meaning |
|--------|---------|
| `idle input` fails (reads a frequency with the generator off) | GP3 picks up noise: the wire from GP16 isn't on the `IN` row's resistor, or GP3's pull-down didn't apply |
| Every frequency reads `no signal` | GP16 → 10kΩ → `IN` → GP3 not complete, or a clamp diode reversed (clamps the signal to 0V) |
| 100kHz and 1MHz fail, lower ones pass | 10kΩ + pin and breadboard capacitance too slow for the edge; shorten the wires |
| All fail by the same percentage | Timer/gate problem: report the numbers |

## 2. Analog path (LM358 Schmitt trigger)

LM358P, notch up, pin 1 top-left: 1 `OUT A`, 2 `IN− A`, 3 `IN+ A`, 4 `GND`, 8 `VCC`. Only half A is used; tie the unused half's `IN+` (5) to GND, `IN−` (6) to `OUT B` (7).

| From | To |
|------|----|
| Pico 3V3(OUT) | LM358 pin 8; 100nF from pin 8 to pin 4 |
| Pico GND | LM358 pin 4 |
| LM358 pins 5 | GND; pin 6 to pin 7 |
| 10kΩ | 3V3 to trimpot pin 1 (an outer pin) |
| Trimpot pin 3 (other outer pin) | 5.1kΩ to GND |
| Trimpot pin 2 (middle, the wiper) | LM358 pin 2 (`IN−`, the switching level `Vref`) |
| Signal in | 10kΩ (`Rin`) to LM358 pin 3 (`IN+`) |
| 1MΩ (`Rf`) | LM358 pin 1 (`OUT`) to pin 3 |
| 10kΩ (`Rpu`) | LM358 pin 1 to 3V3 |
| LM358 pin 1 | 10kΩ → row `IN` (the same row as in step 1; remove the GP16 wire) |
| Signal ground | Pico GND |

Set the level: with the signal source running, turn the trimpot until the
`main.py` reading shows the signal's frequency; the correct range spans the
signal's DC level (slightly below it works best). Measure `Vref` first if in
doubt: `measurement_tools/raw_voltage_probe/` on the wiper reads it.

| Symptom | Likely cause |
|---------|--------------|
| Reads `no signal` for any trimpot position | Signal swing under about 33mV peak-to-peak, or the wiper range misses the signal's DC level |
| Reads a frequency that jumps around | Signal noise exceeds the 33mV hysteresis window: filter it or add gain first |
| Reads double or much higher than expected | Chatter on a slow edge: noise bigger than the window; reduce source noise |
| Output stuck high | Signal's DC level far below the wiper setting |
