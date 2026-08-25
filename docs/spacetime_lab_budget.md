# Spacetime Research Lab: Parts List & Budget Estimate

## Overview
This is a high-level component list derived from general_purpose_circuit_dependency.md and spacetime_circuits_dependency.md. Prices are approximate AliExpress/budget-source estimates as of 2026. Excludes consumables (solder, wire, tape, enclosures) and cheap discretes (resistors, capacitors under $1).

---

## Power Supply System

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| AA Alkaline Batteries | 10 | $0.30 | $3 | Bootstrap, reusable testing |
| AA Battery Holder (2-slot) | 5 | $1.50 | $7.50 | Multiple circuits in progress |
| USB 5V/3A Wall Adapter | 2 | $8 | $16 | Redundancy, different circuits |
| 12V Sabrent USB-C Adapter | 1 | $35 | $35 | Medium-power backbone |
| MacBook 96W USB-C Adapter (or equivalent) | 1 | $45 | $45 | Medium-high tier testing |
| **Subtotal PSU** | | | **$106.50** | |

---

## Circuit Protection Components

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Polyfuses (assorted: 50mA, 500mA, 1A, 2A) | 50 | $0.25 | $12.50 | Bulk, resettable |
| Fast-blow Fuses (1A, 2A, 3A) | 25 | $0.50 | $12.50 | Bulk assortment |
| Schottky Diodes (1N5817 or equiv, 1A) | 50 | $0.15 | $7.50 | Reverse voltage protection |
| MOSFETs (IRF540N or equiv, N-channel) | 10 | $0.80 | $8 | Active current limiting |
| Sense Resistors (shunt, precision 0.01–0.1Ω) | 20 | $2 | $40 | Current measurement |
| **Subtotal Protection** | | | **$80.50** | |

---

## Bootstrap & Measurement Tools

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Salvaged Galvanometer (or high-sensitivity moving-coil meter) | 1 | $15 | $15 | Passive voltmeter base; or build from scratch |
| Magnet Wire (30 AWG, 100m spool) | 1 | $8 | $8 | Coil winding |
| Permanent Magnets (assorted, neodymium) | 5 | $3 | $15 | Galvanometer construction, sensor testing |
| 555 Timer ICs | 10 | $0.50 | $5 | Frequency counter, oscillators |
| Arduino Nano/Clone | 2 | $12 | $24 | Data acquisition, verification |
| I2C 16x2 LCD Display | 2 | $8 | $16 | Readout for voltmeter, frequency counter |
| Tuning Forks (calibrated, 440 Hz or other) | 2 | $5 | $10 | Frequency reference |
| CRT Tube (salvaged from old monitor) | 1 | $0 (salvage) | $0 | Oscilloscope construction |
| Analog Multimeter (or salvage meter movement) | 1 | $25 | $25 | Backup; measurement verification |
| **Subtotal Bootstrap** | | | **$118** | |

---

## Tier 1: Foundational Circuits

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Precision Voltage Reference (LM4040, REF02, or TL431) | 5 | $2.50 | $12.50 | Reference generator backbone |
| Low-noise Op-Amps (OPA2333, NE5532, or equiv) | 20 | $1.50 | $30 | Function generator, oscillator, general analog |
| Crystal Oscillators (assorted: 1MHz, 10MHz, 32kHz) | 10 | $2 | $20 | Precision timing sources |
| Precision Capacitors (film, 1%, critical values) | 50 | $0.80 | $40 | Timing networks, coupling |
| Trim Potentiometers (10-turn, 10k/100k) | 20 | $1.50 | $30 | Oscillator tuning, reference adjustment |
| **Subtotal Tier 1** | | | **$132.50** | |

---

## Tier 2: Essential Validation & Measurement

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Precision Op-Amps (OPA2277, TL072, LM358) | 30 | $1.80 | $54 | Voltmeter, ammeter, transimpedance amp frontend |
| Precision Shunt Resistors (0.1Ω, 1Ω, 10Ω, 1%) | 20 | $2 | $40 | Current measurement |
| High-impedance Resistors (1GΩ, 10GΩ) | 10 | $1.50 | $15 | Voltmeter input, high-Z measurement |
| AD converter modules (12-bit or better) | 5 | $8 | $40 | Frequency counter, data logging |
| Precision Voltage Dividers (resistor networks) | 10 | $3 | $30 | Measurement scaling |
| **Subtotal Tier 2** | | | **$179** | |

---

## Tier 3: Passive Components & Bridges

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Precision Resistors (1%, 0.1%, assorted E12 series) | 100 | $0.30 | $30 | Bridge arms, dividers |
| Film Capacitors (1%, assorted 10pF–100µF) | 100 | $0.50 | $50 | Bridge circuits, timing |
| Inductors (air-core, ferrite, assorted µH–mH) | 20 | $2 | $40 | Bridge resonance, filter inductance |
| Precision Decade Box (or DIY equivalent) | 1 | $40 | $40 | Calibration, bridge tuning |
| Thermistor (NTC, calibrated) | 5 | $5 | $25 | Temperature compensation, thermal monitoring |
| **Subtotal Tier 3** | | | **$185** | |

