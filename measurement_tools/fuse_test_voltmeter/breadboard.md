# Breadboard Wiring — fuse_test_voltmeter

**Just have one fuse and one battery in front of you right now?** Skip
this file and use [quickstart.md](quickstart.md) instead — it's the same
circuit with none of the batch/tier framing below. Come back here for the
500 mA fuse, testing more than one unit, or the PSU demo afterward.

## Circuit overview

This circuit has no PSU prerequisite of its own — the Pico is powered by
the PC's USB port, independent of anything it's probing. It gets used in
three stages, **in this order**:

1. **Self-check** — confirm the voltmeter itself reads correctly and its
   trip/reset logic fires, using a plain jumper wire instead of a fuse.
   No fuse, no PSU.
2. **Test** — bench-test each polyfuse from the batch (20× RXEF005, 20×
   RXEF050) on a minimal standalone jig — a battery, the fuse under test,
   and a load resistor — to sort good units from faulty ones. Still no
   PSU: this jig is *not* `psu_ultralow_v1` or `psu_low_v2`, just enough
   circuit to stress one fuse at a time.
3. **Demo** — once a specific fuse has passed step 2, build
   [psu_ultralow_v1](../../power_supplies/psu_ultralow_v1/) or
   [psu_low_v2](../../power_supplies/psu_low_v2/) per its own
   `breadboard.md` with that confirmed-good fuse installed, and probe it
   the same way. This step confirms the PSU's own wiring around the fuse
   — it is a demonstration, not a test of the fuse component, which was
   already proven in step 2.

Build order is voltmeter → test → PSU → demo. Not PSU-first: a fuse needs
to be known good *before* it's wired into a PSU, not after.

**Equivalent to:** `fuse_test_voltmeter.spice`

---

## Parts required

### Steps 0–1 (self-check + bench test) — no PSU needed

| Component | Value | Quantity |
|-----------|-------|----------|
| Raspberry Pi Pico | RP2040 | 1 |
| Micro USB cable | data-capable, to PC | 1 |
| Dupont M-M jumper | 22cm | 5 (2 probe, 3 arm switch) |
| Slide switch (SPDT) | — | 1 — arm/disarm signal to GP15, see "Wire the arm switch" below |
| AA battery holder (single-cell) | — | 1 (RXEF005 jig, 1.5V) or 2 in series (RXEF050 jig, 3.0V) |
| AA battery | fresh | 1–2, matching holder count above |
| Test load resistor, RXEF005 jig | 10 Ω, 1/4W (kit-standard) | 1 |
| Test load resistor, RXEF050 jig | 10 Ω 1/4W ×4, wired as a 2-series × 2-parallel bank (10 Ω equivalent) | 4 |
| Plain jumper wire | — | 1 (stands in for the fuse during self-check) |
| Polyfuse under test | RXEF005 or RXEF050 | 1 at a time, swapped in from the batch of 20 each |

### Step 2 (demo) — after a PSU is built

| Component | Value | Quantity |
|-----------|-------|----------|
| psu_ultralow_v1 or psu_low_v2 | built with a confirmed-good fuse from step 1 | 1 |
| Raspberry Pi Pico + jumpers | same as above | — |

No new parts beyond what's already in the psu_ultralow_v1 / psu_low_v2
parts lists — the same 10 Ω value is reused for both fuse ratings instead
of ordering a dedicated value. **Wattage matters here**: the RXEF050 jig (3.0V across
10 Ω, cold) dissipates ~0.82W total — a single kit resistor (1/4W /
0.25W, see `pico/docs/inventory.md`; the kit has no higher-wattage part)
would run at over 3x its rating and can overheat, drift, or fail open,
which would read as a false trip. The kit-only fix is a **2-series ×
2-parallel bank of four 10 Ω 1/4W resistors** (two 20 Ω series branches in
parallel), which nets the same 10 Ω equivalent load while each individual
resistor only sees ~0.2W — within its 1/4W rating. The RXEF005 jig doesn't
need this: its single 10 Ω resistor sees ~0.2W (1.5V cold), already under
1/4W, and the fuse self-trips within seconds anyway, limiting exposure.
See `smoke_test.py`, which checks per-resistor power against this actual
kit-part rating for both jigs.

---

## Wiring steps

