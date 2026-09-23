# capacitance_bridge

A Pico-driven RC charge-time capacitance meter: a known reference
resistor (`Rref`) and an unknown capacitor (`Cx`) form a divider, a GPIO
pin drives the charge, and an ADC pin times how long it takes to reach
63.2% of the drive voltage (one RC time constant) — solving `Cx = t /
Rref` from that. This is the tier3 `CAPBRIDGE` node in
[general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md).

This substitutes a known-reference-vs-unknown **timing** comparison for a
classical 4-arm AC capacitance bridge (which needs an AC excitation
source and a phase-sensitive null detector — not available on this
bench). That's the same kind of substitution
[resistance_measurement](../resistance_measurement/) already made for the
tier3 `OHMMETER` node (a DC voltage divider instead of a literal 4-wire
Kelvin bridge) — see
[docs/kb/todo_list_conventions.md](../../docs/kb/todo_list_conventions.md).

Powered from the Pico's own GPIO/3V3 — no separate PSU needed.

---

## Files

| File | Purpose |
|------|---------|
| `capacitance_bridge.spice` | ngspice netlist — RC charge transient, times the 63.2% crossing |
| `schematic.png` | Generated schematic image (gitignored — see repo `README.md`) |
| `breadboard.md` | Step-by-step wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |
| `main.py` | MicroPython — streams real-hardware capacitance readings continuously |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Pico GP14 → `Rref` (100 kΩ) → junction row.
2. Junction row → `Cx` (positive lead) → `Cx` (negative lead) → GND.
3. Pico GP26 (ADC0) → junction row.

---

## Simulate

```bash
# from the repo root
ngspice -b measurement_tools/capacitance_bridge/capacitance_bridge.spice
```

```
--- capacitance_bridge: time to 63.2% of Vin, and derived Cx ---
t63 = 9.996724e-01
c_measured = 9.996724e-06
```

At the netlist's 10µF design point, `t63 ≈ 1.0s` and the derived
capacitance recovers the nominal 10µF within simulation precision.

---

## Range

This timing technique's usable range is bounded by what a Pico polling
loop (`main.py` samples every ~1ms) can actually resolve, at both ends:

| `Cx` | `t = Rref × Cx` at Rref=100kΩ | Usable? |
|------|-------------------------------|---------|
| 10 pF (ceramic assortment) | ~1 µs | No — far below the ~1ms sample interval |
| 100 nF (ceramic assortment) | ~10 ms | Marginal — only a handful of samples across the whole charge |
| 1 µF (electrolytic kit) | ~0.1 s | Yes — ~100 samples |
| 10 µF (electrolytic kit) | ~1.0 s | Yes — this circuit's design/test point |
| 470 µF (electrolytic kit) | ~47 s | Yes, slow — `main.py`'s `TIMEOUT_S` (60s) covers it with margin |

**This build targets the aluminum electrolytic capacitor kit (1µF–470µF,
see `docs/inventory.md`), not the pF/nF multilayer ceramic assortment.**
Measuring a ceramic-range value with this circuit would need a much
smaller `Rref` and a hardware timer/capture-based timing method instead
of ADC polling — not what's built here.

---

## Expected behaviour

Driving the junction HIGH from a fully-discharged `Cx` produces a
standard exponential charge curve, `Vc(t) = Vin(1 - e^{-t/RC})`, crossing
63.2% of `Vin` at exactly `t = Rref × Cx`. The netlist's `.meas` statement
finds that crossing directly; `main.py` finds the same crossing on real
hardware by polling the ADC.

---

## Validation

`main.py` runs continuously, each loop iteration discharging `Cx`
(polling until its voltage drops below 2% of `Vin`, not a fixed sleep —
important for the largest kit values, whose discharge takes just as long
as their charge), then timing a fresh charge to 63.2%:

```bash
mpremote run main.py
```

Swap in different `Cx` values from the electrolytic kit between runs and
confirm the printed µF figure lands within the kit's own ±20% tolerance
of the value marked on the part. A result of "No 63.2% crossing" means
either `Cx` is larger than the range table above supports at this `Rref`,
or the junction isn't actually wired to both `Rref` and `Cx` (open
circuit).

**A result stuck near 0.00–0.01µF regardless of which `Cx` is installed**
(seen 2026-09-22 with a 33µF `Cx`) points the other way: `Rref`'s far
lead isn't actually making contact at the junction (e.g. resting next to
the hole rather than in it, easy to miss by eye on a crowded breadboard),
which leaves the ADC pin floating and picking up noise/coupling that
crosses both thresholds almost instantly. Reseat that lead fully into
the same hole as the ADC probe wire and `Cx`'s positive lead and rerun —
don't treat this as a `main.py` bug without checking the physical joint
first.

**Physically assembled and bench-tested, PASS (2026-09-22).** After
reseating `Rref`'s lead per the above and swapping `Cx` for a 47µF (25V)
electrolytic, three consecutive `mpremote run main.py` runs read
48.87µF, 47.75µF, and 47.64µF — all within the kit's own ±20% tolerance
of the 47µF nominal, and consistent with each other run to run. Moved to
`README.md`'s "built & bench-tested" table.
