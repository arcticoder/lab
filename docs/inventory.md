# Component Inventory

Parts available from the **SunFounder Thales Kit** and other sources.
Update quantities as components are used or added.

Moved here from `pico/docs/inventory.md` on 2026-09-07 — this repo (`lab/`)
is where most of the ordering/build work referencing it happens day to
day. `pico/docs/inventory.md` is now a one-line pointer back to this file,
kept so `pico/`'s own generic circuit BOMs still resolve a path without
requiring `lab/` to be cloned alongside it — see
[kb/repo_docs_conventions.md](kb/repo_docs_conventions.md).

---

## LEDs

| Component  | Quantity |
|------------|----------|
| Red LED    | 10       |
| Blue LED   | 10       |
| Green LED  | 10       |
| White LED  | 10       |
| Yellow LED | 10       |
| RGB LED    | 1        |

---

## Resistors

All values below are the SunFounder Thales kit's standard **1/4W (0.25W)**
axial resistors — the kit does not include any higher-wattage part. No
value/quantity row here is individually rated ≥1W; a circuit needing more
than ~0.2W of continuous dissipation at a given value needs a
series/parallel network of these to spread the load, not a single
higher-wattage part pulled from this table. See
`lab/measurement_tools/fuse_test_voltmeter/breadboard.md` for a worked
example (RXEF050 tier's 10 Ω test load).

| Value   | Quantity |
|---------|----------|
| 10 Ω    | 10       |
| 100 Ω   | 10       |
| 220 Ω   | 10       |
| 330 Ω   | 10       |
| 1 kΩ    | 10       |
| 2 kΩ    | 10       |
| 5.1 kΩ  | 10       |
| 10 kΩ   | 10       |
| 100 kΩ  | 10       |
| 1 MΩ    | 10       |

---

## Active Components and Sensors

| Component                     | Quantity | Notes                              |
|-------------------------------|----------|------------------------------------|
| S8550 Transistor (PNP)        | 2        |                                    |
| S8050 Transistor (NPN)        | 2        |                                    |
| Tilt Switch                   | 1        |                                    |
| Potentiometer                 | 1        |                                    |
| 100 nF Capacitor              | 10       |                                    |
| 10 nF Capacitor               | 10       |                                    |
| Photoresistor (LDR)           | 2        |                                    |
| Thermistor (NTC)              | 1        | Suspect faulty — prefer photoresistor for initial analog experiments |
| 9G Servo                      | 1        |                                    |
| PIR Motion Sensor             | 1        |                                    |
| 74HC595 Shift Register        | 1        |                                    |

---

## Output and Interface

| Component               | Quantity | Notes                        |
|--------------------------|----------|------------------------------|
| Passive Buzzer          | 1        |                              |
| Active Buzzer           | 1        |                              |
| 7-Segment Display       | 1        |                              |
| I2C LCD 1602            | 1        |                              |
| WS2812 RGB LED Strip    | 1        | 8-LED strip                  |
| Slide Switch            | 5        | 3-pin SPDT slide switch (SunFounder Thales kit part). Pin 2 (middle) is the fixed/common contact; sliding the bar left connects pin 2 to pin 1, sliding it right connects pin 2 to pin 3 — one throw is always made, never both open at once. No printed pin markings; identify pin 2 by continuity/position (it's the one that stays connected across both slide directions) rather than by probing for a floating pin. Used as an ARMED/DISARMED signal switch (pin 2 to a GPIO with the GPIO's internal pull-down enabled, pin 1 to 3V3, pin 3 left unconnected — only one throw is ever wired to a rail, since the switch never bridges both outer pins at once, so wiring the second outer pin to GND would do nothing but invite a bridging risk for no benefit; the GPIO reads a defined HIGH on the 3V3 throw and a defined pulled-down LOW on the unconnected throw) in `lab/measurement_tools/fuse_test_voltmeter/`, gating trip/reset detection so manually connecting/disconnecting the battery under test isn't misread as a fuse trip. |
| Push Button             | 10       | Used as a "ready" signal (Pin.PULL_UP, active-low) in circuits that need to pause mid-run for a physical action — `mpremote run` can't forward keystrokes for `input()`, so a hardcoded countdown was the old workaround; a button removes the time pressure. See `lab/signal_conditioning/voltage_reference_lm358/` |

---

## Prototyping and Cables

| Component              | Quantity | Notes                                                    |
|--------------------------|----------|-------------------------------------------------------------|
| Breadboard (full)      | 1        | 830-point                                                 |
| Breadboard (mini SYB-170) | 1     | 170-point, black; from a 6-in-1 color pack (AliExpress). See `lab/docs/orders.md` / `lab/docs/parts_reference.md` for full specs |
| Micro USB Cable        | 1        | For Pico power + data                                     |

---

## Jump Wires (solid-core, pre-bent 90°)

### Jump Wires Box — Left Side

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Orange | 2.25        | 14       |
| Red    | 2.5         | 10       |
| Black  | 1.5         | 14       |

### Jump Wires Box — Middle Left

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| White  | 1.5         | 14       |
| White  | 5           | 10       |
| Yellow | 2           | 12       |

### Jump Wires Box — Middle Right

| Colour      | Length (cm) | Quantity |
|-------------|-------------|----------|
| Black       | 0.4         | 10       |
| Yellow      | 0.6         | 10       |
| Green       | 1.0         | 10       |
| Blue        | 1.25        | 10       |
| Non-covered | 0.25        | 13       |

### Jump Wires Box — Middle Top

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Green  | 7.5         | 10       |
| Blue   | 10          | 10       |

### Jump Wires Box — Middle Bottom

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Red    | 12.6        | 10       |

---

## Jumper Wires (M-M Dupont, pre-cut)

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Blue   | 16          | 2        |
| Red    | 16          | 2        |
| Black  | 16          | 2        |
| Red    | 20          | 1        |
| Blue   | 20          | 1        |
| White  | 20          | 1        |
| Blue   | 25          | 1        |
| White  | 25          | 1        |
| Red    | 25          | 1        |
| Black  | 25          | 1        |
| White  | 12          | 7        |
| Black  | 12          | 7        |
| Orange | 12          | 7        |
| Blue   | 12          | 7        |
| Green  | 12          | 7        |
| Yellow | 12          | 7        |
| Red    | 12          | 7        |

---

## Dupont Wires (M-F)

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Red    | 22          | 1        |
| Yellow | 22          | 1        |
| Grey   | 22          | 1        |
| Orange | 22          | 1        |
| Green  | 22          | 1        |
| Blue   | 22          | 1        |
| Purple | 22          | 1        |
| Black  | 22          | 1        |
| White  | 22          | 1        |
| Beige  | 22          | 1        |
---

## Microcontroller

| Component              | Quantity | Notes                         |
|------------------------|----------|-------------------------------|
| Raspberry Pi Pico      | 1        | RP2040, no wireless           |

---

## Power Supply & Protection Components

For the `lab/` repo's spacetime research PSU tiers (`psu_ultralow`,
`psu_low`). Full specs and datasheets in `lab/docs/orders.md` and
`lab/docs/parts_reference.md`.