### 0. Plug the Pico into the PC

Micro USB cable, Pico to PC. This powers the Pico and gives you the serial
connection `main.py` prints to — no separate power source for the Pico.

### 0b. Wire the arm switch

`main.py` reads GP15 as a digital input with no pull resistor, so it must
be wired before any run of the script — an unconnected GP15 floats and
produces unpredictable ARMED/DISARMED readings. Wire this once; it's
reused across every stage below and isn't part of the battery power path.

| From | To | Wire |
|------|----|------|
| Switch pin 2 (middle/common) | Pico GP15 | Dupont M-M jumper |
| Switch pin 1 | Pico GND (any pin) | Dupont M-M jumper |
| Switch pin 3 | Pico 3V3(OUT) | Dupont M-M jumper |

Run `mpremote run main.py` and slide the switch — one direction prints
`-- ARMED --`, the other `-- DISARMED --`. Note which physical direction
is which (no printed markings on this part). Leave it DISARMED whenever
you're inserting or removing a battery; flip to ARMED only once the
circuit is settled and you're actually watching for a trip. Voltage keeps
streaming in both states — only trip/reset detection and the onboard LED
are gated on ARMED.

### 1. Self-check the voltmeter (no fuse yet)

Build the bare jig with a plain jumper wire in place of a fuse:
`battery → jumper wire → 10 Ω load resistor network → GND`. For the
RXEF005 (1.5V) jig, that "network" is the single 10 Ω resistor from the
parts table. For the RXEF050 (3.0V) jig, build the 2-series × 2-parallel
bank of four 10 Ω resistors described above first — self-check the bank
itself, not a single resistor, since that's what the bench test in step 2
will actually be probing.

| From | To | Wire |
|------|----|------|
| Pico GP26 | Load network's jumper-side node (the node between the jumper and the resistor/bank) | Dupont M-M jumper |
| Pico GND | Load network's ground-side node | Dupont M-M jumper |

Run `main.py` (`mpremote run main.py`), slide the arm switch to **ARMED**
once the reading looks settled, and check:

- Cold reading is close to the battery's fresh voltage (a plain wire adds
  ~0 Ω, so this should track the SPICE cold-state numbers below).
