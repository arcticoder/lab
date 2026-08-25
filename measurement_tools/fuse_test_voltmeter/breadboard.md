# Breadboard Wiring — fuse_test_voltmeter

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
| Dupont M-M jumper | 22cm | 2 |
| AA battery holder (single-cell) | — | 1 (RXEF005 jig, 1.5V) or 2 in series (RXEF050 jig, 3.0V) |
| AA battery | fresh | 1–2, matching holder count above |
| Test load resistor | 10 Ω, **≥1W** | 1 |
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
10 Ω, cold) dissipates ~0.82W in the load resistor — a standard 1/4W or
1/2W part will run hot or fail. Use a ≥1W resistor (or a higher resistance
at correspondingly lower current) for this jig; see `smoke_test.py`.

---

## Wiring steps

### 0. Plug the Pico into the PC

Micro USB cable, Pico to PC. This powers the Pico and gives you the serial
connection `main.py` prints to — no separate power source for the Pico.

### 1. Self-check the voltmeter (no fuse yet)

Build the bare jig with a plain jumper wire in place of a fuse:
`battery → jumper wire → 10 Ω load resistor → GND`.

| From | To | Wire |
|------|----|------|
| Pico GP26 | Load resistor's jumper-side leg (the node between the jumper and the resistor) | Dupont M-M jumper |
| Pico GND | Load resistor's ground-side leg | Dupont M-M jumper |

Run `main.py` (`mpremote run main.py`) and check:

- Cold reading is close to the battery's fresh voltage (a plain wire adds
  ~0 Ω, so this should track the SPICE cold-state numbers below).
- Deliberately touch the resistor's two leads together (short it) — the
  reading should collapse toward 0V, `main.py` should print
  `*** FUSE TRIPPED ***`, and the onboard LED should light.
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
| Pico GP26 | Load resistor's fuse-side leg (the node between the fuse and the resistor) | Dupont M-M jumper |
| Pico GND | Load resistor's ground-side leg | Dupont M-M jumper |

For **RXEF005** units, use the 1×AA (1.5V) jig. For **RXEF050** units, use
the 2×AA-in-series (3.0V) jig — same 10 Ω load resistor either way.

For each fuse under test:

1. Note the cold reading — should be close to the SPICE prediction for
   that tier (see "Simulate" in [README.md](README.md)).
2. Short the load resistor to force an over-threshold current — expect the
   voltage to collapse and `main.py` to print `*** FUSE TRIPPED ***`
   within about a second.
3. Remove the short, wait ~2 minutes for the polyfuse to cool, and confirm
   full reset — voltage and LED both back to normal, `*** fuse reset ***`
   printed.
4. **Pass**: trips promptly, resets fully, cold reading matches
   prediction. **Fail**: doesn't trip, doesn't reset, or reads far off the
   prediction — discard the unit; don't wire it in front of an LED.

Repeat per unit across the batch. Keep a simple tally of which units
passed — those are the only ones that go into a PSU build in step 3.

### 3. Build the PSU, then demo the confirmed-good fuse

Only after step 2 has produced at least one confirmed-good fuse for the
tier you're building:

1. Build [psu_ultralow_v1](../../power_supplies/psu_ultralow_v1/) or
   [psu_low_v2](../../power_supplies/psu_low_v2/) per its own
   `breadboard.md`, installing that specific confirmed-good fuse:
   `battery → fuse → 10 Ω load resistor → ground`.
2. Wire the Pico the same way as step 2, but clipped onto the built PSU's
   own load-resistor node instead of the bench jig's:

   | From | To | Wire |
   |------|----|------|
   | Pico GP26 | PSU's load resistor's fuse-side leg | Dupont M-M jumper |
   | Pico GND | PSU's load resistor's ground-side leg | Dupont M-M jumper |

3. Run the same short/reset check as step 2. Since the fuse itself was
   already proven good, this run is a demonstration that the PSU's own
   wiring around the fuse is correct — not a re-test of the fuse.

Either use a spare GND pin on the Pico's header, or share the circuit's own
ground rail — both are the same reference as long as the Pico and the
circuit under test share a common ground point.

---

## Expected behavior

**RXEF005 tier (1.5V, 50 mA fuse):** steady ~1.43V at the probe point
under normal 10 Ω load. Short the load resistor to force ~150 mA (3x trip
threshold) — voltage collapses to ~0.14V within about a second as the fuse
trips, and `main.py` prints `*** FUSE TRIPPED ***` and lights the Pico's
onboard LED. Remove the short and wait ~2 minutes for the polyfuse to cool
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
