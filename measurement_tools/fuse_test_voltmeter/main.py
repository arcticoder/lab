"""
fuse_test_voltmeter/main.py
----------------------------
Pico ADC voltmeter for polyfuse trip testing.

Hardware
--------
  GP26 (ADC0) — probe lead, clipped to the load resistor's fuse-side leg in
                 psu_ultralow_v1 or psu_low_v2 (battery -> fuse -> 10 Ohm
                 load -> GND)
  GND         — probe lead, clipped to the load resistor's ground-side leg
  GP25        — onboard LED, lit while the fuse under test reads tripped
  GP15        — arm switch common (SPDT slide switch), internal pull-down
                 enabled: one throw wired to 3V3 (OUT), the other throw left
                 unconnected. HIGH (3V3 throw) = ARMED, LOW (pulled down,
                 unconnected throw) = DISARMED. Only one throw is ever wired
                 to a rail, so the switch can never bridge 3V3 to GND.

What this measures
-------------------
  * Voltage at the probe point, streamed over USB serial to the PC
  * Trip/reset transitions (voltage crossing LOW_VOLTAGE) while ARMED, so a
    fuse can be proven good before it's ever wired in front of an LED

Arm switch
----------
  Flip to DISARMED before connecting or disconnecting the battery, then to
  ARMED once it's settled and you're actually watching for a trip. This
  keeps the expected zero-volt reading while the battery is out of the
  circuit from being reported as a false trip. Voltage still streams either
  way; only the trip/reset detection and LED are gated on ARMED.

Run from MicroPico (or rshell / mpremote), Pico connected to the PC by USB:
  mpremote run main.py
"""

from machine import ADC, Pin
import time

# ---------------------------------------------------------------------------
# Hardware configuration
# ---------------------------------------------------------------------------

ADC_PROBE  = ADC(Pin(26))          # GP26 / ADC0, across the load resistor
LED        = Pin(25, Pin.OUT)      # onboard LED, mirrors trip state
ARM_SWITCH = Pin(15, Pin.IN, Pin.PULL_DOWN)  # SPDT common: HIGH (3V3 throw)
                                    # = armed, LOW (unconnected throw, pulled
                                    # down) = disarmed

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
    print("GP15 arm switch: DISARMED while touching the battery, ARMED "
          "while watching for a trip")

    tripped = False
    armed = None
    while True:
        now_armed = bool(ARM_SWITCH.value())
        if now_armed != armed:
            armed = now_armed
            tripped = False
            LED.value(False)
            print("-- ARMED --" if armed else "-- DISARMED --")

        v = raw_to_voltage(ADC_PROBE.read_u16())
        if armed:
            now_tripped = v < LOW_VOLTAGE
            if now_tripped != tripped:
                tripped = now_tripped
                print("*** FUSE TRIPPED ***" if tripped else "*** fuse reset ***")
            LED.value(tripped)
        print(f"{v:.3f}V")
        time.sleep(SAMPLE_INTERVAL_S)


if __name__ == "__main__":
    main()
