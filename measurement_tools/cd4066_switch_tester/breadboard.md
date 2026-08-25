# Breadboard Wiring — cd4066_switch_tester

## Circuit overview

VDD → 10kΩ → I/O A → [switch under test] → I/O B → 10kΩ → GND, with the
control pin driven by a Pico GPIO and I/O B probed by another.

**Equivalent to:** `cd4066_switch_tester.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| CD4066BCN | quad bilateral switch, DIP-14 | 1 |
| Resistor | 10 kΩ | 2 |
| Dupont M-M jumper (red) | 12–20cm | 1 |
| Dupont M-M jumper (black) | 12–20cm | 1 |
| Dupont M-M jumper | 22cm | 2 |

---

## CD4066B pinout (DIP-14, per `lab/docs/parts_reference.md`)

Testing switch 1 (pins 1, 2, 13) below; the other three switches use the
same pattern on their own I/O A / I/O B / control pins.

| Pin | Function | Pin | Function |
|-----|----------|-----|----------|
| 1 | Switch 1 I/O A | 14 | VDD |
| 2 | Switch 1 I/O B | 13 | Control 1 |
| 6 | VSS (GND) | — | — |

---

## Wiring steps

### 1. Power the chip

| From | To | Wire |
|------|----|------|
| [psu_pico_rail](../../power_supplies/psu_pico_rail/) 3V3 | CD4066B pin 14 (VDD) | Red Dupont jumper |
| psu_pico_rail GND | CD4066B pin 6 (VSS) | Black Dupont jumper |

### 2. Wire I/O A and I/O B

- 10kΩ resistor from VDD rail to pin 1 (I/O A)
- 10kΩ resistor from pin 2 (I/O B) to GND rail

### 3. Wire the control and probe pins

| From | To | Wire |
|------|----|------|
| Pico GP15 | CD4066B pin 13 (Control 1) | Dupont M-M jumper |
| Pico GP26 (ADC0) | CD4066B pin 2 (I/O B) | Dupont M-M jumper |

### 4. Run and read

Run `main.py` (`mpremote run main.py`). It toggles the control pin every
second and prints the I/O B voltage alongside the commanded state — see
[README.md § Expected behaviour](README.md#expected-behaviour) for
pass/fail criteria.

---

## Testing the other 3 switches

Move the wiring from step 2/3 to the next switch's pins (switch 2: I/O A
pin 4, I/O B pin 3, control pin 5; switch 3: I/O A pin 8, I/O B pin 9,
control pin 7; switch 4: I/O A pin 11, I/O B pin 10, control pin 12), and
re-run. VDD/VSS wiring from step 1 stays the same for all four.
