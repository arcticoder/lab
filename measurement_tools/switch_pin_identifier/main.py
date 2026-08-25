"""
switch_pin_identifier/main.py
-------------------------------
Pico digital probe for identifying which pin(s) of an unmarked 2- or
3-pin switch are actually connected in each physical position, without a
multimeter. Generalizes the ad hoc diagnostic from
../../docs/history.md (2026-08-22 21:41 onward), which worked out that one
of the pico/ repo's slide switches is a 3-pin "1P2T" part with one floating
outer pin — see pico/docs/inventory.md's "Slide Switch" row.

Hardware
--------
  GP14, GP15, GP16 — probe leads, one per switch terminal (works for a
                      2-pin switch too; just leave GP16 unconnected)
  GND               — probe lead, shared reference

All three pins use the Pico's internal pull-up, so no external resistors
are needed: each pin reads HIGH (1) when its terminal is not connected to
GND, and LOW (0) when the switch connects it to GND in the current
position.

What this measures
-------------------
  Prints A/B/C pin states continuously. Slide/press the switch through
  each of its positions and watch which pin(s) toggle — see README.md for
  how to read the result.

Run from MicroPico (or rshell / mpremote), Pico connected to the PC by USB:
  mpremote run main.py
"""

from machine import Pin
import time

PIN_A = Pin(14, Pin.IN, Pin.PULL_UP)
PIN_B = Pin(15, Pin.IN, Pin.PULL_UP)
PIN_C = Pin(16, Pin.IN, Pin.PULL_UP)

SAMPLE_INTERVAL_S = 0.3


def main() -> None:
    print("switch_pin_identifier — probing GP14(A)/GP15(B)/GP16(C) vs GND, Ctrl-C to stop")
    print("Slide/press the switch through each position; a 0 means that pin is")
    print("connected to GND in the current position, a 1 means it's floating (pulled high).")

    last = None
    while True:
        state = (PIN_A.value(), PIN_B.value(), PIN_C.value())
        if state != last:
            last = state
            print(f"A:{state[0]} B:{state[1]} C:{state[2]}")
        time.sleep(SAMPLE_INTERVAL_S)


if __name__ == "__main__":
    main()
