# KB: RP2040-Zero (ordered 2026-10-05) and the user's breadboard plan

For future LLM sessions.

## Why it was ordered

The user wants a second RP2040 so a circuit can stay wired while the Pico
moves to the next experiment, and a second 800-point breadboard for the same
reason: the user compared breadboard-and-wire against perfboard on cost and
chose breadboards, as long as the breadboard version supports the
validation. So "semi-permanent" in this repo means a circuit left on its own
board with its own controller, not soldered. Don't propose perfboard or
soldered builds as the default. The user also wants the Pico's capabilities
used more (second core, PIO, more peripherals), so a design that can use one
is a reasonable pick for the next design pass.

## What differs from the Pico

Full table in `docs/parts_reference.md#rp2040-zero`. The ones that bite:
`GP16` is the WS2812 (it is the output in `frequency_counter` and
`vibration_driver`), `GP25` has no LED, there is no `ADC_VREF` pin (so
`REFGEN2`'s external-reference idea is Pico-only), `GP29` is a free ADC pin
(the Pico's `GP29` reads VSYS). Pin numbers in breadboard tables (3V3(OUT)
pin 36, GND pin 38) don't exist on it; write tables by silkscreen name when a
circuit moves to it. Pinout was copied from the listing text, which lists
header pins loosely; check against the board's silkscreen on arrival.
Unknown until it arrives: whether headers are fitted, and the USB-C cable
situation (the Pico on the bench uses micro-USB).

## Order ingestion notes

The 2026-10-05 order was reported as four line items in the user's message
with listing text pasted in. Checkout totals and shipping weren't reported, so
none are recorded; the earlier rule (no single-item or under-threshold
shipping fees) is assumed satisfied because the user paid. The magnet listing's
attached test report is for a different size (20×6×2mm) and shows about 11%
total rare earth; recorded as unverified strength. The magnets are
radially magnetized, which changes how `hall_amplifier`'s magnet test is
done (curved side toward the sensor).
