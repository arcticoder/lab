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
  and `psu_low` protection tiers per [history.md](history.md) design
  conversation. See
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

Nothing currently on order.
