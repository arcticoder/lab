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

M3 hex nuts (black carbon steel, 55) and 304 stainless GB818 pan head M3 screws (50 each of 10, 12, 14 mm) are in `inventory.md` "Prototyping and Cables" with no bag; ask for the bag at the next arrival check.

The five AliExpress items of 2026-10-24 (stainless sheet, foam tape, copper pads, copper foil tape, brass rod) arrived 2026-11-05 and were assigned a new bag, `BALANCE MATERIALS` (the stainless sheet is a roll, despite the listing's "plate" title, and goes in loosely with nothing pressing on it; a crease ruins it). Keep the copper pads and the brass rod apart from the N42 discs' bag (`MISC`). The user had not yet measured the rod (100 mm stated) or run the magnet check on pads, rod and sheet. The M3 nuts and screws above still have no bag recorded.

## Top-level bags (user, 2026-11-20)

Three outer freezer bags: `ELECTRONICS` (the labelled bags above are inner bags of it), `BALANCE MATERIALS` (no inner bags: small items such as weights get their own baggie) and `MISC TOOLS` (M3 hardware, washers, blades, files, calipers and cells). Magnetic or magnet-sensitive balance parts (steel weights) stay out of the bag with the N42 discs (`MISC` in `ELECTRONICS`).

## Tools photos (2026-11-20)

Five photos of the two tool bags' contents (not the `SCREWS + NUTS` or `NOZZLES` sub-bags, not `BALANCE MATERIALS`) are extracted in `spurious-force-balance/docs/img/inbox/tools_bags_2026-11-20/` (git-ignored; the zip is deleted). The mat has a printed cm grid, so quote items as photo number plus x/y in cm. Photo order by file name: 1 calipers and cutters, 2 glue and red printed part, 3 tweezers and iron parts, 4 soldering stand and files, 5 blue films and washers. The filing plan in `inventory.md` is final as of the identifications below; the user sorts the bags. Note: the photos are not a complete tool list (the user has other tools; ask when a tool is not listed), and the two tool bags have no specific purpose (items went into whichever had room). Identified by the user: photo 2 red part = printed solder-wire holder; photo 3 black cylinder = printed revolver screwdriver; photo 4 yellow stand and rod = iron holder with an extra tip; photo 5 films = double-sided acrylic adhesive squares. Formerly unidentified: photo 2 red printed clamp-like part (x 15-22, y 0-8); photo 3 black printed cylinder (x 12-22, y 16-20) and black printed holder (x 17.5-22, y 21-25), pointed rod and yellow oval stand in photo 4 (x 15-20, y 15-21), the five blue-tinted 6 cm film squares and the bag labelled "shuangmian-6x6-10PCS" in photo 5 (x 1-14, y 1-22).

