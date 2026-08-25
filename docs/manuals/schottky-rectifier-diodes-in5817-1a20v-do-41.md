# Schottky Rectifier Diodes — 1N5817 (1A 20V, DO-41)

> **Extraction note:** the source PDF (`schottky-rectifier-diodes-in5817-1a20v-do-41.pdf`,
> 15 pages) is scanned/image-only with no embedded text layer — `markitdown` and
> `pdftotext -layout` both return zero characters. No OCR pass has been run.
> The content below is the seller's listing description as given at order time,
> not an OCR transcription of the PDF. If page-image detail (e.g. a printed
> outline drawing) is ever needed, re-open the PDF directly.

## Listing / variant ordered

- AliExpress item: "20pcs DIP Schottky Rectifier Diodes 1N5408 IN5408 IN 1N 5401
  5402 5404 5406 5399 5822 5817 5819 5824 Diodes 1A 5A 3A 1000V 200V"
- Variant selected: **IN5817 1A20V DO-41** — i.e. this order is 1N5817 parts,
  not the other part numbers bundled into the listing title.
- Package: DO-41 through-hole.

## Key specs (1N5817)

- Forward current: 1A
- Reverse voltage: 20V
- Package: DO-41
- Schottky junction — lower forward voltage drop (~0.45V typical) than a
  silicon rectifier (~0.7V), and faster switching, at the cost of higher
  reverse leakage and lower reverse voltage rating.
- Cathode is marked with a band on the DO-41 body; anode is the unmarked end.

## Use in this project

Matches the Schottky diode called for in the `psu_low` power tier in
[general_purpose_circuit_dependency.md](../general_purpose_circuit_dependency.md)
(reverse-polarity / back-EMF protection in series with the 2×AA supply) —
see `history.md` for why this part was chosen over a generic 1N5408.
