# Breadboard Wiring — hall_amplifier

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| SS49E / 49E Hall sensor, TO-92 | 1 | **no** — 15 on order (2026-10-02, `docs/orders.md`) |
| LM358P, DIP-8 | 1 (`U1`) | yes (10) |
| 3296 trimpot, 10kΩ | 1 | yes (10) |
| 10kΩ resistor | 8 (3 above the trimpot, 3 below, `Rinp`, `Rinn`) | yes (10: leaves two spare) |
| 100kΩ resistor | 2 (`Rfp`, `Rfn`) | yes (10) |
| 5.1kΩ resistor | 1 | yes (10) |
| 2kΩ resistor | 1 | yes (10) |
| 100nF ceramic capacitor | 2 (sensor supply, LM358 supply) | yes (10) |
| Jumper wires | about 20 | yes |
| A magnet | 1 | **no** — see `docs/TODO-arcticoder.md` "Next order" |

Check each resistor's colour bands before it goes in; `docs/inventory.md`
records a 10kΩ bin that held a 220Ω part.

## Pinouts used

SS49E, TO-92, flat face (the printed side) toward you, leads down, left to
right: **`VCC`(+), `GND`, `OUT`** (the datasheet's drawing labels them +, −, 0).
The 49E clones are normally the same, but this is the one thing to confirm
from the datasheet picture against the physical part. The datasheet allows a
supply of −5V, so swapping the outer two leads is survivable; check after
power-up that the sensor stays cool anyway (touch test, a few seconds).

LM358P, notch up, pin 1 top-left: 1 `OUT A`, 2 `IN− A`, 3 `IN+ A`, 4 `GND`, 5 `IN+ B`, 6 `IN− B`, 7 `OUT B`, 8 `VCC`.

3296 trimpot: the two outer pins are the ends of the 10kΩ track, the middle pin is the wiper.

## Wiring steps

Name the rows as you go: `HALL`, `VP`, `VM`, `VN`, `VR`, `WIP`, `OUT`.

### 1. Power

| From | To |
|------|----|
| Pico 3V3(OUT) (pin 36) | + rail |
| Pico GND (pin 38) | − rail |
| `U1` pin 8 | + rail; 100nF from pin 8 to pin 4 |
| `U1` pin 4 | − rail |
| Sensor pin `VCC` | + rail; 100nF from `VCC` to `GND` at the sensor |
| Sensor pin `GND` | − rail |

### 2. Null reference (`U1B`)

| From | To |
|------|----|
| 10kΩ ×3 in series | + rail to trimpot end A |
| Trimpot end B | 10kΩ ×3 in series to − rail |
| Trimpot wiper | row `WIP`, and `U1` pin 5 |
| `U1` pin 6 | `U1` pin 7 |
| `U1` pin 7 | row `VN` |

### 3. Output reference and amplifier (`U1A`)

| From | To |
|------|----|
| 5.1kΩ | + rail to row `VR` |
| 2kΩ | `VR` to − rail |
| Sensor `OUT` | row `HALL` |
| 10kΩ (`Rinp`) | `HALL` to `VP` |
| 100kΩ (`Rfp`) | `VP` to `VR` |
| `U1` pin 3 | `VP` |
| 10kΩ (`Rinn`) | `VN` to `VM` |
| 100kΩ (`Rfn`) | `VM` to `OUT` |
| `U1` pin 2 | `VM` |
| `U1` pin 1 | `OUT` |
| Row `OUT` | Pico GP26 (pin 31) |

Keep the magnet and any steel tools away from the sensor while the circuit is
being nulled. Don't set the Pico's USB cable's ferrite or a phone next to it.

## Run

```bash
mpremote run main.py
```

1. The `NULL` lines print the output every 0.1s. Turn the trimpot until they
   read `on target` (0.94V ±15mV) and keep them there for 3s.
2. `[PASS] zero-field noise` should follow, with a std of well under 3mV.
3. `Live reading.` prints the field in gauss every 0.2s. Bring a magnet slowly
   toward the sensor's flat face from 5cm: the reading rises or falls
   smoothly with distance and flips sign with the magnet reversed.

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| `NULL` stuck at 0.02V | `U1` unpowered, `U1A`'s inputs swapped, or the sensor's `OUT` isn't on `HALL` |
| `NULL` stuck at 1.8V and the trimpot does nothing | `Rfn` not on `OUT`, or `U1B` (pins 5–7) wrong |
| Reaches the target only at one extreme of the trimpot, then falls off | A sensor whose zero-field output is above about 1.8V; swap in another of the 15 |
| `NULL` target reached but `noise` fails | Loose breadboard contact on `HALL`/`VP`; a nearby moving magnet, a motor or a switching supply; USB cable moving |
| Reading drifts steadily for minutes | Sensor warming up (null drifts about 16mV/°C at the output); let it settle |
| Sensor hot to the touch | Wrong pin order. Unplug at once |
| Live reading doesn't change with a magnet | Sensor's flat face turned away from the magnet's axis, or a latching/switch part from the SS49E listing (40AF/41F) instead of a linear one: a linear part reads half of `VCC` with no magnet |
