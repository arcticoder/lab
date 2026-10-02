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

Solder bridging adjacent header pins is cleared with desoldering wick
(braid), which draws the excess up by capillary action. Wick is in the
AliExpress cart (see `TODO-arcticoder.md`'s "Next order"); this step waits
for it to arrive.

1. Lay a ~1cm length of the braid flat over the bridged pins.
2. Press the iron tip on top of the braid, not on the pins directly, for
   2–3 seconds until the solder wicks into the braid.
3. Lift the braid and the iron together while the solder is still molten,
   so the braid doesn't freeze onto the board. Cut off the used,
   solder-filled end before the next pass.
4. Recheck the row by eye (a bright light or magnifier helps) before
   wiring to the Pico.

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
