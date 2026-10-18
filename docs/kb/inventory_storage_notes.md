# KB: storage bags and the arrival checklist

Audience: future LLM sessions. The user moved inventory organization into this
repo on 2026-10-17 (it had been done in a web chat). The bag map lives in
`docs/inventory.md` § "Storage — which bag holds what"; this note is the rule
for filling it in.

## The twelve bags

`MISC`, `SWITCHES / SENSORS`, `PROTECTION`, `10K / 1K`, `10K-1M`, `1K-5.1K`,
`10R-330R`, `BATTERY HOLDERS`, `BREADBOARDS`, `ICs & LCDs`, `TRANSISTORS /
CAPACITORS` (subdivided: capacitor sub-bags by value range, one transistor
sub-bag), `LEDS`. The assignments the user had already made (from the chat
history they pasted): NE555, TL082, SN74HC86N → `ICs & LCDs`; 3296 trimmers →
`10K-1M`; TL431A, IRLZ44N → the transistor sub-bag; piezo discs, GY-521,
KY-003, MF52AT → `SWITCHES / SENSORS`; CY7C68013A board and the inductor
assortment → `MISC`. Everything else in the map is a placement chosen by
function on 2026-10-17 and marked as such where it was a judgment call.

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
4. Mains adapters, cables and tools are not bagged.
5. Add the bag in the same edit that moves the row from "On Order" to a
   received table, and record the date as "arrived by <date>" when the user
   reports a whole batch without per-item dates.

## Open

- `10K / 1K`: the chat history doesn't say what it holds. It is the one bag
  that mixes the two resistors that differ in a single colour band (`brown
  black black brown brown` against `... red brown`); the lock-in's `Rbias`
  slot held a 10kΩ, so the map suggests splitting it. Ask once, then fill in.
- The capacitor sub-bag boundaries are not recorded; the map lists the
  capacitor families, not the sub-bags.

## Jumper wires are not tracked (2026-10-17)

The user dropped jumper and jump-wire inventory because working out which
lengths a build needs is overhead for no benefit. Removed from `inventory.md`
and from every `breadboard.md` parts table, plus the `pico/` repo's parts and
BOM tables. Not removed: wiring-step tables that name a wire type or colour
per connection (they are instructions, not stock). Don't add jumper rows back
to a parts table.
