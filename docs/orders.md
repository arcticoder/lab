# AliExpress Component Orders

Running log of components ordered for the lab build. Each entry
cross-references which subsystem in
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)
or [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) it
supports. Physical part counts are mirrored into the sibling `pico/` repo's
[`pico/docs/inventory.md`](../../pico/docs/inventory.md), which is the
shared master inventory across both repos — update both files together.

Datasheets/manuals for these parts, where available, are converted to
Markdown under [docs/manuals/](manuals/) (the source PDFs are gitignored;
the converted `.md` files are tracked).

---

## Received

### SYB-170 Mini Breadboard — 6-in-1 pack (black selected)

- Listing: "1-6 Pcs Mini Breadboard Kit with 170 Tie Points - Solderless
  SYB-170 Prototype PCB Bread Board for Arduino, Raspberry Pi More"
  (variant: black)
- Type SYB170, 170 tie points, 1mm hole diameter, 2.54mm hole pitch, 10mm
  thick, rated 300V / <5A, self-adhesive back, boards can be interlocked for
  expansion.
- Compatible with 22–29 AWG jumper wire.
- Supports: bootstrap-tier builds needing a small breadboard footprint
  (`psu_ultralow_v1`, `psu_low_v2`) — see
  [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)
  `psu_ultralow`/`psu_low` subgraphs.
- Logged received: 2026-08-21.

### Polyfuses (RXEF005 and RXEF050)

