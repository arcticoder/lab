# Breadboard Wiring — accelerometer_interface

## Circuit overview

The GY-521 module (MPU-6050) already has its own 16-bit ADC, a 3.3V
regulator and I2C pull-ups on board, so this is a four-wire connection to
the Pico: power, ground, and the two I2C lines. `main.py` finds the
module, reads its ID, and checks that gravity comes out as 1g and the
readings are quiet.

**Equivalent to:** `accelerometer_interface.spice` (which models the I2C
bus timing and the supply, the only electrical things that can go wrong)

Powered from the Pico's 3V3(OUT) pin — the module draws ~4mA, far under
`psu_pico_rail`'s ~100mA budget.

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| GY-521 module (MPU-6050) | 8-pin header: VCC, GND, SCL, SDA, XDA, XCL, AD0, INT | 1 |
| Dupont M-M jumper | 12–20cm | 4 |

If the 8-pin header came loose in the bag rather than soldered on, solder
it to the module first (short side of the pins through the board, long
side up).

### If pins bridge during header soldering

Too much solder between adjacent pins doesn't clear by touching the iron
to the blob alone — that just spreads it further. Use the drag-soldering
technique instead, with the WorkPro 30W iron and rosin-core solder tube
already on hand:

1. Tin the iron tip with a fresh small bead of solder — the flux in the
   rosin core is what makes this work; a dry, oxidized tip drags nothing.
2. Rest the flat side of the tip against the bridged pins, angled
   30–45° away from the header.
3. In one continuous motion, drag the tip along the row and off the end
   of the header, onto a scrap surface or the tip cleaner — the molten
   solder follows the flux and rides off onto the tip instead of staying
   bridged.
4. Wipe the tip clean (damp sponge or brass wool) and re-tin it before
   each new pass; a dirty tip won't wick anything.
5. Recheck the row for bridging by eye (a bright light/magnifier helps)
   before wiring to the Pico.

If a bridge doesn't fully clear this way, solder wick is the fallback
(in the AliExpress cart as of 2026-09-24, not yet received): lay a length
over the bridge, press the iron on top, and it draws the solder up by
capillary action instead of dragging it off.

---

## Wiring steps

Seat the module in the breadboard so each pin has its own row, then
jumper from those rows to the Pico:

| Module pin | Pico pin | Physical pin |
|------------|----------|--------------|
| VCC | 3V3(OUT) | 36 |
| GND | GND | 38 |
| SDA | GP4 | 6 |
| SCL | GP5 | 7 |

Leave `XDA`, `XCL`, `AD0` and `INT` unconnected. (`AD0` floating puts the
module at address `0x68`; `main.py` also accepts `0x69` in case the board
ties it high.)

Keep the SDA/SCL jumpers as short as the layout allows: the bus timing in
`README.md` § Bus timing has margin for ordinary breadboard wiring but not
for a long loose jumper.

Run it with the Pico on USB power, module lying still on the bench:

```bash
mpremote run main.py
```

---

## Expected behavior

```
[PASS] module answers on I2C0: scan found ['0x68']
[PASS] WHO_AM_I: 0x68 (MPU-6050)
mean (g): x=+0.0.. y=-0.0.. z=+1.0..   sample rate ... Hz
[PASS] gravity magnitude at rest: |a| = 1.0..g
[PASS] noise at rest: worst per-axis std ~5mg
vibration RMS over this window: ~8 mg
```

Which axis carries the ~1g depends on how the module is lying; flat on
the bench with components up, it is Z.

| Result | Meaning |
|--------|---------|
| `scan found []` | Nothing on the bus: SDA/SCL swapped, VCC or GND not seated, or the header pins aren't making contact with the board |
| `WHO_AM_I` is `0x70`–`0x72` | Compatible/clone chip (the listing variant was "Compatible"); accelerometer registers are the same, the check passes with a note |
| `WHO_AM_I` unrecognized | Something answers at `0x68`/`0x69` but isn't an MPU-6050-family part |
| `gravity magnitude` fails | Module moved during the ~1s of sampling, or the accelerometer is out of its ±3% sensitivity spec |
| `noise at rest` fails | The bench is vibrating (a nearby fan, a hand on the table) — the reading is real, not a fault |
