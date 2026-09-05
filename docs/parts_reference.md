# Parts Reference

Pinouts and electrical notes for components that don't have a proper
datasheet checked in yet. See [orders.md](orders.md) for what was ordered
and why; see individual [manuals/](manuals/) for converted PDF manuals where
one exists.

---

## Breadboard variants on hand / on order

| Type | Tie points | Size | Source |
|---|---|---|---|
| SYB-170 (received, 6-pack) | 170 | 35 × 47mm approx, 10mm thick | black variant received |
| SYB-170 (received, 2-pack) | 170 | same as above | second listing, separate order; received 2026-08-24 |
| MB-102 (received) | 400 (300 terminal-strip + 100 distribution-bar) | 8.5 × 5.5 × 1.0cm | [manual](manuals/400-tie-points-solderless-breadboard-_mb-102_-for-diy-electronics.md); received 2026-08-24 |
| Full breadboard (existing inventory) | 830 | — | SunFounder Thales kit, see `pico/docs/inventory.md` |

MB-102 terminal strips: rows labeled a–e and f–j are connected horizontally
within a row, split by the center DIP channel. Distribution bars (side
rails) are marked red (+) / blue (−) and run vertically the length of the
board. Rated for low-voltage prototyping only, current limit ~2A per the
manual; wire gauge 21–26 AWG recommended for the spring clips.

---

## CD4066B (quad bilateral switch)

10 received 2026-08-24, DIP-14 package. Not yet validated per-unit — see
[measurement_tools/cd4066_switch_tester/](../measurement_tools/cd4066_switch_tester/)
for the bring-up jig that checks each of the 4 switches per chip before
trusting one downstream. Four independent analog switches, each gated by
its own digital control pin (logic high = closed/conducting). Useful for:
analog multiplexer (tier9 `MUX`), sample-and-hold gating (tier9 `SAMHOLD`),
synchronous demodulator switching (tier4 `DEMOD`).

Standard DIP-14 pinout (verify against the specific manufacturer's
datasheet before building — this is the common legacy 4000-series pinout,
consistent across TI/ON Semi/Fairchild, but confirm before relying on it):

| Pin | Function | Pin | Function |
|---|---|---|---|
| 1 | Switch 1 I/O A | 14 | VDD |
| 2 | Switch 1 I/O B | 13 | Control 1 |
| 3 | Switch 2 I/O B | 12 | Control 4 |
| 4 | Switch 2 I/O A | 11 | Switch 4 I/O A |
| 5 | Control 2 | 10 | Switch 4 I/O B |
| 6 | VSS (GND) | 9 | Switch 3 I/O B |
| 7 | Control 3 | 8 | Switch 3 I/O A |

Switches are bidirectional — either I/O pin can be signal in or out.

---

## LM358 (dual op-amp)

10 received 2026-08-24, DIP-8. First use:
[signal_conditioning/voltage_reference_lm358/](../signal_conditioning/voltage_reference_lm358/).
Standard pinout:

| Pin | Function |
|---|---|
| 1 | Output 1 |
| 2 | Inverting input 1 (−) |
| 3 | Non-inverting input 1 (+) |
| 4 | VEE / GND |
| 5 | Non-inverting input 2 (+) |
| 6 | Inverting input 2 (−) |
| 7 | Output 2 |
| 8 | VCC |

Single-supply capable (input range includes GND), which is why it shows up
as the go-to cheap op-amp for battery-powered analog frontends. Candidate
for tier2 voltmeter/ammeter frontends and tier4 differential amp — though
precision op-amps (OPA2277, TL072) are the preferred choice where
noise/offset actually matters; LM358 is the budget/bring-up substitute.

---

## USB-C 16-pin test breakout board

1 received 2026-08-24, blue variant. Board size 21.6×14.2mm, 2.54mm hole
pitch, FR-4, double-sided (front/back plug testing). Breakout pads, as
silkscreened:

`CC2, D+, D-, SBU1, SBU2, CC1, VBUS, GND`

> The AliExpress product photo's third-party transcription (in the order
> notes) listed the second pad as `U+`. That's almost certainly a
> transcription slip — no standard USB-C pinout has a `U+`, and `D+` is the
> expected pad in that position alongside `D-`. Confirm against the
> physical board silkscreen once it arrives before wiring anything to it.

