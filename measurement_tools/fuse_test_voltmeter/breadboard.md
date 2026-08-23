# Breadboard Wiring — fuse_test_voltmeter

## Circuit overview

No new power circuit — this probes whichever PSU circuit you build first
([psu_ultralow_v1](../power_supplies/psu_ultralow_v1/) or
[psu_low_v2](../power_supplies/psu_low_v2/)) with a Raspberry Pi Pico ADC
input. Neither this circuit nor its prerequisite PSU has been built yet;
build the PSU first, per its own `breadboard.md`, then come back here. The
Pico is powered by the PC's USB port, independent of the circuit under
test.

**Equivalent to:** `fuse_test_voltmeter.spice`

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| Raspberry Pi Pico | RP2040 | 1 |
| Micro USB cable | data-capable, to PC | 1 |
| Dupont M-F jumper | 22cm | 2 |
| psu_ultralow_v1 or psu_low_v2 | build and wire first | 1 |
| Test load resistor | 10 Ω | 1 (part of the PSU breadboard build) |

No new parts beyond what's already in the psu_ultralow_v1 / psu_low_v2
parts lists — see [docs/history.md](../docs/history.md) (2026-08-15 10:41)
for why 10 Ω is reused for both fuse ratings instead of ordering a
dedicated value.

---

## Wiring steps

### 1. Plug the Pico into the PC

Micro USB cable, Pico to PC. This powers the Pico and gives you the serial
connection `main.py` prints to — no separate power source for the Pico.

### 2. Probe the test load

The fuse under test needs to be wired first on its own breadboard, per
[psu_ultralow_v1/breadboard.md](../power_supplies/psu_ultralow_v1/breadboard.md)
or
[psu_low_v2/breadboard.md](../power_supplies/psu_low_v2/breadboard.md):
`battery → fuse → 10 Ω load resistor → ground`.

| From | To | Wire |
|------|----|------|
| Pico GP26 | Load resistor's fuse-side leg (the node between the fuse and the resistor) | Dupont M-F, female end on breadboard |
| Pico GND | Load resistor's ground-side leg | Dupont M-F, female end on breadboard |

Either use a spare GND pin on the Pico's header, or share the PSU circuit's
own ground rail — both are the same reference as long as the Pico and the
PSU-under-test share a common ground point.

### 3. Run `main.py`

Load `main.py` onto the Pico (Thonny, `mpremote run main.py`, or copy it on
as `main.py` to autorun). Open the serial monitor on the PC to watch
voltage readings stream in.

---

## Expected behavior

**v1 (psu_ultralow_v1, 1.5V, 50 mA fuse):** steady ~1.43V at the probe point
under normal 10 Ω load. Short the load resistor to force ~150 mA (3x trip
threshold) — voltage collapses to ~0.14V within about a second as the fuse
trips, and `main.py` prints `*** FUSE TRIPPED ***` and lights the Pico's
onboard LED. Remove the short and wait ~2 minutes for the polyfuse to cool
and reset; voltage should climb back to ~1.43V and the onboard LED turns
off.

**v2 (psu_low_v2, 3.0V, 500 mA fuse):** same test, ~2.86V normal, ~0.27V
tripped, forcing current sits right at the 500 mA threshold rather than 3x
over it, so the trip may take longer.

If the fuse doesn't reset after cooling, or the tripped-state voltage
doesn't drop the way the SPICE numbers predict, don't trust it near an LED —
see [README.md](README.md) for the full test procedure.
