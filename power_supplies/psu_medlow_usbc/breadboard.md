# Breadboard Wiring — psu_medlow_usbc

**Before wiring: this build is unverified.** The USB-C breakout board below
is passive (traces only, no PD controller IC) — a USB-C source only drives
VBUS once it sees CC1/CC2 sink termination, which this specific board may
or may not have (see `README.md` Status and `docs/parts_reference.md` §
USB-C 16-pin test breakout board). Check for VBUS with a meter after step 1
before proceeding — if it's absent, this board needs CC1/CC2 pull-down
resistors (5.1kΩ) added, or a dedicated PD sink controller IC (e.g.
STUSB4500, CH224, TPS65987D) plus a downstream buck converter if targeting
a voltage other than what gets negotiated.

## Circuit overview

USB-C VBUS (5V, adapter-regulated, *if the sink termination is present* —
see warning above) → 500 mA polyfuse → 100 nF bypass cap → output.

**Equivalent to:** `psu_medlow_usbc.spice` (models only the downstream
fuse+bypass stage — does not model CC/PD negotiation)

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| USB-C breadboard breakout board | passive VBUS/GND breakout | 1 |
| USB-C wall adapter | 5V, 2–3A | 1 |
| Polyfuse | Littelfuse RXEF050 (500 mA slow-blow) | 1 |
| Ceramic capacitor | 100nF | 1 |
| Dupont M-M jumper (red) | 16–20cm | 1 |
| Dupont M-M jumper (black) | 16–20cm | 1 |
| SYB170 breadboard | 170-pin, 300V, <5A | 1 |

---

## Wiring steps

### 1. Seat the USB-C breakout

Plug the breakout board into the breadboard so VBUS and GND land on
separate rows. Plug in the wall adapter and check VBUS with a meter before
continuing — if it reads ~0V, the source is withholding power pending sink
termination it isn't seeing (see warning above).

### 2. Place the polyfuse

Insert the polyfuse in series on the VBUS row, downstream of the breakout.

### 3. Place the bypass cap

| From | To |
|------|----|
| Polyfuse output | 100nF cap (+) |
| 100nF cap (−) | Ground rail |

### 4. Take the output

Output (+) is the polyfuse output / cap (+) node. Output (−) is the ground
rail, tied to USB GND.

---

## Expected behavior

With a 10 Ω test load across the output: ~4.76 V, ~476 mA — near the
polyfuse's 500 mA rating by design. See [README.md](README.md) for the full
simulate workflow.
