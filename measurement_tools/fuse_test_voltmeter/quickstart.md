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
- 2× male-male jumper wires
- Your 50 mA polyfuse

## What you're building

One loop: **battery → fuse → resistor → back to battery.** The Pico just
taps two points on that loop to read voltage — it's not part of the power
path.

## Wire it

1. Battery holder's **+** lead → one leg of the fuse.
2. Fuse's other leg → one leg of the 10 Ω resistor. This junction is the
   **probe node**.
3. Resistor's other leg → battery holder's **−** lead. This junction is
   the **ground node**.
4. Jumper: Pico **GP26** → probe node (the junction from step 2).
5. Jumper: Pico **GND** → ground node (the junction from step 3).

That's it — two parts in series across the battery, Pico watching the
midpoint. Leave the battery out of the holder until all the wiring above
is done, then drop it in last.

## Run it

From this folder:

```
mpremote run main.py
```

## What you should see

- A steady reading around **1.4V**, printed roughly 5×/second.
- Touch the resistor's two legs together (a dead short across it) — the
  reading collapses toward **0V**, the terminal prints
  `*** FUSE TRIPPED ***`, and the Pico's onboard LED lights up.
- Let go of the short, wait about 2 minutes for the fuse to cool, and the
  reading climbs back to ~1.4V, the terminal prints `*** fuse reset ***`,
  LED goes off.

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
