"""
parts.py — candidate parts for the instrument board (WP2).

    python hardware/instrument/parts.py            # check the table against the JLC snapshot, print it
    python hardware/instrument/parts.py --write    # also rewrite parts.md

Every part is a machine-placed SMT part in JLCPCB's library (the fab places them; nothing is mailed in).
Quantities are per main board and are estimates until the schematic (WP4) fixes them; the passive
families (resistors and capacitors) list the values the draft uses with an estimated count.
Stock and prices are read live from the jlcparts snapshot (~/jlcparts/cache.sqlite3).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import jlc_query  # noqa: E402

# (group, role, lcsc number, quantity per main board, why this part)
BOM = [
    ("core", "RP2040 microcontroller", 2040, 1, "keeps every RP2040 register address the repo's code uses; PIO + DMA for the LED modulation and ADC readout"),
    ("core", "QSPI flash, 16 Mbit", 131025, 1, "W25Q16JV, the flash on the Pico itself, so MicroPython and the repo's firmware boot unchanged"),
    ("core", "12 MHz crystal (RP2040)", 9002, 1, "basic part"),
    ("core", "USB-C receptacle, 16-pin", 165948, 1, "power and data"),
    ("core", "USB ESD protection", 7519, 1, "USBLC6-2SC6 on D+/D-/VBUS"),
    ("core", "input polyfuse, 0.75 A hold", 20987, 1, "SMD1206P075TF; the USB budget peaks near 390 mA (pins.py)"),
    ("core", "tactile switch (BOOTSEL, RESET)", 318884, 2, "basic part"),
    ("power", "3.3 V LDO, 250 mA, 6.5 uVrms noise (analog and digital rails)", 80670, 2, "LP5907-3.3, one part number for both rails: the analog rail (ADC AVDD, op-amps, optical heads, 82 dB PSRR at 1 kHz) and the digital rail (RP2040, sensors, logic); the digital load stays under 100 mA (pins.py)"),
    ("power", "ferrite bead, 600 ohm at 100 MHz", 1002, 3, "analog/digital rail split and supply entry; basic part"),
    ("power", "boost converter (to 24 V)", 84817, 1, "MT3608, 2 V to 24 V adjustable, for the plate driver"),
    ("power", "boost inductor, 22 uH", 128694, 1, "SMMS0630-220M, 2.6 A"),
    ("power", "Schottky diode, 1 A 40 V (boost, motor flyback)", 2480, 3, "SS14; basic part"),
    ("analog", "24-bit simultaneous ADC, 4 channels", 882747, 1, "ADS131A04: 79 nV/rtHz input-referred at 3.3 V (TI Table 1), up to 128 kSPS, 16.384 MHz clock"),
    ("analog", "ADC clock, 16.384 MHz crystal", 21900468, 1, "3X016384UP, 16 pF, +/-10 ppm"),
    ("analog", "quad 12-bit DAC with I2C", 108207, 1, "MCP4728: LED currents, plate drive, device-current set"),
    ("analog", "op-amp, dual, 10 MHz, rail-to-rail", 398355, 2, "TLV9062: LED current sinks; device-under-test current source; TIAs on the heads use the same part"),
    ("analog", "op-amp, 36 V, 10 MHz, rail-to-rail output", 221351, 1, "OPA197: electrostatic plate driver on the 24 V rail"),
    ("analog", "analog switch, SPDT (LED gate)", 10426, 2, "SN74LVC1G3157: gates each LED's current reference from the PIO"),
    ("analog", "N-MOSFET, SOT-23 (motor drivers, LED sinks)", 20917, 4, "AO3400A; basic part"),
    ("analog", "N-MOSFET, DPAK (device-under-test current sink)", 99124, 1, "AOD4184A, 40 V 50 A; dissipation is the open point of WP3"),
    ("analog", "device-current shunt, 1 ohm 1206 1%", 17928, 1, "0.3 A gives 0.3 V (90 mW of 250 mW); read by the ADC; basic part"),
    ("analog", "device-current ballast, 4.7 ohm 2512 1 W", 25489, 1, "takes 1.3 V and 0.42 W of the 5 V off the sink MOSFET (WP3 thermal check); on the board, not the balance"),
    ("sensors", "temperature sensor, 16-bit digital", 699536, 1, "TMP117 on the main board; two more on the heads"),
    ("sensors", "3-axis accelerometer", 189624, 1, "LIS2DW12: floor motion and level"),
    ("sensors", "3-axis magnetometer (head board)", 404329, 1, "MMC5983MA, 18-bit, +/-8 G, I2C/SPI"),
    ("optical", "photodiode, SMD 4.4 x 3.9 mm (each head)", 145262, 2, "VBPW34S"),
    ("optical", "940 nm IR LED, 1206, 20 degrees (LED head)", 131280, 1, "IR26-21C"),
    ("connectors", "JST-SH 1 mm, 4-pin, SMD", 160404, 6, "LED heads x2 (3V3A, ground, LED sink, reference-photodiode output), photodiode heads x2 (3V3A, ground, output, ground), I2C heads x2"),
    ("connectors", "JST-SH 1 mm, 2-pin, SMD", 160402, 4, "plate, two motors, device leads"),
    ("connectors", "2.54 mm pin header, 1 x 2, SMD", 41417359, 8, "debug serial, SWD, spare I/O in pairs, test pads (Dupont wires plug on)"),
    ("indicators", "red LED, 0603", 2286, 2, "status; basic part"),
    ("passives", "resistor 1 kohm 0603 1%", 21190, 12, "basic"),
    ("passives", "resistor 10 kohm 0603 1%", 25804, 20, "basic"),
    ("passives", "resistor 5.1 kohm 0603 1% (CC pulldowns, I2C)", 23186, 6, "basic"),
    ("passives", "resistor 2.2 kohm 0603 1% (I2C pull-ups)", 4190, 2, "basic"),
    ("passives", "resistor 33 kohm 0603 1% (TIA feedback)", 4216, 2, "basic"),
    ("passives", "resistor 100 kohm 0603 1%", 25803, 8, "basic"),
    ("passives", "resistor 51 ohm 0603 1% (LED current sense)", 23197, 2, "basic; 1.02 V = 20 mA"),
    ("passives", "resistor 47 kohm 0603 1% (plate driver feedback)", 25819, 1, "basic; gain 1 + 47k/10k = 5.7"),
    ("passives", "resistor 0 ohm 0603", 21189, 4, "basic"),
    ("passives", "resistor 27 ohm 0805 (USB series)", 17594, 2, "extended; RP2040 USB needs 27 ohm in series"),
    ("passives", "capacitor 100 nF 0603 X7R", 14663, 40, "basic; decoupling at every supply pin"),
    ("passives", "capacitor 1 uF 0603 X5R", 15849, 10, "basic"),
    ("passives", "capacitor 10 uF 0805 X5R", 15850, 8, "basic"),
    ("passives", "capacitor 22 pF 0603 C0G (crystal loads)", 1653, 4, "basic"),
    ("passives", "capacitor 10 pF 0603 C0G (plate-driver feedback)", 1634, 1, "basic; removes an 8.6% overshoot in the WP3 simulation"),
    ("passives", "capacitor 1 nF 0603 X7R (TIA feedback, filters)", 1588, 6, "basic"),
    ("passives", "capacitor 4.7 uF 0805 X5R", 1779, 6, "basic"),
]

# boards and their order quantity: JLC's minimum for assembled prototypes is read at order time
BOARDS_PER_ORDER = 5
STOCK_FACTOR = 20  # stock must cover this many times the whole order's need


def lookup(lcsc):
    rows = jlc_query.search(lcsc=lcsc, min_stock=0, limit=1)
    return rows[0] if rows else None


def check():
    out = []
    for group, role, lcsc, qty, why in BOM:
        r = lookup(lcsc)
        out.append((group, role, lcsc, qty, why, r))
    return out


def machine_placed(lcsc):
    db = jlc_query.connect()
    row = db.execute("select assembly_process, assembly_mode, package from jlc_components where lcsc=?", (lcsc,)).fetchone()
    if row is None:
        return False
    proc, mode, pkg = row
    return (proc == "SMT" and mode == "smtWeld") or (proc is None and "插件" not in (pkg or ""))


def table(rows):
    lines = ["| Group | Role | LCSC | Type | Qty | In stock | Unit price (5) | Part | Why |", "|---|---|---|---|---|---|---|---|---|"]
    total = 0.0
    ext = set()
    for group, role, lcsc, qty, why, r in rows:
        if r is None:
            lines.append(f"| {group} | {role} | C{lcsc} | **not in the snapshot** | {qty} | | | | {why} |")
            continue
        total += qty * r["unit_price"]
        if r["type"] == "extended":
            ext.add(lcsc)
        lines.append(f"| {group} | {role} | C{lcsc} | {r['type']} | {qty} | {r['stock']:,} | ${r['unit_price']:.4f} | {r['mfr']} ({r['package']}) | {why} |")
    return "\n".join(lines), total, ext


def main():
    rows = check()
    text, total, ext = table(rows)
    n_parts = sum(q for _, _, _, q, _, _ in rows)
    summary = (
        f"{len(rows)} part numbers, {n_parts} components per board; {len(ext)} extended parts (JLC charges a per-part setup fee for each "
        f"extended part on an assembled order, amount to be read on jlcpcb.com at order time); parts cost about ${total:.2f} per board at the 5-piece "
        f"unit prices (components only: the board, assembly fee and shipping are extra)."
    )
    print(text)
    print("\n" + summary)
    if "--write" in sys.argv:
        head = (
            "# Candidate parts — instrument board (WP2)\n\nGenerated by `hardware/instrument/parts.py` from the JLC parts snapshot; do not edit by hand.\n"
            "Every part is machine-placed SMT in JLCPCB's library. Quantities are per main board and are fixed by the schematic (WP4).\n\n"
        )
        open(os.path.join(HERE, "parts.md"), "w").write(head + text + "\n\n" + summary + "\n")
        print("wrote parts.md")


if __name__ == "__main__":
    main()