- Deliberately short the load network's two end nodes together with a
  spare jumper wire seated in the same breadboard rows as those nodes
  (RXEF005: the resistor's two rows; RXEF050: the bank's two outer rows —
  not any single resistor's leads within the bank) rather than
  hand-holding two wire tips together, which is a spotty, easy-to-fumble
  connection — the reading should collapse toward 0V, `main.py` should
  print `*** FUSE TRIPPED ***`, and the onboard LED should light.
- Remove the short — reading should recover immediately, `main.py` should
  print `*** fuse reset ***`, LED off.

If any of this doesn't happen, the problem is the Pico wiring or firmware
— fix that before testing any real fuse. A miswired probe can make a good
fuse look bad or a bad fuse look good.

### 2. Bench-test the polyfuse batch

With the self-check passing, swap the plain jumper for one polyfuse at a
time from the batch:

| From | To | Wire |
|------|----|------|
| Pico GP26 | Load network's fuse-side node (the node between the fuse and the resistor/bank) | Dupont M-M jumper |
| Pico GND | Load network's ground-side node | Dupont M-M jumper |

For **RXEF005** units, use the 1×AA (1.5V) jig with the single 10 Ω
resistor. For **RXEF050** units, use the 2×AA-in-series (3.0V) jig with the
2-series × 2-parallel bank of four 10 Ω resistors — both networks are 10 Ω
equivalent, so the SPICE predictions below apply to either one, but the
RXEF050 jig needs the bank specifically (see "Wattage matters here"
above); a single 1/4W resistor there is not safe.

For each fuse under test:

0. Swap the fuse in with the arm switch **DISARMED**, then slide to
   **ARMED** once the reading looks settled — otherwise the initial
   zero-to-cold-voltage transition can print as a spurious trip/reset.
1. Note the cold reading — should be close to the SPICE prediction for
   that tier (see "Simulate" in [README.md](README.md)). For the RXEF005
   tier this reading may only last a few seconds before the fuse trips on
   its own, since the plain 10 Ω load already draws ~3x its rated current
   — that's expected, not a sign of a problem.
2. Short the load network's two end nodes with a spare jumper wire seated
   in the same breadboard rows as those nodes (the single resistor's rows
   for RXEF005, or the bank's two outer rows for RXEF050 — not a single
   resistor within the bank; don't hand-hold wire tips against the leads,
   see step 1's short instruction above) to force a much larger
   overcurrent — expect the voltage to collapse and `main.py` to print
   `*** FUSE TRIPPED ***` within about a second. Do this regardless of
   whether the fuse already tripped on its own in step 1 — it's the
   deterministic version of the same check.
3. Remove the short, wait ~2 minutes for the polyfuse to cool, and confirm
   full reset — voltage and LED both back to normal, `*** fuse reset ***`
   printed.
4. **Pass**: trips promptly, resets fully, cold reading matches
   prediction. **Fail**: doesn't trip, doesn't reset, or reads far off the
   prediction — discard the unit; don't wire it in front of an LED.
5. Slide back to **DISARMED** before pulling this fuse for the next one.

Repeat per unit across the batch. Keep a simple tally of which units
passed — those are the only ones that go into a PSU build in step 3.

### 3. Build the PSU, then demo the confirmed-good fuse

Only after step 2 has produced at least one confirmed-good fuse for the
tier you're building:

1. Build [psu_ultralow_v1](../../power_supplies/psu_ultralow_v1/) or
   [psu_low_v2](../../power_supplies/psu_low_v2/) per its own
   `breadboard.md`, installing that specific confirmed-good fuse:
   `battery → fuse → 10 Ω load resistor network → ground`. Reuse the same
   network from step 2 — the single 10 Ω resistor for RXEF005, or the
   2-series × 2-parallel bank of four for RXEF050 (same wattage reasoning
   applies here; it's the same physical resistor(s), not a fresh part).
2. Wire the Pico the same way as step 2, but clipped onto the built PSU's
   own load-network node instead of the bench jig's:

   | From | To | Wire |
   |------|----|------|
   | Pico GP26 | PSU's load network's fuse-side node | Dupont M-M jumper |
   | Pico GND | PSU's load network's ground-side node | Dupont M-M jumper |

   The arm switch from step 0b stays wired as-is — it's on the Pico side,
   not the PSU, so nothing about it changes for the demo. Same DISARMED/
   ARMED discipline applies: disarm before seating the fuse or touching
   the battery, arm once settled and watching for a trip.

3. Run the same short/reset check as step 2. Since the fuse itself was
   already proven good, this run is a demonstration that the PSU's own
   wiring around the fuse is correct — not a re-test of the fuse.

Either use a spare GND pin on the Pico's header, or share the circuit's own
ground rail — both are the same reference as long as the Pico and the
circuit under test share a common ground point.

---

## Expected behavior

**RXEF005 tier (1.5V, 50 mA fuse):** ~1.43V at the probe point under the
plain 10 Ω load itself — note that this is already ~150 mA, 3x the fuse's
rated current, so a good unit may begin heating and trip on its own within
a few seconds of being loaded, before you ever short anything. Treat that
as expected, not a sign of a bad fuse or bad wiring. Shorting the load
resistor (step 2 below) isn't required to see a trip — it forces a much
larger overcurrent (near-dead-short across the battery/fuse) that
guarantees a fast, unambiguous trip regardless of unit-to-unit tolerance,
which is why the procedure below still calls for it as the deliberate
test step. Either way, voltage collapses to ~0.14V once tripped, and
`main.py` prints `*** FUSE TRIPPED ***` and lights the Pico's onboard LED.
Remove the short (if applied) and wait ~2 minutes for the polyfuse to cool
and reset; voltage should climb back to ~1.43V and the onboard LED turns
off.

**RXEF050 tier (3.0V, 500 mA fuse):** same test, ~2.86V normal, ~0.27V
tripped, forcing current sits right at the 500 mA threshold rather than 3x
over it, so the trip may take longer.

These numbers apply identically whether you're running the bench jig
(step 2) or the demo in a built PSU (step 3) — the electrical topology
across the probe point is the same either way. If a fuse doesn't reset
after cooling, or the tripped-state voltage doesn't drop the way the SPICE
numbers predict, don't trust it near an LED — see [README.md](README.md)
for the full test procedure.
