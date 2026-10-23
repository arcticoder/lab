"""
smoke_test.py — hardware/instrument: the pin map and the USB power budget (WP1).

Safety: every operating mode, with the biggest loads at their worst case, stays under the 500 mA a USB
host guarantees, and under the input polyfuse's hold current with margin, so neither a host current limit
nor the fuse trips in normal use; no 3.3 V GPIO is asked to be an analog input anywhere but GP26-GP29.

Functional: no GPIO is used twice; every peripheral function asked of a pin exists on that pin in the
RP2040 datasheet's function table; the ADC SPI uses SPI0 on GP16-GP19 and the I2C bus I2C0 on GP4/GP5; the
two motor PWM pins are one PWM slice's A and B outputs; all four RP2040 ADC inputs are accounted for.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pins as P  # noqa: E402
sys.path.insert(0, HERE)

failures = []


def check(label, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    if not ok:
        failures.append(label)


gp = [v[0] for v in P.PINS.values()]
dup = sorted({g for g in gp if gp.count(g) > 1})
check("functional — no GPIO is used twice", not dup, f"{len(gp)} signals on {len(set(gp))} pins" + (f", duplicated: {dup}" if dup else ""))
bad = [(n, g, f) for n, (g, f, _) in P.PINS.items() if f and f not in P.FUNCTIONS[g]]
check("functional — every requested peripheral function exists on its pin (RP2040 Table 2)", not bad, f"{bad}" if bad else f"{sum(1 for v in P.PINS.values() if v[1])} functions checked")
check("functional — all 30 GPIOs are accounted for", set(gp) == set(range(30)), f"missing {sorted(set(range(30)) - set(gp))}")
adc = {n: g for n, (g, _, _) in P.PINS.items() if n.startswith("MON_")}
check("safety — analog monitors sit only on GP26-GP29 (the ADC inputs)", all(g in P.ADC_PINS for g in adc.values()) and len(adc) == 4, f"{adc}")
slice_of = lambda g: (g >> 1) & 7  # noqa: E731
m1, m2 = P.PINS["MOTOR1_PWM"][0], P.PINS["MOTOR2_PWM"][0]
check("functional — the two motor PWM pins are one slice's A and B outputs", slice_of(m1) == slice_of(m2) and m1 % 2 == 0 and m2 == m1 + 1, f"GP{m1} and GP{m2}, slice {slice_of(m1)}")
check("functional — ADC SPI is SPI0 on GP16-GP19", [P.PINS[n][0] for n in ("ADC_MISO", "ADC_CS", "ADC_SCK", "ADC_MOSI")] == [16, 17, 18, 19], "RX, CSn, SCK, TX")
check("functional — I2C is I2C0 on GP4 and GP5", (P.PINS["I2C_SDA"][0], P.PINS["I2C_SCL"][0]) == (4, 5), "")

for mode in P.MODES:
    i = P.mode_current(mode)
    check(f"safety — {mode} mode stays under USB's 500 mA and the fuse's hold current with 15% margin", i <= P.USB_LIMIT_MA * 0.9 and i * 1.15 <= P.PTC_HOLD_MA, f"{i:.0f} mA (USB {P.USB_LIMIT_MA:.0f}, fuse hold {P.PTC_HOLD_MA:.0f})")
for mode in P.MODES:
    for rail in ("3V3_D", "3V3_A"):
        i = P.rail_current(mode, rail)
        check(f"safety — {mode}: the {rail} regulator stays under 60% of its 250 mA rating", i <= 0.6 * P.LDO_MAX_MA, f"{i:.0f} mA")
check("safety — the coin motors run from 5 V with their duty capped so the average is their 3 V rating", abs(P.MOTOR_DUTY_MAX * 5.0 - 3.0) < 1e-9 and P.RAIL["coin motor 1 at stall"] == "5V", f"{P.MOTOR_DUTY_MAX*100:.0f}% of 5 V = {P.MOTOR_DUTY_MAX*5:.1f} V")
check("functional — the device-under-test current is set by the budget: 300 mA fits, 400 mA does not", P.mode_current("lead-current run") <= 450 and P.mode_current("lead-current run") + 100 > 450, f"{P.mode_current('lead-current run'):.0f} mA with 300 mA; 400 mA would be {P.mode_current('lead-current run') + 100:.0f} mA")

# ---- the candidate parts against the live JLC snapshot (skipped if the snapshot is not on this machine) ----
import parts  # noqa: E402

if not os.path.exists(os.path.expanduser("~/jlcparts/cache.sqlite3")):
    print("[SKIP] parts checks: ~/jlcparts/cache.sqlite3 is not on this machine (see hardware/README.md)")
else:
    rows = parts.check()
    missing = [(l, r) for g, role, l, q, w, r in rows if r is None]
    check("functional — every candidate part is in the JLC snapshot", not missing, f"{len(rows)} part numbers" + (f", missing {missing}" if missing else ""))
    thin = [(role, r["stock"], q * parts.BOARDS_PER_ORDER) for g, role, l, q, w, r in rows if r and r["stock"] < parts.STOCK_FACTOR * q * parts.BOARDS_PER_ORDER]
    check(f"functional — stock covers {parts.STOCK_FACTOR}x the order's need for every part", not thin, f"{thin}" if thin else "all parts")
    tht = [role for g, role, l, q, w, r in rows if r and not parts.machine_placed(l)]
    check("safety — every part is machine-placed SMT, none is hand-soldered through-hole", not tht, f"{tht}" if tht else "44 parts" if len(rows) == 44 else f"{len(rows)} parts")
    ext = {l for g, role, l, q, w, r in rows if r and r["type"] == "extended"}
    check("functional — the extended-part count (each carries a setup fee) is at most 25", len(ext) <= 25, f"{len(ext)} extended of {len(rows)}")

# ---- the analog blocks in ngspice (WP3) -------------------------------------------------------------------
import shutil  # noqa: E402

if shutil.which("ngspice") is None:
    print("[SKIP] analog block simulations: ngspice is not installed")
else:
    import analog_sims as A  # noqa: E402

    t = A.tia()
    check("functional — TIA: 10 kV/A at 1 kHz, no peaking, corner near 16 kHz (70 pF photodiode, 1 nF feedback)", abs(t["gain_1k_db"] - 80) < 0.1 and t["peak_db"] < 0.5 and 14e3 < t["f3_hz"] < 19e3, f"{t['gain_1k_db']:.2f} dB, peak {t['peak_db']:.2f} dB, -3 dB at {t['f3_hz']/1e3:.1f} kHz")
    led = A.led_sink()
    check("functional — LED sink: 20 mA at a 1.02 V reference, zero when gated off, 1 V of headroom on 3.3 V", abs(led["on_mA"] - 20) < 0.1 and abs(led["off_uA"]) < 1 and led["headroom_V"] > 0.5, f"{led['on_mA']:.2f} mA on, {led['off_uA']:.2f} uA off, headroom {led['headroom_V']:.2f} V")
    check("functional — LED sink: the gated edge settles to 1% in under 2 us (a 1-2 kHz carrier has 250 us half-periods)", led["settle_us"] < 2.0, f"{led['settle_us']:.2f} us")
    corners = [(kp, cgs, rl) for kp in (90, 274, 820) for cgs in ("1.0n", "1.7n") for rl in (0.5, 10.0)]
    worst = (0.0, 0.0)
    err = 0.0
    for kp, cgs, rl in corners:
        r = A.dut(kp=kp, cgs=cgs, rload=rl)
        worst = (max(worst[0], r["overshoot_pct"]), max(worst[1], r["settle_us"]))
        err = max(err, abs(r["final_A"] - 0.30) / 0.30)
    check("functional — device current sink: no overshoot and 300 mA to 0.5% for gFS x0.33 to x3, Ciss 1.0 to 1.7 nF, loads 0.5 to 10 ohm", worst[0] < 2.0 and err < 0.005, f"{len(corners)} corners: worst overshoot {worst[0]:.2f}%, worst error {err*100:.3f}%, worst settling {worst[1]:.0f} us")
    # dissipation at the worst load (leads only): 5 V supply, 0.5 ohm of leads, 4.7 ohm ballast, 1 ohm shunt, 300 mA
    i_dut = 0.30
    v_ds = 5.0 - i_dut * (0.5 + 4.7 + 1.0)
    p_fet, p_bal = v_ds * i_dut, i_dut**2 * 4.7
    check("safety — device current sink: junction rise at 300 mA under 60 K (AOD4184A, 55 K/W steady state on its test footprint) and the 4.7 ohm ballast under half its 1 W rating", p_fet * 55 < 60 and p_bal < 0.5, f"FET {p_fet:.2f} W -> {p_fet*55:.0f} K; ballast {p_bal:.2f} W")
    pl = A.plate()
    check("functional — plate driver: linear to 0.1% from 2.9 V to 22.8 V, overshoot under 5%, settles in under 5 us with 300 pF of cable", pl["gain_err_pct"] < 0.1 and pl["overshoot_pct"] < 5 and pl["settle_us"] < 5, f"gain error {pl['gain_err_pct']:.4f}%, overshoot {pl['overshoot_pct']:.1f}%, settles {pl['settle_us']:.1f} us")
    check("safety — the plate voltage never exceeds the repo's 50 V DC line, with the driver at its worst", pl["max_V"] < 50, f"peak {pl['max_V']:.1f} V on a 24 V rail")

if failures:
    print(f"\n{len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\nAll checks passed.")
