# Breadboard Wiring — logic_analyzer_check

## Circuit overview

Two wires between the Pico and the CY7C68013A board: the Pico's test
signal into one analyzer channel, and a shared ground. The analyzer takes
its power from its own Mini-USB cable; the Pico from its Micro-USB cable.
Both USB devices need to be attached to WSL for the host script and
`mpremote` to see them.

**Equivalent to:** no netlist — there's no analog circuit to simulate.
`smoke_test.py` covers the analysis instead.

---

## Parts required

| Component | Quantity |
|-----------|----------|
| Raspberry Pi Pico (USB-connected) | 1 |
| CY7C68013A board, jumper J4 removed, Mini-USB cable | 1 |
| Dupont jumper (M-M or M-F as the board's header needs) | 2 |

---

## Wiring steps

| From | To |
|------|----|
| Pico GP15 (physical pin 20) | analyzer header pad `PB0` (J2, row "PB0 / PB1", the outer-left pin) |
| Pico GND (physical pin 18) | analyzer GND pad — J2's left-column `GND` in the bottom row, below `PB2` |

The board's silkscreen has no pad named `D0`. Its data pads are `PB0`–`PB7`
and `PD0`–`PD7`; `sigrok`'s generic profile for this chip calls them
`D0`–`D15`, and the expected mapping is `PB0`–`PB7` → `D0`–`D7`,
`PD0`–`PD7` → `D8`–`D15`. That mapping comes from the sigrok project's
description of this chip family, not from this board, so confirm it on the
first run (next section). Several pads are `VCC`: keep the Pico's wires off
them.

---

## Before the first capture (WSL only): usbipd

On first use, `sigrok-cli` uploads its firmware to the FX2, and the board
disconnects and reconnects to run it. `usbipd` treats the reconnected
board as a new, unshared device and drops it from WSL, so the capture
fails with `Device failed to renumerate` (seen 2026-10-01). A
loose-looking "detach" is this, not the cable.

In an **administrator** PowerShell on Windows:

```powershell
usbipd list                                  # note the BUSID of the 'fx2lafw' / 04b4:8613 board
usbipd bind --busid <BUSID>                  # once the firmware is loaded, the board is listed as "fx2lafw"
usbipd attach --wsl --busid <BUSID> --auto-attach
```

Leave the `--auto-attach` window open; it re-attaches the board whenever it
drops. What worked on 2026-10-02: the first `bind`/`attach` (board listed as
an unnamed device) attached, then dropped the moment sigrok loaded its
firmware; in a second administrator window `usbipd list` showed the same bus id
as `fx2lafw ... Not shared`, and a fresh `bind` + `attach --auto-attach` on it
held for the rest of the session. The firmware stays loaded until the board is unplugged. After an
unplug/replug the first `sigrok-cli` run reloads it and the board drops once
more; if `usbipd list` then shows it as "fx2lafw — Not shared", run the
`bind` line again.

---

## Find which pad is which channel (first run only)

With the Pico running `main.py` and wired to `PB0`:

```bash
python3 check_capture.py --find-channel
```

It prints the channels that toggle. `toggling: D0` confirms the mapping
above. A different channel means the mapping differs on this board;
`check_capture.py --channel <that one>` then works for the rest of the run,
and `docs/parts_reference.md` should get the correction.

---

## Run

Terminal 1, the signal:

```bash
mpremote run main.py
```

Terminal 2, the capture (while terminal 1 is running):

```bash
python3 check_capture.py
```

## Expected behavior

```
captured 25000 samples of D0 at 1000000Hz
[PASS] enough periods captured: 24 full periods
[PASS] frequency: 999.9Hz vs 1000Hz ±1%
[PASS] duty cycle (also catches an inverted channel: 75%): 25.0% vs 25% ±1
```

(That is the output seen on 2026-10-02. `--find-channel` printed `toggling: D0`.
The check also passes at `--samplerate 4000000`, with 100 000 samples.)

| Result | Meaning |
|--------|---------|
| `no fx2lafw device found` | Board not attached to WSL (see usbipd above), or J4 is in |
| `Device failed to renumerate` / `No devices found` after the board was found | usbipd dropped the board after the firmware load; see usbipd above |
| `fewer than two rising edges` | Signal wire not on `PB0`, ground not shared, or the Pico script isn't running |
| duty ≈ 75% | Channel reads inverted — unexpected for this board; note which pad it is |
| frequency off by more than 1% | The analyzer's samplerate isn't what `sigrok-cli` was asked for, or the Pico script was changed |
