import machine
import time

# Raw GP26 voltage reader -- no resistance math, no divider assumptions.
# Whatever external divider or node is wired to GP26/GND at the time, this
# just prints the averaged voltage Pico ADC0 actually sees. Compare the
# printed average against whatever target the calling circuit's own
# README documents for the probe point currently wired -- this script
# doesn't know which circuit or probe point it's being used for, so it
# has no PASS/FAIL of its own to report. See this folder's README.md for
# which circuits reuse it and why it's kept generic rather than folded
# into resistance_measurement/ (known-R_ref math) or fuse_test_voltmeter/
# (trip/reset detection).
#
# NEVER wire this to a node carrying more than 3.3V directly -- GP26
# (like every RP2040 GPIO) tops out at 3.3V. Always probe through a
# resistor divider sized for the source rail; never straight onto a raw
# high-voltage node.

adc = machine.ADC(26)  # GPIO 26 = ADC0
V_IN = 3.3  # Pico's own 3V3 rail, used only to convert ADC counts to volts
SAMPLES_PER_READING = 50
READINGS = 20


def read_voltage(samples=SAMPLES_PER_READING):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.001)
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * V_IN


total = 0.0
for i in range(READINGS):
    v = read_voltage()
    print(f"[{i + 1}/{READINGS}] GP26 raw voltage: {v:.3f} V")
    total += v
    time.sleep(0.2)

print(f"Average over {READINGS} readings: {total / READINGS:.3f} V")
print("Compare against the target documented for your current probe point in the calling circuit's own README.")
