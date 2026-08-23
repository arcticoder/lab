"""
fuse_test_voltmeter/main.py
----------------------------
Pico ADC voltmeter for polyfuse trip testing.

Hardware
--------
  GP26 (ADC0) — probe lead, clipped to the load resistor's fuse-side leg in
                 psu_ultralow_v1 or psu_low_v2 (battery -> fuse -> 10kOhm
                 load -> GND)
  GND         — probe lead, clipped to the load resistor's ground-side leg
  GP25        — onboard LED, lit while the fuse under test reads tripped

What this measures
-------------------
  * Voltage at the probe point, streamed over USB serial to the PC
  * Trip/reset transitions (voltage crossing LOW_VOLTAGE), so a fuse can be
    proven good before it's ever wired in front of an LED — see
    ../docs/history.md (2026-08-15) for why this exists

Run from MicroPico (or rshell / mpremote), Pico connected to the PC by USB:
  mpremote run main.py
"""

from machine import ADC, Pin
import time

# ---------------------------------------------------------------------------
# Hardware configuration
# ---------------------------------------------------------------------------

ADC_PROBE = ADC(Pin(26))          # GP26 / ADC0, across the load resistor
LED       = Pin(25, Pin.OUT)      # onboard LED, mirrors trip state

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ADC_MAX         = 65535   # 16-bit ADC full scale
VREF            = 3.3     # Pico ADC reference voltage
LOW_VOLTAGE     = 0.5     # below this, treat the fuse as tripped (see README)
SAMPLE_INTERVAL_S = 0.2


def raw_to_voltage(raw: int) -> float:
    """Convert 16-bit ADC reading to voltage."""
    return raw * VREF / ADC_MAX


def main() -> None:
    print("fuse_test_voltmeter — probing GP26 vs GND, Ctrl-C to stop")

    tripped = False
    while True:
        v = raw_to_voltage(ADC_PROBE.read_u16())
        now_tripped = v < LOW_VOLTAGE
        if now_tripped != tripped:
            tripped = now_tripped
            print("*** FUSE TRIPPED ***" if tripped else "*** fuse reset ***")
        LED.value(tripped)
        print(f"{v:.3f}V")
        time.sleep(SAMPLE_INTERVAL_S)


if __name__ == "__main__":
    main()
