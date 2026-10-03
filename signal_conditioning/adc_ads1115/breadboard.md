# Breadboard Wiring — adc_ads1115

## Parts required

| Component | Quantity | On hand? |
|-----------|----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 | yes |
| ADS1115 16-bit ADC module | 1 | **on order** (2026-10-02). The listing doesn't say whether the 10 header pins are soldered; if they come loose in a bag, solder them first (iron on hand; the solder wick, still to order, clears a bridge) |
| 10kΩ resistor | 3 (two divider, one `Rin`) | yes |
| 100nF capacitor | 1 | yes |
| 1N5817 Schottky diode | 2 | yes (18 untested) |
| Jumper wires | about 10 | yes |

Module pins: `VDD, GND, SCL, SDA, ADDR, ALRT, A0, A1, A2, A3`.

## Wiring steps

| From | To |
|------|----|
| Pico `3V3(OUT)` (pin 36) | Module `VDD`; top of the divider |
| Pico GND (pin 38) | Module `GND`; bottom of the divider |
| Pico GP4 (pin 6) | Module `SDA` |
| Pico GP5 (pin 7) | Module `SCL` |
| Module `ADDR` | GND (address 0x48) |
| Module `A1`, `A2`, `A3` | GND |
| Divider: 10kΩ from 3V3 to a node, 10kΩ from that node to GND | The node is the "midpoint", about 1.65V |
| Midpoint | Pico GP26 (pin 31), and one end of `Rin` (10kΩ) |
| Other end of `Rin` | Module `A0`, 100nF to GND, 1N5817 anode to `A0` with its cathode (stripe) on 3V3, 1N5817 cathode (stripe) to `A0` with its anode on GND |

Both diodes are clamps: one stripe on the 3V3 side, one stripe on the `A0` side.
A reversed clamp reads as a wrong voltage or as a short; if a diode's stripe is
worn, check its orientation with the forward-drop check in
`power_supplies/psu_low_v2/README.md` § Validation before wiring it in.
`ALRT` stays unconnected. Most modules carry I2C pull-ups; if the scan is empty,
add 5.1kΩ from SDA and from SCL to 3V3.

## Run

```bash
mpremote run main.py
```

## Expected behavior

```
[PASS] ADS1115 answers at 0x48: scan found ['0x48']
[PASS] ADS1115 reads the divider midpoint: 1.64xxV vs 1.65V ±10%
[PASS] ADS1115 and Pico ADC agree: ... difference a few mV (limit 30mV)
[PASS] ADS1115 reading is steady: std well under 1000µV
```

| Result | Meaning |
|--------|---------|
| scan finds nothing | SDA/SCL swapped, no VDD/GND, or no pull-ups on the module |
| scan finds another address | `ADDR` not tied to GND (VDD → 0x49, SDA → 0x4A, SCL → 0x4B); change `ADDR` in `main.py` or the wire |
| reading near 0V | `A0` not connected, `Rin` open, or a clamp diode reversed |
| ADS and Pico disagree by more than 30mV | Divider midpoint wire on the wrong pin, or the Pico ADC offset is larger than assumed — report both numbers |
| ADS std above 1mV | Loose breadboard contact on the `A0` node, or noise from a nearby motor or switching supply |