- 20 of each hold-current variant received, matching the `psu_ultralow`
  and `psu_low` protection tiers. See
  [parts_reference.md](parts_reference.md#polyfuses-rxef-series) for the
  RXEF naming convention and trip-curve caveat.
- Not yet validated per-unit — before trusting any individual fuse in
  front of an LED, run it through
  [fuse_test_voltmeter](../measurement_tools/fuse_test_voltmeter/) to confirm cold-state
  resistance and correct trip/reset behavior. Bulk AliExpress buys have a
  nonzero DOA rate, so "received" here does not yet mean "known good."
- Logged received: 2026-08-21.

### 1N5817 Schottky diode (1A 20V, DO-41)

- 20 received, for `psu_low` reverse-polarity protection.
- Not yet validated per-unit — check forward drop (~0.35–0.45V) on each
  before wiring into `psu_low_v2`; see
  [psu_low_v2/README.md](../power_supplies/psu_low_v2/README.md#validation-without-a-multimeter)
  for the Pico-probe procedure used to check it without a multimeter.
- Manual: [schottky-rectifier-diodes-in5817-1a20v-do-41.md](manuals/schottky-rectifier-diodes-in5817-1a20v-do-41.md)
  (source PDF is scanned/image-only with no text layer — listing
  description used instead, see the manual file for the caveat).
- Logged received: 2026-08-21.

### AA battery holder (1×AA, single-cell)

- 5 received, for `psu_ultralow`/`psu_low` tiers.
- No validation step needed — ready for direct use in
  [psu_ultralow_v1](../power_supplies/psu_ultralow_v1/) and
  [psu_low_v2](../power_supplies/psu_low_v2/) builds.
- Manual: [aa-power-battery-holder-lr6-container-with-lead-cables.md](manuals/aa-power-battery-holder-lr6-container-with-lead-cables.md)
- Logged received: 2026-08-21.

### SYB-170 mini breadboard (2pk)

- Listing: "SYB-170 Breadboard", second small-breadboard source, distinct
  from the received 6-pack above.
- 2 received.
- Supports: same bootstrap-tier builds as the black SYB-170 above.
- Logged received: 2026-08-24.

### MB-102 breadboard (400 tie-point)

- 300 terminal-strip + 100 distribution-bar tie points, full-size board
  for larger builds (tier2+). Manual:
  [400-tie-points-solderless-breadboard-_mb-102_-for-diy-electronics.md](manuals/400-tie-points-solderless-breadboard-_mb-102_-for-diy-electronics.md).
- 1 received.
- Logged received: 2026-08-24.

### CD4066BCN (quad bilateral switch, DIP-14)

- 10 received. See
  [parts_reference.md](parts_reference.md#cd4066b-quad-bilateral-switch)
  for pinout. Bring-up/validation jig:
  [measurement_tools/cd4066_switch_tester/](../measurement_tools/cd4066_switch_tester/) —
  not yet validated per-unit (40 individual switches across 10 chips);
  run each switch through the tester before trusting it in a downstream
  design (tier9 `MUX`, tier4 `DEMOD`).
- Logged received: 2026-08-24.

### LM358P (dual op-amp, DIP-8)

- 10 received. See
  [parts_reference.md](parts_reference.md#lm358-dual-op-amp) for pinout.
  First use:
  [signal_conditioning/voltage_reference_lm358/](../signal_conditioning/voltage_reference_lm358/)
  (tier1 `REF`).
- Logged received: 2026-08-24.

### TYPE-C Female Test Board (USB3.1 16P → 2.54mm breakout, blue)

- 1 received. See
  [parts_reference.md](parts_reference.md#usb-c-16-pin-test-breakout-board)
  for the pad list and the `U+`/`D+` transcription caveat — verify against
  the physical silkscreen now that it's on hand.
- Logged received: 2026-08-24.

---

## On order (placed, not yet received)

### 3296W trimming potentiometer

- Listing: "10PCS 3296W Potentiometer Precision Adjustable Resistance
  Multi-turn Trimming 1K 2K 5K 10K 100K 103 100R Trimmer Potentiometer"
  (variant selected: "10K Ohm").
- 10 ordered, all 10kΩ. The listing title bundles several resistance
  values under one product; only the 10kΩ variant was selected.
- The title calls this "multi-turn," but the 3296 package designation is
  the standard Bourns-style single-turn cermet trimmer (top-adjust screw,
  ~25 turns of the screw ≠ multi-turn wiper travel) — treat "multi-turn"
  as unverified marketing copy until the physical part confirms actual
  wiper behavior. See
  [parts_reference.md](parts_reference.md#3296-trimming-potentiometer).
- Supports: tier1 `OSC`/reference-adjustment use (calibration trim), per
  [spacetime_lab_budget.md](spacetime_lab_budget.md)'s "Trim
  Potentiometers" line.
- Ordered: 2026-08-25.

### Panel-mount fuse holder (6×30mm)

- Listing: "EGBO 1~10PCS 5×20mm & 6×30mm Glass Fuse Holders (EGBO,
  1~10PCS): Panel Mount Socket for Fuse Panels" (variant selected:
  "6X30mm 1PCS").
- 1 ordered. Panel-mount socket, opening 12/14mm, rated 10A/250V.
- Supports: `psu_medlow` protection tier, paired with the 2A glass fuse
  below. See
  [parts_reference.md](parts_reference.md#panel-mount-fuse-holder).
- Ordered: 2026-08-25.

### NE555 timer IC (DIP-8)

- Listing: "10-100PCS NE555 555 DIP-8 IC Timers NEW GOOD QUALITY
  PRECISION TIMERS" (variant selected: "DIP-10PCS").
- 10 ordered, DIP-8 package.
- Supports: tier1 `OSC` (precision timing oscillator) and tier2 `FREQC`
  (basic frequency counter, typically 555-gated). See
  [parts_reference.md](parts_reference.md#ne555-timer).
- Ordered: 2026-08-25.

### TL431A precision shunt reference (TO-92)

- Listing: "5piece TL431A TL431 TO-92".
- 5 ordered, TO-92 package.
- Supports: tier1 `REF` — an adjustable bandgap shunt reference, a more
  precise alternative to the resistor-divider + LM358 buffer approach in
  [voltage_reference_lm358](../signal_conditioning/voltage_reference_lm358/).
  See [parts_reference.md](parts_reference.md#tl431a-precision-shunt-reference).
- Ordered: 2026-08-25.

### Glass tube fuses, 6×30mm 250V

- Listing: "Hzy 10pcs multimeter Fuse Quick Fast Blow Fuse Glass Tube
  thermo Fuses 6*30mm 250V 1A/2A/3A/4A/5A/6A/7A/8A/10A/15A/20A/25A/30A"
  (variant selected: "2A").
- 10 ordered (lot of 10 per the listing's unit type), all 2A fast-blow.
- Supports: `psu_medlow` protection tier, paired with the panel-mount
  holder above. See
  [parts_reference.md](parts_reference.md#glass-tube-fuses-6x30mm).
- Ordered: 2026-08-25.

### 18-in-1 wire stripper/crimper pliers

- Listing: "18 in 1 Electrician Pliers Multifunctional Wire Stripper
  Crimper Cutting Pliers Professional Electrical Repair Hand Tool".
  High-carbon steel + PVC handle, insulated/non-insulated terminal
  crimping, common AWG stripping gauges.
- 1 ordered. Not an electrical component — a tool. Resolves the
  wire-stripper dependency that's been blocking AA battery holder lead
  termination for `psu_ultralow_v1`/`psu_low_v2` (see
  [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)).
- **Note:** the URL given for this listing was identical to the glass
  tube fuse listing above (`1005003099267179`) — almost certainly a
  paste artifact, since the two products are unrelated. Not corrected
  here; re-verify the actual order/tracking details against the AliExpress
  order history rather than the URL in this note once the item ships.
- Ordered: 2026-08-25.

### Metal film resistor kit (1W, 1%)

- Listing: "20pcs 1W Metal film resistor 1% 0.1R-2.2M 10R 22R 47R 100R
  330R 1K 4.7K 10K 22K 47K 1" —
  https://www.aliexpress.com/item/1005001652734632.html
- 20 ordered, assorted values from the listing's range, notably including
  **0.1Ω** — not previously stocked (the SunFounder Thales kit's resistor
  assortment bottoms out at 10Ω, per
  [pico/docs/inventory.md](../../pico/docs/inventory.md)).
- Also 1W-rated, above the Thales kit's 1/4W (0.25W) ceiling.
- Supports: replacing the jumper-wire-chain shunt currently used in
  [measurement_tools/ammeter_1ohm](../measurement_tools/ammeter_1ohm/)
  (see
  [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/)
  for how that chain was characterized at ~1.005Ω in the absence of a
  0.1Ω part) with an actual 0.1Ω resistor once received. See
  [parts_reference.md](parts_reference.md#metal-film-resistor-kit-1w-1).
- Ordered: 2026-08-30.

### PT334-6C photodiode (5mm)

- Listing: "10pcs/lot PT334-6C 5MM photodiodes photodiode new original In
  Stock" — https://www.aliexpress.com/item/1005007386609423.html
- 10 ordered.
- Not yet assigned to a tier in
  [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)
  or [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) —
  candidate for a future light-sensing/photodetector interface circuit.
  See [parts_reference.md](parts_reference.md#pt334-6c-photodiode).
- Ordered: 2026-08-30.
