"""
switch_pin_identifier/main.py
-------------------------------
Pico digital probe for identifying which terminal(s) of an unmarked 2- or
3-pin switch are actually connected in each physical position, without a
multimeter.

Hardware
--------
  GND        — wired directly to one of the switch's terminals (the
               reference point)
  GP14, GP15 — probe leads, one per remaining switch terminal (works for
               a 2-pin switch too; just leave GP15 unconnected)

Both probe pins use the Pico's internal pull-up, so no external resistors
are needed: each reads HIGH (1) when its terminal is not connected, by the
switch, to the terminal wired to GND, and LOW (0) when the switch connects
it to that grounded terminal in the current position.

If neither pin ever reads 0 across every position, the terminal wired to
GND isn't in this switch's current-carrying path — move the GND wire to a
different terminal and re-run.

What this measures
-------------------
  Prints A/B pin states continuously. Slide/press the switch through
  each of its positions and watch which pin(s) toggle — see README.md for
  how to read the result.

Run from MicroPico (or rshell / mpremote), Pico connected to the PC by USB:
  mpremote run main.py
"""

from machine import Pin
import time

PIN_A = Pin(14, Pin.IN, Pin.PULL_UP)
PIN_B = Pin(15, Pin.IN, Pin.PULL_UP)

SAMPLE_INTERVAL_S = 0.3


def main() -> None:
    print("switch_pin_identifier — probing GP14(A)/GP15(B) vs GND, Ctrl-C to stop")
    print("Slide/press the switch through each position; a 0 means that pin is")
    print("connected to GND in the current position, a 1 means it's floating (pulled high).")

    last = None
    while True:
        state = (PIN_A.value(), PIN_B.value())
        if state != last:
            last = state
            print(f"A:{state[0]} B:{state[1]}")
        time.sleep(SAMPLE_INTERVAL_S)


if __name__ == "__main__":
    main()