Two SMD resistors near the connector (labeled `512` and `215` on the
photo) are almost certainly the CC1/CC2 pull-down or configuration-channel
resistors used to advertise a fixed current/role to a USB-C source —
verify values with a meter before assuming a specific standard resistance.

---

## Polyfuses (RXEF series)

Naming pattern: `RXEF<NNN>` where the numeric suffix is the hold current in
amps, decimal point implied — e.g. `RXEF005` = 0.05A hold, `RXEF050` =
0.5A hold. This matches the RXEF005/RXEF050 already used in the
`psu_ultralow`/`psu_low` design. Trip
current and trip time are *not* implied by the part number alone (typically
higher than hold current by some multiple, and time-dependent) — check the
Littelfuse/Bourns datasheet for the exact trip curve before relying on a
specific trip threshold.

Both values received 2026-08-21 (20 each):

- RXEF005 (0.05A / 50mA) — `psu_ultralow` tier
- RXEF050 (0.5A / 500mA) — `psu_low` tier

Not yet validated per-unit — see [orders.md](orders.md#polyfuses-rxef005-and-rxef050)
and [fuse_test_voltmeter](../measurement_tools/fuse_test_voltmeter/) for the per-fuse
trip/reset check before trusting one near an LED.

---

## 1N5817 Schottky diode

See [manuals/schottky-rectifier-diodes-in5817-1a20v-do-41.md](manuals/schottky-rectifier-diodes-in5817-1a20v-do-41.md).
1A / 20V, DO-41, ~0.45V forward drop. Cathode-banded end.

20 received 2026-08-21, not yet validated per-unit — see
[orders.md](orders.md#1n5817-schottky-diode-1a-20v-do-41).

---

## AA battery holder (single-cell)

See [manuals/aa-power-battery-holder-lr6-container-with-lead-cables.md](manuals/aa-power-battery-holder-lr6-container-with-lead-cables.md).
ABS housing, red/black lead wires. Manual's only real content: insert
battery per polarity marking, avoid humid environments, don't let bare
lead ends touch once a battery is loaded (short-circuit risk), wires are
thin/low-current rated only.

5 received 2026-08-21, ready to use — no per-unit validation needed.

---

## 3296 trimming potentiometer

10 received 2026-09-01 (10kΩ variant). See
[orders.md](orders.md#3296w-trimming-potentiometer).

Standard 3-pin cermet trimmer, top-adjust screw wiper. The listing calls
it "multi-turn," but the 3296 package designation is normally a
**single-turn** trimmer (a multi-turn part in this size class is usually
labeled 3296X or similar) — verify actual wiper travel/turns-per-span
against the physical part once received rather than trusting the listing
title. Pinout: two outer pins are the fixed ends of the resistive
element (10kΩ end-to-end), the middle pin is the wiper. Candidate use:
calibration trim for tier1 `OSC` timing or fine-adjusting a reference
divider ratio.

---

## Panel-mount fuse holder (6×30mm)

1 received 2026-09-01. See
[orders.md](orders.md#panel-mount-fuse-holder-6x30mm). EGBO brand, panel
opening 12/14mm, rated 10A/250V max, accepts standard 6×30mm glass tube
fuses (also fits 5×20mm per the listing, though the selected variant is
sized for 6×30mm). Pairs with the 2A glass tube fuse below for the
`psu_medlow` protection tier.

---

## NE555 timer

10 received 2026-09-01, DIP-8 package; untested/not yet validated per-unit
(bulk IC batch, no per-unit test jig built yet). See
[orders.md](orders.md#ne555-timer-ic-dip-8). Standard NE555 pinout:

| Pin | Function | Pin | Function |
|---|---|---|---|
| 1 | GND | 8 | VCC |
| 2 | Trigger | 7 | Discharge |
| 3 | Output | 6 | Threshold |
| 4 | Reset | 5 | Control Voltage |

Supply 4.5–16V typical. Astable configuration designed & simulated
2026-09-01 in `oscillators/ne555_astable/` (tier1 `OSC`, 5V rail, 1kΩ Ra +
3296 10kΩ trimpot as Rb + 100nF timing cap — ~686Hz–2.9kHz recommended
trim range), not yet bench-built/validated on real hardware. Also a
candidate for tier2 `FREQC` (as a gate-time generator for a frequency
counter).

---

## TL431A precision shunt reference

5 received 2026-09-01, TO-92 package; untested. See
[orders.md](orders.md#tl431a-precision-shunt-reference-to-92). 3-terminal
adjustable shunt regulator/reference: Cathode, Anode, Reference. Internal
bandgap reference is 2.495V between Ref and Anode; feeding back a
resistor divider from Cathode to Ref sets any output from 2.5V up to 36V,
regulated by the device sinking current at Cathode to hold Ref at 2.495V.
Needs a pull-up/current source into Cathode (it only sinks, never
sources) — unlike the LM358 buffer in
[voltage_reference_lm358](../signal_conditioning/voltage_reference_lm358/),
which is a true low-impedance source output. Candidate as a more
temperature-stable tier1 `REF` alternative once wired with its required
external pull-up resistor.

---

## Glass tube fuses (6×30mm)

10 received 2026-09-01, 2A fast-blow variant, 250V rated; untested/not yet
validated per-unit (bulk consumable-fuse batch, no per-unit test jig built
yet — distinct from the polyfuse tester in
[measurement_tools/fuse_test_voltmeter/](../measurement_tools/fuse_test_voltmeter/),
which tests resettable PTC polyfuses, not glass cartridge fuses). See
[orders.md](orders.md#glass-tube-fuses-6x30mm-250v). Same listing offers
0.1A–30A variants; 2A was the selected SKU. Pairs with the panel-mount
holder above for the `psu_medlow` protection tier (2A fast-blow +
polyfuse backup, per
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)'s
`PROTMEDLOW` node).

---

## Metal film resistor kit (1W, 1%)

40 received 2026-09-03 (ordered 2026-08-30). See
[orders.md](orders.md#metal-film-resistor-kit-1w-1). Axial metal film,
1% tolerance, 1W power rating (vs. the SunFounder Thales kit's 1/4W
stock). **Not an assortment pull** — the listing lets the buyer pick
specific values from its range (0.1Ω, 10Ω, 22Ω, 47Ω, 100Ω, 330Ω, 1kΩ,
4.7kΩ, 10kΩ, 22kΩ, 47kΩ, up to 2.2MΩ), and two values were specifically
selected at 20 units each: **0.1Ω** and **1Ω**, 40 pieces total, no other
values received. (An earlier version of this entry described a single
20-piece "assorted" pull including 0.1Ω — that was wrong on both count
and framing; corrected here and in
[orders.md](orders.md#metal-film-resistor-kit-1w-1).) The 0.1Ω value
replaces the jumper-wire-chain shunt in
[ammeter_1ohm](../measurement_tools/ammeter_1ohm/) with an actual
resistor. The 1Ω value has no assigned use yet — candidate reference
resistor for a tier3 `OHMMETER` (4-wire Kelvin) build.

---

## PT334-6C photodiode

10 received 2026-09-03 (ordered 2026-08-30), 5mm package, untested. See
[orders.md](orders.md#pt334-6c-photodiode-5mm). Silicon PIN photodiode,
typically used reverse-biased in a transimpedance amplifier front-end
(anode to GND, cathode through a feedback resistor/op-amp to a positive
rail) — candidate for a tier2 `TIA` build alongside the on-hand LM358P.
Pin identification: the longer lead is the anode, matching standard
photodiode/LED lead convention — confirm against the physical part
before wiring, since some photodiode packages reverse this convention
relative to LEDs.

---

## Color-ring inductor assortment (0307, 1/4W)

120 ordered 2026-08-30, not yet received. See
[orders.md](orders.md#color-ring-inductor-assortment-0307-14w). Axial,
color-ring-coded, epoxy-coated, 0307 package (1/4W/0.25W) — the listing
also offers 0410 (1/2W) and 0510 (1W) packages under the same title, but
those variants were **not** selected. 12 values × 10pcs: 1µH, 10µH, 22µH,
33µH, 47µH, 100µH, 150µH, 220µH, 330µH, 470µH, 560µH, 1mH. Rated
dielectric withstand 250V AC rms, operating temperature −25 to 85°C.
Read the color-ring code the same way as resistor color bands (the
listing gives no photo of the actual band-to-value mapping) — verify
against a multimeter's inductance mode or an LCR-adjacent bridge circuit
once [INDBRIDGE](general_purpose_circuit_dependency.md) exists, rather
than trusting the band colors alone, since misprinted/faded bands on
cheap bulk assortments are a known failure mode for color-coded passives.
First candidate use: tier3 `INDBRIDGE` (inductance bridge) directly, or
any future RF/filter/oscillator tank-circuit design.

---

## Multilayer ceramic capacitor assortment (50V)

300 ordered 2026-08-30, not yet received. See
[orders.md](orders.md#multilayer-ceramic-capacitor-assortment-50v).
Through-hole/in-line MLCC, 50V rated, 10% tolerance, 5.08mm lead pitch.
10 values × 30pcs: 10pF, 20pF, 30pF, 47pF, 56pF, 68pF, 100pF, 1nF, 10nF,
100nF. **Operating temperature is unresolved** — the listing's own
structured spec field says −40 to 80°C while its free-text description
says −25°C to 185°C for the same part; treat both as unconfirmed until a
datasheet or physical part marking settles it, and don't silently pick
one when referencing this part elsewhere. Ceramic capacitors have no
polarity — either lead can go to either node. First candidate use: tier3
`CAPBRIDGE` (capacitance bridge) directly, general bypass/decoupling
across any circuit here, and NE555 timing capacitors (tier1 `OSC`) — the
100nF/10nF SunFounder-kit ceramic caps (already on hand, not this ordered
assortment) cover the [NE555 timer](#ne555-timer)'s `OSC` design in
`oscillators/ne555_astable/` (designed & simulated 2026-09-01, not yet
bench-built), so this assortment isn't actually needed for that use once
it arrives.

---

## Aluminum electrolytic capacitor kit (16V/25V/50V)

120 ordered 2026-08-30, not yet received. See
[orders.md](orders.md#aluminum-electrolytic-capacitor-kit-1665025050v) —
**that entry's listing URL is unresolved** (the user supplied a literal
`???` placeholder instead of a real item ID); don't trust any URL that
might later get attached to this part without re-verifying against the
actual AliExpress order history. Brand YTDMEN, radial-lead DIP-style,
±20% tolerance. 12 values × 10pcs, by voltage/capacitance:

| # | Voltage | Capacitance |
|---|---------|-------------|
| 1 | 50V | 1µF |
| 2 | 50V | 2.2µF |
| 3 | 50V | 3.3µF |
| 4 | 50V | 4.7µF |
| 5 | 50V | 10µF |
| 6 | 25V | 22µF |
| 7 | 25V | 33µF |
| 8 | 25V | 47µF |
| 9 | 16V | 100µF |
| 10 | 16V | 220µF |
| 11 | 16V | 330µF |
| 12 | 16V | 470µF |

**Polarized — orientation matters.**

---

## TL082 JFET-input dual op-amp

10 ordered 2026-09-03, DIP-8, not yet received. See
[orders.md](orders.md#tl082-jfet-input-dual-op-amp-dip-8). Same physical
pinout convention as the on-hand LM358:

| Pin | Function |
|---|---|
| 1 | Output 1 |
| 2 | Inverting input 1 (−) |
| 3 | Non-inverting input 1 (+) |
| 4 | V− |
| 5 | Non-inverting input 2 (+) |
| 6 | Inverting input 2 (−) |
| 7 | Output 2 |
| 8 | V+ |

Unlike LM358 (bipolar-input, ~20–100nA bias current), TL082 is
JFET-input with bias current in the low pA range — the device class
tier5 `EPFIELD` (electric field probe) and `CHGAMP` (charge amplifier)
actually need, since both front-ends present a very high source
impedance to the op-amp's input. Typically needs a dual (split) supply
or a mid-rail bias network for single-supply use, unlike LM358's
single-supply-friendly input range down to GND — confirm the specific
TL082 variant's input common-mode range against its datasheet before
wiring a single-supply front end.

---

## MF52AT NTC thermistor (10kΩ)

10 ordered 2026-09-03, not yet received. See
[orders.md](orders.md#mf52at-ntc-thermistor-10k). 2-lead bead
thermistor, no polarity. R25 = 10kΩ ±1%, B(25/50) = 3950K ±1%, operating
range −55–125°C, black modified-phenolic body, nickel-tin-plated leads.
**Caveat:** the listing's own spec sheet's worked example decodes a
different part (`104` EIA code = 100kΩ) than the 10kΩ (`103` code)
variant actually ordered — treat only the tolerance/B-value/temperature-
range figures as trustworthy for this specific part, not the R25 value
in the sheet's example. Fills the safety `THERM` gap; the existing
thermistor in `pico/docs/inventory.md` is flagged "suspect faulty."

---

## KY-003 A3144 Hall sensor breakout module

1 ordered 2026-09-03, not yet received. See
[orders.md](orders.md#ky-003-a3144-hall-sensor-breakout-module). 3-pin header
module wrapping an A3144 Hall-switch IC plus onboard pull-up:

| Pin | Function |
|---|---|
| 1 | GND |
| 2 | 3V3 |
| 3 | GPIO (digital output) |

**This is a digital switch-output sensor, not a linear analog one** —
the A3144 die's own datasheet describes its output as "a digital
voltage signal." Output is open-collector-style, active-low near a
sufficient magnetic field (turn-on ~7–23mT typ, release ~5–17.5mT typ),
so it reads as a simple presence/proximity digital input on a Pico
GPIO — no amplifier stage needed. Fills the tier5 `HALLAMP` gap only
partially: it does not exercise an actual Hall-amplifier design, since
there's nothing analog to amplify. A linear/analog Hall element (e.g. a
49E) would still be needed if the `HALLAMP` op-amp circuit itself is
still wanted as a build target.

---

## IRLZ44N logic-level MOSFET

1 ordered 2026-09-03, TO-220, not yet received. See
[orders.md](orders.md#irlz44n-logic-level-n-channel-mosfet-to-220).
Standard TO-220 pinout, tab facing away, pins left to right:

| Pin | Function |
|---|---|
| 1 | Gate |
| 2 | Drain (also the metal tab) |
| 3 | Source |

Logic-level N-channel MOSFET — gate threshold voltage low enough (~1–2V
typ) to switch fully on from a 3.3V Pico GPIO directly, unlike a
standard-level MOSFET that needs a ~10V gate drive. Typical ratings:
Vds 55V, Id ~47A (heatsink-dependent), Rds(on) low-mΩ range at Vgs=5V.
Fills the tier7 `HVPULSE` and protection `ACTIVELIM` gap — no switching
MOSFET of any kind was previously on hand.

---

## Piezo element, 12mm disc

20 ordered 2026-09-03, not yet received. See
[orders.md](orders.md#piezo-element-12mm-disc). 2-terminal ceramic disc
element (brass or copper backing plate + piezoceramic layer), no fixed
polarity convention like a diode — used either as a driven
buzzer/actuator or, wired into a charge-amplifier front end, as a
charge-output transducer (mechanical flex/vibration → small charge
signal). Fills the tier5 `CHGAMP` gap: nothing else in inventory
generates a charge signal for that node to actually amplify. No
diameter-specific capacitance or resonant-frequency spec is available
from the listing — measure or look up once the physical part is on
hand.

---

## SN74HC86N quad 2-input XOR gate

1 ordered 2026-09-03, DIP-14, not yet received. See
[orders.md](orders.md#sn74hc86n-quad-2-input-xor-gate). Standard 74HC86
pinout (verify against the specific manufacturer's datasheet before
building, same caveat as the CD4066B entry above):

| Pin | Function | Pin | Function |
|---|---|---|---|
| 1 | 1A | 8 | 3Y |
| 2 | 1B | 9 | 3A |
| 3 | 1Y | 10 | 3B |
| 4 | 2A | 11 | 4Y |
| 5 | 2B | 12 | 4A |
| 6 | 2Y | 13 | 4B |
| 7 | GND | 14 | VCC |

Four independent 2-input XOR gates. Fills the tier4 `PHASED` gap: XOR is
the standard phase-detector primitive (output duty cycle proportional
to phase difference between two same-frequency square waves), which
feeds tier6 `LOCKIN`. **Listing's own variant string had a truncated
package suffix ("DIP-1")** — treated as DIP-14 until the physical part
confirms otherwise; see the caveat in
[orders.md](orders.md#sn74hc86n-quad-2-input-xor-gate). Long lead = positive; the can body
is marked with a stripe (usually with `−` symbols) on the negative side.
Per the listing's own manual text: solder at 350–380°C for ≤3 seconds
per joint (prolonged heat can damage the electrolyte), keep the working
voltage at or below 80% of the rated voltage for the selected value, and
mount vertically with pin spacing matched to the pad spacing. First
candidate use: bulk output filtering for `psu_medlow_lm317`/
`psu_medlow_usbc`, and higher-capacitance tier3 `CAPBRIDGE` work beyond
what the ceramic kit above covers.
