"""
main.py — adc_ads1115 (MicroPython, Raspberry Pi Pico)

Bring-up check for an ADS1115 16-bit ADC module on I2C0 (SDA=GP4, SCL=GP5,
address 0x48 with ADDR tied to GND). A 10k/10k divider from 3V3 gives about
1.65V; the Pico's own ADC (GP26) reads that midpoint directly, and the
ADS1115 reads it through the 10k + 100nF + clamp-diode input network. The
two readings must agree, and the ADS1115's reading must be steady to well
under a millivolt.

    mpremote run main.py

Prints one [PASS]/[FAIL] line per check. The ADS1115 config word, LSB sizes
and register map follow the datasheet as recalled; the smoke test pins the
config word and LSB table, so a typo here is caught.
"""

import time

ADDR = 0x48
REG_CONV = 0x00
REG_CONFIG = 0x01
PGA_FSR = {0: 6.144, 1: 4.096, 2: 2.048, 3: 1.024, 4: 0.512, 5: 0.256}
DR_SPS = {0: 8, 1: 16, 2: 32, 3: 64, 4: 128, 5: 250, 6: 475, 7: 860}

EXPECTED_V = 1.65
EXPECTED_TOL = 0.10  # two 10k parts of unknown tolerance set the divider
AGREE_V = 0.030  # Pico ADC offset/gain error is tens of mV at worst
ADS_STD_MAX_V = 0.001
N = 64


def config_word(channel, pga=1, dr=4):
    """Single-shot, single-ended read of AIN<channel>, comparator disabled."""
    return 0x8000 | ((0x4 + channel) << 12) | (pga << 9) | 0x0100 | (dr << 5) | 0x0003


def counts_to_volts(counts, pga=1):
    if counts & 0x8000:
        counts -= 0x10000
    return counts * PGA_FSR[pga] / 32768


def lsb_volts(pga=1):
    return PGA_FSR[pga] / 32768


def read_volts(i2c, channel=0, pga=1, dr=4):
    i2c.writeto_mem(ADDR, REG_CONFIG, config_word(channel, pga, dr).to_bytes(2, "big"))
    for _ in range(50):
        time.sleep(0.001)
        cfg = i2c.readfrom_mem(ADDR, REG_CONFIG, 2)
        if cfg[0] & 0x80:  # OS bit set: conversion finished
            break
    else:
        raise OSError("ADS1115 conversion never finished")
    raw = i2c.readfrom_mem(ADDR, REG_CONV, 2)
    return counts_to_volts((raw[0] << 8) | raw[1], pga)


def mean_std(xs):
    m = sum(xs) / len(xs)
    return m, (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5


def evaluate(ads, pico):
    """Checks on two lists of volts; returns [(label, ok, detail)]."""
    am, asd = mean_std(ads)
    pm, psd = mean_std(pico)
    return [
        (
            "ADS1115 reads the divider midpoint",
            abs(am - EXPECTED_V) <= EXPECTED_TOL * EXPECTED_V,
            f"{am:.4f}V vs {EXPECTED_V}V ±{EXPECTED_TOL*100:.0f}%",
        ),
        (
            "ADS1115 and Pico ADC agree",
            abs(am - pm) <= AGREE_V,
            f"ADS {am:.4f}V, Pico {pm:.4f}V, difference {abs(am-pm)*1e3:.1f}mV (limit {AGREE_V*1e3:.0f}mV)",
        ),
        (
            "ADS1115 reading is steady",
            asd <= ADS_STD_MAX_V,
            f"std {asd*1e6:.0f}µV (Pico ADC: {psd*1e6:.0f}µV); one ADS LSB is {lsb_volts()*1e6:.0f}µV, one Pico LSB is 806µV",
        ),
    ]


def main():
    from machine import ADC, I2C, Pin

    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
    found = i2c.scan()
    ok = ADDR in found
    print(f"[{'PASS' if ok else 'FAIL'}] ADS1115 answers at 0x48: scan found {[hex(a) for a in found]}")
    if not ok:
        print("  check SDA/SCL, VDD, GND, ADDR->GND; if the scan is empty add 5.1k pull-ups from SDA and SCL to 3V3")
        return 1
    adc = ADC(26)
    ads, pico = [], []
    for _ in range(N):
        ads.append(read_volts(i2c))
        pico.append(sum(adc.read_u16() for _ in range(16)) / 16 / 65535 * 3.3)
    all_ok = True
    for label, passed, detail in evaluate(ads, pico):
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        all_ok = all_ok and passed
    return 0 if all_ok else 1


if __name__ == "__main__":
    main()
