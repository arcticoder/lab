# Instrument board — requirements, budgets and block design (WP1)

Draft of 2026-10-22. It traces to the plan's three gates (`docs/research_instrument_plan.md`): the board
implements the readout, the actuators and the monitors of the torsion balance in `hardware/balance/`.
The numbers below are the ones the checks in `smoke_test.py` hold the design to; the parts are in
[parts.md](parts.md) (generated from the live JLC library); the simulations are in `sim/`.

## What the board must do

| Function | Requirement | Where it comes from |
|----------|-------------|---------------------|
| Read the flag's displacement | An optical channel: modulated IR LED, photodiode, TIA, 24-bit simultaneous ADC, digital lock-in in firmware. Readout noise far under the environment's (G3: 146 pm/√Hz against 4.8 nN/√Hz of air currents) | G3 |
| Normalize LED intensity | A second photodiode on the LED head, sampled at the same instant as the signal | G3 (the LED-noise term) |
| Calibrate and inject known forces | A plate driver: 0 to about 23 V, DAC-set, 1 mV steps (0.28 nN around a 40 V bias; at low voltage far finer), linear to 0.1% | G2 (electrostatic plates), A2 |
| Source and measure the device current | 0 to 0.3 A through the leads and device card, programmable, read back by the ADC on a 1 Ω shunt | G1 (lead-current force F = B I L), USB budget |
| Disturb the balance on command | Two coin-motor drivers, PWM, duty capped at 60% from 5 V (their 3 V average rating) | A2 (transfer functions) |
| Monitor the environment | Temperature (3 digital sensors), magnetic field (3-axis, at the device mount), floor motion (3-axis accelerometer) | G3 (the environmental terms), A2 |
| Stream data | USB to a host logger: ADC samples at up to 8 kSPS per channel, sensors at their own rates, timestamped | WP8 |
| Be built by the fab alone | Every part machine-placed SMT from the fab's library; nothing hand-soldered; sensor heads separate boards joined by cables | the user's constraints |

## Block diagram

```
USB-C ── polyfuse ── +5V ──┬── LP5907 ── 3V3_D ── RP2040 ── flash, crystal, SWD, buttons, status LEDs
 (ESD)    (0.75 A hold)     │                       │ SPI0                    I2C0             PIO / PWM / GPIO
                            │                       ▼                          │
                            ├── LP5907 ── 3V3_A ── ADS131A04 ◄─ ch0 PD head    ├─ MCP4728 DAC (LED1, plate, DUT set, spare)
                            │                       (16.384 MHz) ◄─ ch1 ref PD  ├─ TMP117 (ambient) on the board
                            │                                  ◄─ ch2 shunt     ├─ LIS2DW12 (floor motion)
                            │                                  ◄─ ch3 plate V   └─ JST-SH ×2 → heads (MMC5983MA + TMP117)
                            ├── MT3608 boost → 24 V ── OPA197 gain 5.7 ── plate out (JST-SH 2P)
                            ├── AOD4184A + 1 Ω shunt + 4.7 Ω ballast ── device leads out (JST-SH 2P)   [TLV9062 loop]
                            └── AO3400A ×2 ── coin motors (JST-SH 2P ×2)
LED head (JST-SH 4P): IR LED + reference photodiode + TIA     PD head (JST-SH 4P): photodiode + TIA
LED current: TLV9062 + AO3400A sink, 51 Ω sense, reference gated by SN74LVC1G3157 from a PIO pin
```

## Numbers the design is held to (all checked in `smoke_test.py`)