---

## Tier 4: Core Analog Signal Processing

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Instrumentation Amps (INA128, AD8221, or equiv) | 10 | $4 | $40 | Differential measurement, noise rejection |
| Low-noise Op-Amps for precision (OPA2333, TL072) | 30 | $1.80 | $54 | Differential amps, phase detectors, demodulators |
| Precision Multipliers/Phase Detectors (AD633, NE612, or equiv) | 5 | $6 | $30 | Phase detection, synchronous demodulation |
| Precision Rectifier Diodes (1N457, OA91, or equiv) | 20 | $1 | $20 | Phase detector output, demodulator |
| Matched Resistor Pairs (precision 0.1%) | 20 | $2 | $40 | Bridge-balanced circuits |
| **Subtotal Tier 4** | | | **$184** | |

---

## Tier 5: Specialized Sensor Interfaces

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Hall Effect Sensor ICs (A1302, SS490, or equiv) | 5 | $3 | $15 | Magnetic field measurement |
| Accelerometer Modules (ADXL345 I2C, or 3-axis) | 3 | $8 | $24 | Gravitational measurement, vibration detection |
| High-impedance Buffer Op-Amp (OPA128, OPA2228) | 10 | $3 | $30 | Electric field probe conditioning |
| Transimpedance Amplifier (TIA) pre-built or IC | 5 | $5 | $25 | Photodiode interface, charge detection |
| Charge Amplifier ICs or discrete (e.g., based on OPA128) | 5 | $8 | $40 | Piezoelectric, capacitive sensor interface |
| LVDT Transducer (displacement sensor) | 2 | $15 | $30 | Mechanical/position measurement |
| **Subtotal Tier 5** | | | **$164** | |

---

## Tier 6: Advanced Detection & Analysis

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Lock-in Amplifier Module (pre-built or DSP-based) | 1 | $120 | $120 | Weak signal extraction; can build from scratch cheaper |
| Anti-aliasing Filter ICs (Sallen-Key or VCVS topology) | 10 | $2 | $20 | Data acquisition frontend |
| Time-to-Digital Converter IC (TDC7001, or DIY) | 2 | $30 | $60 | High-precision time interval measurement |
| Low-noise Pre-amplifier (e.g., for photodiode) | 3 | $8 | $24 | Detector signal conditioning |
| Jitter Measurement: Precision Delay Line IC or FPGA | 1 | $50 | $50 | Phase/timing jitter characterization |
| **Subtotal Tier 6** | | | **$274** | |

---

## Tier 7: High-Frequency & Specialized

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| RF Diode Detector (AD8318, LT5534, or equiv) | 3 | $8 | $24 | RF power measurement |
| Gilbert Cell Mixer IC (SA612A, NE612) | 5 | $3 | $15 | Frequency mixing, heterodyne detection |
| Function Generator Module (DDS-based, pre-built) | 1 | $40 | $40 | Precision sweep function generator |
| High-Voltage Pulse Generator (dedicated IC or circuit) | 1 | $60 | $60 | Transient testing, capacitor discharge |
| HV MOSFET Driver (TC4427, MCP1407) | 5 | $3 | $15 | Switching control for pulse generator |
| **Subtotal Tier 7** | | | **$154** | |

---

## Tier 8: Energy & Complex Measurement

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Calorimeter Transducer (thermopile or thermocouple) | 2 | $15 | $30 | Heat measurement |
| Thermocouple Amplifier IC (MAX31855, AD8495) | 3 | $5 | $15 | Temperature sensor interface |
| AC Power Factor Measurement IC (ADI or TI chipset) | 2 | $20 | $40 | Power quality measurement |
| Energy Integrator Circuit (precision integrator op-amp) | 2 | $5 | $10 | Energy measurement |
| Noise Figure Measurement: Low-noise source + analyzer | 1 | $80 | $80 | Noise characterization |
| **Subtotal Tier 8** | | | **$175** | |

---

## Tier 9: Data Acquisition & Integration

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Sample-and-Hold IC (LF398, or MOSFET-based) | 5 | $3 | $15 | Sampling frontend |
| Analog Multiplexer (16-channel 4051, or IC) | 5 | $2 | $10 | Multi-channel input switching |
| ADC Modules (16-bit, SPI/I2C interface) | 5 | $12 | $60 | Data acquisition backend |
| Reference Voltage Distribution (precision supply supervisor) | 3 | $5 | $15 | Reference buffering and distribution |
| Data Logger Firmware/SD Card Module | 2 | $8 | $16 | Long-term data storage |
| **Subtotal Tier 9** | | | **$116** | |

