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
| SYB-170 (on order, 2-pack) | 170 | same as above | second listing, separate order |
| MB-102 | 400 (300 terminal-strip + 100 distribution-bar) | 8.5 × 5.5 × 1.0cm | [manual](manuals/400-tie-points-solderless-breadboard-_mb-102_-for-diy-electronics.md) |
| Full breadboard (existing inventory) | 830 | — | SunFounder Thales kit, see `pico/docs/inventory.md` |

MB-102 terminal strips: rows labeled a–e and f–j are connected horizontally
within a row, split by the center DIP channel. Distribution bars (side
rails) are marked red (+) / blue (−) and run vertically the length of the
board. Rated for low-voltage prototyping only, current limit ~2A per the
manual; wire gauge 21–26 AWG recommended for the spring clips.

---

## CD4066B (quad bilateral switch)

10 ordered, DIP-14 package. Four independent analog switches, each gated by
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

10 ordered, DIP-8. Standard pinout:

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
`spacetime_lab_budget.md` calls out precision op-amps (OPA2277, TL072) as
the preferred choice where noise/offset actually matters; LM358 is the
budget/bring-up substitute.

---

## USB-C 16-pin test breakout board

Board size 21.6×14.2mm, 2.54mm hole pitch, FR-4, double-sided (front/back
plug testing). Breakout pads, as silkscreened:

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
`psu_ultralow`/`psu_low` design (see [history.md](history.md)). Trip
current and trip time are *not* implied by the part number alone (typically
higher than hold current by some multiple, and time-dependent) — check the
Littelfuse/Bourns datasheet for the exact trip curve before relying on a
specific trip threshold.

Both values received 2026-08-21 (20 each):

- RXEF005 (0.05A / 50mA) — `psu_ultralow` tier
- RXEF050 (0.5A / 500mA) — `psu_low` tier

Not yet validated per-unit — see [orders.md](orders.md#polyfuses-rxef005-and-rxef050)
and [fuse_test_voltmeter](../fuse_test_voltmeter/) for the per-fuse
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
