"""
main.py — accelerometer_interface

Bring-up check for the GY-521 (MPU-6050) on I2C0: finds the module,
reads WHO_AM_I, wakes it, sets the +/-2g range, then samples the
accelerometer for about a second and prints a PASS/FAIL verdict and
exits (same convention as the other validation scripts here).

With the module lying still, the reading is gravity: the total should be
1g and one axis should carry nearly all of it. The script also prints the
vibration RMS over the sampling window (what remains after the mean is
removed), which is the figure `VIBISO` will compare between a platform
and the bare bench.

Wire SDA to GP4, SCL to GP5, VCC to 3V3(OUT), GND to GND — see
breadboard.md. Run with the Pico plugged in over USB:

    mpremote run main.py
"""

import machine
import math
import struct
import time

SDA_PIN = 4
SCL_PIN = 5
I2C_FREQ = 100_000  # standard mode; smoke_test.py confirms the bus meets it for pull-ups
# up to 10k with up to 100pF of wiring. 400_000 also meets timing at the design point.

PWR_MGMT_1 = 0x6B
CONFIG = 0x1A
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
WHO_AM_I = 0x75

LSB_PER_G = 16384.0  # +/-2g range
N_SAMPLES = 400
GRAVITY_TOLERANCE_G = 0.10  # datasheet sensitivity tolerance is +/-3%, zero-g offset +/-50mg/axis
MAX_NOISE_G = 0.03  # per-axis std at rest; datasheet noise floor is ~7mg RMS at this bandwidth

# 0x68 is a real MPU-6050. The listing variant for this board is "Compatible",
# so 0x70-0x72 (MPU-6500/9250-family IDs some clones report) are accepted
# with a note — their accelerometer registers are laid out the same way.
GENUINE_ID = 0x68
CLONE_IDS = (0x70, 0x71, 0x72)

i2c = machine.I2C(0, sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=I2C_FREQ)

failures = []


def check(label, condition, detail):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}: {detail}")
    if not condition:
        failures.append(label)


def finish():
    if failures:
        print(f"\n{len(failures)} check(s) failed: {failures}")
    else:
        print("\nAll checks passed.")


found = i2c.scan()
addr = next((a for a in found if a in (0x68, 0x69)), None)
check(
    "module answers on I2C0",
    addr is not None,
    f"scan found {[hex(a) for a in found]}"
    + ("" if addr is not None else " — no 0x68/0x69: check SDA/SCL/VCC/GND, and that the pins aren't swapped"),
)
if addr is None:
    finish()
    raise SystemExit

who = i2c.readfrom_mem(addr, WHO_AM_I, 1)[0]
check(
    "WHO_AM_I",
    who == GENUINE_ID or who in CLONE_IDS,
    f"0x{who:02X}"
    + (" (MPU-6050)" if who == GENUINE_ID else " (clone/compatible ID — accel registers are the same)" if who in CLONE_IDS else " — unrecognized chip"),
)

i2c.writeto_mem(addr, PWR_MGMT_1, b"\x00")  # clear SLEEP (the chip powers up asleep)
time.sleep_ms(100)
i2c.writeto_mem(addr, CONFIG, b"\x00")  # DLPF off: 260Hz accelerometer bandwidth
i2c.writeto_mem(addr, ACCEL_CONFIG, b"\x00")  # +/-2g

xs, ys, zs = [], [], []
t0 = time.ticks_us()
for _ in range(N_SAMPLES):
    raw = i2c.readfrom_mem(addr, ACCEL_XOUT_H, 6)
    x, y, z = struct.unpack(">hhh", raw)
    xs.append(x / LSB_PER_G)
    ys.append(y / LSB_PER_G)
    zs.append(z / LSB_PER_G)
elapsed_s = time.ticks_diff(time.ticks_us(), t0) / 1e6


def mean(v):
    return sum(v) / len(v)


def std(v):
    m = mean(v)
    return math.sqrt(sum((a - m) ** 2 for a in v) / len(v))


mx, my, mz = mean(xs), mean(ys), mean(zs)
total_g = math.sqrt(mx * mx + my * my + mz * mz)
worst_std = max(std(xs), std(ys), std(zs))
vib_rms_g = math.sqrt(sum(std(v) ** 2 for v in (xs, ys, zs)))

print(f"mean (g): x={mx:+.3f} y={my:+.3f} z={mz:+.3f}   sample rate {N_SAMPLES/elapsed_s:.0f} Hz")
check(
    "gravity magnitude at rest",
    abs(total_g - 1.0) < GRAVITY_TOLERANCE_G,
    f"|a| = {total_g:.3f}g (expect 1.00g +/-{GRAVITY_TOLERANCE_G}) — hold the module still",
)
check(
    "noise at rest",
    worst_std < MAX_NOISE_G,
    f"worst per-axis std {worst_std*1000:.1f}mg (limit {MAX_NOISE_G*1000:.0f}mg)",
)
print(f"vibration RMS over this window: {vib_rms_g*1000:.1f} mg")
finish()
