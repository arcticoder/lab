"""
main.py — thermal_monitor

Reads the Rref/Rntc divider (GP26), inverts the divider equation to get
the thermistor's resistance, converts that to a temperature via the
MF52AT's beta equation, and drives an alarm LED (GP15) when the
temperature crosses ALARM_THRESHOLD_C. No PASS/FAIL verdict to print and
exit on — this streams continuously, same reasoning as
raw_voltage_probe/main.py.

Wire GP26 to the Rref/Rntc divider midpoint and GP15 (through the 220ohm
resistor) to the alarm LED's anode — see breadboard.md — then run with
the Pico plugged in over USB:

    mpremote run main.py

Warm the thermistor (finger pinch, or hold a soldering iron NEAR, not
touching, it) to see the reported temperature rise and the alarm LED
light once it crosses the threshold.
"""

import machine
import time
import math

adc = machine.ADC(26)  # GPIO 26 = ADC0, wired to the Rref/Rntc divider midpoint
alarm_led = machine.Pin(15, machine.Pin.OUT)

VREF = 3.3
RREF = 10_000  # ohms
R25 = 10_000  # ohms, MF52AT nominal resistance at 25C
BETA = 3950  # K, MF52AT B(25/50) per docs/parts_reference.md
T25_K = 298.15  # 25C in kelvin
ALARM_THRESHOLD_C = 40.0


def read_voltage(samples=20):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.001)
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * VREF


def resistance_from_voltage(v_mid):
    # Rref (VCC->MID) in series with Rntc (MID->GND): v_mid = VCC * Rntc/(Rref+Rntc)
    return RREF * v_mid / (VREF - v_mid)


def temperature_c_from_resistance(r_ntc):
    # Beta equation: 1/T = 1/T25 + (1/B)*ln(R/R25)
    inv_t = 1 / T25_K + (1 / BETA) * math.log(r_ntc / R25)
    return (1 / inv_t) - 273.15


while True:
    v = read_voltage()
    r_ntc = resistance_from_voltage(v)
    temp_c = temperature_c_from_resistance(r_ntc)
    alarm = temp_c >= ALARM_THRESHOLD_C
    alarm_led.value(1 if alarm else 0)
    print(f"THERM: {v:.3f}V, {r_ntc:.0f}ohm, {temp_c:.1f}C  {'ALARM' if alarm else ''}")
    time.sleep(0.5)
