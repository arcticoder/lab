# logic_analyzer_check

First real capture on the CY7C68013A logic analyzer (`SCOPELA`): the Pico
drives a known 1kHz, 25%-duty square wave on GP15, the analyzer samples it
through `sigrok-cli` (`fx2lafw` driver), and a host script checks the
measured frequency and duty cycle against what the Pico was told to
output.

`sigrok-cli --driver fx2lafw --scan` already finds the board (2026-10-01),
which proves the firmware upload over USB works. It doesn't prove that a
signal on a header pin ends up in a capture, that the channel numbering
matches the silkscreen, or that the sample clock is right. This does, with
no circuit to build and no parts beyond what is on hand.

The 25% duty is chosen on purpose: an inverted channel reads 75%, and a
line stuck at a mid level or floating shows no edges at all, so each
failure mode produces a different message.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython — 1kHz / 25% PWM on GP15 |
| `check_capture.py` | Host side — runs `sigrok-cli`, measures frequency/duty from full periods, prints PASS/FAIL |
| `smoke_test.py` | Host side — analysis unit checks (ideal wave, wrong frequency, inverted, stuck, too short), the Pico script against a mocked `machine`, the csv parser against real `sigrok-cli` demo output, and a live capture when the board is plugged in (SKIP otherwise) |
| `breadboard.md` | The two wires and the run steps |

---

## Run

See [breadboard.md](breadboard.md). In short: GP15 → `D0`, a Pico GND →
the analyzer's GND, `mpremote run main.py` in one terminal,
`python3 check_capture.py` in another.

## Tolerances

| Check | Limit | Why |
|-------|-------|-----|
| Frequency | ±1% of 1000Hz | Pico PWM and the analyzer's sample clock both run from crystals (tens of ppm); 1% leaves room for a misconfigured samplerate to be caught |
| Duty | ±1 percentage point of 25% | One sample is 0.1% of a period at 1MHz sampling |
| Periods | ≥ 15 full periods | The capture requests 25; fewer means the capture was cut short |

Frequency and duty are measured from rising edge to rising edge, so the
partial periods at the ends of the capture don't bias them.

## What a pass does and doesn't show

A pass shows that `D0` samples correctly at 1MHz and that a 3.3V logic
signal from the Pico reads as clean 0/1. It says nothing about `D1`–`D15`
(rerun with `--channel D1` after moving the wire to check another), the
analyzer's higher sample rates, or its behavior with faster signals.
Higher rates over USB 2.0 with many channels enabled are where cheap
FX2 boards start dropping samples; that isn't tested here.
