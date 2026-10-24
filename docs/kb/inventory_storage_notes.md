# KB: storage bags and the arrival checklist

Audience: future LLM sessions. The user moved inventory organization into this
repo on 2026-10-17 (it had been done in a web chat). The bag map lives in
`docs/inventory.md` § "Storage — which bag holds what"; this note is the rule
for filling it in.

## The bags (corrected 2026-10-17)

`MISC`, `SWITCHES / SENSORS`, `PROTECTION`, `RESISTORS` (three sub-bags:
`10K-1M`, `1K-5.1K`, `10ohm-330ohm`), `BATTERY HOLDERS`, `BREADBOARDS`,
`ICs & LCDs`, `TRANSISTORS / CAPACITORS` (capacitor sub-bags by value range,
one transistor sub-bag), `LEDS`, `INDUCTORS` (the assortment is too big for
`MISC`). **There is no `10K / 1K` bag**: the pasted chat history listed one
and I carried it into the first map; the user corrected it. Take bag lists
from the user's current statement, not from an old chat export.

The user's own assignments (chat history plus corrections): NE555, TL082,
SN74HC86N → `ICs & LCDs`; 3296 trimmers → `10K-1M`; TL431A, IRLZ44N → the
transistor sub-bag; piezo discs (bare and leaded), GY-521, KY-003, MF52AT,
49E and SS49E → `SWITCHES / SENSORS`; ADS1115 module and RP2040-Zero →
`ICs & LCDs`; coin motors and N42 magnets → `MISC`; CY7C68013A board → `MISC`;
inductor assortment → `INDUCTORS`; new 830-point board → `BREADBOARDS`; 1W
resistors already in their own baggie. Everything else was a placement I
chose by function and marked as such.

## Placement rule for a new part

1. By what the part *is*: ICs and display modules → `ICs & LCDs`; sensors,
   switches and transducers (including bare and leaded piezo) → `SWITCHES /
   SENSORS`; discrete transistors, and TO-92 references that look like them →
   the transistor sub-bag; fixed resistors by value range into the three range
   bags; breadboards → `BREADBOARDS`; protection devices (fuses, polyfuses,
   diodes bought for protection) → `PROTECTION`; motors, magnets, oddments →
   `MISC`.
2. **Magnets never go in `SWITCHES / SENSORS`** (Hall sensors, reed/tilt parts);
   own baggie in `MISC`.
3. **Look-alike parts get a baggie each, labelled**: 49E vs SS49E (the SS49E
   listing also sold latching types), 1W 0.1Ω/1Ω vs quarter-watt resistors,
   leaded vs bare piezo.
4. Mains adapters, cables and tools are not bagged. Tell the user, when it
   matters, that magnets stay bubble-wrapped and away from the Hall sensors
   and the drive enclosures (they can't hurt the FX2LP board).
5. Add the bag in the same edit that moves the row from "On Order" to a
   received table, and record the date as "arrived by <date>" when the user
   reports a whole batch without per-item dates.

## Open

- The capacitor sub-bag boundaries are not recorded; the map lists the
  capacitor families, not the sub-bags.

## Jumper wires are not tracked (2026-10-17)

The user dropped jumper and jump-wire inventory because working out which
lengths a build needs is overhead for no benefit. Removed from `inventory.md`
and from every `breadboard.md` parts table, plus the `pico/` repo's parts and
BOM tables. Not removed: wiring-step tables that name a wire type or colour
per connection (they are instructions, not stock). Don't add jumper rows back
to a parts table.

## Hardware added 2026-10-23 (bag not recorded)

M3 hex nuts (black carbon steel, 55) and 304 stainless GB818 pan head M3 screws (50 each of 10, 12, 14 mm) are in `inventory.md` "Prototyping and Cables" with no bag; ask for the bag at the next arrival check. The
five AliExpress items ordered 2026-10-24 (stainless sheet, foam tape, copper pads, copper foil tape, brass rod) need a bag on arrival; the copper pads and the brass rod must be kept away from the N42 discs' bag.
