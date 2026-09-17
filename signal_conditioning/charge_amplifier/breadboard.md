# Breadboard Wiring — charge_amplifier

## Circuit overview

A 12mm piezo disc (charge-output transducer) feeding one channel of a
TL082 wired as an inverting charge amplifier: the piezo injects charge
into the inverting input, a feedback capacitor (`Cf`) integrates it into
a voltage, and a large parallel bias resistor (`Rf_bias`) prevents the
output from drifting to a rail. The non-inverting input is biased to
VCC/2 so the output can swing both directions around that midpoint —
needed because a piezo tap produces both a compression and a release
transient, opposite in sign.

**Equivalent to:** `charge_amplifier.spice`

Powered from [psu_pico_rail](../../power_supplies/psu_pico_rail/) — see
`README.md` for why (same ADC-safety rationale as
`electric_field_probe`).

---

## Parts required

| Component | Value | Quantity |
|-----------|-------|----------|
| TL082 | JFET-input dual op-amp, DIP-8 | 1 |
| Piezo element | 12mm disc | 1 |
| Resistor | 1 MΩ (bias divider, `R1`/`R2`) | 2 |
| Resistor | 1 MΩ (feedback, `Rf_bias`) | 1 |
| Ceramic capacitor | 10 nF (feedback, `Cf`; EIA code `103`) | 1 |
| Dupont M-M jumper (red) | 12–20cm | 1 |
| Dupont M-M jumper (black) | 12–20cm | 2 |

The 10nF cap is from the multilayer ceramic assortment already on hand
(see `docs/parts_reference.md#multilayer-ceramic-capacitor-assortment-50v`
for the EIA-code decode table) — no new capacitor needed.

---

## TL082 pinout (DIP-8, per `lab/docs/parts_reference.md`)

| Pin | Function | Pin | Function |
|-----|----------|-----|----------|
| 1 | Output 1 | 8 | V+ |
| 2 | Inverting input 1 (−) | 7 | Output 2 (unused) |
| 3 | Non-inverting input 1 (+) | 6 | Inverting input 2 (unused) |
| 4 | V− | 5 | Non-inverting input 2 (unused) |

Only channel 1 (pins 1–3) is used; leave channel 2 (pins 5–7)
unconnected. V− (pin 4) goes to GND — single-supply build.

## Piezo element pinout

Two terminals, no fixed polarity convention (unlike a diode) — either
lead can go to either node.

**The bare disc has no pre-attached leads.** Before it can plug into
the breadboard, solder a short lead onto each of its two contacts (the
center ceramic face and the metal backing plate). **Use rosin flux
(paste or pen) and a quick, low-heat touch** — a 2026-09-16 attempt
without flux destroyed a unit: the ceramic disc conducts heat poorly,
so without flux to help the joint wet quickly, the extra dwell time
needed cracks the ceramic or depoles the piezo effect before the solder
takes. See
[parts_reference.md#piezo-element-12mm-disc](../../docs/parts_reference.md#piezo-element-12mm-disc).

---

## Wiring steps

### 1. Power the TL082

| From | To | Wire |
|------|----|------|
| Pico 3V3(OUT) pin | TL082 pin 8 (V+) | Red Dupont jumper |
| Pico GND pin | TL082 pin 4 (V−/GND) | Black Dupont jumper |

### 2. Wire the bias divider (non-inverting input)

- R1 (1 MΩ): one leg to the same row as TL082 pin 8 (V+/3.3V), other leg
  to a fresh row — call this the BIAS row.
- R2 (1 MΩ): one leg to the BIAS row, other leg to GND.
- Jumper the BIAS row to TL082 pin 3 (non-inverting input).

### 3. Wire the piezo into the inverting input

Connect one piezo lead to TL082 pin 2 (inverting input) — call this the
VIRT row. Connect the other piezo lead to GND.

### 4. Wire the feedback network

Between the VIRT row and TL082 pin 1 (output), place **both** in
parallel: the 10nF ceramic cap (`Cf`) and a 1MΩ resistor (`Rf_bias`).
Both components' legs land in the same two rows (VIRT and OUT) — this is
what makes them parallel, not the order they're inserted.

### 5. Take the output

Output is TL082 pin 1. Wire it to a Pico ADC-capable GPIO (e.g. GP28 —
GP26/GP27 may already be in use by `ne555_astable`/`electric_field_probe`
if those are on the same breadboard).

---

## Expected behavior

At rest, the output should read close to ~1.65V (VCC/2) — see
`README.md`'s simulated bias math. Tapping or flexing the piezo should
produce a brief transient blip away from 1.65V (direction depends on
whether the tap compresses or releases the disc), settling back toward
1.65V over roughly a 10ms time constant (`Rf_bias * Cf` — see
`README.md`'s corner-frequency note) once the mechanical event ends. This
is fast enough that averaging with `raw_voltage_probe`'s technique will
mostly miss it — use `main.py` (which reads and prints as fast as the
Pico ADC allows) and watch for the transient live, or use
`oscillation_probe`'s burst-sampling approach if a cleaner capture is
needed. If the reading never moves regardless of tapping the piezo,
check TL082 power (pins 8/4), that `Cf`/`Rf_bias` are actually in
parallel (not in series, and not accidentally only one of the two
present), and that both piezo leads are making contact.
