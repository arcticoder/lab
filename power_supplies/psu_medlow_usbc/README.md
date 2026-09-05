# psu_medlow_usbc

5V USB-C wall adapter, a 500 mA polyfuse, and a 100 nF bypass cap to smooth
adapter ripple. No local regulation — the wall adapter already regulates to
5V, so this is fuse + bypass only *if VBUS actually comes up* — see Status
below.

**Status: incomplete / unverified — do not assume this powers on as
drawn.** The USB-C breakout in the parts list (`TYPE-C Female Test Board`,
see [pico/docs/inventory.md](../../../pico/docs/inventory.md)) is a
**passive** breakout — it only routes the receptacle's pins (`CC2, D+, D-,
SBU1, SBU2, CC1, VBUS, GND`) out to 2.54mm pads; it has no PD controller
IC. A USB-C *source* only drives VBUS once it sees a valid sink
termination on CC1/CC2 (5.1kΩ pull-downs to GND, for default 5V/up to
1.5–3A); a PD-only charger with no legacy fallback may output nothing at
all without that termination, and any voltage above the negotiated default
(or a specific voltage from a multi-voltage PD adapter) needs active BMC
negotiation from a PD sink controller IC (e.g. STUSB4500, CH224,
TPS65987D) plus a downstream buck converter if the target rail differs
from what gets negotiated. Whether this specific breakout board has CC
pull-down resistors already wired is **unconfirmed** — see
`docs/parts_reference.md` § USB-C 16-pin test breakout board ("verify
values with a meter before assuming a specific standard resistance"). The
`.spice` netlist and `smoke_test.py` below model only the downstream
fuse+bypass stage on the assumption that VBUS is already present — they do
not, and cannot, verify CC/PD negotiation, and `smoke_test.py` fails
pending that verification.

Spec: 5V USB path of the medium-low tier. See
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md)
(`psu_medlow` node).

---

## Files

| File | Purpose |
|------|---------|
| `psu_medlow_usbc.spice` | ngspice netlist — operating point + load sweep |
| `schematic.png` | Generated schematic image, gitignored — see repo `README.md` (note: the schematic tool only draws V/R/D elements, so the bypass cap isn't rendered — see the netlist for the full circuit) |
| `breadboard.md` | Step-by-step breadboard wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. USB-C breakout board (breadboard-compatible pin breakout, passive — no
   PD negotiation) fed from any USB-C wall adapter. **Unverified whether
   VBUS actually comes up** — see Status above; confirm with a meter
   before wiring the rest, and add CC1/CC2 termination or a PD sink
   controller IC if it doesn't.
2. 500 mA polyfuse (Littelfuse RXEF050) in series on VBUS.
3. 100 nF ceramic bypass cap from the fuse output to ground.
4. Output taken from the bypass cap node (+) and adapter GND (−).

---

## Simulate

```bash
# from the repo root
ngspice -b psu_medlow_usbc/psu_medlow_usbc.spice
```

The first block prints the operating point at the nominal 10 Ω load
(~500 mA — right at the polyfuse trip point by design). The second block
sweeps the load from 5 Ω to 50 Ω.

---

## Expected behaviour

```
V_out ≈ 5.0V × Rload / (Rload + Rfuse)
```

At Rload = 10 Ω: **V_out ≈ 4.76 V, I ≈ 476 mA** — close to the fuse's rated
threshold, which is intentional: this load point exercises the fuse near
its trip boundary. Use a higher Rload (lighter load) for normal operation.
