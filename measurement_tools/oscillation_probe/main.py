import machine
import time

# Pico ADC toggle/oscillation detector -- distinguishes a genuinely
# swinging square-wave node from a flat/stuck DC level, which
# raw_voltage_probe's averaged reading can't do on its own: averaging 50
# samples 1ms apart (a 50ms window) collapses anything faster than a few
# Hz into a duty-weighted mid-voltage indistinguishable from a real
# fixed-DC fault. This instead grabs a tight back-to-back burst of raw
# ADC reads (no sleep between them) and reports min/max/swing plus a
# zero-crossing count -- direct evidence of toggling.
#
# NEVER wire this to a node carrying more than 3.3V directly -- GP26
# (like every RP2040 GPIO) tops out at 3.3V. Always probe through a
# resistor divider sized for the source rail; never straight onto a raw
# high-voltage node. If a reading here pins at exactly 3.300V (ADC
# saturation) rather than landing under the expected divided value,
# that's a sign the divider isn't actually dividing (e.g. a missing or
# open-circuit bottom leg) and the pin may be seeing more than 3.3V,
# clipped -- disconnect and check the divider before continuing, don't
# keep probing to "get a cleaner reading."

adc = machine.ADC(26)  # GPIO 26 = ADC0
V_IN = 3.3  # Pico's own 3V3 rail, used only to convert ADC counts to volts
BURST_SAMPLES = 2000  # tight loop, no sleep -- sample as fast as the ADC allows

raw = []
t0 = time.ticks_us()
for _ in range(BURST_SAMPLES):
    raw.append(adc.read_u16())
t1 = time.ticks_us()

elapsed_us = time.ticks_diff(t1, t0)
sample_rate_hz = BURST_SAMPLES / (elapsed_us / 1e6)

v = [(r / 65535.0) * V_IN for r in raw]
vmin, vmax = min(v), max(v)
vavg = sum(v) / len(v)
swing = vmax - vmin

mid = (vmin + vmax) / 2.0
crossings = 0
above = v[0] > mid
for x in v[1:]:
    now_above = x > mid
    if now_above != above:
        crossings += 1
        above = now_above

print(f"Samples: {BURST_SAMPLES} over {elapsed_us} us (~{sample_rate_hz:.0f} sps)")
print(f"GP26 min={vmin:.3f}V max={vmax:.3f}V avg={vavg:.3f}V swing={swing:.3f}V")
print(f"Zero-crossings (about mid={mid:.3f}V): {crossings}")
if crossings >= 2:
    est_hz = (crossings / 2) / (elapsed_us / 1e6)
    print(f"Rough toggle-rate estimate: ~{est_hz:.0f} Hz (crude, aliasing-prone -- not a substitute for a real frequency counter)")
print("Compare swing/crossings against the target documented for your current probe point in the calling circuit's own README.")
