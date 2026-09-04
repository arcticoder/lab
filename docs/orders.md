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

### Panel-mount fuse holder (6×30mm)

- 1 received. EGBO brand, panel opening 12/14mm, rated 10A/250V. See
  [parts_reference.md](parts_reference.md#panel-mount-fuse-holder). Pairs
  with the 2A glass tube fuses below for the `psu_medlow` protection tier —
  neither has a circuit built against it yet.
- Logged received: 2026-09-01.

### NE555 timer IC (DIP-8)

- 10 received, DIP-8 package. See
  [parts_reference.md](parts_reference.md#ne555-timer) for pinout. Not yet
  validated per-unit (bulk IC batch, no test jig built yet) — run each
  through a bring-up check before trusting it in tier1 `OSC` or tier2
  `FREQC`.
- Logged received: 2026-09-01.

### Glass tube fuses, 6×30mm 250V

- 10 received, all 2A fast-blow. See
  [parts_reference.md](parts_reference.md#glass-tube-fuses-6x30mm). Not yet
  validated per-unit (bulk consumable-fuse batch, no test jig built yet —
  distinct from the polyfuse tester in
  [measurement_tools/fuse_test_voltmeter/](../measurement_tools/fuse_test_voltmeter/),
  which tests resettable PTC polyfuses, not glass cartridge fuses). Pairs
  with the panel-mount holder above for `psu_medlow`.
- Logged received: 2026-09-01.

### 3296W trimming potentiometer

- 10 received, all 10kΩ. The listing title called this "multi-turn," but
  the 3296 package designation is the standard Bourns-style single-turn
  cermet trimmer — treat "multi-turn" as unverified marketing copy until
  the physical part confirms actual wiper behavior. See
  [parts_reference.md](parts_reference.md#3296-trimming-potentiometer).
- Used as Rb in [oscillators/ne555_astable](../oscillators/ne555_astable/)
  (tier1 `OSC`, designed & simulated, not yet bench-built).
- Logged received: 2026-09-01.

### TL431A precision shunt reference (TO-92)

- 5 received, TO-92 package. Untested. Supports tier1 `REF` — an
  adjustable bandgap shunt reference, a more precise alternative to the
  resistor-divider + LM358 buffer approach in
  [voltage_reference_lm358](../signal_conditioning/voltage_reference_lm358/).
  See [parts_reference.md](parts_reference.md#tl431a-precision-shunt-reference).
- Logged received: 2026-09-01.

### 18-in-1 wire stripper/crimper pliers

- 1 received. Not an electrical component — a tool; logged in
  [pico/docs/inventory.md](../../pico/docs/inventory.md) Tools table, not
  here. Resolves the wire-stripper dependency that was blocking AA
  battery holder lead termination for `psu_ultralow_v1`/`psu_low_v2` (see
  [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)).
- **Note:** the URL given for this listing was identical to the glass
  tube fuse listing above (`1005003099267179`) — almost certainly a
  paste artifact, since the two products are unrelated. Not corrected
  here; re-verify the actual order/tracking details against the AliExpress
  order history rather than the URL in this note if it's ever needed.
- Logged received: 2026-09-03.

### Metal film resistor kit (1W, 1%)

- Listing: "20pcs 1W Metal film resistor 1% 0.1R-2.2M 10R 22R 47R 100R
  330R 1K 4.7K 10K 22K 47K 1" —
  https://www.aliexpress.com/item/1005001652734632.html
- **Correction (2026-09-03): this was not a single 20-piece assortment
  pull.** The listing lets the buyer pick specific values instead of an
  assortment, and two separate selections of 20 units each were made from
  it — 20× 0.1Ω and 20× 1Ω, 40 resistors total, no other values included.
  The earlier "20 ordered, assorted values… notably including 0.1Ω"
  description in this file and in
  [parts_reference.md](parts_reference.md#metal-film-resistor-kit-1w-1)
  was wrong on both the total count and the "assorted" framing; both have
  been corrected.
- 0.1Ω (20 received): not previously stocked (the SunFounder Thales kit's
  resistor assortment bottoms out at 10Ω, per
  [pico/docs/inventory.md](../../pico/docs/inventory.md)). Also 1W-rated,
  above the Thales kit's 1/4W (0.25W) ceiling. Supports replacing the
  jumper-wire-chain shunt currently used in
  [measurement_tools/ammeter_1ohm](../measurement_tools/ammeter_1ohm/)
  (see
  [measurement_tools/resistance_measurement](../measurement_tools/resistance_measurement/)
  for how that chain was characterized at ~1.005Ω in the absence of a
  0.1Ω part) with an actual 0.1Ω resistor.
- 1Ω (20 received): not yet assigned to a tier — candidate reference
  resistor for a tier3 `OHMMETER` (4-wire Kelvin) build alongside the
  0.1Ω value.
- Logged received: 2026-09-03.

### PT334-6C photodiode (5mm)

- Listing: "10pcs/lot PT334-6C 5MM photodiodes photodiode new original In
  Stock" — https://www.aliexpress.com/item/1005007386609423.html
- 10 received. Candidate for a tier2 `TIA` (transimpedance amplifier)
  build alongside the on-hand LM358P — see
  [parts_reference.md](parts_reference.md#pt334-6c-photodiode).
- Logged received: 2026-09-03.

---

## On order (placed, not yet received)

### Color-ring inductor assortment (0307, 1/4W)

- Listing: "12values Color Ring Inductor Assortment 0307 1/4W 0.25W 0410
  1/2W 0510 1W 1UH 10UH 100UH Inductors Inductors Assorted Set Kit" —
  https://www.aliexpress.com/item/32988801481.html (variant selected:
  "0307-120PCS-1lot").
- 120 ordered (12 values × 10pcs). The listing title bundles three
  different package sizes (0307 1/4W, 0410 1/2W, 0510 1W) under one
  product; the selected variant is the 0307 1/4W size only. Values: 1µH,
  10µH, 22µH, 33µH, 47µH, 100µH, 150µH, 220µH, 330µH, 470µH, 560µH, 1mH.
  Axial, color-ring-coded, epoxy-coated. Rated dielectric withstand 250V
  AC rms, operating temperature −25 to 85°C.
- Supports: tier3 `INDBRIDGE` (inductance bridge) directly, and any
  future filter/oscillator tank-circuit use. See
  [parts_reference.md](parts_reference.md#color-ring-inductor-assortment-0307-14w).
- Ordered: 2026-08-30.

### Multilayer ceramic capacitor assortment (50V)

- Listing: "300pcs 10Value 50V 10pF 20pF 30pF 47pF 56pF 68pF 100pF 1nF
  10nF 100nF Multilayer Ceramic Capacitor Assortment Monolithic Kit Box" —
  https://www.aliexpress.com/item/1005004741548166.html. **No specific
  variant was given for this item** (unlike the other two orders in this
  batch) — the listing may not have a selectable variant at all (a single
  fixed 10-value/300pc box), but that isn't confirmed; check the actual
  AliExpress order history once it ships rather than assuming.
- 300 ordered (10 values × 30pcs). Values: 10pF, 20pF, 30pF, 47pF, 56pF,
  68pF, 100pF, 1nF, 10nF, 100nF. Through-hole/in-line MLCC, 50V rated,
  10% tolerance, 5.08mm lead pitch.
- **Discrepancy in the listing itself:** the structured "Specifications"
  block states operating temperature −40 to 80°C, but the free-text
  product description states −25°C to 185°C for the same part. Don't
  trust either figure as confirmed until a datasheet or physical
  markings are available — flagged rather than picking one.
- Supports: tier3 `CAPBRIDGE` (capacitance bridge) directly, plus general
  bypass/decoupling and NE555-timing (tier1 `OSC`) use once received. See
  [parts_reference.md](parts_reference.md#multilayer-ceramic-capacitor-assortment-50v).
- Ordered: 2026-08-30.

### Aluminum electrolytic capacitor kit (16V/25V/50V)

- Listing: "120pcs Electrolytic Capacitor 16V 25V 50V Aluminum
  Electrolytic Capacitor Kit 12 Values 1uF-470uF DIP Electrolyte
  Capacitors". **The user-supplied URL for this item was a literal
  placeholder (`https://www.aliexpress.com/item/???.html`) — the real
  item ID was never provided.** Per the "don't guess a URL" convention
  (see [kb/ordering_ingestion_notes.md](kb/ordering_ingestion_notes.md)),
  no URL is recorded here; re-derive it from the AliExpress order history
  once the item ships rather than trusting any link that might get
  attached to this entry later.
- 120 ordered (12 values × 10pcs), brand YTDMEN, radial-lead DIP-style,
  ±20% tolerance:
  1. 50V 1µF
  2. 50V 2.2µF
  3. 50V 3.3µF
  4. 50V 4.7µF
  5. 50V 10µF
  6. 25V 22µF
  7. 25V 33µF
  8. 25V 47µF
  9. 16V 100µF
  10. 16V 220µF
  11. 16V 330µF
  12. 16V 470µF
- Supports: general PSU output/bulk filtering (`psu_medlow_lm317`,
  `psu_medlow_usbc`) and future tier3 `CAPBRIDGE` use at higher
  capacitance than the ceramic kit above covers. See
  [parts_reference.md](parts_reference.md#aluminum-electrolytic-capacitor-kit-1665025050v).
- Ordered: 2026-08-30.