- **Pins** (`pins.py`): 30 signals on 30 GPIOs, every function checked against the RP2040 datasheet's function table; the ADC on SPI0 (GP16–19), I2C0 on GP4/GP5, the two motor PWMs on one slice, four ADC monitors on GP26–29.
- **Power, from the 5 V USB rail**: measurement 89 mA; lead-current run 389 mA; disturbance run 329 mA. USB guarantees 500 mA and the input polyfuse holds 750 mA, so each mode stays under 90% of USB's limit and under the fuse's hold with 15% margin. The device current is capped at 300 mA by this budget (400 mA would be 489 mA); a bench supply would be needed above that. The two 3.3 V regulators run at 35 mA (digital) and 49 mA (analog) of their 250 mA.
- **TIA** (each head): 10 kΩ and 1 nF with the VBPW34S's 70 pF at zero bias: 79.98 dB (10 kV/A) at 1 kHz, no peaking, corner 16.8 kHz. A 100 µA photocurrent with ambient light up to about the same stays inside the ADC's ±2.44 V.
- **LED sink**: 20.00 mA at a 1.02 V reference, zero when gated off, 1.08 V of headroom on 3.3 V; the gated edge settles to 1% in 0.2 µs (the carrier's half-period is 250 µs or more). The op-amp drives the gate directly; every added gate resistor or compensation capacitor made it worse.
- **Device-current sink**: the AOD4184A's 1.5 nF gate and 37 S of transconductance, driven through a 1 kΩ/10 nF integrator compensation, show no overshoot and 300 mA to 0.5% at gain ×0.33 to ×3, Ciss 1.0 to 1.7 nF, loads 0.5 to 10 Ω (worst settling 22 µs). At 300 mA into the leads alone the MOSFET dissipates 0.94 W (52 K rise at 55 K/W) and the ballast 0.42 W of its 1 W; both are on the board, away from the balance.
- **Plate driver**: gain 5.7 (47 kΩ/10 kΩ) with 10 pF across the feedback resistor: linear to 0.001%, no overshoot, settles in 3.9 µs with 300 pF of cable, peak 22.8 V against the repo's 50 V DC line.
- **Parts** (`parts.md`): 48 part numbers, 193 components per board, 25 extended (the fee-bearing kind); about $24 of components per board; every part in stock at 20× the order's need.

The simulations use a behavioral op-amp built from the TLV9062 and OPA197 data sheets (gain-bandwidth, phase margin,
resistive output impedance, rails); TI's SPICE macro models replace it before layout.

## Decisions made so far

- RP2040 on the board (not RP2350: see `docs/kb/rp2350_notes.md`), 16 Mbit flash as on the Pico.
- One regulator part number (LP5907) for both 3.3 V rails, to keep the extended-part count down; connectors reduced to two JST-SH sizes (4-pin, 2-pin) and one 2.54 mm SMD header.
- ADC: ADS131A04 (3 V analog with the charge pump, 16.384 MHz crystal, 79 nV/√Hz input-referred). The ADS1220 ($2.23, 2 kSPS) was the cheaper option; it can't take the signal and reference photodiodes at the same instant.
- DAC: MCP4728 (12-bit, I2C, $2.33): LED current, plate drive, device-current set. A 16-bit DAC8554 costs $11; 12 bits give 42 pN steps on the plate and 10 µA steps on the LED.
- No coil, no magnets on the arm (G3). Magnetic compensation, if A5 shows it is needed, is a later separate coil driver.
- A device card (a small separately-ordered board with the device's resistor and a 2-pin header) carries the load; variants: leads only, 2.2 Ω, 10 Ω. Defined in WP4.

## Open points, to be closed before layout

1. The ADS131A04's input network and its charge-pump configuration (the datasheet's AVSS/VNCP pins), and the ADC's input protection.
2. The 24 V boost's feedback network and ripple (MT3608 at 1.2 MHz into the plate: the mechanical bandwidth is 0.2 Hz, so ripple matters only through the ADC and the optical channel's electronics; filter it).
3. Enough analog ground discipline: the plate driver and the LED sinks are the noisiest blocks on the board; the layout partitions them (WP5).
4. The optical readout's real photocurrent (assumed 100 µA at mid-flag from the data sheets): A5 measures it, and the TIA's Rf may change.
5. A5 itself: the balance's measured noise spectrum, before layout.