| Component                              | Quantity | Notes                                                           |
|------------------------------------------|----------|--------------------------------------------------------------------|
| Polyfuse RXEF005 (0.05A / 50mA)         | 20       | Received 2026-08-21; validated 2026-08-30 — all 20 units PASS (trip + reset confirmed) via `lab/measurement_tools/ammeter_10ohm/`, superseding the earlier `fuse_test_voltmeter` voltage-probe approach |
| Polyfuse RXEF050 (0.5A / 500mA)         | 20       | Received 2026-08-21; validated 2026-08-30 — all 20 units PASS (trip + reset confirmed) via `lab/measurement_tools/ammeter_1ohm/` |
| 1N5817 Schottky diode (1A 20V, DO-41)   | 20       | Received 2026-08-21; untested — verify forward drop/orientation per unit before use in `psu_low_v2` |
| AA battery holder (1×AA, single-cell)  | 5        | Received 2026-08-21; ready for direct use in `psu_ultralow_v1`/`psu_low_v2`. Confirmed-working temporary lead termination (2026-08-28, ahead of the wire stripper order arriving): twist a non-covered 0.25cm jump wire around each bare holder lead and wrap in electrical tape — no soldering/crimping needed. Treat as a stand-in until leads are stripped/soldered to Dupont connectors, not a wiring defect if seen on a breadboard. |

---

## Prototyping, Analog ICs & Test Equipment

For the `lab/` repo's spacetime research build. Full specs and datasheets
in `lab/docs/orders.md` and `lab/docs/parts_reference.md`.

