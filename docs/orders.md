# AliExpress Component Orders

Running log of components ordered for the spacetime research lab build. Each
entry cross-references which subsystem in
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md) it
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
  [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md)
  `psu_ultralow`/`psu_low` subgraphs.
- Logged received: 2026-08-21.

---

## On order (placed, not yet received as of 2026-08-21)

| Item | Variant ordered | Qty | Manual/notes |
|---|---|---|---|
| SYB-170 mini breadboard (2pk) | SYB-170 Breadboard | 2 | Second small-breadboard source, distinct listing from the received 6-pack above |
| MB-102 breadboard | 400 tie-point (300 terminal + 100 distribution) | 1 | [manual](manuals/400-tie-points-solderless-breadboard-_mb-102_-for-diy-electronics.md) — full-size board for larger builds (tier2+) |
| CD4066BCN | Quad bilateral analog switch, DIP-14 | 10 | See [parts_reference.md](parts_reference.md#cd4066b-quad-bilateral-switch) |
| LM358P | Dual op-amp, DIP-8 | 10 | See [parts_reference.md](parts_reference.md#lm358-dual-op-amp) |
| TYPE-C Female Test Board | USB3.1 16P → 2.54mm breakout, blue | 1 | See [parts_reference.md](parts_reference.md#usb-c-16-pin-test-breakout-board) |
| RXEF005 polyfuse | 0.05A / 50mA | 20 | Matches `psu_ultralow` protection per [history.md](history.md) design conversation |
| RXEF050 polyfuse | 0.5A / 500mA | 20 | Matches `psu_low` protection |
| 1N5817 Schottky diode | 1A 20V, DO-41 | 20 | [manual](manuals/schottky-rectifier-diodes-in5817-1a20v-do-41.md) — `psu_low` reverse-polarity protection |
| AA battery holder (1×AA) | 1AA, single-cell, lead cables | 5 | [manual](manuals/aa-power-battery-holder-lr6-container-with-lead-cables.md) — `psu_ultralow`/`psu_low` |

None of the on-order items are reflected in `pico/docs/inventory.md` yet —
they move from this table into that inventory (and out of "on order" here)
once physically received, same as the SYB-170 6-pack above.
