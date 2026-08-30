# Breadboard Wiring — psu_medlow_lm317

**This kit has not been physically built or tested yet.** The wiring below
is the standard LM317 adjustable-regulator topology mapped onto this kit's
exact BOM (see [README.md](README.md) § Design), not a confirmed-correct
trace-by-trace reading of the actual PCB. Confirm against the board's
silkscreen once it arrives, and update this file if anything here turns
out to be wrong — same treatment as any other "designed, not yet built"
circuit in this repo.

## Circuit overview

DC barrel jack → 1N4004 (reverse-polarity protection) → 100µF input cap →
LM317 (IN/OUT/ADJ) → switch-selected feedback network (3.3V or 5V) → 10µF
output cap → output header pins. A second switch gates the barrel jack's
positive lead as the main power on/off. A red LED off the output rail
indicates power is present.

**No `.spice` netlist** — see README.md for why.

---

## Parts required

All parts come from the kit itself (see README.md § Kit contents) — no
substitutions needed from the shared inventory.

---

## Wiring steps

### 1. Input protection and smoothing

| From | To |
|------|----|
| DC barrel jack (+) | 1N4004 anode |
| 1N4004 cathode (banded end) | LM317 IN pin, and 100µF cap (+) |
| 100µF cap (−) | GND rail |
| DC barrel jack (−) / sleeve | GND rail |

### 2. Main power switch

Insert the first SPDT slide switch in series between the barrel jack's
positive lead and the 1N4004 anode (from step 1), so it fully de-powers the
board rather than just gating the output.

### 3. LM317 output and feedback network

| From | To |
|------|----|
| LM317 OUT | 10µF cap (+), and output header (+) |
| 10µF cap (−) | GND rail |
| LM317 ADJ | R1 (240Ω) to GND rail |
| LM317 ADJ | 0.1µF bypass cap to GND rail |
| LM317 OUT | R2 base (390Ω) to LM317 ADJ |

### 4. Voltage-select switch

Wire the second SPDT slide switch so its common connects into the ADJ-side
node of the 390Ω resistor from step 3:

- **3.3V throw**: leaves the 390Ω alone (ADJ node ties straight to R1).
- **5V throw**: routes through the second 330Ω resistor in series before
  reaching R1, adding it to the feedback network (390Ω + 330Ω = 720Ω).

### 5. Power LED

| From | To |
|------|----|
| Output rail (+) | Other 330Ω resistor |
| 330Ω resistor | LED anode |
| LED cathode | GND rail |

### 6. Output header

Solder the 4 header pins to the output (+) and GND rail pads, sized to
plug directly into a breadboard's power rails on both sides of the center
gap.

---

## Expected behaviour

See [README.md](README.md) § Expected behaviour — ~3.28V or ~5.00V at the
output header depending on switch position, LED lit whenever powered.
