# fuse_test_voltmeter — Quickstart (one fuse, what's on your bench right now)

This is for exactly what you have in front of you: **one AA battery
holder, one 50 mA polyfuse, one Pico on a breadboard, USB already
connected.** Not batches, not the 500 mA fuse, not a PSU — just this one
part.

(For the 500 mA fuse, testing more than one fuse, or building the PSU
demo afterward, see [breadboard.md](breadboard.md) instead — that file
covers the general/batch procedure this one doesn't.)

## Parts to add to what's already on the breadboard

- 1× AA battery (fresh)
- 1× 10 Ω resistor, 1/4 W (any one from the kit's resistor drawer)
- 1× slide switch (SPDT) — arm/disarm signal, see step 6 below
- 4× male-male jumper wires (2 for the probe, 2 for the switch)
- 1× spare male-male jumper wire (or a bent solid-core jumper), kept aside
  for shorting the resistor later — don't wire this one in yet
- Your 50 mA polyfuse

## What you're building

One loop: **battery → fuse → resistor → back to battery.** The Pico just
taps two points on that loop to read voltage — it's not part of the power
path. A second, separate switch tells the Pico "I'm intentionally
connecting/disconnecting the battery right now" so it doesn't mistake that
for a real fuse trip.

## Wire it

1. Battery holder's **+** lead → one leg of the fuse.
2. Fuse's other leg → one leg of the 10 Ω resistor. This junction is the
   **probe node**.
3. Resistor's other leg → battery holder's **−** lead. This junction is
   the **ground node**.
4. Jumper: Pico **GP26** → probe node (the junction from step 2).
5. Jumper: Pico **GND** → ground node (the junction from step 3).
6. Arm switch — this is a separate signal path, not part of the battery
   loop above:
   - Switch pin 2 (the middle/common pin) → Pico **GP15**.
   - Switch pin 1 → Pico **3V3(OUT)**.
   - Switch pin 3 → leave unconnected. Don't wire it to GND — the switch
     only ever bridges pin 2 to *one* outer pin at a time, so wiring both
     outer pins to GND and 3V3 would let a single slide direction connect
     GP15 to one rail while leaving the other rail dangling one pin away
     for no reason; `main.py` uses GP15's internal pull-down to read a
     defined LOW when pin 3 is selected, so the unconnected pin still gives
     a clean DISARMED reading, not a floating one.

That's it — two parts in series across the battery, Pico watching the
midpoint, plus the arm switch off to the side. Leave the battery out of
the holder until all the wiring above is done, then drop it in last.

## Run it

From this folder:

```
mpremote run main.py
```

Slide the arm switch back and forth once and watch the terminal — one
direction prints `-- ARMED --`, the other `-- DISARMED --`. Note which
physical direction is which (the switch has no printed markings), then
leave it on **DISARMED** before you drop the battery in.

## What you should see

- With the switch DISARMED and the battery seated, the reading settles —
  trip/reset detection is suspended in this state, so an unsteady or
  near-zero number here is expected, not a fault.
- Slide to **ARMED**. You should now see a steady reading around **1.4V**,
  printed roughly 5×/second, with no `TRIPPED`/`reset` chatter from the act
  of arming itself.
- With a spare jumper wire (or the bent one you set aside), bridge the
  resistor's two breadboard rows directly — plug both ends into the same
  two rows the resistor's legs occupy, rather than hand-holding two wire
  tips against the leads. Touching bare leads together is a spotty, easy
  to fumble connection; a jumper seated in the breadboard rows gives a
  firm, repeatable short. This collapses the reading toward **0V**, prints
  `*** FUSE TRIPPED ***`, and lights the Pico's onboard LED.
- Pull that jumper, wait about 2 minutes for the fuse to cool, and the
  reading climbs back to ~1.4V, the terminal prints `*** fuse reset ***`,
  LED goes off.
- Before disconnecting the battery again, slide back to **DISARMED** first
  — otherwise the drop to 0V as you pull it reads as another trip.

**A good fuse can also trip on its own, before you touch anything** — this
10 Ω load already draws ~150 mA, 3x the fuse's 50 mA rating, so a fresh
unit may self-trip within seconds of the battery going in. If that
self-trip clears again almost immediately (sub-second, not the ~2 minute
figure above) and keeps repeating, that's the fuse chattering right at its
trip threshold under this marginal overload — not a full cool-down cycle,
and not necessarily a bad unit. The real pass/fail check is still the
deliberate short above: it should trip promptly, *stay* tripped once you
let go, and take the full ~2 minutes to recover. If a fuse won't hold a
trip for that long after a genuine short, that's a fail.

## Pass / fail

- **Pass**: trips when shorted, fully resets after cooling, cold reading
  lands close to 1.4V.
- **Fail**: doesn't trip, doesn't reset, or reads far off 1.4V — set that
  fuse aside, don't wire it in front of an LED.

## If the reading looks wrong before you even touch the fuse

Pull the fuse and bridge steps 1–2 with a spare jumper wire instead (no
fuse anywhere in the loop). If the reading still isn't near 1.4V, or
shorting the resistor doesn't print the trip message, the problem is the
Pico wiring (GP26/GND), not the fuse — fix that first.

**If it's landing consistently around 1.0–1.1V instead (same result across
more than one fuse, so not a fuse-specific problem)**, check the battery
chemistry before suspecting wiring: 1.4V assumes a fresh 1.5V alkaline
cell. A NiMH rechargeable AA is 1.2V nominal, and 1.2V through this same
10 Ω/cold-fuse math lands around 1.14V — already most of the gap, with the
rest plausibly ordinary battery sag under the ~150 mA this load draws.
There's no multimeter on this bench, but the Pico can substitute: with
ARMED off, temporarily move the GP26/GND jumpers straight onto the battery
holder's two leads (bypassing the fuse and resistor entirely) and read the
open-circuit voltage directly — 1.5–1.65V confirms alkaline (a fresh cell
with nothing loading it commonly rests a bit above the 1.5V nominal, so a
reading like 1.6V here isn't a fault), close to 1.2–1.3V means it's NiMH
(or a partly-discharged cell), which explains a sub-1.4V resting reading on
its own, independent of any wiring fault.
