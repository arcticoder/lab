"""
diagnose_demod.py — lockin_amplifier (MicroPython, Raspberry Pi Pico)

Says which averager is not responding to the signal. It drives the in-phase
and then the anti-phase test signal (the same states as main.py) and prints
how far each averager, A (GP26) and B (GP27), moves between them.

    mpremote mount . run diagnose_demod.py

(the mount lets this script import main.py's register code.) In a working
lock-in the signal gates OUT1 into A during one half-cycle and into B during
the other, so flipping the signal's phase swings both: the swing is large and
opposite in sign (about 130mV each way at the design gain, more if the gain
stage clips). An averager that reads the same in both states is not connected
to a switch.

Seen 2026-10-17: A moved 40mV and B moved 0.1mV between the two states, and B
sat at 1.172V in every state of main.py.
"""

import time
from machine import ADC

import main

MIN_SWING = 0.030  # volts


def run():
    adc_a, adc_b = ADC(main.ADC_A_PIN), ADC(main.ADC_B_PIN)
    main.start()
    seen = {}
    for name, sig in (("in phase", "in"), ("anti phase", "anti")):
        main.set_state(sig, 0, False)
        time.sleep(main.SETTLE_S)
        seen[name] = main.read_ab(adc_a, adc_b)
        print("%-10s A %.3fV  B %.3fV" % (name, seen[name][0], seen[name][1]))
    da = seen["in phase"][0] - seen["anti phase"][0]
    db = seen["in phase"][1] - seen["anti phase"][1]
    for label, d in (("A (S1 path)", da), ("B (S2 path)", db)):
        ok = abs(d) >= MIN_SWING
        print("[%s] %s moves with the signal: %+.1fmV between in phase and anti phase, minimum %.0fmV" % ("PASS" if ok else "FAIL", label, d * 1e3, MIN_SWING * 1e3))
    if da * db > 0:
        print("note: A and B moved the same way; they should move in opposite directions")


try:
    run()
finally:
    main.shutdown()
