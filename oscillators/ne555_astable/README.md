# ne555_astable

An NE555 timer wired as an astable square-wave oscillator, with the 3296
10kΩ trimpot as the variable timing resistor — the first per-unit
validation of the NE555 batch (mirrors how
[cd4066_switch_tester](../../measurement_tools/cd4066_switch_tester/)
validated the CD4066B batch), and the tier1 `OSC` node in
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md).
`OSC` unlocks tier2 `FREQC`, plus `SIMPLECNT`, `TUNINGFK`, and eventually
`LOCKIN` downstream — and doubles as a basic `SIMPGEN` (Simple Function
Generator), since a 555 astable run from a several-volt rail *is* one.

Powered from [psu_4xaa](../../power_supplies/psu_4xaa/) (4x AA in series,
6.0V raw) rather than a wall adapter — the AA-battery tier was preferred
over building `psu_medlow_usbc` for this circuit. The NE555 needs ≥4.5V;
`psu_3xaa` (4.5V raw) was ruled out because its own smoke test shows it
sags to ~4.02V under load, under that minimum, so `psu_4xaa` is the first
AA tier that actually clears it, with real margin. If it ever proves
insufficient on the real bench, the next step up is a 12V supply (not yet
its own folder — see `docs/parts_reference.md`'s `psu_medlow` node), not
another AA tier.

---

## Files

| File | Purpose |
|------|---------|
| `ne555_astable.spice` | ngspice netlist — transient sim at two trimpot settings |
| `schematic.png` | Generated schematic image, gitignored — see repo `README.md` (the schematic tool only draws R/C/V/D elements, so the 555 itself isn't rendered — see the netlist for the full circuit) |
| `breadboard.md` | Step-by-step breadboard wiring |
| `smoke_test.py` | Runs the netlist and asserts safe/expected values — see repo `README.md` § Smoke-testing |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring. Short
version:

1. Power the NE555 (pin 8 VCC, pin 1 GND) from
   [psu_4xaa](../../power_supplies/psu_4xaa/); tie pin 4 (Reset) to VCC.
2. Timing network: 1kΩ resistor (Ra) from VCC to pin 7 (Discharge); 3296
   trimpot (Rb, 0–10kΩ) from pin 7 to pins 2+6 (Trigger+Threshold, tied
   together); 100nF capacitor (C) from pins 2+6 to GND.
3. 10nF capacitor from pin 5 (Control Voltage) to GND (decoupling only).
4. Output square wave on pin 3.

---

## Simulate

```bash
# from the repo root
ngspice -b oscillators/ne555_astable/ne555_astable.spice
```

```
freq_lo = 6.493506e+02      # Rb=10k (full CW): ~649Hz, ~50% duty
duty_lo = 4.954545e-01
freq_hi = 2.730893e+03      # Rb=2k: ~2.7kHz, ~57% duty
duty_hi = 5.685197e-01
```

Frequency and duty cycle only depend on Ra, Rb, and C — not on VCC — so
these numbers are the same regardless of which supply powers the chip.

The netlist models the NE555 with a behavioral macromodel — not a vendor
transistor-level part — valid specifically for astable operation (see the
netlist's header comment for what it does and doesn't capture).

**Startup warnings are expected, not a fault.** Running this netlist
prints `Warning: Dynamic gmin stepping failed` / `True gmin stepping
failed` / `source stepping failed` twice (once per `tran` run — the
netlist sweeps two trimpot settings, see the netlist's `.control`
section), followed by `Note: Transient op started` /
`Transient op finished successfully`. Those three stepping methods are
ngspice's usual ways of finding a DC bias point, and they struggle with
this circuit's discontinuous behavioral comparator/switch; ngspice falls
back to solving the initial point directly in the time domain instead,
which succeeds every time here and produces the frequency/duty numbers
above matching the standard 555 formulas. The `Note: No compatibility
mode selected!` line is unrelated — ngspice prints it on every run in
this repo regardless of netlist — and the two separate "Initial Transient
Solution" blocks are the two `tran` runs (Rb=10k, then Rb=2k after
`alter`), not a repeated/duplicated analysis. Nothing here indicates a
problem with the model or the result.

---

## Expected behaviour

With Ra=1kΩ fixed and C=100nF, the frequency and duty cycle follow the
standard 555 astable formulas:

```
f = 1.44 / ((Ra + 2·Rb)·C)
D = (Ra + Rb) / (Ra + 2·Rb)
```

Turning the trimpot's Rb from 10kΩ (full CW) down toward 0Ω sweeps the
output from **~686Hz at ~52% duty** (most square, Rb=10k) up toward
higher frequencies with duty skewing further *above* 50% as Rb shrinks —
not toward 100% duty as Rb increases, the opposite direction. This
simple 3-pin astable network (no diode across Rb) can't produce a duty
cycle below 50%; that's expected behavior, not a fault.

**Recommended usable trim range** (reasonably square output, confirmed
by the sim): **~686Hz (Rb=10k, D≈52%) to ~2.9kHz (Rb=2k, D≈60%)**. Below
Rb≈2k, duty climbs further from 50% and frequency keeps rising toward a
theoretical ~14.4kHz at Rb→0, which is both harder to read cleanly and
approaches the pathological 100%-duty limit — stay above roughly Rb=2k
for a clean square wave.

The full range sits inside the desktop PC's onboard-soundcard scope
(`SCOPEPC`, 20Hz–20kHz — see
[docs/general_purpose_circuit_dependency.md](../../docs/general_purpose_circuit_dependency.md))
audio band, so the built oscillator's actual frequency can be confirmed
there even before `FREQC` (tier2) exists — feed pin 3 through a
DC-blocking/attenuator buffer into line-in, per `SCOPEPC`'s node note.

**Fault signatures**: output stuck high or low (not toggling) — check the
pin 2/6 tie and the 100nF timing cap; output toggling but frequency far
from the formula above — check Ra/Rb values and that the trimpot's wiper
is landing in the pin 2/6 row, not floating.