---

## Safety Circuits (All Tiers)

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Temperature Sensor ICs (LM35, DS18B20) | 10 | $1.50 | $15 | Thermal monitoring |
| Ground Fault/Leakage Detection ICs (or relay-based) | 3 | $8 | $24 | AC safety |
| ESD Suppression Diodes (assorted, TVS) | 50 | $0.30 | $15 | Component protection |
| Arc Detection Photodiode (BPV22) | 2 | $5 | $10 | High-voltage arc detection |
| Vacuum Pressure Sensor (MPX5100, or vacuum gauge) | 1 | $20 | $20 | Vacuum chamber monitoring |
| Smoke/Flame Detector Interface (analog output) | 1 | $12 | $12 | Lab safety |
| **Subtotal Safety** | | | **$96** | |

---

## Mechanical & Enclosure (High-Level)

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Aluminum Enclosures (various sizes, for PSU, circuits) | 5 | $20 | $100 | Shielding, heat dissipation |
| Heat Sinks (small to medium, TO-220, DIP) | 20 | $2 | $40 | Regulator, power dissipation |
| Breadboards & Protoboards (assorted) | 10 | $5 | $50 | Prototyping, temporary builds |
| PCB Blanks & Etching Supplies (for permanent circuits) | 5 | $8 | $40 | Circuit board fabrication |
| Connectors (BNC, banana plugs, XLR, USB) | 100 | $0.50 | $50 | I/O and interconnect |
| **Subtotal Mechanical** | | | **$280** | |

---

## Test & Calibration Fixtures

| Component | Qty | Unit Cost | Total | Notes |
|-----------|-----|-----------|-------|-------|
| Precision Resistor Calibration Kit (1%, assorted) | 1 | $30 | $30 | Bridge and measurement verification |
| RF Attenuators & Terminations | 5 | $5 | $25 | High-frequency testing |
| Precision Capacitor Substitution Box | 1 | $25 | $25 | Circuit tuning, calibration |
| **Subtotal Test Fixtures** | | | **$80** | |

---

## Contingency & Misc

| Item | Subtotal |
|------|----------|
| Spare IC chips (expected failures/learning) | $100 |
| Replacement sensors & transducers | $80 |
| Repair & rework tools (desoldering pump, etc.) | $50 |
| Documentation & reference manuals (PDFs, datasheets) | $0 |
| **Subtotal Contingency** | **$230** |

---

## TOTAL BUDGET ESTIMATE

| Section | Subtotal |
|---------|----------|
| Power Supply System | $106.50 |
| Circuit Protection | $80.50 |
| Bootstrap & Measurement Tools | $118 |
| Tier 1 | $132.50 |
| Tier 2 | $179 |
| Tier 3 | $185 |
| Tier 4 | $184 |
| Tier 5 | $164 |
| Tier 6 | $274 |
| Tier 7 | $154 |
| Tier 8 | $175 |
| Tier 9 | $116 |
| Safety Circuits | $96 |
| Mechanical & Enclosure | $280 |
| Test & Calibration Fixtures | $80 |
| Contingency & Misc | $230 |
| | |
| **GRAND TOTAL** | **$2,375.50** |

---

## Notes

1. **Excludes:** Cheap discretes (resistors <$1, caps <$1), solder, wire, tape, labels, enclosure hardware
2. **AliExpress pricing:** Assumes bulk/kit discounts; individual quantities are more expensive
3. **Salvage opportunities:** CRT tubes, galvanometers, old meter movements can drop bootstrap cost by $50–100
4. **Lock-in Amplifier:** $120 estimate is pre-built module. DIY from scratch (mixed-signal DSP) costs $40–80 but requires significant development
5. **Contingency (9.7% of total):** Accounts for IC failures, incorrect part ordering, learning curve breakage
6. **Scalability:** This workbench can grow incrementally; you don't need everything at once. Start with PSU + Bootstrap (~$225), then add Tiers 1–2 (~$312), then scale upward.

---

## Recommended Build Path by Budget

- **Phase 1 ($225):** PSU system + Bootstrap tools (AA batteries, voltmeter, frequency counter)
- **Phase 2 (+$312, ~$537 cumulative):** Tiers 1–2 (oscillators, references, basic measurement)
- **Phase 3 (+$370, ~$907 cumulative):** Tiers 3–4 (bridges, analog processing)
- **Phase 4 (+$328, ~$1,235 cumulative):** Tiers 5–6 (sensor interfaces, advanced detection)
- **Phase 5 (+$289, ~$1,524 cumulative):** Tiers 7–8 (RF, energy measurement)
- **Phase 6 (+$116, ~$1,640 cumulative):** Tier 9 (data acquisition)
- **Safety & Mechanical:** $376 (parallel with build, not phase-gated)
- **Contingency & Rework:** $230 (spread across all phases)