| Component                              | Quantity | Notes                                                           |
|------------------------------------------|----------|--------------------------------------------------------------------|
| Breadboard (mini SYB-170, 2pk)         | 2        | Received 2026-08-24; separate listing from the black SYB-170 already in "Prototyping and Cables" above |
| Breadboard (MB-102, 400-point)         | 1        | Received 2026-08-24; 300 terminal + 100 distribution-bar tie points |
| CD4066BCN (quad bilateral switch, DIP-14) | 10    | Received 2026-08-24; analog switch/mux — see `lab/measurement_tools/cd4066_switch_tester/` for the per-unit bring-up check before trusting one in a downstream design. All 10 units' switch 1 (I/O A pin 1 / I/O B pin 2 / control pin 13) bench-tested PASS 2026-08-28 after an earlier FAIL was root-caused to DIP pin misidentification, not a bad chip — see `lab/docs/parts_reference.md` for the correct pinout before wiring. Switches 2–4 on each chip are not yet individually tested. |
| LM358P (dual op-amp, DIP-8)            | 10       | Received 2026-08-24; budget op-amp for bring-up circuits — see `lab/signal_conditioning/voltage_reference_lm358/` |
| TYPE-C Female Test Board (USB3.1 16P → 2.54mm) | 1 | Received 2026-08-24; blue variant, pads `CC2, D+, D-, SBU1, SBU2, CC1, VBUS, GND` per `lab/docs/parts_reference.md#usb-c-16-pin-test-breakout-board` |
| Fuse holder, panel-mount (6×30mm, 10A/250V)   | 1        | Received 2026-09-01; EGBO panel-mount socket, opening 12/14mm, rated 10A/250V. Pairs with the 2A glass fuse below for the `psu_medlow` protection tier. See `lab/docs/parts_reference.md#panel-mount-fuse-holder` |
| NE555 timer IC (DIP-8)                        | 10       | Received 2026-09-01; untested/not yet validated per-unit — no per-unit test jig built yet for this bulk IC batch. Astable `OSC` design (`lab/oscillators/ne555_astable/`) simulated 2026-09-01, not yet bench-built — that build will double as the first per-unit validation. Also candidate for tier2 `FREQC` (frequency counter). See `lab/docs/parts_reference.md#ne555-timer` |
| Glass tube fuse, 6×30mm 250V 2A (fast-blow)   | 10       | Received 2026-09-01; untested/not yet validated per-unit — no per-unit test jig built yet for this bulk consumable-fuse batch. Pairs with the panel-mount holder above for `psu_medlow`. See `lab/docs/parts_reference.md#glass-tube-fuses-6x30mm` |
| 3296 trimming potentiometer, 10 kΩ            | 10       | Received 2026-09-01; single-turn cermet trimmer (listing's "multi-turn" claim not yet verified against the physical part). Used as Rb (0-10kΩ, wired as a glitch-safe 2-terminal rheostat) in the `lab/oscillators/ne555_astable/` tier1 `OSC` design (simulated 2026-09-01, not yet bench-built) alongside the NE555 batch above. See `lab/docs/parts_reference.md#3296-trimming-potentiometer` |
| TL431A precision shunt reference (TO-92)      | 5        | Received 2026-09-01; untested. Adjustable 2.5–36V bandgap reference — candidate alternative/upgrade to the LM358 divider-buffer for tier1 `REF`; needs an external pull-up/current source into Cathode (sink-only device). See `lab/docs/parts_reference.md#tl431a-precision-shunt-reference` |
| Metal film resistor, 1% 1W, 0.1Ω              | 20       | Received 2026-09-03; untested. Not a random assortment pull — the AliExpress listing offers an assortment of values to choose from, and this was one of two values specifically selected (20 units each; see the 1Ω row below), no other values included. Intended to replace the jumper-wire-chain shunt currently used in `lab/measurement_tools/ammeter_1ohm/` (see `lab/measurement_tools/resistance_measurement/`) with an actual resistor; also 1W-rated, above the SunFounder Thales kit's 1/4W ceiling. See `lab/docs/parts_reference.md#metal-film-resistor-kit-1w-1`. |
| Metal film resistor, 1% 1W, 1Ω                | 20       | Received 2026-09-03; untested. The second of the two specifically-selected values from the same listing/order as the 0.1Ω row above (not a separate order). Not yet assigned to a tier — candidate reference resistor for a tier3 `OHMMETER` (4-wire Kelvin) build alongside the 0.1Ω value. See `lab/docs/parts_reference.md#metal-film-resistor-kit-1w-1`. |
| PT334-6C photodiode (5mm)                     | 10       | Received 2026-09-03; untested. Silicon PIN photodiode — candidate for a tier2 `TIA` (transimpedance amplifier) build alongside the on-hand LM358P. See `lab/docs/parts_reference.md#pt334-6c-photodiode`. |
| Multilayer ceramic capacitor assortment, 50V (10 values, 10pF-100nF) | 300 | Received 2026-09-10 (ordered 2026-08-30); untested. Physical EIA 3-digit codes confirmed against all 10 ordered values — see `lab/docs/parts_reference.md#multilayer-ceramic-capacitor-assortment-50v` for the decode table. Operating temperature still unresolved (listing self-contradicts). |
| Aluminum electrolytic capacitor kit, 16V/25V/50V (12 values, 1µF-470µF) | 120 | Received 2026-09-10 (ordered 2026-08-30); untested. Polarized, radial-lead DIP-style, ±20% tolerance. See `lab/docs/parts_reference.md#aluminum-electrolytic-capacitor-kit-1665025050v` for the full per-value table. |

---

## On Order (AliExpress)

Placed for the `lab/` repo's spacetime research build; new rows go here
first, with full specs/links/datasheets in `lab/docs/orders.md` and
`lab/docs/parts_reference.md`. Move each row up into its proper table
above once physically received.

| Component                                    | Quantity | Notes                                                           |
|-----------------------------------------------|----------|--------------------------------------------------------------------|
| TL082 JFET-input dual op-amp, DIP-8 | 10 | Ordered 2026-09-03, not yet received. Fills the tier5 `EPFIELD`/`CHGAMP` gap — the on-hand LM358 is bipolar-input (wrong device class for a high-impedance electrometer/charge-amp front end). See `lab/docs/parts_reference.md#tl082-jfet-input-dual-op-amp`. |
| MF52AT NTC thermistor, 10kΩ, B3950, 1% | 10 | Ordered 2026-09-03, not yet received. Fills the safety `THERM` gap — the existing thermistor in this table (Active Components and Sensors, above) is flagged "suspect faulty." See `lab/docs/parts_reference.md#mf52at-ntc-thermistor-10k`. |
| KY-003 A3144 Hall sensor breakout module | 1 | Ordered 2026-09-03, not yet received. Fills the tier5 `HALLAMP` gap only partially — this is a digital switch-output Hall IC, not the linear analog sensor the gap called for. See `lab/docs/parts_reference.md#ky-003-a3144-hall-sensor-breakout-module`. |
| IRLZ44N logic-level N-channel MOSFET, TO-220 | 1 | Ordered 2026-09-03, not yet received. Fills the tier7 `HVPULSE` and protection `ACTIVELIM` gap — no switching MOSFET of any kind was previously on hand. See `lab/docs/parts_reference.md#irlz44n-logic-level-mosfet`. |
| Piezo element, 12mm disc | 20 | Ordered 2026-09-03, not yet received. Fills the tier5 `CHGAMP` gap — a charge-output transducer to drive the charge amplifier. See `lab/docs/parts_reference.md#piezo-element-12mm-disc`. |
| SN74HC86N quad 2-input XOR gate, DIP-14 | 1 | Ordered 2026-09-03, not yet received. Fills the tier4 `PHASED` → tier6 `LOCKIN` gap — no logic gate IC on hand besides the 74HC595 shift register. See `lab/docs/parts_reference.md#sn74hc86n-quad-2-input-xor-gate`. |
| EZ-USB FX2LP CY7C68013A USB core board (SCOPELA logic analyzer) | 1 | Ordered 2026-09-10, not yet received. *Is* the `SCOPELA` tier purchase itself; `sigrok`'s `fx2lafw` firmware supports it out of the box. See `lab/docs/parts_reference.md#ez-usb-fx2lp-cy7c68013a-usb-core-board-scopela-logic-analyzer`. |
| GY-521 (MPU6050) 3-axis gyro/accelerometer module | 1 | Ordered 2026-09-10, not yet received. Substitutes for the originally-scoped ADXL335 to fill the tier5 `ACCELIF` gap. See `lab/docs/parts_reference.md#gy-521-mpu6050-3-axis-gyroaccelerometer-module`. |
| Color-ring inductor assortment, 0307 1/4W (12 values, 1µH-1mH) — reorder | 120 | Ordered 2026-09-10, not yet received. Reorder of the cancelled item below (same listing/variant, still cheapest available). Blocks tier3 `INDBRIDGE`. See `lab/docs/parts_reference.md#color-ring-inductor-assortment-0307-14w`. |

---

## Cancelled / needs replacement

Ordered, then cancelled by the seller/platform before shipping (refund in
progress, not a "received" or "on order" state — track replacement
sourcing in [TODO-arcticoder.md](TODO-arcticoder.md)).

| Component                                    | Quantity | Notes                                                           |
|-----------------------------------------------|----------|--------------------------------------------------------------------|
| Color-ring inductor assortment, 0307 1/4W (12 values, 1µH-1mH) | 120 | Ordered 2026-08-30; **cancelled by AliExpress 2026-09-07 (shipping issue)**, refund processed. **Reordered 2026-09-10** — see the "On Order" table above and `lab/docs/parts_reference.md#color-ring-inductor-assortment-0307-14w`. |

---

## Tools

| Component                    | Quantity | Notes                                                    |
|-------------------------------|----------|-------------------------------------------------------------|
| WorkPro 30W Soldering Iron    | 1        | Received 2026-08-24                                        |
| Rosin core solder (tube)      | 1        | Included with iron                                          |
| Soldering iron stand          | 1        | Included with iron                                          |
| Soldering tip, 5/32 in.       | 2        | Included with iron                                          |
| 18-in-1 wire stripper/crimper pliers | 1 | Received 2026-09-03; high-carbon steel + PVC handle. Resolves the wire-stripper dependency that was blocking `psu_ultralow_v1`/`psu_low_v2` AA-holder lead termination in `lab/`. |
