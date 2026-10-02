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
| Pico GP15 (physical pin 20) | analyzer header pad `D0` |
| Pico GND (physical pin 18) | analyzer header pad marked GND |

Pad names are read off the board's silkscreen; the board's header map
isn't recorded in this repo yet. If you confirm which pad is `D0` and
which is GND, `docs/kb/` and `parts_reference.md` can carry it for the
next session.

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
[PASS] frequency: 1000.0Hz vs 1000Hz ±1%
[PASS] duty cycle (also catches an inverted channel: 75%): 25.0% vs 25% ±1
```

| Result | Meaning |
|--------|---------|
| `no fx2lafw device found` | Board not attached to WSL, or J4 is in |
| `fewer than two rising edges` | Signal wire not on `D0`, ground not shared, or the Pico script isn't running |
| duty ≈ 75% | Channel reads inverted — unexpected for this board; note which pad it is |
| frequency off by more than 1% | The analyzer's samplerate isn't what `sigrok-cli` was asked for, or the Pico script was changed |
